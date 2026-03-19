# begin-of-file

CREATE DATABASE IF NOT EXISTS gold;

use gold;

CREATE TABLE IF NOT EXISTS  `client` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `uid` char(32) COLLATE utf8mb4_general_ci NOT NULL,
  `pwd` char(32) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `level` enum('0','10','20','30','40','50') COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0',
  `credit` decimal(8,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`id`),
  UNIQUE KEY `client_uid_pwd` (`uid`,`pwd`)
) ENGINE=InnoDB AUTO_INCREMENT=8457 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS `exchangerate` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `day` date NOT NULL,
  `usd` decimal(8,4) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `exchangerate_day` (`day`)
) ENGINE=InnoDB AUTO_INCREMENT=427 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS `goldapicom` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `day` date NOT NULL,
  `clock` time NOT NULL,
  `price` decimal(8,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `goldapicom_day_clock` (`day`,`clock`)
) ENGINE=InnoDB AUTO_INCREMENT=555228 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS `info` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `day` date NOT NULL,
  `clock` time NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `url` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `info_day_clock` (`day`,`clock`)
) ENGINE=InnoDB AUTO_INCREMENT=104 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS `infocontent` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `info_id` int unsigned NOT NULL,
  `content` longtext COLLATE utf8mb4_general_ci,
  `pdf` longtext COLLATE utf8mb4_general_ci,
  `comment` longtext COLLATE utf8mb4_general_ci,
  PRIMARY KEY (`id`),
  KEY `infocontent_info_id` (`info_id`),
  CONSTRAINT `infocontent_info_id` FOREIGN KEY (`info_id`) REFERENCES `info` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS `variety` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `day` date NOT NULL,
  `clock` time NOT NULL,
  `gold` decimal(8,2) DEFAULT NULL,
  `silver` decimal(8,2) DEFAULT NULL,
  `copper` decimal(8,2) DEFAULT NULL,
  `platinum` decimal(8,2) DEFAULT NULL,
  `palladium` decimal(8,2) DEFAULT NULL,
  `butter` decimal(8,2) DEFAULT NULL,
  `cheese` decimal(8,2) DEFAULT NULL,
  `treasury_10y` decimal(8,2) DEFAULT NULL,
  `treasury_1y` decimal(8,2) DEFAULT NULL,
  `treasury_2y` decimal(8,2) DEFAULT NULL,
  `treasury_5y` decimal(8,2) DEFAULT NULL,
  `treasury_30y` decimal(8,2) DEFAULT NULL,
  `fed_funds` decimal(8,2) DEFAULT NULL,
  `unemployment` decimal(8,2) DEFAULT NULL,
  `cpi` decimal(8,2) DEFAULT NULL,
  `bitcoin` decimal(8,2) DEFAULT NULL,
  `ethereum` decimal(8,2) DEFAULT NULL,
  `solana` decimal(8,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `variety_day_clock` (`day`,`clock`)
) ENGINE=InnoDB AUTO_INCREMENT=18675 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

# end-of-file