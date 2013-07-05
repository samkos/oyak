<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>
<?php

if ($action == "send")
{
$titre = trim($titre);
$titre = strip_tags($titre);
$titre = str_replace('"','&quot;',$titre);
$titre = stripslashes($titre);

	if ($titre == "")
	{
	$msg = "Veuillez introduire un titre";
	}
	else
	{
				$titre = addslashes($titre);
				
				$req = mysql_query("insert into ".$prefixe_table."produits_cat values ('','$titre')");
				
				mysql_close($connect_db);
				header("location: index.php");
				exit();

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

<form action="ajouter_cat.php" method="post">
<input type="hidden" name="action" value="send">

<table border="0" align="center">
   <tr>
      <td><b>Titre</b> :</td>
	  <td><input type="text" name="titre" size="50" value="<?php echo("$titre"); ?>"></td>
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