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
import atexit
import os
import socket
import sys
#
from hotspot_login_manager.libs.core import hlm_daemonize
from hotspot_login_manager.libs.core import hlm_paths
from hotspot_login_manager.libs.core import hlm_pidfile
from hotspot_login_manager.libs.daemon import hlm_config


#-----------------------------------------------------------------------------
_controlSocket = None


#-----------------------------------------------------------------------------
def _createSpecialFiles(keepFiles):
    ''' hookPreChangeOwner function that runs just before root rights are relinquished,
        but after we have detached / umask'd. This is the perfect place to create the
        PID file and the client control socket.
    '''
    # Create the PID file
    pidFile = hlm_paths.pidFile()
    pidDir = os.path.dirname(pidFile)
    try:
        os.mkdir(pidDir, 0o755)
    except OSError as exc:
        if exc.errno != 17:
            raise
        os.chmod(pidDir, 0o755)
    hlm_pidfile.createPIDFile(pidFile)

    # Create the client control socket
    socketFile = hlm_paths.controlSocket()
    try:
        # We can afford to just remove it since the PID file is now an acquired lock
        os.remove(socketFile)
    except OSError as exc:
        if exc.errno != 2:
            raise
    global _controlSocket
    _controlSocket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    _controlSocket.bind(socketFile)
    keepFiles.append(_controlSocket.fileno())
    atexit.register(_closeControlSocket)
    if __DEBUG__: logDebug('Created notification socket {0}.'.format(socketFile))

    return keepFiles


#-----------------------------------------------------------------------------
def _closeControlSocket():
    try:
        global _controlSocket
        _controlSocket.close()
    except:
        pass
    try:
        socketFile = hlm_paths.controlSocket()
        os.remove(socketFile)
    except:
        pass


#-----------------------------------------------------------------------------
def main(args):
    # Canonicalize command-line to allow correct detection of stale PID files
    hlm_daemonize.ensureCanonicalCommandLine()

    # Load daemon configuration
    (user, group) = hlm_config.loadDaemon()
    # Load credentials configuration
    credentials = hlm_config.loadCredentials()

    # Daemonize the process
    hlm_daemonize.daemonize(
                            umask = 0o022,
                            hookPreChangeOwner = _createSpecialFiles,
                            uid = user,
                            gid = group,
                           )

    import time
    from hotspot_login_manager.libs.daemon import hlm_wireless
    #
    while True:
        wirelessIfaces = hlm_wireless.getInterfaces()
        logInfo('Wireless interfaces:', str(wirelessIfaces))
        for iface in wirelessIfaces:
            logInfo('   ', iface, '=', hlm_wireless.getSSID(iface))
        time.sleep(30)


    s.listen(1)
    conn, addr = s.accept()
    while 1:
        data = conn.recv(1024)
        if not data:
            break
        conn.send(data)
    conn.close()


    raise NotImplementedError('NOT IMPLEMENTED: --daemon')

    sys.exit(0)


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
