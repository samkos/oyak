<?php include("../../inc/conf.php"); ?>
<?php include("../../inc/fonctions.php"); ?>
</HEAD>

<?php include("../../inc/header.php"); ?>


<center>

<table border="0" align="center" cellpadding="3" cellspacing="1" bgcolor="#000000" width="770">
   <tr>
	  <td bgcolor="#99CCCC" align="center" width="25%"><b>Fichier</b></td>  
	  <td bgcolor="#99CCCC" align="center" width="25%"><b>Fichier</b></td>
	  <td bgcolor="#99CCCC" align="center" width="25%"><b>Fichier</b></td>
	  <td bgcolor="#99CCCC" align="center" width="25%"><b>Fichier</b></td>
   </tr>

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