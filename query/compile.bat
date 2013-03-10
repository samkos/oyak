
PATH=c:\program Files\MiKTeX 2.6\miktex\bin;C:\WINDOWS\system32;c:\windows;c:\program Files\ghostgum\gsview
latex "\nonstopmode\input" %1.tex
dvips %1
copy %1.ps c:\Oyak\%1.ps
rem 
@md \Oyak\ToPrint\PR42
copy %1.ps c:\Oyak\ToPrint\PR42\%1.ps
del %1.*
rem gsprint all.ps
