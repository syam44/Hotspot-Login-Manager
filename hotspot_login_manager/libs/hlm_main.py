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


import hotspot_login_manager.libs.core.hlm_debug
#-----------------------------------------------------------------------------
# Do not import any HLM module before this one, translation services are needed everywhere!
import hotspot_login_manager.libs.core.hlm_i18n
#
import sys
#
from hotspot_login_manager.libs.core import hlm_args


#-----------------------------------------------------------------------------
def main():
    args = hlm_args.args()
    #
    # Sample code below
    #

    # --daemon
    if args.runDaemon:
        from hotspot_login_manager.libs.daemon import hlm_wireless
        #
        wirelessIfaces = hlm_wireless.getInterfaces()
        debug('Wireless interfaces:', wirelessIfaces)
        for iface in wirelessIfaces:
            debug('   ', iface, '=', hlm_wireless.getSSID(iface))

    # --notifier=kde4
    if args.runNotifier:
        import time
        from hotspot_login_manager.libs.core import hlm_daemonize
        from hotspot_login_manager.libs.notifier import hlm_backends
        #
        hlm_daemonize.daemonize(pidFile = '/tmp/hotspot-login-manager.pid')
        notifier = hlm_backends.NotificationBackend(args.notifierBackend)
        iteration = 0
        while True:
            iteration += 1
            message = _('Notification #{0}\nIt works!').format(iteration)
            notifier.notify(message)
            time.sleep(5)

    sys.exit(0)


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
