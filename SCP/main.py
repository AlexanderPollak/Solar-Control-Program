#START OF MAIN:

import configparser
from control import *


def main():
    
    # Import SCP gonfiguration values from scp.cfg file in etc directory
    config = configparser.ConfigParser()
    config.read('/usr/local/Solar-Control-Program/etc/scp.cfg') # Location of config file

    # Parse values into the control function.

    # Communication settings to connect to the Pylontech BMS and the Conext Modbus.
    Serial_Port = config.get('COMMUNICATION SETTINGS','Serial_Port')  # Serial Port for Communication with Pylontech
    Modbus_Host = config.get('COMMUNICATION SETTINGS','Modbus_Host')  # Modbus Server Address for Communication with Inverter
    Modbus_Address_XW = config.getint('COMMUNICATION SETTINGS','Modbus_Address_XW') # Modbus Address for XW+ 8548 Inverter
    Modbus_Address_MPPT_West = config.getint('COMMUNICATION SETTINGS','Modbus_Address_MPPT_West') # Modbus Address for MPPT 60 15 Charge Controller on West Roof
    Modbus_Address_MPPT_East = config.getint('COMMUNICATION SETTINGS','Modbus_Address_MPPT_East') # Modbus Address for MPPT 60 15 Charge Controller on East Roof

    # Location fo the .csv BMS logfile and the number of batteries installed (1-8).
    Log_File_Path = config.get('PYLONTECH BATTERY SPECIFIC SETTINGS','CSV_Log_File_Path')
    Battery_Modules = config.getint('PYLONTECH BATTERY SPECIFIC SETTINGS','Battery_Modules')  # Number of Installed Modules
    
    # General control values for the solar-control-program 
    Cadance = config.getint('GENERAL CONTROL SETTINGS','Cadance')  # Control Loop refresh rate in seconds
    Display = config.getboolean('GENERAL CONTROL SETTINGS','Display') # Enable Terminal SoC Print
    CSV_Log = config.getboolean('GENERAL CONTROL SETTINGS','CSV_Log') # Enable BMS logging into csv
    SQL_Log = config.getboolean('GENERAL CONTROL SETTINGS','SQL_Log') # Enable BMS logging into SQL
    Control = config.getboolean('GENERAL CONTROL SETTINGS','Control')# Enable Inverter Control Loop

    # Specific values for the control loop that enables and disables the inverter.
    SoC_high = config.getint('CONTROL LOOP SPECIFIC SETTINGS','SoC_high')  # Percent
    SoC_low = config.getint('CONTROL LOOP SPECIFIC SETTINGS','SoC_low')  # Percent
    Battery_low = config.getfloat('CONTROL LOOP SPECIFIC SETTINGS','Battery_low')  # Volt
    Battery_hysteresis = config.getfloat('CONTROL LOOP SPECIFIC SETTINGS','Battery_hysteresis')   # Volt
    Default_battery_low = config.getfloat('CONTROL LOOP SPECIFIC SETTINGS','Default_battery_low')  # Volt
    Default_battery_hysteresis = config.getfloat('CONTROL LOOP SPECIFIC SETTINGS','Default_battery_hysteresis')   # Volt

    # Specific variables for the SQL database writer

    SQL_Host = config.get('MySQL SPECIFIC SETTINGS','SQL_Host')  # MySQL server address
    SQL_Auth = config.get('MySQL SPECIFIC SETTINGS','SQL_Auth')  # MySQL authentication method
    SQL_User = config.get('MySQL SPECIFIC SETTINGS','SQL_User')  # MySQl username
    SQL_Password = config.get('MySQL SPECIFIC SETTINGS','SQL_Password')  # MySQl user password
    SQL_Database = config.get('MySQL SPECIFIC SETTINGS','SQL_Database')  # MySQL database


    ################################################################################################################


    print('Current Configuration of Control program \n')
    print('Battery Modules: '+str(Battery_Modules))
    print('Cadance: ' + str(Cadance))
    print('SoC inverter ON: ' + str(SoC_high))
    print('SoC inverter OFF: ' + str(SoC_low))
    print('\n')
    print('Battery Low Voltage: ' + str(Battery_low))
    print('Battery Hysteresis Voltage: '+str(Battery_hysteresis))
    print('\n')
    print('Control- Display:' +str(Display))
    print('Control- CSV Data Log:' + str(CSV_Log))
    print('Control- SQL Data Log:' + str(SQL_Log))
    print('Control- Inv. Ctrl.:' + str(Control))
    print('\n')




    control(Serial_Port=Serial_Port, Modbus_Host=Modbus_Host, Modbus_Address_XW=Modbus_Address_XW, Modbus_Address_MPPT_West=Modbus_Address_MPPT_West,\
         Modbus_Address_MPPT_East=Modbus_Address_MPPT_East, Battery_Modules=Battery_Modules, Cadance=Cadance,\
         Display=Display, CSV_Log=CSV_Log,SQL_Log=SQL_Log, Control=Control, SoC_high=SoC_high, SoC_low=SoC_low,\
         Battery_low=Battery_low, Battery_hysteresis=Battery_hysteresis,Default_battery_low=Default_battery_low,\
         Default_battery_hysteresis=Default_battery_hysteresis, Log_file_path=Log_File_Path,\
         SQL_Host=SQL_Host,SQL_Auth=SQL_Auth, SQL_User=SQL_User,SQL_Password=SQL_Password,SQL_Database=SQL_Database)


if __name__ == '__main__':

    main()


