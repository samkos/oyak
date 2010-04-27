PATH=c:\program Files\MiKTeX 2.5\miktex\bin;C:\WINDOWS\system32;c:\windows;c:\program Files\ghostgum\gsview
cd "work"
dvips barcodes
del *.eps  *.aux 	
copy barcodes.ps c:\Oyak\barcodes.ps																				
gsprint barcodes.ps
cd ..

