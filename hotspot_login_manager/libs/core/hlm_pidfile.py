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
# Description: Manage a daemon's PID file.
#              Stale locks are automatically detected and handled by this class.
#


#-----------------------------------------------------------------------------
import atexit
import os
#
from hotspot_login_manager.libs.core import hlm_psargs


#-----------------------------------------------------------------------------
class PIDFile(object):
    ''' Manage the lifecycle of a daemon's PID file.
    '''
    #-----------------------------------------------------------------------------
    def __init__(self, path):
        self.__path = path
        if not _tryCreateFile(path, False):
            _deleteIfStaleFile(path)
            _tryCreateFile(path, True)
        atexit.register(self.__deleteFile)


    #-----------------------------------------------------------------------------
    def __deleteFile(self):
        try:
            os.remove(self.__path)
        except:
            pass


#-----------------------------------------------------------------------------
def readPID(path):
    ''' Read the PID contained in a file.
    '''
    try:
        pidfile = open(path, 'r')
        try:
            return int(pidfile.readline())
        finally:
            pidfile.close()
    except:
        pass
    return None


#-----------------------------------------------------------------------------
def _tryCreateFile(path, raiseError):
    ''' Try to create the PID file and return a boolean accordingly
        (or raise an error if raiseError is True).
    '''
    try:
        pidfile_fd = os.open(path, (os.O_CREAT | os.O_EXCL | os.O_WRONLY), 0o644)
        pidfile = os.fdopen(pidfile_fd, 'w')
        pid = os.getpid()
        pidfile.write('{0}\n'.format(os.getpid()))
        pidfile.close()
        return True
    except:
        if raiseError:
            raise
        return False


#-----------------------------------------------------------------------------
def _deleteIfStaleFile(path):
    ''' Delete the PID file in case it doesn't belong to us anymore.

        In order to detect this, every daemon has to use a normalized command-line
        (which is ensured by core/hlm_daemonize).

        NOTE: we don't try to protect against malicious programs that actively
              try to DoS us by tricking us into thinking we're already running,
              we are only concerned about stale locks that remain behind after
              an unclean shutdown, eg. a SIGKILL.
    '''
    try:
        pid = readPID(path)
        if pid != None:
            isCanonical = hlm_psargs.isCanonicalCommandLine(pid)
            if (isCanonical == None) or (isCanonical == False):
                os.remove(path)
    except:
        pass


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
