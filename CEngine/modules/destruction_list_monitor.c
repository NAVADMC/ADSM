/** @file destruction_list_monitor.c
 * Tracks the number of units waiting to be destroyed.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @version 0.1
 * @date April 2004
 *
 * Copyright &copy; University of Guelph, 2004-2009
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
#define new destruction_list_monitor_new
#define run destruction_list_monitor_run
#define local_free destruction_list_monitor_free
#define handle_before_each_simulation_event destruction_list_monitor_handle_before_each_simulation_event
#define handle_new_day_event destruction_list_monitor_handle_new_day_event
#define handle_commitment_to_destroy_event destruction_list_monitor_handle_commitment_to_destroy_event
#define handle_destruction_event destruction_list_monitor_handle_destruction_event

#include "module.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#include "destruction_list_monitor.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "destruction-list-monitor"



/** Specialized information for this model. */
typedef struct
{
  GPtrArray *production_types;
  unsigned int nunits;          /* Number of units. */
  GHashTable *status; /**< The status of each unit with respect to destruction.
    If the unit is not awaiting destruction, it will not be present in the
    table. */
  unsigned int peak_nunits, peak_nanimals;
  unsigned int peak_wait;
  double sum; /**< The numerator for calculating the average wait time. */
  unsigned int count; /**< The denominator for calculating the average wait time. */
  RPT_reporting_t *nunits_awaiting_destruction;
  RPT_reporting_t *nunits_awaiting_destruction_by_prodtype;
  RPT_reporting_t *nanimals_awaiting_destruction;
  RPT_reporting_t *nanimals_awaiting_destruction_by_prodtype;
  RPT_reporting_t *peak_nunits_awaiting_destruction;
  RPT_reporting_t *peak_nunits_awaiting_destruction_day;
  RPT_reporting_t *peak_nanimals_awaiting_destruction;
  RPT_reporting_t *peak_nanimals_awaiting_destruction_day;
  RPT_reporting_t *peak_wait_time;
  RPT_reporting_t *average_wait_time;
  RPT_reporting_t *unit_days_in_queue;
  RPT_reporting_t *animal_days_in_queue;
}
local_data_t;



/**
 * Before each simulation, reset the recorded statistics to zero.
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

  g_hash_table_remove_all (local_data->status);

  RPT_reporting_zero (local_data->nunits_awaiting_destruction);
  RPT_reporting_zero (local_data->nunits_awaiting_destruction_by_prodtype);
  RPT_reporting_zero (local_data->nanimals_awaiting_destruction);
  RPT_reporting_zero (local_data->nanimals_awaiting_destruction_by_prodtype);
  RPT_reporting_zero (local_data->peak_nunits_awaiting_destruction);
  RPT_reporting_set_null (local_data->peak_nunits_awaiting_destruction_day, NULL);
  RPT_reporting_zero (local_data->peak_nanimals_awaiting_destruction);
  RPT_reporting_set_null (local_data->peak_nanimals_awaiting_destruction_day, NULL);
  RPT_reporting_set_null (local_data->peak_wait_time, NULL);
  RPT_reporting_set_null (local_data->average_wait_time, NULL);
  RPT_reporting_zero (local_data->unit_days_in_queue);
  RPT_reporting_zero (local_data->animal_days_in_queue);

  local_data->peak_nunits = local_data->peak_nanimals = 0;
  local_data->peak_wait = 0;
  local_data->sum = local_data->count = 0;

  #if DEBUG
    g_debug ("----- EXIT handle_before_each_simulation_event (%s)", MODEL_NAME);
  #endif

  return;
}



/**
 * Responds to a new day event by updating unit-days in queue and animal-days
 * in queue.
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

  RPT_reporting_add_integer (local_data->unit_days_in_queue,
                             RPT_reporting_get_integer (local_data->nunits_awaiting_destruction, NULL),
                             NULL);
  RPT_reporting_add_integer (local_data->animal_days_in_queue,
                             RPT_reporting_get_integer (local_data->nanimals_awaiting_destruction, NULL),
                             NULL);

#if DEBUG
  g_debug ("----- EXIT handle_new_day_event (%s)", MODEL_NAME);
#endif

  return;
}



/**
 * Responds to a commitment to destroy event by recording the unit's status as
 * "waiting".
 *
 * @param self the model.
 * @param event a commitment to destroy event.
 */
