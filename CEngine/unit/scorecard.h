/** @file scorecard.h
 * Administrative
 *
 * Symbols from this module begin with USC_.
 *
 * @author Anthony Schwickerath <Drew.Schwickerath@colostate.edu><br>
 *   Animal Population Health Institute<br>
 *   Colorado State University<br>
 *   Fort Collins, CO 80526-8117<br>
 *   USA
 *
 * @version 0.1
 * @date April 2009
 *
 * Copyright &copy; Colorado State University, 2009
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#ifndef SCORECARD_H
#define SCORECARD_H

#include <stdio.h>

#if STDC_HEADERS
#  include <stdlib.h>
#endif

#include <glib.h>
#include <event.h>
#include "gis.h"


/** The authorities' information for one unit. */
typedef struct
{
  UNT_unit_t *unit;
  gboolean is_awaiting_vaccination;
  GQueue *vaccination_requests; /**< New requests are added to the tail */
}
USC_scorecard_t;



/* Prototypes. */

USC_scorecard_t *USC_new_scorecard (UNT_unit_t *);
void USC_free_scorecard (USC_scorecard_t *);
void USC_free_scorecard_as_GDestroyNotify (gpointer);

char *USC_scorecard_to_string (USC_scorecard_t *);
int USC_fprintf_scorecard (FILE *, USC_scorecard_t *);
#define USC_printf_scorecard(S) USC_fprintf_scorecard(stdout,S)

void USC_scorecard_register_vaccination_request (USC_scorecard_t *,
                                                 EVT_event_t *);
EVT_event_t *USC_scorecard_vaccination_request_peek_oldest (USC_scorecard_t *);
EVT_event_t *USC_scorecard_vaccination_request_pop_oldest (USC_scorecard_t *);
EVT_event_t *USC_scorecard_vaccination_request_peek_newest (USC_scorecard_t *);
void USC_scorecard_clear_vaccination_requests (USC_scorecard_t *);

void USC_scorecard_reset (USC_scorecard_t *);

#endif /* !SCORECARD_H */
