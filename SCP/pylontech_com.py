""" This module contains classes and functions to establish a communication with the
 Pylontech US2000B Plus Battery Management System.

**Description:**

    The communication is established over a USB to RS232 adapter, which is connected
    to the console port of the first battery. The console must be initialised with a
    defined string at a baud rate of; 1200,8,n,1. After a successful initialisation
    one can communicate via a text based terminal interface operating at a baud rate
    of; 115200,8,n,1.
    The functions in this module will allow to extract the required information necessary
    for the Solar-Control-Program. The main parameters extracted from the BMS are:
        1. SoC
        2. Voltage
        3. Current
        4. Temperature
The main class in this module (``US2000B``) allows the user to
communicate with the Pylontech US2000B Plus BMS.

"""

import serial,time


# EMBEDDING CIRCUIT CLASS ----------------------------------------------------

class US2000B(object):
    """This class implements the serial connection functions """
    def __init__(self):
        ''' Constructor for this class. '''
        #self.__port = 0
        #try:
            #tmp = open('tmp.txt', 'r')
            #self.__comp_time_disabled = float(tmp.read())
            #tmp.close()
            # Store configuration file values
        #except:
            #Keep preset values
            #self.__comp_time_disabled=0

    def __del__(self):
        ''' Destructor for this class. '''
        #if self.__port !=0:
            #self.close()


    def initialise(self, port='/dev/ttyUSB0'):
        """ Initialises the console communication fo the US2000B BMS
                :param port: path to serial port. Default='/dev/ttyUSB0'
                :returns Boolean value True or False """
        temp_port = serial.Serial(port,1200, timeout=0.05)
        temp_port.write('~20014682C0048520FCC3\r')
        time.sleep(5)
        temp_port = serial.Serial(port,115200, timeout=0.05)
        temp_port.write('\r\n')
        temp_receive = repr(temp_port.read(1000))
        temp_port.close()
        return temp_receive == ""






    def open(self, port='/dev/ttyUSB0', baud=19200):
        """ Open serial port for communication
                :param port: path to serial port. Default='/dev/ttyUSB0'
                :param baud: defines the baud rate. Default=19200
                :returns Boolean value True or False """
        self.__port = serial.Serial(port,baud, timeout=0.05)
        #self.sensor = sensor(self.__port)
        #self.error = error(self.__port)
        #self.compressor = compressor(self.__port, self.__comp_time_disabled)
        return self.__port.is_open

    def close(self):
        """ Close serial port """
        self.__port.close()
        #self.sensor.__del__()
        #self.error.__del__()
        #self.__comp_time_disabled = self.compressor.__del__()
        #try:
        #    tmp = open('tmp.txt', 'w+')
        #    tmp.write(str(self.__comp_time_disabled))
        #    tmp.close()
            # Store configuration file values
        #except:
        #    print'ERROR in saving the temp file!'
        return not self.__port.is_open