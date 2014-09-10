/** @file spatial_search_memo.c
 * Functions for finding objects in a spatial arrangement.
 *
 * The current implementation uses the R-tree data structure developed by A.
 * Guttman.  The purpose of wrapping the R-tree in another data structure (the
 * spatial search object) is to make it easier to replace or augment the R-tree
 * with other data structures and algorithms.
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#if HAVE_CONFIG_H
#  include <config.h>
#endif

#include "spatial_search.h"



/**
 * The data used internally in a spatial search object.  It is defined here to
 * hide the implementation details.
 */
typedef struct
{
  spatial_search_t *underlying_search;
}
private_data_t;



/**
 * Adds a new point location.
 *
 * Side effects: may modify the values of min_x, max_x, min_y, and max_y
 * inside the spatial search object.
 *
 * @param searcher the spatial search object.
 * @param x the x-coordinate.
 * @param y the y-coordinate.
 */
static void
add_point (spatial_search_t *searcher, double x, double y)
{
  private_data_t *private_data;

  private_data = (private_data_t *)(searcher->private_data);

  /* Also pass along to the underlying search method. */
  spatial_search_add_point (private_data->underlying_search, x, y);

  return;
}



/**
 * Prepares the spatial search object for use, after all the points have been
 * added.
 *
 * @param searcher the spatial search object.
 */
static void
prepare (spatial_search_t *searcher)
{
  private_data_t *private_data;
  spatial_search_t *underlying_search;

  #if DEBUG
    g_debug ("----- ENTER prepare");
  #endif

  private_data = (private_data_t *)(searcher->private_data);

  /* Prepare the underlying search object. */
  underlying_search = private_data->underlying_search;
  spatial_search_prepare (underlying_search);

  /* Copy some metadata from the underlying search method. */
  searcher->npoints = underlying_search->npoints;
  searcher->min_x = underlying_search->min_x;
  searcher->min_y = underlying_search->min_y;
  searcher->max_x = underlying_search->max_x;
  searcher->max_y = underlying_search->max_y;

  #if DEBUG
    g_debug ("----- EXIT prepare");
  #endif

  return;
}



/**
 * Searches for points within the given circle.  The callback function provided
 * as an argument will be called with the id's of points in the circle.
 *
 * @param searcher the spatial search object.
 * @param x the x-coordinate of the center of the circle.
 * @param y the y-coordinate of the center of the circle.
 * @param radius the radius of the circle.
 * @param user_function the function to be called with the id's of points in
 *   the circle.
 * @param user_data any data to be passed to user_function.  Can be NULL.
 */
static void
search_circle_by_xy (spatial_search_t * searcher,
                     double x, double y, double radius,
                     spatial_search_hit_callback user_function,
                     gpointer user_data)
{
  private_data_t *private_data;

  #if DEBUG
    g_debug ("----- ENTER search_circle_by_xy (x=%g, y=%g, radius=%g)", x, y, radius);
  #endif

  private_data = (private_data_t *)(searcher->private_data);

  /* Pass request to underlying search method. */
  spatial_search_circle_by_xy (private_data->underlying_search,
                               x, y, radius,
                               user_function, user_data);

  #if DEBUG
    g_debug ("----- EXIT search_circle_by_xy");
  #endif

  return;
}



/**
 * Searches for points within a circle around a particular point.  The callback
 * function provided as an argument will be called with the id's of points in
 * the circle.
 *
 * @param searcher the spatial search object.
 * @param id the id of the point at the center of the circle.
 * @param radius the radius of the circle.
 * @param user_function the function to be called with the id's of points in
 *   the circle.
 * @param user_data any data to be passed to user_function.  Can be NULL.
 */
static void
search_circle_by_id (spatial_search_t * searcher,
                     int id, double radius,
                     spatial_search_hit_callback user_function,
                     gpointer user_data)
{
  private_data_t *private_data;

  #if DEBUG
    g_debug ("----- ENTER search_circle_by_id (id=%i, radius=%g)", id, radius);
  #endif

  private_data = (private_data_t *)(searcher->private_data);

  /* Pass request to underlying search method. */
  spatial_search_circle_by_id (private_data->underlying_search,
                               id, radius,
                               user_function, user_data);

  #if DEBUG
    g_debug ("----- EXIT search_circle_by_id");
  #endif

  return;
}



/**
 * Searches for points within the given rectangle.  The callback function provided
 * as an argument will be called with the id's of points in the rectangle.
 *
 * @param searcher the spatial search object.
 * @param x1 the x-coordinate of one corner of the rectangle.
 * @param y1 the y-coordinate of one corner of the rectangle.
 * @param x2 the x-coordinate of the opposite corner of the rectangle.
 * @param y2 the y-coordinate of the opposite corner of the rectangle.
 * @param user_function the function to be called with the id's of points in
 *   the rectangle.
 * @param user_data any data to be passed to user_function.  Can be NULL.
 */
static void
search_rectangle (spatial_search_t * searcher,
                  double x1, double y1, double x2, double y2,
                  spatial_search_hit_callback user_function,
                  gpointer user_data)
{
  private_data_t *private_data;

  #if DEBUG
    g_debug ("----- ENTER search_rectangle");
  #endif

  private_data = (private_data_t *)(searcher->private_data);

  /* Pass request to underlying search method. */
  spatial_search_rectangle (private_data->underlying_search,
                            x1, y1, x2, y2,
                            user_function, user_data);

  #if DEBUG
    g_debug ("----- EXIT search_rectangle");
  #endif

  return;
}



/**
 * Deletes this spatial search object from memory.  Also frees the underlying
 * search method object that was passed in as an argument to
 * new_spatial_search_with_memoization().
 *
 * @param searcher a spatial search object.
 */
static void
free_searcher (spatial_search_t *searcher)
{
  private_data_t *private_data;

  #if DEBUG
    g_debug ("----- ENTER free_searcher");
  #endif

  if (searcher != NULL)
  {
    private_data = (private_data_t *)(searcher->private_data);
    free_spatial_search (private_data->underlying_search);
    g_free (private_data);
    g_free (searcher);
  }

  #if DEBUG
    g_debug ("----- EXIT free_searcher");
  #endif

  return;
}



/**
 * Creates a new spatial search object.
 *
 * @param y the single y-value.
 * @return a pointer to a newly-created REL_chart_t structure.
 */
spatial_search_t *
new_spatial_search_with_memoization (spatial_search_t *underlying_search)
{
  spatial_search_t *searcher;
  private_data_t *private_data;

  #if DEBUG
    g_debug ("----- ENTER new_spatial_search_with_memoization");
  #endif

  searcher = g_new (spatial_search_t, 1);
  searcher->npoints = 0;
  /* min_x, max_x, min_y, and max_y are undefined until the first point is
   * added. */
  private_data = g_new (private_data_t, 1);
  private_data->underlying_search = underlying_search;
  searcher->private_data = (gpointer) private_data;
  
  /* Function pointers */
  searcher->add_point = add_point;
  searcher->prepare = prepare;
  searcher->search_circle_by_xy = search_circle_by_xy;
  searcher->search_circle_by_id = search_circle_by_id;
  searcher->search_rectangle = search_rectangle;
  searcher->free = free_searcher;
  
  #if DEBUG
    g_debug ("----- EXIT new_spatial_search_with_memoization");
  #endif

  return searcher;
}

/* end of file spatial_search_memo.c */
