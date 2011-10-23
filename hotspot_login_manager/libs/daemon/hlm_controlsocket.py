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
# Description: Server-side of the control socket.
#


#-----------------------------------------------------------------------------
import socket
import threading


#-----------------------------------------------------------------------------
class ControlSocket(threading.Thread):
    ''' Server-side of the control socket.
    '''
    #-----------------------------------------------------------------------------
    def __init__(self, socket, authenticator):
        threading.Thread.__init__(self, name = 'Socket #{0}'.format(socket.fileno()))
        self.daemon = True
        self.__socket = socket
        self.__authenticator = authenticator
        self.start()


    #-----------------------------------------------------------------------------
    def run(self):
        try:
            if __DEBUG__: logDebug('Control socket got a connection (#{0}).'.format(socket.fileno()))
            self.__socket.settimeout(None)
            self.__file = self.__socket.makefile(mode = 'rw')
            command = self.__file.readline()
            if __DEBUG__: logDebug('Control socket #{0} received the command {1}.'.format(socket.fileno(), command))
            if command == 'reauth':
                self.__authenticator.wakeUp.set()
                # TODO: reauth tracking
                pass
            elif command == 'status':
                # TODO: status
                pass
            elif command == 'notify':
                # TODO: notify
                #while True:
                pass

            if __DEBUG__: logDebug('Closing control socket #{0}...'.format(socket.fileno()))
            self.__file.close()
            self.__socket.shutdown(socket.SHUT_RDWR)
            self.__socket.close()
        except BaseException as exc:
            if __WARNING__: logWarning('Control socket error: {0}'.format(exc))


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
