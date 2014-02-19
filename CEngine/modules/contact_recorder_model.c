/** @file contact_recorder_model.c
 * Module that records direct and indirect contacts, and carries out traces
 * when requested.  This module would correspond in the real world to paper
 * records kept by producers, RFID tracking systems, etc.
 *
 * This module has two responsibilities, detailed in the sections below.
 *
 * <b>Collecting trace information</b>
 *
 * This module records exposures.  It can be set to record direct contacts,
 * indirect contacts, or both; it can also be set to record contacts involving
 * only certain production types, or contacts involving any production type.
 *
 * <b>Tracing</b>
 *
 * When this module hears an AttemptToTrace event, it finds units to which
 * the specified unit sent animals (direct contact) or products or material
 * (indirect contact).  This is tracing out.  This module also identifies units
 * which sent the specified unit animals or products or material.  This is
 * tracing in.  The module announces TraceResult events for any contacts it
 * finds.
 *
 * <b>Implementation notes</b>
 *
 * Because we want to quickly discover contacts <i>from</i> or <i>to</i> a
 * given unit, we maintain two linked lists for each unit.  The linked lists
 * store EVT_event_type_t objects, each of which records one exposure event.
 * The in-lists and out-lists share the exposure event objects. So when an
 * exposure event is no longer needed, it must be removed from the out-list
 * attached to its source unit <i>and</i> from the in-list attached to its
 * recipient unit before it is freed.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date July 2007
 *
 * Copyright &copy; University of Guelph, 2007-2008
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#if HAVE_CONFIG_H
#  include <config.h>
#endif

/* To avoid name clashes when multiple modules have the same interface. */
#define is_singleton contact_recorder_model_is_singleton
#define new contact_recorder_model_new
#define set_params contact_recorder_model_set_params
#define run contact_recorder_model_run
#define reset contact_recorder_model_reset
#define events_listened_for contact_recorder_model_events_listened_for
#define is_listening_for contact_recorder_model_is_listening_for
#define has_pending_actions contact_recorder_model_has_pending_actions
#define has_pending_infections contact_recorder_model_has_pending_infections
#define to_string contact_recorder_model_to_string
#define local_printf contact_recorder_model_printf
#define local_fprintf contact_recorder_model_fprintf
#define local_free contact_recorder_model_free
#define handle_new_day_event contact_recorder_model_handle_new_day_event
#define handle_exposure_event contact_recorder_model_handle_exposure_event
#define handle_attempt_to_trace_event contact_recorder_model_handle_attempt_to_trace_event

#include "module.h"
#include "module_util.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#if HAVE_STRINGS_H
#  include <strings.h>
#endif

#if HAVE_MATH_H
#  include <math.h>
#endif

#include "contact_recorder_model.h"

#include "spreadmodel.h"

#if !HAVE_ROUND && HAVE_RINT
#  define round rint
#endif

double round (double x);

/** This must match an element name in the DTD. */
#define MODEL_NAME "contact-recorder-model"



#define NEVENTS_LISTENED_FOR 3
EVT_event_type_t events_listened_for[] = { EVT_Exposure, EVT_AttemptToTrace,
  EVT_NewDay };



