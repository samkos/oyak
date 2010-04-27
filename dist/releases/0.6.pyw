# -*- coding: cp1252 -*-
from Tkinter import *
import string
import urllib

maxDigits=13
cible=001
oneFrame=0
version="0.6"

if cible:
    zoomedWindow=1
    erreurCatch=1
    debugMessages=0
    raiseError=0
else:
    erreurCatch=0
    debugMessages=1
    zoomedWindow=0
    raiseError=1

Produits={}
ProduitsFournisseurs={}
ProduitsRacourcis={}
ProduitsCodes={}
Clients={}
Vendeurs={}
Fournisseurs={}
Releases={}

clefsClients=list()

formatFact="%5.2f|%15s|%5.2f"
enteteFact="%5s|%15s|%5s"%("quant","produit","prix")

selectedCode={}
selectedRacourci={}
selectedFournisseur={}
selectedDate={}
selectedPrix={}
selectedQuantite={}


website_address="http://127.0.0.1/phpmyfactures"
website_address="http://192.168.111.77/phpmyfactures"
url_retrieve_client=website_address+"/admin/work/CLIENT.txt"
url_retrieve_produit=website_address+"/admin/work/PRODUIT.txt"
url_get_client=website_address+"/query/get_data.php?clients=1"
url_get_produit=website_address+"/query/get_data.php?produits=1"
url_get_vendeur=website_address+"/query/get_data.php?vendeurs=1"
url_get_fournisseur=website_address+"/query/get_data.php?fournisseurs=1"
url_get_release=website_address+"/query/get_data.php?releases=1"

fichierClientsBackup='\Oyak\Cli000.bak'
fichierVendeursBackup='\Oyak\Ven000.bak'
fichierFournisseursBackup='\Oyak\Fou000.bak'
fichierProduitsBackup='\Oyak\Pro000.bak'
fichierReleasesBackup='\Oyak\Rel000.bak'

url_send_commande=website_address+"/query/index.php?"
url_update_commande=website_address+"/query/download.php?"

sep1=";"
sep2="!"


vendeur=(0,"xxx",'xx')


clientNB = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}

###################################################################
#
#  fonction IHM annexe
#
###################################################################

class messageBox:
    
    def __init__(self,s):
        global zoomedWindow
        
        self.t=Toplevel()
        l=Button(self.t,text=s,command=self.efface)
        l.pack(expand=1,fill=BOTH)
        l.focus_set()
        if zoomedWindow:
            self.t.wm_state(newstate="zoomed")

    def efface(self):
        try:
            self.t.destroy()
        except:
            pass
        
def getNBclient() :
    global clientNB
    i=1
    while clientNB[i]>0  and i<8:
        i=i+1
    clientNB[i]=1
    return i

def releaseNBclient(i):
    global clientNB
    clientNB[i]=0

def bindElementKeysFunction(element, keys, func):
    for c in keys:
        element.bind(c,func)


