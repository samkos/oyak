<?php


if (!(isset($fonction_inc))) {
  $fonction_inc=1;

    // anti spam
    function email_encode($string) 
    { 
    // CETTE FONCTION VA ENCODER L ADRESSE EMAIL
    $ret_string=""; 
    $len=strlen($string); 
    for($x=0;$x<$len;$x++) 
    { 
    $ord=ord(substr($string,$x,1)); 
    $ret_string.="&#$ord;"; 
    } 
    return $ret_string; 
    }

    // Teste la validité d'une adresse e-mail 
    function EmailOK($email) 
    { 
    return eregi("^([&_a-z0-9-]+(\.[&_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)+)$",$email); 
    } 

    // converti une date xxxx-xx-xx en xx/xx/xxxx
    function conver_date($date)
    {
    return ereg_replace('^([0-9]{2,4})-([0-9]{1,2})-([0-9]{1,2})$', '\\3/\\2/\\1', $date);
    }

    // Teste la validité d'un nom d'utilisateur 
    function okPseudo($pseudo) 
    { 
    return eregi("^[A-Z0-9][A-Z0-9_]{2,19}$",$pseudo); 
    } 

    // Teste la validité d'une URL 
    function okURL($url) 
    { 
    return eregi("^(http|https)://[_A-Z0-9-]+\.[_A-Z0-9-]+[.A-Z0-9-]*(/~|/?)[/_.A-Z0-9#?&=+-]*$",$url); 
    }

    // Teste la validité d'une image 
    function okImage($url) 
    { 
    return eregi("^http://[_A-Z0-9-]+\.[_A-Z0-9-]+[.A-Z0-9-]*/~?[/_.A-Z0-9-]*[_.A-Z0-9-]+\.(jpg|gif|png)$",$url); 
    } 

    // Tronque une chaine de caractères 
    function trunc_str($texte,$length,$end_str="...") 
    { 
    if(strlen($texte) <= $length) return $texte; 
    return trim(substr($texte,0,$length))."$end_str"; 
    } 

    // Teste la validité d'un code couleur 
    function Test_coul($code) 
    { 
    return(eregi('^#[0-9A-F]{6}$',$code)); 
    } 

    // Vérifie la validité d'une date de format YYYY-mm-dd ou YYYY-mm-dd HH:mm:ss 
    function okDate($date) 
    { 
    if(($len_date=strlen($date)) == 10) 
    { 
    $date=explode("-",$date); 
    return checkdate($date[1],$date[2],$date[0]); 
    } 
    elseif($len_date == 19) 
    { 
    $date=ereg_replace("^(.{4})-(.{2})-(.{2}) (.{2}):(.{2}):(.{2})$","\\1-\\2-\\3-\\4-\\5-\\6",$date); 
    $date=explode("-",$date); 
    if(!checkdate($date[1],$date[2],$date[0])) return false; 
    if($date[3] < '0' || $date[3] > '23') return false; 
    if($date[4] < '0' || $date[4] > '59') return false; 
    if($date[5] < '0' || $date[5] > '59') return false; 
    return true; 
    } 
    return false; 
    } 

    // Formate une date de type YYYY-mm-dd (HH:ii:ss) au format jj/mm/aaaa ou jj/mm/aaaa à Hhm 
    function date_formatx($date) 
    { 
    if(($len_date=strlen($date)) == 10) 
    { 
    return eregi_replace("([0-9]{4})-([0-9]{2})-([0-9]{2})","\\3/\\2/\\1",$date); 
    } 
    elseif($len_date == 19) 
    { 
    return eregi_replace("([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2}):([0-9]{2})","\\3/\\2/\\1 à \\4h\\5",$date); 
    } 
    return false; 
    } 

    // Transforme une URL ou une adresse e-mail en lien HTML 
    function lienhtml($chaine) 
    { 
    if(!eregi("(<a|<img|<script|<iframe)",$chaine)) 
    { 
    $chaine=eregi_replace("(https?|ftp)://([[:alnum:]#?/&=._+-]+)","<a href=\"\\1://\\2\" target=\"_blank\">\\1://\\2</a>",$chaine); 
    $chaine=eregi_replace("([_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9?=-]+)+)","<A HREF=\"mailto:\\1\">\\1</A>",$chaine); 
    } 
    return $chaine; 
    } 

    // Génère un mot de passe aléatoire de 8 caractères 
    function GenerPassword() 
    { 
    $string="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"; 
    $pass=""; 
    for($i=0;$i<8;$i++) 
    { 
    $pass.=$string[mt_rand()%strlen($string)]; 
    } 
    return $pass; 
    } 

    // Coupe un mot trop long en plusieurs sous-mots 
    function cutword($string,$length=30,$separation=" ") 
    { 
    return preg_replace('/([^ ]{'.$length.'})/si','\\1'.$separation,$string); 
    } 

    // transforme une date en chaine
    function date2string($s) {
      $s1 = str_replace(":","",$s);
    	$s2 = str_replace("-","",$s1);
    	$s3 = str_replace(" ","",$s2);
    	return $s3;
    }   
}

?>