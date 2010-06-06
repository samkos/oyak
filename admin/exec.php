<?php
function my_exec($cmd)
{

   $cwd = getcwd();

    $outputfile= "c:/oyak/out";
    $batch = 'c:/oyak/exec.bat';
    $fp = fopen($batch, 'w');
    fwrite($fp, "@echo off\ncd $cwd \n");
    fwrite($fp, "$cmd \n");  
    fclose($fp);
    $WshShell = new COM("WScript.Shell");
    //$oExec = $WshShell->Run("cmd /C $batch > $outputfile 2>&1", 0, true);
    // fix provisoire easyphp 1.8
    system("$batch > $outputfile 2>&1",$status);

    // Read the file file.
    //print $outputfile;
    $data = file_get_contents($outputfile);
    $res = explode("\n",$data);
    //print_r($res);
    return $res;
}

?> 

