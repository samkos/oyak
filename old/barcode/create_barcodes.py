#!/usr/local/bin/python

import bookland
reload(bookland)
import os

version = "%s %s" % (bookland.MYVERSION, bookland.DATE)

import what


# All the basic versions:

n=1
for isbn,price,comment in what.codebarlist:
    outfile="%s.eps" % isbn
    if not(os.path.exists(outfile)):
        n=n+1
        #print "depart : "+str(isbn)
        #print "generating : ",isbn
        try:
            b = bookland.ean13print(isbn,price)
            #b = bookland.upc5print(isbn,price)
            b.ps.out(outfile)
            #print "\\foo{%s}{%s \\\\bookland.py %s}" % (outfile,comment,version)
        except:
            print "error generating : ",isbn
            #print "\\foo{%s}{%s \\\\bookland.py %s}" % (outfile,comment,version)


#nn = input("<fin du programme>")


