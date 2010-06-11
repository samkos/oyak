@echo off
PATH=c:\Program Files\EasyPHP1-8\php\;c:\Program Files\EasyPHP1-8\php\extensions\;c:\program Files\ghostgum\gsview;c:\program Files\MiKTeX 2.6\miktex\bin;
c:
cd "\Program Files\EasyPHP1-8\www\phpmyfactures\barcode"
"c:\Program Files\EasyPHP1-8\php\php.exe"  latex_barcode.php --nohtml=1

