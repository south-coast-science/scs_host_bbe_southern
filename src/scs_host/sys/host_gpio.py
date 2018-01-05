"""
Created on 22 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Note: this class only exists in order to gather together all the warning messages generated by the
incorrectly-constructed Adafruit_BBIO.GPIO package.
"""

import Adafruit_BBIO.GPIO as GPIO


# --------------------------------------------------------------------------------------------------------------------

class HostGPIO(object):
    """
    classdocs
    """
    IN = GPIO.IN
    OUT = GPIO.OUT

    RISING = GPIO.RISING
    FALLING = GPIO.FALLING

    HIGH = GPIO.HIGH
    LOW = GPIO.LOW


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def cleanup():
        GPIO.cleanup()


    @staticmethod
    def setup(pin, direction):
        GPIO.setup(pin, direction)


    @staticmethod
    def input(pin):
        GPIO.input(pin)


    @staticmethod
    def output(pin, direction):
        GPIO.setup(pin, direction)


    @staticmethod
    def wait_for_edge(pin, edge):
        GPIO.wait_for_edge(pin, edge)