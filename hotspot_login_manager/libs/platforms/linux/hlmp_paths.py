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
def controlSocket():
    ''' Return the path for the daemon's client control socket.
    '''
    return '/tmp/hotspot-login-manager.socket' # FIXME: /tmp so we can test in userland; real value: '/var/run/hotspot-login-manager.socket'


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
