PATH=c:\program Files\easyPHP1-8\mysql\bin;C:\WINDOWS\system32;c:\windows;
mysql -u root < clean_tables.sql
mysql -u root < work\CLIENT_sql.sql
mysql -u root < work\PRODUIT_sql.sql

