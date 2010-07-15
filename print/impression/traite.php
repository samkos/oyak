<?php include("../../inc/conf.php"); ?>
<?php include("../../inc/fonctions.php"); ?>
<?php include("../../inc/cmdline.php"); ?>
<?php include("../process.php"); ?>

<?php

$exe_print="\"c:\\Program Files\\Ghostgum\\gsview\\gsprint.exe\"   ";
$exe_python="c:\\Python24\\python.exe ..\\print\\demon.pyw";


@unlink("c:/Oyak/screen.pdf");


$dir_imprime="c:\impprint\*";

$header="";
$orientation="portrait";
$nb_lignes_imprime=18;
$erreur=0; 

if (!(isset($nohtml))) {
  include("../../inc/header.php");
  $br="<BR>";
 }
 else {
   $br="";
 }
if (!isset($debug)) { $debug=0;}

$not_deleting=0;

$filenames=glob($dir_imprime);
if ((isset($file))) {
  $filenames=array();
  array_push($filenames,$file);
  $not_deleting=1;
 }

if ($debug)   print_r($filenames);



if (!(isset($nohtml))) {
  ?>
  <center>
    <table>
    <tr>
    <td bgcolor="#99CCCC" colspan=6 align=center>  <b> resultat d impression </b> </td> </tr> 
    <tr >
    <tr> <td>
    <?php 
    }

// lecture des masques
$dir=".";

$preambule_portrait=join("",file("$dir/preambule.tex"));
$preambule_landscape=join("",file("$dir/preambule_landscape.tex"));
$header=join("",file("$dir/header.tex"));
$footer=join("",file("$dir/footer.tex"));
$conclusion=join("",file("$dir/conclusion.tex"));
$printer="default";
$copies=1;


$nb_pages_portrait=0;
$nb_pages_landscape=0;


if ($filenames) {


  foreach ($filenames as $filename) {

    $orientation="PORTRAIT";
    // traitement fichier en cours
    echo "$BR Traitement impression $filename................................................";
    $out=make_imprime($filename);

    // ecriture vers le fichier all_portrait ou all_landscape.tex


    if (strstr($orientation,"PAYSAGE")) {
      if ($nb_pages_landscape>0) {
	fwrite($file_landscape_out,"\\clearpage");
      }
      else {
	@unlink("all_landscape.tex");
	@unlink("all_landscape.dvi");
	@unlink("all_landscape.pdf");
	@unlink("all_landscape.aux");
	@unlink('c:/Oyak/imprime_landscape.pdf');
	$file_landscape_out=fopen("all_landscape.tex","w");
	fwrite($file_landscape_out,$preambule_landscape);
      }
      $nb_pages_landscape=$nb_pages_landscape+1;
      fwrite($file_landscape_out,$out);
    }
    else {
      if ($nb_pages_portrait>0) {
	fwrite($file_portrait_out,"\\clearpage");
      }
      else {
	@unlink("all_portrait.tex");
	@unlink("all_portrait.dvi");
	@unlink("all_portrait.pdf");
	@unlink("all_portrait.aux");
	@unlink('c:/Oyak/imprime_portrait.pdf');
	$file_portrait_out=fopen("all_portrait.tex","w");
	fwrite($file_portrait_out,$preambule_portrait);
      }
      $nb_pages_portrait=$nb_pages_portrait+1;
      fwrite($file_portrait_out,$out);
    }

    if ($not_deleting) {
      echo "\n$BR Effacement $filename NON FAIT   NON FAIT.... $BR $BR.";
    }
    else {
      unlink($filename);
      echo "\n$BR Effacement $filename OK.... $BR $BR.";
    }
  }

  $erreur=0;
  if ($nb_pages_portrait) {
    fwrite($file_portrait_out,$conclusion);
    fclose($file_portrait_out);

    if (!latex_and_check("compile_portrait.bat", $filename)) {
      print_all("portrait");
    }

  }

  if ($nb_pages_landscape) {
    fwrite($file_landscape_out,$conclusion);
    fclose($file_landscape_out);

    if (!latex_and_check("compile_landscape.bat", $filename)) {
      print_all("landscape");
    }
  }

  print "$BR ".($nb_pages_portrait+$nb_pages_landscape)." crées$BR ";


 }
 else {
   print "pas de documents a imprimer en attente $BR";
 }

