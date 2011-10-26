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
import getpass
import os
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
    hlm_daemonize.daemonize(syslogLabel = 'Hotspot Login Manager (notifications for {0})'.format(quote(getpass.getuser())),
                            keepFiles = [clientSocket.fileno()],
                           )

    if __INFO__: logInfo('HLM notifier daemon is up and running.')
    try:
        clientSocket.write('notify')
        #
        # Regexes for parsing the notifications:
        # If a notification starts with [...] then the "..." is supposed
        # to be an icon that we will pass to notify-send.
        # Icons are taken from the hotspot_login_manager/icons directory.
        #
        regex = re.compile('^\\[([^]/]+)\\] ')
        #
        while True:
            message = clientSocket.readMessage()
            if message == '':
                break
            # Default icon
            icon = None
            match = regex.search(message)
            if match != None:
                # We found [icon], check it and adjust the message
                iconName = match.group(1)
                iconPath = hlm_application.getPath() + '/icons/' + iconName + '.png'
                if os.path.isfile(iconPath):
                    icon = iconPath
                    message = message[len(iconName)+3:]
            # Send the notification to the end-user
            hlm_notifierbackend.notify(message, icon)
    finally:
        if __INFO__: logInfo('HLM notifier daemon is shutting down...')
        clientSocket.close()
        sys.exit(0)


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
