<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>
<?php

$req = mysql_query("select titre from ".$prefixe_table."produits_cat where id=\"$id_cat\"");
if (mysql_num_rows($req)==0)
{
mysql_close($connect_db);
header("location: index.php");
exit();
}

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
				
				$req = mysql_query("update ".$prefixe_table."produits_cat set titre=\"$titre\" where id=\"$id_cat\"");
				
				mysql_close($connect_db);
				header("location: modifier_cat.php?id_cat=$id_cat&msg=Catégorie+modifiée+!");
				exit();
	}
}

$titre = mysql_result($req,0,"titre");

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

<form action="modifier_cat.php?id_cat=<?php echo("$id_cat"); ?>" method="post">
<input type="hidden" name="action" value="send">

<table border="0" align="center">
   <tr>
      <td><b>Titre</b> :</td>
	  <td><input type="text" name="titre" size="50" value="<?php echo("$titre"); ?>"></td>
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