PATH=c:\program Files\MiKTeX 2.5\miktex\bin;C:\WINDOWS\system32;c:\windows;c:\python24
cd "work"
copy ..\create_barcodes.py .
copy ..\bookland.py .
python create_barcodes.py
latex "\nonstopmode\input{barcodes.tex}"
dvips barcodes
@md \Oyak\ToPrint\__PR_ETIQ__
copy barcodes.ps c:\Oyak\barcodes.ps
copy barcodes.ps c:\Oyak\ToPrint\__PR_ETIQ__\barcodes.ps
cd ..


