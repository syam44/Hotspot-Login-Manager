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
# Description: List network interfaces (either all or wifi), and get the SSID of a wifi interface.
#              This is a wrapper around the platform-specific implementations.
#


#-----------------------------------------------------------------------------
from hotspot_login_manager.libs import hlm_platform


#-----------------------------------------------------------------------------
#
# getInterfaces(wifiOnly = False):
#     Return the list of all network interface names.
#     If wifiOnly is True, only the wireless interfaces are returned.
#
getInterfaces = hlm_platform.hlmp_network.getInterfaces
#
# getSSID(iface):
#     Return the SSID of the specified wireless interface.
#     If iface does not designate a valid wireless interface, return None.
#
getSSID = hlm_platform.hlmp_network.getSSID


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
