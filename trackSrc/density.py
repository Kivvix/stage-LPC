#!/usr/bin/env python
# -*- coding: utf-8 -*-

## @package density
#  @author J. Massot
#  @date 2014-04-30
#
#  @brief Calculate density of pictures into strip 82
#	
#  @details Search all coordinates of each `fits` file and count density

from numpy import *
import math
# to manipulate fits files
import pyfits

import csv
import glob

## @def RA_BEG RA_END
#  @brief begin and end of field in RA 
RA_BEG = 5.0
RA_END = 7.5

DEC_BEG = -1.2
DEC_END =  1.2

## @def RA_N DEC_N
#  @brief number of division in RA and Dec
RA_N  = 1000
DEC_N = 100

## @def RA_A RA_B
#  @brief coeficient of equation y = RA_A*x + RA_B to convert coordinates into indices on matrix (x coordinate, y indice)
RA_A = (RA_N)/(RA_END - RA_BEG)
RA_B = -1.0*RA_A*RA_BEG

DEC_A = (DEC_N)/(DEC_END - DEC_BEG)
DEC_B = -1.0*DEC_A*DEC_BEG

## @def fname
#  @brief name of output file
fname = "density.csv"

## @fn foncfg
#  @brief global function of f(u,v) et g(u,v)
#	
# @param L   lettre of matrix name (A ou B)
# @param img object containing all data on the image of the current calexp
# @param u   variables intermediate calculation `SKY1_CRVAL1` and `SKY2_CRVAL2`
# @param v   same as u
#	
# @return r value of $f(u,v)$ or $g(u,v)$ according to the value of L
def foncfg(L,img,u,v):
	r = 0
	for p in range( 0 , img[L+"_ORDER"] ):
		for q in range( 0 , img[L+"_ORDER"]-p ):
			try:
				# security to confirm L_p_q
				a = img[L+"_"+str(p)+"_"+str(q)]
			except:
				a = 0.0
			r += a * (u**p) * (v**q)

	return r

## @fn f
#  @brief see function `#foncfg` for more information
#
# @return f(u,v)
def f(img,u,v):
	return foncfg('A',img,u,v)

##	fn g
#	@ see function `#foncfg` for more information
#	@return g(u,v)
def g(img,u,v):
	return foncfg('B',img,u,v)

## @fn X
#  @brief Compute vector with `SKY1_CRVAL1` et `SKY2_CRVAL2` value
#	
# @param img object containing all data on the image of the current calexp
# @param u   variables intermediate calculation `SKY1_CRVAL1` and `SKY2_CRVAL2`
# @param v   same as u
#	
# @return X matrix (one column) with coordonate of `SKY1_CRVAL1` and `SKY2_CRVAL2`
def X(img,u,v,CD):
	fuv = f(img,u,v)
	guv = g(img,u,v)
	Y = matrix(str(u+fuv) + " ; " + str(v+guv))
	
	X = CD*Y
	X = X + matrix( str(img["CRVAL1"]) + " ; " + str(img["CRVAL2"]) )
	
	return X


## @fn CD
#  @brief matrix to calculate `SKY1_CRVAL1` and `SKY2_CRVAL2`
#	
# @param img object containing all data on the image of the current `calexp`
#	
# @return CD matrix to calculate `SKY1_CRVAL1` and `SKY2_CRVAL2`
def CD(img):
	return matrix( str(img["CD1_1"]) + " " + str(img["CD1_2"]) + " ; " + \
	               str(img["CD2_1"]) + " " + str(img["CD2_2"]) )

## @fn coord
#  @brief compute extreme coordinates of current `calexp`
#
# @param fits name of fits file
#
# @return coordMin,coordMax list of matrix with extreme coordinates
def coord(fits):
	# open fits file
	hdulist = pyfits.open(fits)

	## @def img
	#  @brief img object containing all data on the image of the current calexp
	img = hdulist[1].header
	CDmat = CD(img)
	hdulist.close()

	# compute SKY1_CRVAL1 and SKY2_CRVAL2 in pixel (0,0)
	coordMin = X(img,img["CRPIX1"],img["CRPIX2"],CDmat)
	
	return coordMin


def addZone(fits):
	global RA_A  , RA_B
	global DEC_A , DEC_B
	
	global RA_N , DEC_N
	global mat
	
	coordMin = coord(fits)
	numFits = fits.split('/')[-1][7:21]
	
	#print " ( " + str(coordMin[0]) + " ; " + str(coordMin[1]) + " )"
	for i in range( int(math.floor(RA_A * coordMin[0] + RA_B)) , int(math.floor(RA_A * (coordMin[0]+0.2) + RA_B)) ):
		if i > 0 and i < RA_N:
			for j in range( int(DEC_A * coordMin[1] + DEC_B) , int(DEC_A * (coordMin[1]+0.2) + DEC_B) ):
				if j > 0 and j < DEC_N:
					try:
						mat[(i,j)][1].append(numFits)
						mat[(i,j)] = ( mat[(i,j)][0]+1 , mat[(i,j)][1] )
					except:
						mat[(i,j)] = ( 1 , [fits.split('/')[-1][7:21],] )

mat = {}
listFits = glob.glob("/sps/lsst/data/dev/lsstprod/DC_2013_one_percent/calexp_dir/sci-results/*/*/u/calexp/calexp-*.fits")
#listFits = glob.glob("/home/massot/Projet/compareSrc/data/calexp/calexp-*.fits")
nFits = len(listFits)
n = 1
print "début de la récupération des données : "
for fits in listFits:
	print "\r"+str(n) + " / " + str(nFits),
	n += 1 
	# for each calexp fits file
	addZone(fits)

print "\nfin de la récupération des données"

f = open(fname, "wb")
writer = csv.writer(f)
writer.writerow( ('i', 'j', 'density' , 'rrrrrr-cv-ffff') )

for i,j in mat:
	writer.writerow( (i,j,mat[i,j][0],mat[i,j][1]) )

