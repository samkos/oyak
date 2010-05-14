<?php

// through a Wscript
function _exec($cmd)
{
   $WshShell = new COM("WScript.Shell");
   $cwd = getcwd();
   if (strpos($cwd,' '))
   {  if ($pos = strpos($cmd, ' '))
      {  $cmd = substr($cmd, 0, $pos) . '" ' . substr($cmd, $pos);
      }
      else
      {  $cmd .= '"';
      }
      $cwd = '"' . $cwd;
   }  
   $oExec = $WshShell->Run("cmd /C \" $cwd\\$cmd\"", 0,true);
  
   return $oExec == 0 ? true : false;
}

function my_exec($cmd)
{

   $cwd = getcwd();

    $outputfile= "c:/oyak/out";
    $batch = 'c:/oyak/exec.bat';
    $fp = fopen($batch, 'w');
    fwrite($fp, "@echo off\n e:\ncd $cwd \n");
    fwrite($fp, "$cmd \n");  
    fclose($fp);
    $WshShell = new COM("WScript.Shell");
    $oExec = $WshShell->Run("cmd /C $batch > $outputfile 2>&1", 0, true);

    // Read the file file.
    $res = file($outputfile);

    return $res;
}


if (0) {
// Setup the command to run from "run"
$cmdline = "cmd /C $commande " . " > $outputfile 2>&1";
print $cmdline;
// Make a new instance of the COM object
$WshShell = new COM("WScript.Shell");  
// Make the command window but don't show it.
$oExec = $WshShell->Run($cmdline, 0, true);
// Read the file file.
$res = file($outputfile);
}



// pstools.inc.php

function PsExecute($command, $timeout = 60, $sleep = 2) {
    // First, execute the process, get the process ID
    $pid = PsExec($command);
   
    if( $pid === false )
        return false;
   
    $cur = 0;
    // Second, loop for $timeout seconds checking if process is running
    while( $cur < $timeout ) {
        sleep($sleep);
        $cur += $sleep;
        // If process is no longer running, return true;
        if( !PsExists($pid) )
            return true; // Process must have exited, success!
    }
   
    // If process is still running after timeout, kill the process and return false
    PsKill($pid);
    return false;
}

function PsExec($command) {
    
    exec( "pstools\\psexec.exe -s -d $command  2>&1", $output);

    while( list(,$row) = each($output) ) {
        $found = stripos($row, 'with process ID ');
        if( $found )
            return substr($row, $found, strlen($row)-$found-strlen('with process ID ')-1); // chop off last character '.' from line
    }
   
    return false;
}

function PsExists($pid) {
    exec( dirname(__FILE__). "\\pslist.exe $pid 2>&1", $output);

    while( list(,$row) = each($output) ) {
        $found = stristr($row, "process $pid was not found");
        if( $found !== false )
            return false;
    }
   
    return true;
}

function PsKill($pid) {
    exec( dirname(__FILE__). "\\pskill.exe $pid", $output);
}

?> 

