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
# Description: Daemon logging facility.
#              Uses syslog under the hood.
#


#-----------------------------------------------------------------------------
import atexit
import sys
import syslog


#-----------------------------------------------------------------------------
def open():
    ''' Open the syslog facility.
    '''
    global _logger
    if _logger == None:
        _logger =  _Logger()


#-----------------------------------------------------------------------------
def activate():
    ''' Activate the log facility globally.
    '''
    if _logger != None:
        _logger.activate()


#-----------------------------------------------------------------------------
_logger = None

#-----------------------------------------------------------------------------
class _Logger(object):
    ''' Log facility with capped logging levels.
        There must be only one instance of this class in the whole program, which
        is enforced by open() / activate() module functions.
    '''
    #-----------------------------------------------------------------------------
    def __init__(self):
        self.__active = False
        syslog.openlog('Hotspot Login Manager', (syslog.LOG_PID | syslog.LOG_NDELAY), syslog.LOG_DAEMON)
        atexit.register(syslog.closelog)
        if __DEBUG__: logDebug('Syslog facility is ready and waiting to be activated.')


    #-----------------------------------------------------------------------------
    def activate(self):
        if not self.__active:
            globals()['__builtins__']['logDebug'] = self.logDebug
            globals()['__builtins__']['logInfo'] = self.logInfo
            globals()['__builtins__']['logWarning'] = self.logWarning
            globals()['__builtins__']['logError'] = self.logError
            if __DEBUG__: logDebug('Syslog facility is now active.')
            self.__active = True


    #-----------------------------------------------------------------------------
    def logDebug(self, *args):
        if __DEBUG__:
            self.__log(syslog.LOG_DEBUG, 'DEBUG:', *args)


    #-----------------------------------------------------------------------------
    def logInfo(self, *args):
        if __INFO__:
            self.__log(syslog.LOG_INFO, 'INFO:', *args)


    #-----------------------------------------------------------------------------
    def logWarning(self, *args):
        if __WARNING__:
            self.__log(syslog.LOG_WARNING, 'WARNING:', *args)


    #-----------------------------------------------------------------------------
    def logError(self, *args):
        if __ERROR__:
            self.__log(syslog.LOG_ERR, 'ERROR:', *args)


    #-----------------------------------------------------------------------------
    def __log(self, priority, *args):
        message = ' '.join(map(str, args))
        syslog.syslog(priority, message)


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
