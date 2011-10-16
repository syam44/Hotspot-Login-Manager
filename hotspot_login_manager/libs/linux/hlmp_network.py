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
# Description: List network interfaces (either all or wifi), and get the SSID of a wifi interface.
#              This is the Linux-specific implementation.
#
#              Most code in this module has been borrowed from python-wifi 0.5.0 by Roman Joost / Sean Robinson (which is also licensed under GPL).
#              We definitely don't need the full IW API, so depending on this third party library makes no sense, especially since it is still alpha and not yet packaged in Debian.
#              http://pythonwifi.wikispot.org/
#


#-----------------------------------------------------------------------------
import array
import fcntl
import re
import socket
import struct


#-----------------------------------------------------------------------------
# Wireless Extensions constants
__WE_IFNAMSIZE      = 16        # max size of an interface name
__WE_ESSID_MAX_SIZE = 32        # max size of an SSID string
__WE_SIOCGIWESSID   = 0x8B1B    # IOCTL: get SSID


#-----------------------------------------------------------------------------
# IOCTL socket
__ioctlSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


#-----------------------------------------------------------------------------
def getInterfaces(wifiOnly = False):
    ''' Return the list of all network interface names.
        If wifiOnly is True, only the wireless interfaces are returned.

        Uses /prov/net/dev or /proc/net/wireless under the hood.
    '''
    regex = re.compile('^ *([a-z]{2,}[0-9]*):')
    ifaces = []

    if wifiOnly == True:
        fd = open('/proc/net/wireless', 'r')
    else:
        fd = open('/proc/net/dev', 'r')

    for line in fd:
        try:
            ifaces.append(regex.search(line).group(1))
        except AttributeError:
            pass

    fd.close()
    return ifaces


#-----------------------------------------------------------------------------
def getSSID(iface):
    ''' Return the SSID of the specified wireless interface.
        If iface does not designate a valid wireless interface, return None.

        Uses IOCTLs under the hood.
    '''
    if iface not in getInterfaces(True):
      return None
    iwpoint = __IwPoint('\x00' * __WE_ESSID_MAX_SIZE)
    status, result = __IW_GetExtension(iface, __WE_SIOCGIWESSID, iwpoint.packed)
    return iwpoint.result.tostring().strip('\x00')


#-----------------------------------------------------------------------------
class __IwPoint(object):
    ''' Store iw_point data.
    '''
    def __init__(self, data, flags = 0):
        self.result = array.array('c', data)
        caddr_t, length = self.result.buffer_info()
        # Format: P pointer to data, H length, H flags
        self.packed = struct.pack('PHH', caddr_t, length, flags)


#-----------------------------------------------------------------------------
def __IW_GetExtension(ifname, ioctlRequest, data = None):
    ''' Read information from ifname.
    '''
    padding = __WE_IFNAMSIZE - len(ifname)
    request = array.array('c', ifname + '\0' * padding)
    # put some additional data behind the interface name
    if data is not None:
        request.extend(data)
    else:
        padding = 32
        request.extend('\0' * padding)

    result = fcntl.ioctl(__ioctlSocket.fileno(), ioctlRequest, request)
    return (result, request[__WE_IFNAMSIZE:])


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
