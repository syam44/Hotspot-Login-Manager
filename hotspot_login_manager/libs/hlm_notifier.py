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
# Description: User notification daemon.
#


#-----------------------------------------------------------------------------
import os
import subprocess
from hotspot_login_manager.libs import hlm_application


#-----------------------------------------------------------------------------
def getAvailableBackends():
    ''' List all available notification backends.
    '''
    try:
        availableBackends = []
        entries = os.listdir(__notifierBackendsPath + '/')
        for backend in entries:
            if __isValidBackend(backend):
                availableBackends.append(backend)
        return availableBackends
    except:
        return []


#-----------------------------------------------------------------------------
def notify(backend, message):
    ''' Send a notification message to the user through the backend program.
        Return a boolean indicating success.
    '''
    try:
        subprocess.check_call([__backendFullPath(backend), message])
        return True
    except:
        return False


#-----------------------------------------------------------------------------
#
# Filesystem path for the notification backends
#
__notifierBackendsPath = hlm_application.getPath() + '/notifiers'


#-----------------------------------------------------------------------------
def __backendFullPath(backend):
    ''' Return the full path of a specific notification backend.
    '''
    return os.path.realpath(__notifierBackendsPath + '/' + backend)


#-----------------------------------------------------------------------------
def __isValidBackend(backend):
    ''' Determine whether a particular notification backend is callable from
        the current user session context.
    '''
    try:
        backendPath = __backendFullPath(backend)
        if os.path.isfile(backendPath):
            subprocess.check_call([backendPath])
            return True
    except:
        pass
    return False


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
