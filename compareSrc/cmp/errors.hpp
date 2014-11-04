/**
 * @file errors.hpp
 * @package compare
 * @author J. Massot
 * @date 2014-04-14
 * 
 * @brief Print errors
 */

#ifndef __ERRORS_HPP__
#define __ERRORS_HPP__

#include <iostream>
#include <fstream>
#include <sstream>

#include "config.hpp"

/** @fn printErr
 *  @brief function call the print of errors into different `csv` files
 *  @param list of differents errors (multiSdss, aloneSdss, multiStack, aloneStack) **/
void printErr( std::ostringstream & ,
               std::ostringstream & ,
               std::ostringstream & ,
               std::ostringstream & ,
               std::string );

/** @fn error
 *  @brief print one error into a `csv` file
 *  @param `int errId` id of error ( 0:multiSdds, 1:aloneSdss , 2:multiStack , 3:aloneStack )
 *  @param `std::ostringstream & errors` stream whith errors of the id **/
void error( int , std::ostringstream & , std::string );

#endif