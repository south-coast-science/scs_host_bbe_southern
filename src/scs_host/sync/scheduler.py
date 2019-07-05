"""
Created on 28 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Warning: only one sampler per semaphore!

http://semanchuk.com/philip/posix_ipc/#semaphore
https://pymotw.com/2/multiprocessing/basics.html
"""

import multiprocessing
import sys
import time

from scs_core.sync.interval_timer import IntervalTimer

from scs_host.sync.binary_semaphore import BinarySemaphore, BusyError


# --------------------------------------------------------------------------------------------------------------------

class Scheduler(object):
    """
    classdocs
    """

    DELAY_STEP =                    1.0     # (optional) delay between semaphores

    RELEASE_PERIOD =                0.3     # ScheduleItem release period
    HOLD_PERIOD =                   0.6     # ScheduleRunner hold period


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, schedule, verbose=False):
        """
        Constructor
        """
        self.__schedule = schedule
        self.__verbose = verbose

        self.__jobs = []


    # ----------------------------------------------------------------------------------------------------------------

    def run(self):
        delay = 0.0

        # prepare...
        for item in self.schedule.items:
            target = SchedulerItem(item, delay, self.verbose)
            job = multiprocessing.Process(name=item.name, target=target.run)
            job.daemon = True

            self.__jobs.append(job)

            delay += self.DELAY_STEP

        # run...
        for job in self.__jobs:
            job.start()

        # wait...
        if len(self.__jobs) > 0:
            self.__jobs[0].join()


    def terminate(self):
        for job in self.__jobs:
            job.terminate()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def schedule(self):
        return self.__schedule


    @property
    def verbose(self):
        return self.__verbose


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Scheduler:{schedule:%s, verbose:%s}" % (self.schedule, self.verbose)


# --------------------------------------------------------------------------------------------------------------------

class SchedulerItem(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, item, delay, verbose=False):
        """
        Constructor
        """
        self.__item = item                      # ScheduleItem
        self.__delay = delay                    # float (seconds)
        self.__verbose = verbose                # bool

        self.__mutex = BinarySemaphore(self.item.name)


    # ----------------------------------------------------------------------------------------------------------------

    def run(self):
        timer = IntervalTimer(self.item.interval)

        while timer.true():
            time.sleep(self.delay)

            if self.verbose:
                print('%s: run' % self.item.name, file=sys.stderr)
                sys.stderr.flush()

            # enable...
            self.__mutex.release()

            time.sleep(Scheduler.RELEASE_PERIOD)        # release period: hand semaphore to sampler

            try:
                # disable...
                self.__mutex.acquire(self.item.interval)        # TODO: what happens if semaphore cannot be acquired?

            except BusyError:
                # release...
                self.__mutex.release()

                print('%s: release' % self.item.name, file=sys.stderr)
                sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def item(self):
        return self.__item


    @property
    def delay(self):
        return self.__delay


    @property
    def verbose(self):
        return self.__verbose


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SchedulerItem:{item:%s, delay:%s, verbose:%s, mutex:%s}" % \
               (self.item, self.delay, self.verbose, self.__mutex)
