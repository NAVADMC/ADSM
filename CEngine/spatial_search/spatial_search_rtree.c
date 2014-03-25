/** @file spatial_search_rtree.c
 * Functions for finding objects in a spatial arrangement.
 *
 * The current implementation uses the R-tree data structure developed by A.
 * Guttman.  The purpose of wrapping the R-tree in another data structure (the
 * spatial search object) is to make it easier to replace the R-tree with
 * newer, better data structures and algorithms.
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

#if HAVE_CONFIG_H
#  include <config.h>
#endif

#if HAVE_MATH_H
#  include <math.h>
#endif

#include "spatial_search.h"
#include <rTreeIndex.h>
#include "ch2d.h"
#include "wml.h"
#include <gsl/gsl_math.h>



#define EPSILON 0.001



/**
 * The data used internally in a spatial search object.  It is defined here to
 * hide the implementation details.
 */
typedef struct
{
  struct Node *rtree;
  double rtree_threshold;
  GArray *xy;
  double bounding_box[8]; /**< a rectangle around the herds, as
    x1,y1,x2,y2,.... */
  double xaxis_length, yaxis_length; /**< the length in km of the sides of the
    minimum-area oriented rectangle. */
  double short_axis_length; /**< xaxis_length or yaxis_length, whichever is
    less. */
}
private_data_t;



/**
 * Returns the distance between two points.
 *
 * @param x1 the x-coordinate of point 1.
 * @param y1 the y-coordinate of point 1.
 * @param x2 the x-coordinate of point 2.
 * @param y2 the y-coordinate of point 2.
 * @return the distance between point 1 and point 2.
 */
double
distance (double x1, double y1, double x2, double y2)
{
  double dx, dy;

  dx = x2 - x1;
  dy = y2 - y1;

  return sqrt (dx * dx + dy * dy);
}



/**
 * Returns the square of the distance between two points.
 *
 * @param x1 the x-coordinate of point 1.
 * @param y1 the y-coordinate of point 1.
 * @param x2 the x-coordinate of point 2.
 * @param y2 the y-coordinate of point 2.
 * @return the square of the distance between point 1 and point 2.
 */
double
distance_sq (double x1, double y1, double x2, double y2)
{
  double dx, dy;

  dx = x2 - x1;
  dy = y2 - y1;

  return dx * dx + dy * dy;
}



/**
 * Creates a new spatial search object.
 *
 * @return a pointer to a newly-created spatial_search_t structure.
 */
spatial_search_t *
new_spatial_search (void)
{
  spatial_search_t *searcher;
  private_data_t *private_data;

#if DEBUG
  g_debug ("----- ENTER new_spatial_search");
#endif

  searcher = g_new (spatial_search_t, 1);
  searcher->npoints = 0;
  /* min_x, max_x, min_y, and max_y are undefined until the first point is
   * added. */
  private_data = g_new (private_data_t, 1);
  private_data->rtree = RTreeNewIndex ();
  private_data->xy = g_array_new (FALSE, FALSE, sizeof(double));
  searcher->private_data = (gpointer) private_data;

#if DEBUG
  g_debug ("----- EXIT new_spatial_search");
#endif

  return searcher;
}



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
void
spatial_search_add_point (spatial_search_t *searcher, double x, double y)
{
  private_data_t *private_data;
  struct Rect rect;

  private_data = (private_data_t *)(searcher->private_data);
  rect.boundary[0] = x;
  rect.boundary[1] = y;
  rect.boundary[2] = x;
  rect.boundary[3] = y;
  searcher->npoints++;
  RTreeInsertRect (&rect, searcher->npoints, &(private_data->rtree), 0);
  g_array_append_val (private_data->xy, x);
  g_array_append_val (private_data->xy, y);
  if (searcher->npoints == 1)
    {
      /* This is the very first point. */
      searcher->min_x = searcher->max_x = x;
      searcher->min_y = searcher->max_y = y;
    }
  else
    {
      if (x < searcher->min_x)
        searcher->min_x = x;
      else if (x > searcher->max_x)
        searcher->max_x = x;
      if (y < searcher->min_y)
        searcher->min_y = y;
      else if (y > searcher->max_y)
        searcher->max_y = y;
    }

  return;
}



/**
 * Calculates a minimum-area oriented rectangle bounding the points.  After
 * this function is called, the bounding_box field of the spatial_search_t
 * structure will be filled in.  The 8 doubles in the bounding_box array are
 * x,y pairs in counter-clockwise.
 *
 * @param searcher the spatial search object.
 */
