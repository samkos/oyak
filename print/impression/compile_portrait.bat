call ../../inc/path.bat
latex "\nonstopmode\input" all_portrait.tex
dvips all_portrait
copy all_portrait.ps c:\Oyak\general_portrait.ps
copy all_portrait.ps c:\Oyak\ToPrint\general_portrait.ps
rem gsprint all.ps
