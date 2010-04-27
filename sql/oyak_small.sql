-- phpMyAdmin SQL Dump
-- version 2.6.1
-- http://www.phpmyadmin.net
-- 
-- Serveur: localhost
-- Généré le : Lundi 03 Septembre 2007 à 17:13
-- Version du serveur: 4.1.9
-- Version de PHP: 4.3.10
-- 
-- Base de données: `oyak`
-- 

-- --------------------------------------------------------

-- 
-- Structure de la table `pcfact_clients`
-- 

DROP TABLE IF EXISTS `pcfact_clients`;
CREATE TABLE `pcfact_clients` (
  `id` int(8) NOT NULL default '0',
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
  `balance` decimal(10,2) NOT NULL default '0.00',
  `timestamp` bigint(20) NOT NULL auto_increment,
  PRIMARY KEY  (`timestamp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci AUTO_INCREMENT=3109 ;

-- 
-- Contenu de la table `pcfact_clients`
-- 

INSERT INTO `pcfact_clients` (`id`, `civilite`, `nom`, `prenom`, `societe`, `adresse`, `adresse2`, `ville`, `code_postal`, `pays`, `telephone`, `fax`, `portable`, `email`, `clef`, `balance`, `timestamp`) VALUES (0, '', '', '', 'CLIENT DE PASSAGE', '', '', '', '', 33, '', '', '', '', 'C0', 0.00, 1),
(0, '', '', '', 'espace pierre declercq', '', '', 'Chilly Mazarin', '', 33, '', '', '', '', 'C1', 0.00, 2),
(0, '', '', '', 'A.L.M. (M-A1)', '', '', 'PARIS', '', 33, '', '', '', '', 'C10', 0.00, 3),
(0, '', '', '', 'SANDRA """"""', '', '', 'PARIS', '', 33, '', '', '', '', 'C100', 0.00, 4),
(0, '', '', '', 'LINARD FLEURISTE', '', '', 'BOURGES', '', 33, '', '', '', '', 'C1001', 0.00, 5),
(0, '', '', '', 'FLORAPOLIS (PC)', '', '', 'PARIS', '', 33, '', '', '', '', 'C1002', 0.00, 6),
(0, '', '', '', 'HOME DECORATION SARL', '', '', 'PARIS 6 me', '', 33, '', '', '', '', 'C1003', 0.00, 7),
(0, '', '', '', 'VERDIER', '', '', 'PARIS', '', 33, '', '', '', '', 'C1005', 0.00, 8),
(0, '', '', '', 'THOMAS FLEURS', '', '', 'LE PERRAY EN YVELINE', '', 33, '', '', '', '', 'C1006', 0.00, 9),
(0, '', '', '', 'ROUET', '', '', 'VILLEBON/YVETTE', '', 33, '', '', '', '', 'C1007', 0.00, 10);

-- --------------------------------------------------------

-- 
-- Structure de la table `pcfact_compteur`
-- 

DROP TABLE IF EXISTS `pcfact_compteur`;
CREATE TABLE `pcfact_compteur` (
  `compteur` bigint(12) NOT NULL auto_increment,
  `vendeur` varchar(16) NOT NULL default '',
  `temps` bigint(20) default '0',
  KEY `compteur` (`compteur`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=287 ;

-- 
-- Contenu de la table `pcfact_compteur`
-- 

INSERT INTO `pcfact_compteur` (`compteur`, `vendeur`, `temps`) VALUES (172, '5', 1178533213),
(284, '6', 1188606312),
(281, '2', 1183500232),
(166, '3', 1175443146),
(285, '6', 1188606321),
(165, '3', 1175442411),
(164, '3', 1175442312),
(163, '3', 1175442274),
(162, '3', 1175442211),
(173, '5', 1180208021),
(283, '2', 1183678573),
(262, '0', 1181503297),
(282, '2', 1183678564),
(286, '1', 1188831355);

-- --------------------------------------------------------

-- 
-- Structure de la table `pcfact_fournisseurs`
-- 

DROP TABLE IF EXISTS `pcfact_fournisseurs`;
CREATE TABLE `pcfact_fournisseurs` (
  `id` int(8) NOT NULL default '0',
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
  `timestamp` bigint(20) NOT NULL auto_increment,
  PRIMARY KEY  (`timestamp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci AUTO_INCREMENT=82 ;

-- 
-- Contenu de la table `pcfact_fournisseurs`
-- 

INSERT INTO `pcfact_fournisseurs` (`id`, `civilite`, `nom`, `prenom`, `societe`, `adresse`, `adresse2`, `ville`, `code_postal`, `pays`, `telephone`, `fax`, `portable`, `email`, `clef`, `timestamp`) VALUES (0, '', '', '', 'CI', '', '', 'COTE D''IVOIRE', '', 33, '', '', '', '', '1', 1),
(0, '', '', '', 'Afrique Sud - Cap mountai', '', '', 'Afrique du sud', '', 33, '', '', '', '', '10', 2),
(0, '', '', '', 'FLORAL PLANTES', '', '', 'COTE D''IVOIRE', '', 33, '', '', '', '', '11', 3),
(0, '', '', '', 'Eglin', '', '', 'cote d''ivoire', '', 33, '', '', '', '', '12', 4),
(0, '', '', '', 'SOTROPA - COTE D''IVOIRE', '', '', 'COTE D''IVOIRE', '', 33, '', '', '', '', '13', 5),
(0, '', '', '', 'EVER GREEN - EQUATEUR', '', '', 'Equateur', '', 33, '', '', '', '', '14', 6),
(0, '', '', '', 'Sri Lanka / Greenet', '', '', 'SRI LANKA', '', 33, '', '', '', '', '15', 7),
(0, '', '', '', 'TROPIC - MAURICE', '', '', 'ILE MAURICE', '', 33, '', '', '', '', '16', 8),
(0, '', '', '', 'BATHFIELD - MAURICE', '', '', 'ILE MAURICE', '', 33, '', '', '', '', '17', 9),
(0, '', '', '', 'IVOIRE FLEURS', '', '', 'COTE D''IVOIRE', '', 33, '', '', '', '', '18', 10);

-- --------------------------------------------------------

-- 
-- Structure de la table `pcfact_produits`
-- 

DROP TABLE IF EXISTS `pcfact_produits`;
CREATE TABLE `pcfact_produits` (
  `id` int(8) NOT NULL default '0',
  `titre` varchar(35) collate latin1_general_ci NOT NULL default '',
  `id_cat` int(4) NOT NULL default '1',
  `description` text collate latin1_general_ci NOT NULL,
  `prix_vente_ht` decimal(20,2) NOT NULL default '0.00',
  `prix_plancher_ht` decimal(10,2) default '0.00',
  `prix_stock_ht` decimal(10,0) NOT NULL default '0',
  `id_taux_tva` decimal(4,2) NOT NULL default '19.60',
  `stock` int(1) NOT NULL default '1',
  `barcode` varchar(13) collate latin1_general_ci NOT NULL default '',
  `fournisseur` varchar(7) collate latin1_general_ci default NULL,
  `clef` int(11) NOT NULL default '0',
  `poids` float NOT NULL default '0',
  `timestamp` bigint(20) unsigned NOT NULL auto_increment,
  PRIMARY KEY  (`timestamp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci AUTO_INCREMENT=1933 ;

-- 
-- Contenu de la table `pcfact_produits`
-- 

INSERT INTO `pcfact_produits` (`id`, `titre`, `id_cat`, `description`, `prix_vente_ht`, `prix_plancher_ht`, `prix_stock_ht`, `id_taux_tva`, `stock`, `barcode`, `fournisseur`, `clef`, `poids`, `timestamp`) VALUES (0, '****', 1, '', 0.00, 0.00, 0, 19.60, 1, '3700003000003', '3', 0, 1, 1),
(0, 'HIPERICUM', 1, '', 0.00, 0.00, 0, 19.60, 1, '3700003000010', '3', 1, 1, 2),
(0, 'ASPIDSTRA', 1, '', 0.00, 0.00, 0, 19.60, 1, '3700003000027', '3', 2, 1, 3),
(0, 'RUSCUS', 1, '', 0.00, 0.00, 0, 19.60, 1, '3700003000034', '3', 3, 1, 4),
(0, 'TREE FERN', 1, '', 0.00, 0.00, 0, 19.60, 1, '3700003000041', '3', 4, 1, 5),
(0, 'CRASPEDIA', 1, '', 0.00, 0.00, 0, 19.60, 1, '3700003000058', '3', 5, 1, 6),
(0, 'DENDROBIUM (ORCHIDEE)', 1, '', 0.00, 0.00, 0, 19.60, 1, '3700003000065', '3', 6, 1, 7),
(0, 'MOKARA (ORCHIDEE)', 1, '', 0.00, 0.00, 0, 19.60, 1, '3700003000072', '3', 7, 1, 8),
(0, 'ONCIDIUM JAUNE (ORCHIDEE)', 1, '', 0.00, 0.00, 0, 19.60, 1, '3700003000089', '3', 8, 1, 9),
(0, 'MARSHALL ANTHURIUM', 1, '', 0.00, 0.00, 0, 19.60, 1, '3700003000096', '3', 9, 1, 10);

-- --------------------------------------------------------

-- 
-- Structure de la table `pcfact_vendeurs`
-- 

DROP TABLE IF EXISTS `pcfact_vendeurs`;
CREATE TABLE `pcfact_vendeurs` (
  `id` tinyint(4) NOT NULL default '0',
  `nom` varchar(20) NOT NULL default '',
  `prenom` varchar(30) NOT NULL default '',
  `timestamp` bigint(20) NOT NULL auto_increment,
  PRIMARY KEY  (`timestamp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=14 ;

-- 
-- Contenu de la table `pcfact_vendeurs`
-- 

INSERT INTO `pcfact_vendeurs` (`id`, `nom`, `prenom`, `timestamp`) VALUES (1, 'Durand', 'Jean-Jacques', 7),
(2, 'Barrault', 'Maurice', 8),
(3, 'Mansard', 'Jacques', 9),
(5, 'Bertrand', 'jacques', 10),
(6, 'Chirac', 'Patrick', 11),
(121, 'K', 'S', 13);
