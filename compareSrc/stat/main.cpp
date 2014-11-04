/**
 * @file stat.cpp
 * @package compare
 * @author J. Massot
 * @date 2014-05-26
 * 
 * @brief Display some stat about sources association
 */

/*
 * COMPILATION
 * ===========
 * 
 * $> g++ -I/home/massot/Public/root/include -g -c stat.cpp
 * $> libtool --mode=link g++  -g -o stat stat.o -L/home/massot/Public/root/lib -lCore -lCint -lRIO -lNet -lHist -lGraf -lGraf3d -lGpad -lTree -lRint -lPostscript -lMatrix -lPhysics -lz -lGui -pthread -lm -ldl -rdynamic
 * $> ./stat
 *  
 */

#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <cstdlib>

/* Include for ROOT */
#include "root.hpp"

#include "config.hpp"

#include "hist.hpp"

int main(int argc, char **argv)
{
	if ( argc != 2 ) {
		std::cout << "Usage : \n\t " << argv[0] << " [rrrrrr-bc-ffff]\n With [rrrrrr-bc-ffff] identifier of a fits file." << std::endl;
		return 1;
	}
	
	// nom du fichier csv d'entrée
	std::string csvFile  = PATH_INPUT + "/src-same-"  + std::string(argv[1]) + ".csv";
	
	// flux de mon fichier csv
	std::ifstream infile( csvFile.c_str() );
	
	// vecteur de stockage
	std::vector< std::vector<float> > data; 
	
	bool first = true;
	
	// on parcourt le fichier csv
	while (infile) {
		std::vector<float> tmp;
		std::string line;
		
		if (!getline( infile, line )) {
			break;
		}
		
		if (!first) {

			std::istringstream fluxLine( line );
			std::vector<std::string> record;

			while (fluxLine) {
				std::string s;
				if (!getline( fluxLine, s, ',' )) {
					break;
				}
				record.push_back( s );
			}
			//std::cout << record[8] << "   " << record[9] << "   " << record[10] << std::endl;
			tmp.push_back(std::atof( record[8].c_str() ));
			tmp.push_back(std::atof( record[9].c_str() ));
			tmp.push_back(std::atof( record[10].c_str() ));

			data.push_back(tmp);
			record.pop_back(); // pour ne pas utiliser trop de mémoire
		} else {
			first = false;
		}
		
	}
	
	if (!infile.eof()) 	{
		std::cerr << "Impossible to read " << PATH_OUTPUT << "/src-same-"  << argv[1] << ".csv" << std::cout;
	}
	
	hCoord( data , std::string(argv[1]) );
	hMag  ( data , std::string(argv[1]) );

	return 0;

}