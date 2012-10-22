# Create your views here.
import os, sys, time, string

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


import sqlite3
ROOT_PATH = os.path.dirname(__file__)
print "ouverture base %s/../db.sqlite" % ROOT_PATH
conn = sqlite3.connect('%s/../db.sqlite' % ROOT_PATH)
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
    if url in ("fournisseurs","vendeurs"):
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
        filename = "../%s" % url
        if config.PORTAL_DEBUG:
            print "[VIEW]  fichier : ---> ",filename
        if os.path.isfile(filename):
            l = open(filename,"r").read()
        else:
            print "[VIEW]  ZZZZZ file non existing : ",filename
            l=page_message("nothing yet!")
    return  HttpResponse(l)



def browse(table):
 
   c = conn.cursor()  
   c.execute("SELECT * FROM pcfact_%s " % table)
   
   print c.description

   colonnes = {}
   i = 0
   for col in c.description:   
       colonnes[i] = {"name"  : col[0]}
       i=i+1

   print colonnes

   i = 0
   for ligne in c:

       print ligne
       # post_dict[i] = {
       #     "id" : row.id,
       #     "tweet":row.tweet,
       #     "author":  row.author,
       #     "published":row.published,
       #     "read":row.read
       #     }
       i=i+1

    #print post_dict
   c = render_to_string('index.html' , {'oyak_version': config.oyak_version, 
                                               'table' : table
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
    response['Content-Length'] = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s" % basename
    return response
