/**
 * @file hist.hpp
 * @package compare
 * @author J. Massot
 * @date 2014-06-16
 * 
 * @brief Display histograms
 */
 
#ifndef __HIST_HPP__
#define __HIST_HPP__
 
#include <iostream>
#include <string>
#include <vector>

#include "root.hpp"
#include "config.hpp"

void hCoord( std::vector< std::vector<float> > & , std::string run );

void hMag( std::vector< std::vector<float> > & , std::string run );

#endif