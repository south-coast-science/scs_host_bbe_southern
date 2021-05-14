#!/usr/bin/env python3

"""
Created on 8 May 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_host.bus.i2c import I2C


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.Sensors.open()
    I2C.Sensors.start_tx(0x45)      # external SHT31

    while True:
        start = time.time()

        try:
            status_msb, status_lsb, _ = I2C.Sensors.read_cmd16(0xf32d, 3)       # test with sensor present and absent
            elapsed = time.time() - start
            print("elapsed: %f" % elapsed)

            status = (status_msb << 8) | status_lsb
            print("status: 0x%4x" % status)
            break

        except OSError as ex:
            elapsed = time.time() - start
            print("elapsed: %f" % elapsed)

            print(repr(ex))
            time.sleep(2)

finally:
    I2C.Sensors.end_tx()
    I2C.Sensors.close()

