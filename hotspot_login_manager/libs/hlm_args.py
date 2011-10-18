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
from hotspot_login_manager.libs import hlm_notifier


#-----------------------------------------------------------------------------
def exitWithError(error):
    ''' Print the program version and error string to stderr and exit.
    '''
    print(error, file = sys.stderr)
    sys.exit(2) # traditional Unix exit status for command-line errors


#-----------------------------------------------------------------------------
def parse():
    ''' Parse command-line arguments and perform basic sanity checks.
        Some arguments are handled directly by this function to avoid useless clutter outside of it.
    '''
    #
    # FIXME: currently, notification backends are systematically checked on program startup
    #        this has no impact right now because there's only one, but as the list grows it could
    #        become a startup performance problem
    #        solution: multiple-pass arguments checking...
    #            --help checks every notification backend to display the available ones to the end user
    #            --notifier just checks the backend corresponding to the given argument (unless there is
    #                       an error, then we also check all the backends to display a proper error message
    #            every other option just does its job, ignoring the notification backends
    #
    parser = OptionParser(usage = _('Usage: %prog OPTIONS'), add_help_option = False)
    # Map Python english error messages to custom i18n messages
    parser.error = _i18nErrorMapper
    # Set default options
    parser.set_defaults(displayHelp = False,
                        displayVersion = False,
                        # System daemon
                        runDaemon = False,
                        daemonConfig = None,
                        daemonLogLevel = None,
                        # User notifications
                        runReauth = False,
                        notifierBackend = None,
                        runStatus = False
                        )

    group = OptionGroup(parser, _('General information'))
    group.add_option('-h', '--help',
                     help = _('Display this help message and exit.'),
                     dest = 'displayHelp', action = 'store_true')
    group.add_option('-v', '--version',
                     help = _('Display the program version and exit.'),
                     dest = 'displayVersion', action = 'store_true')
    parser.add_option_group(group)

    group = OptionGroup(parser, _('System daemon options'))
    group.add_option('-d', '--daemon',
                     help = _('Run as a system daemon (unique instance).'),
                     dest = 'runDaemon', action = 'store_true')
    group.add_option('--config', metavar = _('FILE'),
                     help = _('Use the configuration file FILE. If this option is omitted {0} will be used.')
                            .format(_quoted([hlm_paths.defaultConfigFile()])),
                     dest = 'daemonConfig')
    group.add_option('--log', metavar = _('LEVEL'),
                     help = _('Determine the maximum verbosity LEVEL of the log messages. In increasing verbosity order, the possible levels are: {0}. If this option is omitted, a default level of {1} will be used. Log messages are emitted to syslog\'s {2} facility.')
                            .format(_quoted(hlm_log.levels), _quoted([hlm_log.defaultLevel]), _quoted([hlm_log.facility])),
                     dest = 'daemonLogLevel', choices = hlm_log.levels)
    parser.add_option_group(group)

    group = OptionGroup(parser, _('Unpriviledged user options'))

    availableNotifierBackends = hlm_notifier.getAvailableBackends()
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
                     help = _('Run as a daemon that displays end-user HLM notifications using the BACKEND method.') + ' ' + notifierBackendsMessage,
                     choices = availableNotifierBackends, dest = 'notifierBackend')
    parser.add_option_group(group)

    (options, args) = parser.parse_args()

    # Handle --help and --version and exit immediately
    if options.displayHelp or options.displayVersion:
        print('Hotspot Login Manager {0}'.format(hlm_application.getVersion()))
        if options.displayHelp:
          print()
          parser.print_help()
        sys.exit(0)
    # We don't need the parser anymore
    parser.destroy()

    # Do not accept additional options
    if args != []:
        exitWithError(_N('Unknown option:', 'Unknown options:', len(args)) + ' ' + ' '.join(args))

    # Boolean runNotifier value to handle sanity checks more easily
    runNotifier = (options.notifierBackend != None)

    # Mutually exclusive options
    mainCommands = _quoted(['--daemon', '--reauth', '--status', '--notifier'])
    mainCommandsCount = sum([options.runDaemon, options.runReauth, options.runStatus, runNotifier])
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
    if options.runDaemon and (options.daemonLogLevel == None):
        options.daemonLogLevel = hlm_log.defaultLevel

    return options


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
            if match.group(4) != None:
                possibleChoices = _quoted(match.group(4).split('\', \''))
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
