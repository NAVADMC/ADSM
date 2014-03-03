/** @file gis.h
 * Interface for gis.c.
 *
 * Symbols from this module begin with GIS_.
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

#ifndef GIS_H
#define GIS_H

/*  These symbols make it possible to use functions defined in this file
*   in a Windows DLL.  If DLL_EXPORTS and DLL_IMPORTS are undefined
*   (e.g. in typical *nix builds), the symbol DLL_API is ignored.  In Windows
*   builds, defining DLL_EXPORTS will make these functions available in a DLL.
*   If DLL_IMPORTS is defined, a C program may use the functions from the DLL.
*/
#if defined(DLL_EXPORTS)
#	define DLL_API __declspec( dllexport )
#elif defined(DLL_IMPORTS)
# define DLL_API __declspec( dllimport )
#else
# define DLL_API
#endif

#include <gpcl/gpc.h>
#include <glib.h>
#include <proj_api.h>

#define GIS_EARTH_RADIUS 6378.137 /**< equatorial radius in km, WGS84 */



/* Prototypes. */
DLL_API double GIS_great_circle_distance (double lat1, double lon1, double lat2, double lon2);
DLL_API double GIS_distance (double x1, double y1, double x2, double y2);
DLL_API double GIS_distance_sq (double x1, double y1, double x2, double y2);

double GIS_great_circle_heading (double lat1, double lon1, double lat2, double lon2);
double GIS_heading (double x1, double y1, double x2, double y2);

gboolean GIS_point_in_polygon (gpc_polygon * poly, float x, float y);
gboolean GIS_point_in_contour (gpc_vertex_list * poly, float x, float y);
double GIS_polygon_area (gpc_polygon * poly);
double GIS_polygon_perimeter (gpc_polygon * poly);

/* Helper functions for working with GPC polygons. */
gpc_polygon *gpc_new_polygon (void);

#endif /* !GIS_H */
