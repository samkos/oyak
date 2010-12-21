<?php include("../../inc/conf.php"); ?>
<?php include("../../inc/fonctions.php"); ?>
<?php include("../../inc/cmdline.php"); ?>
<?php include("../process.php"); ?>
<?php

$exe_print="\"c:\\Program Files\\Ghostgum\\gsview\\gsprint.exe\"   ";
$exe_python="c:\\Python24\\python.exe ..\\print\\demon.pyw";

//$dir_facture=""\Oyak\work\*";
$dir_facture="c:\facprint\*";
$filenames=glob($dir_facture);

$header=1;
$nb_lignes_facture1=24;
$nb_lignes_facture2=24;

if (!isset($debug)) {
  $debug=0;
 }

@unlink("c:/Oyak/screen.pdf");

if (!(isset($nohtml))) {
  include("../../inc/header.php");

  echo  "
<center>
<table>
    <tr>
    <td bgcolor='#99CCCC' colspan=6 align=center>  <b> resultat d'impression </b> </td> </tr> 
    <tr >
      <tr> <td>
";
 }
$del_file=1;

if ((isset($file))) {
  print_r($filenames);
  $filenames=array();
  array_push($filenames,$file);
  print_r($filenames);
  $del_file=0;
 }

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

if ($filenames) {
  $file_out=fopen("all.tex","w");
  fwrite($file_out,$preambule);

  foreach ($filenames as $filename) {
    if ($i>0) {
      fwrite($file_out,"\\clearpage");
    }
    $i=$i+1;
    if (!$nohtml) { echo "<BR";}
    echo "Traitement factture $filename....................";
    $out=make_facture($filename);
    fwrite($file_out,$out);
    if (!$debug and $del_file)  {
      unlink($filename);
    }
  }

  fwrite($file_out,$conclusion);
  fclose($file_out);

  if (!latex_and_check("compile.bat", $filename)) {

    //print "res=$status";
    print "<BR> $i crées<BR> ";

  
    // impression...
    if (isset($noprint)) {
      print "<BR> ecran only";
      copy ("all.pdf", "c:/Oyak/screen.pdf");
    }
    else {
      
      @mkdir ("c:/Oyak/ToPrint",0755);
      if ($printer=="default") {
	copy ("all.pdf", "c:/Oyak/ToPrint/facture.pdf");
	copy ("all.pdf", "c:/Oyak/facture.pdf");
      }
      else {
	@mkdir ("c:/Oyak/ToPrint/$printer",0755);
	copy ("all.pdf", "c:/Oyak/ToPrint/$printer/facture.pdf");
	copy ("all.pdf", "c:/Oyak/facture.pdf");
      }
    }
  }
 }

 else {
   print "pas de facture en attente ";
 }

//echo "<blockquote> $out </blockquote>";

if (!isset($nohtml)) {
  ?>


  </body>

    </html>

    <?php
    }

function make_facture ($file) {
  global $debug, $header, $footer,$body,$body_vide,
    $nb_lignes_facture1,
    $nb_lignes_facture2,
    $footer2,$header2,$printer,$copies;
  

  $document="";
  $nb_ligne=0;
  $total=0;
  $out=$header;

  $find=array();
  $replace=array();
  
  $lines=file($file);

  $nb_ligne=0;
  $nb_lignes_facture=$nb_lignes_facture1;

  foreach ($lines as $line) {
    // traitement des choses en gras et petit caractères
    $line = code2latex($line);
    $line=rtrim($line);
    $champs = split("!",$line);
    $clef=trim(array_shift($champs));


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
      print " $BR printer : !!$printer!!$BR  copies : !!$copies!!$BR document : !!$document!!$BR orientation : !!$orientation!!";
    
    }

    if (ereg("^Z5,",$clef))  { // nouvelle ligne
      $nb_ligne=$nb_ligne+1;

      // si facture trop grande on cree une nouvelle page
      if ($nb_ligne>$nb_lignes_facture) {
	$out = $out.$footer2.$header2;
	$nb_ligne=0;
        $nb_lignes_facture=$nb_lignes_facture2;
	echo "new pag!!!";
      }

      $current=$body;
      while (count($champs)) {
	$c=array_shift($champs);
	$i=$i+1;
	$cherche=sprintf("#Z5,%d#",$i);
	$width=33;
	//print strlen($c); print"\n";
        if (strlen($c)>$width) {
	  print strlen($c); print "new_line /$c/\n"; 
	  //$c="\\shorstack{".substr($c,1,32)."\\hfill\\ ".substr($c,33,99)."}";
	  //$c="$\\shorstack[l]{".substr($c,0,32)."\\\\".substr($c,31,99)."}$";
	  $c=substr($c,0,$width-1)."\\-".substr($c,$width-1,99);
	  $nb_ligne=$nb_ligne+1;
	}
	$c=str_replace(" ",'~',$c);
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
  $out=ereg_replace("#Z.,..#","",$out);

  // traitement des choses en gras et petit caractères
  $out = accent2latex($out);

  return $out;
}



  		

?>
