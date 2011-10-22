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
# Description: Main program for the system daemon.
#


#-----------------------------------------------------------------------------
import os
import sys
#
from hotspot_login_manager.libs.core import hlm_daemonize
from hotspot_login_manager.libs.core import hlm_paths
from hotspot_login_manager.libs.core import hlm_pidfile


#-----------------------------------------------------------------------------
def daemonPreChangeOwner(keepFiles):
    ''' Wrapper function that runs just before root rights are relinquished.
    '''
    createPIDFile()
    keepFiles = loadCredentials(keepFiles)
    keepFiles = createClientSocket(keepFiles)
    return keepFiles


#-----------------------------------------------------------------------------
def createPIDFile():
    ''' Create the PID lock file
    '''
    pidFile = hlm_paths.pidFile()
    try:
        os.mkdir(os.path.dirname(pidFile, 0o644))
    except OSError as exc:
        if exc.errno != 17:
            raise
    hlm_pidfile.createPIDFile(pidFile)


#-----------------------------------------------------------------------------
def loadCredentials(keepFiles):
    ''' Load the credentials configuration file.
    '''
    logWarning('NOT IMPLEMENTED: hlm_main_daemon.loadCredentials()')
    return keepFiles


#-----------------------------------------------------------------------------
def createClientSocket(keepFiles):
    ''' Create the client control socket.
    '''
    logWarning('NOT IMPLEMENTED: hlm_main_daemon.createClientSocket()')
    return keepFiles


#-----------------------------------------------------------------------------
def loadDaemonConfig(args):
    ''' Load the daemon configuration file.
    '''
    logWarning('NOT IMPLEMENTED: hlm_main_daemon.loadDaemonConfig()')

    args.daemonCredentials = ''
    return ('/', 0o644, 1000, 1000)


#-----------------------------------------------------------------------------
def main(args):
    (workingDir, umask, uid, gid) = loadDaemonConfig(args)
    hlm_daemonize.daemonize(
                            workingDir = workingDir,
                            umask = umask,
                            hookPreChangeOwner = daemonPreChangeOwner,
                            uid = uid,
                            gid = gid,
                           )

    import time
    from hotspot_login_manager.libs.daemon import hlm_wireless
    #
    while True:
        wirelessIfaces = hlm_wireless.getInterfaces()
        logInfo('Wireless interfaces:', str(wirelessIfaces))
        for iface in wirelessIfaces:
            logInfo('   ', iface, '=', hlm_wireless.getSSID(iface))
        time.sleep(5)

    raise NotImplementedError('NOT IMPLEMENTED: --daemon')

    sys.exit(0)


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
