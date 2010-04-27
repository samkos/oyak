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
      <td colspan="16" align="center"><hr size="1" color="#000000">Oyak v<?php print $version ?></td>
   </tr>
   <tr>
      <td colspan="16" align="center"><hr size="1" color="#000000"></td>
   </tr>
   <tr>
      <td width="12%" align="center"><a href="/<?php echo("$prefixe_dossier"); ?>index.php">Accueil</a></td>
      <td width="12%" align="center"><a href="/<?php echo("$prefixe_dossier"); ?>barcode/index.php?id_cat=1">Impression <br> Code Bar</a></td>
      <td width="12%" align="center"><a href="/<?php echo("$prefixe_dossier"); ?>clients/">Clients</a></td>
      <td width="12%" align="center"><a href="/<?php echo("$prefixe_dossier"); ?>fournisseurs/">fournisseurs</a></td>
      <td width="12%" align="center"><a href="/<?php echo("$prefixe_dossier"); ?>produits/">Produits</a></td>
      <td width="12%" align="center"><a href="/<?php echo("$prefixe_dossier"); ?>vendeurs/">Vendeurs</a></td>
      <td width="12%" align="center"><a href="/<?php echo("$prefixe_dossier"); ?>commandes/">Commandes</a></td>
      <td width="12%" align="center">
     <a href="/<?php echo("$prefixe_dossier"); ?>admin/">Administrer</a> <BR>
     <a href="/<?php echo("$prefixe_dossier"); ?>params/">Options</a> <BR>
     <a href="/<?php echo("$prefixe_dossier"); ?>produits/check.php">Vérifier</a>
			</td>
   </tr>
   <tr>
      <td colspan="16" align="center"><hr size="1" color="#000000"></td>
   </tr>
</table>

<br>

<?php $id_cat=1 ?>
