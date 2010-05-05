<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>
<?php

$exe_print="\"c:\\Program Files\\Ghostgum\\gsview\\gsprint.exe\"   ";
$exe_python="c:\\Python24\\python.exe ..\\print\\demon.pyw";

//$dir_facture=""\Oyak\work\*";
$dir_facture="\facprint\*";

$header=1;
$nb_lignes_facture=30;

include("../inc/header.php");
$debug=0;

// lecture des masques
$dir=".";

$preambule=join("",file("$dir/preambule.tex"));
$header=join("",file("$dir/header.tex"));
$header2=join("",file("$dir/header2.tex"));
$body=join("",file("$dir/body.tex"));
$body_vide=join("",file("$dir/body_vide.tex"));
$footer=join("",file("$dir/footer.tex"));
$footer2=join("",file("$dir/footer2.tex"));
$conclusion=join("",file("$dir/conclusion.tex"));
$printer="default";
$copies=1;


$i=0;
$filenames=glob($dir_facture);
if ($filenames) {
  $file_out=fopen("all.tex","w");
  fwrite($file_out,$preambule);

  foreach ($filenames as $filename) {
    if ($i>0) {
      fwrite($file_out,"\\clearpage");
    }
    $i=$i+1;
    echo "<BR> Traitement factture $filename................................................";
    $out=make_facture($filename);
    fwrite($file_out,$out);
    if (!$debug)  {
       unlink($filename);
    }
  }

  fwrite($file_out,$conclusion);
  fclose($file_out);

  system("compile.bat > out",$status);
  //print "res=$status";
  print "<BR> $i crées<BR> ";

  @mkdir ("c:/Oyak/ToPrint",0755);
  if ($printer=="default") {
    copy ("all.ps", "c:/Oyak/ToPrint/facture.ps");
    copy ("all.ps", "c:/Oyak/facture.ps");
  }
  else {
    @mkdir ("c:/Oyak/ToPrint/$printer",0755);
    copy ("all.ps", "c:/Oyak/ToPrint/$printer/facture.ps");
    copy ("all.ps", "c:/Oyak/facture.ps");
  }

}
else {
  print "pas de facture en attente <BR>";
}

//echo "<blockquote> $out </blockquote>";


print "<BR> <a href='../admin/index.php>  Retour Administration\n";




function make_facture ($file) {
  global $debug, $header, $footer,$body,$body_vide,
    $nb_lignes_facture,$footer2,$header2,$printer,$copies;
  

  $document="";
  $nb_ligne=0;
  $total=0;
  $out=$header;

  $find=array();
  $replace=array();
  
  $lines=file($file);

  $nb_ligne=0;

  foreach ($lines as $line) {
    $champs = split("!",$line);
    $clef=array_shift($champs);
#print "<BR>";
#print_r($champs);

    $i=0;

# Z0,1!PR1!1!Bon de Livraison
    if (ereg("^Z0,1",$clef))  { 
      // nom de l'imprimante, nombre d'impression, type de document
	$printer=array_shift($champs);
	$copies=array_shift($champs);
	$document=array_shift($champs);	

	$cherche=sprintf("#%s#",$clef);
	$par=$document;
	array_push($find,$cherche);
	array_push($replace,$par);
    
        }

    if (ereg("^Z5,",$clef))  { // nouvelle ligne
      $nb_ligne=$nb_ligne+1;

      // si facture trop grande on cree une nouvelle page
      if ($nb_ligne>$nb_lignes_facture) {
	$out = $out.$footer2.$header2;
	$nb_ligne=0;
	echo "new pag!!!";
      }

      $current=$body;
      while (count($champs)) {
	$c=array_shift($champs);
	$i=$i+1;
	$cherche=sprintf("#Z5,%d#",$i);
	$current=str_replace($cherche,$c,$current);
        //print "<BR> $cherche -> $c";
      }
      $out=$out.$current;
    }
    else if (ereg("^Z6,1",$clef) or ereg("^Z8,1",$clef))  { // ligne Z6
      $cherche=sprintf("#%s#",$clef);
      if (count($champs)>0) {
	$par=array_shift($champs);
      }
      else {
	$par=" ";
      }
      array_push($find,$cherche);
      array_push($replace,$par);
      $i=1;
      while (count($champs)) {
	$c=array_shift($champs);
	$i=$i+1;
	$cherche=sprintf("#%s%d#",substr($clef,0,-1),$i);
	array_push($find,$cherche);
	array_push($replace,$c);
        //print "<BR> $cherche -> $c";
      }
    }
    else {
      $cherche=sprintf("#%s#",$clef);
      if (count($champs)>0) {
	$par=array_shift($champs);
      }
      else {
	$par=" ";
      }
      array_push($find,$cherche);
      array_push($replace,$par);
    }
  }
  
  if ($debug) {
    print print_r($find,TRUE)."<BR>";
    print_r($replace);
  }

  for ($i=$nb_ligne;$i<$nb_lignes_facture;$i++) {
    $out=$out.$body_vide;
  }

  # traitement type de document
  if ($document=="") {
    $document="Facture";
  }

  $cherche=sprintf("#%s#","Z0,1");
  $par=$document;
  array_push($find,$cherche);
  array_push($replace,$par);


  $out=$out.$footer;
  $out=str_replace($find,$replace,$out);

  // remplacement des champs non remplis par des blancs
  $out=ereg_replace("#Z.,.#","",$out);

  // traitement des choses en gras et petit caractères


  $out=ereg_replace("__PETIT__","{\\tiny ",$out);
  $out=ereg_replace("__GRAS__","\\textbf{ ",$out);
  $out=ereg_replace("__GRIS__","\\colorbox[gray]{0.8}{ ",$out);
  $out=ereg_replace("__petit__","}",$out);
  $out=ereg_replace("__gras__","}",$out);
  $out=ereg_replace("__gris__","}",$out);

  return $out;
}



  		

?>
