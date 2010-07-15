<?php

function latex_and_check($command, $filename) {
  global $debug;

  system("$command > out",$status);
  //print "res=$status";
  $lines=file("out");
  $l=array_shift($lines);
  $msg="";
  
  while($l){
    $msg=$msg."$l $BR";
    $l=array_shift($lines);
  }
  //print "//////////: $msg ////////////////";
  if (ereg("Emergency stop",$msg) or ereg("No pages of output",$msg) or ereg("ERREUR",$msg))  {
    $msg=ereg_replace("^.*aux))","ERREUR : ",$msg);
    $msg=ereg_replace("No pages of output.*$","No pages of ouput",$msg);
    print "$BR <BOLD> $br <B> ERREUR D'INTERPRETATION dans $filename !!!! </B> $BR $msg $BR";
    system("msg /time:5 * erreur de compilation dans $filename");
    $erreur=1;
    return -1;
  }
  else {
    // print_all("portrait");
    if ($debug) print "$BR $br <B> tout semble ok dans $filename !!!! </B> $BR $msg $BR";
    return 0;
  }
}


function code2latex($in) {
  // traitement des choses en gras et petit caractères

  $out=ereg_replace("__PETIT__","{\\tiny ",$in);
  $out=ereg_replace("__GRAS__","\\textbf{ ",$out);
  $out=ereg_replace("__GRIS__","\\colorbox[gray]{0.8}{ ",$out);
  $out=ereg_replace("__petit__","}",$out);
  $out=ereg_replace("__gras__","}",$out);
  $out=ereg_replace("__gris__","}",$out);

  return $out;

}


?>
