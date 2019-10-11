""" This module contains classes and functions to initilize a MYSQL data base for the Solar-Control-Program storing BMS and
 Schneider Conext parameters.

**Description:**





"""
import mysql.connector
from mysql.connector import Error



class MySQL(object):

    def __init__(self):
        ''' Constructor for this class. '''
        self.host = '192.168.0.205'
        self.database = 'SolarControlDataBase'
        self.user = 'pollak'
        self.password = 'PASSWORD'

    def __del__(self):
        ''' Destructor for this class. '''


    def verify_connection(self):

        try:
            connection = mysql.connector.connect(host=self.host,database=self.database,user=self.user,password=self.password)

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



    def create_table_bms(self):

        try:
            connection = mysql.connector.connect(shost=self.host,database=self.database,user=self.user,password=self.password)

            if connection.is_connected():

                mySql_Create_Table_Query = """CREATE TABLE BMS ( 
                                        Id INT NOT NULL,
                                        Time TIMESTAMP NOT NULL,
                                        SoC1 MEDIUMINT NOT NULL,
                                        Voltage1 MEDIUMINT NOT NULL,
                                        Current1 MEDIUMINT NOT NULL,
                                        Temperature1 MEDIUMINT NOT NULL,
                                        SoC2 MEDIUMINT NOT NULL,
                                        Voltage2 MEDIUMINT NOT NULL,
                                        Current2 MEDIUMINT NOT NULL,
                                        Temperature2 MEDIUMINT NOT NULL,
                                        SoC3 MEDIUMINT NOT NULL,
                                        Voltage3 MEDIUMINT NOT NULL,
                                        Current3 MEDIUMINT NOT NULL,
                                        Temperature3 MEDIUMINT NOT NULL,
                                        SoC4 MEDIUMINT NOT NULL,
                                        Voltage4 MEDIUMINT NOT NULL,
                                        Current4 MEDIUMINT NOT NULL,
                                        Temperature4 MEDIUMINT NOT NULL,
                                        SoC5 MEDIUMINT NOT NULL,
                                        Voltage5 MEDIUMINT NOT NULL,
                                        Current5 MEDIUMINT NOT NULL,
                                        Temperature5 MEDIUMINT NOT NULL,
                                        SoC6 MEDIUMINT NOT NULL,
                                        Voltage6 MEDIUMINT NOT NULL,
                                        Current6 MEDIUMINT NOT NULL,
                                        Temperature6 MEDIUMINT NOT NULL,
                                        SoC7 MEDIUMINT NOT NULL,
                                        Voltage7 MEDIUMINT NOT NULL,
                                        Current7 MEDIUMINT NOT NULL,
                                        Temperature7 MEDIUMINT NOT NULL,
                                        SoC8 MEDIUMINT NOT NULL,
                                        Voltage8 MEDIUMINT NOT NULL,
                                        Current8 MEDIUMINT NOT NULL,
                                        Temperature8 MEDIUMINT NOT NULL,
                                        PRIMARY KEY (Id)) """

                cursor = connection.cursor()
                result = cursor.execute(mySql_Create_Table_Query)
                print(" Table created successfully ")
                print (result)

        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("MySQL connection is closed")


    def drop_table_bms(self):

        try:
            connection = mysql.connector.connect(host=self.host,database=self.database,user=self.user,password=self.password)

            if connection.is_connected():

                mySql_Drop_Table_Query = """DROP TABLE BMS """

                cursor = connection.cursor()
                result = cursor.execute(mySql_Drop_Table_Query)
                print(" Table droped successfully ")
                print(result)

        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("MySQL connection is closed")


if __name__ == '__main__':
    test=MySQL()
    test.verify_connection()