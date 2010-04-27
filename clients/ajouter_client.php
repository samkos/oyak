<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>
<?php

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

$clef = trim($clef);
$clef = strip_tags($clef);
$clef = str_replace('"','&quot;',$clef);
$clef = stripslashes($clef);

	if ($civilite == "0")
	{
	$msg = "Veuillez sélectionner une civilité";
	}
	else
	{
	   if ($nom == "")
	   {
	   $msg = "Veuillez introduire le nom";
	   }
	   else
	   {
	      if ($prenom == "")
		  {
		  $msg = "Veuillez introduire le prénom";
		  }
		  else
		  {
		     if ($pays == "0")
			 {
			 $msg = "Veuillez sélectionner le pays";
			 }
			 else
			 {
			    if (!EmailOK($email))
				{
				$msg = "L'email est invalide";
				}
				else
				{
				$nom = addslashes($nom);
				$prenom = addslashes($prenom);
				$societe = addslashes($societe);
				$adresse = addslashes($adresse);
				$adresse2 = addslashes($adresse2);
				$ville = addslashes($ville);
				$code_postal = addslashes($code_postal);
				$telephone = addslashes($telephone);
				$fax = addslashes($fax);
				$portable = addslashes($portable);
				$email = addslashes($email);
				
				$req = mysql_query("insert into ".$prefixe_table."clients values ('','$civilite','$nom','$prenom','$societe','$adresse','$adresse2','$ville','$code_postal','$pays','$telephone','$fax','$portable','$email',NULL)");
				
				mysql_close($connect_db);
				header("location: index.php");
				exit();
				}
			 }
		  }
	   }
	}
}

?>
<?php include("../verif.php"); ?>
<?php include("../inc/header.php"); ?>

<?php

if ($msg != "")
{
$msg = str_replace("+"," ",$msg);
echo("<center><font color=\"#ff0000\"><b>$msg</b></font></center><br>");
}

?>

<form action="ajouter_client.php" method="post">
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
      <td>Société :</td>
	  <td><input type="text" name="societe" size="50" value="<?php echo("$societe"); ?>"></td>
   </tr>
   <tr>
      <td>Clef :</td>
	  <td><input type="text" name="clef" size="50" value="<?php echo("$clef"); ?>"></td>
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

<center><input type="submit" value="Ajouter"></center>

</form>

<br>

<center>
<a href="index.php">Retour</a>
</center>

<?php include("../inc/footer.php"); ?>