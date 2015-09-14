/** @file prob_dist.c
 * Functions for creating, destroying, printing, and getting values and
 * variates from probability distributions.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @author Aaron Reeves <Aaron.Reeves@colostate.edu><br>
 *   Animal Population Health Institute<br>
 *   Colorado State University<br>
 *   Fort Collins, CO 80523<br>
 *   USA
 * @author Shaun Case <Shaun.Case@colostate.edu><br>
 *   Animal Population Health Institute<br>
 *   College of Veterinary Medicine and Biomedical Sciences<br>
 *   Colorado State University<br>
 *   Fort Collins, CO 80523<br>
 *   USA 
 * @author Anthony Schwickerath <Drew.Schwickerath@colostate.edu><br>
 *   Animal Population Health Institute<br>
 *   Colorado State University<br>
 *   Fort Collins, CO 80523<br>
 *   USA
 * @date February 2003
 *
 * Copyright &copy; University of Guelph, 2003-2010
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#if HAVE_CONFIG_H
#  include "config.h"
#endif

#include "prob_dist.h"

#if HAVE_MATH_H
#  include <math.h>
#endif

#if !HAVE_ROUND && HAVE_RINT
#  define round rint
#endif

/* Temporary fix -- "round" and "rint" are in the math library on Red Hat 7.3,
 * but they're #defined so AC_CHECK_FUNCS doesn't find them. */
double round (double x);

#if HAVE_LIMITS_H
#  include <limits.h>
#endif

#include <glib.h>
#include <gsl/gsl_math.h>
#include <gsl/gsl_poly.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_cdf.h>
#include <gsl/gsl_sf_gamma.h>
#include <gsl/gsl_integration.h>

#define EPSILON 0.00001
#define MAX_BISECTION_ITER 300



/**
 * Names for the probability distributions, terminated with a NULL sentinel.
 *
 * @sa PDF_dist_type_t
 */
const char *PDF_dist_type_name[] = {
  "Point", "Uniform", "Triangular", "Piecewise", "Histogram", "Gaussian",
  "Poisson", "Beta", "Gamma", "Weibull", "Exponential", "Pearson5", "Logistic",
  "LogLogistic", "Lognormal", "NegativeBinomial", "Pareto", "Bernoulli", 
  "Binomial", "Discrete Uniform", "Hypergeometric", "Inverse Gaussian", NULL
};



/**
 * Creates a new point distribution (one that always returns the same value).
 *
 * @param value the number that the distribution will always return.
 * @return a pointer to a newly-created PDF_dist_t structure, or NULL if there
 *   wasn't enough memory to allocate one.
 */
PDF_dist_t *
PDF_new_point_dist (double value)
{
  PDF_dist_t *dist;
  PDF_point_dist_t *t;          /* part specific to this distribution */

#if DEBUG
  g_debug ("----- ENTER PDF_new_point_dist");
#endif

  dist = g_new (PDF_dist_t, 1);
  dist->type = PDF_Point;
  dist->has_inf_lower_tail = dist->has_inf_upper_tail = FALSE;
  dist->discrete = FALSE;
  t = &(dist->u.point);
  t->value = value;

#if DEBUG
  g_debug ("----- EXIT PDF_new_point_dist");
#endif

  return dist;
}



/**
 * Returns a text representation of a point distribution.
 *
 * @param dist a point distribution.
 * @return a string.
 */
char *
PDF_point_dist_to_string (PDF_point_dist_t * dist)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<point probability distribution\n value=%.2g>", dist->value);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new uniform (flat) distribution with parameters as illustrated
 * below.
 *
 * @image html uniform.png
 *
 * @return a pointer to a newly-created PDF_dist_t structure, or NULL if there
 *   wasn't enough memory to allocate one.
 */
PDF_dist_t *
PDF_new_uniform_dist (double a, double b)
{
  PDF_dist_t *dist;
  PDF_uniform_dist_t *t;        /* part specific to this distribution */
  double tmp;

#if DEBUG
  g_debug ("----- ENTER PDF_new_uniform_dist");
#endif

  /* If a and b are the same, return a point distribution instead. */
  if (gsl_fcmp (a, b, EPSILON) == 0)
    {
      dist = PDF_new_point_dist (a);
    }
  else
    {
      dist = g_new (PDF_dist_t, 1);
      dist->type = PDF_Uniform;
      dist->has_inf_lower_tail = dist->has_inf_upper_tail = FALSE;
      dist->discrete = FALSE;
      t = &(dist->u.uniform);

      /* Swap a and b if they're in the wrong order. */
      if (b < a)
        {
          tmp = a;
          a = b;
          b = tmp;
        }
      t->a = a;
      t->b = b;
      t->range = b - a;
    }

#if DEBUG
  g_debug ("----- EXIT PDF_new_uniform_dist");
#endif

  return dist;
}



/**
 * Returns a text representation of a uniform (flat) distribution.
 *
 * @param dist a uniform distribution.
 * @return a string.
 */
char *
PDF_uniform_dist_to_string (PDF_uniform_dist_t * dist)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s,
                    "<uniform (flat) probability distribution\n from %.2g to %.2g>",
                    dist->a, dist->b);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Computes the cumulative area <= \a x for a uniform (flat) distribution.
 *
 * @param x
 * @param dist a uniform distribution.
 */
double
uniform_cdf (double x, PDF_uniform_dist_t * dist)
{
  if (x < dist->a)
    return 0;
  else if (x > dist->b)
    return 1;
  else
    return (x - dist->a) / dist->range;
}



/**
 * The inverse cumulative distribution function for a uniform (flat)
 * distribution.
 *
 * @param area 0 <= \a area <= 1.
 * @param dist a uniform distribution.
 * @return the value at which the cumulative distribution function = \a area.
 */
double
uniform_inverse_cdf (double area, PDF_uniform_dist_t * dist)
{
  return dist->range * area + dist->a;
}



/**
 * Creates a new triangular distribution with parameters as illustrated below.
 * If <i>a</i>, <i>c</i>, and <i>b</i> are given in the wrong order, they will
 * be re-arranged.  If <i>a</i>, <i>c</i>, and <i>b</i> are all the same value,
 * a "point" distribution is returned instead of a triangular distribution.
 *
 * @image html triangular.png
 *
 * @param a the minimum.
 * @param c the mode.
 * @param b the maximum.
 * @return a pointer to a newly-created PDF_dist_t structure, or NULL if there
 *   wasn't enough memory to allocate one.
 */
PDF_dist_t *
PDF_new_triangular_dist (double a, double c, double b)
{
  PDF_dist_t *dist;
  PDF_triangular_dist_t *t;     /* part specific to this distribution */
  gboolean out_of_order = FALSE;
  double tmp;

#if DEBUG
  g_debug ("----- ENTER PDF_new_triangular_dist");
#endif

  if (gsl_fcmp (a, b, EPSILON) == 0 && gsl_fcmp (b, c, EPSILON) == 0)
    {
      dist = PDF_new_point_dist (a);
      goto end;
    }

  dist = g_new (PDF_dist_t, 1);
  dist->type = PDF_Triangular;
  dist->has_inf_lower_tail = dist->has_inf_upper_tail = FALSE;
  dist->discrete = FALSE;
  t = &(dist->u.triangular);

  /* Re-order the parameters if they're given out of order. */
  if (a > c)
    {
      tmp = a;
      a = c;
      c = tmp;
      out_of_order = TRUE;
    }
  if (c > b)
    {
      tmp = c;
      c = b;
      b = tmp;
      out_of_order = TRUE;
    }
  if (a > c)
    {
      tmp = a;
      a = c;
      c = tmp;
      out_of_order = TRUE;
    }
  if (out_of_order)
    g_warning ("parameters were rearranged so that a <= c <= b");

  t->a = a;
  t->b = b;
  t->c = c;
  t->P = (c - a) / (b - a);
  t->one_minus_P = 1 - t->P;
  t->range = b - a;
  t->width_1 = c - a;
  t->width_2 = b - c;
  t->rw1 = t->range * t->width_1;
  t->rw2 = t->range * t->width_2;

end:
#if DEBUG
  g_debug ("----- EXIT PDF_new_triangular_dist");
#endif

  return dist;
}



/**
 * Returns a text representation of a triangular distribution.
 *
 * @param dist a triangular distribution.
 * @return a string.
 */
char *
PDF_triangular_dist_to_string (PDF_triangular_dist_t * dist)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s,
                    "<triangular probability distribution\n a=%.2g, c=%.2g, b=%.2g\n P=%.2g>",
                    dist->a, dist->c, dist->b, dist->P);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}




/**
 * Computes the probability density p(x) at x for a triangular distribution.
 *
 * @param x
 * @param dist a triangular distribution.
 */
double
triangular_pdf (double x, PDF_triangular_dist_t * dist)
{
  if (x <= dist->a)
    return 0;
  else if (x < dist->c)
    return 2 * (x - dist->a) / dist->rw1;
  else if (x < dist->b)
    return 2 * (dist->b - x) / dist->rw2;
  else
    return 0;
}



/**
 * Computes the cumulative area <= \a x for a triangular distribution.
 *
 * @param x
 * @param dist a triangular distribution.
 */
double
triangular_cdf (double x, PDF_triangular_dist_t * dist)
{
  double tmp;

  if (x <= dist->a)
    return 0;
  else if (x < dist->c)
    {
      tmp = x - dist->a;
      return tmp * tmp / dist->rw1;
    }
  else if (x < dist->b)
    {
      tmp = dist->b - x;
      return 1 - tmp * tmp / dist->rw2;
    }
  else
    return 1;
}


/**
 * The inverse cumulative distribution function for a triangular distribution.
 *
 * @param area 0 <= \a area <= 1.
 * @param dist a triangular distribution.
 * @return the value at which the cumulative distribution function = \a area.
 */
double
triangular_inverse_cdf (double area, PDF_triangular_dist_t * dist)
{
  double x1, x2, x;
  int nsolutions;

  if (area < dist->P)
    {
      nsolutions =
        gsl_poly_solve_quadratic (1, -2 * dist->a,
                                  (dist->a * dist->a) - area * dist->rw1, &x1, &x2);
      if (nsolutions == 1)
        x = x1;
      else
        {
          /* check which one is the solution */
          x = ((x1 >= dist->a) && (x1 <= dist->c) ? x1 : x2);
        }
    }
  else
    {
      nsolutions =
        gsl_poly_solve_quadratic (1, -2 * dist->b,
                                  (dist->b * dist->b) - (1 - area) * dist->rw2, &x1, &x2);
      if (nsolutions == 1)
        x = x1;
      else
        {
          /* check which one is the solution */
          x = ((x1 >= dist->c) && (x1 <= dist->b) ? x1 : x2);
        }
    }

  return x;
}

#ifdef WIN_DLL
/**
 * Computes the probability density p(x) at x for a triangular distribution.
 * This form of the function is primarily intended to be called from a
 * library.
 *
 * @param x
 * @param min the minimum value used to define a triangular PDF.
 * @param mode the mode used to define a triangular PDF.
 * @param max the maximum value used to define a triangular PDF.
 * @return the probability density p(x)
 */
DLL_API double
aphi_triangular_pdf( double x, double min, double mode, double max )
{
  PDF_dist_t *dist;
  double result;

  dist = PDF_new_triangular_dist (min, mode, max);
  result = triangular_pdf (x, &(dist->u.triangular));
  PDF_free_dist (dist);
  return result;
}


/**
 * Computes the cumulative area <= \a x for a triangular distribution.
 * This form of the function is primarily intended to be called from a
 * library.
 *
 * @param x
 * @param min the minimum value used to define a triangular PDF.
 * @param mode the mode used to define a triangular PDF.
 * @param max the maximum value used to define a triangular PDF.
 * @return the cumulative area <= \a x
 */
DLL_API double
aphi_triangular_cdf( double x, double min, double mode, double max )
{
  PDF_dist_t *dist;
  double result;

  dist = PDF_new_triangular_dist (min, mode, max);
  result = triangular_cdf (x, &(dist->u.triangular));
  PDF_free_dist (dist);
  return result;
}



/**
 * The inverse cumulative distribution function for a triangular distribution.
 * This form of the function is primarily intended to be called from a
 * library.
 *
 * @param area 0 <= \a area <= 1.
 * @param min the minimum value used to define a triangular PDF.
 * @param mode the mode used to define a triangular PDF.
 * @param max the maximum value used to define a triangular PDF.
 * @return the value at which the cumulative distribution function = \a area.
 */
DLL_API double
aphi_triangular_inverse_cdf( double area, double min, double mode, double max )
{
  PDF_dist_t *dist;
  double result;

  dist = PDF_new_triangular_dist (min, mode, max);
  result = triangular_inverse_cdf (area, &(dist->u.triangular));
  PDF_free_dist (dist);
  return result;
}
#endif


/**
 * Returns a random variate from a triangular distribution.
 *
 * @param dist a triangular distribution.
 * @param rng a random number generator.
 */
double
ran_triangular (PDF_triangular_dist_t * dist, RAN_gen_t * rng)
{
  double r;

  r = RAN_num (rng);
  if (r <= dist->P)
    return dist->a + dist->width_1 * sqrt (r / dist->P);
  else
    return dist->b - dist->width_2 * sqrt ((1 - r) / dist->one_minus_P);
}


#ifdef WIN_DLL
/**
 * Generates random variates from a triangular distribution.
 * This form of the function is primarily intended to be called from a 
 * library.
 *
 * @param rng a Delphi-compatible pointer to the random number generator.
 * @param min the minimum value used to define a triangular PDF.
 * @param mode the mode used to define a triangular PDF.
 * @param max the maximum value used to define a triangular PDF.
 * @return a random variate from the specified distribution.
 */
DLL_API double 
aphi_triangular_rand( int unsigned rng, double min, double mode, double max )
{
  PDF_dist_t* dist;
  double result;

  dist = PDF_new_triangular_dist( min, mode, max );
  result = PDF_random( dist, (RAN_gen_t*)rng );
  PDF_free_dist( dist );
  return result;
}

#endif

/**
 * Fills in the cumulative distribution at each x-coordinate for a
 * PDF_piecewise_dist_t structure.
 *
 * @param a a piecewise distribution.
 */
double
calc_cumulative_for_piecewise (PDF_piecewise_dist_t * a)
{
  double width;
  unsigned int i;               /* loop counter */

  a->cumul[0] = 0;
  for (i = 1; i < a->n; i++)
    {
      width = a->x[i] - a->x[i - 1];
      a->cumul[i] = a->cumul[i - 1] + ((a->y[i - 1] + a->y[i]) / 2) * width;
      a->slope[i - 1] = (a->y[i] - a->y[i - 1]) / width;
    }
  return a->cumul[a->n - 1];
}



/**
 * Creates a new piecewise distribution.  The distribution is built from
 * triangles and trapezoids, and is defined by a set of points, as shown in the
 * example below.
 *
 * @image html piecewise.png
 *
 * @param n the number of points on the curve.  \a n >= 1.
 * @param x an array containing the <i>x</i>-coordinates of the points on the
 *   curve.  The <i>x</i>-coordinates must be strictly increasing.  The values
 *   from x are copied, so the array can be freed if desired after calling this
 *   function.
 * @param y an array containing the <i>y</i>-coordinates of the points on the
 *   curve.  The first and last <i>y</i>-coordinates must be 0.  The others
 *   must be positive or 0, and at least one of them must be positive.  The
 *   <i>y</i>-coordinates will be scaled if necessary to make the area under
 *   the curve equal 1.  The values from y are copied, so the array can be
 *   freed if desired after calling this function.
 * @return a pointer to a newly-created PDF_dist_t structure, or NULL if there
 *   wasn't enough memory to allocate one.  If \a n = 1, this function will
 *   return a "point" distribution.
 */
PDF_dist_t *
PDF_new_piecewise_dist (unsigned int n, double *x, double *y)
{
  PDF_dist_t *dist;
  PDF_piecewise_dist_t *p;      /* part specific to this distribution */
  unsigned int i;               /* loop counter */
  gboolean positive_y;
  double total;

#if DEBUG
  g_debug ("----- ENTER PDF_new_piecewise_dist");
#endif

  g_assert (n >= 1);

  if (n == 1)
    dist = PDF_new_point_dist (y[0]);
  else
    {
      dist = g_new (PDF_dist_t, 1);
      dist->type = PDF_Piecewise;
      dist->has_inf_lower_tail = dist->has_inf_upper_tail = FALSE;
      dist->discrete = FALSE;
      p = &(dist->u.piecewise);
      p->x = g_new (double, n);
      p->y = g_new (double, n);
      p->cumul = g_new (double, n);
      p->slope = g_new (double, n - 1);

      /* Copy the coordinate list. */
      p->n = n;
      positive_y = FALSE;
      for (i = 0; i < n; i++)
        {
          p->x[i] = x[i];
          if (i > 0)
            {
              g_assert (p->x[i] > p->x[i - 1]);
            }
          p->y[i] = y[i];
          if (i == 0 || i == n - 1)
            g_assert (p->y[i] == 0);
          else
            {
              g_assert (p->y[i] >= 0);
              if (p->y[i] > 0)
                positive_y = TRUE;
            }
        }
      g_assert (positive_y == TRUE);
      p->first_x = p->x[0];
      p->last_x = p->x[n - 1];

      /* Calculate the cumulative probability at each x-coordinate.  If the
       * total is not 1, scale the y-coordinates to make it so. */
      total = calc_cumulative_for_piecewise (p);
      if (gsl_fcmp (total, 1, EPSILON) != 0)
        {
          for (i = 1; i < n - 1; i++)
            p->y[i] /= total;
          calc_cumulative_for_piecewise (p);
        }
    }

#if DEBUG
  g_debug ("----- EXIT PDF_new_piecewise_dist");
#endif

  return dist;
}



/**
 * Deletes the dynamically-allocated parts of piecewise distribution from
 * memory.
 *
 * @param dist a piecewise distribution.
 */
void
PDF_free_piecewise_dist (PDF_piecewise_dist_t * dist)
{
  g_free (dist->x);
  g_free (dist->y);
  g_free (dist->slope);
  g_free (dist->cumul);
}



/**
 * Returns a text representation of a piecewise distribution.
 *
 * @param dist a piecewise distribution.
 * @return a string.
 */
