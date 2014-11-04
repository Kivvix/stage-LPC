#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	:Module:
		data.src
	:Langage:
		Python 2.6
	:Auteur:
		\J. Massot
	:Date:
		2014-04-04

	| Recherche de `RA`, `Dec`, `ABmag` et `id` depuis un fichier `fits` ``src``.


	Le sous-module ``src.py`` permet la récupération de toutes les sources identifiées par le logiciel *Stack* à l'aide de la lecture du fichier ``src-rrrrrr-bc-ffff.fits``. Une mesure de calibration récupérée dans un fichier tierce (``Science_Ccd_Exposure.csv``) est cependant nécessaire pour calculer la magnitude des soruces.

	.. tip::
		Dans la suite de cette page, chaque fonction sera détaillée, ses paramètres, ce qu'elle fait et ce qu'elle retourne.
"""

# to logarithm calculate and pi
import numpy
# to manipulate fits files
import pyfits

import csv


from decimal import getcontext, Decimal
getcontext().prec = 50

from config import *


""" --- searchFluxMag0 ----------------------------------------------------- """
def searchFluxMag0( num ) :
	"""
		Fonction cherchant la valeur de calibration ``fluxMag0`` dans le fichier ``Science_Ccd_Exposure.csv`` Ã  partir du numéro de la *run*.
			
		Cette fonction est modifiable suivant les besions, ainsi, peuvent être redéfini suivant la configuration :

			* ``csvFile``     : chemin et nom du fichier `csv` où chercher la constante ``fluxMag0`` ;
			* ``fluxMagCol``  : colonne du fichier `csv` où se trouve ``fluxMag0`` ;
			* ``run``         : valeur de la *run* ;
			* ``filterTab``   : tableau de correspondance entre les lettres et les numéros de filtres ;
			* ``filterIdCol`` : colonne du fichier `csv` où se trouve l'*id* du filtre.
		
		
		Paramètre
		---------
			num : ``string``
				numéro de la *run*.
		
		Retour
		------
			``fluxMag0`` : ``string``
				valeur de calibration pour le calcul de la magnitude.
	"""
	global PATH_CALIB

	csvFile = PATH_CALIB + '/Science_Ccd_Exposure.csv'


	fluxMagCol = 35
	fluxMag0 = 0

	run = str(int( num[0:6] ))
	runCol = 1

	filterTab = {'u':'0', 'g':'1','r':'2','i':'3','z':'4'}
	filterId = filterTab[ num[7] ]
	filterIdCol = 3	
	
	field = str(int( num[10:] ))
	fieldCol = 4
	
	inputFile  = open(csvFile, "rb")
	reader = csv.reader(inputFile)
	
	# file browse
	for row in reader:
		if row[runCol] == run and row[filterIdCol] == filterId and row[fieldCol] == field:
			fluxMag0 = row[fluxMagCol]
			break

	inputFile.close()
	
	return fluxMag0


""" --- coord -------------------------------------------------------------- """
def coord( fits , num , first=True ) :
	"""
		Fonction recherchant les coordonnées (*RA*, *Dec*) dans le fichier ``fits`` ainsi que la magnitude (``fluxMag0`` étant recherché à  l'aide de la fonction ``searchFluxMag0``).
		
		Paramètres
		----------
			fits : ``string``
				nom du fichier ``fits`` de ``src`` de la *run* courante
			num : ``string``
				uméro de la run courante
			first : ``boolean``
				indique s’il est nécessaire ou non de prendre tout le fichier ``fits`` ou l’image tronquée des 128 premier pixels (possiblement variable à l’aide de la variable ``width_same`` du fichier ``config.py``)
		
		Retour
		------
			``ids, radec, ABmag`` : tuples de listes
				tuples conteant les ``id`` données par le *Stack* les coordonnées (*RA*, *Dec*), et la magnitude de toutes les sources.
		
		La magnitude est calculé à l'aide la formule suivante :
		
		.. math::
				flux = 3.63078\cdot 10^{­20} * \frac{\texttt{psfFlux}}{\texttt{fluxMag0}} \\
				ABmag = -2.5 * \log _{10}(flux) - 48.6
	"""
	global width_same
	
	hduList = pyfits.open(fits)

	data = hduList[1].data

	hduList.close()
	
	# coord of all src in this fits file
	radec = data.field('coord')
	ids   = data.field('id')
	
	if not(first):
		tmp = radec
		radec = []
		for i in tmp:
			if i[0] > 128.0:
				radec.append(i)

	# calcul of magnitude of all sources
	fluxMag0 = searchFluxMag0(num)
	ABmag = []
	for i in range( len( data.field('flux_psf') ) ) :
		flux = Decimal('3.63078E-20') * Decimal(str( data.field('flux_psf')[i] )) / Decimal(fluxMag0)
		try:
			ABmag.append( Decimal('-2.5') * numpy.log10( flux ) - Decimal('48.6') )
		except:
			ABmag.append( Decimal('0') )
	
	return ids, radec, ABmag


""" --- map ---------------------------------------------------------------- """
def map( ids , coord , mag , num ) :
	"""
		Transforme les coordonnées et la magnitude en une chaîne de caractères pré-formatée pour être écrite dans un fichier ``csv``.
		
		Paramètres
		----------
			ids : liste de ``int``
				*id* unique des sources identifiées par le *Stack*
			coord : liste de tableaux de ``floats``
				coordonnées des sources
			mag : liste de ``floats``
				magnitudes des sources
		
		Retour
		------
			``lines`` : liste de ``strings``
				chaînes de caractères formatées : ``id,run,col,field,filtre,ra,dec,mag``.
	"""
	lines = []
	for i in range( len (coord) ):
		lines.append( str(ids[i]) + ',' + str(int(num[0:6])) + ',' + num[8] + ',' + str(int(num[10:])) + ',' + num[7] + ',' + str(180.0*coord[i][0]/numpy.pi) + ',' + str(180*coord[i][1]/numpy.pi) + ',' + str(mag[i]) + '\n')
	
	return lines


""" --- write -------------------------------------------------------------- """
def write( lines , firstLine , num , dest , first = True ) :
	"""
		Fonction écrivant les lignes dans un fichier ``csv``.
		
		Paramètres
		----------
			lines : liste de ``strings``
				lignes à écrire
			firstLine : ``string``
				première ligne à écrire (entête)
			num : ``string``
				numéro caractéristique du fichier (par exemple celui du fichier ``fits`` : ``rrrrrr-bc-ffff``)
			dest : ``string``
				destination du fichier ``csv``
			first : ``boolean``
				indicateur de la première écriture dans le fichier (implique l'écrasement du fichier et l'écriture de l'entête)
	"""
	if first:
		fileDB = open(dest + "/src-stack-" + num + ".csv", "w")
		fileDB.write(firstLine+'\n')
	else:
		fileDB = open(dest + "/src-stack-" + num + ".csv", "a")
	
	#print "src " + num + " : " + str(len(lines))
	for line in lines[1:]:
		fileDB.write(line)
	fileDB.close()
