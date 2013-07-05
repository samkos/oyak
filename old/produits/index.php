<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>
<?php
$nb_produit = 3000;
if ($action == "delete")
{
$req = mysql_query("delete from ".$prefixe_table."produits where id=\"$id_produit\"");
}

?>
<?php include("../inc/header.php"); ?>

<table border="0" align="center" cellpadding="3" cellspacing="1" bgcolor="#000000" width="770">
   <tr>
      <!-- <td bgcolor="#99CCCC" align="right" width="10%"><b>n°</b></td> -->
      <td bgcolor="#99CCCC" align="center" width="8%"><b>Référence</b></td>
      <td bgcolor="#99CCCC" align="center" width="8%"><b>Produit</b></td>
      <td bgcolor="#99CCCC" align="center" width="8%"><b>Fournisseur</b></td>
      <td bgcolor="#99CCCC" align="center" width="8%"><b>Prix vente HT</b></td>
      <td bgcolor="#99CCCC" align="center" width="8%"><b>Prix plancher HT</b></td>
      <td bgcolor="#99CCCC" align="center" width="8%"><b>Poids</b></td>
      <td bgcolor="#99CCCC" align="center" width="50%"><b>Titre</b></td>
	  <td bgcolor="#99CCCC" align="center" width="18%" colspan="3"><b>Actions</b></td>
   </tr>
    <tr>
      <form action="">
     
    <td bgcolor="#99CCCC" colspan=1> 
    	<input type=text name=filtre_ref size=15 value="<?php echo $filtre_ref ?>"> 
    </td>
    <td bgcolor="#99CCCC" colspan=1>       
    	<input type=text name=filtre_produit size=4 value="<?php echo $filtre_produit ?>"> 
   	</td>
    <td bgcolor="#99CCCC" colspan=1>
    	<input type=text name=filtre_fournisseur size=5 value="<?php echo $filtre_fournisseur ?>">
		</td>  
    <td bgcolor="#99CCCC" > </td>
    <td bgcolor="#99CCCC" > </td>
    <td bgcolor="#99CCCC" > </td>
    <td bgcolor="#99CCCC" >
		    <input type=text name=filtre_titre size=25 value="<?php echo $filtre_titre ?>"> 
		 </td>
    <td bgcolor="#99CCCC" ></td>
    <td bgcolor="#99CCCC" colspan=2>  <input type="submit" value="Filtrer"> </td>
    </td>
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



if(!$start) 
{$start=0;}

if (!$filtre_clef) {$filtre_clef='*';}
if (!$filtre_fournisseur) {$filtre_fournisseur='*';}
if (!$filtre_produit) {$filtre_produit='*';}
if (!$filtre_ref) {$filtre_ref='*';}
if (!$filtre_titre) {$filtre_titre='*';}

$sql_filtre=str_replace("*","%","where id_cat=\"$id_cat\" and clef like '$filtre_produit' and barcode like '$filtre_ref' and fournisseur like '$filtre_fournisseur' and titre like '$filtre_titre' and not(clef > 9999)" );
//print $sql_filtre;

$query="select id,titre,stock,barcode,prix_vente_ht,prix_plancher_ht,fournisseur,clef,poids from ".$prefixe_table
							 ."produits $sql_filtre"
                       ."order by titre,barcode limit $start,$nb_produit";
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
$poids = $ligne["poids"];
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


echo("<tr>
   <!--  <td bgcolor=\"#ffffff\" align=\"center\" width=\"10%\">$id</td> -->
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"8%\">$barcode</td>
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"8%\">$produit</td>
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"8%\">$fournisseur <BR> </td>
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"8%\">$prix_vente_ht</td>
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"8%\">$prix_plancher_ht</td>
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"8%\">$poids</td>
   <td bgcolor=\"#ffffff\" align=\"left\" width=\"50%\">$titre</td>
   <!-- <td bgcolor=\"#ffffff\" align=\"center\" width=\"6%\"><a href=\"$stock\">Stocks</a></td> -->
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"9%\"><a href=\"modifier_produit.php?id_produit=$id&start=$start\">Modifier</a></td>
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"9%\"><a href=\"#null\" onclick=\"javascript:if(confirm('Etes-vous sûr de vouloir supprimer ce produit &quot;$titre&quot; ?')) document.location.replace('produits.php?action=delete&id_produit=$id');\">Supprimer</a></td>
</tr>");
}

?>
</table>

<br>

<center>[ <?php

$result=mysql_query("select count(*) from ".$prefixe_table."produits $sql_filtre");
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


<?php include("../inc/footer.php"); ?>