char *
PDF_piecewise_dist_to_string (PDF_piecewise_dist_t * dist)
{
  GString *s;
  char *chararray;
  int i;                        /* loop counter */

  s = g_string_new ("<piecewise probability distribution\n points={");
  for (i = 0; i < dist->n; i++)
    g_string_sprintfa (s, i > 0 ? ", (%.2g,%.2g)" : "(%.2g,%.2g)", dist->x[i], dist->y[i]);
  g_string_append (s, "}\n cumulative={");
  for (i = 0; i < dist->n; i++)
    g_string_sprintfa (s, i > 0 ? ", %.2g" : "%.2g", dist->cumul[i]);
  g_string_append (s, "}>");
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Computes the probability density p(x) at x for a piecewise distribution.
 *
 * @param x
 * @param dist a piecewise distribution.
 */
double
piecewise_pdf (double x, PDF_piecewise_dist_t * dist)
{
  unsigned int seg;             /* the segment in which x lies */
  unsigned int lo, hi;          /* for a binary search */

  if (x <= dist->first_x || x >= dist->last_x)
    return 0.0;

  /* Find the segment in which x lies (binary search). */
  lo = 0;
  hi = dist->n;
  while (hi - lo > 1)
    {
      seg = (lo + hi) / 2;
      if (x >= dist->x[seg])
        lo = seg;
      else
        hi = seg;
    }

  /* Linear interpolation. */
  x -= dist->x[lo];
  return dist->y[lo] + x * dist->slope[lo];
}



/**
 * Computes the cumulative area <= \a x for a piecewise distribution.
 *
 * @param x
 * @param a a piecewise distribution.
 */
double
piecewise_cdf (double x, PDF_piecewise_dist_t * a)
{
  unsigned int seg;             /* the segment in which x lies */
  unsigned int lo, hi;          /* for a binary search */
  double y;

#if DEBUG
  g_debug ("----- ENTER piecewise_cdf");
#endif

  if (x <= a->first_x)
    return 0.0;
  if (x >= a->last_x)
    return 1.0;

  /* Find the segment in which x lies (binary search). */
  lo = 0;
  hi = a->n;
  while (hi - lo > 1)
    {
      seg = (lo + hi) / 2;
      if (x >= a->x[seg])
        lo = seg;
      else
        hi = seg;
    }
#if DEBUG
  g_debug ("x (%g) is in segment %u", x, lo);
#endif

  x -= a->x[lo];
  y = a->y[lo] + x * a->slope[lo];

#if DEBUG
  g_debug ("----- EXIT piecewise_cdf");
#endif

  return a->cumul[lo] + x * ((y + a->y[lo]) / 2);
}



/**
 * The inverse cumulative distribution function for a piecewise distribution.
 * In some cases this function cannot give a meaningful answer.  In the example
 * below, the area of the left triangle is 0.5.  The cumulative area is 0.5
 * over the range [3,4].  So this function may return any number in that range
 * if asked for the value at which the area = 0.5.
 *
 * @image html piecewise_flat.png
 *
 * @param area 0 <= \a area <= 1.
 * @param dist a piecewise distribution.
 * @return the value at which the cumulative distribution function = \a area.
 */
double
piecewise_inverse_cdf (double area, PDF_piecewise_dist_t * dist)
{
  unsigned int seg;             /* the segment in which area lies */
  unsigned int lo, hi;          /* for a binary search */
  double x, y, slope;

#if DEBUG
  g_debug ("----- ENTER piecewise_inverse_cdf");
#endif

  if (area <= 0.0)
    return dist->first_x;
  if (area >= 1.0)
    return dist->last_x;

  /* Find the segment in which area lies (binary search). */
  lo = 0;
  hi = dist->n;
  while (hi - lo > 1)
    {
      seg = (lo + hi) / 2;
      if (area >= dist->cumul[seg])
        lo = seg;
      else
        hi = seg;
    }
  #if DEBUG
    g_debug ("area (%g) is in segment %u", area, lo);
  #endif

  area -= dist->cumul[lo];
  y = dist->y[lo];
  slope = dist->slope[lo];
  #if DEBUG
    g_debug ("for trapezoid calculation area=%g, h1=%g, slope=%g", area, y, slope);
  #endif

  if (gsl_fcmp (slope, 0, EPSILON) == 0)
    {
      /* easy case. */
      x = area / y;
    }
  else
    {
      /* this case requires solving a quadratic equation. */
      double x1, x2, max_x;
      int nsolutions;

      nsolutions = gsl_poly_solve_quadratic (slope / 2, y, -area, &x1, &x2);
      if (nsolutions == 1)
        x = x1;
      else
        {
          /* check which one is the solution */
          max_x = dist->x[lo + 1] - dist->x[lo];
          #if DEBUG
            g_debug ("max_x=%g, choices=(%g,%g)\n", max_x, x1, x2);
          #endif
          x = ((x1 >= 0) && (x1 <= max_x) ? x1 : x2);
        }
    }
#if DEBUG
  g_debug ("solution=%g", x + dist->x[lo]);
  g_debug ("----- EXIT piecewise_inverse_cdf");
#endif

  return x + dist->x[lo];
}



/**
 * Returns a random variate from a piecewise distribution.
 *
 * @param dist a piecewise distribution.
 * @param rng a random number generator.
 */
double
ran_piecewise (PDF_piecewise_dist_t * dist, RAN_gen_t * rng)
{
  double r;

  while (1)
    {
      r = dist->first_x + RAN_num (rng) * (dist->last_x - dist->first_x);
      if (RAN_num (rng) <= piecewise_pdf (r, dist))
        break;
    }
  return r;
}



/**
 * Creates a new histogram distribution.
 *
 * @param histo a histogram.  This function copies the histogram, so the
 *   original may be freed or modified afterward.
 * @return a pointer to a newly-created PDF_dist_t structure, or NULL if there
 *   wasn't enough memory to allocate one.
 */
PDF_dist_t *
PDF_new_histogram_dist (gsl_histogram * histo)
{
  PDF_dist_t *dist;
  PDF_histogram_dist_t *t;      /* part specific to this distribution */
  gsl_histogram_pdf *pdf;

#if DEBUG
  g_debug ("----- ENTER PDF_new_histogram_dist");
#endif

  dist = g_new (PDF_dist_t, 1);
  dist->type = PDF_Histogram;
  dist->has_inf_lower_tail = dist->has_inf_upper_tail = FALSE;
  dist->discrete = TRUE;
  t = &(dist->u.histogram);
  t->histo = gsl_histogram_clone (histo);
  g_assert (t->histo != NULL);

  /* Scale the histogram so that its bin values sum to 1. */
  gsl_histogram_scale (t->histo, 1.0 / gsl_histogram_sum (histo));

  /* Allocate a GSL histogram probability distribution struct, which comes with
   * a sampling function. */
  pdf = gsl_histogram_pdf_alloc (gsl_histogram_bins (histo));
  g_assert (pdf != NULL);
  gsl_histogram_pdf_init (pdf, histo);

  t->pdf = pdf;
  t->first_x = gsl_histogram_min (histo);
  t->last_x = gsl_histogram_max (histo);

#if DEBUG
  g_debug ("----- EXIT PDF_new_histogram_dist");
#endif

  return dist;
}



/**
 * Deletes the dynamically-allocated parts of a histogram distribution from
 * memory.
 *
 * @param dist a histogram distribution.
 */
void
PDF_free_histogram_dist (PDF_histogram_dist_t * dist)
{
  gsl_histogram_pdf_free (dist->pdf);
  gsl_histogram_free (dist->histo);
}



/**
 * Returns a text representation of a histogram distribution.
 *
 * @param dist a histogram distribution.
 * @return a string.
 */
char *
PDF_histogram_dist_to_string (PDF_histogram_dist_t * dist)
{
  GString *s;
  size_t bins;
  double lower, upper;
  int i;                        /* loop counter */
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<histogram probability distribution\n %lu bins",
                    (unsigned long) gsl_histogram_bins (dist->histo));
  bins = gsl_histogram_bins (dist->histo);
  for (i = 0; i < bins; i++)
    {
      gsl_histogram_get_range (dist->histo, i, &lower, &upper);
      g_string_sprintfa (s, "\n bin #%i [%g,%g) %g", i, lower, upper,
                         gsl_histogram_get (dist->histo, i));
    }
  g_string_append_c (s, '>');
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Computes the probability density p(x) at x for a histogram distribution.
 *
 * @param x
 * @param dist a histogram distribution.
 */
double
histogram_pdf (double x, PDF_histogram_dist_t * dist)
{
  size_t i;

  if (x < dist->first_x || x >= dist->last_x)
    return 0.0;

  gsl_histogram_find (dist->histo, x, &i);
  return gsl_histogram_get (dist->histo, i);
}



/**
 * Computes the cumulative area <= \a x for a histogram distribution.
 *
 * @param x
 * @param dist a histogram distribution.
 */
double
histogram_cdf (double x, PDF_histogram_dist_t * dist)
{
  size_t bin;
  double lower, upper;
  double frac;
  double area;

  if (x < dist->first_x)
    area = 0.0;
  else if (x >= dist->last_x)
    area = 1.0;
  else
    {
      gsl_histogram_find (dist->histo, x, &bin);
      gsl_histogram_get_range (dist->histo, bin, &lower, &upper);
      frac = (x - lower) / (upper - lower);
      area = dist->pdf->sum[bin] + frac * (dist->pdf->sum[bin + 1] - dist->pdf->sum[bin]);
    }
  return area;
}



/**
 * The inverse cumulative distribution function for a histogram distribution.
 *
 * @param area 0 <= \a area <= 1.
 * @param dist a histogram distribution.
 * @return the value at which the cumulative distribution function = \a area.
 */
double
histogram_inverse_cdf (double area, PDF_histogram_dist_t * dist)
{
  unsigned int seg;             /* the segment in which area lies */
  unsigned int lo, hi;          /* for a binary search */
  double x, y;
  double lower, upper;

  if (area <= 0.0)
    return dist->first_x;
  if (area >= 1.0)
    return dist->last_x;

  /* Find the segment in which area lies (binary search). */
  lo = 0;
  hi = gsl_histogram_bins (dist->histo);
  while (hi - lo > 1)
    {
      seg = (lo + hi) / 2;
      if (area >= dist->pdf->sum[seg])
        lo = seg;
      else
        hi = seg;
    }
#if DEBUG
  g_debug ("area (%g) is in bin %u", area, lo);
#endif

  area -= dist->pdf->sum[lo];
  y = gsl_histogram_get (dist->histo, lo);
  x = area / y;
  gsl_histogram_get_range (dist->histo, lo, &lower, &upper);
  return x + lower;
}



/**
 * Returns a random variate from a histogram distribution.
 *
 * @param dist a histogram distribution.
 * @param rng a random number generator.
 */
double
ran_histogram (PDF_histogram_dist_t * dist, RAN_gen_t * rng)
{
  return gsl_histogram_pdf_sample (dist->pdf, RAN_num (rng));
}



/**
 * Creates a new Gaussian distribution with parameters as illustrated below.
 *
 * @image html gaussian.png
 *
 * @param mu the mean.
 * @param sigma the standard deviation.
 * @return a pointer to a newly-created PDF_dist_t structure.
 */
PDF_dist_t *
PDF_new_gaussian_dist (double mu, double sigma)
{
  PDF_dist_t *dist;
  PDF_gaussian_dist_t *t;       /* part specific to this distribution */

#if DEBUG
  g_debug ("----- ENTER PDF_new_gaussian_dist");
#endif

  dist = g_new (PDF_dist_t, 1);
  dist->type = PDF_Gaussian;
  dist->has_inf_lower_tail = dist->has_inf_upper_tail = TRUE;
  dist->discrete = FALSE;
  t = &(dist->u.gaussian);
  t->mu = mu;
  t->sigma = sigma;

#if DEBUG
  g_debug ("----- EXIT PDF_new_gaussian_dist");
#endif

  return dist;
}



/**
 * Returns a text representation of a Gaussian distribution.
 *
 * @param dist a Gaussian distribution.
 * @return a string.
 */
char *
PDF_gaussian_dist_to_string (PDF_gaussian_dist_t * dist)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s,
                    "<Gaussian probability distribution\n mean=%.2g, std dev=%.2g>",
                    dist->mu, dist->sigma);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new inverse Gaussian distribution with parameters as illustrated
 * below.
 *
 * @image html inverse_gaussian.png
 *
 * @param mu the mean.
 * @param lambda the shape parameter, equal to mu^3/variance.
 * @return a pointer to a newly-created PDF_dist_t structure.
 */
PDF_dist_t *
PDF_new_inverse_gaussian_dist (double mu, double lambda)
{
  PDF_dist_t *dist;
  PDF_inverse_gaussian_dist_t *t;       /* part specific to this distribution */

#if DEBUG
  g_debug ("----- ENTER PDF_new_inverse_gaussian_dist");
#endif

  dist = g_new (PDF_dist_t, 1);
  dist->type = PDF_Inverse_Gaussian;
  dist->has_inf_lower_tail = FALSE;
  dist->has_inf_upper_tail = TRUE;
  dist->discrete = FALSE;
  t = &(dist->u.inverse_gaussian);
  t->mu = mu;
  t->lambda = lambda;

#if DEBUG
  g_debug ("----- EXIT PDF_new_inverse_gaussian_dist");
#endif

  return dist;
}



/**
 * Returns a text representation of an inverse Gaussian distribution.
 *
 * @param dist an inverse Gaussian distribution.
 * @return a string.
 */
char *
PDF_inverse_gaussian_dist_to_string (PDF_inverse_gaussian_dist_t * dist)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s,
                    "<inverse Gaussian probability distribution\n mu=%.2g, lambda=%.2g>",
                    dist->mu, dist->lambda);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Computes the probability density p(x) at x for an inverse Gaussian
 * distribution.
 *
 * @param x
 * @param dist an inverse Gaussian distribution.
 */
double
inverse_gaussian_pdf (double x, PDF_inverse_gaussian_dist_t * dist)
{
  if (x <= 0.0)
    return 0.0;

  return (sqrt (dist->lambda / (2.0 * M_PI * gsl_pow_3 (x))) *
          exp (- ((dist->lambda * gsl_pow_2 (x - dist->mu)) /
                  (2.0 * gsl_pow_2 (dist->mu) * x))));
}



/**
 * Computes the cumulative area <= \a x for an inverse Gaussian distribution.
 *
 * @param x
 * @param dist an inverse Gaussian distribution.
 * @return the area under the distribution curve to the left of \a x.
 */
double
inverse_gaussian_cdf (double x, PDF_inverse_gaussian_dist_t * dist)
{
#define AS_PHI(_x) gsl_cdf_ugaussian_P (_x)
  if (x <= 0.0)
    return 0.0;

  return ((AS_PHI (sqrt (dist->lambda / x) *
                   ((x / dist->mu) - 1.0))) +
          (exp (2.0 * dist->lambda / dist->mu) *
           AS_PHI (-sqrt (dist->lambda / x) *
                   ((x / dist->mu) + 1.0))));
#undef AS_PHI
}



/**
 * The inverse cumulative distribution function for an inverse Gaussian
 * distribution.  It finds the answer iteratively using the bisection method.
 *
 * @param area 0 <= \a area <= 1.
 * @param dist an inverse Gaussian distribution.
 * @return the value at which the cumulative distribution function = \a area.
 */
double
inverse_gaussian_inverse_cdf (double area, PDF_inverse_gaussian_dist_t * dist)
{
  int iter;
  double x_lo, x_hi, x, a;
  gboolean hibound_found;

  /* Eliminate compiler warnings about uninitialized values */
  x_hi = NAN;

  if (area == 0)
    return 0;

  x_lo = 0;
  x = dist->mu;   /* starting guess = mean */
  hibound_found = FALSE;
  iter = 0;
  do
    {
      iter++;
      a = inverse_gaussian_cdf (x, dist);
      if (fabs (a - area) < EPSILON)
        {
          /* We've found a good approximation to the answer. */
          break;
        }
      if (a < area)
        {
          /* We're to the left of the proper x.  Move x to the right. */
          x_lo = x;
          if (hibound_found)
            x = x_lo + (x_hi - x_lo) / 2;
          else
            x = 2 * x;
        }
      else
        {
          /* We're to the right of the proper x.  Move x to the left. */
          if (!hibound_found)
            hibound_found = TRUE;
          x_hi = x;
          x = x_lo + (x_hi - x_lo) / 2;
        }
    }
  while (iter < MAX_BISECTION_ITER);

  return x;
}


#ifdef WIN_DLL
/**
 * Computes the probability density p(x) at x for an inverse Gaussian
 * distribution.  This form of the function is primarily intended to
 * be called from a library.
 *
 * @param x
 * @param mu the mean used to define an inverse Gaussian distribution.
 * @param lambda the mu^3/variance.
 * @return the probability density p(x)
 */
DLL_API double
aphi_inverse_gaussian_pdf (double x, double mu, double lambda)
{
  PDF_dist_t *dist;
  double result;

  dist = PDF_new_inverse_gaussian_dist (mu, lambda);
  result = inverse_gaussian_pdf (x, &(dist->u.inverse_gaussian));
  PDF_free_dist (dist);
  return result;
}



/**
 * Computes the cumulative area <= \a x for an inverse Gaussian
 * distribution.  This form of the function is primarily intended to
 * be called from a library.
 *
 * @param x
 * @param mu the mean used to define an inverse Gaussian distribution.
 * @param lambda mu^3/variance
 * @return the cumulative area <= \a x
 */
DLL_API double
aphi_inverse_gaussian_cdf (double x, double mu, double lambda)
{
  PDF_dist_t *dist;
  double result;

  dist = PDF_new_inverse_gaussian_dist (mu, lambda);
  result = inverse_gaussian_cdf (x, &(dist->u.inverse_gaussian));
  PDF_free_dist (dist);
  return result;
}



/**
 * The inverse cumulative distribution function for an inverse
 * Gaussian distribution.  This form of the function is primarily
 * intended to be called from a library.
 *
 * @param area 0 <= \a area <= 1.
 * @param mu the mean used to define an inverse Gaussian distribution.
 * @param lambda mu^3/variance
 * @return the value at which the cumulative distribution function = \a area.
 */
DLL_API double
aphi_inverse_gaussian_inverse_cdf (double area, double mu, double lambda)
{
  PDF_dist_t *dist;
  double result;

  dist = PDF_new_inverse_gaussian_dist (mu, lambda);
  result = inverse_gaussian_inverse_cdf (area, &(dist->u.inverse_gaussian));
  PDF_free_dist (dist);
  return result;
}
#endif


/**
 * Returns a random variate from an inverse Gaussian distribution.
 * Algorithm is from Devroye, L.  1986.  Non-Uniform Random Variate
 * Generation. New York: Springer-Verlag. 
 * See http://cg.scs.carleton.ca/~luc/rnbookindex.html
 *
 * @param dist an inverse Gaussian distribution.
 * @param rng a random number generator.
 */
