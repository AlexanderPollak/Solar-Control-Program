"""Test the embedding conext_com module (SCP.conext_com).
This module has a class (SCP.conext_com.com) that is used to
communicate with the Schneider Conext devices. The tests for
this class require the Schneider Conext devices to be connected
via ethernet.
"""

import numpy as np
import pytest
import SCP
from  SCP.conext_com import *


def test_read_firmware():
    """Checks if the communication between the computer and the BMS is operational."""

    conext = ComBox()

    conext.open()
    tmp = conext.read_firmware()
    print (tmp)
    conext.close()


    # Test for successful initialisation of the connection.
    #assert tmp == True


def test_is_connected():
    """Checks if the communication between the computer and the BMS is operational."""

    conext = ComBox()

    conext.open()
    tmp_check = conext.is_connected()
    conext.close()

#    # Test for successful initialisation of the connection.
#    assert tmp_check == True


def test_read_Grid_Voltage():
    """Reads the Grid Voltage value from the ComBox and XW"""

    combox = ComBox()
    combox.open()
    tmp = combox.read_Grid_Voltage()
    print (tmp)
    combox.close()
#
    xw = XW()
    xw.open()
    tmp = xw.read_Grid_Voltage()
    print (tmp)
    xw.close()


def test_read_Grid_Frequency():
    """Reads the Grid Frequency value from the ComBox and XW"""

    combox = ComBox()
    combox.open()
    tmp = combox.read_Grid_Frequency()
    print (tmp)
    combox.close()

    xw = XW()
    xw.open()
    tmp = xw.read_Grid_Frequency()
    print (tmp)
    xw.close()

def test_read_Low_Battery_Cut_Out():
    """Reads the Low Battery Cut Out Voltage and Delay from the XW+"""

    xw = XW()
    xw.open()
    tmp = xw.read_Low_Battery_Cut_Out_Delay()
    print (tmp)
    xw.close()


def test_read_Inverter_Status():
    """Reads the Low Battery Cut Out Voltage and Delay from the XW+"""

    xw = XW()
    xw.open()
    tmp = xw.read_Inverter_Status()
    print (tmp)
    xw.close()

def test_Low_Battery_Cut_Out_Delay():
    """Reads the Low Battery Cut Out Voltage and Delay from the XW+"""

    xw = XW()
    xw.open()
    tmp = xw.write_Low_Battery_Cut_Out_Delay(180)
    print (tmp)
    xw.close()

def test_write_Low_Battery_Cut_Out():
    """Reads the Low Battery Cut Out Voltage and Delay from the XW+"""

    xw = XW()
    xw.open()
    tmp = xw.read_Low_Battery_Cut_Out()
    print (tmp)
    xw.close()


def test_read_Hysteresis():
    """Reads the Low Battery Cut Out Voltage and Delay from the XW+"""

    xw = XW()
    xw.open()
    tmp = xw.read_Hysteresis()
    print (tmp)
    xw.close()


if __name__ == "__main__":

    #test_read_firmware()
    #test_is_connected()
    #test_read_Grid_Voltage()
    #test_read_Grid_Frequency()
    #test_read_Inverter_Status()
    #test_write_Low_Battery_Cut_Out()
    test_read_Hysteresis()
    #test_Low_Battery_Cut_Out_Delay()