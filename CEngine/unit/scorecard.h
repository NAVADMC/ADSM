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
  gboolean is_in_suppressive_ring; /**< This field is used to decide whether
    the "hole-punching" effect of protective rings applies to this unit.  If
    the unit is in a suppressive ring, then the hole-punching effect does not
    apply. */
  GQueue *vaccination_requests; /**< New requests are added to the tail */
  UNT_unit_t *unit_at_vacc_ring_center; /**< The unit at the center of the
    vaccination ring this unit belongs to. The idea of "belonging" to a certain
    ring is used for round-robin prioritizing. */
  double distance_from_vacc_ring_center; /**< Distance from the center of the
    vaccination ring this unit belongs to. Used when a new vaccination ring is
    created, to decide whether the unit now belongs to the new ring. The idea
    of "belonging" to a certain ring is used for round-robin prioritizing. This
    field is set to a negative value when the unit is not part of any
    vaccination ring. */
  double distance_from_vacc_ring_inside; /**< Distance from the inner edge of
    the ring. Used for inside-out prioritization. This field is set to a
    negative value when the herd is not part of any vaccination ring. */
  double distance_from_vacc_ring_outside; /**< Distance from the outer edge of
    the ring. Used for outside-in prioritization. This field is set to a
    negative value when the herd is not part of any vaccination ring, and to
    DBL_MAX when the herd is inside the hole in a protective ring. */

  gboolean is_detected_as_diseased;
  int day_detected_as_diseased;
}
USC_scorecard_t;



/**
 * Data structure used in an argument to USC_scorecard_register_vaccination_request.
 */
typedef struct
{
  UNT_unit_t *unit_at_center;
  double supp_radius; /**< -1 if no suppressive circle is defined */
  double prot_inner_radius; /**< -1 if no protective ring is defined */
  double prot_outer_radius; /**< -1 if no protective ring is defined */
}
USC_vaccination_ring_t;



/* Prototypes. */

USC_scorecard_t *USC_new_scorecard (UNT_unit_t *);
void USC_free_scorecard (USC_scorecard_t *);
void USC_free_scorecard_as_GDestroyNotify (gpointer);

char *USC_scorecard_to_string (USC_scorecard_t *);
int USC_fprintf_scorecard (FILE *, USC_scorecard_t *);
#define USC_printf_scorecard(S) USC_fprintf_scorecard(stdout,S)

void USC_scorecard_register_vaccination_request (USC_scorecard_t *,
                                                 EVT_event_t *);
void USC_scorecard_register_vaccination_ring (USC_scorecard_t *,
                                              USC_vaccination_ring_t *);
EVT_event_t *USC_scorecard_vaccination_request_peek_oldest (USC_scorecard_t *);
EVT_event_t *USC_scorecard_vaccination_request_pop_oldest (USC_scorecard_t *);
EVT_event_t *USC_scorecard_vaccination_request_peek_newest (USC_scorecard_t *);
void USC_scorecard_clear_vaccination_requests (USC_scorecard_t *);

void USC_scorecard_reset (USC_scorecard_t *);

gboolean USC_record_detection_as_diseased (USC_scorecard_t *, int day);

#endif /* !SCORECARD_H */