double
ran_inverse_gaussian (PDF_inverse_gaussian_dist_t * dist, RAN_gen_t * rng)
{
  double v = gsl_ran_gaussian (RAN_generator_as_gsl (rng), 1.0 /* sigma */);
  double y = gsl_pow_2 (v);
  double x = (dist->mu +
              ((gsl_pow_2 (dist->mu) * y) / (2.0 * dist->lambda)) -
              ((dist->mu / (2.0 * dist->lambda)) *
               sqrt (4.0 * dist->mu * dist->lambda * y +
                     gsl_pow_2 (dist->mu) * gsl_pow_2 (y))));
  double z = gsl_rng_uniform (RAN_generator_as_gsl (rng));

  if (z <= ((dist->mu) / (dist->mu + x)))
    return x;
  else
    return (gsl_pow_2(dist->mu) / x);
}



/**
 * Creates a new Poisson distribution with parameters as illustrated below.
 *
 * @image html poisson.png
 *
 * @param mu the mean.
 * @return a pointer to a newly-created PDF_dist_t structure.
 */
PDF_dist_t *
PDF_new_poisson_dist (double mu)
{
  PDF_dist_t *dist;
  PDF_poisson_dist_t *t;        /* part specific to this distribution */

#if DEBUG
  g_debug ("----- ENTER PDF_new_poisson_dist");
#endif

  dist = g_new (PDF_dist_t, 1);
  dist->type = PDF_Poisson;
  dist->has_inf_lower_tail = FALSE;
  dist->has_inf_upper_tail = TRUE;
  dist->discrete = TRUE;
  t = &(dist->u.poisson);
  t->mu = mu;

#if DEBUG
  g_debug ("----- EXIT PDF_new_poisson_dist");
#endif

  return dist;
}



/**
 * Returns a text representation of a Poisson distribution.
 *
 * @param dist a Poisson distribution.
 * @return a string.
 */
char *
PDF_poisson_dist_to_string (PDF_poisson_dist_t * dist)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<Poisson probability distribution\n mean=%.2g>", dist->mu);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Computes the cumulative area <= \a x for a Poisson distribution.  From
 * Bowerman, Nolty, and Scheuer, "Calculation of the Poisson Cumulative
 * Distribution Function", IEEE Transactions on Reliability, vol. 32 no. 2,
 * June 1990.
 *
 * @param x
 * @param dist a Poisson distribution.
 * @return the area under the distribution curve to the left of \a x.
 */
double
poisson_cdf (double x, PDF_poisson_dist_t * dist)
{
  double BRK_POINT = 1, ADJ_FACTOR = 350.0;
  long n = (long) x, i, num_of_adjusts;
  double mu, cumprob, sum, old_factor;

  if (x < 0)
    return 0;

  num_of_adjusts = 0;
  sum = old_factor = 1.0;
  mu = dist->mu;

  for (i = 1; i <= n; i++)
    {
      old_factor = mu / i * old_factor;
      sum = sum + old_factor;
      if (sum > BRK_POINT)
        {
          old_factor = old_factor / exp (ADJ_FACTOR);
          sum = sum / exp (ADJ_FACTOR);
          num_of_adjusts++;
        }
    }

  cumprob = exp (num_of_adjusts * ADJ_FACTOR - mu) * sum;

  return cumprob;
}


#ifdef WIN_DLL
/**
 * Computes the probability density p(x) at x for a Poisson distribution.
 * This form of the function is primarily intended to be called from a
 * library.
 *
 * @param x
 * @param mean the mean used to define a Poisson distribution.
 * @return the probability density p(x)
 */
DLL_API double
aphi_poisson_pdf( double x, double mean )
{
  return gsl_ran_poisson_pdf ((unsigned int) x, mean);
}



/**
 * Computes the cumulative area <= \a x for a Poisson distribution.
 * This form of the function is primarily intended to be called from a
 * library.
 *
 * @param x
 * @param mean the mean used to define a Poisson distribution.
 * @return the cumulative area <= \a x
 */
DLL_API double
aphi_poisson_cdf( double x, double mean )
{
  PDF_dist_t *dist;
  double result;

  dist = PDF_new_poisson_dist (mean);
  result = poisson_cdf (x, &(dist->u.poisson));
  PDF_free_dist (dist);
  return result;
}
#endif


/**
 * Creates a new beta distribution with parameters as illustrated below.
 *
 * @image html beta.png
 *
 * @param alpha the alpha parameter.
 * @param beta the beta parameter.
 * @param location how many units left (-) or right (+) to shift the
 *   distribution.
 * @param scale the upper bound of the distribution.
 * @return a pointer to a newly-created PDF_dist_t structure.
 */
PDF_dist_t *
PDF_new_beta_dist (double alpha, double beta, double location, double scale)
{
  PDF_dist_t *dist;
  PDF_beta_dist_t *t;           /* part specific to this distribution */

#if DEBUG
  g_debug ("----- ENTER PDF_new_beta_dist");
#endif

  dist = g_new (PDF_dist_t, 1);
  dist->type = PDF_Beta;
  dist->has_inf_lower_tail = dist->has_inf_upper_tail = FALSE;
  dist->discrete = FALSE;
  t = &(dist->u.beta);
  t->alpha = alpha;
  t->beta = beta;
  t->location = location;
  t->scale = scale;
  t->width = scale - location;

#if DEBUG
  g_debug ("----- EXIT PDF_new_beta_dist");
#endif

  return dist;
}



/**
 * Creates a new beta distribution with parameters estimated from a minimum,
 * maximum, and mode.
 *
 * The formulas used to estimate the alpha and beta parameters are:
 * \f[d = \frac{min + 4 \times mode + max}{6}\f]
 * \f[\alpha = [ 6 \left[ \frac{d-min}{max-min} \right] \f]
 * \f[\beta = [ 6 \left[ \frac{max-d}{max-min} \right] \f]
 *
 *
 * These calculations follow A Concise Summary of @@RISK Probability
 * Distribution Functions (2002, Palisade Corporation).
 *
 * @image html betapert.png
 *
 * @param min the minimum.
 * @param mode the mode.
 * @param max the maximum.
 * @return a pointer to a newly-created PDF_dist_t structure.
 */
PDF_dist_t *
PDF_new_beta_pert_dist (double min, double mode, double max)
{
  PDF_dist_t *dist;
  PDF_beta_dist_t *t;           /* part specific to this distribution */
  double d, v;

#if DEBUG
  g_debug ("----- ENTER PDF_new_beta_pert_dist");
#endif

  dist = g_new (PDF_dist_t, 1);
  dist->type = PDF_Beta;
  dist->has_inf_lower_tail = dist->has_inf_upper_tail = FALSE;
  dist->discrete = FALSE;
  t = &(dist->u.beta);
  d = (min + 4 * mode + max) / 6;
  v = (max - min) * (max - min) / 36;

  /* These calculations follow the @RISK documentation */
  t->alpha = 6 * ((d - min) / (max - min));
  t->beta = 6 * ((max - d) / (max - min));

  /*
     These calculations follow an online course reader by R.E. Davis at
     http://www.cob.sjsu.edu/facstaff/davis_r/courses/QBAreader/QBAtoc.html
     
     \f[d = \frac{min + 4 \times mode + max}{6}\f]
     \f[\sigma^2 = \frac{(max-min)^2}{36} \f]
     \f[
       \alpha = \left( \frac{d-min}{max-min} \right)
         \left[ \frac{(d-min)(max-d)}{\sigma^2} - 1 \right]
     \f]
     \f[
       \beta = \left( \frac{max-d}{d-min} \right) \alpha
     \f]

     t->alpha = (d - min) / (max - min) * ((d - min) * (max - d) / v - 1);
     t->beta = (max - d) / (d - min) * t->alpha;
   */
  t->location = min;
  t->scale = max;
  t->width = max - min;

#if DEBUG
  g_debug ("----- EXIT PDF_new_beta_pert_dist");
#endif

  return dist;
}



/**
 * Returns a text representation of a beta distribution.
 *
 * @param dist a beta distribution.
 * @return a string.
 */
char *
PDF_beta_dist_to_string (PDF_beta_dist_t * dist)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s,
                    "<beta probability distribution\n alpha=%.3g beta=%.3g\n location=%.2g scale=%.2g>",
                    dist->alpha, dist->beta, dist->location, dist->scale);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Computes the cumulative area <= \a x for a beta distribution.
 *
 * @param x
 * @param dist a beta distribution.
 */
double
beta_cdf (double x, PDF_beta_dist_t * dist)
{
  double result;

  result = (x < dist->location) ? 0 :
    gsl_cdf_beta_P ((x - dist->location) / dist->width, dist->alpha, dist->beta);
  return result;
}



/**
 * The inverse cumulative distribution function for a beta distribution.  It
 * finds the answer iteratively using the bisection method.
 *
 * @param area 0 <= \a area <= 1.
 * @param dist a beta distribution.
 * @return the value at which the cumulative distribution function = \a area.
 */
double
beta_inverse_cdf (double area, PDF_beta_dist_t * dist)
{
  int iter;
  double x_lo, x_hi, x, a;

  if (area == 0)
    return dist->location;

  x_lo = dist->location;
  x_hi = dist->scale;
  x = (x_hi - x_lo) / 2;        /* starting guess */
  iter = 0;
  do
    {
      iter++;
      a = beta_cdf (x, dist);
      if (fabs (a - area) < EPSILON)
        {
          /* We've found a good approximation to the answer. */
          break;
        }
      if (a < area)
        {
          /* We're to the left of the proper x.  Move x to the right. */
          x_lo = x;
          x = x_lo + (x_hi - x_lo) / 2;
        }
      else
        {
          /* We're to the right of the proper x.  Move x to the left. */
          x_hi = x;
          x = x_lo + (x_hi - x_lo) / 2;
        }
    }
  while (iter < MAX_BISECTION_ITER);

  return x;
}


#ifdef WIN_DLL
/**
 * Computes the probability density p(x) at x for a beta distribution.
 * This form of the function is primarily intended to be called from a
 * library.
 *
 * @param x
 * @param alpha parameter used to define a beta PDF.
 * @param beta parameter used to define a beta PDF.
 * @param location the minimum value used to define a beta PDF.
 * @param scale the maximum value used to define a beta PDF.
 * @return the probability density p(x)
 */
DLL_API double
aphi_beta_pdf( double x, double alpha, double beta, double location, double scale ) 
{
  PDF_dist_t *dist;
  double result;
  
  if( x <= location )
    result = 0.0;
  else if( x >= scale )
    result = 0.0;
  else
    {
      dist = PDF_new_beta_dist (alpha, beta, location, scale);
    
      /* This returns the probability density for the "unit" beta, with width = 1 */
      result =
        gsl_ran_beta_pdf ((x - dist->u.beta.location) / dist->u.beta.width, dist->u.beta.alpha,
                          dist->u.beta.beta);
    
      /* For non-unit beta functions, this correction is necessary */
      result = result / dist->u.beta.width;
    }

  return result;
}



/**
 * Computes the cumulative area <= \a x for a beta distribution.
 * This form of the function is primarily intended to be called from a
 * library.
 *
 * @param x
 * @param alpha parameter used to define a beta PDF.
 * @param beta parameter used to define a beta PDF.
 * @param location the minimum value used to define a beta PDF.
 * @param scale the maximum value used to define a beta PDF.
 * @return the cumulative area <= \a x
 */
DLL_API double
aphi_beta_cdf( double x, double alpha, double beta, double location, double scale )
{
  PDF_dist_t *dist;
  double result;

  dist = PDF_new_beta_dist (alpha, beta, location, scale);
  result = beta_cdf (x, &(dist->u.beta));
  PDF_free_dist (dist);

  return result;
}


/**
 * The inverse cumulative distribution function for a beta distribution.
 * This form of the function is primarily intended to be called from a
 * library.
 *
 * @param area 0 <= \a area <= 1.
 * @param alpha1 parameter used to define a beta PDF.
 * @param alpha2 parameter used to define a beta PDF.
 * @param min the minimum value used to define a beta PDF.
 * @param max the maximum value used to define a beta PDF.
 * @return the value at which the cumulative distribution function = \a area.
 */
DLL_API double
aphi_beta_inverse_cdf( double area, double alpha1, double alpha2, double min, double max )
{
  PDF_dist_t *dist;
  double result;

  dist = PDF_new_beta_dist (alpha1, alpha2, min, max);
  result = beta_inverse_cdf (area, &(dist->u.beta));
  PDF_free_dist (dist);
  return result;
}


/**
 * Generates random variates from a beta distribution.
 * This form of the function is primarily intended to be called from a 
 * library.
 *
 * @param rng a Delphi-compatible pointer to the random number generator.
 * @param alpha parameter used to define a beta PDF.
 * @param beta parameter used to define a beta PDF.
 * @param location the minimum value used to define a beta PDF.
 * @param scale the maximum value used to define a beta PDF.
 * @return a random variate from the specified distribution.
 */
DLL_API double 
aphi_beta_rand( int unsigned rng, double alpha1, double alpha2, double min, double max )
{
  PDF_dist_t* dist;
  double result;

  dist = PDF_new_beta_dist ( alpha1, alpha2, min, max );
  result = PDF_random( dist, (RAN_gen_t*)rng );
  PDF_free_dist( dist );
  return result;
}


/**
 * Computes the probability density p(x) at x for a betaPERT distribution.
 * This form of the function is primarily intended to be called from a
 * library.
 *
 * @param x
 * @param min the minimum value used to define a betaPERT PDF.
 * @param mode the mode used to define a betaPERT PDF.
 * @param max the maximum value used to define a betaPERT PDF.
 * @return the probability density p(x)
 */
DLL_API double
aphi_beta_pert_pdf( double x, double min, double mode, double max )
{
  PDF_dist_t *dist;
  double result;

  if( x <= min )
    result = 0.0;
  else if( x >= max )
    result = 0.0;
  else
    {
      dist = PDF_new_beta_pert_dist (min, mode, max);
      result = aphi_beta_pdf( x, dist->u.beta.alpha, dist->u.beta.beta, dist->u.beta.location, dist->u.beta.scale );
      PDF_free_dist (dist);
    }
  return result;
}


/**
 * Computes the cumulative area <= \a x for a betaPERT distribution.
 * This form of the function is primarily intended to be called from a
 * library.
 *
 * @param x
 * @param min the minimum value used to define a betaPERT PDF.
 * @param mode the mode used to define a betaPERT PDF.
 * @param max the maximum value used to define a betaPERT PDF.
 * @return the cumulative area <= \a x
 */
DLL_API double
aphi_beta_pert_cdf( double x, double min, double mode, double max )
{
  PDF_dist_t *dist;
  double result;

  dist = PDF_new_beta_pert_dist (min, mode, max);
  result = beta_cdf (x, &(dist->u.beta));
  PDF_free_dist (dist);
  return result;
}



/**
 * The inverse cumulative distribution function for a betaPERT distribution.
 * This form of the function is primarily intended to be called from a
 * library.
 *
 * @param area 0 <= \a area <= 1.
 * @param min the minimum value used to define a betaPERT PDF.
 * @param mode the mode used to define a betaPERT PDF.
 * @param max the maximum value used to define a betaPERT PDF.
 * @return the value at which the cumulative distribution function = \a area.
 */
DLL_API double
aphi_beta_pert_inverse_cdf( double area, double min, double mode, double max )
{
  PDF_dist_t *dist;
  double result;

  dist = PDF_new_beta_pert_dist (min, mode, max);
  result = beta_inverse_cdf (area, &(dist->u.beta));
  PDF_free_dist (dist);
  return result;
}


/**
 * Generates random variates from a betaPERT distribution.
 * This form of the function is primarily intended to be called from a 
 * library.
 *
 * @param rng a Delphi-compatible pointer to the random number generator.
 * @param min the minimum value used to define a betaPERT PDF.
 * @param mode the mode used to define a betaPERT PDF.
 * @param max the maximum value used to define a betaPERT PDF.
 * @return a random variate from the specified distribution.
 */
DLL_API double 
aphi_beta_pert_rand( int unsigned rng, double min, double mode, double max )
{
  PDF_dist_t* dist;
  double result;

  dist = PDF_new_beta_pert_dist( min, mode, max );
  result = PDF_random( dist, (RAN_gen_t*)rng );
  PDF_free_dist( dist );
  return result;
}

#endif

/**
 * Creates a new gamma distribution with parameters as illustrated below.
 *
 * @image html gamma.png
 *
 * @param alpha the alpha parameter.
 * @param beta the beta parameter.
 * @return a pointer to a newly-created PDF_dist_t structure.
 */
PDF_dist_t *
PDF_new_gamma_dist (double alpha, double beta)
{
  PDF_dist_t *dist;
  PDF_gamma_dist_t *t;          /* part specific to this distribution */

#if DEBUG
  g_debug ("----- ENTER PDF_new_gamma_dist");
#endif

  dist = g_new (PDF_dist_t, 1);
  dist->type = PDF_Gamma;
  dist->has_inf_lower_tail = FALSE;
  dist->has_inf_upper_tail = TRUE;
  dist->discrete = FALSE;
  t = &(dist->u.gamma);
  t->alpha = alpha;
  t->beta = beta;

#if DEBUG
  g_debug ("----- EXIT PDF_new_gamma_dist");
#endif

  return dist;
}



/**
 * Returns a text representation of a gamma distribution.
 *
 * @param dist a gamma distribution.
 * @return a string.
 */
char *
PDF_gamma_dist_to_string (PDF_gamma_dist_t * dist)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s,
                    "<gamma probability distribution\n alpha=%.3g beta=%.3g>",
                    dist->alpha, dist->beta);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new Weibull distribution with parameters as illustrated below.
 *
 * @image html weibull.png
 *
 * @param alpha the exponent parameter.
 * @param beta the scale parameter.
 * @return a pointer to a newly-created PDF_dist_t structure.
 */
PDF_dist_t *
PDF_new_weibull_dist (double alpha, double beta)
{
  PDF_dist_t *dist;
  PDF_weibull_dist_t *t;        /* part specific to this distribution */

#if DEBUG
  g_debug ("----- ENTER PDF_new_weibull_dist");
#endif

  dist = g_new (PDF_dist_t, 1);
  dist->type = PDF_Weibull;
  dist->has_inf_lower_tail = FALSE;
  dist->has_inf_upper_tail = TRUE;
  dist->discrete = FALSE;
  t = &(dist->u.weibull);
  t->alpha = alpha;
  t->beta = beta;

#if DEBUG
  g_debug ("----- EXIT PDF_new_weibull_dist");
#endif

  return dist;
}



/**
 * Returns a text representation of a Weibull distribution.
 *
 * @param dist a Weibull distribution.
 * @return a string.
 */
char *
PDF_weibull_dist_to_string (PDF_weibull_dist_t * dist)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s,
                    "<Weibull probability distribution\n alpha=%.2g beta=%.2g>",
                    dist->alpha, dist->beta);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new exponential distribution with parameters as illustrated below.
 *
 * @image html exponential.png
 *
 * @param mean the mean.
 * @return a pointer to a newly-created PDF_dist_t structure.
 */
