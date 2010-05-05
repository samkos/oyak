PATH=c:\program Files\MiKTeX 2.6\miktex\bin;C:\WINDOWS\system32;c:\windows;c:\program Files\ghostgum\gsview
latex "\nonstopmode\input" all_landscape.tex
dvips all_landscape
copy all_landscape.ps c:\Oyak\general_landscape.ps
copy all_landscape.ps c:\Oyak\ToPrint\general_landscape.ps
rem gsprint all.ps
