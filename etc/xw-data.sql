-- MySQL dump 10.13  Distrib 8.0.34, for Linux (x86_64)
--
-- Host: localhost    Database: scpdata
-- ------------------------------------------------------
-- Server version	8.0.34-0ubuntu0.20.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;



--
-- Table structure for table `conext_xw`
--

DROP TABLE IF EXISTS `conext_xw`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
  PRIMARY KEY (`ts`,`device_name`),
  KEY `idx` (`device_name`,`ts`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

