<?
$hauteur_etiquette="2.5 cm";
$largeur_etiquette="6.5 cm";
$entre_ligne_etiquette="0.2 cm";
$vertical_offset="-6.2 cm";
$horizontal_offset="-3.4 cm";
$nb_per_line=3;
$nb_per_page=8;

$exe_print="\"c:/Program Files/Ghostgum/gsview/gsprint.exe\"   ";
$printer="default";

?>

<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>



<?php include("../inc/header.php"); 


/**
 * Increases the max. allowed time to run a script
 */
@set_time_limit(300);

$format="|c|c|c|";
$format=" c c c";

print "$action ...<br />";

if ($action=="print") {
  foreach (array_keys($GLOBALS) as $var) {
    if (preg_match("/^choisis([0-9]+)/",$var,$reg)) {
      print $GLOBALS[$var]." : ".$GLOBALS["quantite".$reg[1]]."x".$GLOBALS["produit".$reg[1]]."<BR>";
      $barcodes[$reg[1]]=$GLOBALS["choisis".$reg[1]];
      $quantites[$reg[1]]=$GLOBALS["quantite".$reg[1]];
      $produits[$reg[1]]=$GLOBALS["produit".$reg[1]];
    }
  }
  //  $GLOBALS[$var]=$_SESSION[$var];
  print "----------------------------------";
}

else  {
  $dir_etiquette="\etiqprint\*";
  $filenames=glob($dir_etiquette);
  $nb_etiq=0;

  foreach ($filenames as $filename) {
    echo "<BR> Traitement fichier etiquette $filename................................................";
    $lines=file($filename);
    foreach ($lines as $line) {
      $champs = split("!",$line);
      $clef=array_shift($champs);
      //print "$line, xxxxxx $clef <BR>";
      
      if (ereg("^Z0,1",$clef))  { 
	// nom de l'imprimante, nombre d'impression, type de document
	$printer=array_shift($champs);
	$copies=array_shift($champs);
	$document=array_shift($champs);	
      }

      if (ereg("^Z2,",$clef))  { // nouvelle etiquette
	$nb_etiq=$nb_etiq+1;
	$barcode=array_shift($champs);
	$produit=array_shift($champs);
	$barcodes[$nb_etiq]=$barcode;
	$quantites[$nb_etiq]=1;
	$produits[$nb_etiq]=$produit;
	print "$barcode : 1 x $produit <BR>";
      }
    }
    unlink($filename);
  }
  print "----------------------------------";
}


  //print_r($barcodes);
  $ftex=fopen($tex_file,"w");
  $fpython=fopen($python_file,"w");
  fwrite($ftex,
	 '\documentclass[a4paper]{article}
   %
   \usepackage{graphicx}
   %
   \setlength{\voffset}{'.$vertical_offset.'}
   \setlength{\hoffset}{'.$horizontal_offset.'}

   \setlength{\oddsidemargin}{0pt}
   \setlength{\evensidemargin}{0.5cm}

   \setlength{\textwidth}{550pt}

   \setlength{\topmargin}{1cm}
   \setlength{\textheight}{2cm}

   \setlength{\headheight}{90pt}

   \setlength{\headsep}{0pt}
   \setlength{\parindent}{1cm}
   \setlength{\parskip}{0.2cm}

   \setlength{\marginparwidth}{0pt}
   \setlength{\marginparsep}{0pt}   %
   \begin{document}

   \begin{small}
   \begin{tabular}{'.$format.'}
   ');

  fwrite($fpython,"codebarlist = [\\");
	 
  $nb_lignes=0;



  // capture info code barre

  $sql_query = "select id,titre,stock,barcode from ".$prefixe_table."produits  ";

  print "<BR> $sql_query <BR>";
  $req = mysql_query("$sql_query ");

  $nb=0;
  
  $name_line="";
  $etiquette_line="";

  foreach (array_keys($barcodes) as $key) {
    for ($i=1;$i<=$quantites[$key];$i++) {
      $python_line=sprintf('
			    ("%s", "%s", "%s"),',$barcodes[$key],$produits[$key],"99.99", $barcodes[$key]); 
      fwrite ($fpython, $python_line);
      fwrite ($fpython, $python_line);
      $produit=substr($produits[$key],0,17);
		 
      $name_line=$name_line."\n \\begin{bf} \\begin{large} \\parbox{6cm}{\\begin{center}".$produit."\\end{center}} \\end{large} \\end{bf} ";
      $etiquette_line=$etiquette_line.sprintf("\includegraphics[height=$hauteur_etiquette,width=$largeur_etiquette]{%s.eps}  ",$barcodes[$key]);
      $nb=$nb+1;
      if ($nb<$nb_per_line) {
	$name_line=$name_line."&";
	$etiquette_line=$etiquette_line."&";
      }
      else {
	$nb=0;
	$nb_lignes=$nb_lignes+1;
	fwrite($ftex,"  $name_line \\\\   ");
	fwrite($ftex," \\vspace{-0.7cm} \\\\ $etiquette_line \\\\   ");
	$name_line="";
	$etiquette_line="";
  
	if ($nb_lignes==$nb_per_page) {
	  fwrite ($ftex,' \\ \end{tabular} \eject \n' );
	  fwrite ($ftex,'\begin{tabular}{'.$format.'} ');
	  $nb_lignes=0;
	}
	else {
	  fwrite($ftex," \\vspace{-0.6cm} \\\\ \\vspace{".$entre_ligne_etiquette."} \\\\    ");
	}
      }
    }
  }
	
fwrite($ftex," $name_line\\\\   ");
fwrite($ftex," $etiquette_line \\\\  ");
fwrite ($ftex,"\\end{tabular}    \\end{small} \\end{document}\n");
fwrite($fpython,"];
		");

fclose($ftex);
fclose($fpython);

//system("compile.bat > work/compile.out ",$status);
system("compile.bat  ",$status);
print "resultat-> $status";

  if ($printer=="default") {
    copy ("work/barcodes.ps", "c:/Oyak/ToPrint/barcodes.ps");
    copy ("work/barcodes.ps", "c:/Oyak/barcodes.ps");
  }
  else {
    @mkdir ("c:/Oyak/ToPrint/$printer",0755);
    copy ("work/barcodes.ps", "c:/Oyak/ToPrint/$printer/barcodes.ps");
    copy ("work/barcodes.ps", "c:/Oyak/barcodes.ps");
  }





?>

<script language="JavaScript" type="text/javascript">





function loadPage() {

  document.location.href = "../index.php";
}

//loadPage();



</script>



 
<br>
<?php include("../inc/footer.php"); ?>
