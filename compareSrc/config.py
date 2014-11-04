#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	============    ============
	*@package :*    compareSrc
	*@langage :*    *Python 2.6*
	*@auteur  :*    \J. Massot
	*@date    :*    2014-04-10
	============    ============

	Configuration, all gloabl variables
"""

import time

## @def name
#  @brief name of the current job
name = "compareSrc"
user = "jmassot"

# ╒══════════════════════════════════════════════════════════════════════════╕ #
# │    VALUES                                                                │ #
# ╘══════════════════════════════════════════════════════════════════════════╛ #

## @def epsi
#  @brief compare source at epsilon, 2 arcsec in degree
epsi = "0.0005555555555555556"

## @def b
#  @brief default value of filter (`sdssdm.pdf` p47)
b = "u"

## @def width_same
#  @brief width of overlap in pixels (`sdssdm.pdf` p47)
width_same = 128



# ╒══════════════════════════════════════════════════════════════════════════╕ #
# │    INPUT PATHS                                                           │ #
# ╘══════════════════════════════════════════════════════════════════════════╛ #

## @def PWD
#  @brief path working directory
PWD = "/afs/in2p3.fr/home/j/jmassot/public/compareSrc/"

## @def PATH_DATA
#  @brief directory where calexp and src directory
PATH_DATA = "/sps/lsst/data/dev/lsstprod/DC_2013_one_percent/calexp_dir/sci-results"
## @def PATH_CALIB
#  @brief directory where Science_Ccd_Exposure.csv
PATH_CALIB = "/afs/in2p3.fr/home/j/jmassot/public/data"

# ╒══════════════════════════════════════════════════════════════════════════╕ #
# │    OUTPUT PATHS                                                          │ #
# ╘══════════════════════════════════════════════════════════════════════════╛ #

## @def PATH_OUTPUT
#  @brief directory output csv
PATH_OUTPUT = "/sps/lsst/dev/jmassot/data/src"
## @def PATH_OUTPUT_CPP
#  @brief directory output csv
PATH_OUTPUT_CPP = "/sps/lsst/dev/jmassot/data/asso"
## @def PATH_OUTPUT_ROOT
#  @brief directory output root and eps files
PATH_OUTPUT_ROOT = "/sps/lsst/dev/jmassot/data/root"

## @def PATH_RAPPORT
#  @brief directory output tex
PATH_RAPPORT = "/sps/lsst/dev/jmassot/rapport"

## @def IO_PATH
#  @brief directory where print stdout and stderr
IO_PATH = "/sps/lsst/dev/jmassot/jobs_io/"

# ╒══════════════════════════════════════════════════════════════════════════╕ #
# │    MISCELLANEOUS                                                         │ #
# ╘══════════════════════════════════════════════════════════════════════════╛ #

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

BOLD = "\033[1m"

def infog( msg ):
	print "\n" + OKGREEN + msg + ENDC

def info( msg ):
	print "\n" + OKBLUE + msg + ENDC

def warn( msg ):
	print "\n" + WARNING + msg + ENDC

def err( msg ):
	print "\n" + FAIL + msg + ENDC

def tps():
	print BOLD + time.strftime('%d/%m/%y %H:%M:%S',time.localtime()) + ENDC
