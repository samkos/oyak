# -*- coding: latin-1 -*-
       
from fpdf import *
import os,sys,string
import exceptions, traceback

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
                for i in range(0,len(w)):
                    self.cell(w[i],2,"",'T',0,'C')
                i=0
                justification= [""]*15
                if len(header):
                    justification = header[0]
                    for h in header[1:]:
                        if i:
                            self.set_xy(x,self.get_y()+3)
                        self.set_x(x)
                        for i in range(0,len(w)):
			    hx=h[i]	
                            self.set_font('Arial','B',8)
                            if h[i].find("_s_")>-1:
                                self.set_font('Arial','B',6)
                                hx = string.replace(h[i],"_s_","")
                            self.cell(w[i],7,hx,'LR',align='C')
                    self.ln()
                    self.set_x(x)
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
                        for i in range(0,len(w)):
                            if row[i].find("__GRAS__")>-1:
                                self.set_font('Arial','B',8)
                                row[i] = string.replace(row[i],"__gras__","")
                                row[i] = string.replace(row[i],"__GRAS__","")
                            self.cell(w[i],height,row[i],'LR',0,justification[i])
                            self.set_font('Arial','',8)
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
                self.set_x(x)
		self.cell(sum(w),0,'','T')

 


def print_facture(fic,mode):
    print "processing ",fic,"mode :",mode

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
                valeurs[clef]="xxx"

    header_entete=[]
    w_entete = [20,30]
    x_entete = 10
    y_entete = 10
    data_entete = [ ["Date Facture" , valeurs['Z1,2']], 
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
    y_fac = 80
    data_facture = []
    i=1
    while 'Z5,%d'%i in clefs:
        data_facture = data_facture + [ valeurs['Z5,%d'%i]]
        i=i+1
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
                      ["R�glement Client","Date","_s_N de Facture","_s_Ancien Solde","_s_au","_s_Nouveau Solde"]]
    w_footer2      =  [40                ,15            ,15            ,15            ,15  ,15        ]
    x_footer2 = 90
    y_footer2 = 230
    data_footer2 =  [ valeurs['Z8,1']] 


    data_vignette = [ ["Facture ",valeurs['Z8,1'][0]], 
                      ["Montant ",valeurs['Z8,1'][1]], 
                      ["Ancien solde ",valeurs['Z8,1'][2]], 
                      ["Au ",valeurs['Z8,1'][3]],
                      ["Nouveau solde ",valeurs['Z8,1'][4]], 
                      ] 

    header_vignette =  []
    w_vignette      =  [20,30]
    x_vignette = 158
    y_vignette = 256

    pdf = PDF()

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

    pdf.set_font('Arial','',14)
    pdf.output('tuto5.pdf','F')
     
    os.system("evince tuto5.pdf")



if __name__ == "__main__":
    print_facture("TESTS/fac/BL",0)