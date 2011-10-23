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
# Description: Main program for the notifier client daemon.
#


#-----------------------------------------------------------------------------
import sys
#
from hotspot_login_manager.libs.core import hlm_application
from hotspot_login_manager.libs.notifier import hlm_backend


#-----------------------------------------------------------------------------
def main(args):
    if not hlm_backend.isAvailable():
        sys.exit(1)

    import time
    #
    iteration = 0
    while True:
        iteration += 1
        message = _('Notification #{0}\nIt works!').format(iteration)
        hlm_backend.notify(message, hlm_application.getPath() + '/icons/wireless-connected.png')
        time.sleep(5)

    raise NotImplementedError('NOT IMPLEMENTED: --notifier')

    sys.exit(0)


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
