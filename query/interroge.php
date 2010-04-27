<?php

include("../inc/conf.php");


if ($header) {
  include("../inc/header.php"); 
  print "<center>";
}

if ($header) {
  // vendeur, client, produit, fournisseur
  print "<BR> <a href='interroge.php?requete=0;C3183;1!5&header=1'>Test requete</a>";
  print "<BR> <br> <a href='../admin/'>Retour a l'administration </a> <br />  <br>";
}

if ($requete) {
  $articles=split(";",$requete);
  $vendeur=$articles[0];	
  $client=$articles[1];	
  $produit=$articles[2];	
  $fournisseur=$articles[3];	
    

  print "0!";
  if ($client) {
  	$filename="c:/solcli/$client";
  	if (file_exists($filename)) {
		$lines = file($filename);
		foreach ($lines as $line_num => $line) {
			$line=str_replace("ı","!",$line);
    		echo "$line\n";
		}
  	}
  	else {
  		print "Pas de renseignements disponibles! sur le client $client";	
  	}
  }
  else
  {
	  print "from serveur! Interrogation recue ! vendeur=$vendeur ! client=$client ! produit=$produit ! fournisseur=$fournisseur";
  }
}

	 
?>