#!/usr/bin/env python3

"""
Created on 29 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

home_path = Host.home_path()
print("home_path: %s" % home_path)

du = Host.disk_usage(home_path)
print("du: %s" % du)

