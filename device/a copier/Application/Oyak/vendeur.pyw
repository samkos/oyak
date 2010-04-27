# -*- coding: cp1252 -*-
from Tkinter import *
import os
import shutil
import string
import traceback
import urllib

oyak=0

class singleton:
    
    def __init__(self):
        
        self.maxDigits=130
        self.cible=os.path.exists('\Platform')
        self.version="0.33"
        self.time_last_key=0
        self.isServeurInjoignable=0
        
        if self.cible:
            self.zoomedWindow=1
            self.erreurCatch=0
            self.debugMessages=0
            self.raiseError=0
            self.website_address="http://192.168.111.77/phpmyfactures"
            self.fichierIp='\Platform\S24Profiles.reg'
            self.fichierIpBackup='\\Oyak\\S24old.reg'
            self.fichierIpNew='\\Oyak\\S24New.reg'
            self.fichierIpTemplate='\\Application\\Oyak\\S24Profiles.reg'
            self.fichierAppTemplate='\\Application\\Oyak\\Data\\%s.bak'
            self.fichierAppOldTemplate='\\Application\\Oyak\\Data\\%s.old'
            self.fichierBackup_Template='\Oyak\%s.bak'
            self.fichierTemp_Template='\Oyak\%s.tmp'
            self.fichierOld_Template='\Oyak\%s.old'
        else:
            self.erreurCatch=0
            self.debugMessages=1
            self.zoomedWindow=0
            self.raiseError=1
            self.website_address="http://127.0.0.1/phpmyfactures"
            self.root_address="c:/Program Files/EasyPHP1-8/www/phpmyfactures/device/a copier/"
            self.fichierIp=self.root_address+"Platform/test/S24Profiles.reg"
            self.fichierIpBackup=self.root_address+"Platform/test/S24old.reg"
            self.fichierIpNew=self.root_address+"Platform/test/S24new.reg"
            self.fichierIpTemplate=self.root_address+"Application/Oyak/S24Profiles.reg"
            self.fichierAppTemplate=self.root_address+"Application/Oyak/Data/%s.bak"
            self.fichierAppOldTemplate=self.root_address+"Application/Oyak/Data/%s.old"
            self.fichierBackup_Template='c:\Oyak\%s.bak'
            self.fichierTemp_Template='c:\Oyak\%s.tmp'
            self.fichierOld_Template='c:\Oyak\%s.old'
        
        self.myVendeur=0
        self.myClient=0;
        self.myFournisseur=0
        self.myProduit=0
        self.myRelease=0
        
        self.myCurrentAddChar=0
        self.myCurrentDelChar=0
        self.myCurrentEnterChar=0
        self.myCurrentEntry=0
        
        self.Produits={}
        self.ProduitsFournisseurs={}
        self.ProduitsRacourcis={}
        self.ProduitsCodes={}
        self.Clients={}
        self.Vendeurs={}
        self.Fournisseurs={}
        self.Fournisseurs['9999']=('XXXX', 'xxxx', '9999')
        self.Releases={}
        self.Factures={}
        self.clientNB = {}
        self.timestamp = {}
        
        for i in range(10):
            self.clientNB[i]=0
            
        self.clefsClients=list()
        self.nbChamps = {"vendeurs":4, "fournisseurs":4, "clients":4,
                    "releases":2, "produits":8}
        self.isAlreadyPaneled = {"vendeurs":0, "fournisseurs":0, "clients":0,
                    "releases":0, "produits":0}
        self.barSize = {"vendeurs":0.1, "fournisseurs":0.9, "clients":0.3,
                    "releases":0.96, "produits":0.6}
        
        self.formatFact="%5.2f|%15s|%5.2f"
        self.enteteFact="%5s|%15s|%5s"%("quant", "produit", "prix")
        
        
        
        self.url_send_commande=self.website_address+"/query/index.php?"
        self.url_update_commande=self.website_address+"/query/download.php?"
        
        self.url_get_Template=self.website_address+"/query/get_data.php?%s=1"
        
        
        self.sep1=";"
        self.sep2="!"
        
        
        self.vendeurChoisi=(0, "xxx", 'xx')
        self.factureCurrent=0
        self.ihm=0


    ###################################################################
    #
    #  fonction IHM annexe
    #
    ###################################################################
    
    def getNBfacture(self) :
        i=1
        for i in range(10):
            if oyak.clientNB[i]==0:
                oyak.clientNB[i]=1
                return i
        return -1
    
    def getFirstFacture(self) :
       for i in range(10):
            if oyak.clientNB[i]>0:
                return i
       return -1
    
    def releaseNBfacture(self,i):
        oyak.clientNB[i]=0
    
    def  isNBfacture(self,i):
          return oyak.clientNB[i]
    
    def bindElementKeysFunction(self,element, keys, func):
        for c in keys:
            element.bind(c, func)
    


###############################################################################################
# Gestion rationalisée de l'IHM
###############################################################################################


