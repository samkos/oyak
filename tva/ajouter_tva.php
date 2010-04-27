<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>
<?php

if ($action == "send")
{
$tva = trim($tva);
$tva = strip_tags($tva);
$tva = str_replace('"','&quot;',$tva);
$tva = stripslashes($tva);

	if ($tva == "")
	{
	$msg = "Veuillez introduire une TVA";
	}
	else
	{
	   $tva = addslashes($tva);
	   
	   $req = mysql_query("insert into ".$prefixe_table."taux_tva values ('','$tva')");
	   
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

<form action="ajouter_tva.php" method="post">
<input type="hidden" name="action" value="send">

<table border="0" align="center">
   <tr>
      <td><b>Taux TVA</b> :</td>
	  <td><input type="text" name="tva" size="50" value="<?php echo("$tva"); ?>"></td>
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