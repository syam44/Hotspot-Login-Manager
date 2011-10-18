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
#
from hotspot_login_manager.libs.core import hlm_application
from hotspot_login_manager.libs.core import hlm_plugin


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
# Detect the current platform, and exit if it is not supported.
#
_platform = None

if (os.name == 'posix') and (platform.system() == 'Linux'):
    _platform = 'linux'

else:
    print(_('Sorry, your platform ({0}/{1} {2}) is not supported.').format(os.name, platform.system(), platform.release()))
    sys.exit(255)

#
# Plugins path for the current platform.
#
_platformPluginsPath = hlm_application.getPath() + '/libs/platforms/' + _platform


#-----------------------------------------------------------------------------
def install(wrapperVars, moduleName):
    ''' Import moduleName and install into the wrapper module every public
        variable/function/class it defines.
        Modules imported by moduleName are not installed into the wrapper.

        Public items are the ones NOT starting with an underscore.

        Usage:
            from hotspot_login_manager.libs.core import hlm_platform
            hlm_platform.install(vars(), 'module')
    '''
    moduleObject = hlm_plugin.load('hlmp_' + moduleName, _platformPluginsPath, 'platform')
    moduleVars = vars(moduleObject)
    for varName in moduleVars.keys():
        varObject = moduleVars[varName]
        if (not type(varObject) is types.ModuleType) and (not varName.startswith('_')):
            wrapperVars[varName] = varObject


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
