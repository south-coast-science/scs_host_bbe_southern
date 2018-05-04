"""
Created on 28 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Warning: only one sampler per semaphore!

http://semanchuk.com/philip/posix_ipc/#semaphore
"""

import sys
import time

from scs_core.sync.runner import Runner

from scs_host.sync.binary_semaphore import BinarySemaphore
from scs_host.sync.scheduler import Scheduler


# --------------------------------------------------------------------------------------------------------------------

class ScheduleRunner(Runner):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name, verbose=False):
        """
        Constructor
        """
        self.__name = name
        self.__verbose = verbose

        self.__mutex = BinarySemaphore(self.name)


    # ----------------------------------------------------------------------------------------------------------------

    def samples(self, sampler):
        while True:
            try:
                # start...
                self.__mutex.acquire()

                if self.verbose:
                    print('%s: start' % self.name, file=sys.stderr)
                    sys.stderr.flush()

                yield sampler.sample()

            finally:
                # done...
                self.__mutex.release()

                if self.verbose:
                    print('%s: done' % self.name, file=sys.stderr)
                    sys.stderr.flush()

                time.sleep(Scheduler.HOLD_PERIOD)


    def reset(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__name


    @property
    def verbose(self):
        return self.__verbose


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ScheduleRunner:{name:%s, verbose:%s, mutex:%s}" % (self.name, self.verbose, self.__mutex)
