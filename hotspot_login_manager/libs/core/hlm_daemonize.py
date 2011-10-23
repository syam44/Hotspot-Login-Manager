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
# Description: Turn the process into a well-behaved Unix daemon.
#


#-----------------------------------------------------------------------------
import grp
import os
import pwd
import signal
import sys
#
from hotspot_login_manager.libs.core import hlm_args
from hotspot_login_manager.libs.core import hlm_application
from hotspot_login_manager.libs.core import hlm_daemonize_psf
from hotspot_login_manager.libs.core import hlm_log
#
from hotspot_login_manager.libs.core import hlm_platform
hlm_platform.install(vars(), 'rlimit_files')


#-----------------------------------------------------------------------------
def defaultSignalsMap():
    ''' Default signals map.
    '''
    return { 'SIGABRT': cleanExit,
             'SIGFPE': cleanExit,
             'SIGHUP': cleanExit,
             'SIGILL': cleanExit,
             'SIGINT': cleanExit,
             'SIGPIPE': None,
             'SIGSEGV': cleanExit,
             'SIGTERM': cleanExit,
             'SIGTSTP': None,
             'SIGTTIN': None,
             'SIGTTOU': None,
             'SIGBUS': cleanExit,
             'SIGSYS': cleanExit,
             'SIGSTKFLT': cleanExit,
           }


#-----------------------------------------------------------------------------
def cleanExit(signalNumber, stackFrame):
    ''' Signal handler for exiting the daemon cleanly.
    '''
    if __INFO__:
        signalName = 'UNKNOWN'
        for (name, value) in vars(signal).items():
            if value == signalNumber:
                signalName = name
                break
        logInfo('Received signal {0} ({1}), exiting.'.format(signalName, signalNumber))
    sys.exit(0)


#-----------------------------------------------------------------------------
def daemonize(
              # unprivileged option (any user)
              preventCoreDump = True,       # If core dumps are allowed the daemon may leak sensitive information.

              # unprivileged options (any user)
              workingDir = '/',             # Working directory.
              umask = None,                 # Set umask (None: inherit from parent process, unreliable if the daemon creates files).


              # unprivileged options (any user)
              syslogFacility = True,        # True: setup the syslog facility and activate it.
                                            # False: do not use syslog.
              detach = None,                # None : detach the process, except when called from init / inetd
                                            # True: always detach the process
                                            # False: never detach the process

              signals = defaultSignalsMap(),# Signals map. Each dictionary entry must be in the form { 'SIGWHATEVER': handler }
                                            #     Signals not available for the current platform are ignored rather than raising an error.
                                            #     None as the handler object results in the signal being ignored (signal.SIG_IGN).

              stdin = None,                 # File/fileno that is rebound to stdin (mode r).
              stdout = None,                # File/fileno that is rebound to stdout (mode w+).
              stderr = None,                # File/fileno that is rebound to stderr (mode w+).

              # privileged options (root)
              uid = None,                   # Change process UID. [*]
              gid = None,                   # Change process GID. [*]
                                            # [*] If UID and/or GID are None, relinquish any inherited effective privilege elevation.
                                            #     Both accept either an int or a string (name that will be looked up).

              # unprivileged options (any user)
              keepFiles = [],               # List of file-like objects / filenos that must be kept open.
             ):
    ''' Turn the process into a well-behaved Unix daemon.
    '''
    # Prevent core dumps
    if preventCoreDump:
        hlm_daemonize_psf.preventCoreDump()
        if __DEBUG__: logDebug('Core dumps are now disabled.')

    # Change working directory
    hlm_daemonize_psf.setWorkingDir(workingDir)
    if __DEBUG__: logDebug('Changed working directory to {0}.'.format(quote(workingDir)))
    # Change umask
    if umask != None:
        hlm_daemonize_psf.setUmask(umask)
        if __DEBUG__: logDebug('Changed creation file mask to {0}.'.format(oct(umask)))

    # Create log object before we detach from the terminal
    if syslogFacility:
        hlm_log.open()

    # Detach the process
    if detach != False:
        if __DEBUG__:
            oldPID = os.getpid()
            logDebug('Preparing to detach process (PID={0})...'.format(oldPID))
        detached = hlm_daemonize_psf.detachProcess(detach, hlm_log.activate)
        if __DEBUG__:
            if detached:
                logDebug('The child process (PID {0}) has been detached from its parent (PID {1}).'.format(os.getpid(), oldPID))
            else:
                logDebug('The process (PID {0}) has been started by init or inetd, no need to detach.'.format(os.getpid()))

    # Ensure the syslog facility is active even if we are not detached.
    if syslogFacility:
        hlm_log.activate()
    # Set signal map
    hlm_daemonize_psf.setSignalMap(signals)
    if __DEBUG__: logDebug('Signal handlers have been installed.')

    # Change process owner
    (uid, gid) = _lookupOwnerIds(uid, gid)
    hlm_daemonize_psf.setOwner(uid, gid)
    if __DEBUG__: logDebug('Changed process owner to UID={0}, GID={1}.'.format(uid, gid))

    # std* streams redirects
    hlm_daemonize_psf.redirectStandardStreams(stdin, stdout, stderr)
    if __DEBUG__: logDebug('Standard streams have been redirected.')
    # Close file descriptors (we want to keep custom std* streams too)
    hlm_daemonize_psf.closeFiles(keepFiles, maxFileDescriptors())
    if __DEBUG__: logDebug('All irrelevant file descriptors have been closed.')


#-----------------------------------------------------------------------------
def _lookupOwnerIds(uid, gid):
    ''' Lookup the uid/gid identifiers if a name was passed instead of an integer.
    '''
    try:
        # Lookup UID
        _uid = uid
        if _uid == None:
            _uid = os.getuid()
        elif not isinstance(_uid, int):
            _uid = pwd.getpwnam(_uid).pw_uid
    except SystemExit:
        raise
    except BaseException as exc:
        raise FatalError(_('No user named {0} has been found: {1}').format(quote(uid), exc))

    try:
        # Lookup GID
        _gid = gid
        if _gid == None:
            _gid = os.getgid()
        elif not isinstance(_gid, int):
            _gid = grp.getgrnam(gid).gr_gid
    except SystemExit:
        raise
    except BaseException as exc:
        raise FatalError(_('No group named {0} has been found: {1}').format(quote(gid), exc))

    return (_uid, _gid)


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