PDF_dist_t *
PDF_new_exponential_dist (double mean)
{
  PDF_dist_t *dist;
  PDF_exponential_dist_t *t;    /* part specific to this distribution */

#if DEBUG
  g_debug ("----- ENTER PDF_new_exponential_dist");
#endif

  dist = g_new (PDF_dist_t, 1);
  dist->type = PDF_Exponential;
  dist->has_inf_lower_tail = FALSE;
  dist->has_inf_upper_tail = TRUE;
  dist->discrete = FALSE;
  t = &(dist->u.exponential);
  t->mean = mean;

#if DEBUG
  g_debug ("----- EXIT PDF_new_exponential_dist");
#endif

  return dist;
}



/**
 * Returns a text representation of an exponential distribution.
 *
 * @param dist an exponential distribution.
 * @return a string.
 */
char *
PDF_exponential_dist_to_string (PDF_exponential_dist_t * dist)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<exponential probability distribution\n mean=%.2g>", dist->mean);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new Pearson Type V distribution with parameters as illustrated
 * below.
 *
 * @image html pearson.png
 *
 * @param alpha the alpha parameter.
 * @param beta the beta parameter.
 * @return a pointer to a newly-created PDF_dist_t structure.
 */
PDF_dist_t *
PDF_new_pearson5_dist (double alpha, double beta)
{
  PDF_dist_t *dist;
  PDF_pearson5_dist_t *t;       /* part specific to this distribution */

#if DEBUG
  g_debug ("----- ENTER PDF_new_pearson5_dist");
#endif

  dist = g_new (PDF_dist_t, 1);
  dist->type = PDF_Pearson5;
  dist->has_inf_lower_tail = FALSE;
  dist->has_inf_upper_tail = TRUE;
  dist->discrete = FALSE;
  t = &(dist->u.pearson5);
  t->alpha = alpha;
  t->beta = beta;
  t->one_over_beta = 1.0 / beta;
  t->loggamma_alpha = gsl_sf_lngamma (alpha);

#if DEBUG
  g_debug ("----- EXIT PDF_new_pearson5_dist");
#endif

  return dist;
}



/**
 * Returns a text representation of a Pearson Type V distribution.
 *
 * @param dist a Pearson Type V distribution.
 * @return a string.
 */
char *
PDF_pearson5_dist_to_string (PDF_pearson5_dist_t * dist)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s,
                    "<Pearson Type V probability distribution\n alpha=%.2g beta=%.2g>",
                    dist->alpha, dist->beta);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Computes the probability density p(x) at x for a Pearson Type V
 * distribution.
 *
 * @param x
 * @param dist a Pearson Type V distribution.
 */
double
pearson5_pdf (double x, PDF_pearson5_dist_t * dist)
{
  double a, b;

  if (x <= 0)
    return 0;

  a = dist->alpha;
  b = dist->beta;
  return exp (-b / x - dist->loggamma_alpha - (a + 1) * log (x / b)) / b;
}



/**
 * The function pearson5_pdf cast to a gsl_function.
 */
double
pearson5_pdf_as_gsl_function (double x, void *params)
{
  return pearson5_pdf (x, (PDF_pearson5_dist_t *) params);
}



/**
 * Computes the cumulative area <= \a x for a Pearson Type V distribution.
 * Uses numerical integration.
 *
 * @param x
 * @param dist a Pearson Type V distribution.
 */
double
pearson5_cdf (double x, PDF_pearson5_dist_t * dist)
{
  gsl_function f;
  double result;
  int err;
  double abserr;
  gsl_integration_workspace* iw;

  if (x <= 0)
    return 0;

  f.function = pearson5_pdf_as_gsl_function;
  f.params = (void *) dist;

  iw = gsl_integration_workspace_alloc (100); 
  /* Documentation from the GSL...
  int gsl_integration_qag (
    const gsl_function *f, double a, double b, 
    double epsabs, double epsrel, 
    size_t limit, int key, 
    gsl_integration_workspace * workspace, 
    double * result, double * abserr)
  */
  err = gsl_integration_qag (
    &f, 0, x, 
    EPSILON, 1, 
    100, GSL_INTEG_GAUSS15, 
    iw,
    &result, &abserr );
  gsl_integration_workspace_free (iw);
  
  return result;
}



/**
 * The inverse cumulative distribution function for a Pearson Type V
 * distribution.  It finds the answer iteratively using the bisection method.
 *
 * @param area 0 <= \a area <= 1.
 * @param dist a Pearson Type V distribution.
 * @return the value at which the cumulative distribution function = \a area.
 */
double
pearson5_inverse_cdf (double area, PDF_pearson5_dist_t * dist)
{
  int iter;
  double x_lo, x_hi, x, a;
  gboolean hibound_found;

  /* Eliminate compiler warnings about uninitialized values */
  x_hi = NAN;

  if (area == 0)
    return 0;

  x_lo = 0;
  x = dist->beta / (dist->alpha - 1);   /* starting guess = mean */
  hibound_found = FALSE;
  iter = 0;
  do
    {
      iter++;
      a = pearson5_cdf (x, dist);
      if (fabs (a - area) < EPSILON)
        {
          /* We've found a good approximation to the answer. */
          break;
        }
      if (a < area)
        {
          /* We're to the left of the proper x.  Move x to the right. */
          x_lo = x;
          if (hibound_found)
            x = x_lo + (x_hi - x_lo) / 2;
          else
            x = 2 * x;
        }
      else
        {
          /* We're to the right of the proper x.  Move x to the left. */
          if (!hibound_found)
            hibound_found = TRUE;
          x_hi = x;
          x = x_lo + (x_hi - x_lo) / 2;
        }
    }
  while (iter < MAX_BISECTION_ITER);

  return x;
}


#ifdef WIN_DLL
/**
 * Computes the probability density p(x) at x for a Pearson Type V
 * distribution.
 * This form of the function is primarily intended to be called from a
 * library.
 *
 * @param x
 * @param alpha the alpha parameter of the distribution.
 * @param beta the beta parameter of the distribution.
 * @return the probability density p(x)
 */
DLL_API double
aphi_pearson5_pdf( double x, double alpha, double beta )
{
  PDF_dist_t *dist;
  double result;

  dist = PDF_new_pearson5_dist (alpha, beta);
  result = pearson5_pdf (x, &(dist->u.pearson5));
  PDF_free_dist (dist);
  return result;
}



/**
 * Computes the cumulative area <= \a x for a Pearson Type V
 * distribution.
 * This form of the function is primarily intended to be called from a
 * library.
 *
 * @param x
 * @param alpha the alpha parameter of the distribution.
 * @param beta the beta parameter of the distribution.
 * @return the cumulative area <= \a x
 */
DLL_API double
aphi_pearson5_cdf( double x, double alpha, double beta )
{
  PDF_dist_t *dist;
  double result;

  dist = PDF_new_pearson5_dist (alpha, beta);
  result = pearson5_cdf (x, &(dist->u.pearson5));
  PDF_free_dist (dist);
  return result;
}



/**
 * The inverse cumulative distribution function for a Pearson Type V
 * distribution.
 * This form of the function is primarily intended to be called from a
 * library.
 *
 * @param area 0 <= \a area <= 1.
 * @param alpha the alpha parameter of the distribution.
 * @param beta the beta parameter of the distribution.
 * @return the value at which the cumulative distribution function = \a area.
 */
DLL_API double
aphi_pearson5_inverse_cdf( double area, double alpha, double beta )
{
  PDF_dist_t *dist;
  double result;

  dist = PDF_new_pearson5_dist (alpha, beta);
  result = pearson5_inverse_cdf (area, &(dist->u.pearson5));
  PDF_free_dist (dist);
  return result;
}


/**
 * Generates random variates from a Pearson Type V distribution.
 * This form of the function is primarily intended to be called from a 
 * library.
 *
 * @param rng a Delphi-compatible pointer to the random number generator.
 * @param alpha the alpha parameter of the distribution.
 * @param beta the beta parameter of the distribution.
 * @return a random variate from the specified distribution.
 */
DLL_API double 
aphi_pearson5_rand( int unsigned rng, double alpha, double beta )
{
  PDF_dist_t* dist;
  double result;

  dist = PDF_new_pearson5_dist ( alpha, beta );
  result = PDF_random( dist, (RAN_gen_t*)rng );
  PDF_free_dist( dist );
  return result;
}
#endif

/**
 * Creates a new logistic distribution with parameters as illustrated below.
 *
 * @image html logistic.png
 *
 * @param location the location parameter.
 * @param scale the scale parameter.
 * @return a pointer to a newly-created PDF_dist_t structure.
 */
PDF_dist_t *
PDF_new_logistic_dist (double location, double scale)
{
  PDF_dist_t *dist;
  PDF_logistic_dist_t *t;       /* part specific to this distribution */

#if DEBUG
  g_debug ("----- ENTER PDF_new_logistic_dist");
#endif

  dist = g_new (PDF_dist_t, 1);
  dist->type = PDF_Logistic;
  dist->has_inf_lower_tail = TRUE;
  dist->has_inf_upper_tail = TRUE;
  dist->discrete = FALSE;
  t = &(dist->u.logistic);
  t->location = location;
  t->scale = scale;

#if DEBUG
  g_debug ("----- EXIT PDF_new_logistic_dist");
#endif

  return dist;
}



/**
 * Returns a text representation of a logistic distribution.
 *
 * @param dist a logistic distribution.
 * @return a string.
 */
char *
PDF_logistic_dist_to_string (PDF_logistic_dist_t * dist)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s,
                    "<logistic probability distribution\n location=%.2g scale=%.2g>",
                    dist->location, dist->scale);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new loglogistic (a.k.a. Fisk) distribution with parameters as
 * illustrated below.
 *
 * @image html loglogistic.png
 *
 * @param location the location parameter.
 * @param scale the scale parameter.
 * @param shape the scale parameter.
 * @return a pointer to a newly-created PDF_dist_t structure.
 */
PDF_dist_t *
PDF_new_loglogistic_dist (double location, double scale, double shape)
{
  PDF_dist_t *dist;
  PDF_loglogistic_dist_t *t;    /* part specific to this distribution */

#if DEBUG
  g_debug ("----- ENTER PDF_new_loglogistic_dist");
#endif

  dist = g_new (PDF_dist_t, 1);
  dist->type = PDF_LogLogistic;
  dist->has_inf_lower_tail = FALSE;
  dist->has_inf_upper_tail = TRUE;
  dist->discrete = FALSE;
  t = &(dist->u.loglogistic);
  t->location = location;
  t->scale = scale;
  t->shape = shape;
  t->shape_over_scale = shape / scale;

#if DEBUG
  g_debug ("----- EXIT PDF_new_loglogistic_dist");
#endif

  return dist;
}



/**
 * Returns a text representation of a loglogistic distribution.
 *
 * @param dist a loglogistic distribution.
 * @return a string.
 */
char *
PDF_loglogistic_dist_to_string (PDF_loglogistic_dist_t * dist)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s,
                    "<loglogistic probability distribution\n location=%.2g scale=%.2g shape=%.2g>",
                    dist->location, dist->scale, dist->shape);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Computes the probability density p(x) at x for a loglogistic distribution.
 *
 * @param x
 * @param dist a loglogistic distribution.
 */
double
loglogistic_pdf (double x, PDF_loglogistic_dist_t * dist)
{
  double A, B, C, tmp1, tmp2;

  if (x <= dist->location)
    return 0;

  A = dist->location;
  B = dist->scale;
  C = dist->shape;

  tmp1 = (x - A) / B;
  tmp2 = 1 + pow (tmp1, C);

  return dist->shape_over_scale * pow (tmp1, C - 1) / (tmp2 * tmp2);
}



/**
 * Computes the cumulative area <= \a x for a loglogistic distribution.
 *
 * @param x
 * @param dist a loglogistic distribution.
 */
double
loglogistic_cdf (double x, PDF_loglogistic_dist_t * dist)
{
  double A, B, C;

  if (x <= dist->location)
    return 0;

  A = dist->location;
  B = dist->scale;
  C = dist->shape;

  return 1 / (1 + pow ((x - A) / B, -C));
}



/**
 * The inverse cumulative distribution function for a loglogistic distribution.
 *
 * @param area 0 <= \a area <= 1.
 * @param dist a loglogistic distribution.
 * @return the value at which the cumulative distribution function = \a area.
 */
double
loglogistic_inverse_cdf (double area, PDF_loglogistic_dist_t * dist)
{
  double A, B, C;

  A = dist->location;
  B = dist->scale;
  C = dist->shape;

  return B * pow (area / (1 - area), 1 / C) + A;
}



/**
 * Returns a random variate from a loglogistic distribution.
 *
 * @param dist a loglogistic distribution.
 * @param rng a random number generator.
 */
double
ran_loglogistic (PDF_loglogistic_dist_t * dist, RAN_gen_t * rng)
{
  double A, B, C, r;

  A = dist->location;
  B = dist->scale;
  C = dist->shape;

  r = RAN_num (rng);
  return A + B * pow (r / (1 - r), 1 / C);
}


#ifdef WIN_DLL
/**
 * Computes the probability density p(x) at x for a loglogistic distribution.
 * This form of the function is primarily intended to be called from a
 * library.
 *
 * @param x
 * @param location the location parameter of the distribution.
 * @param scale the scale parameter of the distribution.
 * @param shape the scale parameter of the distribution.
 * @return the probability density p(x)
 */
DLL_API double
aphi_loglogistic_pdf( double x, double location, double scale, double shape )
{
  PDF_dist_t *dist;
  double result;

  dist = PDF_new_loglogistic_dist (location, scale, shape);
  result = loglogistic_pdf (x, &(dist->u.loglogistic));
  PDF_free_dist (dist);
  return result;
}



/**
 * Computes the cumulative area <= \a x for a loglogistic distribution.
 * This form of the function is primarily intended to be called from a
 * library.
 *
 * @param x
 * @param location the location parameter of the distribution.
 * @param scale the scale parameter of the distribution.
 * @param shape the scale parameter of the distribution.
 * @return the cumulative area <= \a x
 */
DLL_API double
aphi_loglogistic_cdf( double x, double location, double scale, double shape )
{
  PDF_dist_t *dist;
  double result;

  dist = PDF_new_loglogistic_dist (location, scale, shape);
  result = loglogistic_cdf (x, &(dist->u.loglogistic));
  PDF_free_dist (dist);
  return result;
}



/**
 * The inverse cumulative distribution function for a loglogistic distribution.
 * This form of the function is primarily intended to be called from a
 * library.
 *
 * @param area 0 <= \a area <= 1.
 * @param location the location parameter of the distribution.
 * @param scale the scale parameter of the distribution.
 * @param shape the scale parameter of the distribution.
 * @return the value at which the cumulative distribution function = \a area.
 */
DLL_API double
aphi_loglogistic_inverse_cdf( double area, double location, double scale, double shape )
{
  PDF_dist_t *dist;
  double result;

  dist = PDF_new_loglogistic_dist (location, scale, shape);
  result = loglogistic_inverse_cdf (area, &(dist->u.loglogistic));
  PDF_free_dist (dist);
  return result;
}


/**
 * Generates random variates from a loglogistic distribution.
 * This form of the function is primarily intended to be called from a 
 * library.
 *
 * @param rng a Delphi-compatible pointer to the random number generator.
 * @param location the location parameter of the distribution.
 * @param scale the scale parameter of the distribution.
 * @param shape the scale parameter of the distribution.
 * @return a random variate from the specified distribution.
 */
DLL_API double 
aphi_loglogistic_rand( int unsigned rng, double location, double scale, double shape )
{
  PDF_dist_t* dist;
  double result;

  dist = PDF_new_loglogistic_dist ( location, scale, shape );
  result = PDF_random( dist, (RAN_gen_t*)rng );
  PDF_free_dist( dist );
  return result;
}
#endif

/**
 * Creates a new lognormal distribution with parameters as illustrated below.
 *
 * @image html lognormal.png
 *
 * @param zeta the zeta parameter.
 * @param sigma the sigma parameter.
 * @return a pointer to a newly-created PDF_dist_t structure.
 */
PDF_dist_t *
PDF_new_lognormal_dist (double zeta, double sigma)
{
  PDF_dist_t *dist;
  PDF_lognormal_dist_t *t;      /* part specific to this distribution */

#if DEBUG
  g_debug ("----- ENTER PDF_new_lognormal_dist");
#endif

  dist = g_new (PDF_dist_t, 1);
  dist->type = PDF_Lognormal;
  dist->has_inf_lower_tail = FALSE;
  dist->has_inf_upper_tail = TRUE;
  dist->discrete = FALSE;
  t = &(dist->u.lognormal);
  t->zeta = zeta;
  t->sigma = sigma;

#if DEBUG
  g_debug ("----- EXIT PDF_new_lognormal_dist");
#endif

  return dist;
}



/**
 * Returns a text representation of a lognormal distribution.
 *
 * @param dist a lognormal distribution.
 * @return a string.
 */
char *
PDF_lognormal_dist_to_string (PDF_lognormal_dist_t * dist)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s,
                    "<lognormal probability distribution\n zeta=%.2g sigma=%.2g>",
                    dist->zeta, dist->sigma);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new negative binomial distribution with parameters as illustrated
 * below.
 *
 * @image html negbinomial.png
 *
 * @param s the number of successes.
 * @param p the probability of a single success.  (The letters used for the
 *   parameters are the same ones used in \@RISK.)
 * @return a pointer to a newly-created PDF_dist_t structure.
 */
PDF_dist_t *
PDF_new_negative_binomial_dist (unsigned int s, double p)
{
  PDF_dist_t *dist;
  PDF_negative_binomial_dist_t *t;    /* part specific to this distribution */

#if DEBUG
  g_debug ("----- ENTER PDF_new_negative_binomial_dist");
#endif

  dist = g_new (PDF_dist_t, 1);
  dist->type = PDF_NegativeBinomial;
  dist->has_inf_lower_tail = FALSE;
  dist->has_inf_upper_tail = TRUE;
  dist->discrete = TRUE;
  t = &(dist->u.negative_binomial);
  t->s = (double) s;
  t->p = p;

#if DEBUG
  g_debug ("----- EXIT PDF_new_negative_binomial_dist");
#endif

  return dist;
}



/**
 * Returns a text representation of a negative binomial distribution.
 *
 * @param dist a negative binomial distribution.
 * @return a string.
 */
