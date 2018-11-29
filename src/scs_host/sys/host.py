"""
Created on 16 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

http://dumb-looks-free.blogspot.co.uk/2014/05/beaglebone-black-bbb-revision-serial.html

"""

import os
import pyudev
import re
import socket
import subprocess
import sys

from scs_core.sys.disk_usage import DiskUsage
from scs_core.sys.node import Node


# --------------------------------------------------------------------------------------------------------------------

class Host(Node):
    """
    TI Sitara AM3358AZCZ100 processor
    """

    OS_ENV_PATH =           'SCS_ROOT_PATH'

    I2C_EEPROM =            2
    I2C_SENSORS =           2

    DFE_EEPROM_ADDR =       0x50
    DFE_UID_ADDR =          0x58


    # ----------------------------------------------------------------------------------------------------------------
    # devices...

    __OPC_SPI_PATH =        '/ocp/spi@48030000'                 # hard-coded path
    __OPC_SPI_DEVICE =      0

    __NDIR_SPI_PATH =       '/ocp/spi@481a0000'                 # hard-coded path
    __NDIR_SPI_DEVICE =     0

    __GPS_DEVICE =          1                                   # hard-coded path

    __NDIR_USB_DEVICE =     '/dev/ttyUSB0'                      # hard-coded path       - Alphasense USB device

    __PSU_DEVICE =          5                                   # hard-coded path


    # ----------------------------------------------------------------------------------------------------------------
    # directories...

    __DEFAULT_HOME_DIR =    '/home/scs'                         # hard-coded abs path
    __LOCK_DIR =            '/run/lock/southcoastscience'       # hard-coded abs path
    __TMP_DIR =             '/tmp/southcoastscience'            # hard-coded abs path

    __SCS_DIR =             'SCS'                               # hard-coded rel path

    __COMMAND_DIR =         'cmd'                               # hard-coded rel path
    __CONF_DIR =            'conf'                              # hard-coded rel path
    __AWS_DIR =             'aws'                               # hard-coded rel path
    __OSIO_DIR =            'osio'                              # hard-coded rel path
    __DFE_EEP_IMAGE =       'dfe_cape.eep'                      # hard-coded rel path


    # ----------------------------------------------------------------------------------------------------------------
    # commands...

    __SHUTDOWN_CMD =        '/sbin/shutdown'                    # hard-coded path


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def spi_bus(spi_path, spi_device):
        context = pyudev.Context()

        kernel_path = spi_path + '/channel@' + str(spi_device)
        # print("kernel_path: %s" % kernel_path)

        for device in context.list_devices(subsystem='spidev'):
            parent_node = device.parent
            # print("parent_node: %s" % parent_node)

            # print("type: %s" % type(parent_node))
            # print("OF_FULLNAME: %s" % parent_node['OF_FULLNAME'])
            # print("-")

            if parent_node['OF_FULLNAME'] == kernel_path:
                # opc_spidev = device.device_node

                # print("node: %s" % device.device_node)

                match = re.match('[^0-9]+([0-9]+).[0-9]+', device.device_node)      # e.g. /dev/spidev1.0
                # print("match: %s" % match)

                fields = match.groups()
                # print("bus: %s" % fields[0])

                return int(fields[0])

        raise OSError("No SPI bus could be found for %s" % kernel_path)


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def serial_number():
        serial = os.popen("hexdump -e '8/1 \"%c\"' /sys/bus/i2c/devices/0-0050/eeprom -s 16 -n 12").readline()

        return serial


    @staticmethod
    def enable_eeprom_access():
        # nothing needs to be done?
        pass


    @staticmethod
    def mcu_temp():
        return None


    @classmethod
    def shutdown(cls):
        subprocess.call([cls.__SHUTDOWN_CMD, 'now'])


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
        return cls.spi_bus(cls.__OPC_SPI_PATH, cls.__OPC_SPI_DEVICE)
        # return cls.__OPC_SPI_BUS


    @classmethod
    def opc_spi_device(cls):
        return cls.__OPC_SPI_DEVICE


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def disk_usage(cls, volume):
        st = os.statvfs(volume)

        free = st.f_bavail * st.f_frsize
        used = (st.f_blocks - st.f_bfree) * st.f_frsize
        total = st.f_blocks * st.f_frsize

        return DiskUsage(volume, free, used, total)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def home_dir(cls):
        return os.environ[cls.OS_ENV_PATH] if cls.OS_ENV_PATH in os.environ else cls.__DEFAULT_HOME_DIR


    @classmethod
    def lock_dir(cls):
        return cls.__LOCK_DIR


    @classmethod
    def tmp_dir(cls):
        return cls.__TMP_DIR


    @classmethod
    def scs_dir(cls):
        return os.path.join(cls.home_dir(), cls.__SCS_DIR)


    @classmethod
    def command_dir(cls):
        return os.path.join(cls.home_dir(), cls.__SCS_DIR, cls.__COMMAND_DIR)


    @classmethod
    def conf_dir(cls):
        return os.path.join(cls.home_dir(), cls.__SCS_DIR, cls.__CONF_DIR)


    @classmethod
    def aws_dir(cls):
        return os.path.join(cls.home_dir(), cls.__SCS_DIR, cls.__AWS_DIR)


    @classmethod
    def osio_dir(cls):
        return os.path.join(cls.home_dir(), cls.__SCS_DIR, cls.__OSIO_DIR)


    @classmethod
    def eep_image(cls):
        return os.path.join(cls.home_dir(), cls.__SCS_DIR, cls.__DFE_EEP_IMAGE)
