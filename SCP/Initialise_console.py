# this script initialises the Pylontech console.

import serial
import time

serial_interface='/dev/ttyUSB1'
#serial_interface='/dev/ttyr00'

pylontech = serial.Serial(serial_interface,1200, timeout=0.05)
pylontech = serial.Serial(serial_interface,1200, timeout=0.05)

pylontech.write(str.encode('~20014682C0048520FCC3\r'))

time.sleep(5)

pylontech = serial.Serial(serial_interface,115200, timeout=0.05)

pylontech.write(str.encode('\r\n'))
time.sleep(1)
temp_str = repr(pylontech.read(1000))

print (temp_str== str("b'\\n\\rpylon>\\n\\rpylon>'"))

#print temp_str

pylontech.close()
