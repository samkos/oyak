<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>
<?php

$exe_python=" demon.py";

include("../inc/header.php");
$debug=0;
$commande="git $action";
system("$commande > out");
$res=file("out");

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
  	<a href='index.php'>  Retour administration </a> </td> </tr>
</table>

</body>

</html>

