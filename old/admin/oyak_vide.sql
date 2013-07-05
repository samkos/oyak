-- phpMyAdmin SQL Dump
-- version 2.6.1
-- http://www.phpmyadmin.net
-- 
-- Serveur: localhost
-- Généré le : Jeudi 28 Décembre 2006 à 10:40
-- Version du serveur: 4.1.9
-- Version de PHP: 4.3.10
-- 
-- Base de données: `oyak`
-- 

-- --------------------------------------------------------
use oyak;
-- 
-- Structure de la table `pcfact_clients`
-- 

DROP TABLE IF EXISTS `pcfact_clients`;
CREATE TABLE IF NOT EXISTS `pcfact_clients` (
  `id` int(8) NOT NULL auto_increment,
  `civilite` varchar(15) collate latin1_general_ci NOT NULL default '',
  `nom` varchar(30) collate latin1_general_ci NOT NULL default '',
  `prenom` varchar(30) collate latin1_general_ci NOT NULL default '',
  `societe` varchar(35) collate latin1_general_ci NOT NULL default '',
  `adresse` varchar(155) collate latin1_general_ci NOT NULL default '',
  `adresse2` varchar(155) collate latin1_general_ci NOT NULL default '',
  `ville` varchar(50) collate latin1_general_ci NOT NULL default '',
  `code_postal` varchar(15) collate latin1_general_ci NOT NULL default '',
  `pays` int(3) NOT NULL default '33',
  `telephone` varchar(15) collate latin1_general_ci NOT NULL default '',
  `fax` varchar(15) collate latin1_general_ci NOT NULL default '',
  `portable` varchar(15) collate latin1_general_ci NOT NULL default '',
  `email` varchar(155) collate latin1_general_ci NOT NULL default '',
  `clef` varchar(7) collate latin1_general_ci NOT NULL default '',
  KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci AUTO_INCREMENT=1140 ;

-- --------------------------------------------------------

-- 
-- Structure de la table `pcfact_compteur`
-- 

DROP TABLE IF EXISTS `pcfact_compteur`;
CREATE TABLE IF NOT EXISTS `pcfact_compteur` (
  `compteur` bigint(12) NOT NULL auto_increment,
  `vendeur` varchar(16) NOT NULL default '',
  `temps` bigint(20) default '0',
  KEY `compteur` (`compteur`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

-- 
-- Structure de la table `pcfact_factures`
-- 

DROP TABLE IF EXISTS `pcfact_factures`;
CREATE TABLE IF NOT EXISTS `pcfact_factures` (
  `num` int(8) NOT NULL auto_increment,
  `id_clt` int(8) NOT NULL default '0',
  `id_taux` int(2) NOT NULL default '0',
  `escompte` decimal(4,2) NOT NULL default '0.00',
  `date` date NOT NULL default '0000-00-00',
  `type` char(1) collate latin1_general_ci NOT NULL default '',
  `etat` int(1) NOT NULL default '0',
  KEY `num` (`num`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci AUTO_INCREMENT=3 ;

-- --------------------------------------------------------

-- 
-- Structure de la table `pcfact_factures_produits`
-- 

DROP TABLE IF EXISTS `pcfact_factures_produits`;
CREATE TABLE IF NOT EXISTS `pcfact_factures_produits` (
  `id` int(15) NOT NULL auto_increment,
  `num_fact` int(8) NOT NULL default '0',
  `id_produit` int(8) NOT NULL default '0',
  `id_remise` int(2) NOT NULL default '0',
  `quantite` decimal(20,2) NOT NULL default '0.00',
  KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci AUTO_INCREMENT=4 ;

-- --------------------------------------------------------

-- 
-- Structure de la table `pcfact_pays`
-- 

DROP TABLE IF EXISTS `pcfact_pays`;
CREATE TABLE IF NOT EXISTS `pcfact_pays` (
  `id` int(3) NOT NULL auto_increment,
  `pays` varchar(35) collate latin1_general_ci NOT NULL default '',
  `pref_tel` varchar(4) collate latin1_general_ci NOT NULL default '',
  KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci AUTO_INCREMENT=50 ;

-- --------------------------------------------------------

-- 
-- Structure de la table `pcfact_produits`
-- 

DROP TABLE IF EXISTS `pcfact_produits`;
CREATE TABLE IF NOT EXISTS `pcfact_produits` (
  `id` int(8) NOT NULL auto_increment,
  `titre` varchar(35) collate latin1_general_ci NOT NULL default '',
  `id_cat` int(4) NOT NULL default '1',
  `description` text collate latin1_general_ci NOT NULL,
  `prix_vente_ht` decimal(20,2) NOT NULL default '0.00',
  `id_taux_tva` decimal(4,2) NOT NULL default '19.60',
  `stock` int(1) NOT NULL default '1',
  `barcode` varchar(13) collate latin1_general_ci NOT NULL default '',
  KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci AUTO_INCREMENT=1735 ;

-- --------------------------------------------------------

-- 
-- Structure de la table `pcfact_produits_cat`
-- 

DROP TABLE IF EXISTS `pcfact_produits_cat`;
CREATE TABLE IF NOT EXISTS `pcfact_produits_cat` (
  `id` int(4) NOT NULL auto_increment,
  `titre` varchar(50) collate latin1_general_ci NOT NULL default '',
  KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

-- 
-- Structure de la table `pcfact_remises`
-- 

DROP TABLE IF EXISTS `pcfact_remises`;
CREATE TABLE IF NOT EXISTS `pcfact_remises` (
  `id` int(2) NOT NULL auto_increment,
  `titre` varchar(35) collate latin1_general_ci NOT NULL default '',
  `taux` decimal(4,2) NOT NULL default '0.00',
  KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

-- 
-- Structure de la table `pcfact_stocks`
-- 

DROP TABLE IF EXISTS `pcfact_stocks`;
CREATE TABLE IF NOT EXISTS `pcfact_stocks` (
  `id` int(6) NOT NULL auto_increment,
  `ref_produit` int(6) NOT NULL default '0',
  `quantite` decimal(20,2) NOT NULL default '0.00',
  `prix_ht` decimal(20,2) NOT NULL default '0.00',
  `date` date NOT NULL default '0000-00-00',
  KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci AUTO_INCREMENT=5 ;

-- --------------------------------------------------------

-- 
-- Structure de la table `pcfact_taux_tva`
-- 

DROP TABLE IF EXISTS `pcfact_taux_tva`;
CREATE TABLE IF NOT EXISTS `pcfact_taux_tva` (
  `id` int(2) NOT NULL auto_increment,
  `taux` decimal(4,2) NOT NULL default '0.00',
  KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

-- 
-- Structure de la table `pcfact_vendeurs`
-- 

DROP TABLE IF EXISTS `pcfact_vendeurs`;
CREATE TABLE IF NOT EXISTS `pcfact_vendeurs` (
  `id` tinyint(4) NOT NULL auto_increment,
  `nom` varchar(20) NOT NULL default '',
  `prenom` varchar(30) NOT NULL default '',
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=7 ;
