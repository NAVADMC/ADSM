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
  RPT_reporting_t   *nunits_potentially_traced;
  RPT_reporting_t  **nunits_potentially_traced_by_contacttype;
  RPT_reporting_t  **nunits_potentially_traced_by_prodtype;
  RPT_reporting_t ***nunits_potentially_traced_by_contacttype_and_prodtype;
  RPT_reporting_t   *cumul_nunits_potentially_traced;
  RPT_reporting_t  **cumul_nunits_potentially_traced_by_contacttype;
  RPT_reporting_t  **cumul_nunits_potentially_traced_by_prodtype;
  RPT_reporting_t ***cumul_nunits_potentially_traced_by_contacttype_and_prodtype;
  RPT_reporting_t   *nunits_traced;
  RPT_reporting_t  **nunits_traced_by_contacttype;
  RPT_reporting_t  **nunits_traced_by_prodtype;
  RPT_reporting_t ***nunits_traced_by_contacttype_and_prodtype;
  RPT_reporting_t   *cumul_nunits_traced;
  RPT_reporting_t  **cumul_nunits_traced_by_contacttype;
  RPT_reporting_t  **cumul_nunits_traced_by_prodtype;
  RPT_reporting_t ***cumul_nunits_traced_by_contacttype_and_prodtype;
  RPT_reporting_t   *nanimals_potentially_traced;
  RPT_reporting_t  **nanimals_potentially_traced_by_contacttype;
  RPT_reporting_t  **nanimals_potentially_traced_by_prodtype;
  RPT_reporting_t ***nanimals_potentially_traced_by_contacttype_and_prodtype;
  RPT_reporting_t   *cumul_nanimals_potentially_traced;
  RPT_reporting_t  **cumul_nanimals_potentially_traced_by_contacttype;
  RPT_reporting_t  **cumul_nanimals_potentially_traced_by_prodtype;
  RPT_reporting_t ***cumul_nanimals_potentially_traced_by_contacttype_and_prodtype;
  RPT_reporting_t   *nanimals_traced;
  RPT_reporting_t  **nanimals_traced_by_contacttype;
  RPT_reporting_t  **nanimals_traced_by_prodtype;
  RPT_reporting_t ***nanimals_traced_by_contacttype_and_prodtype;
  RPT_reporting_t   *cumul_nanimals_traced;
  RPT_reporting_t  **cumul_nanimals_traced_by_contacttype;
  RPT_reporting_t  **cumul_nanimals_traced_by_prodtype;
  RPT_reporting_t ***cumul_nanimals_traced_by_contacttype_and_prodtype;
  GPtrArray *daily_outputs; /**< Daily outputs, in a list to make it easy to
    zero them all at once. */
  GPtrArray *cumul_outputs; /**< Cumulative outputs, is a list to make it easy
    to zero them all at once. */
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
  g_ptr_array_foreach (local_data->cumul_outputs, RPT_reporting_zero_as_GFunc, NULL);

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
  g_ptr_array_foreach (local_data->daily_outputs, RPT_reporting_zero_as_GFunc, NULL);

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
  UNT_trace_t trace;
  ADSM_contact_type contact_type;
  UNT_production_type_t prodtype;
  double nanimals;

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

  contact_type = event->contact_type;
  prodtype = identified_unit->production_type;
  nanimals = (double)(identified_unit->size);

  RPT_reporting_add_integer (local_data->nunits_potentially_traced, 1);
  RPT_reporting_add_integer (local_data->nunits_potentially_traced_by_contacttype[contact_type], 1);
  RPT_reporting_add_integer (local_data->nunits_potentially_traced_by_prodtype[prodtype], 1);
  RPT_reporting_add_integer (local_data->nunits_potentially_traced_by_contacttype_and_prodtype[contact_type][prodtype], 1);
  RPT_reporting_add_integer (local_data->cumul_nunits_potentially_traced, 1);
  RPT_reporting_add_integer (local_data->cumul_nunits_potentially_traced_by_contacttype[contact_type], 1);
  RPT_reporting_add_integer (local_data->cumul_nunits_potentially_traced_by_prodtype[prodtype], 1);
  RPT_reporting_add_integer (local_data->cumul_nunits_potentially_traced_by_contacttype_and_prodtype[contact_type][prodtype], 1);
  RPT_reporting_add_real (local_data->nanimals_potentially_traced, nanimals);
  RPT_reporting_add_real (local_data->nanimals_potentially_traced_by_contacttype[contact_type], nanimals);
  RPT_reporting_add_real (local_data->nanimals_potentially_traced_by_prodtype[prodtype], nanimals);
  RPT_reporting_add_real (local_data->nanimals_potentially_traced_by_contacttype_and_prodtype[contact_type][prodtype], nanimals);
  RPT_reporting_add_real (local_data->cumul_nanimals_potentially_traced, nanimals);
  RPT_reporting_add_real (local_data->cumul_nanimals_potentially_traced_by_contacttype[contact_type], nanimals);
  RPT_reporting_add_real (local_data->cumul_nanimals_potentially_traced_by_prodtype[prodtype], nanimals);
  RPT_reporting_add_real (local_data->cumul_nanimals_potentially_traced_by_contacttype_and_prodtype[contact_type][prodtype], nanimals);

  if (event->traced == TRUE)
    {
      /* Record a successfully traced contact. */

      RPT_reporting_add_integer (local_data->nunits_traced, 1);
      RPT_reporting_add_integer (local_data->nunits_traced_by_contacttype[contact_type], 1);
      RPT_reporting_add_integer (local_data->nunits_traced_by_prodtype[prodtype], 1);
      RPT_reporting_add_integer (local_data->nunits_traced_by_contacttype_and_prodtype[contact_type][prodtype], 1);
      RPT_reporting_add_integer (local_data->cumul_nunits_traced, 1);
      RPT_reporting_add_integer (local_data->cumul_nunits_traced_by_contacttype[contact_type], 1);
      RPT_reporting_add_integer (local_data->cumul_nunits_traced_by_prodtype[prodtype], 1);
      RPT_reporting_add_integer (local_data->cumul_nunits_traced_by_contacttype_and_prodtype[contact_type][prodtype], 1);
      RPT_reporting_add_real (local_data->nanimals_traced, nanimals);
      RPT_reporting_add_real (local_data->nanimals_traced_by_contacttype[contact_type], nanimals);
      RPT_reporting_add_real (local_data->nanimals_traced_by_prodtype[prodtype], nanimals);
      RPT_reporting_add_real (local_data->nanimals_traced_by_contacttype_and_prodtype[contact_type][prodtype], nanimals);
      RPT_reporting_add_real (local_data->cumul_nanimals_traced, nanimals);
      RPT_reporting_add_real (local_data->cumul_nanimals_traced_by_contacttype[contact_type], nanimals);
      RPT_reporting_add_real (local_data->cumul_nanimals_traced_by_prodtype[prodtype], nanimals);
      RPT_reporting_add_real (local_data->cumul_nanimals_traced_by_contacttype_and_prodtype[contact_type][prodtype], nanimals);
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

#if DEBUG
  g_debug ("----- ENTER free (%s)", MODEL_NAME);
#endif

  /* Free the dynamically-allocated parts. */
  local_data = (local_data_t *) (self->model_data);
  g_ptr_array_free (local_data->daily_outputs, /* free_seg = */ TRUE);
  g_ptr_array_free (local_data->cumul_outputs, /* free_seg = */ TRUE);
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
  guint nprodtypes;
  ADSM_contact_type contact_type;
  UNT_production_type_t prodtype;

#if DEBUG
  g_debug ("----- ENTER new (%s)", MODEL_NAME);
#endif

  self = g_new (adsm_module_t, 1);
  local_data = g_new (local_data_t, 1);

  self->name = MODEL_NAME;
  self->events_listened_for = adsm_setup_events_listened_for (events_listened_for);
  self->outputs = g_ptr_array_new();
  self->model_data = local_data;
  self->run = run;
  self->is_listening_for = adsm_model_is_listening_for;
  self->has_pending_actions = adsm_model_answer_no;
  self->has_pending_infections = adsm_model_answer_no;
  self->to_string = adsm_module_to_string_default;
  self->printf = adsm_model_printf;
  self->fprintf = adsm_model_fprintf;
  self->free = local_free;

  local_data->daily_outputs = g_ptr_array_new();
  local_data->cumul_outputs = g_ptr_array_new();
  local_data->production_types = units->production_type_names;
  nprodtypes = local_data->production_types->len;
  {
    RPT_bulk_create_t outputs[] = {
      { &local_data->nunits_potentially_traced, "trnUAllp", RPT_integer,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->nunits_potentially_traced_by_contacttype, "trnU%sp", RPT_integer,
        RPT_CharArray, ADSM_contact_type_abbrev, ADSM_NCONTACT_TYPES,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->nunits_potentially_traced_by_prodtype, "trnUp%s", RPT_integer,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->nunits_potentially_traced_by_contacttype_and_prodtype, "trnU%sp%s", RPT_integer,
        RPT_CharArray, ADSM_contact_type_abbrev, ADSM_NCONTACT_TYPES,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        self->outputs, local_data->daily_outputs },

      { &local_data->cumul_nunits_potentially_traced, "trcUAllp", RPT_integer,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nunits_potentially_traced_by_contacttype, "trcU%sp", RPT_integer,
        RPT_CharArray, ADSM_contact_type_abbrev, ADSM_NCONTACT_TYPES,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nunits_potentially_traced_by_prodtype, "trcUp%s", RPT_integer,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nunits_potentially_traced_by_contacttype_and_prodtype, "trcU%sp%s", RPT_integer,
        RPT_CharArray, ADSM_contact_type_abbrev, ADSM_NCONTACT_TYPES,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        self->outputs, local_data->cumul_outputs },

      { &local_data->nunits_traced, "trnUAll", RPT_integer,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->nunits_traced_by_contacttype, "trnU%s", RPT_integer,
        RPT_CharArray, ADSM_contact_type_abbrev, ADSM_NCONTACT_TYPES,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->nunits_traced_by_prodtype, "trnU%s", RPT_integer,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->nunits_traced_by_contacttype_and_prodtype, "trnU%s%s", RPT_integer,
        RPT_CharArray, ADSM_contact_type_abbrev, ADSM_NCONTACT_TYPES,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        self->outputs, local_data->daily_outputs },

      { &local_data->cumul_nunits_traced, "trcUAll", RPT_integer,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nunits_traced_by_contacttype, "trcU%s", RPT_integer,
        RPT_CharArray, ADSM_contact_type_abbrev, ADSM_NCONTACT_TYPES,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nunits_traced_by_prodtype, "trcU%s", RPT_integer,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nunits_traced_by_contacttype_and_prodtype, "trcU%s%s", RPT_integer,
        RPT_CharArray, ADSM_contact_type_abbrev, ADSM_NCONTACT_TYPES,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        self->outputs, local_data->cumul_outputs },

      { &local_data->nanimals_potentially_traced, "trnAAllp", RPT_real,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->nanimals_potentially_traced_by_contacttype, "trnA%sp", RPT_real,
        RPT_CharArray, ADSM_contact_type_abbrev, ADSM_NCONTACT_TYPES,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->nanimals_potentially_traced_by_prodtype, "trnAp%s", RPT_real,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->nanimals_potentially_traced_by_contacttype_and_prodtype, "trnA%sp%s", RPT_real,
        RPT_CharArray, ADSM_contact_type_abbrev, ADSM_NCONTACT_TYPES,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        self->outputs, local_data->daily_outputs },

      { &local_data->cumul_nanimals_potentially_traced, "trcAAllp", RPT_real,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nanimals_potentially_traced_by_contacttype, "trcA%sp", RPT_real,
        RPT_CharArray, ADSM_contact_type_abbrev, ADSM_NCONTACT_TYPES,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nanimals_potentially_traced_by_prodtype, "trcAp%s", RPT_real,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nanimals_potentially_traced_by_contacttype_and_prodtype, "trcA%sp%s", RPT_real,
        RPT_CharArray, ADSM_contact_type_abbrev, ADSM_NCONTACT_TYPES,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        self->outputs, local_data->cumul_outputs },

      { &local_data->nanimals_traced, "trnAAll", RPT_real,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->nanimals_traced_by_contacttype, "trnA%s", RPT_real,
        RPT_CharArray, ADSM_contact_type_abbrev, ADSM_NCONTACT_TYPES,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->nanimals_traced_by_prodtype, "trnA%s", RPT_real,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->nanimals_traced_by_contacttype_and_prodtype, "trnA%s%s", RPT_real,
        RPT_CharArray, ADSM_contact_type_abbrev, ADSM_NCONTACT_TYPES,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        self->outputs, local_data->daily_outputs },

      { &local_data->cumul_nanimals_traced, "trcAAll", RPT_real,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nanimals_traced_by_contacttype, "trcA%s", RPT_real,
        RPT_CharArray, ADSM_contact_type_abbrev, ADSM_NCONTACT_TYPES,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nanimals_traced_by_prodtype, "trcA%s", RPT_real,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nanimals_traced_by_contacttype_and_prodtype, "trcA%s%s", RPT_real,
        RPT_CharArray, ADSM_contact_type_abbrev, ADSM_NCONTACT_TYPES,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        self->outputs, local_data->cumul_outputs },

      { NULL }
    };  
    RPT_bulk_create (outputs);
  }

  /* Only two of the contact types apply to tracing, so dispose of the other
   * output variables to keep the output neater. */
  for (contact_type = 0; contact_type < ADSM_NCONTACT_TYPES; contact_type++)
    {
      if (contact_type != ADSM_DirectContact && contact_type != ADSM_IndirectContact)
        {
          g_ptr_array_remove_fast (self->outputs, local_data->nunits_potentially_traced_by_contacttype[contact_type] );
          g_ptr_array_remove_fast (self->outputs, local_data->cumul_nunits_potentially_traced_by_contacttype[contact_type] );
          g_ptr_array_remove_fast (self->outputs, local_data->nanimals_potentially_traced_by_contacttype[contact_type] );
          g_ptr_array_remove_fast (self->outputs, local_data->cumul_nanimals_potentially_traced_by_contacttype[contact_type] );
          g_ptr_array_remove_fast (self->outputs, local_data->nunits_traced_by_contacttype[contact_type] );
          g_ptr_array_remove_fast (self->outputs, local_data->cumul_nunits_traced_by_contacttype[contact_type] );
          g_ptr_array_remove_fast (self->outputs, local_data->nanimals_traced_by_contacttype[contact_type] );
          g_ptr_array_remove_fast (self->outputs, local_data->cumul_nanimals_traced_by_contacttype[contact_type] );
          for (prodtype = 0; prodtype < nprodtypes; prodtype++)
            {
              g_ptr_array_remove_fast (self->outputs, local_data->nunits_potentially_traced_by_contacttype_and_prodtype[contact_type][prodtype] );
              g_ptr_array_remove_fast (self->outputs, local_data->cumul_nunits_potentially_traced_by_contacttype_and_prodtype[contact_type][prodtype] );
              g_ptr_array_remove_fast (self->outputs, local_data->nanimals_potentially_traced_by_contacttype_and_prodtype[contact_type][prodtype] );
              g_ptr_array_remove_fast (self->outputs, local_data->cumul_nanimals_potentially_traced_by_contacttype_and_prodtype[contact_type][prodtype] );
              g_ptr_array_remove_fast (self->outputs, local_data->nunits_traced_by_contacttype_and_prodtype[contact_type][prodtype] );
              g_ptr_array_remove_fast (self->outputs, local_data->cumul_nunits_traced_by_contacttype_and_prodtype[contact_type][prodtype] );
              g_ptr_array_remove_fast (self->outputs, local_data->nanimals_traced_by_contacttype_and_prodtype[contact_type][prodtype] );
              g_ptr_array_remove_fast (self->outputs, local_data->cumul_nanimals_traced_by_contacttype_and_prodtype[contact_type][prodtype] );
            }
        }
    }

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file trace_monitor.c */
