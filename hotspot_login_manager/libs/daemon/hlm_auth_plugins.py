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
# Description: Authentication plugins loader.
#


#-----------------------------------------------------------------------------
''' This module pre-loads all authentication plugins that live in libs/auth
    and checks that they are in the correct format.

    An authentication plugin should provide four functions:

        getSupportedProviders(): returns a list of strings that indicates which
            service providers this plugin supports. It is needed to allow credentials
            sharing across several different authentication plugins.
            eg. SSID "SFR WiFi FON" supports both Neuf/SFR and FON credentials,
            while SSID "FON" only supports FON credentials and SSID "SFR WiFi Public"
            only supports Neuf/SFR credentials.

        getSupportedSSIDs(): returns a list of strings that indicates which WiFi SSIDs
            are supported by this plugin.

        getSupportedRedirectPrefixes(): returns a list of strings that indicates which
            redirected URL prefixes are supported by this plugin. Those strings are matched
            against the actual redirectURL using "redirectURL.startswith(supportedPrefix)".

        authenticate(redirectURL, connectedSSIDs, credentials, pluginName):
            tries to authenticate on the hotspot's Wifi network using "credentials", provided
            the "redirectURL" and "connectedSSIDs" match the ones supported by this plugin.

            "redirectURL" is the URL to which our ping test was redirected to.

            "connectedSSIDs" is just a list of SSID strings to which the computer
                             is currently connected to.

            "credentials" is a dictionary of the form { provider: (user, password) }

            "pluginName" is the plugin's name, for e.g. clean debugging output.
'''


#-----------------------------------------------------------------------------
import os
import re
#
from hotspot_login_manager.libs.core import hlm_application
from hotspot_login_manager.libs.core import hlm_plugin


#-----------------------------------------------------------------------------
class _Status(BaseException):
    ''' Base class for reporting a plugin's status to the authenticator controller.
    '''
    def __init__(self, plugin, message):
        BaseException.__init__(self)
        self.plugin = plugin
        self.message = message


#-----------------------------------------------------------------------------
class Status_Error(_Status):
    ''' An authentification plugin should raise this exception when the captive
        portal is not recognized.
        This could be either because the plugin is not supposed to handle that portal,
        or because the portal's connection protocol has changed.
    '''


#-----------------------------------------------------------------------------
class Status_WrongCredentials(_Status):
    ''' An authentification plugin should raise this exception when the captive
        portal does not accept the credentials.
    '''
    def __init__(self, plugin, credentials):
        message = _('The hotspot rejected your {0} credentials.').format(quote(credentials))
        Status_Error.__init__(self, plugin, message)


#-----------------------------------------------------------------------------
class Status_Success(_Status):
    ''' An authentification plugin should raise this exception when it successfully
        logged in into the captive portal.
    '''
    def __init__(self, plugin, credentials):
        message = _('Successfully connected to the hotspot using your {0} credentials.').format(quote(credentials))
        _Status.__init__(self, plugin, message)


#-----------------------------------------------------------------------------
def getAuthPlugins():
    ''' Load all the authentication plugins.
    '''
    if getAuthPlugins.__cachePlugins == None:
        pluginsPath = hlm_application.getPath() + '/libs/auth'
        regex = re.compile('^hlma_([a-zA-Z0-9_]+).py$')
        plugins = []
        providers = set()
        for item in os.listdir(pluginsPath):
            if os.path.isfile(pluginsPath + '/' + item):
                match = regex.search(item)
                if match != None:
                    try:
                        pluginModule = hlm_plugin.load(item[:-3], pluginsPath, 'auth')
                        pluginProviders = pluginModule.getSupportedProviders()
                        providers = providers.union(pluginProviders)
                        pluginModule.pluginName = match.group(1)
                        plugins.append(pluginModule)
                    except SystemExit:
                        raise
                    except BaseException as exc:
                        if __WARNING__: logWarning(_('Invalid authentication plugin {0}: {1}').format(quote(item), exc))
        # Normalize the providers list
        providers = [provider for provider in providers]
        providers.sort()
        if providers == []:
            raise FatalError(_('No authentication plugin available / no supported service provider, exiting.'))
        # Cache the results
        getAuthPlugins.__cachePlugins = plugins
        getAuthPlugins.__cacheProviders = providers

    return getAuthPlugins.__cachePlugins

#
# Cached results
#
getAuthPlugins.__cachePlugins = None
getAuthPlugins.__cacheProviders = None


#-----------------------------------------------------------------------------
def getSupportedProviders():
    ''' Return the list of all supported service providers.
    '''
    if getAuthPlugins.__cacheProviders == None:
        getAuthPlugins()
    return getAuthPlugins.__cacheProviders


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
