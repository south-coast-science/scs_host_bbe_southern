#!/usr/bin/env python3

"""
Created on 28 Nov 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

spi_path = '/ocp/spi@48030000'
spi_device = '0'

bus = Host.spi_bus(spi_path, spi_device)

print("bus:%d" % bus)
