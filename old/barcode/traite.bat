@echo off
call ../inc/path.bat
c:
cd "%www%\barcode"
php.exe  latex_barcode.php --nohtml=1

