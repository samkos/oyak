
# -*- coding: latin-1 -*-
       
from fpdf import *
import os,sys,string
import exceptions, traceback

#import bookland

import barcode
from barcode.writer import ImageWriter
#print barcode.PROVIDED_BARCODES
EAN = barcode.get_barcode_class('ean13')


class PDF(FPDF):
	#Simple table
	def basic_table(self,header,data):
		#Header
		for col in header:
			self.cell(40,7,col,1)
		self.ln()
		#Data
		for row in data:
			for col in row:
				self.cell(40,6,col,1)
			self.ln()

	#Better table
	def oyak_table(self,x,y,w,header,data,height,countour=1):
		#Column widths
                self.set_xy(x,y)
                x=self.get_x()
		#Header
		if countour:
                   for i in range(0,len(w)):
		       self.cell(w[i],2,"",'T',0,'C')
                i=0
                justification= [""]*15
		if countour:
		   bords = 'LR'
		else:
                   bords = ' '
		# header of table
                if len(header):
                    justification = header[0]
                    for h in header[1:]:
                        if i:
                            self.set_xy(x,self.get_y()+3)
                        self.set_x(x)
                        for i in range(0,len(w)):
			    hx=h[i]	
                            self.set_font('Arial','B',8)
                            if hx.find("_s_")>-1:
                                self.set_font('Arial','B',6)
                                hx = string.replace(hx,"_s_","")
                            if hx.find("_b_")>-1:
                                self.set_font('Arial','B',12)
                                hx = string.replace(hx,"_b_","")
                            if hx.find("_h_")>-1:
                                self.set_font('Arial','B',20)
                                hx = string.replace(hx,"_h_","")
                            self.cell(w[i],7,hx,bords,align='C')
		    self.ln()
                    self.set_x(x)
		    if countour:
                       for i in range(0,len(w)):
                           self.cell(w[i],2,"",'T',0,'C')


		#Data
                self.set_font('Arial','',8)
		for row in data:
                    while len(row)<len(w):
                        row = row + ['']
                    #print row
                    self.set_x(x)
                    try:
                        i = 0
			while i<len(w): 
                            width = w[i]
			    r = row[i]
			    # ligne seule
			    if r=="T__jj__":
			       self.cell(sum(w),0,'','T')
			       break
			    # traitement d'un format particulier d'une colonne
                            if r.find("__bb__")>-1: 
				    (cadre,r) = r.split("__bb__")
			    else:
				    cadre = bords
			    # traitement d'une justification particuliere d'une colonne
                            if r.find("__jj__")>-1: 
				   (just,r) = r.split("__jj__")
				   if just=="g":
				     just="L"
				   elif just=="d":
				     just="R"
				   elif just=="c":
				     just="C"
			    else:
				   just = justification[i]
			    # traitement d'un format particulier d'une colonne
                            if r.find("__ff__")>-1: 
				    (format,r) = r.split("__ff__")
				    just=format[0]
				    for j in range(int(format[1])-1):
				      i=i+1
				      width = width+w[i]
				      #print "format,width",format,width
                            if r.find("__GRAS__")>-1:
                                self.set_font('Arial','B',8)
                                r = string.replace(r,"__gras__","")
                                r = string.replace(r,"__GRAS__","")
                            if r.find("_b_")>-1:
                                self.set_font('Arial','',12)
                                r = string.replace(r,"_b_","")
                            if r.find("_h_")>-1:
                                self.set_font('Arial','',14)
                                r = string.replace(r,"_h_","")
                            if r.find("_z_")>-1:
                                r = string.replace(r,"_z_","")
				print "includes images ",r
                                self.image(r,self.get_x(),self.get_y(),width,10*height,type='',link='')
				self.set_xy(self.get_x(),self.get_y()+20)
			    else:
			    #print "width,height,r,bords,0,just",width,height,r,bords,0,just
				self.cell(width,height,r,cadre,0,just)
				self.set_font('Arial','',8)
			    i = i+1
			self.ln() 
                    except:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        print "!!!!!!!!!!!!!!!!!!!!!!!!!"
                        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                                  file=sys.stderr)
                        print "zzzzzzzzzzzz erreur printing...."
                        for i in range(0,len(w)):
                            print w[i],height,row[i],justification[i]
                        
		#Closure line
	        if countour:
                   self.set_x(x)
		   self.cell(sum(w),0,'','T')

 

def print_facture(fics,output_file):

    pdf = PDF()
    pdf.set_auto_page_break(auto=False,margin=0)

    fics.sort()
    print fics

    for fic in fics:
      printer=print_one_facture(pdf,fic)

    pdf.output(output_file,'F')
    return printer

