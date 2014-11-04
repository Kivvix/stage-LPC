#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	:Module:
		data.calexp
	:Langage:
		Python 2.6
	:Auteur:
		\J. Massot
	:Date:
		2014-04-03

	| Recherche les sources identifiées par SDSS à partir de la lecture d'un fichier ``fits`` ``calexp``.

	Le sous module ``calexp.py`` permet la récupération des sources identifiées par SDSS à partir de la lecture du fichier ``calexp-rrrrrr-bc-ffff.fits``. Cela s'effectue en plusieurs étapes.

	#. La lecture de la matrice CD ;

	#. Le calcul des coordonnées définissant le champ ;

	#. L'écriture de la requête SQL ;

	#. Envoie de la requête SQL sur le serveur de SDSS, sur la base de données de la *stripe 82* ;

	#. Récupération de toutes les sources avec leur coordonnées (*RA*, *Dec*) et leur magnitude.


	Le calcul des coordonnées s'effectue après la lecture de la matrice CD, cela permet la convertion des coordonnées locales (en pixel à partir du coin inférieur droit) en coordonnées astronomiques (à partir du méridien et de l'équateur céleste) en ascension droite (*RA*) et déclinaison (*Dec*). La requête SQL sur la base de données de la *stripe 82* de SDSS permet la récupération de toutes les sources lumineuses du champ considéré. Ces données seront confrontés aux sources identifiées par le logiciel Stack dans le :ref:`module cmp <doc-cmp>`.

	.. tip::
		Dans la suite de cette page, chaque fonction sera détaillée à l'aide de ses paramêtres, ce qu'elle fait et ce qu'elle retourne.
"""

# to matrix calculate (without namespace)
from numpy import *
# to manipulate fits files
import pyfits

import csv

from config import *


# ╒══════════════════════════════════════════════════════════════════════════╕ #
# │    FITS PART                                                             │ #
# ╘══════════════════════════════════════════════════════════════════════════╛ #

def foncfg( L , img , u , v ) :
	"""
		Fonction généralisant le rôle des fonctions *f* et *g* nécessaire au calcul des coordonnées astronomiques.
		
		Paramètres
		----------
			L : ``char``
				lettre des coeficients de la matrice *A* ou *B*, à lire dans le fichier fits
			img : objet ``hdu`` de ``pyfits``
				accesseur sur le fichier ``fits`` et son image
			u : ``float``
				variables intérmediaire de calcul pour ``SKY1_CRVAL1`` et ``SKY2_CRVAL2``
			v : ``float``
				semble à ``u``
		
		Retour
		------
			``r`` : ``float``
				*f(u,v)* ou *g(u,v)* suivant la valeur de ``L``
	"""
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


def f( img , u , v ) :
	"""
		Fonction entrant dans le calcul des coordonnées astronomiques. Celle-ci appelle la fonction plus générale :func:`foncfg`.
		
		Paramètres
		----------
			img : objet ``hdu`` de ``pyfits``
				accesseur sur le fichier `fits` et son image
			u et v : ``float``
				variables intérmédiaire pour le calcul de ``SKY1_CRVAL1`` et ``SKY2_CRVAL2``
		
		Retour
		------
			*f(u,v)* : ``float``
	"""
	return foncfg( 'A' , img , u , v )

def g( img , u , v ) :
	"""
		Fonction entrant dans le calcul des coordonnées astronomiques. Celle-ci appelle la fonction plus générale :func:`foncfg`.
		
		Paramètres
		----------
		img : objet ``hdu`` de ``pyfits``
			accesseur sur le fichier `fits` et son image
		u et v : ``float``
			variables intérmédiaire pour le calcul de ``SKY1_CRVAL1`` et ``SKY2_CRVAL2``
		
		Retour
		------
			*g(u,v)* : ``float``
	"""
	return foncfg( 'B' , img , u , v )


def X( img , u , v , CD ) :
	"""
		Calcul le vecteur ``SKY1_CRVAL1`` et ``SKY2_CRVAL2``, correspondant aux coordonnées astronomiques
		
		Paramètres
		----------
			img : objet ``hdu`` de ``pyfits``
				accesseur sur le fichier `fits` et son image
			u et v : ``float``
				variables intérmédiaire pour le calcul de ``SKY1_CRVAL1`` et ``SKY2_CRVAL2``
			CD : objet ``matrix`` de ``numpy``
				matrice permettant le calcul des coordonnées
		
		Retour
		------
			X : objet ``matrix`` de ``numpy``
				vecteur (type ``matrix`` avec une seule colonne) avec les coordonées calculées ``SKY1_CRVAL1`` et ``SKY2_CRVAL2``
	"""
	fuv = f(img,u,v)
	guv = g(img,u,v)
	Y = matrix(str(u+fuv) + " ; " + str(v+guv))
	
	X = CD*Y
	X = X + matrix( str(img["CRVAL1"]) + " ; " + str(img["CRVAL2"]) )
	
	return X


def CD( img ) :
	"""
		Fonction donnant la matrice nécessaire au calul de ``SKY1_CRVAL1`` et ``SKY2_CRVAL2``
		
		Paramètre
		---------
			img : objet ``hdu`` de ``pyfits``
				accesseur sur le fichier `fits` et son image
		
		Retour
		------
			CD : objet ``matrix`` de ``numpy``
				la matrice CD
	"""
	return matrix( str(img["CD1_1"]) + " " + str(img["CD1_2"]) + " ; " + \
	               str(img["CD2_1"]) + " " + str(img["CD2_2"]) )


def coord( fits , first=True ):
	"""
		Calcule les coordonnées extrême (bas-gauche et haut-droit) du fichier `calexp` courant

		Paramètres
		----------
			fits : ``string``
				nom du fichier ``fits`` de ``calexp`` de la *run* courante
			first : ``boolean``
				indique s'il faut ou non tronquer les 128 premiers pixels
		
		Retour
		------
			coordMin, coordMax : tuple d'objets ``matrix`` de ``numpy``
				couples de matrices contenant les coordonnées minimales et maximales de l'image du fichier ``fits``
	"""
	
	global width_same
	
	# open fits file
	hdulist = pyfits.open(fits)

	## @def img
	#  @brief img object containing all data on the image of the current calexp
	img = hdulist[1].header
	CDmat = CD(img)
	hdulist.close()
	
	# compute SKY1_CRVAL1 and SKY2_CRVAL2 in pixel (0,0)
	coordMin = X( img , -img["CRPIX1"] , -img["CRPIX2"] , CDmat )
	# compute SKY1_CRVAL1 and SKY2_CRVAL2 in pixel (maxX,maxY)
	coordMax = X( img , img["NAXIS2"] - img["CRPIX1"] , img["NAXIS1"] - img["CRPIX2"] , CDmat )
	
	# move coordMin if this is not the first call of this function
	coordMin = coordMin - matrix( str(width_same*(not(first))) + ";" + "0" )
	
	return coordMin, coordMax


# ╒══════════════════════════════════════════════════════════════════════════╕ #
# │    SQL PART                                                              │ #
# ╘══════════════════════════════════════════════════════════════════════════╛ #

def query( coordMin , coordMax , attr , num ) :
	"""
		Fonction écrivant la requête SQL et appelant les fonctions du fichier `sqlcl.py` nécessaires à l'appelle de la base de données de SDSS.
		
		.. note::
			Cette partie est essentiellement réalisé par le script fournit par SDSS permettant à l’origine des requêtes SQL sur la base de données de la dernière realease et non pas sur la stripe 82. Une modification de l’url du formulaire permettant la requête à permis l’accès automatique aux données souhaitées.
		
		Paramètres
		----------
			coordMin : objet ``matrix`` de ``numpy``
				coordonnées du coin inférieur gauche en (RA, Dec)
			coordMax : objet ``matrix`` de ``numpy``
				coordonnées du coin supérieur droit en (RA, Dec)
			attr : ``string``
				attributs à sélectionner dans la requête SQL
			num : ``string``
				numéro du fichier `fits` (``rrrrrr-bc-ffff``)
		
		Retour
		------
			lines : liste de ``strings``
				lignes de retour de la requête SQL sur la base de données SDSS
	"""
	
	# to submit sql query on SDSS data base
	import sqlcl
	# SQL query
	sqlQuery = """SELECT """ + attr + """
