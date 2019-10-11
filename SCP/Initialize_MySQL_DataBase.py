""" This module contains classes and functions to initilize a MYSQL data base for the Solar-Control-Program storing BMS and
 Schneider Conext parameters.

**Description:**





"""
import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(host='192.168.0.205',database='SolarControlDataBase',user='pollak',password='PASSWORD')

    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("Your connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")