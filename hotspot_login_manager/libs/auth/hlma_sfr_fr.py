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
# Description: Authentication plugin for SFR.FR hotspots
#


#-----------------------------------------------------------------------------
def getSupportedProviders():
    return ['sfr.fr']


#-----------------------------------------------------------------------------
def getSupportedSSIDs():
    return ['SFR WiFi Public']


#-----------------------------------------------------------------------------
def getSupportedRedirectPrefixes():
    return ['https://hotspot.neuf.fr/indexEncryptingChilli.php?']


#-----------------------------------------------------------------------------
def authenticate(redirectURL, connectedSSIDs, credentials, pluginName):
    # TODO
    reportFailure('Plain SFR.FR (without FON) is not yet supported.')


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