class ihmRoot:
    
    global oyak

    def __init__(self):
       self.ihm=Tk()
       self.kbd=Tk()
       
       if oyak.cible:
           self.ihm.overrideredirect(1)

       self.ihmPanels={}
       self.ihmPanelsContents={}
       self.filtreChoice={}
       self.filtreLabel={}
       self.listbox={}
       self.listbox0={}
       self.facture={}
       self.factureButton={}
       self.okButton={}
       self.kbd.keyboardSV=StringVar()

       
       self.Xmax=38
       self.Ymax=24

       self.ihm.rowconfigure(0, weight=1)
       self.ihm.columnconfigure(0, weight=1)
       #self.ihm.master.grid(sticky=W+E+N+S)
       
       self.messagePanelCreate()
       self.messageOuiNonPanelCreate()

       self.progressBarCreate()
       self.menuCreate()
       self.keyboardCreate()
       self.adminCreate()
       self.ipCreate()
       
       self.currentShown="message"
       
    # fonctions de Management des fenetres types
    
    def title(self, s):
       self.ihm.title(s)

    def add(self, panelName, widgetName, widget, row, column, rowspan=1, colspan=1, sticky=N+E+W+S):
        if panelName in self.ihmPanels.keys():
           self.ihmPanels[panelName].append(widgetName)
        else:
           self.ihmPanels[panelName]=[widgetName]
        self.ihmPanelsContents[panelName, widgetName]=(widget, row, column, rowspan, colspan, sticky)
      
    def hide(self, panelName):
        for widgetName in self.ihmPanels[panelName]:
            (widget, row, column, rowspan, colspan, sticky)=self.ihmPanelsContents[panelName, widgetName]
            widget.grid_forget()
            
    def show(self, panelName, title="Oyak", hidingAll=1):
        
        if hidingAll:
            self.hideAll()
        
        self.ihm.title(title)
        for widgetName in self.ihmPanels[panelName]:
            (widget, row, column, rowspan, colspan, sticky)=self.ihmPanelsContents[panelName, widgetName]
            widget.grid(row=row, column=column, rowspan=rowspan, columnspan=colspan, sticky=sticky)

        if oyak.zoomedWindow:
            self.ihm.wm_state(newstate="zoomed")

        self.previousShown=self.currentShown
        self.currentShown=panelName


    def hideAll(self):
        for panel in self.ihmPanels.keys():
            if not(panel=="keyboard"):
                self.hide(panel)

    def returnPrevious(self):
        self.show(self.previousShown)
        #self.ihm.call('focus',self.oldFocus)


    # creation fenetre type message
    
    def messagePanelCreate(self):
        self.message=StringVar("")
        self.message.set("Message Type")
        self.MessageButton=Button(self.ihm, textvariable=self.message, width=self.Xmax, height=self.Ymax)
        self.add("message", "texte", self.MessageButton, 0, 0)

    def showMessage(self, what, commande=0):
        self.message.set(what)
        if not(commande):
            self.MessageButton["command"]=self.returnPrevious
        else:
            self.MessageButton["command"]=commande
        self.show("message")

        self.MessageButton.bind("<Key>", lambda x="fake":self.MessageButton.invoke())
        self.MessageButton.focus_set()
        

    # creation fenetre type Oui/Non
    
    def messageOuiNonPanelCreate(self):
        self.messageOuiNon=StringVar("")
        self.messageOuiNon.set("Message Type")
        self.labelOuiNon=Label(self.ihm, textvariable=self.messageOuiNon, width=self.Xmax, height=self.Ymax/3)
        self.add("OuiNon", "question", self.labelOuiNon, 0, 0)
        self.buttonOui=Button(self.ihm, text="Oui", width=self.Xmax, height=self.Ymax/3)
        self.add("OuiNon", "oui", self.buttonOui, 1, 0)
        self.buttonNon=Button(self.ihm, text="Non", width=self.Xmax, height=self.Ymax/3)
        self.add("OuiNon", "non", self.buttonNon, 2, 0)

    def showMessageOuiNon(self, what, siOui=0, siNon=0):
        self.messageOuiNon.set(what)
        if not(siOui):
            self.buttonOui["command"]=self.returnPrevious
        else:
            self.buttonOui["command"]=siOui

        if not(siNon):
            self.buttonNon["command"]=self.returnPrevious
        else:
            self.buttonNon["command"]=siNon

        self.show("OuiNon")

        self.buttonNon.bind("<Key>", lambda x="fake":self.buttonNon.invoke())
        self.buttonNon.focus_set()
        

    # creation fenetre type progressBar
    def progressBarCreate(self):
        self.messageBar=StringVar("")
        self.messageBar.set("Message Type")
        self.labelBar=Button(self.ihm, textvariable=self.messageBar, width=self.Xmax, height=self.Ymax-2)
        self.add("progress", "texte", self.labelBar, 0, 0)
        self.progressBar=Canvas(self.ihm, width=self.Xmax, height=30)
        self.add("progress", "bar", self.progressBar, 1, 0)

    def startProgressBar(self, what):
        self.show("progress")
        self.updateProgressBar(what, 0)
    
    def updateProgressBar(self, what, ratio):
        self.show("progress")
        self.messageBar.set(what)
        self.labelBar.update()
        self.progressBar.delete(ALL)
        self.progressBar.create_rectangle(0, 0, self.Xmax* ratio*6., 30, fill='blue')
        self.ihm.update()
        
        
    # creation fenetre type Menu
    
    def menuCreate(self):

        panelName = "menu"
        
        label = Button(self.ihm, text="Retour", command=self.returnPrevious, height=3, width=self.Xmax)
        self.add(panelName, "retour", label, 1, 0)

        label = Button(self.ihm, text="Factures en Cours", command=self.showFactureFirst, height=4, width=self.Xmax)
        self.add(panelName, "en cours", label, 2, 0)

        label = Button(self.ihm, text="Nouvelle Facture", command=processFacture, height=4, width=self.Xmax)
        self.add(panelName, "autre", label, 3, 0)

        label = Button(self.ihm, text="Choisir Vendeur", command=self.changeVendeur, height=4, width=self.Xmax)
        self.add(panelName, "vendeur", label, 5, 0)

        label = Button(self.ihm, text="Relire Donnée", command=self.rechargeBase, height=4, width=self.Xmax)
        self.add(panelName, "reloader", label, 6, 0)
        
#        label = Button(self.ihm, text="Clavier", command=self.showKeyboard,height=4,width=self.Xmax)
#        self.add(panelName,"reloader",label,7,0)

#        label = Button(self.ihm, text="Reglages", command=self.showIp,height=4,width=self.Xmax)
#        self.add(panelName,"update",label,8,0)

#        label = Button(self.ihm, text="Reactiver Scanner", command=self.scanner,height=4,width=self.Xmax)
#        self.add(panelName,"scanner",label,9,0)


        label = Button(self.ihm, text="QUITTER", command=self.ihm.quit, height=4, width=self.Xmax)
        self.add(panelName, "quitter", label, 10, 0)

         
#        label = Button(self.ihm, text="Administrer", command=self.showAdmin,height=5,width=self.Xmax)
#        self.add(panelName,"admin",label,10,0)

    # creation fenetre type Menu
    
    def adminCreate(self):

        panelName = "admin"
        
        label = Button(self.ihm, text="Retour", command=self.returnPrevious, height=3, width=self.Xmax)
        self.add(panelName, "retour", label, 2, 0)

        label = Button(self.ihm, text="Relire Donnée", command=self.rechargeBase, height=4, width=self.Xmax)
        self.add(panelName, "reloader", label, 6, 0)
        
        label = Button(self.ihm, text="Mettre a jour", command=chooseRelease, height=4, width=self.Xmax)
        self.add(panelName, "update", label, 7, 0)
        
        label = Button(self.ihm, text="Connection", command=self.showIp, height=4, width=self.Xmax)
        self.add(panelName, "update", label, 8, 0)
        
        label = Button(self.ihm, text="Retour", command=self.showMenu, height=3, width=self.Xmax)
        self.add(panelName, "retour", label, 9, 0)

        label = Button(self.ihm, text="QUITTER", command=self.ihm.quit, height=4, width=self.Xmax)
        self.add(panelName, "quitter", label, 10, 0)
        
    # creation fenetre type changement IP
    


    def ipCreate(self):

        self.ipAddress=StringVar()
        self.ipSid=StringVar()
        
        panelName = "ip"

        # quantite, prix, article, fournisseur, date

        label=Label(self.ihm, text="Adresse ;")
        entry  = Entry(self.ihm, textvariable=self.ipAddress)
        self.add(panelName, "ipLabel", label, 2, 0)
        self.add(panelName, "ipEntry", entry, 3, 0)

        label=Label(self.ihm, text="Reseau ;")
        entry  = Entry(self.ihm, textvariable=self.ipSid)
        self.add(panelName, "sidLabel", label, 4, 0)
        self.add(panelName, "sidEntry", entry, 5, 0)

        
        
