"""
Created on 28 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Warning: only one sampler per semaphore!

http://semanchuk.com/philip/posix_ipc/#semaphore
https://pymotw.com/2/multiprocessing/basics.html
"""

import copy
import sys
import time

from multiprocessing import Manager

from scs_core.sync.interval_timer import IntervalTimer
from scs_core.sync.synchronised_process import SynchronisedProcess

from scs_host.sync.binary_semaphore import BinarySemaphore, BusyError


# --------------------------------------------------------------------------------------------------------------------

class Scheduler(object):
    """
    classdocs
    """

    DELAY_STEP =                    0.0     # (optional) delay between semaphores

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

    def start(self):
        try:
            delay = 0.0

            # prepare...
            for item in self.schedule.items:
                job = SchedulerItem(item, delay, self.verbose)
                # job = Process(name=item.name, target=target.run)
                # job.daemon = True

                self.__jobs.append(job)

                delay += self.DELAY_STEP

            # run...
            for job in self.__jobs:
                job.start()

            # wait...
            # if len(self.__jobs) > 0:
            #     self.__jobs[0].join()

        except (BrokenPipeError, KeyboardInterrupt):
            pass


    # def terminate(self):
    #     print("attempting to terminate", file=sys.stderr)
    #     sys.stderr.flush()
    #
    #     SchedulerItem.RUNNING = False
        # for job in self.__jobs:
        #     print("attempting to terminate %s" % job, file=sys.stderr)
        #     sys.stderr.flush()

            # job.terminate()

    def stop(self):
        for job in self.__jobs:
            job.set_running(False)
            # job.stop()

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

class SchedulerItem(SynchronisedProcess):
    """
    classdocs
    """

    def __init__(self, item, delay, verbose=False):
        """
        Constructor
        """
        manager = Manager()

        SynchronisedProcess.__init__(self, manager.list())

        self._value.append(True)

        self.__item = item                                  # ScheduleItem
        self.__delay = delay                                # float (seconds)
        self.__verbose = verbose                            # bool

        self.__mutex = BinarySemaphore(self.item.name, True)

        self.__running = True

    # ----------------------------------------------------------------------------------------------------------------

    def stop(self):
        try:
            print('%s: stop' % self.item.name, file=sys.stderr)
            sys.stderr.flush()
            # super().stop()

        except (BrokenPipeError, KeyboardInterrupt):
            pass


    def run(self):
        running = True

        try:
            pass
            self.__mutex.acquire(self.item.interval)            # protect against initially-released semaphores
        except BusyError:
            pass

        try:
            timer = IntervalTimer(self.item.interval)

            while timer.true():
                with self._lock:
                    running = copy.deepcopy(self._value[0])

                print('%s: run loop: %s' % (self.item.name, running), file=sys.stderr)
                sys.stderr.flush()

                if not running:
                    print('%s: exiting run' % self.item.name, file=sys.stderr)
                    sys.stderr.flush()
                    return

                if self.verbose:
                    print('%s: run' % self.item.name, file=sys.stderr)
                    sys.stderr.flush()

                # enable...
                self.__mutex.release()

                time.sleep(Scheduler.RELEASE_PERIOD)            # release period: hand semaphore to sampler

                try:
                    # disable...
                    pass
                    self.__mutex.acquire(self.item.interval)

                except BusyError:
                    # release...
                    pass
                    self.__mutex.release()

                    print('%s: release' % self.item.name, file=sys.stderr)
                    sys.stderr.flush()

                time.sleep(self.delay)

        except (BrokenPipeError, KeyboardInterrupt):
            pass


    # ----------------------------------------------------------------------------------------------------------------
    # setter for client process...

    def set_running(self, running):
        with self._lock:
            self._value[0] = running


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
