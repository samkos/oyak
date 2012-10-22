import string
import os

def txt2sql(fileName,tableName,what):
    origFileh = open(fileName,"r")
    sqlFileh = open(fileName+"_sql.sql","w")
                     
    fileList = origFileh.readlines()

    nbArticles=0
    sqlFileh.write("use oyak; \n")
    sqlFileh.write("TRUNCATE %s; \n"%tableName)
    for l in fileList:
        l=l.replace("'","\\'")
        articles=string.split(l,"=")
        for a in articles:
            nbArticles+=1
            champs=string.split(a,"!")
            if len(champs)>1:
                s='INSERT into %s (%s,timestamp) VALUES('%(tableName,what)
                nChamps=0
                for champ in champs:
                    if nChamps>0:
                        s=s+","
                    if len(champ)==0:
                        champ="xxx"
                    nChamps+=1
                    s = s + "\'"+ champ + "\'"
                s=s+",NULL)"
                s=s.replace("xxx","")
                sqlFileh.write(s+"; \n")

    origFileh.close()
    sqlFileh.close()

    print "%d articles trouves dans %s "%(nbArticles,fileName)

def sqlbatch(job,comment):
    mysql_cmd="\"c:\\Program Files\\easyPHP1-8\\mysql\\bin\\mysql\" -u root < %s"%job
    print mysql_cmd
    print os.system(mysql_cmd)
    print comment
    
def updateBase():
    sqlbatch("ITEM_sql.sql","articles mis a jour")
    sqlbatch("FOUR_sql.sql","fournisseurs mis a jour")
    sqlbatch("CLIENT_sql.sql","clients mis a jour")
    
    

txt2sql("ITEM","pcfact_produits","barcode,prix_vente_ht,prix_plancher_ht,titre,clef,fournisseur,poids")
txt2sql("CLIENT","pcfact_clients","societe,ville,clef")
txt2sql("FOUR","pcfact_fournisseurs","societe,ville,clef")

updateBase()
input("La base est mise a jour!!!")
      
