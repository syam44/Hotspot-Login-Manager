# -*- coding:utf-8 -*-
#
# hotspot-login-manager
# https://github.com/syam44/Hotspot-Login-Manager
#
# Distributed under the GNU General Public License version 3
# https://www.gnu.org/copyleft/gpl.html
#
# Authors: thuban (thuban@singularity.fr)  

# Description : Code to load config



try:
        import sys
        import os
        import ConfigParser

except ImportError as err:
        print ("Couldn't load module. {0}".format(err)) 
        sys.exit(2)


# As prototype, configfile is located in ~/.hlmrc.

CONFIGFILE = os.path.expanduser('~/.hlmrc')

def loadConfig(configfile, plugin):
    '''Return the login and password for a specified plugin

    plugin is either FreeWifi, Neuf, Bouygues... . For a plugin,
    the configfile has informations about login and password to
    use to authentify.
    plugin is also the name of a section in the configfile
    '''
    
    config = ConfigParser.ConfigParser()
    try:
        config.read(configfile)
    except TypeError:
        sys.exit('Can\'t load the config file')
    if config.has_section(plugin):
        login = config.get(plugin, login)
        password = config.get(plugin, password)
        return(login,password)
    else :
        sys.exit('Pas de configuration pour ce plugin')





# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