class ihmRoot:

    def __init__(self):
       self.ihm=Tk()

       self.ihmPanels={}
       self.ihmPanelsContents={}
       self.Xmax=200
       self.Ymax=40
       self.Xmid=100

       self.ihm.rowconfigure(0,weight=1)
       self.ihm.columnconfigure(0,weight=1)
       #self.ihm.master.grid(sticky=W+E+N+S)
       
       self.messagePanelCreate()
       self.choosePanelCreate()
       
    def title(self,s):
       self.ihm.title(s)

    def add(self,panelName,widgetName,widget,row,column,rowspan=1,colspan=1,sticky=N+E+W+S):
        if panelName in self.ihmPanels.keys():
           self.ihmPanels[panelName].append(widgetName)
        else:
           self.ihmPanels[panelName]=[widgetName]
        self.ihmPanelsContents[panelName,widgetName]=(widget,row,column,rowspan,colspan,sticky)
      
    def hide(self,panelName):
        for widgetName in self.ihmPanels[panelName]:
            (widget,row,column,rowspan,colspan,sticky)=self.ihmPanelsContents[panelName,widgetName]
            widget.grid_forget()
            
    def show(self,panelName):
        self.hideAll()
        for widgetName in self.ihmPanels[panelName]:
            (widget,row,column,rowspan,colspan,sticky)=self.ihmPanelsContents[panelName,widgetName]
            widget.grid(row=row,column=column,rowspan=rowspan,columnspan=colspan,sticky=sticky)
            
    def hideAll(self):
        for panel in self.ihmPanels.keys():
            self.hide(panel)

    def messagePanelCreate(self):
        self.message=StringVar("")
        self.message.set("Bienvenue! \n Tapez sur l'ecran")
        l=Button(self.ihm,textvariable=self.message,command=self.chooseVendeur)
        self.add("message","texte",l,0,0,self.Ymax,self.Xmax)
        l.focus_set()

    def choosePanelCreate(self):
        # filtre
        self.filtreLabel=StringVar("")
        self.filtreLabel.set("filtre >")
        label = Label(self.ihm, textvariable=self.filtreLabel, justify="left", fg="red")
        self.add("choose","filtreLabel",label,0,0,1,self.Xmid,sticky="")

        self.filtreName=StringVar("")
        self.filtreName.set("essai")
        label = Label(self.ihm, textvariable=self.filtreName, justify="left", fg="black")
        self.add("choose","filtreName",label,0,self.Xmid,1,self.Xmax-self.Xmid,sticky="")
        
        # liste box

        scrollbar = Scrollbar(self.ihm)
        self.add("choose","scrollbar",scrollbar,1,self.Xmax-1,self.Ymax-1,1,sticky=N+S)
        
        self.listbox = Listbox(self.ihm, yscrollcommand=scrollbar.set)
        self.add("choose","listbox",self.listbox,1,0,self.Ymax-1,self.Xmax-1)
        scrollbar.config(command=self.listbox.yview)



    def chooseVendeur(self):
        self.show("choose")
        
    def start(self):
        global zoomedWindow
        if zoomedWindow:
            self.ihm.wm_state(newstate="zoomed")
        self.show("message")
        self.ihm.mainloop()
     
    
###################################################################
#
#  Gestion de la mise a jour
#
###################################################################

def loadRelease(filename):
        print filename
        params = urllib.urlencode({'dwn': filename})
        try:
            f = urllib.urlopen(url_update_commande, params)
        except:
            messageBox("Le serveur Release ne répond pas!")
            return
        new=open("\\Oyak\\vendnew.py","w")
        program=f.readlines()
        for l in program :
            new.write(l)
        new.close()

    
###################################################################
#
#  Lectures des datas
#
###################################################################


class lisData:

    def __init__(self,readFromServer=0):

        self.readFromServer=readFromServer
        if erreurCatch :
           try :
               getClients(url_get_client,fichierClientsBackup,self.readFromServer)
           except:
               print "erreur recuperation liste Client"
           try :
               getFournisseurs(url_get_fournisseur,fichierFournisseursBackup,self.readFromServer)
           except:
               print "erreur recuperation liste Fournisseur"
           try :
               getProduits(url_get_produit,fichierProduitsBackup,self.readFromServer)
           except:
               print "erreur recuperation liste Produit"
           try :
               getVendeurs(url_get_vendeur,fichierVendeursBackup,self.readFromServer)
           except:
               print "erreur recuperation liste Vendeurs"
           try :
               getReleases(url_get_release,fichierReleasesBackup,readFromServer=1)
           except:
               print "erreur recuperation liste Releases"
        else:
          getProduits(url_get_produit,fichierProduitsBackup,self.readFromServer)
          getClients(url_get_client,fichierClientsBackup,self.readFromServer)
          getFournisseurs(url_get_fournisseur,fichierFournisseursBackup,self.readFromServer)
          getVendeurs(url_get_vendeur,fichierVendeursBackup,self.readFromServer)
          getReleases(url_get_release,fichierReleasesBackup,readFromServer=1)
        #check()

    

