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
        must import hlm_i18n as early as possible (ideally it should be the first import).

        Run the provided devtools/i18n-gen-pot script in a shell to extract the strings
        as a .pot file in hotspot_login_manager/lang.

        Once the translation is ready as a LOCALENAME.po file, put it in hotspot_login_manager/lang
        and run the provided devtools/i18n-gen-mo to create the catalog bundles.
'''


#-----------------------------------------------------------------------------
import gettext
#
from hotspot_login_manager.libs import hlm_defaultpaths


#-----------------------------------------------------------------------------
#
# Bind the gettext functions to the locales directory and domain.
#
__localeDir = hlm_defaultpaths.application() + '/hotspot_login_manager/lang'
gettext.bindtextdomain('hotspot-login-manager', __localeDir)
gettext.textdomain('hotspot-login-manager')
__localeDir = None


#-----------------------------------------------------------------------------
#
# Install the translator functions globally. They will be available to every module.
#
#       _()  is the basic string translator (one to one mapping, cf. gettext.lgettext).
#       _N() is the plural string translator (mapping depends on the counter, cf. gettext.lngettext).
#
__builtinVars = vars()['__builtins__']
__builtinVars['_'] = gettext.lgettext
__builtinVars['_N'] = gettext.lngettext
__builtinVars = None


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
