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
            if __DEBUG__: logDebug('Control socket got a connection (#{0}).'.format(self.__socket.fileno()))
            self.__socket.settimeout(None)
            self.__file = self.__socket.makefile(mode = 'rw')
            command = self.__file.readline().strip()
            if __DEBUG__: logDebug('Control socket #{0} received the command {1}.'.format(self.__socket.fileno(), quote(command)))
            if command == 'reauth':
                self.__authenticator.wakeUp.set()
                # TODO: reauth tracking
                self.write('reauth engaged')

            elif command == 'status':
                # TODO: status
                self.write('this is the daemon status')

            elif command == 'notify':
                # TODO: notify
                import time
                while True:
                    self.write('[hlm:wireless-connected] hello\nthis is a notification')
                    time.sleep(5)

        except SystemExit:
            pass
        except socket.error as exc:
            if exc.errno != 32: # Broken pipe
                if __WARNING__: logWarning('Control socket error: {0}'.format(exc))
        except BaseException as exc:
            if __WARNING__: logWarning('Control socket error: {0}'.format(exc))
        finally:
            try:
                if __DEBUG__: logDebug('Closing control socket #{0}...'.format(self.__socket.fileno()))
                self.__file.close()
                self.__socket.shutdown(socket.SHUT_RDWR)
                self.__socket.close()
            except:
                pass


    #-----------------------------------------------------------------------------
    def write(self, message):
        messages = message.split('\n')
        messages = [message.strip() for message in messages]
        message = ' \n'.join(messages)
        self.__file.write(message + '\n')
        self.__file.flush()


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
