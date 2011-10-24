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
# Description: Detect HTTP redirects.
#


#-----------------------------------------------------------------------------
import urllib.request


#-----------------------------------------------------------------------------
class _RedirectError(BaseException):
    ''' Custom error that will hold (status, location) in case of a redirect.
    '''

#-----------------------------------------------------------------------------
class _RedirectHandler(urllib.request.HTTPRedirectHandler):
    ''' This mess is required because of a known bug in Python 3.1's urllib
        which hangs when the default URLopener() is faced with a redirect.
    '''
    def http_error_301(self, req, fp, code, msg, headers):
        self.__redirect(code, headers)
    def http_error_302(self, req, fp, code, msg, headers):
        self.__redirect(code, headers)
    def http_error_303(self, req, fp, code, msg, headers):
        self.__redirect(code, headers)
    def http_error_307(self, req, fp, code, msg, headers):
        self.__redirect(code, headers)

    def __redirect(self, code, headers):
        ''' Raise an error whenever we are redirected.
        '''
        raise _RedirectError(code, headers.get('Location'))


#-----------------------------------------------------------------------------
#
# Our custom URL opener that is actually able to detect redirects...
#
_opener = urllib.request.build_opener(_RedirectHandler)


#-----------------------------------------------------------------------------
def detectRedirect(url):
    ''' Return None if URL does not redirect us, or the new Location otherwise.
        Please note that we are only interested in HTTP redirects, any other
        error is out of our reach.
    '''
    try:
        result = _opener.open(url)
        result.close()
    except _RedirectError as exc:
        return exc.args[1]
    except SystemExit:
        raise
    except BaseException:
        pass
    return None


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
