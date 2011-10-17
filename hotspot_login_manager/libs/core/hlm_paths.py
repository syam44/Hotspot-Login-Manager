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
# Description: Various filesystem paths.
#


#-----------------------------------------------------------------------------
# Import the platform-specific implementation.
from hotspot_login_manager.libs.core import hlm_platform

hlm_platform.install(vars(), 'paths')


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
