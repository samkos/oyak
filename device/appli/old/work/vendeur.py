# -*- coding: cp1252 -*-
from Tkinter import *
import string
import urllib

maxDigits=13

Produits={}
Clients={}
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

vendeur=1
sep1=";"
sep2="!"

###################################################################
#
#  Lectures des datas
#
###################################################################

def getProduits(urlName):
    origFileh = urllib.urlopen(urlName)
                     
    fileList = origFileh.readlines()

    nbArticles=0
    for l in fileList:
        articles=string.split(l,"=")
        for a in articles:
                nbArticles+=1
                article=string.split(a,"!")
                if len(article)==3:
                  (code,prix,libelle)=article
                Produits[code]=(libelle,prix)
                       
    origFileh.close()
    #print "%d Produits lus "%(nbArticles)

#-------------------------------------------------------------------



def getClients(urlName):
    origFileh = urllib.urlopen(urlName)
                     
    fileList = origFileh.readlines()

    nbArticles=0
    for l in fileList:
        articles=string.split(l,"=")
        for a in articles:
                nbArticles+=1
                article=string.split(a,"!")
                if len(article)==3:
                  (societe,ville,clef)=article
                Clients[societe+"^"+clef]=(societe,ville,clef)
                
    origFileh.close()
    # print "%d Clients lus "%(nbArticles)

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

###################################################################
#
#  Oyak widget
#
###################################################################



class OyakFrame:
    """ Frame intelligente,
        precablée pour recevoir des entrees, des boutons..."""
        
    def __init__(self, master):

        self.frame = Frame(master)
        self.frame.pack(side=TOP,expand=1,fill=BOTH)

        entryFrame = Frame(self.frame)
        entryFrame.pack(side=TOP,expand=1,fill=BOTH)

        self.entryFrameName = Frame(entryFrame)
        self.entryFrameName.pack(side=LEFT,fill=BOTH)

        self.entryFrameValue = Frame(entryFrame)
        self.entryFrameValue.pack(side=LEFT,fill=BOTH)

    def addEntry(self,_text,_value="",_justify="left"):


        label = Label(self.entryFrameName, text=_text, justify="left", fg="red")
        label.pack(side=TOP,expand=1,fill=BOTH)

        entry = Entry(self.entryFrameValue, justify=_justify, fg="black" )
        entry.pack(side=TOP,expand=1,fill=BOTH)
	entry.insert(0,_value)

	return entry

    def addLabelEntry(self,_text,_value="",_justify="left"):

        texte = StringVar()
        texte.set(_text)
        label = Label(self.entryFrameName, textvariable=texte, justify="left", fg="red")
        label.pack(side=TOP,expand=1,fill=BOTH)

        entry = Entry(self.entryFrameValue, justify=_justify, fg="black" )
        entry.pack(side=TOP,expand=1,fill=BOTH)
	entry.insert(0,_value)

	return (texte,entry)

    def addLabelLabel(self,_text,_value="",_justify="left"):

        texte = StringVar()
        texte.set(_value)
        label = Label(self.entryFrameName, text=_text, justify="left", fg="red")
        label.pack(side=TOP,expand=1,fill=BOTH)

        label = Label(self.entryFrameValue, textvariable=texte, justify=_justify, fg="black" )
        label.pack(side=TOP,expand=1,fill=BOTH)

	return (texte)


    def addListbox(self):

        listboxFrame = Frame(self.frame)
        listboxFrame.pack(side=TOP,expand=1,fill=BOTH)

        scrollbar = Scrollbar(listboxFrame)
        scrollbar.pack(side=RIGHT, fill=BOTH)

        listbox = Listbox(listboxFrame, yscrollcommand=scrollbar.set)
        listbox.pack(side=LEFT, expand=1, fill=BOTH)
        scrollbar.config(command=listbox.yview)

        return listbox

    def addButton(self,text="XXX"):
        button = Button(self.frame, text=text)
        button.pack(side=LEFT,expand=1,fill=BOTH)
        return button

    def addLabel(self,text="XXX"):
        label = Label(self.frame, textvariable=text)
        label.pack(side=top,expand=1,fill=BOTH)
        return label

    def nothing(self):
        return


###################################################################
#
#  Demarrage interface
#
###################################################################




##################################################################################

class choixClient:

    def __init__(self, master):
    
        self.clefs={}
        
        self.master=master

        frame = Frame(master)
        frame.pack()

    
        self.upFrame   = OyakFrame(frame)
        self.downFrame = OyakFrame(frame)

        
        self.fillDownFrame()
        self.fillUpFrame()
  
        self.action()


    def selectClient(self):
        self.rightFrame.frame.destroy()
        self.fillUpFrame()
        self.action()

################################################################################
# Saisie nom Facture
################################################################################

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
        self.article.focus_set()

    def goToPrice(self,event):
        self.prix.focus_set()

    def addFacture(self,event):
        prix=self.prix.get()
        if len(prix)==0:
                prix=self.prix_default
        quantite=self.quantite.get()
        if len(quantite)==0:
                quantite="1.0"
        article=self.article.get()
        self.listbox.insert(END, formatFact%(float(quantite),article,float(prix)))
        

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
        params = urllib.urlencode({'vendeur': vendeur, 'commande':s})
        f = urllib.urlopen(url_send_commande, params)

        self.selectClient()
        
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
            self.selectClient()
        if valeur=="x":
            self.selectClient()
            
    def saisieFacture(self,choix):
        self.rightFrame.frame.destroy()

        self.rightFrame = OyakFrame(self.upFrame.frame)
        (clef,societe,ville)=choix
        self.clef=clef
        
        self.total = self.rightFrame.addEntry(societe,"")

        self.quantite = self.rightFrame.addEntry("Quantite:    (1.00)","")
        (self.prix_label,self.prix) = self.rightFrame.addLabelEntry("Prix: ","")
        self.article = self.rightFrame.addEntry("Article: ","")

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
        
        self.nbDigit=0
        self.listbox.delete(0,END)
        self.listbox.insert(END, enteteFact)

        self.nbArticles=0


################################################################################
# Saisie nom client
################################################################################



    def go(self,event):
        clef=self.listbox.curselection()[0]
        choix=self.clefs[int(clef)]
        #print choix
        
        self.saisieFacture(choix)
 
    def addchar(self,event):
        self.filtre=self.filtre+event.char
        self.nom.set(string.upper(self.filtre))
        self.action()

    def delchar(self,event):
        self.filtre=self.filtre[:-1]
        self.nom.set(string.upper(self.filtre))
        self.action()

    def fillDownFrame(self):
        self.listbox=self.downFrame.addListbox()
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
        self.listbox.bind("<space>",self.addchar) 
        self.listbox.bind("<BackSpace>",self.delchar)
        self.listbox.bind("<Return>",self.go) 

  
    def fillUpFrame(self):
        self.rightFrame = OyakFrame(self.upFrame.frame)
        self.nom = self.rightFrame.addLabelLabel("Filtre >  ","")
        self.filtre = ""
        self.nom.set(self.filtre)
        self.listbox.focus_set()
        
    def action(self,event="fake"):
        self.listbox.delete(0,END)
        nom = self.nom.get()
        nom.lower()

        self.clefs={}
        i=0
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


class vendeur:

    def __init__(self):
        getClients(url_get_client)
        getProduits(url_get_produit)
        #check()

        root = Tk()
        # make it cover the entire screen
        #w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        #root.overrideredirect(1)
        #root.geometry("%dx%d+0+0" % (w, h))

        app = choixClient(root)

        root.mainloop()
    
if __name__ == "__main__":
   vendeur()

