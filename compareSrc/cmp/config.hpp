
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
const double epsi = 0.0005555555555555556;
const double epsi2 = epsi*epsi;

const std::string PATH_INPUT  = "/sps/lsst/dev/jmassot/data/src";
const std::string PATH_OUTPUT = "/sps/lsst/dev/jmassot/data/asso";

#endif