if (!(isset($nohtml))) {
  ?>
  </td> <tr> <td align=center> 
    <a href='../tests/index.php'>  Retour test d impression </a> </td> </tr>
    </table>

    </body>

    </html>
    <?php
    }



function print_all($orientation) {
  global $printer,$noprint,$erreur;

  @mkdir ("c:/Oyak/ToPrint",0755);
  if (isset($noprint)) {
    print "<BR> ecran only";
    copy ("all_$orientation.pdf", "c:/Oyak/screen.pdf");
  }
  else {
    if ($printer=="default") {
      @copy ("all_$orientation.pdf", "c:/Oyak/ToPrint/imprime_$orientation.pdf");
      @copy ("all_$orientation.pdf", "c:/Oyak/imprime_$orientation.pdf");
    }
    else {
      @mkdir ("c:/Oyak/ToPrint/$printer",0755);
      @copy ("all_$orientation.pdf", "c:/Oyak/ToPrint/$printer/imprime_$orientation.pdf");
      @copy ("all_$orientation.pdf", "c:/Oyak/imprime_$orientation.pdf");
    }
  }
}

function make_imprime ($file) {
  global $debug, $orientation,$header, $footer,$body,$body_vide,
    $nb_lignes_imprime,$footer2,$header2,$printer,$copies;


  $document="";
  $nb_ligne=0;
  $total=0;
  $out=$header;

  $hline='\hline'."\n";

  $lines=file($file);

  $nb_ligne=0;
  $current_ligne=0;
  $esp_ligne=0.2;
  $esp_tab_ligne=0.43;

  foreach ($lines as $line) {
    $line=str_replace("%","\\%",$line);
    $champs = split("!",$line);
    $what=array_shift($champs);

    if ($debug) print "$BR what  = $what";
    if (ereg("^Z0,1",$what))  {
      // nom de l'imprimante, nombre d'impression, type de document
      $printer=array_shift($champs);
      $copies=array_shift($champs);
      $document=array_shift($champs);
      $orientation=array_shift($champs);
      if ($debug) print " <-- <B> OK </B>";
      next;
    }

    if (ereg("^EJECT",$what))  {
      // saut de page
      $out=$out.$footer."\n"."\\clearpage".$header."\n";
      if ($debug) print " <-- <B> OK </B>";
      next;
      $box_open=0;
      $current_ligne=0;
    }

    {


      $x=trim(array_shift($champs));
      $y=trim(array_shift($champs));
      if ($debug) print "x=$x,y=$y<BR>";
      if ($x=="-" and $y=="-") {
	$current_ligne=$current_ligne+$esp_ligne;
	$x=1; $y=$current_ligne;
      } 
      {
	if (!($x=="." and $y==".")) {  
	  $current_ligne=$y;
	  if ($box_open) {
	    $out=$out."}}\n";	
	  }
	  $out=$out."%x=/$x/;y=/$y/;c=/$current_ligne/\n".'\put('.$x.','.(29-$y).'){\shortstack[l]{' ;
	  $box_open=1;
		    
	}
	else {
	  $out=$out.'\\\\'."\n";
	}
      }
      // texte simple
      if ($what=="TXT") {
	$texte=array_shift($champs);
	$texte=ereg_replace('&','\&',$texte);
	$texte=ereg_replace('{','\{',$texte);
	$texte=ereg_replace('}','\}',$texte);
	$texte=ereg_replace('%','\%',$texte);
	$out=$out."$texte";
	$current_ligne=$current_ligne+$esp_ligne;

	if ($debug) print " <-- <B> OK </B>";
	next;
      }
		  
      // tableau
      if ($what=="TAB") {
	$tailles=split("=",array_shift($champs));
		    
	$current_ligne=$current_ligne+$esp_ligne;

	$out=$out.'\mbox{'."\n".'\begin{tabular}[t]{';
		    
	$col=1;
	while ($taille=array_shift($tailles)) {
	  $format_cell[$col]="p{".$taille."cm}";
	  $out=$out.$format_cell[$col];
	  $col=$col+1;
	}
	$out=$out."}\n";
		    
	for ($c=0;$c<$col-2;$c++) {
	  $out = $out." & ";
	}
	$out=$out.'\\\\';
		    
	$nb_lin=0;
	while ($line=array_shift($champs)) {
	  $cells=split("=",$line);
	  $nb_int=0;
	  $col=1;
	  while ($cell=array_shift($cells)) {
			
	    $fields=split(";",$cell);
	    $texte=array_shift($fields);
	    $texte=ereg_replace('&','\&',$texte);
	    $texte=ereg_replace('{','\{',$texte);
	    $texte=ereg_replace('}','\}',$texte);
	    $texte=ereg_replace('%','\%',$texte);
	    $format=array_shift($fields);
	    $masque='\multicolumn{1}{'.$format_cell[$col].'}{%s}';
			
	    // y a-t-il un format associe a la scene?
	    if ($format) {
	      $cadrage=substr($format,0,1);
	      $bords  =substr($format,1,1);
	      $couleur=substr($format,2,1);
	      $font   =substr($format,3,1);
	      $nb_cols=substr($format,4,2);
	      if (!$nb_cols) {$nb_cols=1;}
			  
	      //$out=$out."\n\n %===> texte=$texte; format=$format; cadrage='$cadrage'; bords='$bords'; couleur='$couleur'; font='$font'; nb_cols='$nb_cols';\n";
			  
	      $bord_left=""; $bord_right="";
	      switch($bords) {
	      case "g": $bord_left="|";                  break;
	      case "d": $bord_right="|";                 break;
	      case "c": $bord_left="|"; $bord_right="|"; break;
	      default : $bord_left=""; $bord_right="";
	      }
			  
	      switch($cadrage) {
	      case "d" : $cadrage="r"; break;
	      case "g" : $cadrage="l"; break;
	      case "." : $cadrage=$format_cell[$col]; break;
	      }
			  
	      $bord_left=""; $bord_right="";
	      switch($bords) {
	      case "g": $bord_left="|";                  break;
	      case "d": $bord_right="|";                 break;
	      case "c": $bord_left="|"; $bord_right="|"; break;
	      default : $bord_left=""; $bord_right="";
	      }
			  
	      switch($font) {
	      case "g": $in='\textbf{%s}'; break;
	      case "i": $in='\textsl{%s}'; break;
	      case "l": $in='\large{%s}'; break;
	      case "s": $in='\small{%s}'; break;
	      case "f": $in='\footnotesize{%s}'; break;
	      default : $in='%s';
	      }
			  
	      $masque='\multicolumn{'.$nb_cols.'}{'.$bord_left.$cadrage.$bord_right.'}{'.$in.'}';

	      switch($cadrage) {
	      case "T": $masque=$hline; break;
	      case "t": $masque='\cline{'.$col.'-'.($col+$nb_cols-1).'}';  break;
	      }
			  
	    }

	    if ($col>1) { $out = $out.'&';}
	    $col=$col+1;
	    $out=$out.sprintf($masque,$texte);
	  }
		      
	  if ($masque!=$hline) {
	    $out=$out.'\\\\ '."\n";
	  }
	  $current_ligne=$current_ligne+$esp_tab_ligne;
	}
		    
		    
	$out=$out.'\end{tabular}}'."\n";
	if ($debug) print " <-- <B> OK </B>";
	next;
      }
		  
    }
		
  }
  //	$out=$out."}}\n";
  $out=$out.$footer."\n\n";

  $out = code2latex($out);


  return $out;
}





?>
