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
# Description: Turn the process into a daemon.
#


#-----------------------------------------------------------------------------
import os
#
from hotspot_login_manager.libs.core import hlm_args
from hotspot_login_manager.libs.core import hlm_application
from hotspot_login_manager.libs.core import hlm_psargs


#-----------------------------------------------------------------------------
def daemonize():
    ''' Turn the current process into a well-behaved daemon.
    '''
    # Check if we have been called using a canonical command-line, restart
    # properly otherwise.
    _restartIfNotCanonicalCommandLine()


#-----------------------------------------------------------------------------
def _restartIfNotCanonicalCommandLine():
    args = hlm_args.args()
    isCanonical = hlm_psargs.isCanonicalCommandLine(os.getpid())
    if isCanonical != True:
        # Protect against infinite loops
        if args.strayArgs == [':']:
            raise Exception('Unable to determine canonical command-line, exiting.')
        # Restart the daemon with a properly canonicalized command-line
        exeName = hlm_application.getExecutableName()
        if args.runDaemon:
            os.execl(exeName, exeName, ':', '--daemon', '--config', args.daemonConfig, '--log', args.daemonLogLevel)
        elif args.runNotifier:
            os.execl(exeName, exeName, ':', '--notifier', args.notifierBackend)
        else:
            raise Exception('Unexpected')


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