char *
PDF_negative_binomial_dist_to_string (PDF_negative_binomial_dist_t * dist)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<negative binomial probability distribution\n s=%g p=%.2g>",
                    dist->s, dist->p);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * The inverse cumulative distribution function for a negative binomial
 * distribution.  It finds the answer iteratively using the bisection method.
 * Note that this is a bit different from the other functions in this file that
 * use the bisection method: this is a discrete distribution, so we limit the
 * values to integers.
 *
 * @param area 0 <= \a area <= 1.
 * @param dist a negative binomial distribution.
 * @return the value at which the cumulative distribution function = \a area.
 */
double
negative_binomial_inverse_cdf (double area, PDF_negative_binomial_dist_t * dist)
{
  int iter;
  double s, p;
  double x_lo, x_hi, x, a, previous_x;
  gboolean hibound_found;

  /* Eliminate compiler warnings about uninitialized values */
  x_hi = NAN;

  if (area == 0)
    return 0;

  s = dist->s;
  p = dist->p;
  x_lo = 0;
  x = floor (s * (1 - p) / p);   /* starting guess = mean */
  hibound_found = FALSE;
  iter = 0;

  /* Initialize the "value of x on the previous iteration" variable.  The
   * particular value here (x+1) doesn't matter, it just has to be different
   * from the starting value of x so that it won't break the do loop on the
   * first iteration. */
  previous_x = x+1;

  do
    {
      iter++;
      a = gsl_cdf_negative_binomial_P (x, p, s);
      if (fabs (a - area) < EPSILON || fabs (x - previous_x) < EPSILON)
        {
          /* We've found a good approximation to the answer, or our answer
     * hasn't changed since the last iteration. */
          break;
        }
      if (a < area)
        {
          /* We're to the left of the proper x.  Move x to the right. */
          x_lo = x;
          if (hibound_found)
            x = floor (x_lo + (x_hi - x_lo) / 2);
          else
            x = 2 * x;
        }
      else
        {
          /* We're to the right of the proper x.  Move x to the left. */
          if (!hibound_found)
            hibound_found = TRUE;
          x_hi = x;
          x = floor (x_lo + (x_hi - x_lo) / 2);
        }
    }
  while (iter < MAX_BISECTION_ITER);

  return x;
}



/**
 * Creates a new Pareto distribution with parameters as illustrated below.
 * Note that the lines are straight on a log scale.
 *
 * @image html pareto.png
 * @image html pareto_log.png
 *
 * @param theta the shape parameter, called theta in \@RISK, <i>k</i> in
 *   Wikipedia, and <i>a</i> in the GSL.
 * @param a the location parameter, called <i>a</i> in \@RISK,
 *   <i>x<sub>m</sub></i> in Wikipedia, and <i>b</i> in the GSL.
 * @return a pointer to a newly-created PDF_dist_t structure.
 */
PDF_dist_t *
PDF_new_pareto_dist (double theta, double a)
{
  PDF_dist_t *dist;
  PDF_pareto_dist_t *t;    /* part specific to this distribution */

#if DEBUG
  g_debug ("----- ENTER PDF_new_pareto_dist");
#endif

  dist = g_new (PDF_dist_t, 1);
  dist->type = PDF_Pareto;
  dist->has_inf_lower_tail = FALSE;
  dist->has_inf_upper_tail = TRUE;
  dist->discrete = FALSE;
  t = &(dist->u.pareto);
  t->theta = theta;
  t->a = a;

#if DEBUG
  g_debug ("----- EXIT PDF_new_pareto_dist");
#endif

  return dist;
}



/**
 * Returns a text representation of a Pareto distribution.
 *
 * @param dist a pareto distribution.
 * @return a string.
 */
char *
PDF_pareto_dist_to_string (PDF_pareto_dist_t * dist)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s,
                    "<Pareto probability distribution\n theta=%.2g a=%.2g>",
                    dist->theta, dist->a);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}


/** Creates a new Bernoulli distribution with parameters as illustrated
 * below.
 *
 * @image html bernoulli.png
 *
 * @param p the probability of success of a single trial
 * @return a pointer to a newly created PDF_dist_t structure.
 */
PDF_dist_t*
PDF_new_bernoulli_dist (double p)
{
  PDF_dist_t *dist;
  PDF_bernoulli_dist_t *t;      /* part specific to this distribution */

#if DEBUG
  g_debug ("----- ENTER PDF_new_bernoulli_dist");
#endif

  dist = g_new (PDF_dist_t, 1);
  dist->type = PDF_Bernoulli;
  dist->has_inf_lower_tail = FALSE;
  dist->has_inf_upper_tail = FALSE;
  dist->discrete = TRUE;
  t = &(dist->u.bernoulli);
  t->p = p;

#if DEBUG
  g_debug ("----- EXIT PDF_new_bernoulli_dist");
#endif

  return dist;
}


/**
 * Returns a text representation of a Bernoulli distribution.
 *
 * @param dist a Bernoulli distribution.
 * @return a string.
 */
char *
PDF_bernoulli_dist_to_string (PDF_bernoulli_dist_t * dist)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<Bernoulli probability distribution\n p=%.2g>",
                    dist->p);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}

/**
 * Computes the cumulative area <= \a x for a Bernoulli distribution.
 *
 * @param x
 * @param dist a Bernoulli distribution.
 * @return the area under the distribution curve to the left of \a x.
 */
double
bernoulli_cdf (double x, PDF_bernoulli_dist_t * dist)
{
  if( 0.0 > x )
    return 0.0; 
  else if( 1.0 > x )
    return 1.0 - dist->p;
  else
    return 1.0; 
}


/**
 * The inverse cumulative distribution function for a Bernoulli
 * distribution.  It finds the answer iteratively using the bisection method.
 * Note that this is a bit different from the other functions in this file that
 * use the bisection method: this is a discrete distribution, so we limit the
 * values to integers.
 *
 * FIXME (A. Reeves, 4/11/10) I'm not sure this works for a Bernoulli distribution.
 *
 * @param area 0 <= \a area <= 1.
 * @param dist a Bernoulli distribution.
 * @return the value at which the cumulative distribution function = \a area.
 */
double
bernoulli_inverse_cdf (double area, PDF_bernoulli_dist_t * dist)
{
  int iter;
  double p;
  double x_lo, x_hi, x, a, previous_x;
  gboolean hibound_found;

  /* Eliminate compiler warnings about uninitialized values */
  x_hi = NAN;

  if (area == 0)
    return 0;

  p = dist->p;
  x_lo = 0;
  x = floor (p);   /* starting guess = mean */
  hibound_found = FALSE;
  iter = 0;

  /* Initialize the "value of x on the previous iteration" variable.  The
   * particular value here (x+1) doesn't matter, it just has to be different
   * from the starting value of x so that it won't break the do loop on the
   * first iteration. */
  previous_x = x+1;

  do
    {
      iter++;
      a = bernoulli_cdf (x, dist);
      if (fabs (a - area) < EPSILON || fabs (x - previous_x) < EPSILON)
        {
          /* We've found a good approximation to the answer, or our answer
           * hasn't changed since the last iteration. */
          break;
        }
      if (a < area)
        {
          /* We're to the left of the proper x.  Move x to the right. */
          x_lo = x;
          if (hibound_found)
            x = floor (x_lo + (x_hi - x_lo) / 2);
          else
            x = 2 * x;
        }
      else
        {
          /* We're to the right of the proper x.  Move x to the left. */
          if (!hibound_found)
            hibound_found = TRUE;
          x_hi = x;
          x = floor (x_lo + (x_hi - x_lo) / 2);
        }
    }
  while (iter < MAX_BISECTION_ITER);

  return x;
}


/**
 * Creates a new binomial distribution with parameters as illustrated below.
 *
 * @image html binomial.png
 *
 * @param n the number of trials.
 * @param p the probability of success of a single trial.
 * @return a pointer to a newly-created PDF_dist_t structure.
 */
PDF_dist_t *
PDF_new_binomial_dist (unsigned int n, double p)
{
  PDF_dist_t *dist;
  PDF_binomial_dist_t *t;      /* part specific to this distribution */

#if DEBUG
  g_debug ("----- ENTER PDF_new_binomial_dist");
#endif

  dist = g_new (PDF_dist_t, 1);
  dist->type = PDF_Binomial;
  dist->has_inf_lower_tail = FALSE;
  dist->has_inf_upper_tail = FALSE;
  dist->discrete = TRUE;
  t = &(dist->u.binomial);
  t->n = n;
  t->p = p;

#if DEBUG
  g_debug ("----- EXIT PDF_new_binomial_dist");
#endif

  return dist;
}



/**
 * Returns a text representation of a binomial distribution.
 *
 * @param dist a binomial distribution.
 * @return a string.
 */
char *
PDF_binomial_dist_to_string (PDF_binomial_dist_t * dist)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<binomial probability distribution\n n=%d p=%.2g>",
                    dist->n, dist->p);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * The inverse cumulative distribution function for a binomial
 * distribution.  It finds the answer iteratively using the bisection method.
 * Note that this is a bit different from the other functions in this file that
 * use the bisection method: this is a discrete distribution, so we limit the
 * values to integers.
 *
 * @param area 0 <= \a area <= 1.
 * @param dist a binomial distribution.
 * @return the value at which the cumulative distribution function = \a area.
 */
double
binomial_inverse_cdf (double area, PDF_binomial_dist_t * dist)
{
  int iter;
  unsigned int n;
  double p;
  double x_lo, x_hi, x, a, previous_x;
  gboolean hibound_found;

  /* Eliminate compiler warnings about uninitialized values */
  x_hi = NAN;

  if (area == 0)
    return 0;

  n = dist->n;
  p = dist->p;
  x_lo = 0;
  x = floor (((double) n) * p);   /* starting guess = mean */
  hibound_found = FALSE;
  iter = 0;

  /* Initialize the "value of x on the previous iteration" variable.  The
   * particular value here (x+1) doesn't matter, it just has to be different
   * from the starting value of x so that it won't break the do loop on the
   * first iteration. */
  previous_x = x+1;

  do
    {
      iter++;
      a = gsl_cdf_binomial_P (x, p, n);
      if (fabs (a - area) < EPSILON || fabs (x - previous_x) < EPSILON)
        {
          /* We've found a good approximation to the answer, or our answer
           * hasn't changed since the last iteration. */
          break;
        }
      if (a < area)
        {
          /* We're to the left of the proper x.  Move x to the right. */
          x_lo = x;
          if (hibound_found)
            x = floor (x_lo + (x_hi - x_lo) / 2);
          else
            x = 2 * x;
        }
      else
        {
          /* We're to the right of the proper x.  Move x to the left. */
          if (!hibound_found)
            hibound_found = TRUE;
          x_hi = x;
          x = floor (x_lo + (x_hi - x_lo) / 2);
        }
    }
  while (iter < MAX_BISECTION_ITER);

  return x;
}



/**
 * Creates a new discrete uniform distribution with parameters as illustrated below.
 *
 * @image html discrete_uniform.png
 *
 * @return a pointer to a newly-created PDF_dist_t structure.
 */
PDF_dist_t *
PDF_new_discrete_uniform_dist (int min, int max)
{
  PDF_dist_t *dist;
  PDF_discrete_uniform_dist_t *t;      /* part specific to this distribution */

#if DEBUG
  g_debug ("----- ENTER PDF_new_discrete_uniform_dist");
#endif

  dist = g_new (PDF_dist_t, 1);
  dist->type = PDF_Discrete_Uniform;
  dist->has_inf_lower_tail = FALSE;
  dist->has_inf_upper_tail = FALSE;
  dist->discrete = TRUE;
  t = &(dist->u.discrete_uniform);
  t->min = GSL_MIN(min, max);
  t->max = GSL_MAX(min, max);

#if DEBUG
  g_debug ("----- EXIT PDF_new_discrete_uniform_dist");
#endif

  return dist;
}



/**
 * Returns a text representation of a discrete uniform distribution.
 *
 * @param dist a uniform distribution.
 * @return a string.
 */
char *
PDF_discrete_uniform_dist_to_string (PDF_discrete_uniform_dist_t * dist)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s,
                    "<discrete uniform probability distribution\n from %d to %d>",
                    dist->min, dist->max);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Computes the probability density p(x) at \a x for a discrete uniform distribution.
 *
 * @param x
 * @param dist a discrete uniform distribution.
 * @return the probability density function for \a dist at \a x.
 */
double
discrete_uniform_pdf (int x, PDF_discrete_uniform_dist_t * dist)
{
  if ((x < dist->min) || (x > dist->max))
    return 0.0;
  else
    {
      int range = dist->max - dist->min + 1;
      return 1.0 / (double) range;
    }
}



/**
 * Computes the cumulative area <= \a x for a discrete uniform distribution.
 *
 * @param x
 * @param dist a discrete uniform distribution.
 * @return the cumulative area <= \a x for \a dist.
 */
double
discrete_uniform_cdf (int x, PDF_discrete_uniform_dist_t * dist)
{
  if (x < dist->min)
    return 0.0;
  else if (x > dist->max)
    return 1.0;
  else
    {
      int range = dist->max - dist->min + 1;
      return ((double) (x - dist->min + 1)) / (double) range;
    }
}



/**
 * The inverse cumulative distribution function for a discrete uniform
 * distribution.
 *
 * @param area 0 <= \a area <= 1.
 * @param dist a discrete uniform distribution.
 * @return the value at which the cumulative distribution function = \a area.
 */
int
discrete_uniform_inverse_cdf (double area, PDF_discrete_uniform_dist_t * dist)
{
  int range = dist->max - dist->min + 1;
  return floor (((double) range) * area + dist->min - 0.5);
}



/**
 * Returns a random variate from a discrete uniform distribution.
 *
 * @param dist a discrete uniform distribution.
 * @param rng a random number generator.
 * @return a random variate drawn from \a dist.
 */
int
ran_discrete_uniform (PDF_discrete_uniform_dist_t * dist, RAN_gen_t * rng)
{
  int range = dist->max - dist->min + 1;
  return gsl_rng_uniform_int (RAN_generator_as_gsl (rng), range) + dist->min;
}



/**
 * Creates a new hypergeometric distribution with parameters as illustrated below.
 *
 * @image html hypergeometric.png
 *
 * @param n1 the number of tagged items.
 * @param n2 the number of untagged items.
 * @param t the number of samples drawn.
 * @return a pointer to a newly-created PDF_dist_t structure.
 */
PDF_dist_t *
PDF_new_hypergeometric_dist (unsigned int n1, unsigned int n2, unsigned int t)
{
  PDF_dist_t *dist;
  PDF_hypergeometric_dist_t *d;      /* part specific to this distribution */

#if DEBUG
  g_debug ("----- ENTER PDF_new_hypergeometric_dist(n1=%u,n2=%u,t=%u)", n1, n2, t);
#endif

  dist = g_new (PDF_dist_t, 1);
  dist->type = PDF_Hypergeometric;
  dist->has_inf_lower_tail = FALSE;
  dist->has_inf_upper_tail = FALSE;
  dist->discrete = TRUE;
  d = &(dist->u.hypergeometric);
  d->n1 = n1;
  d->n2 = n2;
  d->t = t;

#if DEBUG
  g_debug ("----- EXIT PDF_new_hypergeometric_dist");
#endif

  return dist;
}



/**
 * Returns a text representation of a hypergeometric distribution.
 *
 * @param dist a hypergeometric distribution.
 * @return a string.
 */
char *
PDF_hypergeometric_dist_to_string (PDF_hypergeometric_dist_t * dist)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<hypergeometric probability distribution\n n1=%d n2=%d t=%d>",
                    dist->n1, dist->n2, dist->t);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * The inverse cumulative distribution function for a hypergeometric
 * distribution.  It finds the answer iteratively using the bisection method.
 *
 * @param area 0 <= \a area <= 1.
 * @param dist a hypergeometric distribution.
 * @return the value at which the cumulative distribution function = \a area.
 */
double
hypergeometric_inverse_cdf (double area, PDF_hypergeometric_dist_t * dist)
{
  unsigned int n1, n2, t;
  unsigned int lo, hi, k;

  n1 = dist->n1;
  n2 = dist->n2;
  t = dist->t;
  /* The minimum value of k is max(0,t-n2). */
  if (n2 < t)
    lo = t-n2;
  else
    lo = 0;
  if (area == 0)
    return lo;

  /* The maximum value of k is min(t,n1). */
  hi = MIN(t,n1) + 1;
  if (area == 1)
    return hi-1;

  while (hi - lo > 1)
    {
      k = (lo + hi) / 2;
      if (area >= gsl_cdf_hypergeometric_P (k, n1, n2, t))
        lo = k;
      else
        hi = k;
    }

  return lo;
}



/**
 * Returns a random variate from a multivariate hypergeometric
 * distribution.  Since this is a multivariate distribution, the
 * variate is an array which the caller will need to g_free when it is
 * no longer needed.
 *
 * @param m array of class counts
 * @param c number of classes
 * @param t number to draw
 * @param rng a random number generator.
 */
unsigned int * ran_multivariate_hypergeometric (unsigned int m[],
						unsigned int c,
						unsigned int t,
						RAN_gen_t *rng)
{
  unsigned int * v = g_new (unsigned int, c);
  int i = 0;
  unsigned int total = 0;
  unsigned int drawn = 0;

  g_assert(v != NULL);

  for (i = 0; i < c; v[i++] = 0) ; /* no body */

  for (total = 0, i = 0; i < c; total += m[i++]) ; /* no body */

  for (drawn = 0, i = 0; (i < (c - 1)) && (drawn < t); i++)
    {
      v[i] = gsl_ran_hypergeometric(RAN_generator_as_gsl (rng),
				    m[i],
				    total - m[i],
				    t - drawn);
      drawn += v[i];
      total -= m[i];
    }
  /* This seems a little risky.  We could end up overdrawing from the
   * last class.  Actually, since we do a draw each time from i and
   * the remaining, we must always have a valid result. */
  v[c - 1] = t - drawn;

  return v;
}



#ifdef WIN_DLL

/* Histogram PDF */

DLL_API gsl_histogram* 
aphi_create_histogram( int size, double ranges[], double bin_vals[] ) {
  gsl_histogram* hist;
  int i;
  double val;
  
  hist = gsl_histogram_alloc( size - 1 );
  
  if( NULL != hist ) {
    gsl_histogram_set_ranges( hist, ranges, size );
    
    for( i = 0; i < size - 1; ++i ) {
      val = ( ranges[i] + ranges[i+1] ) / 2;
      gsl_histogram_accumulate( hist, val, bin_vals[i] ); 
    }
  }  
  
  return hist;
}


DLL_API void 
aphi_free_histogram( int unsigned hist ) {
  gsl_histogram_free( (gsl_histogram*)hist );   
}


