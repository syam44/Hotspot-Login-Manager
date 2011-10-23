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
#
from hotspot_login_manager.libs.daemon import hlm_wireless


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
        self.start()

    #-----------------------------------------------------------------------------
    def run(self):
        while True:
            try:
                ifaces = hlm_wireless.getInterfaces()
                if __DEBUG__: logDebug('Checking available wireless interfaces: {0}'.format(str(ifaces)))
                #watched = None
                #ssid_keys = self.__credentials.ssids.keys()
                #for iface in ifaces:
                    #ssid = hlm_wireless.getSSID(iface)
                    #if ssid not in ssid_keys:
                        #watched = self.__credentials.ssids[ssid]
                        #if __DEBUG__: logDebug('Interface {0} with SSID {1} is available and has attached credentials.'.format(quote(iface), quote(ssid)))
                        #break
                    #else:
                        #if __DEBUG__: logDebug('Interface {0} with SSID {1} has no attached credentials.'.format(quote(iface), quote(ssid)))

                #if watched != None:
                    ## TODO: ping / authenticate
                    #pass

            except SystemExit:
                pass
            except BaseException as exc:
                if __DEBUG__: logDebug('hlm_auth.Authenticator.run(): {0}'.format(exc))
            # Wait for the next event
            self.wakeUp.clear()
            self.wakeUp.wait(self.__credentials.delay)


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