void
find_oriented_bounding_box (spatial_search_t *searcher)
{
  private_data_t *private_data;
  unsigned int npoints;
  double x, y;
  gboolean all_x_same, all_y_same;
  double **hull;
  unsigned int hull_npoints = 0;
  WML_Vector2 *hull2 = NULL;
  WML_Box2 *minbox = NULL;
  WML_Vector2 corner[4];
  unsigned int i;               /* loop counter */
#if DEBUG
  GString *s;
#endif

#if DEBUG
  g_debug ("----- ENTER find_oriented_bounding_box");
#endif

  private_data = (private_data_t *)(searcher->private_data);

  npoints = searcher->npoints;
  if (npoints == 0)
    goto end;

  /* Deal with 2 special cases first. */
  if (npoints == 1)
    {
#if DEBUG
      g_debug ("only 1 point: bounding box is a point");
#endif
      x = g_array_index (private_data->xy, double, 0);
      y = g_array_index (private_data->xy, double, 1);
      for (i = 0; i < 4; i++)
        {
          private_data->bounding_box[2 * i] = x;
          private_data->bounding_box[2 * i + 1] = y;
        }
      goto end;
    }

  if (npoints == 2)
    {
#if DEBUG
      g_debug ("only 2 points: bounding box is a line");
#endif
      x = g_array_index (private_data->xy, double, 0);
      y = g_array_index (private_data->xy, double, 1);
      for (i = 0; i < 2; i++)
        {
          private_data->bounding_box[2 * i] = x;
          private_data->bounding_box[2 * i + 1] = y;
        }
      x = g_array_index (private_data->xy, double, 2);
      y = g_array_index (private_data->xy, double, 3);
      for (i = 2; i < 4; i++)
        {
          private_data->bounding_box[2 * i] = x;
          private_data->bounding_box[2 * i + 1] = y;
        }
      goto end;
    }

  /* If the points are all at the same location, or they are all in a
   * horizontal or vertical line, we can avoid calling the convex hull
   * algorithm. */
  all_x_same = (gsl_fcmp (searcher->min_x, searcher->max_x, EPSILON) == 0);
  all_y_same = (gsl_fcmp (searcher->min_y, searcher->max_y, EPSILON) == 0);
  if (all_x_same && all_y_same)
    {
#if DEBUG
      g_debug ("all %u points have the same location: bounding box is a point", npoints);
#endif
      x = searcher->min_x;
      y = searcher->min_y;
      for (i = 0; i < 4; i++)
        {
          private_data->bounding_box[2 * i] = x;
          private_data->bounding_box[2 * i + 1] = y;
        }
      goto end;
    }
  else if (all_x_same)
    {
#if DEBUG
      g_debug ("all %u points have the same x-location: bounding box is a line", npoints);
#endif
      x = searcher->min_x;
      y = searcher->min_y;
      for (i = 0; i < 2; i++)
        {
          private_data->bounding_box[2 * i] = x;
          private_data->bounding_box[2 * i + 1] = y;
        }
      y = searcher->max_y;
      for (i = 2; i < 4; i++)
        {
          private_data->bounding_box[2 * i] = x;
          private_data->bounding_box[2 * i + 1] = y;
        }
      goto end;
    }
  else if (all_y_same)
    {
#if DEBUG
      g_debug ("all %u points have the same y-location: bounding box is a line", npoints);
#endif
      x = searcher->min_x;
      y = searcher->min_y;
      for (i = 0; i < 2; i++)
        {
          private_data->bounding_box[2 * i] = x;
          private_data->bounding_box[2 * i + 1] = y;
        }
      x = searcher->max_x;
      for (i = 2; i < 4; i++)
        {
          private_data->bounding_box[2 * i] = x;
          private_data->bounding_box[2 * i + 1] = y;
        }
      goto end;
    }

  /* Get the convex hull around the locations. */
#if DEBUG
  g_debug ("getting convex hull around %u points", npoints);
#endif
  /* Set up an array of pointers to each x,y coordinate. */
  hull = g_new (double *, npoints + 1);
  for (i = 0; i < npoints; i++)
    {
      hull[i] = (double *)(private_data->xy->data) + 2 * i;
    }
  hull_npoints = ch2d (hull, npoints);
#if DEBUG
  g_debug ("convex hull has %u points", hull_npoints);
#endif

  /* Get the minimum-area oriented box around the hull.  First we copy the xy
   * array into an array of WML_Vector2 objects, since that's what the function
   * expects. */
  hull2 = g_new (WML_Vector2, hull_npoints);
  for (i = 0; i < hull_npoints; i++)
    {
      hull2[i].X = hull[i][0];
      hull2[i].Y = hull[i][1];
    }
  g_free (hull);
#if DEBUG
  g_debug ("getting minimum-area box around hull");
#endif
  /* FIXME: replace with the O(n log n) algorithm once it's working. */
  minbox = WML_MinBoxOrderNSqr (hull_npoints, hull2);
  WML_Box2_ComputeVertices (minbox, corner);

  /* Copy the corners into the herd list. */
  for (i = 0; i < 4; i++)
    {
      private_data->bounding_box[2 * i] = corner[i].X;
      private_data->bounding_box[2 * i + 1] = corner[i].Y;
    }
#if DEBUG
  s = g_string_new ("minimum-area oriented rectangle (x,y): [");
  for (i = 0; i < 4; i++)
    {
      if (i > 0)
        g_string_append_c (s, ',');
      g_string_append_printf (s, "(%.1f,%.1f)", corner[i].X, corner[i].Y);
    }
  g_string_append_c (s, ']');
  g_debug ("%s", s->str);
  g_string_free (s, TRUE);
#endif

end:
  /* Compute the edge lengths for the bounding rectangle. */
  private_data->xaxis_length =
    distance (private_data->bounding_box[0], private_data->bounding_box[1],
              private_data->bounding_box[2], private_data->bounding_box[3]);
  private_data->yaxis_length =
    distance (private_data->bounding_box[0], private_data->bounding_box[1],
              private_data->bounding_box[6], private_data->bounding_box[7]);
  private_data->short_axis_length = MIN (private_data->xaxis_length, private_data->yaxis_length);
#if DEBUG
  g_debug ("side lengths (km) = %.1f,%.1f",
           private_data->xaxis_length, private_data->yaxis_length);
#endif

  /* Clean up. */
  if (hull2 != NULL)
    g_free (hull2);
  if (minbox != NULL)
    WML_free_Box2 (minbox);
#if DEBUG
  g_debug ("----- EXIT find_oriented_bounding_box");
#endif
  return;
}



