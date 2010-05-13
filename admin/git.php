<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>
<?php

$exe_python=" demon.py";

include("../inc/header.php");
$debug=0;
$commande="git $action";
if ($comment) {
  $commande="git $action -m \"$comment\" ";
}
system("$commande > out");
$res=file("out");

?>
<center>
<table>
<?php 
include("git_command.php"); 
?>
<tr> <td colspan=6 align=center> 
  	<a href='index.php'>  Retour administration </a> </td> </tr>
    <tr>
    <td bgcolor="#99CCCC" colspan=6 align=center>  <b> gestion de configuration </b> </td> </tr> 
    <td bgcolor="#99CCCC" colspan=6 align=center>  <b> <?php print $commande; ?></b> </td> </tr> 
    <tr >
      <tr> <td colspan=6>
  <?php 
  print join($res,"<br>");
  ?>
  </td> <tr> <td align=center colspan=6> 
  	<a href='index.php'>  Retour administration </a> </td> </tr>
</table>

</body>

</html>

