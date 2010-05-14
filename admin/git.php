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



$outputfile= "c:/oyak/out";

if (0) {
// Setup the command to run from "run"
$cmdline = "cmd /C $commande " . " > $outputfile 2>&1";
print $cmdline;
// Make a new instance of the COM object
$WshShell = new COM("WScript.Shell");  
// Make the command window but don't show it.
$oExec = $WshShell->Run($cmdline, 0, true);
// Read the file file.
$res = file($outputfile);
}
else {
     exec(  " $commande  2>&1", $res);
}
//exec("git status  2>&1 ",$status);
//$status=file("c:/oyak/out");

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

