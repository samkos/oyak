<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>
<?php include("../admin/exec.php"); ?>
<?php

$exe_python=" demon.py";

include("../inc/header.php");
$debug=0;
$commande="c:\\Python24\\python.exe -u $exe_python  --once $file";
if ($debug) {
   $commande=$commande." --debug";
}
if ($no_print) {
   $commande=$commande." --noprint";
}
//print $commande;
$res=my_exec("$commande");

?>
<center>
<table>
    <tr>
    <td bgcolor="#99CCCC" colspan=6 align=center>  <b> resultat d'impression </b> </td> </tr> 
    <td bgcolor="#99CCCC" colspan=6 align=center>  <b> <?php print $commande; ?></b> </td> </tr> 
    <tr >
      <tr> <td>
  <?php 
  print join($res,"<br>");
  ?>
  </td> <tr> <td align=center> 
  	<a href='tests/index.php'>  Retour test d'impression </a> </td> </tr>
</table>

</body>

</html>

