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
from hotspot_login_manager.libs import hlm_defaultpaths
from hotspot_login_manager.libs import hlm_version


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
                        # Daemon
                        runDaemon = False,
                        daemonConfig = None,
                        # Client
                        notifierBackend = None,
                        )

    group = OptionGroup(parser, _('General information'))
    group.add_option('-h', '--help', help = _('Display this help message and exit.'),
                     dest = 'displayHelp', action = 'store_true')
    group.add_option('-v', '--hversion', help = _('Display the program version and exit.'),
                     dest = 'displayVersion', action = 'store_true')
    parser.add_option_group(group)

    group = OptionGroup(parser, _('Daemon commands'), _('Those commands control how the system daemon is started.'))
    group.add_option('-d', '--daemon', help = _('Run as a system daemon (unique instance).'),
                     dest = 'runDaemon', action = 'store_true')
    group.add_option('-c', '--config', metavar = 'FILE', help = _('Use the configuration file FILE. If this option is missing {0} will be used.').format('«' + hlm_defaultpaths.defaultConfigFile() + '»'),
                     dest = 'daemonConfig', action = 'store')
    parser.add_option_group(group)

    availableNotifierBackends = __getAvailableNotifierBackends()
    group = OptionGroup(parser, _('Client commands'), _('Those commands interact with the system daemon, possibly from unpriviledged user accounts.'))
    group.add_option('-n', '--notifier', metavar="BACKEND", help = _('Run as an unpriviledged user daemon that receives notifications from the system daemon and forwards them to the user through the BACKEND script. Available BACKENDs are: {0}').format('«' + '», «'.join(availableNotifierBackends) + '»'),
                     choices = availableNotifierBackends,
                     dest = 'notifierBackend', action = 'store')
    parser.add_option_group(group)

    (options, args) = parser.parse_args()

    # Handle --help and --version and exit immediately
    if options.displayHelp or options.displayVersion:
        print('Hotspot Login Manager {0}'.format(hlm_version.getVersion()))
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
    if sum([options.runDaemon, runNotifier]) > 1:
        exitWithError(_('Incompatible options: the options {0} are mutually exclusive.').format('«--daemon», «--notifier»'))
    if (not options.runDaemon) and (options.daemonConfig != None):
        exitWithError(_('Incompatible options: {0} can only be used in combination with {1}.').format('«--config»', '«--daemon»'))

    # Return a clean set of options
    args = Values()
    args.runDaemon = options.runDaemon
    args.daemonConfig = options.daemonConfig
    args.notifierBackend = options.notifierBackend

    return args


#-----------------------------------------------------------------------------
def __i18nErrorMapper(error):
    ''' Map Python english error messages to i18n messages.
    '''
    if error.startswith('ambiguous option: '):
        match = re.search('^ambiguous option: ([^ ]+) \\((.*)\\?\\)$', error)
        if match != None:
            optionName = '«' + match.group(1) + '»'
            possibleOptions = '«' + ('», «').join(match.group(2).split(', ')) + '»'
            exitWithError(_('Ambiguous option: {0} could mean {1}.').format(optionName, possibleOptions))

    if error.endswith(' option requires an argument'):
        match = re.search('^([^ ]+) option requires an argument$', error)
        if match != None:
            optionName = '«' + match.group(1) + '»'
            exitWithError(_('Option {0} requires an argument.').format(optionName))

    if error.startswith('option '):
        match = re.search('^option ([^:]+): invalid choice: \'(.+)\' \(choose from \'(.+)\'\)$', error)
        if match != None:
            optionName = '«' + match.group(1) + '»'
            invalidChoice = '«' + match.group(2) + '»'
            possibleChoices = '«' + ('», «').join(match.group(3).split('\', \'')) + '»'
            exitWithError(_('Invalid argument {0} for option {1}.\nValid arguments are: {2}.').format(invalidChoice, optionName, possibleChoices))

    exitWithError(error)


#-----------------------------------------------------------------------------
def __getAvailableNotifierBackends():
    ''' Retrieve available notifier backends from the hotspot_login_manager/notifiers folder.
    '''
    # TODO: implement // move to hlm_notifier module
    return ['kde4']


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
