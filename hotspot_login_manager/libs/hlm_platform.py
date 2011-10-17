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
import types


#-----------------------------------------------------------------------------
#
# We require at least Python 3.1
#
(_python_major, _python_minor, _python_release) = platform.python_version_tuple()
(_python_major, _python_minor) = (int(_python_major), int(_python_minor))
if (_python_major < 3) or ((_python_major == 3) and (_python_minor < 1)):
    print(_('Sorry, the Python interpreter version must be at least 3.1 but yours is {0}.{1}.').format(_python_major, _python_minor))
    sys.exit(255)


#-----------------------------------------------------------------------------
#
# Detect the current platform, and exits if it is not supported.
#
_platform = None

if (os.name == 'posix') and (platform.system() == 'Linux'):
    _platform = 'linux'

else:
    print(_('Sorry, your platform ({0}/{1} {2}) is not supported.').format(os.name, platform.system(), platform.release()))
    sys.exit(255)


#-----------------------------------------------------------------------------
#
# Load platform-specific modules
#
hlmp_paths = None
hlmp_wifi = None


if _platform == 'linux':
    # hlmp_paths
    import hotspot_login_manager.libs.linux.hlmp_paths
    hlmp_paths = hotspot_login_manager.libs.linux.hlmp_paths
    # hlmp_wifi
    import hotspot_login_manager.libs.linux.hlmp_wifi
    hlmp_wifi = hotspot_login_manager.libs.linux.hlmp_wifi


#-----------------------------------------------------------------------------
def install(wrapperVars, importModule):
    ''' Install every public variable/function/class defined in importModule
        into the wrapper module.
        Modules imported by importModule are not installed into the wrapper.

        Public items are the ones NOT starting with an underscore.

        Usage:
            from hotspot_login_manager.libs import hlm_platform
            hlm_platform.install(vars(), hlm_platform.hlmp_module)
    '''
    moduleVars = vars(importModule)
    for varName in moduleVars.keys():
        varObject = moduleVars[varName]
        if (not type(varObject) is types.ModuleType) and (not varName.startswith('_')):
            wrapperVars[varName] = varObject


#-----------------------------------------------------------------------------
def getPlatform():
    ''' Return the current platform.

        Currently supported:
            linux
    '''
    return _platform


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
