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
# Description: Safe HTTP(S) connections, and redirect detection.
#


#-----------------------------------------------------------------------------
import http.client
import re
import socket
import ssl
import urllib.error
import urllib.request
#
from hotspot_login_manager.libs.core import hlm_paths


#-----------------------------------------------------------------------------
class CertificateError(http.client.HTTPException, urllib.error.URLError):
    ''' Certificate error.
    '''
    def __init__(self, host, reason):
        http.client.HTTPException.__init__(self)
        self.host = host
        self.reason = reason

    def __str__(self):
        return _('SSL certificate error for host {0}: {1}').format(quote(self.host), self.reason)


#-----------------------------------------------------------------------------
def detectRedirect(url):
    ''' Return None if URL does not redirect us, or the new Location otherwise.
        Please note that we are only interested in HTTP redirects, any other
        error is out of our reach.
    '''
    try:
        result = _redirectOpener.open(url)
        result.close()
    except _RedirectError as exc:
        return exc.location
    except SystemExit:
        raise
    except BaseException as exc:
        pass
    return None


#-----------------------------------------------------------------------------
def urlOpener():
    ''' Return an urllib.request.URLopener that actually checks if the peer
        certificate is valid in case of an HTTPS connection.
    '''
    handler = HTTPSHandler(ca_certs = hlm_paths.sslCaCertificates())
    return urllib.request.build_opener(handler)


#-----------------------------------------------------------------------------
def readAll(result, encoding = True):
    ''' Convenience function to read the whole result and optionally decode it at the same time.

        If "encoding" is True, it will automatically detect the encoding according to the Content-Type header.
        IF "encoding" is None or there is no Content-Type header, return the binary data.
    '''
    data = b''
    while True:
        response = result.read()
        if response == b'':
            break
        data += response
    if encoding == True:
        encoding = None
        contentType = result.getheader('Content-Type', None)
        if isinstance(contentType, str):
            match = _regexContentType.search(contentType)
            if match != None:
                encoding = match.group(1)
    if encoding != None:
        try:
            data = data.decode(encoding)
        except:
            pass
    return data


#-----------------------------------------------------------------------------
def splitUrlArguments(url, mandatoryArgs = None, urlLabel = None):
    ''' Convenience function to split an URL and check its arguments.
    '''
    urlArgs = {}
    for arg in urllib.parse.urlsplit(url).query.split('&'):
        (key, value) = arg.split('=')
        (key, value) = (urllib.parse.unquote(key), urllib.parse.unquote(value))
        urlArgs[key] = value
    if mandatoryArgs != None:
        argKeys = urlArgs.keys()
        if urlLabel == None:
            urlLabel = 'URL'
        for arg in mandatoryArgs:
            if arg not in argKeys:
                raise Exception('missing argument {0} in the {1}.'.format(quote(arg), urlLabel))
    return urlArgs


#-----------------------------------------------------------------------------
class _RedirectError(BaseException):
    ''' Custom error that will hold the new location in case of a redirect.
    '''
    def __init__(self, location):
        BaseException.__init__(self)
        self.location = location


#-----------------------------------------------------------------------------
class _RedirectHandler(urllib.request.HTTPRedirectHandler):
    ''' This mess is required because of a known bug in Python 3.1's urllib
        which hangs when the default URLopener() is faced with a redirect.
    '''
    def http_error_301(self, req, fp, code, msg, headers):
        self.__redirect(headers)
    def http_error_302(self, req, fp, code, msg, headers):
        self.__redirect(headers)
    def http_error_303(self, req, fp, code, msg, headers):
        self.__redirect(headers)
    def http_error_307(self, req, fp, code, msg, headers):
        self.__redirect(headers)

    def __redirect(self, headers):
        ''' Raise an error whenever we are redirected.
        '''
        location = headers.get('Location')
        if location == None:
            location = headers.get('URI')
        raise _RedirectError(location)


#-----------------------------------------------------------------------------
#
# Our custom URL opener that is actually able to detect redirects...
#
_redirectOpener = urllib.request.build_opener(_RedirectHandler)



#-----------------------------------------------------------------------------
class HTTPSConnection(http.client.HTTPConnection):
    ''' An HTTPSConnection that actually checks if the peer certificate is valid.
    '''
    default_port = http.client.HTTPS_PORT

    def __init__(self, host, port = None, key_file = None, cert_file = None, ca_certs = None, strict = None, **kwargs):
        http.client.HTTPConnection.__init__(self, host, port, strict, **kwargs)
        self.key_file = key_file
        self.cert_file = cert_file
        self.ca_certs = ca_certs
        if self.ca_certs:
            self.cert_reqs = ssl.CERT_REQUIRED
        else:
            self.cert_reqs = ssl.CERT_NONE

    def connect(self):
        def matchHostname(cert, hostname):
            # Get valid hostnames from the certificate
            hosts = []
            if 'subjectAltName' in cert:
                for rdn in cert['subjectAltName']:
                    if (rdn[0].lower() == 'dns') or (rdn[0][:2].lower() == 'ip'):
                        hosts.append(rdn[1])
            if 'subject' in cert:
                for rdn in cert['subject']:
                    if rdn[0][0].lower() == 'commonname':
                        hosts.append(rdn[0][1])
            # Check all the possible hostnames in turn
            for host in hosts:
                # Escape host for RE usage
                host = host.replace('.', '\\.')   # Avoid dots matching any character
                addStar = False
                if host.startswith('*\\.'):
                    host = host[3:]               # Handle *.domain.tld later, we first need to escape all * characters but the first one
                    addStar = True
                host = host.replace('*', '\\*')   # There should be no other * characters so we force them as litterals
                if addStar:
                    host = '(.*\\.)?' + host      # *.domain.tld matches domain.tld, h.domain.tld, h1.h2.domain.tld
                # Does the hostname match the RE?
                if re.search('^' + host + '$', hostname, re.IGNORECASE):
                    return True
            return False

        sock = socket.create_connection((self.host, self.port))
        self.sock = ssl.wrap_socket(sock, keyfile = self.key_file, certfile = self.cert_file, cert_reqs = self.cert_reqs, ca_certs = self.ca_certs)
        if self.cert_reqs == ssl.CERT_REQUIRED:
            cert = self.sock.getpeercert()
            hostname = self.host.split(':', 0)[0]
            if not matchHostname(cert, hostname):
                raise CertificateError(hostname, 'hostname mismatch.')


#-----------------------------------------------------------------------------
class HTTPSHandler(urllib.request.HTTPSHandler):
    ''' An HTTPSHandler that actually checks if the peer certificate is valid.
    '''
    def __init__(self, **kwargs):
        urllib.request.AbstractHTTPHandler.__init__(self)
        self._connection_args = kwargs

    def https_open(self, req):
        def http_class_wrapper(host, **kwargs):
            full_kwargs = dict(self._connection_args)
            full_kwargs.update(kwargs)
            return HTTPSConnection(host, **full_kwargs)

        try:
            return self.do_open(http_class_wrapper, req)
        except urllib.error.URLError as exc:
            if type(exc.reason) == ssl.SSLError and exc.reason.args[0] == 1:
                raise CertificateError(req.host, exc.reason.args[1])
            raise

    https_request = urllib.request.HTTPSHandler.do_request_


#-----------------------------------------------------------------------------
#
# Pre-compiled regular expression for readAll()
#
_regexContentType = re.compile('charset=([^;]+)')


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
