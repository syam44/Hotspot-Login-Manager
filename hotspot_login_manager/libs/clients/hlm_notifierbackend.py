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
import sys


#-----------------------------------------------------------------------------
def isAvailable():
    ''' Check whether the notification backend is available.
    '''
    if isAvailable.__cache == None:
        try:
            result = subprocess.check_output(['which', 'notify-send']).decode('utf-8')
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
    ''' Send a desktop notification to the end-user.
    '''
    if isAvailable.__cache:
        try:
            if icon == None:
                subprocess.check_output(['notify-send', '-u', 'low', '-t', str(5000), 'Hotspot Login Manager', message])
            else:
                subprocess.check_output(['notify-send', '-u', 'low', '-t', str(5000), '-i', icon, 'Hotspot Login Manager', message])
        except:
            logError('notify-send reported an error, exiting.')
            sys.exit(1)


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
