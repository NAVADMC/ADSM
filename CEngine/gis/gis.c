/** @file gis.c
 * Functions for geographical calculations.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date May 2003
 *
 * Copyright &copy; University of Guelph, 2003-2008
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#if HAVE_CONFIG_H
#  include <config.h>
#endif

#include <gis.h>

#if HAVE_MATH_H
#  include <math.h>
#endif

#include <gsl/gsl_math.h>
#include <gsl/gsl_sf_trig.h>

#if STDC_HEADERS
#  include <stdlib.h>
#endif

#define EPSILON 0.00001
#define RAD2DEG 57.2957795
#define d_acos(x) (fabs (x) >= 1.0 ? ((x) < 0.0 ? M_PI : 0.0) : acos (x))



/**
 * Returns the great-circle distance in km between points 1 and 2.  Latitudes
 * and longitudes must be given in degrees.  Latitudes must be between -90 (at
 * the south pole) and +90 (at the north pole), inclusive.  Longitudes must be
 * between -180 (west is negative) and +180 (east is positive), inclusive.
 * Taken from the Generic Mapping Tools (GMT) 3.4.2 by P. Wessel and W.H.F.
 * Smith.
 *
 * @param lat1 latitude of point 1, in degrees.  -90 &le; <i>lat1</i> &le; 90.
 * @param lon1 longitude of point 1, in degrees.  -180 &le; <i>lon1</i> &le; 180.
 * @param lat2 latitude of point 2, in degrees.  -90 &le; <i>lat2</i> &le; 90.
 * @param lon2 longitude of point 2, in degrees.  -180 &le; <i>lon2</i> &le; 180.
 * @return the distance (in km) between points 1 and 2.
 */
double
GIS_great_circle_distance (double lat1, double lon1, double lat2, double lon2)
{
  double C, a, b, c;
  double cosC, cosa, cosb, cosc;
  double sina, sinb;

  if ((lat1 == lat2) && (lon1 == lon2))
    return 0.0;

  a = DEG_TO_RAD * (90.0 - lat2);
  b = DEG_TO_RAD * (90.0 - lat1);

  C = DEG_TO_RAD * (lon2 - lon1);

  sina = sin (a);
  cosa = cos (a);
  sinb = sin (b);
  cosb = cos (b);
  cosC = cos (C);

  cosc = cosa * cosb + sina * sinb * cosC;
  if (cosc < -1.0)
    c = M_PI;
  else if (cosc > 1)
    c = 0.0;
  else
    c = d_acos (cosc);

  return (c * GIS_EARTH_RADIUS);
}



/**
 * Returns the distance in km between points 1 and 2 on a kilometer grid.
 *
 * @param x1 x-coordinate of point 1.
 * @param y1 y-coordinate of point 1.
 * @param x2 x-coordinate of point 2.
 * @param y2 y-coordinate of point 2.
 * @return the distance (in km) between points 1 and 2.
 */
double
GIS_distance (double x1, double y1, double x2, double y2)
{
  double dx, dy;

  dx = x2 - x1;
  dy = y2 - y1;

  return sqrt (dx * dx + dy * dy);
}



/**
 * Returns the square of the distance in km between points 1 and 2 on a
 * kilometer grid.
 *
 * This function may be useful if you want to compare computed distances to a
 * fixed threshold.  By comparing this function's output to the square of the
 * threshold instead, you can avoid taking square roots.
 *
 * @param x1 x-coordinate of point 1.
 * @param y1 y-coordinate of point 1.
 * @param x2 x-coordinate of point 2.
 * @param y2 y-coordinate of point 2.
 * @return the distance (in km) between points 1 and 2.
 */
double
GIS_distance_sq (double x1, double y1, double x2, double y2)
{
  double dx, dy;

  dx = x2 - x1;
  dy = y2 - y1;

  return (dx * dx + dy * dy);
}



