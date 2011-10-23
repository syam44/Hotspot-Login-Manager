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
# Description: Main program for listing the available providers.
#


#-----------------------------------------------------------------------------
import os
import re
import sys
#
from hotspot_login_manager.libs.core import hlm_application


#-----------------------------------------------------------------------------
def main(args):
    # Just print the contents of the libs/auth directory.
    pluginsPath = hlm_application.getPath() + '/libs/auth'
    regex = re.compile('^hlma_([a-zA-Z0-9_]+).py$')
    plugins = []
    for item in os.listdir(pluginsPath):
        if os.path.isfile(pluginsPath + '/' + item):
            match = regex.search(item)
            if match != None:
                plugins.append(match.group(1))
    plugins.sort()
    print(_('Available authentication providers:'))
    for plugin in plugins:
        print('    ' + plugin)
    sys.exit(0)


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
