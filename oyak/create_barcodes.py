#!/usr/local/bin/python

import bookland
reload(bookland)
import os

version = "%s %s" % (bookland.MYVERSION, bookland.DATE)

debug = False

# import barcode from test

codebarlist = list()

f = open("../print/tests/stock/example","r")
for l in f.readlines():
    code,lots = l[:-1].split("]")
    if debug:
        print code,lots
    #arrivage,vente_cumulee,stock_fin_de_journee,es,s = lots.split("\\")
    #if debug:
    #    print code,arrivage,vente_cumulee,stock_fin_de_journee

codebarlist = [(code,0.0,"xxxxxxx")]

print codebarlist

# All the basic versions:

n=1
for isbn,price,comment in codebarlist:
    outfile="%s.eps" % isbn
    if not(os.path.exists(outfile)):
        n=n+1
        #print "depart : "+str(isbn)
        #print "generating : ",isbn
        b = bookland.ean13print(isbn,price)
        #b = bookland.upc5print(isbn,price)
        b.ps.out(outfile)
        #print "\\foo{%s}{%s \\\\bookland.py %s}" % (outfile,comment,version)


#nn = input("<fin du programme>")