FROM PhotoObj
WHERE 
	ra BETWEEN """ + str(coordMin[0,0]) + """ AND """ + str(coordMax[0,0]) + """ 
	AND dec BETWEEN """ + str(coordMin[1,0]) + """ AND """ + str(coordMax[1,0]) + """
	AND run = """ + str(int( num[0:6] )) + """
	AND camcol = """ + str(int( num[8] )) + """
	AND type = 6
"""

	lines = sqlcl.query(sqlQuery).readlines()
	
	return lines


# ╒══════════════════════════════════════════════════════════════════════════╕ #
# │    SAVE PART                                                             │ #
# ╘══════════════════════════════════════════════════════════════════════════╛ #

def write( lines , firstLine , num , dest , first = True ):
	"""
		Écrit toutes les lignes dans un fichier `csv`. Celui-ci prend le nom de la *run* courante sur laquelle s'effectue la comparaison
		
		Paramètres
		----------
			lines : liste de ``strings``
				lignes à écrire
			firstLine : ``string``
				première ligne à écrire (entête)
			num : ``string``
				numéro de la run sous forme ``rrrrrr-bc-ffff``
			dest : ``string``
				destination du fichier ``csv``
			first : ``boolean``
				indicateur de la première écriture dans le fichier (implique l'écrasement du fichier et l'écriture de l'entête)
	"""
	if first:
		fileDB = open(dest + "/src-sdss-" + num + ".csv", "w")
		fileDB.write(firstLine+'\n')
	else:
		fileDB = open(dest + "/src-sdss-" + num + ".csv", "a")
	
	#print "calexp : " + str(len(lines))
	for line in lines[1:]:
		fileDB.write(line)
	fileDB.close()