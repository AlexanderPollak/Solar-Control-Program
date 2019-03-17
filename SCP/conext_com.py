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
import numpy
from pyModbusTCP.client import ModbusClient
from pymodbus.payload import BinaryPayloadDecoder

# EMBEDDING conext_com CLASS ----------------------------------------------------

class com(object):
    """This class implements the serial connection functions """
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