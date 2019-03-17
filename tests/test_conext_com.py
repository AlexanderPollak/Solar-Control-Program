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

    conext = com()

    conext.open()
    tmp = conext.read_firmware()
    print tmp
    conext.close()


    # Test for successful initialisation of the connection.
    #assert tmp == True


def test_is_connected():
    """Checks if the communication between the computer and the BMS is operational."""

    conext = com()

    conext.open()
    tmp_check = conext.is_connected()
    conext.close()

    # Test for successful initialisation of the connection.
    assert tmp_check == True


if __name__ == "__main__":

    #test_read_firmware()
    test_is_connected()