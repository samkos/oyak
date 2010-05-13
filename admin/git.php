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
system("$commande > out 2>&1 ");
$res=file("out");

?>
<center>
<table>
<?php 
include("git_command.php"); 
?>
<tr> <td colspan=6 align=center> 
  	<a href='index.php'>  Retour administration </a> </td> </tr>
    <tr> <tr> <td> &nbsp; </td> </tr>
    <td bgcolor="#99CCCC" colspan=6 align=center>  <b> <?php print $commande; ?></b> </td> </tr> 
    <tr >
      <tr> <td colspan=6><quote>
  <?php 
  print join($res,"<br>");
  ?></quote>
  </td> <tr> <td align=center colspan=6> 
  	<a href='index.php'>  Retour administration </a> </td> </tr>
</table>

</body>

</html>

