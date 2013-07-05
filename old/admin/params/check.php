<?php include("../../inc/conf.php"); ?>
<?php include("../../inc/fonctions.php"); ?>
<?php

if ($action == "delete")
{
$req = mysql_query("delete from ".$prefixe_table."produits where id=\"$id_produit\"");
}

?>
<?php include("../../inc/header.php"); ?>

<table border="0" align="center" cellpadding="3" cellspacing="1" bgcolor="#000000" width="770">
   <tr>
      <!-- <td bgcolor="#99CCCC" align="right" width="10%"><b>n°</b></td> -->
      <td bgcolor="#99CCCC" align="center" width="8%"><b>Référence</b></td>
      <td bgcolor="#99CCCC" align="center" width="8%"><b>Produit</b></td>
      <td bgcolor="#99CCCC" align="center" width="8%"><b>Fournisseur</b></td>
      <td bgcolor="#99CCCC" align="center" width="8%"><b>Prix vente HT</b></td>
      <td bgcolor="#99CCCC" align="center" width="8%"><b>Prix plancher HT</b></td>
      <td bgcolor="#99CCCC" align="center" width="50%"><b>Titre</b></td>
	  <td bgcolor="#99CCCC" align="center" width="18%" colspan="3"><b>Actions</b></td>
   </tr>
<?php


   // recuperation nom fournisseur
	 
	 $req = mysql_query("select id,societe from ".$prefixe_table."fournisseurs");
	 while($ligne = mysql_fetch_array($req))
	 {
	   $id = $ligne["id"];
	   $societe = $ligne["societe"];
		 $fournisseur_nom[$id]="$societe";
		}


$nb_produit = 300;
if(!$start) 
{$start=0;}

$query="select id,titre,stock,barcode,prix_vente_ht,prix_plancher_ht,fournisseur,clef from ".$prefixe_table."produits where id_cat=\"$id_cat\" order by titre,barcode";
//echo "query=$query <BR>";
$req = mysql_query($query);
while($ligne = mysql_fetch_array($req))
{
$id = $ligne["id"];
$barcode = $ligne["barcode"];
$fournisseur = $ligne["fournisseur"];
$clef = $ligne["clef"];
$produit = $clef;
$prix_vente_ht = $ligne["prix_vente_ht"];
$prix_plancher_ht = $ligne["prix_plancher_ht"];
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

if (strlen($fournisseur_nom[$fournisseur])<2) {
echo("<tr>
   <!--  <td bgcolor=\"#ffffff\" align=\"center\" width=\"10%\">$id</td> -->
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"8%\">$barcode</td>
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"8%\">$produit</td>
   <td  bgcolor=\"#ffffff\" align=\"center\" width=\"8%\" > <B> $fournisseur </B> <BR> </td>
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"8%\">$prix_vente_ht</td>
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"8%\">$prix_plancher_ht</td>
   <td bgcolor=\"#ffffff\" align=\"left\" width=\"50%\">$titre</td>
   <!-- <td bgcolor=\"#ffffff\" align=\"center\" width=\"6%\"><a href=\"$stock\">Stocks</a></td> -->
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"9%\"><a href=\"modifier_produit.php?id_produit=$id&start=$start\">Modifier</a></td>
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"9%\"><a href=\"#null\" onclick=\"javascript:if(confirm('Etes-vous sûr de vouloir supprimer ce produit &quot;$titre&quot; ?')) document.location.replace('produits.php?action=delete&id_produit=$id');\">Supprimer</a></td>
</tr>");
}
}




?>
</table>

<br>




<?php include("../../inc/footer.php"); ?>