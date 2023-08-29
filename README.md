# Solar-Control-Program
This program controls a solar and battery storgae installation using Pylontech US2000B Plus Batteries and Schneider Conext Inverter and Chage Controller.


# Supported Devices
```
Schneider Conext Devices:
	    1. Schneider ComBox
        2. Schneider MPPT60 150
        3. Schneider XW+ 8548E

Pylontech Battery:
		1. US2000B Plus
```

# Communication
```
Schneider Conext Devices:
	The communication is established over ModbusTCP/IP that is provided by the Schneider ComBox.
    The ComBox is connected via ethernet to the control computer and acts as a media converter
    to the Xanbus, which links the Schneider devices. The communication is implemented using "pymodbusTCP".
    The functions in this module will allow to read and write modbus registers of the Schneider devices,
    thereby allowing it to be controlled remotely.

Pylontech Battery:
	The communication is established over a USB to RS232 adapter, which is connected
    to the console port of the first battery. The console must be initialised with a
    defined string at a baud rate of; 1200,8,n,1. After a successful initialisation
    one can communicate via a text based terminal interface operating at a baud rate
    of; 115200,8,n,1.
```



# CLASS Implementation


## pylontech_com: US2000B
```
This module contains classes and functions to establish a communication with the Pylontech US2000B Plus Battery Management System.

The class in this module ("US200B") allows the user to communicate with the the BMS and extract the following information:

List of extracted values:
    1. SoC
    2. Voltage
    3. Current
    4. Temperature
    5. Battery Status
    6. Voltage Status
    7. Current Status
    8. Temperature Status

List of functions:
	initialise()
	open()
	close()
	is_connected()
	read_SoC()
	read_BMS()
	log_SoC()
	log_BMS()
```

## conext_com: XW
```
This module contains classes and functions to communicate with Schneider Conext; ComBox, MPPT60 150, and XW+ Battery Inverter.

The class in this module ("XW") allows the user to communicate with the the XW+ 8548 Battery Inverter:

List of functions:
	open()
	close()
	is_connected()
	reconnect()
	read_firmware()
	read_device_name()
	read_Grid_Voltage()
	read_Grid_Current()
	read_Grid_Power()
	read_Grid_Frequency()
	read_Load_Voltage()
	read_Load_Current()
	read_Load_Power()
	read_Load_Frequency()
	read_Inverter_DC_Current()
	read_Inverter_DC_Power()
	read_Energy_Grid_Month()
	read_Energy_Load_Month()
	read_Energy_Battery_Month()
	read_Inverter_Active_Warning()
	read_Inverter_Active_Fault()
	read_Inverter_Status()
	read_Low_Battery_Cut_Out()
	write_Low_Battery_Cut_Out()
	read_Low_Battery_Cut_Out_Delay()
	write_Low_Battery_Cut_Out_Delay()
	read_Hysteresis()
	write_Hysteresis()
	read_Grid_Support_Status()
	write_Grid_Support_Status()
	read_Load_Shave_Status()
	write_Load_Shave_Status()
	read_Inverter_All()
```

## conext_com: MPPT60
```
This module contains classes and functions to communicate with Schneider Conext; ComBox, MPPT60 150, and XW+ Battery Inverter.

The class in this module ("MPPT60") allows the user to communicate with the the MPPT60 150 Charge Controller:

List of functions:
	open()
	close()
	is_connected()
	reconnect()
	read_firmware()
	read_device_name()
	read_Energy_PV_Day()
	read_Energy_PV_Week()
	read_Energy_PV_Month()
	read_Energy_PV_Year()
	read_DC_Input_Voltage()
	read_DC_Input_Current()
	read_DC_Input_Power()
	read_DC_Output_Voltage()
	read_DC_Output_Current()
	read_DC_Output_Power()
	read_DC_Output_Power_Percentage()
	read_MPPT_Active_Warning()
	read_MPPT_Active_Fault()
	read_MPPT_Status()
	read_MPPT_Charger_Status()
	read_MPPT_All()
```


## mysql_write: MySQL_com
```
This module contains classes and functions to write Pylontech Battery, Schneider XW+ 8548E, and Schneider MPPT60 150 data into a mysql data base.

The class in this module ("mysql_com") allows the user to communicate with the mysql database. Each device then
has its own function which allows to populate the device specific table.

List of functions:
	open()
	close()
	is_connected()
	write_BMS()
	write_XW()
	write_MPPT()
```

