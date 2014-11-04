#!/usr/bin/env python
# -*- coding: utf-8 -*-

##	@package suivStar
#	@author J. Massot
#	@date 2014-05-07
#
#	@brief Traking a star over time

import pyfits
import csv
import numpy

from decimal import getcontext, Decimal
getcontext().prec = 20

class Source:	
	def __init__( self , ra_ , dec_ , mag_ , t_="" ):
		self.ra  = ra_
		self.dec = dec_
		self.mag = mag_
		self.t   = t_
		self.id  = ""
	
	def setId( self , id_ ):
		self.id = id_
	def getId( self )
	
	def __str__(self):
		return str(self.ra) + "," + str(self.dec) + " , " + str(self.mag) + " , " + str(self.t) 

def cmpSrc( s1 , s2 ):    
    if s1.t == s2.t: return 0
    if s1.t >  s2.t: return 1
    return -1

def computeABmag(data,fluxMag0):
	global i
	flux  = Decimal('3.63078E-20') * Decimal(data.field('flux_psf')[i]) / fluxMag0
	ABmag = Decimal('-2.5') * flux.log10() - Decimal('48.6')
	
	return ABmag

sdss = Source(0.0968829171351,0.0132799318858,18.339314672683689882)

listNumFits = ['007112-u5-0105', '007112-u5-0106', '005566-u5-0265', '005566-u5-0266', '006421-u5-0465', '006421-u5-0464', '006430-u5-0467', '006430-u5-0466', '004895-u5-0073', '006474-u5-0466', '006383-u5-0267', '006383-u5-0266', '005642-u5-0112', '005642-u5-0113', '006409-u5-0266', '006513-u5-0466', '006552-u5-0466', '002650-u5-0013', '006559-u5-0466', '007177-u5-0117', '007121-u5-0466', '007170-u5-0465', '006283-u5-0125', '006484-u5-0467', '005765-u5-0031', '005765-u5-0032', '002708-u5-0145', '004253-u5-0145', '006934-u5-0145', '002662-u5-0319', '002662-u5-0320', '006584-u5-0333', '004188-u5-0147', '007202-u5-0339', '004153-u5-0149', '004153-u5-0150', '002649-u5-0158', '002649-u5-0159', '007140-u5-0468', '007117-u5-0159', '006504-u5-0469', '006314-u5-0363', '006314-u5-0364', '004128-u5-0160', '006564-u5-0470', '006564-u5-0471', '006373-u5-0162', '005622-u5-0472', '007034-u5-0165', '007034-u5-0166', '006577-u5-0473', '006577-u5-0472', '006600-u5-0473', '006600-u5-0474', '002768-u5-0169', '003437-u5-0380', '004927-u5-0389', '006414-u5-0220', '005813-u5-0476', '004858-u5-0391', '006982-u5-0233', '004917-u5-0479', '005898-u5-0480', '005898-u5-0481', '004868-u5-0245', '007106-u5-0480', '007195-u5-0396', '005744-u5-0245', '005744-u5-0246', '004198-u5-0399', '006963-u5-0052', '006963-u5-0053', '006533-u5-0484', '006533-u5-0485', '004933-u5-0399', '004933-u5-0400', '005603-u5-0485', '003384-u5-0406', '007155-u5-0486', '004207-u5-0408', '004207-u5-0409', '004849-u5-0491', '004849-u5-0492', '001755-u6-0413', '005709-u5-0491', '005709-u5-0492', '005781-u5-0416', '005781-u5-0417', '005770-u5-0419', '005800-u5-0438', '005800-u5-0439', '005759-u5-0439', '007054-u5-0439', '005823-u5-0442', '005823-u5-0443', '005590-u5-0446', '005590-u5-0447', '002728-u5-0450', '005633-u5-0452', '005633-u5-0453', '006461-u5-0454', '006461-u5-0453', '004874-u5-0458', '005792-u5-0458', '005918-u5-0458', '005878-u5-0459', '005878-u5-0460', '006441-u5-0459', '006441-u5-0460', '007080-u5-0460', '007080-u5-0461', '007047-u5-0012']


# open Science_Ccd_Exposure.csv to find fluxMag0 and time

csvFile = '/afs/in2p3.fr/home/j/jmassot/compareSrc/Science_Ccd_Exposure.csv'
timeCol = 30
fluxMagCol = 36	

fluxTime = {}
with open(csvFile, 'rb') as inputFile:
	reader = csv.reader( inputFile )
	
	for row in reader:
		for numFits in listNumFits:
			run = str(int( numFits[0:6] ))
			c   = numFits[8]
			b   = numFits[7]
			path = "sci-results/" + run + "/" + c + "/" + b + "/calexp/calexp-" + numFits + ".fits"
			
			if row[-1] == path:
				fluxTime[ numFits ] = ( row[ fluxMagCol ] , row[ timeCol ] )
				break

listSrc = []

PATH_DATA = "/sps/lsst/dev/jmassot/data/asso/"

for numFits in listNumFits:
	
	assoFile = PATH_DATA + "src-same-" + numFits[0:8] + ".csv"
	with open(csvFile, 'rb') as inputFile:
		reader = csv.reader( inputFile )
		
		for row in reader:
			
			
	


for numFits in listNumFits:
	
	run = str(int( numFits[0:6] ))
	c   = numFits[8]
	b   = numFits[7]
	PATH_DATA = "/sps/lsst/data/dev/lsstprod/DC_2013_one_percent/calexp_dir/sci-results/" + run + "/" + c + "/" + b
	
	## @def srcFits
	#  @brief path and name of src fits file
	srcFits = PATH_DATA + "/src/src-"+ numFits +".fits"

	src  = pyfits.open(srcFits)
	data = src[1].data
	src.close()
	
	coords = data.field('coord')
	#print "\tsources : " + str(len(coords))
	
	#search fluxMag0 and time
	#fluxMag0, time = searchFluxMag0(numFits)
	
	for i in range(len( coords )):
		tmpList = []
		if ( sdss.ra  - 0.0006 < coords[i][0] < sdss.ra  + 0.0006 ) and ( sdss.dec - 0.01 < coords[i][1] < sdss.dec + 0.01 ) :
						
			#compute ABmag
			ABmag = computeABmag(data,Decimal(fluxTime[numFits][0]))
						
			tmp = Source( coords[i][0] , coords[i][1] , ABmag , fluxTime[numFits][1] )
			#print tmp
			#add source to list
			#tmpList.append( tmp )
			listSrc.append(tmp)
	
	#print numFits + "=== " + str(len(tmpList)) + " ==="	
	#if len(tmpList) > 1:
	#	print "\e[101m YOP !!!"
	
			
	#try:
	#	listSrc.append( tmpList )
	#except:
	#	listSrc

listSrc.sort(cmp=cmpSrc)
for i in listSrc:
	print i

