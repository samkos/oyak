# -*- coding: cp1252 -*-
from Tkinter import *
import string
import urllib

maxDigits=13

Produits={}
Clients={}
Vendeurs={}

formatFact="%5.2f|%15s|%5.2f"
enteteFact="%5s|%15s|%5s"%("quant","produit","prix")
selectedProduit={}
selectedPrix={}
selectedQuantite={}

website_address="http://127.0.0.1/phpmyfactures"
url_send_commande=website_address+"/query/index.php?"
url_retrieve_client=website_address+"/admin/work/CLIENT.txt"
url_retrieve_produit=website_address+"/admin/work/PRODUIT.txt"
url_get_client=website_address+"/query/get_data.php?clients=1"
url_get_produit=website_address+"/query/get_data.php?produits=1"
url_get_vendeur=website_address+"/query/get_data.php?vendeurs=1"

sep1=";"
sep2="!"

###################################################################
#
#  Lectures des datas
#
###################################################################

def messageBox(s):
    t=Toplevel()
    l=Label(t,text=s)
    l.pack()
    

class vendeur:

    def __init__(self):
        try :
            self.getClients(url_get_client)
        except:
            print "erreur recuperation liste Client"
        try :
            self.getProduits(url_get_produit)
        except:
            print "erreur recuperation liste Client"
        try :
            self.getVendeurs(url_get_vendeur)
        except:
            print "erreur recuperation liste Vendeurs"
        #check()

        self.run()

    def run(self):
        root = Tk()
        # make it cover the entire screen
        #w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        #root.overrideredirect(1)
        #root.geometry("%dx%d+0+0" % (w, h))


        app = choixClient(root)

        root.mainloop()
    
    def getProduits(self,urlName):
        origFileh = urllib.urlopen(urlName)
                         
        fileList = origFileh.readlines()

        nbArticles=0
        for l in fileList:
            articles=string.split(l,"=")
            for a in articles:
                    article=string.split(a,"!")
                    if len(article)==3:
                      nbArticles+=1
                      (code,prix,libelle)=article
                      Produits[code]=(libelle,prix)
                           
        origFileh.close()
        #print "%d Produits lus "%(nbArticles)

    #-------------------------------------------------------------------



    def getClients(self,urlName):
        origFileh = urllib.urlopen(urlName)
                         
        fileList = origFileh.readlines()

        nbArticles=0
        for l in fileList:
            articles=string.split(l,"=")
            for a in articles:
                    article=string.split(a,"!")
                    if len(article)==3:
                      nbArticles+=1
                      (societe,ville,clef)=article
                      Clients[societe+"^"+clef]=(societe,ville,clef)
                    
        origFileh.close()
        # print "%d Clients lus "%(nbArticles)

    #-------------------------------------------------------------------



    def getVendeurs(self,urlName):
        origFileh = urllib.urlopen(urlName)
                         
        fileList = origFileh.readlines()

        nbArticles=0
        for l in fileList:
            articles=string.split(l,"=")
            for a in articles:
                    article=string.split(a,"!")
                    if len(article)==3:
                      nbArticles+=1
                      (numero,nom,prenom)=article
                      Vendeurs[numero]=(numero,nom,prenom)
                      #print (numero,nom,prenom)    
        origFileh.close()
        # print "%d vendeurs lus "%(nbArticles)

    #-------------------------------------------------------------------

    def check():
        # verification Produits
        print
        print "Produits :"
        print "------------------------------------"
        for code in Produits.keys():
            (libelle,prix) = Produits[code]
            print (code,prix,libelle)

        # verification Clients
        print
        print "Clients :"
        print "------------------------------------"
        for client in Clients.keys():
            (societe,ville,clef) = Clients[client]
            print (societe,ville)

#-------------------------------------------------------------------

################################################################################
# Saisie nom client
##################################################################################

