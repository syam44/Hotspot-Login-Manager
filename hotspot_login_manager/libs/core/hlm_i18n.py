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
# Description: i18n gettext wrapper
#


#-----------------------------------------------------------------------------
''' I18N module usage:
        This module automatically installs the required translator functions in every single module
        so there is no need to import hlm_i18n to use the translation services (except from the main
        script, see below).

        Every module can access translation services using the following functions:
            _()  is the basic string translator (one to one mapping, cf. gettext.lgettext).
            _N() is the plural string translator (mapping depends on the counter, cf. gettext.lngettext).

        In order to correctly initialize the translation services, the main script (hotspot-login-manager)
        must import hlm_i18n as early as possible (it really should be the first HLM import).

        See hotspot_login_manager/lang/README for information about translation files (.pot / .po / .mo).
'''


#-----------------------------------------------------------------------------
import gettext
#
from hotspot_login_manager.libs.core import hlm_application


#-----------------------------------------------------------------------------
#
# Bind the gettext functions to the locales directory and domain.
#
_localeDir = hlm_application.getPath() + '/lang'
gettext.bindtextdomain('hotspot-login-manager', _localeDir)
gettext.textdomain('hotspot-login-manager')
_localeDir = None


#-----------------------------------------------------------------------------
#
# Install the translator functions globally. They will be available to every module.
#
#       _()  is the basic string translator (one to one mapping, cf. gettext.lgettext).
#       _N() is the plural string translator (mapping depends on the counter, cf. gettext.lngettext).
#
_builtinVars = vars()['__builtins__']
_builtinVars['_'] = gettext.lgettext
_builtinVars['_N'] = gettext.lngettext
_builtinVars = None


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