class getData:

    def __init__(self,urlName,fichierBackup,what,lengthArticle,readFromServer):
        self.create_backup=0
        self.what=what
        self.readFromServer=readFromServer
        self.urlName=urlName
        self.fichierBackup=fichierBackup
        self.dataAvailable=self.openSource()
        if self.dataAvailable==0:
           self.readSource(lengthArticle)
           self.closeSource()
           self.postProcess()

    def readFromUrl(self):
        try:
           self.origFileh = urllib.urlopen(self.urlName)
           if debugMessages:
              print "creation fichier Backup OK pour ",self.what
           self.create_backup=1
           self.backupFile = open(self.fichierBackup,"w")
           return 0
        except:
           if raiseError:
               raise NameError,"in readFromUrl"
           if self.readFromServer:
               messageBox("Solveur injoignable\n Impossibe de télécharger les data du serveur")
           return -1 
            
    def readFromBackup(self):
           global debugMessages
           
           self.origFileh = open(self.fichierBackup)
           if debugMessages:
              print "lecture fichier Backup OK pour ",self.what
           if self.origFileh:
                return 0
           else:
                return -1
            
    def openSource(self):
       global debugMessages
       
       if self.readFromServer:
           if debugMessages:
               print "Force la lecture des Data %s sur serveur"%self.what
           isreached=self.readFromUrl()
       else:
           isreached=self.readFromBackup()
           if isreached<0:
               isreached=self.readFromUrl()
       if isreached>=0:     
          self.fileList = self.origFileh.readlines()
          return 0
       else:
          return -1

    def readSource(self,lengthArticle):
        self.nbArticles=0
        for l in self.fileList:
            if self.create_backup:
                self.backupFile.write(l)
            articles=string.split(l,"=")
            for a in articles:
                article=string.split(a,"!")
                if len(article)==lengthArticle:
                    self.collect(article)
                    self.nbArticles+=1

    def closeSource(self):                    
        self.origFileh.close()
        if self.create_backup:
            self.backupFile.close()
        if debugMessages:
            print "%d %s lus "%(self.nbArticles,self.what)

    def postProcess(self):
        pass

#-------------------------------------------------------------------


class getProduits(getData):
    
    def __init__(self,urlName,fichierBackup,readFromServer):
        getData.__init__(self,urlName,fichierBackup,"Produits",6,readFromServer)

    def collect(self,article):
         (code,clef,fournisseur,prix,prix_plancher,libele)=article
         racourci = int(code[2:7])
         ProduitsRacourcis[racourci]=libele
         if racourci in ProduitsFournisseurs.keys():
            ProduitsFournisseurs[racourci].append(fournisseur)
         else:
            ProduitsFournisseurs[racourci]=[fournisseur]
         ProduitsCodes[racourci,fournisseur]=code
         Produits[code]=(libele,prix,racourci,prix_plancher,fournisseur)

#-------------------------------------------------------------------

class getClients(getData):
    
    def __init__(self,urlName,fichierBackup,readFromServer):
        getData.__init__(self,urlName,fichierBackup,"Clients",3,readFromServer)

    def collect(self,article):
        (societe,ville,clef)=article
        Clients[societe+"/"+ville]=(societe,ville,clef)

    def postProcess(self):
        global clefsClients
        
        clefsClients=Clients.keys()
        clefsClients.sort(key=str.lower)
        pass

#-------------------------------------------------------------------

class getFournisseurs(getData):
    
    def __init__(self,urlName,fichierBackup,readFromServer):
        getData.__init__(self,urlName,fichierBackup,"Fournisseurs",3,readFromServer)
        Fournisseurs['9999']=('XXXX','xxxx','9999')
      
    def collect(self,article):
        (societe,ville,clef)=article
        Fournisseurs[clef]=article

#-------------------------------------------------------------------

class getVendeurs(getData):
    
    def __init__(self,urlName,fichierBackup,readFromServer):
        getData.__init__(self,urlName,fichierBackup,"Vendeurs",3,readFromServer)

    def collect(self,article):
        (numero,nom,prenom)=article
        Vendeurs[numero]=(numero,nom,prenom)

