# -*- coding:utf-8 -*-
#
# hotspot-login-manager
# https://github.com/syam44/Hotspot-Login-Manager
#
# Distributed under the GNU General Public License version 3
# https://www.gnu.org/copyleft/gpl.html
#
# Authors: syam (aks92@free.fr)
#          thuban (thuban@singularity.fr)
#
# Description: Load the daemon configuration files
#


#-----------------------------------------------------------------------------
import configparser
from optparse import Values
import re
#
from hotspot_login_manager.libs.core import hlm_application
from hotspot_login_manager.libs.core import hlm_args
from hotspot_login_manager.libs.core import hlm_paths
from hotspot_login_manager.libs.core import hlm_plugin


#-----------------------------------------------------------------------------
def loadDaemon():
    ''' Load the daemon configuration file.
    '''
    args = hlm_args.args()
    configFile = args.daemonConfig
    if configFile == None:
        configFile = hlm_paths.daemonConfig()
    config = configparser.SafeConfigParser()
    try:
        config.read(configFile)
    except SystemExit:
        raise
    except BaseException as exc:
        raise FatalError(_('Can\'t load the daemon configuration file {0}: {1}').format(quote(configFile), exc))

    try:
        if config.sections() != ['daemon']:
            raise Exception(_('only the section {0} is allowed in this file.').format('[daemon]'))
        options = config.options('daemon')
        _checkAlienDirectives(['credentials', 'user', 'group'], options, 'daemon')
        # "credentials" accepts a credentials.conf file path
        if args.daemonCredentials == None:
            credentials = None
            if config.has_option('daemon', 'credentials'):
                credentials = config.get('daemon', 'credentials')
            else:
                credentials = hlm_paths.credentialsConfig()
            args.daemonCredentials = credentials
        # "user" accepts an account name
        user = None
        if config.has_option('daemon', 'user'):
            user = config.get('daemon', 'user')
        # "group" accepts a group name
        group = None
        if config.has_option('daemon', 'group'):
            group = config.get('daemon', 'group')

        if __DEBUG__: logDebug('Daemon configuration has been loaded from {0}.'.format(configFile))
        return (user, group)
    except SystemExit:
        raise
    except BaseException as exc:
        raise FatalError(_('Incorrect daemon configuration file {0}: {1}').format(quote(configFile), exc))


#-----------------------------------------------------------------------------
def loadCredentials():
    ''' Load the credentials configuration file.
    '''
    configFile = hlm_args.args().daemonCredentials
    config = configparser.SafeConfigParser()
    try:
        config.read(configFile)
    except SystemExit:
        raise
    except BaseException as exc:
        raise FatalError(_('Can\'t load the credentials configuration file {0}: {1}').format(quote(configFile), exc))

    result = Values()
    result.ping = None
    result.ssids = {}
    try:
        sections = config.sections()
        regex = re.compile('^ssid *= *(.+)$')
        for section in sections:
            if section == 'ping':
                options = config.options('ping')
                _checkAlienDirectives(['site', 'delay'], options, section)
                result.ping = _mandatoryDirective('site', options, section, config.get)
                result.delay = _mandatoryDirective('delay', options, section, config.getint)
            else:
                match = regex.search(section)
                if match == None:
                    raise Exception(_('section {0} is not allowed in this file.').format('[' + section + ']'))
                options = config.options(section)
                _checkAlienDirectives(['type', 'user', 'password'], options, section)
                ssid = Values()
                ssid.ssid = match.group(1).strip()
                ssid.authPluginName = _mandatoryDirective('type', options, section, config.get)
                ssid.user = _mandatoryDirective('user', options, section, config.get)
                ssid.password = _mandatoryDirective('password', options, section, config.get)
                try:
                    ssid.authPlugin = hlm_plugin.load('hlma_' + ssid.authPluginName, hlm_application.getPath() + '/libs/auth', 'auth')
                    result.ssids[ssid.ssid] = ssid
                except SystemExit:
                    raise
                except BaseException as exc:
                    if __WARNING__: logWarning('Invalid authentication plugin {0} for SSID {1}: {2}'.format(quote(ssid.authPluginName), quote(ssid.ssid), exc))
        if result.ping == None:
            raise Exception(_('section {0} is missing.').format('[ping]'))
        if len(result.ssids) == 0:
            raise Exception(_('section {0} is missing.').format('[default]'))

        if __DEBUG__: logDebug('Credentials configuration has been loaded from {0}.'.format(configFile))
        return result
    except SystemExit:
        raise
    except BaseException as exc:
        raise FatalError(_('Incorrect credentials configuration file {0}: {1}').format(quote(configFile), exc))


#-----------------------------------------------------------------------------
def _checkAlienDirectives(allowedOptions, options, section):
    for option in options:
        if option not in allowedOptions:
            raise FatalError(_N('directive {0} is the only one allowed in section {1}.',
                                'directives {0} are the only ones allowed in section {1}.',
                                len(allowedOptions))
                                .format(quote(allowedOptions), '[' + section + ']'))


#-----------------------------------------------------------------------------
def _mandatoryDirective(directive, options, section, getter):
    if directive not in options:
        raise Exception(_('directive {0} is missing in section {1}.').format(quote(directive), '[' + section + ']'))
    return getter(section, directive)


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
