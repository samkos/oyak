<?php include("../../inc/conf.php"); ?>
<?php include("../../inc/fonctions.php"); ?>
<?php

$header=1;

if ($header) {
 include("../../inc/header.php");
 print "<center> \n";
}

if (!$commande) {

   // recuperation nom Vendeur
	 
	 $req = mysql_query("select id,nom,prenom from ".$prefixe_table."vendeurs order by nom,prenom,id ");
	 while($ligne = mysql_fetch_array($req))
	 {
	   $id = $ligne["id"];
	   $nom = $ligne["nom"];
	   $prenom = $ligne["prenom"];
		 $vendeur[$id]="$prenom $nom";
		}
		
		
		
	 // liste fichiers	
   $files = glob("$commande_dir/*");
	
?>

<br />
<br />
<table border="0" align="center" cellpadding="3" cellspacing="1" bgcolor="#000000" width="770">
   <tr>
      <td bgcolor="#99CCCC" align="center" width="15%"><b>Fichier</b></td>
	  <td bgcolor="#99CCCC" align="center" width="15%"><b>Date</b></td>
	  <td bgcolor="#99CCCC" align="center" width="15%"><b>Vendeur</b></td>
	  <td bgcolor="#99CCCC" align="center" width="20%" ><b>Client</b></td>
	  <td bgcolor="#99CCCC" align="center" width="40%" colspan="3"><b>Actions</b></td>
   </tr>
<?php
	  $clefs=array();
	  if (count($clefs)==0) {
	    print "<tr><td colspan=9 align=center  bgcolor=\"#ffffff\">pas de commandes en cours... </td></tr>";
	  }
	  else
	  {
	  foreach ($files as $filename) {
		    $clef=date("YmdHis", filectime($filename));
				array_push($clefs,$clef);
				$file_full[$clef]=$filename;
		}
		// print_r($clefs);
                sort($clefs,SORT_STRING);
		while ($clef=array_shift($clefs)){
				
				$filename=$file_full[$clef];
				
		    $date=date("F d Y H:i:s.", filectime($filename));
				
				
				$lines=file($filename);
				
				foreach ($lines as $line_num => $line) {
				    //echo 'Ligne No <strong>' . $line_num . '</strong> : ' . htmlspecialchars($line) . '<br />'."\n";
						$commande[0]=$line;
        }				

				
				//print_r($commande);
				$commande[0]=preg_replace('/!\s*/',"!",$commande[0]);
				$ligne=split(";",$commande[0]);
				//print_r($ligne);
				
	 			$filename=str_replace("$commande_dir/","",$filename);
				
				$vendeur_name=$vendeur[intval($ligne[0])];
				$client_name=$client[intval($ligne[1])];
				$client_name=$ligne[1];


				// recuperaton nom Client
		
				$sql_order="select societe,ville from ".$prefixe_table."clients where clef='$ligne[1]'";
        			$req = mysql_query($sql_order);
				//print $sql_order."<BR>";
        			while($ligne = mysql_fetch_array($req))
        			{
        			 $societe    = $ligne["societe"];
        			 $ville = $ligne["ville"];
        			 $client_name="$societe <BR> ($ville)";
        			}                       
				
				if ($filename!="CVS") {
  	      echo "<tr> <td bgcolor=\"#ffffff\" align=\"center\" > $filename <BR> </td>";
  	      echo "     <td bgcolor=\"#ffffff\" align=\"center\" > $date  <BR> </td>";
  	      echo "     <td bgcolor=\"#ffffff\" align=\"center\" > $vendeur_name  <BR> </td>";
  	      echo "     <td bgcolor=\"#ffffff\" align=\"center\" > $client_name  <BR> </td>";
  	      echo "     <td bgcolor=\"#ffffff\" align=\"center\" > <a href=\"./index.php?commande=$filename&action=lire&contenu=$commande[0]&vendeur=$vendeur_name&client=$client_name&date=$date\" >Consulter</a> <BR> </td>";
  	      echo "     <td bgcolor=\"#ffffff\" align=\"center\" > <a href=\"./index.php?commande=$filename&action=brute&contenu=$commande[0]&vendeur=$vendeur_name&client=$client_name&date=$date\" >Forme brute</a> <BR> </td>";
  	      echo "     <td bgcolor=\"#ffffff\" align=\"center\" > <a href=\"../factures/index.php?commande=$filename&action=imprimer&contenu=$commande[0]&vendeur=$vendeur_name&client=$client_name&date=$date\" >Générer</a> <BR> </td>";
					echo "</tr>";
				}
   }}
	 echo "</table> <br /> <br /> <br />";

}
else {
?>
		<br />
		<br />
		<table border="0" align="center" cellpadding="3" cellspacing="1" bgcolor="#000000" width="770">
<?php		 
    print "<tr> ";
	  print "<td bgcolor='#99CCCC' align='center' colspan=9>  Commande : $commande - $date</td>";
		print "</tr>";
		
    print "<tr> ";
	  print "<td bgcolor='#99CCCC' align='left' colspan=4>  Vendeur : $vendeur </td>";
	  print "<td bgcolor='#99CCCC' align='right' colspan=6> Client : $client <BR> </td>";
		print "</tr>";
		
		if ($action=="brute") {
		  print "<tr> ";
	    print "<td bgcolor='#ffffff' align='left' colspan=5>  $contenu</td>";
		  print "</tr>";
      print "</table> <br /><br />";

			
      echo "     <a href='./index.php?commande=$commande&action=lire&contenu=$contenu&vendeur=$vendeur&client=$client&date=$date'>Commande formatée</a> <BR> ";
 
    }

		
		if ($action=="lire") {		
?>
     	<tr>
        <td bgcolor="#99CCCC" align="center" width="45%" colspan=3><b>Produit</b></td>
        <td bgcolor="#99CCCC" align="center" width="30%" colspan=2><b>Fournisseur</b></td>
        <td bgcolor="#99CCCC" align="center" width="15%" rowspan=2><b>Date</b></td>
  	    <td bgcolor="#99CCCC" align="center" width="15%" rowspan=2><b>Quantite</b></td>
  	    <td bgcolor="#99CCCC" align="center" width="15%" rowspan=2><b>Prix</b></td>
  	    <td bgcolor="#99CCCC" align="center" width="15%" rowspan=2><b>Parametre</b></td>
       </tr>
  
     	<tr>
        <td bgcolor="#99CCCC" align="center" width="15%"><b>Libellé</b></td>
        <td bgcolor="#99CCCC" align="center" width="15%"><b>Code Barre</b></td>
        <td bgcolor="#99CCCC" align="center" width="15%"><b>Code Court</b></td>
        <td bgcolor="#99CCCC" align="center" width="15%"><b>Société</b></td>
        <td bgcolor="#99CCCC" align="center" width="15%"><b>Code</b></td>
       </tr>
  <?php
      $lignes=split(";",$contenu);
	array_shift($lignes);
	array_shift($lignes);
	while ($ligne=array_shift($lignes)) {
	  $col=split("!",$ligne);
	  $code=$col[0];
	  $racourci=$col[1];  			
	  $fournisseur=$col[2];  			
	  $date=$col[3];  			
	  $quantite=$col[4];
	  $prix=$col[5];
	  $parametre=$col[6];
	  
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
  		   <td bgcolor='#ffffff' align='right'> $parametre </td>
  		</tr>";
  		}
  		
      print "</table> <br /><br />";

			
      echo "     <a href='./index.php?commande=$commande&action=brute&contenu=$contenu&vendeur=$vendeur&client=$client&date=$date' >Commande brute</a> <BR> ";
  		}
		

    print "<BR> <a href='./index.php'>  Retour Commandes </a> <br /> <BR> \n";

}


if ($header) {
 print "<BR> <a href='../../admin/index.php>  Retour Administration\n";
}
?>
