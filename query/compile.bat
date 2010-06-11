call ../inc/path.bat
latex "\nonstopmode\input" %1.tex
dvips %1
copy %1.ps c:\Oyak\%1.ps
rem 
@md \Oyak\ToPrint\PR42
copy %1.ps c:\Oyak\ToPrint\PR42\%1.ps
del %1.*
rem gsprint all.ps