#        label = Button(self.ihm, text="Ping", command=self.returnPrevious,height=3)
#        self.add(panelName,"ping",label,6,0,colspan=2)

        label = Button(self.ihm, text="Mettre a jour",
                       command=lambda x=1:ipChange(self.ipAddress.get(), self.ipSid.get()), height=4)
        self.add(panelName, "update", label, 7, 0, colspan=2)

        label = Button(self.ihm, text="QUITTER", command=self.ihm.quit, height=4, width=self.Xmax)
        self.add(panelName, "quitter", label, 10, 0)

    # creation fenetre type menu

    def showMenu(self):
        self.show("menu")

    def showAdmin(self):
        self.show("admin")

    def showIp(self):
        global fichierIp
        
        f=open(fichierIp, "r")
        l=f.readline()
        f.close
        #print fichierIp
        #print l
        r=l.split(' ')
        self.ipAddress.set(r[1])
        self.ipSid.set(r[2])
        self.show("ip")


    def testReseau(self):
        os.system('\windows\nictt.exe')

    def scanner(self):
        os.system('\windows\startup\scanwedge.exe')


    # creation fenetre type Facture
    
    def factureCreate(self, num):

        what="%d"%num
        panelName = "facture"+what
        
        # Menu
        frame = Frame(self.ihm)
        self.add(panelName, "menu", frame, 0, 0, colspan=5)
        label = Button(frame, text="MENU", command=self.showMenu, height=2)
        label.pack(side=LEFT, expand=1, fill=BOTH)
        label = Button(frame, text="KEYB", command=self.showKeyboard, height=2)
        label.pack(side=LEFT, expand=1, fill=BOTH)

        
        # frame

        self.facture[what] = Frame(self.ihm, width=self.Xmax, height=self.Ymax-30)
        self.add(panelName, "facture", self.facture[what], 1, 0, colspan=5)

        button = Button(self.ihm, text="<<<", command=self.facturePrevious, height=3, width=6)
        self.add(panelName, "previous", button, 3, 0)

        button = Button(self.ihm, text="Nouvelle\nFacture", command=self.factureNew, height=3, width=6)
        self.factureButton[num, "ajouter"]=button
        self.add(panelName, "ajouter", button, 3, 1)
        
        button = Button(self.ihm, text="envoyer\nFacture", command=self.ihm.quit, height=3, width=6)
        self.factureButton[num, "envoyer"]=button
        self.add(panelName, "envoyer", button, 3, 2)
        
        button = Button(self.ihm, text="Annuler\nFacture", command=self.ihm.quit, height=3, width=6)
        self.factureButton[num, "annuler"]=button
        self.add(panelName, "annuler", button, 3, 3)

        button = Button(self.ihm, text=">>>", command=self.factureNext, height=3, width=6)
        self.add(panelName, "next", button, 3, 4)


        return self.facture[what]

    def start(self):
        if oyak.zoomedWindow:
            self.ihm.wm_state(newstate="zoomed")
        self.startProgressBar("OYAK v %s \n\n\n Bienvenue"%oyak.version)
        self.ihm.after(2000, self.lectureDonnee)
        self.showKeyboard()
        self.ihm.mainloop()

    def facturePrevious(self):
        global factureCurrent, clientNB
        
        nbPrevious=factureCurrent-1

        while nbPrevious>=0:
            if clientNB[nbPrevious]>0:
                Factures[nbPrevious].show()
                return 
            nbPrevious = nbPrevious-1

        self.showMessage("Pas d'autre\nFacture!!!")

    def factureNext(self):
        global factureCurrent, clientNB
        
        nbNext=factureCurrent+1

        while nbNext<10:
            if clientNB[nbNext]>0:
                Factures[nbNext].show()
                return 
            nbNext = nbNext+1

        self.showMessage("Pas d'autre\nFacture!!!")

    def showFactureFirst(self, menu=0):
        i=getFirstFacture()
        if  i<0 and menu==0:
            self.factureNew()
        else:
            if i<0:
                myClient.ihmShow()
            else:
                Factures[i].show()

    def factureNew(self):
        self.showMessageOuiNon("Demarrer une \nautre Facture?", siOui=processFacture)

    def delCurrentFacture(self):
        global factureCurrent, Factures

        releaseNBfacture(factureCurrent)
        self.showFactureFirst(menu=1)

    def lectureDonnee(self):
        lisData(clearAll=1)
        oyak.myVendeur.ihmShow()

    def rechargeBase(self):
        ihm.showMessage("Telechargement du serveur")
        lisData(clearAll=1, forceRecharge=1)
        ihm.showMessage("OK...", self.showMenu)

    def changeVendeur(self):
        global myVendeur
        myVendeur.ihmShow()



    # creation fenetre type keyboard
    def keyboardCreate(self):

        panelName="keyboard"
        self.keyboardString=""
        

        keyboardFrame=Frame(self.kbd)

#        Label(keyboardFrame, text=">").pack(side=LEFT, expand=1, fill=BOTH)
#        Label(keyboardFrame, textvariable=self.kbd.keyboardSV).pack(side=LEFT, expand=1, fill=BOTH)
        j=0
        self.add(panelName, "input", keyboardFrame, j, 0, colspan=7)
        self.kbd.keyboardSV.set(self.keyboardString)

        keys=Frame(self.kbd)
        self.add(panelName, "keys", keys, j+1, 0, colspan=7)
#        keys=Frame(keyb).pack(side=LEFT,expand=1,fill=BOTH)
#        ctrl=Frame(keyb).pack(side=LEFT,expand=1,fill=BOTH)


        for l in ["1234567890", "azertyuiop", "qsdfghjklm", "wxcvbn,.-*",
                  " ", ["DEL", "ENTER"]]:
            i=0
            line=Frame(keys)
            for c in l:
                b=Button(line, text=c)
                b["command"]=lambda x=c:self.addKey(car=x)
                b.pack(side=LEFT, expand=1, fill=BOTH)
                i=i+1
            line.pack(side=TOP, expand=1, fill=BOTH)
            

    def showKeyboard(self):
        self.show("keyboard", hidingAll=0)
        #self.kdb.Raise()
    
    def addKey(self, car):
        global oyak
        if car=="DEL":
            oyak.myCurrentDelChar("fake")
            return
        if car=="ENTER":
            oyak.myCurrentEnterChar("fake")
            return
        oyak.myCurrentAddChar(car)


###################################################################
#
#  Lectures des datas
#
###################################################################

        
class lisData:

    global oyak
    
    def __init__(self, clearAll=0, forceRecharge=0):
  
        oyak.ihm.updateProgressBar("Chargement Data", 0.)

        self.forceRecharge=forceRecharge
        self.clearAll=clearAll
        
        if clearAll:
            Produits={}
            ProduitsFournisseurs={}
            ProduitsRacourcis={}
            ProduitsCodes={}
            Clients={}
            Vendeurs={}
            Fournisseurs={}
            Fournisseurs['9999']=('XXXX', 'xxxx', '9999')
            Releases={}
            timestamp = {}


        oyak.myVendeur=chooseVendeur(forceRecharge)
        oyak.myClient=chooseClient(forceRecharge)
        oyak.myProduit=chooseProduit(forceRecharge)
        oyak.myFournisseur=chooseFournisseur(forceRecharge)


    
