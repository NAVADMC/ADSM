/** @file spatial_search.h
 * An object to encapsulate a spatial search algorithm.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 *
 * Copyright &copy; University of Guelph, 2010
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */
#ifndef SPATIAL_SEARCH_H
#define SPATIAL_SEARCH_H

#include <glib.h>



/** A spatial search object. */
typedef struct
{
  int npoints;
  double min_x, max_x, min_y, max_y;
  gpointer private_data;
}
spatial_search_t;



/**
 * Type of a callback function sent to the spatial search routine.
 */
typedef void (*spatial_search_hit_callback)(int id, gpointer user_data);



/* Prototypes. */
spatial_search_t *new_spatial_search (void);
void spatial_search_add_point (spatial_search_t *, double x, double y);
void spatial_search_prepare (spatial_search_t *);
void spatial_search_circle_by_xy (spatial_search_t *,
                                  double x, double y, double radius,
                                  spatial_search_hit_callback, gpointer user_data);
void spatial_search_circle_by_id (spatial_search_t *,
                                  int id, double radius,
                                  spatial_search_hit_callback, gpointer user_data);
void spatial_search_rectangle (spatial_search_t *,
                               double x1, double y1, double x2, double y2,
                               spatial_search_hit_callback, gpointer user_data);
void free_spatial_search (spatial_search_t *);

#endif /* !SPATIAL_SEARCH_H */
