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



/** Forward declaration for the spatial search object type. */
struct spatial_search_t_;



/** Type of a function that adds a point to a spatial search object. */
typedef void (*spatial_search_add_point_t) (struct spatial_search_t_ *, double x, double y);

/**
 * Type of a function that is called between adding points and actually using
 * a spatial search object.
 */
typedef void (*spatial_search_prepare_t) (struct spatial_search_t_ *);

/** Type of a callback function sent to the search routines. */
typedef void (*spatial_search_hit_callback) (int id, gpointer user_data);

/**
 * Type of a function that searches a circle with its center specified by
 * an x,y coordinate.
 */
typedef void (*spatial_search_circle_by_xy_t) (struct spatial_search_t_ *,
                                               double x, double y, double radius,
                                               spatial_search_hit_callback,
                                               gpointer user_data);

/**
 * Type of a function that searches a circle with its center specified by a
 * point ID.
 */
typedef void (*spatial_search_circle_by_id_t) (struct spatial_search_t_ *,
                                               int id, double radius,
                                               spatial_search_hit_callback,
                                               gpointer user_data);

/** Type of a function that searches a rectangle. */
typedef void (*spatial_search_rectangle_t) (struct spatial_search_t_ *,
                                            double x1, double y1,
                                            double x2, double y2,
                                            spatial_search_hit_callback,
                                            gpointer user_data);

/** Type of a function that frees a spatial search object. */
typedef void (*spatial_search_free_t) (struct spatial_search_t_ *);



/** A spatial search object. */
typedef struct spatial_search_t_
{
  int npoints;
  double min_x, max_x, min_y, max_y;
  /* Function pointers */
  spatial_search_add_point_t add_point;
  spatial_search_prepare_t prepare;
  spatial_search_circle_by_xy_t search_circle_by_xy;
  spatial_search_circle_by_id_t search_circle_by_id;
  spatial_search_rectangle_t search_rectangle;
  spatial_search_free_t free;
  /* Private object data - data fields specific to each subclass */
  gpointer private_data;
}
spatial_search_t;



/* More convenient syntax for calling member functions. */
#define spatial_search_add_point(S,X,Y) (S->add_point(S,X,Y))
#define spatial_search_prepare(S) (S->prepare(S))
#define spatial_search_circle_by_xy(S,X,Y,R,CB,UD) (S->search_circle_by_xy(S,X,Y,R,CB,UD))
#define spatial_search_circle_by_id(S,I,R,CB,UD) (S->search_circle_by_id(S,I,R,CB,UD))
#define spatial_search_rectangle(S,X1,Y1,X2,Y2,CB,UD) (S->search_rectangle(S,X1,Y1,X2,Y2,CB,UD))
#define free_spatial_search(S) (S->free(S))

#endif /* !SPATIAL_SEARCH_H */
