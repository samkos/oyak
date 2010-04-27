# File: hello2.py

from Tkinter import *
import os

#curDir="C:\\Program Files\\EasyPHP1-8\\www\\phpmyfactures\\device\\Pilote\\"
rapiDir="bin\\"
regSymbol="hklm\\SOFTWARE\\Symbol Technologies, Inc.\\Profiles"
regWLAN1="hklm\COMM\NETWLAN1"
regHKLM="hklm"
outFileName="out.txt"

class IHM   :


    def __init__(self):

        self.debug=01

        # obtention d'une frame principale
        self.root = Tk()
        #self.root.wm_state(newstate="zoomed")

        # fenetre de Bouton
        self.boutonFrame=Frame(self.root)
        self.boutonFrame.pack(expand=0,fill=X)

        # fenetre de resultat
        self.resultFrame=Frame(self.root)
        self.resultFrame.pack(expand=1,fill=BOTH)

        self.scrollbarY = Scrollbar(self.resultFrame)
        self.scrollbarY.pack(side=RIGHT,expand=0,fill=Y)

        self.scrollbarX = Scrollbar(self.resultFrame,orient=HORIZONTAL)
        self.scrollbarX.pack(side=BOTTOM,expand=0,fill=X)

        self.listbox = Listbox(self.resultFrame, xscrollcommand=self.scrollbarX.set, yscrollcommand=self.scrollbarY.set)
        self.listbox.pack(side=LEFT, expand=1, fill=BOTH)
        self.scrollbarX.config(command=self.listbox.xview)
        self.scrollbarY.config(command=self.listbox.yview)


        # definition d'un bouton Wifi
        Titre = Label(self.boutonFrame, text="PILOTE DEVICE v0.1", width=80, height=5)
        # placement du Bouton dans la frame principale
        Titre.pack(expand=1,fill=X)

        # definition d'un bouton Wifi
        Bouton = Button(self.boutonFrame, text="Regler la Connection Wifi", command=self.launchMobileCompanion)
        # placement du Bouton dans la frame principale
        Bouton.pack(expand=1,fill=X)

        b1=self.addButtonReadReg(regSymbol)
        b2=self.addButtonReadReg(regWLAN1)
        b2=self.addButtonReadReg(regHKLM,pipe=0)

        # definition d'un bouton warm reboot
        Bouton = Button(self.boutonFrame, text="warm reboot", command=self.warmReboot)
        # placement du Bouton dans la frame principale
        Bouton.pack(expand=1,fill=X)

        # definition d'un bouton Copie Vendeur
        Bouton = Button(self.boutonFrame, text="Copie Vendeur", command=lambda x="fake":self.copieVendeur("vendeur"))
        # placement du Bouton dans la frame principale
        Bouton.pack(expand=1,fill=X)
        Bouton = Button(self.boutonFrame, text="Copie Vendeur Singleton", command=lambda x="fake":self.copieVendeur("vendeur_singleton"))
        # placement du Bouton dans la frame principale
        Bouton.pack(expand=1,fill=X)

        # definition d'un bouton Copie Vendeur
        Bouton = Button(self.boutonFrame, text="Copie provisoire Vendeur", command=lambda x="fake":self.copieVendeur("vendeur",light=1))
        # placement du Bouton dans la frame principale
        Bouton.pack(expand=1,fill=X)
        Bouton = Button(self.boutonFrame, text="Copie provisoire Vendeur Singleton", command=lambda x="fake":self.copieVendeur("vendeur_singleton",light=1))
        # placement du Bouton dans la frame principale
        Bouton.pack(expand=1,fill=X)

        # definition d'un bouton Installe appli
        Bouton = Button(self.boutonFrame, text="Installe Application", command=self.installAppli)
        # placement du Bouton dans la frame principale
        Bouton.pack(expand=1,fill=X)

        
        # definition d'un bouton Copie Vendeur
        Bouton = Button(self.boutonFrame, text="run Vendeur", command=self.runVendeur)
        # placement du Bouton dans la frame principale
        Bouton.pack(expand=1,fill=X)

        # definition d'un bouton Copie Vendeur
        Bouton = Button(self.boutonFrame, text="kill Vendeur", command=lambda x="fake":self.killProcess("python"))
        # placement du Bouton dans la frame principale
        Bouton.pack(expand=1,fill=X)

        # definition d'un bouton kill Appcenter
        Bouton = Button(self.boutonFrame, text="kill AppCenter", command=lambda x="fake":self.killProcess("AppCenter.exe"))
        # placement du Bouton dans la frame principale
        Bouton.pack(expand=1,fill=X)


        # definition d'un bouton Installe appli
        Bouton = Button(self.boutonFrame, text="Installe Application", command=self.installAppli)
        # placement du Bouton dans la frame principale
        Bouton.pack(expand=1,fill=X)

        # definition d'un bouton del cache
        Bouton = Button(self.boutonFrame, text="Effacer Cache", command=lambda x="fake":self.delCache())
        # placement du Bouton dans la frame principale
        Bouton.pack(expand=1,fill=X)

        # definition d'un bouton del cache
        Bouton = Button(self.boutonFrame, text="Initialiser Cache", command=lambda x="fake":self.initCache())
        # placement du Bouton dans la frame principale
        Bouton.pack(expand=1,fill=X)

        # definition d'un bouton del cache
        Bouton = Button(self.boutonFrame, text="Effacer output", command=lambda x="fake":self.clearWindow())
        # placement du Bouton dans la frame principale
        Bouton.pack(expand=1,fill=X)




    def addButtonReadReg(self,reg,pipe=1):
        # definition d'un bouton lire WLAN valeur
        Bouton = Button(self.boutonFrame, text="Lire registre "+reg,
                        command=lambda : self.getWlanReg(reg,pipe))
        # placement du Bouton dans la frame principale
        Bouton.pack(expand=1,fill=X)
        return Bouton


    # execute une commande sur la device
    def run(self,what,pipe=0):
            commande="%s\\%s"%(rapiDir,what)
            if self.debug:
                self.affiche("EXEC : "+commande)
            output=os.popen(commande)
            res=output.readlines()
            if pipe:
               return output.readlines()
            else:
               for r in res:
                   self.affiche(r)
                   

    def clearWindow(self):
        self.listbox.delete(0, END)


    # fonction appelee par l'appui sur le bouton MobileCompanion
    def launchMobileCompanion(self):
        self.run("prun nictt")

    # fonction appelee par l'appui sur le bouton warmReboot
    def warmReboot(self):
        self.run("preboot")

    # fonction appelee par l'appui sur le bouton Lire registre WLAN
    def copieVendeur(self,name,light=0):
        pput="pput.exe -f ..\\appli\\%s.pyw \\Oyak\\vendeur.pyw"%name
        self.run(pput,pipe=0)
        if light==0:
            pput="pput.exe -f ..\\appli\\%s.pyw \\Application\\Oyak\\vendeur.pyw"%name
            self.run(pput,pipe=0)
        self.affiche("vendeur copié avec succès")
        
    def runVendeur(self):
        prun="prun.exe \\Python25\\python /nopcceshell \\Oyak\\vendeur.pyw"
        output=self.run(prun,pipe=0)
        self.affiche("Application vendeur lancée")

    def killProcess(self,name):
        prun="pkill.exe %s"%name
        output=self.run(prun,pipe=0)
        self.affiche("Application %s arretée"%name)

    def installAppli(self):
        self.listbox.delete(0, END)
        self.installReg()
        self.copieVendeur("vendeur_singleton")
        self.initCache()
        self.affiche("Application Installée correctement")

    def installReg(self):
        pput="pput.exe -f \"..\\a copier\\Application\\AppCenter.reg\"  \\Application\\AppCenter.reg"
        self.run(pput,pipe=0)
        self.affiche("fichier registre Appcenter Installé avec Succès");
        
        
    def initCache(self):
        self.run("pput.exe  -f c:\\Oyak\\*.bak \\Oyak\\")
        self.affiche("fichier de Cache copiés")



    def delCache(self):
        self.run("pdel.exe  \\Oyak\\*.bak")
        self.affiche("fichiers de cache effacés")

    # fonction appelee par l'appui sur le bouton Lire registre WLAN
    def getWlanReg(self,reg,outFile=0,pipe=0):
        print reg,outFile,pipe
        lisReg="pregdmp \""+reg+"\""
        self.run(lisReg,pipe)
        self.affiche("Application de configuration réseau lancée")

        
    def affiche(self,output):
        self.listbox.insert(END,output);
        print output

    def start(self):
       # demarrage de la boucle d'evenements
       self.active=1
       self.root.mainloop()

    
app=IHM()

app.start()




