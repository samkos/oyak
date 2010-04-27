<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>



<?php include("../inc/header.php"); 
/**
 * Increases the max. allowed time to run a script
 */
@set_time_limit(300);

$nb_all=80;
$nb_per_page=14;

// debut du document

print "----------------------------------";
$ftex=fopen($tex_file,"w");
$fpython=fopen($python_file,"w");							
fwrite($ftex,
   '
   \documentclass[a4paper]{article}
   %
   \usepackage{graphicx}
   %
   \setlength{\voffset}{-6.5cm}
   \setlength{\hoffset}{-2.6cm}

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
   \begin{document}

   \begin{small}

   \begin{tabular}{|c|c|c|c|c|c|}
   \hline
   ');

fwrite($fpython,"codebarlist = [");
$nb_lignes=0;


// capture info code barre

$sql_query = "select id,titre,stock,barcode from ".$prefixe_table."produits  ";

print "<BR> $sql_query <BR>";
$req = mysql_query("$sql_query ");

$nb=0;

while(($ligne = mysql_fetch_array($req)) and $nb<$nb_all)
{
  $nb++;
  $id = $ligne["id"];
  $produit = $ligne["titre"];
  $stock = $ligne["stock"];
  $barcode = $ligne["barcode"];
  $id_d = sprintf("%08s",$id);
  $price="99.99";


  fwrite($ftex, sprintf("\includegraphics[height=1.5 cm,width=4 cm]{%s.eps} &  ",$barcode) );
  fwrite($ftex,sprintf(" %s  & %s & %s \\\\ \\hline  ",$barcode,$produit,$price) );
  $python_line=sprintf('("%s", "%s", "%s"),',$barcode,$price,$produit, $barcodes[$key]);			
  fwrite ($fpython, $python_line);
  
  $nb_lignes=$nb_lignes+1;
  
  if ($nb_lignes==$nb_per_page) {
    fwrite ($ftex,' \\ \hline \end{tabular} \eject \n' );
    fwrite ($ftex,'\begin{tabular}{|c|c|c|c|c|c|} \hline');
    $nb_lignes=0;
  }
}
		
fwrite ($ftex,"\\hline \\end{tabular}    \\end{small} \\end{document}\n");
fwrite($fpython,"];
		");

fclose($ftex);
fclose($fpython);

if (isset($print)) {
  system("latexcode.bat ",$status);
  print "resultat-> $status";
  
  system("dvi2ps.bat  ",$status);
  print "resultat-> $status";
}



?>

<?php include("../inc/footer.php"); ?>
