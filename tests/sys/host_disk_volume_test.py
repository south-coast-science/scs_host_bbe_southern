#!/usr/bin/env python3

"""
Created on 15 Oct 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.sys.disk_volume import ReportedDiskVolume

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

mounted_on = '/srv/SCS_logging'
print(mounted_on)

volume = Host.disk_volume(mounted_on)
print(volume)
print(JSONify.dumps(volume))
print("-")

mounted_on = '/'
print(mounted_on)

volume = Host.disk_volume(mounted_on)
print(volume)
print(JSONify.dumps(volume))

usage = Host.disk_usage(mounted_on)
print(usage)

print("-")

jstr = JSONify.dumps(volume)
print(jstr)

jdict = json.loads(jstr)
volume = ReportedDiskVolume.construct_from_jdict(jdict)
print(volume)

