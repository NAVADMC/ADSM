/** @file parameter.h
 * Interface for parameter.c.
 *
 * Symbols from this module begin with PAR_.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @version 0.1
 * @date March 2003
 *
 * Copyright &copy; University of Guelph, 2003-2006
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#ifndef PARAMETER_H
#define PARAMETER_H

#include "prob_dist.h"
#include "rel_chart.h"
#include <scew/scew.h>
#include <glib.h>



/* The generic type of all simulation control parameters. */
typedef scew_element const PAR_parameter_t;



/* Prototypes. */
double PAR_get_length (PAR_parameter_t *, gboolean * success);
double PAR_get_time (PAR_parameter_t *, gboolean * success);
double PAR_get_angle (PAR_parameter_t *, gboolean * success);
double PAR_get_frequency (PAR_parameter_t *, gboolean * success);
double PAR_get_probability (PAR_parameter_t *, gboolean * success);
double PAR_get_money (PAR_parameter_t *, gboolean * success);
PDF_dist_t *PAR_get_PDF (PAR_parameter_t *);
REL_chart_t *PAR_get_relationship_chart (PAR_parameter_t *);
gboolean PAR_get_boolean (PAR_parameter_t *, gboolean * success);
double PAR_get_unitless (PAR_parameter_t *, gboolean * success);
int PAR_get_unitless_int (PAR_parameter_t *, gboolean * success);
char *PAR_get_text (PAR_parameter_t *);

#endif /* !PARAMETER_H */
