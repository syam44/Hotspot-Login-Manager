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


""" I18N module usage:
        The main script (hotspot-login-manager) should call hlm_i18n.init(__file__)
        as early as possible.

        Each module that needs translation services must use the following code:
            import hotspot_login_manager.libs.hlm_i18n
            _, _N = hotspot_login_manager.libs.hlm_i18n.translators()

        Run the provided devtools/i18n-gen-pot script in a shell to extract the strings
        as a .pot file in hotspot_login_manager/lang.
        Once the translation is ready as a LANG.po file, put it in hotspot_login_manager/lang
        and run the provided devtools/i18n-gen-mo to create the catalog bundles.
"""


import gettext
import os


def init(mainFile):
    localeDir = os.path.realpath(os.path.dirname(mainFile) + '/hotspot_login_manager/lang')
    gettext.bindtextdomain('hotspot-login-manager', localeDir)
    gettext.textdomain('hotspot-login-manager')


def translators():
    """ Return the translator functions.

        _, _N = hlm_i18n.translators()
    """
    return (gettext.lgettext, gettext.lngettext)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
