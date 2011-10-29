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
# Description: Main program for listing the available providers.
#


#-----------------------------------------------------------------------------
import sys
#
from hotspot_login_manager.libs.daemon import hlm_auth_plugins


#-----------------------------------------------------------------------------
def main(args):
    providers = hlm_auth_plugins.getSupportedProviders()
    providerNames = list(providers)
    providerNames.sort()

    maxProviderNameLength = 0
    for provider in providerNames:
        maxProviderNameLength = max(maxProviderNameLength, len(provider))

    print(_('Available service providers:'))
    for provider in providerNames:
        padding = ' ' * (maxProviderNameLength - len(provider))
        ssidsList = ', '.join(providers[provider])
        print('    ' + _('{0} {1}(corresponding hotspots: {2})').format(provider, padding, ssidsList))

    sys.exit(0)


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
