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
# Description: Main program for the notifier client daemon.
#


#-----------------------------------------------------------------------------
import sys
#
from hotspot_login_manager.libs.core import hlm_application
from hotspot_login_manager.libs.core import hlm_daemonize
from hotspot_login_manager.libs.notifier import hlm_backend
from hotspot_login_manager.libs.notifier import hlm_clientsocket


#-----------------------------------------------------------------------------
def main(args):
    if not hlm_backend.isAvailable():
        sys.exit(1)

    # Daemonize the process
    hlm_daemonize.daemonize()

    socket = hlm_clientsocket.ClientSocket()
    if __INFO__: logInfo('Notifier daemon is up and running.')
    try:
        socket.write('notify')
        while True:
            message = socket.readline()
            if message == '':
                break
            # TODO: message parser
            hlm_backend.notify(message, hlm_application.getPath() + '/icons/wireless-connected.png')
    finally:
        if __INFO__: logInfo('Notifier daemon is shutting down...')
        socket.close()
        sys.exit(0)


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
