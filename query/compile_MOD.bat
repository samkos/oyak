
PATH=c:\program Files\__LATEX__\miktex\bin;C:\WINDOWS\system32;c:\windows;c:\program Files\ghostgum\gsview
latex "\nonstopmode\input" %1.tex
dvips %1
copy %1.ps c:\Oyak\%1.ps
rem 
@md \Oyak\ToPrint\__PR_BL__
copy %1.ps c:\Oyak\ToPrint\__PR_BL__\%1.ps
del %1.*
rem gsprint all.ps
