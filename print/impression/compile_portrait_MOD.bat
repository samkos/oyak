
PATH=c:\program Files\__LATEX__\miktex\bin;C:\WINDOWS\system32;c:\windows;c:\program Files\ghostgum\gsview
latex "\nonstopmode\input" all_portrait.tex
dvips all_portrait
copy all_portrait.ps c:\Oyak\general_portrait.ps
copy all_portrait.ps c:\Oyak\ToPrint\general_portrait.ps
rem gsprint all.ps
