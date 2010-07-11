call ../../inc/path.bat
del all.pdf
pdflatex "\nonstopmode\input" all.tex
rem copy all.pdf c:\Oyak\facture.pdf
