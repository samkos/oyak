call ../../inc/path.bat
del all_landscape.pdf
pdflatex all_landscape.tex
copy all_landscape.pdf c:\Oyak\general_landscape.pdf
copy all_landscape.pdf c:\Oyak\ToPrint\general_landscape.pdf
