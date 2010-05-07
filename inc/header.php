<html>

<head>
<title>OYAK</title>
<style type="text/css">
body,td,input
{
color: #000000;
font-size: 12px;
font-family: Verdana;
}

input,select,textarea
{
color: #000000;
font-size: 12px;
font-family: Verdana;
}


{
color: #000000;
font-size: 12px;
font-family: Verdana;
text-decoration: underline;
}

a:hover
{
color: #000000;
font-size: 12px;
font-family: Verdana;
text-decoration: underline;
}
</style>
</head>
<body bgcolor="#ffffff">

<table border="0" align="center" width="770">
   <tr>
      <td colspan="16" align="center"><hr size="1" color="#000000"><a href="/<?php echo("$prefixe_dossier"); ?>index.php">Oyak v<?php print $version ?></a></td>
   </tr>
   <tr>
      <td colspan="16" align="center"><hr size="1" color="#000000"></td>
   </tr>
   <tr>
      <td width="12%" align="center" valign="top">Etiquettes<BR>
                                     <a href="/<?php echo("$prefixe_dossier"); ?>barcode/index.php?id_cat=1">lister</a></td>
      <td width="12%" align="center" valign="top">Clients<BR>
                                     <a href="/<?php echo("$prefixe_dossier"); ?>clients/">lister</a></td>
      <td width="12%" align="center" valign="top">Fournisseurs<BR>
	                           <a href="/<?php echo("$prefixe_dossier"); ?>fournisseurs/">lister</a></td>
      <td width="12%" align="center" valign="top"> Produits<BR>
	                             <a href="/<?php echo("$prefixe_dossier"); ?>produits/">lister</a><BR>
                                     <a href="/<?php echo("$prefixe_dossier"); ?>produits/check.php">verifier</a></td>
      <td width="12%" align="center" valign="top">Vendeurs<BR><a href="/<?php echo("$prefixe_dossier"); ?>vendeurs/">lister</a></td>
      <td width="12%" align="center" valign="top"> Commandes 
                                      <a href="/<?php echo("$prefixe_dossier"); ?>print/commandes/">lister</a><br>
                                      <a href="/<?php echo("$prefixe_dossier"); ?>print/tests/">tester</a></td>
     <td width="12%" align="center" valign="top"> Administrer<BR>
     <a href="/<?php echo("$prefixe_dossier"); ?>admin/">gerer</a> <BR>
     <a href="/<?php echo("$prefixe_dossier"); ?>admin/params/">options</a> <BR>
     
			</td>
   </tr>
   <tr>
      <td colspan="16" align="center"><hr size="1" color="#000000"></td>
   </tr>
</table>

<br>

<?php $id_cat=1 ?>
