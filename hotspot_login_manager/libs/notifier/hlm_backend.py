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
# Description: User notification daemon backend.
#


#-----------------------------------------------------------------------------
import subprocess


#-----------------------------------------------------------------------------
def isAvailable():
    ''' Check whether the notification backend is available.
    '''
    if isAvailable.__cache == None:
        try:
            result = subprocess.check_output(['which', 'notify-send']).decode()
            if result.endswith('/notify-send\n'):
                isAvailable.__cache = True
                return isAvailable.__cache
        except SystemExit:
            raise
        except BaseException:
            pass
        isAvailable.__cache = False
    return isAvailable.__cache


#
# Cached results
#
isAvailable.__cache = None


#-----------------------------------------------------------------------------
def notify(message, icon = None):
    try:
        if isAvailable.__cache:
            if icon == None:
                subprocess.check_output(['notify-send', '-u', 'low', '-t', str(5000), 'Hotspot Login Manager', message])
            else:
                subprocess.check_output(['notify-send', '-u', 'low', '-t', str(5000), '-i', icon, 'Hotspot Login Manager', message])

    except SystemExit:
        raise
    except BaseException as exc:
        if __DEBUG__: logDebug('hlm_backend.notify(): {0}'.format(exc))


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
