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
				$nom = addslashes($nom);
				$prenom = addslashes($prenom);
				
				$req = mysql_query("insert into ".$prefixe_table."vendeurs values ('','$nom','$prenom',NULL)");
				
				mysql_close($connect_db);
				header("location: index.php");
				exit();
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

<form action="ajouter_vendeur.php" method="post">
<input type="hidden" name="action" value="send">

<table border="0" align="center">
   <tr>
      <td><b>Nom</b> :</td>
	  <td><input type="text" name="nom" size="50" value="<?php echo("$nom"); ?>"></td>
   </tr>
   <tr>
      <td><b>Prénom</b> :</td>
	  <td><input type="text" name="prenom" size="50" value="<?php echo("$prenom"); ?>"></td>
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