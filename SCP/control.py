""" This module contains classes and functions to control the solar system based on the detected BMS parameter and
settings defined in this class.

**Description:**

    This module implements the required functions to enable and disable the Schneider XW+ inverter based on the
    detected BMS parameters. It uses functions from both, pylontech_com and conext_com modules. It will allow the
    user to enable the readout and write program specific parameters.
    The main functions implemented are:
        1. control_system()
        2. set_low_SoC_cutout()
        3. set_operational_mode()


The main class in this module ("Control") allows the user to
run the control system.


"""
from threading import Thread
from pylontech_com import *
from conext_com import *
from data_log import *


# EMBEDDING SystemControl CLASS ----------------------------------------------------

class SystemControl():
    """This class implements the serial connection functions """

    def __init__(self):
        ''' Constructor for this class. '''

        self.__low_SoC_default_summer                           =22   #Default value for low SoC
        self.__low_SoC_default_winter                           =40  # Default value for low SoC

        self.__low_battery_voltage_default_summer               =46.7 #Default value for low battery voltage
        self.__low_battery_voltage_hysteresis_default_summer    =2.2  #Default value for low battery voltage hysteresis

        self.__low_battery_voltage_default_winter               =47.5  # Default value for low battery voltage
        self.__low_battery_voltage_hysteresis_default_winter    = 3.0  # Default value for low battery voltage hysteresis

        self.__operational_mode_default



    def __del__(self):
        ''' Destructor for this class. '''











