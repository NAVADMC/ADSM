/** @file wml.c
 * Functions from the Wild Magic Library (WML).
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

#if HAVE_CONFIG_H
#  include "config.h"
#endif

#if STDC_HEADERS
#  include <string.h>
#endif

#include "wml.h"
#include <glib.h>

#if HAVE_MATH_H
#  include <math.h>
#endif

#define EPSILON 1e-06
#define COLLINEAR_EPSILON 1e-06



/* special vectors */
WML_Vector2 ZERO = { 0.0, 0.0 };
WML_Vector2 UNIT_X = { 1.0, 0.0 };
WML_Vector2 UNIT_Y = { 0.0, 1.0 };



/**
 * Creates a new Vector.
 *
 * @param fX the <i>x</i>-coordinate.
 * @param fY the <i>y</i>-coordinate.
 * @return a newly-allocated Vector object.
 */
WML_Vector2 *
WML_new_Vector2 (double fX, double fY)
{
  WML_Vector2 *self;

  self = g_new (WML_Vector2, 1);

  self->X = fX;
  self->Y = fY;

  return self;
}



/**
 * Creates a new Vector.
 *
 * @param rkV a Vector.
 * @return a newly-allocated Vector object that is a copy of <i>rkV</i>.
 */
WML_Vector2 *
WML_new_Vector2v (const WML_Vector2 * rkV)
{
  WML_Vector2 *self;

  self = g_new (WML_Vector2, 1);

  memcpy (self, rkV, sizeof (WML_Vector2));

  return self;
}



/**
 * Returns a text representation of a Vector.
 *
 * @param self a vector.
 * @return a string.
 */
char *
WML_Vector2_to_string (WML_Vector2 * self)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<%g,%g>", self->X, self->Y);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Deletes a Vector from memory.
 *
 * @param self a vector.
 */
void
WML_free_Vector2 (WML_Vector2 * self)
{
  if (self == NULL)
    return;

  g_free (self);
}



/**
 * Assigns one Vector to another.
 *
 * @param self the destination vector.
 * @param rkV the source vector.
 * @return the destination vector.
 */
WML_Vector2 *
WML_Vector2_assign (WML_Vector2 * self, WML_Vector2 * rkV)
{
  memcpy (self, rkV, sizeof (WML_Vector2));
  return self;
}



/**
 * Tests whether two Vectors are equal.
 *
 * @param self a vector.
 * @param rkV a vector.
 * @return TRUE if the vectors are identical; FALSE otherwise.
 */
gboolean
WML_Vector2_eq (WML_Vector2 * self, WML_Vector2 * rkV)
{
  return memcmp (self, rkV, sizeof (WML_Vector2)) == 0;
}



/**
 * Adds one vector to another.
 *
 * @param self the first vector.
 * @param rkV the second vector.
 * @return <i>self</i> + <i>rkV</i>.
 */
WML_Vector2
WML_Vector2_add (WML_Vector2 * self, WML_Vector2 * rkV)
{
  WML_Vector2 kSum;

  kSum.X = self->X + rkV->X;
  kSum.Y = self->Y + rkV->Y;
  return kSum;
}



/**
 * Adds one vector from another, leaving the result in the first vector.
 *
 * @param self the first vector.
 * @param rkV the second vector.
 */
void
WML_Vector2_add_inplace (WML_Vector2 * self, WML_Vector2 * rkV)
{
  self->X += rkV->X;
  self->Y += rkV->Y;
}




/**
 * Subtracts one vector from another.
 *
 * @param self the first vector.
 * @param rkV the second vector.
 * @return <i>self</i> - <i>rkV</i>.
 */
WML_Vector2
WML_Vector2_sub (WML_Vector2 * self, WML_Vector2 * rkV)
{
  WML_Vector2 kDiff;

  kDiff.X = self->X - rkV->X;
  kDiff.Y = self->Y - rkV->Y;
  return kDiff;
}



/**
 * Subtracts one vector from another, leaving the result in the first vector.
 *
 * @param self the first vector.
 * @param rkV the second vector.
 */
void
WML_Vector2_sub_inplace (WML_Vector2 * self, WML_Vector2 * rkV)
{
  self->X -= rkV->X;
  self->Y -= rkV->Y;
}



/**
 * Multiplies a vector by a scalar.
 *
 * @param self the first vector.
 * @param m the number to scale by.
 * @return <i>self</i> * <i>m</i>.
 */
WML_Vector2
WML_Vector2_mul (WML_Vector2 * self, double m)
{
  WML_Vector2 kProd;

  kProd.X = self->X * m;
  kProd.Y = self->Y * m;
  return kProd;
}



/**
 * Multiplies a vector by a scalar, leaving the result in the vector.
 *
 * @param self a vector.
 * @param m the number to scale by.
 */
void
WML_Vector2_mul_inplace (WML_Vector2 * self, double m)
{
  self->X *= m;
  self->Y *= m;
}



/**
 * Returns a vector perpendicular to the given one.
 *
 * @param self a vector (<i>x</i>,<i>y</i>).
 * @return the vector (<i>y</i>,-<i>x</i>).
 */
WML_Vector2
WML_Vector2_Perp (WML_Vector2 * self)
{
  WML_Vector2 kPerp;

  kPerp.X = self->Y;
  kPerp.Y = -(self->X);
  return kPerp;
}



/**
 * Finds the length of a vector.
 *
 * @param self a vector.
 * @return the length.
 */
double
WML_Vector2_Length (WML_Vector2 * self)
{
  double fSqrLen = 0.0;

  fSqrLen = self->X * self->X + self->Y * self->Y;
  return sqrt (fSqrLen);
}



/**
 * Finds the squared length of a vector.
 *
 * @param self a vector.
 * @return the squared length.
 */
