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
#include <glib.h>
#include <sqlite3.h>



/* Prototypes. */
PDF_dist_t *PAR_get_PDF (sqlite3 *, guint id);
REL_chart_t *PAR_get_relchart (sqlite3 *, guint id);
gboolean PAR_get_boolean (sqlite3 *, char *query);
char *PAR_get_text (sqlite3 *, char *query);
gint PAR_get_int (sqlite3 *, char *query);

#endif /* !PARAMETER_H */
