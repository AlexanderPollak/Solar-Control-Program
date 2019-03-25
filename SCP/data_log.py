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

class log():
        """This class implements the serial connection functions """

        def __init__(self):
            ''' Constructor for this class. '''


        def __del__(self):
            ''' Destructor for this class. '''


