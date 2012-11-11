import getopt, sys, os, shutil
import string
import re
import time,datetime
from stat import *
from pdfprint import *

if sys.platform.startswith("linux"):
    TMPDIR="/tmp"
else:
    TMPDIR="c:"

timeTouchFile=TMPDIR+"/Oyak/ToPrint/PrintDemon.txt"
timeOK=30


dir_printTODO=TMPDIR+'/Oyak/ToPrint'
dir_workTODO=TMPDIR+"/Oyak/Work"
dir_factureTODO=TMPDIR+"/facprint"
dir_etiqTODO=TMPDIR+"/etiqprint"
dir_impTODO=TMPDIR+"/impprint"
exe_view=exe_print=exe_printTo=exe_facture=exe_etiq = "???exe_xxx"

debug=0

noprint=0
msg=1
once=0
fichier_fac=0
fichier_imp=0
fichier_etiq=0

now=datetime.datetime.now()
timestamp="%s%s"%(now.strftime("%Y%m%d"),now.strftime("%H%M%S"))

#sys.stdout = open(TMPDIR+"/Oyak/print.log","a")

if not(os.path.exists(TMPDIR+"/facprint")):
    os.mkdir(TMPDIR+"/facprint")

if not(os.path.exists(TMPDIR+"/etiqprint")):
    os.mkdir(TMPDIR+"/etiqprint")

if not(os.path.exists(TMPDIR+"/Oyak")):
    os.mkdir(TMPDIR+"/Oyak")

if not(os.path.exists(TMPDIR+"/Oyak/ToPrint")):
    os.mkdir(TMPDIR+"/Oyak/ToPrint")
    
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
    global once,debug,noprint,timeOK,msg,fichier_fac,fichier_imp,fichier_etiq
    
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
            fichier_fac = argument
            #shutil.copy(fichier,dir_factureTODO)
        elif option in ("--etiq"):
            fichier = argument
            #shutil.copy(fichier_fac,dir_etiqTODO)
        elif option in ("--imp"):
            fichier_imp = argument
            #shutil.copy(fichier,dir_impTODO)
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

    if sys.platform.startswith("linux"):
        return

    drives = ["c","e"]

    gs_env=search_soft("gs",drives,["Ghostgum/gsview/"],"gsprint.exe")
    gs_env=search_soft("easyphp",drives,["EasyPHP 2.0b1","EasyPHP1-8"],"/www/phpmyfactures/index.php")
    latex_env=search_soft("latex",drives,["MiKTeX 2.5","MiKTeX 2.6"],"/miktex/bin/pdflatex.exe")
    

def init_env():
    global exe_view, exe_print, exe_printTo,exe_facture,exe_etiq,exe_imp


    if sys.platform.startswith("linux"):
        easyphp = ''
        exe_view="evince "
    else:
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
   #        for easyphp in ["EasyPHP1-8"]:
               if not(easyphp_found):
                   if os.path.isfile(drive+":/Program Files/"+easyphp+"/www/phpmyfactures/index.php"):
                       easyphp_found=drive+":/Program Files/"+easyphp
                   
       if not easyphp_found:
           print "erreur : easyphp not found"
           sys.exit(1)

       easyphp=easyphp_found
       if debug:
           print "easyphp d'installation : ",easyphp

       exe_view="\""+easyphp+"/www/phpmyfactures/print/view.bat \""    
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
    global timestamp,noprint,fichier_fac,debug,TMPDIR
    
    files_pending=os.listdir(dir_factureTODO)
    #print dir_factureTODO,files_pending
    
    files=[]
    for f in files_pending:
        f = "%s/%s" % (dir_factureTODO,f)
        files.append(f)
        
    if files or fichier_fac:
        if msg:
            print "%s"%timestamp+":"+"traitement des factures en attente"
        if fichier_fac:
            files.append(fichier_fac)
        for fic in files:
            print "traitement facture ",fic
            pr = print_facture(fic,"all.pdf")
            if noprint:
                shutil.copy("all.pdf","%s/Oyak/screen.pdf" % TMPDIR)
            else: 
                dir_printer = "%s/Oyak/ToPrint/%s/" % (TMPDIR,pr)
                if not os.path.exists(dir_printer):
                    os.makedirs(dir_printer)
                shutil.copy("all.pdf","%s/facture.pdf" % dir_printer) 
            shutil.copy("all.pdf","%s/Oyak/facture.pdf" % TMPDIR)
            os.unlink("all.pdf")
            if not(fic==fichier_fac):
                os.unlink(fic)
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
    global timestamp,debug,noprint,exe_imp,fichier_imp
    
    files=os.listdir(dir_impTODO)
    if debug:
        print files
        
    if files or fichier_imp:
        if not sys.platform.startswith("linux"):
            pass
        if msg:
            print "%s"%timestamp+":"+"traitement des impressions generales en attente"
            print exe_imp
        commande=exe_imp
        if (noprint):
            commande = commande+" --noprint=1"
        if (debug):
            commande = commande+" --debug=1"
        if (fichier_imp):
            commande = commande+" --file="+fichier_imp
        if debug:
            print "%s"%timestamp+":execution de ",commande
        os.system(commande)
    else:
        if msg:
            print "%s"%timestamp+":"+"Pas d'impression generale en attente"
        

def probePrint(dir_print,printer="default"):
    global timestamp, noprint

    if noprint:
        if sys.platform.startswith("linux"):
            commande = exe_view + TMPDIR+"/Oyak/screen.pdf"
        else:
            commande = exe_view +" c:\oyak\screen.pdf"
        print commande 
        os.system(commande)
        return


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

            # impression fichier
            
              if noprint:
                  print "%s"%timestamp+":"+ "Non impression de %s "%filename
                  commande = exe_view +" "+filename
              else:
                  if printer=="default":
                     commande = exe_print+" "+filename
                  else:
                      if printer.find("@")>=0:
                          (printer,server)=printer.split("@")
                          printer = '\\\\%s\\%s'%(server,printer)
                      commande = exe_printTo+" "+filename+" "+printer
                      if not sys.platform.startswith("linux"):
                          commande = commande.replace('/','\\')
                  if True or debug:
                      print "%s"%timestamp+":execution de "+commande
                  if msg:
                      print "%s"%timestamp+":"+ "Impression de %s "%filename+"sur imprimante %s"%printer

              os.system(commande)

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
