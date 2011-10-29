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
    # See daemon/hlm_auth_plugins
    return { 'free.fr': [], # TODO: ['FreeWifi'],
           }


#-----------------------------------------------------------------------------
def getSupportedRedirectPrefixes():
    return ['https://wifi.free.fr/?url=']


#-----------------------------------------------------------------------------
def authenticate(redirectURL, connectedSSIDs):
    # TODO
    reportFailure('FREE.FR is not yet supported.')


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