class choixClient:

    def __init__(self, root):
    
        self.clefs={}
        self.root=root

        self.what="vendeur"
        self.ihmClient()


        
        self.action()


        
    def go(self,event):
        if self.filtre=="*":
            self.root.destroy()
            self.root.quit()
            return

        clef=self.listbox.curselection()[0]
        choix=self.clefs[int(clef)]

        self.filtre=""
        self.nom.set(string.upper(self.filtre))

        if self.what=="vendeur":
            self.vendeur=choix
            self.what="client"
            self.action()
            (numero,nom,prenom)=self.vendeur
            texte="%s >"%prenom
            self.labelFiltre.set(texte)
        else:
            self.action()
            processFacture(self.root,self.vendeur,choix)
      
    def addchar(self,event):
        self.filtre=self.filtre+event.char
        self.nom.set(string.upper(self.filtre))
        self.action()

    def delchar(self,event):
        self.filtre=self.filtre[:-1]
        self.nom.set(string.upper(self.filtre))
        self.action()

        
    def ihmClient(self):

        # division de la fenetre en deux
        
        self.filtreFrame = Frame(self.root)
        self.filtreFrame.pack(side=TOP,expand=1,fill=BOTH)

        
        self.listFrame = Frame(self.root)
        self.listFrame.pack(side=TOP,expand=1,fill=BOTH)

        # filtre
        self.labelFiltre=StringVar("")
        self.labelFiltre.set("filtre >")
        label = Label(self.filtreFrame, textvariable=self.labelFiltre, justify="left", fg="red")
        label.pack(side=LEFT,fill=BOTH)

        self.nom = StringVar("")
        label = Label(self.filtreFrame, textvariable=self.nom, justify="left", fg="black" )
        label.pack(side=LEFT,fill=BOTH)

        self.filtre=""

        # liste box

        scrollbar = Scrollbar(self.listFrame)
        scrollbar.pack(side=RIGHT, fill=BOTH)

        self.listbox = Listbox(self.listFrame, yscrollcommand=scrollbar.set)
        self.listbox.pack(side=LEFT, expand=1, fill=BOTH)
        scrollbar.config(command=self.listbox.yview)

        self.listbox.bind("a",self.addchar) 
        self.listbox.bind("b",self.addchar) 
        self.listbox.bind("c",self.addchar) 
        self.listbox.bind("d",self.addchar) 
        self.listbox.bind("e",self.addchar) 
        self.listbox.bind("f",self.addchar) 
        self.listbox.bind("g",self.addchar) 
        self.listbox.bind("h",self.addchar) 
        self.listbox.bind("i",self.addchar) 
        self.listbox.bind("j",self.addchar) 
        self.listbox.bind("k",self.addchar) 
        self.listbox.bind("l",self.addchar) 
        self.listbox.bind("m",self.addchar) 
        self.listbox.bind("n",self.addchar) 
        self.listbox.bind("o",self.addchar) 
        self.listbox.bind("p",self.addchar) 
        self.listbox.bind("q",self.addchar) 
        self.listbox.bind("r",self.addchar) 
        self.listbox.bind("s",self.addchar) 
        self.listbox.bind("t",self.addchar) 
        self.listbox.bind("u",self.addchar) 
        self.listbox.bind("v",self.addchar) 
        self.listbox.bind("w",self.addchar) 
        self.listbox.bind("x",self.addchar) 
        self.listbox.bind("y",self.addchar) 
        self.listbox.bind("z",self.addchar) 
        self.listbox.bind("'",self.addchar) 
        self.listbox.bind("-",self.addchar) 
        self.listbox.bind(".",self.addchar) 
        self.listbox.bind("*",self.addchar) 
        self.listbox.bind("<space>",self.addchar) 
        self.listbox.bind("<BackSpace>",self.delchar)
        self.listbox.bind("<Return>",self.go) 

        self.listbox.focus_set()

    def action(self,event="fake"):
        self.listbox.delete(0,END)
        nom = self.nom.get()
        nom.lower()

        self.clefs={}
        i=0
        if self.what=="vendeur":
            liste=Vendeurs.keys()
            liste.sort(key=str.lower)
            for clef in liste:
                (numero,nom,prenom) = Vendeurs[clef]
                nom.lower()
                if string.lower(nom[:len(self.filtre)])==self.filtre:
                    self.listbox.insert(END, "%s %s"%(nom,prenom))
                    self.clefs[i]=(numero,nom,prenom)
                    i=i+1
        else:
            liste=Clients.keys()
            liste.sort(key=str.lower)
            for clef in liste:
                (societe,ville,clef) = Clients[clef]
                societe.lower()
                if string.lower(societe[:len(self.filtre)])==self.filtre:
                    self.listbox.insert(END, "%s/%s"%(societe,ville))
                    self.clefs[i]=(clef,societe,ville)
                    i=i+1
                
        self.listbox.focus_set()
        self.listbox.selection_set(0)



################################################################################
# Saisie nom Facture
################################################################################

