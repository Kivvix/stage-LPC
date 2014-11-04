/**
 * @file coord.cxx
 * @package compare
 * @author J. Massot
 * @date 2014-04-14
 * 
 * @brief Class for coordinates (T,U) (like std::pair)
 */

// CONSTRUCTORS
/** @fn Src
 *  @brief empty constructor for map **/
template <typename T, typename U>
Coord<T,U>::Coord () { }

/** @fn Src
 *  @brief full constructor to build all Coord **/
template <typename T, typename U>
Coord<T,U>::Coord ( T x , U y ): x_(x), y_(y) { }


// GETTERS
/** @fn x
 *  @brief get variable x_ **/
template <typename T, typename U>
T Coord<T,U>::x () const { return x_; }
/** @fn y
 *  @brief get variable y_ **/
template <typename T, typename U>
U Coord<T,U>::y () const { return y_; }


// SETTERS
/** @fn x
 *  @brief set variable x_ **/
template <typename T, typename U>
void Coord<T,U>::x ( T x ) { x_ = x; }
/** @fn y
 *  @brief set variable Y_ **/
template <typename T, typename U>
void Coord<T,U>::y ( U y ) { y_ = y; }

/** @fn xy
 *  @brief set x and y **/
template <typename T, typename U>
void Coord<T,U>::xy ( T x , U y ) { x_ = x; y_ = y; }


// OPERATORS
/** @fn operator<
 *  @brief for map sort with coordinates
 *  @return bool true if A.x < B.x or if A.x = B.x and A.y < B.y **/
template <typename T, typename U>
bool operator < ( const Coord<T,U> &A , const Coord<T,U> &B )
{
    return (A.x() < B.x()) || ((A.x() == B.x()) && (A.y() < B.y()));
}

/** @fn operator%
 *  @brief notion of neightboorhood of two coordinates
 *  @return bool true if dist(A,B) < epsi with dist a norm for square ball **/
template <typename T, typename U>
bool operator % ( const Coord<T,U> &A , const Coord<T,U> &B )
{
	T deltaX = A.x() - B.x();
	U deltaY = A.y() - B.y();
	if ( deltaX*deltaX < epsi2 ) {
		if ( deltaY * deltaY < epsi2 ) {
			return true;
		}
	}
	return false;
	return ( deltaX * deltaX  <  epsi2 ) && ( deltaY * deltaY  <  epsi2 );
}

/** @fn operator<<
 *  @brief for display
 *  @return std::ostream& stream formated : (x,y) **/
template <typename T, typename U>
std::ostream& operator << ( std::ostream &o , const Coord<T,U> &X )
{
    return o << "(" << X.x() << "," << X.y() << ")";
}
