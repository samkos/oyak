call ../../inc/path.bat
latex "\nonstopmode\input" all.tex
dvips all
copy all.ps c:\Oyak\facture.ps
rem copy all.ps c:\Oyak\ToPrint\facture.ps
rem gsprint all.ps
