#!/usr/bin/env python
# -*- coding: utf-8 -*-

## @package compareSrc
#  @author J. Massot
#  @date 2014-05-15
#
# @brief Initialisation and execution of comparaison of all sources
# All fits files are listed with the identifier `rrrrrr-bc-ffff` with :
# rrrrrr : run number
# b      : filter (`u`,`g`,`r`,`i`,`z`)
# c      : column of the CCD (1-6)
# ffff   : field number within the run
#
# We create one job by `run`, calculation on each `run` is parallelized
# in different threads for each column of the CCD (1-6) (`c` id). The
# filter id `u`,`g`,`r`,`i`,`z` (`b` id) is specified with command line,
# with the default value `u`.

# import configuration
from config import *

import os, sys
from stat import *
import glob
import time

# ╒══════════════════════════════════════════════════════════════════════════╕ #
# │    TEST ARGUMENTS                                                        │ #
# ╘══════════════════════════════════════════════════════════════════════════╛ #
usage = False

"""
if ( len(sys.argv) == 1 ) :
	usage = True
else :
	try:
		if ( len(sys.argv) == 2 and sys.argv[1] in ['u','g','r','i','z'] ) :
			usage = True
			b = sys.argv[1]
		else :
			usage = False
	except:
		usage = False

if not(usage):
	err( BOLD + "No good argument")
	sys.exit("Usage : \n\t" + sys.argv[0] + " [b]\nWhere lettre [b] is the id of filtre (`u`,`g`,`r`,`i`,`z`)")
"""

if ( len(sys.argv) >= 2 ):
	jobsList = sys.argv[1]
	if ( len(sys.argv) >= 3 ):
		b = sys.argv[2]
else :
	jobsList = "dcs"


# juste because it's pretty
width_term = int(os.popen("tput cols").readlines()[0] )
print HEADER + """
╭──────────────────────────╮
│ """ + ENDC + OKBLUE + """Comparaison LSST -- SDSS""" + ENDC + HEADER + """ ╞""" + "═"*(width_term - 29) + """╗
╰─╥────────────────────────╯ """ +  " "*(width_term - 30) + """║
  ║ """ + ENDC + """Lancement du job """ + name + HEADER + " "*(width_term - 22 - len(name)) + """║
  ║ """ + ENDC + """   Analyse des produits du Stack, filte """ + BOLD + OKBLUE + b + ENDC + HEADER +" "*(width_term - 46) + """║
  ║ """ + ENDC + """                                  jobs  """ + BOLD + OKBLUE + jobsList + ENDC + HEADER +" "*(width_term - 45 - len(list(jobsList))) + """║
  ║""" + " "*(width_term - 26) + ENDC + BOLD + time.strftime('%H:%M:%S (%Y-%m-%d)',time.localtime()) + ENDC + HEADER + """ ║
  ╚""" + "═"*(width_term - 4) + """╝ """ + ENDC +"""
"""

# ╒══════════════════════════════════════════════════════════════════════════╕ #
# │    CONFIGURATION                                                         │ #
# ╘══════════════════════════════════════════════════════════════════════════╛ #
infog("""--- Changement pour le groupe `lsst` """ + "-"*(width_term - 37) )
tps()
os.system("""tcsh -c "newgroup --temp lsst" """)

infog("""--- Écriture des `config.hpp` """ + "-"*(width_term - 30) )
tps()

### cmp/config.hpp #############################################################
print BOLD + "cmp/config.hpp" + ENDC
print "\t epsi        : " + epsi
print "\t PATH_INPUT  : " + PATH_OUTPUT
print "\t PATH_OUTPUT : " + PATH_OUTPUT_CPP
configCmpHpp = """
/**
 * @file config.hpp
 * @package compare
 * @author J. Massot
 * @date 2014-04-28
 * 
 * @brief Global variables to configure paths and constants
 */

#ifndef __CONFIG_HPP__
#define __CONFIG_HPP__

#include <iostream>

/** @def epsi
 *  @brief compare source at epsilon, 2 arcsec in degree **/
const double epsi = """ + epsi + """;
const double epsi2 = epsi*epsi;

const std::string PATH_INPUT  = \"""" + PATH_OUTPUT     + """\";
const std::string PATH_OUTPUT = \"""" + PATH_OUTPUT_CPP + """\";

#endif
"""

configCmpFile = open( PWD + "cmp/config.hpp" , 'w' )
configCmpFile.write ( configCmpHpp )
configCmpFile.close ()


### stat/config.hpp ############################################################
print BOLD + "stat/config.hpp" + ENDC
print "\t PATH_INPUT  : " + PATH_OUTPUT_CPP
print "\t PATH_OUTPUT : " + PATH_OUTPUT_ROOT
configStatHpp = """
/**
 * @file config.hpp
 * @package compare
 * @author J. Massot
 * @date 2014-05-26
 * 
 * @brief Global variables to configure paths and constants
 */


#ifndef __CONFIG_HPP__
#define __CONFIG_HPP__

#include <iostream>

const std::string PATH_INPUT  = \"""" + PATH_OUTPUT_CPP  + """\";
const std::string PATH_OUTPUT = \"""" + PATH_OUTPUT_ROOT + """\";

#endif
"""

configStatFile = open( PWD + "stat/config.hpp" , 'w' )
configStatFile.write ( configStatHpp )
configStatFile.close ()


### job.py #####################################################################
infog("""--- Écriture du job python """ + "-"*(width_term - 27) )
tps()

script = """#!/usr/bin/env python
# -*- coding: utf-8 -*-

## @package compareSrc
#  @author J. Massot
#  @date 2014-06-20

from config import *
import os, sys
import compareSrc

runNum = sys.argv[1]

"""

jobs = ""
for i in list(jobsList):
	if i == "d" :
		print "data"
		jobs += """
compareSrc.d( runNum )
"""
	if i == "c" :
		print "cmp"
		jobs += """
compareSrc.c(  runNum )
"""
	if i == "s" :
		print "stat"
		jobs += """
compareSrc.s( runNum )
"""
script += jobs

jobFile = open( PWD + "job.py" , 'w' )
jobFile.write ( script )
jobFile.close ()
os.chmod( PWD + "job.py" , S_IRWXU )

# ╒══════════════════════════════════════════════════════════════════════════╕ #
# │    COMPILATION                                                           │ #
# ╘══════════════════════════════════════════════════════════════════════════╛ #
infog("""--- Compilation """ + "-"*(width_term - 16) )
tps()
print BOLD + "Compilation cmp..." + ENDC
os.system("make -C " + PWD + "cmp/")


print BOLD + "Compilation stat..." + ENDC
os.system("source /sps/lsst/Library/root/ROOT/bin/thisroot.sh")
os.system("make -C " + PWD + "stat/")

# ╒══════════════════════════════════════════════════════════════════════════╕ #
# │    EXECUTION RUN BY RUN                                                  │ #
# ╘══════════════════════════════════════════════════════════════════════════╛ #

infog("""--- Lancement des jobs """ + "-"*(width_term - 23) )
tps()

os.chdir( PATH_DATA )
#nRuns = len(glob.glob('*'))
nRuns = 10
N = 100.0

for i in range(0,int(nRuns/N)+1):
	t = str(int(i*N+1)) + "-" + str(min( int((i+1)*N) , nRuns ) )
	print BOLD + "\tjobs : " + t + ENDC
	os.system("qsub -P P_lsst -l sps=1 -o " + IO_PATH + " -j y -pe multicores 6 -q mc_medium -N " + name + " -t " + t + " " + PWD + "job.csh")

os.system("qstat")

