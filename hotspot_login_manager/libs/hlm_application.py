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
# Description: Global application information.
#


#-----------------------------------------------------------------------------
import os
from hotspot_login_manager.libs import hlm_version


#-----------------------------------------------------------------------------
#
# Application root path.
# Note that the hotspot_login_manager directory is considered to be the root path.
#
# We know this module is located in the hotspot_login_manager/libs directory
# so we just go up one level.
#
__applicationPath = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/..')

def getPath():
    ''' Return the root path of the application.
        Note that the hotspot_login_manager directory is considered to be the root path.
    '''
    return __applicationPath


#-----------------------------------------------------------------------------
#
# Application version.
#
getVersion = hlm_version.getVersion


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
