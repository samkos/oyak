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
    codebarlist.append((code,0.0,"xxxxxxx"))
    if debug:
        print code,lots
    #arrivage,vente_cumulee,stock_fin_de_journee,es,s = lots.split("\\")
    #if debug:
    #    print code,arrivage,vente_cumulee,stock_fin_de_journee

#codebarlist = [(code,0.0,"xxxxxxx")]

#print codebarlist

# All the basic versions:

texte = """
   \\documentclass[a4paper]{article}
   %
   \\usepackage{graphicx}
   %
   \\setlength{\\voffset}{-6.5cm}
   \\setlength{\\hoffset}{-2.6cm}

   \\setlength{\\oddsidemargin}{0pt}
   \\setlength{\\evensidemargin}{0.5cm}

   \\setlength{\\textwidth}{550pt}

   \\setlength{\\topmargin}{1cm}
   \\setlength{\\textheight}{26cm}

   \\setlength{\\headheight}{90pt}

   \\setlength{\\headsep}{0pt}
   \\setlength{\\parindent}{1cm}
   \\setlength{\\parskip}{0.2cm}

   \\setlength{\\marginparwidth}{0pt}
   \\setlength{\\marginparsep}{0pt}
   %
   \\begin{document}

   \\begin{small}

   \\begin{tabular}{|c|c|c|c|c|c|}
   \\hline
"""


n=1
l=1
for isbn,price,comment in codebarlist:
    outfile="codes/%s.eps" % isbn
    if not(os.path.exists(outfile)):
        n=n+1
        #print "depart : "+str(isbn)
        print "generating : ",isbn
        b = bookland.ean13print(isbn,price)
        #b = bookland.upc5print(isbn,price)
        b.ps.out(outfile)
        #print "\\foo{%s}{%s \\\\bookland.py %s}" % (outfile,comment,version)
    texte = texte + "\n \includegraphics[height=1.5 cm,width=4 cm]{%s} &  " % outfile
    texte = texte + " %s  & %s & %s \\\\ \\hline  " % (isbn,"produit",999)
    l=l+1
    if l==10:
        texte = texte + "  \\ \hline \end{tabular} \eject \n"
        texte = texte + "\\begin{tabular}{|c|c|c|c|c|c|} \hline"
        l=0
        
    
texte = texte + " \\hline \\end{tabular}    \\end{small} \\end{document}\n"

f = open("es.tex","w")
f.write(texte)
f.close()
os.system("pdflatex es")

#print texte
#nn = input("<fin du programme>")


