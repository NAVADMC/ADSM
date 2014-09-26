/** @file exposure_monitor.c
 * Tracks the cause of exposures.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @version 0.1
 * @date August 2004
 *
 * Copyright &copy; University of Guelph, 2004-2012
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#if HAVE_CONFIG_H
#  include "config.h"
#endif

/* To avoid name clashes when multiple modules have the same interface. */
#define new exposure_monitor_new
#define run exposure_monitor_run
#define local_free exposure_monitor_free
#define handle_before_each_simulation_event exposure_monitor_handle_before_each_simulation_event
#define handle_new_day_event exposure_monitor_handle_new_day_event
#define handle_exposure_event exposure_monitor_handle_exposure_event

#include "module.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#include "exposure_monitor.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "exposure-monitor"



/** Specialized information for this model. */
typedef struct
{
  GPtrArray *production_types;
  RPT_reporting_t   *num_units_exposed;
  RPT_reporting_t  **num_units_exposed_by_cause;
  RPT_reporting_t  **num_units_exposed_by_prodtype;
  RPT_reporting_t ***num_units_exposed_by_cause_and_prodtype;
  RPT_reporting_t   *cumul_num_units_exposed;
  RPT_reporting_t  **cumul_num_units_exposed_by_cause;
  RPT_reporting_t  **cumul_num_units_exposed_by_prodtype;
  RPT_reporting_t ***cumul_num_units_exposed_by_cause_and_prodtype;
  RPT_reporting_t   *num_animals_exposed;
  RPT_reporting_t  **num_animals_exposed_by_cause;
  RPT_reporting_t  **num_animals_exposed_by_prodtype;
  RPT_reporting_t ***num_animals_exposed_by_cause_and_prodtype;
  RPT_reporting_t   *cumul_num_animals_exposed;
  RPT_reporting_t  **cumul_num_animals_exposed_by_cause;
  RPT_reporting_t  **cumul_num_animals_exposed_by_prodtype;
  RPT_reporting_t ***cumul_num_animals_exposed_by_cause_and_prodtype;
  RPT_reporting_t   *num_adequate_exposures;
  RPT_reporting_t   *cumul_num_adequate_exposures;
  RPT_reporting_t  **cumul_num_adequate_exposures_by_cause;
  GPtrArray *daily_outputs; /**< Daily outputs, in a list to make it easy to
    zero them all at once. */
  GPtrArray *cumul_outputs; /**< Cumulative outputs, is a list to make it easy
    to zero them all at once. */
}
local_data_t;



/**
 * Before each simulation, zero the cumulative counts of exposures.
 *
 * @param self the model.
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
 * On each new day, zero the daily counts of exposures.
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
 * Responds to an exposure event by recording it.
 *
 * @param self the model.
 * @param event an exposure event.
 */
