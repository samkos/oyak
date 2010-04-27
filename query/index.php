<?php

include("../inc/conf.php");


if ($header) {
  include("../inc/header.php"); 
  print "<center>";
}

if ($header) {

  print "<BR> <a href='index.php?commande=06;C3426;3700008000671!8!0067!!12!8.00!*;0!16!0012!!109!7.0!*;&vendeur=1&header=1'>Test passage commande</a>";
  print "<BR> <a href='index.php?commande=01;C3183;3700005000049!5!0004!!1.00!1.80!*l;3700022000107!22!0010!!1.00!1.23!*l;&vendeur=1&header=1'>Test passage commande avec *l</a>";
  print "<BR> <br> <a href='../admin/'>Retour a l'administration </a> <br />  <br>";
}

if ($commande) {
  $time=time();
  $query="insert into ".$prefixe_table."compteur values ('','$vendeur','$time')";
  if ($header) { print $query;}
  $req = mysql_query($query);

  $query="select compteur from  ".$prefixe_table."compteur where temps=$time";
  $req = mysql_query($query);
  while($ligne = mysql_fetch_array($req))
    { $compteur = $ligne["compteur"];}
		
  $compteur=sprintf("%05d",$compteur);
  $tag_date=date("Ymd");
  $nom_commande=sprintf("$compteur",$vendeur);
  $out_file="$commande_dir\\$tag_date".$nom_commande;
  if ($header) {print "<BR> sortie vers $out_file";}

  $fout=fopen($out_file,"w");
  $out_commande=sprintf("%02d;$commande",$vendeur);
  fwrite($fout,$out_commande);
  fclose($fout);
		
  if ($header) { print "<BR> commande = $commande <BR> compteur=$compteur";}
	
  $query="delete  from ".$prefixe_table."compteur where (compteur<".($compteur-5)." and vendeur='$vendeur')";
  if ($header) {print "<BR>".$query;}
  $req = mysql_query($query);
	

  print "0!$nom_commande";


   // recuperation nom Vendeur
  
  $req = mysql_query("select id,nom,prenom from ".$prefixe_table."vendeurs where id='$vendeur'");
  while($ligne = mysql_fetch_array($req))
    {
      $id = $ligne["id"];
      $nom = $ligne["nom"];
      $prenom = $ligne["prenom"];
      $vendeur_name ="$prenom $nom";
    }
	
  $articles=split(";",$commande);
  $client=array_shift($articles);

   // recuperation nom client

  $req = mysql_query("select id,clef,societe,ville from ".$prefixe_table."clients where clef='$client'");
  while($ligne = mysql_fetch_array($req))
    {
      $client_name = $ligne[societe]."/".$ligne[ville];
      $client_name = ereg_replace("\*.*$","",$client_name);
    }
	


  // impression BL

  $start_bltex='
      \documentclass[a4paper]{article}
      %
      \usepackage{graphicx}
      %
      \setlength{\voffset}{-4.5cm}
      \setlength{\hoffset}{-3.cm}

      \setlength{\oddsidemargin}{0pt}
      \setlength{\evensidemargin}{0.5cm}

      \setlength{\textwidth}{550pt}

      \setlength{\topmargin}{1cm}
      \setlength{\textheight}{26cm}

      \setlength{\headheight}{90pt}

      \setlength{\headsep}{0pt}
      \setlength{\parindent}{1cm}
      \setlength{\parskip}{0.2cm}

      \setlength{\marginparwidth}{0pt}
      \setlength{\marginparsep}{0pt}
      %
      \begin{document}';

  $in_bltex='

	    \begin{center}

                \begin{Large} \begin{bf} 
                       Bon de Livraison '."$nom_commande"." \\\\
                Date : ".date("d/m/y")." \\\\ Vendeur : $vendeur_name   \\\\ Client : $client_name \\\\ ".'
                \end{bf} \end{Large} 
              \\\\ \vspace{1cm} \\\\
	      \begin{tabular}{|p{4.5cm}|p{2cm}|p{1.5cm}|}
	        \hline
	        \textbf{\small{Designation}} &
	        \textbf{\small{Quant.}} & 
	        \textbf{\small{Prix}} & 
	        \hline
	          ';

  

  if ($header) {
    print "<BR> vendeur=$vendeur_name <BR> client=$client_name  <BR> param=$parametre";
    print '	<BR>	<table border="0" align="center" cellpadding="3" cellspacing="1" bgcolor="#000000" width="770">';
  }

  $total=0.;

  while ($article=array_shift($articles)) {
    $col=split("!",$article);
		$parametre=array_pop($col);
    $code=$col[0];
    $racourci=$col[1];  			
    $fournisseur=$col[2];  			
    $date=$col[3];  			
    $quantite=$col[4];
    $prix=$col[5];
    
    $total = $total+$prix*$quantite;
    
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
   
    $quantite=ereg_replace("\..*$","",$quantite);
    
    $in_bltex=$in_bltex
      ."\small{".$produit."} & \multicolumn{1}{r|}{".$quantite
      ."} & \multicolumn{1}{r|}{".sprintf("%7.2f",$prix)."} \\\\ \n";
      
	  
    if ($header) {
	print "
  		 <tr>
  		   <td bgcolor='#ffffff' align='right'> $quantite</td>
  		   <td bgcolor='#ffffff' align='left'> $produit ($racourci)</td>
  		   <td bgcolor='#ffffff' align='left'> $code</td>
				 <td bgcolor='#ffffff' align='left'> $societe ($fournisseur)</td>
  		   <td bgcolor='#ffffff' align='right'> $date</td>
  		   <td bgcolor='#ffffff' align='right'> $prix</td>
  		</tr>";
      }
  }


    $in_bltex=$in_bltex
      .'\hline \multicolumn{2}{|r|}{Total H.T.: '
      ."} & \multicolumn{1}{r|}{".sprintf("%7.2f",$total)."} \\\\ \n";
      
  
  $in_bltex=$in_bltex.'
    \hline
    \end{tabular} \end{center}';

  $end_bltex = '\end{document}';

	
	 if ($header) {
    print "</table> <br /><br />";
  }
  
	if ($parametre=="*l" or $parametre=="*L") {
      $nom="bl-$nom_commande";
      $file_out=fopen("$nom.tex","w");
      $inside_tex= '\begin{minipage}{0.5\linewidth}'.$in_bltex.'\end{minipage}'
	.'\hspace{1cm}'
	.'\begin{minipage}{0.5\linewidth}'.$in_bltex.'\end{minipage}';
      fwrite($file_out,$start_bltex.$inside_tex.$end_bltex);
      fclose($file_out);

			if ($header) {
			      print "compile.bat bl-$nom_commande";
			}			
 			system("compile.bat bl-$nom_commande > out" ,$result);
  }
	else {
			if ($header) {
			      print "Pas de sortie BL : pas *l   ";
			}			
	}	
	
  mysql_close($connect_db);

}

	 
?>