# -*- coding: cp1252 -*-

#  codebarre
#     aaafffddddddn
#  a article   f : fournisseur,   d  = date,  n = code
#  cadrage a gauche pour a et f
#
from Tkinter import *
import os
import shutil
import string
import traceback
import urllib
import logging
import logging.handlers
import time
import getopt

vendeur_version="0.48"

ROOT_PATH = os.path.dirname(__file__)


if sys.platform.startswith("linux"):
    TMPDIR="/tmp"
else:
    TMPDIR="c:"

dir_Root=TMPDIR+'/Oyak/'
dir_Commande=TMPDIR+'/ventesjours/'
commande_counter_file="%s/%s" % (dir_Commande,"counter.txt")
commande_counter=0
catalog_filename = "catalogue.Zbar"
dir_impTODO=TMPDIR+"/impprint"
        
for d in [dir_Root,dir_Commande,dir_impTODO]:
  if not(os.path.exists(d)):
    os.mkdir(d)

# get counter value
if not(os.path.exists(commande_counter_file)):
    f = open(commande_counter_file,'w')
    f.write("%d" % commande_counter)
    f.close()

f = open(commande_counter_file,'r')
scommande_counter=f.readlines()
print scommande_counter
commande_counter = int(scommande_counter[0])
f.close()    
      
# set log file
logger = logging.getLogger('oyak_device.log')
logger.propagate = 0
logger.setLevel(logging.INFO)
log_file_name = "%s/" % dir_Root+"oyak_device.log"
open(log_file_name, "a").close()
handler = logging.handlers.RotatingFileHandler(
     log_file_name, maxBytes = 20000000,  backupCount = 5)
formatter = logging.Formatter("%(asctime)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

loggerror = logging.getLogger('oyak_err_device.log')
loggerror.propagate = 0
loggerror.setLevel(logging.DEBUG)
log_file_name = "%s/" % dir_Root+"oyak_err_device.log"
open(log_file_name, "a").close()
handler = logging.handlers.RotatingFileHandler(
     log_file_name, maxBytes = 20000000,  backupCount = 5)
handler.setFormatter(formatter)
loggerror.addHandler(handler)


dump_exception_at_screen = True
TEST = False
TEST_PROD = '9000533031510'

def dump_exception(where,fic_contents_initial=0):


    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
    if dump_exception_at_screen:
      traceback.print_exception(exceptionType,exceptionValue, exceptionTraceback,\
                                file=sys.stdout)
    print '!!!! Erreur in %s check error log file!!!'
    logger.info('!!!! Erreur in %s check error log file!!!' % where)
    loggerror.error('Erreur in %s' % where, exc_info=True)
    if fic_contents_initial:
        loggerror.error("\n============ content of file ===========\n"+\
                        "\n".join(fic_contents_initial)+\
                        "========== end content of file =========\n")



def usage(message = None):
    """ helping message"""
    if message:
        print message
    print "  usage: \n \t python vendeur.py \
             \n\t\t[ --help ] \
             \n\t\t[ --test | --prod=<code_barre> ] \
           \n"  
    sys.exit(1)



#########################################################################
# command line parsing...
#########################################################################

def parse():
    """ parse the command line and set global _flags according to it """
    global TEST, TEST_PROD
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "tpc", 
                          ["test", "catalog", "prod="])
    except getopt.GetoptError, err:
        # print help information and exit:
        usage(err)
        signal(CRITICAL,"err")

    # first scan opf option to get prioritary one first
    # those who sets the state of the process
    # especially those only setting flags are expected here
    for option, argument in opts:
        if option in ("-h", "--help"):
            usage("")
        elif option in ("-t", "--test"):
            TEST=True
        elif option in ("-c", "--catalog"):
            TEST="cat"
        elif option in ("-p", "--prod"):
            TEST=True
            print argument
            if argument:
                TEST_PROD=argument
            else:
                TEST_PROD = '0030023456789'
        else:
            print "unhandled option %s" % option
            sys.exit(-1)




oyak=0


class singleton:
    
    def __init__(self):
        
        self.maxDigits=130
        self.cible=os.path.exists('\Platform')
        self.linux=os.path.exists('/etc/passwd')
        self.ip_serveur="77"
        self.version="%s (singleton/serveur=%s)"% (vendeur_version,self.ip_serveur)
        self.time_last_key=0
        self.isServeurInjoignable=0
        
        self.debugFile=0
        self.debugFileOpen=0
        self.debugFileName="c:\\Oyak\\debug.out"
        self.debugging=0
        
        self.notInterrogation=1  # switch saisie facture/mode interrogaation
        self.interrogateur=interrogateur()
        self.notMenuAdded=1
                
        if self.cible:
            self.zoomedWindow=1
            self.erreurCatch=0
            self.debugMessages=0
            self.raiseError=0
            self.website_address="http://192.168.111.%s/phpmyfactures"%self.ip_serveur
            self.fichierIp='\Platform\S24Profiles.reg'
            self.fichierIpBackup='/Oyak/S24old.reg'
            self.fichierIpNew='/Oyak/S24New.reg'
            self.fichierIpTemplate='/Application/Oyak/S24Profiles.reg'
            self.fichierAppTemplate='/Application/Oyak/Data/%s.bak'
            self.fichierAppOldTemplate='/Application/Oyak/Data/%s.old'
            self.fichierBackup_Template='\Oyak\%s.bak'
            self.fichierTemp_Template='\Oyak\%s.tmp'
            self.fichierOld_Template='\Oyak\%s.old'
        else:
            self.version="%s (singleton/serveur=%s)"%(vendeur_version,"localhost")
            self.erreurCatch=0
            self.debugMessages=1
            self.zoomedWindow=0
            self.raiseError=1
            if not(self.linux):
                self.website_address="http://127.0.0.1/phpmyfactures"
                self.root_address="c:/Program Files/EasyPHP1-8/www/phpmyfactures/device/a copier/"
                self.fichierBackup_Template='c:\Oyak\%s.bak'
                self.fichierTemp_Template='c:\Oyak\%s.tmp'
                self.fichierOld_Template='c:\Oyak\%s.old'
            else:
                self.website_address="http://claui2t0.der.edf.fr:8080/~samuel/phpmyfactures"
                self.root_address="/local00/users/samuel/public_html/phpmyfactures/device/a copier/"
                self.tmp_address="/local00/users/samuel/public_html/phpmyfactures/device/tmp"
                self.fichierBackup_Template=self.tmp_address+'/%s.bak'
                self.fichierTemp_Template=self.tmp_address+'/%s.tmp'
                self.fichierOld_Template=self.tmp_address+'/%s.old'
            self.root_address = ROOT_PATH+"../a copier/"
            self.fichierIp=self.root_address+"Platform/test/S24Profiles.reg"
            self.fichierIpBackup=self.root_address+"Platform/test/S24old.reg"
            self.fichierIpNew=self.root_address+"Platform/test/S24new.reg"
            self.fichierIpTemplate=self.root_address+"Application/Oyak/S24Profiles.reg"
            self.fichierAppTemplate=self.root_address+"Application/Oyak/Data/%s.bak"
            self.fichierAppOldTemplate=self.root_address+"Application/Oyak/Data/%s.old"
            self.fichierBackup_Template=dir_Root+'%s.bak'
            self.fichierTemp_Template=dir_Root+'%s.tmp'
            self.fichierOld_Template=dir_Root+'%s.old'       

        self.myVendeur=0
        self.myClient=0;
        self.myFournisseur=0
        self.myProduit=0
        
        self.Produits={}
        self.ProduitsDetail={}
        self.ProduitsRacourcis={}
        self.ProduitsCodes={}
        self.Clients={}
        self.Vendeurs={}
        self.Fournisseurs={}
        self.Factures={}
        self.clientNB = {}
        self.timestamp = {}
        
        for i in range(10):
            self.clientNB[i]=0
            
        self.clefsClients=list()
        self.nbChamps = {"vendeurs":2, "fournisseurs":2, "clients":2,
                    "produits":6}
        self.isAlreadyPaneled = {"vendeurs":0, "fournisseurs":0, "clients":0,
                "produits":0}
        self.barSize = {"vendeurs":0.1, "fournisseurs":0.9, "clients":0.3,
                     "produits":0.6}
        
        self.formatFact="%5.2f|%15s|%5.2f"
        self.enteteFact="%5s|%15s|%5s"%("quant", "produit", "prix")
        
        
        
        self.url_send_commande=self.website_address+"/query/index.php?"
        self.url_update_commande=self.website_address+"/query/download.php?"
        self.url_interroge=self.website_address+"/query/interroge.php?"
        
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
    
    def writeDebug(self,ligne):
        if self.debugMessages:
            if self.debugFileOpen==0:
                self.debugFile=open(self.debugFileName, "w")
                self.debugFileOpen=1
            self.debugFile.write(ligne+"\n")
            self.debugFile.flush()
            

