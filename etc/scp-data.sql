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
-- Table structure for table `battery_bms`
--

DROP TABLE IF EXISTS `pylontech_bms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `battery_bms` (
  `ts` datetime NOT NULL CURRENT_TIMESTAMP,
  `battery` int NOT NULL,
  `soc` float DEFAULT (NULL),
  `voltage` float DEFAULT (NULL),
  `current` float DEFAULT (NULL),
  `temperature` float DEFAULT (NULL),
  `b_status` varchar(16) DEFAULT (NULL),
  `v_status` varchar(16) DEFAULT (NULL),
  `t_status` varchar(16) DEFAULT (NULL),
  PRIMARY KEY (`ts`,`battery`),
  KEY `idx` (`battery`,`ts`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `conext_xw`
--

DROP TABLE IF EXISTS `conext_xw`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `conext_xw` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ts` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `inverter_status` varchar(16) DEFAULT (NULL),
  `firmware` varchar(16) DEFAULT (NULL),
  `grid_voltage` float DEFAULT (NULL),
  `grid_frequency` float DEFAULT (NULL),
  `low_battery_cut_out` float DEFAULT (NULL),
  `low_battery_cut_out_delay` float DEFAULT (NULL),
  `grid_support_status` varchar(16) DEFAULT (NULL),
  `load_shave_status` varchar(16) DEFAULT (NULL),
  `hysteresis` float DEFAULT (NULL),
  PRIMARY KEY (`id`,`ts`)
) ENGINE=InnoDB AUTO_INCREMENT=151022 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

--
-- Table structure for table `conext_mppt`
--

DROP TABLE IF EXISTS `conext_mppt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `conext_xw` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ts` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `inverter_status` varchar(16) DEFAULT (NULL),
  `firmware` varchar(16) DEFAULT (NULL),
  `grid_voltage` float DEFAULT (NULL),
  `grid_frequency` float DEFAULT (NULL),
  `low_battery_cut_out` float DEFAULT (NULL),
  `low_battery_cut_out_delay` float DEFAULT (NULL),
  `grid_support_status` varchar(16) DEFAULT (NULL),
  `load_shave_status` varchar(16) DEFAULT (NULL),
  `hysteresis` float DEFAULT (NULL),
  PRIMARY KEY (`id`,`ts`)
) ENGINE=InnoDB AUTO_INCREMENT=151022 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;













--
-- Table structure for table `antenna_sensors`
--

DROP TABLE IF EXISTS `antenna_sensors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `antenna_sensors` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ts` datetime NOT NULL,
  `ant` varchar(3) NOT NULL,
  `drive_box_temp` float DEFAULT '-99',
  `control_box_temp` float DEFAULT '-99',
  `pax_box_temp` float DEFAULT '-99',
  `rim_box_temp` float DEFAULT '-99',
  PRIMARY KEY (`id`,`ts`,`ant`)
) ENGINE=InnoDB AUTO_INCREMENT=2673438 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `antnums`
--

