@echo off
call ../../inc/path.bat
if exist all_portrait.pdf del all_portrait.pdf
if exist erreur.log del erreur.log
pdflatex  -interaction nonstopmode  all_portrait.tex > erreur.log
if  exist all_portrait.pdf  goto ok
msg /time:5 * fichier all_portrait.pdf inexistant, une erreur est survenue a son visionnement
echo !
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo "!                                   <b> ERREUR DE CREATION DU FICHIER A IMPRIMER </b>"
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo "!!!!!!!!!!!!                <b> fichier all_portrait.pdf  inexistant, <b> une erreur est survenue </b>"
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo !
type erreur.log
goto fin
:ok
:FIN