###############################################################################################
# Gestion rationalisée de l'IHM
###############################################################################################


class ihmRoot:
    
    global oyak

    def __init__(self):
       self.ihm=Tk()
       
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
       
       self.Xmax=38
       self.Ymax=24

       self.ihm.rowconfigure(0, weight=1)
       self.ihm.columnconfigure(0, weight=1)
       #self.ihm.master.grid(sticky=W+E+N+S)
       
       self.messagePanelCreate()
       self.messageOuiNonPanelCreate()

       self.progressBarCreate()
       self.menuCreate()
       self.adminCreate()
       self.ipCreate()
       self.interrogationCreate()

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
        self.add(panelName, "en cours", label, 3, 0)

        label = Button(self.ihm, text="Nouvelle Facture", command=processFacture, height=4, width=self.Xmax)
        self.add(panelName, "autre", label, 4, 0)

        label = Button(self.ihm, text="Choisir Vendeur", command=self.changeVendeur, height=3, width=self.Xmax)
        self.add(panelName, "vendeur", label, 5, 0)

        label = Button(self.ihm, text="Relire Donnee", command=self.rechargeBase, height=3, width=self.Xmax)
        self.add(panelName, "reloader", label, 6, 0)
        
        label = Button(self.ihm, text="Imprimer catalogue", command=self.imprimeCatalogue, height=3, width=self.Xmax)
        self.add(panelName, "catalogue", label, 5, 0)

        
#        label = Button(self.ihm, text="Reglages", command=self.showIp,height=4,width=self.Xmax)
#        self.add(panelName,"update",label,8,0)

#        label = Button(self.ihm, text="Reactiver Scanner", command=self.scanner,height=4,width=self.Xmax)
#        self.add(panelName,"scanner",label,9,0)


        label = Button(self.ihm, text="QUITTER", command=self.ihm.quit, height=4, width=self.Xmax)
        self.add(panelName, "quitter", label, 10, 0)

         
#        label = Button(self.ihm, text="Administrer", command=self.showAdmin,height=5,width=self.Xmax)
#        self.add(panelName,"admin",label,10,0)


    def addMenuInterrogation(self):
        panelName = "menu"   
        label = Button(self.ihm, text="Interrogation", command=self.showInterrogation, height=3, width=self.Xmax)
        self.add(panelName, "interroger", label, 2, 0)
        self.notMenuAdded=0

    # creation fenetre type Menu
    
    def adminCreate(self):

        panelName = "admin"
        
        label = Button(self.ihm, text="Retour", command=self.returnPrevious, height=3, width=self.Xmax)
        self.add(panelName, "retour", label, 2, 0)

        label = Button(self.ihm, text="Relire Donnée", command=self.rechargeBase, height=4, width=self.Xmax)
        self.add(panelName, "reloader", label, 6, 0)
        
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

    def interrogationCreate(self):

        panelName = "interrogation"
        
        label = Button(self.ihm, text="Retour", command=oyak.interrogateur.close, height=3, width=self.Xmax)
        self.add(panelName, "retour", label, 1, 0)

        label = Button(self.ihm, text="info Client", 
                       command=lambda x='client':oyak.interrogateur.compose(x), height=4, width=self.Xmax)
        self.add(panelName, "Client", label, 2, 0)

        label = Button(self.ihm, text="info Produit", 
                       command=lambda x='produit':oyak.interrogateur.compose(x), height=4, width=self.Xmax)
        self.add(panelName, "produit", label, 3, 0)

        label = Button(self.ihm, text="info Fournisseur", 
                       command=lambda x='fournisseur':oyak.interrogateur.compose(x), height=4, width=self.Xmax)
        self.add(panelName, "Fournisseur", label, 4, 0)

        label = Button(self.ihm, text="info Vendeur", 
                       command=lambda x='vendeur':oyak.interrogateur.compose(x), height=4, width=self.Xmax)
        self.add(panelName, "Vendeur", label, 5, 0)

        
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

    def showInterrogation(self):
        self.show("interrogation")

    def testReseau(self):
        os.system('\windows\nictt.exe')

    def scanner(self):
        os.system('\windows\startup\scanwedge.exe')


    def imprimeCatalogue(self):
        global dir_impTODO, catalog_filename

        f=open(catalog_filename,"w")
        for p in oyak.Produits.keys():
            (clef,libelle,fournisseur,\
             code_barre,pds,prx,\
             pch) = oyak.ProduitsDetail[p]
            try:
                if int(fournisseur) in oyak.Fournisseurs.keys():
                    f.write("%s!%s!%s\n" % \
                            (code_barre,libelle,oyak.Fournisseurs[int(fournisseur)]))
            except:
                dump_exception("imprimeCatalogue")
                print "not cataloguing product : ", oyak.ProduitsDetail[p]
                sys.exit(-2)
        f.close()
        print "Catalogue input file done..."
        shutil.copy(catalog_filename,"%s/%s" % (dir_impTODO,catalog_filename))

    # creation fenetre type Facture
    
    def factureCreate(self, num):

        what="%d"%num
        panelName = "facture"+what
        
        # Menu
        frame = Frame(self.ihm)
        self.add(panelName, "menu", frame, 0, 0, colspan=5)
        label = Button(frame, text="MENU", command=self.showMenu, height=2)
        label.pack(side=LEFT, expand=1, fill=X)
        
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
        self.ihm.mainloop()

    def facturePrevious(self):
        
        nbPrevious=oyak.factureCurrent-1

        while nbPrevious>=0:
            if oyak.clientNB[nbPrevious]>0:
                oyak.Factures[nbPrevious].show()
                return 
            nbPrevious = nbPrevious-1

        self.showMessage("Pas d'autre\nFacture!!!")

    def factureNext(self):
        nbNext=oyak.factureCurrent+1

        while nbNext<10:
            if oyak.clientNB[nbNext]>0:
                oyak.Factures[nbNext].show()
                return 
            nbNext = nbNext+1

        self.showMessage("Pas d'autre\nFacture!!!")

    def showFactureFirst(self, menu=0):
        i=oyak.getFirstFacture()
        if  i<0 and menu==0:
            self.factureNew()
        else:
            if i<0:
                oyak.myClient.ihmShow()
            else:
                oyak.Factures[i].show()

    def factureNew(self):
        self.showMessageOuiNon("Demarrer une \nautre Facture?", siOui=processFacture)

    def delCurrentFacture(self):
        oyak.releaseNBfacture(oyak.factureCurrent)
        self.showFactureFirst(menu=1)

    def lectureDonnee(self):
        lisData(clearAll=1)
        oyak.myVendeur.ihmShow()

    def rechargeBase(self):
        self.showMessage("Telechargement du serveur")
        lisData(clearAll=1, forceRecharge=1)
        self.showMessage("OK...", self.showMenu)

    def changeVendeur(self):
        oyak.myVendeur.ihmShow()

    def interroge(self,what):
        i=interrogateur(what)

