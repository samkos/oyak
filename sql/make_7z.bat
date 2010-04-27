@Echo off



cd c:\Oyak\

@ECHO ! Sauvegarde de la base

@PATH=c:\program Files\easyPHP1-8\mysql\bin;C:\WINDOWS\system32;c:\windows;
@mysqldump -u root --add-drop-table -c -f oyak > "c:\Program Files\EasyPHP1-8\www\SAVE\current_tables.sql"

@ECHO ! Creation de l'archive

"c:\Program Files\7-Zip\7z.exe"  a  c:\Oyak\save_site "c:\Program Files\EasyPHP1-8\www\SAVE"  > c:\Oyak\save_site.out



