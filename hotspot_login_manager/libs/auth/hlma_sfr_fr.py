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
# Description: Authentication plugin: sfr.fr
#


#-----------------------------------------------------------------------------
from hotspot_login_manager.libs.daemon import hlm_http


#-----------------------------------------------------------------------------
def authenticate(user, password, redirect, ssids, pluginName):
    if __DEBUG__: logDebug('Checking AuthPlugin {0}.'.format(quote(pluginName)))

    #
    # Filter out the URLs we don't handle
    #
    if not redirect.startswith('https://hotspot.neuf.fr/indexEncryptingChilli.php?'):
        if __DEBUG__: logDebug('AuthPlugin {0} did not recognize the redirect URL.'.format(quote(pluginName)))
        return False
    if __DEBUG__: logDebug('AuthPlugin {0} may handle the redirect URL.'.format(quote(pluginName)))

    #
    # TODO: filter out SSIDs?
    #

    # Get the corresponding page
    result = hlm_http.urlOpener().open(redirect)
    result.close()
    if __DEBUG__: logDebug('AuthPlugin {0} successfully grabbed the login webpage.'.format(quote(pluginName)))

    return False


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
