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
from hotspot_login_manager.libs import hlm_application
from hotspot_login_manager.libs import hlm_notifier
from hotspot_login_manager.libs import hlm_paths


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
    parser = OptionParser(usage = _('Usage: %prog OPTIONS'), add_help_option = False)
    # Map Python english error messages to custom i18n messages
    parser.error = __i18nErrorMapper
    # Set default options
    parser.set_defaults(displayHelp = False,
                        displayVersion = False,
                        # System daemon
                        runDaemon = False,
                        daemonConfig = None,
                        daemonLogLevel = None,
                        # User notification daemon
                        notifierBackend = None,
                        )
    # Use a separate variable for the default log level so we can detect usage of the --log option
    defaultDaemonLogLevel = 'info'

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
                     help = _('Use the configuration file FILE. If this option is missing {0} will be used.')
                            .format(__quoted([hlm_paths.defaultConfigFile()])),
                     dest = 'daemonConfig')
    availableLoggingLevels = ['silent', 'error', 'info', 'debug']
    group.add_option('--log', metavar = _('LEVEL'),
                     help = _('Determine the verbosity LEVEL of the log messages. From least to most verbose, the possible levels are: {0}. If this option is missing, a default level of {1} will be used. Log messages are emitted to syslog\'s {2} facility.')
                            .format(__quoted(availableLoggingLevels), __quoted([defaultDaemonLogLevel]), __quoted(['daemon'])),
                     dest = 'daemonLogLevel', choices = availableLoggingLevels)
    parser.add_option_group(group)

    group = OptionGroup(parser, _('User notification daemon'))

    availableNotifierBackends = hlm_notifier.getAvailableBackends()
    if availableNotifierBackends != []:
        notifierBackendsMessage = _('Available notification backends for your current session are: {0}').format(__quoted(availableNotifierBackends))
    else:
        notifierBackendsMessage = _('There isn\'t any available notification backend for your current session. You cannot run a notifier daemon.')

    group.add_option('-n', '--notifier', metavar = _('BACKEND'),
                     help = _('Run as a user daemon that receives notifications from the system daemon and forwards them to the user through the BACKEND program.') + ' ' + notifierBackendsMessage,
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
    mainCommands = __quoted(['--daemon', '--notifier'])
    mainCommandsCount = sum([options.runDaemon, runNotifier])
    if mainCommandsCount == 0:
        exitWithError(_('Missing option: one of {0} must be used.').format(mainCommands))
    if mainCommandsCount > 1:
        exitWithError(_('Incompatible options: the options {0} are mutually exclusive.').format(mainCommands))
    if (not options.runDaemon) and ((options.daemonConfig != None) or (options.daemonLogLevel != None)):
        if options.daemonConfig != None:
            optionName = '--config'
        elif options.daemonLogLevel != None:
            optionName = '--log'
        exitWithError(_('Incompatible options: {0} can only be used in combination with {1}.').format(__quoted([optionName]), __quoted(['--daemon'])))
    if options.runDaemon and (options.daemonLogLevel == None):
        options.daemonLogLevel = defaultDaemonLogLevel

    # Return a clean set of options
    args = Values()
    args.runDaemon = options.runDaemon
    args.daemonConfig = options.daemonConfig
    args.daemonLogLevel = options.daemonLogLevel
    args.notifierBackend = options.notifierBackend

    return args


#-----------------------------------------------------------------------------
def __i18nErrorMapper(error):
    ''' Map Python english error messages to i18n messages.
    '''
    if error.startswith('ambiguous option: '):
        match = re.search('^ambiguous option: ([^ ]+) \\((.*)\\?\\)$', error)
        if match != None:
            optionName = __quoted([match.group(1)])
            possibleOptions = __quoted(match.group(2).split(', '))
            exitWithError(_('Ambiguous option: {0} could mean {1}.').format(optionName, possibleOptions))

    if error.endswith(' option requires an argument'):
        match = re.search('^([^ ]+) option requires an argument$', error)
        if match != None:
            optionName = __quoted([match.group(1)])
            exitWithError(_('Option {0} requires an argument.').format(optionName))

    if error.startswith('option '):
        match = re.search('^option ([^:]+): invalid choice: \'(.+)\' \(choose from (\'(.+)\')?\)$', error)
        if match != None:
            optionName = __quoted([match.group(1)])
            invalidChoice = __quoted([match.group(2)])
            if match.group(4) != None:
                possibleChoices = __quoted(match.group(4).split('\', \''))
                possibleChoices = _('Valid arguments are: {0}.').format(possibleChoices)
            else:
                possibleChoices = _('There isn\'t any possible valid argument. This option is unusable.')
            exitWithError(_('Invalid argument {0} for option {1}.').format(invalidChoice, optionName) + '\n' + possibleChoices)

    exitWithError(error)


#-----------------------------------------------------------------------------
def __quoted(items):
    ''' Wrap a list of items inside « » quotes, separated by commas.
    '''
    return '«' + ('», «').join(items) + '»'


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
