/**
 * @file coord.hpp
 * @package compare
 * @author J. Massot
 * @date 2014-04-14
 * 
 * @brief Class for pair
 */


#ifndef __COORD_HPP__
#define __COORD_HPP__

#include <iostream>

#include "config.hpp"

/** 
 * @class Coord
 * @brief Class for pair of two values (like std::pair)
 * @param T x_ first data
 * @param U y_ second data
 **/
template <typename T, typename U>
class Coord
{
	private:
		T x_;
		U y_;

	public:
	// CONSTRUCTOR
	/** @fn Src
	 *  @brief empty constructor for map **/
		Coord ();
	/** @fn Src
	 *  @brief full constructor to build all Coord **/
		Coord ( T , U );

	// GETTER
		/** @fn x
		 *  @brief get variable x_ **/
		T x () const;
		/** @fn y
		 *  @brief get variable y_ **/
		U y () const;

	// SETTER
		/** @fn x
		 *  @brief set variable x_ **/
		void x ( T );
		/** @fn y
		 *  @brief set variable Y_ **/
		void y ( U );
		/** @fn xy
		 *  @brief set x and y **/
		void xy( T , U );
};

//OPERATORS
/** @fn operator<
 *  @brief for map sort with coordinates
 *  @return bool true if A.x < B.x or if A.x = B.x and A.y < B.y **/
template <typename T, typename U>
bool operator < ( const Coord<T,U> & , const Coord<T,U> & );

/** @fn operator%
 *  @brief notion of neightboorhood of two coordinates
 *  @return bool true if dist(A,B) < epsi with dist a norm for square ball **/
template <typename T, typename U>
bool operator % ( const Coord<T,U> & , const Coord<T,U> & );

/** @fn operator<<
 *  @brief for display
 *  @return std::ostream& stream formated : (x,y) **/
template <typename T, typename U>
std::ostream& operator << ( std::ostream & , const Coord<T,U> & );

#include "coord.cxx"

#endif

