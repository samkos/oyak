use oyak;

DROP TABLE IF EXISTS `pcfact_produits`;
CREATE TABLE `pcfact_produits` (
  `id` int(8) NOT NULL auto_increment,
  `titre` varchar(35) collate latin1_general_ci NOT NULL default '',
  `id_cat` int(4) NOT NULL default '1',
  `description` text collate latin1_general_ci NOT NULL,
  `prix_vente_ht` decimal(20,2) NOT NULL default '0.00',
  `id_taux_tva` decimal(4,2) NOT NULL default '19.60',
  `stock` int(1) NOT NULL default '1',
  `barcode` varchar(13) collate latin1_general_ci NOT NULL default '',
  KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci AUTO_INCREMENT=868 ;



DROP TABLE IF EXISTS `pcfact_clients`;
CREATE TABLE `pcfact_clients` (
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
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci AUTO_INCREMENT=577 ;


