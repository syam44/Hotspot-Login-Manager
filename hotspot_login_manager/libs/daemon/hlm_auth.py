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
from hotspot_login_manager.libs.daemon import hlm_config
from hotspot_login_manager.libs.daemon import hlm_http_redirect
from hotspot_login_manager.libs.daemon import hlm_wireless


#-----------------------------------------------------------------------------
class _WaitForNextEvent(BaseException):
    ''' Dummy exception class that forces the authenticator loop to wait for the next event.
    '''


#-----------------------------------------------------------------------------
class Authenticator(threading.Thread):
    ''' Authenticator controller class.
    '''
    #-----------------------------------------------------------------------------
    def __init__(self, credentials):
        threading.Thread.__init__(self, name = 'Authenticator')
        self.daemon = True
        self.wakeUp = threading.Event()
        self.__credentials = credentials
        self.__antiDosWaiting = True
        self.__eventDelay = max(self.__credentials.delay - hlm_config.antiDosPingDelay, 1)
        self.start()


    #-----------------------------------------------------------------------------
    def antiDosWaiting(self):
        ''' Whether we are stuck in the anti-DoS delay, so that the control socket can
            inform its client.
        '''
        return self.__antiDosWaiting


    #-----------------------------------------------------------------------------
    def run(self):
        while True:
            try:
                ifaces = hlm_wireless.getInterfaces()
                if __DEBUG__: logDebug('Checking available wireless interfaces: {0}'.format(str(ifaces)))
                # We don't need to do anything if there is no wireless interface available.
                # FIXME: this is disabled for development purposes
                #if ifaces == []:
                #    raise _WaitForNextEvent()

                # Do we already have internet access?
                redirect = hlm_http_redirect.detectRedirect(self.__credentials.ping)
                if redirect == None:
                    if __DEBUG__: logDebug('URL {0} was not redirected. We have internet access.'.format(quote(self.__credentials.ping)))
                    raise _WaitForNextEvent()
                if __DEBUG__: logDebug('URL {0} was redirected to {1}. Trying to find a plugin that accepts the redirected URL...'.format(quote(self.__credentials.ping), quote(redirect)))

                # Get currently configured SSIDs so the plugins can rely on it too
                ssids = [hlm_wireless.getSSID(iface) for iface in ifaces]
                if __DEBUG__: logDebug('Available SSIDs: {0}'.format(ssids))

                #
                # TODO: find relevant plugin (also provide SSIDs)
                #

            except _WaitForNextEvent:
                pass
            except SystemExit:
                pass
            except BaseException as exc:
                if __DEBUG__: logDebug('hlm_auth.Authenticator.run(): {0}'.format(exc))

            # Wait for the next event
            time.sleep(hlm_config.antiDosPingDelay)
            #
            self.__antiDosWaiting = False
            self.wakeUp.clear()
            self.wakeUp.wait(self.__eventDelay)
            self.__antiDosWaiting = True


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
