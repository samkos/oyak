<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>
<?php

$req = mysql_query("select pays,pref_tel from ".$prefixe_table."pays where id=\"$id_pays\"");
if (mysql_num_rows($req)==0)
{
mysql_close($connect_db);
header("location: index.php");
exit();
}

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
	$msg = "Veuillez introduire le pays";
	}
	else
	{
	   if ($prefixe == "")
	   {
	   $msg = "Veuillez introduire le préfixe du téléphone";
	   }
	   else
	   {
	   $pays = addslashes($pays);
	   $prefixe = addslashes($prefixe);
	   
	   $req = mysql_query("update ".$prefixe_table."pays set pays=\"$pays\",pref_tel=\"$prefixe\" where id=\"$id_pays\"");
	   
	   mysql_close($connect_db);
	   header("location: modifier_pays.php?id_pays=$id_pays&msg=Pays+modifié+!");
	   exit();
	   }
	}
}

$pays = mysql_result($req,0,"pays");
$prefixe = mysql_result($req,0,"pref_tel");

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

<form action="modifier_pays.php?id_pays=<?php echo("$id_pays"); ?>" method="post">
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

<center><input type="submit" value="Modifier"></center>

</form>

<br>

<center>
<a href="index.php">Retour</a>
</center>

<?php include("../inc/footer.php"); ?>