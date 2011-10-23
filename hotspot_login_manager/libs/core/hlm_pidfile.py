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
def readPID(path):
    ''' Read the PID contained in a file.
    '''
    try:
        with open(path, 'r') as pidfile:
            return int(pidfile.readline())
    except SystemExit:
        raise
    except BaseException:
        pass
    return None


#-----------------------------------------------------------------------------
def createPIDFile(path):
    ''' Create a PID lock file and keep it alive until the process exits.
    '''
    try:
        pid = _PIDFile(path)
        if __DEBUG__: logDebug('Created PID file {0} with PID {1}.'.format(quote(path), os.getpid()))
    except SystemExit:
        raise
    except OSError as exc:
        if exc.errno == 2: # File does not exist
            raise FatalError(_('Can\'t write the PID lock file {0}: directory {1} does not exist.').format(quote(path), quote(os.path.dirname(path))))
        if exc.errno == 13: # Permission denied
            raise FatalError(_('Can\'t write the PID lock file {0}: permission denied.').format(quote(path)))
        if exc.errno == 17: # File already exists
            raise FatalError(_('The PID lock file {0} already exists. Is another instance of HLM already running?').format(quote(path)))
        raise FatalError(_('Can\'t write the PID lock file {0}: {1}').format(quote(path)))


#-----------------------------------------------------------------------------
class _PIDFile(object):
    ''' Manage the lifecycle of a daemon's PID file.
    '''
    #-----------------------------------------------------------------------------
    def __init__(self, path):
        self.__path = path
        if not _tryCreateFile(path, False):
            if __DEBUG__: logDebug('The PID file already exists, checking if it is a stale one...')
            _deleteIfStaleFile(path)
            _tryCreateFile(path, True)
        atexit.register(self.__deleteFile)


    #-----------------------------------------------------------------------------
    def __deleteFile(self):
        try:
            os.remove(self.__path)
        except SystemExit:
            raise
        except OSError as exc:
            if exc.errno == 13: # Permission denied
                if __WARNING__: logWarning('Unable to delete the PID file: permission denied, most probably because you used the setuid/setgid configuration options.')
        except BaseException:
            pass


#-----------------------------------------------------------------------------
def _tryCreateFile(path, raiseError):
    ''' Try to create the PID file and return a boolean accordingly
        (or raise an error if raiseError is True).
    '''
    try:
        pidfile_fd = os.open(path, (os.O_CREAT | os.O_EXCL | os.O_WRONLY), 0o644)
        try:
            with os.fdopen(pidfile_fd, 'w') as pidfile:
                pidfile_fd = None
                pid = os.getpid()
                pidfile.write('{0}\n'.format(os.getpid()))
                return True
        finally:
            if pidfile_fd != None:
                os.close()
    except SystemExit:
        raise
    except BaseException:
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
                if __DEBUG__: logDebug('The PID file is stale, removing it...')
                os.remove(path)
    except SystemExit:
        raise
    except BaseException:
        pass


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
