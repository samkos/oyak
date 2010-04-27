<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>
<?php

if ($action == "delete")
{
$req = mysql_query("delete from ".$prefixe_table."remises where id=\"$id_remise\"");
}

?>
<?php include("../inc/header.php"); ?>

<table border="0" align="center" cellpadding="3" cellspacing="1" bgcolor="#000000" width="450">
   <tr>
      <td bgcolor="#99CCCC" align="center" width="40%"><b>Titre</b></td>
      <td bgcolor="#99CCCC" align="center" width="20%"><b>Taux</b></td>
	  <td bgcolor="#99CCCC" align="center" width="40%"><b>Actions</b></td>
   </tr>
<?php

$req = mysql_query("select id,titre,taux from ".$prefixe_table."remises order by taux");
while($ligne = mysql_fetch_array($req))
{
$id = $ligne["id"];
$titre = $ligne["titre"];
$taux = $ligne["taux"];

echo("<tr>
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"40%\">$titre</td>
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"20%\">$taux%</td>
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"40%\"><a href=\"#null\" onclick=\"javascript:if(confirm('Etes-vous sûr de vouloir supprimer cette remise &quot;$titre&quot; ?')) document.location.replace('index.php?action=delete&id_remise=$id');\">Supprimer</a></td>
</tr>");
}

?>
</table>

<br>

<center>
<a href="ajouter_remise.php">Ajouter une remise</a> - 
<a href="/<?php echo("$prefixe_dossier"); ?>index.php">Retour</a>
</center>

<?php include("../inc/footer.php"); ?>