<?php include("../../inc/conf.php"); ?>
<?php include("../../inc/fonctions.php"); ?>
<?php

$req = mysql_query("select titre,id_cat,description,prix_vente_ht,id_taux_tva,stock,barcode,clef,fournisseur,poids from ".$prefixe_table."produits where clef=\"$clef_param\"");
if (mysql_num_rows($req)==0)
{
mysql_close($connect_db);
header("location: index.php");
exit();
}

if ($action == "send")
{
  $titre = trim($titre);
  $titre = strip_tags($titre);
  $titre = str_replace('"','&quot;',$titre);
  $titre = stripslashes($titre);
  
  $barcode = trim($barcode);
  $barcode = strip_tags($barcode);
  $barcode = str_replace('"','&quot;',$barcode);
  $barcode = stripslashes($barcode);

  $clef = trim($clef);
  $clef = strip_tags($clef);
  $clef = str_replace('"','&quot;',$clef);
  $clef = stripslashes($clef);

  $fournisseur = trim($fournisseur);
  $fournisseur = strip_tags($fournisseur);
  $fournisseur = str_replace('"','&quot;',$fournisseur);
  $fournisseur = stripslashes($fournisseur);

  $description = trim($description);
  $description = strip_tags($description);
  $description = str_replace('"','&quot;',$description);
  $description = stripslashes($description);

  $prix_vente_ht = trim($prix_vente_ht);
  $prix_vente_ht = strip_tags($prix_vente_ht);
  $prix_vente_ht = str_replace('"','&quot;',$prix_vente_ht);
  $prix_vente_ht = stripslashes($prix_vente_ht);

  $poids = trim($poids);
  $poids = strip_tags($poids);
  $poids = str_replace('"','&quot;',$poids);
  $poids = stripslashes($poids);

  $id_taux_tva = trim($id_taux_tva);
  $id_taux_tva = strip_tags($id_taux_tva);
  $id_taux_tva = str_replace('"','&quot;',$id_taux_tva);
  $id_taux_tva = stripslashes($id_taux_tva);

  $titre = addslashes($titre);
  $description = addslashes($description);
  $prix_vente_ht = addslashes($prix_vente_ht);
  $id_taux_tva = addslashes($id_taux_tva);
 
  $commande = "update ".$prefixe_table."produits set description=\"$description\",titre=\"$titre\",fournisseur=\"$fournisseur\" where clef=\"$clef_param\"";

  //print "<BR> commande=$commande";

  $req = mysql_query($commande);
  
  mysql_close($connect_db);
  header("location: index.php");
  exit();

}

$titre = mysql_result($req,0,"titre");
$description = mysql_result($req,0,"description");
$prix_vente_ht = mysql_result($req,0,"prix_vente_ht");
$id_taux_tva = mysql_result($req,0,"id_taux_tva");
$stock = mysql_result($req,0,"stock");
$cat = mysql_result($req,0,"id_cat");
$barcode = mysql_result($req,0,"barcode");
$clef = mysql_result($req,0,"clef");
$poids = mysql_result($req,0,"poids");
$fournisseur = mysql_result($req,0,"fournisseur");


?>
<?php include("../../inc/header.php"); ?>

<?php

if ($msg != "")
{
$msg = str_replace("+"," ",$msg);
echo("<center><font color=\"#ff0000\"><b>$msg</b></font></center><br>");
}

?>

<form action="modifier_param.php?clef_param=<?php echo("$clef"); ?>" method="post">
<input type="hidden" name="action" value="send">
<input type="hidden" name="start" value="<?php print $start ?>">
<table border="0" align="center">
   <tr>
   <tr>
      <td><b>Clef</b> :</td>
	  <td><input type="text" name="clef" size="15" value="<?php echo("$clef"); ?>"> </td>
   </tr>	 
   <tr>
      <td><b>Nom</b> :</td>
	  <td><input type="text" name="fournisseur" size="15" value="<?php echo("$fournisseur"); ?>"> </td>
   </tr>	 
   <tr>
      <td><b>Description</b> :</td>
	  <td><textarea name="description" cols="49" rows="15"><?php echo("$description"); ?></textarea></td>
   </tr>
   <tr> 
      <td><b>Valeur</b> :</td>
	  <td><input type="text" name="titre" size="50" value="<?php echo("$titre"); ?>"></td>
   </tr>
</table>

<br>

<center><input type="submit" value="Modifier"></center>

</form>

<br>

<center>
<a href="index.php?start=<?php echo $start?>">Retour</a>
</center>

<?php include("../../inc/footer.php"); ?>