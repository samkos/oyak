<?php

// Configuration mySQL

//error_reporting((E_ALL ^ E_NOTICE) & ~E_DEPRECATED & E_USER_DEPRECATED);
error_reporting((E_ALL ^ E_NOTICE));

extract($_POST, EXTR_SKIP);
extract($_GET, EXTR_SKIP);

$host_db = "localhost";
$user_db = "root";
$password_db = "";
$bdd_db = "oyak";

$prefixe_dossier = "phpmyfactures/"; // url du dossier où se trouvera le script (Ne pas commencer par un / mais terminer par un / exemple : factures/ )
$prefixe_table = "pcfact_"; // préfixe des tables (par défaut)

$pseudo_conf = "ciia"; // nom d'utilisateur pour l'espace d'administration
$password_conf = "ciia"; // mot de passe pour y accéder

$work_dir='work';
$tex_file=$work_dir.'\barcodes.tex';
$python_file=$work_dir.'\what.py';
$latex="compile.bat";
$make_ps="2ps.bat";
$python="python ";
$gsprint="gsprint";
$release_dir="../dist/releases";
$commande_dir="c:\\ventesjour\\";

//require "debug.php";
$version="0.4";



// ne pas toucher se qui suit !
$connect_db = mysql_connect($host_db,$user_db,$password_db);
mysql_select_db($bdd_db,$connect_db);


?>