double
WML_Vector2_SquaredLength (WML_Vector2 * self)
{
  double fSqrLen = 0.0;

  fSqrLen = self->X * self->X + self->Y * self->Y;
  return fSqrLen;
}



/**
 * Finds the dot product of two vectors.
 *
 * @param self the first vector.
 * @param rkV the second vector.
 * @return <i>self</i> \htmlonly &middot; \endhtmlonly \latexonly $\dot$ \endlatexonly <i>rkV</i>.
 */
double
WML_Vector2_Dot (WML_Vector2 * self, WML_Vector2 * rkV)
{
  return self->X * rkV->X + self->Y * rkV->Y;
}



/**
 * Normalizes a vector.
 *
 * @param self a vector.
 * @return the length of the vector before normalization.
 */
double
WML_Vector2_Normalize (WML_Vector2 * self)
{
  double fLength, fInvLength;

  fLength = WML_Vector2_Length (self);
  if (fLength > EPSILON)
    {
      fInvLength = 1.0 / fLength;
      self->X *= fInvLength;
      self->Y *= fInvLength;
    }
  else
    {
      fLength = 0;
      self->X = self->Y = 0;
    }

  return fLength;
}



/**
 * Finds the cross product of two vectors.
 *
 * @param self the first vector.
 * @param rkV the second vector.
 * @return Cross((x,y,0),(V.x,V.y,0)) = x*V.y - y*V.x.
 */
double
WML_Vector2_Kross (WML_Vector2 * self, WML_Vector2 * rkV)
{
  return self->X * rkV->Y - self->Y * rkV->X;
}



/**
 * Creates a new Box.  No initialization for efficiency.
 *
 * @return a newly-allocated Box object.
 */
WML_Box2 *
WML_new_Box2 (void)
{
  WML_Box2 *self;

  self = g_new (WML_Box2, 1);

  return self;
}



/**
 * Creates a deep copy of an existing Box.
 *
 * @param other the box to copy.
 * @return a newly-allocated Box object.
 */
WML_Box2 *
WML_clone_Box2 (WML_Box2 * other)
{
  WML_Box2 *self;
  int i;

  self = g_new (WML_Box2, 1);
  WML_Vector2_assign (WML_Box2_Center (self), WML_Box2_Center (other));
  for (i = 0; i < 2; i++)
    {
      WML_Vector2_assign (WML_Box2_Axis (self, i), WML_Box2_Axis (other, i));
      self->m_afExtent[i] = other->m_afExtent[i];
    }

  return self;
}



/**
 * Returns a text representation of a Box.
 *
 * @param self a box.
 * @return a string.
 */
