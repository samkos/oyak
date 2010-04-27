<?

//------------------------------------------------------------------------------
// niveau d'erreur
//------------------------------------------------------------------------------
//error_reporting(E_ALL);
error_reporting(E_ERROR);
//error_reporting(E_ERROR^E_PARSE^E_WARNING^E_NOTICE);
//error_reporting(E_ERROR^E_PARSE^E_WARNING);

if (false) {

//------------------------------------------------------------------------------
// rappatrie toutes les variables
//------------------------------------------------------------------------------
import_request_variables("gps","") ;
foreach (array_keys($_SESSION) as $var) {
  print "$var=".$_SESSION[$var];
  $GLOBALS[$var]=$_SESSION[$var];
}
}

if (false) {
//------------------------------------------------------------------------------
// flag debugging
//------------------------------------------------------------------------------
  $is_deb=0;
  $deb_opt=array(
	       "glob" => 0,       // montrer les variables globales
	        "post" => 0,      // montrer les variables postées
	       "o" => 0,          // message lie a la base : ordre sql
	       "do" => 0,         // message lie a la base : row par row
	       "f" =>  0,         // message lie a l'exploration des réperto
	       "env" => 0,        // message lie a l'environnement exterieur
	       "group" => 0,      // message lie a l'enregistrement group
	       "admin" => 0,      // message admin
	       "load" => 0,       // message load
	       "session" => 10,   // message session
	       "image" => 10,     // message image expose
         "broadcast" => 0        // message lie au broadcast
   );


  //print_debug("glob",print_r($GLOBALS,true));
  print_debug("post","POST : ".print_r($HTTP_POST_VARS,true));
  print_debug("session","SESSION : ".print_r($_SESSION,true));	 
}

function print_debug($flag,$message) {
	global $deb_opt;
	global $is_deb;
	if ($is_deb and $deb_opt[$flag]) {
	  echo "<color=red> *".$flag."* $message </color> <BR>";
		}
}

?>
