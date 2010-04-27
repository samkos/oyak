<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>
<?php

$req = mysql_query("select civilite,nom,prenom,clef,adresse,adresse2,ville,code_postal,telephone,fax,portable,email,societe,pays from ".$prefixe_table."fournisseurs where id=\"$id_fournisseur\"");
if (mysql_num_rows($req)==0)
{
mysql_close($connect_db);
header("location: index.php");
exit();
}

if ($action == "send")
{
$nom = trim($nom);
$nom = strip_tags($nom);
$nom = str_replace('"','&quot;',$nom);
$nom = stripslashes($nom);

$prenom = trim($prenom);
$prenom = strip_tags($prenom);
$prenom = str_replace('"','&quot;',$prenom);
$prenom = stripslashes($prenom);

$clef = trim($clef);
$clef = strip_tags($clef);
$clef = str_replace('"','&quot;',$clef);
$clef = stripslashes($clef);

$adresse = trim($adresse);
$adresse = strip_tags($adresse);
$adresse = str_replace('"','&quot;',$adresse);
$adresse = stripslashes($adresse);

$adresse2 = trim($adresse2);
$adresse2 = strip_tags($adresse2);
$adresse2 = str_replace('"','&quot;',$adresse2);
$adresse2 = stripslashes($adresse2);

$ville = trim($ville);
$ville = strip_tags($ville);
$ville = str_replace('"','&quot;',$ville);
$ville = stripslashes($ville);

$code_postal = trim($code_postal);
$code_postal = strip_tags($code_postal);
$code_postal = str_replace('"','&quot;',$code_postal);
$code_postal = stripslashes($code_postal);

$telephone = trim($telephone);
$telephone = strip_tags($telephone);
$telephone = str_replace('"','&quot;',$telephone);
$telephone = stripslashes($telephone);

$fax = trim($fax);
$fax = strip_tags($fax);
$fax = str_replace('"','&quot;',$fax);
$fax = stripslashes($fax);

$portable = trim($portable);
$portable = strip_tags($portable);
$portable = str_replace('"','&quot;',$portable);
$portable = stripslashes($portable);

$email = trim($email);
$email = strip_tags($email);
$email = str_replace('"','&quot;',$email);
$email = stripslashes($email);

$societe = trim($societe);
$societe = strip_tags($societe);
$societe = str_replace('"','&quot;',$societe);
$societe = stripslashes($societe);

	if ($civilite == "0")
	{
	$civilite="1";
	}

	{
    	$nom = addslashes($nom);
  		$prenom = addslashes($prenom);
  		$clef = addslashes($clef);
  		$societe = addslashes($societe);
  		$adresse = addslashes($adresse);
  		$adresse2 = addslashes($adresse2);
  		$ville = addslashes($ville);
  		$code_postal = addslashes($code_postal);
  		$telephone = addslashes($telephone);
  		$fax = addslashes($fax);
  		$portable = addslashes($portable);
  		$email = addslashes($email);
  		
  		$req = mysql_query("update ".$prefixe_table."fournisseurs set clef=\"$clef\",pays=\"$pays\",email=\"$email\",portable=\"$portable\",fax=\"$fax\",telephone=\"$telephone\",code_postal=\"$code_postal\",nom=\"$nom\",prenom=\"$prenom\",societe=\"$societe\",adresse=\"$adresse\",adresse2=\"$adresse2\",ville=\"$ville\",timestamp=NULL where id=\"$id_fournisseur\"") or die(mysql_error());
  		
  		mysql_close($connect_db);
  		header("location: modifier_fournisseur.php?id_fournisseur=$id_fournisseur&msg=Fournisseur+modifié+!");
  		exit();
	}
}

$civilite = mysql_result($req,0,"civilite");
$nom = mysql_result($req,0,"nom");
$prenom = mysql_result($req,0,"prenom");
$clef = mysql_result($req,0,"clef");
$societe = mysql_result($req,0,"societe");
$adresse = mysql_result($req,0,"adresse");
$adresse2 = mysql_result($req,0,"adresse2");
$ville = mysql_result($req,0,"ville");
$code_postal = mysql_result($req,0,"code_postal");
$pays = mysql_result($req,0,"pays");
$telephone = mysql_result($req,0,"telephone");
$fax = mysql_result($req,0,"fax");
$portable = mysql_result($req,0,"portable");
$email = mysql_result($req,0,"email");

