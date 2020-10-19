#!/usr/bin/env python3

"""
Created on 2 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

home_dir = Host.home_path()
print("home_dir: %s" % home_dir)

print("-")

try:
    lock_dir = Host.lock_dir()
    print("lock_dir: %s" % lock_dir)
except NotImplementedError:
    print("lock_dir: None")

try:
    tmp_dir = Host.tmp_dir()
    print("tmp_dir: %s" % tmp_dir)
except NotImplementedError:
    print("tmp_dir: None")

try:
    command_path = Host.command_path()
    print("command_path: %s" % command_path)
except NotImplementedError:
    print("command_path: None")

print("-")

scs_path = Host.scs_path()
print("scs_path: %s" % scs_path)

conf_dir = Host.conf_dir()
print("conf dir: %s" % conf_dir)

aws_dir = Host.aws_dir()
print("aws dir: %s" % aws_dir)

osio_dir = Host.osio_dir()
print("osio dir: %s" % osio_dir)

print("-")
