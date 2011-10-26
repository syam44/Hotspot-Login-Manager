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
from hotspot_login_manager.libs.daemon import hlm_authenticator
from hotspot_login_manager.libs.daemon import hlm_config
from hotspot_login_manager.libs.daemon import hlm_controlsocket


#-----------------------------------------------------------------------------
_controlSocket = None


#-----------------------------------------------------------------------------
def _createControlSocket():
    ''' Create the client control socket.
    '''
    socketFile = hlm_paths.controlSocket()

    try:
        # We first try to connect to the socket. If noone answers (file not found / connection refused)
        # then we can safely assume it is a stale file.
        clientSocket = None
        try:
            clientSocket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            clientSocket.settimeout(None)
            clientSocket.connect(hlm_paths.controlSocket())
            raise FatalError(_('The HLM system daemon seems to be already running.'))
        except SystemExit:
            raise
        except socket.error as exc:
            if exc.errno == 2: # File not found
                pass
            elif exc.errno == 111: # Connection refused
                # This is a stale file, just delete it
                if __DEBUG__: logDebug('Control socket file {0} already exists but is a stale file. Deleting it.'.format(quote(socketFile)))
                os.remove(socketFile)
            else:
                raise
        clientSocket.shutdown(socket.SHUT_RDWR)
        clientSocket.close()

        # If we got this far then the socket file is available for us.
        global _controlSocket
        _controlSocket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        _controlSocket.settimeout(None)
        _controlSocket.bind(socketFile)
        os.chmod(socketFile, 0o666)
        atexit.register(_closeControlSocket)
        if __DEBUG__: logDebug('Created control socket file {0}.'.format(quote(socketFile)))
    except SystemExit:
        raise
    except BaseException as exc:
        raise FatalError(_('Unable to create the socket file {0}: {1}').format(quote(socketFile), exc))


#-----------------------------------------------------------------------------
def _closeControlSocket():
    try:
        global _controlSocket
        _controlSocket.close()
    except SystemExit:
        raise
    except BaseException:
        pass
    try:
        socketFile = hlm_paths.controlSocket()
        os.remove(socketFile)
    except SystemExit:
        raise
    except BaseException:
        pass


#-----------------------------------------------------------------------------
def main(args):
    # Create the client control socket
    _createControlSocket()
    # Load daemon configuration
    configDaemon = hlm_config.loadDaemon()
    # Load credentials configuration
    configRelevantPluginCredentials = hlm_config.loadRelevantPluginCredentials()

    # Daemonize the process
    hlm_daemonize.daemonize(
                            umask = 0,
                            syslogLabel = 'Hotspot Login Manager',
                            uid = configDaemon.user,
                            gid = configDaemon.group,
                            keepFiles = [_controlSocket.fileno()],
                           )

    authenticator = hlm_authenticator.Authenticator(configDaemon, configRelevantPluginCredentials)

    _controlSocket.listen(2)
    if __INFO__: logInfo('HLM system daemon is up and running.')
    while True:
        (controlSocket, address) = _controlSocket.accept()
        controlSocket = hlm_controlsocket.ControlSocket(controlSocket, authenticator)


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
