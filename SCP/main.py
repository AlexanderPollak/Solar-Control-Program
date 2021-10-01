#START OF MAIN:

from SCP.control import *

def main():
    Serial_Port = '/dev/ttyUSB0'  # Serial Port for Communication with Pylontech
    Modbus_Host = '192.168.0.210'  # Modbus Server Address for Communication with Inverter
    Log_File_Path = '/home/pollak/Solar-Control-Program/Log'

    Battery_Modules = 6  # Number of Installed Modules
    Cadance = 30  # Control Loop refresh rate in seconds
    Display = True  # Enable Terminal SoC Print
    Log = True  # Enable BMS logging
    Control = True  # Enable Inverter Control Loop

    SoC_high = 80  # Percent
    SoC_low = 40  # Percent
    Battery_low = 45.5  # Volt
    Battery_hysteresis = 2.0  # Volt

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


