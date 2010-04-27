<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>
<?php include("../verif.php"); ?>



<?php include("../inc/header.php"); 


/**
 * Increases the max. allowed time to run a script
 */
@set_time_limit(300);



	 system("run_vendeur.bat",$status);
	 print "resultat-> $status";
	 
?>
