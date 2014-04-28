/** @file unit_state_monitor.c
 * Tracks the number of units in each disease state.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
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
#define new unit_state_monitor_new
#define run unit_state_monitor_run
#define reset unit_state_monitor_reset
#define events_listened_for unit_state_monitor_events_listened_for
#define to_string unit_state_monitor_to_string
#define local_free unit_state_monitor_free
#define handle_before_any_simulations_event unit_state_monitor_handle_before_any_simulations_event
#define handle_new_day_event unit_state_monitor_handle_new_day_event

#include "module.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#if HAVE_MATH_H
#  include <math.h>
#endif


#include "unit_state_monitor.h"

/* 
unit_state_monitor.c needs access to the functions defined in spreadmodel.h,
even when compiled as a *nix executable (in which case, 
the functions defined will all be NULL). 
*/
#include "spreadmodel.h"

#include "general.h"

#ifdef USE_SC_GUILIB
#  include <sc_spreadmodel_outputs.h>
#endif

/** This must match an element name in the DTD. */
#define MODEL_NAME "unit-state-monitor"



#define NEVENTS_LISTENED_FOR 2
EVT_event_type_t events_listened_for[] =
  { EVT_BeforeAnySimulations,
    EVT_NewDay
};



/** Specialized information for this model. */
typedef struct
{
  GPtrArray *production_types;
  RPT_reporting_t *num_units_in_state;
  RPT_reporting_t *num_units_in_state_by_prodtype;
  RPT_reporting_t *num_animals_in_state;
  RPT_reporting_t *num_animals_in_state_by_prodtype;
  RPT_reporting_t *avg_prevalence;
  RPT_reporting_t *last_day_of_disease;
  gboolean disease_end_recorded;
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
 * On each new day, count the number of units and animals in each state.
 *
 * @param self this module.
 * @param event a new day event.
 */
void
handle_new_day_event (struct spreadmodel_model_t_ *self, EVT_new_day_event_t * event,
                      UNT_unit_list_t *units)
{
  local_data_t *local_data;
  double prevalence_num, prevalence_denom;
  guint nunits, i;
  UNT_unit_t *unit;
  UNT_state_t state;
  const char *drill_down_list[3] = { NULL, NULL, NULL };
  gboolean active_infections;

  #if DEBUG
    g_debug ("----- ENTER handle_new_day_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);

  /* Count the number of units and animals infected, vaccinated, and
   * destroyed, and the number of units and animals in each state. */
  RPT_reporting_zero (local_data->num_units_in_state);
  RPT_reporting_zero (local_data->num_units_in_state_by_prodtype);
  RPT_reporting_zero (local_data->num_animals_in_state);
  RPT_reporting_zero (local_data->num_animals_in_state_by_prodtype);
  prevalence_num = prevalence_denom = 0;

  active_infections = FALSE;
  nunits = UNT_unit_list_length (units);
  for (i = 0; i < nunits; i++)
    {
      unit = UNT_unit_list_get (units, i);
      state = unit->state;

      RPT_reporting_add_integer1 (local_data->num_units_in_state, 1, UNT_state_name[state]);
      RPT_reporting_add_integer1 (local_data->num_animals_in_state, unit->size,
                                  UNT_state_name[state]);
      drill_down_list[0] = unit->production_type_name;
      drill_down_list[1] = UNT_state_name[state];
      RPT_reporting_add_integer (local_data->num_units_in_state_by_prodtype, 1, drill_down_list);
      RPT_reporting_add_integer (local_data->num_animals_in_state_by_prodtype, unit->size,
                                 drill_down_list);

      if (state >= Latent && state <= InfectiousClinical)
        {
          active_infections = TRUE;
          prevalence_num += unit->size * unit->prevalence;
          prevalence_denom += unit->size;
        }
      RPT_reporting_set_real (local_data->avg_prevalence, (prevalence_denom > 0) ?
                              prevalence_num / prevalence_denom : 0, NULL);
    }                   /* end loop over units */

  if (active_infections)
    {
      local_data->disease_end_recorded = FALSE;
    }
  else
    {
      if (local_data->disease_end_recorded == FALSE)
        {
          RPT_reporting_set_integer (local_data->last_day_of_disease, event->day - 1, NULL);
          local_data->disease_end_recorded = TRUE;
        }
    }

  #if DEBUG
    g_debug ("----- EXIT handle_new_day_event (%s)", MODEL_NAME);
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
      handle_new_day_event (self, &(event->u.new_day), units);
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
  RPT_reporting_set_null (local_data->last_day_of_disease, NULL);
  local_data->disease_end_recorded = FALSE;

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
to_string (struct spreadmodel_model_t_ *self)
{
  return g_strdup_printf ("<%s>", MODEL_NAME);
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

#if DEBUG
  g_debug ("----- ENTER free (%s)", MODEL_NAME);
#endif

  /* Free the dynamically-allocated parts. */
  local_data = (local_data_t *) (self->model_data);
  RPT_free_reporting (local_data->num_units_in_state);
  RPT_free_reporting (local_data->num_units_in_state_by_prodtype);
  RPT_free_reporting (local_data->num_animals_in_state);
  RPT_free_reporting (local_data->num_animals_in_state_by_prodtype);
  RPT_free_reporting (local_data->avg_prevalence);

  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Returns a new infection monitor.
 */
spreadmodel_model_t *
new (sqlite3 * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  spreadmodel_model_t *self;
  local_data_t *local_data;
  guint n, i, j;
  const char *drill_down_list[3] = { NULL, NULL, NULL };

#if DEBUG
  g_debug ("----- ENTER new (%s)", MODEL_NAME);
#endif

  self = g_new (spreadmodel_model_t, 1);
  local_data = g_new (local_data_t, 1);

  self->name = MODEL_NAME;
  self->events_listened_for = events_listened_for;
  self->nevents_listened_for = NEVENTS_LISTENED_FOR;
  self->outputs = g_ptr_array_sized_new (18);
  self->model_data = local_data;
  self->run = run;
  self->reset = reset;
  self->is_listening_for = spreadmodel_model_is_listening_for;
  self->has_pending_actions = spreadmodel_model_answer_no;
  self->has_pending_infections = spreadmodel_model_answer_no;
  self->to_string = to_string;
  self->printf = spreadmodel_model_printf;
  self->fprintf = spreadmodel_model_fprintf;
  self->free = local_free;

  local_data->num_units_in_state =
    RPT_new_reporting ("tsdU", RPT_group, RPT_daily);
  local_data->num_units_in_state_by_prodtype =
    RPT_new_reporting ("tsdU", RPT_group, RPT_daily);
  local_data->num_animals_in_state =
    RPT_new_reporting ("tsdA", RPT_group, RPT_daily);
  local_data->num_animals_in_state_by_prodtype =
    RPT_new_reporting ("tsdA", RPT_group, RPT_daily);
  local_data->avg_prevalence =
    RPT_new_reporting ("average-prevalence", RPT_real, RPT_daily);
  local_data->last_day_of_disease =
    RPT_new_reporting ("diseaseDuration", RPT_integer, RPT_daily);
  g_ptr_array_add (self->outputs, local_data->num_units_in_state);
  g_ptr_array_add (self->outputs, local_data->num_units_in_state_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->num_animals_in_state);
  g_ptr_array_add (self->outputs, local_data->num_animals_in_state_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->avg_prevalence);
  g_ptr_array_add (self->outputs, local_data->last_day_of_disease);

  /* Initialize the output variables. */
  local_data->production_types = units->production_type_names;
  n = local_data->production_types->len;
  for (i = 0; i < UNT_NSTATES; i++)
    {
      RPT_reporting_set_integer1 (local_data->num_units_in_state, 0, UNT_state_name[i]);
      RPT_reporting_set_integer1 (local_data->num_animals_in_state, 0, UNT_state_name[i]);
      drill_down_list[1] = UNT_state_name[i];
      for (j = 0; j < n; j++)
        {
          drill_down_list[0] = (char *) g_ptr_array_index (units->production_type_names, j);
          RPT_reporting_set_integer (local_data->num_units_in_state_by_prodtype, 0, drill_down_list);
          RPT_reporting_set_integer (local_data->num_animals_in_state_by_prodtype, 0, drill_down_list);
        }
    }

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file unit_state_monitor.c */
