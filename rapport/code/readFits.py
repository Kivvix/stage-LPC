#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyfits

def readFits( fits )
	# récupération des données du fichier fits
	hduList = pyfits.open(fits)
	data = hduList[1].data
	hduList.close()

	# radec : liste des coordonnées contenues dans le champ field du tableau data
	radec = data.field('coord')