# MySQL Database Tables
```
This section describes the implemented tables in the MySQL database.

Pylontech Battery Table:

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


Schneider Conext XW Table:

        DROP TABLE IF EXISTS `conext_xw`;
        CREATE TABLE `conext_xw` (
            `ts` datetime NOT NULL,
            `device_name` varchar(16) DEFAULT (NULL),
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


Schneider Conext MPPT60 Table:

        DROP TABLE IF EXISTS `conext_mppt`;
        CREATE TABLE `conext_mppt` (
            `ts` datetime NOT NULL,
            `device_name` varchar(16) DEFAULT (NULL),
            `dc_input_voltage` float DEFAULT (NULL),
            `dc_input_current` float DEFAULT (NULL),
            `dc_input_power` float DEFAULT (NULL),
            `dc_output_voltage` float DEFAULT (NULL),
            `dc_output_current` float DEFAULT (NULL),
            `dc_output_power` float DEFAULT (NULL),
            `dc_output_power_percentage` float DEFAULT (NULL),
            `energy_pv_day` float DEFAULT (NULL),
            `energy_pv_week` float DEFAULT (NULL),
            `energy_pv_month` float DEFAULT (NULL),
            `energy_pv_year` float DEFAULT (NULL),
            `mppt_status` varchar(16) DEFAULT (NULL),
            `mppt_charger_status` varchar(16) DEFAULT (NULL),
            `mppt_active_warnings_status` varchar(16) DEFAULT (NULL),
            `mppt_active_faults_status` varchar(16) DEFAULT (NULL),
        PRIMARY KEY (`ts`,`device_name`),
        KEY `idx` (`device_name`,`ts`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```


# Software Installation
```
It is recommended to install the software in the following location: "/usr/local/solar-control-program/"

git clone git@github.com:AlexanderPollak/Solar-Control-Program.git /usr/local/solar-control-program/


The configuration file for the control program is located at: "/usr/local/solar-control-program/etc/scp.cfg"
This file contains all settings that are required to adjust the program to the individual solar battery configuration.
The main sections are:
	1. COMMUNICATION SETTINGS
	2. PYLONTECH BATTERY SPECIFIC SETTINGS
	3. GENERAL CONTROL SETTINGS
	4. CONTROL LOOP SPECIFIC SETTINGS
	5. MySQL SPECIFIC SETTINGS


The required python3 modules are listed in a pip requirement file located at: "/usr/local/solar-control-program/etc/scp-pip-req.txt" 

pip install -r /usr/local/solar-control-program/etc/scp-pip-req.txt


To install the MySQL database follow these steps:


Step 1 — Installing MySQL

apt update
apt install mysql-server
systemctl enable mysql.service
systemctl start mysql.service
systemctl status mysql.service


Step 2 — Configuring MySQL

mysql
mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
mysql> exit
mysql_secure_installation

mysql -u root -p
mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH auth_socket;


Step 3 — Creating a Dedicated MySQL User and Granting Privileges

mysql
mysql> CREATE USER 'grafana'@'localhost' IDENTIFIED WITH authentication_plugin BY 'password';


Step 4 - Create new database called: scpdata

mysql
mysql> CREATE DATABASE scpdata;


Step 5 - Create a New User and Grant Permissions in MySQL

mysql
mysql> CREATE USER 'grafanauser'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
mysql> GRANT ALL on scpdata.* TO 'grafanauser'@'localhost';
mysql> FLUSH PRIVILEGES;


Step 6 - Create a tables in database scpdata

mysql scpdata < /usr/local/solar-control-program/etc/bms-data.sql
mysql scpdata < /usr/local/solar-control-program/etc/xw-data.sql
mysql scpdata < /usr/local/solar-control-program/etc/mppt-data.sql




To install the Grafana data visualization follow these steps:


Step 1 — Install Grafana

wget -q -O - https://packages.grafana.com/gpg.key | gpg --dearmor | sudo tee /usr/share/keyrings/grafana.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/grafana.gpg] https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
apt update
apt install grafana
systemctl start grafana-server
systemctl enable grafana-server
systemctl status grafana-server


Step 2 — Install Solar Control Dashboard


Click Dashboards in the left-side menu.
Click New and select Import in the dropdown menu.
Upload dashboard JSON file from: "/usr/local/solar-control-program/etc/scp-dashboard.json"


```


# Usage:
```
Run the executable shell script in a screen session.

screen -R scp
/usr/local/solar-control-program/Solar-Control-Program.sh
Crtl-A D

To reconnect to the screen session execute:

screen -r scp
```

