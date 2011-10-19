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
def load(moduleName, searchPath, applicationDomain):
    ''' Dynamically load a plugin module knowing its name and path.
        Return the module object.
    '''
    # Lock the import global mutex
    imp.acquire_lock()
    try:
        # Just try to return something from the registry. If it fails then we must actually load the module.
        try:
            return _registry[applicationDomain][moduleName]
        except KeyError:
            pass

        # Check module name to guard against directory traversal and other annoyances.
        if _moduleNameRegex.search(moduleName) == None:
            ImportError(_('Invalid plugin name {0}.').format(moduleName))
        searchPath = os.path.realpath(searchPath)

        # Try to find the relevant module. If an exception arises, let the caller handle it.
        moduleObject = imp.load_source(moduleName, searchPath + '/' + moduleName + '.py')
        # Register the plugin locally (we don't want to rely solely on the global modules namespace)
        if applicationDomain not in _registry.keys():
            _registry[applicationDomain] = {}
        _registry[applicationDomain][moduleName] = moduleObject
        return moduleObject
    finally:
        # Release import global mutex
        imp.release_lock()


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