DROP TABLE IF EXISTS `antnums`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `antnums` (
  `ant` varchar(2) NOT NULL,
  `num` tinyint NOT NULL,
  PRIMARY KEY (`ant`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `feed_sensors`
--

DROP TABLE IF EXISTS `feed_sensors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feed_sensors` (
  `ts` datetime NOT NULL,
  `ant` varchar(3) NOT NULL,
  `state` tinyint NOT NULL DEFAULT '0',
  `fanpwm` varchar(8) DEFAULT NULL,
  `fanspeed` float DEFAULT '-99',
  `cryoattemp` varchar(8) DEFAULT NULL,
  `controlboardtemp` float DEFAULT '-99',
  `outsideairtemp` float DEFAULT '-99',
  `paxairtemp` float DEFAULT '-99',
  `exhausttemp` float DEFAULT '-99',
  `coolerrejectiontemp` float DEFAULT '-99',
  `coolerhousingtemp` float DEFAULT '-99',
  `lnatemp` float DEFAULT '-99',
  `lnadiodevoltage` float DEFAULT '-99',
  `accelminx` float DEFAULT '-99',
  `accelmeanx` float DEFAULT '-99',
  `accelstdx` float DEFAULT '-99',
  `accelmaxx` float DEFAULT '-99',
  `accelminy` float DEFAULT '-99',
  `accelmeany` float DEFAULT '-99',
  `accelstdy` float DEFAULT '-99',
  `accelmaxy` float DEFAULT '-99',
  `accelminz` float DEFAULT '-99',
  `accelmeanz` float DEFAULT '-99',
  `accelstdz` float DEFAULT '-99',
  `accelmaxz` float DEFAULT '-99',
  `relaystate` varchar(8) DEFAULT NULL,
  `feedstartmode` varchar(8) DEFAULT NULL,
  `cryotempregulating` varchar(8) DEFAULT NULL,
  `cryotempnoregulating` varchar(8) DEFAULT NULL,
  `vdc24volt` float DEFAULT '-99',
  `errormessages` varchar(8) DEFAULT NULL,
  `displayexcesstemp` int DEFAULT '-99',
  `excesstempturbo` int DEFAULT '-99',
  `turbocurrrent` int DEFAULT '-99',
  `ophours` int DEFAULT '-99',
  `turbospeednominal` int DEFAULT '-99',
  `turbopower` int DEFAULT '-99',
  `electronicsboardtemp` int DEFAULT '-99',
  `turbobottomtemp` int DEFAULT '-99',
  `turbobearingtemp` int DEFAULT '-99',
  `turbomotortemp` int DEFAULT '-99',
  `turbospeedactual` int DEFAULT '-99',
  `cryopower` float DEFAULT '-99',
  `cryotemp` float DEFAULT '-99',
  PRIMARY KEY (`ts`,`ant`),
  KEY `idx` (`ant`,`ts`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `lna_bias`
--

DROP TABLE IF EXISTS `lna_bias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lna_bias` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ts` datetime NOT NULL,
  `sn` varchar(16) NOT NULL,
  `x_vg` float DEFAULT '-99',
  `x_vd` float DEFAULT '-99',
  `x_vm` float DEFAULT '-99',
  `x_id` float DEFAULT '-99',
  `y_vg` float DEFAULT '-99',
  `y_vd` float DEFAULT '-99',
  `y_vm` float DEFAULT '-99',
  `y_id` float DEFAULT '-99',
  PRIMARY KEY (`id`,`ts`,`sn`)
) ENGINE=InnoDB AUTO_INCREMENT=1628168 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `weather`
--

DROP TABLE IF EXISTS `weather`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `weather` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ts` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `primary_pressure_mb` float DEFAULT (NULL),
  `secondary_pressure_mb` float DEFAULT (NULL),
  `primary_outside_temp_c` float DEFAULT (NULL),
  `secondary_outside_temp_c` float DEFAULT (NULL),
  `primary_outside_humidity_pct` float DEFAULT (NULL),
  `secondary_outside_humidity_pct` float DEFAULT (NULL),
  `primary_windspeed_avg_mph` float DEFAULT (NULL),
  `secondary_windspeed_avg_mph` float DEFAULT (NULL),
  `primary_windspeed_max_mph` float DEFAULT (NULL),
  `secondary_windspeed_max_mph` float DEFAULT (NULL),
  `primary_windspeed_min_mph` float DEFAULT (NULL),
  `secondary_windspeed_min_mph` float DEFAULT (NULL),
  `primary_windspeed_dir_avg_deg` float DEFAULT (NULL),
  `secondary_windspeed_dir_avg_deg` float DEFAULT (NULL),
  `primary_rain_rate_mm_hr` float DEFAULT (NULL),
  `secondary_rain_rate_mm_hr` float DEFAULT (NULL),
  `primary_windspeed_dir_min_deg` float DEFAULT (NULL),
  `secondary_windspeed_dir_min_deg` float DEFAULT (NULL),
  `primary_windspeed_dir_max_deg` float DEFAULT (NULL),
  `secondary_windspeed_dir_max_deg` float DEFAULT (NULL),
  `primary_rain_accumulation_mm` float DEFAULT (NULL),
  `secondary_rain_accumulation_mm` float DEFAULT (NULL),
  `primary_rain_duration_sec` float DEFAULT (NULL),
  `secondary_rain_duration_sec` float DEFAULT (NULL),
  `primary_hail_accumulation_hts_cm` float DEFAULT (NULL),
  `secondary_hail_accumulation_hts_cm` float DEFAULT (NULL),
  `primary_hail_duration_sec` float DEFAULT (NULL),
  `secondary_hail_duration_sec` float DEFAULT (NULL),
  `primary_hail_intensity_hts_cmh` float DEFAULT (NULL),
  `secondary_hail_intensity_hts_cmh` float DEFAULT (NULL),
  `primary_heating_temp_c` float DEFAULT (NULL),
  `secondary_heating_temp_c` float DEFAULT (NULL),
  `primary_heating_vltg` float DEFAULT (NULL),
  `secondary_heating_vltg` float DEFAULT (NULL),
  `primary_supply_vltg` float DEFAULT (NULL),
  `secondary_supply_vltg` float DEFAULT (NULL),
  `primary_ref_vltg` float DEFAULT (NULL),
  `secondary_ref_vltg` float DEFAULT (NULL),
  PRIMARY KEY (`id`,`ts`)
) ENGINE=InnoDB AUTO_INCREMENT=151022 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-08-16  8:35:16
