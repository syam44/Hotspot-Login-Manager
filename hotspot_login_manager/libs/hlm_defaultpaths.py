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
# Description: Default filesystem paths.
#


#-----------------------------------------------------------------------------
# Import the platform-specific implementation.
from hotspot_login_manager.libs import hlm_platform
hlm_platform.install(vars(), hlm_platform.hlmp_defaultpaths)


#-----------------------------------------------------------------------------
import os


#-----------------------------------------------------------------------------
#
# Application root path.
# We know this module is located in the hotspot_login_manager/libs directory
# so we just go up two levels.
#
__applicationPath = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../..')

def application():
    ''' Return the root path of the application.
    '''
    return __applicationPath


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
