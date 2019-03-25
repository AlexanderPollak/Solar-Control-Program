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

import serial,time,re,datetime,csv,os
import numpy as np
import socket


# EMBEDDING US2000B CLASS ----------------------------------------------------

class US2000B(object):
    """This class implements the serial connection functions """
    def __init__(self):
        ''' Constructor for this class. '''
        self.__port = 0
    def __del__(self):
        ''' Destructor for this class. '''
        if self.__port !=0:
            self.close()




    def initialise(self, port='/dev/ttyUSB0'):
        """Initialises the console communication fo the US2000B BMS
        Args:
            port: path to serial port. Default='/dev/ttyUSB0'
        Returns: Boolean value True or False"""
        temp_port = serial.Serial(port,1200, timeout=0.05)
        temp_port.write('~20014682C0048520FCC3\r')
        time.sleep(5)
        temp_port = serial.Serial(port,115200, timeout=0.05)
        temp_port.write('\r\n')
        temp_receive = repr(temp_port.read(1000))
        temp_port.close()
        return temp_receive == str("'\\n\\rpylon>\\n\\rpylon>'")

    def open(self, port='/dev/ttyUSB0', baud=115200):
        """Open serial port for communication

        Args:
            port: path to serial port. Default='/dev/ttyUSB0'
            baud: defines the baud rate. Default=115200

        Returns: Boolean value True or False

        """
        self.__port = serial.Serial(port,baud, timeout=0.05)
        return self.__port.is_open

    def close(self):
        """Close serial port

        Returns: Boolean value True or False

        """
        self.__port.close()
        return not self.__port.is_open

    def is_connected(self):
        """This function checks if the connection to the BMS is established
        and if the BMS responds to readout commands.

        Returns: Boolean value True or False

        """
        self.__port.write('\r\n')
        temp_receive = repr(self.__port.read(1000))
        return temp_receive == str("'\\n\\rpylon>\\n\\rpylon>'")


    def read_SoC(self, N_MODULES=1):
        """This function returns the State of Charge value of the
        Pylontech Batteries.
        Args:
            N_MODULES: number of modules to be read. Default=1

        Returns: list of length n_modules containing numpy arrays with the [SOC] dtype=float64.

        """
        try:
            SoC_array = np.zeros((N_MODULES, 1))
            self.__port.write('pwr\r')
            time.sleep(0.5)
            rec_str = self.__port.read(2200)
            rec_int = re.findall(r'\d+', rec_str)
            #Writes values into SOC_array and returns it.
            if N_MODULES == 1:
                SoC_array[0,0] = str(rec_int[8])
                return SoC_array
            if N_MODULES == 2:
                SoC_array[0,0] = str(rec_int[8])
                SoC_array[1,0] = str(rec_int[23])
                return SoC_array
            if N_MODULES == 3:
                SoC_array[0,0] = str(rec_int[8])
                SoC_array[1,0] = str(rec_int[23])
                SoC_array[2,0] = str(rec_int[38])
                return SoC_array
            if N_MODULES == 4:
                SoC_array[0,0] = str(rec_int[8])
                SoC_array[1,0] = str(rec_int[23])
                SoC_array[2,0] = str(rec_int[38])
                SoC_array[3,0] = str(rec_int[53])
                return SoC_array
            if N_MODULES == 5:
                SoC_array[0,0] = str(rec_int[8])
                SoC_array[1,0] = str(rec_int[23])
                SoC_array[2,0] = str(rec_int[38])
                SoC_array[3,0] = str(rec_int[53])
                SoC_array[4,0] = str(rec_int[68])
                return SoC_array
            if N_MODULES == 6:
                SoC_array[0,0] = str(rec_int[8])
                SoC_array[1,0] = str(rec_int[23])
                SoC_array[2,0] = str(rec_int[38])
                SoC_array[3,0] = str(rec_int[53])
                SoC_array[4,0] = str(rec_int[68])
                SoC_array[5,0] = str(rec_int[83])
                return SoC_array
            if N_MODULES == 7:
                SoC_array[0,0] = str(rec_int[8])
                SoC_array[1,0] = str(rec_int[23])
                SoC_array[2,0] = str(rec_int[38])
                SoC_array[3,0] = str(rec_int[53])
                SoC_array[4,0] = str(rec_int[68])
                SoC_array[5,0] = str(rec_int[83])
                SoC_array[6,0] = str(rec_int[98])
                return SoC_array
            if N_MODULES == 8:
                SoC_array[0,0] = str(rec_int[8])
                SoC_array[1,0] = str(rec_int[23])
                SoC_array[2,0] = str(rec_int[38])
                SoC_array[3,0] = str(rec_int[53])
                SoC_array[4,0] = str(rec_int[68])
                SoC_array[5,0] = str(rec_int[83])
                SoC_array[6,0] = str(rec_int[98])
                SoC_array[7,0] = str(rec_int[113])
                return SoC_array
            else:
                return SoC_array
        except:
            print"ERROR no communication possible, check if the connection has been opened with open()"

    def read_BMS(self, N_MODULES=1):
        """This function returns the values of the: SoC, Voltage, Current, and Temperature
        provided by the Pylontech BMS.
        Args:
            N_MODULES: number of modules to be read. Default=1

        Returns: list of length n_modules containing numpy arrays with the:
        [SoC, Voltage, Current, Temperature] dtype=float64.

        """
        try:
            BMS_array = np.zeros((N_MODULES, 4))
            self.__port.write('pwr\r')
            time.sleep(0.5)
            rec_str = self.__port.read(2200)
            rec_int = re.findall(r'\d+', rec_str)
            #Writes values into BMS_array and returns it.
            if N_MODULES == 1:
                BMS_array[0,0] = str(rec_int[8])#SOC
                BMS_array[0,1] = str(rec_int[1])#Voltage
                BMS_array[0,2] = str(rec_int[2])#Current
                BMS_array[0,3] = str(rec_int[3])#Temperature
                return BMS_array

            if N_MODULES == 2:
                BMS_array[0,0] = str(rec_int[8])#SOC
                BMS_array[0,1] = str(rec_int[1])#Voltage
                BMS_array[0,2] = str(rec_int[2])#Current
                BMS_array[0,3] = str(rec_int[3])#Temperature

                BMS_array[1,0] = str(rec_int[23])#SOC
                BMS_array[1,1] = str(rec_int[16])#Voltage
                BMS_array[1,2] = str(rec_int[17])#Current
                BMS_array[1,3] = str(rec_int[18])#Temperature
                return BMS_array

            if N_MODULES == 3:
                BMS_array[0, 0] = str(rec_int[8])  # SOC
                BMS_array[0, 1] = str(rec_int[1])  # Voltage
                BMS_array[0, 2] = str(rec_int[2])  # Current
                BMS_array[0, 3] = str(rec_int[3])  # Temperature

                BMS_array[1, 0] = str(rec_int[23])  # SOC
                BMS_array[1, 1] = str(rec_int[16])  # Voltage
                BMS_array[1, 2] = str(rec_int[17])  # Current
                BMS_array[1, 3] = str(rec_int[18])  # Temperature

                BMS_array[2, 0] = str(rec_int[38])  # SOC
                BMS_array[2, 1] = str(rec_int[31])  # Voltage
                BMS_array[2, 2] = str(rec_int[32])  # Current
                BMS_array[2, 3] = str(rec_int[33])  # Temperature
                return BMS_array

            if N_MODULES == 4:
                BMS_array[0, 0] = str(rec_int[8])  # SOC
                BMS_array[0, 1] = str(rec_int[1])  # Voltage
                BMS_array[0, 2] = str(rec_int[2])  # Current
                BMS_array[0, 3] = str(rec_int[3])  # Temperature

                BMS_array[1, 0] = str(rec_int[23])  # SOC
                BMS_array[1, 1] = str(rec_int[16])  # Voltage
                BMS_array[1, 2] = str(rec_int[17])  # Current
                BMS_array[1, 3] = str(rec_int[18])  # Temperature

                BMS_array[2, 0] = str(rec_int[38])  # SOC
                BMS_array[2, 1] = str(rec_int[31])  # Voltage
                BMS_array[2, 2] = str(rec_int[32])  # Current
                BMS_array[2, 3] = str(rec_int[33])  # Temperature

                BMS_array[3, 0] = str(rec_int[53])  # SOC
                BMS_array[3, 1] = str(rec_int[46])  # Voltage
                BMS_array[3, 2] = str(rec_int[47])  # Current
                BMS_array[3, 3] = str(rec_int[48])  # Temperature
                return BMS_array

            if N_MODULES == 5:
                BMS_array[0, 0] = str(rec_int[8])  # SOC
                BMS_array[0, 1] = str(rec_int[1])  # Voltage
                BMS_array[0, 2] = str(rec_int[2])  # Current
                BMS_array[0, 3] = str(rec_int[3])  # Temperature

                BMS_array[1, 0] = str(rec_int[23])  # SOC
                BMS_array[1, 1] = str(rec_int[16])  # Voltage
                BMS_array[1, 2] = str(rec_int[17])  # Current
                BMS_array[1, 3] = str(rec_int[18])  # Temperature

                BMS_array[2, 0] = str(rec_int[38])  # SOC
                BMS_array[2, 1] = str(rec_int[31])  # Voltage
                BMS_array[2, 2] = str(rec_int[32])  # Current
                BMS_array[2, 3] = str(rec_int[33])  # Temperature

                BMS_array[3, 0] = str(rec_int[53])  # SOC
                BMS_array[3, 1] = str(rec_int[46])  # Voltage
                BMS_array[3, 2] = str(rec_int[47])  # Current
                BMS_array[3, 3] = str(rec_int[48])  # Temperature

                BMS_array[4, 0] = str(rec_int[68])  # SOC
                BMS_array[4, 1] = str(rec_int[61])  # Voltage
                BMS_array[4, 2] = str(rec_int[62])  # Current
                BMS_array[4, 3] = str(rec_int[63])  # Temperature
                return BMS_array

            if N_MODULES == 6:
                BMS_array[0, 0] = str(rec_int[8])  # SOC
                BMS_array[0, 1] = str(rec_int[1])  # Voltage
                BMS_array[0, 2] = str(rec_int[2])  # Current
                BMS_array[0, 3] = str(rec_int[3])  # Temperature

                BMS_array[1, 0] = str(rec_int[23])  # SOC
                BMS_array[1, 1] = str(rec_int[16])  # Voltage
                BMS_array[1, 2] = str(rec_int[17])  # Current
                BMS_array[1, 3] = str(rec_int[18])  # Temperature

                BMS_array[2, 0] = str(rec_int[38])  # SOC
                BMS_array[2, 1] = str(rec_int[31])  # Voltage
                BMS_array[2, 2] = str(rec_int[32])  # Current
                BMS_array[2, 3] = str(rec_int[33])  # Temperature

                BMS_array[3, 0] = str(rec_int[53])  # SOC
                BMS_array[3, 1] = str(rec_int[46])  # Voltage
                BMS_array[3, 2] = str(rec_int[47])  # Current
                BMS_array[3, 3] = str(rec_int[48])  # Temperature

                BMS_array[4, 0] = str(rec_int[68])  # SOC
                BMS_array[4, 1] = str(rec_int[61])  # Voltage
                BMS_array[4, 2] = str(rec_int[62])  # Current
                BMS_array[4, 3] = str(rec_int[63])  # Temperature

                BMS_array[5, 0] = str(rec_int[83])  # SOC
                BMS_array[5, 1] = str(rec_int[76])  # Voltage
                BMS_array[5, 2] = str(rec_int[77])  # Current
                BMS_array[5, 3] = str(rec_int[78])  # Temperature
                return BMS_array

            if N_MODULES == 7:
                BMS_array[0, 0] = str(rec_int[8])  # SOC
                BMS_array[0, 1] = str(rec_int[1])  # Voltage
                BMS_array[0, 2] = str(rec_int[2])  # Current
                BMS_array[0, 3] = str(rec_int[3])  # Temperature

                BMS_array[1, 0] = str(rec_int[23])  # SOC
                BMS_array[1, 1] = str(rec_int[16])  # Voltage
                BMS_array[1, 2] = str(rec_int[17])  # Current
                BMS_array[1, 3] = str(rec_int[18])  # Temperature

                BMS_array[2, 0] = str(rec_int[38])  # SOC
                BMS_array[2, 1] = str(rec_int[31])  # Voltage
                BMS_array[2, 2] = str(rec_int[32])  # Current
                BMS_array[2, 3] = str(rec_int[33])  # Temperature

                BMS_array[3, 0] = str(rec_int[53])  # SOC
                BMS_array[3, 1] = str(rec_int[46])  # Voltage
                BMS_array[3, 2] = str(rec_int[47])  # Current
                BMS_array[3, 3] = str(rec_int[48])  # Temperature

                BMS_array[4, 0] = str(rec_int[68])  # SOC
                BMS_array[4, 1] = str(rec_int[61])  # Voltage
                BMS_array[4, 2] = str(rec_int[62])  # Current
                BMS_array[4, 3] = str(rec_int[63])  # Temperature

                BMS_array[5, 0] = str(rec_int[83])  # SOC
                BMS_array[5, 1] = str(rec_int[76])  # Voltage
                BMS_array[5, 2] = str(rec_int[77])  # Current
                BMS_array[5, 3] = str(rec_int[78])  # Temperature

                BMS_array[6, 0] = str(rec_int[98])  # SOC
                BMS_array[6, 1] = str(rec_int[91])  # Voltage
                BMS_array[6, 2] = str(rec_int[92])  # Current
                BMS_array[6, 3] = str(rec_int[93])  # Temperature
                return BMS_array

            if N_MODULES == 8:
                BMS_array[0, 0] = str(rec_int[8])  # SOC
                BMS_array[0, 1] = str(rec_int[1])  # Voltage
                BMS_array[0, 2] = str(rec_int[2])  # Current
                BMS_array[0, 3] = str(rec_int[3])  # Temperature

                BMS_array[1, 0] = str(rec_int[23])  # SOC
                BMS_array[1, 1] = str(rec_int[16])  # Voltage
                BMS_array[1, 2] = str(rec_int[17])  # Current
                BMS_array[1, 3] = str(rec_int[18])  # Temperature

                BMS_array[2, 0] = str(rec_int[38])  # SOC
                BMS_array[2, 1] = str(rec_int[31])  # Voltage
                BMS_array[2, 2] = str(rec_int[32])  # Current
                BMS_array[2, 3] = str(rec_int[33])  # Temperature

                BMS_array[3, 0] = str(rec_int[53])  # SOC
                BMS_array[3, 1] = str(rec_int[46])  # Voltage
                BMS_array[3, 2] = str(rec_int[47])  # Current
                BMS_array[3, 3] = str(rec_int[48])  # Temperature

                BMS_array[4, 0] = str(rec_int[68])  # SOC
                BMS_array[4, 1] = str(rec_int[61])  # Voltage
                BMS_array[4, 2] = str(rec_int[62])  # Current
                BMS_array[4, 3] = str(rec_int[63])  # Temperature

                BMS_array[5, 0] = str(rec_int[83])  # SOC
                BMS_array[5, 1] = str(rec_int[76])  # Voltage
                BMS_array[5, 2] = str(rec_int[77])  # Current
                BMS_array[5, 3] = str(rec_int[78])  # Temperature

                BMS_array[6, 0] = str(rec_int[98])  # SOC
                BMS_array[6, 1] = str(rec_int[91])  # Voltage
                BMS_array[6, 2] = str(rec_int[92])  # Current
                BMS_array[6, 3] = str(rec_int[93])  # Temperature

                BMS_array[7, 0] = str(rec_int[113])  # SOC
                BMS_array[7, 1] = str(rec_int[106])  # Voltage
                BMS_array[7, 2] = str(rec_int[107])  # Current
                BMS_array[7, 3] = str(rec_int[108])  # Temperature
                return BMS_array

            else:
                return BMS_array
        except:
            print"ERROR no communication possible, check if the connection has been opened with open()"

    def log_SoC(self, PATH='../Log/', N_MODULES=1):

        filename = str(PATH) + '/' + str(datetime.date.today()) + '.csv'
        tmp_check_file = os.path.isfile(filename)
        csvfile = open(filename, mode='a')
        name = ['Time','SoC_1', 'Voltage_1', 'Current_1','Temperature_1',
                'SoC_2', 'Voltage_2', 'Current_2', 'Temperature_2',
                'SoC_3', 'Voltage_3', 'Current_3', 'Temperature_3',
                'SoC_4', 'Voltage_4', 'Current_4', 'Temperature_4',
                'SoC_5', 'Voltage_5', 'Current_5', 'Temperature_5',
                'SoC_6', 'Voltage_6', 'Current_6', 'Temperature_6',
                'SoC_7', 'Voltage_7', 'Current_7', 'Temperature_7',
                'SoC_8', 'Voltage_8', 'Current_8', 'Temperature_8',
                ]
        data_writer = csv.DictWriter(csvfile, fieldnames=name)
        if not tmp_check_file:
            data_writer.writeheader()

        tmp_SoC = self.read_SoC(N_MODULES)

        if N_MODULES == 1:
            data_writer.writerow({'Time': str(datetime.datetime.now().hour)+':'+str(datetime.datetime.now().minute),
                                  'SoC_1':tmp_SoC[0,0]})
        if N_MODULES == 2:
            data_writer.writerow({'Time': str(datetime.datetime.now().hour)+':'+str(datetime.datetime.now().minute),
                                  'SoC_1':tmp_SoC[0,0],'SoC_2':tmp_SoC[1,0]})
        if N_MODULES == 3:
            data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                                  'SoC_1': tmp_SoC[0, 0], 'SoC_2': tmp_SoC[1, 0], 'SoC_3': tmp_SoC[2, 0]})
        if N_MODULES == 4:
            data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                                  'SoC_1': tmp_SoC[0, 0], 'SoC_2': tmp_SoC[1, 0], 'SoC_3': tmp_SoC[2, 0], 'SoC_4': tmp_SoC[3, 0]})

        if N_MODULES == 5:
            data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                                  'SoC_1': tmp_SoC[0, 0], 'SoC_2': tmp_SoC[1, 0], 'SoC_3': tmp_SoC[2, 0], 'SoC_4': tmp_SoC[3, 0],
                                  'SoC_5': tmp_SoC[4, 0]})
        if N_MODULES == 6:
            data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                                  'SoC_1': tmp_SoC[0, 0], 'SoC_2': tmp_SoC[1, 0], 'SoC_3': tmp_SoC[2, 0], 'SoC_4': tmp_SoC[3, 0],
                                  'SoC_5': tmp_SoC[4, 0],'SoC_6': tmp_SoC[5, 0]})
        if N_MODULES == 7:
            data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                                  'SoC_1': tmp_SoC[0, 0], 'SoC_2': tmp_SoC[1, 0], 'SoC_3': tmp_SoC[2, 0], 'SoC_4': tmp_SoC[3, 0],
                                  'SoC_5': tmp_SoC[4, 0],'SoC_6': tmp_SoC[5, 0],'SoC_7': tmp_SoC[6, 0]})
        if N_MODULES == 8:
            data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                                  'SoC_1': tmp_SoC[0, 0], 'SoC_2': tmp_SoC[1, 0], 'SoC_3': tmp_SoC[2, 0], 'SoC_4': tmp_SoC[3, 0],
                                  'SoC_5': tmp_SoC[4, 0],'SoC_6': tmp_SoC[5, 0],'SoC_7': tmp_SoC[6, 0],'SoC_8': tmp_SoC[7, 0]})
        else:
            return False

        csvfile.flush()
        csvfile.close()
        return True

    def log_BMS(self, PATH='../Log/', N_MODULES=1):

        filename = str(PATH) + '/' + str(datetime.date.today()) + '.csv'
        tmp_check_file = os.path.isfile(filename)
        csvfile = open(filename, mode='a')
        name = ['Time','SoC_1', 'Voltage_1', 'Current_1','Temperature_1',
                'SoC_2', 'Voltage_2', 'Current_2', 'Temperature_2',
                'SoC_3', 'Voltage_3', 'Current_3', 'Temperature_3',
                'SoC_4', 'Voltage_4', 'Current_4', 'Temperature_4',
                'SoC_5', 'Voltage_5', 'Current_5', 'Temperature_5',
                'SoC_6', 'Voltage_6', 'Current_6', 'Temperature_6',
                'SoC_7', 'Voltage_7', 'Current_7', 'Temperature_7',
                'SoC_8', 'Voltage_8', 'Current_8', 'Temperature_8',
                ]
        data_writer = csv.DictWriter(csvfile, fieldnames=name)
        if not tmp_check_file:
            data_writer.writeheader()

        tmp_BMS = self.read_BMS(N_MODULES)

        if N_MODULES == 1:
            data_writer.writerow({'Time': str(datetime.datetime.now().hour)+':'+str(datetime.datetime.now().minute),
                                  'SoC_1':tmp_BMS[0,0],'Voltage_1':tmp_BMS[0,1],'Current_1':tmp_BMS[0,2],'Temperature_1':tmp_BMS[0,3]})
        if N_MODULES == 2:
            data_writer.writerow({'Time': str(datetime.datetime.now().hour)+':'+str(datetime.datetime.now().minute),
                                  'SoC_1':tmp_BMS[0,0],'Voltage_1':tmp_BMS[0,1],'Current_1':tmp_BMS[0,2],'Temperature_1':tmp_BMS[0,3],
                                  'SoC_2':tmp_BMS[1,0],'Voltage_2':tmp_BMS[1,1],'Current_2':tmp_BMS[1,2],'Temperature_2':tmp_BMS[1,3]})
        if N_MODULES == 3:
            data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                                  'SoC_1':tmp_BMS[0,0],'Voltage_1':tmp_BMS[0,1],'Current_1':tmp_BMS[0,2],'Temperature_1':tmp_BMS[0,3],
                                  'SoC_2':tmp_BMS[1,0],'Voltage_2':tmp_BMS[1,1],'Current_2':tmp_BMS[1,2],'Temperature_2':tmp_BMS[1,3],
                                  'SoC_3':tmp_BMS[2,0],'Voltage_3':tmp_BMS[2,1],'Current_3':tmp_BMS[2,2],'Temperature_3':tmp_BMS[2,3]})
        if N_MODULES == 4:
            data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                                  'SoC_1':tmp_BMS[0,0],'Voltage_1':tmp_BMS[0,1],'Current_1':tmp_BMS[0,2],'Temperature_1':tmp_BMS[0,3],
                                  'SoC_2':tmp_BMS[1,0],'Voltage_2':tmp_BMS[1,1],'Current_2':tmp_BMS[1,2],'Temperature_2':tmp_BMS[1,3],
                                  'SoC_3':tmp_BMS[2,0],'Voltage_3':tmp_BMS[2,1],'Current_3':tmp_BMS[2,2],'Temperature_3':tmp_BMS[2,3],
                                  'SoC_4':tmp_BMS[3,0],'Voltage_4':tmp_BMS[3,1],'Current_4':tmp_BMS[3,2],'Temperature_4':tmp_BMS[3,3]})
        if N_MODULES == 5:
            data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                                  'SoC_1':tmp_BMS[0,0],'Voltage_1':tmp_BMS[0,1],'Current_1':tmp_BMS[0,2],'Temperature_1':tmp_BMS[0,3],
                                  'SoC_2':tmp_BMS[1,0],'Voltage_2':tmp_BMS[1,1],'Current_2':tmp_BMS[1,2],'Temperature_2':tmp_BMS[1,3],
                                  'SoC_3':tmp_BMS[2,0],'Voltage_3':tmp_BMS[2,1],'Current_3':tmp_BMS[2,2],'Temperature_3':tmp_BMS[2,3],
                                  'SoC_4':tmp_BMS[3,0],'Voltage_4':tmp_BMS[3,1],'Current_4':tmp_BMS[3,2],'Temperature_4':tmp_BMS[3,3],
                                  'SoC_5':tmp_BMS[4,0],'Voltage_5':tmp_BMS[4,1],'Current_5':tmp_BMS[4,2],'Temperature_5':tmp_BMS[4,3]})
        if N_MODULES == 6:
            data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                                  'SoC_1':tmp_BMS[0,0],'Voltage_1':tmp_BMS[0,1],'Current_1':tmp_BMS[0,2],'Temperature_1':tmp_BMS[0,3],
                                  'SoC_2':tmp_BMS[1,0],'Voltage_2':tmp_BMS[1,1],'Current_2':tmp_BMS[1,2],'Temperature_2':tmp_BMS[1,3],
                                  'SoC_3':tmp_BMS[2,0],'Voltage_3':tmp_BMS[2,1],'Current_3':tmp_BMS[2,2],'Temperature_3':tmp_BMS[2,3],
                                  'SoC_4':tmp_BMS[3,0],'Voltage_4':tmp_BMS[3,1],'Current_4':tmp_BMS[3,2],'Temperature_4':tmp_BMS[3,3],
                                  'SoC_5':tmp_BMS[4,0],'Voltage_5':tmp_BMS[4,1],'Current_5':tmp_BMS[4,2],'Temperature_5':tmp_BMS[4,3],
                                  'SoC_6':tmp_BMS[5,0],'Voltage_6':tmp_BMS[5,1],'Current_6':tmp_BMS[5,2],'Temperature_6':tmp_BMS[5,3]})
        if N_MODULES == 7:
            data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                                  'SoC_1':tmp_BMS[0,0],'Voltage_1':tmp_BMS[0,1],'Current_1':tmp_BMS[0,2],'Temperature_1':tmp_BMS[0,3],
                                  'SoC_2':tmp_BMS[1,0],'Voltage_2':tmp_BMS[1,1],'Current_2':tmp_BMS[1,2],'Temperature_2':tmp_BMS[1,3],
                                  'SoC_3':tmp_BMS[2,0],'Voltage_3':tmp_BMS[2,1],'Current_3':tmp_BMS[2,2],'Temperature_3':tmp_BMS[2,3],
                                  'SoC_4':tmp_BMS[3,0],'Voltage_4':tmp_BMS[3,1],'Current_4':tmp_BMS[3,2],'Temperature_4':tmp_BMS[3,3],
                                  'SoC_5':tmp_BMS[4,0],'Voltage_5':tmp_BMS[4,1],'Current_5':tmp_BMS[4,2],'Temperature_5':tmp_BMS[4,3],
                                  'SoC_6':tmp_BMS[5,0],'Voltage_6':tmp_BMS[5,1],'Current_6':tmp_BMS[5,2],'Temperature_6':tmp_BMS[5,3],
                                  'SoC_7':tmp_BMS[6,0],'Voltage_7':tmp_BMS[6,1],'Current_7':tmp_BMS[6,2],'Temperature_7':tmp_BMS[6,3]})
        if N_MODULES == 8:
            data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                                  'SoC_1':tmp_BMS[0,0],'Voltage_1':tmp_BMS[0,1],'Current_1':tmp_BMS[0,2],'Temperature_1':tmp_BMS[0,3],
                                  'SoC_2':tmp_BMS[1,0],'Voltage_2':tmp_BMS[1,1],'Current_2':tmp_BMS[1,2],'Temperature_2':tmp_BMS[1,3],
                                  'SoC_3':tmp_BMS[2,0],'Voltage_3':tmp_BMS[2,1],'Current_3':tmp_BMS[2,2],'Temperature_3':tmp_BMS[2,3],
                                  'SoC_4':tmp_BMS[3,0],'Voltage_4':tmp_BMS[3,1],'Current_4':tmp_BMS[3,2],'Temperature_4':tmp_BMS[3,3],
                                  'SoC_5':tmp_BMS[4,0],'Voltage_5':tmp_BMS[4,1],'Current_5':tmp_BMS[4,2],'Temperature_5':tmp_BMS[4,3],
                                  'SoC_6':tmp_BMS[5,0],'Voltage_6':tmp_BMS[5,1],'Current_6':tmp_BMS[5,2],'Temperature_6':tmp_BMS[5,3],
                                  'SoC_7':tmp_BMS[6,0],'Voltage_7':tmp_BMS[6,1],'Current_7':tmp_BMS[6,2],'Temperature_7':tmp_BMS[6,3],
                                  'SoC_8':tmp_BMS[7,0],'Voltage_8':tmp_BMS[7,1],'Current_8':tmp_BMS[7,2],'Temperature_8':tmp_BMS[7,3]})
        else:
            return False

        csvfile.flush()
        csvfile.close()
        return True


    def socket_SoC(self, N_MODULES=1, UDP_IP ="127.0.0.1", UDP_PORT1 = 5005, UDP_PORT2 = 5006, UDP_PORT3 = 50057):
        """This function sends the State of Charge value of the
        Pylontech Batteries to a dedicated socket via UDP protocol.
        The program opens 3 ports for the Control, Control, and Plot functions.
        Basically it sends the data to ports: 5005,5006,5007
        Args:
            N_MODULES: number of modules to be read. Default=1
            UDP_IP: udp ip address. Default="127.0.0.1"
            UDP_PORT1: port to which the "Control" packets should be send to. Default=5005
            UDP_PORT2: port to which the "Log" packets should be send to. Default=5006
            UDP_PORT3: port to which the "Plot" packets should be send to. Default=5007
        Returns:

        """
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

        try:
            while True:
                self.__port.write('pwr\r')
                time.sleep(0.5)
                rec_str = self.__port.read(2200)
                rec_int = re.findall(r'\d+', rec_str)
                #Writes values into SOC_array and returns it.
                if N_MODULES == 1:
                    MESSAGE = "SoC"+"\t"+"N=1"+"\t"+"A="+str(rec_int[8])

                elif N_MODULES == 2:
                    MESSAGE = "SoC"+"\t"+"N=2"+"\t"+"A="+str(rec_int[8])+"\t"+"B="+str(rec_int[23])

                elif N_MODULES == 3:
                    MESSAGE = "SoC"+"\t"+"N=3"+"\t"+"A="+str(rec_int[8])+"\t"+"B="+str(rec_int[23])+"\t"+"C="+str(rec_int[38])

                elif N_MODULES == 4:
                    MESSAGE = "SoC"+"\t"+"N=4"+"\t"+"A="+str(rec_int[8])+"\t"+"B="+str(rec_int[23])+"\t"+"C="+str(rec_int[38])+"\t"+"D="+str(rec_int[53])

                elif N_MODULES == 5:
                    MESSAGE = "SoC"+"\t"+"N=5"+"\t"+"A="+str(rec_int[8])+"\t"+"B="+str(rec_int[23])+"\t"+"C="+str(rec_int[38])+"\t"+"D="+str(rec_int[53])+"\t"+"E="+str(rec_int[68])

                elif N_MODULES == 6:
                    MESSAGE = "SoC"+"\t"+"N=6"+"\t"+"A="+str(rec_int[8])+"\t"+"B="+str(rec_int[23])+"\t"+"C="+str(rec_int[38])+"\t"+"D="+str(rec_int[53])+"\t"+"E="+str(rec_int[68])+"\t"+"F="+str(rec_int[83])

                elif N_MODULES == 7:
                    MESSAGE = "SoC"+"\t"+"N=7"+"\t"+"A="+str(rec_int[8])+"\t"+"B="+str(rec_int[23])+"\t"+"C="+str(rec_int[38])+"\t"+"D="+str(rec_int[53])+"\t"+"E="+str(rec_int[68])+"\t"+"F="+str(rec_int[83])+"\t"+"G="+str(rec_int[98])

                elif N_MODULES == 8:
                    MESSAGE = "SoC"+"\t"+"N=8"+"\t"+"A="+str(rec_int[8])+"\t"+"B="+str(rec_int[23])+"\t"+"C="+str(rec_int[38])+"\t"+"D="+str(rec_int[53])+"\t"+"E="+str(rec_int[68])+"\t"+"F="+str(rec_int[83])+"\t"+"G="+str(rec_int[98])+"\t"+"H="+str(rec_int[113])

                else:
                    print"ERROR number of modules not recognised please specify a number between 1 and 8"
                    sock.close()
                    return
                sock.sendto(MESSAGE, (UDP_IP, UDP_PORT1))
                sock.sendto(MESSAGE, (UDP_IP, UDP_PORT2))
                sock.sendto(MESSAGE, (UDP_IP, UDP_PORT3))
                time.sleep(5)
        except KeyboardInterrupt:
                sock.close()
                return
        except Exception:
            print"ERROR no communication possible, check if the connection has been opened with open()"
            sock.close()
            return

    def socket_BMS(self, N_MODULES=1, UDP_IP ="127.0.0.1", UDP_PORT = 5005):
        """This function sends the values of the: SoC, Voltage, Current, and Temperature
        provided by the Pylontech BMS to an dedicated socket via UDP protocol.
        The program opens 3 ports incremental to the specified UDP port eg. Default=5005
        so it sends the data to ports: 5005,5006,5007
        Args:
            N_MODULES: number of modules to be read. Default=1
            UDP_IP: udp ip address. Default="127.0.0.1"
            UDP_PORT: port to which the packets should be send to. Default=5005
        Returns:

        """
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

        try:
            while True:

                self.__port.write('pwr\r')
                time.sleep(0.5)
                rec_str = self.__port.read(2200)
                rec_int = re.findall(r'\d+', rec_str)
                #Writes values into BMS_array and returns it.

                if N_MODULES == 1:
                    MESSAGE = "BMS" + "\t" + "N=1" + "\t" + "A=" + str(rec_int[8])+ "\t"+ str(rec_int[1])+ "\t"+ str(rec_int[2])+ "\t"+ str(rec_int[3])

                elif N_MODULES == 2:
                    MESSAGE = "BMS" + "\t" + "N=2"\
                              + "\t" + "A=" + str(rec_int[8]) + "\t" + str(rec_int[1]) + "\t" + str(rec_int[2]) + "\t" + str(rec_int[3])\
                              + "\t" + "B=" + str(rec_int[23]) + "\t" + str(rec_int[16]) + "\t" + str(rec_int[17]) + "\t" + str(rec_int[18])

                elif N_MODULES == 3:
                    MESSAGE = "BMS" + "\t" + "N=3" \
                          + "\t" + "A=" + str(rec_int[8]) + "\t" + str(rec_int[1]) + "\t" + str(rec_int[2]) + "\t" + str(rec_int[3]) \
                          + "\t" + "B=" + str(rec_int[23]) + "\t" + str(rec_int[16]) + "\t" + str(rec_int[17]) + "\t" + str(rec_int[18])\
                          + "\t" + "C=" + str(rec_int[38]) + "\t" + str(rec_int[31]) + "\t" + str(rec_int[32]) + "\t" + str(rec_int[33])

                elif N_MODULES == 4:
                    MESSAGE = "BMS" + "\t" + "N=4" \
                          + "\t" + "A=" + str(rec_int[8]) + "\t" + str(rec_int[1]) + "\t" + str(rec_int[2]) + "\t" + str(rec_int[3]) \
                          + "\t" + "B=" + str(rec_int[23]) + "\t" + str(rec_int[16]) + "\t" + str(rec_int[17]) + "\t" + str(rec_int[18])\
                          + "\t" + "C=" + str(rec_int[38]) + "\t" + str(rec_int[31]) + "\t" + str(rec_int[32]) + "\t" + str(rec_int[33])\
                          + "\t" + "D=" + str(rec_int[53]) + "\t" + str(rec_int[46]) + "\t" + str(rec_int[47]) + "\t" + str(rec_int[48])

                elif N_MODULES == 5:
                    MESSAGE = "BMS" + "\t" + "N=5" \
                          + "\t" + "A=" + str(rec_int[8]) + "\t" + str(rec_int[1]) + "\t" + str(rec_int[2]) + "\t" + str(rec_int[3]) \
                          + "\t" + "B=" + str(rec_int[23]) + "\t" + str(rec_int[16]) + "\t" + str(rec_int[17]) + "\t" + str(rec_int[18])\
                          + "\t" + "C=" + str(rec_int[38]) + "\t" + str(rec_int[31]) + "\t" + str(rec_int[32]) + "\t" + str(rec_int[33])\
                          + "\t" + "D=" + str(rec_int[53]) + "\t" + str(rec_int[46]) + "\t" + str(rec_int[47]) + "\t" + str(rec_int[48])\
                          + "\t" + "E=" + str(rec_int[68]) + "\t" + str(rec_int[61]) + "\t" + str(rec_int[62]) + "\t" + str(rec_int[63])

                elif N_MODULES == 6:
                    MESSAGE = "BMS" + "\t" + "N=6" \
                          + "\t" + "A=" + str(rec_int[8]) + "\t" + str(rec_int[1]) + "\t" + str(rec_int[2]) + "\t" + str(rec_int[3]) \
                          + "\t" + "B=" + str(rec_int[23]) + "\t" + str(rec_int[16]) + "\t" + str(rec_int[17]) + "\t" + str(rec_int[18])\
                          + "\t" + "C=" + str(rec_int[38]) + "\t" + str(rec_int[31]) + "\t" + str(rec_int[32]) + "\t" + str(rec_int[33])\
                          + "\t" + "D=" + str(rec_int[53]) + "\t" + str(rec_int[46]) + "\t" + str(rec_int[47]) + "\t" + str(rec_int[48])\
                          + "\t" + "E=" + str(rec_int[68]) + "\t" + str(rec_int[61]) + "\t" + str(rec_int[62]) + "\t" + str(rec_int[63])\
                          + "\t" + "F=" + str(rec_int[83]) + "\t" + str(rec_int[76]) + "\t" + str(rec_int[77]) + "\t" + str(rec_int[78])

                elif N_MODULES == 7:
                    MESSAGE = "BMS" + "\t" + "N=7" \
                          + "\t" + "A=" + str(rec_int[8]) + "\t" + str(rec_int[1]) + "\t" + str(rec_int[2]) + "\t" + str(rec_int[3]) \
                          + "\t" + "B=" + str(rec_int[23]) + "\t" + str(rec_int[16]) + "\t" + str(rec_int[17]) + "\t" + str(rec_int[18])\
                          + "\t" + "C=" + str(rec_int[38]) + "\t" + str(rec_int[31]) + "\t" + str(rec_int[32]) + "\t" + str(rec_int[33])\
                          + "\t" + "D=" + str(rec_int[53]) + "\t" + str(rec_int[46]) + "\t" + str(rec_int[47]) + "\t" + str(rec_int[48])\
                          + "\t" + "E=" + str(rec_int[68]) + "\t" + str(rec_int[61]) + "\t" + str(rec_int[62]) + "\t" + str(rec_int[63])\
                          + "\t" + "F=" + str(rec_int[83]) + "\t" + str(rec_int[76]) + "\t" + str(rec_int[77]) + "\t" + str(rec_int[78])\
                          + "\t" + "G=" + str(rec_int[98]) + "\t" + str(rec_int[91]) + "\t" + str(rec_int[92]) + "\t" + str(rec_int[93])

                elif N_MODULES == 8:
                    MESSAGE = "BMS" + "\t" + "N=8" \
                          + "\t" + "A=" + str(rec_int[8]) + "\t" + str(rec_int[1]) + "\t" + str(rec_int[2]) + "\t" + str(rec_int[3]) \
                          + "\t" + "B=" + str(rec_int[23]) + "\t" + str(rec_int[16]) + "\t" + str(rec_int[17]) + "\t" + str(rec_int[18])\
                          + "\t" + "C=" + str(rec_int[38]) + "\t" + str(rec_int[31]) + "\t" + str(rec_int[32]) + "\t" + str(rec_int[33])\
                          + "\t" + "D=" + str(rec_int[53]) + "\t" + str(rec_int[46]) + "\t" + str(rec_int[47]) + "\t" + str(rec_int[48])\
                          + "\t" + "E=" + str(rec_int[68]) + "\t" + str(rec_int[61]) + "\t" + str(rec_int[62]) + "\t" + str(rec_int[63])\
                          + "\t" + "F=" + str(rec_int[83]) + "\t" + str(rec_int[76]) + "\t" + str(rec_int[77]) + "\t" + str(rec_int[78])\
                          + "\t" + "G=" + str(rec_int[98]) + "\t" + str(rec_int[91]) + "\t" + str(rec_int[92]) + "\t" + str(rec_int[93])\
                          + "\t" + "H=" + str(rec_int[113]) + "\t" + str(rec_int[106]) + "\t" + str(rec_int[107]) + "\t" + str(rec_int[108])

                else:
                    sock.close()
                    print"ERROR number of modules not recognised please specify a number between 1 and 8"
                    return

                sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
                sock.sendto(MESSAGE, (UDP_IP, UDP_PORT+1))
                sock.sendto(MESSAGE, (UDP_IP, UDP_PORT+2))
                time.sleep(5)
        except KeyboardInterrupt:
            sock.close()
            return
        except Exception:
            sock.close()
            print"ERROR no communication possible, check if the connection has been opened with open()"
            return