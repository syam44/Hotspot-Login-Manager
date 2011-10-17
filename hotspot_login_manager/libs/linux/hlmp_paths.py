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
def clientNotifierSocket():
    ''' Return the path for the daemon's client notifier socket.
    '''
    return '/var/run/hotspot-login-manager.notifier.socket'


#-----------------------------------------------------------------------------
def clientControlSocket():
    ''' Return the path for the daemon's client control socket.
    '''
    return '/var/run/hotspot-login-manager.control.socket'


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
