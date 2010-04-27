rem PATH=e:\Program Files\EasyPHP 2.0b1\php5\;e:\Program Files\EasyPHP 2.0b1\php5\ext\;e:\program Files\ghostgum\gsview;
PATH=e:\program Files\MiKTeX 2.6\miktex\bin;e:\Program Files\EasyPHP1-8\php\;e:\Program Files\EasyPHP1-8\php\extensions\;e:\program Files\ghostgum\gsview;C:\WINDOWS\system32;c:\windows
copy fact120 c:\facprint
cd ../../../factures/
php.exe traite.php > out_traite.txt
rem copy c:\Oyak\facture.ps c:\Oyak\ToPrint\facture.ps
echo "impression en cours"
cd ../print/tests/persepolis