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
  EVT_request_for_vaccination_event_t *event_details; 

  g_assert (event->type == EVT_RequestForVaccination);
  g_queue_push_tail (self->vaccination_requests, EVT_clone_event (event));
  event_details = &(event->u.request_for_vaccination);
  #if DEBUG
    g_debug ("scorecard for unit \"%s\" register request: now %u vaccination requests in scorecard",
             self->unit->official_id, g_queue_get_length (self->vaccination_requests));
  #endif
  self->is_awaiting_vaccination = TRUE;

  return;
}

/* end of file scorecard.c */