class getData:
    global oyak

    def __init__(self, what, forceRecharge):
        
        oyak.ihm.updateProgressBar("Chargement %s..."%what, oyak.barSize[what])
        
        # initialisation
        self.what=what
        
        lengthArticle=oyak.nbChamps[what]

        # creation des nom de fichiers
        self.fichierBackup=oyak.fichierBackup_Template%what
        self.fichierTemp=oyak.fichierTemp_Template%what

        # ouverture du fichier temporaire
            
        # lecture sur fichier backup d'abord
        if not(forceRecharge) and self.readFromBackup()==0:
            if oyak.debugMessages:
                print "lecture from Backup pour %s"%what
            self.readSource(lengthArticle)
            self.closeSource()
        # lecture depuis la base
        else:
            if oyak.debugMessages:
                print "lecture from web pour %s "%what

	    isThere=os.path.exists(self.fichierBackup)
            if isThere:
               os.unlink(self.fichierBackup)
            self.tmpFile = open(self.fichierTemp, "w")
            self.urlName=url_get_Template%what

            if self.readFromUrl()==0:
                self.readSource(lengthArticle)
                self.closeSource()

        # sauvegarde sur la device des données
            self.tmpFile.close()
            self.fichierOld=fichierOld_Template%what
            try :
                os.rename(self.fichierTemp, self.fichierBackup)

                # recopie dans la zone permanente
                shutil.copy(self.fichierBackup, fichierAppTemplate%what)
            except:
                if oyak.debugMessages:
                    print "pb a la sauvegarde du fichier Backup"
                raise
            
        # creation du panel lie a cette variable

        if not(oyak.isAlreadyPaneled[what]):
            self.choosePanelCreate(what)
            oyak.isAlreadyPaneled[what]=1


    # creation fenetre type choix
    
    def choosePanelCreate(self, what):
        
        panelName = what
        panelName0 = what+"0"
        
        # Menu
        frame = Frame(oyak.ihm.ihm)
        oyak.ihm.add(panelName, "menu", frame, 0, 0, colspan=2)
        label = Button(frame, text="MENU", command=oyak.ihm.showMenu, height=2)
        label.pack(side=LEFT, expand=1, fill=BOTH)
        label = Button(frame, text="KEYB", command=oyak.ihm.showKeyboard, height=2)
        label.pack(side=LEFT, expand=1, fill=BOTH)
        
        # filtre
        oyak.ihm.filtreLabel[what]=StringVar("")
        oyak.ihm.filtreLabel[what].set("filtre >")
        label = Label(oyak.ihm.ihm, textvariable=oyak.ihm.filtreLabel[what],
                      width=oyak.ihm.Xmax-1, height=1, justify="left", fg="red")
        oyak.ihm.add(panelName, "filtreLabel", label, 1, 0, sticky="W")
        oyak.ihm.add(panelName0, "filtreLabel", label, 1, 0, sticky="W")
        
        # liste box

        scrollbar = Scrollbar(oyak.ihm.ihm)
        scrollbar0 = Scrollbar(oyak.ihm.ihm)
        oyak.ihm.add(panelName, "scrollbar", scrollbar, 2, 1, sticky=N+S)
        oyak.ihm.add(panelName0, "scrollbar", scrollbar0, 2, 1, sticky=N+S)
        
        oyak.ihm.listbox[what] = Listbox(oyak.ihm.ihm, height=oyak.ihm.Ymax-6, yscrollcommand=scrollbar.set)
        oyak.ihm.add(panelName, "listbox", oyak.ihm.listbox[what], 2, 0)
        scrollbar.config(command=oyak.ihm.listbox[what].yview)

        oyak.ihm.listbox0[what] = Listbox(oyak.ihm.ihm, height=oyak.ihm.Ymax-6, yscrollcommand=scrollbar.set)
        oyak.ihm.add(panelName0, "listbox", oyak.ihm.listbox0[what], 2, 0)
        scrollbar0.config(command=oyak.ihm.listbox0[what].yview)


        # Menu
        button = Button(oyak.ihm.ihm, text="OK", height=3)
        oyak.ihm.okButton[what]=button
        oyak.ihm.add(panelName, "OK", button, 3, 0, colspan=2)
        oyak.ihm.add(panelName0, "OK", button, 3, 0, colspan=2)


        
    def readFromUrl(self):
        global isServeurInjoignable

        self.create_backup=1

        if not(isServeurInjoignable):
            try:
                self.origFileh = urllib.urlopen(self.urlName)
                return 0
            except:
                oyak.ihm.showMessage("Solveur injoignable\n Impossibe de télécharger les data du serveur \n Repli sur Backup")
                isServeurInjoignable=1
        return -1 
            
    def readFromBackup(self):
        self.create_backup=0
        
        try :
            self.origFileh = open(self.fichierBackup)
            return 0
        except :
            return -1     

            
    def readSource(self, lengthArticle):
        self.fileList = self.origFileh.readlines()
        self.nbArticles=0
        for l in self.fileList:
            if self.create_backup:
                self.tmpFile.write(l)
            articles=string.split(l, "=")
            for a in articles:
                article=string.split(a, "!")
                if len(article)==lengthArticle:
                    if self.collect(article):
                        self.nbArticles+=1

    def closeSource(self):                    
        self.origFileh.close()
        if oyak.debugMessages:
            print "%d %s lus"%(self.nbArticles, self.what)
            print
            



###############################################################################################
# Gestion adresse IP et reseau
###############################################################################################

def ipChange(ipAddress, ipSid):
    global ipFichier, ipFichierTemplate
    
    shutil.copy(fichierIp, fichierIpBackup)

    f=open(fichierIpTemplate)
    g=open(fichierIpNew, "w")
    
    l=f.readline()
    while (l):
        l=string.replace(l, "OYAK_SID", ipSid)
        l=string.replace(l, "OYAK_IP", ipAddress)
        g.write(l)
        l=f.readline()

    f.close()
    g.close()

    try :
        os.unlink(fichierIp)
        os.rename(fichierIpNew, fichierIp)
    except:
        shutil.copy(fichierIpBackup, fichierIp)


################################################################################
# Choix Vendeur, client, Produits, fournisseurs
##################################################################################

class chooseXXX(getData):
    global oyak
 
    def __init__(self, what, forceRecharge=0):
        getData.__init__(self, what, forceRecharge)
        
        
    def ihmShow(self, what, filtre="", killable=0):
                
        self.listbox = oyak.ihm.listbox[what]
        self.listbox0 = oyak.ihm.listbox0[what]
        self.clefs0={}
        
        self.what=what
        self.killable=killable
        self.filtre=filtre
        self.initPanel()
        self.setFiltre(filtre)
        self.ihmChoix()

        oyak.ihm.okButton[what]["command"]=lambda x="fake" : self.go("fake")
        self.listePrepare()

        oyak.ihm.show(what)
        self.action()
        
    def initPanel(self):
        pass
            
    def listePrepare(self):
        pass
            
    def setFiltre(self, filtre):
        
        oyak.ihm.filtreLabel[self.what].set(self.filtreName+filtre)
        self.filtre=filtre
        oyak.myCurrentAddChar=self.addcharFromKbd
        oyak.myCurrentDelChar=self.delchar
        oyak.myCurrentEnterChar=self.go
        
    def addcharFromKbd(self, char):
        self.filtre=self.filtre+char
        self.setFiltre(self.filtre)
        self.action()

    def addchar(self, event):
        self.filtre=self.filtre+event.char
        self.setFiltre(self.filtre)
        self.action()

    def delchar(self, event):
        if len(self.filtre)==0 and self.killable:
             oyak.ihm.returnPrevious()
             return
        self.filtre=self.filtre[:-1]
        self.setFiltre(self.filtre)
        self.action()


    def ihmChoix(self):

        oyak.bindElementKeysFunction(self.listbox,
                                "0123456789abcdefghijklmnopqrstuvwxyz'-*+",
                                self.addchar)

        oyak.bindElementKeysFunction(self.listbox0,
                                "0123456789abcdefghijklmnopqrstuvwxyz'-*+",
                                self.addchar)

        self.listbox.bind("<space>", self.addchar) 
        self.listbox.bind("<BackSpace>", self.delchar)
        self.listbox.bind("<Return>", self.go) 

        self.listbox0.bind("<space>", self.addchar) 
        self.listbox0.bind("<BackSpace>", self.delchar)
        self.listbox0.bind("<Return>", self.go) 