DLL_API double 
aphi_histogram_pdf( double x, int unsigned hist ) {
  PDF_dist_t* dist;
  double result;

  dist = PDF_new_histogram_dist( (gsl_histogram*)hist );
  result = PDF_pdf( x, dist );
  PDF_free_dist( dist );
  
  return result;   
}

DLL_API double 
aphi_histogram_cdf( double x, int unsigned hist ) {
  PDF_dist_t* dist;
  double result;

  dist = PDF_new_histogram_dist( (gsl_histogram*)hist );
  result = PDF_cdf( x, dist );
  PDF_free_dist( dist );
  
  return result;   
}

 
DLL_API double 
aphi_histogram_inverse_cdf( double area, int unsigned hist ) {
  PDF_dist_t* dist;
  double result;

  dist = PDF_new_histogram_dist( (gsl_histogram*)hist );
  result = PDF_inverse_cdf( area, dist );
  PDF_free_dist( dist );
  
  return result;   
}


DLL_API double 
aphi_histogram_rand( int unsigned rng, int unsigned hist ) {
  PDF_dist_t* dist;
  double result;

  dist = PDF_new_histogram_dist( (gsl_histogram*)hist );
  result = PDF_random( dist, (RAN_gen_t*)rng );
  PDF_free_dist( dist );
  
  return result;   
}

 
DLL_API double 
aphi_histogram_mean( int unsigned hist ) {
  return gsl_histogram_mean( (gsl_histogram*)hist );   
} 

#endif

/**
 * Deletes a distribution from memory.
 *
 * @param dist a distribution.
 */
void
PDF_free_dist (PDF_dist_t * dist)
{
  if (dist == NULL)
    return;

  switch (dist->type)
    {
    case PDF_Piecewise:
      PDF_free_piecewise_dist (&(dist->u.piecewise));
      break;
    case PDF_Histogram:
      PDF_free_histogram_dist (&(dist->u.histogram));
      break;
    default:
      /* No dynamically-allocated parts to free. */
      break;
    }
  g_free (dist);
}



/**
 * Makes a deep copy of a distribution.
 *
 * @param dist a distribution.
 * @return a deep copy of the distribution.
 */
PDF_dist_t *
PDF_clone_dist (PDF_dist_t * dist)
{
  PDF_dist_t *clone;

  if (dist == NULL)
    return NULL;

  switch (dist->type)
    {
    case PDF_Point:
      {
        PDF_point_dist_t *d;
        d = &(dist->u.point);
        clone = PDF_new_point_dist (d->value);
        break;
      }
    case PDF_Uniform:
      {
        PDF_uniform_dist_t *d;
        d = &(dist->u.uniform);
        clone = PDF_new_uniform_dist (d->a, d->b);
        break;
      }
    case PDF_Triangular:
      {
        PDF_triangular_dist_t *d;
        d = &(dist->u.triangular);
        clone = PDF_new_triangular_dist (d->a, d->c, d->b);
        break;
      }
    case PDF_Piecewise:
      {
        PDF_piecewise_dist_t *d;
        d = &(dist->u.piecewise);
        clone = PDF_new_piecewise_dist (d->n, d->x, d->y);
        break;
      }
    case PDF_Histogram:
      {
        PDF_histogram_dist_t *d;
        d = &(dist->u.histogram);
        clone = PDF_new_histogram_dist (d->histo);
        break;
      }
    case PDF_Gaussian:
      {
        PDF_gaussian_dist_t *d;
        d = &(dist->u.gaussian);
        clone = PDF_new_gaussian_dist (d->mu, d->sigma);
        break;
      }
    case PDF_Inverse_Gaussian:
      {
        PDF_inverse_gaussian_dist_t *d;
        d = &(dist->u.inverse_gaussian);
        clone = PDF_new_inverse_gaussian_dist (d->mu, d->lambda);
        break;
      }
    case PDF_Poisson:
      {
        PDF_poisson_dist_t *d;
        d = &(dist->u.poisson);
        clone = PDF_new_poisson_dist (d->mu);
        break;
      }
    case PDF_Beta:
      {
        PDF_beta_dist_t *d;
        d = &(dist->u.beta);
        clone = PDF_new_beta_dist (d->alpha, d->beta, d->location, d->scale);
        break;
      }
    case PDF_Gamma:
      {
        PDF_gamma_dist_t *d;
        d = &(dist->u.gamma);
        clone = PDF_new_gamma_dist (d->alpha, d->beta);
        break;
      }
    case PDF_Weibull:
      {
        PDF_weibull_dist_t *d;
        d = &(dist->u.weibull);
        clone = PDF_new_weibull_dist (d->alpha, d->beta);
        break;
      }
    case PDF_Exponential:
      {
        PDF_exponential_dist_t *d;
        d = &(dist->u.exponential);
        clone = PDF_new_exponential_dist (d->mean);
        break;
      }
    case PDF_Pearson5:
      {
        PDF_pearson5_dist_t *d;
        d = &(dist->u.pearson5);
        clone = PDF_new_pearson5_dist (d->alpha, d->beta);
        break;
      }
    case PDF_Logistic:
      {
        PDF_logistic_dist_t *d;
        d = &(dist->u.logistic);
        clone = PDF_new_logistic_dist (d->location, d->scale);
        break;
      }
    case PDF_LogLogistic:
      {
        PDF_loglogistic_dist_t *d;
        d = &(dist->u.loglogistic);
        clone = PDF_new_loglogistic_dist (d->location, d->scale, d->shape);
        break;
      }
    case PDF_Lognormal:
      {
        PDF_lognormal_dist_t *d;
        d = &(dist->u.lognormal);
        clone = PDF_new_lognormal_dist (d->zeta, d->sigma);
        break;
      }
    case PDF_NegativeBinomial:
      {
        PDF_negative_binomial_dist_t *d;
        d = &(dist->u.negative_binomial);
        clone = PDF_new_negative_binomial_dist (d->s, d->p);
        break;
      }
    case PDF_Pareto:
      {
        PDF_pareto_dist_t *d;
        d = &(dist->u.pareto);
        clone = PDF_new_pareto_dist (d->theta, d->a);
        break;
      }
    case PDF_Bernoulli:
      {
        PDF_bernoulli_dist_t *d;
        d = &(dist->u.bernoulli);
        clone = PDF_new_bernoulli_dist (d->p);
        break;
      }
    case PDF_Binomial:
      {
        PDF_binomial_dist_t *d;
        d = &(dist->u.binomial);
        clone = PDF_new_binomial_dist (d->n, d->p);
        break;
      }
    case PDF_Discrete_Uniform:
      {
        PDF_discrete_uniform_dist_t *d;
        d = &(dist->u.discrete_uniform);
        clone = PDF_new_discrete_uniform_dist (d->min, d->max);
        break;
      }
    case PDF_Hypergeometric:
      {
        PDF_hypergeometric_dist_t *d;
        d = &(dist->u.hypergeometric);
        clone = PDF_new_hypergeometric_dist (d->n1, d->n1, d->t);
        break;
      }
    default:
      g_assert_not_reached ();
    }

  return clone;
}



/**
 * Returns a text representation of a distribution.
 *
 * @param dist a distribution.
 * @return a string.
 */
char *
PDF_dist_to_string (PDF_dist_t * dist)
{
  char *s;

  switch (dist->type)
    {
    case PDF_Point:
      s = PDF_point_dist_to_string (&(dist->u.point));
      break;
    case PDF_Uniform:
      s = PDF_uniform_dist_to_string (&(dist->u.uniform));
      break;
    case PDF_Triangular:
      s = PDF_triangular_dist_to_string (&(dist->u.triangular));
      break;
    case PDF_Piecewise:
      s = PDF_piecewise_dist_to_string (&(dist->u.piecewise));
      break;
    case PDF_Histogram:
      s = PDF_histogram_dist_to_string (&(dist->u.histogram));
      break;
    case PDF_Gaussian:
      s = PDF_gaussian_dist_to_string (&(dist->u.gaussian));
      break;
    case PDF_Inverse_Gaussian:
      s = PDF_inverse_gaussian_dist_to_string (&(dist->u.inverse_gaussian));
      break;
    case PDF_Poisson:
      s = PDF_poisson_dist_to_string (&(dist->u.poisson));
      break;
    case PDF_Beta:
      s = PDF_beta_dist_to_string (&(dist->u.beta));
      break;
    case PDF_Gamma:
      s = PDF_gamma_dist_to_string (&(dist->u.gamma));
      break;
    case PDF_Weibull:
      s = PDF_weibull_dist_to_string (&(dist->u.weibull));
      break;
    case PDF_Exponential:
      s = PDF_exponential_dist_to_string (&(dist->u.exponential));
      break;
    case PDF_Pearson5:
      s = PDF_pearson5_dist_to_string (&(dist->u.pearson5));
      break;
    case PDF_Logistic:
      s = PDF_logistic_dist_to_string (&(dist->u.logistic));
      break;
    case PDF_LogLogistic:
      s = PDF_loglogistic_dist_to_string (&(dist->u.loglogistic));
      break;
    case PDF_Lognormal:
      s = PDF_lognormal_dist_to_string (&(dist->u.lognormal));
      break;
    case PDF_NegativeBinomial:
      s = PDF_negative_binomial_dist_to_string (&(dist->u.negative_binomial));
      break;
    case PDF_Pareto:
      s = PDF_pareto_dist_to_string (&(dist->u.pareto));
      break;
    case PDF_Bernoulli:
      s = PDF_bernoulli_dist_to_string (&(dist->u.bernoulli));
      break;      
    case PDF_Binomial:
      s = PDF_binomial_dist_to_string (&(dist->u.binomial));
      break;
    case PDF_Discrete_Uniform:
      s = PDF_discrete_uniform_dist_to_string (&(dist->u.discrete_uniform));
      break;
    case PDF_Hypergeometric:
      s = PDF_hypergeometric_dist_to_string (&(dist->u.hypergeometric));
      break;
    default:
      g_assert_not_reached ();
    }

  return s;
}



/**
 * Prints a distribution to a stream.
 *
 * @param stream a stream to write to.  If NULL, defaults to stdout.
 * @param dist a distribution.
 * @return the number of characters printed (not including the trailing '\\0').
 */
int
PDF_fprintf_dist (FILE * stream, PDF_dist_t * dist)
{
  char *s;
  int nchars_written;

  s = PDF_dist_to_string (dist);
  nchars_written = fprintf (stream ? stream : stdout, "%s", s);
  free (s);
  return nchars_written;
}



/**
 * Returns a random variate from a distribution.
 *
 * @param dist a distribution.
 * @param rng a random number generator.
 * @return a random number drawn from \a dist.
 */
double
PDF_random (PDF_dist_t * dist, RAN_gen_t * rng)
{
  double r;

  /* The random number generator is sometimes "fixed" at a particular value for
   * testing purposes. */
  if (rng->fixed)
    {
      if (!dist->discrete)
        {
          /* For continuous distributions, get a return value using the inverse
           * cumulative distribution function.  For example, if the rng is
           * "fixed" at 0.5, return the value x at which cdf(x) = 0.5.  Watch
           * out for "fixed" values near 0 or 1 when there are infinite tails. */
          double modified_fixed_value;
          modified_fixed_value = rng->fixed_value;
          if (dist->has_inf_lower_tail)
            modified_fixed_value = MAX (0.01, modified_fixed_value);
          if (dist->has_inf_upper_tail)
            modified_fixed_value = MIN (0.99, modified_fixed_value);
          r = PDF_inverse_cdf (modified_fixed_value, dist);
        } /* end of case for continuous distributions */
      else
        {
          /* For discrete distributions, a useful interpretation in the "fixed"
           * case is to return the lowest value k for which the cdf is >= the
           * fixed random value.
           *
           * This hack is mostly just here so that we can write completely
           * deterministic test cases involving within-unit spread. */
          unsigned int lo, hi, k;
#if DEBUG
          GString *s;
#endif
          lo = (unsigned int) trunc (PDF_min (dist));
          hi = (unsigned int) trunc (PDF_max (dist)) + 1;
          /* Binary search to find k. */
          while (hi - lo > 1)
            {
              k = (lo + hi - 1) / 2;
              if (PDF_cdf ((double) k, dist) + EPSILON < rng->fixed_value)
                lo = k+1;
              else
                hi = k+1;
            }
          r = (double) lo;
#if DEBUG
          /* For debugging, show the CDF values and highlight the one we chose. */
          lo = (unsigned int) trunc (PDF_min (dist));
          hi = (unsigned int) trunc (PDF_max (dist)) + 1;
          g_debug ("lowest value allowed = %u, highest = %u", lo, hi-1);
          s = g_string_new (NULL);
          for (k = lo; k < hi; k++)
            g_string_append_printf (s, (double) k == r ? " [%g]" : " %g", PDF_cdf ((double) k, dist));
          g_debug ("%s", s->str);
#endif
        } /* end of case for discrete distributions */
      return r;
    } /* end of case where random number generator is “fixed” */

  switch (dist->type)
    {
    case PDF_Triangular:
      r = ran_triangular (&(dist->u.triangular), rng);
      break;
    case PDF_Piecewise:
      r = ran_piecewise (&(dist->u.piecewise), rng);
      break;
    case PDF_Uniform:
      r = gsl_ran_flat (RAN_generator_as_gsl (rng), dist->u.uniform.a, dist->u.uniform.b);
      break;
    case PDF_Histogram:
      r = ran_histogram (&(dist->u.histogram), rng);
      break;
    case PDF_Gaussian:
      r = gsl_ran_gaussian (RAN_generator_as_gsl (rng), dist->u.gaussian.sigma);
      r += dist->u.gaussian.mu;
      break;
    case PDF_Inverse_Gaussian:
      r = ran_inverse_gaussian (&(dist->u.inverse_gaussian), rng);
      break;
    case PDF_Poisson:
      r = gsl_ran_poisson (RAN_generator_as_gsl (rng), dist->u.poisson.mu);
      break;
    case PDF_Point:
      r = dist->u.point.value;
      break;
    case PDF_Beta:
      r = gsl_ran_beta (RAN_generator_as_gsl (rng), dist->u.beta.alpha, dist->u.beta.beta);
      r = r * dist->u.beta.width + dist->u.beta.location;
      break;
    case PDF_Gamma:
      r = gsl_ran_gamma (RAN_generator_as_gsl (rng), dist->u.gamma.alpha, dist->u.gamma.beta);
      break;
    case PDF_Weibull:
      /*
         The order in which the GSL functions for Weibull distributions accept
         parameters is different from most other references.  For this reason,
         it may appear that these parameters are given in the wrong order.
       */
      r = gsl_ran_weibull (RAN_generator_as_gsl (rng), dist->u.weibull.beta, dist->u.weibull.alpha);
      break;
    case PDF_Exponential:
      r = gsl_ran_exponential (RAN_generator_as_gsl (rng), dist->u.exponential.mean);
      break;
    case PDF_Pearson5:
      r = 1.0 / gsl_ran_gamma (RAN_generator_as_gsl (rng),
                               dist->u.pearson5.alpha, dist->u.pearson5.one_over_beta);
      break;
    case PDF_Logistic:
      r = gsl_ran_logistic (RAN_generator_as_gsl (rng), dist->u.logistic.scale);
      r += dist->u.logistic.location;
      break;
    case PDF_LogLogistic:
      r = ran_loglogistic (&(dist->u.loglogistic), rng);
      break;
    case PDF_Lognormal:
      r = gsl_ran_lognormal (RAN_generator_as_gsl (rng),
                             dist->u.lognormal.zeta, dist->u.lognormal.sigma);
      break;
    case PDF_NegativeBinomial:
      /* The return value is an integer, since the negative binomial
       * distribution is a discrete distribution. */
      r = (double) gsl_ran_negative_binomial (RAN_generator_as_gsl (rng),
                                              dist->u.negative_binomial.p,
                                              dist->u.negative_binomial.s);
      break;
    case PDF_Pareto:
      /* Recall that parameters have different names here than in the GSL.
       * theta = GSL's a, a = GSL's b */
      r = gsl_ran_pareto (RAN_generator_as_gsl (rng),
                          dist->u.pareto.theta, dist->u.pareto.a);
      break;
    case PDF_Bernoulli:
      r = gsl_ran_bernoulli (RAN_generator_as_gsl (rng),
                            dist->u.binomial.p);      
    case PDF_Binomial:
      r = gsl_ran_binomial (RAN_generator_as_gsl (rng),
                            dist->u.binomial.p, dist->u.binomial.n);
      break;
    case PDF_Discrete_Uniform:
      r = ran_discrete_uniform (&(dist->u.discrete_uniform), rng);
      break;
    case PDF_Hypergeometric:
      r = gsl_ran_hypergeometric (RAN_generator_as_gsl (rng),
                                  dist->u.hypergeometric.n1, dist->u.hypergeometric.n2,
                                  dist->u.hypergeometric.t);
      break;
    default:
      g_assert_not_reached ();
    }

  return r;
}



/**
 * Returns a random variate from a distribution, constrained to be non-negative
 * (either zero or positive).
 *
 * @param dist a distribution.
 * @param rng a random number generator.
 * @return a non-negative random number drawn from \a dist.
 */
double
PDF_random_non_neg (PDF_dist_t * dist, RAN_gen_t * rng)
{
  double r;

  do
    {
      r = PDF_random (dist, rng);
    }
  while (r < 0);
  return r;
}



/**
 * Returns a random variate from a distribution, constrained to be positive
 * (greater than zero).
 *
 * @param dist a distribution.
 * @param rng a random number generator.
 * @return a positive random number drawn from \a dist.
 */
double
PDF_random_pos (PDF_dist_t * dist, RAN_gen_t * rng)
{
  double r;

  do
    {
      r = PDF_random (dist, rng);
    }
  while (r <= 0);
  return r;
}



/**
 * Returns a random variate from a distribution, rounded to an integer.
 *
 * @param dist a distribution.
 * @param rng a random number generator.
 * @return a random number drawn from \a dist.
 */
int
PDF_random_int (PDF_dist_t * dist, RAN_gen_t * rng)
{
  double r;

  do
    {
      r = PDF_random (dist, rng);
    }
  while (r < INT_MIN || r > INT_MAX);
  return (int) round (r);
}



/**
 * Returns a random variate from a distribution, rounded to an integer and
 * constrained to be non-negative (either zero or positive).
 *
 * @param dist a distribution.
 * @param rng a random number generator.
 * @return a non-negative random number drawn from \a dist.
 */
int
PDF_random_non_neg_int (PDF_dist_t * dist, RAN_gen_t * rng)
{
  double r;

  do
    {
      r = PDF_random (dist, rng);
    }
  while (r <= -0.5 || r > INT_MAX);
  /* The manpage for round says that half-way cases will be rounded away from
   * zero, -0.5 would round to -1. */
  return (int) round (r);
}



