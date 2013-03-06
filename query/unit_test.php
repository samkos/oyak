<?php 

include("../inc/conf.php");
include("../inc/fonctions.php");
include("../verif.php"); 


if ($header) {
 include("../inc/header.php"); 
 print "<center>";
}
$commande_defaut="C1;3700006000291!6!29!23/06/1969!1!2.5;3700054000809!54!80!1/1/45!10!2.7";
$vendeur_defaut=1;

if (!$commande) {
  $commande=$commande_defaut;
	$vendeur=$vendeur_defaut;
}

if ($commande) {
	$time=time();
  $query="insert into ".$prefixe_table."compteur values ('','$vendeur','$time')";
	//print $query;
  $req = mysql_query($query);

	$query="select compteur from  ".$prefixe_table."compteur where temps=$time";
	$req = mysql_query($query);
	while($ligne = mysql_fetch_array($req))
	{ $compteur = $ligne["compteur"];}
		
	$compteur=sprintf("%05d",$compteur);
  $tag_date=date("Ymd");
	$out_file=sprintf("$commande_dir\\"."$tag_date$compteur");

	 $fout=fopen($out_file,"w");
   $out_commande=sprintf("%02d;$commande",$vendeur);
	 fwrite($fout,$out_commande);
	
	$query="delete  from ".$prefixe_table."compteur where (compteur<".($compteur-5)." and vendeur='$vendeur')";
	//print "<BR>".$query;
	$req = mysql_query($query);
	
	mysql_close($connect_db);
	
}

if ($header) {
   print "<BR> <a href='unit_test.php?commande=C1;3700006000291!6!29!01/04/2007!1!2.5;3700054000809!10!2.7;&vendeur=3'>Ajout d'une commande factice</a>";
   print "<center> <BR> commande = $commande <BR> compteur=$compteur";
	 print "<BR> <BR> <a href='../admin/index.php>  Retour Administration\n";
}
else {
    header("location: ../admin/index.php?message=Nouvelle Commande n° $compteur passée ");	
}
	 
?>