void
handle_commitment_to_destroy_event (struct adsm_module_t_ *self,
                                    EVT_commitment_to_destroy_event_t * event)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  unsigned int nunits, nanimals;

#if DEBUG
  g_debug ("----- ENTER handle_commitment_to_destroy_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;

  if (g_hash_table_lookup (local_data->status, unit) == NULL)
    {
      g_hash_table_insert (local_data->status, unit, GINT_TO_POINTER(1));

      if (NULL != adsm_queue_unit_for_destruction)
        {
          adsm_queue_unit_for_destruction (unit->index);
        }

      /* Increment the count of units awaiting destruction. */
      RPT_reporting_add_integer (local_data->nunits_awaiting_destruction, 1, NULL);
      RPT_reporting_add_integer1 (local_data->nunits_awaiting_destruction_by_prodtype, 1,
                                  unit->production_type_name);
      nunits = RPT_reporting_get_integer (local_data->nunits_awaiting_destruction, NULL);
      if (nunits > local_data->peak_nunits)
        {
          local_data->peak_nunits = nunits;
          RPT_reporting_set_integer (local_data->peak_nunits_awaiting_destruction, nunits, NULL);
          RPT_reporting_set_integer (local_data->peak_nunits_awaiting_destruction_day, event->day, NULL);
        }

      /* Increment the count of animals awaiting destruction. */
      RPT_reporting_add_integer (local_data->nanimals_awaiting_destruction, unit->size, NULL);
      RPT_reporting_add_integer1 (local_data->nanimals_awaiting_destruction_by_prodtype,
                                  unit->size, unit->production_type_name);
      nanimals = RPT_reporting_get_integer (local_data->nanimals_awaiting_destruction, NULL);
      if (nanimals > local_data->peak_nanimals)
        {
          local_data->peak_nanimals = nanimals;
          RPT_reporting_set_integer (local_data->peak_nanimals_awaiting_destruction, nanimals,
                                     NULL);
          RPT_reporting_set_integer (local_data->peak_nanimals_awaiting_destruction_day, event->day,
                                     NULL);
        }
    }

#if DEBUG
  g_debug ("----- EXIT handle_commitment_to_destroy_event (%s)", MODEL_NAME);
#endif
}



/**
 * Responds to a destruction event by removing the unit's "waiting" status and
 * updating the peak and average wait times.
 *
 * @param self the model.
 * @param event a destruction event.
 */
void
handle_destruction_event (struct adsm_module_t_ *self, EVT_destruction_event_t * event)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  unsigned int wait;

