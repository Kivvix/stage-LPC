/**
 * @file errors.cpp
 * @package compare
 * @author J. Massot
 * @date 2014-04-14
 * 
 * @brief Print errors
 */

#include "errors.hpp"


/** @fn printErr
 *  @brief function call the print of errors into different `csv` files
 *  @param list of differents errors (multiSdss, aloneSdss, multiStack, aloneStack) **/
void printErr( std::ostringstream & error0 ,
               std::ostringstream & error1 ,
               std::ostringstream & error2 ,
               std::ostringstream & error3 ,
               std::string numFits )
{	
	error( 0 , error0 , numFits );
	error( 1 , error1 , numFits );
	error( 2 , error2 , numFits );
	error( 3 , error3 , numFits );
}

/** @fn error
 *  @brief print one error into a `csv` file
 *  @param `int errId` id of error ( 0:multiSdds, 1:aloneSdss , 2:multiStack , 3:aloneStack )
 *  @param `std::ostringstream & errors` stream whith errors of the id **/
void error( int errId , std::ostringstream & errors , std::string numFits )
{
	std::string nameFile, firstLine;
	switch ( errId ) {
		case 0:
			nameFile = PATH_OUTPUT+"/errors/sdss-multi-" + numFits + ".csv";
			firstLine = "idSdss1, raSdss1, decSdss1, magSdss1, idSdss2, raSdss2, decSdss2, magSdss2, idStack, raStack, decStack, magStack";
			break;
		case 1:
			nameFile = PATH_OUTPUT+"/errors/sdss-alone-" + numFits + ".csv";
			firstLine = "idSdss, raSdss, decSdss, magSdss";
			break;
		case 2:
			nameFile = PATH_OUTPUT+"/errors/stack-multi-" + numFits + ".csv";
			firstLine = "idStack1, raStack1, decStack1, magStack1, idStack2, raStack2, decStack2, magStack2, idSdss, raSdss, decSdss, magSdss";
			break;
		case 3:
			nameFile = PATH_OUTPUT+"/errors/stack-alone-" + numFits + ".csv";
			firstLine = "idStack, raStack, decStack, magStack";
			break;
	}
	std::ofstream f( nameFile.c_str() );
	if ( f ) {
		f << firstLine << std::endl;
		f << errors.str() << std::endl;
	}
	else {
		std::cout << "===================\n Can't open file : " << nameFile << std::endl;
		std::cout << "-------------------\n " << errors.str() << std::endl;
	}
	f.close();
}