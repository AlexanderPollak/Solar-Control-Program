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

def runtime_error_conext(self, ERROR_COUNTER, MODBUS_ADDRESS):
    print('Communication Error With Conext Device Modbus Address:'+str(MODBUS_ADDRESS)+'. Try:'+str(ERROR_COUNTER))


    if error_counter >=5:
        print('Reconnect with Conext Device Modbus Address:'+str(MODBUS_ADDRESS))
        time.sleep(300)
        if self.reconnect(SERVER_UNIT=MODBUS_ADDRESS):
            print('Reconnect with Conext Succesful!')
            return True
    if ERROR_COUNTER >=60:
        exit()
    return False


def control(Serial_Port, Modbus_Host, Modbus_Address_XW, Modbus_Address_MPPT_West,\
            Modbus_Address_MPPT_East, Battery_Modules, Cadance, Display, CSV_Log, SQL_Log, Control,\
            SoC_high, SoC_low, Battery_low, Battery_hysteresis, Default_battery_low, Default_battery_hysteresis,\
            Log_file_path, SQL_Host, SQL_Auth, SQL_User, SQL_Password, SQL_Database):



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
        Inv = XW()
        Inv.open(SERVER_HOST=Modbus_Host, SERVER_UNIT=Modbus_Address_XW)
        time.sleep(1)
        tmp_c = Inv.is_connected()
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
            print('Write Battery Low Voltage Cut: '+str(Inv.write_Low_Battery_Cut_Out(Battery_low))+'Volt')
            time.sleep(1)
            print('Write Battery Hysteresis: '+str(Inv.write_Hysteresis(Battery_hysteresis))+'Volt')
            time.sleep(1)
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
                        tmp_xw_log = Inv.read_Inverter_All()
                    except:
                        error_counter_conext = error_counter_conext + 1
                        if runtime_error_conext(Inv, ERROR_COUNTER=error_counter_conext, MODBUS_ADDRESS=Modbus_Address_XW):
                            error_counter_conext=0                        
                        
                    try:
                        tmp_mppt_west_log = MPPT_West.read_MPPT_All()
                    except:
                        error_counter_conext = error_counter_conext + 1
                        if runtime_error_conext(MPPT_West, ERROR_COUNTER=error_counter_conext, MODBUS_ADDRESS=Modbus_Address_MPPT_West):
                            error_counter_conext=0     

                    try:
                        tmp_mppt_east_log = MPPT_East.read_MPPT_All()
                    except:
                        error_counter_conext = error_counter_conext + 1
                        if runtime_error_conext(MPPT_East, ERROR_COUNTER=error_counter_conext, MODBUS_ADDRESS=Modbus_Address_MPPT_East):
                            error_counter_conext=0   

                        
                    tmp_mppt_log = tmp_mppt_west_log + tmp_mppt_east_log
                    if CSV_Log:
                        try:
                            PYLONTECH.log_BMS(PATH=Log_file_path,BMS_LIST=tmp_bms_log)
                        except:
                            error_counter_pylontech=error_counter_pylontech+1
                            runtime_error_pylontech(error_counter_pylontech)
                    if SQL_Log:
                        try:
                            SQL.write_BMS(BMS_LIST=tmp_bms_log)
                            SQL.write_XW(XW_LIST=tmp_xw_log)
                            SQL.write_MPPT(MPPT_LIST=tmp_mppt_log)
                        except Exception as error:
                            print("SQL_Log error:", error)


                if Display:  # Condition to print the SoC in terminal
                    try:
                        tmp = PYLONTECH.read_SoC(N_MODULES=Battery_Modules)
                        print('A:' + str(tmp[0][0]) + '\t' + 'B:' + str(tmp[1][0]) + '\t' + 'C:' + str(tmp[2][0]) + '\t' + \
                              'D:' + str(tmp[3][0]) + '\t' + 'E:' + str(tmp[4][0]) + '\t' + 'F:' + str(tmp[5][0]) + '\t' \
                             +Inv.read_Inverter_Status())
                    except:
                        error_counter_conext=error_counter_conext+1
                        if runtime_error_conext(Inv,error_counter_conext):
                            error_counter_conext=0



                if Control:  # Condition to Control Inverter Based on SoC
                    try:
                        Battery_SoC = PYLONTECH.read_SoC(N_MODULES=Battery_Modules)
                        Avg_SoC = 0
                        for i in range(len(Battery_SoC)) :
                            Avg_SoC=Avg_SoC+Battery_SoC[i][0]
                        Avg_SoC = round(Avg_SoC / Battery_Modules)
                        
                        if Avg_SoC >= SoC_high:  # Condition to enable Inverter Grid Support
                            if Inv.read_Load_Shave_Status() == 'Disable':
                                Inv.write_Load_Shave_Status('Enable')
                                print('Grid Support: ON')
                        if Avg_SoC <= SoC_low:  # Condition to disable Inverter Grid Support
                            if Inv.read_Load_Shave_Status() == 'Enable':
                                Inv.write_Load_Shave_Status('Disable')
                                print('Grid Support: OFF')
                    except:
                        error_counter_conext = error_counter_conext + 1
                        if runtime_error_conext(Inv, error_counter_conext):
                            error_counter_conext=0


        except Exception as error:
            print("An error occurred:", error)




        except KeyboardInterrupt:
            try:
                Inv.write_Hysteresis(Default_battery_hysteresis)
                Inv.write_Low_Battery_Cut_Out(Default_battery_low)
                Inv.write_Load_Shave_Status('disable')
                del PYLONTECH
                del Inv
                del MPPT_West
                del MPPT_East
                del SQL
                print('interrupted!')
            except:
                print('Control Stop!')
            # ---------------------------------------------------------------------------#







    except KeyboardInterrupt:
        try:
            Inv.write_Hysteresis(Default_battery_hysteresis)
            Inv.write_Low_Battery_Cut_Out(Default_battery_low)
            Inv.write_Load_Shave_Status('disable')
            del PYLONTECH
            del Inv
            del MPPT_West
            del MPPT_East
            del SQL
        except:
            print('Control Stop!')
    except Exception as tmp_exeption:
        try:
            Inv.write_Hysteresis(Default_battery_hysteresis)
            Inv.write_Low_Battery_Cut_Out(Default_battery_low)
            Inv.write_Load_Shave_Status('disable')
            del PYLONTECH
            del Inv
            del MPPT_West
            del MPPT_East
            del SQL
        except:
            print('Control Stop! Exception'+tmp_exeption)