class chooseVendeur(chooseXXX):
    global oyak

    def __init__(self, forceRecharge=0):
        chooseXXX.__init__(self, "vendeurs", forceRecharge)        

    def ihmShow(self):
        chooseXXX.ihmShow(self, "vendeurs")        

    def collect(self, article):
        global Vendeurs
        (numero, nom, prenom, timestamp)=article
        oyak.Vendeurs[numero]=(numero, nom, prenom)
        return 1
                                    
    def initPanel(self):
        self.filtreName="Vendeur > "

    def go(self, event):
        
        try :
          #print len(self.clefs0)
          if len(self.filtre)==0 and len(self.clefs0)>0:
              clef=self.listbox0.curselection()[0]
              choix=self.clefs0[int(clef)]
              #print clef,choix
          else:
              clef=self.listbox.curselection()[0]
              choix=self.clefs[int(clef)]
        except:
          if self.filtre=="ipipip" or self.filtre=="IPIPIP":
            oyak.ihm.showIp()
            return
          oyak.ihm.showMessage("Choix impossible!!!", self.action)
          return
          
        self.filtre=""
        self.setFiltre(self.filtre)
        
        oyak.vendeurChoisi=choix
        oyak.myClient.ihmShow()

    def action(self, event="fake"):
        self.listbox.delete(0, END)


        self.clefs={}
        i=0
        liste=oyak.Vendeurs.keys()
        liste.sort(key=str.lower)
        for clef in liste:
               (numero, nom, prenom) = oyak.Vendeurs[clef]
               nom.lower()
               if string.lower(nom[:len(self.filtre)])==self.filtre:
                   self.listbox.insert(END, "%s %s"%(nom, prenom))
                   self.clefs[i]=(numero, nom, prenom)
                   i=i+1
        oyak.ihm.show(self.what)
        self.listbox.focus_set()
        self.listbox.selection_set(0)



class chooseClient(chooseXXX):

    def __init__(self, forceRecharge=0):
        chooseXXX.__init__(self, "clients", forceRecharge)
        
    def ihmShow(self):
        chooseXXX.ihmShow(self, "clients")
        
    def collect(self, article):
        (societe, ville, clef, timestamp)=article
        oyak.Clients[societe+"/"+ville]=(societe, ville, clef)
        return 1

    def listePrepare(self):
        clefsClients=oyak.Clients.keys()
        clefsClients.sort(key=str.lower)

        i=0
        for clef in clefsClients:
            (societe, ville, nb)=oyak.Clients[clef]
            self.listbox0.insert(END, "%04d-%s"%(int(nb[1:]), clef))
            self.clefs0[i]=clef
            i=i+1
        #print self.listbox0

        pass

    def initPanel(self):
        self.clefs={}
        (numero, nom, prenom)=oyak.vendeurChoisi
        self.filtreName="%s > "%prenom

    def go(self, event):
        global oyak
        try :
          if len(self.filtre)==0 and len(self.clefs0)>0:
              clef=self.listbox0.curselection()[0]
              choix=oyak.Clients[self.clefs0[int(clef)]]
          else:
              clef=self.listbox.curselection()[0]
              choix=oyak.Clients[self.clefs[int(clef)]]
        except:
            oyak.ihm.showMessage("Choix impossible!!!", self.action)
            return 0

        self.filtre=""
        self.setFiltre(self.filtre)
                
        processFacture(client=choix)

    def action(self, event="fake"):
        global clefsClients


        i=0
        n=len(self.filtre)
        if n==0:
            oyak.ihm.show("clients0")
            self.listbox0.focus_set()
            self.listbox0.selection_set(0)
        else:
            self.listbox.delete(0, END)
            oyak.ihm.show("clients")
            self.listbox.focus_set()
            self.listbox.selection_set(0)
            for clef in oyak.Clients.keys():
                (societe, ville, nb)=oyak.Clients[clef]
                nb=nb[1:]
                if string.lower(clef[:n])==self.filtre or  nb.find(self.filtre)==0:
                    self.listbox.insert(END, "%04d-%s"%(int(nb), clef))
                    self.clefs[i]=clef
                    i=i+1




class chooseProduit(chooseXXX):

    def __init__(self, forceRecharge=0):
        
        chooseXXX.__init__(self, "produits", forceRecharge)
        
    def ihmShow(self, facture, valeur):
        self.liste0={}
        self.clefs0={}
        
        self.facture=facture
        self.valeur=valeur
        (societe, ville, clef) = facture.client
        self.filtreName="%s >"%societe
        chooseXXX.ihmShow(self, "produits", killable=1)
        
    def initPanel(self):
        self.filtre=self.valeur
        

    def collect(self, article):
         (code, clef, fournisseur, prix, prix_plancher, poids, libele, timestamp)=article
         racourci = int(clef)
         oyak.ProduitsRacourcis[racourci]=libele
         if racourci in oyak.ProduitsFournisseurs.keys():
             oyak.ProduitsFournisseurs[racourci].append(fournisseur)
         else:
             oyak.ProduitsFournisseurs[racourci]=[fournisseur]
         oyak.ProduitsCodes[racourci, fournisseur]=code
         oyak.Produits[code]=(libele, prix, racourci, prix_plancher, poids, fournisseur)
         return 1

    def listePrepare(self):
        self.liste=oyak.ProduitsRacourcis.keys()
        self.liste.sort()
        
    def go(self, event):
        try:
            clef=self.listbox.curselection()[0]
            (racourci, libelle)=self.clefs[int(clef)]
        except:
            return

        oyak.myFournisseur.ihmShow(self.facture, racourci)


    def action(self, event="fake"):
        self.listbox.delete(0, END)

        self.clefs={}
        i=0

        for racourci in self.liste:
            (libelle) = oyak.ProduitsRacourcis[racourci]
            libelle.lower()
            s="%04d-%s"%(racourci, libelle)
            c="%s"%racourci
            n=len(self.filtre)
            if string.lower(libelle[:n])==self.filtre or c.find(self.filtre)==0:
                self.listbox.insert(END, s)
                self.clefs[i]=(racourci, libelle)
                i=i+1
                if i==25:
                   self.listbox.update()
                
        self.listbox.focus_set()
        self.listbox.selection_set(0)


