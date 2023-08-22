""" This module contains classes and functions to write Pylontech battery,
Schneider XW+ 8548E, and Schneider MPPT60 150 data into a mysql data base.  

**Description:**

    This module contains a description for each table in the data base and the implementation two write 
    data into the specific tables. It requires a valid username, password, hostaddress, and database.
    This package includes functions to write aquired data from the following devices:
        1. Pylontech US2000B Battery
        2. Schneider MPPT60 150
        3. Schneider XW+ 8548E

The main class in this module ("mysql_com") allows the user to
communicate with the mysql database. Each device then
has its own class which includes the device specific table and functions.

"""
import numpy as np
import datetime
from struct import *
import mysql.connector
#import logging


# EMBEDDING Pylontech CLASS ----------------------------------------------------

class MySQL_com():
    """This class implements functions specific to the Pylontech US2000B Battery"""
    def __init__(self):
        ''' Constructor for this class. '''
        self._port = 0


    def __del__(self):
        ''' Destructor for this class. '''
        if self._port !=0:
            self.close()

    def open (self,HOST='localhost',USER ='grafanauser',PASSWORD='Mars2020',DATABASE='scpdata',AUTH_PLUGIN='mysql_native_password'):
        """Establishing the connection to the mqsql database

        Args:
            HOST: network address of the server hosting the mysql database. Default='localhost'
            USER: mysql database user login for specified database. Default='grafanauser'
            PASSWORD: mysql database user password for specified user. Default='Mars2020'
            DATABASE: specifies the mysql database. Default='scpdata'
            AUTH_PLUGIN: specifies the login method to the mysql server. Default='mysql_native_password'

        Returns: Boolean value True or False

        """
        self._port = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE, auth_plugin=AUTH_PLUGIN)
        if not self._port.is_connected():
            print("Unable to connect to " + str(HOST))

        return self._port.is_connected()

    def close(self):
        """Closes the connection to the MySQL server

        Returns: Boolean value True or False

        """
        self._port.close()
        return not self._port.is_connected()

    def is_connected(self):
        """This function checks if the connection to the MySQL server is established.


        Returns: Boolean value True or False

        """
        return self._port.is_connected()




    def write_BMS(self,BMS_LIST):
        """This function writes the parsed data into the mysql database table for pylontech_bms and returns a boolean value
        if the write process was sucessful.

        Args:
            BMS_LIST: list of length [n_modules] containing:
            [SoC, Voltage, Current, Temperature, Battery Status, Voltage Status, Current Status, Temperature Status] dtype=float64 and dtype=str.


        DROP TABLE IF EXISTS `pylontech_bms`;
        CREATE TABLE `pylontech_bms` (
            `ts` datetime NOT NULL,
            `battery` varchar(16) DEFAULT (NULL),
            `soc` float DEFAULT (NULL),
            `voltage` float DEFAULT (NULL),
            `current` float DEFAULT (NULL),
            `temperature` float DEFAULT (NULL),
            `b_status` varchar(16) DEFAULT (NULL),
            `v_status` varchar(16) DEFAULT (NULL),
            `c_status` varchar(16) DEFAULT (NULL),
            `t_status` varchar(16) DEFAULT (NULL),
            PRIMARY KEY (`ts`,`battery`),
            KEY `idx` (`battery`,`ts`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
    

        Returns: Boolean value True or False

        """
        tmp_n_modules = len(BMS_LIST)
        tmp_time ="{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day,datetime.datetime.now().hour,datetime.datetime.now().minute,datetime.datetime.now().second)

        cursor = self._port.cursor()
        
        tmp_BMS = BMS_LIST

        # Preparing SQL query to INSERT a record into the database.
        if tmp_n_modules == 1:
            tmp_sql = "INSERT INTO pylontech_bms (ts,battery,soc,voltage,current,temperature,b_status,v_status,c_status,t_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            tmp_val = [(tmp_time,'Battery: 1',tmp_BMS[0][0],tmp_BMS[0][1],tmp_BMS[0][2],tmp_BMS[0][3],tmp_BMS[0][4],tmp_BMS[0][5],tmp_BMS[0][6],tmp_BMS[0][7])]

        elif tmp_n_modules == 2:
            tmp_sql = "INSERT INTO pylontech_bms (ts,battery,soc,voltage,current,temperature,b_status,v_status,c_status,t_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            tmp_val = [ (tmp_time,'Battery: 1',tmp_BMS[0][0],tmp_BMS[0][1],tmp_BMS[0][2],tmp_BMS[0][3],tmp_BMS[0][4],tmp_BMS[0][5],tmp_BMS[0][6],tmp_BMS[0][7]),\
                        (tmp_time,'Battery: 2',tmp_BMS[1][0],tmp_BMS[1][1],tmp_BMS[1][2],tmp_BMS[1][3],tmp_BMS[1][4],tmp_BMS[1][5],tmp_BMS[1][6],tmp_BMS[1][7])]
        
        elif tmp_n_modules == 3:
            tmp_sql = "INSERT INTO pylontech_bms (ts,battery,soc,voltage,current,temperature,b_status,v_status,c_status,t_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            tmp_val = [ (tmp_time,'Battery: 1',tmp_BMS[0][0],tmp_BMS[0][1],tmp_BMS[0][2],tmp_BMS[0][3],tmp_BMS[0][4],tmp_BMS[0][5],tmp_BMS[0][6],tmp_BMS[0][7]),\
                        (tmp_time,'Battery: 2',tmp_BMS[1][0],tmp_BMS[1][1],tmp_BMS[1][2],tmp_BMS[1][3],tmp_BMS[1][4],tmp_BMS[1][5],tmp_BMS[1][6],tmp_BMS[1][7]),\
                        (tmp_time,'Battery: 3',tmp_BMS[2][0],tmp_BMS[2][1],tmp_BMS[2][2],tmp_BMS[2][3],tmp_BMS[2][4],tmp_BMS[2][5],tmp_BMS[2][6],tmp_BMS[2][7])]

        elif tmp_n_modules == 4:
            tmp_sql = "INSERT INTO pylontech_bms (ts,battery,soc,voltage,current,temperature,b_status,v_status,c_status,t_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            tmp_val = [ (tmp_time,'Battery: 1',tmp_BMS[0][0],tmp_BMS[0][1],tmp_BMS[0][2],tmp_BMS[0][3],tmp_BMS[0][4],tmp_BMS[0][5],tmp_BMS[0][6],tmp_BMS[0][7]),\
                        (tmp_time,'Battery: 2',tmp_BMS[1][0],tmp_BMS[1][1],tmp_BMS[1][2],tmp_BMS[1][3],tmp_BMS[1][4],tmp_BMS[1][5],tmp_BMS[1][6],tmp_BMS[1][7]),\
                        (tmp_time,'Battery: 3',tmp_BMS[2][0],tmp_BMS[2][1],tmp_BMS[2][2],tmp_BMS[2][3],tmp_BMS[2][4],tmp_BMS[2][5],tmp_BMS[2][6],tmp_BMS[2][7]),\
                        (tmp_time,'Battery: 4',tmp_BMS[3][0],tmp_BMS[3][1],tmp_BMS[3][2],tmp_BMS[3][3],tmp_BMS[3][4],tmp_BMS[3][5],tmp_BMS[3][6],tmp_BMS[3][7])]

        elif tmp_n_modules == 5:
            tmp_sql = "INSERT INTO pylontech_bms (ts,battery,soc,voltage,current,temperature,b_status,v_status,c_status,t_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            tmp_val = [ (tmp_time,'Battery: 1',tmp_BMS[0][0],tmp_BMS[0][1],tmp_BMS[0][2],tmp_BMS[0][3],tmp_BMS[0][4],tmp_BMS[0][5],tmp_BMS[0][6],tmp_BMS[0][7]),\
                        (tmp_time,'Battery: 2',tmp_BMS[1][0],tmp_BMS[1][1],tmp_BMS[1][2],tmp_BMS[1][3],tmp_BMS[1][4],tmp_BMS[1][5],tmp_BMS[1][6],tmp_BMS[1][7]),\
                        (tmp_time,'Battery: 3',tmp_BMS[2][0],tmp_BMS[2][1],tmp_BMS[2][2],tmp_BMS[2][3],tmp_BMS[2][4],tmp_BMS[2][5],tmp_BMS[2][6],tmp_BMS[2][7]),\
                        (tmp_time,'Battery: 4',tmp_BMS[3][0],tmp_BMS[3][1],tmp_BMS[3][2],tmp_BMS[3][3],tmp_BMS[3][4],tmp_BMS[3][5],tmp_BMS[3][6],tmp_BMS[3][7]),\
                        (tmp_time,'Battery: 5',tmp_BMS[4][0],tmp_BMS[4][1],tmp_BMS[4][2],tmp_BMS[4][3],tmp_BMS[4][4],tmp_BMS[4][5],tmp_BMS[4][6],tmp_BMS[4][7])]

        elif tmp_n_modules == 6:
            tmp_sql = "INSERT INTO pylontech_bms (ts,battery,soc,voltage,current,temperature,b_status,v_status,c_status,t_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            tmp_val = [ (tmp_time,'Battery: 1',tmp_BMS[0][0],tmp_BMS[0][1],tmp_BMS[0][2],tmp_BMS[0][3],tmp_BMS[0][4],tmp_BMS[0][5],tmp_BMS[0][6],tmp_BMS[0][7]),\
                        (tmp_time,'Battery: 2',tmp_BMS[1][0],tmp_BMS[1][1],tmp_BMS[1][2],tmp_BMS[1][3],tmp_BMS[1][4],tmp_BMS[1][5],tmp_BMS[1][6],tmp_BMS[1][7]),\
                        (tmp_time,'Battery: 3',tmp_BMS[2][0],tmp_BMS[2][1],tmp_BMS[2][2],tmp_BMS[2][3],tmp_BMS[2][4],tmp_BMS[2][5],tmp_BMS[2][6],tmp_BMS[2][7]),\
                        (tmp_time,'Battery: 4',tmp_BMS[3][0],tmp_BMS[3][1],tmp_BMS[3][2],tmp_BMS[3][3],tmp_BMS[3][4],tmp_BMS[3][5],tmp_BMS[3][6],tmp_BMS[3][7]),\
                        (tmp_time,'Battery: 5',tmp_BMS[4][0],tmp_BMS[4][1],tmp_BMS[4][2],tmp_BMS[4][3],tmp_BMS[4][4],tmp_BMS[4][5],tmp_BMS[4][6],tmp_BMS[4][7]),\
                        (tmp_time,'Battery: 6',tmp_BMS[5][0],tmp_BMS[5][1],tmp_BMS[5][2],tmp_BMS[5][3],tmp_BMS[5][4],tmp_BMS[5][5],tmp_BMS[5][6],tmp_BMS[5][7])]

        elif tmp_n_modules == 7:
            tmp_sql = "INSERT INTO pylontech_bms (ts,battery,soc,voltage,current,temperature,b_status,v_status,c_status,t_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            tmp_val = [ (tmp_time,'Battery: 1',tmp_BMS[0][0],tmp_BMS[0][1],tmp_BMS[0][2],tmp_BMS[0][3],tmp_BMS[0][4],tmp_BMS[0][5],tmp_BMS[0][6],tmp_BMS[0][7]),\
                        (tmp_time,'Battery: 2',tmp_BMS[1][0],tmp_BMS[1][1],tmp_BMS[1][2],tmp_BMS[1][3],tmp_BMS[1][4],tmp_BMS[1][5],tmp_BMS[1][6],tmp_BMS[1][7]),\
                        (tmp_time,'Battery: 3',tmp_BMS[2][0],tmp_BMS[2][1],tmp_BMS[2][2],tmp_BMS[2][3],tmp_BMS[2][4],tmp_BMS[2][5],tmp_BMS[2][6],tmp_BMS[2][7]),\
                        (tmp_time,'Battery: 4',tmp_BMS[3][0],tmp_BMS[3][1],tmp_BMS[3][2],tmp_BMS[3][3],tmp_BMS[3][4],tmp_BMS[3][5],tmp_BMS[3][6],tmp_BMS[3][7]),\
                        (tmp_time,'Battery: 5',tmp_BMS[4][0],tmp_BMS[4][1],tmp_BMS[4][2],tmp_BMS[4][3],tmp_BMS[4][4],tmp_BMS[4][5],tmp_BMS[4][6],tmp_BMS[4][7]),\
                        (tmp_time,'Battery: 6',tmp_BMS[5][0],tmp_BMS[5][1],tmp_BMS[5][2],tmp_BMS[5][3],tmp_BMS[5][4],tmp_BMS[5][5],tmp_BMS[5][6],tmp_BMS[5][7]),\
                        (tmp_time,'Battery: 7',tmp_BMS[6][0],tmp_BMS[6][1],tmp_BMS[6][2],tmp_BMS[6][3],tmp_BMS[6][4],tmp_BMS[6][5],tmp_BMS[6][6],tmp_BMS[6][7])]

        elif tmp_n_modules == 8:
            tmp_sql = "INSERT INTO pylontech_bms (ts,battery,soc,voltage,current,temperature,b_status,v_status,c_status,t_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            tmp_val = [ (tmp_time,'Battery: 1',tmp_BMS[0][0],tmp_BMS[0][1],tmp_BMS[0][2],tmp_BMS[0][3],tmp_BMS[0][4],tmp_BMS[0][5],tmp_BMS[0][6],tmp_BMS[0][7]),\
                        (tmp_time,'Battery: 2',tmp_BMS[1][0],tmp_BMS[1][1],tmp_BMS[1][2],tmp_BMS[1][3],tmp_BMS[1][4],tmp_BMS[1][5],tmp_BMS[1][6],tmp_BMS[1][7]),\
                        (tmp_time,'Battery: 3',tmp_BMS[2][0],tmp_BMS[2][1],tmp_BMS[2][2],tmp_BMS[2][3],tmp_BMS[2][4],tmp_BMS[2][5],tmp_BMS[2][6],tmp_BMS[2][7]),\
                        (tmp_time,'Battery: 4',tmp_BMS[3][0],tmp_BMS[3][1],tmp_BMS[3][2],tmp_BMS[3][3],tmp_BMS[3][4],tmp_BMS[3][5],tmp_BMS[3][6],tmp_BMS[3][7]),\
                        (tmp_time,'Battery: 5',tmp_BMS[4][0],tmp_BMS[4][1],tmp_BMS[4][2],tmp_BMS[4][3],tmp_BMS[4][4],tmp_BMS[4][5],tmp_BMS[4][6],tmp_BMS[4][7]),\
                        (tmp_time,'Battery: 6',tmp_BMS[5][0],tmp_BMS[5][1],tmp_BMS[5][2],tmp_BMS[5][3],tmp_BMS[5][4],tmp_BMS[5][5],tmp_BMS[5][6],tmp_BMS[5][7]),\
                        (tmp_time,'Battery: 7',tmp_BMS[6][0],tmp_BMS[6][1],tmp_BMS[6][2],tmp_BMS[6][3],tmp_BMS[6][4],tmp_BMS[6][5],tmp_BMS[6][6],tmp_BMS[6][7]),\
                        (tmp_time,'Battery: 8',tmp_BMS[7][0],tmp_BMS[7][1],tmp_BMS[7][2],tmp_BMS[7][3],tmp_BMS[7][4],tmp_BMS[7][5],tmp_BMS[7][6],tmp_BMS[7][7])]

        else:
            print("Unsuported number of battery modules. Only 1-8 modules are supported. The module number parsed is:" + str(tmp_n_modules))
            return False
        try:
            # Executing the SQL command
            cursor.executemany(tmp_sql, tmp_val)
            #print(cursor.rowcount, "records inserted.")
            # Commit your changes in the database
            self._port.commit()
            #print("successfully send data to database")
            return True
        except:
            # Rolling back in case of error
            self._port.rollback()
            print("Failed to send data to database")
            return False


