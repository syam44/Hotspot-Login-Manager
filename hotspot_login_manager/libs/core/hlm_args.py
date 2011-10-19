# -*- coding:utf-8 -*-
#
# hotspot-login-manager
# https://github.com/syam44/Hotspot-Login-Manager
#
# Distributed under the GNU General Public License version 3
# https://www.gnu.org/copyleft/gpl.html
#
# Authors: syam (aks92@free.fr)
#
# Description: Command-line arguments parser.
#


#-----------------------------------------------------------------------------
from optparse import OptionParser, OptionGroup, Values
import re
import sys
#
from hotspot_login_manager.libs.core import hlm_application
from hotspot_login_manager.libs.core import hlm_paths
from hotspot_login_manager.libs.daemon import hlm_log
from hotspot_login_manager.libs.notifier import hlm_backends


#-----------------------------------------------------------------------------
def args():
    ''' Parse command-line arguments and perform basic sanity checks.
        Some arguments are handled directly by this function to avoid useless clutter outside of it.

        This function's results are cached so calling it several times incurs no penalty / side-effects.
    '''
    if args.__cache == None:
        args.__cache = _parse()
    return args.__cache

#
# Cached results
#
args.__cache = None


#-----------------------------------------------------------------------------
def exitWithError(error):
    ''' Print an error string to stderr and exit.
    '''
    print(error, file = sys.stderr)
    sys.exit(2) # traditional Unix exit status for command-line errors


#-----------------------------------------------------------------------------
def _parse():
    ''' Perform the actual arguments parsing.
    '''
    # Double-pass arguments checking to reduce performance hit when many notification backends are available
    #   --notifier option requires double-pass if the provided backend is not available
    #   --help always requires double-pass in order to display the available backends
    (parser, options) = _parseArgs(ignoreNotifier = True)
    if (options.displayHelp == True) or (options.runNotifier and (not hlm_backends.isAvailableBackend(options.notifierBackend))):
        (parser, options) = _parseArgs(ignoreNotifier = False)

    # Handle --help and --version and exit immediately
    if options.displayHelp or options.displayVersion:
        print('Hotspot Login Manager {0}'.format(hlm_application.getVersion()))
        if options.displayHelp:
            print()
            parser.print_help()
        sys.exit(0)
    # We don't need the parser anymore
    parser.destroy()

    # Do not accept additional options except a stray ':' to avoid infinite recursion during command-line canonicalization
    # (cf. core/hlm_daemonize, core/hlm_psargs)
    if (options.strayArgs != []) and (options.strayArgs != [':']):
        exitWithError(_N('Unknown option:', 'Unknown options:', len(options.strayArgs)) + ' ' + ' '.join(options.strayArgs))

    # Mutually exclusive options
    mainCommands = _quoted(['--daemon', '--reauth', '--status', '--notifier'])
    mainCommandsCount = sum([options.runDaemon, options.runReauth, options.runStatus, options.runNotifier])
    if mainCommandsCount == 0:
        exitWithError(_('Missing option: one of {0} must be used.').format(mainCommands))
    if mainCommandsCount > 1:
        exitWithError(_('Incompatible options: the options {0} are mutually exclusive.').format(mainCommands))
    if (not options.runDaemon) and ((options.daemonConfig != None) or (options.daemonLogLevel != None)):
        if options.daemonConfig != None:
            optionName = '--config'
        elif options.daemonLogLevel != None:
            optionName = '--log'
        exitWithError(_('Incompatible options: {0} can only be used in combination with {1}.').format(_quoted([optionName]), _quoted(['--daemon'])))

    # Apply default values
    if options.runDaemon:
        if options.daemonConfig == None:
            options.daemonConfig = hlm_paths.defaultConfigFile()
        if options.daemonLogLevel == None:
            options.daemonLogLevel = hlm_log.defaultLevel

    return options