#if DEBUG
  g_debug ("----- ENTER handle_destruction_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;

  /* Special case: if a unit's starting state is Destroyed, it won't be on a
   * waiting list and it won't affect the various counts maintained by this
   * monitor. */
  if (g_hash_table_lookup (local_data->status, unit) != NULL)
    {
      /* The day when the unit went onto the waiting list is recorded in the
       * destruction event. */
      wait = event->day - event->day_commitment_made;

      /* Update the peak wait time. */
      local_data->peak_wait = MAX (local_data->peak_wait, wait);
      RPT_reporting_set_integer (local_data->peak_wait_time, local_data->peak_wait, NULL);

      /* Update the average wait time. */
      local_data->sum += wait;
      local_data->count += 1;
      RPT_reporting_set_real (local_data->average_wait_time,
                              local_data->sum / local_data->count, NULL);

      /* Mark the unit as no longer on a waiting list. */
      g_hash_table_remove (local_data->status, unit);

      /* Decrement the counts of units and animals awaiting destruction. */
      RPT_reporting_sub_integer (local_data->nunits_awaiting_destruction, 1, NULL);
      RPT_reporting_sub_integer1 (local_data->nunits_awaiting_destruction_by_prodtype, 1,
                                  unit->production_type_name);
      RPT_reporting_sub_integer (local_data->nanimals_awaiting_destruction, unit->size, NULL);
      RPT_reporting_sub_integer1 (local_data->nanimals_awaiting_destruction_by_prodtype,
                                  unit->size, unit->production_type_name);
    }

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
      handle_new_day_event (self);
      break;
    case EVT_CommitmentToDestroy:
      handle_commitment_to_destroy_event (self, &(event->u.commitment_to_destroy));
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
  g_hash_table_destroy (local_data->status);
  g_free (local_data);
  g_ptr_array_free (self->outputs, /* free_seg = */ TRUE); /* also frees all output variables */
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Returns a new destruction list monitor.
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
    EVT_CommitmentToDestroy,
    EVT_Destruction,
    0
  };
  unsigned int i;      /* loop counter */

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

  local_data->nunits_awaiting_destruction =
    RPT_new_reporting ("deswUAll", RPT_integer);
  local_data->nunits_awaiting_destruction_by_prodtype =
    RPT_new_reporting ("deswU", RPT_group);
  local_data->nanimals_awaiting_destruction =
    RPT_new_reporting ("deswAAll", RPT_integer);
  local_data->nanimals_awaiting_destruction_by_prodtype =
    RPT_new_reporting ("deswA", RPT_group);
  local_data->peak_nunits_awaiting_destruction =
    RPT_new_reporting ("deswUMax", RPT_integer);
  local_data->peak_nunits_awaiting_destruction_day =
    RPT_new_reporting ("deswUMaxDay", RPT_integer);
  local_data->peak_nanimals_awaiting_destruction =
    RPT_new_reporting ("deswAMax", RPT_integer);
  local_data->peak_nanimals_awaiting_destruction_day =
    RPT_new_reporting ("deswAMaxDay", RPT_integer);
  local_data->peak_wait_time =
    RPT_new_reporting ("deswUTimeMax", RPT_integer);
  local_data->average_wait_time =
    RPT_new_reporting ("deswUTimeAvg", RPT_real);
  local_data->unit_days_in_queue =
    RPT_new_reporting ("deswUDaysInQueue", RPT_integer);
  local_data->animal_days_in_queue =
    RPT_new_reporting ("deswADaysInQueue", RPT_integer);
  g_ptr_array_add (self->outputs, local_data->nunits_awaiting_destruction);
  g_ptr_array_add (self->outputs, local_data->nunits_awaiting_destruction_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->nanimals_awaiting_destruction);
  g_ptr_array_add (self->outputs, local_data->nanimals_awaiting_destruction_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->peak_nunits_awaiting_destruction);
  g_ptr_array_add (self->outputs, local_data->peak_nunits_awaiting_destruction_day);
  g_ptr_array_add (self->outputs, local_data->peak_nanimals_awaiting_destruction);
  g_ptr_array_add (self->outputs, local_data->peak_nanimals_awaiting_destruction_day);
  g_ptr_array_add (self->outputs, local_data->peak_wait_time);
  g_ptr_array_add (self->outputs, local_data->average_wait_time);
  g_ptr_array_add (self->outputs, local_data->unit_days_in_queue);
  g_ptr_array_add (self->outputs, local_data->animal_days_in_queue);

  /* Set the reporting frequency for the output variables. */

  local_data->nunits = UNT_unit_list_length (units);
  local_data->production_types = units->production_type_names;
  for (i = 0; i < local_data->production_types->len; i++)
    {
      RPT_reporting_set_integer1 (local_data->nunits_awaiting_destruction_by_prodtype, 0,
                                  (char *) g_ptr_array_index (local_data->production_types, i));
      RPT_reporting_set_integer1 (local_data->nanimals_awaiting_destruction_by_prodtype, 0,
                                  (char *) g_ptr_array_index (local_data->production_types, i));
    }

  /* Initialize the unit status table. */
  local_data->status = g_hash_table_new (g_direct_hash, g_direct_equal);

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file destruction_list_monitor.c */
