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
            print("unable to connect to " + HOST)

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




    def write_bms(self,BMS_ARRAY):
        """This function writes the parsed data into the mysql database table for pylontech_bms and returns a boolean value
        if the write process was sucessful.

        Args:
            BMS_ARRAY: list of length [n_modules] containing numpy arrays with the:
            [SoC, Voltage, Current, Temperature, Battery Status, Voltage Status, Temperature Status] dtype=float64 and dtype=str.


        DROP TABLE IF EXISTS `pylontech_bms`;
        CREATE TABLE `pylontech_bms` (
            `ts` datetime NOT NULL,
            `battery` int NOT NULL,
            `soc` float DEFAULT (NULL),
            `voltage` float DEFAULT (NULL),
            `current` float DEFAULT (NULL),
            `temperature` float DEFAULT (NULL),
            `b_status` float DEFAULT (NULL),
            `v_status` float DEFAULT (NULL),
            `t_status` float DEFAULT (NULL),
            PRIMARY KEY (`ts`,`battery`),
            KEY `idx` (`battery`,`ts`)
            ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
    

        Returns: Boolean value True or False

        """
        tmp_n_modules = len(BMS_ARRAY)
        tmp_time = str(datetime.datetime.now().date()) + ' ' + str(datetime.datetime.now().hour) + ':' + str(
            datetime.datetime.now().minute) + ':' + str(datetime.datetime.now().second)

        cursor = self._port.cursor()
        

        # Preparing SQL query to INSERT a record into the database.
        if tmp_n_modules == 1:
            tmp_sql = "INSERT INTO pylontech_bms (ts,battery,soc,voltage,current,temperature,b_status,v_status,t_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            tmp_val = [(tmp_time,1,BMS_ARRAY[0, 0],BMS_ARRAY[0, 1],BMS_ARRAY[0, 2],BMS_ARRAY[0, 3],BMS_ARRAY[0, 4],BMS_ARRAY[0, 5],BMS_ARRAY[0, 6])]

        if tmp_n_modules == 2:
            tmp_sql = "INSERT INTO pylontech_bms (ts,battery,soc,voltage,current,temperature,b_status,v_status,t_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            tmp_val = [ (tmp_time,1,BMS_ARRAY[0, 0],BMS_ARRAY[0, 1],BMS_ARRAY[0, 2],BMS_ARRAY[0, 3],BMS_ARRAY[0, 4],BMS_ARRAY[0, 5],BMS_ARRAY[0, 6]),\
                        (tmp_time,2,BMS_ARRAY[1, 0],BMS_ARRAY[1, 1],BMS_ARRAY[1, 2],BMS_ARRAY[1, 3],BMS_ARRAY[1, 4],BMS_ARRAY[1, 5],BMS_ARRAY[1, 6])]
        
        if tmp_n_modules == 3:
            tmp_sql = "INSERT INTO pylontech_bms (ts,battery,soc,voltage,current,temperature,b_status,v_status,t_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            tmp_val = [ (tmp_time,1,BMS_ARRAY[0, 0],BMS_ARRAY[0, 1],BMS_ARRAY[0, 2],BMS_ARRAY[0, 3],BMS_ARRAY[0, 4],BMS_ARRAY[0, 5],BMS_ARRAY[0, 6]),\
                        (tmp_time,2,BMS_ARRAY[1, 0],BMS_ARRAY[1, 1],BMS_ARRAY[1, 2],BMS_ARRAY[1, 3],BMS_ARRAY[1, 4],BMS_ARRAY[1, 5],BMS_ARRAY[1, 6]),\
                        (tmp_time,3,BMS_ARRAY[2, 0],BMS_ARRAY[2, 1],BMS_ARRAY[2, 2],BMS_ARRAY[2, 3],BMS_ARRAY[2, 4],BMS_ARRAY[2, 5],BMS_ARRAY[2, 6])]

        if tmp_n_modules == 4:
            tmp_sql = "INSERT INTO pylontech_bms (ts,battery,soc,voltage,current,temperature,b_status,v_status,t_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            tmp_val = [ (tmp_time,1,BMS_ARRAY[0, 0],BMS_ARRAY[0, 1],BMS_ARRAY[0, 2],BMS_ARRAY[0, 3],BMS_ARRAY[0, 4],BMS_ARRAY[0, 5],BMS_ARRAY[0, 6]),\
                        (tmp_time,2,BMS_ARRAY[1, 0],BMS_ARRAY[1, 1],BMS_ARRAY[1, 2],BMS_ARRAY[1, 3],BMS_ARRAY[1, 4],BMS_ARRAY[1, 5],BMS_ARRAY[1, 6]),\
                        (tmp_time,3,BMS_ARRAY[2, 0],BMS_ARRAY[2, 1],BMS_ARRAY[2, 2],BMS_ARRAY[2, 3],BMS_ARRAY[2, 4],BMS_ARRAY[2, 5],BMS_ARRAY[2, 6]),\
                        (tmp_time,4,BMS_ARRAY[3, 0],BMS_ARRAY[3, 1],BMS_ARRAY[3, 2],BMS_ARRAY[3, 3],BMS_ARRAY[3, 4],BMS_ARRAY[3, 5],BMS_ARRAY[3, 6])]                        

        if tmp_n_modules == 5:
            tmp_sql = "INSERT INTO pylontech_bms (ts,battery,soc,voltage,current,temperature,b_status,v_status,t_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            tmp_val = [ (tmp_time,1,BMS_ARRAY[0, 0],BMS_ARRAY[0, 1],BMS_ARRAY[0, 2],BMS_ARRAY[0, 3],BMS_ARRAY[0, 4],BMS_ARRAY[0, 5],BMS_ARRAY[0, 6]),\
                        (tmp_time,2,BMS_ARRAY[1, 0],BMS_ARRAY[1, 1],BMS_ARRAY[1, 2],BMS_ARRAY[1, 3],BMS_ARRAY[1, 4],BMS_ARRAY[1, 5],BMS_ARRAY[1, 6]),\
                        (tmp_time,3,BMS_ARRAY[2, 0],BMS_ARRAY[2, 1],BMS_ARRAY[2, 2],BMS_ARRAY[2, 3],BMS_ARRAY[2, 4],BMS_ARRAY[2, 5],BMS_ARRAY[2, 6]),\
                        (tmp_time,4,BMS_ARRAY[3, 0],BMS_ARRAY[3, 1],BMS_ARRAY[3, 2],BMS_ARRAY[3, 3],BMS_ARRAY[3, 4],BMS_ARRAY[3, 5],BMS_ARRAY[3, 6]),\
                        (tmp_time,5,BMS_ARRAY[4, 0],BMS_ARRAY[4, 1],BMS_ARRAY[4, 2],BMS_ARRAY[4, 3],BMS_ARRAY[4, 4],BMS_ARRAY[4, 5],BMS_ARRAY[4, 6])]  

        if tmp_n_modules == 6:
            tmp_sql = "INSERT INTO pylontech_bms (ts,battery,soc,voltage,current,temperature,b_status,v_status,t_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            tmp_val = [ (tmp_time,1,BMS_ARRAY[0, 0],BMS_ARRAY[0, 1],BMS_ARRAY[0, 2],BMS_ARRAY[0, 3],BMS_ARRAY[0, 4],BMS_ARRAY[0, 5],BMS_ARRAY[0, 6]),\
                        (tmp_time,2,BMS_ARRAY[1, 0],BMS_ARRAY[1, 1],BMS_ARRAY[1, 2],BMS_ARRAY[1, 3],BMS_ARRAY[1, 4],BMS_ARRAY[1, 5],BMS_ARRAY[1, 6]),\
                        (tmp_time,3,BMS_ARRAY[2, 0],BMS_ARRAY[2, 1],BMS_ARRAY[2, 2],BMS_ARRAY[2, 3],BMS_ARRAY[2, 4],BMS_ARRAY[2, 5],BMS_ARRAY[2, 6]),\
                        (tmp_time,4,BMS_ARRAY[3, 0],BMS_ARRAY[3, 1],BMS_ARRAY[3, 2],BMS_ARRAY[3, 3],BMS_ARRAY[3, 4],BMS_ARRAY[3, 5],BMS_ARRAY[3, 6]),\
                        (tmp_time,5,BMS_ARRAY[4, 0],BMS_ARRAY[4, 1],BMS_ARRAY[4, 2],BMS_ARRAY[4, 3],BMS_ARRAY[4, 4],BMS_ARRAY[4, 5],BMS_ARRAY[4, 6]),\
                        (tmp_time,6,BMS_ARRAY[5, 0],BMS_ARRAY[5, 1],BMS_ARRAY[5, 2],BMS_ARRAY[5, 3],BMS_ARRAY[5, 4],BMS_ARRAY[5, 5],BMS_ARRAY[5, 6])] 

        if tmp_n_modules == 7:
            tmp_sql = "INSERT INTO pylontech_bms (ts,battery,soc,voltage,current,temperature,b_status,v_status,t_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            tmp_val = [ (tmp_time,1,BMS_ARRAY[0, 0],BMS_ARRAY[0, 1],BMS_ARRAY[0, 2],BMS_ARRAY[0, 3],BMS_ARRAY[0, 4],BMS_ARRAY[0, 5],BMS_ARRAY[0, 6]),\
                        (tmp_time,2,BMS_ARRAY[1, 0],BMS_ARRAY[1, 1],BMS_ARRAY[1, 2],BMS_ARRAY[1, 3],BMS_ARRAY[1, 4],BMS_ARRAY[1, 5],BMS_ARRAY[1, 6]),\
                        (tmp_time,3,BMS_ARRAY[2, 0],BMS_ARRAY[2, 1],BMS_ARRAY[2, 2],BMS_ARRAY[2, 3],BMS_ARRAY[2, 4],BMS_ARRAY[2, 5],BMS_ARRAY[2, 6]),\
                        (tmp_time,4,BMS_ARRAY[3, 0],BMS_ARRAY[3, 1],BMS_ARRAY[3, 2],BMS_ARRAY[3, 3],BMS_ARRAY[3, 4],BMS_ARRAY[3, 5],BMS_ARRAY[3, 6]),\
                        (tmp_time,5,BMS_ARRAY[4, 0],BMS_ARRAY[4, 1],BMS_ARRAY[4, 2],BMS_ARRAY[4, 3],BMS_ARRAY[4, 4],BMS_ARRAY[4, 5],BMS_ARRAY[4, 6]),\
                        (tmp_time,6,BMS_ARRAY[5, 0],BMS_ARRAY[5, 1],BMS_ARRAY[5, 2],BMS_ARRAY[5, 3],BMS_ARRAY[5, 4],BMS_ARRAY[5, 5],BMS_ARRAY[5, 6]),\ 
                        (tmp_time,7,BMS_ARRAY[6, 0],BMS_ARRAY[6, 1],BMS_ARRAY[6, 2],BMS_ARRAY[6, 3],BMS_ARRAY[6, 4],BMS_ARRAY[6, 5],BMS_ARRAY[6, 6])] 

        if tmp_n_modules == 8:
            tmp_sql = "INSERT INTO pylontech_bms (ts,battery,soc,voltage,current,temperature,b_status,v_status,t_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            tmp_val = [ (tmp_time,1,BMS_ARRAY[0, 0],BMS_ARRAY[0, 1],BMS_ARRAY[0, 2],BMS_ARRAY[0, 3],BMS_ARRAY[0, 4],BMS_ARRAY[0, 5],BMS_ARRAY[0, 6]),\
                        (tmp_time,2,BMS_ARRAY[1, 0],BMS_ARRAY[1, 1],BMS_ARRAY[1, 2],BMS_ARRAY[1, 3],BMS_ARRAY[1, 4],BMS_ARRAY[1, 5],BMS_ARRAY[1, 6]),\
                        (tmp_time,3,BMS_ARRAY[2, 0],BMS_ARRAY[2, 1],BMS_ARRAY[2, 2],BMS_ARRAY[2, 3],BMS_ARRAY[2, 4],BMS_ARRAY[2, 5],BMS_ARRAY[2, 6]),\
                        (tmp_time,4,BMS_ARRAY[3, 0],BMS_ARRAY[3, 1],BMS_ARRAY[3, 2],BMS_ARRAY[3, 3],BMS_ARRAY[3, 4],BMS_ARRAY[3, 5],BMS_ARRAY[3, 6]),\
                        (tmp_time,5,BMS_ARRAY[4, 0],BMS_ARRAY[4, 1],BMS_ARRAY[4, 2],BMS_ARRAY[4, 3],BMS_ARRAY[4, 4],BMS_ARRAY[4, 5],BMS_ARRAY[4, 6]),\
                        (tmp_time,6,BMS_ARRAY[5, 0],BMS_ARRAY[5, 1],BMS_ARRAY[5, 2],BMS_ARRAY[5, 3],BMS_ARRAY[5, 4],BMS_ARRAY[5, 5],BMS_ARRAY[5, 6]),\ 
                        (tmp_time,7,BMS_ARRAY[6, 0],BMS_ARRAY[6, 1],BMS_ARRAY[6, 2],BMS_ARRAY[6, 3],BMS_ARRAY[6, 4],BMS_ARRAY[6, 5],BMS_ARRAY[6, 6]),\
                        (tmp_time,8,BMS_ARRAY[7, 0],BMS_ARRAY[7, 1],BMS_ARRAY[7, 2],BMS_ARRAY[7, 3],BMS_ARRAY[7, 4],BMS_ARRAY[7, 5],BMS_ARRAY[7, 6])] 

        else:
            print("Unsuported number of battery modules. Only 1-8 modules are supported. The module number parsed is:" + tmp_n_modules)
            return False
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
            print("failed to send data to database")
            return False





