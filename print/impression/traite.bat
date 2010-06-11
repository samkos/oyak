@echo off
call ../../inc/path.bat
c:
cd "%www%\print\impression"
php.exe traite.php --nohtml=1

