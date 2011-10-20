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
# Description: Define a few global functions and classes.
#


#-----------------------------------------------------------------------------
''' Module usage:
        This module automatically installs the required functions and classes in every single module.

        Every module has access to the following services:
            quote() allows to wrap its argument (either a list or a string) into pretty quotes « » (cf. _quote())
            FatalError as it name implies should not be trapped anywhere else than in the main script.

        In order to correctly initialize the global services, the main script (hotspot-login-manager)
        must import hlm_globals as early as possible (just after core/hlm_log).
'''


#-----------------------------------------------------------------------------
import sys


#-----------------------------------------------------------------------------
def _quote(arg):
    ''' Wrap arg into pretty quotes.
        If arg is a list each individual item will be quoted, and joined with ', '.
    '''
    if isinstance(arg, list):
        return '«' + '», «'.join(arg) + '»'
    return '«' + str(arg) + '»'


#-----------------------------------------------------------------------------
class _FatalError(Exception):
    ''' FatalError as it name implies should not be trapped anywhere else than in the main script.
    '''


#-----------------------------------------------------------------------------
#
# Install the functions and classes globally. They will be available to every module.
#
globals()['__builtins__']['quote'] = _quote
globals()['__builtins__']['FatalError'] = _FatalError


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