/**
 * Returns the initial heading in degrees from point 1 to point 2.  Latitudes
 * and longitudes must be given in degrees.  Latitudes must be between -90 (at
 * the south pole) and +90 (at the north pole), inclusive.  Longitudes must be
 * between -180 (west is negative) and +180 (east is positive), inclusive.
 * Taken from the Generic Mapping Tools (GMT) 3.4.2 by P. Wessel and W.H.F.
 * Smith.
 *
 * @param lat1 latitude of point 1, in degrees.  -90 &le; <i>lat1</i> &le; 90.
 * @param lon1 longitude of point 1, in degrees.  -180 &le; <i>lon1</i> &le; 180.
 * @param lat2 latitude of point 2, in degrees.  -90 &le; <i>lat2</i> &le; 90.
 * @param lon2 longitude of point 2, in degrees.  -180 &le; <i>lon2</i> &le; 180.
 * @return the initial heading (in degrees) from point 1 to point 2.
 */
double
GIS_great_circle_heading (double lat1, double lon1, double lat2, double lon2)
{
  double C, a, b, c;
  double cosC, cosa, cosb, cosc;
  double sina, sinb;

  if ((lat1 == lat2) && (lon1 == lon2))
    return 0.0;

  a = DEG_TO_RAD * (90.0 - lat2);
  b = DEG_TO_RAD * (90.0 - lat1);

  C = DEG_TO_RAD * (lon2 - lon1);

  sina = sin (a);
  cosa = cos (a);
  sinb = sin (b);
  cosb = cos (b);
  cosC = cos (C);

  cosc = cosa * cosb + sina * sinb * cosC;
  if (cosc < -1.0)
    c = M_PI;
  else if (cosc > 1)
    c = 0.0;
  else
    c = d_acos (cosc);

  return (c * GIS_EARTH_RADIUS);
}



/**
 * Returns the initial heading in degrees from point 1 to point 2.
 *
 * @param x1 x-coordinate of point 1.
 * @param y1 y-coordinate of point 1.
 * @param x2 x-coordinate of point 2.
 * @param y2 y-coordinate of point 2.
 * @return the initial heading (in degrees) from point 1 to point 2.
 */
double
GIS_heading (double x1, double y1, double x2, double y2)
{
  double dx, dy;
  double heading;

  dx = x2 - x1;
  dy = y2 - y1;

  /* Flip the order of atan2's arguments to rotate the coordinate system from
   * 0 = E, + = counter-clockwise (the trig way) to 0 = N, + = clockwise (the
   * navigation/surveying way). */
  heading = atan2 (dx, dy) * RAD2DEG;

  /* atan2's return values are in the range -pi to pi; make sure this function
   * returns values in [0,360). */
  if (heading < 0)
    heading += 360;

  return heading;
}



/**
 * Tells whether the given point is inside the given polygon contour.
 * Following the terminology used in the General Polygon Clipper library, a
 * "polygon" may consist of more than one separated "contour".  This function
 * has not been tested on self-intersecting contours.
 *
 * This function is copyright 1970-2003 Wm. Randolph Franklin.  A page with
 * information about this function can be found at
 *
 * http://www.ecse.rpi.edu/Homepages/wrf/Research/Short_Notes/pnpoly.html
 *
 * From the page:
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to
 * deal in the Software without restriction, including without limitation the
 * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
 * sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimers.
 * 2. Redistributions in binary form must reproduce the above copyright notice
 *    in the documentation and/or other materials provided with the
 *    distribution.
 * 3. The name of Wm. Randolph Franklin may not be used to endorse or promote
 *    products derived from this Software without specific prior written
 *    permission.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
 * IN THE SOFTWARE. 
 *
 * This function has been modified to accept the polygon in the format used by
 * the General Polygon Clipper library.
 *
 * @param poly the polygon contour.
 * @param x the x-coordinate of the point.
 * @param y the y-coordinate of the point.
 * @return TRUE if the point is inside the contour, FALSE otherwise.
 */
gboolean
GIS_point_in_contour (gpc_vertex_list * poly, float x, float y)
{
  int npol;
  int i, j;
  gboolean c = FALSE;
  gpc_vertex *v;

  npol = poly->num_vertices;
  v = poly->vertex;
  c = FALSE;
  for (i = 0, j = npol - 1; i < npol; j = i++)
    {
      if ((((v[i].y <= y) && (y < v[j].y)) ||
           ((v[j].y <= y) && (y < v[i].y))) &&
          (x < (v[j].x - v[i].x) * (y - v[i].y) / (v[j].y - v[i].y) + v[i].x))

        c = !c;
    }

  return c;
}



