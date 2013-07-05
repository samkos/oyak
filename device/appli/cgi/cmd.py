#!/usr/bin/python
##c:/Python27/python.exe
 
import cgi
import os
import sys
import time

if sys.platform.startswith("linux"):
    TMPDIR="/tmp"
else:
    TMPDIR="c:"

dir_Root=TMPDIR+'/Oyak/'
dir_Commande=TMPDIR+'/ventesjours/'
commande_counter_file="%s/%s" % (dir_Commande,"counter.txt")
commande_counter=0

# get counter value
if not(os.path.exists(commande_counter_file)):
    f = open(commande_counter_file,'w')
    f.write("%d" % commande_counter)
    f.close()

f = open(commande_counter_file,'r')
scommande_counter=f.readlines()
commande_counter = int(scommande_counter[0])
f.close()    


form = cgi.FieldStorage()
 
val1 = form.getvalue('data')
print >> sys.stderr, val1


#try:
if True:
    commande_counter = (commande_counter+1)%1000
    name_file="%s/%s%03d%s" % (dir_Commande,time.strftime("%Y%m%d"),
                               commande_counter,1)
    f = open(name_file,"w")
    f.write(val1)
    f.close()
    f = open(commande_counter_file,'w')
    f.write("%d" % commande_counter)
    f.close()

    out = "0"

#except:
else:
    out = "EXCEPTION"
 
#print >> sys.stderr, out



if True:
   print """
%s
""" % out 