/**
 * Returns a random variate from a distribution, rounded to an integer and
 * constrained to be positive (greater than zero).
 *
 * @param dist a distribution.
 * @param rng a random number generator.
 * @return a positive random number drawn from \a dist.
 */
guint
PDF_random_pos_int (PDF_dist_t * dist, RAN_gen_t * rng)
{
  double r;

  do
    {
      r = PDF_random (dist, rng);
    }
  while (r < 0.5 || r > INT_MAX);
  /* The manpage for round says that half-way cases will be rounded away from
   * zero, so 0.5 will round to 1. */
  return (guint) round (r);
}



/**
 * Computes the probability density p(x) at x for a distribution.
 *
 * @param x
 * @param dist a distribution.
 * @return p(x).
 */
double
PDF_pdf (double x, PDF_dist_t * dist)
{
  double p;

  switch (dist->type)
    {
    case PDF_Triangular:
      p = triangular_pdf (x, &(dist->u.triangular));
      break;
    case PDF_Piecewise:
      p = piecewise_pdf (x, &(dist->u.piecewise));
      break;
    case PDF_Uniform:
      p = gsl_ran_flat_pdf (x, dist->u.uniform.a, dist->u.uniform.b);
      break;
    case PDF_Histogram:
      p = histogram_pdf (x, &(dist->u.histogram));
      break;
    case PDF_Gaussian:
      p = gsl_ran_gaussian_pdf (x - dist->u.gaussian.mu, dist->u.gaussian.sigma);
      break;
    case PDF_Inverse_Gaussian:
      p = inverse_gaussian_pdf (x, &(dist->u.inverse_gaussian));
      break;
    case PDF_Poisson:
      p = gsl_ran_poisson_pdf ((unsigned int) x, dist->u.poisson.mu);
      break;
    case PDF_Point:
      p = (gsl_fcmp (x, dist->u.point.value, EPSILON) == 0) ? 1 : 0;
      break;
    case PDF_Beta:
      /* This returns the probability density for the "unit" beta, with width = 1 */
      p = gsl_ran_beta_pdf ((x - dist->u.beta.location) / dist->u.beta.width,
                            dist->u.beta.alpha, dist->u.beta.beta);

      /* For non-unit beta PDFs, this transformation is necessary */
      p = p / dist->u.beta.width;
      break;
    case PDF_Gamma:
      p = gsl_ran_gamma_pdf (x, dist->u.gamma.alpha, dist->u.gamma.beta);
      break;
    case PDF_Weibull:
      /*
         The order in which the GSL functions for Weibull distributions accept
         parameters is different from most other references.  For this reason,
         it may appear that these parameters are given in the wrong order.
       */
      p = gsl_ran_weibull_pdf (x, dist->u.weibull.beta, dist->u.weibull.alpha);
      break;
    case PDF_Exponential:
      p = gsl_ran_exponential_pdf (x, dist->u.exponential.mean);
      break;
    case PDF_Pearson5:
      p = pearson5_pdf (x, &(dist->u.pearson5));
      break;
    case PDF_Logistic:
      p = gsl_ran_logistic_pdf (x - dist->u.logistic.location, dist->u.logistic.scale);
      break;
    case PDF_LogLogistic:
      p = loglogistic_pdf (x, &(dist->u.loglogistic));
      break;
    case PDF_Lognormal:
      p = gsl_ran_lognormal_pdf (x, dist->u.lognormal.zeta, dist->u.lognormal.sigma);
      break;
    case PDF_NegativeBinomial:
      p = gsl_ran_negative_binomial_pdf (x, dist->u.negative_binomial.p, dist->u.negative_binomial.s);
      break;
    case PDF_Pareto:
      p = gsl_ran_pareto_pdf (x, dist->u.pareto.theta, dist->u.pareto.a);
      break;
    case PDF_Bernoulli:
      p = gsl_ran_bernoulli_pdf (x, dist->u.bernoulli.p);
      break;
    case PDF_Binomial:
      p = gsl_ran_binomial_pdf (x, dist->u.binomial.p, dist->u.binomial.n);
      break;
    case PDF_Discrete_Uniform:
      p = discrete_uniform_pdf (x, &(dist->u.discrete_uniform));
      break;
    case PDF_Hypergeometric:
      p = gsl_ran_hypergeometric_pdf (x,
                                      dist->u.hypergeometric.n1, dist->u.hypergeometric.n2,
                                      dist->u.hypergeometric.t);
      break;
    default:
      g_assert_not_reached ();
    }
  return p;
}



/**
 * Computes the cumulative area <= \a x for a distribution.
 *
 * @param x
 * @param dist a distribution.
 * @return the area under the distribution curve to the left of \a x.
 */
double
PDF_cdf (double x, PDF_dist_t * dist)
{
  double c;

  switch (dist->type)
    {
    case PDF_Triangular:
      c = triangular_cdf (x, &(dist->u.triangular));
      break;
    case PDF_Piecewise:
      c = piecewise_cdf (x, &(dist->u.piecewise));
      break;
    case PDF_Uniform:
      c = uniform_cdf (x, &(dist->u.uniform));
      break;
    case PDF_Histogram:
      c = histogram_cdf (x, &(dist->u.histogram));
      break;
    case PDF_Gaussian:
      c = gsl_cdf_gaussian_P (x - dist->u.gaussian.mu, dist->u.gaussian.sigma);
      break;
    case PDF_Inverse_Gaussian:
      c = inverse_gaussian_cdf (x, &(dist->u.inverse_gaussian));
      break;
    case PDF_Poisson:
      c = poisson_cdf (x, &(dist->u.poisson));
      break;
    case PDF_Point:
      c = (x < dist->u.point.value) ? 0 : 1;
      break;
    case PDF_Beta:
      c = beta_cdf (x, &(dist->u.beta));
      break;
    case PDF_Gamma:
      c = gsl_cdf_gamma_P (x, dist->u.gamma.alpha, dist->u.gamma.beta);
      break;
    case PDF_Weibull:
      /*
         The order in which the GSL functions for Weibull distributions accept
         parameters is different from most other references.  For this reason,
         it may appear that these parameters are given in the wrong order.
       */
      c = (x < 0) ? 0 : gsl_cdf_weibull_P (x, dist->u.weibull.beta, dist->u.weibull.alpha);
      break;
    case PDF_Exponential:
      c = (x < 0) ? 0 : gsl_cdf_exponential_P (x, dist->u.exponential.mean);
      break;
    case PDF_Pearson5:
      c = pearson5_cdf (x, &(dist->u.pearson5));
      break;
    case PDF_Logistic:
      c = gsl_cdf_logistic_P (x - dist->u.logistic.location, dist->u.logistic.scale);
      break;
    case PDF_LogLogistic:
      c = loglogistic_cdf (x, &(dist->u.loglogistic));
      break;
    case PDF_Lognormal:
      c = (x < 0) ? 0 : gsl_cdf_lognormal_P (x, dist->u.lognormal.zeta, dist->u.lognormal.sigma);
      break;
    case PDF_NegativeBinomial:
      c = (x < 0) ? 0 : gsl_cdf_negative_binomial_P (x, dist->u.negative_binomial.p, dist->u.negative_binomial.s);
      break;
    case PDF_Pareto:
      c = gsl_cdf_pareto_P (x, dist->u.pareto.theta, dist->u.pareto.a);
      break;
    case PDF_Bernoulli:
      c = bernoulli_cdf (x, &(dist->u.bernoulli));
    case PDF_Binomial:
      c = (x < 0) ? 0 : gsl_cdf_binomial_P (x, dist->u.binomial.p, dist->u.binomial.n);
      break;
    case PDF_Discrete_Uniform:
      c = discrete_uniform_cdf (x, &(dist->u.discrete_uniform));
      break;
    case PDF_Hypergeometric:
      c = (x < 0) ? 0 : gsl_cdf_hypergeometric_P (x,
                                                  dist->u.hypergeometric.n1,
                                                  dist->u.hypergeometric.n2,
                                                  dist->u.hypergeometric.t);
      break;
    default:
      g_assert_not_reached ();
    }
  return c;
}



/**
 * The inverse cumulative distribution function.
 *
 * @param area 0 <= \a area <= 1.
 * @param dist a distribution.
 * @return the value at which the cumulative distribution function = \a area.
 */
double
PDF_inverse_cdf (double area, PDF_dist_t * dist)
{
  double c;

  g_assert (0 <= area && area <= 1);

  switch (dist->type)
    {
    case PDF_Triangular:
      c = triangular_inverse_cdf (area, &(dist->u.triangular));
      break;
    case PDF_Piecewise:
      c = piecewise_inverse_cdf (area, &(dist->u.piecewise));
      break;
    case PDF_Uniform:
      c = uniform_inverse_cdf (area, &(dist->u.uniform));
      break;
    case PDF_Histogram:
      c = histogram_inverse_cdf (area, &(dist->u.histogram));
      break;
    case PDF_Gaussian:
      c = gsl_cdf_gaussian_Pinv (area, dist->u.gaussian.sigma) + dist->u.gaussian.mu;
      break;
    case PDF_Inverse_Gaussian:
      c = inverse_gaussian_inverse_cdf (area, &(dist->u.inverse_gaussian));
      break;
    case PDF_Point:
      c = dist->u.point.value;
      break;
    case PDF_Beta:
      c = beta_inverse_cdf (area, &(dist->u.beta));
      break;
    case PDF_Gamma:
      c = gsl_cdf_gamma_Pinv (area, dist->u.gamma.alpha, dist->u.gamma.beta);
      break;
    case PDF_Weibull:
      /*
         The order in which the GSL functions for Weibull distributions accept
         parameters is different from most other references.  For this reason,
         it may appear that these parameters are given in the wrong order.
       */
      c = gsl_cdf_weibull_Pinv (area, dist->u.weibull.beta, dist->u.weibull.alpha);
      break;
    case PDF_Exponential:
      c = gsl_cdf_exponential_Pinv (area, dist->u.exponential.mean);
      break;
    case PDF_Pearson5:
      c = pearson5_inverse_cdf (area, &(dist->u.pearson5));
      break;
    case PDF_Logistic:
      c = gsl_cdf_logistic_Pinv (area, dist->u.logistic.scale) + dist->u.logistic.location;
      break;
    case PDF_LogLogistic:
      c = loglogistic_inverse_cdf (area, &(dist->u.loglogistic));
      break;
    case PDF_Lognormal:
      c = gsl_cdf_lognormal_Pinv (area, dist->u.lognormal.zeta, dist->u.lognormal.sigma);
      break;
    case PDF_NegativeBinomial:
      c = negative_binomial_inverse_cdf (area, &(dist->u.negative_binomial));
      break;
    case PDF_Pareto:
      c = gsl_cdf_pareto_Pinv (area, dist->u.pareto.theta, dist->u.pareto.a);
      break;
    case PDF_Bernoulli:
      c = bernoulli_inverse_cdf (area, &(dist->u.bernoulli));
    case PDF_Binomial:
      c = binomial_inverse_cdf (area, &(dist->u.binomial));
      break;
    case PDF_Discrete_Uniform:
      c = discrete_uniform_inverse_cdf (area, &(dist->u.discrete_uniform));
      break;
    case PDF_Hypergeometric:
      c = hypergeometric_inverse_cdf (area, &(dist->u.hypergeometric));
      break;
    default:
      g_assert_not_reached ();
    }
  return c;
}

/**
 * Does the range for this PDF have a minimum?
 *
 * @param dist a distribution.
 * @return TRUE if this PDF has a minimum, FALSE if the PDF has an infinite lower tail.
 */
gboolean
PDF_has_min (PDF_dist_t * dist)
{
  return !(dist->has_inf_lower_tail);
}

/**
 * Does the range for this PDF have a maximum?
 *
 * @param dist a distribution.
 * @return TRUE if this PDF has a maximum, FALSE if the PDF has an infinite upper tail.
 */
gboolean
PDF_has_max (PDF_dist_t * dist)
{
  return !(dist->has_inf_upper_tail);
}

/**
 * The minimum value in the range of this PDF
 *
 * @param dist a distribution.
 * @return the minimum value for this PDF if there is one, GSL_NEGINF if it has an infinite lower tail.
 */
double
PDF_min (PDF_dist_t * dist)
{
  double min;

  if (dist->has_inf_lower_tail)
    return GSL_NEGINF;

  switch (dist->type)
    {
    case PDF_Point:
      {
        PDF_point_dist_t *d;
        d = &(dist->u.point);
        min = d->value;
        break;
      }
    case PDF_Uniform:
      {
        PDF_uniform_dist_t *d;
        d = &(dist->u.uniform);
        min = d->a;
        break;
      }
    case PDF_Triangular:
      {
        PDF_triangular_dist_t *d;
        d = &(dist->u.triangular);
        min = d->a;
        break;
      }
    case PDF_Piecewise:
      {
        PDF_piecewise_dist_t *d;
        d = &(dist->u.piecewise);
        min = d->first_x;
        break;
      }
    case PDF_Histogram:
      {
        PDF_histogram_dist_t *d;
        d = &(dist->u.histogram);
        min = d->first_x;
        break;
      }
    case PDF_Gaussian:
      {
        min = GSL_NEGINF;
        break;
      }
    case PDF_Inverse_Gaussian:
      {
        min = 0.0;
        break;
      }
    case PDF_Poisson:
      {
        min = 0.0;
        break;
      }
    case PDF_Beta:
      {
        PDF_beta_dist_t *d;
        d = &(dist->u.beta);
        min = d->location;
        break;
      }
    case PDF_Gamma:
      {
        min = 0.0;
        break;
      }
    case PDF_Weibull:
      {
        min = 0.0;
        break;
      }
    case PDF_Exponential:
      {
        min = 0.0;
        break;
      }
    case PDF_Pearson5:
      {
        min = 0.0;
        break;
      }
    case PDF_Logistic:
      {
        min = GSL_NEGINF;
        break;
      }
    case PDF_LogLogistic:
      {
        PDF_loglogistic_dist_t *d;
        d = &(dist->u.loglogistic);
        min = d->location;
        break;
      }
    case PDF_Lognormal:
      {
        min = 0.0;
        break;
      }
    case PDF_NegativeBinomial:
      {
        min = 0.0;
        break;
      }
    case PDF_Pareto:
      {
        PDF_pareto_dist_t *d;
        d = &(dist->u.pareto);
        min = d->a;
        break;
      }
    case PDF_Bernoulli:
      {
        min = 0.0;
        break;  
      }
    case PDF_Binomial:
      {
        min = 0;
        break;
      }
    case PDF_Discrete_Uniform:
      {
        PDF_discrete_uniform_dist_t *d;
        d = &(dist->u.discrete_uniform);
        min = d->min;
        break;
      }
    case PDF_Hypergeometric:
      {
        PDF_hypergeometric_dist_t *d;
        d = &(dist->u.hypergeometric);
        min = gsl_max (0, d->t - d->n2);
        break;
      }
    default:
      g_assert_not_reached ();
    }

  return min;
}

/**
 * The maximum value in the range of this PDF
 *
 * @param dist a distribution.
 * @return the maximum value for this PDF if there is one, GSL_POSINF if it has an infinite upper tail.
 */
double
PDF_max (PDF_dist_t * dist)
{
  double max;

  if (dist->has_inf_upper_tail)
    return GSL_POSINF;

  switch (dist->type)
    {
    case PDF_Point:
      {
        PDF_point_dist_t *d;
        d = &(dist->u.point);
        max = d->value;
        break;
      }
    case PDF_Uniform:
      {
        PDF_uniform_dist_t *d;
        d = &(dist->u.uniform);
        max = d->b;
        break;
      }
    case PDF_Triangular:
      {
        PDF_triangular_dist_t *d;
        d = &(dist->u.triangular);
        max = d->b;
        break;
      }
    case PDF_Piecewise:
      {
        PDF_piecewise_dist_t *d;
        d = &(dist->u.piecewise);
        max = d->last_x;
        break;
      }
    case PDF_Histogram:
      {
        PDF_histogram_dist_t *d;
        d = &(dist->u.histogram);
        max = d->last_x;
        break;
      }
    case PDF_Gaussian:
      {
        max = GSL_POSINF;
        break;
      }
    case PDF_Inverse_Gaussian:
      {
        max = GSL_POSINF;
        break;
      }
    case PDF_Poisson:
      {
        max = GSL_POSINF;
        break;
      }
    case PDF_Beta:
      {
        PDF_beta_dist_t *d;
        d = &(dist->u.beta);
        max = d->scale;
        break;
      }
    case PDF_Gamma:
      {
        max = GSL_POSINF;
        break;
      }
    case PDF_Weibull:
      {
        max = GSL_POSINF;
        break;
      }
    case PDF_Exponential:
      {
        max = GSL_POSINF;
        break;
      }
    case PDF_Pearson5:
      {
        max = GSL_POSINF;
        break;
      }
    case PDF_Logistic:
      {
        max = GSL_POSINF;
        break;
      }
    case PDF_LogLogistic:
      {
        max = GSL_POSINF;
        break;
      }
    case PDF_Lognormal:
      {
        max = GSL_POSINF;
        break;
      }
    case PDF_NegativeBinomial:
      {
        max = GSL_POSINF;
        break;
      }
    case PDF_Pareto:
      {
        max = GSL_POSINF;
        break;
      }
    case PDF_Bernoulli:
      {
        PDF_bernoulli_dist_t *d;
        d = &(dist->u.bernoulli);
        if( 0.0 == d->p )
          max = 0.0;
        else
          max = 1.0;
        break; 
      }
    case PDF_Binomial:
      {
        PDF_binomial_dist_t *d;
        d = &(dist->u.binomial);
        max = d->n;
        break;
      }
    case PDF_Discrete_Uniform:
      {
        PDF_discrete_uniform_dist_t *d;
        d = &(dist->u.discrete_uniform);
        max = d->max;
        break;
      }
    case PDF_Hypergeometric:
      {
        PDF_hypergeometric_dist_t *d;
        d = &(dist->u.hypergeometric);
        max = gsl_min (d->t, d->n1);
        break;
      }
    default:
      g_assert_not_reached ();
    }

  return max;
}

/**
 * Does the PDF have a mean?
 *
 * @param dist a distribution.
 * @return TRUE if this PDF has a mean, FALSE if the PDF does not have a mean.
 */
