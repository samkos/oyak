<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>
<?php

$header=1;

$nb_ligne=0;
$total=0;

if ($header) {
  include("../inc/header.php");
  print "<center> \n";
}

?>
<br />
<br />
<table border="0" align="center" cellpadding="3" cellspacing="1" bgcolor="#000000" width="770">
<?		 
print "<tr> ";
print "<td bgcolor='#99CCCC' align='center' colspan=8>  Commande : $commande - $date</td>";
print "</tr>";
		
print "<tr> ";
print "<td bgcolor='#99CCCC' align='left' colspan=3>  Vendeur : $vendeur </td>";
print "<td bgcolor='#99CCCC' align='right' colspan=5> Client : $client <BR> </td>";
print "</tr>";
		

?>			
<tr>
<td bgcolor="#99CCCC" align="center" width="45%" colspan=3><b>Produit</b></td>
<td bgcolor="#99CCCC" align="center" width="30%" colspan=2><b>Fournisseur</b></td>
<td bgcolor="#99CCCC" align="center" width="15%" rowspan=2><b>Date</b></td>
<td bgcolor="#99CCCC" align="center" width="15%" rowspan=2><b>Quantite</b></td>
<td bgcolor="#99CCCC" align="center" width="15%" rowspan=2><b>Prix</b></td>
</tr>
  
<tr>
<td bgcolor="#99CCCC" align="center" width="15%"><b>Libellé</b></td>
<td bgcolor="#99CCCC" align="center" width="15%"><b>Code Barre</b></td>
<td bgcolor="#99CCCC" align="center" width="15%"><b>Code Court</b></td>
<td bgcolor="#99CCCC" align="center" width="15%"><b>Société</b></td>
<td bgcolor="#99CCCC" align="center" width="15%"><b>Code</b></td>
</tr>
<?


$header=join("",file("header.tex"));
$body=join("",file("body.tex"));
$body_vide=join("",file("body_vide.tex"));
$footer=join("",file("footer.tex"));


$out=ereg_replace("#SOCIETE#",$client,$header);
$client_all=split(" ",$client);
$out=ereg_replace("#CLIENT#",array_shift($client_all),$header);
$out=ereg_replace("<BR>","\\\\",$out);


$lignes=split(";",$contenu);
array_shift($lignes);
array_shift($lignes);

while ($ligne=array_shift($lignes)) {
  $col=split("!",$ligne);
  $code=$col[0];
  $racourci=$col[1];  			
  $fournisseur=$col[2];  			  $date=$col[3];  			
  $quantite=$col[4];
  $prix=$col[5];
  	
  $query="select titre from ".$prefixe_table."produits where barcode=\"$code\"";
  $req = mysql_query($query);
  //print $req;
  //print "query = ".$query."<BR>";
  while($ligne = mysql_fetch_array($req))
    {	
      //print_r($ligne);
      $produit = $ligne["titre"];
    }
  
  $query="select societe from ".$prefixe_table."fournisseurs where clef=\"$fournisseur\"";
  $query=sprintf("select societe from ".$prefixe_table."fournisseurs where clef=\"%d\"",$fournisseur);
  $req = mysql_query($query);
  //print $req;
  //print "query = ".$query."<BR>";
  while($ligne = mysql_fetch_array($req))
    {	
      //print_r($ligne);
      $societe = $ligne["societe"];
    }
  
  			
  print "
  		 <tr>
  		   <td bgcolor='#ffffff' align='left'> $produit </td>
  		   <td bgcolor='#ffffff' align='left'> $code</td>
				 <td bgcolor='#ffffff' align='left'> $racourci</td>
				 <td bgcolor='#ffffff' align='left'> $societe </td>
				 <td bgcolor='#ffffff' align='left'> $fournisseur</td>
  		   <td bgcolor='#ffffff' align='right'> $date</td>
  		   <td bgcolor='#ffffff' align='right'> $quantite</td>
  		   <td bgcolor='#ffffff' align='right'> $prix</td>
  		</tr>";
  $ligne=$body;
  $ligne=ereg_replace("#NUM#",$codet,$ligne);
  $ligne=ereg_replace("#LABEL#",$produit,$ligne);
  $ligne=ereg_replace("#QTY#",$quantite,$ligne);
  $ligne=ereg_replace("#PU#",$prix_unit,$ligne);
  $ligne=ereg_replace("#PRICE#",$prix,$ligne);
  $ligne=ereg_replace("#NUM#",$code,$ligne);
  $ligne=ereg_replace("#COLIS#","1",$ligne);
  $ligne=ereg_replace("#POIDS#","1.00",$ligne);
  
  $out=$out.$ligne;
  $nb_ligne=$nb_ligne+1;
  $total=$total+$prix;
}
print "</table> <br /><br />";

for ($i=$nb_ligne;$i<$nb_lignes_factures;$i++) {
  $out=$out.$body_vide;
}

			
print "<BR> <a href='./index.php'>  Retour Commandes </a> <br /> <BR>";

$date=date('d/m/Y');
$spot  = time() + (60 * 24 * 60 * 60);
$date_echeance=date("d/m/Y",$spot);
$spot  = time() + (2 * 24 * 60 * 60);
$date_livraison=date("d/m/Y",$spot);

$out=$out.$footer;
$out=ereg_replace("&amp;","&",$out);
$out=ereg_replace("#DATE#","$date",$out);
$out=ereg_replace("#ECHEANCE#","$date_echeance",$out);
$out=ereg_replace("#LIVRAISON#","$date_livraison",$out);
$out=ereg_replace("#NUMFACTURE#","$commande",$out);
$out=ereg_replace("#TOTAL#","$total",$out);
$out=ereg_replace("#",".",$out);

$file_out=fopen("./all.tex","w");
fwrite($file_out,$out);
fclose($file_out);

system("compile.bat > compile.out",$status);
print "res=$status";

//echo "<blockquote> $out </blockquote>";



if ($header) {
  print "<BR> <a href='../admin/index.php>  Retour Administration\n";
}


  		

?>
