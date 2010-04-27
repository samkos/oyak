<?php

include("../inc/conf.php");

if ($header) {
 include("../inc/header.php");
?>
 <center>
<table border="0" cellpadding="2" cellspacing="0">
<tr >
    <td /> <a href="../query/get_data.php?clients=1&header=1">Liste Brute Client</a></td> <br>
    <td /> <a href="../query/get_data.php?clients=1&header=1&date=1">Date Brute Client</a></td>
</tr>
<tr >
    <td /> <a href="../query/get_data.php?fournisseurs=1&header=1">Liste Brute Fournisseur</a></td><br>
    <td /> <a href="../query/get_data.php?fournisseurs=1&header=1&date=1">Date Brute Fournisseur</a></td>
</tr>
<tr >
    <td /> <a href="../query/get_data.php?produits=1&header=1">Liste Brute Produit</a></td><br>
    <td /> <a href="../query/get_data.php?produits=1&header=1&date=1">Date Brute Produit</a></td>
</tr>
<tr >
    <td /> <a href="../query/get_data.php?vendeurs=1&header=1">Liste Brute Vendeur</a></td><br>
    <td /> <a href="../query/get_data.php?vendeurs=1&header=1&date=1">Date Brute Vendeur</a></td>
</tr>
<tr >
    <td /> <a href="../query/get_data.php?releases=1&header=1">Liste Brute releases</a></td>
</tr>
<tr >
    <td /> <a href="../admin/">Retour Admin</a></td>
</tr>
</table> </center>
<?php 
}

function date2string($s) {
  $s1 = str_replace(":","",$s);
	$s2 = str_replace("-","",$s1);
	$s3 = str_replace(" ","",$s2);
	return $s3;
}

if ($date) {
  if ($vendeurs) {$table="vendeurs";}
	if ($clients) {$table="clients";}
	if ($fournisseurs) {$table="fournisseurs";}
	if ($produits) {$table="produits";}
	
	if($table) {
    $query="select min(timestamp),max(timestamp) from ".$prefixe_table.$table;
  	//print $query;
    $req = mysql_query($query);
  	while($ligne = mysql_fetch_array($req))
  	{ print date2string($ligne["min(timestamp)"]).'!'.date2string($ligne["max(timestamp)"]).'=';
  	  if ($header) {print "<BR>";}
  	}
  }
  
}
else {
  
  
  if ($vendeurs) {
    $query="select id,nom,prenom,timestamp from ".$prefixe_table."vendeurs order by nom";
  	//print $query;
    $req = mysql_query($query);
  	while($ligne = mysql_fetch_array($req))
  	{ print $ligne["id"].'!'.$ligne[nom].'!'.$ligne[prenom].'!'.date2string($ligne[timestamp]).'=';
  	  if ($header) {print "<BR>";}
  	}
  }
  
  
  if ($clients) {
    $query="select societe,ville,clef,timestamp from ".$prefixe_table."clients";
  	//print $query;
    $req = mysql_query($query);
  	while($ligne = mysql_fetch_array($req))
  	{ print $ligne["societe"].'!'.$ligne[ville].'!'.$ligne[clef].'!'.date2string($ligne[timestamp]).'=';
  	  if ($header) {print "<BR>";}
  	}
  }
  
  if ($fournisseurs) {
    $query="select societe,ville,clef,timestamp from ".$prefixe_table."fournisseurs";
  	//print $query;
    $req = mysql_query($query);
  	while($ligne = mysql_fetch_array($req))
  	{ //print $ligne["societe"].'!'.$ligne[ville].'!'.$ligne[clef].'=';
  	  printf ("%s!%s!%04d!%s=",$ligne["societe"],$ligne[ville],$ligne[clef],date2string($ligne[timestamp]));
  	  if ($header) {print "<BR>";}
  	}
  }
  	 
  if ($produits) {
    $query="select barcode,clef,fournisseur,prix_vente_ht,prix_plancher_ht,poids,titre,timestamp from "
      .$prefixe_table."produits where clef<10000";
  	//print $query;
    $req = mysql_query($query);
  	while($ligne = mysql_fetch_array($req))
  	{ 
  	  #print $ligne["barcode"].'!'.$ligne[clef].'!'.$ligne[fournisseur].'!'.$ligne[prix_vente_ht].'!'.$ligne[prix_plancher_ht].'!'.$ligne[titre].'=';
  		//$clef=substr($ligne["barcode"],2,5);
  		$clef=sprintf("%04d",$ligne["clef"]);
  		$fournisseur=substr($ligne["barcode"],7,5);
  	  printf ("%s!%d!%04d!%7.2f!%7.2f!%7.2f!%s!%s=",$ligne["barcode"],$ligne[clef],$ligne[fournisseur],$ligne[prix_vente_ht],$ligne[prix_plancher_ht],$ligne[poids],$ligne[titre],date2string($ligne[timestamp]));
  	  if ($header) {print "<BR>";}
  	}
  }
  
  if ($releases) {
  	   $files = glob("$release_dir/*");
  		$i=0;
      foreach ($files as $filename) {
  	 			$filename=str_replace("$release_dir/","",$filename);
  				if ($filename!="CVS") {
        	      print "$i!$filename=";
  							$i=$i+1;
  				}
  
  
  	  if ($header) {print "<BR>";}
  	}
  }
}

?>