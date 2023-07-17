#!/usr/bin/env python3

"""
Created on 14 Jul 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_host.sync.binary_semaphore import BinarySemaphore


# --------------------------------------------------------------------------------------------------------------------

semaphore = BinarySemaphore('scs-provisioning', True)
print(semaphore)

try:
    while True:
        semaphore.release()
        print('released semaphore')
        time.sleep(1)

        start_time = time.time()
        semaphore.acquire()
        wait = time.time() - start_time
        print('acquired semaphore after %0.3f' % wait)
        time.sleep(3)

except KeyboardInterrupt:
    pass
