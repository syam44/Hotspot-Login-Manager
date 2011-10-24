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
import os
import socket
import threading
#
from hotspot_login_manager.libs.daemon import hlm_config


#-----------------------------------------------------------------------------
class _ExitFromSocket(BaseException):
    ''' Dummy exception class that forces the program flow to close the control socket.
    '''


#-----------------------------------------------------------------------------
class ControlSocket(threading.Thread):
    ''' Server-side of the control socket.
    '''
    #-----------------------------------------------------------------------------
    def __init__(self, controlSocket, authenticator):
        threading.Thread.__init__(self, name = 'Socket #{0}'.format(controlSocket.fileno()))
        self.__socket = controlSocket
        self.__socket.settimeout(None)
        self.__authenticator = authenticator
        self.daemon = True
        self.start()


    #-----------------------------------------------------------------------------
    def run(self):
        try:
            if __DEBUG__: logDebug('Control socket got a connection (#{0}).'.format(self.__socket.fileno()))
            self.__file = self.__socket.makefile(mode = 'rw')
            command = self.__file.readline().strip()
            if __DEBUG__: logDebug('Control socket #{0} received the command {1}.'.format(self.__socket.fileno(), quote(command)))


            #-----------------------------------------------------------------------------
            if command == 'pid':
                self.write(os.getpid())


            #-----------------------------------------------------------------------------
            elif command == 'reauth':
                if self.__authenticator.antiDosWaiting():
                    self.write(_('A reauthentication just happened less than {0} seconds ago, please try again later.').format(hlm_config.antiDosPingDelay))
                    raise _ExitFromSocket()

                self.__authenticator.wakeUp.set()
                # TODO: reauth tracking
                self.write('reauth engaged')


            #-----------------------------------------------------------------------------
            elif command == 'status':
                # TODO: status
                self.write('this is the daemon status')


            #-----------------------------------------------------------------------------
            elif command == 'notify':
                # TODO: notify
                import time
                while True:
                    self.write('[wireless-connected] hello\nthis is a notification')
                    time.sleep(5)


        #-----------------------------------------------------------------------------
        except _ExitFromSocket:
            pass
        except SystemExit:
            pass
        except socket.error as exc:
            if exc.errno != 32: # Broken pipe
                if __WARNING__: logWarning('Control socket error: {0}'.format(exc))
        except BaseException as exc:
            if __WARNING__: logWarning('Control socket error: {0}'.format(exc))

        finally:
            # Silently close the socket
            try:
                if __DEBUG__: logDebug('Closing control socket #{0}...'.format(self.__socket.fileno()))
                self.__file.close()
                self.__socket.shutdown(socket.SHUT_RDWR)
                self.__socket.close()
            except:
                pass


    #-----------------------------------------------------------------------------
    def write(self, message):
        ''' Send a message to the connected HLM client.
            If a message spans over multiple lines, each line except the last one
            will have a space character just before the newline.
        '''
        messages = str(message).split('\n')
        messages = [message.rstrip() for message in messages]
        message = ' \n'.join(messages)
        self.__file.write(message + '\n')
        self.__file.flush()


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
