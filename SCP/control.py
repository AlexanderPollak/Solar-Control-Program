# This script connects to the Pylontech US2000B Plus
# and read the charge status, voltage, current, and temperature
# it stores the data in a .csv file with the actual date

from conext_com import *
from pylontech_com import *
from mysql_write import *
import time


def runtime_error_pylontech(error_counter):
    print('Communication Error With Pylontech! Try:'+str(error_counter))
    if error_counter >=100:
        print('Max Communication retries reached!')
        exit()
    return

def runtime_error_conext(self, error_counter):
    print('Communication Error With Conext! Try:'+str(error_counter))


    if error_counter >=10:
        print('Reconnect with Conext!')
        time.sleep(300)
        if self.reconnect():
            print('Reconnect with Conext Succesful!')
            return True
    if error_counter >=60:
        exit()
    return False


def control(Serial_Port, Modbus_Host, Modbus_Address_XW, Modbus_Address_MPPT_West,\
            Modbus_Address_MPPT_East, Battery_Modules, Cadance, Display, CSV_Log, SQL_Log, Control,\
            SoC_high, SoC_low, Battery_low, Battery_hysteresis, Log_file_path, SQL_Host, SQL_Auth,\
            SQL_User, SQL_Password, SQL_Database):



    try:

        print('SolarControl:1.1.0 ')

        # ---------------------------------------------------------------------------#
        # Initialise communication to BMS
        PYLONTECH = US2000B()
        tmp_b = PYLONTECH.initialise(port=Serial_Port)
        print('BATTERY Connection Initialised:' + str(tmp_b))

        # Establish connection to BMS
        time.sleep(2)
        PYLONTECH.open(port=Serial_Port)
        time.sleep(1)
        tmp_b = PYLONTECH.is_connected()
        print('BATTERY Connection Established:' + str(tmp_b))
        # ---------------------------------------------------------------------------#


        # ---------------------------------------------------------------------------#
        # Establish communication to Inverter
        XW = XW()
        XW.open(SERVER_HOST=Modbus_Host, SERVER_UNIT=Modbus_Address_XW)
        time.sleep(1)
        tmp_c = XW.is_connected()
        print('INVERTER Connection Established:' + str(tmp_c))
        # ---------------------------------------------------------------------------#

        # ---------------------------------------------------------------------------#
        # Establish communication to Charge Controller West Roof
        MPPT_West = MPPT60()
        MPPT_West.open(SERVER_HOST=Modbus_Host, SERVER_UNIT=Modbus_Address_MPPT_West)
        time.sleep(1)
        tmp_mw = MPPT_West.is_connected()
        print('MPPT Charge Controller West Roof Connection Established:' + str(tmp_mw))
        # ---------------------------------------------------------------------------#

        # ---------------------------------------------------------------------------#
        # Establish communication to Charge Controller East Roof
        MPPT_East = MPPT60()
        MPPT_East.open(SERVER_HOST=Modbus_Host, SERVER_UNIT=Modbus_Address_MPPT_East)
        time.sleep(1)
        tmp_me = MPPT_East.is_connected()
        print('MPPT Charge Controller East Roof Connection Established:' + str(tmp_me))
        # ---------------------------------------------------------------------------#


        # ---------------------------------------------------------------------------#
        # Connect to MySQL Server
        SQL= MySQL_com()
        SQL.open(HOST=SQL_Host,USER =SQL_User,PASSWORD=SQL_Password,DATABASE=SQL_Database,AUTH_PLUGIN=SQL_Auth)
        time.sleep(1)
        tmp_s = SQL.is_connected()
        print('SQL Server Connection Established:' + str(tmp_s))
        # ---------------------------------------------------------------------------#



        # ---------------------------------------------------------------------------#
        if not (tmp_b):  # Stopps program if connection has not been established.
            print ('ERROR: No Connection to BMS!')
            exit()
        if not (tmp_c):  # Stopps program if connection has not been established.
            print ('ERROR: No Connection to INVERTER!')
            exit()
        if not (tmp_mw):  # Stopps program if connection has not been established.
            print ('ERROR: No Connection to MPPT Charge Controller West Roof!')
            exit()
        if not (tmp_me):  # Stopps program if connection has not been established.
            print ('ERROR: No Connection to MPPT Charge Controller East Roof!')
            exit()
        if not (tmp_s):  # Stopps program if connection has not been established.
            print ('ERROR: No Connection to SQL Server!')
            exit()
        # ---------------------------------------------------------------------------#





        # ---------------------------------------------------------------------------#
        try:  # Program Loop
            XW.write_Low_Battery_Cut_Out(Battery_low)
            XW.write_Hysteresis(Battery_hysteresis)
            error_counter_pylontech=0
            error_counter_conext = 0
            while True:
                time.sleep(Cadance)
                if CSV_Log or SQL_Log:  # Condition to log BMS data into .csv file or SQL Database.
                    try:
                        tmp_bms_log = PYLONTECH.read_BMS(N_MODULES=Battery_Modules)
                    except:
                        error_counter_pylontech=error_counter_pylontech+1
                        runtime_error_pylontech(error_counter_pylontech)
                    
                    try:
                        tmp_xw_log = XW.read_Inverter_All()
                    except:
                        error_counter_conext = error_counter_conext + 1
                        if runtime_error_conext(XW, error_counter_conext):
                            error_counter_conext=0                        
                        
                    try:
                        tmp_mppt_west_log = MPPT_West.read_MPPT_All()
                    except:
                        error_counter_conext = error_counter_conext + 1
                        if runtime_error_conext(MPPT_West, error_counter_conext):
                            error_counter_conext=0     

                    try:
                        tmp_mppt_east_log = MPPT_East.read_MPPT_All()
                    except:
                        error_counter_conext = error_counter_conext + 1
                        if runtime_error_conext(MPPT_East, error_counter_conext):
                            error_counter_conext=0   

                        
                    tmp_mppt_log = tmp_mppt_west_log + tmp_mppt_east_log
                    if CSV_Log:
                        try:
                            PYLONTECH.log_BMS(PATH=Log_file_path,BMS_LIST=tmp_bms_log)
                        except:
                            error_counter_pylontech=error_counter_pylontech+1
                            runtime_error_pylontech(error_counter_pylontech)
                    if SQL_Log:
                        SQL.write_BMS(BMS_LIST=tmp_bms_log)
                        SQL.write_XW(XW_LIST=tmp_xw_log)
                        SQL.write_MPPT(MPPT_LIST=tmp_mppt_log)



                if Display:  # Condition to print the SoC in terminal
                    try:
                        tmp = PYLONTECH.read_SoC(N_MODULES=Battery_Modules)
                        print('A:' + str(tmp[0][0]) + '\t' + 'B:' + str(tmp[1][0]) + '\t' + 'C:' + str(tmp[2][0]) + '\t' + \
                              'D:' + str(tmp[3][0]) + '\t' + 'E:' + str(tmp[4][0]) + '\t' + 'F:' + str(tmp[5][0]) + '\t' \
                             +XW.read_Inverter_Status())
                    except:
                        error_counter_conext=error_counter_conext+1
                        if runtime_error_conext(XW,error_counter_conext):
                            error_counter_conext=0



                if Control:  # Condition to Control Inverter Based on SoC
                    try:
                        Battery_SoC = PYLONTECH.read_SoC(N_MODULES=Battery_Modules)
                        Avg_SoC = 0
                        for i in range(len(Battery_SoC)) :
                            Avg_SoC=Avg_SoC+Battery_SoC[i][0]
                        Avg_SoC = round(Avg_SoC / Battery_Modules)
                        
                        if Avg_SoC >= SoC_high:  # Condition to enable Inverter Grid Support
                            if XW.read_Load_Shave_Status() == 'Disable':
                                XW.write_Load_Shave_Status('Enable')
                                print('Grid Support: ON')
                        if Avg_SoC <= SoC_low:  # Condition to disable Inverter Grid Support
                            if XW.read_Load_Shave_Status() == 'Enable':
                                XW.write_Load_Shave_Status('Disable')
                                print('Grid Support: OFF')
                    except:
                        error_counter_conext = error_counter_conext + 1
                        if runtime_error_conext(XW, error_counter_conext):
                            error_counter_conext=0


        except Exception as error:
            print("An error occurred:", error)




        except KeyboardInterrupt:
            try:
                XW.write_Hysteresis(2.5)
                XW.write_Low_Battery_Cut_Out(46.5)
                XW.write_Load_Shave_Status('disable')
                del PYLONTECH
                del XW
                del MPPT_West
                del MPPT_East
                del SQL
                print('interrupted!')
            except:
                print('Control Stop!')
            # ---------------------------------------------------------------------------#







    except KeyboardInterrupt:
        try:
            XW.write_Hysteresis(2.5)
            XW.write_Low_Battery_Cut_Out(46.5)
            XW.write_Load_Shave_Status('disable')
            del PYLONTECH
            del XW
            del MPPT_West
            del MPPT_East
            del SQL
        except:
            print('Control Stop!')
    except Exception as tmp_exeption:
        try:
            XW.write_Hysteresis(2.5)
            XW.write_Low_Battery_Cut_Out(46.5)
            XW.write_Load_Shave_Status('disable')
            del PYLONTECH
            del XW
            del MPPT_West
            del MPPT_East
            del SQL
        except:
            print('Control Stop! Exception'+tmp_exeption)