def print_one_facture(pdf,fic):
    print "processing facture ",fic

    fic_contents = open(fic).readlines()
    valeurs = {}
    for f in fic_contents:
        if f[-2:]=='\r\n':
            f = f[:-2]
        fields = f.split("!")
        id  = fields[0]
        if len(fields[1:])==1:
            valeurs[id] = fields[1]
        else:
            valeurs[id] = fields[1:]

    #print valeurs
    clefs = valeurs.keys()

    for i in range(9):
        for j in range(10):
            clef = 'Z%d,%d' % (i,j)
            if not ( clef in clefs):
                valeurs[clef]=" "


    (printer,n,title) = valeurs['Z0,1']
    facture = valeurs["Z1,1"]
    data_title =  [ [" "],["_b_%s" % valeurs["Z4,1"]]]
    header_title =  [ ["C"],["_h_"+title]]
    w_title  =  [160]
    x_title = 40
    y_title = 75


    header_entete=[]
    w_entete = [20,30]
    x_entete = 10
    y_entete = 10

    data_entete = [ ["C2__ff__%s N %s" % (title,valeurs['Z1,1']) ],
	            ["Date Facture" , valeurs['Z1,2']], 
                    ["Echeance   "  , valeurs['Z1,3']], 
                    ["Livraison N"  , valeurs['Z1,1']], 
                    ["Client N   "  ,  valeurs['Z1,5']], 
                    ["           "  , valeurs['Z1,6']], 
                    ["N  TVA Client", valeurs['Z1,7']], 
                    ["Total        ", valeurs['Z1,8']] ] 
     

    header_adresse=[]
    w_adresse = [60]
    x_adresse = 120
    y_adresse = 40
    data_adresse = [ [valeurs['Z3,1']], 
                     [valeurs['Z3,2']], 
                     [valeurs['Z3,3']], 
                     [valeurs['Z3,4']], 
                     [valeurs['Z3,5']], 
                     [valeurs['Z3,6']], 
                     [valeurs['Z3,7']] ] 


    header_fac = [ ["C","L","C","C","R",
                    "C","R","R","R","R"],
                   ["Article","Designation","Zone","Vd","Colis",
                    "Poids","Poids","Prix","Total","TVA"],
                   ["","","Peche","","",
                    "Unit.","Quant.","Unit.","H.T.",""]]
    w_fac = [10,85,25,10,20,10,10,10,15,7]
    x_fac = 5
    y_fac = 95
    data_facture = []
    taille_designation = int(w_fac[1]/1.7)
    i=1
    while 'Z5,%d'%i in clefs:
        v = valeurs['Z5,%d'%i]
	designation = v[1]
	designation_suite = False
	if len(designation)>taille_designation:
		designation_suite = designation[taille_designation:]
		designation = designation[:taille_designation]
	v[1] = designation
        data_facture = data_facture + [ v ]
	#print v
        i=i+1
	if designation_suite:
		while designation_suite:
		   w = copy.deepcopy(v)
		   for j in range(len(w)):
	              w[j] = ' '
		   w[1] = designation_suite[:taille_designation]
		   data_facture = data_facture + [ w ]
		   #print w
		   designation_suite = designation_suite[taille_designation:]

    #print data_facture
    nb_ligne_fac_page =  20

    header_footer1 = [["C"    ,"R"    ,"R"     ,"R"      ,"R"     ,"R"       ,"R"        ,"R"        ],
                      ["Colis","Poids","H.T. 1","TVA 5.5","H.T. 2","TVA 19.6","Total TVA","Total TTC"]]
    w_footer1      = [10     ,15     ,15      ,15       ,15      ,15        ,15         ,15         ]
    x_footer1 = 90
    y_footer1 = 210

    data_footer1 =  [ valeurs['Z6,1'], 
                      #[valeurs['Z7,1']],
                      ] 

    header_footer2 = [["L"               ,"R"            ,"R"          ,"R"           ,"R" ,"R"        ],
                      ["Règlement Client","Date","_s_N de Facture","_s_Ancien Solde","_s_au","_s_Nouveau Solde"]]
    w_footer2      =  [50                ,15   ,15                ,15               ,15      ,15        ]
    x_footer2 = 80
    y_footer2 = 230
    data_footer2 =  [ valeurs['Z8,1']] 


    # data_vignette = [ ["Facture ",facture], 
    # 		      ["Montant ",valeurs['Z6,1'][-1]], 
    #                   ["Ancien solde ",valeurs['Z8,1'][3]], 
    #                   ["Au ",valeurs['Z8,1'][4]],
    #                   ["Nouveau solde ",valeurs['Z8,1'][5]], 
    #                   ] 

    # header_vignette =  []
    # w_vignette      =  [20,20]
    # x_vignette = 168
    # y_vignette = 275


    header_vignette = [["L"                   ,"R"               ,"R"               ,"R"      ,
			"R"                   ,"C"               ,"R"  ],
		       ["Raison social Client", "_s_Date Facture","_s_N de Facture","_s_Montant",
		       "_s_Ancien Solde"      ,"_s_au","_s_Nouveau Solde"]]
    w_vignette      =  [40                    ,25                ,20               ,17         ,
			17                    ,17                ,17         ]
    x_vignette = 25
    y_vignette = 284
    print len(valeurs['Z8,1']),valeurs['Z8,1']
    data_vignette =  [ [ valeurs['Z8,1'][0], valeurs['Z8,1'][1], valeurs['Z8,1'][2], valeurs['Z6,1'][7], 
		       valeurs['Z8,1'][3], valeurs['Z8,1'][4], valeurs['Z8,1'][5]]
                      ] 


 


    #Data loading




    while len(data_facture):
        data_page = []
        i=0
        while len(data_facture) and i<nb_ligne_fac_page:
            x = data_facture.pop(0)
            data_page.append(x)
            i=i+1
        #print data_page,len(data_facture)
        pdf.add_page()
        pdf.oyak_table(x_entete,y_entete,w_entete,header_entete,data_entete,4)
        pdf.oyak_table(x_adresse,y_adresse,w_adresse,header_adresse,data_adresse,4,countour=0)
        pdf.oyak_table(x_fac,y_fac,w_fac,header_fac,data_page,4)
        pdf.oyak_table(x_footer1,y_footer1,w_footer1,header_footer1,data_footer1,4)
        pdf.oyak_table(x_footer2,y_footer2,w_footer2,header_footer2,data_footer2,4)
        pdf.oyak_table(x_vignette,y_vignette,w_vignette,header_vignette,data_vignette,4)
        pdf.oyak_table(x_title,y_title,w_title,header_title,data_title,4,countour=0)

    pdf.set_font('Arial','',14)
    
    return printer





