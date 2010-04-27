<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>
<?php

if ($action == "delete")
{
$req = mysql_query("delete from ".$prefixe_table."taux_tva where id=\"$id_taux\"");
}

?>
<?php include("../inc/header.php"); ?>

<table border="0" align="center" cellpadding="3" cellspacing="1" bgcolor="#000000" width="300">
   <tr>
      <td bgcolor="#99CCCC" align="center" width="40%"><b>Taux</b></td>
	  <td bgcolor="#99CCCC" align="center" width="60%"><b>Actions</b></td>
   </tr>
<?php

$req = mysql_query("select id,taux from ".$prefixe_table."taux_tva order by taux");
while($ligne = mysql_fetch_array($req))
{
$id = $ligne["id"];
$taux = $ligne["taux"];

echo("<tr>
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"40%\">$taux%</td>
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"60%\"><a href=\"#null\" onclick=\"javascript:if(confirm('Etes-vous sûr de vouloir supprimer ce taux &quot;$taux%&quot; ?')) document.location.replace('index.php?action=delete&id_taux=$id');\">Supprimer</a></td>
</tr>");
}

?>
</table>

<br>

<center>
<a href="ajouter_tva.php">Ajouter une TVA</a> - 
<a href="/<?php echo("$prefixe_dossier"); ?>produits/index.php">Retour</a>
</center>

<?php include("../inc/footer.php"); ?>