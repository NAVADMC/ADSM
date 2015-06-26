/** @file rel_chart.h
 * Relationship charts.
 *
 * Symbols from this module begin with REL_.
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
#ifndef REL_CHART_H
#define REL_CHART_H

#include <stdio.h>
#include <glib.h>
#include <gsl/gsl_spline.h>



/** A single-point relationship chart. */
typedef struct
{
  double value;
}
REL_point_chart_t;



/** A generic (2 or more points) relationship chart. */
typedef struct
{
  gsl_spline *spline;
  gsl_interp_accel *accelerator;
  double first_x; /** lowest x-coordinate */
  double last_x; /** highest x-coordinate */
  double min; /** lowest y-coordinate */
  double max; /** highest y-coordinate */
}
REL_generic_chart_t;



/** Relationship chart types in this module. */
typedef enum
{
  REL_Point, REL_Generic
}
REL_chart_type_t;



/** A supertype for all relationship charts. */
typedef struct
{
  REL_chart_type_t type;
  union
  {
    REL_point_chart_t point;
    REL_generic_chart_t generic;
  }
  u;
}
REL_chart_t;



/* Prototypes. */
REL_chart_t *REL_new_chart (double *x, double *y, size_t);
REL_chart_t *REL_new_point_chart (double);
void REL_free_chart (REL_chart_t *);
REL_chart_t * REL_clone_chart (REL_chart_t *);
char *REL_chart_to_string (REL_chart_t *);
int REL_fprintf_chart (FILE *, REL_chart_t *);

#define REL_printf_chart(C) REL_fprintf_chart(stdout,C)

double REL_chart_lookup (double, REL_chart_t *);
double REL_chart_max (REL_chart_t *);
double REL_chart_min (REL_chart_t *);
void REL_chart_get_domain (REL_chart_t *, double *min_x, double *max_x);
void REL_chart_set_domain (REL_chart_t *, double min_x, double max_x);
gboolean REL_chart_zero_at_left (REL_chart_t *, double *first_x);
gboolean REL_chart_zero_at_right (REL_chart_t *, double *last_x);

#endif /* !REL_CHART_H */
