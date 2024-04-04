#!/usr/bin/env python3

"""
Created on 7 Nov 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

print("os...")
print("actual: %s" % Host.os_release())
print("acceptable: %s" % Host.has_acceptable_os_release())
print("-")

print("kernel...")
print("actual: %s" % Host.kernel_release())
print("acceptable: %s" % Host.has_acceptable_kernel_release())
print("-")

print("greengrass...")
print("minimum: %s" % Host.minimum_required_greengrass_version())
print("actual: %s" % Host.greengrass_version())
