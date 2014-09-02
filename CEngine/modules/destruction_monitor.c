/** @file destruction_monitor.c
 * Tracks the number of and reasons for destructions.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @version 0.1
 * @date January 2005
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
#define new destruction_monitor_new
#define run destruction_monitor_run
#define local_free destruction_monitor_free
#define handle_before_each_simulation_event destruction_monitor_handle_before_each_simulation_event
#define handle_new_day_event destruction_monitor_handle_new_day_event
#define handle_destruction_event destruction_monitor_handle_destruction_event

#include "module.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#include "destruction_monitor.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "destruction-monitor"



/** Specialized information for this model. */
typedef struct
{
  GPtrArray *production_types;
  RPT_reporting_t   *destruction_occurred;
  RPT_reporting_t   *first_destruction;
  RPT_reporting_t  **first_destruction_by_reason;
  RPT_reporting_t  **first_destruction_by_prodtype;
  RPT_reporting_t ***first_destruction_by_reason_and_prodtype;
  RPT_reporting_t   *num_units_destroyed;
  RPT_reporting_t  **num_units_destroyed_by_reason;
  RPT_reporting_t  **num_units_destroyed_by_prodtype;
  RPT_reporting_t ***num_units_destroyed_by_reason_and_prodtype;
  RPT_reporting_t   *cumul_num_units_destroyed;
  RPT_reporting_t  **cumul_num_units_destroyed_by_reason;
  RPT_reporting_t  **cumul_num_units_destroyed_by_prodtype;
  RPT_reporting_t ***cumul_num_units_destroyed_by_reason_and_prodtype;
  RPT_reporting_t   *num_animals_destroyed;
  RPT_reporting_t  **num_animals_destroyed_by_reason;
  RPT_reporting_t  **num_animals_destroyed_by_prodtype;
  RPT_reporting_t ***num_animals_destroyed_by_reason_and_prodtype;
  RPT_reporting_t   *cumul_num_animals_destroyed;
  RPT_reporting_t  **cumul_num_animals_destroyed_by_reason;
  RPT_reporting_t  **cumul_num_animals_destroyed_by_prodtype;
  RPT_reporting_t ***cumul_num_animals_destroyed_by_reason_and_prodtype;
  GPtrArray *daily_outputs; /**< Daily outputs, in a list to make it easy to
    zero them all at once. */
  GPtrArray *cumul_outputs; /**< Cumulative outputs, in a list to make it easy
    to zero them all at once. */
  GPtrArray *null_outputs; /**< Outputs that start out null, in a list to make
    it easy set them null all at once. */
}
local_data_t;



/**
 * Before each simulation, zero the cumulative counts of destructions.
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
  g_ptr_array_foreach (local_data->null_outputs, RPT_reporting_set_null_as_GFunc, NULL);

  #if DEBUG
    g_debug ("----- EXIT handle_before_each_simulation_event (%s)", MODEL_NAME);
  #endif

  return;
}



/**
 * On each new day, zero the daily counts of destructions.
 *
 * @param self the model.
 * @param event a new day event.
 */
