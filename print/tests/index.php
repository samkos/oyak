<?php include("../../inc/conf.php"); ?>
<?php include("../../inc/fonctions.php"); ?>
</HEAD>

<?php include("../../inc/header.php"); ?>


<center>

  <center>
  <table border="0" cellpadding="2" cellspacing="0">
    <tr>
    <td bgcolor="#99CCCC" colspan=6 align=center>  <b> imprimer les encours </b> </td> </tr> 
    <tr >
    <td> tous (<a xref="../traite.php&dest=screen&no_print=1">ecran</a> <a href="../traite.php">imprimante</a>)</td> </tr> <tr>
      <td>     <a href="../factures/traite.php">factures </a></td>
      <td> </td>
      <td> <a href="../../barcode/latex_barcode.php?action=file">etiquettes  </a> 
      <td> <a href="../impression/traite.php">autres documents   </a> </td>
  </tr>
  <tr><td><br></td></tr>
  <tr></tr>
  <tr>
    <td bgcolor="#99CCCC" colspan=6 align=center>  <b> tester des impressions specifiques</b> </td> </tr> 

<?php 
$files2test=array();

# fichier en test
$testing_files=array_merge(glob("./*/*")); 
if ($testing_files) {
  $waiting_files=array();
  while ($file=array_pop($testing_files)) {
    array_push($waiting_files,"../tests/"."$file");
  }
  $files2test=array_merge($files2test,$waiting_files);
 }
//print_r($files2test);

# factures en attente
$waiting_factures=glob("/facprint/*");
if ($waiting_factures) {
  $files2test=array_merge($files2test,$waiting_factures);
 }
# impression generale en attente
$waiting_factures=glob("/impprint/*");
if ($waiting_factures) {
  $files2test=array_merge($files2test,$waiting_factures);
 }
//print_r($files2test); 

$new_line=1;
$nb=0;
$nb_per_line=1;
while ($file=array_pop($files2test)) {
  if (preg_match("/~$/",$file)==0 and preg_match("/.svn/",$file)==0) {
    if (strpos($file,"fac/")>-1) { $chunk="fac";}
    if (strpos($file,"facprint/")>-1) { $chunk="fac";}
    if (strpos($file,"imp/")>-1) { $chunk="imp";}
    if (strpos($file,"impprint/")>-1) { $chunk="imp";}
    $file_to_print = "--".$chunk."=$file";
    $file=str_replace("../","",$file);
    $file=str_replace("./","",$file);
    if ($new_line) { print "<tr bgcolor=\"#ffffff\">"; $new_line=0; }
    print "<td bgcolor=\"#ffffff\"><a href='$file'>$file</a></td>";
    print "<td> <a href='../traite.php?dest=screen&file=$file_to_print&no_print=1'>ecran</a> 
                <a href='../traite.php?dest=print&file=$file_to_print'>imprimante</a> </td>";
    $nb=$nb+1;
    if ($nb>$nb_per_line) {
        print "</tr>";
	$new_line=1;
	$nb=0;
	}
    else {
        print "      <td> &nbsp; &nbsp;</td>";
    }
  }
}
if ($nb) {print"</tr>";}
print "</table>";  

?> 
</center>


<?php include("../../inc/footer.php"); ?>