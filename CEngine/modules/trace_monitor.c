/** @file trace_monitor.c
 * Tracks the number of attempted and successful traces.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @version 0.1
 * @date October 2005
 *
 * Copyright &copy; University of Guelph, 2005-2009
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
#define new trace_monitor_new
#define run trace_monitor_run
#define reset trace_monitor_reset
#define events_listened_for trace_monitor_events_listened_for
#define local_free trace_monitor_free
#define handle_before_any_simulations_event trace_monitor_handle_before_any_simulations_event
#define handle_new_day_event trace_monitor_handle_new_day_event
#define handle_trace_result_event trace_monitor_handle_trace_result_event

#include "module.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#include "trace_monitor.h"

#include "spreadmodel.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "trace-monitor"



#define NEVENTS_LISTENED_FOR 3
EVT_event_type_t events_listened_for[] = { EVT_BeforeAnySimulations, EVT_NewDay, EVT_TraceResult };



/** Specialized information for this model. */
typedef struct
{
  GPtrArray *production_types;
  RPT_reporting_t *nunits_potentially_traced;
  RPT_reporting_t *nunits_potentially_traced_by_contacttype;
  RPT_reporting_t *nunits_potentially_traced_by_prodtype;
  RPT_reporting_t *nunits_potentially_traced_by_contacttype_and_prodtype;
  RPT_reporting_t *cumul_nunits_potentially_traced;
  RPT_reporting_t *cumul_nunits_potentially_traced_by_contacttype;
  RPT_reporting_t *cumul_nunits_potentially_traced_by_prodtype;
  RPT_reporting_t *cumul_nunits_potentially_traced_by_contacttype_and_prodtype;
  RPT_reporting_t *nunits_traced;
  RPT_reporting_t *nunits_traced_by_contacttype;
  RPT_reporting_t *nunits_traced_by_prodtype;
  RPT_reporting_t *nunits_traced_by_contacttype_and_prodtype;
  RPT_reporting_t *cumul_nunits_traced;
  RPT_reporting_t *cumul_nunits_traced_by_contacttype;
  RPT_reporting_t *cumul_nunits_traced_by_prodtype;
  RPT_reporting_t *cumul_nunits_traced_by_contacttype_and_prodtype;
  RPT_reporting_t *nanimals_potentially_traced;
  RPT_reporting_t *nanimals_potentially_traced_by_contacttype;
  RPT_reporting_t *nanimals_potentially_traced_by_prodtype;
  RPT_reporting_t *nanimals_potentially_traced_by_contacttype_and_prodtype;
  RPT_reporting_t *cumul_nanimals_potentially_traced;
  RPT_reporting_t *cumul_nanimals_potentially_traced_by_contacttype;
  RPT_reporting_t *cumul_nanimals_potentially_traced_by_prodtype;
  RPT_reporting_t *cumul_nanimals_potentially_traced_by_contacttype_and_prodtype;
  RPT_reporting_t *nanimals_traced;
  RPT_reporting_t *nanimals_traced_by_contacttype;
  RPT_reporting_t *nanimals_traced_by_prodtype;
  RPT_reporting_t *nanimals_traced_by_contacttype_and_prodtype;
  RPT_reporting_t *cumul_nanimals_traced;
  RPT_reporting_t *cumul_nanimals_traced_by_contacttype;
  RPT_reporting_t *cumul_nanimals_traced_by_prodtype;
  RPT_reporting_t *cumul_nanimals_traced_by_contacttype_and_prodtype;
  /* These two arrays are needed to form variable names like "trcUDirp" and
   * "trcUIndPigsp". */
  char *contact_type_name_with_p[SPREADMODEL_NCONTACT_TYPES];
  char **production_type_name_with_p;
}
local_data_t;



/**
 * Before any simulations, this module announces the output variables it is
 * recording.
 *
 * @param self this module.
 * @param queue for any new events this function creates.
 */