/* Specialized information for this model. */
typedef struct
{
  GPtrArray *production_types; /**< Each item in the list is a char *. */
  int trace_period;            /**< Number of days back we are interesting in tracing back. */
  double *trace_success[SPREADMODEL_NCONTACT_TYPES]; /**< Probability of tracing a
    contact.  Use an expression of the form
    trace_success[contact_type][source_production_type]
    to get a particular value.  A negative number means "we don't record these
    contacts". */
  PDF_dist_t **trace_delay[SPREADMODEL_NCONTACT_TYPES]; /**< Number of days that a
    trace takes.  Use an expression of the form
    trace_delay[contact_type][source_production_type]
    to get a particular distribution. */
  GQueue **trace_out; /* Lists of exposures originating <i>from</i> a unit.
    The array contains one GQueue for each unit.  Each node of a GQueue stores
    a pointer to an Exposure event.  The newest exposures are at the head of
    the queue.  The Exposure event objects are shared with trace_in. */
  GQueue **trace_in;            /* Lists of exposures going <i>to</i> each
                                   each unit.  The array contains one GQueue for each unit.  Each node of a
                                   GQueue stores a pointer to an Exposure event.  The exposure event objects
                                   are shared with trace_out.  Note that we never free an exposure event
                                   pointed to by trace_in. */
  unsigned int nunits;          /* Number of units.  Stored here because it is
                                   also the length of the trace_out and trace_in lists. */
  GPtrArray *pending_results; /**< An array to store delayed results.  Each
    item in the array is a GQueue of TraceResult events.  (Actually a singly-
    linked list would suffice, but the GQueue syntax is much more readable than
    the GSList syntax.)  An index "rotates" through the array, so an event that
    is to happen in 1 day is placed in the GQueue that is 1 place ahead of the
    rotating index, an event that is to happen in 2 days is placed in the
    GQueue that is 2 places ahead of the rotating index, etc. */
  unsigned int npending_results;
  unsigned int rotating_index; /**< To go with pending_results. */
}
local_data_t;



/**
 * Responds to a contact exposure event by copying the event and storing it in
 * the trace lists.  We check the production types and contact type in deciding
 * whether to store the event.
 *
 * @param self the model.
 * @param e an exposure event.
 */
