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
#include "memoization.h"



/**
 * The data used internally in a spatial search object.  It is defined here to
 * hide the implementation details.
 */
typedef struct
{
  GArray *x; /* For gathering up locations prior to prepare() */
  GArray *y; /* For gathering up locations priot to prepare() */
  MemoizationTable *memo;
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

  /* Add to the lists that will be used to initialize the memoization table. */
  g_array_append_val (private_data->x, x);
  g_array_append_val (private_data->y, y);

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
    g_debug ("----- ENTER prepare (memoization table)");
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

  /* Initialize the memoization table. */
  private_data->memo =
    initMemoization ((double *)(private_data->x->data),
                     (double *)(private_data->y->data),
                     searcher->npoints);
  g_array_free (private_data->x, /* free_segment = */ TRUE);
  private_data->x = NULL;
  g_array_free (private_data->y, /* free_segment = */ TRUE);
  private_data->y = NULL;

  #if DEBUG
    g_debug ("----- EXIT prepare (memoization table)");
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
    g_debug ("----- ENTER search_circle_by_xy (memoization table, x=%g, y=%g, radius=%g)", x, y, radius);
  #endif

  private_data = (private_data_t *)(searcher->private_data);

  /* Pass request to underlying search method. */
  spatial_search_circle_by_xy (private_data->underlying_search,
                               x, y, radius,
                               user_function, user_data);

  #if DEBUG
    g_debug ("----- EXIT search_circle_by_xy (memoization table)");
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
    g_debug ("----- ENTER search_circle_by_id (memoization table, id=%i, radius=%g)", id, radius);
  #endif

  private_data = (private_data_t *)(searcher->private_data);

  /* This is a case the memoization table handles. */
  searchWithMemoization (private_data->memo,
                         private_data->underlying_search,
                         id, radius,
			             user_function, user_data);

  #if DEBUG
    g_debug ("----- EXIT search_circle_by_id (memoization table)");
  #endif

  return;
}



/**
 * Searches for points closest to a give distance from a particular point.  The
 * callback function provided as an argument will be called with the id's of
 * points found.
 *
 * @param searcher the spatial search object.
 * @param id the id of the point.
 * @param desired_distance the desired distance from the point.
 * @param user_function the function to be called with the id's of points found.
 * @param user_data any data to be passed to user_function.  Can be NULL.
 */
static void
search_closest_to_distance_by_id (spatial_search_t * searcher,
                                  int id, double desired_distance,
                                  spatial_search_hit_callback user_function,
                                  gpointer user_data)
{
  private_data_t *private_data;

  #if DEBUG
    g_debug ("----- ENTER search_closest_to_distance_by_id (memoization table, id=%i, desired_distance=%g)",
             id, desired_distance);
  #endif

  private_data = (private_data_t *)(searcher->private_data);

  /* This is a case the memoization table handles. */
  searchClosestToDistanceWithMemoization (private_data->memo,
                                          private_data->underlying_search,
                                          id, desired_distance,
                                          user_function, user_data);

  #if DEBUG
    g_debug ("----- EXIT search_closest_to_distance_by_id (memoization table)");
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
    g_debug ("----- ENTER search_rectangle (memoization table)");
  #endif

  private_data = (private_data_t *)(searcher->private_data);

  /* Pass request to underlying search method. */
  spatial_search_rectangle (private_data->underlying_search,
                            x1, y1, x2, y2,
                            user_function, user_data);

  #if DEBUG
    g_debug ("----- EXIT search_rectangle (memoization table)");
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
    g_debug ("----- ENTER free_searcher (memoization table)");
  #endif

  if (searcher != NULL)
  {
    private_data = (private_data_t *)(searcher->private_data);
    deleteMemoization (private_data->memo);
    free_spatial_search (private_data->underlying_search);
    g_free (private_data);
    g_free (searcher);
  }

  #if DEBUG
    g_debug ("----- EXIT free_searcher (memoization table)");
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
  private_data->x = g_array_new (FALSE, FALSE, sizeof(double));
  private_data->y = g_array_new (FALSE, FALSE, sizeof(double));
  /* The memoization table is null until the call to prepare(). */
  private_data->memo = NULL;
  private_data->underlying_search = underlying_search;
  searcher->private_data = (gpointer) private_data;
  
  /* Function pointers */
  searcher->add_point = add_point;
  searcher->prepare = prepare;
  searcher->search_circle_by_xy = search_circle_by_xy;
  searcher->search_circle_by_id = search_circle_by_id;
  searcher->search_closest_to_distance_by_id = search_closest_to_distance_by_id;
  searcher->search_rectangle = search_rectangle;
  searcher->free = free_searcher;
  
  #if DEBUG
    g_debug ("----- EXIT new_spatial_search_with_memoization");
  #endif

  return searcher;
}

/* end of file spatial_search_memo.c */
