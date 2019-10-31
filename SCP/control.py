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

import threading
#from pylontech_com import *
#from conext_com import *
#from data_log import *



# EMBEDDING Controller_Thread CLASS ----------------------------------------------------

import threading
import time



class dataLogThread (threading.Thread):

    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self._stop = threading.Event()

    def __del__(self):
        ''' Destructor for this class. '''
        self._stop.set()
        print ("deleted")



    def run(self):
        print ("Starting " + self.name)
        while True:
            if self.stopped():
                print("Exiting " + self.name)
                return
            time.sleep(1)
            print("%s: %s" % (self.name, time.ctime(time.time())))


    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()













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

        #self.__operational_mode_default


        #Variables to manage logging control
        self.__dlt_exist=False




    def __del__(self):
        ''' Destructor for this class. '''
        self.__dlt.stop()



    def dataLogStart(self):

        if not self.__dlt_exist:
            self.__dlt=dataLogThread(1, "Log-1")
            self.__dlt.start()
            self.__dlt_exist=True
            print ("Log Started")
        else:
            print("Log Already Started")

    def dataLogStop(self):

        if self.__dlt_exist:
            self.__dlt.stop()
            self.__dlt_exist = False
            del self.__dlt
            print("Log Stopped")
        else:
            print("Log Already Stopped")

    def dataLogRestart(self):

        if not self.__dlt_exist:
            self.__dlt=dataLogThread(1, "Log-1")
            self.__dlt.start()
            self.__dlt_exist=True
            print ("Log Started")
        elif self.__dlt_exist:
            self.__dlt.stop()
            del self.__dlt
            self.__dlt = dataLogThread(1, "Log-1")
            self.__dlt.start()
            print ("Log Restarted")
        else:
            print("ERROR Restart Log")


    def dataLogStatus(self):

        if self.__dlt_exist:
            print("Log Running")
            return self.__dlt.isAlive()
        else:
            print("Log Stopped")
            return False




if __name__ == '__main__':

    SystemControl.dataLogStart()
    print("Exiting Main Thread")







