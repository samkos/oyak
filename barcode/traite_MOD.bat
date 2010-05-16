@echo off
PATH=__DRIVE__:\Program Files\EasyPHP1-8\php\;__DRIVE__:\Program Files\EasyPHP1-8\php\extensions\;__DRIVE__:\program Files\ghostgum\gsview;__DRIVE__:\Program Files\EasyPHP 2.0b1\php5\;__DRIVE__:\Program Files\EasyPHP 2.0b1\php5\ext\;__DRIVE__:\program Files\ghostgum\gsview;__DRIVE__:\program Files\__LATEX__\miktex\bin;
__DRIVE__:
cd "\Program Files\EasyPHP 2.0b1\www\phpmyfactures\barcode"
php.exe latex_barcode.php --nohtml=1

