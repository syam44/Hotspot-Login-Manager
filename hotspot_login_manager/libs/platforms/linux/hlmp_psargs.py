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
# Description: Get a process' command-line knowing its PID.
#              This is the Linux-specific implementation.
#


#-----------------------------------------------------------------------------
import re
import subprocess
#
from hotspot_login_manager.libs.core import hlm_application
from hotspot_login_manager.libs.core import hlm_args


#-----------------------------------------------------------------------------
#
# Pre-compiled regular expression
#
_processArgsResult = re.compile('^([^\n]+)\n$')


#-----------------------------------------------------------------------------
def _getProcessArguments(pid):
    ''' Get process command-line from its PID.
    '''
    try:
        result = subprocess.check_output(['ps', '--no-heading', '-o', 'command', '-p', str(pid)]).decode()
        match = _processArgsResult.search(result)
        if match != None:
            return match.group(1)
    except:
        pass
    return None


#-----------------------------------------------------------------------------
def isCanonicalCommandLine(pid):
    ''' Check whether a specific process PID belongs to us and has been created
        using a canonical command-line.

        core/hlm_daemonize ensures that a daemon is always called using its
        canonical command-line.

        Return values:
            True  = the process is ours, using a canonical command-line
            False = the process exists but doesn't use a canonical command-line
            None  = the process doesn't exist
    '''
    processArgs = _getProcessArguments(pid)
    if processArgs == None:
        return None

    args = hlm_args.args()
    canonicalAppPath = hlm_application.getPath() + '/hotspot-login-manager '
    if args.runDaemon:
        canonicalAppPath += '--daemon'
    elif args.notifierBackend != None:
        canonicalAppPath += '--notifier'
    else:
        return False

    return processArgs.startswith(canonicalAppPath)


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
