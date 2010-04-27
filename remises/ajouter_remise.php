<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>
<?php

if ($action == "send")
{
$titre = trim($titre);
$titre = strip_tags($titre);
$titre = str_replace('"','&quot;',$titre);
$titre = stripslashes($titre);

$taux = trim($taux);
$taux = strip_tags($taux);
$taux = str_replace('"','&quot;',$taux);
$taux = stripslashes($taux);

	if ($titre == "")
	{
	$msg = "Veuillez introduire une TVA";
	}
	else
	{
	   if ($taux == "")
	   {
	   $msg = "Veuillez introduire le taux";
	   }
	   else
	   {
	   $titre = addslashes($titre);
	   $taux = addslashes($taux);
	   
	   $req = mysql_query("insert into ".$prefixe_table."remises values ('','$titre','$taux')");
	   
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

<form action="ajouter_remise.php" method="post">
<input type="hidden" name="action" value="send">

<table border="0" align="center">
   <tr>
      <td><b>Titre</b> :</td>
	  <td><input type="text" name="titre" size="50" value="<?php echo("$tire"); ?>"></td>
   </tr>
   <tr>
      <td><b>Taux</b> :</td>
	  <td><input type="text" name="taux" size="10" value="<?php echo("$taux"); ?>"></td>
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