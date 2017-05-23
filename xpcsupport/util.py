# XPCSupport: Support tool for XPC Computers
# Copyright (C) 2017 Xotic PC
#
# This file is part of `xpcsupport`.
#
# `xpcsupport` is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# `xpcsupport` is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with `xpcsupport`; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
This will collect logs and other information to assist support and dev
teams.
"""

import os
from os import path
import shutil
import tempfile
import platform

from .model import determine_model
from .mockable import SubProcess


def dump_logs(base):
    fp = open(path.join(base, 'systeminfo.txt'), 'x')
    # XPCReference
    fp.write('XPC Model: {}\n'.format(determine_model()))
    fp.write('OS Version: {}\n'.format(', '.join(platform.dist())))
    fp.write('Kernel Version: {}\n'.format(platform.uname().release))

    fp = open(path.join(base, 'dmidecode'), 'xb')
    SubProcess.check_call(['dmidecode'], stdout=fp)

    fp = open(path.join(base, 'lspci'), 'xb')
    SubProcess.check_call(['lspci', '-vv'], stdout=fp)

    fp = open(path.join(base, 'lsusb'), 'xb')
    SubProcess.check_call(['lsusb', '-vv'], stdout=fp)

    fp = open(path.join(base, 'dmesg'), 'xb')
    SubProcess.check_call(['dmesg'], stdout=fp)

    for parts in [('Xorg.0.log',), ('syslog',)]:  #, ('apt', 'history.log')]:
        src = path.join('/var/log', *parts)
        if path.isfile(src):
            dst = path.join(base, *parts)
            dst_dir = path.dirname(dst)
            if not path.isdir(dst_dir):
                os.makedirs(dst_dir)
            assert not path.exists(dst)
            shutil.copy(src, dst)


def create_tmp_logs(func=dump_logs):
    tmp = tempfile.mkdtemp(prefix='logs.')
    base = path.join(tmp, 'system76-logs')
    os.mkdir(base)
    if func is not None:
        func(base)
    tgz = path.join(tmp, 'system76-logs.tgz')
    cmd = [
        'tar', '-czv',
        '-f', tgz,
        '-C', tmp,
        'system76-logs',
    ]
    SubProcess.check_call(cmd)
    return (tmp, tgz)


def create_logs(homedir, func=dump_logs):
    (tmp, src) = create_tmp_logs(func)
    assert path.isdir(homedir)
    dst = path.join(homedir, path.basename(src))
    shutil.copy(src, dst)
    shutil.rmtree(tmp)
    return dst