/**
 * Prepares the spatial search object for use, after all the points have been
 * added.
 *
 * @param searcher the spatial search object.
 */
void
spatial_search_prepare (spatial_search_t *searcher)
{
  private_data_t *private_data;

#if DEBUG
  g_debug ("----- ENTER spatial_search_prepare");
#endif

  private_data = (private_data_t *)(searcher->private_data);

#if DEBUG
  g_debug ("x range %g-%g y range %g-%g",
           searcher->min_x, searcher->max_x,
           searcher->min_y, searcher->max_y);
#endif

  /* This is specific to the R-tree algorithm: it is useful to know how large
   * the area covered by the points is.  So we find the minimum-area oriented
   * bounding box around the point. */
  find_oriented_bounding_box (searcher);
  private_data->rtree_threshold = 0.25 * private_data->short_axis_length;

#if DEBUG
  g_debug ("----- EXIT spatial_search_prepare");
#endif

  return;
}



typedef struct
{
  spatial_search_hit_callback user_function;
  gpointer user_data;
  GArray *xy;
  double center_x, center_y, radius_sq; /* used just in circular searches */
}
spatial_search_callback_args_t;



/**
 * The function that the R-tree code library calls when it finds a point inside
 * the requested search rectangle.  Because we want a search circle, we do an
 * additional distance check before passing this point along to the
 * user-provided callback function.
 *
 * @param id the id of the point found by the R-tree search.
 * @param arg the user-provided function to notify about the found point.
 */
