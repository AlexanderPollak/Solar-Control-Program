# This script connects to the Pylontech US2000B Plus
# and read the charge status, voltage, current, and temperature
# it stores the data in a .csv file with the actual date

from  SCP.conext_com import *
from  SCP.pylontech_com import *


def main():

    Serial_Port = '/dev/ttyUSB0'  # Serial Port for Communication with Pylontech
    Modbus_Host = '192.168.0.210'  # Modbus Server Address for Communication with Inverter

    Battery_Modules = 6  # Number of Installed Modules
    Cadance = 10  # Control Loop refresh rate in seconds
    Display = True  # Enable Terminal SoC Print
    Log = True  # Enable BMS logging
    Control = True  # Enable Inverter Control Loop

    SoC_high = 62  # Percent
    SoC_low = 61  # Percent
    Battery_Low = 45.5  # Volt
    Battery_Hysteresis = 2.0  # Volt


    try:

        print('SolarControl:v2 ')

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
        CONEXT = XW()
        CONEXT.open(SERVER_HOST=Modbus_Host)
        time.sleep(1)
        tmp_c = CONEXT.is_connected()
        print('INVERTER Connection Established:' + str(tmp_c))
        # ---------------------------------------------------------------------------#

        # ---------------------------------------------------------------------------#
        if not (tmp_b):  # Stopps program if connection has not been established.
            print ('ERROR: No Connection to BMS!')
            exit()
        if not (tmp_c):  # Stopps program if connection has not been established.
            print ('ERROR: No Connection to INVERTER!')
            exit()
        # ---------------------------------------------------------------------------#





        # ---------------------------------------------------------------------------#
        try:  # Program Loop
            CONEXT.write_Low_Battery_Cut_Out(Battery_Low)
            CONEXT.write_Hysteresis(Battery_Hysteresis)
            while True:
                time.sleep(Cadance)
                if Log:  # Condition to log BMS data into .csv file
                    PYLONTECH.log_BMS(N_MODULES=Battery_Modules)

                if Display:  # Condition to print the SoC in terminal
                    tmp = PYLONTECH.read_SoC(N_MODULES=Battery_Modules)
                    print('A:' + str(tmp[0, 0]) + '\t' + 'B:' + str(tmp[1, 0]) + '\t' + 'C:' + str(tmp[2, 0]) + '\t' + \
                          'D:' + str(tmp[3, 0]) + '\t' + 'E:' + str(tmp[4, 0]) + '\t' + 'F:' + str(tmp[5, 0]) + '\t' + \
                          CONEXT.read_Inverter_Status())

                if Control:  # Condition to Control Inverter Based on SoC
                    Battery_SoC = PYLONTECH.read_SoC(N_MODULES=Battery_Modules)
                    Avg_SoC = sum(Battery_SoC) / Battery_Modules
                    if Avg_SoC >= SoC_high:  # Condition to enable Inverter Grid Support
                        if CONEXT.read_Load_Shave_Status() == 'Disable':
                            CONEXT.write_Load_Shave_Status('Enable')
                            print('Grid Support: ON')
                    if Avg_SoC <= SoC_low:  # Condition to disable Inverter Grid Support
                        if CONEXT.read_Load_Shave_Status() == 'Enable':
                            CONEXT.write_Load_Shave_Status('Disable')
                            print('Grid Support: OFF')







        except KeyboardInterrupt:
            CONEXT.write_Hysteresis(2.5)
            CONEXT.write_Low_Battery_Cut_Out(46.5)
            CONEXT.write_Load_Shave_Status('disable')
            print('interrupted!')
            # ---------------------------------------------------------------------------#







    except KeyboardInterrupt:
        CONEXT.write_Hysteresis(2.5)
        CONEXT.write_Low_Battery_Cut_Out(46.5)
        CONEXT.write_Load_Shave_Status('disable')
        del PYLONTECH
        del CONEXT
    except:
        CONEXT.write_Hysteresis(2.5)
        CONEXT.write_Low_Battery_Cut_Out(46.5)
        CONEXT.write_Load_Shave_Status('disable')
        del PYLONTECH
        del CONEXT


#START OF MAIN:

if __name__ == '__main__':
    main()
