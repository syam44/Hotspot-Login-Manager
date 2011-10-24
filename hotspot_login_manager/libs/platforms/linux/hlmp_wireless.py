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
# Description: List all active wireless network interfaces, and get the SSID of an interface.
#              This is the Linux-specific implementation.
#
#              Most code in this module has been borrowed from python-wifi 0.5.0 by Roman Joost, Sean Robinson et al. (which is also licensed under the GPL, originally v2).
#                  http://pypi.python.org/pypi/python-wifi/
#                  http://pythonwifi.wikispot.org/
#              We definitely don't need the full IW API, so depending on this library makes no sense, especially since it is still alpha and not yet packaged in Debian.
#


#-----------------------------------------------------------------------------
import array
import fcntl
import re
import socket
import struct


#-----------------------------------------------------------------------------
#
# Wireless Extensions constants
#
_WE_IFNAMSIZE      = 16        # max size of an interface name
_WE_ESSID_MAX_SIZE = 32        # max size of an SSID string
_WE_SIOCGIWESSID   = 0x8B1B    # IOCTL: get SSID


#-----------------------------------------------------------------------------
#
# IOCTL socket
#
_ioctlSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
_ioctlSocket.settimeout(None)

#
# Pre-compiled regular expression
#
_networkInterfacesRegex = re.compile('^ *([a-z]{2,}[0-9]*):')


#-----------------------------------------------------------------------------
def getInterfaces():
    ''' Return the list of all active (connected) wireless network interface.

        Uses /proc/net/wireless under the hood.
    '''
    ifaces = []
    try:
        with open('/proc/net/wireless', 'r') as devices:
            for device in devices:
                try:
                    ifaces.append(_networkInterfacesRegex.search(device).group(1))
                except SystemExit:
                    raise
                except BaseException:
                    pass
    except SystemExit:
        raise
    except BaseException:
        pass
    return ifaces


#-----------------------------------------------------------------------------
def getSSID(iface):
    ''' Return the SSID of the specified wireless interface.
        If iface does not designate a connected wireless interface, return None.

        Uses IOCTLs under the hood.
    '''
    if iface in getNetworkInterfaces(True):
        try:
            iwpoint = _IwPoint('\x00' * _WE_ESSID_MAX_SIZE)
            (status, result) = _IW_GetExtension(iface, _WE_SIOCGIWESSID, iwpoint.packed)
            return iwpoint.result.tostring().strip('\x00')
        except SystemExit:
            raise
        except BaseException:
            pass
    return None


#-----------------------------------------------------------------------------
class _IwPoint(object):
    ''' Store iw_point data.
    '''
    #-----------------------------------------------------------------------------
    def __init__(self, data, flags = 0):
        self.result = array.array('c', data)
        (caddr_t, length) = self.result.buffer_info()
        # Format: P pointer to data, H length, H flags
        self.packed = struct.pack('PHH', caddr_t, length, flags)


#-----------------------------------------------------------------------------
def _IW_GetExtension(ifname, ioctlRequest, data = None):
    ''' Read information from ifname.
    '''
    padding = _WE_IFNAMSIZE - len(ifname)
    request = array.array('c', ifname + ('\0' * padding))
    # put some additional data behind the interface name
    if data is not None:
        request.extend(data)
    else:
        padding = 32
        request.extend('\0' * padding)

    result = fcntl.ioctl(_ioctlSocket.fileno(), ioctlRequest, request)
    return (result, request[_WE_IFNAMSIZE:])


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
