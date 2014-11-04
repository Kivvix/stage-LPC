/**
 * @file src.hpp
 * @package compare
 * @author J. Massot
 * @date 2014-04-15
 * 
 * @brief Class represent sources
 */

#ifndef __SRC_HPP__
#define __SRC_HPP__

#include <iostream>
#include <sstream>
#include <cmath> // std::abs

#include "coord.hpp"

/** 
 * @class Src
 * @brief Class reprent one source with its position, magnitude, id and difference between its and an other source.
 * @param ra_  right ascension
 * @param dec_ declinaison
 * @param mag_ magnitude
 * @param id_  identifier in data base (SDSS or Stack)
 * 
 * @param deltaRa_  difference between this source and an other source in RA
 * @param deltaDec_ same in declinaison
 * @param deltaMag_ same in magnitude
 **/

class Src
{
	private:
		double ra_;
		double dec_;
		double mag_;
		long id_;
		
		float deltaRa_;
		float deltaDec_;
		float deltaMag_;
		

	public:
	// CONSTRUCTOR
	/** @fn Src()
	 *  @brief empty constructor for map **/
		Src();
	/** @fn Src
	 *  @brief constructor with magnitude for sort in list
	 *  @param double magnitude of the source **/
		Src( double );

	// GETTER
		double ra () const;
		double dec() const;
		double mag() const;
		long   id () const;
		
		float deltaRa () const;
		float deltaDec() const;
		float deltaMag() const;
		
		Coord<double,double> coord () const;

	// SETTER
	/** @fn build
	 *  @brief set all value with two coordonates, usefull for loop
	 *  @param Coord<double,double> (Ra,Dec)
	 *  @param Coord<double,long>  (Mag,Id)
	 *  @return None **/
	void build( Coord<double,double> , Coord<double,long> );
	
	/** @fn delta
	 *  @brief compute delta between current source and an other source
	 *  @param const Src & Source of reference
	 *  @return None **/
	void delta( const Src &a );
	
	/** @fn str
	 *  @brief return a string with information about source
	 *  @return string **/
	std::string str() const;
};

// OPERATORS
/** @fn operator<
 *  @brief for map sort with coordonate
 *  @return bool **/
bool operator < (const Src &a, const Src &b);
bool operator == (const Src &a, const Src &b);

std::ostream& operator<<(std::ostream &o, const Src &a);

// FUNCTIONS
/** @fn opMag
 *  @brief comparaison of two sources with theire magnitude
 *  @param const Src & Two sources to compare **/
bool opMag( const Src &a , const Src &b );

#endif