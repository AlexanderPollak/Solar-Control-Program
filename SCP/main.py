#START OF MAIN:

import configparser
from SCP.control import *


def main():
    
    config = configparser.ConfigParser()

    config.read('/usr/local/solar-control-program/etc/scp.cfg') # Location of config file


    # Serial_Port = '/dev/ttyUSB0'  # Serial Port for Communication with Pylontech
    # Modbus_Host = '192.168.0.210'  # Modbus Server Address for Communication with Inverter
    # Log_File_Path = '/home/pollak/Solar-Control-Program/Log'

    # Battery_Modules = 6  # Number of Installed Modules
    # Cadance = 30  # Control Loop refresh rate in seconds
    # Display = True  # Enable Terminal SoC Print
    # Log = True  # Enable BMS logging
    # Control = True  # Enable Inverter Control Loop

    # SoC_high = 80  # Percent
    # SoC_low = 40  # Percent
    # Battery_low = 45.5  # Volt
    # Battery_hysteresis = 2.0  # Volt

    Serial_Port = config['COMMUNICATION SETTINGS']['Serial_Port']  # Serial Port for Communication with Pylontech
    Modbus_Host = config['COMMUNICATION SETTINGS']['Modbus_Host']  # Modbus Server Address for Communication with Inverter
    
    Log_File_Path = config['PYLONTECH BATTERY SPECIFIC SETTINGS']['CSV_Log_File_Path']
    Battery_Modules = config['PYLONTECH BATTERY SPECIFIC SETTINGS']['Battery_Modules']  # Number of Installed Modules
    
    Cadance = config['GENERAL CONTROL SETTINGS']['Cadance']  # Control Loop refresh rate in seconds
    Display = config['GENERAL CONTROL SETTINGS']['Display']  # Enable Terminal SoC Print
    Log = config['GENERAL CONTROL SETTINGS']['CSV_Log'] # Enable BMS logging
    Control = config['GENERAL CONTROL SETTINGS']['Control'] # Enable Inverter Control Loop

    SoC_high = config['CONTROL LOOP SPECIFIC SETTINGS']['SoC_high']  # Percent
    SoC_low = config['CONTROL LOOP SPECIFIC SETTINGS']['SoC_low']  # Percent
    Battery_low = config['CONTROL LOOP SPECIFIC SETTINGS']['Battery_low']  # Volt
    Battery_hysteresis = config['CONTROL LOOP SPECIFIC SETTINGS']['Battery_hysteresis']  # Volt






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
    print('Control- Data Log:' + str(Log))
    print('Control- Inv. Ctrl.:' + str(Control))
    print('\n')




    control(Serial_Port=Serial_Port, Modbus_Host=Modbus_Host, Battery_Modules=Battery_Modules, Cadance=Cadance,\
         Display=Display, Log=Log, Control=Control, SoC_high=SoC_high, SoC_low=SoC_low, Battery_low=Battery_low,\
         Battery_hysteresis=Battery_hysteresis, Log_file_path=Log_File_Path)


if __name__ == '__main__':

    main()


