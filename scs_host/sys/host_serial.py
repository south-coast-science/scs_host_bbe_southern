"""
Created on 26 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/port
"""

import serial
import time

from scs_host.lock.lock import Lock


# --------------------------------------------------------------------------------------------------------------------

class HostSerial(object):
    """
    classdocs
    """

    EOL =               "\r\n"

    __PORT_PREFIX =     "/dev/ttyO"           # hard-coded path


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, port_number, baud_rate, hard_handshake=False):
        """
        Constructor
        """
        self.__port_number = port_number
        self.__baud_rate = baud_rate
        self.__hard_handshake = hard_handshake

        self.__ser = None


    # ----------------------------------------------------------------------------------------------------------------

    def open(self, timeout):
        # lock...
        Lock.acquire(self.__lock_name, timeout)

        # port...
        port = HostSerial.__PORT_PREFIX + str(self.__port_number)

        self.__ser = serial.Serial(port=port, baudrate=self.__baud_rate,
                                   rtscts=self.__hard_handshake, dsrdtr=False, timeout=1)

        if self.__ser.is_open:
            self.__ser.close()

        self.__ser.open()


    def close(self):
        try:
            # port...
            if self.__ser:
                self.__ser.close()
                self.__ser = None

        finally:
            # lock...
            Lock.release(self.__lock_name)


    # ----------------------------------------------------------------------------------------------------------------

    def read_line(self, eol, timeout):
        end_time = time.time() + timeout

        line = ""
        while True:
            if time.time() > end_time:
                break

            char = self.__ser.read().decode(errors='ignore')
            line += char

            if line.endswith(eol):
                break

        return line.strip()


    def write_line(self, text, eol=None):
        terminator = HostSerial.EOL if eol is None else eol

        text_ln = text.strip() + terminator
        packet = text_ln.encode()

        return self.__ser.write(packet)


    # ----------------------------------------------------------------------------------------------------------------

    def read(self, count):
        chars = self.__ser.read(count)

        return chars


    def write(self, *chars):
        self.__ser.write(bytearray(chars))


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def __lock_name(self):
        return HostSerial.__name__ + "-" + str(self.__port_number)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "HostSerial:{port_number:%d, baud_rate=%d, hard_handshake=%s, serial:%s}" % \
                    (self.__port_number, self.__baud_rate, self.__hard_handshake, self.__ser)