class chooseFournisseur(chooseXXX):

    def __init__(self, forceRecharge=0):
        chooseXXX.__init__(self, "fournisseurs", forceRecharge)
        
    def ihmShow(self, facture, racourci, all=0):
        self.facture=facture
        self.racourci=racourci
        self.all=all
        chooseXXX.ihmShow(self, "fournisseurs", killable=1)
        
    def initPanel(self):
        if self.all:
            self.fournisseurs = Fournisseurs.keys()
        else:   
            self.fournisseurs = oyak.ProduitsFournisseurs[self.racourci]
        self.filtreName="%s > "%oyak.ProduitsRacourcis[self.racourci]

    def collect(self, article):
        (societe, ville, clef, timestamp)=article
        oyak.Fournisseurs[clef]=(societe, ville, clef)
        return 1
    
    def go(self, event):
        try:
          clef=self.listbox.curselection()[0]
          choix=self.clefs[int(clef)]
        except:
          return  

        (societe, ville, clef) = choix
        if clef==0: # selection de tous les fournisseurs
            self.ihmShow(self.facture, self.racourci, all=1)
        else:                
            self.facture.acceptProduit(self.racourci, clef, autre_fournisseur=self.all)

    def action(self, event="fake"):
        self.listbox.delete(0, END)

        self.clefs={}
        i=0
        liste=self.fournisseurs
        n=len(self.filtre)
        for code in liste:
            (societe, ville, clef)=oyak.Fournisseurs[code]
            s="%04d-%s"%(int(clef), societe)
            c="%d"%int(clef)
            n=len(self.filtre)
            if string.lower(societe[:n])==self.filtre or c.find(self.filtre)==0:
                self.listbox.insert(END, s)
                self.clefs[i]=(societe, ville, clef)
                i=i+1

	# ajout de 'TOUS'
        self.listbox.insert(END, "TOUS LES FOURNISSEURS")
        self.clefs[i]=("TOUS", "PARTOUT", 0)
				
                        
        self.listbox.focus_set()
        self.listbox.selection_set(0)



class chooseRelease(chooseXXX):

    def __init__(self, forceRecharge=0):
        chooseXXX.__init__(self, "releases")

    def ihmShow(self, facture, racourci, save=0):
        chooseXXX.ihmShow(self, "releases", killable=1)

    def panelInit(self):
        self.facture=facture
        self.save=save
        self.filtreName="Oyak Version > "

    def collect(self, article):
        (numero, filename)=article
        Releases[numero]=(numero, filename)

    def go(self, event):
        
        try:
          clef=self.listbox.curselection()[0]
          choix=self.clefs[int(clef)]
        except:
          oyak.ihm.returnPrevious()  

        (numero, filename) = choix
        oyak.ihm.messageShow("telechargement %s"%filename)
        loadRelease(filename, self.save)


    def action(self, event="fake"):
        self.listbox.delete(0, END)

        self.clefs={}
        i=0
        liste=Releases.keys()
        n=len(self.filtre)
        for code in liste:
            (numero, filename)=Releases[code]
            s="%s"%(filename)
            n=len(self.filtre)
            if filename.find(self.filtre)==0:
                self.listbox.insert(END, s)
                self.clefs[i]=(numero, filename)
                i=i+1
                
        self.listbox.focus_set()
#        self.listbox.selection_set(0)




###################################################################
#
#  Gestion de la mise a jour
#
###################################################################

def loadRelease(filename, save):
    global oyak
    
    if not(save):
        params = urllib.urlencode({'dwn': filename})
        try:
            f = urllib.urlopen(url_update_commande, params)
        except:
            oyak.ihm.showMessage("Le serveur Release ne répond pas!")
            return
        try:
          os.remove("\\Oyak\\%s"%filename)
        except:
          pass

        new=open("\\Oyak\\%s"%filename, "w")
        program=f.readlines()
        for l in program :
            new.write("%s\n"%l[:-1])
        new.close()
        try:
            shutil.copy("\\Oyak\\%s"%filename, "\\Windows\\Desktop\\%s"%filename)
        except:
            pass
    else:
        try:
            shutil.copy("\\Oyak\\%s"%filename, "\\Application\\Python\\vendeur.pyw")
            oyak.ihm.showMessage("Device Flashe avec %s"%filename)
        except:
            oyak.ihm.showMessage("Pb dans la mise a jour %s"%filename)
        

    





################################################################################
# Saisie nom Facture
################################################################################

class processFacture:
    global oyak
    
    def __init__(self, nb=0, client=0, check=0):
        self.nb=nb

        self.selectedCode={}
        self.selectedRacourci={}
        self.selectedFournisseur={}
        self.selectedDate={}
        self.selectedPrix={}
        self.selectedQuantite={}

        self.buttonQuantite=list()
        self.buttonProduit=list()
        self.buttonPrix=list()


        
        if self.nb==0 and client==0:
            self.vendeur=oyak.vendeurChoisi
            self.clefs={}
            myClient.ihmShow()

            ## chooseClient()
            return

        else:
            self.client=client
            (societe, ville, clef)=self.client
        

            self.nb=oyak.getNBfacture()
            oyak.factureCurrent=self.nb
            oyak.Factures[self.nb]=self
            
            self.root=oyak.ihm.factureCreate(self.nb)

            if oyak.zoomedWindow:
                oyak.ihm.wm_state(newstate="zoomed")
            
            (numero, nom, prenom)=oyak.vendeurChoisi
            self.vendeur_prenom=prenom
            self.vendeur_numero=numero

            self.ihmFacture()

            oyak.ihm.factureButton[self.nb, "annuler"]["command"]=self.annuler
            oyak.ihm.factureButton[self.nb, "envoyer"]["command"]=self.envoyer
        
            oyak.ihm.show("facture%d"%self.nb)
            self.goToArticle()

    def __del__(self):
        try:
            if self.nb>0:
                releaseNBfacture(self.nb)
                self.root.quit()
        except:
            pass
           
    def show(self):
        oyak.factureCurrent=self.nb
        oyak.ihm.show("facture%d"%self.nb)
        self.goToArticle()

    def annuler(self, send):
        oyak.ihm.showMessageOuiNon("Annuler la \n Facture?", siOui=oyak.ihm.delCurrentFacture)
        

    def addLabelEntry(self, s):
        sVar= StringVar()
        sVar.set(s)

        hVar= StringVar()
        hVar.set("---")

        label = Label(self.nameFrame, textvariable=sVar, fg="red")
        label.pack(side=TOP)

        f = Frame(self.inputFrame)
        f.pack(side=TOP)

        eVar=StringVar()
        
        e = Entry(f, fg="black",textvariable=eVar)
        e.pack(side=LEFT)
        
        button = Button(f, textvariable=hVar, fg="red")
        button["command"]=lambda x=1:self.labelEntryFocus(e, hVar, eVar)
        button.pack(side=LEFT)
        
        return (sVar, e, hVar, eVar)

    def labelEntryFocus(self, e, h, content):
        self.article_focus.set("---")
        self.fournisseur_focus.set("---")
        self.date_focus.set("---")
        self.quantite_focus.set("---")
        self.prix_focus.set("---")
        h.set("<<")
        e.focus_set()
        oyak.myCurrentAddChar=self.addcharFromKbd
        oyak.myCurrentDelChar=self.delcharFromKbd
        oyak.myCurrentEnterChar=0
        oyak.myCurrentEntry=content

    def addcharFromKbd(self, char):
        valeur=oyak.myCurrentEntry.get()+char
        oyak.myCurrentEntry.set(valeur) 
        
    def delcharFromKbd(self,char):
        valeur=oyak.myCurrentEntry.get()
        oyak.myCurrentEntry.set(valeur[:-1]) 
        
    def ihmFacture(self):
               
        # division de la fenetre en trois
        
        self.clientFrame = Frame(self.root)
        self.clientFrame.pack(side=TOP)
        
        self.prixFrame = Frame(self.root)
        self.prixFrame.pack(side=TOP)

        self.ligneFrame = Frame(self.root)
        self.ligneFrame.pack(side=TOP, expand=1, fill=BOTH)

        self.nameFrame = Frame(self.prixFrame)
        self.nameFrame.pack(side=LEFT)

        self.inputFrame = Frame(self.prixFrame)
        self.inputFrame.pack(side=LEFT)

        
        self.listFrame = Frame(self.root)
        self.listFrame.pack(side=TOP, expand=1, fill=BOTH)


        (societe, ville, clef)=self.client
        self.clientClef=clef

        # rappel nom client
        label = Label(self.clientFrame,
                      text="%s>%s"%(self.vendeur_prenom, societe), justify="center", fg="red", width=36)
        label.pack(side=TOP)

        # quantite, prix, article, fournisseur, date

        self.article_label, self.article, self.article_focus, self.article_content = self.addLabelEntry("Article:")
        self.fournisseur_label, self.fournisseur, self.fournisseur_focus, self.fournisseur_content = self.addLabelEntry("Fournisseur:")
        self.date_label, self.date, self.date_focus, self.date_content = self.addLabelEntry("Date:")
        self.quantite_label, self.quantite, self.quantite_focus, self.quantite_content = self.addLabelEntry("Quantite:")
        self.prix_label, self.prix, self.prix_focus, self.prix_content = self.addLabelEntry("Prix:")

        # action sur les lignes

        b=Button(self.ligneFrame, text='copier', command=lambda x=1:self.addFacture(operation='copie'))
        b.pack(side=LEFT, expand=1, fill=BOTH)
        
        b=Button(self.ligneFrame, text='effacer', command=lambda x=1:self.addFacture(operation='supression'))
        b.pack(side=LEFT, expand=1, fill=BOTH)
        
        self.valider=Button(self.ligneFrame, text='Valider', command=lambda x=1:self.addFacture())
        self.valider.bind("<Return>", lambda x="fake":self.valider.invoke())
        self.valider.pack(side=LEFT, expand=1, fill=BOTH)
        

        # liste box

        scrollbar = Scrollbar(self.listFrame)
        scrollbar.pack(side=RIGHT, expand=0, fill=BOTH)

        self.quantiteListFrame = Frame(self.listFrame)
        self.quantiteListFrame.pack(side=LEFT, expand=1, fill=BOTH)

        self.produitListFrame = Frame(self.listFrame)
        self.produitListFrame.pack(side=LEFT, expand=1, fill=BOTH)

        self.prixListFrame = Frame(self.listFrame)
        self.prixListFrame.pack(side=LEFT, expand=1, fill=BOTH)



