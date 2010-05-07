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
<!--      <td /> <a href="../query/releases.php?liste=1&header=1">Télécharger logiciel vendeur</a></td> 
      <td> <a href="../factures/traite.php?noprint=1">Creer les factures  </a> </td> -->
      <td>     <a href="../traite.php">tous </a></td>
      <td>     <a href="../factures/traite.php">factures </a></td>
      <td> <a href="../../barcode/latex_barcode.php?action=file">etiquettes  </a> 
      <td> <a href="../impression/traite.php">autres documents   </a> </td>
  </tr>
  <tr></tr>
  <tr></tr>
  <tr></tr>
  <tr>
    <td bgcolor="#99CCCC" colspan=6 align=center>  <b> tester des impressions specifiques</b> </td> </tr> 

<?php 
$files2test=array_merge(glob("./*/*"));
//print_r($files2test);

$new_line=1;
$nb=0;
while ($file=array_pop($files2test)) {
      
  if (preg_match("/~$/",$file)==0 and preg_match("/.svn/",$file)==0) {
    if ($new_line) { print "<tr bgcolor=\"#ffffff\">"; $new_line=0; }
    print "<td bgcolor=\"#ffffff\">$file</td>";
    $nb=$nb+1;
    if ($nb>3) {
        print "</tr>\n-";
	$new_line=1;
	$nb=0;
	}
  }
}
if ($nb) {print"</tr>";}
print "</table>";  

?> 
</center>


<?php include("../../inc/footer.php"); ?>