def write_XW(self,XW_LIST):
        """This function writes the parsed data into the mysql database table for Conext XW+ inverter and returns a boolean value
        if the write process was sucessful.

        Args:
            XW_list: list of length [1] containing:
            [inverter, grid_voltage, grid_current, grid_power, grid_frequency, load_voltage, load_current, load_power, load_frequency,
            inverter_dc_current, inverter_dc_power, energy_grid_month, energy_load_month, energy_battery_month, battery_low_voltage,
            battery_low_voltage_delay, battery_hysteresis, inverter_status, inverter_active_warnings_status, inverter_active_faults_status,
            inverter_grid_support_status, inverter_load_shave_status]
            dtype=float and dtype=str.


        DROP TABLE IF EXISTS `conext_xw`;
        CREATE TABLE `conext_xw` (
            `ts` datetime NOT NULL,
            `inverter` varchar(16) DEFAULT (NULL),
            `grid_voltage` float DEFAULT (NULL),
            `grid_current` float DEFAULT (NULL),
            `grid_power` float DEFAULT (NULL),
            `grid_frequency` float DEFAULT (NULL),
            `load_voltage` float DEFAULT (NULL),
            `load_current` float DEFAULT (NULL),
            `load_power` float DEFAULT (NULL),
            `load_frequency` float DEFAULT (NULL),
            `inverter_dc_current` float DEFAULT (NULL),
            `inverter_dc_power` float DEFAULT (NULL),
            `energy_grid_month` float DEFAULT (NULL),
            `energy_load_month` float DEFAULT (NULL),
            `energy_battery_month` float DEFAULT (NULL),
            `battery_low_voltage` float DEFAULT (NULL),
            `battery_low_voltage_delay` float DEFAULT (NULL),
            `battery_hysteresis` float DEFAULT (NULL),
            `inverter_status` varchar(16) DEFAULT (NULL),
            `inverter_active_warnings_status` varchar(16) DEFAULT (NULL),
            `inverter_active_faults_status` varchar(16) DEFAULT (NULL),
            `inverter_grid_support_status` varchar(16) DEFAULT (NULL),
            `inverter_load_shave_status` varchar(16) DEFAULT (NULL),
            PRIMARY KEY (`ts`,`inverter`),
            KEY `idx` (`inverter`,`ts`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;


        Returns: Boolean value True or False

        """
        tmp_n_modules = len(BMS_LIST)
        tmp_time ="{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day,datetime.datetime.now().hour,datetime.datetime.now().minute,datetime.datetime.now().second)

        cursor = self._port.cursor()
        
        tmp_list = XW_LIST

        # Preparing SQL query to INSERT a record into the database.
        
        tmp_sql = "INSERT INTO conext_xw (ts,inverter,grid_voltage,grid_current,grid_power,grid_frequency,load_voltage,load_current,load_power,load_frequency,inverter_dc_current,inverter_dc_power,energy_grid_month,energy_load_month,energy_battery_month,battery_low_voltage,battery_low_voltage_delay,battery_hysteresis,inverter_status,inverter_active_warnings_status,inverter_active_faults_status,inverter_grid_support_status,inverter_load_shave_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        tmp_val = [(tmp_time,tmp_list[0][0],tmp_list[0][1],tmp_list[0][2],tmp_list[0][3],tmp_list[0][4],tmp_list[0][5],tmp_list[0][6],tmp_list[0][7],tmp_list[0][8],tmp_list[0][9],tmp_list[0][10],tmp_list[0][11],tmp_list[0][12],tmp_list[0][13],tmp_list[0][14],tmp_list[0][15],tmp_list[0][16],tmp_list[0][17],tmp_list[0][18],tmp_list[0][19],tmp_list[0][20],tmp_list[0][21])]

        
        try:
            # Executing the SQL command
            cursor.executemany(tmp_sql, tmp_val)
            print(cursor.rowcount, "records inserted.")
            # Commit your changes in the database
            self._port.commit()
            print("successfully send data to database")
            return True
        except:
            # Rolling back in case of error
            self._port.rollback()
            print("Failed to send data to database")
            return False



