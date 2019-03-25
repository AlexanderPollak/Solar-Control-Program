"""Test the embedding conext_com module (SCP.conext_com).
This module has a class (SCP.conext_com.com) that is used to
communicate with the Schneider Conext devices. The tests for
this class require the Schneider Conext devices to be connected
via ethernet.
"""

import numpy as np
import pytest
import SCP
from  SCP.data_log import *




def test_log_BMS():
    """Reads the Low Battery Cut Out Voltage and Delay from the XW+"""

    BMS = Log()
    BMS.log_BMS()



if __name__ == "__main__":

    #test_read_firmware()
    #test_is_connected()
    #test_read_Grid_Voltage()
    #test_read_Grid_Frequency()
    #test_read_Inverter_Status()
    #test_write_Low_Battery_Cut_Out()
    test_log_BMS()