\rm -rf ./ex2
#zcat $1.gz | sqlite3 ex2
cat $1 | sqlite3 ex2

cp ../db.sqlite db.sqlite.old
echo nouvelle base generee,  ancienne sauvegardee , reste a faire
echo mv ex2 ../db.sqlite