void
handle_exposure_event (struct adsm_module_t_ *self, EVT_exposure_event_t * event)
{
  local_data_t *local_data;
  UNT_unit_t *exposing_unit, *exposed_unit;
  UNT_expose_t update;
  ADSM_contact_type cause;
  UNT_production_type_t prodtype;
  double nanimals;
  
#if DEBUG
  g_debug ("----- ENTER handle_exposure_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  exposing_unit = event->exposing_unit;
  exposed_unit = event->exposed_unit;

  cause = event->contact_type;
                                
  /* No exposing unit means this is an initially infected unit. */
  if (exposing_unit != NULL)
    {
      update.src_index = exposing_unit->index;
      update.src_state = (ADSM_disease_state) exposing_unit->state;
      update.dest_index = exposed_unit->index;
      update.dest_state = (ADSM_disease_state) exposed_unit->state;
  
      update.initiated_day = (int) event->initiated_day;
      update.finalized_day = (int) event->initiated_day + event->delay;
  
      if( TRUE == event->adequate )
        update.is_adequate = ADSM_SuccessTrue;
      else
        update.is_adequate = ADSM_SuccessFalse;
  
      switch (event->contact_type)
        {
          case ADSM_DirectContact:
          case ADSM_IndirectContact:
          case ADSM_AirborneSpread:
            update.exposure_method = event->contact_type;
            break;      
          default:
            /* If this condition occurs, someone forgot something. */
            g_error( "An unrecognized exposure mechanism (%s) occurred in handle_exposure_event", cause );
            update.exposure_method = 0;     
        }

    #ifdef USE_SC_GUILIB
      sc_expose_unit( exposed_unit, update );
    #else	  
      if (NULL != adsm_expose_unit)
        {
          adsm_expose_unit (update);
        }
    #endif  

    #if UNDEFINED
      printf ("unit at index %d exposed by method %s\n", event->exposed_unit->index, cause);
    #endif

      /* Update the counts of exposures. */
      prodtype = exposed_unit->production_type;
      nanimals = (double)(exposed_unit->size);
      RPT_reporting_add_integer (local_data->num_units_exposed, 1);
      RPT_reporting_add_integer (local_data->num_units_exposed_by_cause[cause], 1);
      RPT_reporting_add_integer (local_data->num_units_exposed_by_prodtype[prodtype], 1);
      RPT_reporting_add_integer (local_data->num_units_exposed_by_cause_and_prodtype[cause][prodtype], 1);
      RPT_reporting_add_real (local_data->num_animals_exposed, nanimals);
      RPT_reporting_add_real (local_data->num_animals_exposed_by_cause[cause], nanimals);
      RPT_reporting_add_real (local_data->num_animals_exposed_by_prodtype[prodtype], nanimals);
      RPT_reporting_add_real (local_data->num_animals_exposed_by_cause_and_prodtype[cause][prodtype], nanimals);
      RPT_reporting_add_integer (local_data->cumul_num_units_exposed, 1);
      RPT_reporting_add_integer (local_data->cumul_num_units_exposed_by_cause[cause], 1);
      RPT_reporting_add_integer (local_data->cumul_num_units_exposed_by_prodtype[prodtype], 1);
      RPT_reporting_add_integer (local_data->cumul_num_units_exposed_by_cause_and_prodtype[cause][prodtype], 1);
      RPT_reporting_add_real (local_data->cumul_num_animals_exposed, nanimals);
      RPT_reporting_add_real (local_data->cumul_num_animals_exposed_by_cause[cause], nanimals);
      RPT_reporting_add_real (local_data->cumul_num_animals_exposed_by_prodtype[prodtype], nanimals);
      RPT_reporting_add_real (local_data->cumul_num_animals_exposed_by_cause_and_prodtype[cause][prodtype], nanimals);
      if (event->adequate)
        {
          RPT_reporting_add_integer (local_data->num_adequate_exposures, 1);
          RPT_reporting_add_integer (local_data->cumul_num_adequate_exposures, 1);
          RPT_reporting_add_integer (local_data->cumul_num_adequate_exposures_by_cause[cause], 1);
        }
    }

#if DEBUG
  g_debug ("----- EXIT handle_exposure_event (%s)", MODEL_NAME);
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
    case EVT_Exposure:
      handle_exposure_event (self, &(event->u.exposure));
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
 * Returns a new exposure monitor.
 */
adsm_module_t *
new (sqlite3 * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  adsm_module_t *self;
  local_data_t *local_data;
  EVT_event_type_t events_listened_for[] = {
    EVT_BeforeAnySimulations,
    EVT_BeforeEachSimulation,
    EVT_NewDay,
    EVT_Exposure,
    0
  };
  guint nprodtypes;
  ADSM_contact_type cause;
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
      { &local_data->num_units_exposed, "expnU", RPT_integer,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->num_units_exposed_by_cause, "expnU%s", RPT_integer,
        RPT_CharArray, ADSM_contact_type_abbrev, ADSM_NCONTACT_TYPES,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->num_units_exposed_by_prodtype, "expnU%s", RPT_integer,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->num_units_exposed_by_cause_and_prodtype, "expnU%s%s", RPT_integer,
        RPT_CharArray, ADSM_contact_type_abbrev, ADSM_NCONTACT_TYPES,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        self->outputs, local_data->daily_outputs },

      { &local_data->cumul_num_units_exposed, "expcU", RPT_integer,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_num_units_exposed_by_cause, "expcU%s", RPT_integer,
        RPT_CharArray, ADSM_contact_type_abbrev, ADSM_NCONTACT_TYPES,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_num_units_exposed_by_prodtype, "expcU%s", RPT_integer,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_num_units_exposed_by_cause_and_prodtype, "expcU%s%s", RPT_integer,
        RPT_CharArray, ADSM_contact_type_abbrev, ADSM_NCONTACT_TYPES,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        self->outputs, local_data->cumul_outputs },

      { &local_data->num_animals_exposed, "expnA", RPT_real,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->num_animals_exposed_by_cause, "expnA%s", RPT_real,
        RPT_CharArray, ADSM_contact_type_abbrev, ADSM_NCONTACT_TYPES,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->num_animals_exposed_by_prodtype, "expnA%s", RPT_real,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->num_animals_exposed_by_cause_and_prodtype, "expnA%s%s", RPT_real,
        RPT_CharArray, ADSM_contact_type_abbrev, ADSM_NCONTACT_TYPES,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        self->outputs, local_data->daily_outputs },

      { &local_data->cumul_num_animals_exposed, "expcA", RPT_real,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_num_animals_exposed_by_cause, "expcA%s", RPT_real,
        RPT_CharArray, ADSM_contact_type_abbrev, ADSM_NCONTACT_TYPES,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_num_animals_exposed_by_prodtype, "expcA%s", RPT_real,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_num_animals_exposed_by_cause_and_prodtype, "expcA%s%s", RPT_real,
        RPT_CharArray, ADSM_contact_type_abbrev, ADSM_NCONTACT_TYPES,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        self->outputs, local_data->cumul_outputs },

      { &local_data->num_adequate_exposures, "adqnU", RPT_integer,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->cumul_num_adequate_exposures, "adqcU", RPT_integer,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_num_adequate_exposures_by_cause, "adqcU%s", RPT_integer,
        RPT_CharArray, ADSM_contact_type_abbrev, ADSM_NCONTACT_TYPES,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { NULL }
    };  
    RPT_bulk_create (outputs);
  }

  /* Dispose of a few output variables we aren't interested in, to keep the
   * output neater. */
  for (cause = 0; cause < ADSM_NCONTACT_TYPES; cause++)
    {
      if (cause == ADSM_UnspecifiedInfectionType || cause == ADSM_InitiallyInfected)
        {
          g_ptr_array_remove_fast (self->outputs, local_data->num_units_exposed_by_cause[cause] );
          g_ptr_array_remove_fast (self->outputs, local_data->cumul_num_units_exposed_by_cause[cause] );
          g_ptr_array_remove_fast (self->outputs, local_data->num_animals_exposed_by_cause[cause] );
          g_ptr_array_remove_fast (self->outputs, local_data->cumul_num_animals_exposed_by_cause[cause] );
          g_ptr_array_remove_fast (self->outputs, local_data->cumul_num_adequate_exposures_by_cause[cause] );
          for (prodtype = 0; prodtype < nprodtypes; prodtype++)
            {
              g_ptr_array_remove_fast (self->outputs, local_data->num_units_exposed_by_cause_and_prodtype[cause][prodtype] );
              g_ptr_array_remove_fast (self->outputs, local_data->cumul_num_units_exposed_by_cause_and_prodtype[cause][prodtype] );
              g_ptr_array_remove_fast (self->outputs, local_data->num_animals_exposed_by_cause_and_prodtype[cause][prodtype] );
              g_ptr_array_remove_fast (self->outputs, local_data->cumul_num_animals_exposed_by_cause_and_prodtype[cause][prodtype] );
            }
        }
    }

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file exposure_monitor.c */
