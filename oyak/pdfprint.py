from fpdf import *
import os

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
                            self.cell(w[i],7,h[i],'LR',align='C')
                    self.ln()
                    self.set_x(x)
                    for i in range(0,len(w)):
                        self.cell(w[i],2,"",'T',0,'C')
		#Data
		for row in data:
                    while len(row)<len(w):
                        row = row + ['']
                    #print row
                    self.set_x(x)
                    for i in range(0,len(w)):
                        self.cell(w[i],height,row[i],'LR',0,justification[i])
                    self.ln()
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

    data_entete = [ ["Date Facture" , valeurs['Z1,2']], 
                    ["Echeance   "  , valeurs['Z1,3']], 
                    ["Livraison N"  , valeurs['Z1,1']], 
                    ["Client N   "  ,  valeurs['Z1,5']], 
                    ["           "  , valeurs['Z1,6']], 
                    ["N  TVA Client", valeurs['Z1,7']], 
                    ["Total        ", valeurs['Z1,8']] ] 
     
    data_adresse = [ [valeurs['Z3,1']], 
                     [valeurs['Z3,2']], 
                     [valeurs['Z3,3']], 
                     [valeurs['Z3,4']], 
                     [valeurs['Z3,5']], 
                     [valeurs['Z3,6']], 
                     [valeurs['Z3,7']] ] 

    data_facture = []
    i=1
    while 'Z5,%d'%i in clefs:
        data_facture = data_facture + [ valeurs['Z5,%d'%i]]
        i=i+1
    #print data_facture

    pdf = PDF()

    #Data loading
    pdf.set_font('Arial','',8)
    pdf.add_page()
    pdf.oyak_table(10,10,[20,30],[],data_entete,4)
    pdf.oyak_table(120,40,[60],[],data_adresse,4,countour=0)
    header = [ ["C","L","C","C","R",
                "C","R","R","R","R"],
               ["Article","Designation","Zone","Vd","Colis",
                "Poids","Poids","Prix","Total","TVA"],
               ["","","Peche","","",
                "Unit.","Quant.","Unit.","H.T.",""]]
    w = [10,85,25,10,20,10,10,10,15,7]
    print "w, h, d_fact ",len(w),len(header),len(data_facture[0])
    pdf.oyak_table(5,80,w,header,data_facture,5)
    pdf.set_font('Arial','',14)
    pdf.output('tuto5.pdf','F')
     
    os.system("evince tuto5.pdf")



if __name__ == "__main__":
    print_facture("TESTS/fac/BL",0)
