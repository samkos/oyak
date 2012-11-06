# Create your views here.
import os, sys, time, string, glob
from datetime import datetime, date, time

from django import forms
from django.contrib.auth.forms import *

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext, Context, loader
from django.contrib.auth import authenticate, login
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template.loader import render_to_string



import mimetypes
from django.core.servers.basehttp import FileWrapper

from django.views.decorators.cache import cache_control
# from django.views.decorators.vary import vary_on_cookie
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_response_exempt

from django.http import QueryDict

import config, sys, traceback


show_colonnes = { "fournisseurs" : [ "id,clef,societe,ville", "clef","societe"],
                  "clients"      : [ "id,clef,societe,ville", "clef","societe"],
                  "produits"     : [ "id,titre,stock,barcode,prix_vente_ht,prix_plancher_ht,"+\
                                         "fournisseur,clef,poids", "clef","titre"],
                  "vendeurs"     : [ "id,nom,prenom", "id","nom"] }


data = {}

import sqlite3
ROOT_PATH = os.path.dirname(__file__)
print "ouverture base %s/../db.sqlite" % ROOT_PATH
conn = sqlite3.connect('%s/../db.sqlite' % ROOT_PATH, check_same_thread = False  )
conn.row_factory = sqlite3.Row                # acces facile aux colonnes

# everything fine... start list
try:
    HOME = os.environ['HOME']
except:
    print "[VIEW] ERROR Problem occured when loading vishnu module"
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print "*** print_tb:"
    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
    print "*** print_exception:"
    traceback.print_exception(exc_type, exc_value, exc_traceback,
                              limit=2, file=sys.stdout)
    sys.exit(1)

@cache_control(must_revalidate=True, max_age=6)
def index(request , url):
    if len(url)==0:
        t = loader.get_template('index.html')
        c = Context({
            'oyak_version':  config.oyak_version,
            })
        return HttpResponse(t.render(c))
    print "url=/%s/"%url
    if url[-1]=="/":
        url=url[:-1]
    if url=="commandes/test":
        out=list_tests()
        return HttpResponse(out)
    if url=="cartouche":
        t = loader.get_template('cartouche.html')
        c = Context({
            'oyak_version':  config.oyak_version,
            })
        return HttpResponse(t.render(c))
        
    if url in ("fournisseurs","vendeurs","clients","produits"):
        out= browse(url)
        return HttpResponse(out)
    if url=="cartouche":
        out= ihm_www.wrap(None,"cartouche")
        return HttpResponse(out)
    if url[0:3]=="xxx":
        filename = "../DOCS/%s" % url[3:]
        if config.PORTAL_DEBUG:
            print "[VIEW]  file  : ",filename
        if os.path.isfile(filename):
            l = open(filename,"r").read()
            l=page_framed(filename)
        else:        
            l=page_message("to come not!")
    else:
        filename = "%s" % url
        if config.PORTAL_DEBUG:
            print "[VIEW]  fichier : ---> ",filename
        if os.path.isfile(filename):
            l = open(filename,"r").read()
        else:
            print "[VIEW]  ZZZZZ file non existing : ",filename
            l=page_message("nothing yet!")
    return  HttpResponse(l)


def list_tests():
    testing_facs = glob.glob("TESTS/fac/*")
    testing_etiq = glob.glob("TESTS/etiq/*")
    testing_imp =  glob.glob("TESTS/imp/*")

    waiting_factures = glob.glob("%s/facprint/*" % config.OYAK_DIR)
    waiting_printings = glob.glob("%s/impprint/*" % config.OYAK_DIR)

    valeurs = {}
    colonnes = {}
    colonnes[0] = {"name"  : "fichiers"}
    i = 0
    print "testing_facs",testing_facs+testing_etiq+testing_imp
    for fic in testing_facs+testing_etiq+testing_imp:
        valeurs[i] = \
                   ( "<a href='/edit/%s'>'%s</a>" % (fic,fic) + "</td><td>"\
                     "&nbsp; <a href='/process/screen/%s'>ecran</a> " % fic+ \
                     "&nbsp; <a href='/process/print/%s'>imprimante</a> " % fic)
        i = i+1

    dt = datetime.now() 
    c = render_to_string('tests.html' , {'date' : dt.strftime("%A, %d. %B %Y %I:%M%p"),
                                        'colonnes' : colonnes,
                                         'valeurs' : valeurs,
                                        'titre' : "Liste des tests"
                                               })
    return c

def browse(table):
 
   c = conn.cursor()  
   fields,nom_clef,nom_valeur = show_colonnes[table]
   c.execute("SELECT %s FROM pcfact_%s " % (fields,table))
   
   #print c.description

   colonnes = {}
   colname = {}
   i = 0
   for col in c.description:   
       colonnes[i] = {"name"  : col[0]}
       if col[0]==nom_clef:
           clef = i
       if col[0]==nom_valeur:
           valeur = i
       colname[i] = col[0]
       i=i+1

   #print colonnes
   
   valeurs = {}
   i = 0
   for ligne in c:
       j = 0
       u = list()
       for l in ligne:
           key = "%ss-%s" % (colname[j],l)
           #print "key : ",key
           if key in data.keys():
               u.append("%s (%s)" % (data[key],l))
           else:
               u.append(l)
           j = j+1
       #print ligne
       valeurs[i] = "</td><td>".join(map(lambda x:"%s"%x,u))
       data [ "%s-%s" % (table,ligne[clef]) ] = ligne[valeur]
       i=i+1
   
   #print data
   #print "valeurs : ",valeurs
    #print post_dict
   dt = datetime.now() 
   c = render_to_string('table.html' , {'date' : dt.strftime("%A, %d. %B %Y %I:%M%p"),
                                        'colonnes' : colonnes,
                                         'valeurs' : valeurs,
                                        'titre' : "Liste des %s" % table
                                               })
   return c
    

@cache_control(must_revalidate=True, max_age=6000)
def image(request , url,ext):
    filename = "../%s.%s" % (url,ext)
    if config.PORTAL_DEBUG:
        print "image : ---> ",filename
    if os.path.isfile(filename):   
        image_data = open(filename, "rb").read()
        return HttpResponse(image_data, mimetype="image/%s" % ext[1:])
    else:
        print "ZZZZZ image non existing : ",filename
        l=page_message("nothing yet!")
        return  HttpResponse(l)




def fichier_o(request , url):
    filename = "../%s" % url
    print "download ",filename,os.stat(filename).st_size
    l = HttpResponse(mimetype='application/force-download') 
    l['Pragma'] = 'no-cache'
    l['Cache-Control'] = 'no-cache must-revalidate proxy-revalidate'
    l['Content-Disposition']='attachment;filename="%s"'%filename
    l["X-Sendfile"] = filename
    l['Content-length'] = os.stat(filename).st_size
    return l


def fichier(request,url):
    filename = "../%s" % url
    basename = os.path.basename(filename)
    print "download ",filename,os.stat(filename).st_size,basename
    response = HttpResponse(FileWrapper(open(filename)),
                           content_type=mimetypes.guess_type(filename)[0])
    filename = "../%s" % url
    basename = os.path.basename(filename)
   
    response['Content-Length'] = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s" % basename
    return response
