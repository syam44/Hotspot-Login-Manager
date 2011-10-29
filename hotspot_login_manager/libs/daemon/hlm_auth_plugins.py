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

    An authentication plugin should provide three functions:

        getSupportedProviders(): returns a dictionary of the form { provider: [ssids] }
            that indicates which service providers this plugin supports, and which SSIDs
            support this particular service provider.
            It is needed to allow credentials sharing across several different authentication plugins.
            See sfr_fr_fon plugin for a full example.

        getSupportedRedirectPrefixes(): returns a list of strings that indicates which
            redirected URL prefixes are supported by this plugin. Those strings are matched
            against the actual redirectURL using "redirectURL.startswith(supportedPrefix)".

        authenticate(redirectURL, connectedSSIDs):
            tries to authenticate on the hotspot's Wifi network using "credentials", provided
            the "redirectURL" and "connectedSSIDs" match the ones supported by this plugin.

            "redirectURL" is the URL to which our ping test was redirected to.

            "connectedSSIDs" is just a list of SSID strings to which the computer
                             is currently connected to.

    The following module variables are reserved and should not be used (they will be
    automatically populated by the plugin loader / config parser):

        pluginName: contains the plugin's name, for e.g. clean debugging output.

        pluginCredentials: a dictionary of the form { provider: (user, password) } that
                           only contains the relevant credentials for this particular plugin.
                           (added by daemon/hlm_config)

        supportedSSIDs: a list of all the SSIDs supported by the plugin,
                        computed from the getSupportedProviders() dictionary.
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
        allProviders = {}
        for item in os.listdir(pluginsPath):
            if os.path.isfile(pluginsPath + '/' + item):
                match = regex.search(item)
                if match != None:
                    try:
                        pluginModule = hlm_plugin.load(item[:-3], pluginsPath, 'auth')
                        pluginModule.pluginName = match.group(1)
                        # Compute the supported providers, supported SSIDs etc
                        pluginProviders = pluginModule.getSupportedProviders()
                        pluginSSIDs = set()
                        for provider in pluginProviders:
                            pluginSSIDs = pluginSSIDs.union(pluginProviders[provider])
                        pluginModule.supportedSSIDs = list(pluginSSIDs)
                        # Merge the supported plugin providers/SSIDs in the global cache
                        for provider in pluginProviders:
                            if pluginProviders[provider] != []:
                                if provider not in allProviders:
                                    allProviders[provider] = set()
                                allProviders[provider] = allProviders[provider].union(pluginProviders[provider])
                        # Add the plugin
                        plugins.append(pluginModule)
                    except SystemExit:
                        raise
                    except BaseException as exc:
                        if __WARNING__: logWarning(_('Invalid authentication plugin {0}: {1}').format(quote(item), exc))
        # Normalize the providers list
        if allProviders == {}:
            raise FatalError(_('No authentication plugin available / no supported service provider, exiting.'))
        for provider in allProviders:
            allProviders[provider] = list(allProviders[provider])
            allProviders[provider].sort()
        # Cache the results
        getAuthPlugins.__cachePlugins = plugins
        getAuthPlugins.__cacheProviders = allProviders

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
