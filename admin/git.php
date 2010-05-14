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



$outputfile= "c:/oyak/out";

if (0) {
   $cmd = " start /b $commande > $outputfile 2>&1";
   if ( ($fh = popen($cmd, 'w')) === false )
        die("Open failed: ${php_errormsg}\n");

    fwrite($fh, "Line one\nLine two\n");

    pclose($fh); 
   PsExecute(" $commande > $outputfile 2>&1");
   // Read the file file.
   $res = file($outputfile);
}
else {
    // exec(  ' start /B "xx" "git.exe" ', $res, $ret);
    //exec('start /B "window_name" "path to your exe"',$output,$return); 
    $done = "c:\\oyak\\done.txt";
    $batch = 'c:/oyak/exec.bat';
    @unlink($done);
    $fp = fopen($batch, 'w');
    fwrite($fp, "@echo off\n e:\ncd \"\\Program Files\\EasyPHP 2.0b1\\www\\phpmyfactures\\admin\"\n");
    fwrite($fp, "$commande \n");  
    fwrite($fp, "echo done > $done\n");  
    fclose($fp);
    $WshShell = new COM("WScript.Shell");
    $oExec = $WshShell->Run("cmd /C $batch > $outputfile 2>&1", 0, true);
    //print $oExec;
    //sleep(1);

    
   // Read the file file.
   $res = file($outputfile);

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

