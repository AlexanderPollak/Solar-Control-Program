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
        5. Battery Status
        6. Voltage Status
        7. Current Status
        8. Temperature Status
The main class in this module (``US2000B``) allows the user to
communicate with the Pylontech US2000B Plus BMS.

"""

import serial,time,re,datetime,csv,os
import numpy as np
import socket,threading


# EMBEDDING US2000B CLASS ----------------------------------------------------

class US2000B(object):
    """This class implements the serial connection functions """
    def __init__(self):
        ''' Constructor for this class. '''
        self._port = 0
    def __del__(self):
        ''' Destructor for this class. '''
        if self._port !=0:
            self.close()




    def initialise(self, port='/dev/ttyUSB0'):
        """Initialises the console communication fo the US2000B BMS
        Args:
            port: path to serial port. Default='/dev/ttyUSB0'
        Returns: Boolean value True or False"""
        temp_port = serial.Serial(port,1200, timeout=0.05)
        temp_port.write(str.encode('~20014682C0048520FCC3\r'))
        time.sleep(5)
        temp_port = serial.Serial(port,115200, timeout=0.05)
        temp_port.write(str.encode('\r\n'))
        temp_receive = repr(temp_port.read(1000))
        temp_port.close()
        return temp_receive== str("b'\\n\\rpylon>\\n\\rpylon>'")

    def open(self, port='/dev/ttyUSB0', baud=115200):
        """Open serial port for communication

        Args:
            port: path to serial port. Default='/dev/ttyUSB0'
            baud: defines the baud rate. Default=115200

        Returns: Boolean value True or False

        """
        self._port = serial.Serial(port, baud, timeout=0.05)
        return self._port.is_open

    def close(self):
        """Close serial port

        Returns: Boolean value True or False

        """
        self._port.close()
        return not self._port.is_open

    def is_connected(self):
        """This function checks if the connection to the BMS is established
        and if the BMS responds to readout commands.

        Returns: Boolean value True or False

        """
        self._port.write(str.encode('\r\n'))
        temp_receive = repr(self._port.read(1000))
        return temp_receive== str("b'\\n\\rpylon>\\n\\rpylon>'")



    def read_SoC(self, N_MODULES=1):
        """This function returns the State of Charge value of the Pylontech Batteries.
        
        Args:
            N_MODULES: number of modules to be read. Default=1

        Returns: SoC_list: list of length [n_modules] containing: [SoC] dtype=float.

        """
        try:
            SoC_list = [[0 for i in range(1)] for j in range(N_MODULES)]
            self._port.write(str.encode('pwr\r'))
            time.sleep(0.5)
            rec_content = str(self._port.read(2200), 'utf-8')
            rec_int = re.findall(r'\d+',rec_content)
            #Writes values into SOC_array and returns it.
            if 1 <= N_MODULES <= 8:
                for x in range(N_MODULES):
                    SoC_list[x][0] = float(rec_int[(8+(x*15))])#SOC
                return SoC_list
            else:
                print("ERROR: Number of modules must be 1-8. Number parsed:"+N_MODULES)
                return SoC_list
        except:
            print("ERROR no communication possible, check if the connection has been opened with open()")

    def read_BMS(self, N_MODULES=1):
        """This function returns the values of the: SoC, Voltage, Current, Temperature, Battery Status,
        Voltage Status, Current Status, and Temperature Status provided by the Pylontech BMS.
        
        Args:
            N_MODULES: number of modules to be read. Default=1

        Returns: BMS_list: list of length [n_modules] containing:
            [SoC, Voltage, Current, Temperature, Battery Status, Voltage Status, Current Status, Temperature Status]
            dtype=float and dtype=str.


        """
        try:
            BMS_list = [[0 for i in range(8)] for j in range(N_MODULES)]
            self._port.write(str.encode('pwr\r'))
            time.sleep(0.5)
            rec_content = str(self._port.read(2200), 'utf-8')
            rec_str = re.findall(r'\w+', rec_content)
            #Writes values into BMS_list and returns it.
            #Note that 21 is the offset between each value index for the individual batteries.
            if 1 <= N_MODULES <= 8:
                for x in range(N_MODULES):
                    BMS_list[x][0] = float(rec_str[(37+(x*21))])#SOC
                    BMS_list[x][1] = float(rec_str[(26+(x*21))])/1000.0 #Voltage
                    BMS_list[x][2] = float(rec_str[(27+(x*21))])/1000.0 #Current
                    BMS_list[x][3] = float(rec_str[(28+(x*21))])/1000.0 #Temperature
                    BMS_list[x][4] = str(rec_str[(33+(x*21))])#Battery Status
                    BMS_list[x][5] = str(rec_str[(34+(x*21))])#Voltage Status
                    BMS_list[x][6] = str(rec_str[(35+(x*21))])#Current Status
                    BMS_list[x][7] = str(rec_str[(36+(x*21))])#Temperature Status
                return BMS_list
            else:
                print("ERROR: Number of modules must be 1-8. Number parsed:"+N_MODULES)
                return BMS_list
        except:
            print("ERROR: no communication possible, check if the connection has been opened with open()")


    def log_SoC(self, SOC_LIST, PATH='../var/BMS_log'):
        """This function writes the State of Charge (SoC) into a '.csv' file.
        
        Args:
            PATH: path to the directory where the .csv file will be saved.
            SOC_LIST: list of length [n_modules] containing: [SoC] dtype=float.

        Returns: Boolean value True or False

        """
        filename = str(PATH) + '/' + str(datetime.date.today()) + '.csv'
        tmp_check_file = os.path.isfile(filename)
        csvfile = open(filename, mode='a')
        name = ['Time','SoC_1', 'Voltage_1', 'Current_1','Temperature_1', 'B_Status_1', 'V_Status_1', 'C_Status_1', 'T_Status_1',
                'SoC_2', 'Voltage_2', 'Current_2', 'Temperature_2', 'B_Status_2', 'V_Status_2', 'C_Status_2', 'T_Status_2',
                'SoC_3', 'Voltage_3', 'Current_3', 'Temperature_3', 'B_Status_3', 'V_Status_3', 'C_Status_3', 'T_Status_3',
                'SoC_4', 'Voltage_4', 'Current_4', 'Temperature_4', 'B_Status_4', 'V_Status_4', 'C_Status_4', 'T_Status_4',
                'SoC_5', 'Voltage_5', 'Current_5', 'Temperature_5', 'B_Status_5', 'V_Status_5', 'C_Status_5', 'T_Status_5',
                'SoC_6', 'Voltage_6', 'Current_6', 'Temperature_6', 'B_Status_6', 'V_Status_6', 'C_Status_6', 'T_Status_6',
                'SoC_7', 'Voltage_7', 'Current_7', 'Temperature_7', 'B_Status_7', 'V_Status_7', 'C_Status_7', 'T_Status_7',
                'SoC_8', 'Voltage_8', 'Current_8', 'Temperature_8', 'B_Status_8', 'V_Status_8', 'C_Status_8', 'T_Status_8'
                ]
        data_writer = csv.DictWriter(csvfile, fieldnames=name)
        if not tmp_check_file:
            data_writer.writeheader()

        tmp_time = str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute) + ':' + str(datetime.datetime.now().second)
        tmp_n_modules = len(SOC_LIST)
        tmp_SoC = SOC_LIST

        if tmp_n_modules == 1:
            data_writer.writerow({'Time':tmp_time,'SoC_1':tmp_SoC[0][0]})
        elif tmp_n_modules == 2:
            data_writer.writerow({'Time':tmp_time,'SoC_1':tmp_SoC[0][0],'SoC_2':tmp_SoC[1][0]})
        elif tmp_n_modules == 3:
            data_writer.writerow({'Time':tmp_time,'SoC_1':tmp_SoC[0][0],'SoC_2':tmp_SoC[1][0],'SoC_3':tmp_SoC[2][0]})
        elif tmp_n_modules == 4:
            data_writer.writerow({'Time':tmp_time,'SoC_1':tmp_SoC[0][0],'SoC_2':tmp_SoC[1][0],'SoC_3':tmp_SoC[2][0],'SoC_4':tmp_SoC[3][0]})
        elif tmp_n_modules == 5:
            data_writer.writerow({'Time':tmp_time,'SoC_1':tmp_SoC[0][0],'SoC_2':tmp_SoC[1][0],'SoC_3':tmp_SoC[2][0],'SoC_4':tmp_SoC[3][0],'SoC_5':tmp_SoC[4][0]})
        elif tmp_n_modules == 6:
            data_writer.writerow({'Time':tmp_time,'SoC_1':tmp_SoC[0][0],'SoC_2':tmp_SoC[1][0],'SoC_3':tmp_SoC[2][0],'SoC_4':tmp_SoC[3][0],'SoC_5':tmp_SoC[4][0],'SoC_6':tmp_SoC[5][0]})
        elif tmp_n_modules == 7:
            data_writer.writerow({'Time':tmp_time,'SoC_1':tmp_SoC[0][0],'SoC_2':tmp_SoC[1][0],'SoC_3':tmp_SoC[2][0],'SoC_4':tmp_SoC[3][0],'SoC_5':tmp_SoC[4][0],'SoC_6':tmp_SoC[5][0],'SoC_7':tmp_SoC[6][0]})
        elif tmp_n_modules == 8:
            data_writer.writerow({'Time':tmp_time,'SoC_1':tmp_SoC[0][0],'SoC_2':tmp_SoC[1][0],'SoC_3':tmp_SoC[2][0],'SoC_4':tmp_SoC[3][0],'SoC_5':tmp_SoC[4][0],'SoC_6':tmp_SoC[5][0],'SoC_7':tmp_SoC[6][0],'SoC_8':tmp_SoC[7][0]})
        else:
            print("Unsuported number of battery modules. Only 1-8 modules are supported. The module number parsed is:" + tmp_n_modules)
            csvfile.flush()
            csvfile.close()
            return False

        csvfile.flush()
        csvfile.close()
        return True

    def log_BMS(self, BMS_LIST, PATH='../var/BMS_log'):
        """This function writes the BMS information into a '.csv' file.
        
        Args:
            PATH: path to the directory where the .csv file will be saved.
            SOC_LIST: list of length [n_modules] containing:
            [SoC, Voltage, Current, Temperature, Battery Status, Voltage Status, Current Status, Temperature Status]
            dtype=float and dtype=str.

        Returns: Boolean value True or False

        """
        filename = str(PATH) + '/' + str(datetime.date.today()) + '.csv'
        tmp_check_file = os.path.isfile(filename)
        csvfile = open(filename, mode='a')
        name = ['Time','SoC_1', 'Voltage_1', 'Current_1','Temperature_1', 'B_Status_1', 'V_Status_1', 'C_Status_1', 'T_Status_1',
                'SoC_2', 'Voltage_2', 'Current_2', 'Temperature_2', 'B_Status_2', 'V_Status_2', 'C_Status_2', 'T_Status_2',
                'SoC_3', 'Voltage_3', 'Current_3', 'Temperature_3', 'B_Status_3', 'V_Status_3', 'C_Status_3', 'T_Status_3',
                'SoC_4', 'Voltage_4', 'Current_4', 'Temperature_4', 'B_Status_4', 'V_Status_4', 'C_Status_4', 'T_Status_4',
                'SoC_5', 'Voltage_5', 'Current_5', 'Temperature_5', 'B_Status_5', 'V_Status_5', 'C_Status_5', 'T_Status_5',
                'SoC_6', 'Voltage_6', 'Current_6', 'Temperature_6', 'B_Status_6', 'V_Status_6', 'C_Status_6', 'T_Status_6',
                'SoC_7', 'Voltage_7', 'Current_7', 'Temperature_7', 'B_Status_7', 'V_Status_7', 'C_Status_7', 'T_Status_7',
                'SoC_8', 'Voltage_8', 'Current_8', 'Temperature_8', 'B_Status_8', 'V_Status_8', 'C_Status_8', 'T_Status_8'
                ]
        data_writer = csv.DictWriter(csvfile, fieldnames=name)
        if not tmp_check_file:
            data_writer.writeheader()

        tmp_time = str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute) + ':' + str(datetime.datetime.now().second)
        tmp_n_modules = len(BMS_LIST)
        tmp_BMS = BMS_LIST

        if tmp_n_modules == 1:
            data_writer.writerow({'Time':tmp_time,
                                  'SoC_1':tmp_BMS[0][0],'Voltage_1':tmp_BMS[0][1],'Current_1':tmp_BMS[0][2],'Temperature_1':tmp_BMS[0][3],'B_Status_1':tmp_BMS[0][4],'V_Status_1':tmp_BMS[0][5],'C_Status_1':tmp_BMS[0][6],'T_Status_1':tmp_BMS[0][7]})
        elif tmp_n_modules == 2:
            data_writer.writerow({'Time':tmp_time,
                                  'SoC_1':tmp_BMS[0][0],'Voltage_1':tmp_BMS[0][1],'Current_1':tmp_BMS[0][2],'Temperature_1':tmp_BMS[0][3],'B_Status_1':tmp_BMS[0][4],'V_Status_1':tmp_BMS[0][5],'C_Status_1':tmp_BMS[0][6],'T_Status_1':tmp_BMS[0][7],
                                  'SoC_2':tmp_BMS[1][0],'Voltage_2':tmp_BMS[1][1],'Current_2':tmp_BMS[1][2],'Temperature_2':tmp_BMS[1][3],'B_Status_2':tmp_BMS[1][4],'V_Status_2':tmp_BMS[1][5],'C_Status_2':tmp_BMS[1][6],'T_Status_2':tmp_BMS[1][7]})
        elif tmp_n_modules == 3:
            data_writer.writerow({'Time':tmp_time,
                                  'SoC_1':tmp_BMS[0][0],'Voltage_1':tmp_BMS[0][1],'Current_1':tmp_BMS[0][2],'Temperature_1':tmp_BMS[0][3],'B_Status_1':tmp_BMS[0][4],'V_Status_1':tmp_BMS[0][5],'C_Status_1':tmp_BMS[0][6],'T_Status_1':tmp_BMS[0][7],
                                  'SoC_2':tmp_BMS[1][0],'Voltage_2':tmp_BMS[1][1],'Current_2':tmp_BMS[1][2],'Temperature_2':tmp_BMS[1][3],'B_Status_2':tmp_BMS[1][4],'V_Status_2':tmp_BMS[1][5],'C_Status_2':tmp_BMS[1][6],'T_Status_2':tmp_BMS[1][7],
                                  'SoC_3':tmp_BMS[2][0],'Voltage_3':tmp_BMS[2][1],'Current_3':tmp_BMS[2][2],'Temperature_3':tmp_BMS[2][3],'B_Status_3':tmp_BMS[2][4],'V_Status_3':tmp_BMS[2][5],'C_Status_3':tmp_BMS[2][6],'T_Status_3':tmp_BMS[2][7]})
        elif tmp_n_modules == 4:
            data_writer.writerow({'Time':tmp_time,
                                  'SoC_1':tmp_BMS[0][0],'Voltage_1':tmp_BMS[0][1],'Current_1':tmp_BMS[0][2],'Temperature_1':tmp_BMS[0][3],'B_Status_1':tmp_BMS[0][4],'V_Status_1':tmp_BMS[0][5],'C_Status_1':tmp_BMS[0][6],'T_Status_1':tmp_BMS[0][7],
                                  'SoC_2':tmp_BMS[1][0],'Voltage_2':tmp_BMS[1][1],'Current_2':tmp_BMS[1][2],'Temperature_2':tmp_BMS[1][3],'B_Status_2':tmp_BMS[1][4],'V_Status_2':tmp_BMS[1][5],'C_Status_2':tmp_BMS[1][6],'T_Status_2':tmp_BMS[1][7],
                                  'SoC_3':tmp_BMS[2][0],'Voltage_3':tmp_BMS[2][1],'Current_3':tmp_BMS[2][2],'Temperature_3':tmp_BMS[2][3],'B_Status_3':tmp_BMS[2][4],'V_Status_3':tmp_BMS[2][5],'C_Status_3':tmp_BMS[2][6],'T_Status_3':tmp_BMS[2][7],
                                  'SoC_4':tmp_BMS[3][0],'Voltage_4':tmp_BMS[3][1],'Current_4':tmp_BMS[3][2],'Temperature_4':tmp_BMS[3][3],'B_Status_4':tmp_BMS[3][4],'V_Status_4':tmp_BMS[3][5],'C_Status_4':tmp_BMS[3][6],'T_Status_4':tmp_BMS[3][7]})
        elif tmp_n_modules == 5:
            data_writer.writerow({'Time':tmp_time,
                                  'SoC_1':tmp_BMS[0][0],'Voltage_1':tmp_BMS[0][1],'Current_1':tmp_BMS[0][2],'Temperature_1':tmp_BMS[0][3],'B_Status_1':tmp_BMS[0][4],'V_Status_1':tmp_BMS[0][5],'C_Status_1':tmp_BMS[0][6],'T_Status_1':tmp_BMS[0][7],
                                  'SoC_2':tmp_BMS[1][0],'Voltage_2':tmp_BMS[1][1],'Current_2':tmp_BMS[1][2],'Temperature_2':tmp_BMS[1][3],'B_Status_2':tmp_BMS[1][4],'V_Status_2':tmp_BMS[1][5],'C_Status_2':tmp_BMS[1][6],'T_Status_2':tmp_BMS[1][7],
                                  'SoC_3':tmp_BMS[2][0],'Voltage_3':tmp_BMS[2][1],'Current_3':tmp_BMS[2][2],'Temperature_3':tmp_BMS[2][3],'B_Status_3':tmp_BMS[2][4],'V_Status_3':tmp_BMS[2][5],'C_Status_3':tmp_BMS[2][6],'T_Status_3':tmp_BMS[2][7],
                                  'SoC_4':tmp_BMS[3][0],'Voltage_4':tmp_BMS[3][1],'Current_4':tmp_BMS[3][2],'Temperature_4':tmp_BMS[3][3],'B_Status_4':tmp_BMS[3][4],'V_Status_4':tmp_BMS[3][5],'C_Status_4':tmp_BMS[3][6],'T_Status_4':tmp_BMS[3][7],
                                  'SoC_5':tmp_BMS[4][0],'Voltage_5':tmp_BMS[4][1],'Current_5':tmp_BMS[4][2],'Temperature_5':tmp_BMS[4][3],'B_Status_5':tmp_BMS[4][4],'V_Status_5':tmp_BMS[4][5],'C_Status_5':tmp_BMS[4][6],'T_Status_5':tmp_BMS[4][7]})
        elif tmp_n_modules == 6:
            data_writer.writerow({'Time':tmp_time,
                                  'SoC_1':tmp_BMS[0][0],'Voltage_1':tmp_BMS[0][1],'Current_1':tmp_BMS[0][2],'Temperature_1':tmp_BMS[0][3],'B_Status_1':tmp_BMS[0][4],'V_Status_1':tmp_BMS[0][5],'C_Status_1':tmp_BMS[0][6],'T_Status_1':tmp_BMS[0][7],
                                  'SoC_2':tmp_BMS[1][0],'Voltage_2':tmp_BMS[1][1],'Current_2':tmp_BMS[1][2],'Temperature_2':tmp_BMS[1][3],'B_Status_2':tmp_BMS[1][4],'V_Status_2':tmp_BMS[1][5],'C_Status_2':tmp_BMS[1][6],'T_Status_2':tmp_BMS[1][7],
                                  'SoC_3':tmp_BMS[2][0],'Voltage_3':tmp_BMS[2][1],'Current_3':tmp_BMS[2][2],'Temperature_3':tmp_BMS[2][3],'B_Status_3':tmp_BMS[2][4],'V_Status_3':tmp_BMS[2][5],'C_Status_3':tmp_BMS[2][6],'T_Status_3':tmp_BMS[2][7],
                                  'SoC_4':tmp_BMS[3][0],'Voltage_4':tmp_BMS[3][1],'Current_4':tmp_BMS[3][2],'Temperature_4':tmp_BMS[3][3],'B_Status_4':tmp_BMS[3][4],'V_Status_4':tmp_BMS[3][5],'C_Status_4':tmp_BMS[3][6],'T_Status_4':tmp_BMS[3][7],
                                  'SoC_5':tmp_BMS[4][0],'Voltage_5':tmp_BMS[4][1],'Current_5':tmp_BMS[4][2],'Temperature_5':tmp_BMS[4][3],'B_Status_5':tmp_BMS[4][4],'V_Status_5':tmp_BMS[4][5],'C_Status_5':tmp_BMS[4][6],'T_Status_5':tmp_BMS[4][7],
                                  'SoC_6':tmp_BMS[5][0],'Voltage_6':tmp_BMS[5][1],'Current_6':tmp_BMS[5][2],'Temperature_6':tmp_BMS[5][3],'B_Status_6':tmp_BMS[5][4],'V_Status_6':tmp_BMS[5][5],'C_Status_6':tmp_BMS[5][6],'T_Status_6':tmp_BMS[5][7]})
        elif tmp_n_modules == 7:
            data_writer.writerow({'Time':tmp_time,
                                  'SoC_1':tmp_BMS[0][0],'Voltage_1':tmp_BMS[0][1],'Current_1':tmp_BMS[0][2],'Temperature_1':tmp_BMS[0][3],'B_Status_1':tmp_BMS[0][4],'V_Status_1':tmp_BMS[0][5],'C_Status_1':tmp_BMS[0][6],'T_Status_1':tmp_BMS[0][7],
                                  'SoC_2':tmp_BMS[1][0],'Voltage_2':tmp_BMS[1][1],'Current_2':tmp_BMS[1][2],'Temperature_2':tmp_BMS[1][3],'B_Status_2':tmp_BMS[1][4],'V_Status_2':tmp_BMS[1][5],'C_Status_2':tmp_BMS[1][6],'T_Status_2':tmp_BMS[1][7],
                                  'SoC_3':tmp_BMS[2][0],'Voltage_3':tmp_BMS[2][1],'Current_3':tmp_BMS[2][2],'Temperature_3':tmp_BMS[2][3],'B_Status_3':tmp_BMS[2][4],'V_Status_3':tmp_BMS[2][5],'C_Status_3':tmp_BMS[2][6],'T_Status_3':tmp_BMS[2][7],
                                  'SoC_4':tmp_BMS[3][0],'Voltage_4':tmp_BMS[3][1],'Current_4':tmp_BMS[3][2],'Temperature_4':tmp_BMS[3][3],'B_Status_4':tmp_BMS[3][4],'V_Status_4':tmp_BMS[3][5],'C_Status_4':tmp_BMS[3][6],'T_Status_4':tmp_BMS[3][7],
                                  'SoC_5':tmp_BMS[4][0],'Voltage_5':tmp_BMS[4][1],'Current_5':tmp_BMS[4][2],'Temperature_5':tmp_BMS[4][3],'B_Status_5':tmp_BMS[4][4],'V_Status_5':tmp_BMS[4][5],'C_Status_5':tmp_BMS[4][6],'T_Status_5':tmp_BMS[4][7],
                                  'SoC_6':tmp_BMS[5][0],'Voltage_6':tmp_BMS[5][1],'Current_6':tmp_BMS[5][2],'Temperature_6':tmp_BMS[5][3],'B_Status_6':tmp_BMS[5][4],'V_Status_6':tmp_BMS[5][5],'C_Status_6':tmp_BMS[5][6],'T_Status_6':tmp_BMS[5][7],
                                  'SoC_7':tmp_BMS[6][0],'Voltage_7':tmp_BMS[6][1],'Current_7':tmp_BMS[6][2],'Temperature_7':tmp_BMS[6][3],'B_Status_7':tmp_BMS[6][4],'V_Status_7':tmp_BMS[6][5],'C_Status_7':tmp_BMS[6][6],'T_Status_7':tmp_BMS[6][7]})
        elif tmp_n_modules == 8:
            data_writer.writerow({'Time':tmp_time,
                                  'SoC_1':tmp_BMS[0][0],'Voltage_1':tmp_BMS[0][1],'Current_1':tmp_BMS[0][2],'Temperature_1':tmp_BMS[0][3],'B_Status_1':tmp_BMS[0][4],'V_Status_1':tmp_BMS[0][5],'C_Status_1':tmp_BMS[0][6],'T_Status_1':tmp_BMS[0][7],
                                  'SoC_2':tmp_BMS[1][0],'Voltage_2':tmp_BMS[1][1],'Current_2':tmp_BMS[1][2],'Temperature_2':tmp_BMS[1][3],'B_Status_2':tmp_BMS[1][4],'V_Status_2':tmp_BMS[1][5],'C_Status_2':tmp_BMS[1][6],'T_Status_2':tmp_BMS[1][7],
                                  'SoC_3':tmp_BMS[2][0],'Voltage_3':tmp_BMS[2][1],'Current_3':tmp_BMS[2][2],'Temperature_3':tmp_BMS[2][3],'B_Status_3':tmp_BMS[2][4],'V_Status_3':tmp_BMS[2][5],'C_Status_3':tmp_BMS[2][6],'T_Status_3':tmp_BMS[2][7],
                                  'SoC_4':tmp_BMS[3][0],'Voltage_4':tmp_BMS[3][1],'Current_4':tmp_BMS[3][2],'Temperature_4':tmp_BMS[3][3],'B_Status_4':tmp_BMS[3][4],'V_Status_4':tmp_BMS[3][5],'C_Status_4':tmp_BMS[3][6],'T_Status_4':tmp_BMS[3][7],
                                  'SoC_5':tmp_BMS[4][0],'Voltage_5':tmp_BMS[4][1],'Current_5':tmp_BMS[4][2],'Temperature_5':tmp_BMS[4][3],'B_Status_5':tmp_BMS[4][4],'V_Status_5':tmp_BMS[4][5],'C_Status_5':tmp_BMS[4][6],'T_Status_5':tmp_BMS[4][7],
                                  'SoC_6':tmp_BMS[5][0],'Voltage_6':tmp_BMS[5][1],'Current_6':tmp_BMS[5][2],'Temperature_6':tmp_BMS[5][3],'B_Status_6':tmp_BMS[5][4],'V_Status_6':tmp_BMS[5][5],'C_Status_6':tmp_BMS[5][6],'T_Status_6':tmp_BMS[5][7],
                                  'SoC_7':tmp_BMS[6][0],'Voltage_7':tmp_BMS[6][1],'Current_7':tmp_BMS[6][2],'Temperature_7':tmp_BMS[6][3],'B_Status_7':tmp_BMS[6][4],'V_Status_7':tmp_BMS[6][5],'C_Status_7':tmp_BMS[6][6],'T_Status_7':tmp_BMS[6][7],
                                  'SoC_8':tmp_BMS[7][0],'Voltage_8':tmp_BMS[7][1],'Current_8':tmp_BMS[7][2],'Temperature_8':tmp_BMS[7][3],'B_Status_8':tmp_BMS[7][4],'V_Status_8':tmp_BMS[7][5],'C_Status_8':tmp_BMS[7][6],'T_Status_8':tmp_BMS[7][7]})
        else:
            print("Unsuported number of battery modules. Only 1-8 modules are supported. The module number parsed is:" + tmp_n_modules)
            csvfile.flush()
            csvfile.close()
            return False

        csvfile.flush()
        csvfile.close()
        return True



    def socket_SoC(self, N_MODULES=1, UDP_IP ="127.0.0.1", UDP_PORT1 = 5005, UDP_PORT2 = 5006, UDP_PORT3 = 5007):
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
                self._port.write(str.encode('pwr\r'))
                time.sleep(0.5)
                rec_str = str(self._port.read(2200), 'utf-8')
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
                    print("ERROR number of modules not recognised please specify a number between 1 and 8")
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
            print("ERROR no communication possible, check if the connection has been opened with open()")
            sock.close()
            return

    def socket_BMS(self, N_MODULES=1, UDP_IP ="127.0.0.1", UDP_PORT1 = 5005, UDP_PORT2 = 5006, UDP_PORT3 = 5007):
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

                self._port.write(str.encode('pwr\r'))
                time.sleep(0.5)
                rec_str = str(self._port.read(2200),'utf-8')
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
                    print("ERROR number of modules not recognised please specify a number between 1 and 8")
                    return

                sock.sendto(MESSAGE, (UDP_IP, UDP_PORT1))
                sock.sendto(MESSAGE, (UDP_IP, UDP_PORT2))
                sock.sendto(MESSAGE, (UDP_IP, UDP_PORT3))
                time.sleep(5)
        except KeyboardInterrupt:
            sock.close()
            return
        except Exception:
            sock.close()
            print("ERROR no communication possible, check if the connection has been opened with open()")
            return


# EMBEDDING ThreadedControl CLASS ----------------------------------------------------

class US2000B_socket_BMS_Thread(threading.Thread):


    def __init__(self,group=None,target=None,name=None,verbose=None,N_MODULES=1, UDP_IP ="127.0.0.1", UDP_PORT1 = 5005, UDP_PORT2 = 5006, UDP_PORT3 = 5007):

        threading.Thread.__init__(self,group=group,target=target,name=name,verbose=verbose)

        self._stopevent =threading.Event()# used to stop the socket loop.

        self.N_MODULES=N_MODULES
        self.UDP_IP=UDP_IP
        self.UDP_PORT1=UDP_PORT1
        self.UDP_PORT2 = UDP_PORT2
        self.UDP_PORT3 = UDP_PORT3


    def run(self):
        """Main control loop"""
        BMS = US2000B()
        BMS.open()
        self._port = BMS._port

        for i in range(1,10):
            if BMS.is_connected():
                break
            time.sleep(1)
            if i == 5:
                BMS.initialise()
            if i == 10:
                print ("ERROR, no connection could be established!")
                return
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            while not self._stopevent.isSet():

                self._port.write(str.encode('pwr\r'))
                time.sleep(0.5)
                rec_str = str(self._port.read(2200),'utf-8')
                rec_int = re.findall(r'\d+', rec_str)
                # Writes values into BMS_array and returns it.

                if self.N_MODULES == 1:
                    MESSAGE = "BMS" + "\t" + "N=1" + "\t" + "A=" + str(rec_int[8]) + "\t" + str(
                        rec_int[1]) + "\t" + str(rec_int[2]) + "\t" + str(rec_int[3])

                elif self.N_MODULES == 2:
                    MESSAGE = "BMS" + "\t" + "N=2"\
                              + "\t" + "A=" + str(rec_int[8]) + "\t" + str(rec_int[1]) + "\t" + str(rec_int[2]) + "\t" + str(rec_int[3])\
                              + "\t" + "B=" + str(rec_int[23]) + "\t" + str(rec_int[16]) + "\t" + str(rec_int[17]) + "\t" + str(rec_int[18])

                elif self.N_MODULES == 3:
                    MESSAGE = "BMS" + "\t" + "N=3" \
                          + "\t" + "A=" + str(rec_int[8]) + "\t" + str(rec_int[1]) + "\t" + str(rec_int[2]) + "\t" + str(rec_int[3]) \
                          + "\t" + "B=" + str(rec_int[23]) + "\t" + str(rec_int[16]) + "\t" + str(rec_int[17]) + "\t" + str(rec_int[18])\
                          + "\t" + "C=" + str(rec_int[38]) + "\t" + str(rec_int[31]) + "\t" + str(rec_int[32]) + "\t" + str(rec_int[33])

                elif self.N_MODULES == 4:
                    MESSAGE = "BMS" + "\t" + "N=4" \
                          + "\t" + "A=" + str(rec_int[8]) + "\t" + str(rec_int[1]) + "\t" + str(rec_int[2]) + "\t" + str(rec_int[3]) \
                          + "\t" + "B=" + str(rec_int[23]) + "\t" + str(rec_int[16]) + "\t" + str(rec_int[17]) + "\t" + str(rec_int[18])\
                          + "\t" + "C=" + str(rec_int[38]) + "\t" + str(rec_int[31]) + "\t" + str(rec_int[32]) + "\t" + str(rec_int[33])\
                          + "\t" + "D=" + str(rec_int[53]) + "\t" + str(rec_int[46]) + "\t" + str(rec_int[47]) + "\t" + str(rec_int[48])

                elif self.N_MODULES == 5:
                    MESSAGE = "BMS" + "\t" + "N=5" \
                          + "\t" + "A=" + str(rec_int[8]) + "\t" + str(rec_int[1]) + "\t" + str(rec_int[2]) + "\t" + str(rec_int[3]) \
                          + "\t" + "B=" + str(rec_int[23]) + "\t" + str(rec_int[16]) + "\t" + str(rec_int[17]) + "\t" + str(rec_int[18])\
                          + "\t" + "C=" + str(rec_int[38]) + "\t" + str(rec_int[31]) + "\t" + str(rec_int[32]) + "\t" + str(rec_int[33])\
                          + "\t" + "D=" + str(rec_int[53]) + "\t" + str(rec_int[46]) + "\t" + str(rec_int[47]) + "\t" + str(rec_int[48])\
                          + "\t" + "E=" + str(rec_int[68]) + "\t" + str(rec_int[61]) + "\t" + str(rec_int[62]) + "\t" + str(rec_int[63])

                elif self.N_MODULES == 6:
                    MESSAGE = "BMS" + "\t" + "N=6" \
                          + "\t" + "A=" + str(rec_int[8]) + "\t" + str(rec_int[1]) + "\t" + str(rec_int[2]) + "\t" + str(rec_int[3]) \
                          + "\t" + "B=" + str(rec_int[23]) + "\t" + str(rec_int[16]) + "\t" + str(rec_int[17]) + "\t" + str(rec_int[18])\
                          + "\t" + "C=" + str(rec_int[38]) + "\t" + str(rec_int[31]) + "\t" + str(rec_int[32]) + "\t" + str(rec_int[33])\
                          + "\t" + "D=" + str(rec_int[53]) + "\t" + str(rec_int[46]) + "\t" + str(rec_int[47]) + "\t" + str(rec_int[48])\
                          + "\t" + "E=" + str(rec_int[68]) + "\t" + str(rec_int[61]) + "\t" + str(rec_int[62]) + "\t" + str(rec_int[63])\
                          + "\t" + "F=" + str(rec_int[83]) + "\t" + str(rec_int[76]) + "\t" + str(rec_int[77]) + "\t" + str(rec_int[78])

                elif self.N_MODULES == 7:
                    MESSAGE = "BMS" + "\t" + "N=7" \
                          + "\t" + "A=" + str(rec_int[8]) + "\t" + str(rec_int[1]) + "\t" + str(rec_int[2]) + "\t" + str(rec_int[3]) \
                          + "\t" + "B=" + str(rec_int[23]) + "\t" + str(rec_int[16]) + "\t" + str(rec_int[17]) + "\t" + str(rec_int[18])\
                          + "\t" + "C=" + str(rec_int[38]) + "\t" + str(rec_int[31]) + "\t" + str(rec_int[32]) + "\t" + str(rec_int[33])\
                          + "\t" + "D=" + str(rec_int[53]) + "\t" + str(rec_int[46]) + "\t" + str(rec_int[47]) + "\t" + str(rec_int[48])\
                          + "\t" + "E=" + str(rec_int[68]) + "\t" + str(rec_int[61]) + "\t" + str(rec_int[62]) + "\t" + str(rec_int[63])\
                          + "\t" + "F=" + str(rec_int[83]) + "\t" + str(rec_int[76]) + "\t" + str(rec_int[77]) + "\t" + str(rec_int[78])\
                          + "\t" + "G=" + str(rec_int[98]) + "\t" + str(rec_int[91]) + "\t" + str(rec_int[92]) + "\t" + str(rec_int[93])

                elif self.N_MODULES == 8:
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
                    print("ERROR number of modules not recognised please specify a number between 1 and 8")
                    return

                sock.sendto(MESSAGE, (self.UDP_IP, self.UDP_PORT1))
                sock.sendto(MESSAGE, (self.UDP_IP, self.UDP_PORT2))
                sock.sendto(MESSAGE, (self.UDP_IP, self.UDP_PORT3))
                #print"Send Package!"
                time.sleep(5)
        except Exception:
            sock.close()
            print("ERROR no communication possible, check if the connection has been opened with open()")
            return

    def join(self, timeout=None):
        """Stop the thread"""
        self._stopevent.set()
        threading.Thread.join(self, timeout)


# EMBEDDING ThreadedControl CLASS ----------------------------------------------------

class US2000B_socket_SoC_Thread(threading.Thread):


    def __init__(self,group=None,target=None,name=None,verbose=None,N_MODULES=1, UDP_IP ="127.0.0.1", UDP_PORT1 = 5005, UDP_PORT2 = 5006, UDP_PORT3 = 5007):

        threading.Thread.__init__(self,group=group,target=target,name=name,verbose=verbose)

        self._stopevent =threading.Event()# used to stop the socket loop.

        self.N_MODULES=N_MODULES
        self.UDP_IP=UDP_IP
        self.UDP_PORT1=UDP_PORT1
        self.UDP_PORT2 = UDP_PORT2
        self.UDP_PORT3 = UDP_PORT3


    def run(self):
        """Main control loop"""
        BMS = US2000B()
        BMS.open()
        self._port = BMS._port

        for i in range(1,10):
            if BMS.is_connected():
                break
            time.sleep(1)
            if i == 5:
                BMS.initialise()
            if i == 10:
                print ("ERROR, no connection could be established!")
                return
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            while not self._stopevent.isSet():

                self._port.write(str.encode('pwr\r'))
                time.sleep(0.5)
                rec_str = str(self._port.read(2200),'utf-8')
                rec_int = re.findall(r'\d+', rec_str)
                #Writes values into SOC_array and returns it.
                if self.N_MODULES == 1:
                    MESSAGE = "SoC"+"\t"+"N=1"+"\t"+"A="+str(rec_int[8])

                elif self.N_MODULES == 2:
                    MESSAGE = "SoC"+"\t"+"N=2"+"\t"+"A="+str(rec_int[8])+"\t"+"B="+str(rec_int[23])

                elif self.N_MODULES == 3:
                    MESSAGE = "SoC"+"\t"+"N=3"+"\t"+"A="+str(rec_int[8])+"\t"+"B="+str(rec_int[23])+"\t"+"C="+str(rec_int[38])

                elif self.N_MODULES == 4:
                    MESSAGE = "SoC"+"\t"+"N=4"+"\t"+"A="+str(rec_int[8])+"\t"+"B="+str(rec_int[23])+"\t"+"C="+str(rec_int[38])+"\t"+"D="+str(rec_int[53])

                elif self.N_MODULES == 5:
                    MESSAGE = "SoC"+"\t"+"N=5"+"\t"+"A="+str(rec_int[8])+"\t"+"B="+str(rec_int[23])+"\t"+"C="+str(rec_int[38])+"\t"+"D="+str(rec_int[53])+"\t"+"E="+str(rec_int[68])

                elif self.N_MODULES == 6:
                    MESSAGE = "SoC"+"\t"+"N=6"+"\t"+"A="+str(rec_int[8])+"\t"+"B="+str(rec_int[23])+"\t"+"C="+str(rec_int[38])+"\t"+"D="+str(rec_int[53])+"\t"+"E="+str(rec_int[68])+"\t"+"F="+str(rec_int[83])

                elif self.N_MODULES == 7:
                    MESSAGE = "SoC"+"\t"+"N=7"+"\t"+"A="+str(rec_int[8])+"\t"+"B="+str(rec_int[23])+"\t"+"C="+str(rec_int[38])+"\t"+"D="+str(rec_int[53])+"\t"+"E="+str(rec_int[68])+"\t"+"F="+str(rec_int[83])+"\t"+"G="+str(rec_int[98])

                elif self.N_MODULES == 8:
                    MESSAGE = "SoC"+"\t"+"N=8"+"\t"+"A="+str(rec_int[8])+"\t"+"B="+str(rec_int[23])+"\t"+"C="+str(rec_int[38])+"\t"+"D="+str(rec_int[53])+"\t"+"E="+str(rec_int[68])+"\t"+"F="+str(rec_int[83])+"\t"+"G="+str(rec_int[98])+"\t"+"H="+str(rec_int[113])

                else:
                    print("ERROR number of modules not recognised please specify a number between 1 and 8")
                    sock.close()
                    return
                sock.sendto(MESSAGE, (self.UDP_IP, self.UDP_PORT1))
                sock.sendto(MESSAGE, (self.UDP_IP, self.UDP_PORT2))
                sock.sendto(MESSAGE, (self.UDP_IP, self.UDP_PORT3))
                time.sleep(5)
        except Exception:
            sock.close()
            print("ERROR no communication possible, check if the connection has been opened with open()")
            return

    def join(self, timeout=None):
        """Stop the thread"""
        self._stopevent.set()
        threading.Thread.join(self, timeout)