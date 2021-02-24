""" This module contains classes and functions to establish a communication with the
 Schneider Conext; ComBox, MPPT60 150, and XW+ Battery Inverter.

**Description:**

    The communication is established over ModbusTCP/IP that is provided by the Schneider ComBox.
    The ComBox is connected via ethernet to the control computer and acts as a media converter
    to the Xanbus, which links the Schneider devices. The communication is implemented using "pymodbusTCP".
    The functions in this module will allow to read and write modbus registers of the Schneider devices,
    thereby allowing it to be controlled remotely. This package includes functions to communicate with following
    devices:
        1. Schneider ComBox
        2. Schneider MPPT60 150
        3. Schneider XW+ 8548E
The main class in this module ("conect_com") allows the user to
communicate with the Schneider devices. Each device then
has its own class which includes the device specific functions.

"""
import numpy as np
import time
from struct import *
from pyModbusTCP.client import ModbusClient

# EMBEDDING com CLASS ----------------------------------------------------

class com(object):
    """This class implements the modbusTCP connection functions """
    def __init__(self):
        ''' Constructor for this class. '''
        self._port = 0


    def __del__(self):
        ''' Destructor for this class. '''
        if self._port !=0:
            self.close()




    def open (self,SERVER_HOST = "192.168.0.210",SERVER_PORT = 502,SERVER_UNIT = 201):
        """Open modbus connection to the ComBox

        Args:
            SERVER_HOST: network address of the ComBox. Default='192.168.0.210'
            SERVER_PORT: modbus TCP port. Default='502'
            SERVER_UNIT: modbus address of the ComBox. Default='201'

        Returns: Boolean value True or False

        """
        self._port = ModbusClient(SERVER_HOST, SERVER_PORT, SERVER_UNIT)
        if not self._port.is_open():
            if not self._port.open():
                print("unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT))

        return self._port.is_open()

    def close(self):
        """Closes the modbusTCP connection

        Returns: Boolean value True or False

        """
        self._port.close()
        return not self._port.is_open()

    def is_connected(self):
        """This function checks if the connection to the Schneider Conext ComBox is established
        and if it responds to readout commands. It requests the firmware version of the ComBox
        and checks for an received bitstream.

        Returns: Boolean value True or False

        return
        """
        bitstream = self._port.read_holding_registers(0x001E, 7)  # 0x001E Firmware Version str20 r
        if bitstream:
            return True
        else:
            return False

    def reconnect(self, SERVER_HOST = "192.168.0.210",SERVER_PORT = 502,SERVER_UNIT = 201):
        """Reconnects communication with modbus client.

        Args:
            SERVER_HOST: network address of the ComBox. Default='192.168.0.210'
            SERVER_PORT: modbus TCP port. Default='502'
            SERVER_UNIT: modbus address of the ComBox. Default='201'

        Returns: Boolean value True or False

        """
        if self._port !=0:
            self.close()
        self.open(SERVER_HOST=SERVER_HOST, SERVER_PORT=SERVER_PORT, SERVER_UNIT=SERVER_UNIT)
        time.sleep(1)
        return self.is_connected()



# EMBEDDING ComBox CLASS ----------------------------------------------------

class ComBox():
    """This class implements functions specific to the Schneider ComBox """
    def __init__(self):
        ''' Constructor for this class. '''
        self._port = 0


    def __del__(self):
        ''' Destructor for this class. '''
        if self._port !=0:
            self.close()

    def open (self,SERVER_HOST = "192.168.0.210",SERVER_PORT = 502,SERVER_UNIT = 201):
        """Open modbus connection to the ComBox

        Args:
            SERVER_HOST: network address of the ComBox. Default='192.168.0.210'
            SERVER_PORT: modbus TCP port. Default='502'
            SERVER_UNIT: modbus address of the ComBox. Default='201'

        Returns: Boolean value True or False

        """
        self._port = ModbusClient(SERVER_HOST, SERVER_PORT, SERVER_UNIT)
        if not self._port.is_open():
            if not self._port.open():
                print("unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT))

        return self._port.is_open()

    def close(self):
        """Closes the modbusTCP connection

        Returns: Boolean value True or False

        """
        self._port.close()
        return not self._port.is_open()

    def is_connected(self):
        """This function checks if the connection to the Schneider Conext ComBox is established
        and if it responds to readout commands. It requests the firmware version of the ComBox
        and checks for an received bitstream.

        Returns: Boolean value True or False

        return
        """
        bitstream = self._port.read_holding_registers(0x001E, 7)  # 0x001E Firmware Version str20 r
        if bitstream:
            return True
        else:
            return False

    def reconnect(self, SERVER_HOST="192.168.0.210", SERVER_PORT=502, SERVER_UNIT=201):
        """Reconnects communication with modbus client.

        Args:
            SERVER_HOST: network address of the ComBox. Default='192.168.0.210'
            SERVER_PORT: modbus TCP port. Default='502'
            SERVER_UNIT: modbus address of the ComBox. Default='201'

        Returns: Boolean value True or False

        """
        if self._port != 0:
            self.close()
        self.open(SERVER_HOST=SERVER_HOST, SERVER_PORT=SERVER_PORT, SERVER_UNIT=SERVER_UNIT)
        time.sleep(1)
        return self.is_connected()

    def read_firmware(self):
        """This function reads the firmware version of the ComBox and returns it as a string.

        Returns: string {firmware version}

        """
        bitstream = self._port.read_holding_registers(0x001E, 7)# 0x001E Firmware Version str14
        result = str(unpack('%ds' % 14, pack('<HHHHHHH', bitstream[0], bitstream[1], bitstream[2], bitstream[3], bitstream[4], bitstream[5], bitstream[6]))[0], 'utf-8')# combines seven 16bit registers into str14
        return result


    def read_Grid_Voltage(self):
        """This function reads the Grid Voltage from the ComBox and returns Volt.

        Returns: float {Grid Voltage in Volt}

        """
        bitstream = self._port.read_holding_registers(0x004C, 2)# 0x004C Grid Voltage uint32 r
        result = unpack('L',pack('<HH',bitstream[0],bitstream[1]))[0]/1000.0 # combines two 16bit registers into uint32
        return result

    def read_Grid_Frequency(self):
        """This function reads the Grid Frequency from the ComBox and returns it in Hz.

        Returns: float {Grid Frequency in Hz}

        """
        bitstream = self._port.read_holding_registers(0x004E, 2)# 0x004E Grid Frequency uint32 r
        result = unpack('L', pack('<HH', bitstream[0], bitstream[1]))[0] / 100.0  # combines two 16bit registers into uint32
        return result


# EMBEDDING XW CLASS ----------------------------------------------------

class XW():
    """This class implements functions specific to the Schneider ComBox """
    def __init__(self):
        ''' Constructor for this class. '''
        self._port = 0


    def __del__(self):
        ''' Destructor for this class. '''
        if self._port !=0:
            self.close()

    def open (self,SERVER_HOST = "192.168.0.210",SERVER_PORT = 502,SERVER_UNIT = 10):
        """Open modbus connection to the ComBox

        Args:
            SERVER_HOST: network address of the ComBox. Default='192.168.0.210'
            SERVER_PORT: modbus TCP port. Default='502'
            SERVER_UNIT: modbus address of the ComBox. Default='201'

        Returns: Boolean value True or False

        """
        self._port = ModbusClient(SERVER_HOST, SERVER_PORT, SERVER_UNIT)
        if not self._port.is_open():
            if not self._port.open():
                print("unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT))

        return self._port.is_open()

    def close(self):
        """Closes the modbusTCP connection

        Returns: Boolean value True or False

        """
        self._port.close()
        return not self._port.is_open()

    def is_connected(self):
        """This function checks if the connection to the Schneider Conext XW+ is established
        and if it responds to readout commands. It requests the firmware version of the XW+
        and checks for an received bitstream.

        Returns: Boolean value True or False

        return
        """
        bitstream = self._port.read_holding_registers(0x001E, 7)  # 0x001E Firmware Version str20 r
        if bitstream:
            return True
        else:
            return False

    def reconnect(self, SERVER_HOST="192.168.0.210", SERVER_PORT=502, SERVER_UNIT=10):
        """Reconnects communication with modbus client.

        Args:
            SERVER_HOST: network address of the ComBox. Default='192.168.0.210'
            SERVER_PORT: modbus TCP port. Default='502'
            SERVER_UNIT: modbus address of the ComBox. Default='201'

        Returns: Boolean value True or False

        """
        if self._port != 0:
            self.close()
        self.open(SERVER_HOST=SERVER_HOST, SERVER_PORT=SERVER_PORT, SERVER_UNIT=SERVER_UNIT)
        time.sleep(1)
        return self.is_connected()

    def read_firmware(self):
        """This function reads the firmware version of the XW+ inverter and returns it as a string.

        Returns: string {firmware version}

        """
        bitstream = self._port.read_holding_registers(0x001E, 7)# 0x001E Firmware Version str14 r
        result = str(unpack('%ds' % 14, pack('<HHHHHHH', bitstream[0], bitstream[1], bitstream[2], bitstream[3], bitstream[4], bitstream[5], bitstream[6]))[0], 'utf-8')  # combines seven 16bit registers into str14
        return result

    def read_Grid_Voltage(self):
        """This function reads the Grid Voltage from the XW+ inverter and returns Volt.

        Returns: float {Grid Voltage in Volt}

        """
        bitstream = self._port.read_holding_registers(0x0062, 2)  # 0x0062 Grid Voltage uint32 r
        result = unpack('L', pack('<HH', bitstream[0], bitstream[1]))[0] / 1000.0  # combines two 16bit registers into uint32
        return result

    def read_Grid_Frequency(self):
        """This function reads the Grid Frequency from the XW+ inverter and returns it in Hz.

        Returns: float {Grid Frequency in Hz}

        """
        bitstream = self._port.read_holding_registers(0x0061, 1)  # 0x0061 Grid Frequency uint16 r
        result = unpack('H', pack('<H', bitstream[0]))[0] / 100.0
        return result

    def read_Low_Battery_Cut_Out(self):
        """This function reads the Low_Battery_Cut_Out Voltage from the XW+ inverter and returns it in Volt.

        Returns: float {Low Battery Cut Out in Volt}

        """
        bitstream = self._port.read_holding_registers(0x017C, 2) # 0x017C Low Battery Cut Out uint32 r/w
        result = unpack('L', pack('<HH', bitstream[0], bitstream[1]))[0] / 1000.0  # combines two 16bit registers into uint32
        return result

    def read_Low_Battery_Cut_Out_Delay(self):
        """This function reads the Low Battery Cut Out Delay from the XW+ inverter and returns it in Seconds.

        Returns: float {Low Battery Cut Out Delay in Seconds}

        """
        bitstream = self._port.read_holding_registers(0x017E, 1)  # 0x017E Low Battery Cut Out Delay uint16 r/w
        result = unpack('H', pack('<H', bitstream[0]))[0] / 100.0
        return result

    def read_Inverter_Status(self):
        """This function reads the Inverter Status from the XW+ inverter and returns the status as a string.

        Returns: string {status}

        """
        bitstream = self._port.read_holding_registers(0x007A, 1) # 0x007A Inverter Status uint16 r
        result = unpack('H', pack('<H', bitstream[0]))[0]
        if result == 1024:
            return str('Invert')
        elif result == 1025:
            return str('AC Pass Through')
        elif result == 1026:
            return str('APS Only')
        elif result == 1027:
            return str('Load Sense')
        elif result == 1028:
            return str('Inverter Disabled')
        elif result == 1029:
            return str('Load Sense Ready')
        elif result == 1030:
            return str('Engaging Inverter')
        elif result == 1031:
            return str('Invert Fault')
        elif result == 1032:
            return str('Inverter Standby')
        elif result == 1033:
            return str('Grid-Tied')
        elif result == 1034:
            return str('Grid Support')
        elif result == 1035:
            return str('Gen Support')
        elif result == 1036:
            return str('Sell-to-Grid')
        elif result == 1037:
            return str('Load Shaving')
        elif result == 1038:
            return str('Grid Frequency Stabilization')
        else:
            return str('UNKNOWN STATE!')

    def read_Grid_Support_Status(self):
        """This function reads the Grid Support status from the XW+ inverter and returns the state.

        Returns: str {Grid Support state}

        """
        bitstream = self._port.read_holding_registers(0x01B3, 1)  # 0x01B3 Grid Support uint16 r
        result = unpack('H', pack('<H', bitstream[0]))[0]
        if result == 0:
            return str('Disable')
        if result == 1:
            return str('Enable')

    def write_Grid_Support_Status(self, status):
        """This function writes the Grid Support to the XW+ inverter and returns the value in the register.

        Returns: str {Grid Support state}

        """
        if status == 'enable' or status == 'Enable' or status == 'ENABLE':
            self._port.write_single_register(0x01B3, 1)
        elif status == 'disable' or status == 'Disable' or status == 'DISABLE':
            self._port.write_single_register(0x01B3, 0)
        else:
            print ('ERROR:Grid Support Input Parameter must be: "enable" or "disable"')

        bitstream = self._port.read_holding_registers(0x01B2, 1)  # 0x01B3 Grid Support uint16 r/w
        result = unpack('H', pack('<H', bitstream[0]))[0]
        if result == 0:
            return str('Disable')
        if result == 1:
            return str('Enable')


    def write_Low_Battery_Cut_Out_Delay(self, delay=0.1):
        """This function writes the Low Battery Cut Out Delay to the XW+ inverter and returns the value in the register.

        Returns: float {Low Battery Cut Out Delay in Seconds}

        """
        delay = np.uint16(delay * 100)
        Upper_limit = np.uint16(100 * 190) #upper limit 60 Seconds
        Lower_limit = np.uint16(100 * 1)#Lower limit 1 Seconds
        if delay in range(Lower_limit, Upper_limit):
            self._port.write_single_register(0x017E, delay)
        else:
            print ('ERROR: Low Battery Delay value out of range!')

        bitstream = self._port.read_holding_registers(0x017E, 1)  # 0x017E Low Battery Cut Out Delay uint16 r/w
        result = unpack('H', pack('<H', bitstream[0]))[0]/100.0
        return result

    def write_Low_Battery_Cut_Out(self, voltage=47):
        """This function writes the Low Battery Cut Out to the XW+ inverter and returns the value in the register.

        Returns: float {Low Battery Cut Out in Volt}

        """
        voltage = np.uint32(voltage * 1000)
        Upper_limit = np.uint32(1000 * 49) #upper limit 60 Seconds
        Lower_limit = np.uint32(1000 * 45)#Lower limit 1 Seconds
        if voltage in range(Lower_limit, Upper_limit):
            self._port.write_multiple_registers(0x017C, [voltage, 00000])
        else:
            print ('ERROR: Low Battery Voltage value out of range!')

        bitstream = self._port.read_holding_registers(0x017C, 2) # 0x017C Low Battery Cut Out uint32 r/w
        result = unpack('L', pack('<HH', bitstream[0], bitstream[1]))[0] / 1000.0  # combines two 16bit registers into uint32
        return result



    def read_Load_Shave_Status(self):
        """This function reads the Load Shave status from the XW+ inverter and returns the state.

        Returns: str {Load Shave state}

        """
        bitstream = self._port.read_holding_registers(0x01B2, 1)  # 0x017E Low Battery Cut Out Delay uint16 r/w
        result = unpack('H', pack('<H', bitstream[0]))[0]
        if result == 0:
            return str('Disable')
        if result == 1:
            return str('Enable')

    def write_Load_Shave_Status(self, status):
        """This function writes the Load Shave to the XW+ inverter and returns the value in the register.

        Returns: str {Load Shave state}

        """
        if status == 'enable' or status == 'Enable' or status == 'ENABLE':
            self._port.write_single_register(0x01B2, 1)
        elif status == 'disable' or status == 'Disable' or status == 'DISABLE':
            self._port.write_single_register(0x01B2, 0)
        else:
            print ('ERROR: Load Shave Input Parameter must be: "enable" or "disable"')

        bitstream = self._port.read_holding_registers(0x01B2, 1)  # 0x01B2 Load Shave uint16 r/w
        result = unpack('H', pack('<H', bitstream[0]))[0]
        if result == 0:
            return str('Disable')
        if result == 1:
            return str('Enable')


    def read_Hysteresis(self):
        """This function reads the Low_Battery_Cut_Out Hysteresis from the XW+ inverter and returns it in Volt.

        Returns: float {Low Battery Cut Out Hysteresis in Volt}

        """

        bitstream = self._port.read_holding_registers(0x01F2, 2)  # 0x017C Low Battery Cut Out Hysteresis uint32 r/w
        result = unpack('L', pack('<HH', bitstream[0], bitstream[1]))[0] / 1000.0  # combines two 16bit registers into uint32
        return result

    def write_Hysteresis(self, voltage=2.3):
        """This function writes the Low Battery Cut Out Hysteresis to the XW+ inverter and returns the value in the register.

        Returns: float {Low Battery Cut Out in Volt}

        """
        voltage = np.uint32(voltage * 1000)
        Upper_limit = np.uint32(1000 * 5) #upper limit 5 Volt
        Lower_limit = np.uint32(1000 * 1)#Lower limit 1 Volt
        if voltage in range(Lower_limit, Upper_limit):
            self._port.write_multiple_registers(0x01F2, [voltage, 00000])
        else:
            print ('ERROR: Hysteresis Voltage value out of range!')

        bitstream = self._port.read_holding_registers(0x01F2, 2)  # 0x017C Low Battery Cut Out Hysteresis uint32 r/w
        result = unpack('L', pack('<HH', bitstream[0], bitstream[1]))[0] / 1000.0  # combines two 16bit registers into uint32
        return result
