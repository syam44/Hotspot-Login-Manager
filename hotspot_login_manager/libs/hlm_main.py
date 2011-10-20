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
# Description: Main program.
#


#-----------------------------------------------------------------------------
# Do not import any HLM module before these ones, those services are needed everywhere!
# Also, don't touch their relative order.
import hotspot_login_manager.libs.core.hlm_log
import hotspot_login_manager.libs.core.hlm_globals
import hotspot_login_manager.libs.core.hlm_i18n
#
import sys
import traceback
#
from hotspot_login_manager.libs.core import hlm_args


#-----------------------------------------------------------------------------
#
# Debug switch
#
_forceDebug = True

#-----------------------------------------------------------------------------
def main():
    try:
        globals()['__builtins__']['isDebug'] = False
        args = hlm_args.args()
        # Enforce global debugging flag
        if _forceDebug:
            args.logLevel = 'debug'
        # Apply command-line debugging flag back to the global flag
        globals()['__builtins__']['isDebug'] = (args.logLevel == 'debug')
        if isDebug: logDebug('Debugging mode is on.')

        # --daemon
        if args.runDaemon:
            from hotspot_login_manager.libs.daemon import hlm_main_daemon
            hlm_main_daemon.main(args)

        # --reauth
        if args.runReauth:
            from hotspot_login_manager.libs.notifier import hlm_main_reauth
            hlm_main_reauth.main(args)

        # --status
        if args.runStatus:
            from hotspot_login_manager.libs.notifier import hlm_main_status
            hlm_main_status.main(args)

        # --notifier
        if args.runNotifier:
            from hotspot_login_manager.libs.notifier import hlm_main_notifier
            hlm_main_notifier.main(args)

    except SystemExit as exc:
        sys.exit(exc.code)

    except ImportError as exc:
        logError('Couldn\'t load module: {0}'.format(exc))
        if isDebug: logDebug('Full exception info:', ''.join(traceback.format_exception(*sys.exc_info())))
        sys.exit(255)

    except BaseException as exc:
        logError(exc)
        if isDebug: logDebug('Full exception info:', ''.join(traceback.format_exception(*sys.exc_info())))
        sys.exit(1)

    sys.exit(0)


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
