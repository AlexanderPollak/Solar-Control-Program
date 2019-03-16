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

    console = US2000B.initialise()

    # Test for successful initialisation of the connection.
    assert console == True


def test_read_SOC():
    """Checks if the initialisation of the terminal was
    successful."""

    BMS = US2000B()

    console =BMS.open()

    print console

    print BMS.read_SOC(1)



    # Test for successful initialisation of the connection.
    assert console == True



if __name__ == "__main__":

    test_initialise()