def print_general(fic,output_file,debug_till=0):
    print "processing general file ",fic,debug_till


    fic_contents = open(fic).readlines()
    printed_at_each_page = []
    OUT = False


    while len(fic_contents) and not(OUT):
        f = fic_contents.pop(0)	     
        if f[-2:]=='\r\n':
            f = f[:-2]
        fields = f.split("!")
	#print fields
        what  = fields.pop(0).strip()
	#print what
	page_number = 1

	
	if what=="Z0,1":
	    (printer,copies,document,orientation) = fields	
	    print "orientation:",orientation
	    pdf = PDF(orientation)
	    pdf.set_auto_page_break(auto=False,margin=0)
	    pdf.set_font('Arial','',14)
	    pdf.add_page()
    
	    nb_ligne = 0
	    current_ligne = 0
	    esp_ligne = 0.2
	    esp_tab_ligne = 0.43 
	    data_tab = []
	    continue

	if what=="EJECT" or (orientation=="landscape" and current_ligne>15) or (current_ligne>60):
	   nb_ligne = 0
	   current_ligne = 0
	   if len(data_tab):
              pdf.oyak_table(x_tab,y_tab,w_tab,first_line_tab,data_tab,4)
           print "EJECT§!!!!!!!!!!!"
           pdf.add_page()
	   page_number = page_number+1
	   for l in printed_at_each_page:
		   [x,y,texte] = l
		   if texte.find("__numero_page__")>-1:
		     texte = string.replace(texte,"__numero_page__","%d" % page_number)
		   pdf.oyak_table(x,y,[10],[],[[texte]],4,countour=0)
	   data_tab = []
	   continue

	y = fields.pop(0).strip()
	x = fields.pop(0).strip()
	if x=="." and y==".":
	    current_ligne = current_ligne + esp_ligne
	    x = 1
	    y = current_ligne
	    
	#print fields
	if what[:3]=='TXT':
            texte = fields.pop(0)
	    x = int(x)*3+5
	    y = int(y)*4   
	    #print "x=/%s/,y=/%s/,texte=/%s/"%(x,y,texte)
	    if texte.find("__on_all_pages__")>-1:
	      texte = string.replace(texte,"__on_all_pages__","")
	      printed_at_each_page.append([x,y,texte])
	    if texte.find("__numero_page__")>-1:
	      texte = string.replace(texte,"__numero_page__","%d" % page_number)
	    pdf.oyak_table(x,y,[10],[],[[texte]],4,countour=0)
	    current_ligne = current_ligne + esp_ligne
	    
	    continue


	if what=="TAB":
	    print fields[0]
	    tailles = fields.pop(0).strip().split("=")
	    w_tab = tailles
	    for i in range(len(tailles)):
              w_tab[i] = int( float(w_tab[i])*40)
	    if debug_till:
	      print "tailles",w_tab
	    x_tab = pdf.get_x()
	    y_tab = pdf.get_y()
	    header_tab = ""
	    first_line_tab = []
	    if debug_till:
	      print "nb colonnes :",len(tailles)
	      print tailles
	    nb_test = 0
	    if len(fields):
	        tailles = fields.pop(0).strip().split("=")
	        if debug_till:
		   print "tailles",tailles
	    current_ligne = current_ligne + esp_ligne
	    data_tab = []
	    while len(fields):
                nb_test = nb_test + 1
	        if nb_test < debug_till:
                   debug = True
		else:
                   debug = False                   
	        line = fields.pop(0)
		cells = line.split("=")
		if debug:
		  print "---- Ligne %d --------" % nb_test
		  print cells
		nb_cell = 0
		data_ligne=[]
		for cell in cells:
                    if debug:
		      print "cell(%d)=/%s/" % (nb_cell,cell)
		    nb_cell = nb_cell + 1
		    champs = cell.split(";")
		    texte = champs.pop(0)
		    cadrage,bords,couleur,font = "xx","xx","xx","xx"
		    if len(champs):
		      format = champs.pop(0)
		      if len(format):
		         cadrage=format[0]
			 texte = "%s__jj__%s" % (cadrage,texte)
			 format=format[1:]
		      if len(format):
		         bords=format[0]
			 if bords=="g":
                           bords = "L"
			 elif bords=="d":
                           bords = "R"
			 elif bords=="c":
                           bords = "LR"
			 if not bords==".":
                           texte = "%s__bb__%s" % (bords,texte)
			 format=format[1:]
		      if len(format):
		         couleur=format[0]
			 if couleur=="g":
                            texte = "__GRAS__%s__gras__" % texte_
			 if couleur=="i":
                            texte = "__SLANTED__%s__slanted__" % texte_
			 if couleur=="G":
                            texte = "__GRAY__%s__GRAY__" % texte_
			 if couleur=="r":
                            texte = "__RED__%s__red__" % texte_
			 format=format[1:]
		      if len(format):
		         font=format[0]
			 if not font==".":
  			   texte = "__%s__%s" % (font,texte)
			 format=format[1:]
		    data_ligne.append(texte)
		    if debug:
		      print "texte=/%s/,cadrage=%s,bords=%s,couleur=%s,font=%s" % (texte,cadrage,bords,couleur,font)
		if debug:
                  print data_ligne
		if len(first_line_tab)==0:
                  first_line_tab=data_ligne
		  centering = []
		  title = []
		  for c in range(len(first_line_tab)):
		    r = first_line_tab[c]	  
		    if r.find("__bb__")>-1: 
		      (cadre,r) = r.split("__bb__")
		    # traitement d'une justification particuliere d'une colonne
		    if r.find("__jj__")>-1: 
		      (just,r) = r.split("__jj__")
		    else:
		      just = "C"
		    centering.append(just)
		    title.append(r) #"%s/%s"%(r,just))
		  header_tab = [ centering, title]
		  print "header:", header_tab
		else:
                  data_tab.append(data_ligne)
		current_ligne = current_ligne +1
		if current_ligne>35:
                  nb_ligne = 0
		  current_ligne = 0
		  if len(data_tab):
                    pdf.oyak_table(x_tab,y_tab,w_tab,header_tab,data_tab,4)
		  if debug:
		     print "EJECT§!!!!!!!!!!!"
		  pdf.add_page()
		  page_number = page_number+1
		  data_tab = []
		  for l in printed_at_each_page:
		    [x,y,texte] = l
		    if texte.find("__numero_page__")>-1:
		      texte = string.replace(texte,"__numero_page__","%d" % page_number)
		    pdf.oyak_table(x,y,[10],[],[[texte]],4,countour=0)
		OUT = True
	    if len(data_tab):
              pdf.oyak_table(x_tab,y_tab,w_tab,header_tab,data_tab,4)

    pdf.output(output_file,'F')
    return printer
	    	
if __name__ == "__main__":
    #print_facture("TESTS/fac/FACT1plus","tuto5.pdf",marge=1)
    #print_general("../print/tests/imp/PAYSAGE.txt","tuto5.pdf")
    #print_general("../print/tests/imp/TEST0.txt","tuto5.pdf")
    print_general("../print/tests/imp/VEND2.txt","tuto5.pdf",4)
    #print_catalog("../print/tests/stock/example","tuto5.pdf")
    if sys.platform.startswith("linux"):
	    os.system("evince tuto5.pdf")
