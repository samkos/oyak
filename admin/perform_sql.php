<?php 
include("../inc/conf.php"); 
include("../inc/fonctions.php"); 
include("../verif.php"); 


if ($header) {
 include("../inc/header.php"); 
}

/**
 * Increases the max. allowed time to run a script
 */
@set_time_limit(300);

if ($order)  {
   
	 if ($header) {
	   system("$order.bat",$status); print "resultat-> $status";}
	 else {
	 system("$order.bat > out",$status);
 	 header("location: index.php?message=Commande exécutée");
	 }

}

?>
