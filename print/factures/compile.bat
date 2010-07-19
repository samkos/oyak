@echo off
call ../../inc/path.bat
if exist all.pdf del all.pdf
if exist erreur.log del erreur.log
echo | time | find "actuelle" >> perf.out
latex  -interaction nonstopmode  all.tex
echo | time | find "actuelle" >> perf.out
if  exist all.pdf  goto ok
msg /time:5 * fichier all.pdf inexistant, une erreur est survenue a son visionnement
echo !
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo "!                                   <b> ERREUR DE CREATION DU FICHIER A IMPRIMER </b>"
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo "!!!!!!!!!!!!                <b> fichier all.pdf  inexistant, <b> une erreur est survenue </b>"
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo !
type erreur.log
goto fin
:ok
:FIN
