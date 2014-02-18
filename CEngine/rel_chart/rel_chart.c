/** @file rel_chart.c
 * Functions for creating, destroying, printing, and getting values from
 * relationship charts.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date May 2003
 *
 * Copyright &copy; University of Guelph, 2003-2006
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#if HAVE_CONFIG_H
#  include <config.h>
#endif

#if HAVE_STRING_H
#  include <string.h>
#endif

#include "rel_chart.h"
#include <gsl/gsl_math.h>

#define EPSILON 0.00001



/**
 * Creates a new single-point relationship chart.  Useful for constructing
 * simple default relationship charts.
 *
 * @param y the single y-value.
 * @return a pointer to a newly-created REL_chart_t structure.
 */
REL_chart_t *
REL_new_point_chart (double y)
{
  REL_chart_t *chart;
  REL_point_chart_t *t;         /* part specific to this chart type */

#if DEBUG
  g_debug ("----- ENTER REL_new_point_chart");
#endif

  chart = g_new (REL_chart_t, 1);
  chart->type = REL_Point;
  t = &(chart->u.point);
  t->value = y;

#if DEBUG
  g_debug ("----- EXIT REL_new_point_chart");
#endif

  return chart;
}



/**
 * Returns a text representation of a single-point relationship chart.
 *
 * @param chart a single-point relationship chart.
 * @return a string.
 */
