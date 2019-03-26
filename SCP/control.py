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

# EMBEDDING ThreadedControl CLASS ----------------------------------------------------

class Socket_BMS_Thread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self._stop = False

    def run(self, N_MODULES=1, UDP_IP ="127.0.0.1", UDP_PORT1 = 5005, UDP_PORT2 = 5006, UDP_PORT3 = 5007):
        BMS = US2000B()
        BMS.open()

        for i in range(1,10):
            if BMS.is_connected():
                break
            time.sleep(1)
            if i == 5:
                BMS.initialise()
            if i == 10:
                print "ERROR, no connection could be established!"
                return
        BMS.socket_BMS(1,self._stop)



    def stop(self):
        self._stop = True







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