class processFacture:

    def __init__(self, root,vendeur,client):
    
        self.clefs={}
        
        self.root=Toplevel()
        self.client=client
        (numero,nom,prenom)=vendeur
        self.vendeur_prenom=prenom
        self.vendeur_numero=numero
        
        self.ihmFacture()
  

    def __del__(self):
        self.root.destroy()
        
    def ihmFacture(self):
        
        # division de la fenetre en trois
        
        self.clientFrame = Frame(self.root)
        self.clientFrame.pack(side=TOP,expand=1,fill=BOTH)
        
        self.prixFrame = Frame(self.root)
        self.prixFrame.pack(side=TOP,expand=1,fill=BOTH)

        self.nameFrame = Frame(self.prixFrame)
        self.nameFrame.pack(side=LEFT,expand=1,fill=BOTH)

        self.inputFrame = Frame(self.prixFrame)
        self.inputFrame.pack(side=LEFT,expand=1,fill=BOTH)

        
        self.listFrame = Frame(self.root)
        self.listFrame.pack(side=TOP,expand=1,fill=BOTH)


        (clef,societe,ville)=self.client
        self.clef=clef

        # rappel nom client
        label = Label(self.clientFrame, text="%s>%s"%(self.vendeur_prenom,societe), justify="center", fg="red")
        label.pack(side=TOP,expand=1,fill=BOTH)

        # quantite, prix, article

        label = Label(self.nameFrame, text="Quantite: (1.00)", justify="left", fg="red")
        label.pack(side=TOP,expand=1,fill=BOTH)

        self.quantite = Entry(self.inputFrame, fg="black" )
        self.quantite.pack(side=TOP,expand=1,fill=BOTH)
        
        self.prix_label= StringVar()
        self.prix_label.set("Prix :")

        label = Label(self.nameFrame, textvariable=self.prix_label, fg="red" )
        label.pack(side=TOP,expand=1,fill=BOTH)

        self.prix = Entry(self.inputFrame, fg="black" )
        self.prix.pack(side=TOP,expand=1,fill=BOTH)

        label = Label(self.nameFrame, text="Article : ", justify="left", fg="red")
        label.pack(side=TOP,expand=1,fill=BOTH)

        self.article = Entry(self.inputFrame, fg="black" )
        self.article.pack(side=TOP,expand=1,fill=BOTH)

        # liste box

        scrollbar = Scrollbar(self.listFrame)
        scrollbar.pack(side=RIGHT, fill=BOTH)

        self.listbox = Listbox(self.listFrame, yscrollcommand=scrollbar.set)
        self.listbox.pack(side=LEFT, expand=1, fill=BOTH)
        scrollbar.config(command=self.listbox.yview)

        # Bindings...

        self.article.focus_set()
        self.article.bind("0",self.processCode)
        self.article.bind("1",self.processCode)
        self.article.bind("2",self.processCode)
        self.article.bind("3",self.processCode)
        self.article.bind("4",self.processCode)
        self.article.bind("5",self.processCode)
        self.article.bind("6",self.processCode)
        self.article.bind("7",self.processCode)
        self.article.bind("8",self.processCode)
        self.article.bind("9",self.processCode)
        self.article.bind("<BackSpace>",self.deleteCode)
        self.article.bind("<FocusOut>",self.cleanCode)
        
        self.article.bind("<Return>",self.route)
        self.quantite.bind("<Return>",self.goToPrice)
        self.prix.bind("<Return>",self.addFacture)

        #self.quantite.bind("*",self.goToPrice)
        #self.prix.bind("*",self.goToQuantite)
        
        self.nbDigit=0
        self.listbox.delete(0,END)
        self.listbox.insert(END, enteteFact)

        self.nbArticles=0

    def processCode(self,event):
        valeur=self.article.get()
        if len(valeur)==maxDigits-1:
                self.produit=valeur+event.char
                code=valeur+event.char
                if code in Produits.keys():
                    (libelle,prix)=Produits[code]
                    self.quantite.focus_set()
                    self.article.delete(0,END)
                    self.article.insert(END,libelle)
                    self.prix.delete(0,END)
                    self.prix_label.set("Prix : ("+"%6.2f"%(eval(prix)+0.00)+")")
                    self.prix_default=prix

                else:
                    self.deleteCode("")
                

    def cleanCode(self,event):
        l=len(self.article.get())
        self.article.delete(l-1,l)

    def deleteCode(self,event):
        self.article.delete(0,END)
        self.prix.delete(0,END)
        self.quantite.delete(0,END)
        self.article.focus_set()

    def goToPrice(self,event):
        self.prix.focus_set()

    def goToQuantite(self,event):
        self.quantite.focus_set()

    def addFacture(self,event):
        prix=self.prix.get()
        if len(prix)==0:
                prix=self.prix_default
        quantite=self.quantite.get()
        if len(quantite)==0:
                quantite="1.0"
        article=self.article.get()
        try :
          self.listbox.insert(END, formatFact%(float(quantite),article,float(prix)))
        except :
            self.deleteCode("fake")
        

        selectedProduit[self.nbArticles]=self.produit
        selectedPrix[self.nbArticles]=prix
        selectedQuantite[self.nbArticles]=quantite
        self.nbArticles=self.nbArticles+1
        
        self.deleteCode("fake")

    def factureOut(self):
        s="%s%s"%(self.clef,sep1)
        for l in range(0,self.nbArticles):
             s=s+"%s%s%s%s%s%s"%(selectedProduit[l],sep2,selectedQuantite[l],sep2,selectedPrix[l],sep1)
        #print s
        params = urllib.urlencode({'vendeur': self.vendeur_numero, 'commande':s})
        f = urllib.urlopen(url_send_commande, params)
        self.__del__()
    
    def route(self,event):
        valeur=self.article.get()
        if valeur=="-":
            l=self.listbox.size()
            if l>1:
                self.listbox.delete(l-1,l)
                self.nbArticles=self.nbArticles-1
            self.deleteCode("fake")
        if valeur=="*":
            self.factureOut()
            self.__del__()
        if valeur=="." or valeur=="x":
            self.__del__()
            

if __name__ == "__main__":
   vendeur()

