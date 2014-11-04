#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import glob

from config import *
import data.calexp
import data.src

## @def attributs
#  @brief attributs which we select in SDSS DB and src fits file
attributs = 'objid,run,camcol,field,ra,dec,u,g,r,i,z'

## Calexp treatment ##
def coordCalexp( fitsNum , calexpFits , first=True ):
	coordMin, coordMax = data.calexp.coord( calexpFits , first )
	
	if ( first ):
		return coordMin
	else:
		return coordMax

def savCalexp( coordMin , coordMax , fitsNum ):
	global attributs , PATH_OUTPUT
	
	calexpLines = data.calexp.query( coordMin , coordMax , attributs , fitsNum )
	data.calexp.write( calexpLines , attributs , fitsNum , PATH_OUTPUT , True )

def calexp( fitsNum , calexpFits , first=True ):
	"""
		find and write calexp data (id,ra,dec,mag)
		
		:param fitsNum:    number of fits file (``rrrrrr-bc-ffff``)
		:param calexpFits: name of calexp fits file
		:param first:      take all the picture or less 128 first pixels
		
		:type fitsNum:     string
		:type calexpFits:  string
		:type first:       boolean
	"""
	global attributs , PATH_OUTPUT
		
	coordMin, coordMax = data.calexp.coord( calexpFits , first )
	calexpLines        = data.calexp.query( coordMin , coordMax , attributs , fitsNum )
	data.calexp.write( calexpLines , attributs , fitsNum[0:9] , PATH_OUTPUT , first )

## Src treatment ##
def src( fitsNum , srcFits , first=True ):
	"""
		find and write src data (id,ra,dec,mag)
		
		:param fitsNum: number of fits file (``rrrrrr-bc-ffff``)
		:param srcFits: name of src fits file
		:param first:   take all the picture or less 128 first pixels
		
		:type fitsNum:  string
		:type srcFits:  string
		:type first:    boolean
	"""
	global attributs , PATH_OUTPUT
	
	srcCoord,srcMag = data.src.coord( srcFits , fitsNum , first )
	srcLines        = data.src.map( srcCoord , srcMag )
	data.src.write( srcLines , attributs , fitsNum[0:9] , PATH_OUTPUT , first )


def analyCol( runNum , c ):
	"""
		function threaded calling research of data
		
		:param runNum_c: tupe with run number and column of the CCD (1-6)
		:type runNum_c:  tuple of string
	"""
	global b , PATH_DATA , PWD
	
	print " " + str(c) + "  ",
	# data of each pair of fits files
	first = True
	for fits in glob.glob( c + "/" + b  + "/calexp/calexp*.fits" ):
		fitsNum = fits[18:32]
		
		## @def calexpFits
		#  @brief path and name of calexp fits file
		calexpFits = PATH_DATA + "/" + runNum + "/" + c + "/" + b  + "/calexp/calexp-" + fitsNum + ".fits"
		## @def srcFits
		#  @brief path and name of src fits file
		#srcFits    = PATH_DATA + "/" + runNum + "/" + c + "/" + b  + "/src/src-" + fitsNum + ".fits"
		
		#calexp( fitsNum , calexpFits , first )
		if ( first ):
			coordMin = coordCalexp( fitsNum , calexpFits , first )
		else:
			coordMax = coordCalexp( fitsNum , calexpFits , first )
		
		#src( fitsNum , srcFits , first )
		
		first = False

	savCalexp( coordMin , coordMax , "%06d" % int(runNum) + "-" + b + c )

def analyRun( runNum ):

	global b , PWD , PATH_DATA , PATH_OUTPUT , attributs
	
	print "run : " + str(runNum ) + " : ",
	
	os.chdir( PATH_DATA + "/" + runNum )
	columns = glob.glob( "*" )
	
	for c in columns :
		analyCol( runNum , c )

if __name__ == '__main__':
	os.chdir( PATH_DATA )
	runs = glob.glob( "*" )
	#runs = ( 7158, 7112, 5924, 5566, 6421, 7057, 6430, 4895, 5895, 6474, 6383, 7038, 5642, 6409, 6513, 6501, 6552, 2650, 6559, 6355, 7177, 7121, 3465, 7170, 7051, 6283, 6458, 5853, 6484, 5765, 2708, 5786, 4253, 6934, 6508, 2662, 6518, 6584, 4188, 6976, 7202, 7173, 4153, 5820, 2649, 7140, 6330, 3388, 7117, 6504, 6314, 4128, 6596, 6564, 5807, 6367, 6373, 5622, 5882, 7034, 7136, 6577, 6600, 2768, 3437, 4927, 6414, 3434, 5813, 7084, 4858, 7124, 6982, 4917, 4192, 5898, 6479, 4868, 7106, 7195, 5744, 3360, 4198, 6963, 6533, 4933, 5603, 3384, 7155, 5619, 4207, 4849, 5582, 7024, 1755, 5709, 5781, 5770, 7145, 5754, 5646, 5800, 5759, 6287, 6568, 7054, 4203, 5776, 6433, 4247, 5823, 5052, 3325, 5836, 5590, 6580, 7161, 2728, 4145, 5633, 6461, 6555, 6955, 4874, 5792, 5918, 6425, 6377, 4263, 5878, 6441, 6447, 7080, 5905, 5713, 6618, 6537, 5637, 6402, 6530, 7047, 6524, 7101, 6293 )

	for r in runs :
		analyRun( r )
		print " "
		time.sleep(60)