#-----------------------------------------------------------------------------
def _parseArgs(ignoreNotifier):
    ''' Parse the command-line arguments, optionally ignoring the notification backend choices.
    '''
    parser = OptionParser(usage = _('Usage: %prog OPTIONS'), add_help_option = False)
    # Map Python english error messages to custom i18n messages
    parser.error = _i18nErrorMapper
    # Set default options
    parser.set_defaults(displayHelp = False,
                        displayVersion = False,
                        # User notifications
                        runReauth = False,
                        runStatus = False,
                        runNotifier = False,
                        notifierBackend = None,
                        # System daemon
                        runDaemon = False,
                        daemonConfig = None,
                        daemonLogLevel = None,
                       )

    group = OptionGroup(parser, _('General information'))
    group.add_option('-h', '--help',
                     help = _('Display this help message and exit.'),
                     dest = 'displayHelp', action = 'store_true')
    group.add_option('-v', '--version',
                     help = _('Display the program version and exit.'),
                     dest = 'displayVersion', action = 'store_true')
    parser.add_option_group(group)

    group = OptionGroup(parser, _('User commands'))

    # Double-pass arguments checking to reduce performance hit when many notification backends are available
    # We don't want to check every single backend if the user doesn't ask that
    if ignoreNotifier:
        availableNotifierBackends = None
        notifierBackendsMessage = ''
    else:
        availableNotifierBackends = hlm_backends.getAvailableBackends()
        if availableNotifierBackends != []:
            notifierBackendsMessage = _('Available notification backends for your current user session are: {0}').format(_quoted(availableNotifierBackends))
        else:
            notifierBackendsMessage = _('There isn\'t any available notification backend for your current user session. You cannot run a notifier daemon.')

    group.add_option('-r', '--reauth',
                     help = _('Ask the system daemon to reauthenticate you immediately (bypassing the connection watchdog\'s timer) in case the hotspot decided to disconnect you.'),
                     dest = 'runReauth', action = 'store_true')
    group.add_option('-s', '--status',
                     help = _('Display the current status of the system daemon and exit.'),
                     dest = 'runStatus', action = 'store_true')
    group.add_option('-n', '--notifier', metavar = _('BACKEND'),
                     help = _('Run in the background and display end-user notifications using the BACKEND method.') + ' ' + notifierBackendsMessage,
                     choices = availableNotifierBackends, dest = 'notifierBackend')
    parser.add_option_group(group)

    group = OptionGroup(parser, _('System daemon options'))
    group.add_option('-d', '--daemon',
                     help = _('Run as a system daemon (unique instance).'),
                     dest = 'runDaemon', action = 'store_true')
    group.add_option('--config', metavar = _('FILE'),
                     help = _('Use the configuration file FILE. If this option is omitted {0} will be used.')
                            .format(_quoted([hlm_paths.defaultConfigFile()])),
                     dest = 'daemonConfig')
    availableLogLevels = list(hlm_log.levels.keys())
    group.add_option('--log', metavar = _('LEVEL'),
                     help = _('Determine the maximum verbosity LEVEL of the log messages. In increasing verbosity order, the possible levels are: {0}. If this option is omitted, a default level of {1} will be used. Log messages are emitted to syslog\'s {2} facility.')
                            .format(_quoted(availableLogLevels), _quoted([hlm_log.defaultLevel]), _quoted([hlm_log.facilityName])),
                     dest = 'daemonLogLevel', choices = availableLogLevels)
    parser.add_option_group(group)

    (options, strayArgs) = parser.parse_args()

    # Boolean runNotifier value to handle sanity checks more easily
    options.runNotifier = (options.notifierBackend != None)
    # Store stray args in the options
    options.strayArgs = strayArgs

    return (parser, options)


#-----------------------------------------------------------------------------
def _i18nErrorMapper(error):
    ''' Map Python english error messages to i18n messages.
    '''
    #
    # No need to pre-compile the regexes as we exit immediately after using it exactly once.
    #
    if error.startswith('ambiguous option: '):
        match = re.search('^ambiguous option: ([^ ]+) \\((.*)\\?\\)$', error)
        if match != None:
            optionName = _quoted([match.group(1)])
            possibleOptions = _quoted(match.group(2).split(', '))
            exitWithError(_('Ambiguous option: {0} could mean {1}.').format(optionName, possibleOptions))

    if error.endswith(' option requires an argument'):
        match = re.search('^([^ ]+) option requires an argument$', error)
        if match != None:
            optionName = _quoted([match.group(1)])
            exitWithError(_('Option {0} requires an argument.').format(optionName))

    if error.startswith('option '):
        match = re.search('^option ([^:]+): invalid choice: \'(.+)\' \(choose from (\'(.+)\')?\)$', error)
        if match != None:
            optionName = _quoted([match.group(1)])
            invalidChoice = _quoted([match.group(2)])
            validChoices = match.group(4)
            if validChoices != None:
                possibleChoices = _quoted(validChoices.split('\', \''))
                possibleChoices = _('Valid arguments are: {0}.').format(possibleChoices)
            else:
                possibleChoices = _('There isn\'t any possible valid argument. This option is unusable.')
            exitWithError(_('Invalid argument {0} for option {1}.').format(invalidChoice, optionName) + '\n' + possibleChoices)

    exitWithError(error)


#-----------------------------------------------------------------------------
def _quoted(items):
    ''' Convenience function for wrapping a list of items inside « » quotes, separated by commas.
    '''
    return '«' + ('», «').join(items) + '»'


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