class interrogateur:
    global oyak
    
    def __init__(self):
        self.alreadyInit=0
        pass
    
    def check(self):
        if not(self.alreadyInit):
            self.facture=processFacture()
            self.alreadyInit=1
            
    def compose(self,what):
        #self.check()
        oyak.notInterrogation=0
        if what=="client":
            oyak.myClient.ihmShow()
        if what=="produit":
            self.client=("choix", "", "")
            oyak.myProduit.ihmShow(self, "")            
        if what=="fournisseur":
            oyak.myFournisseur.ihmShow(self, "", all=1)
        if what=="vendeur":
            oyak.myVendeur.ihmShow()

    def ask(self,vendeur=0,client=0,produit=0,fournisseur=0):
        #interrogation du serveur
        if oyak.debugMessages:
            print "interrogation.... vendeur=%s,client=%s,produit=%s,fournisseur=%s"%(vendeur,client,produit,fournisseur)
        s="%s%s%s%s%s%s%s"%(vendeur, oyak.sep1,client, oyak.sep1,produit, oyak.sep1,fournisseur)
        params = urllib.urlencode({'requete': s})
        try:
            f = urllib.urlopen(oyak.url_interroge, params)
        except:
            oyak.ihm.showMessage("Le serveur ne répond pas!", self.goToArticle)
            oyak.ihm.showMessage("Le serveur ne répond pas! \n url=%s \n v=%s \n s=%s"%
                                 (oyak.url_send_commande,self.vendeur_numero,s), 
                                 self.goToArticle)
            oyak.writeDebug("?vendeur=1&params="+s)
            return
        ack=f.readlines()
        ok=ack[0]
        if (ok[0]=="0"):
            if oyak.debugMessages:
                print ok[2:]
            s=string.replace(ok[2:], "!","\n")
            oyak.ihm.showMessage("%s"%s, oyak.ihm.showInterrogation)
        else:
            oyak.ihm.showMessage("Echec de l'interrogation!", oyak.ihm.showInterrogation)
       
    def close(self):
        oyak.notInterrogation=1
        oyak.ihm.showFactureFirst()
        
###################################################################
#
#  Lectures des datas
#
###################################################################

        
class lisData:

    global oyak, TEST
    
    def __init__(self, clearAll=0, forceRecharge=0):
  
        oyak.ihm.updateProgressBar("Chargement Data", 0.)

        self.forceRecharge=forceRecharge
        self.clearAll=clearAll
        
        if clearAll:
            Produits={}
            ProduitsDetail={}
            ProduitsRacourcis={}
            ProduitsCodes={}
            Clients={}
            Vendeurs={}
            Fournisseurs={}
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
            
        # creation d'un fichier test si on est sous linux
        if sys.platform.startswith("linux"):
            print "do something for linux!!!!!!!!"
            copying  = "cat '../../data/%s.txt' | awk '{clef=$1; $1=\"\"; printf(\"%%s!%%s=\", clef,$0);}' > '%s'" % \
                (what,self.fichierBackup)
            copying  = "cp '../../data/%s.txt' '%s'" % \
                (what,self.fichierBackup)
            print copying
            os.system(copying)
        else:
            print "do something for windows!!!!!!!!"
            copying  = "copy 'c:datadevice/%s.txt' '%s'" % \
                (what,self.fichierBackup)
            print copying
            shutil.copy('/datadevice/%s.txt'%what,self.fichierBackup)

        # lecture sur fichier backup d'abord
        if not(forceRecharge) and self.readFromBackup()==0:
            if oyak.debugMessages:
                print "lecture from Backup pour %s a %d Articles" % (what,lengthArticle)
            self.readSource(lengthArticle)
            self.closeSource()
        # lecture depuis la base
        else:
            if oyak.debugMessages:
                print "lecture from web pour %s  a %d Articles" % (what,lengthArticle)

            isThere=os.path.exists(self.fichierBackup)
            if isThere:
               os.unlink(self.fichierBackup)
            self.tmpFile = open(self.fichierTemp, "w")
            self.urlName=oyak.url_get_Template%what

            if self.readFromUrl()==0:
                self.readSource(lengthArticle)
                self.closeSource()

        # sauvegarde sur la device des données
            self.tmpFile.close()
            self.fichierOld=oyak.fichierOld_Template%what
            try :
                os.rename(self.fichierTemp, self.fichierBackup)

                # recopie dans la zone permanente
                shutil.copy(self.fichierBackup, oyak.fichierAppTemplate%what)
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
        oyak.ihm.add(panelName0, "menu", frame, 0, 0, colspan=2)
        label = Button(frame, text="MENU", command=oyak.ihm.showMenu, height=2)
        label.pack(side=LEFT, expand=1, fill=X)
        #label.pack(side=LEFT, expand=1, fill=BOTH)
        
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
        self.create_backup=1

        if not(oyak.isServeurInjoignable):
            try:
                self.origFileh = urllib.urlopen(self.urlName)
                return 0
            except:
                oyak.ihm.showMessage("Solveur injoignable\n Impossibe de télécharger les data du serveur \n Repli sur Backup")
                oyak.isServeurInjoignable=1
        return -1 
            
    def readFromBackup(self):
        self.create_backup=0
        
        try :
            self.origFileh = open(self.fichierBackup)
            return 0
        except :
            return -1     

            
    def readSource(self, lengthArticle):
        printMessageNotYet = True

        self.fileList = self.origFileh.readlines()
        self.nbArticles=0
        for l in self.fileList:
            if self.create_backup:
                self.tmpFile.write(l)
            articles=string.split(l, "=")
            for a in articles:
                article=string.split(a, "!")
                if len(article)>lengthArticle :
                    if oyak.debugMessages and printMessageNotYet:
                        print "reading ",article
                        print "expecting %s fields " % (lengthArticle)
                        print "Truncating...."
                        print
                        printMessageNotYet = False
                    article = article[:lengthArticle]
                if len(article)<lengthArticle :
                    if oyak.debugMessages and printMessageNotYet:
                        print "reading ",article
                        print "expecting %s fields " % (lengthArticle)
                        print "adding fake values for missing fields..."
                        print
                        printMessageNotYet = False
                    if False:
                        while (len(article)<lengthArticle):
                            article.append(self.default[len(article)-1])
                    else:
                        print "not collecting ",article
                        continue 
                                   
                if self.collect(article):
                    self.nbArticles+=1
                else:
                     if oyak.debugMessages and printMessageNotYet:
                         print "article has not been collected ",article
                         printMessageNotYet = False


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
        self.setFiltre(self.filtre)
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
        self.default = [9999,"Prenom"]
        chooseXXX.__init__(self, "vendeurs", forceRecharge)

    def ihmShow(self):
        chooseXXX.ihmShow(self, "vendeurs")
        if TEST:
            oyak.vendeurChoisi=self.clefs[1]
            oyak.myClient.ihmShow()

    def collect(self, article):
        global Vendeurs
        (numero, prenom)=article
        oyak.Vendeurs[numero]=(numero, prenom)
        print article
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
        
        if oyak.notInterrogation:
            oyak.vendeurChoisi=choix