#        self.listbox = Listbox(self.listFrame, yscrollcommand=scrollbar.set)
#        self.listbox.pack(side=LEFT, expand=1, fill=BOTH)
#        scrollbar.config(command=self.listbox.yview)

        # Bindings...

        self.goToArticle()
        self.article.bind(".", self.processProduit)
        
        self.article.bind("<Return>", self.route)
        self.date.bind("<Return>", self.goToQuantite)
        self.quantite.bind("<Return>", self.goToPrice)
        self.prix.bind("<Return>", lambda x=1:self.valider.focus_set())

        self.ajouteLigneFacture("Quant.", "Produit", "Prix")
#        self.listbox.delete(0,END)
#        self.listbox.insert(END, enteteFact)
        self.nbArticles=0
        self.currentArticle=0
        
        self.selectedCode[self.currentArticle]=""
        self.selectedRacourci[self.currentArticle]=""
        self.selectedFournisseur[self.currentArticle]=""
        self.selectedDate[self.currentArticle]=""
        self.selectedQuantite[self.currentArticle]=""
        self.selectedPrix[self.currentArticle]=""



    def processProduit(self, event):
                
        valeur=self.article.get()
        self.article.delete(0, END)
        oyak.myProduit.ihmShow(self, valeur)


    def acceptProduit(self, racourci, fournisseur, autre_fournisseur=0):
        self.autre_fournisseur=autre_fournisseur
        
        try:
          # que se passe-t-il si on vire la fenetre de facturation qui
          # a appelé??
          self.article.delete(0, END)
          self.fournisseur.delete(0, END)
          self.prix.delete(0, END)
        except:
          return
            
        oyak.ihm.show("facture%d"%self.nb, title="Oyak? Facture ")

        # le produit selectionne a un code barre
        if (racourci, fournisseur) in oyak.ProduitsCodes.keys():
            code = oyak.ProduitsCodes[racourci, fournisseur]
            (libelle, prix, racourci, prix_plancher, poids, fournisseur)=oyak.Produits[code]

        # le fournisseur est forcé par un appel a autre fournisseur
        if autre_fournisseur:
            code = 00
            (libelle, prix, prix_plancher, poids)=(oyak.ProduitsRacourcis[racourci], "0", "0", "0")
            

        if (racourci, fournisseur) in oyak.ProduitsCodes.keys() or autre_fournisseur:

            (societe, ville, clef)=oyak.Fournisseurs[fournisseur]
            self.fournisseur.insert(END, societe)
            self.fournisseur_label.set("Fournisseur : %s"%fournisseur)
              
            self.article.insert(END, libelle)
            self.article_label.set("Article : %d"%racourci)
      
            self.quantite_label.set("Quantite : ("+"%6.2f"%(eval(poids)+0.00)+")")
            self.prix_label.set("Prix : ("+"%6.2f"%(eval(prix)+0.00)+")")
            self.prix_default=prix
            self.prix_plancher=prix_plancher
            self.poids=poids
            self.produit=code

            self.selectedCode[self.currentArticle]=code
            self.selectedRacourci[self.currentArticle]=racourci
            self.selectedFournisseur[self.currentArticle]=fournisseur    

            self.goToDate()
        else:
            oyak.ihm.showMessage("Article a part numero %s fournisseur %s", racourci, fournisseur)
                
    def deleteCode(self, event):
        self.article.delete(0, END)
        self.article_label.set("Article :")
        self.fournisseur.delete(0, END)
        self.fournisseur_label.set("Fournisseur :")
        self.date.delete(0, END)
        self.prix.delete(0, END)
        self.prix_label.set("Prix :")
        self.quantite.delete(0, END)
        self.goToArticle()

    def goToArticle(self, event="fake"):
        oyak.ihm.show("facture%d"%self.nb, title="Oyak? Facture ")
        self.labelEntryFocus(self.article, self.article_focus,self.article_content)


    def goToFournisseur(self, event="fake"):
        self.labelEntryFocus(self.fournisseur, self.fournisseur_focus,self.fournisseur_content)


    def goToPrice(self, event="fake"):
        oyak.ihm.show("facture%d"%self.nb, title="Oyak? Facture ")
        self.labelEntryFocus(self.prix, self.prix_focus,self.prix_content)

    def goToQuantite(self, event="fake"):
        self.labelEntryFocus(self.quantite, self.quantite_focus,self.quantite_content)

    def goToDate(self, event="fake"):
        self.labelEntryFocus(self.date, self.date_focus,self.date_content)

    def addFacture(self, operation="create"):

        try :
          self.prix_saisi=self.prix.get()
          if len(self.prix_saisi)==0:
                self.prix_saisi=self.prix_default
          if (eval(self.prix_saisi)+0.0)<eval(self.prix_plancher)+0.:
            oyak.ihm.showMessageOuiNon("le prix %s est inferieur au prix plancher %6.2f! \n Entrée valide?"%(self.prix_saisi, (eval(self.prix_plancher)+0.00)),
                           siOui=self.ajouteArticle, siNon=self.goToPrice)
            return
        except:
            self.prix.delete(0, END)
            oyak.ihm.showMessage("le prix "+self.prix_saisi+" n'est pas reconnu", self.goToPrice)
            return
        self.ajouteArticle(operation)


    def ajouteLigneFacture(self, quantite, produit, prix, ligne=-1):

        if ligne==-1:
            l=Label(self.quantiteListFrame, text=quantite)
            l.pack(side=TOP)
            l=Label(self.produitListFrame, text=produit)
            l.pack(side=TOP)
            l=Label(self.prixListFrame, text=prix)
            l.pack(side=TOP)
        else:
            if ligne==self.nbArticles:
                l=Button(self.quantiteListFrame, text=quantite,
                         command=lambda x=1:self.getArticle(ligne, "quantite")) 
                self.buttonQuantite.append(l)
                l.pack(side=TOP, expand=1, fill=BOTH)
                l=Button(self.produitListFrame, text=produit,
                         command=lambda x=1:self.getArticle(ligne, "produit"))
                self.buttonProduit.append(l)
                l.pack(side=TOP, expand=1, fill=BOTH)
                l=Button(self.prixListFrame, text=prix,
                         command=lambda x=1:self.getArticle(ligne, "prix"))
                self.buttonPrix.append(l)
                l.pack(side=TOP, expand=1, fill=BOTH)
            else:
                self.buttonQuantite[ligne].config(text=quantite)
                self.buttonProduit[ligne].config(text=produit)
                self.buttonPrix[ligne].config(text=prix)


            
    def getArticle(self, ligne, focus):
        self.currentArticle=ligne
        self.acceptProduit(self.selectedRacourci[ligne], self.selectedFournisseur[ligne])
        if focus=="quantite":
            self.goToQuantite()
        if focus=="produit":
            self.goToArticle()
        if focus=="prix":
            self.goToPrice()
        return


    def ajouteArticle(self, operation='creation'):
        oyak.ihm.show("facture%d"%self.nb, title="Oyak? Facture ")
        quantite=self.quantite.get()
        if len(quantite)==0:
                quantite=self.poids

        article=self.article.get()
        if operation=='copie':
            self.currentArticle=self.nbArticles
        
