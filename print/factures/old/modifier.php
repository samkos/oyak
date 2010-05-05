<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>
<?php include("../verif.php"); ?>
<?php

$req2 = mysql_query("select id_clt,id_taux,escompte,date,type,etat from ".$prefixe_table."factures where num=\"$id_facture\"");
if (mysql_num_rows($req2)==0)
{
mysql_close($connect_db);
header("location: index.php");
exit();
}

if ($action == "delete_produit")
{
$req = mysql_query("delete from ".$prefixe_table."factures_produits where id=\"$id_produit_del\"");
}

if ($action == "ajouter")
{
$quantite_ajout = trim($quantite_ajout);
$quantite_ajout = strip_tags($quantite_ajout);
$quantite_ajout = str_replace('"','&quot;',$quantite_ajout);
$quantite_ajout = stripslashes($quantite_ajout);

   if ($id_produit_ajout == "0")
   {
   $msg = "Veuillez choisir un produit";
   }
   else
   {
   $quantite_ajout = addslashes($quantite_ajout);
   
   $req = mysql_query("insert into ".$prefixe_table."factures_produits values ('','$id_facture','$id_produit_ajout','$id_remise_ajout','$quantite_ajout')");
   
   mysql_close($connect_db);
   header("location: modifier.php?id_facture=$id_facture&msg=Produit+ajouté+!");
   exit();
   }
}

if ($action == "send")
{
$req = mysql_query("update ".$prefixe_table."factures set etat=\"$etat\",type=\"$type\",date=\"$date\",escompte=\"$escompte\",id_taux=\"$id_taux\",id_clt=\"$id_clt\" where num=\"$id_facture\"")or die(mysql_error());

mysql_close($connect_db);
header("location: modifier.php?id_facture=$id_facture&msg=Facture+modifiée+!");
exit();
}

$id_clt = mysql_result($req2,0,"id_clt");
$id_taux = mysql_result($req2,0,"id_taux");
$escompte = mysql_result($req2,0,"escompte");
$date = mysql_result($req2,0,"date");
$type = mysql_result($req2,0,"type");
$etat = mysql_result($req2,0,"etat");

?>
<?php include("../inc/header.php"); ?>

<?php

if ($msg != "")
{
$msg = str_replace("+"," ",$msg);
echo("<center><font color=\"#ff0000\"><b>$msg</b></font></center><br>");
}

?>

<form action="modifier.php?id_facture=<?php echo("$id_facture"); ?>" method="post">
<input type="hidden" name="action" value="send">

<table border="0" align="center">
   <tr>
      <td><b>Client</b> :</td>
	  <td><select name="id_clt" style="width: 320px">
	  <?php
	  
	  $req = mysql_query("select id,nom,prenom from ".$prefixe_table."clients order by nom,prenom");
	  while($ligne = mysql_fetch_array($req))
	  {
	  $id = $ligne["id"];
	  $nom = $ligne["nom"];
	  $prenom = $ligne["prenom"];
	  
	  echo("<option value=\"$id\"");
	  if ($id == $id_clt){echo(" selected");}
	  echo(">$nom $prenom</option>");
	  }
	  
	  ?>
	  </select></td>
   </tr>
   <tr>
      <td><b>Taux T.V.A</b> :</td>
	  <td><select name="id_taux" style="width: 320px">
	  <?php
	  
	  $req = mysql_query("select * from ".$prefixe_table."taux_tva order by taux");
	  while($ligne = mysql_fetch_array($req))
	  {
	  $id = $ligne["id"];
	  $taux = $ligne["taux"];
	  echo("<option value=\"$id\"");
	  if ($id == $id_taux){echo(" selected");}
	  echo(">$taux</option>");
	  }
	  
	  ?>
	  </select></td>
   </tr>
   <tr>
      <td><b>Escompte</b> :</td>
	  <td><input type="text" name="escompte" size="15" value="<?php echo("$escompte"); ?>"> %</td>
   </tr>
   <tr>
      <td><b>Date</b> :</td>
	  <td><input type="text" name="date" size="50" value="<?php echo("$date"); ?>"></td>
   </tr>
   <tr>
      <td><b>Type</b> :</td>
	  <td><input type="radio" name="type" value="d" <?php if($type == "d"){echo("checked");} ?>> Devis 
	  <input type="radio" name="type" value="f" <?php if($type == "f"){echo("checked");} ?>> Facture</td>
   </tr>
   <tr>
      <td><b>Etat</b> :</td>
	  <td><input type="radio" name="etat" value="0" <?php if($etat == "0"){echo("checked");} ?>> En cours
	  <input type="radio" name="etat" value="1" <?php if($etat == "1"){echo("checked");} ?>> Terminé
	  <input type="radio" name="etat" value="2" <?php if($etat == "2"){echo("checked");} ?>> Terminé / payé  
	  <input type="radio" name="etat" value="3" <?php if($etat == "3"){echo("checked");} ?>> Annulé</td>
   </tr>
</table>

<br>

<center><input type="submit" value="Modifier"></center>

</form>

