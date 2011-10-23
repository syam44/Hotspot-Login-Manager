#!/usr/bin/python3.1
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
# Description: Entry point.
#
# Note: Keeping the main script to the bare minimum enhances load-time
#       thanks to precompiled .pyc files.
#       So yeah, *bare* minimum.
#


#-----------------------------------------------------------------------------
import sys # This must be imported first to ensure sys.exit() works
try:
    from hotspot_login_manager.libs import hlm_main

except ImportError as err:
    print('Couldn\'t load module: {0}'.format(err), file = sys.stderr)
    sys.exit(255)


#-----------------------------------------------------------------------------
if __name__ == '__main__':
   hlm_main.main()


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