#-------------------------------------------------------------------

class getReleases(getData):
    
    def __init__(self,urlName,fichierBackup,readFromServer):
        getData.__init__(self,urlName,fichierBackup,"Releases",2,readFromServer)

    def collect(self,article):
        (numero,filename)=article
        Releases[numero]=(numero,filename)

################################################################################
# Choix Vendeur, client, Produits, fournisseurs
##################################################################################

class choixXXX:

    def __init__(self,root,killable=0,minLengthFiltre=0):
        global zoomedWindow

        self.root=root
        self.clefs={}
        self.ihmChoix()
        self.minLengthFiltre=minLengthFiltre
        self.action()
        self.killable=killable
        if zoomedWindow:
           self.root.wm_state(newstate="zoomed")
           self.root.update()
        
    def __del__(self):
        try:
            self.root.destroy()
        except:
            pass
        

    def erase(self):
        try:
           self.filtreFrame.destroy()
           self.listFrame.destroy()
        except:
           pass
        
    def addchar(self,event):
        self.filtre=self.filtre+event.char
        self.nom.set(string.upper(self.filtre))
        self.action()

    def delchar(self,event):
        if len(self.filtre)==0 and self.killable:
            self.__del__()
            return
        self.filtre=self.filtre[:-1]
        self.nom.set(string.upper(self.filtre))
        self.action()

        
    def ihmChoix(self):

        # division de la fenetre en deux
        
        self.filtreFrame = Frame(self.root,height=1)
        self.filtreFrame.pack(side=TOP)

        
        self.listFrame = Frame(self.root)
        self.listFrame.pack(side=TOP,expand=1,fill=BOTH)

        # filtre
        self.labelFiltre=StringVar("")
        self.labelFiltre.set("filtre >")
        label = Label(self.filtreFrame, textvariable=self.labelFiltre, justify="left", fg="red", width=16)
        label.pack(side=LEFT,expand=1,fill=X)

        self.nom = StringVar("")
        label = Label(self.filtreFrame, textvariable=self.nom,  fg="black",width=20 )
        label.pack(side=LEFT,expand=1,fill=X)

        self.filtre=""

        # liste box

        scrollbar = Scrollbar(self.listFrame)
        scrollbar.pack(side=RIGHT,expand=0,fill=Y)

        self.listbox = Listbox(self.listFrame, yscrollcommand=scrollbar.set, height=22, width=35)
        self.listbox.pack(side=LEFT, expand=1, fill=BOTH)
        scrollbar.config(command=self.listbox.yview)

        bindElementKeysFunction(self.listbox,
                                "0123456789abcdefghijklmnopqrstuvwxyz'-*+",
                                self.addchar)

        self.listbox.bind("<space>",self.addchar) 
        self.listbox.bind("<BackSpace>",self.delchar)
        self.listbox.bind("<Return>",self.go) 

        self.listbox.focus_set()




class choixVendeur(choixXXX):

    def __init__(self):

        global version
        
        self.root = Tk()
        self.root.title("Oyak %s ? Vendeur ?"%version)
        choixXXX.__init__(self,self.root)        
        texte=">"
        self.labelFiltre.set(texte)
        self.root.mainloop()

    def go(self,event):
        global vendeur
        
        if self.filtre=="*":
           self.__del__()
           return

        try :
          clef=self.listbox.curselection()[0]
          choix=self.clefs[int(clef)]
        except:
          messageBox("Choix impossible!!!")
          return
          
        self.filtre=""
        self.nom.set(string.upper(self.filtre))
        vendeur=choix
        self.erase()
        choixClient(vendeur,self.root)
  
    def action(self,event="fake"):
        self.listbox.delete(0,END)
        nom = self.nom.get()
        nom.lower()

        self.clefs={}
        i=0
        liste=Vendeurs.keys()
        liste.sort(key=str.lower)
        for clef in liste:
               (numero,nom,prenom) = Vendeurs[clef]
               nom.lower()
               if string.lower(nom[:len(self.filtre)])==self.filtre:
                   self.listbox.insert(END, "%s %s"%(nom,prenom))
                   self.clefs[i]=(numero,nom,prenom)
                   i=i+1
        self.listbox.focus_set()
        self.listbox.selection_set(0)





