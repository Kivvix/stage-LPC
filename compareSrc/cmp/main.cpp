/**
 * @file main.cpp
 * @package compare
 * @author J. Massot
 * @date 2014-04-14
 * 
 * @brief Compare sources between 2 fits files
 */

#include <iostream>
#include <fstream>
#include <map>
#include <list>
#include <set>
#include <string>
#include <sstream>
#include <algorithm>
#include <cmath>

#include "config.hpp"

#include "coord.hpp"
#include "src.hpp"
#include "csv.hpp"
#include "errors.hpp"

#define tab_Src std::map< Coord<double,double> , Coord<double,long> >

int main(int argc, char **argv)
{
	if ( argc != 2 ) {
		std::cerr << "Usage : \n\t " << argv[1] << " [rrrrrr-bc-ffff]\n With [rrrrrr-bc-ffff] identifier of a fits file.\nrrrrrr : run number\n		b      : filter\n		c      : column\n		ffff   : field number " << std::endl;
		return 1;
	}
	
	// errors flux
	std::ostringstream sdssErrAlone, stackErrAlone, sdssErrMulti, stackErrMulti;
	
	// maps for SDSS sources and Srack sources
	tab_Src sdssSrc;
	tab_Src stackSrc;
	
	tab_Src::iterator p, q;

	// path and name of input `csv` files
	std::string sdssName  = PATH_INPUT+"/src-sdss-"  + std::string(argv[1]) + ".csv";
	std::string stackName = PATH_INPUT+"/src-stack-" + std::string(argv[1]) + ".csv";
	
	
	std::set<Src> sdssSave;
	std::set<Src> stackSave;
	sdssSrc  = csvToTab( sdssName  , sdssSave  );
	stackSrc = csvToTab( stackName , stackSave );
	
	
	// output structure
	std::map< Src , std::list<Src> > sameSrc;
	
	std::list<Src>::iterator low;
	
	// temporary sources objects
	Src sdssTmp, stackTmp;
	std::list<Src> sdssList;

	// check if SDSS source is associated to a Stack source
	bool sdssAlone;
	// Build table with all similar sources
	/* run on all SDSS sources -------------------------------------- */
	for ( p = sdssSrc.begin() ; p != sdssSrc.end() ; p++ ) {

		// build a temporary source object
		sdssTmp.build  ( p->first , p->second );
		sdssAlone = true;

		// run on all Stack sources
		for ( q = stackSrc.begin() ; q != stackSrc.end() ; q++ ) {
			if ( p->first % q->first ) {
				// sources are neighboor
				sdssAlone = false;
				// instanciation of stackTmp, and compute delta relatve to stackTmp
				stackTmp.build ( q->first , q->second );
				stackTmp.delta ( sdssTmp  );
				stackSave.erase( stackTmp );
				
				// check if one Stack source has been associated to 2 SDSS sources
				if ( ! sdssSave.erase(sdssTmp) ) {
					stackErrMulti << stackTmp.str() << " , " <<(*(sameSrc[ sdssTmp ]).begin()).str() << " , " <<sdssTmp.str() << std::endl;
				}

				// Insertion sorted
					// Search the lower iterator
				low = std::lower_bound( sameSrc[ sdssTmp ].begin(),    // first element of list
				                        sameSrc[ sdssTmp ].end(),      // last element of list
				                        std::abs(stackTmp.deltaMag()), // value to search
				                        opMag );                       // partial order function
					// And insert
				sameSrc[ sdssTmp ].push_back( stackTmp );				
			}
		}
		
		// check if a SDSS source has not been identify by Stack
		if ( sdssAlone && sameSrc[sdssTmp].size() == 0 ) {
			sdssErrAlone << sdssTmp.str() << std::endl;
		}
		
		// check if current SDSS source has been associated to 2 Stack sources
		if ( sameSrc[sdssTmp].size() > 1 ) {
			sdssList = sameSrc[sdssTmp];
			std::list<Src>::iterator lit (sdssList.begin());
			for ( ; lit != sdssList.end() ; ++lit ) {
				sdssErrMulti << sdssTmp.str() << " , " << (*lit).str() << " , " << (*(sdssList).begin()).str() << std::endl;
			}
		}

	}
	
	// check if a Stack source has not been identify by SDSS
	if ( ! stackSave.empty() ) {
		
		std::set<Src>::iterator sit(stackSave.begin());
		
		for( ; sit != stackSave.end() ; ++sit ) {
			stackErrAlone << (*sit).str() << std::endl;
		}
	}

	
	printErr( sdssErrMulti , sdssErrAlone , stackErrMulti , stackErrAlone , std::string(argv[1]) );
	
	// save pair of sources in csv file
	std::string nameFile = PATH_OUTPUT + "/src-same-" + std::string(argv[1]) + ".csv";
	std::string firstLine = "idSdss,raSdss(deg),decSdss(deg),magSdss , idStack,raStack(deg),decStack(deg),magStack, deltaRa(arcsec),deltaDec(arcsec),deltaMag";
	std::ofstream f( nameFile.c_str() );
	std::ostringstream tmp;
	if ( f ) {
		f << firstLine << std::endl;
		std::map< Src , std::list<Src> >::iterator it(sameSrc.begin());
		
		for( ; it != sameSrc.end() ; ++it ) {
			f << (it->first).str() << " , " << (*(it->second.begin())).str() << " , " << (*(it->second.begin())).deltaRa()*3600 << "," << (*(it->second.begin())).deltaDec()*3600 << "," << (*(it->second.begin())).deltaMag() << std::endl;
		}
	}
	
	return 0;
}

