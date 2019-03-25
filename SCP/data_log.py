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
import datetime,os,csv,socket
import numpy as np


class log():
        """This class implements the serial connection functions """

        def __init__(self):
            ''' Constructor for this class. '''


        def __del__(self):
            ''' Destructor for this class. '''


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

            try:
                while True:
                    # filename = str(PATH) + '/' + 'BMS_'+ str(datetime.date.today()) + '.csv'
                    # tmp_check_file = os.path.isfile(filename)
                    # csvfile = open(filename, mode='a')
                    # name = ['Time','SoC_1', 'Voltage_1', 'Current_1','Temperature_1',
                    #         'SoC_2', 'Voltage_2', 'Current_2', 'Temperature_2',
                    #         'SoC_3', 'Voltage_3', 'Current_3', 'Temperature_3',
                    #         'SoC_4', 'Voltage_4', 'Current_4', 'Temperature_4',
                    #         'SoC_5', 'Voltage_5', 'Current_5', 'Temperature_5',
                    #         'SoC_6', 'Voltage_6', 'Current_6', 'Temperature_6',
                    #         'SoC_7', 'Voltage_7', 'Current_7', 'Temperature_7',
                    #         'SoC_8', 'Voltage_8', 'Current_8', 'Temperature_8',
                    #         ]
                    # data_writer = csv.DictWriter(csvfile, fieldnames=name)
                    # if not tmp_check_file:
                    #     data_writer.writeheader()


                    data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
                    tmp_pointer = data.find('N=')
                    N_MODULES = int(data[tmp_pointer:tmp_pointer+1])
                    tmp_BMS = np.zeros((N_MODULES, 4))



                    # if N_MODULES == 1:
                    #     data_writer.writerow({'Time': str(datetime.datetime.now().hour)+':'+str(datetime.datetime.now().minute),
                    #                         'SoC_1':tmp_BMS[0,0],'Voltage_1':tmp_BMS[0,1],'Current_1':tmp_BMS[0,2],'Temperature_1':tmp_BMS[0,3]})
                    # elif N_MODULES == 2:
                    #     data_writer.writerow({'Time': str(datetime.datetime.now().hour)+':'+str(datetime.datetime.now().minute),
                    #                         'SoC_1':tmp_BMS[0,0],'Voltage_1':tmp_BMS[0,1],'Current_1':tmp_BMS[0,2],'Temperature_1':tmp_BMS[0,3],
                    #                         'SoC_2':tmp_BMS[1,0],'Voltage_2':tmp_BMS[1,1],'Current_2':tmp_BMS[1,2],'Temperature_2':tmp_BMS[1,3]})
                    # elif N_MODULES == 3:
                    #     data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                    #                         'SoC_1':tmp_BMS[0,0],'Voltage_1':tmp_BMS[0,1],'Current_1':tmp_BMS[0,2],'Temperature_1':tmp_BMS[0,3],
                    #                         'SoC_2':tmp_BMS[1,0],'Voltage_2':tmp_BMS[1,1],'Current_2':tmp_BMS[1,2],'Temperature_2':tmp_BMS[1,3],
                    #                         'SoC_3':tmp_BMS[2,0],'Voltage_3':tmp_BMS[2,1],'Current_3':tmp_BMS[2,2],'Temperature_3':tmp_BMS[2,3]})
                    # elif N_MODULES == 4:
                    #     data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                    #                         'SoC_1':tmp_BMS[0,0],'Voltage_1':tmp_BMS[0,1],'Current_1':tmp_BMS[0,2],'Temperature_1':tmp_BMS[0,3],
                    #                         'SoC_2':tmp_BMS[1,0],'Voltage_2':tmp_BMS[1,1],'Current_2':tmp_BMS[1,2],'Temperature_2':tmp_BMS[1,3],
                    #                         'SoC_3':tmp_BMS[2,0],'Voltage_3':tmp_BMS[2,1],'Current_3':tmp_BMS[2,2],'Temperature_3':tmp_BMS[2,3],
                    #                         'SoC_4':tmp_BMS[3,0],'Voltage_4':tmp_BMS[3,1],'Current_4':tmp_BMS[3,2],'Temperature_4':tmp_BMS[3,3]})
                    # elif N_MODULES == 5:
                    #     data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                    #                         'SoC_1':tmp_BMS[0,0],'Voltage_1':tmp_BMS[0,1],'Current_1':tmp_BMS[0,2],'Temperature_1':tmp_BMS[0,3],
                    #                         'SoC_2':tmp_BMS[1,0],'Voltage_2':tmp_BMS[1,1],'Current_2':tmp_BMS[1,2],'Temperature_2':tmp_BMS[1,3],
                    #                         'SoC_3':tmp_BMS[2,0],'Voltage_3':tmp_BMS[2,1],'Current_3':tmp_BMS[2,2],'Temperature_3':tmp_BMS[2,3],
                    #                         'SoC_4':tmp_BMS[3,0],'Voltage_4':tmp_BMS[3,1],'Current_4':tmp_BMS[3,2],'Temperature_4':tmp_BMS[3,3],
                    #                         'SoC_5':tmp_BMS[4,0],'Voltage_5':tmp_BMS[4,1],'Current_5':tmp_BMS[4,2],'Temperature_5':tmp_BMS[4,3]})
                    # elif N_MODULES == 6:
                    #     data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                    #                         'SoC_1':tmp_BMS[0,0],'Voltage_1':tmp_BMS[0,1],'Current_1':tmp_BMS[0,2],'Temperature_1':tmp_BMS[0,3],
                    #                         'SoC_2':tmp_BMS[1,0],'Voltage_2':tmp_BMS[1,1],'Current_2':tmp_BMS[1,2],'Temperature_2':tmp_BMS[1,3],
                    #                         'SoC_3':tmp_BMS[2,0],'Voltage_3':tmp_BMS[2,1],'Current_3':tmp_BMS[2,2],'Temperature_3':tmp_BMS[2,3],
                    #                         'SoC_4':tmp_BMS[3,0],'Voltage_4':tmp_BMS[3,1],'Current_4':tmp_BMS[3,2],'Temperature_4':tmp_BMS[3,3],
                    #                         'SoC_5':tmp_BMS[4,0],'Voltage_5':tmp_BMS[4,1],'Current_5':tmp_BMS[4,2],'Temperature_5':tmp_BMS[4,3],
                    #                         'SoC_6':tmp_BMS[5,0],'Voltage_6':tmp_BMS[5,1],'Current_6':tmp_BMS[5,2],'Temperature_6':tmp_BMS[5,3]})
                    # elif N_MODULES == 7:
                    #     data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                    #                         'SoC_1':tmp_BMS[0,0],'Voltage_1':tmp_BMS[0,1],'Current_1':tmp_BMS[0,2],'Temperature_1':tmp_BMS[0,3],
                    #                         'SoC_2':tmp_BMS[1,0],'Voltage_2':tmp_BMS[1,1],'Current_2':tmp_BMS[1,2],'Temperature_2':tmp_BMS[1,3],
                    #                         'SoC_3':tmp_BMS[2,0],'Voltage_3':tmp_BMS[2,1],'Current_3':tmp_BMS[2,2],'Temperature_3':tmp_BMS[2,3],
                    #                         'SoC_4':tmp_BMS[3,0],'Voltage_4':tmp_BMS[3,1],'Current_4':tmp_BMS[3,2],'Temperature_4':tmp_BMS[3,3],
                    #                         'SoC_5':tmp_BMS[4,0],'Voltage_5':tmp_BMS[4,1],'Current_5':tmp_BMS[4,2],'Temperature_5':tmp_BMS[4,3],
                    #                         'SoC_6':tmp_BMS[5,0],'Voltage_6':tmp_BMS[5,1],'Current_6':tmp_BMS[5,2],'Temperature_6':tmp_BMS[5,3],
                    #                         'SoC_7':tmp_BMS[6,0],'Voltage_7':tmp_BMS[6,1],'Current_7':tmp_BMS[6,2],'Temperature_7':tmp_BMS[6,3]})
                    # elif N_MODULES == 8:
                    #     data_writer.writerow({'Time': str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute),
                    #                         'SoC_1':tmp_BMS[0,0],'Voltage_1':tmp_BMS[0,1],'Current_1':tmp_BMS[0,2],'Temperature_1':tmp_BMS[0,3],
                    #                         'SoC_2':tmp_BMS[1,0],'Voltage_2':tmp_BMS[1,1],'Current_2':tmp_BMS[1,2],'Temperature_2':tmp_BMS[1,3],
                    #                         'SoC_3':tmp_BMS[2,0],'Voltage_3':tmp_BMS[2,1],'Current_3':tmp_BMS[2,2],'Temperature_3':tmp_BMS[2,3],
                    #                         'SoC_4':tmp_BMS[3,0],'Voltage_4':tmp_BMS[3,1],'Current_4':tmp_BMS[3,2],'Temperature_4':tmp_BMS[3,3],
                    #                         'SoC_5':tmp_BMS[4,0],'Voltage_5':tmp_BMS[4,1],'Current_5':tmp_BMS[4,2],'Temperature_5':tmp_BMS[4,3],
                    #                         'SoC_6':tmp_BMS[5,0],'Voltage_6':tmp_BMS[5,1],'Current_6':tmp_BMS[5,2],'Temperature_6':tmp_BMS[5,3],
                    #                         'SoC_7':tmp_BMS[6,0],'Voltage_7':tmp_BMS[6,1],'Current_7':tmp_BMS[6,2],'Temperature_7':tmp_BMS[6,3],
                    #                         'SoC_8':tmp_BMS[7,0],'Voltage_8':tmp_BMS[7,1],'Current_8':tmp_BMS[7,2],'Temperature_8':tmp_BMS[7,3]})
                    #
                    # csvfile.flush()

            except KeyboardInterrupt:
                sock.close()
                csvfile.close()
                return
            except Exception:
                print"ERROR no communication possible"
                sock.close()
                csvfile.close()
                return