void
handle_exposure_event (struct spreadmodel_model_t_ *self, EVT_event_t * e)
{
  local_data_t *local_data;
  EVT_exposure_event_t *event;
  EVT_event_t *event_copy;

#if DEBUG
  g_debug ("----- ENTER handle_exposure_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  event = &(e->u.exposure);

  /* Exposures by airborne spread can be recorded by exposure-monitor, but
   * they cannot be traced, so nothing should be done with them here.
  */  
  if (event->traceable && event->exposing_unit != NULL)
    {
      if (SPREADMODEL_UnspecifiedInfectionType  == event->contact_type)
        g_error( "Contact type is unspecified in contact-recorder-model.handle_exposure_event" );
      else
        {
          if (local_data->trace_success[event->contact_type][event->exposing_unit->production_type] >= 0
              || local_data->trace_success[event->contact_type][event->exposed_unit->production_type] >= 0)
            {
              #if DEBUG
                g_debug ("recording exposure from unit \"%s\" -> unit \"%s\" on day %hu",
                         event->exposing_unit->official_id, event->exposed_unit->official_id, event->day);
              #endif
          
              event_copy = EVT_clone_event (e);
              g_queue_push_head (local_data->trace_out[event->exposing_unit->index], event_copy);
              g_queue_push_head (local_data->trace_in[event->exposed_unit->index], event_copy);
            }
        }
    }

  #if DEBUG
    g_debug ("----- EXIT handle_exposure_event (%s)", MODEL_NAME);
  #endif
}



/**
 * Responds to an attempt to trace by going through the records and issuing
 * trace result events.
 *
 * @param self the model.
 * @param event an attempt to trace event.
 * @param rng a random number generator.
 * @param queue for any new events the function creates.
 */
void
handle_attempt_to_trace_event (struct spreadmodel_model_t_ *self,
                               EVT_attempt_to_trace_event_t * event,
                               RAN_gen_t * rng, EVT_event_queue_t * queue)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  int day;
  SPREADMODEL_trace_direction direction;
  GList *iter;
  EVT_exposure_event_t *record;
  double p, r;
  EVT_event_t *result;
  int days_ago;
  PDF_dist_t *delay_dist;
  int delay;
  int delay_index;
  GQueue *q;
  gboolean trace_successful;

#if DEBUG
  g_debug ("----- ENTER handle_attempt_to_trace_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  unit = event->unit;
  day = event->day;
  direction = event->direction;

  #if DEBUG
    g_debug ("attempting %s from unit \"%s\", %i days back",
             SPREADMODEL_trace_direction_name[direction], unit->official_id,
             local_data->trace_period);
  #endif

  /* Do the trace.  Note that this process may issue multiple TraceResults for
   * the same pair of units if A has had contact with B several times in the
   * time period of interest. */
  if (direction == SPREADMODEL_TraceBackOrIn)
    iter = g_queue_peek_head_link (local_data->trace_in[unit->index]);
  else if (direction == SPREADMODEL_TraceForwardOrOut)
    iter = g_queue_peek_head_link (local_data->trace_out[unit->index]);
  else
    iter = NULL;

  #if DEBUG
    if (direction == SPREADMODEL_TraceBackOrIn)
      g_debug ("trace list contains %u records",
               g_queue_get_length (local_data->trace_in[unit->index]));
    else if (direction == SPREADMODEL_TraceForwardOrOut)
      g_debug ("trace list contains %u records",
               g_queue_get_length (local_data->trace_out[unit->index]));
  #endif

  for (; iter != NULL; iter = g_list_next (iter))
    {
      record = &(((EVT_event_t *) (iter->data))->u.exposure);

      days_ago = day - record->day;

      if (days_ago > local_data->trace_period)
        /* FIXME: add a cleanup step here. */
        break;

      /* We need to mark contacts that have already been traced, so we don't
       * get caught in a loop of tracing out & in along the same paths. */
      if (record->traced == TRUE)
        continue;

      if (record->contact_type != event->contact_type)
        continue;

      p = local_data->trace_success[record->contact_type][unit->production_type];
      r = RAN_num (rng);
      trace_successful = (r < p);
      
      #if DEBUG
        if (trace_successful) 
          g_debug ("r (%g) < p (%g)", r, p);
        else
          g_debug ("r (%g) >= p (%g)", r, p);
      #endif

      if (!trace_successful)
        { 
          /* The failure to trace will be reported immediately */  		  
          EVT_event_enqueue (queue,
                             EVT_new_trace_result_event (record->exposing_unit,
                                                         record->exposed_unit,
                                                         record->contact_type,
                                                         direction, day, day, FALSE));
          #if DEBUG
            g_debug ("%s misses contact from unit \"%s\" -> unit \"%s\" on day %hu (%i days ago)",
                     SPREADMODEL_trace_direction_name[direction],
                     record->exposing_unit->official_id,
                     record->exposed_unit->official_id, record->day, days_ago);
          #endif
          continue;
        }

      /* Otherwise... */
      /* The trace succeeded in finding this contact. */
      record->traced = TRUE;
      
      /* The release of the trace result may be delayed. */
      delay_dist = local_data->trace_delay[record->contact_type][unit->production_type];
      if (delay_dist == NULL)
        delay = 0;
      else
        delay = (int) round (PDF_random (delay_dist, rng));      
      
      result = EVT_new_trace_result_event (record->exposing_unit,
                                           record->exposed_unit,
                                           record->contact_type,
                                           direction, day, day, TRUE);
      #if DEBUG
        g_debug ("%s finds contact from unit \"%s\" -> unit \"%s\" on day %hu (%i days ago)",
                 SPREADMODEL_trace_direction_name[direction],
                 record->exposing_unit->official_id,
                 record->exposed_unit->official_id, record->day, days_ago);
      #endif
 
      if (delay <= 0)
        {
          EVT_event_enqueue (queue, result);
        }
      else
        {
          result->u.trace_result.day += delay;
          if (delay > local_data->pending_results->len)
            spreadmodel_extend_rotating_array (local_data->pending_results, delay,
                                               local_data->rotating_index);
          delay_index = (local_data->rotating_index + delay) % local_data->pending_results->len;
          q = (GQueue *) g_ptr_array_index (local_data->pending_results, delay_index);
          g_queue_push_tail (q, result);
          local_data->npending_results++;
          #if DEBUG
            g_debug ("  trace result will be delayed %i days", delay);
          #endif
        }
    }                           /* end of iteration over trace list. */

#if DEBUG
  g_debug ("----- EXIT handle_attempt_to_trace_event (%s)", MODEL_NAME);
#endif
}



/**
 * Responds to a new day event by releasing any pending results.
 *
 * @param self the model.
 * @param event a new day event.
 * @param queue for any new events the model creates.
 */
void
handle_new_day_event (struct spreadmodel_model_t_ *self,
                      EVT_new_day_event_t * event,
                      EVT_event_queue_t * queue)
{
  local_data_t *local_data;
  GQueue *q;
  EVT_event_t *pending_event;

#if DEBUG
  g_debug ("----- ENTER handle_new_day_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* Release any pending (due to trace delays) events. */
  local_data->rotating_index =
    (local_data->rotating_index + 1) % local_data->pending_results->len;
  q = (GQueue *) g_ptr_array_index (local_data->pending_results, local_data->rotating_index);
  while (!g_queue_is_empty (q))
    {
      /* Remove the event from this model's internal queue and place it in the
       * simulation's event queue. */
      pending_event = (EVT_event_t *) g_queue_pop_head (q);
#ifndef WIN_DLL
      /* Double-check that the event is coming out on the correct day. */
      g_assert (pending_event->u.trace_result.day == event->day);
#endif
      EVT_event_enqueue (queue, pending_event);
      local_data->npending_results--;
    }

#if DEBUG
  g_debug ("----- EXIT handle_new_day_event (%s)", MODEL_NAME);
#endif

  return;
}



/**
 * Runs this model.
 *
 * @param self the model.
 * @param units a unit list.
 * @param zones a zone list.
 * @param event the event that caused the model to run.
 * @param rng a random number generator.
 * @param queue for any new events the model creates.
 */
void
run (struct spreadmodel_model_t_ *self, UNT_unit_list_t * units, ZON_zone_list_t * zones,
     EVT_event_t * event, RAN_gen_t * rng, EVT_event_queue_t * queue)
{
#if DEBUG
  g_debug ("----- ENTER run (%s)", MODEL_NAME);
#endif

  switch (event->type)
    {
    case EVT_Exposure:
      handle_exposure_event (self, event);
      break;
    case EVT_AttemptToTrace:
      handle_attempt_to_trace_event (self, &(event->u.attempt_to_trace), rng, queue);
      break;
    case EVT_NewDay:
      handle_new_day_event (self, &(event->u.new_day), queue);
      break;
    default:
      g_error
        ("%s has received a %s event, which it does not listen for.  This should never happen.  Please contact the developer.",
         MODEL_NAME, EVT_event_type_name[event->type]);
    }

#if DEBUG
  g_debug ("----- EXIT run (%s)", MODEL_NAME);
#endif
}



/**
 * Resets this model after a simulation run.
 *
 * @param self the model.
 */
void
reset (struct spreadmodel_model_t_ *self)
{
  local_data_t *local_data;
  unsigned int i;
  GQueue *q;

#if DEBUG
  g_debug ("----- ENTER reset (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* Free all nodes in the trace_out lists, and free the exposure events they
   * point to. */
  for (i = 0; i < local_data->nunits; i++)
    {
      q = local_data->trace_out[i];
      while (!g_queue_is_empty (q))
        EVT_free_event ((EVT_event_t *) g_queue_pop_head (q));
    }

  /* Free all nodes in the trace_in lists, but do not attempt to free the
   * exposure events they point to.  That has already been done because the
   * trace_out and trace_in lists share exposure events. */
  for (i = 0; i < local_data->nunits; i++)
    {
      q = local_data->trace_in[i];
      while (!g_queue_is_empty (q))
        g_queue_pop_head (q);
    }

  for (i = 0; i < local_data->pending_results->len; i++)
    {
      q = (GQueue *) g_ptr_array_index (local_data->pending_results, i);
      while (!g_queue_is_empty (q))
        EVT_free_event (g_queue_pop_head (q));
    }
  local_data->npending_results = 0;
  local_data->rotating_index = 0;

#if DEBUG
  g_debug ("----- EXIT reset (%s)", MODEL_NAME);
#endif
}



/**
 * Reports whether this model is listening for a given event type.
 *
 * @param self the model.
 * @param event_type an event type.
 * @return TRUE if the model is listening for the event type.
 */
gboolean
is_listening_for (struct spreadmodel_model_t_ *self, EVT_event_type_t event_type)
{
  int i;

  for (i = 0; i < self->nevents_listened_for; i++)
    if (self->events_listened_for[i] == event_type)
      return TRUE;
  return FALSE;
}



/**
 * Reports whether this model has any pending actions to carry out.
 *
 * @param self the model.
 * @return TRUE if the model has pending actions.
 */
gboolean
has_pending_actions (struct spreadmodel_model_t_ * self)
{
  local_data_t *local_data;

  local_data = (local_data_t *) (self->model_data);
  return (local_data->npending_results > 0);
}



/**
 * Reports whether this model has any pending infections to cause.
 *
 * @param self the model.
 * @return TRUE if the model has pending infections.
 */
gboolean
has_pending_infections (struct spreadmodel_model_t_ * self)
{
  return FALSE;
}



/**
 * Returns a text representation of this model.
 *
 * @param self the model.
 * @return a string.
 */
char *
to_string (struct spreadmodel_model_t_ *self)
{
  local_data_t *local_data;
  GString *s;
  SPREADMODEL_contact_type contact_type;
  unsigned int nprod_types, i;
  double p;
  PDF_dist_t *delay;
  char *delay_as_string;
  char *chararray;

  local_data = (local_data_t *) (self->model_data);
  s = g_string_new (NULL);
  g_string_printf (s, "<%s", MODEL_NAME);

  g_string_sprintfa (s, "\n  trace-period=%i", local_data->trace_period);

  /* Add the trace success parameter for each combination of contact type and
   * source production type. */
  g_string_sprintfa (s, "\n  trace-success=");
  nprod_types = local_data->production_types->len;
  for (contact_type = SPREADMODEL_DirectContact; contact_type <= SPREADMODEL_IndirectContact; contact_type++)
    for (i = 0; i < nprod_types; i++)
      {
        p = local_data->trace_success[contact_type][i];
        g_string_append_printf (s, "\n    %g for %s from %s", p,
                                SPREADMODEL_contact_type_name[contact_type],
                                (char *) g_ptr_array_index (local_data->production_types, i));
      }

  /* Add the trace delay parameter for each combination of contact type and
   * source production type. */
  g_string_sprintfa (s, "\n  trace-delay=");
  for (contact_type = SPREADMODEL_DirectContact; contact_type <= SPREADMODEL_IndirectContact; contact_type++)
    for (i = 0; i < nprod_types; i++)
      {
        delay = local_data->trace_delay[contact_type][i];
        if (delay == NULL)
          {
            g_string_append_printf (s, "\n    0 for %s from %s",
                                    SPREADMODEL_contact_type_name[contact_type],
                                    (char *) g_ptr_array_index (local_data->production_types, i));
          }
        else
          {
            delay_as_string = PDF_dist_to_string (delay);
            g_string_append_printf (s, "\n    %s for %s from %s",
                                    delay_as_string,
                                    SPREADMODEL_contact_type_name[contact_type],
                                    (char *) g_ptr_array_index (local_data->production_types, i));
            g_free (delay_as_string);
          }
      }
  g_string_append_c (s, '>');

  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Prints this model to a stream.
 *
 * @param stream a stream to write to.
 * @param self the model.
 * @return the number of characters printed (not including the trailing '\\0').
 */
int
local_fprintf (FILE * stream, struct spreadmodel_model_t_ *self)
{
  char *s;
  int nchars_written;

  s = to_string (self);
  nchars_written = fprintf (stream, "%s", s);
  free (s);
  return nchars_written;
}



/**
 * Prints this model.
 *
 * @param self the model.
 * @return the number of characters printed (not including the trailing '\\0').
 */
int
local_printf (struct spreadmodel_model_t_ *self)
{
  return local_fprintf (stdout, self);
}



/**
 * Frees this model.  Does not free the contact type name or production type
 * names.
 *
 * @param self the model.
 */
void
local_free (struct spreadmodel_model_t_ *self)
{
  local_data_t *local_data;
  SPREADMODEL_contact_type contact_type;
  unsigned int nprod_types, i;
  GQueue *q;

#if DEBUG
  g_debug ("----- ENTER free (%s)", MODEL_NAME);
#endif

  /* Free the dynamically-allocated parts. */
  local_data = (local_data_t *) (self->model_data);

  nprod_types = local_data->production_types->len;
  for (contact_type = SPREADMODEL_DirectContact; contact_type <= SPREADMODEL_IndirectContact; contact_type++)
    {
      g_free (local_data->trace_success[contact_type]);
    }

  for (contact_type = SPREADMODEL_DirectContact; contact_type <= SPREADMODEL_IndirectContact; contact_type++)
    {
      for (i = 0; i < nprod_types; i++)
        PDF_free_dist (local_data->trace_delay[contact_type][i]);
      g_free (local_data->trace_delay[contact_type]);
    }

  for (i = 0; i < local_data->nunits; i++)
    {
      q = local_data->trace_out[i];
      while (!g_queue_is_empty (q))
        EVT_free_event ((EVT_event_t *) g_queue_pop_head (q));
      g_queue_free (q);
    }
  g_free (local_data->trace_out);

  for (i = 0; i < local_data->nunits; i++)
    {
      q = local_data->trace_in[i];
      g_queue_free (q);
    }
  g_free (local_data->trace_in);

  for (i = 0; i < local_data->pending_results->len; i++)
    {
      q = (GQueue *) g_ptr_array_index (local_data->pending_results, i);
      while (!g_queue_is_empty (q))
        EVT_free_event (g_queue_pop_head (q));
      g_queue_free (q);
    }
  g_ptr_array_free (local_data->pending_results, TRUE);

  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Returns whether this model is a singleton or not.
 */
gboolean
is_singleton (void)
{
  return TRUE;
}



/**
 * Adds a set of parameters to the model.
 */
void
set_params (struct spreadmodel_model_t_ *self, PAR_parameter_t * params)
{
  local_data_t *local_data;
  scew_element const *e;
  gboolean success;
  scew_attribute *attr;
  XML_Char const *attr_text;
  SPREADMODEL_contact_type contact_type;
  gboolean *production_type;
  double trace_success;
  unsigned int nprod_types, i;
  int trace_period;
  PDF_dist_t *trace_delay;

#if DEBUG
  g_debug ("----- ENTER set_params (%s)", MODEL_NAME);
#endif

  /* Make sure the right XML subtree was sent. */
  g_assert (strcmp (scew_element_name (params), MODEL_NAME) == 0);

  local_data = (local_data_t *) (self->model_data);

  /* Find out whether these parameters are for direct or indirect contact. */
  attr = scew_element_attribute_by_name (params, "contact-type");
  g_assert (attr != NULL);
  attr_text = scew_attribute_value (attr);
  if (strcmp (attr_text, "direct") == 0)
    contact_type = SPREADMODEL_DirectContact;
  else if (strcmp (attr_text, "indirect") == 0)
    contact_type = SPREADMODEL_IndirectContact;
  else
    g_assert_not_reached ();

  /* Find out which source production type these parameters apply to. */
  production_type =
    spreadmodel_read_prodtype_attribute (params, "production-type", local_data->production_types);

  e = scew_element_by_name (params, "trace-success");
  if (e != NULL)
    {
      trace_success = PAR_get_probability (e, &success);
      if (success == FALSE)
        {
          g_warning ("%s: settting probability of trace success to 1", MODEL_NAME);
          trace_success = 1;
        }
    }
  else
    {
      g_warning ("%s: probability of trace success missing, setting to 1", MODEL_NAME);
      trace_success = 1;
    }

  nprod_types = local_data->production_types->len;
  for (i = 0; i < nprod_types; i++)
    if (production_type[i] == TRUE)
      local_data->trace_success[contact_type][i] = trace_success;

  trace_period = 0;
  e = scew_element_by_name (params, "trace-period");
  if (e != NULL)
    {
      trace_period = (int) ceil (PAR_get_time (e, &success));
      if (success == FALSE)
        g_warning ("%s: period of interest not modified", MODEL_NAME);
    }
  else
    {
      g_warning ("%s: period of interest missing", MODEL_NAME);
    }
  local_data->trace_period = MAX (local_data->trace_period, trace_period);

  e = scew_element_by_name (params, "trace-delay");
  if (e != NULL)
    {
      trace_delay = PAR_get_PDF (e);
      g_assert (trace_delay != NULL);
      for (i = 0; i < nprod_types; i++)
        if (production_type[i] == TRUE)
          local_data->trace_delay[contact_type][i] = PDF_clone_dist (trace_delay);
      PDF_free_dist (trace_delay);
    }

  g_free (production_type);

#if DEBUG
  g_debug ("----- EXIT set_params (%s)", MODEL_NAME);
#endif

  return;
}



/**
 * Returns a new contact recorder model.
 */
spreadmodel_model_t *
new (scew_element * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  spreadmodel_model_t *self;
  local_data_t *local_data;
  unsigned int nprod_types;
  SPREADMODEL_contact_type contact_type;
  unsigned int i;

#if DEBUG
  g_debug ("----- ENTER new (%s)", MODEL_NAME);
#endif

  self = g_new (spreadmodel_model_t, 1);
  local_data = g_new (local_data_t, 1);

  self->name = MODEL_NAME;
  self->events_listened_for = events_listened_for;
  self->nevents_listened_for = NEVENTS_LISTENED_FOR;
  self->outputs = g_ptr_array_new ();
  self->model_data = local_data;
  self->set_params = set_params;
  self->run = run;
  self->reset = reset;
  self->is_listening_for = is_listening_for;
  self->has_pending_actions = has_pending_actions;
  self->has_pending_infections = has_pending_infections;
  self->to_string = to_string;
  self->printf = local_printf;
  self->fprintf = local_fprintf;
  self->free = local_free;

  /* Make sure the right XML subtree was sent. */
  g_assert (strcmp (scew_element_name (params), MODEL_NAME) == 0);

  /* Create an array to hold probabilities of trace success.  The array is 2-
   * dimensional because it is indexed by contact type and source production
   * type. */
  local_data->production_types = units->production_type_names;
  nprod_types = units->production_type_names->len;
  for (contact_type = SPREADMODEL_DirectContact; contact_type <= SPREADMODEL_IndirectContact; contact_type++)
    {
      local_data->trace_success[contact_type] = g_new (double, nprod_types);
      for (i = 0; i < nprod_types; i++)
        {
          local_data->trace_success[contact_type][i] = -1;
        }
    }

  /* Create an array to hold trace delays.  The array is 2-dimensional because
   * it is indexed by contact type and source production type. */
  for (contact_type = SPREADMODEL_DirectContact; contact_type <= SPREADMODEL_IndirectContact; contact_type++)
    {
      local_data->trace_delay[contact_type] = g_new0 (PDF_dist_t *, nprod_types);
    }

  /* Initialize an array for delayed results.  We don't know yet how long the
   * the array needs to be, since that will depend on values we sample from the
   * delay distribution, so we initialize it to length 1. */
  local_data->pending_results = g_ptr_array_new ();
  g_ptr_array_add (local_data->pending_results, g_queue_new ());
  local_data->npending_results = 0;
  local_data->rotating_index = 0;

  local_data->nunits = UNT_unit_list_length (units);

  /* No exposures have been tracked yet. */
  local_data->trace_out = g_new0 (GQueue *, local_data->nunits);
  local_data->trace_in = g_new0 (GQueue *, local_data->nunits);
  for (i = 0; i < local_data->nunits; i++)
    {
      local_data->trace_out[i] = g_queue_new ();
      local_data->trace_in[i] = g_queue_new ();
    }

  local_data->trace_period = 0;

  /* Send the XML subtree to the init function to read the production type
   * combination specific parameters. */
  self->set_params (self, params);

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file contact_recorder_model.c */
