"""
Created on 16 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

http://dumb-looks-free.blogspot.co.uk/2014/05/beaglebone-black-bbb-revision-serial.html

"""

import os
import socket
import subprocess

from pathlib import Path
from scs_core.sys.node import Node


# --------------------------------------------------------------------------------------------------------------------

class Host(Node):
    """
    TI Sitara AM3358AZCZ100 processor
    """

    I2C_EEPROM =            2
    I2C_SENSORS =           2

    DFE_EEPROM_ADDR =       0x50
    DFE_UID_ADDR =          0x58
    if "SCS_ROOT_PATH" in os.environ:
        __SCS = os.environ["SCS_ROOT_PATH"]  # hard-coded path
    else:
        __SCS = os.path.join(str(Path.home()), "SCS")
    COMMAND_DIR =           os.path.join(__SCS, "cmd")                # hard-coded path

    DFE_EEP_IMAGE =         os.path.join(__SCS, "dfe_cape.eep")        # hard-coded path

    SCS_LOCK =              "/run/lock/southcoastscience/"      # hard-coded path

    SCS_TMP =               "/tmp/southcoastscience/"           # hard-coded path


    # ----------------------------------------------------------------------------------------------------------------

    __OPC_SPI_BUS =         1                                   # based on spidev
    __OPC_SPI_DEVICE =      0                                   # based on spidev

    __NDIR_SPI_BUS =        2                                   # based on spidev
    __NDIR_SPI_DEVICE =     0                                   # based on spidev

    __GPS_DEVICE =          1                                   # hard-coded path

    __NDIR_USB_DEVICE =     "/dev/ttyUSB0"                      # hard-coded path       - Alphasense USB device

    __PSU_DEVICE =          5                                   # hard-coded path

    __SCS_CONF =            "conf/"                             # hard-coded path
    __SCS_AWS =             "aws/"                              # hard-coded path
    __SCS_OSIO =            "osio/"                             # hard-coded path


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def serial_number():
        serial = os.popen("hexdump -e '8/1 \"%c\"' /sys/bus/i2c/devices/0-0050/eeprom -s 16 -n 12").readline()

        return serial


    @staticmethod
    def power_cycle():
        subprocess.call(['sudo', 'reboot'])     # TODO: control the power cycle feature on the PSU


    @staticmethod
    def enable_eeprom_access():
        # nothing needs to be done?
        pass


    @staticmethod
    def mcu_temp():
        return None


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def gps_device(cls):
        return cls.__GPS_DEVICE             # we might have to search for it instead


    @classmethod
    def ndir_usb_device(cls):
        return cls.__NDIR_USB_DEVICE        # we might have to search for it instead


    @classmethod
    def psu_device(cls):
        return cls.__PSU_DEVICE             # we might have to search for it instead


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def name(cls):
        return socket.gethostname()


    @classmethod
    def ndir_spi_bus(cls):
        return cls.__NDIR_SPI_BUS


    @classmethod
    def ndir_spi_device(cls):
        return cls.__NDIR_SPI_DEVICE


    @classmethod
    def opc_spi_bus(cls):
        return cls.__OPC_SPI_BUS


    @classmethod
    def opc_spi_device(cls):
        return cls.__OPC_SPI_DEVICE


    @classmethod
    def scs_dir(cls):
        return cls.__SCS


    @classmethod
    def conf_dir(cls):
        return os.path.join(cls.__SCS, cls.__SCS_CONF)


    @classmethod
    def aws_dir(cls):
        return os.path.join(cls.__SCS, cls.__SCS_AWS)


    @classmethod
    def osio_dir(cls):
        return os.path.join(cls.__SCS, cls.__SCS_OSIO)
