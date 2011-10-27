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
# Description: Authentication plugin for FREE.FR hotspots
#


#-----------------------------------------------------------------------------
def getSupportedProviders():
    return ['free.fr']


#-----------------------------------------------------------------------------
def getSupportedSSIDs():
    return ['FreeWifi']


#-----------------------------------------------------------------------------
def getSupportedRedirectPrefixes():
    return ['https://wifi.free.fr/?url=']


#-----------------------------------------------------------------------------
def authenticate(redirectURL, connectedSSIDs, credentials, pluginName):
    # TODO
    reportFailure('FREE.FR is not yet supported.')


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
