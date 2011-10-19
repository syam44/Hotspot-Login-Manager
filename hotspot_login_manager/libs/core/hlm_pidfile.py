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
class PIDFileError(OSError):
    ''' Error creating a PID lock file.
    '''


#-----------------------------------------------------------------------------
def readPID(path):
    ''' Read the PID contained in a file.
    '''
    try:
        with open(path, 'r') as pidfile:
            return int(pidfile.readline())
    except:
        pass
    return None


#-----------------------------------------------------------------------------
def createPIDFile(path):
    ''' Create a PID lock file and keep it alive until the process exits.
    '''
    if path != None:
        try:
            pid = _PIDFile(path)
            debug('hlm_pidfile.createPIDFile: created pidfile «{0}»'.format(path))
        except OSError as err:
            pathQuoted = '«' + path + '»'
            if err.errno == 13:
                raise PIDFileError(err.errno, _('Can\'t write the PID lock file {0}: permission denied.').format(pathQuoted))
            if err.errno == 17:
                raise PIDFileError(err.errno, _('The PID lock file {0} already exists. Is another instance of HLM already running?').format(pathQuoted))
            raise PIDFileError(err.errno, err.strerror, path)


#-----------------------------------------------------------------------------
class _PIDFile(object):
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
        debug('hlm_pidfile._deleteIfStaleFile: checking PID {0}'.format(pid))
        if pid != None:
            isCanonical = hlm_psargs.isCanonicalCommandLine(pid)
            if (isCanonical == None) or (isCanonical == False):
                os.remove(path)
                debug('hlm_pidfile._deleteIfStaleFile: removed stale pidfile «{0}»'.format(path))
    except:
        pass


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
