@echo off
call ../../inc/path.bat
c:
cd "%www%\print\factures"
php.exe traite.php --nohtml=1
