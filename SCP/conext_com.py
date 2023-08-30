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
        result = unpack('<L',pack('<HH',bitstream[0],bitstream[1]))[0]/1000.0 # combines two 16bit registers into uint32
        return result

    def read_Grid_Frequency(self):
        """This function reads the Grid Frequency from the ComBox and returns it in Hz.

        Returns: float {Grid Frequency in Hz}

        """
        bitstream = self._port.read_holding_registers(0x004E, 2)# 0x004E Grid Frequency uint32 r
        result = unpack('<L', pack('<HH', bitstream[0], bitstream[1]))[0] / 100.0  # combines two 16bit registers into uint32
        return result


# EMBEDDING XW CLASS ----------------------------------------------------

class XW():
    """This class implements functions specific to the Schneider XW+ 8548E Inverter """
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
            SERVER_UNIT: modbus address of the XW+ Inverter. Default='10'

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
            SERVER_UNIT: modbus address of the XW+ Inverter. Default='10'

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
        return result.rstrip('\x00')

    def read_device_name(self):
        """This function reads the device name of the XW+ inverter and returns it as a string.

        Returns: string {device name}

        """
        bitstream = self._port.read_holding_registers(0x0000, 8)# 0x0000 Device Name str16 r
        result = str(unpack('%ds' % 16, pack('<HHHHHHHH', bitstream[0], bitstream[1], bitstream[2], bitstream[3], bitstream[4], bitstream[5], bitstream[6], bitstream[7]))[0], 'utf-8')  # combines seven 16bit registers into str14
        return result.rstrip('\x00')

    ###################################################################################################
    # Grid AC Read Functions
    ###################################################################################################
    def read_Grid_Voltage(self):
        """This function reads the Grid AC Input Voltage from the XW+ inverter and returns the Voltage in [Volt].

        Returns: float {Grid AC Voltage in Volt}

        """
        bitstream = self._port.read_holding_registers(0x0062, 2)  # 0x0062 Grid Voltage uint32 r
        result = unpack('<L', pack('<HH', bitstream[0], bitstream[1]))[0] / 1000.0  # combines two 16bit registers into uint32
        return result

    def read_Grid_Current(self):
        """This function reads the Grid AC Current from the XW+ inverter and returns the Current in [Ampere].

        Returns: float {Grid AC Current in Ampere}

        """
        bitstream = self._port.read_holding_registers(0x0064, 2)  # 0x0064 Grid AC Current sint32 r
        result = unpack('<l', pack('<HH', bitstream[0], bitstream[1]))[0] / 1000.0  # combines two 16bit registers into sint32
        return result

    def read_Grid_Power(self):
        """This function reads the Grid AC Power from the XW+ inverter and returns the Power in [Watt].

        Returns: float {Grid AC Power in Watt}

        """
        bitstream = self._port.read_holding_registers(0x0066, 2)  # 0x0066 Grid AC Power sint32 r
        result = unpack('<l', pack('<HH', bitstream[0], bitstream[1]))[0] / 1.0  # combines two 16bit registers into sint32
        return result


    def read_Grid_Frequency(self):
        """This function reads the Grid AC Frequency from the XW+ inverter and returns it in Hz.

        Returns: float {Grid AC Frequency in Hz}

        """
        bitstream = self._port.read_holding_registers(0x0061, 1)  # 0x0061 Grid Frequency uint16 r
        result = unpack('<H', pack('<H', bitstream[0]))[0] / 100.0
        return result


    ###################################################################################################
    # Load AC Read Functions
    ###################################################################################################
    def read_Load_Voltage(self):
        """This function reads the Load AC Voltage from the XW+ inverter and returns the Voltage in [Volt].

        Returns: float {Load AC Voltage in Volt}

        """
        bitstream = self._port.read_holding_registers(0x008C, 2)  # 0x008C Load Voltage uint32 r
        result = unpack('<L', pack('<HH', bitstream[0], bitstream[1]))[0] / 1000.0  # combines two 16bit registers into uint32
        return result

    def read_Load_Current(self):
        """This function reads the Load AC Current from the XW+ inverter and returns the Current in [Ampere].

        Returns: float {Load AC Current in Ampere}

        """
        bitstream = self._port.read_holding_registers(0x0096, 2)  # 0x0096 Load AC Current uint32 r
        result = unpack('<L', pack('<HH', bitstream[0], bitstream[1]))[0] / 1000.0  # combines two 16bit registers into uint32
        return result

    def read_Load_Power(self):
        """This function reads the Load AC Power from the XW+ inverter and returns the Power in [Watt].

        Returns: float {Load AC Power in Watt}

        """
        bitstream = self._port.read_holding_registers(0x009A, 2)  # 0x009A Load AC Power uint32 r
        result = unpack('<L', pack('<HH', bitstream[0], bitstream[1]))[0] / 1.0  # combines two 16bit registers into uint32
        return result


    def read_Load_Frequency(self):
        """This function reads the Load AC Frequency from the XW+ inverter and returns it in Hz.

        Returns: float {Load AC Frequency in Hz}

        """
        bitstream = self._port.read_holding_registers(0x0098, 1)  # 0x0098 Load Frequency uint16 r
        result = unpack('<H', pack('<H', bitstream[0]))[0] / 100.0
        return result

    ###################################################################################################
    # Inverter DC Read Functions
    ###################################################################################################
    def read_Inverter_DC_Current(self):
        """This function reads the Inverter DC Current from the XW+ inverter and returns the Current in [Ampere].

        Returns: float {Inverter DC Current in Ampere}

        """
        bitstream = self._port.read_holding_registers(0x0058, 2)  # 0x0058 Invert DC Current uint32 r
        result = unpack('<L', pack('<HH', bitstream[0], bitstream[1]))[0] / 1000.0  # combines two 16bit registers into uint32
        return result

    def read_Inverter_DC_Power(self):
        """This function reads the Inverter DC Power from the XW+ inverter and returns the Power in [Watt].

        Returns: float {Inverter DC Power in Watt}

        """
        bitstream = self._port.read_holding_registers(0x005A, 2)  # 0x005A Invert DC Power uint32 r
        result = unpack('<L', pack('<HH', bitstream[0], bitstream[1]))[0] / 1.0  # combines two 16bit registers into uint32
        return result

    
    ###################################################################################################
    # Inverter Energy Read Functions
    ###################################################################################################
    def read_Energy_Grid_Month(self):
        """This function reads the energy input from the grid in the current month from the XW+ inverter and returns the Energy in [kWh].

        Returns: float {Energy from Grid in kWh}

        """
        bitstream = self._port.read_holding_registers(0x010C, 2)  # 0x010C Grid Input Energy This Month uint32 r
        result = unpack('<L', pack('<HH', bitstream[0], bitstream[1]))[0] / 1000.0  # combines two 16bit registers into uint32
        return result

    def read_Energy_Load_Month(self):
        """This function reads the energy output to the load in the current month from the XW+ inverter and returns the Energy in [kWh].

        Returns: float {Energy to Load in kWh}

        """
        bitstream = self._port.read_holding_registers(0x013C, 2)  # 0x013C Load Output Energy This Month uint32 r
        result = unpack('<L', pack('<HH', bitstream[0], bitstream[1]))[0] / 1000.0  # combines two 16bit registers into uint32
        return result

    def read_Energy_Battery_Month(self):
        """This function reads the energy output from the battery in the current month from the XW+ inverter and returns the Energy in [kWh].

        Returns: float {Energy from Battery in kWh}

        """
        bitstream = self._port.read_holding_registers(0x00DC, 2)  # 0x013C Energy From Battery This Month uint32 r
        result = unpack('<L', pack('<HH', bitstream[0], bitstream[1]))[0] / 1000.0  # combines two 16bit registers into uint32
        return result


    ###################################################################################################
    # Inverter Status, Error, and Warning Flags
    ###################################################################################################
    def read_Inverter_Active_Warning(self):
        """This function reads the Active Warning Flag from the XW+ inverter and returns the warning status as a string.

        Returns: string {Waring Status}

        """
        bitstream = self._port.read_holding_registers(0x004C, 1) # 0x007A Inverter Active Warnings Flag uint16 r
        result = unpack('<H', pack('<H', bitstream[0]))[0]
        if result == 0:
            return str('No Warnings')
        elif result == 1:
            return str('Active Warnings')
        else:
            return str('UNKNOWN STATE!')

    def read_Inverter_Active_Fault(self):
        """This function reads the Active Fault Flag from the XW+ inverter and returns the fault status as a string.

        Returns: string {Fault Status}

        """
        bitstream = self._port.read_holding_registers(0x004B, 1) # 0x007A Inverter Active Faults Flag uint16 r
        result = unpack('<H', pack('<H', bitstream[0]))[0]
        if result == 0:
            return str('No Faults')
        elif result == 1:
            return str('Active Faults')
        else:
            return str('UNKNOWN STATE!')

    def read_Inverter_Status(self):
        """This function reads the Inverter Status from the XW+ inverter and returns the status as a string.

        Returns: string {status}

        """
        bitstream = self._port.read_holding_registers(0x007A, 1) # 0x007A Inverter Status uint16 r
        result = unpack('<H', pack('<H', bitstream[0]))[0]
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


    ###################################################################################################
    # Inverter Battery Related Functions
    ###################################################################################################
    def read_Low_Battery_Cut_Out(self):
        """This function reads the Low_Battery_Cut_Out Voltage from the XW+ inverter and returns it in Volt.

        Returns: float {Low Battery Cut Out in Volt}

        """
        bitstream = self._port.read_holding_registers(0x017C, 2) # 0x017C Low Battery Cut Out uint32 r/w
        result = unpack('<L', pack('<HH', bitstream[0], bitstream[1]))[0] / 1000.0  # combines two 16bit registers into uint32
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
        result = unpack('<L', pack('<HH', bitstream[0], bitstream[1]))[0] / 1000.0  # combines two 16bit registers into uint32
        return result


    def read_Low_Battery_Cut_Out_Delay(self):
        """This function reads the Low Battery Cut Out Delay from the XW+ inverter and returns it in Seconds.

        Returns: float {Low Battery Cut Out Delay in Seconds}

        """
        bitstream = self._port.read_holding_registers(0x017E, 1)  # 0x017E Low Battery Cut Out Delay uint16 r/w
        result = unpack('<H', pack('<H', bitstream[0]))[0] / 100.0
        return result

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
        result = unpack('<H', pack('<H', bitstream[0]))[0]/100.0
        return result    


    def read_Hysteresis(self):
        """This function reads the Low_Battery_Cut_Out Hysteresis from the XW+ inverter and returns it in Volt.

        Returns: float {Low Battery Cut Out Hysteresis in Volt}

        """

        bitstream = self._port.read_holding_registers(0x01F2, 2)  # 0x017C Low Battery Cut Out Hysteresis uint32 r/w
        result = unpack('<L', pack('<HH', bitstream[0], bitstream[1]))[0] / 1000.0  # combines two 16bit registers into uint32
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
        result = unpack('<L', pack('<HH', bitstream[0], bitstream[1]))[0] / 1000.0  # combines two 16bit registers into uint32
        return result


    ###################################################################################################
    # Inverter Control Functions
    ###################################################################################################
    def read_Grid_Support_Status(self):
        """This function reads the Grid Support status from the XW+ inverter and returns the state.

        Returns: str {Grid Support state}

        """
        bitstream = self._port.read_holding_registers(0x01B3, 1)  # 0x01B3 Grid Support uint16 r
        result = unpack('<H', pack('<H', bitstream[0]))[0]
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
        result = unpack('<H', pack('<H', bitstream[0]))[0]
        if result == 0:
            return str('Disable')
        if result == 1:
            return str('Enable')


    def read_Load_Shave_Status(self):
        """This function reads the Load Shave status from the XW+ inverter and returns the state.

        Returns: str {Load Shave state}

        """
        bitstream = self._port.read_holding_registers(0x01B2, 1)  # 0x017E Low Battery Cut Out Delay uint16 r/w
        result = unpack('<H', pack('<H', bitstream[0]))[0]
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
        result = unpack('<H', pack('<H', bitstream[0]))[0]
        if result == 0:
            return str('Disable')
        if result == 1:
            return str('Enable')

    ###################################################################################################
    # Inverter Read All for SQL Query
    ###################################################################################################


    def read_Inverter_All(self):
        """This function reads all inverter XW+ specific values and returns a list with the aquired values.

        Args:
            NONE

        Returns: XW_list: list of length [1] containing:
            [inverter, grid_voltage, grid_current, grid_power, grid_frequency, load_voltage, load_current, load_power, load_frequency,
            inverter_dc_current, inverter_dc_power, energy_grid_month, energy_load_month, energy_battery_month, battery_low_voltage,
            battery_low_voltage_delay, battery_hysteresis, inverter_status, inverter_active_warnings_status, inverter_active_faults_status,
            inverter_grid_support_status, inverter_load_shave_status]
            dtype=float and dtype=str.


        """
        XW_list = [[0 for i in range(22)] for j in range(1)]

            
        XW_list[0][0] = self.read_device_name()
        XW_list[0][1] = self.read_Grid_Voltage()
        XW_list[0][2] = self.read_Grid_Current()
        XW_list[0][3] = self.read_Grid_Power()
        XW_list[0][4] = self.read_Grid_Frequency()
        XW_list[0][5] = self.read_Load_Voltage()
        XW_list[0][6] = self.read_Load_Current()
        XW_list[0][7] = self.read_Load_Power()
        XW_list[0][8] = self.read_Load_Frequency()
        XW_list[0][9] = self.read_Inverter_DC_Current()
        XW_list[0][10] = self.read_Inverter_DC_Power()
        XW_list[0][11] = self.read_Energy_Grid_Month()
        XW_list[0][12] = self.read_Energy_Load_Month()
        XW_list[0][13] = self.read_Energy_Battery_Month()
        XW_list[0][14] = self.read_Low_Battery_Cut_Out()
        XW_list[0][15] = self.read_Low_Battery_Cut_Out_Delay()
        XW_list[0][16] = self.read_Hysteresis()
        XW_list[0][17] = self.read_Inverter_Status()
        XW_list[0][18] = self.read_Inverter_Active_Warning()
        XW_list[0][19] = self.read_Inverter_Active_Fault()
        XW_list[0][20] = self.read_Grid_Support_Status()
        XW_list[0][21] = self.read_Load_Shave_Status()

        return XW_list