<table border="0" align="center" cellpadding="3" cellspacing="1" bgcolor="#000000" width="770">
   <tr>
      <td bgcolor="#99CCCC" align="center" width="10%"><b>Référence</b></td>
	  <td bgcolor="#99CCCC" align="center" width="30%"><b>Titre</b></td>
	  <td bgcolor="#99CCCC" align="center" width="10%"><b>Prix HT</b></td>
	  <td bgcolor="#99CCCC" align="center" width="10%"><b>Q</b></td>
	  <td bgcolor="#99CCCC" align="center" width="10%"><b>R%</b></td>
	  <td bgcolor="#99CCCC" align="center" width="15%"><b>Total HT</b></td>
	  <td bgcolor="#99CCCC" align="center" width="15%"><b>Actions</b></td>
   </tr>
<?php

function titre_article($id)
{
global $prefixe_table;
$req = mysql_query("select titre from ".$prefixe_table."produits where id=\"$id\"");
return mysql_result($req,0,"titre");
}

function ref_article($id)
{
global $prefixe_table;
$req = mysql_query("select id from ".$prefixe_table."produits where id=\"$id\"");
return mysql_result($req,0,"id");
}

function prix_article($id)
{
global $prefixe_table;
$req = mysql_query("select prix_vente_ht from ".$prefixe_table."produits where id=\"$id\"");
return mysql_result($req,0,"prix_vente_ht");
}

function taux_remise($id)
{
global $prefixe_table;
$req = mysql_query("select taux from ".$prefixe_table."remises where id=\"$id\"");
return mysql_result($req,0,"taux");
}

$req = mysql_query("select * from ".$prefixe_table."factures_produits where num_fact=\"$id_facture\"");
while($ligne = mysql_fetch_array($req))
{
$id = $ligne["id"];
$id_produit = $ligne["id_produit"];
$id_remise = $ligne["id_remise"];
$quantite = $ligne["quantite"];

if($id_remise != "0"){$taux_r = taux_remise($id_remise);}else{$taux_r = 0;}

$titre = titre_article($id_produit);
$prix = prix_article($id_produit);

$ref = ref_article($id_produit);
$ref = sprintf("%08s",$ref);

$total_ht = $prix*$quantite;

if($id_remise != "0")
{
$remise = $total_ht*$taux_r/100;
$total_ht = $total_ht-$remise;
}

echo("   <tr>
	  <td bgcolor=\"#ffffff\" align=\"center\">#$ref</td>
	  <td bgcolor=\"#ffffff\" align=\"center\">$titre</td>
	  <td bgcolor=\"#ffffff\" align=\"center\">$prix €</td>
	  <td bgcolor=\"#ffffff\" align=\"center\">$quantite</td>
	  <td bgcolor=\"#ffffff\" align=\"center\">$taux_r %</td>
	  <td bgcolor=\"#ffffff\" align=\"center\">$total_ht €</td>
	  <td bgcolor=\"#ffffff\" align=\"center\"><a href=\"#null\" onclick=\"javascript:if(confirm('Etes-vous sûr de vouloir supprimer ce produit de la facture &quot;$titre&quot; ?')) document.location.replace('modifier.php?action=delete_produit&id_produit_del=$id&id_facture=$id_facture');\">Supprimer</a></td>
   </tr>");
}

?>
</table>

<br>

<form action="modifier.php?id_facture=<?php echo("$id_facture"); ?>" method="post">
<input type="hidden" name="action" value="ajouter">

<table border="0" align="center">
   <tr>
      <td><b>Produit</b> :</td>
	  <td><select name="id_produit_ajout" style="width: 320px">
	  <option value="0">Choisissez</option>
	  <?php
	  
	  function liste_produits($cat,$titre_cat)
	  {
	  global $id_produit_ajout,$prefixe_table;
	  
	  $req = mysql_query("select id,titre from ".$prefixe_table."produits where id_cat=\"$cat\" order by id");
	  while($ligne = mysql_fetch_array($req))
	  {
	  $id = $ligne["id"];
	  $titre = $ligne["titre"];
	  
	  echo("<option value=\"$id\"");
	  if ($id == $id_produit_ajout){echo(" selected");}
	  echo(">$titre_cat &gt; $titre</option>");
	  }
	  }
	  
	  $req = mysql_query("select id,titre from ".$prefixe_table."produits_cat order by titre");
	  while($ligne = mysql_fetch_array($req))
	  {
	  $id = $ligne["id"];
	  $titre_cat = $ligne["titre"];
	  liste_produits($id,$titre_cat);
	  }
	  
	  ?>
	  </select></td>
   </tr>
   <tr>
      <td><b>Remise</b> :</td>
	  <td><select name="id_remise_ajout" style="width: 320px">
	  <option value="0">Choisissez (facultatif)</option>
	  <?php
	  
	  $req = mysql_query("select id,taux from ".$prefixe_table."remises order by id");
	  while($ligne = mysql_fetch_array($req))
	  {
	  $id = $ligne["id"];
	  $taux = $ligne["taux"];
	  
	  echo("<option value=\"$id\"");
	  if ($id == $id_remise_ajout){echo(" selected");}
	  echo(">$taux %</option>");
	  }
	  
	  ?>
	  </select></td>
   </tr>
   <tr>
      <td><b>Quantité</b> :</td>
	  <td><input type="text" name="quantite_ajout" size="15" value="<?php echo("$quantite_ajout"); ?>"> %</td>
   </tr>
</table>

<br>

<center><input type="submit" value="Ajouter"></center>

</form>

<center>
<a href="index.php">Retour</a>
</center>

<?php include("../inc/footer.php"); ?>