class choixClient(choixXXX):

    def __init__(self,vendeur,root):
        global zoomedWindow

        self.root = root
        self.root.title("? Client ?")
        choixXXX.__init__(self,self.root,minLengthFiltre=1)        
        #print vendeur
        (numero,nom,prenom)=vendeur
        texte="%s >"%prenom
        self.labelFiltre.set(texte)
        if zoomedWindow:
           self.root.wm_state(newstate="zoomed")
           self.root.update()
        self.action()

    def go(self,event):
        if self.filtre=="*":
           try:
             self.root.destroy()
             self.root.quit()
           except:
              pass
           return

        choix=0
        try :
          clef=self.listbox.curselection()[0]
          choix=Clients[self.clefs[int(clef)]]
        except:
          if debugMessages:
              print "choix incoherent"
              return

        self.filtre=""
        self.nom.set(string.upper(self.filtre))

        if choix:
            self.action()
            processFacture(self.root,vendeur,choix)

    def action(self,event="fake"):
        global clefsClients

        self.listbox.delete(0,END)
        nom = self.nom.get()
        nom.lower()

        i=0
        n=len(self.filtre)
        if n>=self.minLengthFiltre:
          for clef in clefsClients:
            if string.lower(clef[:n])==self.filtre:
               self.listbox.insert(END, clef)
               self.clefs[i]=clef
               i=i+1
                
          self.listbox.focus_set()
          self.listbox.selection_set(0)





class choixProduit(choixXXX):

    def __init__(self,facture,valeur):
 
        self.facture=facture

        self.root = Toplevel()
        self.root.title("?produit?")
        choixXXX.__init__(self,self.root,killable=1)        
        (societe,ville,clef) = facture.client
        texte="%s >"%societe
        self.labelFiltre.set(texte)
        self.filtre=valeur
        self.nom.set(self.filtre)
        self.action()
        


    def go(self,event):
        if self.filtre=="*":
            self.__del__()
            return

        clef=self.listbox.curselection()[0]
        (racourci,libelle)=self.clefs[int(clef)]

        choixFournisseur(self.facture,racourci)

        self.__del__()


    def action(self,event="fake"):
        self.listbox.delete(0,END)
        nom = self.nom.get()
        nom.lower()

        self.clefs={}
        i=0
        liste=ProduitsRacourcis.keys()
        liste.sort()
        for racourci in liste:
            (libelle) = ProduitsRacourcis[racourci]
            libelle.lower()
            s="%04d-%s"%(racourci,libelle)
            c="%d"%racourci
            n=len(self.filtre)
            if string.lower(libelle[:n])==self.filtre or c.find(self.filtre)==0:
                self.listbox.insert(END, s)
                self.clefs[i]=(racourci,libelle)
                i=i+1
                
        self.listbox.focus_set()
        self.listbox.selection_set(0)




class choixFournisseur(choixXXX):

    def __init__(self,facture,racourci):
 
        self.facture=facture
        self.fournisseurs = ProduitsFournisseurs[racourci]
        self.racourci = racourci

        self.root = Toplevel()
        self.root.title(ProduitsRacourcis[racourci])
        choixXXX.__init__(self,self.root,killable=1)        
        (societe,ville,clef) = facture.client
        texte="%s>"%ProduitsRacourcis[racourci]
        self.labelFiltre.set(texte)


    def go(self,event):
        if self.filtre=="*":
            self.__del__()
            return

        clef=self.listbox.curselection()[0]
        choix=self.clefs[int(clef)]

        (societe,ville,clef) = choix
        self.facture.acceptProduit(self.racourci,clef)
        self.__del__()

    def action(self,event="fake"):
        self.listbox.delete(0,END)
        nom = self.nom.get()
        nom.lower()

        self.clefs={}
        i=0
        liste=self.fournisseurs
        n=len(self.filtre)
        for code in liste:
            (societe,ville,clef)=Fournisseurs[code]
            s="%04d-%s"%(int(clef),societe)
            c="%d"%int(clef)
            n=len(self.filtre)
            if string.lower(societe[:n])==self.filtre or c.find(self.filtre)==0:
                self.listbox.insert(END, s)
                self.clefs[i]=(societe,ville,clef)
                i=i+1
                
        self.listbox.focus_set()
        self.listbox.selection_set(0)



