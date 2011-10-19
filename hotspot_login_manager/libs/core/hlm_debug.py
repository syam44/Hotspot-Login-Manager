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
# Description: Debug wrapper for print().
#


#-----------------------------------------------------------------------------
''' Module usage:
        Install debug() as a global function, in every single module.
        Its semantics are the same as print() except it always prints to stderr.
'''


#-----------------------------------------------------------------------------
import sys


#-----------------------------------------------------------------------------
def _debug(*args):
    print('[DEBUG]  ', *args, file = sys.stderr)


#-----------------------------------------------------------------------------
#
# Install the wrapper globally.
#
_builtinVars = vars()['__builtins__']
_builtinVars['debug'] = _debug
_builtinVars = None


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
