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
# Description: Main program for the system daemon.
#


#-----------------------------------------------------------------------------
import sys
#
from hotspot_login_manager.libs.core import hlm_daemonize


#-----------------------------------------------------------------------------
def main(args):

    #
    # TODO: read daemon.conf
    #
    args.daemonCredentials = ''

    # TODO: makedir(hlm_paths.daemonRuntimePath())
    hlm_daemonize.daemonize(
                            umask = 0o644,
                            logLevel = args.logLevel,
                            pidFile = '/tmp/hotspot-login-manager.pid', # hlm_paths.pidFile()
                           )

    from hotspot_login_manager.libs.daemon import hlm_wireless
    #
    wirelessIfaces = hlm_wireless.getInterfaces()
    logInfo('Wireless interfaces:', str(wirelessIfaces))
    for iface in wirelessIfaces:
        logInfo('   ', iface, '=', hlm_wireless.getSSID(iface))

    raise NotImplementedError('NOT IMPLEMENTED: --daemon')

    sys.exit(0)


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
