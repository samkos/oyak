#!/usr/bin/env python
# Coded by Bahattin Vidinli, bvidinli@gmail.com
# msn/email: bvidinli@iyibirisi.com
# sites: www.ehcp.net, Easy Hosting Control Panel

import os,sys

print "php to python converter ... ver 0.003 \n"
print "# Coded by Bahattin Vidinli, bvidinli@gmail.com"
print "# msn/email: bvidinli@iyibirisi.com"
print "# sites: www.ehcp.net, Easy Hosting Control Panel"




#php=raw_input("input php code:")
# karakter karakter inputu analiz et..
nonchar=['(',')','"','',' ','!','{','}','=',"'",',',';','[',']','_']
bosluklar=[' ',"\t"]
enter="\n"
bosluk=' '
tab="\t"
blockstart='{'
blockend='}'

indentlevel=0
instring=False
out=''
line=''

def kelimeal(input):
	out=''
	for k in range(0,input.__len__()):
		if not input[k] in nonchar:
			out+=input[k]
		else:
			break
	out=out.strip()
	#print '('+out+')'
	return out

def degiskenadial(input):
	return kelimeal(input).replace('$','')

os.system('php codeparser2.php > php.beautiful.php') # this step may be skipped. put to make input file even better.
php=open('php.beautiful.php').read()
print "\nyour php code was:\n",php

prev=''
skipword=False
skipn=0
	
for k in range(0,php.__len__()): # bu tur yazinca, bir sonrasini, gerisini de takip edebiliyorsun..
	i=php[k]
	if skipn>0:
		skipn-=1
		continue
		
	if (not i in nonchar) and skipword:
		continue
	else:
		skipword=False
		
	#print i
	ekle=i
	
	
	
	# degisken isimlerinin temizlenmesi..
	if i=='$':
		if not(instring):
			ekle=''
		else:
			if prev=='\\':
				ekle=i
			else:
				degiskenadi=degiskenadial(php[k:k+30])
				#ekle='(degisken yazilacak:'+degiskenadi+')'
				ekle='"+'+degiskenadi+'+"'
				skipword=True
				
	if i=='"':
		instring=not instring
	elif i==blockstart:
		indentlevel+=1
		ekle=''
	elif i==blockend:
		indentlevel-=1	
		ekle=''
	elif i==tab and not instring:
		ekle=''	
	elif i==' ' and  prev in [enter,bosluk,tab] and not instring:
		ekle=''
	elif i==enter:		
		ekle=i+indentlevel*tab
		#print "line:("+line+')'			
		line=''		
	else:
		line+=i
		
		
	
	
	kelime=''
	if (not i in nonchar) and (prev in nonchar) and (k>0):
		kelime=kelimeal(php[k:k+30])
		
	if kelime=='elseif': #elseif leri alt satira at, kodu duzenlemek icin..
		ekle=enter+indentlevel*tab+ekle	
	
	if i=='[' and not instring:	# php nin ['xx'] seklindeki isimli arraylarini, python dictionary lere donustur..
		if php[k+1]=="'":
			arrayindexname=kelimeal(php[k+2:k+32])
			#print "arrayindexname is:",arrayindexname, " array:",php[k:k+20]
			ekle=".get('"+arrayindexname+"')"
			skipn=arrayindexname.__len__()+3
	if i=='!':	 # if(!$usernamefield) seklindeki php iflerini donusturur..
		if php[k+1] not in nonchar:
			degiskenadi=degiskenadial(php[k+1:k+31])
			skipn=degiskenadi.__len__()+1
			ekle="isEmpty("+degiskenadi+")"

	out+=ekle
	prev=i # onceki karakteri set et... \$ gibileri almak icin..

#print "ilk Cikti soyledir:\n",out


out2=''
blokbaslatan=['if(','if (','for(','for (','while(','while (','elseif','else']

print "\nikinci parse:"

satirlar=out.splitlines()

for k in range(0,satirlar.__len__()) :	
	ek=''
	i=satirlar[k]
	#print i.find('function ')
	
	for j in blokbaslatan:
		if i.find(j)>=0:
			#print "if v.b. bulundu"
			i+=':'
			break
	
	if i.find('//')>=0:
		yer=i.find('//')
		onceki=i[0:yer]
		tabsayisi=0
		if k<satirlar.__len__():
			tabsayisi=satirlar[k+1].count(tab)  # commenti alta at, altin tab sirasina uydur
		comment=(tabsayisi*tab)+i[yer:200]
		comment=comment.replace('//','#')
		i=onceki
		ek=comment+enter # commentleri alt satira at..
	
	if i.find('function ')>=0:
		#print "def koydu."
		i=i.replace('function','def')+':'
		
	i=i.replace('this->','self.').replace('===','==').replace('false','False').replace('elseif','elif').replace('true','True').replace('=>array(',':{').replace('=>',':')
	
	
	if i.strip()!=';':
		out2+=i+enter # ek commentler icin, 
	
	out2+=ek

#3. pars
out3=''
lines=out2.splitlines()
for i in lines:
	if i.strip()<>'':
		out3+=i+enter
		

print "\nikinci Cikti soyledir:\n",out3