char *
REL_point_chart_to_string (REL_point_chart_t * chart)
{
  GString *s;
  char *chararray;

  s = g_string_new ("<relationship chart\n points={");
  g_string_sprintfa (s, "(_,%.2g)", chart->value);
  g_string_append (s, "}>");
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new generic (2 or more points) relationship chart.  This function
 * copies the points, so the <i>x</i> and <i>y</i> arrays may be freed or
 * modified afterward.  If there is only 1 point, or if all the points are the
 * same, a "single-point" chart is returned instead of a generic one.
 *
 * @param x the x-values of the points.
 * @param y the y-values of the points.
 * @param n the number of points.
 * @return a pointer to a newly-created REL_chart_t structure.
 */
REL_chart_t *
REL_new_generic_chart (double *x, double *y, size_t n)
{
  REL_chart_t *chart;
  REL_generic_chart_t *t;       /* part specific to this chart type */
  gsl_spline *spline;
  gsl_interp_accel *accelerator;
  size_t i, j;                  /* loop counter */

#if DEBUG
  GString *s;
#endif

#if DEBUG
  g_debug ("----- ENTER REL_new_generic_chart");
#endif

  /* Remove duplicates (assuming points are ordered by x-value). */
  #if DEBUG
    g_debug ("removing duplicate points");
  #endif
  for (i = 0; i + 1 < n;)
    {
      #if DEBUG
        g_debug ("i=%lu", (unsigned long)i);
      #endif
      if (gsl_fcmp (x[i], x[i + 1], EPSILON) == 0 && gsl_fcmp (y[i], y[i + 1], EPSILON) == 0)
        {
          for (j = i; j + 1 < n; j++)
            {
              x[j] = x[j + 1];
              y[j] = y[j + 1];
            }
          n--;
          #if DEBUG
            g_debug ("removing point %lu, now n=%lu", (unsigned long)i, (unsigned long)n);
          #endif
        }
      else
        i++;
    }
#if DEBUG
  s = g_string_new (NULL);
  for (i = 0; i < n; i++)
    g_string_append_printf (s, (i > 0) ? ",(%g,%g)" : "(%g,%g)", x[i], y[i]);
  g_debug ("chart now {%s}", s->str);
  g_string_free (s, TRUE);
#endif

  /* Remove collinear points. */
  #if DEBUG
    g_debug ("removing collinear points");
  #endif
  for (i = 0; i + 2 < n;)
    {
      #if DEBUG
        g_debug ("i=%lu", (unsigned long)i);
      #endif
      if (gsl_fcmp (y[i], y[i + 1], EPSILON) == 0 && gsl_fcmp (y[i + 1], y[i + 2], EPSILON) == 0)
        {
          for (j = i + 1; j + 1 < n; j++)
            {
              x[j] = x[j + 1];
              y[j] = y[j + 1];
            }
          n--;
          #if DEBUG
            g_debug ("removing point %lu, now n=%lu", (unsigned long)i + 1, (unsigned long)n);
          #endif
        }
      else
        i++;
    }
#if DEBUG
  s = g_string_new (NULL);
  for (i = 0; i < n; i++)
    g_string_append_printf (s, (i > 0) ? ",(%g,%g)" : "(%g,%g)", x[i], y[i]);
  g_debug ("chart now {%s}", s->str);
  g_string_free (s, TRUE);
#endif

  if (n == 1)
    {
      chart = REL_new_point_chart (y[0]);
      g_warning ("relationship chart contained only 1 point, (%g,%g)", x[0], y[0]);
      goto end;
    }

  chart = g_new (REL_chart_t, 1);
  chart->type = REL_Generic;
  t = &(chart->u.generic);
  t->first_x = x[0];
  t->last_x = x[n - 1];
  t->min = t->max = y[0];

  for (i = 1; i < n; i++)
    {
      if (y[i] < t->min)
        t->min = y[i];
      else if (y[i] > t->max)
        t->max = y[i];
    }

  spline = gsl_spline_alloc (gsl_interp_linear, n);

  g_assert (spline != NULL);

  gsl_spline_init (spline, x, y, n);

  accelerator = gsl_interp_accel_alloc ();
  g_assert (accelerator != NULL);
  t->spline = spline;
  t->accelerator = accelerator;

end:
#if DEBUG
  g_debug ("----- EXIT REL_new_generic_chart");
#endif
  return chart;
}



/**
 * Deletes the dynamically-allocated parts of a generic relationship chart from
 * memory.
 *
 * @param chart a generic relationship chart.
 */
void
REL_free_generic_chart (REL_generic_chart_t * chart)
{
  gsl_interp_accel_free (chart->accelerator);
  gsl_spline_free (chart->spline);
}



/**
 * Returns a text representation of a generic relationship chart.
 *
 * @param chart a generic relationship chart.
 * @return a string.
 */
char *
REL_generic_chart_to_string (REL_generic_chart_t * chart)
{
  GString *s;
  char *chararray;
  size_t npoints;
  int i;                        /* loop counter */

  s = g_string_new ("<relationship chart\n points={");
  npoints = chart->spline->size;
  for (i = 0; i < npoints; i++)
    g_string_sprintfa (s, i > 0 ? ", (%.2g,%.2g)" : "(%.2g,%.2g)",
                       chart->spline->x[i], chart->spline->y[i]);
  g_string_append (s, "}>");
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new relationship chart.  This function copies the points, so the
 * <i>x</i> and <i>y</i> arrays may be freed or modified afterward.
 *
 * @param x the <i>x</i>-values of the points.  Must be strictly increasing.
 * @param y the <i>y</i>-values of the points.
 * @param n the number of points.
 * @return a pointer to a newly-created REL_chart_t structure.
 */
REL_chart_t *
REL_new_chart (double *x, double *y, size_t n)
{
  REL_chart_t *chart;

#if DEBUG
  g_debug ("----- ENTER REL_new_chart");
#endif

  g_assert (n > 0);
  if (n == 1)
    chart = REL_new_point_chart (y[0]);
  else
    chart = REL_new_generic_chart (x, y, n);

#if DEBUG
  g_debug ("----- EXIT REL_new_chart");
#endif

  return chart;
}



/**
 * Returns a text representation of a relationship chart.
 *
 * @param chart a relationship chart.
 * @return a string.
 */
char *
REL_chart_to_string (REL_chart_t * chart)
{
  char *s;

  switch (chart->type)
    {
    case REL_Generic:
      s = REL_generic_chart_to_string (&(chart->u.generic));
      break;
    case REL_Point:
      s = REL_point_chart_to_string (&(chart->u.point));
      break;
    default:
      g_assert_not_reached ();
    }

  return s;
}



/**
 * Prints a relationship chart to a stream.
 *
 * @param stream a stream to write to.
 * @param chart a relationship chart.
 * @return the number of characters printed (not including the trailing '\\0').
 */
int
REL_fprintf_chart (FILE * stream, REL_chart_t * chart)
{
  char *s;
  int nchars_written;

  s = REL_chart_to_string (chart);
  nchars_written = fprintf (stream, "%s", s);
  free (s);
  return nchars_written;
}



/**
 * Returns the y-value for a given \a x value from a relationship chart.
 *
 * @param x
 * @param chart a relationship chart.
 * @return the <i>y</i>-value at <i>x</i>.  If <i>x</i> < the
 *   <i>x</i>-coordinate of the leftmost point in the chart, the <i>y</i>-value
 *   of the leftmost point is returned.  If <i>x</i> > the <i>x</i>-coordinate
 *   of the rightmost point in the chart, the <i>y</i>-value of the rightmost
 *   point is returned.
 */
double
REL_chart_lookup (double x, REL_chart_t * chart)
{
  double y;

  switch (chart->type)
    {
    case REL_Generic:
      y =
        gsl_spline_eval (chart->u.generic.spline,
                         CLAMP (x, chart->u.generic.first_x,
                                chart->u.generic.last_x), chart->u.generic.accelerator);
      break;
    case REL_Point:
      y = chart->u.point.value;
      break;
    default:
      g_assert_not_reached ();
    }
  return y;
}



/**
 * Returns the greatest <i>y</i>-value in a relationship chart.
 *
 * @param chart a relationship chart.
 * @return the greatest <i>y</i>-value in the chart.
 */
double
REL_chart_max (REL_chart_t * chart)
{
  double y;

  switch (chart->type)
    {
    case REL_Generic:
      y = chart->u.generic.max;
      break;
    case REL_Point:
      y = chart->u.point.value;
      break;
    default:
      g_assert_not_reached ();
    }
  return y;
}



/**
 * Returns the smallest <i>y</i>-value in a relationship chart.
 *
 * @param chart a relationship chart.
 * @return the smallest <i>y</i>-value in the chart.
 */
double
REL_chart_min (REL_chart_t * chart)
{
  double y;

  switch (chart->type)
    {
    case REL_Generic:
      y = chart->u.generic.min;
      break;
    case REL_Point:
      y = chart->u.point.value;
      break;
    default:
      g_assert_not_reached ();
    }
  return y;
}



/**
 * Returns the smallest and largest <i>x</i>-values in a relationship chart.
 * For single-point relationship charts, returns 0 for both.
 *
 * @param chart a relationship chart.
 * @param min_x a location in which to store the smallest <i>x</i>-value.
 * @param max_x a location in which to store the largest <i>x</i>-value.
 */
void
REL_chart_get_domain (REL_chart_t * chart, double *min_x, double *max_x)
{
  switch (chart->type)
    {
    case REL_Generic:
      *min_x = chart->u.generic.first_x;
      *max_x = chart->u.generic.last_x;
      break;
    case REL_Point:
      *min_x = 0;
      *max_x = 0;
      break;
    default:
      g_assert_not_reached ();
    }
  return;
}



/**
 * Translates and scales a relationship chart so that its smallest and largest
 * <i>x</i>-values match what is given.  Has no effect on single-point
 * relationship charts.
 *
 * @param chart a relationship chart.
 * @param min_x the new smallest <i>x</i>-value.
 * @param max_x the new largest <i>x</i>-value.
 */
void
REL_chart_set_domain (REL_chart_t * chart, double min_x, double max_x)
{
  REL_generic_chart_t *t;	/* part specific to the generic chart type */
  size_t n, i;			/* loop counter */
  double scale;
  double *x, *y;

#if DEBUG
  g_debug ("----- ENTER REL_chart_set_domain");
#endif

  if (chart->type != REL_Generic)
    goto end;

  t = &(chart->u.generic);

  /* Copy the existing y values from the GSL spline structure. */
  n = t->spline->size;
  y = g_new (double, n);
  memcpy (y, t->spline->y, n * sizeof(double));

  /* Scale and translate the x-values. */
  x = g_new (double, n);
  scale = (max_x - min_x) / (t->last_x - t->first_x);
  for (i = 0; i < n; i++)
    x[i] = (t->spline->x[i] - t->first_x) * scale + min_x;

  /* Now free the old spline structure and create a new one. */
  gsl_interp_accel_free (t->accelerator);
  gsl_spline_free (t->spline);

  t->spline = gsl_spline_alloc (gsl_interp_linear, n);
  g_assert (t->spline != NULL);
  gsl_spline_init (t->spline, x, y, n);
  t->accelerator = gsl_interp_accel_alloc ();
  g_assert (t->accelerator != NULL);

  t->first_x = min_x;
  t->last_x = max_x;

  /* Since the x and y value arrays were copied by the gsl_spline_init
   * function, we can free them. */
  g_free(x);
  g_free(y);

end:
#if DEBUG
  g_debug ("----- EXIT REL_chart_set_domain");
#endif
  return;
}



/**
 * Returns true if the relationship chart begins with the value 0.
 *
 * Side effect: if this function will return true and if the parameter first_x
 * is not null, this function also fills in the location first_x with the
 * leftmost x-value in the chart.
 *
 * @param chart a relationship chart.
 * @param first_x a location in which to fill in the leftmost x-value in the
 *   chart, or 0 if chart is a single-point relationship chart.  If this
 *   function returns false or if this parameter is null, no value will be
 *   filled in.
 * @return true if the relationship chart begins with the value 0, false
 *   otherwise.
 */
gboolean
REL_chart_zero_at_left (REL_chart_t * chart, double *first_x)
{
  double y;
  gboolean result = FALSE;

  switch (chart->type)
    {
    case REL_Point:
      y = chart->u.point.value;
      if (gsl_fcmp (y, 0, EPSILON))
        {
          result = TRUE;
          if (first_x != NULL)
            *first_x = 0;
        }
      break;
    case REL_Generic:
      y = REL_chart_lookup (chart->u.generic.first_x, chart);
      if (gsl_fcmp (y, 0, EPSILON))
        {
          result = TRUE;
          if (first_x != NULL)
            *first_x = chart->u.generic.first_x;
        }
      break;
    default:
      g_assert_not_reached ();
    }
  return result;
}



/**
 * Returns true if the relationship chart ends with the value 0.
 *
 * Side effect: if this function will return true and if the parameter last_x
 * is not null, this function also fills in the location last_x with the
 * rightmost x-value in the chart.
 *
 * @param chart a relationship chart.
 * @param last_x a location in which to fill in the rightmost x-value in the
 *   chart, or 0 if chart is a single-point relationship chart.  If this
 *   function returns false or if this parameter is null, no value will be
 *   filled in.
 * @return true if the relationship chart ends with the value 0, false
 *   otherwise.
 */
gboolean
REL_chart_zero_at_right (REL_chart_t * chart, double *last_x)
{
  double y;
  gboolean result = FALSE;

#if DEBUG
  g_debug ("----- ENTER REL_chart_zero_at_right");
#endif

  switch (chart->type)
    {
    case REL_Point:
      y = chart->u.point.value;
      if (gsl_fcmp (y, 0, EPSILON) == 0)
        {
          result = TRUE;
          if (last_x != NULL)
            *last_x = 0;
        }
      break;
    case REL_Generic:
      y = REL_chart_lookup (chart->u.generic.last_x, chart);
      if (gsl_fcmp (y, 0, EPSILON) == 0)
        {
          result = TRUE;
          if (last_x != NULL)
            *last_x = chart->u.generic.last_x;
        }
      break;
    default:
      g_assert_not_reached ();
    }

#if DEBUG
  g_debug ("----- EXIT REL_chart_zero_at_right");
#endif

  return result;
}



/**
 * Deletes a relationship chart from memory.
 *
 * @param chart a relationship chart.
 */
void
REL_free_chart (REL_chart_t * chart)
{
  if (chart == NULL)
    return;

  switch (chart->type)
    {
    case REL_Generic:
      REL_free_generic_chart (&(chart->u.generic));
      break;
    case REL_Point:
      /* No dynamically-allocated parts to free. */
      break;
    default:
      g_assert_not_reached ();
    }
  g_free (chart);
}



/**
 * Makes a deep copy of a relationship chart.
 *
 * @param chart a relationship chart.
 * @return a deep copy of the relationship chart.
 */
REL_chart_t *
REL_clone_chart (REL_chart_t * chart)
{
  REL_chart_t *clone;

  if (chart == NULL)
    return NULL;

  switch (chart->type)
    {
    case REL_Point:
      {
        REL_point_chart_t *c;
        c = &(chart->u.point);
        clone = REL_new_point_chart (c->value);
        break;
      }
    case REL_Generic:
      {
        REL_generic_chart_t *c;
        c = &(chart->u.generic);
        /* Copy the x-y coordinates from the existing chart. */
        clone = REL_new_chart (c->spline->x, c->spline->y, c->spline->size);
        break;
      }
    default:
      g_assert_not_reached ();
    }

  return clone;
}

/* end of file rel_chart.c */
