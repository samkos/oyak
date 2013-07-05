<?php

include("../inc/conf.php");

if ($header) {
 include("../inc/header.php");
 print "<center> \n";
}

if ($liste) {
   $files = glob("$release_dir/*");

    foreach ($files as $filename) {
	 			$filename=str_replace("$release_dir/","",$filename);
				if ($filename!="CVS") {
      	      echo "<a href='./download.php?dwn=$filename' type=file> $filename </a> <BR>";
				}
   }
}
else {
   print "<BR> <a href='releases.php?liste=1'>Liste des releases disponibles</a>";
}


if ($header) {
 print "<BR> <a href='../admin/index.php>  Retour Administration\n";
}
?>
