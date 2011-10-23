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
# Description: Main program for the PID client.
#


#-----------------------------------------------------------------------------
import sys
#
from hotspot_login_manager.libs.clients import hlm_clientsocket


#-----------------------------------------------------------------------------
def main(args):
    try:
        clientSocket = hlm_clientsocket.ClientSocket()
        try:
            clientSocket.write('pid')
            while True:
                message = clientSocket.readMessage()
                if message == '':
                    break
                else:
                    # Coerce the result to an integer.
                    # If there is a problem this will raise an error, thus avoiding
                    # the print() altogether and exiting with return code 1 (error).
                    print(int(message))
                    sys.exit(0)
        finally:
            clientSocket.close()
    except SystemExit:
        raise
    except BaseException:
        sys.exit(1)


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
