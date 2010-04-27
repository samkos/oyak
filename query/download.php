<?

include("../inc/conf.php");

if($dwn) {
   
   // ob_clean(); // Vide le buffer (v >= 4.2)

   // Dialogue de téléchargement
   //header("content-type: application/octet-stream");
   // seulement pour application/octet-stream !
   header("Content-Disposition: attachment; filename=".$dwn);

   // Ouvrir avec MSWord
   // header("content-type: application/msword");
   // Ouvrir avec MSExcel
   // header("content-type: application/vnd.ms-excel");
   // Ouvrir en Text
   header("content-type: text/plain");

   // voir aussi http://dev.nexen.net/scripts/details.php?scripts=354

   flush(); // Envoie le buffer

   readfile($release_dir."/".$dwn); // Envoie le fichier

} else { ?>

   <A href="download.php?dwn=download.php">Test</A>

<?php } ?>