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
# Description: Dynamic plugin loading.
#


#-----------------------------------------------------------------------------
import imp
import os
import re


#-----------------------------------------------------------------------------
#
# Register all dynamically loaded plugins here.
#
_registry = {}

#
# Pre-compiled regular expression.
#
_moduleNameRegex = re.compile('^[a-zA-Z0-9_]+$')


#-----------------------------------------------------------------------------
def load(moduleName, searchPath):
    ''' Dynamically load a plugin module knowing its name and path.
        Return the module object.
    '''
    # Check module name to guard against directory traversal and other annoyances.
    if _moduleNameRegex.search(moduleName) == None:
        raise ImportError('Invalid module name {0}'.format(moduleName))

    searchPath = os.path.realpath(searchPath)
    # Lock the import global mutex
    imp.acquire_lock()
    try:
        # Just try to return something from the registry. If it fails then we must actually load the module.
        try:
            return _registry[searchPath][moduleName]
        except KeyError:
            pass
        # Try to find the relevant module. If an exception arises, let the caller handle it.
        moduleObject = imp.load_source(moduleName, searchPath + '/' + moduleName + '.py')
        if moduleObject != None:
            if searchPath not in _registry.keys():
                _registry[searchPath] = {}
            _registry[searchPath][moduleName] = moduleObject
        return moduleObject
    finally:
        # Release import global mutex
        imp.release_lock()


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