/**
 * Tells whether the given point is inside the given polygon.  Following the
 * terminology used in the General Polygon Clipper library, a "polygon" may
 * consist of more than one separated "contour".  This function has not been
 * tested on self-intersecting contours or polygons with holes.
 *
 * @param poly the polygon.
 * @param x the x-coordinate of the point.
 * @param y the y-coordinate of the point.
 * @return TRUE if the point is inside the polygon, FALSE otherwise.
 */
gboolean
GIS_point_in_polygon (gpc_polygon * poly, float x, float y)
{
  int i;
  gboolean c = FALSE;

  for (i = 0; i < poly->num_contours; i++)
    if ((c = GIS_point_in_contour (&(poly->contour[i]), x, y)))
      break;

  return c;
}



/**
 * Returns the area of a polygon.  The x- and y-coordinates are assumed to be
 * on a square grid, so this function isn't directly usable for lat-lon points.
 *
 * @param poly a polygon.
 * @return the area of the polygon.
 */
double
GIS_polygon_area (gpc_polygon * poly)
{
  double poly_area, contour_area;
  int n, i, j;
  gpc_vertex_list *contour;
  gpc_vertex *v;

  poly_area = 0;

  if (poly == NULL)
    goto end;

  /* Add the areas of each sub-polygon or "contour" */
  for (i = 0; i < poly->num_contours; i++)
    {
      contour = &(poly->contour[i]);
      n = contour->num_vertices;
      /* Zero vertices (empty contour), one vertex (single point), or two
       * vertices (line) count for zero area.  The contour must be at least a
       * triangle before we bother to calculate the area. */
      if (n < 3)
        continue;

      contour_area = 0;
      v = contour->vertex;

      for (j = 0; j < n - 1; j++)
        {
          contour_area += (v[j].x * v[j + 1].y - v[j + 1].x * v[j].y);
        }
      /* final point */
      contour_area += (v[j].x * v[0].y - v[0].x * v[j].y);

      poly_area += fabs (0.5 * contour_area);
    }

end:
  return poly_area;
}



/**
 * Returns the perimeter of a polygon.  The x- and y-coordinates are assumed to
 * be on a square grid, so this function isn't directly usable for lat-lon
 * points.
 *
 * @param poly a polygon.
 * @return the perimeter of the polygon.
 */
double
GIS_polygon_perimeter (gpc_polygon * poly)
{
  double poly_perimeter, contour_perimeter;
  int n, i, j;
  gpc_vertex_list *contour;
  gpc_vertex *v;
  double dx, dy;

  poly_perimeter = 0;

  if (poly == NULL)
    goto end;

  /* Add the perimeters of each sub-polygon or "contour" */
  for (i = 0; i < poly->num_contours; i++)
    {
      contour = &(poly->contour[i]);
      n = contour->num_vertices;
      /* Zero vertices (empty contour), one vertex (single point), or two
       * vertices (line) count for zero perimeter.  The contour must be at
       * least a triangle before we bother to calculate the perimeter. */
      if (n < 3)
        continue;

      contour_perimeter = 0;
      v = contour->vertex;

      for (j = 0; j < n - 1; j++)
        {
          dx = v[j+1].x - v[j].x;
          dy = v[j+1].y - v[j].y;
          contour_perimeter += sqrt (dx*dx + dy*dy);
        }
      /* final point */
      dx = v[0].x - v[j].x;
      dy = v[0].y - v[j].y;
      contour_perimeter += sqrt (dx*dx + dy*dy);

      poly_perimeter += contour_perimeter;
    }

end:
  return poly_perimeter;
}



/**
 * Creates a new, initialized GPC polygon.
 *
 * @return a polygon with no contours.
 */
gpc_polygon *
gpc_new_polygon (void)
{
  gpc_polygon *poly;

  poly = (gpc_polygon *) malloc (sizeof(gpc_polygon));
  g_assert (poly != NULL);
  poly->num_contours = 0;
  poly->hole = NULL;
  poly->contour = NULL;
  return poly;
}

/* end of file gis.c */