void
handle_before_any_simulations_event (struct spreadmodel_model_t_ *self,
                                     EVT_event_queue_t *queue)
{
  unsigned int n, i;
  RPT_reporting_t *output;
  GPtrArray *outputs = NULL;

  n = self->outputs->len;
  for (i = 0; i < n; i++)
    {
      output = (RPT_reporting_t *) g_ptr_array_index (self->outputs, i);
      if (output->frequency != RPT_never)
        {
          if (outputs == NULL)
            outputs = g_ptr_array_new();
          g_ptr_array_add (outputs, output);
        }
    }

  if (outputs != NULL)
    EVT_event_enqueue (queue, EVT_new_declaration_of_outputs_event (outputs));
  /* We don't free the pointer array, that will be done when the event is freed
   * after all interested modules have processed it. */

  return;
}



/**
 * First thing on a new day, zero the counts.
 *
 * @param self the model.
 */
void
handle_new_day_event (struct spreadmodel_model_t_ *self)
{
  local_data_t *local_data;

#if DEBUG
  g_debug ("----- ENTER handle_new_day_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* Zero the daily counts. */
  RPT_reporting_zero (local_data->nunits_potentially_traced);
  RPT_reporting_zero (local_data->nunits_potentially_traced_by_contacttype);
  RPT_reporting_zero (local_data->nunits_potentially_traced_by_prodtype);
  RPT_reporting_zero (local_data->nunits_potentially_traced_by_contacttype_and_prodtype);
  RPT_reporting_zero (local_data->nunits_traced);
  RPT_reporting_zero (local_data->nunits_traced_by_contacttype);
  RPT_reporting_zero (local_data->nunits_traced_by_prodtype);
  RPT_reporting_zero (local_data->nunits_traced_by_contacttype_and_prodtype);
  RPT_reporting_zero (local_data->nanimals_potentially_traced);
  RPT_reporting_zero (local_data->nanimals_potentially_traced_by_contacttype);
  RPT_reporting_zero (local_data->nanimals_potentially_traced_by_prodtype);
  RPT_reporting_zero (local_data->nanimals_potentially_traced_by_contacttype_and_prodtype);
  RPT_reporting_zero (local_data->nanimals_traced);
  RPT_reporting_zero (local_data->nanimals_traced_by_contacttype);
  RPT_reporting_zero (local_data->nanimals_traced_by_prodtype);
  RPT_reporting_zero (local_data->nanimals_traced_by_contacttype_and_prodtype);

#if DEBUG
  g_debug ("----- EXIT handle_new_day_event (%s)", MODEL_NAME);
#endif
}



/**
 * Responds to a trace result event by recording it.
 *
 * @param self the model.
 * @param event a trace result event.
 */
void
handle_trace_result_event (struct spreadmodel_model_t_ *self, EVT_trace_result_event_t *event)
{
  local_data_t *local_data;
  UNT_unit_t *identified_unit, *origin_unit;
  const char *contact_type_name;
  const char *drill_down_list[3] = { NULL, NULL, NULL };
  UNT_trace_t trace;
  
  #if DEBUG
    g_debug ("----- ENTER handle_trace_result_event (%s)", MODEL_NAME);
  #endif

  identified_unit = (event->direction == SPREADMODEL_TraceForwardOrOut) ? event->exposed_unit : event->exposing_unit;
  origin_unit = (event->direction == SPREADMODEL_TraceForwardOrOut) ? event->exposing_unit : event->exposed_unit; 
  
  /* Record the trace in the GUI */
  /* --------------------------- */
  trace.day = (int) event->day;
  trace.initiated_day = (int) event->initiated_day;
  
  trace.identified_index = identified_unit->index;
  trace.identified_state = (SPREADMODEL_disease_state) identified_unit->state;
  
  trace.origin_index = origin_unit->index; 
  trace.origin_state = (SPREADMODEL_disease_state) origin_unit->state;
  
  trace.trace_type = event->direction;
  trace.contact_type = event->contact_type;
  if (trace.contact_type != SPREADMODEL_DirectContact
      && trace.contact_type != SPREADMODEL_IndirectContact)
    {
      g_error( "Bad contact type in contact-recorder-model.attempt_trace_event" );
      trace.contact_type = 0;
    }

  if( TRUE == event->traced )
    trace.success = SPREADMODEL_SuccessTrue;
  else
    trace.success = SPREADMODEL_SuccessFalse; 

  #ifdef USE_SC_GUILIB
    sc_trace_unit( event->exposed_unit, trace );
  #else
    if (NULL != spreadmodel_trace_unit)
      spreadmodel_trace_unit (trace);
  #endif


  /* Record the trace in the SC version */
  /* ---------------------------------- */
  local_data = (local_data_t *) (self->model_data);
  
  contact_type_name = SPREADMODEL_contact_type_abbrev[event->contact_type];
  drill_down_list[0] = contact_type_name;

  /* Record a potentially traced contact. */
  drill_down_list[1] = local_data->production_type_name_with_p[identified_unit->production_type];
  RPT_reporting_add_integer (local_data->nunits_potentially_traced, 1, NULL);
  if (local_data->nunits_potentially_traced_by_contacttype->frequency != RPT_never)
    RPT_reporting_add_integer1 (local_data->nunits_potentially_traced_by_contacttype,
                                1, local_data->contact_type_name_with_p[event->contact_type]);
  if (local_data->nunits_potentially_traced_by_prodtype->frequency != RPT_never)
    RPT_reporting_add_integer1 (local_data->nunits_potentially_traced_by_prodtype,
                                1, local_data->production_type_name_with_p[identified_unit->production_type]);
  if (local_data->nunits_potentially_traced_by_contacttype_and_prodtype->frequency != RPT_never)
    RPT_reporting_add_integer (local_data->nunits_potentially_traced_by_contacttype_and_prodtype,
                               1, drill_down_list);
  RPT_reporting_add_integer (local_data->cumul_nunits_potentially_traced, 1, NULL);
  if (local_data->cumul_nunits_potentially_traced_by_contacttype->frequency != RPT_never)
    RPT_reporting_add_integer1 (local_data->cumul_nunits_potentially_traced_by_contacttype,
                                1, local_data->contact_type_name_with_p[event->contact_type]);
  if (local_data->cumul_nunits_potentially_traced_by_prodtype->frequency != RPT_never)
    RPT_reporting_add_integer1 (local_data->cumul_nunits_potentially_traced_by_prodtype,
                                1, local_data->production_type_name_with_p[identified_unit->production_type]);
  if (local_data->cumul_nunits_potentially_traced_by_contacttype_and_prodtype->frequency != RPT_never)
    RPT_reporting_add_integer (local_data->cumul_nunits_potentially_traced_by_contacttype_and_prodtype,
                               1, drill_down_list);
  RPT_reporting_add_integer (local_data->nanimals_potentially_traced, identified_unit->size, NULL);
  if (local_data->nanimals_potentially_traced_by_contacttype->frequency != RPT_never)
    RPT_reporting_add_integer1 (local_data->nanimals_potentially_traced_by_contacttype,
                                identified_unit->size, local_data->contact_type_name_with_p[event->contact_type]);
  if (local_data->nanimals_potentially_traced_by_prodtype->frequency != RPT_never)
    RPT_reporting_add_integer1 (local_data->nanimals_potentially_traced_by_prodtype,
                                identified_unit->size, local_data->production_type_name_with_p[identified_unit->production_type]);
  if (local_data->nanimals_potentially_traced_by_contacttype_and_prodtype->frequency != RPT_never)
    RPT_reporting_add_integer (local_data->nanimals_potentially_traced_by_contacttype_and_prodtype,
                               identified_unit->size, drill_down_list);
  RPT_reporting_add_integer (local_data->cumul_nanimals_potentially_traced, identified_unit->size, NULL);
  if (local_data->cumul_nanimals_potentially_traced_by_contacttype->frequency != RPT_never)
    RPT_reporting_add_integer1 (local_data->cumul_nanimals_potentially_traced_by_contacttype,
                                identified_unit->size, local_data->contact_type_name_with_p[event->contact_type]);
  if (local_data->cumul_nanimals_potentially_traced_by_prodtype->frequency != RPT_never)
    RPT_reporting_add_integer1 (local_data->cumul_nanimals_potentially_traced_by_prodtype,
                                identified_unit->size, local_data->production_type_name_with_p[identified_unit->production_type]);
  if (local_data->cumul_nanimals_potentially_traced_by_contacttype_and_prodtype->frequency != RPT_never)
    RPT_reporting_add_integer (local_data->cumul_nanimals_potentially_traced_by_contacttype_and_prodtype,
                               identified_unit->size, drill_down_list);

  if (event->traced == TRUE)
    {
      /* Record a successfully traced contact. */
      drill_down_list[1] = identified_unit->production_type_name;
      RPT_reporting_add_integer (local_data->nunits_traced, 1, NULL);
      if (local_data->nunits_traced_by_contacttype->frequency != RPT_never)
        RPT_reporting_add_integer1 (local_data->nunits_traced_by_contacttype,
                                    1, contact_type_name);
      if (local_data->nunits_traced_by_prodtype->frequency != RPT_never)
        RPT_reporting_add_integer1 (local_data->nunits_traced_by_prodtype,
                                    1, identified_unit->production_type_name);
      if (local_data->nunits_traced_by_contacttype_and_prodtype->frequency != RPT_never)
        RPT_reporting_add_integer (local_data->nunits_traced_by_contacttype_and_prodtype,
                                   1, drill_down_list);
      RPT_reporting_add_integer (local_data->cumul_nunits_traced, 1, NULL);
      if (local_data->cumul_nunits_traced_by_contacttype->frequency != RPT_never)
        RPT_reporting_add_integer1 (local_data->cumul_nunits_traced_by_contacttype,
                                    1, contact_type_name);
      if (local_data->cumul_nunits_traced_by_prodtype->frequency != RPT_never)
        RPT_reporting_add_integer1 (local_data->cumul_nunits_traced_by_prodtype,
                                    1, identified_unit->production_type_name);
      if (local_data->cumul_nunits_traced_by_contacttype_and_prodtype->frequency != RPT_never)
        RPT_reporting_add_integer (local_data->cumul_nunits_traced_by_contacttype_and_prodtype,
                                   1, drill_down_list);
      RPT_reporting_add_integer (local_data->nanimals_traced, 1, NULL);
      if (local_data->nanimals_traced_by_contacttype->frequency != RPT_never)
        RPT_reporting_add_integer1 (local_data->nanimals_traced_by_contacttype,
                                    1, contact_type_name);
      if (local_data->nanimals_traced_by_prodtype->frequency != RPT_never)
        RPT_reporting_add_integer1 (local_data->nanimals_traced_by_prodtype,
                                    1, identified_unit->production_type_name);
      if (local_data->nanimals_traced_by_contacttype_and_prodtype->frequency != RPT_never)
        RPT_reporting_add_integer (local_data->nanimals_traced_by_contacttype_and_prodtype,
                                   1, drill_down_list);
      RPT_reporting_add_integer (local_data->cumul_nanimals_traced, 1, NULL);
      if (local_data->cumul_nanimals_traced_by_contacttype->frequency != RPT_never)
        RPT_reporting_add_integer1 (local_data->cumul_nanimals_traced_by_contacttype,
                                    1, contact_type_name);
      if (local_data->cumul_nanimals_traced_by_prodtype->frequency != RPT_never)
        RPT_reporting_add_integer1 (local_data->cumul_nanimals_traced_by_prodtype,
                                    1, identified_unit->production_type_name);
      if (local_data->cumul_nanimals_traced_by_contacttype_and_prodtype->frequency != RPT_never)
        RPT_reporting_add_integer (local_data->cumul_nanimals_traced_by_contacttype_and_prodtype,
                                   1, drill_down_list);
    }

  #if DEBUG
    g_debug ("----- EXIT handle_trace_result_event (%s)", MODEL_NAME);
  #endif
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
    case EVT_BeforeAnySimulations:
      handle_before_any_simulations_event (self, queue);
      break;
    case EVT_NewDay:
      handle_new_day_event (self);
      break;
    case EVT_TraceResult:
      handle_trace_result_event (self, &(event->u.trace_result));
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

#if DEBUG
  g_debug ("----- ENTER reset (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  RPT_reporting_zero (local_data->cumul_nunits_potentially_traced);
  RPT_reporting_zero (local_data->cumul_nunits_potentially_traced_by_contacttype);
  RPT_reporting_zero (local_data->cumul_nunits_potentially_traced_by_prodtype);
  RPT_reporting_zero (local_data->cumul_nunits_potentially_traced_by_contacttype_and_prodtype);
  RPT_reporting_zero (local_data->cumul_nunits_traced);
  RPT_reporting_zero (local_data->cumul_nunits_traced_by_contacttype);
  RPT_reporting_zero (local_data->cumul_nunits_traced_by_prodtype);
  RPT_reporting_zero (local_data->cumul_nunits_traced_by_contacttype_and_prodtype);
  RPT_reporting_zero (local_data->cumul_nanimals_potentially_traced);
  RPT_reporting_zero (local_data->cumul_nanimals_potentially_traced_by_contacttype);
  RPT_reporting_zero (local_data->cumul_nanimals_potentially_traced_by_prodtype);
  RPT_reporting_zero (local_data->cumul_nanimals_potentially_traced_by_contacttype_and_prodtype);
  RPT_reporting_zero (local_data->cumul_nanimals_traced);
  RPT_reporting_zero (local_data->cumul_nanimals_traced_by_contacttype);
  RPT_reporting_zero (local_data->cumul_nanimals_traced_by_prodtype);
  RPT_reporting_zero (local_data->cumul_nanimals_traced_by_contacttype_and_prodtype);

#if DEBUG
  g_debug ("----- EXIT reset (%s)", MODEL_NAME);
#endif
}



/**
 * Frees this model.
 *
 * @param self the model.
 */
void
local_free (struct spreadmodel_model_t_ *self)
{
  local_data_t *local_data;
  unsigned int i;

#if DEBUG
  g_debug ("----- ENTER free (%s)", MODEL_NAME);
#endif

  /* Free the dynamically-allocated parts. */
  local_data = (local_data_t *) (self->model_data);

  RPT_free_reporting (local_data->nunits_potentially_traced);
  RPT_free_reporting (local_data->nunits_potentially_traced_by_contacttype);
  RPT_free_reporting (local_data->nunits_potentially_traced_by_prodtype);
  RPT_free_reporting (local_data->nunits_potentially_traced_by_contacttype_and_prodtype);
  RPT_free_reporting (local_data->cumul_nunits_potentially_traced);
  RPT_free_reporting (local_data->cumul_nunits_potentially_traced_by_contacttype);
  RPT_free_reporting (local_data->cumul_nunits_potentially_traced_by_prodtype);
  RPT_free_reporting (local_data->cumul_nunits_potentially_traced_by_contacttype_and_prodtype);
  RPT_free_reporting (local_data->nunits_traced);
  RPT_free_reporting (local_data->nunits_traced_by_contacttype);
  RPT_free_reporting (local_data->nunits_traced_by_prodtype);
  RPT_free_reporting (local_data->nunits_traced_by_contacttype_and_prodtype);
  RPT_free_reporting (local_data->cumul_nunits_traced);
  RPT_free_reporting (local_data->cumul_nunits_traced_by_contacttype);
  RPT_free_reporting (local_data->cumul_nunits_traced_by_prodtype);
  RPT_free_reporting (local_data->cumul_nunits_traced_by_contacttype_and_prodtype);
  RPT_free_reporting (local_data->nanimals_potentially_traced);
  RPT_free_reporting (local_data->nanimals_potentially_traced_by_contacttype);
  RPT_free_reporting (local_data->nanimals_potentially_traced_by_prodtype);
  RPT_free_reporting (local_data->nanimals_potentially_traced_by_contacttype_and_prodtype);
  RPT_free_reporting (local_data->cumul_nanimals_potentially_traced);
  RPT_free_reporting (local_data->cumul_nanimals_potentially_traced_by_contacttype);
  RPT_free_reporting (local_data->cumul_nanimals_potentially_traced_by_prodtype);
  RPT_free_reporting (local_data->cumul_nanimals_potentially_traced_by_contacttype_and_prodtype);
  RPT_free_reporting (local_data->nanimals_traced);
  RPT_free_reporting (local_data->nanimals_traced_by_contacttype);
  RPT_free_reporting (local_data->nanimals_traced_by_prodtype);
  RPT_free_reporting (local_data->nanimals_traced_by_contacttype_and_prodtype);
  RPT_free_reporting (local_data->cumul_nanimals_traced);
  RPT_free_reporting (local_data->cumul_nanimals_traced_by_contacttype);
  RPT_free_reporting (local_data->cumul_nanimals_traced_by_prodtype);
  RPT_free_reporting (local_data->cumul_nanimals_traced_by_contacttype_and_prodtype);

  for (i = SPREADMODEL_DirectContact; i <= SPREADMODEL_IndirectContact; i++)
    g_free (local_data->contact_type_name_with_p[i]);
  for (i = 0; i < local_data->production_types->len; i++)
    g_free (local_data->production_type_name_with_p[i]);
  g_free (local_data->production_type_name_with_p);
  
  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Returns a new trace monitor.
 */
spreadmodel_model_t *
new (sqlite3 * params, UNT_unit_list_t * units, projPJ projections,
     ZON_zone_list_t * zones)
{
  spreadmodel_model_t *self;
  local_data_t *local_data;
  unsigned int i, j;      /* loop counters */
  const char *contact_type_name;
  char *prodtype_name;
  const char *drill_down_list[3] = { NULL, NULL, NULL };

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
  self->run = run;
  self->reset = reset;
  self->is_listening_for = spreadmodel_model_is_listening_for;
  self->has_pending_actions = spreadmodel_model_answer_no;
  self->has_pending_infections = spreadmodel_model_answer_no;
  self->to_string = spreadmodel_model_to_string_default;
  self->printf = spreadmodel_model_printf;
  self->fprintf = spreadmodel_model_fprintf;
  self->free = local_free;

  local_data->nunits_potentially_traced =
    RPT_new_reporting ("trnUAllp", RPT_integer, RPT_never);
  local_data->nunits_potentially_traced_by_contacttype =
    RPT_new_reporting ("trnU", RPT_group, RPT_never);
  local_data->nunits_potentially_traced_by_prodtype =
    RPT_new_reporting ("trnU", RPT_group, RPT_never);
  local_data->nunits_potentially_traced_by_contacttype_and_prodtype =
    RPT_new_reporting ("trnU", RPT_group, RPT_never);
  local_data->cumul_nunits_potentially_traced =
    RPT_new_reporting ("trcUAllp", RPT_integer, RPT_never);
  local_data->cumul_nunits_potentially_traced_by_contacttype =
    RPT_new_reporting ("trcU", RPT_group, RPT_never);
  local_data->cumul_nunits_potentially_traced_by_prodtype =
    RPT_new_reporting ("trcU", RPT_group, RPT_never);
  local_data->cumul_nunits_potentially_traced_by_contacttype_and_prodtype =
    RPT_new_reporting ("trcU", RPT_group, RPT_never);
  local_data->nunits_traced =
    RPT_new_reporting ("trnUAll", RPT_integer, RPT_never);
  local_data->nunits_traced_by_contacttype =
    RPT_new_reporting ("trnU", RPT_group, RPT_never);
  local_data->nunits_traced_by_prodtype =
    RPT_new_reporting ("trnU", RPT_group, RPT_never);
  local_data->nunits_traced_by_contacttype_and_prodtype =
    RPT_new_reporting ("trnU", RPT_group, RPT_never);
  local_data->cumul_nunits_traced =
    RPT_new_reporting ("trcUAll", RPT_integer, RPT_never);
  local_data->cumul_nunits_traced_by_contacttype =
    RPT_new_reporting ("trcU", RPT_group, RPT_never);
  local_data->cumul_nunits_traced_by_prodtype =
    RPT_new_reporting ("trcU", RPT_group, RPT_never);
  local_data->cumul_nunits_traced_by_contacttype_and_prodtype =
    RPT_new_reporting ("trcU", RPT_group, RPT_never);
  local_data->nanimals_potentially_traced =
    RPT_new_reporting ("trnAAllp", RPT_integer, RPT_never);
  local_data->nanimals_potentially_traced_by_contacttype =
    RPT_new_reporting ("trnA", RPT_group, RPT_never);
  local_data->nanimals_potentially_traced_by_prodtype =
    RPT_new_reporting ("trnA", RPT_group, RPT_never);
  local_data->nanimals_potentially_traced_by_contacttype_and_prodtype =
    RPT_new_reporting ("trnA", RPT_group, RPT_never);
  local_data->cumul_nanimals_potentially_traced =
    RPT_new_reporting ("trcAAllp", RPT_integer, RPT_never);
  local_data->cumul_nanimals_potentially_traced_by_contacttype =
    RPT_new_reporting ("trcA", RPT_group, RPT_never);
  local_data->cumul_nanimals_potentially_traced_by_prodtype =
    RPT_new_reporting ("trcA", RPT_group, RPT_never);
  local_data->cumul_nanimals_potentially_traced_by_contacttype_and_prodtype =
    RPT_new_reporting ("trcA", RPT_group, RPT_never);
  local_data->nanimals_traced =
    RPT_new_reporting ("trnAAll", RPT_integer, RPT_never);
  local_data->nanimals_traced_by_contacttype =
    RPT_new_reporting ("trnA", RPT_group, RPT_never);
  local_data->nanimals_traced_by_prodtype =
    RPT_new_reporting ("trnA", RPT_group, RPT_never);
  local_data->nanimals_traced_by_contacttype_and_prodtype =
    RPT_new_reporting ("trnA", RPT_group, RPT_never);
  local_data->cumul_nanimals_traced =
    RPT_new_reporting ("trcAAll", RPT_integer, RPT_never);
  local_data->cumul_nanimals_traced_by_contacttype =
    RPT_new_reporting ("trcA", RPT_group, RPT_never);
  local_data->cumul_nanimals_traced_by_prodtype =
    RPT_new_reporting ("trcA", RPT_group, RPT_never);
  local_data->cumul_nanimals_traced_by_contacttype_and_prodtype =
    RPT_new_reporting ("trcA", RPT_group, RPT_never);
  g_ptr_array_add (self->outputs, local_data->nunits_potentially_traced);
  g_ptr_array_add (self->outputs, local_data->nunits_potentially_traced_by_contacttype);
  g_ptr_array_add (self->outputs, local_data->nunits_potentially_traced_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->nunits_potentially_traced_by_contacttype_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_potentially_traced);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_potentially_traced_by_contacttype);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_potentially_traced_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_potentially_traced_by_contacttype_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->nunits_traced);
  g_ptr_array_add (self->outputs, local_data->nunits_traced_by_contacttype);
  g_ptr_array_add (self->outputs, local_data->nunits_traced_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->nunits_traced_by_contacttype_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_traced);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_traced_by_contacttype);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_traced_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_traced_by_contacttype_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->nanimals_potentially_traced);
  g_ptr_array_add (self->outputs, local_data->nanimals_potentially_traced_by_contacttype);
  g_ptr_array_add (self->outputs, local_data->nanimals_potentially_traced_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->nanimals_potentially_traced_by_contacttype_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_nanimals_potentially_traced);
  g_ptr_array_add (self->outputs, local_data->cumul_nanimals_potentially_traced_by_contacttype);
  g_ptr_array_add (self->outputs, local_data->cumul_nanimals_potentially_traced_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_nanimals_potentially_traced_by_contacttype_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->nanimals_traced);
  g_ptr_array_add (self->outputs, local_data->nanimals_traced_by_contacttype);
  g_ptr_array_add (self->outputs, local_data->nanimals_traced_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->nanimals_traced_by_contacttype_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_nanimals_traced);
  g_ptr_array_add (self->outputs, local_data->cumul_nanimals_traced_by_contacttype);
  g_ptr_array_add (self->outputs, local_data->cumul_nanimals_traced_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_nanimals_traced_by_contacttype_and_prodtype);

  /* Set the reporting frequency for the output variables. */

  /* Initialize the categories in the output variables. */
  local_data->production_types = units->production_type_names;
  /* These are the outputs broken down by contact type. */
  for (i = SPREADMODEL_DirectContact; i <= SPREADMODEL_IndirectContact; i++)
    {
      /* Make a copy of each contact type name, but with "p" appended.  We need
       * this to form variables like "trcUDirp" and "trcUIndp". */
      local_data->contact_type_name_with_p[i] =
        g_strdup_printf ("%sp", SPREADMODEL_contact_type_abbrev[i]);
      
      contact_type_name = local_data->contact_type_name_with_p[i];
      RPT_reporting_add_integer1 (local_data->nunits_potentially_traced_by_contacttype, 0, contact_type_name);
      RPT_reporting_add_integer1 (local_data->cumul_nunits_potentially_traced_by_contacttype, 0, contact_type_name);
      RPT_reporting_add_integer1 (local_data->nanimals_potentially_traced_by_contacttype, 0, contact_type_name);
      RPT_reporting_add_integer1 (local_data->cumul_nanimals_potentially_traced_by_contacttype, 0, contact_type_name);
      contact_type_name = SPREADMODEL_contact_type_abbrev[i];
      RPT_reporting_add_integer1 (local_data->nunits_traced_by_contacttype, 0, contact_type_name);
      RPT_reporting_add_integer1 (local_data->cumul_nunits_traced_by_contacttype, 0, contact_type_name);
      RPT_reporting_add_integer1 (local_data->nanimals_traced_by_contacttype, 0, contact_type_name);
      RPT_reporting_add_integer1 (local_data->cumul_nanimals_traced_by_contacttype, 0, contact_type_name);
    }
  /* These are the outputs broken down by production type. */
  local_data->production_type_name_with_p = g_new0 (char *, local_data->production_types->len);
  for (i = 0; i < local_data->production_types->len; i++)
    {
      /* Make a copy of each production type name, but with "p" appended.  We
       * need this to form variables like "trcUCattlep". */
       local_data->production_type_name_with_p[i] =
         g_strdup_printf ("%sp", (char *) g_ptr_array_index (local_data->production_types, i));
      
      prodtype_name = local_data->production_type_name_with_p[i];
      RPT_reporting_add_integer1 (local_data->nunits_potentially_traced_by_prodtype, 0, prodtype_name);
      RPT_reporting_add_integer1 (local_data->cumul_nunits_potentially_traced_by_prodtype, 0, prodtype_name);
      RPT_reporting_add_integer1 (local_data->nanimals_potentially_traced_by_prodtype, 0, prodtype_name);
      RPT_reporting_add_integer1 (local_data->cumul_nanimals_potentially_traced_by_prodtype, 0, prodtype_name);
      prodtype_name = (char *) g_ptr_array_index (local_data->production_types, i);
      RPT_reporting_add_integer1 (local_data->nunits_traced_by_prodtype, 0, prodtype_name);
      RPT_reporting_add_integer1 (local_data->cumul_nunits_traced_by_prodtype, 0, prodtype_name);
      RPT_reporting_add_integer1 (local_data->nanimals_traced_by_prodtype, 0, prodtype_name);
      RPT_reporting_add_integer1 (local_data->cumul_nanimals_traced_by_prodtype, 0, prodtype_name);
    }
  /* These are the outputs broken down by contact type and production type. */
  for (i = SPREADMODEL_DirectContact; i <= SPREADMODEL_IndirectContact; i++)
    {
      drill_down_list[0] = SPREADMODEL_contact_type_abbrev[i];
      for (j = 0; j < local_data->production_types->len; j++)
        {
          drill_down_list[1] = local_data->production_type_name_with_p[j];
          RPT_reporting_add_integer (local_data->nunits_potentially_traced_by_contacttype_and_prodtype, 0, drill_down_list);
          RPT_reporting_add_integer (local_data->cumul_nunits_potentially_traced_by_contacttype_and_prodtype, 0, drill_down_list);
          RPT_reporting_add_integer (local_data->nanimals_potentially_traced_by_contacttype_and_prodtype, 0, drill_down_list);
          RPT_reporting_add_integer (local_data->cumul_nanimals_potentially_traced_by_contacttype_and_prodtype, 0, drill_down_list);
          drill_down_list[1] = (char *) g_ptr_array_index (local_data->production_types, j);
          RPT_reporting_add_integer (local_data->nunits_traced_by_contacttype_and_prodtype, 0, drill_down_list);
          RPT_reporting_add_integer (local_data->cumul_nunits_traced_by_contacttype_and_prodtype, 0, drill_down_list);
          RPT_reporting_add_integer (local_data->nanimals_traced_by_contacttype_and_prodtype, 0, drill_down_list);
          RPT_reporting_add_integer (local_data->cumul_nanimals_traced_by_contacttype_and_prodtype, 0, drill_down_list);
        }
    }

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file trace_monitor.c */
