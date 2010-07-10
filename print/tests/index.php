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
      <td>     <a href="../traite.php">tous </a></td>
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
$files2test=array_merge(glob("./*/*"));
//print_r($files2test);

$new_line=1;
$nb=0;
$nb_per_line=1;
while ($file=array_pop($files2test)) {
  if (preg_match("/~$/",$file)==0 and preg_match("/.svn/",$file)==0) {
    $file = str_replace("./","",$file);
    $chunks = split("/",$file);
    $file_to_print = "--".$chunks[0]."=tests/".$file;
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