"""Solar-Control-Software
This software is used to connect to Pylontech US2000B Plus Batteries
and Schneider Conext Devices via serial link and modbusTCP, respectively.
It allows to read and write parameter from and too the connected devices;
the Pylontech US2000B batteries and the Conext; ComBox, MPPT60 150, and XW+ Inverter.
"""

import SCP.pylontech_com
import SCP.conext_com
import serial