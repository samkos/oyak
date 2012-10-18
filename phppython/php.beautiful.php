if (!function_exists("mysql_connect"))
{
    echo "Sistemdeki sorun nedeniyle sayfalar calismayabilir. Lütfen daha sonra tekrar deneyiniz.";
    mail("bvidinli@gmail.com","--ACÝLLL- mysql calismiyor serverda...");
    mail("bvidinli@yahoo.com","--ACÝLLL- mysql calismiyor serverda...");
    exit;
}
;


function alanlarial($tablo)
{
    // adodb de calýsýyor.
    global $db2;
    foreach ($db2->MetaColumnNames($tablo) as $alan)
    {
        $alanlar[]=$alan;
    }
    return $alanlar;
}




function isPasswordOk($username,$password,$usernamefield='',$passwordfield='')
{
    if (!$usernamefield)
    {
        $usernamefield=$this->conf['logintable']['usernamefield'];
    }
    if (!$passwordfield)
    {
        $passwordfield=$this->conf['logintable']['passwordfield'];
    }
    if (!$usernamefield)
    {
        $usernamefield='username';
    }
    if (!$passwordfield)
    {
        $passwordfield='password';
    }
    
    if ($this->conf['logintable']['passwordtype']=='md5')
    {
        $where="$usernamefield='$username' and md5('$password')=$passwordfield";
    }
    else
    {
        $where="$usernamefield='$username' and '$password'=$passwordfield";
    }
    
    $sayi=$this->recordcount($this->conf['logintable']['tablename'],$where);
    if ($sayi===false)
    {
        //echo "<hr>buraya geldiii..</hr>";
        $this->error_occured("dologin2");
        return false;
    }
    
    if ($sayi==0)
    {
        return false;
    }
    elseif ($sayi>0)
    {
        return true;
    }
}
