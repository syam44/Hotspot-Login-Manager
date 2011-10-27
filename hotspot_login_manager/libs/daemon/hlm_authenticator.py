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
# Description: Hotspot authenticator controller.
#


#-----------------------------------------------------------------------------
import threading
import time
#
from hotspot_login_manager.libs.daemon import hlm_auth_plugins
from hotspot_login_manager.libs.daemon import hlm_config
from hotspot_login_manager.libs.daemon import hlm_http
#
from hotspot_login_manager.libs.core import hlm_platform
hlm_platform.install(vars(), 'wireless')


#-----------------------------------------------------------------------------
class _WaitForNextEvent(BaseException):
    ''' Dummy exception class that forces the authenticator loop to wait for the next event.
    '''


#-----------------------------------------------------------------------------
class Authenticator(threading.Thread):
    ''' Authenticator controller class.
    '''
    #-----------------------------------------------------------------------------
    def __init__(self, configDaemon, configRelevantPluginCredentials):
        threading.Thread.__init__(self, name = 'Authenticator')
        self.daemon = True
        self.wakeUp = threading.Event()
        self.__configDaemon = configDaemon
        self.__relevantPlugins = configRelevantPluginCredentials
        self.__antiDosWaiting = True
        self.__sleepInterval = max(self.__configDaemon.pingInterval - hlm_config.antiDosPingInterval, 1)
        self.start()


    #-----------------------------------------------------------------------------
    def antiDosWaiting(self):
        ''' Whether we are stuck in the anti-DoS delay, so that the control socket can
            inform its client.
        '''
        return self.__antiDosWaiting


    #-----------------------------------------------------------------------------
    def run(self):
        ''' Main authenticator controller loop.
        '''

        while True:
            try:
                ifaces = getInterfaces()
                if __DEBUG__: logDebug('Checking available wireless interfaces: {0}'.format(str(ifaces)))
                # We don't need to do anything if there is no wireless interface available.
                if ifaces == []:
                    raise _WaitForNextEvent()

                # Do we already have internet access?
                redirectURL = hlm_http.detectRedirect(self.__configDaemon.pingSite)
                if redirectURL == None:
                    if __DEBUG__: logDebug('Ping URL {0} was not redirected. We have internet access.'.format(quote(self.__configDaemon.pingSite)))
                    raise _WaitForNextEvent()

                if __DEBUG__: logDebug('Ping URL {0} was redirected to {1}. Trying to find a plugin that accepts the redirected URL...'.format(quote(self.__configDaemon.pingSite), quote(redirectURL)))

                # Get currently configured SSIDs so the plugins can rely on it too
                connectedSSIDs = [getSSID(iface) for iface in ifaces]
                if __DEBUG__: logDebug('Available SSIDs: {0}'.format(connectedSSIDs))

                # Try each relevant authentication plugin in turn
                for plugin in self.__relevantPlugins:
                    try:
                        # Verify the redirected URL
                        isSupported = False
                        supportedRedirects = plugin.getSupportedRedirectPrefixes()
                        for redirectPrefix in supportedRedirects:
                            if redirectURL.startswith(redirectPrefix):
                                isSupported = True
                                break
                        if not isSupported:
                            continue
                        # Verify the connected SSIDs
                        isSupported = False
                        supportedSSIDs = plugin.getSupportedSSIDs()
                        for ssid in connectedSSIDs:
                            if ssid in supportedSSIDs:
                                isSupported = True
                                break
                        if not isSupported:
                            continue
                        # The plugin matches both the redirectURL and the connected SSIDs, let's try to authenticate!
                        if __DEBUG__: logDebug('AuthPlugin {0} could match, trying to authenticate...'.format(quote(plugin.pluginName)))
                        if plugin.authenticate(redirectURL, connectedSSIDs, plugin.credentials, plugin.pluginName):
                            # If the plugin successfully authenticated us, it must return True so we don't need to try the other plugins
                            if __DEBUG__: logDebug('AuthPlugin {0} authenticated us successfully.'.format(quote(plugin.pluginName)))
                            break
                        else:
                           raise Exception('failed to authenticate (without explanation).')

                    except SystemExit:
                        raise
                    except hlm_http.CertificateError as exc:
                        if __WARNING__: logWarning(exc)
                    except BaseException as exc:
                        if __DEBUG__: logDebug('AuthPlugin {0} FAILURE: {1}'.format(quote(plugin.pluginName), exc))


            except _WaitForNextEvent:
                pass
            except SystemExit:
                pass
            except BaseException as exc:
                if __DEBUG__: logDebug('Authenticator.run(): {0}'.format(exc))

            # Wait for the next event
            time.sleep(hlm_config.antiDosPingInterval)
            self.__antiDosWaiting = False
            self.wakeUp.wait(self.__sleepInterval)
            self.wakeUp.clear()
            self.__antiDosWaiting = True


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
