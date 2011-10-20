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
#
from hotspot_login_manager.libs.core import hlm_args
from hotspot_login_manager.libs.core import hlm_application
from hotspot_login_manager.libs.core import hlm_log
from hotspot_login_manager.libs.core import hlm_pidfile
from hotspot_login_manager.libs.core import hlm_psargs
#
from hotspot_login_manager.libs.core import hlm_daemonize_psf
#
from hotspot_login_manager.libs.core import hlm_platform
hlm_platform.install(vars(), 'rlimit_files')


#-----------------------------------------------------------------------------
def daemonize(
              # unprivileged option (any user)
              preventCoreDump = True,       # If core dumps are allowed the daemon may leak sensitive information.

              #-------------------------------------------------------------
              # The next options will be protected against core dumps.
              #-------------------------------------------------------------

              hookPreChroot = None,         # Function that will be called just before the chroot.
              # privileged option (root)
              chroot = None,                # Directory to chroot into.
                                            # IMPORTANT: HLM files must not have their path changed once inside the chroot.

              #-------------------------------------------------------------
              # The next options will be processed once the chroot is set up.
              #-------------------------------------------------------------

              # unprivileged options (any user)
              workingDir = '/',             # Working directory.
              umask = None,                 # Set umask (None: inherit from parent process, unreliable if the daemon creates files).

              hookPreChangeOwner = None,    # Function that will be called just before the process owner is changed.
              # privileged options (root)
              uid = None,                   # Change process UID. [*]
              gid = None,                   # Change process GID. [*]
                                            # [*] If UID and/or GID are None, relinquish any inherited effective privilege elevation.
                                            #     Both accept either an int (xID) or a string (name that will be looked up).

              #-------------------------------------------------------------
              # The next options will be processed under the new credentials
              # (usually, an unprivileged user).
              #-------------------------------------------------------------

              # unprivileged options (any user)
              hookPreDetach = None,         # Function that will be called just before the process is detached.
              logLevel = None,              # Maximum log level. None does not create a log object (which is strongly discouraged).
              detach = None,                # None : detach the process, except when called from init / inetd
                                            # True: always detach the process
                                            # False: never detach the process

              signals = {},                 # Signals map. Each dictionary entry must be in the form { signal.SIGWHATEVER: function }
                                            #     Signals not available for the current platform are left as-is.
                                            #     None as the function object results in the signal being ignored (signal.SIG_IGN).

              keepFiles = [],               # List of file-like objects / filenos that must be kept open.
              stdin = None,                 # File/fileno that is rebound to stdin (mode r).
              stdout = None,                # File/fileno that is rebound to stdout (mode w+).
              stderr = None,                # File/fileno that is rebound to stderr (mode w+).

              pidFile = None,               # PID lock file name.
             ):
    ''' Turn the process into a well-behaved Unix daemon.
    '''
    # Canonicalize command-line to allow correct detection of stale PID files
    _ensureCanonicalCommandLine()
    # Prevent core dumps
    if preventCoreDump:
        hlm_daemonize_psf.preventCoreDump()
        if isDebug: logDebug('Prevented core dump.')

    # hookPreChroot
    if hookPreChroot != None:
        hookPreChroot()
    # chroot
    if chroot != None:
        hlm_daemonize_psf.setChroot(chroot)
        if isDebug: logDebug('Chrooted to {0}.'.format(quote(chroot)))

    # Change working directory
    hlm_daemonize_psf.setWorkingDir(workingDir)
    if isDebug: logDebug('Changed working directory to {0}.'.format(quote(workingDir)))
    # Change umask
    if umask != None:
        hlm_daemonize_psf.setUmask(umask)
        if isDebug: logDebug('Changed creation file mask to {0}.'.format(oct(umask)))

    # hookPreChangeOwner
    if hookPreChangeOwner != None:
        hookPreChangeOwner()
    # Change process owner
    (uid, gid) = _lookupOwnerIds(uid, gid)
    hlm_daemonize_psf.setOwner(uid, gid)
    if isDebug: logDebug('Changed process owner to UID={0}, GID={1}.'.format(uid, gid))

    # Create log object before we detach from the terminal
    if logLevel != None:
        hlm_log.open(logLevel)

    # hookPreDetach
    if hookPreDetach != None:
        hookPreDetach()
    # Detach the process
    if detach != False:
        oldPID = os.getpid()
        if isDebug: logDebug('Preparing to detach process (PID={0})...'.format(oldPID))
        hlm_daemonize_psf.detachProcess(detach, hlm_log.activate)
        if isDebug:
            newPID = os.getpid()
            if oldPID != newPID:
                logDebug('Successfully detached process (PID={0}).'.format(os.getpid()))
            else:
                logDebug('The process has been started by init or inetd, no need to detach.'.format(os.getpid()))
    # Ensure the syslog facility is active even if we are not detached.
    hlm_log.activate()

    # Set signal map
    hlm_daemonize_psf.setSignalMap(signals)
    if isDebug: logDebug('Signal handlers have been installed.')
    # std* streams redirects
    hlm_daemonize_psf.redirectStandardStreams(stdin, stdout, stderr)
    if isDebug: logDebug('Standard streams have been redirected.')
    # Close file descriptors (we want to keep custom std* streams too)
    hlm_daemonize_psf.closeFiles(keepFiles, maxFileDescriptors())
    if isDebug: logDebug('All irrelevant file descriptors have been closed.')

    # Create the PID lock file
    if pidFile != None:
        hlm_pidfile.createPIDFile(pidFile)


#-----------------------------------------------------------------------------
def _ensureCanonicalCommandLine():
    ''' Check if we have been called using a canonical command-line, restart
        properly otherwise.
    '''
    isCanonical = hlm_psargs.isCanonicalCommandLine(os.getpid())
    if isCanonical != True:
        args = hlm_args.args()
        # Protect against infinite loops in case of canonicalization failure
        if args.strayArgs == [':']:
            raise FatalError('[BUG] Unable to enforce canonical command-line, exiting.')

        if isDebug: logDebug('Relaunching the process using a canonical command-line...')
        # Restart the daemon with a properly canonicalized command-line
        exeName = hlm_application.getExecutableName()
        if args.runDaemon:
            os.execl(exeName, exeName, ':', '--daemon', '--log', args.logLevel, '--config', args.daemonConfig, '--credentials', args.daemonCredentials)
        elif args.runNotifier:
            os.execl(exeName, exeName, ':', '--notifier', args.notifierBackend, '--log', args.logLevel)
        else:
            raise FatalError('[BUG] Unexpected combination of command-line arguments (should never happen).')


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
    except BaseException as exc:
        raise FatalError(_('No user named {0} has been found:\n{1}').format(quote(uid), exc))

    try:
        # Lookup GID
        _gid = gid
        if _gid == None:
            _gid = os.getgid()
        elif not isinstance(_gid, int):
            _gid = grp.getgrnam(gid).gr_gid
    except BaseException as exc:
        raise FatalError(_('No group named {0} has been found:\n{1}').format(quote(gid), exc))

    return (_uid, _gid)


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
