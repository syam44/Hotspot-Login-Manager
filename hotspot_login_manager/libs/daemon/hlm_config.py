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
#
# The minimum ping delay (in seconds) accepted from the credentials configuration.
#
_minimumPingDelay = 15


#-----------------------------------------------------------------------------
#
# The bare minimum ping delay (in seconds).
# This value is used in daemon/hlm_auth to enforce a minimum waiting time between each
# try, so we can protect against reauth spamming (which amounts to DoS).
#
# Obviously it must be smaller than _minimumPingDelay above.
#
antiDosPingDelay = 5


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
    result.auths = []
    try:
        sections = config.sections()
        regex = re.compile('^provider = ([a-zA-Z0-9_]+)$')
        for section in sections:
            if section == 'ping':
                options = config.options('ping')
                _checkAlienDirectives(['site', 'delay'], options, section)
                result.ping = _mandatoryDirective('site', options, section, config.get)
                if not result.ping.startswith('http://'):
                    raise Exception(_('ping website {0} is is incorrect, exiting.').format(quote(result.ping)))
                result.delay = _mandatoryDirective('delay', options, section, config.getint)
                if result.delay < _minimumPingDelay:
                    if __WARNING__: logWarning(_('Credentials configuration file {0}: ping interval {1} is way too low ({2} seconds), forcing it to {3} seconds.').format(quote(configFile), quote('delay'), result.delay, _minimumPingDelay))
                    result.delay = _minimumPingDelay
            else:
                match = regex.search(section)
                if match == None:
                    raise Exception(_('section {0} is not allowed in this file.').format('[' + section + ']'))
                options = config.options(section)
                _checkAlienDirectives(['user', 'password'], options, section)
                auth = Values()
                auth.pluginName = match.group(1).strip()
                auth.user = _mandatoryDirective('user', options, section, config.get)
                auth.password = _mandatoryDirective('password', options, section, config.get)
                try:
                    auth.pluginModule = hlm_plugin.load('hlma_' + auth.pluginName, hlm_application.getPath() + '/libs/auth', 'auth')
                    result.auths.append(auth)
                except SystemExit:
                    raise
                except BaseException as exc:
                    if __WARNING__: logWarning('Invalid authentication provider {0}: {1}'.format(quote(auth.pluginName), exc))
        if result.ping == None:
            raise Exception(_('section {0} is missing.').format('[ping]'))
        if result.auths == []:
            raise Exception(_('no configured credentials, exiting.'))

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
