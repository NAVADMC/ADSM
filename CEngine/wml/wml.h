/** @file wml.h
 * Interface to the Wild Magic Library.
 *
 * The Wild Magic Library (WML) is written by David H. Eberly.  The WML code
 * used here has been converted to C.  The entire WML source code is not here;
 * only enough parts to provide some needed functions.
 *
 * Magic Software, Inc.<br>
 * http://www.magic-software.com<br>
 * http://www.wild-magic.com<br>
 * Copyright &copy; 2003.  All Rights Reserved
 *
 * The Wild Magic Library (WML) source code is supplied under the terms of
 * the license agreement http://www.magic-software.com/License/WildMagic.pdf
 * and may not be copied or disclosed except in accordance with the terms of
 * that agreement.
 *
 * The WML license states, in part, "The Software may be used, edited,
 * modified, copied, and distributed by you for commercial products provided
 * that such products are not intended to wrap The Software solely for the
 * purposes of selling it as if it were your own product.  The intent of this
 * clause is that you use The Software, in part or in whole, to assist you in
 * building your own original products."
 */

#ifndef WML_H
#define WML_H

#include <glib.h>



/** A two-dimensional vector. */
typedef struct
{
  double X, Y;
}
WML_Vector2;



/* Operations on vectors. */

WML_Vector2 *WML_new_Vector2 (double fX, double fY);
WML_Vector2 *WML_new_Vector2v (const WML_Vector2 * rkV);
char *WML_Vector2_to_string (WML_Vector2 *);
void WML_free_Vector2 (WML_Vector2 *);

gboolean WML_Vector2_eq (WML_Vector2 *, WML_Vector2 *);
WML_Vector2 WML_Vector2_add (WML_Vector2 *, WML_Vector2 *);
WML_Vector2 WML_Vector2_sub (WML_Vector2 *, WML_Vector2 *);
WML_Vector2 WML_Vector2_mul (WML_Vector2 *, double);
void WML_Vector2_add_inplace (WML_Vector2 *, WML_Vector2 *);
void WML_Vector2_sub_inplace (WML_Vector2 *, WML_Vector2 *);
void WML_Vector2_mul_inplace (WML_Vector2 *, double);
#define WML_Vector2_negate(V) WML_Vector2_mul_inplace(V,-1)
WML_Vector2 *WML_Vector2_assign (WML_Vector2 * self, WML_Vector2 * rkV);

WML_Vector2 WML_Vector2_Perp (WML_Vector2 *);
double WML_Vector2_Length (WML_Vector2 *);
double WML_Vector2_SquaredLength (WML_Vector2 *);
double WML_Vector2_Dot (WML_Vector2 *, WML_Vector2 *);
double WML_Vector2_Normalize (WML_Vector2 *);
double WML_Vector2_Kross (WML_Vector2 *, WML_Vector2 *);



/** A two-dimensional box. */
typedef struct
{
  WML_Vector2 m_kCenter;
  WML_Vector2 m_akAxis[2];
  double m_afExtent[2];
}
WML_Box2;



/* Operations on boxes. */

WML_Box2 *WML_new_Box2 (void);
WML_Box2 *WML_clone_Box2 (WML_Box2 *);
char *WML_Box2_to_string (WML_Box2 *);
void WML_free_Box2 (WML_Box2 *);

/**
 * Returns the center of a Box.
 *
 * @param B a box.
 * @return the center.
 */
#define WML_Box2_Center(B) (&(B)->m_kCenter)

WML_Vector2 *WML_Box2_Axis (WML_Box2 *, int i);
WML_Vector2 *WML_Box2_Axes (WML_Box2 *);
double WML_Box2_Extent (WML_Box2 *, int i);
double *WML_Box2_Extents (WML_Box2 *);
void WML_Box2_ComputeVertices (WML_Box2 *, WML_Vector2 akVertex[4]);



/** Convex hull definitions and functions. */

typedef enum
{
  WML_HULL_POINT,
  WML_HULL_LINEAR,
  WML_HULL_PLANAR
}
WML_HullType;



/** for collinearity tests */
typedef enum
{
  WML_ORDER_POSITIVE,
  WML_ORDER_NEGATIVE,
  WML_ORDER_COLLINEAR_LEFT,
  WML_ORDER_COLLINEAR_RIGHT,
  WML_ORDER_COLLINEAR_CONTAIN
}
WML_OrderType;



typedef struct
{
  /* hull stored in counterclockwise order */
  /* vertex information */
  int m_iVQuantity;
  WML_Vector2 *m_akVertex;

  /* indices for ordered vertices of hull */
  int m_iHQuantity;
  int *m_aiHIndex;

  /* hull information */
  WML_HullType m_iHullType;
  GArray *m_kHull;

}
WML_ConvexHull2;



/* ConvexHull2 does not take ownership of the input array.  The application is
 * responsible for deleting it. */
WML_ConvexHull2 *WML_new_ConvexHull2 (int iVQuantity,
                                      WML_Vector2 * akVertex, gboolean bIncremental);
void WML_free_ConvexHull2 (WML_ConvexHull2 *);

int WML_ConvexHull2_GetQuantity (WML_ConvexHull2 *);
int *WML_ConvexHull2_GetIndices (WML_ConvexHull2 *);
gboolean WML_ConvexHull2_ContainsPoint (WML_ConvexHull2 *, WML_Vector2 *);



/* Minimum bounding box functions. */

WML_Box2 *WML_MinBox (int iQuantity, WML_Vector2 * akPoint);
WML_Box2 *WML_MinBoxOrderNSqr (int iQuantity, WML_Vector2 * akPoint);

#endif /* !WML_H */