class choixRelease(choixXXX):

    def __init__(self,facture,racourci):
 
        self.facture=facture

        self.root = Toplevel()
        self.root.title("Choix d'une version")
        choixXXX.__init__(self,self.root,killable=1)        
        texte="choix>"
        self.labelFiltre.set(texte)


    def go(self,event):
        if self.filtre=="*":
            self.__del__()
            return

        clef=self.listbox.curselection()[0]
        choix=self.clefs[int(clef)]

        (numero,filename) = choix
        loadRelease(filename)
        messageBox("telechargement %s"%filename)
        self.__del__()

    def action(self,event="fake"):
        self.listbox.delete(0,END)
        nom = self.nom.get()
        nom.lower()

        self.clefs={}
        i=0
        liste=Releases.keys()
        n=len(self.filtre)
        for code in liste:
            (numero,filename)=Releases[code]
            s="%s"%(filename)
            n=len(self.filtre)
            if filename.find(self.filtre)==0:
                self.listbox.insert(END, s)
                self.clefs[i]=(numero,filename)
                i=i+1
                
        self.listbox.focus_set()
        self.listbox.selection_set(0)





################################################################################
# Saisie nom Facture
################################################################################

class processFacture:

    def __init__(self, root,vendeur,client):
        global zoomedWindow

        self.client=client
        self.numero_client=getNBclient()
        self.clefs={}
        
        self.root=Toplevel()
        (societe,ville,clef)=self.client
        self.root.title("%d-%s"%(self.numero_client,societe))

        if zoomedWindow:
           self.root.wm_state(newstate="zoomed")


        (numero,nom,prenom)=vendeur
        self.vendeur_prenom=prenom
        self.vendeur_numero=numero
        
        self.ihmFacture()
  

    def __del__(self):
        releaseNBclient(self.numero_client)
        try:
            self.root.destroy()
        except:
            pass
        

    def addLabelEntry(self,s):
        sVar= StringVar()
        sVar.set(s)

        label = Label(self.nameFrame, textvariable=sVar,  fg="red" )
        label.pack(side=TOP)

        e = Entry(self.inputFrame, fg="black" )
        e.pack(side=TOP)
        return (sVar,e)

    def ihmFacture(self):
        
        # division de la fenetre en trois
        
        self.clientFrame = Frame(self.root)
        self.clientFrame.pack(side=TOP)
        
        self.prixFrame = Frame(self.root)
        self.prixFrame.pack(side=TOP)

        self.nameFrame = Frame(self.prixFrame)
        self.nameFrame.pack(side=LEFT)

        self.inputFrame = Frame(self.prixFrame)
        self.inputFrame.pack(side=LEFT)

        
        self.listFrame = Frame(self.root)
        self.listFrame.pack(side=TOP,expand=1,fill=BOTH)


        (societe,ville,clef)=self.client
        self.clientClef=clef

        # rappel nom client
        label = Label(self.clientFrame, text="%s>%s"%(self.vendeur_prenom,societe), justify="center", fg="red",width=36)
        label.pack(side=TOP)

        # quantite, prix, article, fournisseur, date

        label,self.quantite = self.addLabelEntry("Quantite: (1.00)")
        self.prix_label,self.prix = self.addLabelEntry("Prix:")
        self.article_label,self.article = self.addLabelEntry("Article:")
        self.fournisseur_label,self.fournisseur = self.addLabelEntry("Fournisseur:")
        self.date_label,self.date = self.addLabelEntry("Date:")

        # liste box

        scrollbar = Scrollbar(self.listFrame)
        scrollbar.pack(side=RIGHT, expand=0, fill=BOTH)

        self.listbox = Listbox(self.listFrame, yscrollcommand=scrollbar.set, height=10)
        self.listbox.pack(side=LEFT, expand=1, fill=BOTH)
        scrollbar.config(command=self.listbox.yview)

        # Bindings...

        self.article.focus_set()
        bindElementKeysFunction(self.article,
                                "0123456789-x*",
                                self.processCodeProduit)
    
        self.article.bind(".",self.processProduit)
        #self.article.bind("<BackSpace>",self.deleteCode)
        #self.article.bind("<FocusOut>",self.cleanCode)
        
        self.article.bind("<Return>",self.route)

        bindElementKeysFunction(self.fournisseur,
                                "0123456789-x*",
                                self.processCodeFournisseur)
        self.fournisseur.bind(".",self.processFournisseur)

        self.date.bind("<Return>",self.goToQuantite)
        self.quantite.bind("<Return>",self.goToPrice)
        self.prix.bind("<Return>",self.addFacture)
        
        self.nbDigit=0
        self.listbox.delete(0,END)
        self.listbox.insert(END, enteteFact)
        self.nbArticles=0

        selectedCode[self.nbArticles]=""
        selectedRacourci[self.nbArticles]=""
        selectedFournisseur[self.nbArticles]=""
        selectedDate[self.nbArticles]=""
        selectedQuantite[self.nbArticles]=""
        selectedPrix[self.nbArticles]=""



    def processProduit(self,event):
        valeur=self.article.get()
        self.article.delete(0,END)
        choixProduit(self,valeur)

    def processFournisseur(self,event):
        choixFournisseur(self)

    def processCodeProduit(self,event):
        valeur=self.article.get()
        if len(valeur)==maxDigits-1:
                self.produit=valeur+event.char
                code=valeur+event.char
                if code in Produits.keys():
                    (libelle,prix,racourci,prix_plancher,fournisseur)=Produits[code]
                    self.acceptProduit(racourci,fournisseur)
                else:
                    self.deleteCode("")
                
    def acceptProduit(self,racourci,fournisseur):
        self.article.delete(0,END)
        self.fournisseur.delete(0,END)
        self.prix.delete(0,END)
            
        # le produit selectionne a un code barre
        if (racourci,fournisseur) in ProduitsCodes.keys():
            code = ProduitsCodes[racourci,fournisseur]
            (libelle,prix,racourci,prix_plancher,fournisseur)=Produits[code]
            (societe,ville,clef)=Fournisseurs[fournisseur]
            self.fournisseur.insert(END,societe)
            self.fournisseur_label.set("Fournisseur : %s"%fournisseur)
              
            self.article.insert(END,libelle)
            self.article_label.set("Article : %d"%racourci)
      
            self.prix_label.set("Prix : ("+"%6.2f"%(eval(prix)+0.00)+")")
            self.prix_default=prix
            self.prix_plancher=prix_plancher
            self.produit=code

            selectedCode[self.nbArticles]=code
            selectedRacourci[self.nbArticles]=racourci
            selectedFournisseur[self.nbArticles]=fournisseur    

            self.date.focus_set()
        else:
            messageBox("Article a part numero %s fournisseur %s",racourci,fournisseur)
                
    def processCodeFournisseur(self,event):
        valeur=self.fournisseur.get()
        self.fournisseur=valeur+event.char
        code=valeur+event.char
        
    def processCodeDate(self,event):
        valeur=self.date.get()
        self.date=valeur+event.char

    def cleanCode(self,event):
        l=len(self.article.get())
        self.article.delete(l-1,l)

    def deleteCode(self,event):
        self.article.delete(0,END)
        self.article_label.set("Article :")
        self.fournisseur.delete(0,END)
        self.fournisseur_label.set("Fournisseur :")
        self.date.delete(0,END)
        self.prix.delete(0,END)
        self.prix_label.set("Prix :")
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
        try :
          if (eval(prix)+0.0)<eval(self.prix_plancher)+0.:
            messageBox("Impossible le prix plancher est %6.2f > %s"%((eval(self.prix_plancher)+0.00),prix))
            self.prix.focus_set()
            return
        except:
            messageBox("le prix "+prix+" n'est pas reconnu")
            self.prix.delete(0,END)
            self.prix.focus_set()
            return
        quantite=self.quantite.get()
        if len(quantite)==0:
                quantite="1.0"

        article=self.article.get()
        try :
          self.listbox.insert(END, formatFact%(float(quantite),article,float(prix)))
        except :
            self.deleteCode("fake")

        selectedPrix[self.nbArticles]=prix
        selectedQuantite[self.nbArticles]=quantite
        selectedDate[self.nbArticles]=self.date.get()
        self.nbArticles=self.nbArticles+1

        selectedCode[self.nbArticles]=""
        selectedRacourci[self.nbArticles]=""
        selectedFournisseur[self.nbArticles]=""
        selectedDate[self.nbArticles]=""
        selectedQuantite[self.nbArticles]=""
        selectedPrix[self.nbArticles]=""

        self.deleteCode("fake")

    def factureOut(self):
        s="%s%s"%(self.clientClef,sep1)
        for l in range(0,self.nbArticles):
             s=s+"%s%s"%(selectedCode[l],sep2)
             s=s+"%s%s"%(selectedRacourci[l],sep2)
             s=s+"%s%s"%(selectedFournisseur[l],sep2)
             s=s+"%s%s"%(selectedDate[l],sep2)
             s=s+"%s%s"%(selectedQuantite[l],sep2)
             s=s+"%s%s"%(selectedPrix[l],sep1)
        params = urllib.urlencode({'vendeur': self.vendeur_numero, 'commande':s})
        try:
            f = urllib.urlopen(url_send_commande, params)
        except:
            messageBox("Le serveur ne répond pas!")
            return
        ack=f.readlines()
        l=ack[0]
        if (l=="0"):
            messageBox("Commande reçue!")
            self.__del__()
        else:
            messageBox("Commande perdue!")
            return
            
    
    def route(self,event):
        racourci=self.article.get()
        fournisseur=self.fournisseur.get()
        if racourci=="e" or fournisseur=="e":
            l=self.listbox.size()
            if l>1:
                self.listbox.delete(l-1,l)
                self.nbArticles=self.nbArticles-1
            self.deleteCode("fake")
            return
        # * ->  La commande est envoye
        if racourci=="*" or fournisseur=="*":
            if self.nbArticles==0:
              messageBox("La commande est vide!!!")
              self.article.delete(0,END)
              return            
            self.factureOut()
            return
        # * ou x ->  on tue la facture courrante
        if racourci=="x" or fournisseur=="x":
            messageBox("Commande annulee!")
            self.__del__()
            return
        if racourci=="DDD" or racourci=="ddd":
            messageBox("Telechargement du serveur")
            lisData(readFromServer=1)
            messageBox("OK...")
            return
        if racourci=="vvv" or racourci=="vvv":
            choixRelease(self,racourci)
            messageBox("OK nouvelle version telechargée, redemarrer le logiciel...")
            return
        # sinon on process le couple (racourci,fournisseur)
        try :
            racourci=int(racourci)
        except:
            messageBox("%s n'est pas un code reconnu!"%racourci)
            self.article.delete(0,END)
            return
        if racourci in ProduitsRacourcis.keys() and len(fournisseur)==0:
            choixFournisseur(self,racourci)
        else:
            messageBox("%d n'est pas un code reconnu!"%racourci)
            self.article.delete(0,END)
            
        
def run():
    if oneFrame:
       ihm = ihmRoot()
       ihm.start()
    else:
##        if erreurCatch:
##            try:
##               lisData() 
##               choixVendeur()
##            except:
##               pass
##        else:
            lisData() 
            choixVendeur()


if __name__ == "__main__":
    run()
