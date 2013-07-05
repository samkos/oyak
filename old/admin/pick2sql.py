import string

def txt2sql(fileName,tableName,what):
    origFileh = open(fileName+".txt","r")
    sqlFileh = open(fileName+"_sql.sql","w")
                     
    fileList = origFileh.readlines()

    sqlFileh.write("use oyak; \n")
		
    nbArticles=0
    for l in fileList:
        articles=string.split(l,"=")
        for a in articles:
            nbArticles+=1
            champs=string.split(a,"!")
            s='INSERT into %s (%s) VALUES('%(tableName,what)
            nChamps=0
            for champ in champs:
                if nChamps>0:
                    s=s+","
                if len(champ)==0:
                    champ="xxx"
                nChamps+=1
                s = s + "\""+ champ + "\""
            s=s+")"
            sqlFileh.write(s+"; \n")

    origFileh.close()
    sqlFileh.close()

    print "%d articles trouves dans %s "%(nbArticles,fileName)

txt2sql("PRODUIT","pcfact_produits","barcode,prix_vente_ht,titre")
txt2sql("CLIENT","pcfact_clients","societe,ville,clef")

0

