<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>
<?php

if ($action == "delete")
{
$req = mysql_query("delete from ".$prefixe_table."pays where id=\"$id_pays\"");
}

?>
<?php include("../inc/header.php"); ?>

<table border="0" align="center" cellpadding="3" cellspacing="1" bgcolor="#000000" width="770">
   <tr>
      <td bgcolor="#99CCCC" align="center" width="70%"><b>Pays</b></td>
	  <td bgcolor="#99CCCC" align="center" width="30%" colspan="2"><b>Actions</b></td>
   </tr>
<?php

$req = mysql_query("select id,pays from ".$prefixe_table."pays order by pays");
while($ligne = mysql_fetch_array($req))
{
$id = $ligne["id"];
$pays = $ligne["pays"];

echo("<tr>
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"70%\">$pays</td>
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"15%\"><a href=\"modifier_pays.php?id_pays=$id\">Modifier</a></td>
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"15%\"><a href=\"#null\" onclick=\"javascript:if(confirm('Etes-vous sûr de vouloir supprimer ce pays &quot;$pays&quot; ?')) document.location.replace('index.php?action=delete&id_pays=$id');\">Supprimer</a></td>
</tr>");
}

?>
</table>

<br>

<center>
<a href="ajouter_pays.php">Ajouter un pays</a> - 
<a href="/<?php echo("$prefixe_dossier"); ?>clients/">Retour</a>
</center>

<?php include("../inc/footer.php"); ?>