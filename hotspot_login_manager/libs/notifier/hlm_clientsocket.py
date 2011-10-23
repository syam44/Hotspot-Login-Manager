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
# Description: Client-side of the control socket.
#


#-----------------------------------------------------------------------------
import socket
#
from hotspot_login_manager.libs.core import hlm_paths


#-----------------------------------------------------------------------------
class ClientSocket(object):
    ''' Client-side of the control socket.
    '''
    #-----------------------------------------------------------------------------
    def __init__(self):
        try:
            self.__socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.__socket.connect(hlm_paths.controlSocket())
            self.__socket.settimeout(None)
            self.__file = self.__socket.makefile(mode = 'rw')
            if __DEBUG__: logDebug('Created client socket #{0}.'.format(self.__socket.fileno()))
        except SystemExit:
            raise
        except socket.error as exc:
            if exc.errno == 2: # File does not exist
                pass
            elif exc.errno == 111: # Connection refused
                pass
            else:
                _socketError(exc, 'connect()')
            raise FatalError(_('Could not connect to the HLM system daemon. Is it running?'))
        except BaseException as exc:
            _socketError(exc, 'connect()')


    #-----------------------------------------------------------------------------
    def readline(self):
        try:
            message = self.__file.readline()
            if message.endswith(' \n'):
                return message.strip() + '\n' + self.readline()
            else:
                return message.strip()
        except SystemExit:
            raise
        except BaseException as exc:
            return ''


    #-----------------------------------------------------------------------------
    def write(self, message):
        try:
            self.__file.write(message + '\n')
            self.__file.flush()
        except SystemExit:
            raise
        except BaseException as exc:
            _socketError(exc, 'write()')


    #-----------------------------------------------------------------------------
    def close(self):
        try:
            if __DEBUG__: logDebug('Closing client socket #{0}...'.format(self.__socket.fileno()))
            self.__file.close()
            self.__socket.shutdown(socket.SHUT_RDWR)
            self.__socket.close()
        except SystemExit:
            raise
        except BaseException as exc:
            _socketError(exc, 'close()', False)


    #-----------------------------------------------------------------------------
    def fileno(self):
        return self.__socket.fileno()


#-----------------------------------------------------------------------------
def _socketError(exc, where, raiseError = True):
    message = 'Client socket error in {0}: {1}'.format(where, exc)
    if raiseError:
        raise FatalError(message)
    else:
        if __DEBUG__: logDebug(message)


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
