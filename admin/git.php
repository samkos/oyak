<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>
<?php include("./exec.php"); ?>
<?php

$exe_python=" demon.py";

include("../inc/header.php");
$debug=0;
$commande="git $action";
if ($comment) {
  $commande="git $action -m \"$comment\" ";
}


$res = my_exec($commande);

?>
<center>
<table>
<?php 
include("git_command.php"); 
?>
</tr>
<tr> <td colspan=6 align=center> 
<? print $status; ?>
</td>
</tr>
<tr> <td colspan=6 align=center> 
  	<a href='index.php'>  Retour administration </a> </td> </tr>
    <tr> <tr> <td> &nbsp; </td> </tr>
    <td bgcolor="#99CCCC" colspan=6 align=center>  <b> <?php print $commande; ?></b> </td> </tr> 
    <tr >
      <tr> <td colspan=6><quote>
  <?php 
  if ($action=="branch -a") {
    while ($res) {
      $r = array_shift($res);
      if ($r[0]=="*") {
         print "$r<BR>";
      }
      else {	 
        print "<a href='git.php?action=checkout $r'>$r</a><BR>";
      }
    }
  }
  else { if (substr($action,0,3)=="log") {
    while ($res) {
      $r = array_shift($res);
      $rs = split(" ",$r);
      if ($rs[0]=="commit") {
        print "commit <a href='git.php?action=checkout $rs[1]'>$rs[1]</a><BR>";
      }
      else {	 
         print "$r<BR>";
      }
    }
  }
  else {
    print join($res,"<br>");
  } }
  ?></quote>
  </td> <tr> <td align=center colspan=6> 
  	<a href='index.php'>  Retour administration </a> </td> </tr>
</table>

</body>

</html>

