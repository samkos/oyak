@echo off
if  exist %*  goto ok
msg /time:5 * fichier %* inexistant, une erreur est survenue a son visionnement
echo !
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo "!                                   <b> ERREUR D'IMPRESSION A L'ECRAN </b>"
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo "!!!!!!!!!!!!                <b> fichier %* inexistant, <b> une erreur est survenue </b>"
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo !
goto fin
:ok
wscript.exe invis.vbs view2.bat %*
:fin 
