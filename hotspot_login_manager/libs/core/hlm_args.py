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
from hotspot_login_manager.libs.core import hlm_globals
from hotspot_login_manager.libs.core import hlm_paths
from hotspot_login_manager.libs.clients import hlm_notifierbackend


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
    (parser, options) = _parseArgs()

    # Handle --help and --version and exit immediately
    if options.displayHelp or options.displayVersion:
        print('Hotspot Login Manager {0}'.format(hlm_application.getVersion()))
        if options.displayHelp:
            print()
            parser.print_help()
        sys.exit(0)
    # We don't need the parser anymore
    parser.destroy()

    # Do not accept any additional options
    if options.strayArgs != []:
        exitWithError(_N('Unknown option:',
                         'Unknown options:',
                         len(options.strayArgs))
                      + ' ' + ' '.join(options.strayArgs))

    # Mutually exclusive options
    mainCommands = quote(['--reauth', '--status', '--pid', '--notifier', '--daemon'])
    mainCommandsCount = sum([options.runReauth, options.runStatus, options.runPID, options.runNotifier, options.runDaemon])
    if mainCommandsCount == 0:
        exitWithError(_('Missing option: one of {0} must be used.').format(mainCommands))
    if mainCommandsCount > 1:
        exitWithError(_('Incompatible options: the options {0} are mutually exclusive.').format(mainCommands))
    if (not options.runDaemon) and ((options.daemonConfig != None) or (options.daemonCredentials != None)):
        optionNames = []
        if options.daemonConfig != None:
            optionNames.append('--config')
        if options.daemonCredentials != None:
            optionNames.append('--credentials')
        exitWithError(_N('Incompatible options: {0} can only be used in combination with {1}.',
                         'Incompatible options: {0} can only be used in combination with {1}.',
                         len(optionNames))
                        .format(quote(optionNames), quote('--daemon')))
    if options.runNotifier and not hlm_notifierbackend.isAvailable():
        exitWithError(_('{0} is not available on your system, you cannot run a notifier daemon.').format(quote('notify-send')))

    # Apply default values
    if options.logLevel == None:
        options.logLevel = hlm_globals.defaultLogLevel
    if options.runDaemon:
        # We'll handle daemonCredentials later on because it could be defined in daemon.conf
        if options.daemonConfig == None:
            options.daemonConfig = hlm_paths.daemonConfig()

    return options


#-----------------------------------------------------------------------------
def _parseArgs():
    ''' Parse the command-line arguments, optionally ignoring the notification backend choices.
    '''
    parser = OptionParser(usage = _('Usage: %prog OPTIONS'), add_help_option = False)
    # Map Python english error messages to custom i18n messages
    parser.error = _i18nErrorMapper
    # Set default options
    parser.set_defaults(displayHelp = False,
                        displayVersion = False,
                        # User commands
                        runReauth = False,
                        runStatus = False,
                        runPID = False,
                        # Notification daemon
                        runNotifier = False,
                        # System daemon
                        runDaemon = False,
                        daemonConfig = None,
                        daemonCredentials = None,
                        # Verbosity
                        logLevel = None,
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
    group.add_option('-r', '--reauth',
                     help = _('Ask the system daemon to reauthenticate you immediately (bypassing the connection watchdog\'s timer) in case the hotspot decided to disconnect you.'),
                     dest = 'runReauth', action = 'store_true')
    group.add_option('-s', '--status',
                     help = _('Display the current status of the system daemon and exit.'),
                     dest = 'runStatus', action = 'store_true')
    group.add_option('-p', '--pid',
                     help = _('Display the current PID of the system daemon and exit.'),
                     dest = 'runPID', action = 'store_true')
    parser.add_option_group(group)

    group = OptionGroup(parser, _('Notification daemon options'),
                                _('This daemon can be run under an unprivileged account.'))

    if hlm_notifierbackend.isAvailable():
        notifierBackendMessage = ''
    else:
        notifierBackendMessage = ' ' + _('Unfortunately {0} is not available on your system. You cannot run a notifier daemon.').format(quote('notify-send'))

    group.add_option('-n', '--notifier',
                     help = _('Run in the background and display end-user desktop notifications using {0}.').format(quote('notify-send')) + notifierBackendMessage,
                     dest = 'runNotifier', action = "store_true")
    parser.add_option_group(group)

    group = OptionGroup(parser, _('System daemon options'),
                                _('This daemon must be run under a privileged account.'))
    group.add_option('-d', '--daemon',
                     help = _('Run as a system daemon (unique instance).'),
                     dest = 'runDaemon', action = 'store_true')
    group.add_option('--config', metavar = _('FILE'),
                     help = _('Use the daemon configuration file FILE.'),
                     dest = 'daemonConfig')
    group.add_option('--credentials', metavar = _('FILE'),
                     help = _('Use the credentials configuration file FILE. This option overrides the equivalent option from the daemon configuration file.'),
                     dest = 'daemonCredentials')
    parser.add_option_group(group)

    group = OptionGroup(parser, _('Verbosity'))
    # Remove 'debug' level from the levels available to end-users
    availableLogLevels = hlm_globals.availableLogLevels[:]
    availableLogLevels.remove('debug')
    group.add_option('--log', metavar = _('LEVEL'),
                     help = _('Determine the maximum verbosity LEVEL of the informational messages. In decreasing verbosity order, the possible levels are: {0}. If this option is omitted, a default level of {1} will be used. In both daemon modes, messages are emitted to syslog\'s {2} facility.')
                            .format(quote(availableLogLevels), quote(hlm_globals.defaultLogLevel), quote('daemon')),
                     dest = 'logLevel', choices = availableLogLevels)
    parser.add_option_group(group)

    (options, strayArgs) = parser.parse_args()

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
            optionName = quote(match.group(1))
            possibleOptions = quote(match.group(2).split(', '))
            exitWithError(_('Ambiguous option: {0} could mean {1}.').format(optionName, possibleOptions))

    if error.endswith(' option requires an argument'):
        match = re.search('^([^ ]+) option requires an argument$', error)
        if match != None:
            optionName = quote(match.group(1))
            exitWithError(_('Option {0} requires an argument.').format(optionName))

    if error.startswith('option '):
        match = re.search('^option ([^:]+): invalid choice: \'(.+)\' \(choose from (\'(.+)\')?\)$', error)
        if match != None:
            optionName = quote(match.group(1))
            invalidChoice = quote(match.group(2))
            validChoices = match.group(4)
            if validChoices != None:
                possibleChoices = quote(validChoices.split('\', \''))
                possibleChoices = _('Valid arguments are: {0}.').format(possibleChoices)
            else:
                possibleChoices = _('There isn\'t any possible valid argument. This option is unusable.')
            exitWithError(_('Invalid argument {0} for option {1}.').format(invalidChoice, optionName) + '\n' + possibleChoices)

    exitWithError(error)


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
