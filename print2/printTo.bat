rem @echo off
PATH=c:\program Files\MiKTeX 2.6\miktex\bin;C:\WINDOWS\system32;c:\windows;c:\program Files\ghostgum\gsview;c:\python24\;c:\Program Files\EasyPHP1-8\php\
set www=c:\Program Files\EasyPHP1-8\www\phpmyfactures\
if  exist %1  goto ok
msg /time:5 * fichier %1 inexistant, une erreur est survenue a son impression sur %2
echo !
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo !                                    ERREUR D'IMPRESSION 
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo !!!!!!!!!!!!   fichier %1 inexistant, une erreur est survenue a son impression vers %2
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo !
goto fin
:ok
gsprint  -printer %2 %1
echo "impression en cours" %1
del %1
							


