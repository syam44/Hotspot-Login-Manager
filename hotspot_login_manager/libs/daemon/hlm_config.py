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
#
from hotspot_login_manager.libs.daemon import hlm_auth_plugins


#-----------------------------------------------------------------------------
#
# The minimum ping interval (in seconds) accepted from the credentials configuration.
#
_minimumPingInterval = 15


#-----------------------------------------------------------------------------
#
# The bare minimum ping interval (in seconds).
# This value is used in daemon/hlm_authenticator to enforce a minimum waiting time between each
# try, so we can protect against reauth spamming (which amounts to DoS).
#
# Obviously it must be smaller than _minimumPingInterval above.
#
antiDosPingInterval = 5


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
        _checkAlienDirectives(['credentials', 'user', 'group', 'ping_site', 'ping_interval'], options, 'daemon')
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
        # "pingSite" requires an http:// website URL
        pingSite = _mandatoryDirective('ping_site', options, 'daemon', config.get)
        if not pingSite.startswith('http://'):
            raise Exception(_('ping_site {0} is is incorrect (must start with {1}), exiting.').format(quote(pingSite), quote('http://')))
        pingInterval = _mandatoryDirective('ping_interval', options, 'daemon', config.getint)
        if pingInterval < _minimumPingInterval:
            if __WARNING__: logWarning(_('Daemon configuration file {0}: ping_interval is way too low ({1} seconds), forcing it to {2} seconds.').format(quote(configFile), pingInterval, _minimumPingInterval))
            pingInterval = _minimumPingInterval

        # Wrap configuration into a single Values() object
        configCredentials = Values()
        configCredentials.user = user
        configCredentials.group = group
        configCredentials.pingSite = pingSite
        configCredentials.pingInterval = pingInterval

        if __DEBUG__: logDebug('Daemon configuration has been loaded from {0}.'.format(configFile))
        return configCredentials
    except SystemExit:
        raise
    except BaseException as exc:
        raise FatalError(_('Incorrect daemon configuration file {0}: {1}').format(quote(configFile), exc))


#-----------------------------------------------------------------------------
def loadRelevantPluginCredentials():
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

    configCredentials = {}
    try:
        supportedProviders = hlm_auth_plugins.getSupportedProviders()

        sections = config.sections()
        regex = re.compile('^provider = ([a-zA-Z0-9_.]+)$')
        for section in sections:
            # Check service provider
            match = regex.search(section)
            if match == None:
                raise Exception(_('section {0} is not allowed in this file.').format('[' + section + ']'))
            provider = match.group(1)
            if provider not in supportedProviders:
                raise Exception(_('service provider {0} is not (currently) supported by HLM.').format(quote(provider)))
            # Check options
            options = config.options(section)
            _checkAlienDirectives(['user', 'password'], options, section)
            user = _mandatoryDirective('user', options, section, config.get)
            password = _mandatoryDirective('password', options, section, config.get)
            configCredentials[provider] = (user, password)

        if configCredentials == {}:
            raise Exception(_('no configured credentials, exiting.'))

        # Check which plugins we may use, according to the provided credentials.
        availablePlugins = hlm_auth_plugins.getAuthPlugins()
        relevantPlugins = set()

        for plugin in availablePlugins:
            plugin.pluginCredentials = {}
            pluginProviders = plugin.getSupportedProviders()
            for provider in configCredentials:
                if provider in pluginProviders:
                    plugin.pluginCredentials[provider] = configCredentials[provider]
                    relevantPlugins.add(plugin)

        relevantPlugins = list(relevantPlugins)
        if relevantPlugins == []:
            raise Exception(_('configured credentials don\'t match any available authentication plugin, exiting.'))

        if __DEBUG__: logDebug('Credentials configuration has been loaded from {0}.'.format(configFile))
        return relevantPlugins
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
