"""
Created on 4 Jul 2016

http://tightdev.net/SpiDev_Doc.pdf
http://www.takaitra.com/posts/492

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

/boot/uEnv.txt...
cape_disable=bone_capemgr.disable_partno=BB-BONELT-HDMI,BB-BONELT-HDMIN
cape_enable=bone_capemgr.enable_partno=BB-SPIDEV0,BB-SPIDEV1

chmod a+rw /sys/devices/platform/bone_capemgr/slots
"""

import spidev


# TODO: put tx lock in open / close

# --------------------------------------------------------------------------------------------------------------------

class HostSPI(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, bus, device, mode, max_speed):
        """
        Constructor
        """

        self.__connection = bus
        self.__device = device
        self.__mode = mode
        self.__max_speed = max_speed

        self.__connection = None


    # ----------------------------------------------------------------------------------------------------------------

    def open(self):
        if self.__connection:
            return

        self.__connection = spidev.SpiDev()
        self.__connection.open(self.__connection, self.__device)

        self.__connection.mode = self.__mode
        self.__connection.max_speed_hz = self.__max_speed


    def close(self):
        self.__connection.close()
        self.__connection = None


    # ----------------------------------------------------------------------------------------------------------------

    def xfer(self, args):
        self.__connection.xfer(args)


    def read_bytes(self, count):
        return self.__connection.readbytes(count)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "HostSPI:{bus:%d, device:%s, mode:%d, max_speed:%d, bus:%s}" % \
               (self.__connection, self.__device, self.__mode, self.__max_speed, self.__connection)



