call ../inc/path.bat
cd "work"
copy ..\create_barcodes.py .
copy ..\bookland.py .
python create_barcodes.py
latex "\nonstopmode\input{barcodes.tex}"
dvips barcodes
@md \Oyak\ToPrint\PR432
copy barcodes.ps c:\Oyak\catalog.ps
cd ..


