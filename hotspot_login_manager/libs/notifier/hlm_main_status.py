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
# Description: Main program for the status client.
#


#-----------------------------------------------------------------------------
import sys
#
from hotspot_login_manager.libs.notifier import hlm_clientsocket


#-----------------------------------------------------------------------------
def main(args):
    socket = hlm_clientsocket.ClientSocket()
    try:
        socket.write('status')
        while True:
            message = socket.readline()
            if message == '':
                break
            else:
                print(message)
    finally:
        socket.close()
        sys.exit(0)


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
