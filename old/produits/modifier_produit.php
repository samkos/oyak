<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>
<?php

$req = mysql_query("select titre,id_cat,description,prix_vente_ht,id_taux_tva,stock,barcode,clef,fournisseur,poids from ".$prefixe_table."produits where id=\"$id_produit\"");
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

	if ($titre == "")
	{
	$msg = "Veuillez introduire un titre";
	}
	else
	{
	   if ($description == "")
	   {
	   $msg = "Veuillez introduire la description";
	   }
	   else
	   {
	      if ($prix_vente_ht == "")
		  {
		  $msg = "Veuillez introduire le prix de vente ht";
		  }
		  else
		  {
		     if ($id_taux_tva == "0")
			 {
			 $msg = "Veuillez sélectionner la tva";
			 }
			 else
			 {
			    if ($cat == 0)
				{
				$msg = "Veuillez choisir une catégorie";
				}
				else
				{
				$titre = addslashes($titre);
				$description = addslashes($description);
				$prix_vente_ht = addslashes($prix_vente_ht);
				$id_taux_tva = addslashes($id_taux_tva);
				
				$req = mysql_query("update ".$prefixe_table."produits set id_cat=\"$cat\",stock=\"$stock\",id_taux_tva=\"$id_taux_tva\",prix_vente_ht=\"$prix_vente_ht\",description=\"$description\",titre=\"$titre\",barcode=\"$barcode\",fournisseur=\"$fournisseur\",clef=\"$clef\",poids=\"$poids\",timestamp=NULL where id=\"$id_produit\"");
				
				mysql_close($connect_db);
				header("location: modifier_produit.php?id_produit=$id_produit&msg=Produit+modifié+!");
				exit();
				}
			 }
		  }
	   }
	}
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
<?php include("../inc/header.php"); ?>

<?php

if ($msg != "")
{
$msg = str_replace("+"," ",$msg);
echo("<center><font color=\"#ff0000\"><b>$msg</b></font></center><br>");
}

?>

<form action="modifier_produit.php?id_produit=<?php echo("$id_produit"); ?>" method="post">
<input type="hidden" name="action" value="send">
<input type="hidden" name="start" value="<?php print $start ?>">
<table border="0" align="center">
   <tr>
      <td><b>Catégorie</b> :</td>
	  <td><select name="cat">
	  <?php
	  
	  $req = mysql_query("select * from ".$prefixe_table."produits_cat order by titre");
	  while($ligne = mysql_fetch_array($req))
	  {
	  $id = $ligne["id"];
	  $titre_cat = $ligne["titre"];
	  echo("<option value=\"$id\"");
	  if ($id == $cat) echo(" selected");
	  echo(">$titre_cat</option>");
	  }
	  
	  ?>
	  </select></td>
   </tr>
   <tr>
      <td><b>Titre</b> :</td>
	  <td><input type="text" name="titre" size="50" value="<?php echo("$titre"); ?>"></td>
   </tr>
   <tr>
      <td><b>Code Barre</b> :</td>
	  <td><input type="text" name="barcode" size="15" value="<?php echo("$barcode"); ?>"> </td>
   </tr>	 
   <tr>
      <td><b>Clef</b> :</td>
	  <td><input type="text" name="clef" size="15" value="<?php echo("$clef"); ?>"> </td>
   </tr>	 
	 <input type="hidden" name="description" value="blabla">
<!--   <tr>
      <td><b>Description</b> :</td>
	  <td><textarea name="description" cols="49" rows="15"><?php echo("$description"); ?></textarea></td>
   </tr>
   <tr> -->
   <tr>
      <td><b>Fournisseur</b> :</td>
	  <td><input type="text" name="fournisseur" size="15" value="<?php echo("$fournisseur"); ?>"> </td>
   </tr>	 

      <td><b>Prix HT</b> :</td>
	  <td><input type="text" name="prix_vente_ht" size="50" value="<?php echo("$prix_vente_ht"); ?>"></td>
   </tr>
	 	 <input type="hidden" name="id_taux_tva" value="18.6">
<!--
   <tr>
      <td><b>Taux T.V.A</b> :</td>
	  <td><select name="id_taux_tva" style="width: 320px">
	  <option value="0">Choisissez</option>
	  <?php
	  
	  $req = mysql_query("select * from ".$prefixe_table."taux_tva order by taux");
	  while($ligne = mysql_fetch_array($req))
	  {
	  $id = $ligne["id"];
	  $taux = $ligne["taux"];
	  echo("<option value=\"$id\"");
	  if ($id == $id_taux_tva){echo(" selected");}
	  echo(">$taux</option>");
	  }
	  
	  ?>
	  </select></td>
   </tr>
-->
	 <input type="hidden" name="stock" value="1">
   <tr>
      <td><b>Poids</b> :</td>
	  <td><input type="text" name="poids" size="15" value="<?php echo("$poids"); ?>"> </td>
   </tr>	 
<!--
   <tr>
      <td><b>Gestion do stock</b> :</td>
	  <td><input type="checkbox" name="stock" value="1" <?php if($stock == "1"){echo("checked");} ?>> Oui</td>
   </tr>
-->
</table>

<br>

<center><input type="submit" value="Modifier"></center>

</form>

<br>

<center>
<a href="index.php?start=<?php echo $start?>">Retour</a>
</center>

<?php include("../inc/footer.php"); ?>