void
handle_new_day_event (struct adsm_module_t_ *self, EVT_new_day_event_t * event)
{
  local_data_t *local_data;

#if DEBUG
  g_debug ("----- ENTER handle_new_day_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* Zero the daily counts. */
  if (event->day > 1)
    {
      g_ptr_array_foreach (local_data->daily_outputs, RPT_reporting_zero_as_GFunc, NULL);
    }

#if DEBUG
  g_debug ("----- EXIT handle_new_day_event (%s)", MODEL_NAME);
#endif
}



/**
 * Responds to a destruction by recording it.
 *
 * @param self the model.
 * @param event a destruction event.
 */
void
handle_destruction_event (struct adsm_module_t_ *self, EVT_destruction_event_t * event)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  UNT_control_t update;
  ADSM_control_reason reason;
  UNT_production_type_t prodtype;
  double nanimals;

#if DEBUG
  g_debug ("----- ENTER handle_destruction_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;

  update.unit_index = unit->index;
  update.day_commitment_made = event->day_commitment_made;
  update.reason = event->reason;
  
#ifdef USE_SC_GUILIB
  sc_destroy_unit( event->day, unit, update );
#else
  if (NULL != adsm_destroy_unit)
    {
      adsm_destroy_unit (update);
    }
#endif  

  reason = event->reason;
  prodtype = unit->production_type;
  nanimals = (double)(unit->size);

  /* Initially destroyed units do not count as the first destruction. */
  if (reason != ADSM_ControlInitialState)
    {
      if (RPT_reporting_is_null (local_data->first_destruction, NULL))
        {
          RPT_reporting_set_integer (local_data->first_destruction, event->day, NULL);
          RPT_reporting_set_integer (local_data->destruction_occurred, 1, NULL);
        }
      if (RPT_reporting_is_null (local_data->first_destruction_by_reason[reason], NULL))
        RPT_reporting_set_integer (local_data->first_destruction_by_reason[reason], event->day, NULL);
      if (RPT_reporting_is_null (local_data->first_destruction_by_prodtype[prodtype], NULL))
        RPT_reporting_set_integer (local_data->first_destruction_by_prodtype[prodtype], event->day, NULL);  
      if (RPT_reporting_is_null (local_data->first_destruction_by_reason_and_prodtype[reason][prodtype], NULL))
        RPT_reporting_set_integer (local_data->first_destruction_by_reason_and_prodtype[reason][prodtype], event->day, NULL);

      /* Initially destroyed units also are not included in many of the counts.
       * They will not be part of desnUAll or desnU broken down by production
       * type.  They will be part of desnUIni and desnUIni broken down by
       * production type. */
      RPT_reporting_add_integer  (local_data->num_units_destroyed, 1, NULL);
      RPT_reporting_add_integer (local_data->num_units_destroyed_by_prodtype[prodtype], 1, NULL);
      RPT_reporting_add_real  (local_data->num_animals_destroyed, nanimals, NULL);
      RPT_reporting_add_real (local_data->num_animals_destroyed_by_prodtype[prodtype], nanimals, NULL);
      RPT_reporting_add_integer  (local_data->cumul_num_units_destroyed, 1, NULL);
      RPT_reporting_add_integer (local_data->cumul_num_units_destroyed_by_prodtype[prodtype], 1, NULL);
      RPT_reporting_add_real  (local_data->cumul_num_animals_destroyed, nanimals, NULL);
      RPT_reporting_add_real (local_data->cumul_num_animals_destroyed_by_prodtype[prodtype], nanimals, NULL);
    }
  RPT_reporting_add_integer (local_data->num_units_destroyed_by_reason[reason], 1, NULL);
  RPT_reporting_add_real (local_data->num_animals_destroyed_by_reason[reason], nanimals, NULL);
  RPT_reporting_add_integer (local_data->cumul_num_units_destroyed_by_reason[reason], 1, NULL);
  RPT_reporting_add_real (local_data->cumul_num_animals_destroyed_by_reason[reason], nanimals, NULL);
  RPT_reporting_add_integer (local_data->num_units_destroyed_by_reason_and_prodtype[reason][prodtype], 1, NULL);
  RPT_reporting_add_real (local_data->num_animals_destroyed_by_reason_and_prodtype[reason][prodtype], nanimals,
                          NULL);
  RPT_reporting_add_integer (local_data->cumul_num_units_destroyed_by_reason_and_prodtype[reason][prodtype], 1,
                             NULL);
  RPT_reporting_add_real (local_data->cumul_num_animals_destroyed_by_reason_and_prodtype[reason][prodtype], nanimals,
                          NULL);

#if DEBUG
  g_debug ("----- EXIT handle_destruction_event (%s)", MODEL_NAME);
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
      handle_new_day_event (self, &(event->u.new_day));
      break;
    case EVT_Destruction:
      handle_destruction_event (self, &(event->u.destruction));
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
  g_ptr_array_free (local_data->null_outputs, /* free_seg = */ TRUE);
  g_free (local_data);
  g_ptr_array_free (self->outputs, /* free_seg = */ TRUE); /* also frees all output variables */
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Returns a new destruction monitor.
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
    EVT_Destruction,
    0
  };
  guint nprodtypes;

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

  local_data->daily_outputs = g_ptr_array_new();
  local_data->cumul_outputs = g_ptr_array_new();
  local_data->null_outputs = g_ptr_array_new();
  local_data->production_types = units->production_type_names;
  nprodtypes = local_data->production_types->len;
  {
    RPT_bulk_create_t outputs[] = {
      { &local_data->destruction_occurred, "destrOccurred", RPT_integer,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->first_destruction, "firstDestruction", RPT_integer,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->null_outputs },

      { &local_data->first_destruction_by_reason, "firstDestruction%s", RPT_integer,
        RPT_CharArray, ADSM_control_reason_abbrev, ADSM_NCONTROL_REASONS,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->null_outputs },

      { &local_data->first_destruction_by_prodtype, "firstDestruction%s", RPT_integer,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->null_outputs },

      { &local_data->first_destruction_by_reason_and_prodtype, "firstDestruction%s%s", RPT_integer,
        RPT_CharArray, ADSM_control_reason_abbrev, ADSM_NCONTROL_REASONS,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        self->outputs, local_data->null_outputs },

      { &local_data->num_units_destroyed, "desnUAll", RPT_integer,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->num_units_destroyed_by_reason, "desnU%s", RPT_integer,
        RPT_CharArray, ADSM_control_reason_abbrev, ADSM_NCONTROL_REASONS,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->num_units_destroyed_by_prodtype, "desnU%s", RPT_integer,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->num_units_destroyed_by_reason_and_prodtype, "desnU%s%s", RPT_integer,
        RPT_CharArray, ADSM_control_reason_abbrev, ADSM_NCONTROL_REASONS,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        self->outputs, local_data->daily_outputs },

      { &local_data->cumul_num_units_destroyed, "descUAll", RPT_integer,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_num_units_destroyed_by_reason, "descU%s", RPT_integer,
        RPT_CharArray, ADSM_control_reason_abbrev, ADSM_NCONTROL_REASONS,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_num_units_destroyed_by_prodtype, "descU%s", RPT_integer,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_num_units_destroyed_by_reason_and_prodtype, "descU%s%s", RPT_integer,
        RPT_CharArray, ADSM_control_reason_abbrev, ADSM_NCONTROL_REASONS,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        self->outputs, local_data->cumul_outputs },

      { &local_data->num_animals_destroyed, "desnAAll", RPT_real,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->num_animals_destroyed_by_reason, "desnA%s", RPT_real,
        RPT_CharArray, ADSM_control_reason_abbrev, ADSM_NCONTROL_REASONS,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->num_animals_destroyed_by_prodtype, "desnA%s", RPT_real,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->num_animals_destroyed_by_reason_and_prodtype, "desnA%s%s", RPT_real,
        RPT_CharArray, ADSM_control_reason_abbrev, ADSM_NCONTROL_REASONS,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        self->outputs, local_data->daily_outputs },

      { &local_data->cumul_num_animals_destroyed, "descAAll", RPT_real,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_num_animals_destroyed_by_reason, "descA%s", RPT_real,
        RPT_CharArray, ADSM_control_reason_abbrev, ADSM_NCONTROL_REASONS,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_num_animals_destroyed_by_prodtype, "descA%s", RPT_real,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_num_animals_destroyed_by_reason_and_prodtype, "descA%s%s", RPT_real,
        RPT_CharArray, ADSM_control_reason_abbrev, ADSM_NCONTROL_REASONS,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        self->outputs, local_data->cumul_outputs },

      { NULL }
    };  
    RPT_bulk_create (outputs);
  }

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file destruction_monitor.c */
