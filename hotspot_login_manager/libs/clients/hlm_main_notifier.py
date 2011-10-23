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
from hotspot_login_manager.libs.clients import hlm_notifierbackend
from hotspot_login_manager.libs.clients import hlm_clientsocket


#-----------------------------------------------------------------------------
def main(args):
    if not hlm_notifierbackend.isAvailable():
        sys.exit(1)

    clientSocket = hlm_clientsocket.ClientSocket()

    # Daemonize the process
    hlm_daemonize.daemonize(keepFiles = [clientSocket.fileno()])

    if __INFO__: logInfo('HLM notifier daemon is up and running.')
    try:
        clientSocket.write('notify')
        regex1 = re.compile('^\\[([^]]+)\\] ')
        regex2 = re.compile('^hlm:(.*)$')
        while True:
            message = clientSocket.readline()
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
            hlm_notifierbackend.notify(message, icon)
    finally:
        if __INFO__: logInfo('HLM notifier daemon is shutting down...')
        clientSocket.close()
        sys.exit(0)


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
