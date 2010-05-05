<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>
<?php

if ($action == "delete")
{
$req = mysql_query("delete from ".$prefixe_table."factures where num=\"$id_fact\"");
$req = mysql_query("delete from ".$prefixe_table."factures_produits where num_fact=\"$id_fact\"");
}

?>
<?php include("../inc/header.php"); ?>

<table border="0" align="center" cellpadding="3" cellspacing="1" bgcolor="#000000" width="770">
   <tr>
      <td bgcolor="#99CCCC" align="center" width="15%"><b>N°</b></td>
	  <td bgcolor="#99CCCC" align="center" width="30%"><b>Client</b></td>
	  <td bgcolor="#99CCCC" align="center" width="15%"><b>Date</b></td>
	  <td bgcolor="#99CCCC" align="center" width="10%"><b>Type</b></td>
	  <td bgcolor="#99CCCC" align="center" width="30%" colspan="3"><b>Actions</b></td>
   </tr>
<?php

function client($id)
{
global $prefixe_table;
$req = mysql_query("select nom,prenom from ".$prefixe_table."clients where id=\"$id\"") or die(mysql_error());
$nom = mysql_result($req,0,"nom");
$prenom = mysql_result($req,0,"prenom");
return "$nom $prenom";
}

$nb_fact = 30;
if(!$start) 
{$start=0;}

$req = mysql_query("select num,id_clt,date,type from ".$prefixe_table."factures order by date desc, num desc limit $start,$nb_fact");
while($ligne = mysql_fetch_array($req))
{
$num = $ligne["num"];
$id_clt = $ligne["id_clt"];
$date = $ligne["date"];
$type = $ligne["type"];

$date = ereg_replace('^([0-9]{2,4})-([0-9]{1,2})-([0-9]{1,2})$', '\\3/\\2/\\1', $date);

if ($type == "f")
{
$type = "Facture";
}
elseif ($type == "d")
{
$type = "Devis";
}

$num_d = sprintf("%08s",$num);
$client = client($id_clt);

echo("<tr>
   <td bgcolor=\"#ffffff\" align=\"center\">#$num_d</td>
   <td bgcolor=\"#ffffff\" align=\"center\">$client</td>
   <td bgcolor=\"#ffffff\" align=\"center\">$date</td>
   <td bgcolor=\"#ffffff\" align=\"center\">$type</td>
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"10%\"><a href=\"modifier.php?id_facture=$num\">Modifier</a></td>
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"10%\"><a href=\"#null\" onclick=\"javascript:if(confirm('Etes-vous sûr de vouloir supprimer cette facture ?')) document.location.replace('index.php?action=delete&id_fact=$num');\">Supprimer</a></td>
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"10%\"><a href=\"generer.php?id_facture=$num\">Générer</a></td>
</tr>");
}

?>
</table>

<br>

<center>[ <?php

$result=mysql_query("select count(*) from ".$prefixe_table."factures");
$row=mysql_fetch_row($result);

if ($start == "0")
{
echo"<b>1</b> ";
}
else
{
echo"<a href=\"index.php?start=0\">1</a> ";
}

for($index=1;($index*$nb_fact)<$row[0];$index++) 
{
   $pg = $index+1;
   if(($index*$nb_fact)!=$start) 
   {
   print(" - <a href=\"index.php?start=".($index*$nb_fact)."\">");
   echo"$pg";
   print("</a>");
   }
   else
   {
   echo" - <b>$pg</b>";
   }
}

?> ]</center>

<br>

<center>
<a href="ajouter.php">Ajouter une facture / devis</a> - 
<a href="/<?php echo("$prefixe_dossier"); ?>index.php">Retour</a>
</center>

<?php include("../inc/footer.php"); ?>