int
spatial_search_circle_callback (int id, void *arg)
{
  spatial_search_callback_args_t *args;
  unsigned int index;
  double point_x, point_y;

  args = (spatial_search_callback_args_t *) arg;
  /* Retrieve the x and y-coordinate of the point with id "id".  Recall that
   * R-tree id's start at 1. */
  index = (id - 1) * 2;
  point_x = g_array_index (args->xy, double, index);
  point_y = g_array_index (args->xy, double, index + 1);

  if (distance_sq (args->center_x, args->center_y, point_x, point_y) <= args->radius_sq)
    args->user_function (id - 1, args->user_data);

  /* A return value of 0 would mean that the R-tree search should stop early
   * (before all points in the search circle were visited).  We don't want
   * that, so return 1. */
  return 1;
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
void
spatial_search_circle_by_xy (spatial_search_t * searcher,
                             double x, double y, double radius,
                             spatial_search_hit_callback user_function,
                             gpointer user_data)
{
  private_data_t *private_data;
  spatial_search_callback_args_t args;

#if DEBUG
  g_debug ("----- ENTER spatial_search_circle_by_xy (x=%g, y=%g, radius=%g)", x, y, radius);
#endif

  private_data = (private_data_t *)(searcher->private_data);

  args.user_function = user_function;
  args.user_data = user_data;
  args.xy = private_data->xy;
  args.center_x = x;
  args.center_y = y;
  args.radius_sq = gsl_pow_2 (radius);

  if (radius * 2 <= private_data->rtree_threshold)
    {
      struct Rect search_rect;
#if DEBUG
      g_debug ("use R-tree");
#endif
      search_rect.boundary[0] = x - radius;
      search_rect.boundary[1] = y - radius;
      search_rect.boundary[2] = x + radius;
      search_rect.boundary[3] = y + radius;
      RTreeSearch (private_data->rtree, &search_rect, spatial_search_circle_callback, &args);
    }
  else
    {
      unsigned int npoints, id;
#if DEBUG
      g_debug ("use exhaustive search");
#endif
      npoints = searcher->npoints;
      for (id = 1; id <= npoints; id++)
        spatial_search_circle_callback (id, &args);
    }

#if DEBUG
  g_debug ("----- EXIT spatial_search_circle_by_xy");
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
void
spatial_search_circle_by_id (spatial_search_t * searcher,
                             int id, double radius,
                             spatial_search_hit_callback user_function,
                             gpointer user_data)
{
  private_data_t *private_data;
  unsigned int index;
  double x, y;

#if DEBUG
  g_debug ("----- ENTER spatial_search_circle_by_id (id=%i, radius=%g)", id, radius);
#endif

  private_data = (private_data_t *)(searcher->private_data);
  index = id * 2;
  x = g_array_index (private_data->xy, double, index);
  y = g_array_index (private_data->xy, double, index + 1);
  spatial_search_circle_by_xy (searcher, x, y, radius, user_function, user_data);

#if DEBUG
  g_debug ("----- EXIT spatial_search_circle_by_id");
#endif

  return;
}



/**
 * The function that the R-tree code library calls when it finds a point inside
 * the requested search rectangle.
 *
 * @param id the id of the point found by the R-tree search.
 * @param arg the user-provided function to notify about the found point.
 */
int
spatial_search_rectangle_callback (int id, void *arg)
{
  spatial_search_callback_args_t *args;

  args = (spatial_search_callback_args_t *) arg;
  args->user_function (id - 1, args->user_data);

  /* A return value of 0 would mean that the R-tree search should stop early
   * (before all points in the search circle were visited).  We don't want
   * that, so return 1. */
  return 1;
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
void
spatial_search_rectangle (spatial_search_t * searcher,
                          double x1, double y1, double x2, double y2,
                          spatial_search_hit_callback user_function,
                          gpointer user_data)
{
  private_data_t *private_data;
  spatial_search_callback_args_t args;
  double long_axis;

#if DEBUG
  g_debug ("----- ENTER spatial_search_rectangle");
#endif

  private_data = (private_data_t *)(searcher->private_data);

  args.user_function = user_function;
  args.user_data = user_data;

  long_axis = MAX (fabs(x2 - x1), fabs(y2 - y1));
  if (long_axis <= private_data->rtree_threshold)
    {
      struct Rect search_rect;
      search_rect.boundary[0] = x1;
      search_rect.boundary[1] = y1;
      search_rect.boundary[2] = x2;
      search_rect.boundary[3] = y2;
      RTreeSearch (private_data->rtree, &search_rect, spatial_search_rectangle_callback, &args);
    }
  else
    {
      unsigned int npoints, id;
      double *x, *y;
      npoints = searcher->npoints;
      x = y = (double *)(private_data->xy->data);
      y++;
      for (id = 1; id <= npoints; id++, x+=2, y+=2)
      {
        if (*x >= x1 && *x < x2 && *y >= y1 && *y < y2)
          spatial_search_rectangle_callback (id, &args);
      }
    }

#if DEBUG
  g_debug ("----- EXIT spatial_search_rectangle");
#endif

  return;
}



/**
 * Deletes a spatial search object from memory.
 *
 * @param searcher a spatial search object.
 */
void
free_spatial_search (spatial_search_t *searcher)
{
  private_data_t *private_data;

#if DEBUG
  g_debug ("----- ENTER free_spatial_search");
#endif

  if (searcher != NULL)
  {
    private_data = (private_data_t *)(searcher->private_data);  
    RTreeDeleteIndex (private_data->rtree);
    g_array_free (private_data->xy, TRUE);
    g_free (private_data);
    g_free (searcher);
  }

#if DEBUG
  g_debug ("----- EXIT free_spatial_search");
#endif

  return;
}

/* end of file spatial_search_rtree.c */
