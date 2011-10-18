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
# Description: Log facility with capped logging levels.
#              Uses syslog under the hood.
#


#-----------------------------------------------------------------------------
import atexit
import syslog


#-----------------------------------------------------------------------------
#
# Available verbosity levels
#
levels = [ 'error', 'warning', 'info', 'debug' ]
#
# Default verbosity level
#
defaultLevel = 'info'
#
# Syslog's facility friendly name
#
facility = 'daemon'


#-----------------------------------------------------------------------------
#
# Syslog's facility
#
_syslogFacility = syslog.LOG_DAEMON


#-----------------------------------------------------------------------------
class Logger(object):
    ''' Log facility with capped logging levels.
        There should be only one instance of this class in the whole program.
    '''
    def __init__(self, level):
        self.__priority = _translateLogLevel(level)
        syslog.openlog('Hotspot Login Manager', syslog.LOG_PID + syslog.LOG_NDELAY, _syslogFacility)
        atexit.register(syslog.close)


    def isAllowed(level):
        return _translateLogLevel(level) <= self.__prioprity


    def log(self, level, message):
        self.__log(message, _translateLogLevel(level))


    def logDebug(self, message):
        self.__log(message, syslog.LOG_DEBUG, 'DEBUG: ')


    def logInfo(self, message):
        self.__log(message, syslog.LOG_INFO, 'INFO: ')


    def logWarning(self, message):
        self.__log(message, syslog.LOG_WARNING, 'WARNING: ')


    def logError(self, message):
        self.__log(message, syslog.LOG_ERR, 'ERROR: ')


    def __log(self, message, priority, prefix = ''):
        if priority <= self.__priority:
            syslog.syslog(priority, prefix + message)


#-----------------------------------------------------------------------------
def _translateLogLevel(level):
    ''' Convenience function to translate hlm_log log levels to syslog values.
    '''
    if level == 'error':
        return syslog.LOG_ERR
    if level == 'warning':
        return syslog.LOG_WARNING
    if level == 'debug':
        return syslog.LOG_DEBUG
    return syslog.LOG_INFO


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
