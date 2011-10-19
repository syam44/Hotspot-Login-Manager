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
import sys
#
from hotspot_login_manager.libs.core import hlm_args
from hotspot_login_manager.libs.core import hlm_application
from hotspot_login_manager.libs.core import hlm_pidfile
from hotspot_login_manager.libs.core import hlm_psargs
#
from hotspot_login_manager.libs.core import hlm_daemonize_psf


#-----------------------------------------------------------------------------
def daemonize(
              pidFile = None,           # PID lock file name
              workingDir = None,        # Working directory *after* chroot
              umask = None,             # Default umask inherits from parent process
              # root options
              chroot = None,            # Directory to chroot into
              uid = None,               # Change process UID (default: relinquish any inherited effective privilege elevation)
              gid = None,               # Change process GID (default: relinquish any inherited effective privilege elevation)
             ):
    ''' Turn the current process into a well-behaved daemon.
    '''
    try:
        # Canonicalize command-line to allow correct detection of stale PID files
        _restartIfNotCanonicalCommandLine()

        #
        # TODO: proper daemonization
        #

        # Create the PID lock file
        hlm_pidfile.createPIDFile(pidFile)
    except Exception as err:
        print(err, file = sys.stderr)
        sys.exit(1)


#-----------------------------------------------------------------------------
def _restartIfNotCanonicalCommandLine():
    ''' Check if we have been called using a canonical command-line, restart
        properly otherwise.
    '''
    args = hlm_args.args()
    isCanonical = hlm_psargs.isCanonicalCommandLine(os.getpid())
    if isCanonical != True:
        # Protect against infinite loops
        if args.strayArgs == [':']:
            raise Exception('[BUG] Unable to enforce canonical command-line, exiting.')
        debug('hlm_daemonize._restartIfNotCanonicalCommandLine: canonicalizing command-line...')
        # Restart the daemon with a properly canonicalized command-line
        exeName = hlm_application.getExecutableName()
        if args.runDaemon:
            os.execl(exeName, exeName, ':', '--daemon', '--config', args.daemonConfig, '--log', args.daemonLogLevel)
        elif args.runNotifier:
            os.execl(exeName, exeName, ':', '--notifier', args.notifierBackend)
        else:
            raise Exception('[BUG] Unexpected combination of command-line arguments.')


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
