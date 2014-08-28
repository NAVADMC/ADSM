/** @file trace_quarantine_model.c
 * Module that simulates a policy of quarantining units that have been found
 * through trace-out or trace-in.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @version 0.1
 * @date August 2007
 *
 * Copyright &copy; University of Guelph, 2007
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
#define new trace_quarantine_model_new
#define run trace_quarantine_model_run
#define reset trace_quarantine_model_reset
#define to_string trace_quarantine_model_to_string
#define local_free trace_quarantine_model_free
#define handle_trace_result_event trace_quarantine_model_handle_trace_result_event

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

#include "trace_quarantine_model.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "trace-quarantine-model"



/** Specialized information for this model. */
typedef struct
{
  int dummy;                    /* to prevent "struct has no members" warnings */
}
local_data_t;



/**
 * Responds to a trace result by ordering quarantine.
 *
 * @param self the model.
 * @param units the list of units.
 * @param event a trace result event.
 */
void
handle_trace_result_event (struct adsm_module_t_ *self, UNT_unit_list_t * units,
                           EVT_trace_result_event_t * event)
{
  local_data_t *local_data;
  UNT_unit_t *unit;

#if DEBUG
  g_debug ("----- ENTER handle_trace_result_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  if (event->traced)
    {
      if (event->direction == ADSM_TraceForwardOrOut)
        unit = event->exposed_unit;
      else
        unit = event->exposing_unit;

      #if DEBUG
        g_debug ("requesting quarantine of unit \"%s\"", unit->official_id);
      #endif

      UNT_quarantine (unit);
    }

#if DEBUG
  g_debug ("----- EXIT handle_trace_result_event (%s)", MODEL_NAME);
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
run (struct adsm_module_t_ *self, UNT_unit_list_t * units, ZON_zone_list_t * zones,
     EVT_event_t * event, RAN_gen_t * rng, EVT_event_queue_t * queue)
{
#if DEBUG
  g_debug ("----- ENTER run (%s)", MODEL_NAME);
#endif

  switch (event->type)
    {
    case EVT_TraceResult:
      handle_trace_result_event (self, units, &(event->u.trace_result));
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
reset (struct adsm_module_t_ *self)
{
#if DEBUG
  g_debug ("----- ENTER reset (%s)", MODEL_NAME);
#endif

  /* Nothing to do. */

#if DEBUG
  g_debug ("----- EXIT reset (%s)", MODEL_NAME);
#endif
}



/**
 * Returns a text representation of this model.
 *
 * @param self the model.
 * @return a string.
 */
char *
to_string (struct adsm_module_t_ *self)
{
  return g_strdup_printf ("<%s>", MODEL_NAME);
}



/**
 * Frees this model.
 *
 * @param self the model.
 */
void
local_free (struct adsm_module_t_ *self)
{
  local_data_t *local_data;

#if DEBUG
  g_debug ("----- ENTER free (%s)", MODEL_NAME);
#endif

  /* Free the dynamically-allocated parts. */
  local_data = (local_data_t *) (self->model_data);
  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Returns a new trace quarantine model.
 */
adsm_module_t *
new (sqlite3 * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  adsm_module_t *self;
  local_data_t *local_data;
  EVT_event_type_t events_listened_for[] = {
    EVT_TraceResult,
    0
  };

#if DEBUG
  g_debug ("----- ENTER new (%s)", MODEL_NAME);
#endif

  self = g_new (adsm_module_t, 1);
  local_data = g_new (local_data_t, 1);

  self->name = MODEL_NAME;
  self->events_listened_for = adsm_setup_events_listened_for (events_listened_for);
  self->outputs = g_ptr_array_new ();
  self->model_data = local_data;
  self->run = run;
  self->reset = reset;
  self->is_listening_for = adsm_model_is_listening_for;
  self->has_pending_actions = adsm_model_answer_no;
  self->has_pending_infections = adsm_model_answer_no;
  self->to_string = to_string;
  self->printf = adsm_model_printf;
  self->fprintf = adsm_model_fprintf;
  self->free = local_free;

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file trace_quarantine_model.c */
