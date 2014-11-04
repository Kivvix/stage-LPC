/**
 * @file csv.cpp
 * @package compare
 * @author J. Massot
 * @date 2014-04-14
 * 
 * @brief Compare sources between 2 fits files
 */

#ifndef __CSV_HPP__
#define __CSV_HPP__

#include <iostream>
#include <fstream>
#include <map>
#include <set>
#include <string>
#include <algorithm>
#include <cmath>
#include <boost/lexical_cast.hpp>

#include "coord.hpp"
#include "src.hpp"

/** @fn csvToTab
 *  @brief convert `csv` file into associated table (map) [ (ra,dec) ] = (mag,id)
 *  @details `csv` file is formated `id,ra,dec,mag`
 *  @param `std::string fileName` name of csv file
 *  @param `std::set<long> save` list to save sources
 *  @return `std::map< Coord<double,double> , Coord<double,long> > tab` (Ra,Dec) => (mag,id) **/
std::map< Coord<double,double> , Coord<double,long> > csvToTab( std::string , std::set<Src> & );

#endif
