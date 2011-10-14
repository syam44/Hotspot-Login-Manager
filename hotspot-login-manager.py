#!/usr/bin/python2.7
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


import hotspotlm.libs.network


def main():
    print 'All interfaces', hotspotlm.libs.network.getInterfaces(wifiOnly = False)
    wirelessIfaces = hotspotlm.libs.network.getInterfaces(wifiOnly = True)
    print 'Wireless interfaces', wirelessIfaces
    for iface in wirelessIfaces:
      print '    ', iface, '=', hotspotlm.libs.network.getSSID(iface)
    return 0


if __name__ == '__main__':
   main()


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