#        try :
#          #self.listbox.insert(END, formatFact%(float(quantite),article,float(self.prix_saisi)))
        self.ajouteLigneFacture(quantite, article, float(self.prix_saisi), self.currentArticle)
#        except :
#            self.deleteCode("fake")

        self.selectedPrix[self.currentArticle]=self.prix_saisi
        self.selectedQuantite[self.currentArticle]=quantite
        self.selectedDate[self.currentArticle]=self.date.get()

        if self.nbArticles==self.currentArticle:
            self.nbArticles=self.nbArticles+1
        self.currentArticle=self.nbArticles

        self.selectedCode[self.currentArticle]=""
        self.selectedRacourci[self.currentArticle]=""
        self.selectedFournisseur[self.currentArticle]=""
        self.selectedDate[self.currentArticle]=""
        self.selectedQuantite[self.currentArticle]=""
        self.selectedPrix[self.currentArticle]=""

        self.deleteCode("fake")

    def neRienFaire(self):
        return
    
    def envoyer(self, parametre=""):

        oyak.ihm.showMessage("Traitement Commande en  cours ", self.neRienFaire)
        if self.nbArticles==0:
              self.article.delete(0, END)
              oyak.ihm.showMessage("La commande est vide!!!", self.goToArticle)
              return            

        s="%s%s"%(self.clientClef, sep1)
        for l in range(0, self.nbArticles):
             s=s+"%s%s"%(self.selectedCode[l], sep2)
             s=s+"%s%s"%(self.selectedRacourci[l], sep2)
             s=s+"%s%s"%(self.selectedFournisseur[l], sep2)
             s=s+"%s%s"%(self.selectedDate[l], sep2)
             s=s+"%s%s"%(self.selectedQuantite[l], sep2)
             s=s+"%s%s"%(self.selectedPrix[l], sep2)
             s=s+"*%s%s"%(parametre, sep1)
        params = urllib.urlencode({'vendeur': self.vendeur_numero, 'commande':s})
        try:
            f = urllib.urlopen(url_send_commande, params)
        except:
            oyak.ihm.showMessage("Le serveur ne répond pas!", self.goToArticle)
            return
        ack=f.readlines()
        ok=ack[0]
        if (ok[0]=="0"):
            oyak.ihm.showMessage("Commande %s!"%ok[2:], oyak.ihm.delCurrentFacture)
        else:
            oyak.ihm.showMessage("Commande perdue!", oyak.ihm.delCurrentFacture)
            return
            
    
    def route(self, event):
       
        racourci=self.article.get()
        if len(racourci)==0:
            oyak.ihm.showMessage("Article vide!", self.goToArticle)
            return
        if racourci in oyak.Produits.keys():
            (libelle, prix, racourci, prix_plancher, poids, fournisseur)=oyak.Produits[racourci]
            self.acceptProduit(racourci, fournisseur)
            return
        fournisseur=self.fournisseur.get()
        if racourci=="e" or fournisseur=="e":
            l=self.listbox.size()
            if l>1:
                self.listbox.delete(l-1, l)
                self.nbArticles=self.nbArticles-1
            self.deleteCode("fake")
            return
        # * ->  La commande est envoye
        if racourci[0]=="*" :
            self.envoyer(racourci[1:])
            return
        # * ou x ->  on tue la facture courrante
        if racourci=="x" or fournisseur=="x":
            self.annuler()
            return
        if racourci=="DDD" or racourci=="ddd":
            oyak.ihm.showMessage("Telechargement du serveur")
            lisData(clearAll=1, forceRecharge=1)
            self.article.delete(0, END)
            oyak.ihm.showMessage("OK...", self.goToArticle)
            return
        if racourci=="vvv" or racourci=="vvv":
            chooseRelease(self, racourci)
            return
        if racourci=="sss" or racourci=="sss":
            chooseRelease(self, racourci, save=1)
            return
        # sinon on process le couple (racourci,fournisseur)
        try :
            racourci=int(racourci)
        except:
            self.article.delete(0, END)
            oyak.ihm.showMessage("%s n'est pas un code reconnu!"%racourci, self.goToArticle)
            return
        if racourci in oyak.ProduitsRacourcis.keys() and len(fournisseur)==0:
            myFournisseur.ihmShow(self, racourci)
        else:
            self.article.delete(0, END)
            oyak.ihm.showMessage("%d n'est pas un code reconnu!"%racourci, self.goToArticle)



        
def run():
    global oyak

    oyak.ihm = ihmRoot()
    oyak.ihm.start()

if __name__ == "__main__":
    oyak = singleton()
    if oyak.cible:
        try:
            run()
        except:
             f=open('\Oyak\except.out', "w")
             f.write("Exception in user code:\n")
             f.write('-'*60)
             traceback.print_exc(file=f)
             f.write('-'*60)
             f.close()
             if oyak.ihm:
                 oyak.ihm.showMessage("Une Erreur est survenue!")
    else:
        run()
