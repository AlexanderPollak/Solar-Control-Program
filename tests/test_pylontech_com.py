"""Test the embedding pylontech_com module (SCP.pylontech_com).
This module has a class (SCP.pylontech_com.US2000B) that is used to
communicate with the BMS of the Pylontech Batteries. The tests for
this class require the BMS to be connected to serial port of the computer.
"""

import numpy as np
import pytest
import SCP
from  SCP.pylontech_com import *




def test_initialise():
    """Checks if the initialisation of the terminal was
    successful."""

    BMS = US2000B()
    tmp = BMS.initialise()

    # Test for successful initialisation of the connection.
    assert tmp == True

def test_is_connected():
    """Checks if the communication between the computer and the BMS is operational."""

    BMS = US2000B()

    BMS.open()
    tmp = BMS.is_connected()



    # Test for successful initialisation of the connection.
    assert tmp == True


def test_read_SOC():
    """Checks if the software can read out a State of Charge value."""

    BMS = US2000B()

    BMS.open()
    print BMS.read_SOC(1)


def test_log_SOC():
    """Checks if the software can write a State of Charge value into the Logfile."""

    BMS = US2000B()

    BMS.open()
    BMS.log_SoC()

    # Test for successful initialisation of the connection.
    #assert tmp == True





if __name__ == "__main__":

    test_is_connected()