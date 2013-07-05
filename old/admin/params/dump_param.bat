@Echo off
@ECHO ! Sauvegarde des parametres

@PATH=c:\program Files\easyPHP1-8\mysql\bin;C:\WINDOWS\system32;c:\windows;
echo use oyak; > "params.sql"
echo delete from pcfact_produits where clef not between 0 and 9999;  >> "params.sql"
@mysqldump --skip-comments -c -n -t -u root "-wclef>=10000"  oyak pcfact_produits >> "params.sql"




