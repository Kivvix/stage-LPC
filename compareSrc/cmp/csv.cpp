/**
 * @file csv.cpp
 * @package compare
 * @author J. Massot
 * @date 2014-04-14
 * 
 * @brief Compare sources between 2 fits files
 */

#include "csv.hpp"

/** @fn csvToTab
 *  @brief convert `csv` file into associated table (map) [ (ra,dec) ] = (mag,id)
 *  @details `csv` file is formated `id,ra,dec,mag`
 *  @param `std::string fileName` name of csv file
 *  @param `std::set<long> save` list to save sources
 *  @return `std::map< Coord<double,double> , Coord<double,long> > tab` (Ra,Dec) => (mag,id) **/
std::map< Coord<double,double> , Coord<double,long> > csvToTab( std::string fileName , std::set<Src> &save )
{
	// map returned : [ (ra,dec) ] = (mag,id)
	std::map< Coord<double,double> , Coord<double,long> > tab;
	
	std::string s_id, s_ra, s_dec, s_mag; // variables to recover `csv` data
	double ra,dec,mag; long id;           // data after conversion

	// coordinates for map (Ra,Dec) => (mag,id)
	Coord<double,double> radec;
	Coord<double,long>  magid;
	Src tmp;
	
	// input file stream
	std::ifstream file( fileName.c_str() );
	
	// read first line but doing nothing (for header line)
	getline(file, s_id);

	// read all data with `getline`, first id, then ra, dec and magnitude
	// data are converted directly into id, ra, dec and mag variables
	while ( getline(file, s_id, ',') ) {
		id = atol(s_id.c_str());
		getline(file, s_ra,  ','); ra  = atof( s_ra.c_str () );
		getline(file, s_dec, ','); dec = atof( s_dec.c_str() ); 
		getline(file, s_mag);      mag = atof( s_mag.c_str() );
		
		// complete coordinates
		radec.xy(ra,dec);
		magid.xy(mag,id);
		
		// insert in tab
		tab.insert(std::pair<Coord<double,double>, Coord<double,long> >(radec, magid));
		// save curent source into a set for test errors
		tmp.build(radec,magid);
		save.insert(tmp);
	}
	
	return tab;
}