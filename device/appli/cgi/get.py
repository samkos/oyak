#!/usr/bin/python
##c:/Python27/python.exe
 
import cgi
import os
import sys

form = cgi.FieldStorage()
 
val1 = form.getvalue('data')


try:
    templates = [ "/datadevice/%s.txt" ,"../../data/%s.txt"]

    out = False

    for t in templates :

        filename = t % val1
        

        if os.path.exists(filename):
            print  >> sys.stderr, "sending ",filename
            f = open(filename,"r")
            data = f.readlines()
            f.close()
            out = data[0]
        else:
            print >> sys.stderr, "testing %s with no success " % filename

    if out==False:
        out = "ERROR File /%s/ not exists" % val1

except:
    out = "EXCEPTION"
    print >> sys.stderr, out
 

print >> sys.stderr, out

if True:
   print """
%s
""" % out 
