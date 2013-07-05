PATH=c:\program Files\MiKTeX 2.5\miktex\bin;C:\WINDOWS\system32;c:\windows;c:\program Files\ghostgum\gsview
cd "work"
dvips barcodes
copy barcodes.ps c:\Oyak\barcodes.ps
ps2pdf barcodes.ps barcodes.pdf
rem del *.eps  *.aux 	
copy barcodes.pdf c:\Oyak\barcodes.pdf
rem gsprint barcodes.ps
cd ..


