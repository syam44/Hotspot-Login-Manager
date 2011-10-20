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
def configPath():
    ''' Return the default directory for the configuration files (daemon and credentials).
    '''
    return '/etc/hotspot-login-manager'


#-----------------------------------------------------------------------------
def daemonConfig():
    ''' Return the default path for the daemon configuration file.
    '''
    return configPath() + '/daemon.conf'


#-----------------------------------------------------------------------------
def credentialsConfig():
    ''' Return the default path for the credentials configuration file.
    '''
    return configPath() + '/credentials.conf'


#-----------------------------------------------------------------------------
def daemonRuntimePath():
    ''' Return the directory for the daemon's runtime files (PID and socket).
    '''
    return '/var/run/hotspot-login-manager'


#-----------------------------------------------------------------------------
def pidFile():
    ''' Return the path for the daemon's PID file.
    '''
    return daemonRuntimePath() + '/hlm.pid'


#-----------------------------------------------------------------------------
def notificationSocket():
    ''' Return the path for the daemon's client notification socket.
    '''
    return daemonRuntimePath() + '/hlm.socket'


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
