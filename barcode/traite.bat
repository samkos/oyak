@echo off
PATH=c:\Program Files\EasyPHP1-8\php\;c:\Program Files\EasyPHP1-8\php\extensions\;c:\program Files\ghostgum\gsview;
cd   "c:\Program Files\EasyPHP1-8\www\phpmyfactures\barcode"
php.exe latex_barcode.php >> out_php
rem copy c:\Oyak\facture.ps c:\Oyak\ToPrint\facture.ps
echo "impression etiquette en cours"