gboolean
PDF_has_mean (PDF_dist_t * dist)
{
  switch(dist->type)
    {
    case PDF_Point:
    case PDF_Uniform:
    case PDF_Triangular:
    case PDF_Histogram:
    case PDF_Gaussian:
    case PDF_Inverse_Gaussian:
    case PDF_Poisson:
    case PDF_Beta:
    case PDF_Gamma:
    case PDF_Weibull:
    case PDF_Exponential:
    case PDF_Logistic:
    case PDF_Lognormal:
    case PDF_NegativeBinomial:
    case PDF_Bernoulli:
    case PDF_Binomial:
    case PDF_Discrete_Uniform:
    case PDF_Hypergeometric:
      {
        return TRUE;
      }
    case PDF_Pearson5:
      {
        PDF_pearson5_dist_t *d;
        d = &(dist->u.pearson5);
        if (1.0 >= d->alpha)
          {
             return FALSE;
          }
        else
          {
            return TRUE;
          }
      }
    case PDF_LogLogistic:
      {
        PDF_loglogistic_dist_t *d;

        d = &(dist->u.loglogistic);
        if (1.0 >= d->shape)
          {
            return FALSE;
          }
        else
          {
            return TRUE;
          }
      }
    case PDF_Pareto:
      {
        PDF_pareto_dist_t *d;
        d = &(dist->u.pareto);
        if (1.0 >= d->theta)
          {
            return FALSE;
          }
        else
          {
            return TRUE;
          }
      }
    case PDF_Piecewise:
      {
        /* TODO. */
        return FALSE;
      }
    default:
      g_assert_not_reached ();
    }
}

/**
 * The mean of this PDF
 *
 * @param dist a distribution.
 * @return the mean for this PDF if there is one, GSL_NAN if none can be computed.
 */
double
PDF_mean (PDF_dist_t * dist)
{
  double mean;

  switch (dist->type)
    {
    case PDF_Point:
      {
        PDF_point_dist_t *d;
        d = &(dist->u.point);
        mean = d->value;
        break;
      }
    case PDF_Uniform:
      {
        PDF_uniform_dist_t *d;
        d = &(dist->u.uniform);
        mean = (d->a + d->b) / 2.0;
        break;
      }
    case PDF_Triangular:
      {
        PDF_triangular_dist_t *d;
        d = &(dist->u.triangular);
        mean = (d->a + d->b + d->c) / 3.0;
        break;
      }
    case PDF_Piecewise:
      {
        PDF_piecewise_dist_t *d;
        d = &(dist->u.piecewise);
        /* TODO */
        mean = GSL_NAN;
        break;
      }
    case PDF_Histogram:
      {
        PDF_histogram_dist_t *d;
        d = &(dist->u.histogram);
        mean = gsl_histogram_mean (d->histo);
        break;
      }
    case PDF_Gaussian:
      {
        PDF_gaussian_dist_t *d;
        d = &(dist->u.gaussian);
        mean = d->mu;
        break;
      }
    case PDF_Inverse_Gaussian:
      {
        PDF_inverse_gaussian_dist_t *d;
        d = &(dist->u.inverse_gaussian);
        mean = d->mu;
        break;
      }
    case PDF_Poisson:
      {
        PDF_poisson_dist_t *d;
        d = &(dist->u.poisson);
        mean = d->mu;
        break;
      }
    case PDF_Beta:
      {
        PDF_beta_dist_t *d;
        d = &(dist->u.beta);
        mean = d->location + (d->alpha / (d->alpha + d->beta)) * (d->scale - d->location);
        break;
      }
    case PDF_Gamma:
      {
        PDF_gamma_dist_t *d;
        d = &(dist->u.gamma);
        mean = d->alpha * d->beta;
        break;
      }
    case PDF_Weibull:
      {
        PDF_weibull_dist_t *d;
        d = &(dist->u.weibull);
        mean = (d->beta / d->alpha) * gsl_sf_gamma (1.0 + 1.0 / d->alpha);
        break;
      }
    case PDF_Exponential:
      {
        PDF_exponential_dist_t *d;
        d = &(dist->u.exponential);
        mean = d->mean;
        break;
      }
    case PDF_Pearson5:
      {
        PDF_pearson5_dist_t *d;
        d = &(dist->u.pearson5);
        if (1.0 >= d->alpha)
          {
            /* Cannot compute mean for alpha <= 1. */
            mean = GSL_NAN;
          }
        else
          {
            mean = d->beta / (d->alpha - 1.0);
          }
        break;
      }
    case PDF_Logistic:
      {
        PDF_logistic_dist_t *d;
        d = &(dist->u.logistic);
        mean = d->location;
        break;
      }
    case PDF_LogLogistic:
      {
        PDF_loglogistic_dist_t *d;
        d = &(dist->u.loglogistic);
        if (1.0 >= d->shape)
          {
            /* Cannot compute mean for shape <= 1.0. */
            mean = GSL_NAN;
          }
        else
          {
            double theta;
            theta = M_PI / d->shape;
            mean = d->location + ( d->scale * theta / sin( theta ) );
          }
        break;
      }
    case PDF_Lognormal:
      {
        PDF_lognormal_dist_t *d;
        d = &(dist->u.lognormal);
        mean = exp(d->zeta + d->sigma * d->sigma / 2.0);
        break;
      }
    case PDF_NegativeBinomial:
      {
        PDF_negative_binomial_dist_t *d;
        d = &(dist->u.negative_binomial);
        mean = d->s * (1.0 - d->p) / d->p;
        break;
      }
    case PDF_Pareto:
      {
        PDF_pareto_dist_t *d;
        d = &(dist->u.pareto);
        if (1.0 >= d->theta)
          {
            /* Cannot compute mean for theta <= 1.0. */
            mean = GSL_NAN;
          }
        else
          {
            mean = d->a * d->theta / (d->theta - 1.0);
          }
        break;
      }
    case PDF_Bernoulli:
      {
        PDF_bernoulli_dist_t *d;
        d = &(dist->u.bernoulli);
        mean = d->p;
        break;  
      }
    case PDF_Binomial:
      {
        PDF_binomial_dist_t *d;
        d = &(dist->u.binomial);
        mean = d->n * d->p;
        break;
      }
    case PDF_Discrete_Uniform:
      {
        PDF_discrete_uniform_dist_t *d;
        d = &(dist->u.discrete_uniform);
        mean = ((double) (d->max + d->min)) / 2.0;
        break;
      }
      break;
    case PDF_Hypergeometric:
      {
        PDF_hypergeometric_dist_t *d;
        d = &(dist->u.hypergeometric);
        mean = ((double) (d->t * d->n1)) / (double) (d->n1 + d->n2);
        break;
      }
    default:
      g_assert_not_reached ();
    }

  return mean;
}

/**
 * Does the PDF have a variance?
 *
 * @param dist a distribution.
 * @return TRUE if this PDF has a variance, FALSE if the PDF does not have a variance.
 */
gboolean
PDF_has_variance (PDF_dist_t * dist)
{
  switch(dist->type)
    {
    case PDF_Point:
    case PDF_Uniform:
    case PDF_Triangular:
    case PDF_Gaussian:
    case PDF_Inverse_Gaussian:
    case PDF_Poisson:
    case PDF_Beta:
    case PDF_Gamma:
    case PDF_Weibull:
    case PDF_Exponential:
    case PDF_Logistic:
    case PDF_Lognormal:
    case PDF_NegativeBinomial:
    case PDF_Binomial:
    case PDF_Bernoulli:
    case PDF_Discrete_Uniform:
      {
        return TRUE;
      }
    case PDF_Pearson5:
      {
        PDF_pearson5_dist_t *d;
        d = &(dist->u.pearson5);
        if (2.0 >= d->alpha)
          {
            return FALSE;
          }
        else
          {
            return TRUE;
          }
      }
    case PDF_LogLogistic:
      {
        PDF_loglogistic_dist_t *d;
        d = &(dist->u.loglogistic);
        if (2.0 >= d->shape)
          {
            return FALSE;
          }
        else
          {
            return TRUE;
          }
      }
    case PDF_Pareto:
      {
        PDF_pareto_dist_t *d;
        d = &(dist->u.pareto);
        if (2.0 >= d->theta)
          {
            return FALSE;
          }
        else
          {
            return TRUE;
          }
      }
    case PDF_Hypergeometric:
      {
  PDF_hypergeometric_dist_t *d;
  d = &(dist->u.hypergeometric);
  if (1.0 >= (d->n1 + d->n2))
    {
      return FALSE;
    }
  else
    {
      return TRUE;
    }
      }
      break;
    case PDF_Piecewise:
    case PDF_Histogram:
      {
        /* TODO. */
        return FALSE;
      }
    default:
      g_assert_not_reached ();
    }
}

/**
 * The variance of this PDF
 *
 * @param dist a distribution.
 * @return the variance for this PDF if there is one, GSL_NAN if none can be computed.
 */
double
PDF_variance (PDF_dist_t * dist)
{
  double variance;

  switch (dist->type)
    {
    case PDF_Point:
      {
        PDF_point_dist_t *d;
        d = &(dist->u.point);
        variance = 0.0;
        break;
      }
    case PDF_Uniform:
      {
        PDF_uniform_dist_t *d;
        d = &(dist->u.uniform);
        variance = gsl_pow_2 (d->b - d->a) / 12.0;
        break;
      }
    case PDF_Triangular:
      {
        PDF_triangular_dist_t *d;
        d = &(dist->u.triangular);
        variance =
          (gsl_pow_2 (d->a) + gsl_pow_2 (d->b) + gsl_pow_2 (d->c)
           - d->a * d->b - d->a * d->c - d->b * d->c) / 18.0;
        break;
      }
    case PDF_Piecewise:
      {
        PDF_piecewise_dist_t *d;
        d = &(dist->u.piecewise);
        /* TODO */
        variance = GSL_NAN;
        break;
      }
    case PDF_Histogram:
      {
        PDF_histogram_dist_t *d;
        d = &(dist->u.histogram);
        /* FIX ME.  The value that this spits out does not seem like a
         * close match to what a sizable random sample produces for
         * the test case. */
        variance = gsl_pow_2 (gsl_histogram_sigma (d->histo));
        break;
      }
    case PDF_Gaussian:
      {
        PDF_gaussian_dist_t *d;
        d = &(dist->u.gaussian);
        variance = gsl_pow_2 (d->sigma);
        break;
      }
    case PDF_Inverse_Gaussian:
      {
        PDF_inverse_gaussian_dist_t *d;
        d = &(dist->u.inverse_gaussian);
        variance = gsl_pow_3 (d->mu) / d->lambda;
        break;
      }
    case PDF_Poisson:
      {
        PDF_poisson_dist_t *d;
        d = &(dist->u.poisson);
        variance = d->mu;
        break;
      }
    case PDF_Beta:
      {
        PDF_beta_dist_t *d;
        d = &(dist->u.beta);
        variance =
          (d->alpha * d->beta /
           (gsl_pow_2 (d->alpha + d->beta) *
           (d->alpha + d->beta + 1.0))) *
           gsl_pow_2 (d->scale - d->location);
        break;
      }
    case PDF_Gamma:
      {
        PDF_gamma_dist_t *d;
        d = &(dist->u.gamma);
        variance = gsl_pow_2 (d->beta) * d->alpha;
        break;
      }
    case PDF_Weibull:
      {
        PDF_weibull_dist_t *d;
        d = &(dist->u.weibull);
        variance =
          gsl_pow_2 (d->beta) *
          (gsl_sf_gamma (1.0 + 2.0 / d->alpha) -
           gsl_pow_2 (gsl_sf_gamma (1.0 + 1.0 / d->alpha)));
        break;
      }
    case PDF_Exponential:
      {
        PDF_exponential_dist_t *d;
        d = &(dist->u.exponential);
        variance = gsl_pow_2 (d->mean);
        break;
      }
    case PDF_Pearson5:
      {
        PDF_pearson5_dist_t *d;
        d = &(dist->u.pearson5);
        if (2.0 >= d->alpha)
          {
            /* Cannot compute variance for alpha <= 2. */
            variance = GSL_NAN;
          }
        else
          {
            variance =
              d->beta * d->beta /
              (gsl_pow_2 (d->alpha - 1.0) * (d->alpha - 2.0));
          }
        break;
      }
    case PDF_Logistic:
      {
        PDF_logistic_dist_t *d;
        d = &(dist->u.logistic);
        variance = gsl_pow_2 (M_PI * d->scale) / 3.0;
        break;
      }
    case PDF_LogLogistic:
      {
        PDF_loglogistic_dist_t *d;
        d = &(dist->u.loglogistic);
        if (2.0 >= d->shape)
          {
            /* Cannot compute variance for shape <= 2.0. */
            variance = GSL_NAN;
          }
        else
          {
            const double theta = M_PI / d->shape;
            const double csc_theta = 1.0 / sin(theta);
            const double csc_2theta = 1.0 / sin(2.0 * theta);
            variance =
              d->scale * d->scale * theta *
              (2.0 * csc_2theta - theta * csc_theta * csc_theta);
          }
        break;
      }
    case PDF_Lognormal:
      {
        PDF_lognormal_dist_t *d;
        d = &(dist->u.lognormal);
        {
          double omega = exp(gsl_pow_2 (d->sigma));
          variance = exp(2.0 * d->zeta) * omega * (omega - 1.0);
        }
        break;
      }
    case PDF_NegativeBinomial:
      {
        PDF_negative_binomial_dist_t *d;
        d = &(dist->u.negative_binomial);
        variance = d->s * (1.0 - d->p) / gsl_pow_2 (d->p);
        break;
      }
    case PDF_Pareto:
      {
        PDF_pareto_dist_t *d;
        d = &(dist->u.pareto);
        if (2.0 >= d->theta)
          {
            /* Cannot compute variance for theta <= 2.0. */
            variance = GSL_NAN;
          }
        else
          {
            variance =
              d->theta * gsl_pow_2 (d->a) /
              (gsl_pow_2 (d->theta - 1.0) * (d->theta - 2.0));
          }
        break;
      }
    case PDF_Bernoulli:
      {
        PDF_bernoulli_dist_t *d;
        d = &(dist->u.bernoulli);
        variance = (d->p)*(1 - d->p);
        break;  
      }
    case PDF_Binomial:
      {
        PDF_binomial_dist_t *d;
        d = &(dist->u.binomial);
        variance = (double) d->n * d->p * (1.0 - d->p);
        break;
      }
    case PDF_Discrete_Uniform:
      {
        PDF_discrete_uniform_dist_t *d;
        d = &(dist->u.discrete_uniform);
        int range = d->max - d->min + 1;
        variance = (gsl_pow_2 (range) - 1.0) / 12.0;
        break;
      }
    case PDF_Hypergeometric:
      {
        PDF_hypergeometric_dist_t *d;
        d = &(dist->u.hypergeometric);
        int D = d->n1;
        int M = d->n1 + d->n2;
        int n = d->t;
        if (1 >= M)
          {
            /* Cannot compute variance for M <= 1.0. */
            variance = GSL_NAN;
          }
        else
          {
            variance = ((double) (n * D * (M - D ) * (M - n))) / (double) (gsl_pow_2 (M) * (M - 1));
          }
        break;
      }
    default:
      g_assert_not_reached ();
    }

  return variance;
}



/**
 * Does the PDF have a skewness?
 *
 * @param dist a distribution.
 * @return TRUE if this PDF has a skewness, FALSE if the PDF does not have a skewness.
 */
gboolean
PDF_has_skewness (PDF_dist_t * dist)
{
  gboolean answer;

  switch(dist->type)
    {
    case PDF_Point:
    case PDF_Triangular:
    case PDF_Weibull:
    case PDF_Gaussian:
    case PDF_Gamma:
      {
        answer = TRUE;
        break;
      }
    case PDF_Uniform:
    case PDF_Inverse_Gaussian:
    case PDF_Poisson:
    case PDF_Beta:
    case PDF_Exponential:
    case PDF_Logistic:
    case PDF_Lognormal:
    case PDF_NegativeBinomial:
    case PDF_Binomial:
    case PDF_Bernoulli:
    case PDF_Discrete_Uniform:
    case PDF_Pearson5:
    case PDF_LogLogistic:
    case PDF_Pareto:
    case PDF_Hypergeometric:
    case PDF_Piecewise:
    case PDF_Histogram:
      {
        answer = FALSE;
        break;
      }
    default:
      g_assert_not_reached ();
    }

  return answer;
}

/**
 * The skewness of this PDF
 *
 * @param dist a distribution.
 * @return the skewness for this PDF if there is one, GSL_NAN if none can be computed.
 */
double
PDF_skewness (PDF_dist_t * dist)
{
  double skewness;

  switch (dist->type)
    {
    case PDF_Point:
      {
        skewness = 0;
        break;
      }
    case PDF_Triangular:
      {
        PDF_triangular_dist_t *d;
        double a,b,c;
        d = &(dist->u.triangular);
        a = d->a;
        b = d->b;
        c = d->c;
        /* Formula found on Wikipedia */
        skewness = (M_SQRT2 * (a+b-2*c) * (2*a-b-c) * (a-2*b+c)) /
          (5 * pow (gsl_pow_2(a) + gsl_pow_2(b) + gsl_pow_2(c) - a*b - a*c - b*c, 1.5));
        break;
      }
    case PDF_Weibull:
      {
        PDF_weibull_dist_t *d;
        double alpha, beta;
        double mean, variance;
        d = &(dist->u.weibull);
        alpha = d->alpha;
        beta = d->beta;
        /* Formula found on Wikipedia. Correspondence to Wikipedia version:
         * "alpha" here = k (the "shape parameter") on Wikipedia
         * "beta" here = lambda (the "scale parameter") on Wikipedia */
        mean = PDF_mean( dist );
        variance = PDF_variance( dist );
        skewness = (gsl_sf_gamma(1.0+3.0/alpha)*gsl_pow_3(beta) - 3.0*mean*gsl_pow_2(variance) - gsl_pow_3(mean)) /
          gsl_pow_3(variance);
        break;
      }
    case PDF_Gaussian:
      {
        skewness = 0;
        break;
      }
    case PDF_Gamma:
      {
        PDF_gamma_dist_t *d;
        d = &(dist->u.gamma);
        /* Formula found on Wikipedia. Correspondence to Wikipedia version:
         * "alpha" here = k (the "shape parameter") on Wikipedia
         * "beta" here = theta (the "scale parameter") on Wikipedia */
        skewness = 2.0/sqrt( d->alpha );
        break;
      }
    case PDF_Uniform:
    case PDF_Piecewise:
    case PDF_Histogram:
    case PDF_Inverse_Gaussian:
    case PDF_Poisson:
    case PDF_Beta:
    case PDF_Exponential:
    case PDF_Pearson5:
    case PDF_Logistic:
    case PDF_LogLogistic:
    case PDF_Lognormal:
    case PDF_NegativeBinomial:
    case PDF_Pareto:
    case PDF_Bernoulli:
    case PDF_Binomial:
    case PDF_Discrete_Uniform:
    case PDF_Hypergeometric:
      g_assert_not_reached ();
    default:
      g_assert_not_reached ();
    }

  return skewness;
}

/* end of file prob_dist.c */
