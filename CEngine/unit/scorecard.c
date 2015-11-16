/** @file scorecard.c
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


#if HAVE_CONFIG_H
#  include <config.h>
#endif

#include <unistd.h>
#include <stdio.h>
#include "scorecard.h"

#if STDC_HEADERS
#  include <stdlib.h>
#  include <string.h>
#endif

#if HAVE_STRINGS_H
#  include <strings.h>
#endif

#if HAVE_CTYPE_H
#  include <ctype.h>
#endif

#if HAVE_MATH_H
#  include <math.h>
#endif

#if HAVE_ERRNO_H
#  include <errno.h>
#endif

#define EPSILON 0.01 /* for distance comparisons = 10 m */



USC_scorecard_t *
USC_new_scorecard (UNT_unit_t *unit)
{
  USC_scorecard_t *self;

  self = g_new(USC_scorecard_t, 1);
  self->unit = unit;
  self->vaccination_requests = g_queue_new ();
  USC_scorecard_reset (self);

  return self;
}



/**
 * Returns a pointer to the oldest vaccination request recorded in the
 * scorecard. Does not remove the request from the scorecard. The request
 * object must not be modified or freed by the caller.
 */ 
EVT_event_t *
USC_scorecard_vaccination_request_peek_oldest (USC_scorecard_t *self)
{
  return (EVT_event_t *) g_queue_peek_head (self->vaccination_requests);
}



/**
 * Removes the oldest vaccination request recorded in the scorecard and returns
 * it. Freeing the request object becomes the responsibility of the caller.
 */ 
EVT_event_t *
USC_scorecard_vaccination_request_pop_oldest (USC_scorecard_t *self)
{
  EVT_event_t *request;
  request = (EVT_event_t *) g_queue_pop_head (self->vaccination_requests);
  #if DEBUG
    g_debug ("scorecard \"%s\" pop: now %u vaccination requests in scorecard",
             self->unit->official_id, g_queue_get_length (self->vaccination_requests));
  #endif
  if (g_queue_is_empty (self->vaccination_requests))
    {
      /* Call the clear vaccination requests function to reset all the other
       * variables that go along with having active vaccination requests. */
      USC_scorecard_clear_vaccination_requests (self);
    }
  return request;
}



/**
 * Returns a pointer to the newest vaccination request recorded in the
 * scorecard. Does not remove the request from the scorecard. The request
 * object must not be modified or freed by the caller.
 */ 
EVT_event_t *
USC_scorecard_vaccination_request_peek_newest (USC_scorecard_t *self)
{
  return (EVT_event_t *) g_queue_peek_tail (self->vaccination_requests);
}



void
USC_scorecard_clear_vaccination_requests (USC_scorecard_t *self)
{
  while (!g_queue_is_empty (self->vaccination_requests))
    EVT_free_event ((EVT_event_t *) g_queue_pop_head (self->vaccination_requests));
  self->is_awaiting_vaccination = FALSE;
  self->is_in_suppressive_ring = FALSE;
  self->unit_at_vacc_ring_center = NULL;
  self->distance_from_vacc_ring_center = -1;
  self->distance_from_vacc_ring_inside = -1;
  self->distance_from_vacc_ring_outside = -1;
  return;
}



void
USC_free_scorecard (USC_scorecard_t *self)
{
  if (self != NULL)
    {
      USC_scorecard_clear_vaccination_requests (self);
      g_queue_free (self->vaccination_requests);
      g_free (self);
    }
}



void
USC_free_scorecard_as_GDestroyNotify (gpointer data)
{
  USC_free_scorecard ((USC_scorecard_t *) data);
}



char *
USC_scorecard_to_string (USC_scorecard_t *self)
{
  GString *s;

  s = g_string_new ("<scorecard");
  g_string_append_printf (s, " for unit \"%s\"", self->unit->official_id);
  if (self->is_awaiting_vaccination)
    {
      GList *iter;
      gboolean first;
      g_string_append_printf (s, " requests=[");
      first = TRUE;
      for (iter = g_queue_peek_head_link (self->vaccination_requests);
           iter != NULL;
           iter = g_list_next (iter))
        {
          char *chararray;
          chararray = EVT_event_to_string ((EVT_event_t *)(iter->data));
          g_string_append_printf (s, first ? "%s" : ",%s", chararray);
          first = FALSE;
          g_free (chararray);
        }
      g_string_append_c (s, ']');
	}
  g_string_append_c (s, '>');

  /* don't return the wrapper object */
  return g_string_free (s, FALSE);
}



