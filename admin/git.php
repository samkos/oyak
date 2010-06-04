<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>
<?php include("./exec.php"); ?>
<?php

$exe_python=" demon.py";
$action="log HEAD~1..";
include("../inc/header.php");
$debug=0;
$commande="\"c:/Program Files/Git/bin/git.exe\" $action";
if ($comment) {
  $commande="\"c:/Program Files/Git/bin/git.exe\" $action -m \"$comment\" ";
}

print $commande;
$res = my_exec($commande);
$res="xxx";
print $res;
?>


