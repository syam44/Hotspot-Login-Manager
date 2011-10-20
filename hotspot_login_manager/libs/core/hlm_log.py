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
''' Module usage:
        This module automatically installs the logging services in every single module.

        Every module has access to the following functions:
            logDebug(), logInfo(), logWarning(), logError() just print/log their arguments depending on whether a log facility is available.

        In order to correctly initialize the logging services, the main script (hotspot-login-manager)
        must import hlm_log as early as possible (first HLM import).
'''


#-----------------------------------------------------------------------------
import atexit
import sys
import syslog


#-----------------------------------------------------------------------------
#
# Available verbosity levels
#
levels = { 'error'   : syslog.LOG_ERR,
           'warning' : syslog.LOG_WARNING,
           'info'    : syslog.LOG_INFO,
           'debug'   : syslog.LOG_DEBUG,
         }
orderedLevels = ['debug', 'info', 'warning', 'error']

#
# Default verbosity level
#
defaultLevel = 'info'

#
# Syslog's facility friendly name (see below for the real facility ID)
#
facilityName = 'daemon'

#
# Syslog's facility
#
_syslogFacility = syslog.LOG_DAEMON



#-----------------------------------------------------------------------------
def open(level):
    ''' Open the syslog facility.
    '''
    global _logger
    if _logger == None:
        _logger =  _Logger(level)


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
        There should be only one instance of this class in the whole program.
    '''
    #-----------------------------------------------------------------------------
    def __init__(self, level):
        self.__active = False
        self.__priority = _translateLogLevel(level)
        syslog.openlog('Hotspot Login Manager', (syslog.LOG_PID | syslog.LOG_NDELAY), _syslogFacility)
        atexit.register(syslog.closelog)
        if isDebug: logDebug('Log facility is ready and waiting to be activated.')


    #-----------------------------------------------------------------------------
    def activate(self):
        if not self.__active:
            globals()['__builtins__']['logDebug'] = self.logDebug
            globals()['__builtins__']['logInfo'] = self.logInfo
            globals()['__builtins__']['logWarning'] = self.logWarning
            globals()['__builtins__']['logError'] = self.logError
            if isDebug: logDebug('Log facility is now active.')
            self.__active = True


    #-----------------------------------------------------------------------------
    def logDebug(self, *args):
        self.__log(syslog.LOG_DEBUG, 'DEBUG:', *args)


    #-----------------------------------------------------------------------------
    def logInfo(self, *args):
        self.__log(syslog.LOG_INFO, 'INFO:', *args)


    #-----------------------------------------------------------------------------
    def logWarning(self, *args):
        self.__log(syslog.LOG_WARNING, 'WARNING:', *args)


    #-----------------------------------------------------------------------------
    def logError(self, *args):
        self.__log(syslog.LOG_ERR, 'ERROR:', *args)


    #-----------------------------------------------------------------------------
    def __log(self, priority, *args):
        message = ' '.join(map(str, args))
        if priority <= self.__priority:
            syslog.syslog(priority, message)


#-----------------------------------------------------------------------------
def _translateLogLevel(level):
    ''' Convenience function to translate hlm_log log levels to syslog values.
    '''
    try:
        return levels[level]
    except KeyError:
        return levels[defaultLevel]


#-----------------------------------------------------------------------------
#
# Logging functions.
#
def _logStdErr(*args):
    ''' Used for the logDebug(), logWarning() and logError() global functions until a log facility is available.
    '''
    print(*args, file = sys.stderr)


def _logDebug(*args):
    _logStdErr('DEBUG:', *args)

def _logInfo(*args):
    _logStdErr('INFO:', *args)

def _logWarning(*args):
    _logStdErr('WARNING:', *args)

def _logError(*args):
    _logStdErr('ERROR:', *args)


#-----------------------------------------------------------------------------
#
# Install the logging services globally. They will be available to every module.
#
globals()['__builtins__']['logDebug'] = _logDebug
globals()['__builtins__']['logInfo'] = _logInfo
globals()['__builtins__']['logWarning'] = _logWarning
globals()['__builtins__']['logError'] = _logError


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