int
USC_fprintf_scorecard (FILE *stream, USC_scorecard_t *self)
{
  char *s = NULL;
  int nchars_written = 0;

  #if DEBUG
    g_debug ("----- ENTER USC_fprintf_scorecard");
  #endif

  if (!stream)
    stream = stdout;

  s = USC_scorecard_to_string (self);
  nchars_written = fprintf (stream, "%s", s);
  g_free (s);

  #if DEBUG
    g_debug ("----- EXIT USC_fprintf_scorecard");
  #endif

  return nchars_written;
}



void
USC_scorecard_reset (USC_scorecard_t *self)
{
  USC_scorecard_clear_vaccination_requests (self);

  self->is_detected_as_diseased = FALSE;
  self->day_detected_as_diseased = -1;
}



/**
 * Records a request for vaccination. This function makes a copy of the
 * request object so the original can be modified or freed after the call to
 * this function.
 *
 * @param self this scorecard
 * @param event a request for vaccination event
 */
void
USC_scorecard_register_vaccination_request (USC_scorecard_t *self,
                                            EVT_event_t *event)
{
  EVT_event_t *clone;
  EVT_request_for_vaccination_event_t *event_details; 

  g_assert (event->type == EVT_RequestForVaccination);
  /* The reason for vaccination will come in as "suppressive ring" or
   * "protective ring". For the copy of the request for vaccination that we
   * store in the scorecard, just set it to "ring". This is so that we don't
   * need to worry about the distinction between the two types of rings in the
   * output variables yet. */
  clone = EVT_clone_event (event);
  clone->u.request_for_vaccination.reason = ADSM_ControlRing;
  g_queue_push_tail (self->vaccination_requests, clone);
  event_details = &(event->u.request_for_vaccination);
  #if DEBUG
    g_debug ("scorecard for unit \"%s\" register request: now %u vaccination requests in scorecard",
             self->unit->official_id, g_queue_get_length (self->vaccination_requests));
  #endif
  self->is_awaiting_vaccination = TRUE;
  self->is_in_suppressive_ring = (self->is_in_suppressive_ring || 
    event_details->reason == ADSM_ControlSuppressiveRing);

  /* For the purpose of round-robin prioritization, a unit is set to "belong"
   * to one particular vaccination ring, defined by the ring in which the unit
   * is closest to the center. We don't check that here though, that is handled
   * in the USC_scorecard_register_vaccination_ring function.*/

  /* For the purpose of outside-in or inside-out priority order, a unit is
   * assigned the lowest priority it would get from any ring that it is in.
   * We don't check that here though, that is handled in the
   * USC_scorecard_register_vaccination_ring function. */

  return;
}



/**
 * Checks whether a new vaccination ring changes the outside-in or inside-out
 * priority order.
 *
 * @param self this scorecard
 * @param ring the new vaccination ring.
 */