?>
<?php include("../inc/header.php"); ?>

<?php

if ($msg != "")
{
$msg = str_replace("+"," ",$msg);
echo("<center><font color=\"#ff0000\"><b>$msg</b></font></center><br>");
}

?>

<form action="modifier_fournisseur.php?id_fournisseur=<?php echo("$id_fournisseur"); ?>" method="post">
<input type="hidden" name="action" value="send">

<table border="0" align="center">
   <tr>
      <td><b>Civilité</b> :</td>
	  <td><select name="civilite" style="width: 320px">
	  <option value="0">Choisissez</option>
	  <option value="mr" <?php if ($civilite == "mr"){echo(" selected");} ?>>Monsieur</option>
	  <option value="mme" <?php if ($civilite == "mme"){echo(" selected");} ?>>Madame</option>
	  <option value="mlle" <?php if ($civilite == "mlle"){echo(" selected");} ?>>Mademoiselle</option>
	  </select></td>
   </tr>
   <tr>
      <td><b>Nom</b> :</td>
	  <td><input type="text" name="nom" size="50" value="<?php echo("$nom"); ?>"></td>
   </tr>
   <tr>
      <td><b>Prénom</b> :</td>
	  <td><input type="text" name="prenom" size="50" value="<?php echo("$prenom"); ?>"></td>
   </tr>
   <tr>
      <td>Clef :</td>
	  <td><input type="text" name="clef" size="50" value="<?php echo("$clef"); ?>"></td>
   </tr>
   <tr>
      <td>Société :</td>
	  <td><input type="text" name="societe" size="50" value="<?php echo("$societe"); ?>"></td>
   </tr>
   <tr>
      <td>Adresse :</td>
	  <td><input type="text" name="adresse" size="50" value="<?php echo("$adresse"); ?>"></td>
   </tr>
   <tr>
      <td></td>
	  <td><input type="text" name="adresse2" size="50" value="<?php echo("$adresse2"); ?>"></td>
   </tr>
   <tr>
      <td>Ville :</td>
	  <td><input type="text" name="ville" size="50" value="<?php echo("$ville"); ?>"></td>
   </tr>
   <tr>
      <td>Code Postal :</td>
	  <td><input type="text" name="code_postal" size="15" value="<?php echo("$code_postal"); ?>"></td>
   </tr>
   <tr>
      <td><b>Pays</b> :</td>
	  <td><select name="pays" style="width: 320px">
	  <option value="0">Choisissez</option>
	  <?php
	  
	  $req = mysql_query("select id,pays from ".$prefixe_table."pays order by pays");
	  while($ligne = mysql_fetch_array($req))
	  {
	  $id_pays = $ligne["id"];
	  $nom_pays = $ligne["pays"];
	  echo("<option value=\"$id_pays\"");
	  if ($id_pays == $pays){echo(" selected");}
	  echo(">$nom_pays</option>");
	  }
	  
	  ?>
	  </select></td>
   </tr>
   <tr>
      <td>Téléphone :</td>
	  <td><input type="text" name="telephone" size="20" value="<?php echo("$telephone"); ?>"></td>
   </tr>
   <tr>
      <td>Fax :</td>
	  <td><input type="text" name="fax" size="20" value="<?php echo("$fax"); ?>"></td>
   </tr>
   <tr>
      <td>Portable :</td>
	  <td><input type="text" name="portable" size="20" value="<?php echo("$portable"); ?>"></td>
   </tr>
   <tr>
      <td><b>E-mail</b> :</td>
	  <td><input type="text" name="email" size="50" value="<?php echo("$email"); ?>"></td>
   </tr>
</table>

<br>

<center><input type="submit" value="Modifier"></center>

</form>

<br>

<center>
<a href="index.php">Retour</a>
</center>

<?php include("../inc/footer.php"); ?>