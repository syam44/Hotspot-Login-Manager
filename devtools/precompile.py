#!/usr/bin/python3 -OO
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
# Description: Precompile the sources into .pyo files.
#


#-----------------------------------------------------------------------------
import compileall
import os


#-----------------------------------------------------------------------------
if __name__ == '__main__':
    base_path = os.path.realpath(os.path.dirname(__file__) + '/..')
    compileall.compile_dir(base_path + '/hotspot_login_manager', 20, quiet = True)
    compileall.compile_dir(base_path, 0, quiet = True)


#-----------------------------------------------------------------------------
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