# EMBEDDING MPPT 60 150 CLASS ----------------------------------------------------

class MPPT60():
    """This class implements functions specific to the Schneider MPPT 60 150 Charge Controller"""
    def __init__(self):
        ''' Constructor for this class. '''
        self._port = 0


    def __del__(self):
        ''' Destructor for this class. '''
        if self._port !=0:
            self.close()

    def open (self,SERVER_HOST = "192.168.0.210",SERVER_PORT = 502,SERVER_UNIT = 30):
        """Open modbus connection to the MPPT 60 150

        Args:
            SERVER_HOST: network address of the ComBox. Default='192.168.0.210'
            SERVER_PORT: modbus TCP port. Default='502'
            SERVER_UNIT: modbus address of the MPPT 60 150 Charge Controller. Default='30'

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
        """This function checks if the connection to the Schneider Conext MPPT 60 150 is established
        and if it responds to readout commands. It requests the firmware version of the device
        and checks for an received bitstream.

        Returns: Boolean value True or False

        return
        """
        bitstream = self._port.read_holding_registers(0x001E, 7)  # 0x001E Firmware Version str20 r
        if bitstream:
            return True
        else:
            return False

    def reconnect(self, SERVER_HOST="192.168.0.210", SERVER_PORT=502, SERVER_UNIT=30):
        """Reconnects communication with modbus client.

        Args:
            SERVER_HOST: network address of the ComBox. Default='192.168.0.210'
            SERVER_PORT: modbus TCP port. Default='502'
            SERVER_UNIT: modbus address of the MPPT 60 150 Charge Controller. Default='30'

        Returns: Boolean value True or False

        """
        if self._port != 0:
            self.close()
        self.open(SERVER_HOST=SERVER_HOST, SERVER_PORT=SERVER_PORT, SERVER_UNIT=SERVER_UNIT)
        time.sleep(1)
        return self.is_connected()

    def read_firmware(self):
        """This function reads the firmware version of the MPPT 60 150 Charge Controller and returns it as a string.

        Returns: string {firmware version}

        """
        bitstream = self._port.read_holding_registers(0x001E, 7)# 0x001E Firmware Version str14 r
        result = str(unpack('%ds' % 14, pack('<HHHHHHH', bitstream[0], bitstream[1], bitstream[2], bitstream[3], bitstream[4], bitstream[5], bitstream[6]))[0], 'utf-8')  # combines seven 16bit registers into str14
        return result.rstrip('\x00')

    def read_device_name(self):
        """This function reads the device name of the MPPT 60 150 Charge Controller and returns it as a string.

        Returns: string {device name}

        """
        bitstream = self._port.read_holding_registers(0x0000, 8)# 0x0000 Device Name str16 rw
        result = str(unpack('%ds' % 16, pack('<HHHHHHHH', bitstream[0], bitstream[1], bitstream[2], bitstream[3], bitstream[4], bitstream[5], bitstream[6], bitstream[7]))[0], 'utf-8')  # combines eight 16bit registers into str16
        return result.rstrip('\x00')

    ###################################################################################################
    # MPPT Energy Read Functions
    ###################################################################################################
    def read_Energy_PV_Day(self):
        """This function reads the energy input from the PV in the current day from the MPPT 60 150 Charge Controller and returns the Energy in [kWh].

        Returns: float {Energy from PV in kWh}

        """
        bitstream = self._port.read_holding_registers(0x006A, 2)  # 0x006A Energy from PV this day uint32 r
        result = unpack('<L', pack('<HH', bitstream[0], bitstream[1]))[0] / 1000.0  # combines two 16bit registers into uint32
        return result

    def read_Energy_PV_Week(self):
        """This function reads the energy input from the PV in the current week from the MPPT 60 150 Charge Controller and returns the Energy in [kWh].

        Returns: float {Energy from PV in kWh}

        """
        bitstream = self._port.read_holding_registers(0x006E, 2)  # 0x006E Energy from PV this week uint32 r
        result = unpack('<L', pack('<HH', bitstream[0], bitstream[1]))[0] / 1000.0  # combines two 16bit registers into uint32
        return result

    def read_Energy_PV_Month(self):
        """This function reads the energy input from the PV in the current month from the MPPT 60 150 Charge Controller and returns the Energy in [kWh].

        Returns: float {Energy from PV in kWh}

        """
        bitstream = self._port.read_holding_registers(0x0072, 2)  # 0x0072 Energy from PV this Month uint32 r
        result = unpack('<L', pack('<HH', bitstream[0], bitstream[1]))[0] / 1000.0  # combines two 16bit registers into uint32
        return result

    def read_Energy_PV_Year(self):
        """This function reads the energy input from the PV in the current year from the MPPT 60 150 Charge Controller and returns the Energy in [kWh].

        Returns: float {Energy from PV in kWh}

        """
        bitstream = self._port.read_holding_registers(0x0076, 2)  # 0x0076 Energy from PV this Year uint32 r
        result = unpack('<L', pack('<HH', bitstream[0], bitstream[1]))[0] / 1000.0  # combines two 16bit registers into uint32
        return result


    ###################################################################################################
    # MPPT DC Input Read Functions
    ###################################################################################################
    def read_DC_Input_Voltage(self):
        """This function reads the MPPT DC Input Voltage and returns the value in [Volt].

        Returns: float {MPPP DC Input Voltage in Volt}

        """
        bitstream = self._port.read_holding_registers(0x004C, 2)  # 0x004C Input DC Voltage uint32 r
        result = unpack('<L', pack('<HH', bitstream[0], bitstream[1]))[0] / 1000.0  # combines two 16bit registers into uint32
        return result

    def read_DC_Input_Current(self):
        """This function reads the MPPT DC Input Current and returns the value in [Ampere].

        Returns: float {MPPT DC Input Current in Ampere}

        """
        bitstream = self._port.read_holding_registers(0x004E, 2)  # 0x004E Input DC Current uint32 r
        result = unpack('<L', pack('<HH', bitstream[0], bitstream[1]))[0] / 1000.0  # combines two 16bit registers into uint32
        return result

    def read_DC_Input_Power(self):
        """This function reads the MPPT DC Input Power and returns the value in [Watt].

        Returns: float {MPPT DC Input Power in Watt}

        """
        bitstream = self._port.read_holding_registers(0x0050, 2)  # 0x0050 Input DC Power uint32 r
        result = unpack('<L', pack('<HH', bitstream[0], bitstream[1]))[0] / 1.0  # combines two 16bit registers into uint32
        return result

    ###################################################################################################
    # MPPT DC Output Read Functions
    ###################################################################################################
    def read_DC_Output_Voltage(self):
        """This function reads the MPPT DC Output Voltage and returns the value in [Volt].

        Returns: float {MPPP DC Output Voltage in Volt}

        """
        bitstream = self._port.read_holding_registers(0x0058, 2)  # 0x0058 Output DC Voltage sint32 r
        result = unpack('<l', pack('<HH', bitstream[0], bitstream[1]))[0] / 1000.0  # combines two 16bit registers into sint32
        return result

    def read_DC_Output_Current(self):
        """This function reads the MPPT DC Output Current and returns the value in [Ampere].

        Returns: float {MPPT DC Output Current in Ampere}

        """
        bitstream = self._port.read_holding_registers(0x005A, 2)  # 0x005A Output DC Current sint32 r
        result = unpack('<l', pack('<HH', bitstream[0], bitstream[1]))[0] / 1000.0  # combines two 16bit registers into sint32
        return result

    def read_DC_Output_Power(self):
        """This function reads the MPPT DC Output Power and returns the value in [Watt].

        Returns: float {MPPT DC Output Power in Watt}

        """
        bitstream = self._port.read_holding_registers(0x005C, 2)  # 0x005C Output DC Power uint32 r
        result = unpack('<L', pack('<HH', bitstream[0], bitstream[1]))[0] / 1.0  # combines two 16bit registers into uint32
        return result

    def read_DC_Output_Power_Percentage(self):
        """This function reads the MPPT DC Output Power Percentage and returns the value in [%].

        Returns: float {MPPT DC Output Power Percentage in %}

        """
        bitstream = self._port.read_holding_registers(0x005E, 2)  # 0x005E Output DC Power Percentage uint16 r
        result = unpack('<H', pack('<H', bitstream[0]))[0] / 1.0  # unpacks the 16bit bitstream into uint16
        return result

    ###################################################################################################
    # MPPT Status, Error, and Warning Flags
    ###################################################################################################
    def read_MPPT_Active_Warning(self):
        """This function reads the Active Warning Flag from the MPPT 60 150 Charge Controller and returns the warning status as a string.

        Returns: string {Waring Status}

        """
        bitstream = self._port.read_holding_registers(0x0045, 1) # 0x0045 Active Warnings Flag uint16 r
        result = unpack('<H', pack('<H', bitstream[0]))[0]
        if result == 0:
            return str('No Warnings')
        elif result == 1:
            return str('Active Warnings')
        else:
            return str('UNKNOWN STATE!')

    def read_MPPT_Active_Fault(self):
        """This function reads the Active Fault Flag from the MPPT 60 150 Charge Controller and returns the fault status as a string.

        Returns: string {Fault Status}

        """
        bitstream = self._port.read_holding_registers(0x0044, 1) # 0x0044 Active Faults Flag uint16 r
        result = unpack('<H', pack('<H', bitstream[0]))[0]
        if result == 0:
            return str('No Faults')
        elif result == 1:
            return str('Active Faults')
        else:
            return str('UNKNOWN STATE!')

    def read_MPPT_Status(self):
        """This function reads the MPPT 60 150 Charge Controller Status and returns the status as a string.

        Returns: string {status}

        """
        bitstream = self._port.read_holding_registers(0x0040, 1) # 0x0040 Device Status uint16 r
        result = unpack('<H', pack('<H', bitstream[0]))[0]
        if result == 0:
            return str('Hibernate')
        elif result == 1:
            return str('Power Save')
        elif result == 2:
            return str('Safe Mode')
        elif result == 3:
            return str('Operating')
        elif result == 4:
            return str('Diagnostic Mode')
        elif result == 5:
            return str('Remote Power Off')
        elif result == 255:
            return str('Data Not Available')
        else:
            return str('UNKNOWN STATE!')

    def read_MPPT_Charger_Status(self):
        """This function reads the MPPT 60 150 Charge Controller Charger Status and returns the status as a string.

        Returns: string {status}

        """
        bitstream = self._port.read_holding_registers(0x0049, 1) # 0x0049 Charger Status uint16 r
        result = unpack('<H', pack('<H', bitstream[0]))[0]
        if result == 768:
            return str('Not Charging')
        elif result == 769:
            return str('Bulk')
        elif result == 770:
            return str('Absorption')
        elif result == 771:
            return str('Overcharge')
        elif result == 772:
            return str('Equalize')
        elif result == 773:
            return str('Float')
        elif result == 774:
            return str('No Float')
        elif result == 775:
            return str('Constant VI')
        elif result == 776:
            return str('Charger Disabled')
        elif result == 777:
            return str('Qualifying AC')
        elif result == 778:
            return str('Qualifying APS')
        elif result == 779:
            return str('Engaging Charger')
        elif result == 780:
            return str('Charge Fault')
        elif result == 781:
            return str('Charger Suspend')
        elif result == 782:
            return str('AC Good')
        elif result == 783:
            return str('APS Good')
        elif result == 784:
            return str('AC Fault')
        elif result == 785:
            return str('Charge')
        elif result == 786:
            return str('Absorption Exit Pending')
        elif result == 787:
            return str('Ground Fault')
        elif result == 788:
            return str('AC Good Pending')
        else:
            return str('UNKNOWN STATE!')


    ###################################################################################################
    # MPPT Read All for SQL Query
    ###################################################################################################


    def read_MPPT_All(self):
        """This function reads all inverter XW+ specific values and returns a list with the aquired values.

        Args:
            NONE

        Returns: MPPT_list: list of length [1] containing:
            [device_name,dc_input_voltage,dc_input_current,dc_input_power,dc_output_voltage,dc_output_current,dc_output_power,
            dc_output_power_percentage,energy_pv_day,energy_pv_week,energy_pv_month,energy_pv_year,mppt_status,
            mppt_charger_status,mppt_active_warnings_status,mppt_active_faults_status]
            dtype=float and dtype=str.


        """
        MPPT_list = [[0 for i in range(16)] for j in range(1)]
            
        MPPT_list[0][0] = self.read_device_name()
        MPPT_list[0][1] = self.read_DC_Input_Voltage()
        MPPT_list[0][2] = self.read_DC_Input_Current()
        MPPT_list[0][3] = self.read_DC_Input_Power()
        MPPT_list[0][4] = self.read_DC_Output_Voltage()
        MPPT_list[0][5] = self.read_DC_Output_Current()
        MPPT_list[0][6] = self.read_DC_Output_Power()
        MPPT_list[0][7] = self.read_DC_Output_Power_Percentage()
        MPPT_list[0][8] = self.read_Energy_PV_Day()
        MPPT_list[0][9] = self.read_Energy_PV_Week()
        MPPT_list[0][10] = self.read_Energy_PV_Month()
        MPPT_list[0][11] = self.read_Energy_PV_Year()
        MPPT_list[0][12] = self.read_MPPT_Status()
        MPPT_list[0][13] = self.read_MPPT_Charger_Status()
        MPPT_list[0][14] = self.read_MPPT_Active_Warning()
        MPPT_list[0][15] = self.read_MPPT_Active_Fault()
    
        return MPPT_list







