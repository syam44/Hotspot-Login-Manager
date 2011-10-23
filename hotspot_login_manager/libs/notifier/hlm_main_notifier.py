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
import re
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

    socket = hlm_clientsocket.ClientSocket()

    # Daemonize the process
    hlm_daemonize.daemonize(keepFiles = [socket.fileno()])

    if __INFO__: logInfo('HLM notifier daemon is up and running.')
    try:
        socket.write('notify')
        regex1 = re.compile('^\\[([^]]+)\\] ')
        regex2 = re.compile('^hlm:(.*)$')
        while True:
            message = socket.readline()
            if message == '':
                break
            icon = 'dialog-information'
            match = regex1.search(message)
            if match != None:
                icon = match.group(1)
                message = message[len(icon)+3:]
                match = regex2.search(icon)
                if match != None:
                    icon = hlm_application.getPath() + '/icons/' + match.group(1) + '.png'
            hlm_backend.notify(message, icon)
    finally:
        if __INFO__: logInfo('Notifier daemon is shutting down...')
        socket.close()
        sys.exit(0)


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
