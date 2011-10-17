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
# Description: Various filesystem paths.
#              This is the Linux-specific implementation.
#


#-----------------------------------------------------------------------------
def defaultConfigFile():
    ''' Return the default path for the configuration file.
    '''
    return '/etc/hotspot-login-manager.conf'


#-----------------------------------------------------------------------------
def daemonPID():
    ''' Return the path for the daemon's PID file.
    '''
    return '/var/run/hotspot-login-manager.pid'


#-----------------------------------------------------------------------------
def notificationSocket():
    ''' Return the path for the daemon's client notification socket.
    '''
    return '/var/run/hotspot-login-manager.socket'


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
