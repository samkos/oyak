import os, sys, string, shutil
from stat import *
import time,datetime


from_dir="C:\Program Files\EasyPHP1-8\www\phpmyfactures"
work_dir="C:\Program Files\EasyPHP1-8\www\SAVE"
dirname=string.split(from_dir,'\\')[-1]
to_dir=work_dir+"\\"+dirname

debug=0

def deltree(dir):
    global debug
    
    mode = os.stat(dir)[ST_MODE]
    if S_ISDIR(mode):
      for f in os.listdir(dir):
          pathname = '%s\%s' % (dir, f)
          mode = os.stat(pathname)[ST_MODE]
          if S_ISDIR(mode):
              # It's a directory, recurse into it
              deltree(pathname)
          elif S_ISREG(mode):
              # It's a file removeit
              try:
                  os.remove(pathname)
                  if debug>0:
                      print "F- "+pathname  
              except:
                  print "erreur Affacement fichier  "+pathname
                  raise
      # It's a directory, remove it
      try:
          if debug>0:
                print "D- "+dir
          os.rmdir(dir)
      except:
          print "erreur Effacement Dir "+dir
          raise
      
    



def copytree(dir,from_dir,to_dir):
    global debug
    
    mode = os.stat(dir)[ST_MODE]
    if S_ISDIR(mode):
      for f in os.listdir(dir):
        if not(f==".svn") :
            pathname = '%s\%s' % (dir, f)
            to_pathname=to_dir+"\\"+pathname.replace(from_dir,"")
            mode = os.stat(pathname)[ST_MODE]
            if S_ISDIR(mode):
                # It's a directory, create a copy directory
                try:
                    os.mkdir(to_pathname)
                except:
                    print "erreur Creation Dir "+to_pathname
                    raise
                if debug>0:
                      print "D+ "+to_pathname
                # It's a directory, recurse into it
                if not (f=="work"):
                    copytree(pathname, from_dir, to_dir)

            elif S_ISREG(mode):
                # It's a file copy it!
                try:
                    shutil.copy(pathname,to_pathname)
                except:
                    print "erreur copie fichier  "+pathname+"  "+to_pathname
                    raise
                if debug>0:
                    print "F+ "+to_pathname
    

def save_database():

    os.system("make_7z.bat")

             
if __name__ == '__main__':

    print """
-------------------------------------------------
-------------------------------------------------
! sauvegarde du site
-------------------------------------------------
-------------------------------------------------
"""


    # effacement de la sauvegarde eventuelle
    print "! Effacement de l'ancienne sauvegarde..."
    
    try:
        deltree(work_dir)
        if debug>0:
            print "Effacement "+work_dir
    except:
        print "Erreur effacement " + work_dir
        pass

    # creation du diretory cible
    try:
        os.mkdir(work_dir)
    except:
        print "Erreur creation " + work_dir
        pass
    try:
        os.mkdir(to_dir)
    except:
        print "Erreur creation " + to_dir
        pass

    

    # recopie du site web
    print "! Sauvegarde site web"
    copytree(from_dir,from_dir, to_dir)

    # sauvegarde de la base
    # construction du fichier 7z

    save_database()

    # renommage fichier sauvegarde
    now=datetime.datetime.now()
    name_arch="c:\Oyak\Oyak-%s-%s.7z"%(now.strftime("%Y%m%d"),now.strftime("%H%M%S"))
    print name_arch
    os.rename("c:\Oyak\save_site.7z",name_arch)



    print """
-------------------------------------------------
-------------------------------------------------
! sauvegarde du site termine
-------------------------------------------------
-------------------------------------------------
"""

    input("Le site est sauvegarde dans le fichier "+name_arch)


