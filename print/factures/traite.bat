@echo off
call ../../inc/path.bat
cd "%www%\print\factures"
php.exe traite.php --nohtml=1
