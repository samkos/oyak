-- MySQL dump 10.10
--
-- Host: localhost    Database: oyak
-- ------------------------------------------------------
-- Server version	5.0.27-community-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `pcfact_clients`
--

DROP TABLE IF EXISTS `pcfact_clients`;
CREATE TABLE `pcfact_clients` (
  `id` int(8) NOT NULL default '0',
  `civilite` varchar(15)  NOT NULL default '',
  `nom` varchar(30)  NOT NULL default '',
  `prenom` varchar(30)  NOT NULL default '',
  `societe` varchar(35)  NOT NULL default '',
  `adresse` varchar(155)  NOT NULL default '',
  `adresse2` varchar(155)  NOT NULL default '',
  `ville` varchar(50)  NOT NULL default '',
  `code_postal` varchar(15)  NOT NULL default '',
  `pays` int(3) NOT NULL default '33',
  `telephone` varchar(15)  NOT NULL default '',
  `fax` varchar(15)  NOT NULL default '',
  `portable` varchar(15)  NOT NULL default '',
  `email` varchar(155)  NOT NULL default '',
  `clef` varchar(7)  NOT NULL default '',
  `balance` decimal(10,2) NOT NULL default '0.00',
  `timestamp` INTEGER PRIMARY KEY  autoincrement
) ;

--
-- Table structure for table `pcfact_compteur`
--

DROP TABLE IF EXISTS `pcfact_compteur`;
CREATE TABLE `pcfact_compteur` (
  `compteur` INTEGER PRIMARY KEY autoincrement,
  `vendeur` varchar(16) NOT NULL default '',
  `temps` bigint(20) default '0'
) ;

--
-- Table structure for table `pcfact_fournisseurs`
--

DROP TABLE IF EXISTS `pcfact_fournisseurs`;
CREATE TABLE `pcfact_fournisseurs` (
  `id` int(8) NOT NULL default '0',
  `civilite` varchar(15)  NOT NULL default '',
  `nom` varchar(30)  NOT NULL default '',
  `prenom` varchar(30)  NOT NULL default '',
  `societe` varchar(35)  NOT NULL default '',
  `adresse` varchar(155)  NOT NULL default '',
  `adresse2` varchar(155)  NOT NULL default '',
  `ville` varchar(50)  NOT NULL default '',
  `code_postal` varchar(15)  NOT NULL default '',
  `pays` int(3) NOT NULL default '33',
  `telephone` varchar(15)  NOT NULL default '',
  `fax` varchar(15)  NOT NULL default '',
  `portable` varchar(15)  NOT NULL default '',
  `email` varchar(155)  NOT NULL default '',
  `clef` varchar(7)  NOT NULL default '',
  `timestamp` INTEGER PRIMARY KEY autoincrement
);


--
-- Table structure for table `pcfact_produits`
--

DROP TABLE IF EXISTS `pcfact_produits`;
CREATE TABLE `pcfact_produits` (
  `id` int(8) NOT NULL default '0',
  `titre` varchar(35)  NOT NULL default '',
  `id_cat` int(4) NOT NULL default '1',
  `description` text  NOT NULL,
  `prix_vente_ht` decimal(20,2) NOT NULL default '0.00',
  `prix_plancher_ht` decimal(10,2) default '0.00',
  `prix_stock_ht` decimal(10,0) NOT NULL default '0',
  `id_taux_tva` decimal(4,2) NOT NULL default '19.60',
  `stock` decimal(20,3) NOT NULL default '1.000',
  `barcode` varchar(13)  NOT NULL default '',
  `fournisseur` varchar(7)  default NULL,
  `clef` int(11) NOT NULL default '0',
  `poids` float NOT NULL default '0',
  `timestamp`   PRIMARY KEY  (`timestamp`)
) ;


--
-- Table structure for table `pcfact_vendeurs`
--

DROP TABLE IF EXISTS `pcfact_vendeurs`;
CREATE TABLE `pcfact_vendeurs` (
  `id` tinyint(4) NOT NULL default '0',
  `nom` varchar(20) NOT NULL default '',
  `prenom` varchar(30) NOT NULL default '',
  `timestamp` INTEGER PRIMARY KEY autoincrement
) ;

--
