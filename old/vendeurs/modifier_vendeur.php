<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>
<?php

$req = mysql_query("select id,nom,prenom from ".$prefixe_table."vendeurs where id=\"$id_vendeur\"");
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

$id = trim($id);
$id = strip_tags($id);
$id = str_replace('"','&quot;',$id);
$id = stripslashes($id);

$id_modif = trim($id_modif);
$id = strip_tags($id_modif);
$id_modir = str_replace('"','&quot;',$id_modif);
$id_modif = stripslashes($id_modif);

    	$nom = addslashes($nom);
  		$prenom = addslashes($prenom);
  		$id = addslashes($id);
  		
  		$req = mysql_query("update ".$prefixe_table."vendeurs set id=\"$id_modif\",nom=\"$nom\",prenom=\"$prenom\",timestamp=NULL where id=\"$id_vendeur\"") or die(mysql_error());
  		
  		mysql_close($connect_db);
  		header("location: modifier_vendeur.php?id_vendeur=$id_vendeur&msg=vendeur+modifié+!");
  		exit();
}

$nom = mysql_result($req,0,"nom");
$prenom = mysql_result($req,0,"prenom");
$id = mysql_result($req,0,"id");

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

<form action="modifier_vendeur.php?id_vendeur=<?php echo("$id_vendeur"); ?>" method="post">
<input type="hidden" name="action" value="send">

<table border="0" align="center">
   <tr>
      <td><b>Numero</b> :</td>
	  <td><input type="text" name="id_modif" size="50" value="<?php echo("$id"); ?>"></td>
   </tr>
   <tr>
      <td><b>Nom</b> :</td>
	  <td><input type="text" name="nom" size="50" value="<?php echo("$nom"); ?>"></td>
   </tr>
   <tr>
      <td><b>Prénom</b> :</td>
	  <td><input type="text" name="prenom" size="50" value="<?php echo("$prenom"); ?>"></td>
	  <input type="hidden" name="id" size="50" value="<?php echo("$id"); ?>">
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