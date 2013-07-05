@echo off
PATH=c:\program Files\MiKTeX 2.6\miktex\bin;C:\WINDOWS\system32;c:\windows;c:\program Files\ghostgum\gsview;c:\python24\;c:\Program Files\EasyPHP1-8\php\
set www=c:\Program Files\EasyPHP1-8\www\phpmyfactures\
cd "%www%\print\impression"
php.exe traite.php --nohtml=1 %*

