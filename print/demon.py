import getopt, sys, os, shutil
import string
import re
import time,datetime
from stat import *

timeTouchFile="/Oyak/ToPrint/PrintDemon.txt"
timeOK=30


dir_printTODO='c:\Oyak\ToPrint'
dir_workTODO="c:/Oyak/Work"
dir_factureTODO="c:/facprint"
dir_etiqTODO="c:/etiqprint"
dir_impTODO="c:/impprint"
exe_print=exe_printTo=exe_facture=exe_etiq = "???exe_xxx"

debug=0
noprint=0
msg=1
once=0

now=datetime.datetime.now()
timestamp="%s%s"%(now.strftime("%Y%m%d"),now.strftime("%H%M%S"))

#sys.stdout = open("c:/Oyak/print.log","a")

def usage(message = None):
    """ helping message"""
    if message:
        print message
    print "  usage: \n \t python demon.py \
             \n\t\t[ --help ] \
             \n\t\t[ --once ] \
             \n\t\t[ --debug ] \
             \n\t\t[ --noprint ] \
             \n\t\t[ --fac=<fichier facture a tester> ] \
             \n\t\t[ --etiq=<fichier code barre a tester> ] \
             \n\t\t[ --imp=<fichier bordereau a tester> ] \
             \n\t\t[ --every=<probe every seconds> ] "

    sys.exit(1)




def parse():
    global once,debug,noprint,timeOK,msg
    
    """ parse the command line and set global _flags according to it """
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ht", 
                                   ["help", "once", "every=", "fac=", "etiq=", \
                                    "imp=", "trace=", "debug", "noprint"])
    except getopt.GetoptError, err:        # print help information and exit:
        usage(err)

    # first scan opf option to get prioritary one first
    # those who sets the state of the process
    # especially those only setting flags are expected here
    for option, argument in opts:
        if option in ("-h", "--help"):
            usage("")
        elif option in ("--once"):
            once=1
        elif option in ("--every"):
            timeOK = int(argument)
        elif option in ("--trace"):
            msg = int(argument)
        elif option in ("--fac"):
            fichier = argument
            shutil.copy(fichier,dir_factureTODO)
        elif option in ("--etiq"):
            fichier = argument
            shutil.copy(fichier,dir_etiqTODO)
        elif option in ("--imp"):
            fichier = argument
            shutil.copy(fichier,dir_impTODO)
        elif option in ("--debug"):
            debug = True
        elif option in ("--noprint"):
            noprint = True
        else:
            usage("unhandled option %s" % option)

def search_soft(soft,drives,versions,specific_file="",root="/Program Files/"):
    # recherche easyphp
    path_found=False
    # checking the installed drive
    for drive in drives:
        for version in versions:
            if not(path_found):
                if os.path.isfile(drive+":"+root+version+specific_file):
                    path_found=drive+":"+root+version
                
    if not path_found:
        print "erreur : %s not found"%soft
        sys.exit(1)

    if debug:
        print "%s installe dans  : %s"%(soft,path_found)

    return path_found+"/"+specific_file
        
def init_env_bis():

    drives = ["c","d"]

    gs_env=search_soft("gs",drives,["Ghostgum/gsview/"],"gsprint.exe")
    gs_env=search_soft("easyphp",drives,["EasyPHP 2.0b1","EasyPHP1-8"],"/www/phpmyfactures/index.php")
    latex_env=search_soft("latex",drives,["MiKTeX 2.5","MiKTeX 2.6"],"/miktex/bin/pdflatex.exe")
    

def init_env():
    global exe_print, exe_printTo,exe_facture,exe_etiq,exe_imp

    drive="c:"
    drive_found=False
    # checking the installed drive
    for drive in ["c","d"]:
        if not(drive_found):
            if os.path.isfile(drive+":\Program Files\Ghostgum\gsview\gsprint.exe"):
                drive_found=drive

    if not drive_found:
        print "erreur : drive not found"
        sys.exit(1)

    drive=drive_found
    
    if debug:
        print "drive d'installation : ",drive

    # recherche easyphp
    easyphp_found=False
    # checking the installed drive
    for drive in ["c","e"]:
        for easyphp in ["EasyPHP-5.3.2i","EasyPHP 2.0b1","EasyPHP1-8"]:
            if not(easyphp_found):
                if os.path.isfile(drive+":/Program Files/"+easyphp+"/www/phpmyfactures/index.php"):
                    easyphp_found=drive+":/Program Files/"+easyphp
                
    if not easyphp_found:
        print "erreur : easyphp not found"
        sys.exit(1)

    easyphp=easyphp_found
    if debug:
        print "easyphp d'installation : ",easyphp


    exe_print="\""+easyphp+"/www/phpmyfactures/print/print.bat \""
    exe_printTo="\""+easyphp+"/www/phpmyfactures/print/printTo.bat \""
    exe_facture="\""+easyphp+"/www/phpmyfactures/print/factures/traite.bat\" ";
    exe_etiq="\""+easyphp+"/www/phpmyfactures/barcode/traite.bat\" ";
    exe_imp="\""+easyphp+"/www/phpmyfactures/print/impression/traite.bat\" ";


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



def probeFacture():
    global timestamp
    
    files=os.listdir(dir_factureTODO)

    if files:
        if msg:
            print "%s"%timestamp+":"+"traitement des factures en attente"
        commande=exe_facture
        if debug:
            print "%s"%timestamp+":execution de ",commande
        
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
        if debug:
            print "%s"%timestamp+":execution de ",commande
        os.system(commande)
    else:
        if msg:
            print "%s"%timestamp+":"+"Pas d'etiquette en attente"
        
def probeImp():
    global timestamp,debug,noprint,exe_imp
    
    files=os.listdir(dir_impTODO)
    if debug:
        print files
        
    if files:
        if msg:
            print "%s"%timestamp+":"+"traitement des impressions generales en attente"
            print exe_imp
        commande=exe_imp
        if 1 or debug:
            print "%s"%timestamp+":execution de ",commande
        os.system(commande)
    else:
        if msg:
            print "%s"%timestamp+":"+"Pas d'impression generale en attente"
        

def probePrint(dir_print,printer="default"):
    global timestamp

    if printer=="TEST":
        print "%s"%timestamp+":"+ "pas d'impression pour l'imprimante TEST"
        return
    else:
        print "%s"%timestamp+":"+ "impression des documents pour l'imprimante "+printer
    files=os.listdir(dir_print)

    # reading common environnement settings

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
                    print "%s"%timestamp+":execution de "+commande
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


parse()
if debug:
    print "once=%s,debug=%s,noprint=%s,timeOK=%s,msg=%s"%(once,debug,noprint,timeOK,msg)
init_env_bis()
init_env()

if checkRunning() and not(once):
    print "%s"%timestamp+":"+"Demon OK"
else:
    touchDate()
    
    if debug:
        print "%s"%timestamp+":"+"Demarrage Print Daemon"

    while 1:
        touchDate()
        if msg:
            print "%s"%timestamp+":"+"checking files pending..."
        probeEtiq()
        probeFacture()
        probeImp()
        probePrint(dir_printTODO)
        if debug:
            print once
        if once:
            print "%s"%timestamp+":juste une execution"
            sys.exit(0)
        time.sleep(10)
