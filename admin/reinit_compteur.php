<?php include("../inc/conf.php"); 
 include("../inc/fonctions.php"); 

  $query="truncate table  ".$prefixe_table."compteur";
	//print $query;
  $req = mysql_query($query);
	
	mysql_close($connect_db);

//   print "<BR> <a href='unit_test.php?commande=test1&vendeur=0'>Test ecriture fichier test1</a>";
  // print "compteur remis a zero!";	 
	 header("location: index.php?message=Compteur a zero");
				
?>