void
USC_scorecard_register_vaccination_ring (USC_scorecard_t *self,
                                         USC_vaccination_ring_t *ring)
{
  double distance;
  double ring_radius;
  #if DEBUG
    GString *s;
  #endif

  #if DEBUG
    g_debug ("scorecard for unit \"%s\" register ring", self->unit->official_id);
  #endif

  /* For the purpose of round-robin prioritization, a unit is set to "belong"
   * to one particular vaccination ring, defined by the ring in which the unit
   * is closest to the center. */
  #if DEBUG
    s = g_string_new (NULL);
    if (self->distance_from_vacc_ring_center < 0)
      g_string_append_printf (s, "unit \"%s\" does not currently belong to a ring (distance=%g)",
                              self->unit->official_id,
                              self->distance_from_vacc_ring_center);
    else
      g_string_append_printf (s, "unit \"%s\" currently belongs to ring around unit \"%s\" (distance=%g)",
                              self->unit->official_id,
                              self->unit_at_vacc_ring_center->official_id,
                              self->distance_from_vacc_ring_center);
  #endif
  distance = GIS_distance (self->unit->x, self->unit->y,
                           ring->unit_at_center->x, ring->unit_at_center->y);
  ring_radius = MAX (ring->supp_radius, ring->prot_outer_radius);
  if (distance <= ring_radius + EPSILON
      && (self->distance_from_vacc_ring_center < 0
          || self->distance_from_vacc_ring_center > distance))
    {
      self->unit_at_vacc_ring_center = ring->unit_at_center;
      self->distance_from_vacc_ring_center = distance;
      #if DEBUG
        g_string_append_printf (s, ", new distance %g puts unit in ring around unit \"%s\"",
                                distance,
                                self->unit_at_vacc_ring_center->official_id);
      #endif
    }
  else
    {
      #if DEBUG
        g_string_append_printf (s, ", new distance %g does not change ring membership",
                                distance);
      #endif
      ;
    }
  #if DEBUG
    g_debug ("%s (for round-robin)", s->str);
    g_string_free (s, TRUE);
  #endif

  /* For the purpose of outside-in or inside-out priority order, a unit is
   * assigned the lowest priority it would get from any ring that it is in.
   * Each time a new vaccination ring is created, it may change the prioity
   * order for this unit. */

  /* 5 combinations to take care of:
   * 1. unit already in suppressive ring, new ring does not have a suppressive part
   * 2. unit already in suppressive ring, new ring has a suppressive part
   * - unit not already in suppressive ring, new ring is suppressive-only
   * - unit not already in suppressive ring, new ring is protective-only
   * - unit not already in suppressive ring, new ring has both suppressive and protective parts */
  if (self->is_in_suppressive_ring)
    {
      #if DEBUG
        g_debug ("unit \"%s\" is in 1+ suppressive rings already", self->unit->official_id);
      #endif
      if (ring->supp_radius < 0)
        {
          /* Combination 1: unit already in suppressive ring, new ring does not
           * have a suppressive part. */
          g_debug ("this ring is protective only, cannot affect outside-in order for suppressive");
        }
      else
        {
          /* Combination 2: unit already in suppressive ring, new ring has a
           * suppressive part. */
          #if DEBUG
            g_debug ("checking against ring (%.2f) around unit \"%s\", distance from center=%.2f",
                     ring->supp_radius,
                     ring->unit_at_center->official_id, distance);
          #endif
          if (distance > (ring->supp_radius + EPSILON))
            {
              ; /* do nothing */
            }
          else
            {
              /* Take the largest possible distance from a ring's outer edge, that
               * is, the lowest priority this unit could have according to any ring
               * it is in.  Note that this "if" condition also takes care of the
               * case when this is the first vaccination ring we have looked at,
               * since distance_from_vacc_ring_outside is initialized to a negative
               * value and thus any positive distance will be greater than the old
               * stored value.
               *
               * Take the smallest possible distance from a ring's inner edge,
               * that is, the highest priority this unit could have according to
               * any ring it is in.
               *
               * Note that we also override any settings to DBL_MAX, which indicated
               * this unit was previously inside the hole of a protective ring. */
               double distance_from_outside, distance_from_inside;
               #if DEBUG
                 double old_distance_from_outside, old_distance_from_inside;
                 GString *s;
               #endif
               distance_from_outside = ring->supp_radius - distance;
               #if DEBUG
                 s = g_string_new (NULL);
                 g_string_append_printf (s, "distance from outside=%g", distance_from_outside);
                 old_distance_from_outside = self->distance_from_vacc_ring_outside;
               #endif
               if (self->distance_from_vacc_ring_outside == DBL_MAX
                   || distance_from_outside > self->distance_from_vacc_ring_outside)
                 {
                   self->distance_from_vacc_ring_outside = distance_from_outside;
                   #if DEBUG
                     g_string_append_printf (s, ", overrides old distance %g", old_distance_from_outside);
                   #endif
                 }
               else
                 {
                   #if DEBUG
                     g_string_append_printf (s, ", does not override old distance %g", old_distance_from_outside);
                   #endif
                   ;
                 }
               #if DEBUG
                 g_debug ("%s", s->str);
                 g_string_truncate (s, 0);
               #endif

               distance_from_inside = distance;
               #if DEBUG
                 g_string_append_printf (s, "distance from inside=%g", distance_from_inside);
                 old_distance_from_inside = self->distance_from_vacc_ring_inside;
               #endif
               if (self->distance_from_vacc_ring_inside == DBL_MAX
                   || self->distance_from_vacc_ring_inside < 0
                   || distance_from_inside < self->distance_from_vacc_ring_inside)
                 {
                   self->distance_from_vacc_ring_inside = distance_from_inside;
                   #if DEBUG
                     g_string_append_printf (s, ", overrides old distance %g", old_distance_from_inside);
                   #endif
                 }
               else
                 {
                   #if DEBUG
                     g_string_append_printf (s, ", does not override old distance %g", old_distance_from_inside);
                   #endif
                   ;
                 }
               #if DEBUG
                 g_debug ("%s", s->str);
                 g_string_free (s, TRUE);
               #endif
            }
        }
    } /* end of case where unit was in 1+ suppressive rings already */

  else
    {
      #if DEBUG
        g_debug ("unit \"%s\" is in only protective ring(s)", self->unit->official_id);
      #endif
      /* First check whether distance from the outside edge is already set to
       * DBL_MAX. That indicates the unit is in a do-not-vaccinate situation
       * (inside the hole of another protective ring). */
      if (self->distance_from_vacc_ring_outside >= DBL_MAX)
        {
          #if DEBUG
            g_debug ("unit \"%s\" is already inside the hole of a protective ring", self->unit->official_id);
          #endif
          ;
        }
      else
        {
          #if DEBUG
            g_debug ("checking against ring (%.2f,%.2f) around unit \"%s\", distance from center=%.2f",
                     ring->prot_inner_radius, ring->prot_outer_radius,
                     ring->unit_at_center->official_id, distance);
          #endif
          if (distance > (ring->prot_outer_radius + EPSILON))
            {
              ; /* do nothing */
            }
          else if (distance < (ring->prot_inner_radius - EPSILON))
            {
              /* The unit is inside the hole of a protective vaccination ring. Mark
               * it as the largest possible distance from the edge, DBL_MAX,
               * meaning do not vaccinate. */
              self->distance_from_vacc_ring_outside = DBL_MAX;
              self->distance_from_vacc_ring_inside = DBL_MAX;
              #if DEBUG
                g_debug ("unit \"%s\" is inside the hole of this protective ring", self->unit->official_id);
              #endif
            }
          else
            {
              /* Take the largest possible distance from a ring's outer edge, that
               * is, the lowest priority this unit could have according to any ring
               * it is in.  Note that this "if" condition also takes care of the
               * case when this is the first vaccination ring we have looked at,
               * since distance_from_vacc_ring_outside is initialized to a negative
               * value and thus any positive distance will be greater than the old
               * stored value. Same for the distance from the ring's inner edge.*/
               double distance_from_outside, distance_from_inside;
               #if DEBUG
                 double old_distance_from_outside, old_distance_from_inside;
                 GString *s;
               #endif
               distance_from_outside = ring->prot_outer_radius - distance;
               #if DEBUG
                 s = g_string_new (NULL);
                 g_string_append_printf (s, "distance from outside=%g", distance_from_outside);
                 old_distance_from_outside = self->distance_from_vacc_ring_outside;
               #endif
               if (distance_from_outside > self->distance_from_vacc_ring_outside)
                 {
                   self->distance_from_vacc_ring_outside = distance_from_outside;
                   #if DEBUG
                     g_string_append_printf (s, ", overrides old distance %g", old_distance_from_outside);
                   #endif
                 }
               else
                 {
                   #if DEBUG
                     g_string_append_printf (s, ", does not override old distance %g", old_distance_from_outside);
                   #endif
                   ;
                 }
               #if DEBUG
                 g_debug ("%s", s->str);
                 g_string_truncate (s, 0);
               #endif

               distance_from_inside = distance - ring->prot_inner_radius;
               #if DEBUG
                 g_string_append_printf (s, "distance from inside=%g", distance_from_inside);
                 old_distance_from_inside = self->distance_from_vacc_ring_inside;
               #endif
               if (self->distance_from_vacc_ring_inside < 0
                   || distance_from_inside < self->distance_from_vacc_ring_inside)
                 {
                   self->distance_from_vacc_ring_inside = distance_from_inside;
                   #if DEBUG
                     g_string_append_printf (s, ", overrides old distance %g", old_distance_from_inside);
                   #endif
                 }
               else
                 {
                   #if DEBUG
                     g_string_append_printf (s, ", does not override old distance %g", old_distance_from_inside);
                   #endif
                   ;
                 }
               #if DEBUG
                 g_debug ("%s", s->str);
                 g_string_free (s, TRUE);
               #endif
            }
        }
    } /* end of case where the unit only in protective ring(s) */

  return;
}



gboolean
USC_record_detection_as_diseased (USC_scorecard_t *self, int day)
{
  gboolean result = FALSE;

  if (!self->is_detected_as_diseased)
    {
      self->is_detected_as_diseased = TRUE;
      self->day_detected_as_diseased = day;
      result = TRUE;
    }

  return result;
}

/* end of file scorecard.c */
