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
from pyModbusTCP.client import ModbusClient
from pymodbus.payload import BinaryPayloadDecoder,BinaryPayloadBuilder

# EMBEDDING com CLASS ----------------------------------------------------

class com(object):
    """This class implements the modbusTCP connection functions """
    def __init__(self):
        ''' Constructor for this class. '''
        self.__port = 0


    def __del__(self):
        ''' Destructor for this class. '''
        if self.__port !=0:
            self.close()




    def open (self,SERVER_HOST = "192.168.0.210",SERVER_PORT = 502,SERVER_UNIT = 201):
        """Open modbus connection to the ComBox

        Args:
            SERVER_HOST: network address of the ComBox. Default='192.168.0.210'
            SERVER_PORT: modbus TCP port. Default='502'
            SERVER_UNIT: modbus address of the ComBox. Default='201'

        Returns: Boolean value True or False

        """
        self.__port = ModbusClient(SERVER_HOST,SERVER_PORT,SERVER_UNIT)
        if not self.__port.is_open():
            if not self.__port.open():
                print("unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT))

        return self.__port.is_open()

    def close(self):
        """Closes the modbusTCP connection

        Returns: Boolean value True or False

        """
        self.__port.close()
        return not self.__port.is_open()

    def is_connected(self):
        """This function checks if the connection to the Schneider Conext ComBox is established
        and if it responds to readout commands. It requests the firmware version of the ComBox
        and checks for an received bitstream.

        Returns: Boolean value True or False

        return
        """
        bitstream = self.__port.read_holding_registers(0x001E, 7)  # 0x001E Firmware Version str20 r
        if bitstream:
            return True
        else:
            return False


# EMBEDDING ComBox CLASS ----------------------------------------------------

class ComBox():
    """This class implements functions specific to the Schneider ComBox """
    def __init__(self):
        ''' Constructor for this class. '''
        self.__port = 0


    def __del__(self):
        ''' Destructor for this class. '''
        if self.__port !=0:
            self.close()

    def open (self,SERVER_HOST = "192.168.0.210",SERVER_PORT = 502,SERVER_UNIT = 201):
        """Open modbus connection to the ComBox

        Args:
            SERVER_HOST: network address of the ComBox. Default='192.168.0.210'
            SERVER_PORT: modbus TCP port. Default='502'
            SERVER_UNIT: modbus address of the ComBox. Default='201'

        Returns: Boolean value True or False

        """
        self.__port = ModbusClient(SERVER_HOST,SERVER_PORT,SERVER_UNIT)
        if not self.__port.is_open():
            if not self.__port.open():
                print("unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT))

        return self.__port.is_open()

    def close(self):
        """Closes the modbusTCP connection

        Returns: Boolean value True or False

        """
        self.__port.close()
        return not self.__port.is_open()

    def is_connected(self):
        """This function checks if the connection to the Schneider Conext ComBox is established
        and if it responds to readout commands. It requests the firmware version of the ComBox
        and checks for an received bitstream.

        Returns: Boolean value True or False

        return
        """
        bitstream = self.__port.read_holding_registers(0x001E, 7)  # 0x001E Firmware Version str20 r
        if bitstream:
            return True
        else:
            return False

    def read_firmware(self):
        """This function reads the firmware version of the ComBox and returns it as a string.

        Returns: string {firmware version}

        """
        bitstream = self.__port.read_holding_registers(0x001E, 7)# 0x001E Firmware Version str20 r
        decoder = BinaryPayloadDecoder.fromRegisters(bitstream)
        result = decoder.decode_string(14)
        return result


    def read_Grid_Voltage(self):
        """This function reads the Grid Voltage from the ComBox and returns Volt.

        Returns: float {Grid Voltage in Volt}

        """
        bitstream = self.__port.read_holding_registers(0x004C, 2)# 0x004C Grid Voltage uint32 r
        decoder = BinaryPayloadDecoder.fromRegisters(bitstream)
        result =(decoder.decode_32bit_uint())/1000.0
        return result

    def read_Grid_Frequency(self):
        """This function reads the Grid Frequency from the ComBox and returns it in Hz.

        Returns: float {Grid Frequency in Hz}

        """
        bitstream = self.__port.read_holding_registers(0x004E, 2)# 0x004E Grid Frequency uint32 r
        decoder = BinaryPayloadDecoder.fromRegisters(bitstream)
        result =(decoder.decode_32bit_uint())/100.0
        return result


# EMBEDDING XW CLASS ----------------------------------------------------

class XW():
    """This class implements functions specific to the Schneider ComBox """
    def __init__(self):
        ''' Constructor for this class. '''
        self.__port = 0


    def __del__(self):
        ''' Destructor for this class. '''
        if self.__port !=0:
            self.close()

    def open (self,SERVER_HOST = "192.168.0.210",SERVER_PORT = 502,SERVER_UNIT = 10):
        """Open modbus connection to the ComBox

        Args:
            SERVER_HOST: network address of the ComBox. Default='192.168.0.210'
            SERVER_PORT: modbus TCP port. Default='502'
            SERVER_UNIT: modbus address of the ComBox. Default='201'

        Returns: Boolean value True or False

        """
        self.__port = ModbusClient(SERVER_HOST,SERVER_PORT,SERVER_UNIT)
        if not self.__port.is_open():
            if not self.__port.open():
                print("unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT))

        return self.__port.is_open()

    def close(self):
        """Closes the modbusTCP connection

        Returns: Boolean value True or False

        """
        self.__port.close()
        return not self.__port.is_open()

    def is_connected(self):
        """This function checks if the connection to the Schneider Conext XW+ is established
        and if it responds to readout commands. It requests the firmware version of the XW+
        and checks for an received bitstream.

        Returns: Boolean value True or False

        return
        """
        bitstream = self.__port.read_holding_registers(0x001E, 7)  # 0x001E Firmware Version str20 r
        if bitstream:
            return True
        else:
            return False

    def read_firmware(self):
        """This function reads the firmware version of the XW+ inverter and returns it as a string.

        Returns: string {firmware version}

        """
        bitstream = self.__port.read_holding_registers(0x001E, 7)# 0x001E Firmware Version str20 r
        decoder = BinaryPayloadDecoder.fromRegisters(bitstream)
        result = decoder.decode_string(14)
        return result

    def read_Grid_Voltage(self):
        """This function reads the Grid Voltage from the XW+ inverter and returns Volt.

        Returns: float {Grid Voltage in Volt}

        """
        bitstream = self.__port.read_holding_registers(0x0062, 2)  # 0x0062 Grid Voltage uint32 r
        decoder = BinaryPayloadDecoder.fromRegisters(bitstream)
        result = (decoder.decode_32bit_uint()) / 1000.0
        return result

    def read_Grid_Frequency(self):
        """This function reads the Grid Frequency from the XW+ inverter and returns it in Hz.

        Returns: float {Grid Frequency in Hz}

        """
        bitstream = self.__port.read_holding_registers(0x0061, 1)  # 0x0061 Grid Frequency uint16 r
        decoder = BinaryPayloadDecoder.fromRegisters(bitstream)
        result = (decoder.decode_16bit_uint()) / 100.0
        return result

    def read_Low_Battery_Cut_Out(self):
        """This function reads the Low_Battery_Cut_Out Voltage from the XW+ inverter and returns it in Volt.

        Returns: float {Low Battery Cut Out in Volt}

        """
        bitstream = self.__port.read_holding_registers(0x017C, 2)  # 0x017C Low Battery Cut Out uint32 r/w
        decoder = BinaryPayloadDecoder.fromRegisters(bitstream)
        result = (decoder.decode_32bit_uint()) / 1000.0
        return result

    def read_Low_Battery_Cut_Out_Delay(self):
        """This function reads the Low Battery Cut Out Delay from the XW+ inverter and returns it in Seconds.

        Returns: float {Low Battery Cut Out Delay in Seconds}

        """
        bitstream = self.__port.read_holding_registers(0x017E, 1)  # 0x017E Low Battery Cut Out Delay uint16 r/w
        decoder = BinaryPayloadDecoder.fromRegisters(bitstream)
        result = (decoder.decode_16bit_uint()) / 100.0
        return result

    def read_Inverter_Status(self):
        """This function reads the Inverter Status from the XW+ inverter and returns the status as a string.

        Returns: string {status}

        """
        bitstream = self.__port.read_holding_registers(0x007A, 1)  # 0x007A Inverter Status uint16 r
        decoder = BinaryPayloadDecoder.fromRegisters(bitstream)
        result = (decoder.decode_16bit_uint())
        if result == 1024:
            return str('Invert')
        if result == 1025:
            return str('AC Pass Through')
        if result == 1026:
            return str('APS Only')
        if result == 1027:
            return str('Load Sense')
        if result == 1028:
            return str('Inverter Disabled')
        if result == 1029:
            return str('Load Sense Ready')
        if result == 1030:
            return str('Engaging Inverter')
        if result == 1031:
            return str('Invert Fault')
        if result == 1032:
            return str('Inverter Standby')
        if result == 1033:
            return str('Grid-Tied')
        if result == 1034:
            return str('Grid Support')
        if result == 1035:
            return str('Gen Support')
        if result == 1036:
            return str('Sell-to-Grid')
        if result == 1037:
            return str('Load Shaving')
        if result == 1038:
            return str('Grid Frequency Stabilization')
        else:
            return str('UNKNOWN STATE!')


    def write_Low_Battery_Cut_Out_Delay(self, delay=0.1):
        """This function writes the Low Battery Cut Out Delay to the XW+ inverter and returns the value in the register.

        Returns: float {Low Battery Cut Out Delay in Seconds}

        """
        delay = np.uint16(delay * 100)
        Upper_limit = np.uint16(100 * 60) #upper limit 60 Seconds
        Lower_limit = np.uint16(100 * 1)#Lower limit 1 Seconds
        if delay in range(Lower_limit, Upper_limit):
            self.__port.write_single_register(0x017E,delay)
        else:
            print ('ERROR: delay value out of range!')

        bitstream = self.__port.read_holding_registers(0x017E, 1)  # 0x017E Low Battery Cut Out Delay uint16 r/w
        decoder = BinaryPayloadDecoder.fromRegisters(bitstream)
        result = (decoder.decode_16bit_uint()) / 100.0
        return result

    def write_Low_Battery_Cut_Out(self, voltage=47):
        """This function writes the Low Battery Cut Out to the XW+ inverter and returns the value in the register.

        Returns: float {Low Battery Cut Out in Volt}

        """
        voltage = np.uint32(voltage * 1000)
        Upper_limit = np.uint32(1000 * 49) #upper limit 60 Seconds
        Lower_limit = np.uint32(1000 * 46)#Lower limit 1 Seconds
        if voltage in range(Lower_limit, Upper_limit):
            self.__port.write_multiple_registers(0x017C,[voltage,00000])
        else:
            print ('ERROR: delay value out of range!')

        bitstream = self.__port.read_holding_registers(0x017C, 2)  # 0x017C Low Battery Cut Out uint32 r/w
        decoder = BinaryPayloadDecoder.fromRegisters(bitstream)
        result = (decoder.decode_16bit_uint()) / 1000.0
        return result



    def read_Load_Shave_Status(self):
        """This function reads the Load Shave status from the XW+ inverter and returns the state.

        Returns: str {Load Shave state}

        """
        bitstream = self.__port.read_holding_registers(0x01B2, 1)  # 0x017E Low Battery Cut Out Delay uint16 r/w
        decoder = BinaryPayloadDecoder.fromRegisters(bitstream)
        result = (decoder.decode_16bit_uint())
        if result == 0:
            return str('Disable')
        if result == 1:
            return str('Enable')

    def write_Load_Shave_Status(self, status):
        """This function writes the Load Shave to the XW+ inverter and returns the value in the register.

        Returns: str {Load Shave state}

        """
        if status =='enable'or status == 'Enable' or status == 'ENABLE':
            self.__port.write_single_register(0x01B2, 1)
        if status =='disable'or status == 'Disable' or status == 'DISABLE':
            self.__port.write_single_register(0x01B2, 0)
        else:
            print ('ERROR: Input Parameter must be: "enable" or "disable"')

        bitstream = self.__port.read_holding_registers(0x01B2, 1)  # 0x01B2 Load Shave uint16 r/w
        decoder = BinaryPayloadDecoder.fromRegisters(bitstream)
        result = (decoder.decode_16bit_uint())
        if result == 0:
            return str('Disable')
        if result == 1:
            return str('Enable')