#            oyak.ihm.showMessage("preparation fenetre client")
            oyak.myClient.ihmShow()
        else:
            (num,nom,prenom)=choix
            oyak.interrogateur.ask(vendeur=num)

    def action(self, event="fake"):
        self.listbox.delete(0, END)


        self.clefs={}
        i=0
        liste=oyak.Vendeurs.keys()
        liste.sort(key=str.lower)
        for clef in liste:
               (numero, prenom) = oyak.Vendeurs[clef]
               prenom.lower()
               if string.lower(prenom[:len(self.filtre)])==self.filtre:
                   self.listbox.insert(END, "%s"%(prenom))
                   self.clefs[i]=(numero,prenom)
                   i=i+1
        oyak.ihm.show(self.what)
        self.listbox.focus_set()
        self.listbox.selection_set(0)


class chooseClient(chooseXXX):

    def __init__(self, forceRecharge=0):
        self.default = [999,"Societe"]
        chooseXXX.__init__(self, "clients", forceRecharge)
        
    def ihmShow(self):
        chooseXXX.ihmShow(self, "clients")
        if TEST:
            processFacture(client=2)


    def collect(self, article):
        (clef,societe)=article
        try:
            oyak.Clients[int(clef)]=societe
        except:
            print "rejeté : ",(clef,societe)
        return 1

    def listePrepare(self):
        clefsClients=oyak.Clients.keys()
        clefsClients.sort()#key=str.lower)

        i=0
        for clef in clefsClients:
            societe=oyak.Clients[clef]
            self.listbox0.insert(END, "%03d-%s"%(clef, societe))
            self.clefs0[i]=clef
            i=i+1
        #print self.listbox0

        pass

    def initPanel(self):
        self.clefs={}
        (numero, prenom)=oyak.vendeurChoisi
        self.filtreName="%s > "%prenom

    def go(self, event):
        global oyak
        try :
          if len(self.filtre)==0 and len(self.clefs0)>0:
              clef=self.listbox0.curselection()[0]
              choix=int(self.clefs0[int(clef)])
          else:
              clef=self.listbox.curselection()[0]
              choix=int(self.clefs[int(clef)])
        except:
            oyak.ihm.showMessage("Choix impossible!!!", self.action)
            return 0

        self.filtre=""
        self.setFiltre(self.filtre)
        
        if oyak.notInterrogation:        
            processFacture(client=choix)
        else:
            oyak.interrogateur.ask(client=choix)

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
            for clef in oyak.Clients.keys():
                societe=oyak.Clients[clef]
                sclef = "%04d" % clef
                if string.lower(sclef).find(self.filtre)>=0 or \
                       string.lower(societe).find(self.filtre)>=0:
                    self.listbox.insert(END, "%s-%s"%(sclef, societe))
                    self.clefs[i]=clef
                    i=i+1
            self.listbox.focus_set()
            self.listbox.selection_set(0)



class chooseProduit(chooseXXX):

    def __init__(self, forceRecharge=0):
        self.default = [ 9999,"xxxxxxx"]        
        chooseXXX.__init__(self, "produits", forceRecharge)


    def ihmShow(self, facture, valeur):
        self.liste0={}
        self.clefs0={}
        
        self.facture=facture
        self.valeur=valeur
        clef = facture.client
        societe = oyak.Clients[clef]
        self.filtreName="%s >"%societe
        chooseXXX.ihmShow(self, "produits", killable=1)
        
    def initPanel(self):
        self.filtre=self.valeur
        

    def collect(self, article):
         (clef, libelle, code_barre,pds,prx,pch)=article
         #print "%s]%s" % (code_barre,libele)
         try:
             oyak.Produits[int(clef)]=libelle
             code = "%s"%code_barre
             racourci = int(code[0:3])
             fournisseur = int(code[3:6])
             if len(code)>6:
                 other = int(code[6:])
             else:
                 other = ""
             oyak.ProduitsDetail[int(clef)] = \
                                            (clef,libelle,fournisseur,\
                                                 code_barre,pds,prx,\
                                                 pch)
             oyak.ProduitsDetail[int(code_barre)] = oyak.ProduitsDetail[int(clef)]
         except:
             dump_exception("collect")
             print  "did not take ",article
         return 1

    def listePrepare(self):
        self.liste=oyak.Produits.keys()
        self.liste.sort()
        
    def go(self, event):
        try:
            clef=self.listbox.curselection()[0]
            (numero,libelle)=self.clefs[int(clef)]
        except:
            dump_exception("client_go")
            return

        print numero,libelle
        oyak.Factures[oyak.factureCurrent].racourci=int(numero)
        self.facture.article.delete(0, END)
        self.facture.article.insert(END, libelle)
        self.facture.article_label.set("Article : %d"%numero)
        self.facture.article_clef = numero
        self.facture.goToFournisseur()

    def action(self, event="fake"):
        self.listbox.delete(0, END)

        self.clefs={}
        i=0

        for racourci in self.liste:
            libelle = oyak.Produits[racourci]
            s="%03d-%s"%(racourci, libelle)
            c="%s"%racourci
            l="%s"%libelle
            n=len(self.filtre)
            if string.lower(l).find(self.filtre)>=0 or \
                   string.lower(c).find(self.filtre)>=0:
                self.listbox.insert(END, s)
                self.clefs[i]=(racourci, libelle)
                i=i+1
                if i==25:
                   self.listbox.update()
                   
        self.listbox.focus_set()
        self.listbox.selection_set(0)


