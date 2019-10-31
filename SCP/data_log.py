""" This module contains classes and functions to log data provided in sockets by the BMS and
 Schneider Conext; ComBox, MPPT60 150, and XW+ Battery Inverter.

**Description:**

    The data is provided by the communication methods which are used to read the parameter of the BMS and Schneider
    Devices. The functions check if data is send to the specific ports and if so, writes those into a logfile.
    These logfiles then can be plotted using the visualisation class.
    This package includes functions to log the following device parameters
    devices:
        1. Pylontech SoC
        2. Pylontech BMS
        3. Schneider XW+ 8548E grid voltage
        4. Schneider XW+ 8548E load power
        5. Schneider XW+ 8548E grid power input
        6. Schneider MPPT60 150 solar power

The main class in this module ("log") allows the user to
log provided data via sockets to file.
Each function checks if the socket has data in it and logs the values.

"""
import datetime,time,os,csv,socket,re
import numpy as np


class Log():
        """This class implements the serial connection functions """

        def __init__(self):
            ''' Constructor for this class. '''


        def __del__(self):
            ''' Destructor for this class. '''


        def log_SoC(self, PATH='../Log/', UDP_IP ="127.0.0.1", UDP_PORT = 5006):
            """This function receives the SoC values provided at port 5006 of the
            Pylontech Battery "socket_SoC" function.
            The program listens to the specified UDP port eg. Default=5006

            Args:
                PATH: defines the path where the logfile will be stored.
                UDP_IP: udp ip address. Default="127.0.0.1"
                UDP_PORT: port to which the packets should be send to. Default=5005
            Returns:

            """
            sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  # UDP
            sock.bind((UDP_IP, UDP_PORT))

            #file handling
            filename = str(PATH) + '/' + 'SoC_' + str(datetime.date.today()) + '.csv'
            tmp_date = str(datetime.date.today())
            tmp_check_file = os.path.isfile(filename)
            csvfile = open(filename, mode='a')
            name = ['Time', 'SoC_1', 'Voltage_1', 'Current_1', 'Temperature_1',
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


            try:
                while True:

                    if tmp_date != str(datetime.date.today()): #Creates a new file with the new date.
                        filename = str(PATH) + '/' + 'SoC_' + str(datetime.date.today()) + '.csv'
                        tmp_date = str(datetime.date.today())
                        csvfile = open(filename, mode='a')
                        data_writer = csv.DictWriter(csvfile, fieldnames=name)
                        data_writer.writeheader()


                    data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes

                    if "SoC" == data[0:2]:  # checks for the correct sting received at this port "SoC"
                        tmp_pointer = data.find('N=')+len('N=')
                        if not tmp_pointer==0:
                            N_MODULES = int(data[tmp_pointer:tmp_pointer+1])



                        if N_MODULES == 1:
                            tmp_SoC = re.findall(r'\d+', data)
                            data_writer.writerow({'Time': str(datetime.datetime.now().hour)+':'+str(datetime.datetime.now().minute),
                                                'SoC_1':tmp_SoC[1]})
                        elif N_MODULES == 2:
                            tmp_SoC = re.findall(r'\d+', data)
                            data_writer.writerow({'Time': str(datetime.datetime.now().hour)+':'+str(datetime.datetime.now().minute),
                                                'SoC_1':tmp_SoC[1],'SoC_2':tmp_SoC[2]})
                        elif N_MODULES == 3:
                            tmp_SoC = re.findall(r'\d+', data)
                            data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                                                'SoC_1':tmp_SoC[1],'SoC_2':tmp_SoC[2],'SoC_3':tmp_SoC[3]})
                        elif N_MODULES == 4:
                            tmp_SoC = re.findall(r'\d+', data)
                            data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                                                'SoC_1':tmp_SoC[1],'SoC_2':tmp_SoC[2],'SoC_3':tmp_SoC[3],'SoC_4':tmp_SoC[4]})
                        elif N_MODULES == 5:
                            tmp_SoC = re.findall(r'\d+', data)
                            data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                                                'SoC_1':tmp_SoC[1],'SoC_2':tmp_SoC[2],'SoC_3':tmp_SoC[3],'SoC_4':tmp_SoC[4],
                                                'SoC_5':tmp_SoC[5]})
                        elif N_MODULES == 6:
                            tmp_SoC = re.findall(r'\d+', data)
                            data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                                                'SoC_1':tmp_SoC[1],'SoC_2':tmp_SoC[2],'SoC_3':tmp_SoC[3],'SoC_4':tmp_SoC[4],
                                                'SoC_5':tmp_SoC[5],'SoC_6':tmp_SoC[6]})
                        elif N_MODULES == 7:
                            tmp_SoC = re.findall(r'\d+', data)
                            data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                                                'SoC_1':tmp_SoC[1],'SoC_2':tmp_SoC[2],'SoC_3':tmp_SoC[3],'SoC_4':tmp_SoC[4],
                                                'SoC_5':tmp_SoC[5],'SoC_6':tmp_SoC[6],'SoC_7':tmp_SoC[7]})
                        elif N_MODULES == 8:
                            tmp_SoC = re.findall(r'\d+', data)
                            data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                                                'SoC_1':tmp_SoC[1],'SoC_2':tmp_SoC[2],'SoC_3':tmp_SoC[3],'SoC_4':tmp_SoC[4],
                                                'SoC_5':tmp_SoC[5],'SoC_6':tmp_SoC[6],'SoC_7':tmp_SoC[7],'SoC_8':tmp_SoC[8]})

                        csvfile.flush()
                        time.sleep(30)


            except KeyboardInterrupt:
                sock.close()
                csvfile.close()
                print('interrupted!')
                return
            except Exception:
                print("ERROR no communication possible")
                sock.close()
                csvfile.close()
                return

        def log_BMS(self, PATH='../Log/', UDP_IP ="127.0.0.1", UDP_PORT = 5006):
            """This function receives the BMS values provided at port 5006 of the
            Pylontech Battery "socket_BMS" function.
            The program listens to the specified UDP port eg. Default=5006

            Args:
                PATH: defines the path where the logfile will be stored.
                UDP_IP: udp ip address. Default="127.0.0.1"
                UDP_PORT: port to which the packets should be send to. Default=5005
            Returns:

            """
            sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  # UDP
            sock.bind((UDP_IP, UDP_PORT))

            #file handling
            filename = str(PATH) + '/' + 'BMS_' + str(datetime.date.today()) + '.csv'
            tmp_date = str(datetime.date.today())
            tmp_check_file = os.path.isfile(filename)
            csvfile = open(filename, mode='a')
            name = ['Time', 'SoC_1', 'Voltage_1', 'Current_1', 'Temperature_1',
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


            try:
                while True:

                    if tmp_date != str(datetime.date.today()): #Creates a new file with the new date.
                        filename = str(PATH) + '/' + 'BMS_' + str(datetime.date.today()) + '.csv'
                        tmp_date = str(datetime.date.today())
                        csvfile = open(filename, mode='a')
                        data_writer = csv.DictWriter(csvfile, fieldnames=name)
                        data_writer.writeheader()


                    data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes

                    if "BMS" == data[0:2]:#checks for the correct sting received at this port "BMS"
                        tmp_pointer = data.find('N=')+len('N=')
                        if not tmp_pointer==0:
                            N_MODULES = int(data[tmp_pointer:tmp_pointer+1])



                        if N_MODULES == 1:
                            tmp_BMS = re.findall(r'\d+', data)
                            data_writer.writerow({'Time': str(datetime.datetime.now().hour)+':'+str(datetime.datetime.now().minute),
                                                'SoC_1':tmp_BMS[1],'Voltage_1':tmp_BMS[2],'Current_1':tmp_BMS[3],'Temperature_1':tmp_BMS[4]})
                        elif N_MODULES == 2:
                            tmp_BMS = re.findall(r'\d+', data)
                            data_writer.writerow({'Time': str(datetime.datetime.now().hour)+':'+str(datetime.datetime.now().minute),
                                                'SoC_1':tmp_BMS[1],'Voltage_1':tmp_BMS[2],'Current_1':tmp_BMS[3],'Temperature_1':tmp_BMS[4],
                                                'SoC_2':tmp_BMS[5],'Voltage_2':tmp_BMS[6],'Current_2':tmp_BMS[7],'Temperature_2':tmp_BMS[8]})
                        elif N_MODULES == 3:
                            tmp_BMS = re.findall(r'\d+', data)
                            data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                                                'SoC_1':tmp_BMS[1],'Voltage_1':tmp_BMS[2],'Current_1':tmp_BMS[3],'Temperature_1':tmp_BMS[4],
                                                'SoC_2':tmp_BMS[5],'Voltage_2':tmp_BMS[6],'Current_2':tmp_BMS[7],'Temperature_2':tmp_BMS[8],
                                                'SoC_3':tmp_BMS[9],'Voltage_3':tmp_BMS[10],'Current_3':tmp_BMS[11],'Temperature_3':tmp_BMS[12]})
                        elif N_MODULES == 4:
                            tmp_BMS = re.findall(r'\d+', data)
                            data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                                                'SoC_1':tmp_BMS[1],'Voltage_1':tmp_BMS[2],'Current_1':tmp_BMS[3],'Temperature_1':tmp_BMS[4],
                                                'SoC_2':tmp_BMS[5],'Voltage_2':tmp_BMS[6],'Current_2':tmp_BMS[7],'Temperature_2':tmp_BMS[8],
                                                'SoC_3':tmp_BMS[9],'Voltage_3':tmp_BMS[10],'Current_3':tmp_BMS[11],'Temperature_3':tmp_BMS[12],
                                                'SoC_4':tmp_BMS[13],'Voltage_4':tmp_BMS[14],'Current_4':tmp_BMS[15],'Temperature_4':tmp_BMS[16]})
                        elif N_MODULES == 5:
                            tmp_BMS = re.findall(r'\d+', data)
                            data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                                                'SoC_1':tmp_BMS[1],'Voltage_1':tmp_BMS[2],'Current_1':tmp_BMS[3],'Temperature_1':tmp_BMS[4],
                                                'SoC_2':tmp_BMS[5],'Voltage_2':tmp_BMS[6],'Current_2':tmp_BMS[7],'Temperature_2':tmp_BMS[8],
                                                'SoC_3':tmp_BMS[9],'Voltage_3':tmp_BMS[10],'Current_3':tmp_BMS[11],'Temperature_3':tmp_BMS[12],
                                                'SoC_4':tmp_BMS[13],'Voltage_4':tmp_BMS[14],'Current_4':tmp_BMS[15],'Temperature_4':tmp_BMS[16],
                                                'SoC_5':tmp_BMS[17],'Voltage_5':tmp_BMS[18],'Current_5':tmp_BMS[19],'Temperature_5':tmp_BMS[20]})
                        elif N_MODULES == 6:
                            tmp_BMS = re.findall(r'\d+', data)
                            data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                                                'SoC_1':tmp_BMS[1],'Voltage_1':tmp_BMS[2],'Current_1':tmp_BMS[3],'Temperature_1':tmp_BMS[4],
                                                'SoC_2':tmp_BMS[5],'Voltage_2':tmp_BMS[6],'Current_2':tmp_BMS[7],'Temperature_2':tmp_BMS[8],
                                                'SoC_3':tmp_BMS[9],'Voltage_3':tmp_BMS[10],'Current_3':tmp_BMS[11],'Temperature_3':tmp_BMS[12],
                                                'SoC_4':tmp_BMS[13],'Voltage_4':tmp_BMS[14],'Current_4':tmp_BMS[15],'Temperature_4':tmp_BMS[16],
                                                'SoC_5':tmp_BMS[17],'Voltage_5':tmp_BMS[18],'Current_5':tmp_BMS[19],'Temperature_5':tmp_BMS[20],
                                                'SoC_6':tmp_BMS[21],'Voltage_6':tmp_BMS[22],'Current_6':tmp_BMS[23],'Temperature_6':tmp_BMS[24]})
                        elif N_MODULES == 7:
                            tmp_BMS = re.findall(r'\d+', data)
                            data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                                                'SoC_1':tmp_BMS[1],'Voltage_1':tmp_BMS[2],'Current_1':tmp_BMS[3],'Temperature_1':tmp_BMS[4],
                                                'SoC_2':tmp_BMS[5],'Voltage_2':tmp_BMS[6],'Current_2':tmp_BMS[7],'Temperature_2':tmp_BMS[8],
                                                'SoC_3':tmp_BMS[9],'Voltage_3':tmp_BMS[10],'Current_3':tmp_BMS[11],'Temperature_3':tmp_BMS[12],
                                                'SoC_4':tmp_BMS[13],'Voltage_4':tmp_BMS[14],'Current_4':tmp_BMS[15],'Temperature_4':tmp_BMS[16],
                                                'SoC_5':tmp_BMS[17],'Voltage_5':tmp_BMS[18],'Current_5':tmp_BMS[19],'Temperature_5':tmp_BMS[20],
                                                'SoC_6':tmp_BMS[21],'Voltage_6':tmp_BMS[22],'Current_6':tmp_BMS[23],'Temperature_6':tmp_BMS[24],
                                                'SoC_7':tmp_BMS[25],'Voltage_7':tmp_BMS[26],'Current_7':tmp_BMS[27],'Temperature_7':tmp_BMS[28]})
                        elif N_MODULES == 8:
                            tmp_BMS = re.findall(r'\d+', data)
                            data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                                                'SoC_1':tmp_BMS[1],'Voltage_1':tmp_BMS[2],'Current_1':tmp_BMS[3],'Temperature_1':tmp_BMS[4],
                                                'SoC_2':tmp_BMS[5],'Voltage_2':tmp_BMS[6],'Current_2':tmp_BMS[7],'Temperature_2':tmp_BMS[8],
                                                'SoC_3':tmp_BMS[9],'Voltage_3':tmp_BMS[10],'Current_3':tmp_BMS[11],'Temperature_3':tmp_BMS[12],
                                                'SoC_4':tmp_BMS[13],'Voltage_4':tmp_BMS[14],'Current_4':tmp_BMS[15],'Temperature_4':tmp_BMS[16],
                                                'SoC_5':tmp_BMS[17],'Voltage_5':tmp_BMS[18],'Current_5':tmp_BMS[19],'Temperature_5':tmp_BMS[20],
                                                'SoC_6':tmp_BMS[21],'Voltage_6':tmp_BMS[22],'Current_6':tmp_BMS[23],'Temperature_6':tmp_BMS[24],
                                                'SoC_7':tmp_BMS[25],'Voltage_7':tmp_BMS[26],'Current_7':tmp_BMS[27],'Temperature_7':tmp_BMS[28],
                                                'SoC_8':tmp_BMS[29],'Voltage_8':tmp_BMS[30],'Current_8':tmp_BMS[31],'Temperature_8':tmp_BMS[32]})

                        csvfile.flush()
                        time.sleep(30)

            except KeyboardInterrupt:
                sock.close()
                csvfile.close()
                print('interrupted!')
                return
            except Exception:
                print("ERROR no communication possible")
                sock.close()
                csvfile.close()
                return

