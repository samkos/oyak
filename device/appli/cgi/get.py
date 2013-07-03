#!c:/Python27/python.exe
 
import cgi
import os

form = cgi.FieldStorage()
 
val1 = form.getvalue('data')

try:
    filename = "/datadevice/%s.txt" % val1

    if os.path.exists(filename):
        print "sending ",filename
        f = open(filename,"r")
        data = f.readlines()
        f.close()
        out = data[0]
    else:
        out = "ERROR"
except:
    out = "EXCEPTION"
    print os.stderr,out
print """%s""" % out
 

print out



# if False:
#    print """
# <html><head><title>Test URL Encoding</title></head><body>
# Hello my name is %s %s
# </body></html>""" % (val1, out)