class chooseFournisseur(chooseXXX):

    def __init__(self, forceRecharge=0):
        self.default = [9999,"Societe"]
        chooseXXX.__init__(self, "fournisseurs", forceRecharge)
        
    def ihmShow(self, facture, racourci, all=0):
        print "fournisseur ihm_show (facture, racourci)=",(facture,racourci)
        self.facture=facture
        self.racourci=int(racourci)
        self.all=all
        if int(self.racourci)==0:
            self.facture.fournisseur.delete(0,END)
            self.facture.fournisseur_label.set("Fournisseur :")
            oyak.ihm.showMessage("Choisissez un article!",facture.goToArticle)
            return
        chooseXXX.ihmShow(self, "fournisseurs", killable=1)
        
    def initPanel(self):
        self.fournisseurs = oyak.Fournisseurs.keys()
        if oyak.notInterrogation:
            self.filtreName="%s > "%oyak.Produits[self.racourci]
        else:
            self.filtreName=" ???? >"
            
    def collect(self, article):
        (clef, societe)=article
        try:
            oyak.Fournisseurs[int(clef)]=societe
        except:
            print "did not take ",(clef,societe)
        return 1
    
    def go(self, event):
        try:
          clef=self.listbox.curselection()[0]
          choix=self.clefs[int(clef)]
        except:
          return  

        (societe,  clef) = choix
        if clef==0: # selection de tous les fournisseurs
            self.ihmShow(self.facture, self.racourci, all=1)
        else:               
            if oyak.notInterrogation:
                self.facture.acceptProduit(self.racourci, clef, autre_fournisseur=self.all)
            else:
                oyak.interrogateur.ask(produit=self.racourci,fournisseur=clef)

    def action(self, event="fake"):
        self.listbox.delete(0, END)

        self.clefs={}
        i=0
        liste=self.fournisseurs
        n=len(self.filtre)
        for clef in liste:
            societe=oyak.Fournisseurs[clef]
            s="%03d-%s"%(int(clef), societe)
            c="%d"%int(clef)
            if string.lower(societe).find(self.filtre)>=0 or \
                     string.lower(c).find(self.filtre)>=0:
                self.listbox.insert(END, s)
                self.clefs[i]=(societe,  clef)
                i=i+1

	# ajout de 'TOUS'
        self.listbox.insert(END, "TOUS LES FOURNISSEURS")
        self.clefs[i]=("TOUS", "PARTOUT", 0)
				
                        
        self.listbox.focus_set()
        self.listbox.selection_set(0)









################################################################################
# Saisie nom Facture
################################################################################

class processFacture:
    global oyak, commande_counter, TEST_PROD
    
    def __init__(self, nb=0, client=0, check=0):
        self.nb=nb

        self.selectedCode={}
        self.selectedRacourci={}
        self.selectedFournisseur={}
        self.selectedDate={}
        self.selectedPrix={}
        self.selectedColis={}
        self.selectedpoidsColis={}
        self.selectedQuantite={}

        self.buttonColis=list()
        self.buttonpoidsColis=list()
        self.buttonQuantite=list()
        self.buttonProduit=list()
        self.buttonPrix=list()
        self.buttonQuantiteContent=list()
        self.buttonProduitContent=list()
        self.buttonPrixContent=list()
        
        self.racourci=0


        
        if self.nb==0 and client==0 and oyak.notInterrogation:
            self.vendeur=oyak.vendeurChoisi
            self.clefs={}
            oyak.myClient.ihmShow()

            ## chooseClient()
            return

        else:
        
            if oyak.notMenuAdded:
                oyak.ihm.addMenuInterrogation()

            self.nb=oyak.getNBfacture()
            oyak.factureCurrent=self.nb
            oyak.Factures[self.nb]=self
            
            (numero, prenom)=oyak.vendeurChoisi
            self.vendeur_prenom=prenom
            self.vendeur_numero=numero
                
            if oyak.notInterrogation:
                self.client=client
                societe=oyak.Clients[self.client]
                
                self.root=oyak.ihm.factureCreate(self.nb)

                if oyak.zoomedWindow:
                     oyak.ihm.ihm.wm_state(newstate="zoomed")

                self.ihmFacture()
    
                oyak.ihm.factureButton[self.nb, "annuler"]["command"]=self.annuler
                oyak.ihm.factureButton[self.nb, "envoyer"]["command"]=self.envoyer
            
                oyak.ihm.show("facture%d"%self.nb)
                self.goToArticle()

    def __del__(self):
        try:
            if self.nb>0:
                oyak.releaseNBfacture(self.nb)
                self.root.quit()
        except:
            pass
           
    def show(self):
        oyak.factureCurrent=self.nb
        oyak.ihm.show("facture%d"%self.nb)
        self.goToArticle()

    def annuler(self):
        oyak.ihm.showMessageOuiNon("Annuler la \n Facture?", siOui=oyak.ihm.delCurrentFacture)
        

    def addLabelEntry(self, s, clickable=TRUE):
        sVar= StringVar()
        sVar.set(s)

        hVar= StringVar()
        hVar.set("---")

        if clickable:
            label = Button(self.nameFrame, textvariable=sVar, fg="red")
            label.pack(side=TOP,expand=1,fill=X)
        else:
            label = Label(self.nameFrame, textvariable=sVar, fg="red")
            label.pack(side=TOP,expand=1,fill=X)
            
        f = Frame(self.inputFrame)
        f.pack(side=TOP)

        eVar=StringVar()
    
        if clickable:
            e = Entry(f, fg="black",textvariable=eVar)
        else:
            e = Label(f, fg="black",textvariable=eVar)
        e.pack(side=LEFT)
        
            
        button = Button(f, textvariable=hVar, fg="red",width=5)
        if clickable:
            button["command"]=lambda x=1:self.labelEntryFocus(e, hVar, eVar)
            label["command"]=lambda x=1:self.labelEntryFocus(e, hVar, eVar)
            button.pack(side=LEFT)
        
        return (sVar, e, hVar, eVar)

    def labelEntryFocus(self, e, h, content):
        self.article_focus.set("---")
        self.fournisseur_focus.set("---")
        self.date_focus.set("---")
        self.colis_focus.set("---")
        self.poidsColis_focus.set("---")
        self.quantite_focus.set("---")
        self.prix_focus.set("---")
        h.set("<<")
        e.focus_set()
        e.select_range(0,len(e.get()))
                       
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

        

        clef=self.client
        societe=oyak.Clients[self.client]
                

        # rappel nom client
        label = Label(self.clientFrame,
                      text="%s>%s"%(self.vendeur_prenom, societe), justify="center", fg="red", width=36)
        label.pack(side=TOP)

        # quantite, prix, article, fournisseur, date

        self.article_label, self.article, self.article_focus, self.article_content = self.addLabelEntry("Article:")
        self.article_clef = 0
        self.fournisseur_label, self.fournisseur, self.fournisseur_focus, self.fournisseur_content = self.addLabelEntry("Fournisseur:")
        self.date_label, self.date, self.date_focus, self.date_content = self.addLabelEntry("Date:")
        self.colis_label, self.colis, self.colis_focus, self.colis_content = self.addLabelEntry("Colis:")
        self.poidsColis_label, self.poidsColis, self.poidsColis_focus, self.poidsColis_content = self.addLabelEntry("Poids:")
        self.quantite_label, self.quantite, self.quantite_focus, self.quantite_content = self.addLabelEntry("Quantite:")
        self.prix_label, self.prix, self.prix_focus, self.prix_content = self.addLabelEntry("Prix:")

        # action sur les lignes

        if oyak.debugging:
            b=Button(self.ligneFrame, text='remplir', command=lambda x=1:self.remplirFaccture())
            b.pack(side=LEFT, expand=1, fill=BOTH)

        b=Button(self.ligneFrame, text='effacer', command=lambda x=1:self.ajouteArticle(operation='supression'))
        b.pack(side=LEFT, expand=1, fill=BOTH)
        
        self.valider=Button(self.ligneFrame, text='Valider', command=lambda x=1:self.ajouteArticle('creation'))
        self.valider.bind("<Return>", lambda x="fake":self.valider.invoke())
        self.valider.pack(side=LEFT, expand=1, fill=BOTH)
        

        # liste box

        self.nbLignesVisibles=7

        self.listFrame = Frame(self.root)
        self.listFrame.pack(side=TOP, expand=1, fill=BOTH)

        scrollFrame = Frame(self.listFrame)
        scrollFrame.pack(side=RIGHT, expand=0, fill=BOTH)

        scrollUp=Button(scrollFrame, text='//',command=lambda x=1:self.scrollFacture(-self.nbLignesVisibles+1))
        scrollUp.pack(side=TOP, expand=1, fill=Y)
        scrollDown=Button(scrollFrame, text='//',command=lambda x=1:self.scrollFacture(+self.nbLignesVisibles-1))
        scrollDown.pack(side=TOP, expand=1, fill=Y)

        self.quantiteListFrame = Frame(self.listFrame)
        self.quantiteListFrame.pack(side=LEFT, expand=1, fill=BOTH)

        self.produitListFrame = Frame(self.listFrame)
        self.produitListFrame.pack(side=LEFT, expand=1, fill=BOTH)

        self.prixListFrame = Frame(self.listFrame)
        self.prixListFrame.pack(side=LEFT, expand=1, fill=BOTH)

        # label des colonnes
        l=Label(self.quantiteListFrame, text='Quantite')
        l.pack(side=TOP)
        l=Label(self.produitListFrame, text='Produit')
        l.pack(side=TOP)
        l=Label(self.prixListFrame, text='Prix')
        l.pack(side=TOP)

        # ajout de 4 ligne pre-remplies

        for ligne in range(self.nbLignesVisibles):
            l=Button(self.quantiteListFrame, text='---',
                     command=lambda x=ligne:self.getArticle(x, "quantite")) 
            l.pack(side=TOP, expand=1, fill=BOTH)
            self.buttonQuantite.append(l)
            l=Button(self.produitListFrame, text='---',
                     command=lambda x=ligne:self.getArticle(x, "produit"))
            l.pack(side=TOP, expand=1, fill=BOTH)
            self.buttonProduit.append(l)
            l=Button(self.prixListFrame, text='---',
                     command=lambda x=ligne:self.getArticle(x, "prix"))
            l.pack(side=TOP, expand=1, fill=BOTH)
            self.buttonPrix.append(l)
    

        # Bindings...

        self.goToArticle()
        self.article.bind(".", self.processProduit)
        self.article.bind("<Return>", self.route)
        self.fournisseur.bind(".", self.processFournisseur)
        self.date.bind("<Return>", self.goToColis)
        self.colis.bind("<Return>", self.goTopoidsColis)
        self.poidsColis.bind("<Return>", self.goToQuantite)
        self.quantite.bind("<Return>", self.goToPrice)
        self.prix.bind("<Return>", lambda x=1:self.valider.focus_set())

