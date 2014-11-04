#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	============    ============
	*@package :*    compareSrc
	*@langage :*    *Python 2.6*
	*@auteur  :*    \J. Massot
	*@date    :*    2014-05-16
	============    ============

	Compare sources between `calexp` and `src`
"""

from config import *

import os, sys
import glob
# for multithreading
import threading

import data.calexp
import data.src

## @def attributs
#  @brief attributs which we select in SDSS DB and src fits file
attributs = 'objid,ra,dec,' + b


# ╒══════════════════════════════════════════════════════════════════════════╕ #
# │    RESEARCH DATA                                                         │ #
# ╘══════════════════════════════════════════════════════════════════════════╛ #

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
	
	srcIds,srcCoord,srcMag = data.src.coord( srcFits , fitsNum , first )
	srcLines        = data.src.map( srcIds , srcCoord , srcMag , fitsNum )
	data.src.write( srcLines , attributs , fitsNum[0:9] , PATH_OUTPUT , first )


# ╒══════════════════════════════════════════════════════════════════════════╕ #
# │    WORKER (threaded function)                                            │ #
# ╘══════════════════════════════════════════════════════════════════════════╛ #

def worker( runNum , c ):
	"""
		function threaded calling research of data and comparaison
		
		:param runNum_c: tupe with run number and column of the CCD (1-6)
		:type runNum_c:  tuple of string
	"""
	global b , PATH_DATA , PWD
		
	# data of each pair of fits files
	first = True
	for fits in glob.glob( c + "/" + b  + "/calexp/calexp*.fits" ):
		fitsNum = fits[18:32]
		
		## @def calexpFits
		#  @brief path and name of calexp fits file
		calexpFits = PATH_DATA + "/" + runNum + "/" + c + "/" + b  + "/calexp/calexp-" + fitsNum + ".fits"
		## @def srcFits
		#  @brief path and name of src fits file
		srcFits    = PATH_DATA + "/" + runNum + "/" + c + "/" + b  + "/src/src-" + fitsNum + ".fits"
		
		#calexp( fitsNum , calexpFits , first )
		if ( first ):
			coordMin = coordCalexp( fitsNum , calexpFits , first )
		else:
			coordMax = coordCalexp( fitsNum , calexpFits , first )
		
		src( fitsNum , srcFits , first )
		
		first = False

	savCalexp( coordMin , coordMax , "%06d" % int(runNum) + "-" + b + c )


# ╒══════════════════════════════════════════════════════════════════════════╕ #
# │    CALLED FUNCTIONS                                                      │ #
# ╘══════════════════════════════════════════════════════════════════════════╛ #
def d( runNum ):
	"""
		Function calling thread for analyse one `run`
		
		:param runNum: run number
		:type runNum:  string
	"""
	global b , PWD , PATH_DATA , PATH_OUTPUT , attributs
		
	# We create one thread by column of the CCD	
	os.chdir( PATH_DATA + "/" + runNum )
	columns = glob.glob( "*" )
	
	threads = [ threading.Thread( target = worker , args=(runNum,c) ) for c in columns ]
	
	for t in threads:
		t.start()
	
	for t in threads:
		t.join()
	
	os.system( PWD + "fusionCol.sh " + PATH_OUTPUT + " " + "%06d" % int(runNum) + " " + b )
	
	

def c( runNum ):
	"""
		Function calling comparaison on one `run`
		
		:param runNum: run number
		:type runNum:  string		
	"""
	global b , PWD , PATH_DATA
	
	os.system( PWD + "cmp/cmp " + "%06d" % int(runNum) + "-" + b )

def s( runNum ):
	"""
		Function calling stat on one `run`
		
		:param runNum: run number
		:type runNum:  string		
	"""
	global b , PWD , PATH_DATA
	
	os.system( PWD + "stat/stat " + "%06d" % int(runNum) + "-" + b )
	



# ╒══════════════════════════════════════════════════════════════════════════╕ #
# │    MAIN FUNCTION                                                         │ #
# ╘══════════════════════════════════════════════════════════════════════════╛ #

if __name__ == '__main__':
	run( sys.argv[1] )

