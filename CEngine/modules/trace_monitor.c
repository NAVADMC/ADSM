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
#define local_free trace_monitor_free
#define handle_before_each_simulation_event trace_monitor_handle_before_each_simulation_event
#define handle_new_day_event trace_monitor_handle_new_day_event
#define handle_trace_result_event trace_monitor_handle_trace_result_event

#include "module.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#include "trace_monitor.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "trace-monitor"



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
  /* This array is needed to form variable names like "trcUDirp" and
   * "trcUIndpPigs". */
  char *contact_type_name_with_p[ADSM_NCONTACT_TYPES];
}
local_data_t;



/**
 * Before each simulation, zero the cumulative counts of traces.
 *
 * @param self this module.
 */
void
handle_before_each_simulation_event (struct adsm_module_t_ *self)
{
  local_data_t *local_data;

  #if DEBUG
    g_debug ("----- ENTER handle_before_each_simulation_event (%s)", MODEL_NAME);
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
    g_debug ("----- EXIT handle_before_each_simulation_event (%s)", MODEL_NAME);
  #endif
  
  return;
}



/**
 * First thing on a new day, zero the counts.
 *
 * @param self the model.
 */
void
handle_new_day_event (struct adsm_module_t_ *self)
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
handle_trace_result_event (struct adsm_module_t_ *self, EVT_trace_result_event_t *event)
{
  local_data_t *local_data;
  UNT_unit_t *identified_unit, *origin_unit;
  const char *contact_type_name;
  const char *drill_down_list[3] = { NULL, NULL, NULL };
  UNT_trace_t trace;
  
  #if DEBUG
    g_debug ("----- ENTER handle_trace_result_event (%s)", MODEL_NAME);
  #endif

  identified_unit = (event->direction == ADSM_TraceForwardOrOut) ? event->exposed_unit : event->exposing_unit;
  origin_unit = (event->direction == ADSM_TraceForwardOrOut) ? event->exposing_unit : event->exposed_unit; 
  
  /* Record the trace in the GUI */
  /* --------------------------- */
  trace.day = (int) event->day;
  trace.initiated_day = (int) event->initiated_day;
  
  trace.identified_index = identified_unit->index;
  trace.identified_state = (ADSM_disease_state) identified_unit->state;
  
  trace.origin_index = origin_unit->index; 
  trace.origin_state = (ADSM_disease_state) origin_unit->state;
  
  trace.trace_type = event->direction;
  trace.contact_type = event->contact_type;
  if (trace.contact_type != ADSM_DirectContact
      && trace.contact_type != ADSM_IndirectContact)
    {
      g_error( "Bad contact type in contact-recorder-model.attempt_trace_event" );
      trace.contact_type = 0;
    }

  if( TRUE == event->traced )
    trace.success = ADSM_SuccessTrue;
  else
    trace.success = ADSM_SuccessFalse; 

  #ifdef USE_SC_GUILIB
    sc_trace_unit( event->exposed_unit, trace );
  #else
    if (NULL != adsm_trace_unit)
      adsm_trace_unit (trace);
  #endif


  /* Record the trace in the SC version */
  /* ---------------------------------- */
  local_data = (local_data_t *) (self->model_data);
  

  /* Record a potentially traced contact. */

  contact_type_name = local_data->contact_type_name_with_p[event->contact_type];
  drill_down_list[0] = contact_type_name;
  drill_down_list[1] = identified_unit->production_type_name;

  RPT_reporting_add_integer (local_data->nunits_potentially_traced, 1, NULL);
  RPT_reporting_add_integer1 (local_data->nunits_potentially_traced_by_contacttype,
                              1, contact_type_name);
  RPT_reporting_add_integer1 (local_data->nunits_potentially_traced_by_prodtype,
                              1, identified_unit->production_type_name);
  RPT_reporting_add_integer (local_data->nunits_potentially_traced_by_contacttype_and_prodtype,
                             1, drill_down_list);
  RPT_reporting_add_integer (local_data->cumul_nunits_potentially_traced, 1, NULL);
  RPT_reporting_add_integer1 (local_data->cumul_nunits_potentially_traced_by_contacttype,
                              1, contact_type_name);
  RPT_reporting_add_integer1 (local_data->cumul_nunits_potentially_traced_by_prodtype,
                              1, identified_unit->production_type_name);
  RPT_reporting_add_integer (local_data->cumul_nunits_potentially_traced_by_contacttype_and_prodtype,
                             1, drill_down_list);
  RPT_reporting_add_integer (local_data->nanimals_potentially_traced, identified_unit->size, NULL);
  RPT_reporting_add_integer1 (local_data->nanimals_potentially_traced_by_contacttype,
                              identified_unit->size, contact_type_name);
  RPT_reporting_add_integer1 (local_data->nanimals_potentially_traced_by_prodtype,
                              identified_unit->size, identified_unit->production_type_name);
  RPT_reporting_add_integer (local_data->nanimals_potentially_traced_by_contacttype_and_prodtype,
                             identified_unit->size, drill_down_list);
  RPT_reporting_add_integer (local_data->cumul_nanimals_potentially_traced, identified_unit->size, NULL);
  RPT_reporting_add_integer1 (local_data->cumul_nanimals_potentially_traced_by_contacttype,
                              identified_unit->size, contact_type_name);
  RPT_reporting_add_integer1 (local_data->cumul_nanimals_potentially_traced_by_prodtype,
                              identified_unit->size, identified_unit->production_type_name);
  RPT_reporting_add_integer (local_data->cumul_nanimals_potentially_traced_by_contacttype_and_prodtype,
                             identified_unit->size, drill_down_list);

  if (event->traced == TRUE)
    {
      /* Record a successfully traced contact. */

      contact_type_name = ADSM_contact_type_abbrev[event->contact_type];
      drill_down_list[0] = contact_type_name;

      RPT_reporting_add_integer (local_data->nunits_traced, 1, NULL);
      RPT_reporting_add_integer1 (local_data->nunits_traced_by_contacttype,
                                  1, contact_type_name);
      RPT_reporting_add_integer1 (local_data->nunits_traced_by_prodtype,
                                  1, identified_unit->production_type_name);
      RPT_reporting_add_integer (local_data->nunits_traced_by_contacttype_and_prodtype,
                                 1, drill_down_list);
      RPT_reporting_add_integer (local_data->cumul_nunits_traced, 1, NULL);
      RPT_reporting_add_integer1 (local_data->cumul_nunits_traced_by_contacttype,
                                  1, contact_type_name);
      RPT_reporting_add_integer1 (local_data->cumul_nunits_traced_by_prodtype,
                                  1, identified_unit->production_type_name);
      RPT_reporting_add_integer (local_data->cumul_nunits_traced_by_contacttype_and_prodtype,
                                 1, drill_down_list);
      RPT_reporting_add_integer (local_data->nanimals_traced, 1, NULL);
      RPT_reporting_add_integer1 (local_data->nanimals_traced_by_contacttype,
                                  1, contact_type_name);
      RPT_reporting_add_integer1 (local_data->nanimals_traced_by_prodtype,
                                  1, identified_unit->production_type_name);
      RPT_reporting_add_integer (local_data->nanimals_traced_by_contacttype_and_prodtype,
                                 1, drill_down_list);
      RPT_reporting_add_integer (local_data->cumul_nanimals_traced, 1, NULL);
      RPT_reporting_add_integer1 (local_data->cumul_nanimals_traced_by_contacttype,
                                  1, contact_type_name);
      RPT_reporting_add_integer1 (local_data->cumul_nanimals_traced_by_prodtype,
                                  1, identified_unit->production_type_name);
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
run (struct adsm_module_t_ *self, UNT_unit_list_t * units, ZON_zone_list_t * zones,
     EVT_event_t * event, RAN_gen_t * rng, EVT_event_queue_t * queue)
{
#if DEBUG
  g_debug ("----- ENTER run (%s)", MODEL_NAME);
#endif

  switch (event->type)
    {
    case EVT_BeforeAnySimulations:
      adsm_declare_outputs (self, queue);
      break;
    case EVT_BeforeEachSimulation:
      handle_before_each_simulation_event (self);
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
 * Frees this model.
 *
 * @param self the model.
 */
void
local_free (struct adsm_module_t_ *self)
{
  local_data_t *local_data;
  unsigned int i;

#if DEBUG
  g_debug ("----- ENTER free (%s)", MODEL_NAME);
#endif

  /* Free the dynamically-allocated parts. */
  local_data = (local_data_t *) (self->model_data);

  for (i = ADSM_DirectContact; i <= ADSM_IndirectContact; i++)
    g_free (local_data->contact_type_name_with_p[i]);

  g_free (local_data);
  g_ptr_array_free (self->outputs, /* free_seg = */ TRUE); /* also frees all output variables */
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Returns a new trace monitor.
 */
adsm_module_t *
new (sqlite3 * params, UNT_unit_list_t * units, projPJ projections,
     ZON_zone_list_t * zones)
{
  adsm_module_t *self;
  local_data_t *local_data;
  EVT_event_type_t events_listened_for[] = {
    EVT_BeforeAnySimulations,
    EVT_BeforeEachSimulation,
    EVT_NewDay,
    EVT_TraceResult,
    0
  };
  unsigned int i, j;      /* loop counters */
  const char *contact_type_name;
  char *prodtype_name;
  const char *drill_down_list[3] = { NULL, NULL, NULL };

#if DEBUG
  g_debug ("----- ENTER new (%s)", MODEL_NAME);
#endif

  self = g_new (adsm_module_t, 1);
  local_data = g_new (local_data_t, 1);

  self->name = MODEL_NAME;
  self->events_listened_for = adsm_setup_events_listened_for (events_listened_for);
  self->outputs = g_ptr_array_new_with_free_func ((GDestroyNotify)RPT_free_reporting);
  self->model_data = local_data;
  self->run = run;
  self->is_listening_for = adsm_model_is_listening_for;
  self->has_pending_actions = adsm_model_answer_no;
  self->has_pending_infections = adsm_model_answer_no;
  self->to_string = adsm_module_to_string_default;
  self->printf = adsm_model_printf;
  self->fprintf = adsm_model_fprintf;
  self->free = local_free;

  local_data->nunits_potentially_traced =
    RPT_new_reporting ("trnUAllp", RPT_integer);
  local_data->nunits_potentially_traced_by_contacttype =
    RPT_new_reporting ("trnU", RPT_group);
  local_data->nunits_potentially_traced_by_prodtype =
    RPT_new_reporting ("trnUp", RPT_group);
  local_data->nunits_potentially_traced_by_contacttype_and_prodtype =
    RPT_new_reporting ("trnU", RPT_group);
  local_data->cumul_nunits_potentially_traced =
    RPT_new_reporting ("trcUAllp", RPT_integer);
  local_data->cumul_nunits_potentially_traced_by_contacttype =
    RPT_new_reporting ("trcU", RPT_group);
  local_data->cumul_nunits_potentially_traced_by_prodtype =
    RPT_new_reporting ("trcUp", RPT_group);
  local_data->cumul_nunits_potentially_traced_by_contacttype_and_prodtype =
    RPT_new_reporting ("trcU", RPT_group);
  local_data->nunits_traced =
    RPT_new_reporting ("trnUAll", RPT_integer);
  local_data->nunits_traced_by_contacttype =
    RPT_new_reporting ("trnU", RPT_group);
  local_data->nunits_traced_by_prodtype =
    RPT_new_reporting ("trnU", RPT_group);
  local_data->nunits_traced_by_contacttype_and_prodtype =
    RPT_new_reporting ("trnU", RPT_group);
  local_data->cumul_nunits_traced =
    RPT_new_reporting ("trcUAll", RPT_integer);
  local_data->cumul_nunits_traced_by_contacttype =
    RPT_new_reporting ("trcU", RPT_group);
  local_data->cumul_nunits_traced_by_prodtype =
    RPT_new_reporting ("trcU", RPT_group);
  local_data->cumul_nunits_traced_by_contacttype_and_prodtype =
    RPT_new_reporting ("trcU", RPT_group);
  local_data->nanimals_potentially_traced =
    RPT_new_reporting ("trnAAllp", RPT_integer);
  local_data->nanimals_potentially_traced_by_contacttype =
    RPT_new_reporting ("trnA", RPT_group);
  local_data->nanimals_potentially_traced_by_prodtype =
    RPT_new_reporting ("trnAp", RPT_group);
  local_data->nanimals_potentially_traced_by_contacttype_and_prodtype =
    RPT_new_reporting ("trnA", RPT_group);
  local_data->cumul_nanimals_potentially_traced =
    RPT_new_reporting ("trcAAllp", RPT_integer);
  local_data->cumul_nanimals_potentially_traced_by_contacttype =
    RPT_new_reporting ("trcA", RPT_group);
  local_data->cumul_nanimals_potentially_traced_by_prodtype =
    RPT_new_reporting ("trcAp", RPT_group);
  local_data->cumul_nanimals_potentially_traced_by_contacttype_and_prodtype =
    RPT_new_reporting ("trcA", RPT_group);
  local_data->nanimals_traced =
    RPT_new_reporting ("trnAAll", RPT_integer);
  local_data->nanimals_traced_by_contacttype =
    RPT_new_reporting ("trnA", RPT_group);
  local_data->nanimals_traced_by_prodtype =
    RPT_new_reporting ("trnA", RPT_group);
  local_data->nanimals_traced_by_contacttype_and_prodtype =
    RPT_new_reporting ("trnA", RPT_group);
  local_data->cumul_nanimals_traced =
    RPT_new_reporting ("trcAAll", RPT_integer);
  local_data->cumul_nanimals_traced_by_contacttype =
    RPT_new_reporting ("trcA", RPT_group);
  local_data->cumul_nanimals_traced_by_prodtype =
    RPT_new_reporting ("trcA", RPT_group);
  local_data->cumul_nanimals_traced_by_contacttype_and_prodtype =
    RPT_new_reporting ("trcA", RPT_group);
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
  for (i = ADSM_DirectContact; i <= ADSM_IndirectContact; i++)
    {
      /* Make a copy of each contact type name, but with "p" appended.  We need
       * this to form variables like "trcUDirp" and "trcUIndp". */
      local_data->contact_type_name_with_p[i] =
        g_strdup_printf ("%sp", ADSM_contact_type_abbrev[i]);

      contact_type_name = local_data->contact_type_name_with_p[i];
      RPT_reporting_add_integer1 (local_data->nunits_potentially_traced_by_contacttype, 0, contact_type_name);
      RPT_reporting_add_integer1 (local_data->cumul_nunits_potentially_traced_by_contacttype, 0, contact_type_name);
      RPT_reporting_add_integer1 (local_data->nanimals_potentially_traced_by_contacttype, 0, contact_type_name);
      RPT_reporting_add_integer1 (local_data->cumul_nanimals_potentially_traced_by_contacttype, 0, contact_type_name);
      contact_type_name = ADSM_contact_type_abbrev[i];
      RPT_reporting_add_integer1 (local_data->nunits_traced_by_contacttype, 0, contact_type_name);
      RPT_reporting_add_integer1 (local_data->cumul_nunits_traced_by_contacttype, 0, contact_type_name);
      RPT_reporting_add_integer1 (local_data->nanimals_traced_by_contacttype, 0, contact_type_name);
      RPT_reporting_add_integer1 (local_data->cumul_nanimals_traced_by_contacttype, 0, contact_type_name);
    }
  /* These are the outputs broken down by production type. */
  for (i = 0; i < local_data->production_types->len; i++)
    {
      prodtype_name = (char *) g_ptr_array_index (local_data->production_types, i);
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
  for (i = ADSM_DirectContact; i <= ADSM_IndirectContact; i++)
    {
      for (j = 0; j < local_data->production_types->len; j++)
        {
          drill_down_list[1] = (char *) g_ptr_array_index (local_data->production_types, j);
          drill_down_list[0] = local_data->contact_type_name_with_p[i];
          RPT_reporting_add_integer (local_data->nunits_potentially_traced_by_contacttype_and_prodtype, 0, drill_down_list);
          RPT_reporting_add_integer (local_data->cumul_nunits_potentially_traced_by_contacttype_and_prodtype, 0, drill_down_list);
          RPT_reporting_add_integer (local_data->nanimals_potentially_traced_by_contacttype_and_prodtype, 0, drill_down_list);
          RPT_reporting_add_integer (local_data->cumul_nanimals_potentially_traced_by_contacttype_and_prodtype, 0, drill_down_list);
          drill_down_list[0] = ADSM_contact_type_abbrev[i];
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
