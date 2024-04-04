#!/usr/bin/env python3

"""
Created on 7 Nov 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

print("os...")
print("minimum: %s" % Host.minimum_required_os_version())
print("actual: %s" % Host.os_version())
print("-")

print("kernel...")
print("minimum: %s" % Host.minimum_required_kernel_version())
print("actual: %s" % Host.kernel_version())
print("-")

print("greengrass...")
print("minimum: %s" % Host.minimum_required_greengrass_version())
print("actual: %s" % Host.greengrass_version())
