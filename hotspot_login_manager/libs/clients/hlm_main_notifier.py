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
import os
import re
import sys
import time
#
from hotspot_login_manager.libs.core import hlm_application
from hotspot_login_manager.libs.clients import hlm_notifierbackend
from hotspot_login_manager.libs.clients import hlm_clientsocket


#-----------------------------------------------------------------------------
def main(args):
    if not hlm_notifierbackend.isAvailable():
        sys.exit(1)
    # First connection yields an error if the daemon is not available.
    clientSocket = hlm_clientsocket.ClientSocket()

    while True:
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
                # Keep-alive message, ignore it
                if message == '.':
                    continue
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
            clientSocket.close()

        # Reconnect silently if the daemon went down
        if __DEBUG__: logDebug('Daemon went down, trying to reconnect...')
        while True:
            try:
                time.sleep(1)
                clientSocket = hlm_clientsocket.ClientSocket()
                if __DEBUG__: logDebug('Daemon went up again.')
                break
            except SystemExit:
                raise
            except KeyboardInterrupt:
                raise
            except BaseException:
                pass


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
