#!/usr/bin/python3.1
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
# Description: Main program.
#


#-----------------------------------------------------------------------------
import sys
#
from hotspot_login_manager.libs import hlm_args
from hotspot_login_manager.libs.core import hlm_application
from hotspot_login_manager.libs.core import hlm_plugin


#-----------------------------------------------------------------------------
def main():
    args = hlm_args.parse()

    #
    # Sample code below
    #

    # --daemon
    if args.runDaemon:
        from hotspot_login_manager.libs.network import hlm_wireless
        #
        print(_('All interfaces'), hlm_wireless.getNetworkInterfaces(wirelessOnly = False))
        wirelessIfaces = hlm_wireless.getNetworkInterfaces(wirelessOnly = True)
        print(_N('Wireless interface', 'Wireless interfaces', len(wirelessIfaces)), wirelessIfaces)
        for iface in wirelessIfaces:
            print('    ', iface, '=', hlm_wireless.getSSID(iface))

    # --notifier=kde4
    if args.notifierBackend != None:
        import time
        from hotspot_login_manager.libs import hlm_notifier
        #
        notifier = hlm_notifier.NotificationBackend(args.notifierBackend)
        iteration = 0
        while True:
            iteration += 1
            message = _('Notification #{0}\nIt works!').format(iteration)
            notifier.notify(message)
            time.sleep(5)

    sys.exit(0)


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
