import string
import os




def txt2sql(fileName,tableName,what,numclef):
    origFileh = open(fileName,"r")
    addFileh = open(fileName+"_add.sql","w")
    delFileh = open(fileName+"_del.sql","w")


    where="where (clef='%s')"
                     
    fileList = origFileh.readlines()

    nbArticles=0
    addFileh.write("use oyak; \n")
    delFileh.write("use oyak; \n")
    for l in fileList:
        l=l.replace("'","\\'")
        articles=string.split(l,"=")
        for a in articles:
            nbArticles+=1
            champs=string.split(a,"!")
            if len(champs)>1:
                d="DELETE FROM %s "%tableName+where%(champs[numclef])+";"
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
                addFileh.write(d+"; \n")
                addFileh.write(s+"; \n")


    origFileh.close()
    addFileh.close()
    delFileh.close()

    print "%d articles trouves dans %s "%(nbArticles,fileName)

def sqlbatch(job,comment):
    mysql_cmd="\"c:\\Program Files\\easyPHP1-8\\mysql\\bin\\mysql\" -u root < %s"%job
    print mysql_cmd
    print os.system(mysql_cmd)
    print comment
    
def updateBase():
    sqlbatch("ITEM_add.sql","articles mis a jour")
    sqlbatch("FOUR_add.sql","fournisseurs mis a jour")
    sqlbatch("CLIENT_add.sql","clients mis a jour")
    sqlbatch("ITEM_del.sql","articles effaces")
    sqlbatch("FOUR_del.sql","fournisseurs effaces")
    sqlbatch("CLIENT_del.sql","clients effaces")
    
    


#txt2sql("ITEM","pcfact_produits","barcode,prix_vente_ht,prix_plancher_ht,titre,clef,fournisseur,poids",4)
#txt2sql("CLIENT","pcfact_clients","societe,ville,clef",2)
txt2sql("FOUR","pcfact_fournisseurs","societe,ville,clef",2)

updateBase()
input("La base est mise a jour!!!")
      