#        self.listbox.delete(0,END)
#        self.listbox.insert(END, enteteFact)
        self.nbArticles=0
        self.currentArticle=0
        self.currentTopArticle=0
        
        self.selectedCode[self.currentArticle]=""
        self.selectedRacourci[self.currentArticle]=""
        self.selectedFournisseur[self.currentArticle]=""
        self.selectedDate[self.currentArticle]=""
        self.selectedColis[self.currentArticle]=""
        self.selectedpoidsColis[self.currentArticle]=""
        self.selectedQuantite[self.currentArticle]=""
        self.selectedPrix[self.currentArticle]=""

        if TEST:
            self.article.delete(0, END)
            self.article.insert(END, TEST_PROD)
            if TEST=="cat":
                oyak.ihm.imprimeCatalogue()
                sys.exit(0)

    def afficheLigne(self):
        for ligne in range(self.nbLignesVisibles):
            l=ligne+self.currentTopArticle
            if oyak.debugging and not(oyak.cible):
                print "l=%d ligne=%d"%(l,ligne)
            if l<self.nbArticles:
                self.buttonQuantite[ligne].config(text=self.buttonQuantiteContent[l])
                self.buttonQuantite[ligne].update()
                self.buttonProduit[ligne].config(text=self.buttonProduitContent[l])
                self.buttonProduit[ligne].update()
                self.buttonPrix[ligne].config(text=self.buttonPrixContent[l])
                self.buttonPrix[ligne].update()
            else:
                self.buttonQuantite[ligne].config(text="---")
                self.buttonQuantite[ligne].update()
                self.buttonProduit[ligne].config(text="---")
                self.buttonProduit[ligne].update()
                self.buttonPrix[ligne].config(text="---")
                self.buttonPrix[ligne].update()
    
    def scrollFacture(self,delta):
        i=self.currentTopArticle+delta
        if i>self.nbArticles-self.nbLignesVisibles:
            i=self.nbArticles-self.nbLignesVisibles
        if i<0:
            i=0
        self.currentTopArticle=i
        self.afficheLigne()    

    def processProduit(self, event):
                
        valeur=self.article.get()
        self.article.delete(0, END)
        oyak.myProduit.ihmShow(self, valeur)

    def processFournisseur(self, event):

        if int(self.article_clef)==0:
            oyak.ihm.showMessage("Choisissez un article!",self.goToArticle)

        valeur=self.article_clef
        self.fournisseur.delete(0, END)
        oyak.myFournisseur.ihmShow(self, int(valeur))



    def acceptProduit(self, racourci, fournisseur, autre_fournisseur=0, 
                      date="-99",colis=-99,poidsColis=-99,quantite=-99, prix=-99):

        if TEST:
            print """in accept_produit : racourci=/%s/, fournisseur=/%s/,
            autre_fournisseur=/%s/, date=/%s/, colis=/%s/,
            poidsColis=/%s/,quantite=/%s/, prix=/%s/""" % \
              (racourci, fournisseur, autre_fournisseur, \
               date,colis,poidsColis,quantite, prix)

        self.autre_fournisseur=autre_fournisseur

        self.fournisseurCode=fournisseur
        self.racourci=racourci
        
        try:
          # que se passe-t-il si on vire la fenetre de facturation qui
          # a appelé??
          self.article.delete(0, END)
          self.fournisseur_content.set('')
          self.prix.delete(0, END)
        except:
          oyak.ihm.showMessage("produit rejeté!",self.neRienFaire)
          return
            
        oyak.ihm.show("facture%d"%self.nb, title="Oyak? Facture ")

        
        if True : # (racourci, fournisseur) in oyak.ProduitsCodes.keys() or autre_fournisseur:
            (prix_plancher) = ("0.")
            if int(racourci) in oyak.Produits.keys():
                libelle=oyak.Produits[int(racourci)]
                self.article.insert(END, libelle)
                self.article_label.set("Article : %d"%racourci)
                self.article_clef = racourci
            else:
                oyak.ihm.showMessage("produit %d inexistant!" % racourci,\
                                     self.goToArticle)
                return
            if int(fournisseur) in oyak.Fournisseurs.keys():
                societe=oyak.Fournisseurs[int(fournisseur)]
                self.fournisseur_content.set(societe)
                self.fournisseur_label.set("Fournisseur : %s"%fournisseur)
            else:
                oyak.ihm.showMessage("Fournisseur %d inexistant!" % fournisseur,\
                                     self.goToArticle)
                return
              

            if not (colis==-99):
                self.colis.delete(0, END)
                self.colis.insert(END, colis)
            
            if not (poidsColis==-99):
                self.poidsColis.delete(0, END)
                self.poidsColis.insert(END, poidsColis)
            
            if quantite>0:
                self.quantite.delete(0, END)
                self.quantite.insert(END, quantite)
            #self.quantite_label.set("Quantite : ("+"%6.2f"%(eval(poidsColis)+0.00)+")")

            if prix>0:
                self.prix.delete(0, END)
                self.prix.insert(END,prix)
                #self.prix_label.set("Prix : ("+"%6.2f"%(eval(prix)+0.00)+")")
            self.prix_default=prix
            self.prix_plancher=prix_plancher
            self.poids=poidsColis
            self.produit=racourci

            self.selectedCode[self.currentArticle]=racourci  # devrait etre code barre recalcule
            self.selectedRacourci[self.currentArticle]=racourci
            self.selectedFournisseur[self.currentArticle]=fournisseur    

            
            if not(date=="-99"):
                self.date.delete(0, END)
                self.date.insert(END,date)

            self.goToColis()
        else:
            oyak.ihm.showMessage("Article a part numero %s fournisseur %s"%(racourci, fournisseur), self.neRienFaire())
                
    def deleteCode(self, event):
        self.article.delete(0, END)
        self.article_label.set("Article :")
        self.article_clef = 0
        self.fournisseur.delete(0,END)
        self.fournisseur_label.set("Fournisseur :")
        self.date.delete(0, END)
        self.prix.delete(0, END)
        self.prix_label.set("Prix :")
        self.colis.delete(0, END)
        self.poidsColis.delete(0, END)
        self.quantite.delete(0, END)
        self.goToArticle()

    def goToArticle(self, event="fake"):
        oyak.ihm.show("facture%d"%self.nb, title="Oyak? Facture ")
        self.labelEntryFocus(self.article, self.article_focus,self.article_content)


    def goToFournisseur(self, event="fake"):
        oyak.ihm.show("facture%d"%self.nb, title="Oyak? Facture ")
        self.labelEntryFocus(self.fournisseur, self.fournisseur_focus,self.fournisseur_content)


    def goToPrice(self, event="fake"):
        oyak.ihm.show("facture%d"%self.nb, title="Oyak? Facture ")
        self.labelEntryFocus(self.prix, self.prix_focus,self.prix_content)

    def goToColis(self, event="fake"):
        oyak.ihm.show("facture%d"%self.nb, title="Oyak? Facture ")
        self.labelEntryFocus(self.colis, self.colis_focus,self.colis_content)

    def goTopoidsColis(self, event="fake"):
        oyak.ihm.show("facture%d"%self.nb, title="Oyak? Facture ")
        self.labelEntryFocus(self.poidsColis, self.poidsColis_focus,self.poidsColis_content)

    def goToQuantite(self, event="fake"):
        nb_col = self.colis_content.get()
        pds = self.poidsColis_content.get()
        print "in gotoquantite"
        try:
        #if True:
            q = float(nb_col)*float(pds)
            self.quantite.delete(0, END)
            self.quantite.insert(END, "%s"%q)
        except:
            print "erreur d'évaluation de quantite"
        oyak.ihm.show("facture%d"%self.nb, title="Oyak? Facture ")
        self.labelEntryFocus(self.quantite, self.quantite_focus,self.quantite_content)

    def goToDate(self, event="fake"):
        oyak.ihm.show("facture%d"%self.nb, title="Oyak? Facture ")
        self.labelEntryFocus(self.date, self.date_focus,self.date_content)

    def remplirFacture(self):
        for i in range(self.nbLignesVisibles*3):
            print

    def ajouteLigneFacture(self, quantite, produit, prix, ligne=-1):

        if oyak.debugging and not(oyak.cible):
            print "in ajouteLigneFacture quantite=%s,produit=%s,prix=%s"%(quantite,produit,prix)
            print "in ajouteLigneFacture ligne%d self.nbArticles=%d"%(ligne,self.nbArticles)
        if ligne==self.nbArticles:
            self.buttonQuantiteContent.append(quantite)
            self.buttonProduitContent.append(produit)
            self.buttonPrixContent.append(prix)
            self.nbArticles=self.nbArticles+1
        else:
            self.buttonQuantiteContent[ligne]=quantite
            self.buttonProduitContent[ligne]=produit
            self.buttonPrixContent[ligne]=prix
        
        windowLigne=ligne-self.currentTopArticle
        if oyak.debugging and not(oyak.cible):
            print "windowLigne=%d, self.currentTopArticle=%d"%(windowLigne,self.currentTopArticle)
        if windowLigne>self.nbLignesVisibles-1:
            self.currentTopArticle=ligne-self.nbLignesVisibles+1
            if self.currentTopArticle<0:
                self.currentTopArticle=0
            self.afficheLigne()
        else:
            self.buttonQuantite[windowLigne].config(text=quantite)
            self.buttonProduit[windowLigne].config(text=produit)
            self.buttonPrix[windowLigne].config(text=prix)



            
    def getArticle(self, windowLigne, focus):
        
        ligne=windowLigne+self.currentTopArticle
        if ligne>=self.nbArticles:
            oyak.ihm.showMessage("pas encore d'article ici!!!!",self.neRienFaire())
            return
        self.currentArticle=ligne
        self.acceptProduit(self.selectedRacourci[ligne], 
                           self.selectedFournisseur[ligne],
                           001,
                           self.selectedDate[ligne], 
                           self.selectedColis[ligne],
                           self.selectedpoidsColis[ligne],
                           self.selectedQuantite[ligne],
                           self.selectedPrix[ligne])
        if focus=="quantite":
            self.goToQuantite()
        if focus=="produit":
            self.goToArticle()
        if focus=="prix":
            self.goToPrice()
        return


    def ajouteArticle(self, operation='creation'):

        if operation=="creation":
            
            # verification article
            article=self.article.get()
            if article=="*" or article=="x":
                self.route()
                return
            
            if len(article)==0:
                oyak.ihm.showMessage("Article vide!", self.goToArticle)
                return FALSE
            try:
                article_deja_choisi=oyak.ProduitsRacourcis[self.racourci]
            except:
                article_deja_choisi="xxxxxxx"
                           
            # verification prix
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
                oyak.ihm.showMessage("le prix %s "%self.prix_saisi+" n'est pas reconnu", self.goToPrice)
                return
         
            # verification quantite
            quantite=self.quantite.get()
            if len(quantite)==0:
                    quantite=self.poids
            try:
                if eval(quantite)+0.0<0:
                    oyak.ihm.showMessage("la quantite %s est inferieure à 0"%quantite,self.goToQuantite)
                    return
            except:
                    oyak.ihm.showMessage("la quantite %s est incoherente"%quantite,self.goToQuantite)
                    return
            
            article=self.article.get()
            # verifier si l'article existe
    #        try :
    #          #self.listbox.insert(END, formatFact%(float(quantite),article,float(self.prix_saisi)))
            self.ajouteLigneFacture(quantite, article, float(self.prix_saisi), self.currentArticle)
    #        except :
    #            self.deleteCode("fake")
    
            self.selectedPrix[self.currentArticle]=self.prix_saisi
            self.selectedColis[self.currentArticle]=self.colis.get()
            self.selectedpoidsColis[self.currentArticle]=self.poidsColis.get()
            self.selectedQuantite[self.currentArticle]=quantite
            self.selectedDate[self.currentArticle]=self.date.get()
            self.selectedCode[self.currentArticle]=0
            self.selectedRacourci[self.currentArticle]=self.racourci
            self.selectedFournisseur[self.currentArticle]=self.fournisseurCode
            
            self.currentArticle=self.nbArticles

        if operation=="supression":
            
            
            if self.currentArticle==self.nbArticles:
                oyak.ihm.showMessage("Sélectionnez un article\n à supprimer!",self.neRienFaire())
                return
            
            for i in range(self.currentArticle,self.nbArticles-1): 
                self.selectedPrix[i]       =self.selectedPrix[i+1]    
                self.selectedColis[i]      =self.selectedColis[i+1]
                self.selectedpoidsColis[i]      =self.selectedpoidsColis[i+1]
                self.selectedQuantite[i]   =self.selectedQuantite[i+1]
                self.selectedDate[i]       =self.selectedDate[i+1]
                self.selectedCode[i]       =self.selectedCode[i+1]
                self.selectedRacourci[i]   =self.selectedRacourci[i+1]
                self.selectedFournisseur[i]=self.selectedFournisseur[i+1]

                self.buttonPrixContent[i]       =self.buttonPrixContent[i+1]    
                self.buttonQuantiteContent[i]   =self.buttonQuantiteContent[i+1]
                self.buttonProduitContent[i]    =self.buttonProduitContent[i+1]

            self.buttonPrixContent[self.nbArticles-1]    ="---"
            self.buttonProduitContent[self.nbArticles-1] ="---"
            self.buttonQuantiteContent[self.nbArticles-1]="---"

            self.nbArticles=self.nbArticles-1
            self.currentArticle=self.nbArticles
                
            self.afficheLigne()

        self.selectedCode[self.currentArticle]=""
        self.selectedRacourci[self.currentArticle]=""
        self.selectedFournisseur[self.currentArticle]=""
        self.selectedDate[self.currentArticle]=""
        self.selectedpoidsColis[self.currentArticle]=""
        self.selectedColis[self.currentArticle]=""
        self.selectedQuantite[self.currentArticle]=""
        self.selectedPrix[self.currentArticle]=""

        self.deleteCode("fake")

    def neRienFaire(self):
        return
    
    def envoyer(self, parametre=""):
        global commande_counter
        
        oyak.ihm.showMessage("Traitement Commande en  cours ", self.neRienFaire)
        if self.nbArticles==0:
              self.article.delete(0, END)
              oyak.ihm.showMessage("La commande est vide!!!", self.goToArticle)
              return            

        s="%s%s"%(self.client, oyak.sep1)
        for l in range(0, self.nbArticles):
             racourci=self.selectedRacourci[l]
             fournisseur=self.selectedFournisseur[l]
             s=s+"%s%s"%(racourci, oyak.sep2)
             s=s+"%s%s"%(fournisseur, oyak.sep2)
             s=s+"%s%s"%(self.selectedDate[l], oyak.sep2)
             s=s+"%s%s"%(self.selectedColis[l], oyak.sep2)
             s=s+"%s%s"%(self.selectedpoidsColis[l], oyak.sep2)
             s=s+"%s%s"%(self.selectedQuantite[l], oyak.sep2)
             s=s+"%s"%(self.selectedPrix[l])
             if l<self.nbArticles-1:
                 s = s+oyak.sep1
        #params = urllib.urlencode({'vendeur': self.vendeur_numero, 'commande':s})
        a_ecrire = "%s%s%s" % (self.vendeur_numero,oyak.sep1,s)
        print "facture envoyee /%s/ : vendeur=/%s/ commande=/%s/ " % (a_ecrire,self.vendeur_numero,s)
        oyak.ihm.showMessage("Commande OK!", oyak.ihm.delCurrentFacture)
        commande_counter = (commande_counter+1)%1000
        name_file="%s/%s%03d%s" % (dir_Commande,time.strftime("%Y%m%d"),
                                   commande_counter,self.vendeur_numero)
        f = open(name_file,"w")
	f.write(a_ecrire)
	f.close()
        f = open(commande_counter_file,'w')
        f.write("%d" % commande_counter)
        f.close()
        return
    
        try:
            f = urllib.urlopen(oyak.url_send_commande, params)
        except:
            oyak.ihm.showMessage("Le serveur ne répond pas!", self.goToArticle)
            oyak.ihm.showMessage("Le serveur ne répond pas! \n url=%s \n v=%s \n s=%s"%
                                 (oyak.url_send_commande,self.vendeur_numero,s), 
                                 self.goToArticle)
            oyak.writeDebug("?vendeur=1&params="+s)
            return
        ack=f.readlines()
        ok=ack[0]
        if (ok[0]=="0"):
            oyak.ihm.showMessage("Commande %s!"%ok[2:], oyak.ihm.delCurrentFacture)
        else:
            oyak.ihm.showMessage("Commande perdue!", oyak.ihm.delCurrentFacture)
            return
        f.close()
    
    def route(self, event):
       
       
        article=self.article.get()
        racourci=article
        oyak.Factures[oyak.factureCurrent].racourci=racourci

        if len(racourci)==0:
            oyak.ihm.showMessage("Article vide!", self.goToArticle)
            return FALSE
         # le produit selectionne a un code barre
        if len("%s"%racourci)>1:
            code = "%s"%racourci
            if len(code)>6:
                other = int(code[6:])
            else:
                other = ""
            if int(racourci) in oyak.ProduitsDetail.keys():
                (detail_clef, detail_libelle,detail_fournisseur,\
                 detail_code_barre,detail_poids, detail_prix, \
                 detail_peche) =  oyak.ProduitsDetail[int(racourci)]
                self.fournisseur_clef = detail_fournisseur                                
                self.poidsColis.delete(0, END)
                self.poidsColis.insert(END, detail_poids)
                self.prix.delete(0, END)
                self.prix.insert(END, detail_prix)
            else:
                detail_clef = int(code[0:3])
                if len(code)>3:
                    detail_fournisseur = int(code[3:6])
                    self.fournisseur_clef = code[3:6]                                
                else:
                    detail_fournisseur = -99
                detail_prix = detail_poids = -99
                detail_peche = ""
                
            self.fournisseur.delete(0, END)
            self.fournisseur.insert(END, detail_fournisseur)
            self.date.delete(0, END)
            self.date.insert(END, other)
            self.goToFournisseur()
            self.acceptProduit(int(detail_clef), int(detail_fournisseur), \
                                   date = "%s%s" % (other,detail_peche),prix=detail_prix, poidsColis=detail_poids)
            return TRUE
       
       
        # * ->  La commande est envoye
        if racourci[0]=="*" :
            self.envoyer(racourci[1:])
            return TRUE
        # sinon on process le couple (racourci,fournisseur)
        try :
             if int(racourci) in oyak.ProduitsDetail.keys():
                libelle=oyak.Produits[int(racourci)]
                oyak.Factures[oyak.factureCurrent].racourci=int(racourci)
                self.racourci=racourci
                return True
        except:
                dump_exception("acceptProduit",["clef = %s",racourci])
                self.article.delete(0, END)
                oyak.ihm.showMessage("%s n'est pas un code reconnu!"%racourci, self.goToArticle)
                return FALSE
        

        
def run():
    global oyak

    oyak.ihm = ihmRoot()
    oyak.ihm.start()

if __name__ == "__main__":
    parse()
    oyak = singleton()
    if oyak.cible:
        try:
            run()
        except:
             os.remove("/Oyak/except.out")
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
