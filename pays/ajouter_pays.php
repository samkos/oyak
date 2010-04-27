<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>
<?php

if ($action == "send")
{
$pays = trim($pays);
$pays = strip_tags($pays);
$pays = str_replace('"','&quot;',$pays);
$pays = stripslashes($pays);

$prefixe = trim($prefixe);
$prefixe = strip_tags($prefixe);
$prefixe = str_replace('"','&quot;',$prefixe);
$prefixe = stripslashes($prefixe);

	if ($pays == "0")
	{
	$msg = "Veuillez sélectionner une civilité";
	}
	else
	{
	   if ($prefixe == "")
	   {
	   $msg = "Veuillez introduire le nom";
	   }
	   else
	   {
	   $pays = addslashes($pays);
	   $prefixe = addslashes($prefixe);
	   
	   $req = mysql_query("insert into ".$prefixe_table."pays values ('','$pays','$prefixe')");
	   
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

<form action="ajouter_pays.php" method="post">
<input type="hidden" name="action" value="send">

<table border="0" align="center">
   <tr>
      <td><b>Pays</b> :</td>
	  <td><input type="text" name="pays" size="50" value="<?php echo("$pays"); ?>"></td>
   </tr>
   <tr>
      <td><b>Préfixe du téléphone</b> :</td>
	  <td><input type="text" name="prefixe" size="10" value="<?php echo("$prefixe"); ?>"></td>
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