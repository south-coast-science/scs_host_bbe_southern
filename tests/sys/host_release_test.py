#!/usr/bin/env python3

"""
Created on 7 Nov 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

print("minimum: %s" % Host.MINIMUM_OS_RELEASE)

print("acceptable: %s" % Host.has_acceptable_os_release())
