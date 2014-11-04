/**
 * @file src.cpp
 * @package compare
 * @author J. Massot
 * @date 2014-04-14
 * 
 * @brief Class for Coordonate (double,double)
 */

#include "src.hpp"

// CONSTRUCTOR
/** @fn Src()
 *  @brief empty constructor for map **/
Src::Src () {
	ra_=0; dec_=0; mag_=0; deltaDec_=0; deltaRa_=0; deltaMag_=0; id_=0;
}
/** @fn Src
 *  @brief constructor with magnitude for sort in list
 *  @param `double deltaMag` magnitude of the source **/
Src::Src ( double deltaMag ) { deltaMag_ = deltaMag; }

// GETTER
double Src::ra  () const { return ra_;  }
double Src::dec () const { return dec_; }
double Src::mag () const { return mag_; }
long  Src::id  () const { return id_;  }

float Src::deltaRa  () const { return deltaRa_;  }
float Src::deltaDec () const { return deltaDec_; }
float Src::deltaMag () const { return deltaMag_; }

Coord<double,double> Src::coord () const
{ Coord<double,double> r(ra_,dec_); return r; }

// SETTER
/** @fn build
 *  @brief set all value with two coordonates, usefull for loop
 *  @param Coord<double,double> (Ra,Dec)
 *  @param Coord<double,long>  (Mag,Id)
 *  @return None **/
void Src::build( Coord<double,double> raDec , Coord<double,long> magId )
{
	ra_  = raDec.x(); dec_ = raDec.y();
	mag_ = magId.x(); id_  = magId.y();
	deltaRa_ = deltaDec_ = deltaMag_ = 0;
}

// METHODES
/** @fn delta
 *  @brief compute delta between current source and an other source
 *  @param const Src & Source of reference
 *  @return None **/
void Src::delta( const Src &a )
{
	deltaRa_  = a.ra()  - ra_;	
	deltaDec_ = a.dec() - dec_;
	deltaMag_ = a.mag() - mag_;	
}

/** @fn str
 *  @brief return a string with information about source
 *  @return string **/
std::string Src::str() const
{
	std::ostringstream tmp;
	tmp << id_ << "," << ra_ << "," << dec_ << "," << mag_ ;
	
	return tmp.str();
}

// OPERATORS
/** @fn operator<
 *  @brief for map sort with coordonate
 *  @return bool **/
bool operator < (const Src &a, const Src &b)
{ return a.coord() < b.coord(); }
bool operator == (const Src &a, const Src &b)
{ return a.id() == b.id(); }


std::ostream& operator<<(std::ostream &o, const Src &a)
{
    return o << "--- --- ---\n (ra,dec) = " << a.coord() << "\n\t mag : " << a.mag() << "\n\t id  : " << a.id() << "\n --- \n\t deltaCoord : " << a.deltaRa() << " , " << a.deltaDec() << "\n\t deltaMag : " << a.deltaMag() << std::endl;
}

// FUNCTIONS
/** @fn opMag
 *  @brief comparaison of two sources with theire magnitude for sort in list
 *  @param const Src & Two sources to compare
 *  @return bool **/
bool opMag( const Src &a , const Src &b )
{ return std::abs( a.deltaMag() )  <  std::abs( b.deltaMag() ); }
