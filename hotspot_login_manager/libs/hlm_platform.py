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
# Description: Handles platform-specific implementations.
#


#-----------------------------------------------------------------------------
import os
import platform
import sys


#-----------------------------------------------------------------------------
#
# Detect the current platform, and exits if it is not supported.
#
__platform = None

if (os.name == 'posix') and (platform.system() == 'Linux'):
  __platform = 'linux'

else:
  print('Sorry, your platform ({0}/{1} {2}) is not supported.'.format(os.name, platform.system(), platform.release()))
  sys.exit(255)


#-----------------------------------------------------------------------------
#
# Load platform-specific modules
#
hlmp_network = None

if __platform == 'linux':
    import hotspot_login_manager.libs.linux.hlmp_network
    hlmp_network = hotspot_login_manager.libs.linux.hlmp_network


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
