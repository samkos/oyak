import os
import string
import re
import time,datetime
import sys
from stat import *

timeTouchFile="/Oyak/ToPrint/PrintDemon.txt"
timeOK=30

dir_printTODO='c:\Oyak\ToPrint'
dir_workTODO="/Oyak/Work"
dir_factureTODO="/facprint"
dir_etiqTODO="/etiqprint"
dir_impTODO="/impprint"
exe_print="\"c:\Program Files\Ghostgum\gsview\gsprint.exe\" -printer \"test1\""
exe_print="\"c:\Program Files\Ghostgum\gsview\gsprint.exe\" -printer \"test1\""
exe_print="\"c:/Program Files/EasyPHP1-8/www/phpmyfactures/print/print.bat \""
exe_printTo="\"c:/Program Files/EasyPHP1-8/www/phpmyfactures/print/printTo.bat \""
exe_facture="\"c:/Program Files/EasyPHP1-8/www/phpmyfactures/factures/traite.bat\" ";
exe_etiq="\"c:/Program Files/EasyPHP1-8/www/phpmyfactures/barcode/traite.bat\" ";
exe_imp="\"c:/Program Files/EasyPHP1-8/www/phpmyfactures/impression/traite.bat\" ";

debug=01
msg=1

now=datetime.datetime.now()
timestamp="%s%s"%(now.strftime("%Y%m%d"),now.strftime("%H%M%S"))

#sys.stdout = open("c:/Oyak/print.log","a")

def probeFacture():
    global timestamp
    
    files=os.listdir(dir_factureTODO)

    if files:
        if msg:
            print "%s"%timestamp+":"+"traitement des factures en attente"
        commande=exe_facture
        os.system(commande)
    else:
        if msg:
            print "%s"%timestamp+":"+"Pas de facture en attente"
        

def probeEtiq():
    global timestamp
    
    files=os.listdir(dir_etiqTODO)

    if files:
        if msg:
            print "%s"%timestamp+":"+"traitement des etiquettes en attente"
        commande=exe_etiq
        os.system(commande)
    else:
        if msg:
            print "%s"%timestamp+":"+"Pas d'etiquette en attente"
        

def probeImp():
    global timestamp
    
    files=os.listdir(dir_impTODO)

    if files:
        if msg:
            print "%s"%timestamp+":"+"traitement des impressions generale en attente"
        commande=exe_imp
        os.system(commande)
    else:
        if msg:
            print "%s"%timestamp+":"+"Pas d'impression generale en attente"
        

def probePrint(dir_print,printer="default"):
    global timestamp

    files=os.listdir(dir_print)

    nb=0
    for file in files:

        if not(file=="PrintDemon.txt"):
            filename=dir_print+"/"+file

            # est-ce un repertoire, si oui on recurse
            mode = os.stat(filename)[ST_MODE]
            if S_ISDIR(mode):
                probePrint(filename,file)
                
            else:
            # mpression fichier
                if printer=="default":
                   commande = exe_print+" "+filename
                else:
                   commande = exe_printTo+" "+filename+" "+printer
                if debug:
                    print "%s"%timestamp+":"+commande
                os.system(commande)
        
                if msg:
                    print "%s"%timestamp+":"+ "Impression de %s "%filename

                os.remove(filename)

                if msg:
                    print "%s"%timestamp+":"+ "Effacement de %s "%filename


    return


def touchDate():
    now=datetime.datetime.now()
    timestamp="%s%s"%(now.strftime("%Y%m%d"),now.strftime("%H%M%S"))

    f=open(timeTouchFile,"w")
    f.write(timestamp)
    f.write("\nNe pas effacer!!!!!!!! fichier de controle de l'impression")
    f.close()


def checkRunning():
    global timestamp,timeTouchFile,timeOK

    if not(os.path.exists(timeTouchFile)):
        return 0

    try:
        f=open(timeTouchFile,"r")
        l=f.readlines()
        timestamp_old=eval(l[0])
        timestamp=eval(timestamp)
        #print timestamp_old,timestamp,timestamp_old-timestamp
        diff = timestamp-timestamp_old
        #print diff
        if diff<timeOK:
            return 1
        else:
            return 0
    except:
        return 0
    
if not(os.path.exists(dir_printTODO)):
    os.mkdir(dir_printTODO)

if not(os.path.exists(dir_factureTODO)):
    os.mkdir(dir_factureTODO)

if not(os.path.exists(dir_etiqTODO)):
    os.mkdir(dir_etiqTODO)

if not(os.path.exists(dir_impTODO)):
    os.mkdir(dir_impTODO)

if not(os.path.exists(dir_workTODO)):
    os.mkdir(dir_workTODO)

if checkRunning():
    print "%s"%timestamp+":"+"Demon OK"
else:
    touchDate()
    
    if debug:
        print "%s"%timestamp+":"+"Demarrage Print Daemon"

    while 1:
        touchDate()
        if msg:
            print "%s"%timestamp+":"+"checking files pending..."
        probeFacture()
        probeEtiq()
        probeImp()
        probePrint(dir_printTODO)
        time.sleep(10)
