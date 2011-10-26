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
# Description: Define a few global functions and classes.
#


#-----------------------------------------------------------------------------
''' Module usage:
        This module automatically installs the required functions and classes in every single module.

        Every module has access to the following services:
          * _()  is the basic string translator (one to one mapping, cf. gettext.lgettext).
          * _N() is the plural string translator (mapping depends on the counter, cf. gettext.lngettext).
                See hotspot_login_manager/lang/README for information about translation files (.pot / .po / .mo).

          * logDebug(), logInfo(), logWarning(), logError() just print(stderr) / log(syslog.daemon)
            their arguments depending on whether a log facility is available. Same semantics as print().

          * quote() allows to wrap its argument (either a list or a string) into pretty quotes « » (cf. _quote())
          * FatalError as it name implies should not be trapped anywhere else than in the main script.

        In order to correctly initialize the global services, the main script (hotspot-login-manager)
        must import hlm_globals as early as possible (it should be the first HLM import).
'''


#-----------------------------------------------------------------------------
import gettext
import sys
#
from hotspot_login_manager.libs.core import hlm_application


#-----------------------------------------------------------------------------
#
# Translation services.
# Bind the gettext functions to the locales directory and domain.
#
gettext.bindtextdomain('hotspot-login-manager', hlm_application.getPath() + '/lang')
gettext.textdomain('hotspot-login-manager')


globals()['__builtins__']['_'] = gettext.gettext
globals()['__builtins__']['_N'] = gettext.ngettext


#-----------------------------------------------------------------------------
#
# Basic logging services.
# Those functions will be overriden in daemon mode by daemon/hlm_log.activate()
#


availableLogLevels = ['debug', 'info', 'warning', 'error']
defaultLogLevel = 'info'


def setLogLevel(level):
    ''' Define the global maximum logging level.
    '''
    globals()['__builtins__']['__DEBUG__'] = (level == 'debug')
    globals()['__builtins__']['__INFO__'] = (level == 'info') or __DEBUG__ or (level not in availableLogLevels)
    globals()['__builtins__']['__WARNING__'] = (level == 'warning') or __INFO__
    globals()['__builtins__']['__ERROR__'] = (level == 'error') or __WARNING__


def _logDebug(*args):
    if __DEBUG__: _logStdErr('DEBUG:', *args)

def _logInfo(*args):
    if __INFO__: _logStdErr('INFO:', *args)

def _logWarning(*args):
    if __WARNING__: _logStdErr('WARNING:', *args)

def _logError(*args):
    if __ERROR__: _logStdErr('ERROR:', *args)

def _logStdErr(*args):
    ''' Used for the logDebug(), logWarning() and logError() global functions until a log facility is available.
    '''
    print(*args, file = sys.stderr)


globals()['__builtins__']['logDebug'] = _logDebug
globals()['__builtins__']['logInfo'] = _logInfo
globals()['__builtins__']['logWarning'] = _logWarning
globals()['__builtins__']['logError'] = _logError

globals()['__builtins__']['__DEBUG__'] = False
globals()['__builtins__']['__INFO__'] = False
globals()['__builtins__']['__WARNING__'] = False
globals()['__builtins__']['__ERROR__'] = False

setLogLevel('info')


#-----------------------------------------------------------------------------
#
# Various helpers
#
def _quote(arg):
    ''' Wrap arg into pretty quotes.
        If arg is a list each individual item will be quoted, and joined with ', '.
    '''
    if isinstance(arg, list):
        return '«' + '», «'.join(map(str, arg)) + '»'
    return '«' + str(arg) + '»'


class _FatalError(Exception):
    ''' FatalError as it name implies should not be trapped anywhere else than in the main script.
    '''


globals()['__builtins__']['quote'] = _quote
globals()['__builtins__']['FatalError'] = _FatalError


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
