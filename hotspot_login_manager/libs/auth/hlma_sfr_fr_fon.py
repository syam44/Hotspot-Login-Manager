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
# Description: Authentication plugin for SFR.FR + FON hotspots
#


#-----------------------------------------------------------------------------
import re
import urllib.parse
#
from hotspot_login_manager.libs.daemon import hlm_http


#-----------------------------------------------------------------------------
def getSupportedProviders():
    return ['sfr.fr'] # TODO: fon


#-----------------------------------------------------------------------------
def getSupportedSSIDs():
    return ['SFR WiFi FON']


#-----------------------------------------------------------------------------
def getSupportedRedirectPrefixes():
    return ['https://hotspot.neuf.fr/indexEncryptingChilli.php?']


#-----------------------------------------------------------------------------
def authenticate(redirectURL, connectedSSIDs, credentials, pluginName):
    # Extract the URL arguments
    urlArgs = hlm_http.splitUrlArguments(redirectURL, ['challenge', 'mode', 'uamip', 'uamport', 'channel'], 'redirect URL')
    if __DEBUG__: logDebug('AuthPlugin {0}: got all required arguments from the redirect URL.'.format(quote(pluginName)))

    # Get the login page
    result = hlm_http.urlOpener().open(redirectURL)
    pageData = hlm_http.readAll(result)
    result.close()
    if __DEBUG__: logDebug('AuthPlugin {0}: grabbed the login webpage.'.format(quote(pluginName)))

    # Basic check to see if we are on the right hotspot
    if (_regexCheckNB4.search(pageData) == None) or (_regexCheckChoiceFON.search(pageData) == None):
        raise Exception('basic sanity check failed, we don\'t have a "NeufBox4".')
    if __DEBUG__: logDebug('AuthPlugin {0}: basic sanity check OK, seems we have a "NeufBox4" here.'.format(quote(pluginName)))

    # Double-check the Chillispot URL
    match = _regexChilliURL.search(pageData)
    if match == None:
        raise Exception('in-page data is missing.')
    if match.group(1) != redirectURL:
        raise Exception('in-page data conflicts with the redirected URL.')
    if __DEBUG__: logDebug('AuthPlugin {0}: in-page data confirms the redirect URL.'.format(quote(pluginName)))

    # Post data
    if 'sfr.fr' in credentials.keys():
        (user, password) = credentials['sfr.fr']
        postData = 'choix=neuf&username={0}&password={1}&conditions=on&challenge={2}&accessType=neuf&lang=fr&mode={3}&userurl=http%253a%252f%252fwww.google.com%252f&uamip={4}&uamport={5}&channel={6}&connexion=Connexion'.format(urllib.parse.quote(user), urllib.parse.quote(password), urlArgs['challenge'], urlArgs['mode'], urlArgs['uamip'], urlArgs['uamport'], urlArgs['channel'])

        # Ask the hotspot gateway to give us the Chillispot URL
        result = hlm_http.urlOpener().open('https://hotspot.neuf.fr/nb4_crypt.php', postData)
        pageData = hlm_http.readAll(result)
        result.close()
        if __DEBUG__: logDebug('AuthPlugin {0}: grabbed the encryption gateway (JS redirect) result webpage.'.format(quote(pluginName)))

        # OK, now we have to put up with a Javascript redirect. I mean, WTF?
        match = _regexJSRedirect.search(pageData)
        if match == None:
            raise Exception('missing URL in the encryption gateway (JS redirect) result webpage.')
        redirectURL = match.group(1)
        # Let's see what Chillispot will answer us...
        redirectURL = hlm_http.detectRedirect(redirectURL)
        if redirectURL == None:
            raise Exception('something went wrong during the Chillispot query (redirect expected, but none obtained).')

        # Check the final URL arguments
        urlArgs = hlm_http.splitUrlArguments(redirectURL, ['res'], 'redirect URL')
        urlArgs = urlArgs['res'].lower()

        if urlArgs == 'failed':
            raise Exception('WRONG CREDENTIALS')

        if (urlArgs != 'success') and (urlArgs != 'already'):
            raise Exception('Chillispot didn\'t let us log in, no idea why.')

        return True

    elif 'fon' in credentials.keys():
        # TODO
        return False

    return False


#-----------------------------------------------------------------------------
#
# Pre-compiled regular expressions for authenticate()
#
_regexCheckNB4 = re.compile('<form action="nb4_crypt.php" ')
_regexCheckChoiceFON = re.compile('<select name="choix" ')
_regexChilliURL = re.compile('SFRLoginURL_JIL=(https://hotspot.neuf.fr/indexEncryptingChilli.php?[^>]+)-->')
_regexJSRedirect = re.compile('window.location = "([^"]+)";')


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
