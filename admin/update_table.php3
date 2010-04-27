<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>
<?php include("../verif.php"); ?>



<?php include("../inc/header.php"); 


/**
 * Increases the max. allowed time to run a script
 */
@set_time_limit(300);


if (!empty($file_client)) {

		print_r( $file); print" <BR>";
    copy("$file_client[0]","work/CLIENT.txt");
    copy("$file_produit[0]","work/PRODUIT.txt");
    copy("$file_client[0]","../pocketPC/CLIENT.txt");
    copy("$file_produit[0]","../pocketPC/ITEM.txt");
}

	 system("dump_sql.bat",$status);
	 system("clean_tables.bat",$status);
	 system("init_tables.bat",$status);
	 print "resultat-> $status";
	 
?>
