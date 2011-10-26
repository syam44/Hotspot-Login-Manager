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
# Description: Maximum number of open file descriptors for the current process.
#              This is the BSD-specific implementation.
#
#              This platform-specific file has no wrapper module.
#              It is installed directly in daemon/hlm_daemonize
#


#-----------------------------------------------------------------------------
import resource


#-----------------------------------------------------------------------------
def maxFileDescriptors():
    ''' Maximum number of open file descriptors for the current process.
    '''
    (softLimit, hardLimit) = resource.getrlimit(resource.RLIMIT_OFILE)
    if softLimit == resource.RLIM_INFINITY:
        FatalError(_('[BUG] The maximum number of open file descriptors is infinite, HLM can\'t handle that safely. Exiting.'))
    return softLimit


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
