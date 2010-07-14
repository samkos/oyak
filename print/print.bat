PATH=c:\program Files\MiKTeX 2.6\miktex\bin;C:\WINDOWS\system32;c:\windows;c:\program Files\ghostgum\gsview;c:\python24\;c:\Program Files\EasyPHP1-8\php\
set www=c:\Program Files\EasyPHP1-8\www\phpmyfactures\
if  exist %*  goto ok
msg /time:5 * fichier %* inexistant, une erreur est survenue a son impression
echo !
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo !                                    ERREUR D'IMPRESSION 
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo !!!!!!!!!!!!   fichier %* inexistant, une erreur est survenue 
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo !
goto fin
:ok
gsprint %1
echo "impression en cours" %1
del %1
							