char *
WML_Box2_to_string (WML_Box2 * self)
{
  GString *s;
  char *chararray, *substring;

  s = g_string_new ("<Box2");

  substring = WML_Vector2_to_string (&self->m_kCenter);
  g_string_append_printf (s, " center=%s", substring);
  g_free (substring);

  substring = WML_Vector2_to_string (&self->m_akAxis[0]);
  g_string_append_printf (s, " 1st axis=%s", substring);
  g_free (substring);

  substring = WML_Vector2_to_string (&self->m_akAxis[1]);
  g_string_append_printf (s, " 2nd axis=%s", substring);
  g_free (substring);

  g_string_append_printf (s, " extents=<%g,%g>>", self->m_afExtent[0], self->m_afExtent[1]);

  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Deletes a Box from memory.
 *
 * @param self a box.
 */
void
WML_free_Box2 (WML_Box2 * self)
{
  if (self != NULL)
    g_free (self);
}




/**
 * Returns the <i>i</i>th axis of a Box.
 *
 * @param self a box.
 * @param i the axis to choose, either 0 or 1.
 * @return the <i>i</i>th axis.
 */
WML_Vector2 *
WML_Box2_Axis (WML_Box2 * self, int i)
{
  g_assert (0 <= i && i < 2);
  return &self->m_akAxis[i];
}



/**
 * Returns the axes of a Box.
 *
 * @param self a box.
 * @return the axes (a 2-element array).
 */
WML_Vector2 *
WML_Box2_Axes (WML_Box2 * self)
{
  return self->m_akAxis;
}



/**
 * Returns the <i>i</i>th extent of a Box.
 *
 * @param self a box.
 * @param i the extent to choose, either 0 or 1.
 * @return the <i>i</i>th extent.
 */
double
WML_Box2_Extent (WML_Box2 * self, int i)
{
  g_assert (0 <= i && i < 2);
  return self->m_afExtent[i];
}



/**
 * Returns the extents of a Box.
 *
 * @param self a box.
 * @return the extents (a 2-element array).
 */
double *
WML_Box2_Extents (WML_Box2 * self)
{
  return self->m_afExtent;
}



/**
 * Finds the vertices of a Box.
 *
 * @param self a box.
 * @param akVertex an array of 4 Vectors in which to store the vertices.
 */
void
WML_Box2_ComputeVertices (WML_Box2 * self, WML_Vector2 akVertex[4])
{
  WML_Vector2 akEAxis[2];

  akEAxis[0] = WML_Vector2_mul (&self->m_akAxis[0], self->m_afExtent[0]);
  akEAxis[1] = WML_Vector2_mul (&self->m_akAxis[1], self->m_afExtent[1]);

  WML_Vector2_assign (&akVertex[0], &self->m_kCenter);
  WML_Vector2_sub_inplace (&akVertex[0], &akEAxis[0]);
  WML_Vector2_sub_inplace (&akVertex[0], &akEAxis[1]);

  WML_Vector2_assign (&akVertex[1], &self->m_kCenter);
  WML_Vector2_add_inplace (&akVertex[1], &akEAxis[0]);
  WML_Vector2_sub_inplace (&akVertex[1], &akEAxis[1]);

  WML_Vector2_assign (&akVertex[2], &self->m_kCenter);
  WML_Vector2_add_inplace (&akVertex[2], &akEAxis[0]);
  WML_Vector2_add_inplace (&akVertex[2], &akEAxis[1]);

  WML_Vector2_assign (&akVertex[3], &self->m_kCenter);
  WML_Vector2_sub_inplace (&akVertex[3], &akEAxis[0]);
  WML_Vector2_add_inplace (&akVertex[3], &akEAxis[1]);
}



/* for sorting */
typedef struct
{
  WML_Vector2 m_kV;
  int m_iIndex;
}
WML_SortedVertex;



/**
 * Returns a text representation of a SortedVertex object.
 *
 * @param self a sorted vertex.
 * @return a string.
 */
char *
WML_SortedVertex_to_string (WML_SortedVertex * self)
{
  GString *s;
  char *substring, *chararray;

  s = g_string_new (NULL);
  substring = WML_Vector2_to_string (&(self->m_kV));
  g_string_sprintf (s, "%s#%i", substring, self->m_iIndex);
  g_free (substring);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Assigns one SortedVertex object to another.
 *
 * @param self the destination sorted vertex.
 * @param rkSV the source sorted vertex.
 * @return the destination sorted vertex.
 */
WML_SortedVertex *
WML_SortedVertex_assign (WML_SortedVertex * self, WML_SortedVertex * rkSV)
{
  WML_Vector2_assign (&(self->m_kV), &(rkSV->m_kV));
  self->m_iIndex = rkSV->m_iIndex;
  return self;
}



/**
 * Tests whether two SortedVertex objects are equal.
 *
 * @param self a sorted vertex.
 * @param rkSV a sorted vertex.
 * @return TRUE if the vertices are identical; FALSE otherwise.
 */
gboolean
WML_SortedVertex_eq (WML_SortedVertex * self, WML_SortedVertex * rkSV)
{
  return WML_Vector2_eq (&(self->m_kV), &(rkSV->m_kV));
}



/**
 * Tests whether one SortedVertex object is less than another.
 *
 * @param self a sorted vertex.
 * @param rkSV a sorted vertex.
 * @return TRUE if <i>self</i> < <i>rkSV</i>; FALSE otherwise.
 */
gboolean
WML_SortedVertex_lt (WML_SortedVertex * self, WML_SortedVertex * rkSV)
{
  if (self->m_kV.X < rkSV->m_kV.X)
    return TRUE;
  if (self->m_kV.X > rkSV->m_kV.X)
    return FALSE;
  return self->m_kV.Y < rkSV->m_kV.Y;
}



/**
 * A comparison function for SortedVertex objects suitable for GArray's sort
 * function.
 *
 * @param a a sorted vertex, cast to a gconstpointer.
 * @param b a sorted vertex, cast to a gconstpointer.
 * @return -1 if a < b, 0 if a = b, or 1 if a > b.
 */
gint
WML_SortedVertex_cmp (gconstpointer a, gconstpointer b)
{
  WML_SortedVertex *sv1, *sv2;

  sv1 = (WML_SortedVertex *) a;
  sv2 = (WML_SortedVertex *) b;

  if (WML_SortedVertex_eq (sv1, sv2))
    return 0;
  else if (WML_SortedVertex_lt (sv1, sv2))
    return -1;
  else
    return 1;
}



/**
 * test if point is contained by hull.
 */
gboolean
WML_ConvexHull2_ContainsPoint (WML_ConvexHull2 * self, WML_Vector2 * rkP)
{
  int i0, i1;
  WML_Vector2 *rkV0, *rkV1;
  WML_Vector2 kDir, kNormal, tmp;

  for (i1 = 0, i0 = self->m_iHQuantity - 1; i1 < self->m_iHQuantity; i0 = i1++)
    {
      rkV0 = &(self->m_akVertex[self->m_aiHIndex[i0]]);
      rkV1 = &(self->m_akVertex[self->m_aiHIndex[i1]]);
      kDir = WML_Vector2_sub (rkV1, rkV0);
      kNormal = WML_Vector2_Perp (&kDir);       /* outer normal */

      tmp = WML_Vector2_sub (rkP, rkV0);
      if (WML_Vector2_Dot (&kNormal, &tmp) > 0.0)
        return FALSE;
    }

  return TRUE;
}



/**
 *
 */
WML_OrderType
WML_CollinearTest (WML_Vector2 * rkP, WML_Vector2 * rkQ0, WML_Vector2 * rkQ1)
{
  WML_Vector2 kD, kA;
  double fDdD, fAdA, fDet, fRelative, fDdA;

  kD = WML_Vector2_sub (rkQ1, rkQ0);
  kA = WML_Vector2_sub (rkP, rkQ0);
  fDdD = WML_Vector2_Dot (&kD, &kD);
  fAdA = WML_Vector2_Dot (&kA, &kA);
  fDet = WML_Vector2_Kross (&kD, &kA);
  fRelative = fDet * fDet - COLLINEAR_EPSILON * fDdD * fAdA;

  if (fRelative > 0.0)
    {
      if (fDet > 0.0)
        {
          /* points form counterclockwise triangle <P,Q0,Q1> */
          return WML_ORDER_POSITIVE;
        }
      else if (fDet < 0.0)
        {
          /* points form clockwise triangle <P,Q1,Q0> */
          return WML_ORDER_NEGATIVE;
        }
    }

  /* P is on line of <Q0,Q1> */
  fDdA = WML_Vector2_Dot (&kD, &kA);
  if (fDdA < 0.0)
    {
      /* order is <P,Q0,Q1> */
      return WML_ORDER_COLLINEAR_LEFT;
    }

  if (fDdA > fDdD)
    {
      /* order is <Q0,Q1,P> */
      return WML_ORDER_COLLINEAR_RIGHT;
    }

  /* order is <Q0,P,Q1> */
  return WML_ORDER_COLLINEAR_CONTAIN;
}



void
WML_MergeLinear (WML_ConvexHull2 * self, WML_SortedVertex * rkP)
{
  WML_SortedVertex kCopy;

#if DEBUG
  g_debug ("----- ENTER WML_MergeLinear");
#endif

  switch (WML_CollinearTest
          (&(rkP->m_kV),
           &(g_array_index (self->m_kHull, WML_SortedVertex, 0).m_kV),
           &(g_array_index (self->m_kHull, WML_SortedVertex, 1).m_kV)))
    {
    case WML_ORDER_POSITIVE:
      {
        /* merged hull is <P,Q0,Q1> */
        self->m_iHullType = WML_HULL_PLANAR;
        WML_SortedVertex_assign (&kCopy, &g_array_index (self->m_kHull, WML_SortedVertex, 1));
        g_array_append_val (self->m_kHull, kCopy);
        WML_SortedVertex_assign (&g_array_index
                                 (self->m_kHull, WML_SortedVertex, 1),
                                 &g_array_index (self->m_kHull, WML_SortedVertex, 0));
        WML_SortedVertex_assign (&g_array_index (self->m_kHull, WML_SortedVertex, 0), rkP);
        break;
      }
    case WML_ORDER_NEGATIVE:
      {
        /* merged hull is <P,Q1,Q0> */
        self->m_iHullType = WML_HULL_PLANAR;
        WML_SortedVertex_assign (&kCopy, &g_array_index (self->m_kHull, WML_SortedVertex, 0));
        g_array_append_val (self->m_kHull, kCopy);
        WML_SortedVertex_assign (&g_array_index (self->m_kHull, WML_SortedVertex, 0), rkP);
        break;
      }
    case WML_ORDER_COLLINEAR_LEFT:
      /* linear order is <P,Q0,Q1>, merged hull is <P,Q1> */
      WML_SortedVertex_assign (&g_array_index (self->m_kHull, WML_SortedVertex, 0), rkP);
      break;
    case WML_ORDER_COLLINEAR_RIGHT:
      /* linear order is <Q0,Q1,P>, merged hull is <Q0,P> */
      WML_SortedVertex_assign (&g_array_index (self->m_kHull, WML_SortedVertex, 1), rkP);
      break;
    case WML_ORDER_COLLINEAR_CONTAIN:
      g_assert_not_reached();
      /* case WML_ORDER_COLLINEAR_CONTAIN:  linear order is <Q0,P,Q1>, no change */
    }

#if DEBUG
  g_debug ("----- EXIT WML_MergeLinear");
#endif

  return;
}



void
WML_MergePlanar (WML_ConvexHull2 * self, WML_SortedVertex * rkP)
{
  int iSize;
  int i, iU, iL;
  WML_OrderType iCT;
  GArray *kTmpHull = NULL, *tmp;

#if DEBUG
  g_debug ("----- ENTER WML_MergePlanar");
#endif

  iSize = self->m_kHull->len;

  /* search counterclockwise for last visible vertex */
  for (iU = 0, i = 1; iU < iSize; iU = i++)
    {
      if (i == iSize)
        i = 0;

      iCT =
        WML_CollinearTest (&(rkP->m_kV),
                           &(g_array_index
                             (self->m_kHull, WML_SortedVertex, iU).m_kV),
                           &(g_array_index (self->m_kHull, WML_SortedVertex, i).m_kV));
      if (iCT == WML_ORDER_NEGATIVE)
        continue;
      if (iCT == WML_ORDER_POSITIVE || iCT == WML_ORDER_COLLINEAR_LEFT)
        break;

      /* iCT == WML_ORDER_COLLINEAR_CONTAIN || iCT == WML_ORDER_COLLINEAR_RIGHT */
      goto end;
    }
  g_assert (iU < iSize);

  /* search clockwise for last visible vertex */
  for (iL = 0, i = iSize - 1; i >= 0; iL = i--)
    {
      iCT =
        WML_CollinearTest (&(rkP->m_kV),
                           &(g_array_index
                             (self->m_kHull, WML_SortedVertex, i).m_kV),
                           &(g_array_index (self->m_kHull, WML_SortedVertex, iL).m_kV));
      if (iCT == WML_ORDER_NEGATIVE)
        continue;
      if (iCT == WML_ORDER_POSITIVE || iCT == WML_ORDER_COLLINEAR_RIGHT)
        break;

      /* iCT == WML_ORDER_COLLINEAR_CONTAIN || iCT == WML_ORDER_COLLINEAR_LEFT */
      goto end;
    }
  g_assert (i >= 0);

  if (iU == iL)
    {
      /* This probably occurs when CollinearTest should report collinearity,
       * but does not.  If it does occur, and you care about this code
       * block not occurring, try increasing the size of the collinear
       * epsilon.  When this block does occur, the conclusion is that the
       * input point is collinear with an edge of the hull, so just return. */
      goto end;
    }

  /* construct the counterclockwise-ordered merged-hull vertices */
  kTmpHull = g_array_new (FALSE, FALSE, sizeof (WML_SortedVertex));
  g_array_append_val (kTmpHull, *rkP);
  while (TRUE)
    {
      g_array_append_val (kTmpHull, g_array_index (self->m_kHull, WML_SortedVertex, iU));
      if (iU == iL)
        break;

      if (++iU == iSize)
        iU = 0;
    }
  g_assert (kTmpHull->len > 2);

  tmp = self->m_kHull;
  self->m_kHull = kTmpHull;
  g_array_free (tmp, TRUE);

end:
#if DEBUG
  g_debug ("----- EXIT WML_MergePlanar");
#endif

  return;
}



/**
 * incremental hull
 */
void
WML_ByIncremental (WML_ConvexHull2 * self)
{
  /* In C++ this variable is a vector of SortedVertex objects. */
  GArray *kSVArray = NULL;
  int i;
  WML_SortedVertex sv;
#if DEBUG
  GString *s;
  char *substring;
  int j;
#endif

#if DEBUG
  g_debug ("----- ENTER WML_ByIncremental");
#endif

  /* Sort by x-component and store in contiguous array.  The sort is
   * O(N log N). */
  kSVArray = g_array_sized_new (FALSE, FALSE, sizeof (WML_SortedVertex), self->m_iVQuantity);
  for (i = 0; i < self->m_iVQuantity; i++)
    {
      sv.m_kV = self->m_akVertex[i];
      sv.m_iIndex = i;
      g_array_append_val (kSVArray, sv);
    }
#if DEBUG
  s = g_string_new ("vertices (unsorted):\n");
  for (i = 0; i < self->m_iVQuantity; i++)
    {
      substring = WML_SortedVertex_to_string (&g_array_index (kSVArray, WML_SortedVertex, i));
      g_string_sprintfa (s, (i > 0) ? ", %s" : "%s", substring);
      g_free (substring);
    }
  g_debug ("%s", s->str);
  g_string_free (s, TRUE);
#endif
  g_array_sort (kSVArray, WML_SortedVertex_cmp);
#if DEBUG
  s = g_string_new ("sorted by x:\n");
  for (i = 0; i < self->m_iVQuantity; i++)
    {
      substring = WML_SortedVertex_to_string (&g_array_index (kSVArray, WML_SortedVertex, i));
      g_string_sprintfa (s, (i > 0) ? ", %s" : "%s", substring);
      g_free (substring);
    }
  g_debug ("%s", s->str);
  g_string_free (s, TRUE);
#endif

  /* remove duplicate points */
  i = self->m_iVQuantity - 1;
  while (i > 0)
    {
      if (WML_SortedVertex_eq
          (&g_array_index (kSVArray, WML_SortedVertex, i),
           &g_array_index (kSVArray, WML_SortedVertex, i - 1)))
        g_array_remove_index (kSVArray, i);
      i--;
    }
#if DEBUG
  s = g_string_new ("with duplicates removed:\n");
  for (i = 0; i < kSVArray->len; i++)
    {
      substring = WML_SortedVertex_to_string (&g_array_index (kSVArray, WML_SortedVertex, i));
      g_string_sprintfa (s, (i > 0) ? ", %s" : "%s", substring);
      g_free (substring);
    }
  g_debug ("%s", s->str);
  g_string_free (s, TRUE);
#endif

  /* Compute convex hull incrementally.  The first and second vertices in
   * the hull are managed separately until at least one triangle is formed.
   * At that time an array is used to store the hull in counterclockwise
   * order. */
  self->m_iHullType = WML_HULL_POINT;

  self->m_kHull = g_array_new (FALSE, FALSE, sizeof (WML_SortedVertex));
  g_array_append_val (self->m_kHull, g_array_index (kSVArray, WML_SortedVertex, 0));
#if DEBUG
  s = g_string_new ("hull (start):\n");
  for (i = 0; i < self->m_kHull->len; i++)
    {
      substring = WML_SortedVertex_to_string (&g_array_index (self->m_kHull, WML_SortedVertex, i));
      g_string_sprintfa (s, (i > 0) ? ", %s" : "%s", substring);
      g_free (substring);
    }
  g_debug ("%s", s->str);
  g_string_free (s, TRUE);
#endif
  for (i = 1; i < kSVArray->len; i++)
    {
      switch (self->m_iHullType)
        {
        case WML_HULL_POINT:
          self->m_iHullType = WML_HULL_LINEAR;
          g_array_append_val (self->m_kHull, g_array_index (kSVArray, WML_SortedVertex, i));
          break;
        case WML_HULL_LINEAR:
          WML_MergeLinear (self, &g_array_index (kSVArray, WML_SortedVertex, i));
          break;
        case WML_HULL_PLANAR:
          WML_MergePlanar (self, &g_array_index (kSVArray, WML_SortedVertex, i));
          break;
        }
#if DEBUG
      s = g_string_new (NULL);
      substring = WML_SortedVertex_to_string (&g_array_index (kSVArray, WML_SortedVertex, i));
      g_string_sprintf (s, "hull (after considering %s):\n", substring);
      g_free (substring);
      for (j = 0; j < self->m_kHull->len; j++)
        {
          substring =
            WML_SortedVertex_to_string (&g_array_index (self->m_kHull, WML_SortedVertex, j));
          g_string_sprintfa (s, (j > 0) ? ", %s" : "%s", substring);
          g_free (substring);
        }
      g_debug ("%s", s->str);
      g_string_free (s, TRUE);
#endif
    }

  /* construct index array for ordered vertices of convex hull */
  self->m_iHQuantity = self->m_kHull->len;
  self->m_aiHIndex = g_new (int, self->m_iHQuantity);
  for (i = 0; i < self->m_iHQuantity; i++)
    self->m_aiHIndex[i] = g_array_index (self->m_kHull, WML_SortedVertex, i).m_iIndex;

#if DEBUG
  g_debug ("----- EXIT WML_ByIncremental");
#endif

  return;
}



void
WML_RemoveCollinear (WML_ConvexHull2 * self)
{
  GArray *kHull = NULL;
  int i0, i1, i2;
  WML_OrderType iCT;

#if DEBUG
  g_debug ("----- ENTER WML_RemoveCollinear");
#endif

  if (self->m_iHQuantity <= 2)
    goto end;

  kHull = g_array_sized_new (FALSE, FALSE, sizeof (int), self->m_iHQuantity);
  for (i0 = self->m_iHQuantity - 1, i1 = 0, i2 = 1; i1 < self->m_iHQuantity;)
    {
      iCT = WML_CollinearTest (&(self->m_akVertex[self->m_aiHIndex[i0]]),
                               &(self->m_akVertex[self->m_aiHIndex[i1]]),
                               &(self->m_akVertex[self->m_aiHIndex[i2]]));

      if (iCT == WML_ORDER_POSITIVE || iCT == WML_ORDER_NEGATIVE)
        {
          /* points are not collinear */
          g_array_append_val (kHull, self->m_aiHIndex[i1]);
        }

      i0 = i1++;
      if (++i2 == self->m_iHQuantity)
        i2 = 0;
    }

  /* construct index array for ordered vertices of convex hull */
  self->m_iHQuantity = kHull->len;
  g_free (self->m_aiHIndex);
  self->m_aiHIndex = g_new (int, self->m_iHQuantity);
  memcpy (self->m_aiHIndex, kHull->data, self->m_iHQuantity * sizeof (int));

  g_array_free (kHull, TRUE);

end:
#if DEBUG
  g_debug ("----- EXIT WML_RemoveCollinear");
#endif

  return;
}



/**
 * Constructor.  ConvexHull2 does not take ownership of the input array.  The
 * application is responsible for deleting it.
 *
 * @param iVQuantity the number of points.
 * @param akVertex the points.
 * @param bIncremental if TRUE, the convex hull is computed by the
 *   "incremental" method; otherwise, the convex hull is computer by the
 *   "divide and conquer" method.
 * @returns a newly-allocated convex hull object.
 */
WML_ConvexHull2 *
WML_new_ConvexHull2 (int iVQuantity, WML_Vector2 * akVertex, gboolean bIncremental)
{
  WML_ConvexHull2 *self;

#if DEBUG
  g_debug ("----- ENTER WML_new_ConvexHull2");
#endif

  self = g_new (WML_ConvexHull2, 1);

  self->m_iVQuantity = iVQuantity;
  self->m_akVertex = akVertex;

  if (bIncremental)
    WML_ByIncremental (self);
  else
    {
      /* Implementation to be ported when or if I get around it to. */
      /*
         WML_ByDivideAndConquer (self);
       */
      ;
    }

  if (self->m_iHQuantity >= 3)
    WML_RemoveCollinear (self);

#if DEBUG
  g_debug ("----- EXIT WML_new_ConvexHull2");
#endif

  return self;
}



/**
 * Deletes a convex hull from memory.
 *
 * @param self a convex hull.
 */
void
WML_free_ConvexHull2 (WML_ConvexHull2 * self)
{
#if DEBUG
  g_debug ("----- ENTER WML_free_ConvexHull2");
#endif

  if (self == NULL)
    goto end;

  g_free (self->m_aiHIndex);
  g_free (self);

end:
#if DEBUG
  g_debug ("----- EXIT WML_free_ConvexHull2");
#endif

  return;
}



/**
 * Returns the number of points on a convex hull
 *
 * @param self a convex hull.
 * @return the number of points on the convex hull.
 */
int
WML_ConvexHull2_GetQuantity (WML_ConvexHull2 * self)
{
  return self->m_iHQuantity;
}



/**
 * Returns the indices of the points that are on the convex hull.
 *
 * @param self a convex hull.
 * @return a list of point indices.
 */
int *
WML_ConvexHull2_GetIndices (WML_ConvexHull2 * self)
{
  return self->m_aiHIndex;
}



#define F_NONE 0
#define F_LEFT 1
#define F_RIGHT 2
#define F_BOTTOM 3
#define F_TOP 4



/**
 * Compute minimum area oriented box containing the specified points.  The
 * algorithm uses the rotating calipers method.  NOTE.  The input points must
 * form a convex polygon and be in counterclockwise order.
 *
 * @param iQuantity the number of points.
 * @param akPoint the points.
 * @return the minimum-area box.
 */
WML_Box2 *
WML_MinBox (int iQuantity, WML_Vector2 * akPoint)
{
  int iQuantityM1;
  WML_Vector2 *akEdge;
  gboolean *abVisited;
  int i;
  double fXMin, fXMax, fYMin, fYMax;
  int iLIndex, iRIndex, iBIndex, iTIndex;
  WML_Box2 *kBox;
  double fAreaDiv4, fMinAreaDiv4;
  WML_Vector2 kU, kV, kTmp, tmp;
  gboolean bDone;
  int iFlag;
  double fDot, fMaxDot;
  double fExtent0, fExtent1;

  /* The input points are V[0] through V[N-1] and are assumed to be the
   * vertices of a convex polygon that are counterclockwise ordered.  The
   * input points must not contain three consecutive collinear points. */

  /* Unit-length edge directions of convex polygon.  These could be
   * precomputed and passed to this routine if the application requires it. */
  iQuantityM1 = iQuantity - 1;
  akEdge = g_new (WML_Vector2, iQuantity);
  abVisited = g_new (gboolean, iQuantity);

  for (i = 0; i < iQuantityM1; i++)
    {
      WML_Vector2_assign (&akEdge[i], &akPoint[i + 1]);
      WML_Vector2_sub_inplace (&akEdge[i], &akPoint[i]);

      WML_Vector2_Normalize (&akEdge[i]);
      abVisited[i] = FALSE;
    }
  WML_Vector2_assign (&akEdge[iQuantityM1], &akPoint[0]);
  WML_Vector2_sub_inplace (&akEdge[iQuantityM1], &akPoint[iQuantityM1]);

  WML_Vector2_Normalize (&akEdge[iQuantityM1]);
  abVisited[iQuantityM1] = FALSE;

  /* Find the smallest axis-aligned box containing the points.  Keep track
   * of the extremum indices, L (left), R (right), B (bottom), and T (top)
   * so that the following constraints are met:
   *   V[L].X() <= V[i].X() for all i and V[(L+1)%N].X() > V[L].X()
   *   V[R].X() >= V[i].X() for all i and V[(R+1)%N].X() < V[R].X()
   *   V[B].Y() <= V[i].Y() for all i and V[(B+1)%N].Y() > V[B].Y()
   *   V[T].Y() >= V[i].Y() for all i and V[(T+1)%N].Y() < V[R].Y() */

  fXMin = fXMax = akPoint[0].X;
  fYMin = fYMax = akPoint[0].Y;
  iLIndex = iRIndex = iBIndex = iTIndex = 0;
  for (i = 1; i < iQuantity; i++)
    {
      if (akPoint[i].X <= fXMin)
        {
          fXMin = akPoint[i].X;
          iLIndex = i;
        }
      else if (akPoint[i].X >= fXMax)
        {
          fXMax = akPoint[i].X;
          iRIndex = i;
        }

      if (akPoint[i].Y <= fYMin)
        {
          fYMin = akPoint[i].Y;
          iBIndex = i;
        }
      else if (akPoint[i].Y >= fYMax)
        {
          fYMax = akPoint[i].Y;
          iTIndex = i;
        }
    }

  /* wrap-around tests to ensure the constraints mentioned above */
  if (akPoint[0].X <= fXMin)
    {
      fXMin = akPoint[0].X;
      iLIndex = 0;
    }
  else if (akPoint[0].X >= fXMax)
    {
      fXMax = akPoint[0].X;
      iRIndex = 0;
    }

  if (akPoint[0].Y <= fYMin)
    {
      fYMin = akPoint[0].Y;
      iBIndex = 0;
    }
  else if (akPoint[0].Y >= fYMax)
    {
      fYMax = akPoint[0].Y;
      iTIndex = 0;
    }

  /* dimensions of axis-aligned box (extents store width and height for now) */
  kBox = WML_new_Box2 ();
  WML_Box2_Center (kBox)->X = 0.5 * (fXMin + fXMax);
  WML_Box2_Center (kBox)->Y = 0.5 * (fYMin + fYMax);
  WML_Vector2_assign (WML_Box2_Axis (kBox, 0), &UNIT_X);
  WML_Vector2_assign (WML_Box2_Axis (kBox, 1), &UNIT_Y);
  kBox->m_afExtent[0] = 0.5 * (fXMax - fXMin);
  kBox->m_afExtent[1] = 0.5 * (fYMax - fYMin);
  fMinAreaDiv4 = WML_Box2_Extent (kBox, 0) * WML_Box2_Extent (kBox, 1);

  /* rotating calipers algorithm */
  WML_Vector2_assign (&kU, &UNIT_X);
  WML_Vector2_assign (&kV, &UNIT_Y);

  bDone = FALSE;
  while (!bDone)
    {
      /* determine edge that forms smallest angle with current box edges */
      iFlag = F_NONE;
      fMaxDot = 0;

      fDot = WML_Vector2_Dot (&kU, &akEdge[iBIndex]);
      if (fDot > fMaxDot)
        {
          fMaxDot = fDot;
          iFlag = F_BOTTOM;
        }

      fDot = WML_Vector2_Dot (&kV, &akEdge[iRIndex]);
      if (fDot > fMaxDot)
        {
          fMaxDot = fDot;
          iFlag = F_RIGHT;
        }

      WML_Vector2_negate (&kU);
      fDot = WML_Vector2_Dot (&kU, &akEdge[iTIndex]);
      if (fDot > fMaxDot)
        {
          fMaxDot = fDot;
          iFlag = F_TOP;
        }

      WML_Vector2_negate (&kV);
      fDot = WML_Vector2_Dot (&kV, &akEdge[iLIndex]);
      if (fDot > fMaxDot)
        {
          fMaxDot = fDot;
          iFlag = F_LEFT;
        }

      switch (iFlag)
        {
        case F_BOTTOM:
          if (abVisited[iBIndex])
            bDone = TRUE;
          else
            {
              /* compute box axes with E[B] as an edge */
              WML_Vector2_assign (&kU, &akEdge[iBIndex]);
              WML_Vector2_assign (&kU, &kV);
              WML_Vector2_negate (&kV);
              kV = WML_Vector2_Perp (&kV);

              /* mark edge visited and rotate the calipers */
              abVisited[iBIndex] = TRUE;
              if (++iBIndex == iQuantity)
                iBIndex = 0;
            }
          break;
        case F_RIGHT:
          if (abVisited[iRIndex])
            bDone = TRUE;
          else
            {
              /* compute dimensions of box with E[R] as an edge */
              WML_Vector2_assign (&kV, &akEdge[iRIndex]);
              kU = WML_Vector2_Perp (&kV);

              /* mark edge visited and rotate the calipers */
              abVisited[iRIndex] = TRUE;
              if (++iRIndex == iQuantity)
                iRIndex = 0;
            }
          break;
        case F_TOP:
          if (abVisited[iTIndex])
            bDone = TRUE;
          else
            {
              /* compute dimensions of box with E[T] as an edge */
              WML_Vector2_assign (&kU, &akEdge[iTIndex]);
              WML_Vector2_negate (&kU);
              WML_Vector2_assign (&kV, &kU);
              WML_Vector2_negate (&kV);
              kV = WML_Vector2_Perp (&kV);

              /* mark edge visited and rotate the calipers */
              abVisited[iTIndex] = TRUE;
              if (++iTIndex == iQuantity)
                iTIndex = 0;
            }
          break;
        case F_LEFT:
          if (abVisited[iLIndex])
            bDone = TRUE;
          else
            {
              /* compute dimensions of box with E[L] as an edge */
              WML_Vector2_assign (&kV, &akEdge[iLIndex]);
              WML_Vector2_negate (&kV);
              kU = WML_Vector2_Perp (&kV);

              /* mark edge visited and rotate the calipers */
              abVisited[iLIndex] = TRUE;
              if (++iLIndex == iQuantity)
                iLIndex = 0;
            }
          break;
        case F_NONE:
          /* polygon is a rectangle */
          bDone = TRUE;
          break;
        }

      tmp = WML_Vector2_sub (&akPoint[iRIndex], &akPoint[iLIndex]);
      fExtent0 = 0.5 * WML_Vector2_Dot (&kU, &tmp);
      tmp = WML_Vector2_sub (&akPoint[iTIndex], &akPoint[iBIndex]);
      fExtent1 = 0.5 * WML_Vector2_Dot (&kV, &tmp);
      fAreaDiv4 = fExtent0 * fExtent1;
      if (fAreaDiv4 < fMinAreaDiv4)
        {
          fMinAreaDiv4 = fAreaDiv4;
          WML_Vector2_assign (WML_Box2_Axis (kBox, 0), &kU);
          WML_Vector2_assign (WML_Box2_Axis (kBox, 1), &kV);
          kBox->m_afExtent[0] = fExtent0;
          kBox->m_afExtent[1] = fExtent1;

          /* compute box center */
          kTmp = WML_Vector2_add (&akPoint[iTIndex], &akPoint[iBIndex]);
          WML_Vector2_mul_inplace (&kTmp, 0.5);
          WML_Vector2_sub_inplace (&kTmp, &akPoint[iLIndex]);

          WML_Vector2_assign (WML_Box2_Center (kBox), &akPoint[iLIndex]);
          tmp = WML_Vector2_mul (WML_Box2_Axis (kBox, 0), fExtent0);
          WML_Vector2_add_inplace (WML_Box2_Center (kBox), &tmp);
          tmp = WML_Vector2_mul (WML_Box2_Axis (kBox, 1),
                                 WML_Vector2_Dot (WML_Box2_Axis (kBox, 1), &kTmp));
          WML_Vector2_add_inplace (WML_Box2_Center (kBox), &tmp);
        }
    }

  g_free (abVisited);
  g_free (akEdge);
  return kBox;
}



/**
 * The slower method for computing the minimum area oriented box that does not
 * maintain the extremal points supporting the box (like rotating calipers
 * does).  The input points must also form a convex polygon, but the order may
 * be counterclockwise or clockwise.
 *
 * @param iQuantity the number of points.
 * @param akPoint the points.
 * @return the minimum-area box.
 */
WML_Box2 *
WML_MinBoxOrderNSqr (int iQuantity, WML_Vector2 * akPoint)
{
  double fMinAreaDiv4 = 3.40282347e+38F;
  WML_Box2 *kBox;
  int i1, i0;
  WML_Vector2 kU0, kU1;
  double fS0, fS1, fT0, fT1;
  int j;
  WML_Vector2 kDiff;
  double fTest;
  double fExtent0, fExtent1, fAreaDiv4;
  WML_Vector2 tmp;

  kBox = WML_new_Box2 ();
  for (i1 = 0, i0 = iQuantity - 1; i1 < iQuantity; i0 = i1, i1++)
    {
      kU0 = WML_Vector2_sub (&akPoint[i1], &akPoint[i0]);
      WML_Vector2_Normalize (&kU0);

      WML_Vector2_assign (&kU1, &kU0);
      WML_Vector2_negate (&kU1);
      kU1 = WML_Vector2_Perp (&kU1);

      fS0 = 0;
      fT0 = 0;
      fS1 = 0;
      fT1 = 0;
      for (j = 1; j < iQuantity; j++)
        {
          kDiff = WML_Vector2_sub (&akPoint[j], &akPoint[0]);
          fTest = WML_Vector2_Dot (&kU0, &kDiff);
          if (fTest < fS0)
            fS0 = fTest;
          else if (fTest > fS1)
            fS1 = fTest;

          fTest = WML_Vector2_Dot (&kU1, &kDiff);
          if (fTest < fT0)
            fT0 = fTest;
          else if (fTest > fT1)
            fT1 = fTest;
        }

      fExtent0 = 0.5 * (fS1 - fS0);
      fExtent1 = 0.5 * (fT1 - fT0);
      fAreaDiv4 = fExtent0 * fExtent1;
      if (fAreaDiv4 < fMinAreaDiv4)
        {
          fMinAreaDiv4 = fAreaDiv4;
          WML_Vector2_assign (WML_Box2_Axis (kBox, 0), &kU0);
          WML_Vector2_assign (WML_Box2_Axis (kBox, 1), &kU1);
          kBox->m_afExtent[0] = fExtent0;
          kBox->m_afExtent[1] = fExtent1;

          WML_Vector2_assign (WML_Box2_Center (kBox), &akPoint[0]);

          WML_Vector2_assign (&tmp, &kU0);
          WML_Vector2_mul_inplace (&tmp, 0.5 * (fS0 + fS1));
          WML_Vector2_add_inplace (WML_Box2_Center (kBox), &tmp);

          WML_Vector2_assign (&tmp, &kU1);
          WML_Vector2_mul_inplace (&tmp, 0.5 * (fT0 + fT1));
          WML_Vector2_add_inplace (WML_Box2_Center (kBox), &tmp);
        }
    }

  return kBox;
}

/* end of file wml.c */
