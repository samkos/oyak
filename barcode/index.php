<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>



</HEAD>


<?php include("../inc/header.php"); 

?>




<table border="0" align="center" cellpadding="3" cellspacing="1" bgcolor="#000000" width="770">
   <tr>
      <td bgcolor="#99CCCC" align="center" width="10%"><b> Choix </b></td>
      <td bgcolor="#99CCCC" align="center" width="11%"><b>Quantité</b></td>
      <td bgcolor="#99CCCC" align="center" width="40%"><b>Fournisseur</b></td>
      <td bgcolor="#99CCCC" align="center" width="40%"><b>Titre</b></td>
	   <td bgcolor="#99CCCC" align="center" width="39%" colspan="3"><b>Code Barre</b></td>
   </tr>
<tr>
 
<td bgcolor="#99CCCC" colspan=1> </td>
<td bgcolor="#99CCCC" colspan=1> </td>
  <form action="">
<td bgcolor="#99CCCC" colspan=1>
	<input type=text name=filtre_fournisseur value="<?php echo $filtre_fournisseur ?>">
  <input type="submit" value="Filtrer"> </td>
	<td bgcolor="#99CCCC" colspan=1>
	<input type=text name=filtre_titre size=40 value="<?php echo $filtre_titre ?>"> <BR> 
  <input type="submit" value="Filtrer"> </td>
	<td bgcolor="#99CCCC" colspan=1>
	<input type=text name=filtre_barcode value="<?php echo $filtre_barcode ?>">
	<input type="hidden" name="id_cat" value="<?php print $id_cat ?>">
  <input type="submit" value="Filtrer"> 
	</form>
</td>
</tr>
<?php


$nb_produit = 1000;
if(!$start) {$start=0;}


$sql_query = "select id,titre,stock,barcode,fournisseur from ".$prefixe_table."produits ";

$sql_filtre=" where id_cat=\"$id_cat\"  ";
$url_filtre="";

if ($filtre_titre) { 
   $sql_filtre = $sql_filtre."  and (titre like \"".str_replace("*", "%", $filtre_titre)."\" ) ";
   $url_filtre = $url_filtre."&filtre_titre=$filtre_titre";
}

if ($filtre_fournisseur) { 
   $sql_filtre = $sql_filtre."  and (fournisseur like \"".str_replace("*", "%", $filtre_fournisseur)."\" ) ";
   $url_filtre = $url_filtre."&filtre_fournisseur=$filtre_fournisseur";
}

if ($filtre_barcode) { 
   $sql_filtre = $sql_filtre."  and (barcode like \"".str_replace("*", "%", $filtre_barcode)."\" ) ";
   $url_filtre = $url_filtre."&filtre_barcode=$filtre_barcode";
}
$sql_filtre = $sql_filtre."  order by id ";

//print "<BR> $sql_query <BR>";
$req = mysql_query("$sql_query $sql_filtre limit $start,$nb_produit");
?>

<form name=checkboxform action="latex_barcode.php" method=post >
<input type="hidden" name="action" value="print">
<input type="hidden" name="id_cat" value="<?php print $id_cat ?>">

<tr> 
<td bgcolor="#99CCCC" colspan=1>
  <input type=button value="Tous" onClick="checkAll()">
  <input type=button value="Aucun" onClick="uncheckAll()">
  <input type=button value="Autres" onClick="switchAll()">
<td bgcolor="#99CCCC" colspan=1>
	<input type=text name=filtre_quantite value="1">
	<input type=button value="Set" onClick="setAll()">
</td>
<td bgcolor="#99CCCC" colspan=1> </td>
<td bgcolor="#99CCCC" colspan=2>
  <input type="submit" value="Imprime"> 
</td>
</tr>


<?php
$nb=0;

while($ligne = mysql_fetch_array($req))
{
$nb++;
$id = $ligne["id"];
$titre = $ligne["titre"];
$fournisseur = $ligne["fournisseur"];
$stock = $ligne["stock"];
$barcode = $ligne["barcode"];

$id_d = sprintf("%08s",$id);

$ischecked="";
if  ($GLOBALS["choisis$id"]>0) { $ischecked="checked";}
$nb_print=$GLOBALS["quantite$id"];
if  ($nb_print==0) { $nb_print=1;}


echo("<tr>
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"10%\">
	  <input name='choisis$nb' type='checkbox' value=$barcode $ischecked   /> </td>
   <td bgcolor=\"#ffffff\" align=\"right\" width=\"10%\">
	  <input name='quantite$nb' type=integer value='$nb_print'   /> </td>
	  <input name='produit$nb' type=hidden value='$titre'   /> </td>
		<input name='id$nb' type=hidden value='$id'   /> </td>
   <td bgcolor=\"#ffffff\" align=\"left\" width=\"60%\">$fournisseur</td>
   <td bgcolor=\"#ffffff\" align=\"left\" width=\"60%\">$titre</td>
   <td bgcolor=\"#ffffff\" align=\"center\" width=\"20%\">$barcode</td>
</tr>");
}

//echo $nb."<BR>";

?>
</form>



</table>

<SCRIPT LANGUAGE="JavaScript">

<!-- This script and many more are available free online at -->
<!-- The JavaScript Source!! http://javascript.internet.com -->

<!-- Begin
function checkAll() {
for (var j = 1; j <= <?php print $nb ?> ; j++) {
box = eval("document.checkboxform.choisis" + j); 
if (box.checked == false) box.checked = true;
   }
}

function uncheckAll() {
for (var j = 1; j <= <?php print $nb ?> ; j++) {
box = eval("document.checkboxform.choisis" + j); 
if (box.checked == true) box.checked = false;
   }
}

function switchAll() {
for (var j = 1; j <= <?php print $nb ?> ; j++) {
box = eval("document.checkboxform.choisis" + j); 
box.checked = !box.checked;
   }
}

function setAll() {
box = eval("document.checkboxform.filtre_quantite");
nb=box.value;
for (var j = 1; j <= <?php print $nb ?> ; j++) {
box = eval("document.checkboxform.quantite" + j); 
box.value=nb; 
   }
}




//  End -->
</script>
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
echo"<a href=\"index.php?start=0&$url_filtre\">1</a> ";
}

for($index=1;($index*$nb_produit)<$row[0];$index++) 
{
   $pg = $index+1;
   if(($index*$nb_produit)!=$start) 
   {
   print(" - <a href=\"index.php?start=".($index*$nb_produit)."&$url_filtre\">");
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
