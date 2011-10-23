# -*- coding:utf-8 -*-
#
# hotspot-login-manager
# https://github.com/syam44/Hotspot-Login-Manager
#
# Distributed under the Python Software Foundation License version 2
# http://wiki.python.org/moin/PythonSoftwareFoundationLicenseV2Easy
#
# Authors: syam (aks92@free.fr)
#
# Description: Turn the process into a well-behaved Unix daemon.
#
#              Most code in this module has been borrowed from python-daemon 1.5.5 by Ben Finney et al. (which is licensed under the PSF v2).
#                  http://pypi.python.org/pypi/python-daemon/
#                  Copyright © 2008–2010 Ben Finney <ben+python@benfinney.id.au>
#                  Copyright © 2007–2008 Robert Niederreiter, Jens Klein
#                  Copyright © 2004–2005 Chad J. Schroeder
#                  Copyright © 2003 Clark Evans
#                  Copyright © 2002 Noah Spurrier
#                  Copyright © 2001 Jürgen Hermann
#              Unfortunately this library is not yet ported to Python 3, so I (syam) ported it and refactored it to fit my needs.
#


#-----------------------------------------------------------------------------
import errno
import os
import resource
import signal
import socket
import sys


#-----------------------------------------------------------------------------
def preventCoreDump():
    ''' Prevent this process from generating a core dump.

        Sets the soft and hard limits for core dump size to zero. On
        Unix, this prevents the process from creating core dump
        altogether.

    '''
    try:
        # Ensure the resource limit exists on this platform, by requesting its current value
        current_core_limit = resource.getrlimit(resource.RLIMIT_CORE)
    except BaseException as exc:
        raise FatalError(_('Your system does not support the RLIMIT_CORE resource limit, could not disable core dumps, exiting: {0}').format(exc))
    # Set hard and soft limits to zero, i.e. no core dump at all
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


#-----------------------------------------------------------------------------
def setWorkingDir(path):
    ''' Change the working directory of the process.
    '''
    try:
        os.chdir(path)
    except BaseException as exc:
        raise FatalError(_('Unable to change the working directory to {0}, exiting: {1}').format(quote(path), exc))


#-----------------------------------------------------------------------------
def setUmask(umask):
    ''' Change the file creation mask of the process.
    '''
    try:
        os.umask(umask)
    except BaseException as exc:
        raise FatalError(_('Unable to change the file creation mask, exiting: {0}').format(exc))


#-----------------------------------------------------------------------------
def setOwner(uid, gid):
    ''' Change the owning UID and GID of this process.

        Sets the GID then the UID in that order, to avoid permission errors.
    '''
    try:
        os.setgid(gid)
        os.setuid(uid)
    except BaseException as exc:
        raise FatalError(_('Unable to change the process owner (UID={0}, GID={1}, exiting: {2}').format(uid, gid, exc))


#-----------------------------------------------------------------------------
def detachProcess(detach, hookFirstFork):
    ''' Detach the current process from its parent.
        If detach is None, the process will not detach if it has been started
        either by init or inetd.
    '''
    if detach == None:
        if _isProcessStartedByInit() or _isProcessStartedByInetd():
            return False
    elif not detach:
        return False

    def forkAndExit(error):
        ''' Fork a child process, then exit the parent process.
        '''
        try:
            pid = os.fork()
            if pid > 0:
                os._exit(0)
        except OSError as exc:
            raise FatalError(_('Unable to detach the process: {0} ({1})').format(error, exc))

    forkAndExit(_('failed first fork.'))
    os.setsid()
    if hookFirstFork != None:
        hookFirstFork()
    forkAndExit(_('failed second fork.'))
    return True


#-----------------------------------------------------------------------------
def closeFiles(keepFiles, maxDescriptors):
    ''' Close every single file descriptor except the ones provided by keepFiles.
        Items in keepFiles may be either file-like objects or filenos.
    '''
    # Determine files that must not be closed
    excluded = set()
    keepFiles = keepFiles + [sys.stdin, sys.stdout, sys.stderr]
    for item in keepFiles:
        if item != None:
            if hasattr(item, 'fileno'):
                excluded.add(item.fileno())
            else:
                excluded.add(item)
    # Close all remaining files
    for fd in reversed(range(maxDescriptors)):
        if fd not in excluded:
            try:
                os.close(fd)
            except OSError as exc:
                if exc.errno == errno.EBADF:
                    # File descriptor was not open
                    pass
                else:
                    raise FatalError(_('Failed to close file descriptor {0}: {1}').format(fd, exc))


#-----------------------------------------------------------------------------
def redirectStandardStreams(stdin, stdout, stderr):
    ''' Redirect standard streams to custom defined ones.
        If a stream is None, the corresponding standard stream is redirected to os.devnull.
    '''
    _redirectStandardStream(sys.stdin, stdin)
    _redirectStandardStream(sys.stdout, stdout)
    _redirectStandardStream(sys.stderr, stderr)


#-----------------------------------------------------------------------------
def setSignalMap(signals):
    ''' Define the signal map of the process.
    '''
    if signals == None:
        return

    for (name, handler) in signals.items():
        if hasattr(signal, name):
            oldname = name
            name = getattr(signal, name)
            if handler == None:
                handler = signal.SIG_IGN
            if __DEBUG__: logDebug('Signal {0} ({1}) = {2}'.format(oldname, name, handler))
            signal.signal(name, handler)


#-----------------------------------------------------------------------------
def _redirectStandardStream(stdStream, newStream):
    ''' Redirect a system stream to a specified file.
        If newStream is None, stdStream is redirected to os.devnull.
    '''
    if stdStream != newStream:
        if newStream is None:
            newStream_fd = os.open(os.devnull, os.O_RDWR)
        else:
            newStream_fd = newStream.fileno()
        os.dup2(newStream_fd, stdStream.fileno())


#-----------------------------------------------------------------------------
def _isProcessStartedByInit():
    ''' Determine if the current process is started by the init process.

        The init process has a PID of 1.
    '''
    if os.getppid() == 1:
        return True
    return False


#-----------------------------------------------------------------------------
def _isProcessStartedByInetd():
    ''' Determine if the current process is started by the superserver (inetd).

        The internet superserver creates a network socket, and
        attaches it to the standard streams of the child process.
    '''
    stdin_fd = sys.__stdin__.fileno()
    if _isSocket(stdin_fd):
        return True
    return False


#-----------------------------------------------------------------------------
def _isSocket(fd):
    ''' Determine if the file descriptor is a socket.
    '''
    file_socket = socket.fromfd(fd, socket.AF_INET, socket.SOCK_RAW)
    try:
        socket_type = file_socket.getsockopt(socket.SOL_SOCKET, socket.SO_TYPE)
    except socket.error as exc:
        exc_errno = exc.args[0]
        if exc_errno != errno.ENOTSOCK:
            # Some socket-specific error
            return True
    else:
        # No error getting socket type
        return True
    # Not a socket
    return False


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
