<?php

include("../inc/conf.php");

if ($header) {
 include("../inc/header.php");
?>
 <center>
<table border="0" cellpadding="2" cellspacing="0">
<tr>
  <td colspan=4> <b> nouvelle version avec timestamp </b> </td>
</tr>
<tr >
    <td /> <a href="../query/get_data2.php?clients=1&header=1">Liste Brute Client</a></td> <br>
    <td /> <a href="../query/get_data2.php?clients=1&header=1&date=1">Date Brute Client</a></td>
    <td /> <a href="../query/get_data2.php?clients=1&header=1&from=45">liste Brute Client>45</a></td>
</tr>
<tr >
    <td /> <a href="../query/get_data2.php?fournisseurs=1&header=1">Liste Brute Fournisseur</a></td><br>
    <td /> <a href="../query/get_data2.php?fournisseurs=1&header=1&date=1">Date Brute Fournisseur</a></td>
    <td /> <a href="../query/get_data2.php?fournisseurs=1&header=1&from=20">Date Brute Fournisseur>20</a></td>
</tr>
<tr >
    <td /> <a href="../query/get_data2.php?produits=1&header=1">Liste Brute Produit</a></td><br>
    <td /> <a href="../query/get_data2.php?produits=1&header=1&date=1">Date Brute Produit</a></td>
    <td /> <a href="../query/get_data2.php?produits=1&header=1&from=45">liste Brute Produit>45</a></td>
</tr>
<tr >
    <td /> <a href="../query/get_data2.php?vendeurs=1&header=1">Liste Brute Vendeur</a></td><br>
    <td /> <a href="../query/get_data2.php?vendeurs=1&header=1&date=1">Date Brute Vendeur</a></td>
    <td /> <a href="../query/get_data2.php?vendeurs=1&header=1&from=2">liste Brute Vendeur>2</a></td>
</tr>
<tr >
    <td /> <a href="../query/get_data2.php?releases=1&header=1">Liste Brute releases</a></td>
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

if (isset($from)) {
  $where="where timestamp>=$from";
}
else {
  $where="";
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
    $query="select id,nom,prenom,timestamp from ".$prefixe_table."vendeurs $where order by nom ";
    //print $query;
    $req = mysql_query($query);
  	while($ligne = mysql_fetch_array($req))
	  {     
	  print $ligne["id"].'!'.$ligne[nom].'!'.$ligne[prenom].'!'.($ligne[timestamp]).'=';
  	  if ($header) {print "<BR>";}
  	}
  }
  
  
  if ($clients) {
    $query="select societe,ville,clef,balance,timestamp from ".$prefixe_table."clients $where";
    //print $query;
    $req = mysql_query($query);
  	while($ligne = mysql_fetch_array($req))
  	{ print $ligne["societe"].'!'.$ligne[ville].'!'.$ligne[clef]
	    .'!'.$ligne[balance].'!'.($ligne[timestamp]).'=';
  	  if ($header) {print "<BR>";}
  	}
  }
  
  if ($fournisseurs) {
    $query="select societe,ville,clef,timestamp from ".$prefixe_table."fournisseurs $where";
  	//print $query;
    $req = mysql_query($query);
  	while($ligne = mysql_fetch_array($req))
  	{ //print $ligne["societe"].'!'.$ligne[ville].'!'.$ligne[clef].'=';
  	  printf ("%s!%s!%04d!%s=",$ligne["societe"],$ligne[ville],$ligne[clef],($ligne[timestamp]));
  	  if ($header) {print "<BR>";}
  	}
  }
  	 
  if ($produits) {
    $query="select barcode,clef,fournisseur,prix_vente_ht,prix_plancher_ht,prix_stock_ht,stock,poids,titre,timestamp from ".$prefixe_table."produits $where" ;
  	//print $query;
    $req = mysql_query($query);
  	while($ligne = mysql_fetch_array($req))
  	{ 
  	  #print $ligne["barcode"].'!'.$ligne[clef].'!'.$ligne[fournisseur].'!'.$ligne[prix_vente_ht].'!'.$ligne[prix_plancher_ht].'!'.$ligne[titre].'=';
  		//$clef=substr($ligne["barcode"],2,5);
  		$clef=sprintf("%04d",$ligne["clef"]);
  		$fournisseur=substr($ligne["barcode"],7,5);
  	  printf ("%s!%d!%04d!%7.2f!%7.2f!%7.2f!%7.2f!%7.2f!%s!%s=",
		  $ligne["barcode"],$ligne[clef],$ligne[fournisseur],
		  $ligne[prix_vente_ht],$ligne[prix_plancher_ht],$ligne[prix_stock_ht],
		  $ligne[stock],$ligne[poids],$ligne[titre],($ligne[timestamp]));
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