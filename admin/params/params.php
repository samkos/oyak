<?php include("../../inc/conf.php"); ?>
<?php include("../../inc/fonctions.php"); ?>
<?php include("../../verif.php"); ?>
<?php

if ($action == "delete")
{
$req = mysql_query("delete from ".$prefixe_table."produits where id=\"$id_produit\"");
}

?>
<?php include("../../inc/header.php"); ?>

<table border="0" align="center" cellpadding="3" cellspacing="1" bgcolor="#000000" width="770">
   <tr>
      <td bgcolor="#99CCCC" align="center" width="11%"><b>Référence</b></td>
      <td bgcolor="#99CCCC" align="center" width="50%"><b>Titre</b></td>
	  <td bgcolor="#99CCCC" align="center" width="39%" colspan="3"><b>Actions</b></td>
   </tr>
<?php

$nb_produit = 30;
if(!$start) 
{$start=0;}

$query="select id,titre,stock,barcode from ".$prefixe_table."produits where id_cat=\"$id_cat\" order by id,titre,stock,barcode limit $start,$nb_produit";
echo "query=$query <BR>";
$req = mysql_query($query);
while($ligne = mysql_fetch_array($req))
{
$id = $ligne["id"];
$barcode = $ligne["barcode"];
$titre = $ligne["titre"];
$stock = $ligne["stock"];

$id_d = sprintf("%08s",$id);

if ($stock == "1")
{
$stock = "/".$prefixe_dossier."stocks/index.php?ref_produit=$id";
}
else
{
$stock = "javascript:alert('Pas de gestion de stocks pour ce produit !');";
}

echo("<tr>
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"11%\">$barcode</td>
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"61%\">$titre</td>
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"13%\"><a href=\"$stock\">Stocks</a></td>
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"13%\"><a href=\"modifier_produit.php?id_produit=$id\">Modifier</a></td>
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"13%\"><a href=\"#null\" onclick=\"javascript:if(confirm('Etes-vous sûr de vouloir supprimer ce produit &quot;$titre&quot; ?')) document.location.replace('produits.php?action=delete&id_produit=$id');\">Supprimer</a></td>
</tr>");
}

?>
</table>

<br>

<center>[ <?php

$result=mysql_query("select count(*) from ".$prefixe_table."produits");
$row=mysql_fetch_row($result);

if ($start == "0")
{
echo"<b>1</b> ";
}
else
{
echo"<a href=\"index.php?start=0\">1</a> ";
}

for($index=1;($index*$nb_produit)<$row[0];$index++) 
{
   $pg = $index+1;
   if(($index*$nb_produit)!=$start) 
   {
   print(" - <a href=\"index.php?start=".($index*$nb_produit)."\">");
   echo"$pg";
   print("</a>");
   }
   else
   {
   echo" - <b>$pg</b>";
   }
}

?> ]</center>


<?php include("../../inc/footer.php"); ?>