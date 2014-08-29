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
#define to_string unit_state_monitor_to_string
#define local_free unit_state_monitor_free
#define handle_before_any_simulations_event unit_state_monitor_handle_before_any_simulations_event
#define handle_before_each_simulation_event unit_state_monitor_handle_before_each_simulation_event
#define handle_unit_state_change_event unit_state_monitor_handle_unit_state_change_event
#define handle_new_day_event unit_state_monitor_handle_new_day_event

#include "module.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#if HAVE_MATH_H
#  include <math.h>
#endif


#include "unit_state_monitor.h"

#include "general.h"

#ifdef USE_SC_GUILIB
#  include <sc_adsm_outputs.h>
#endif

/** This must match an element name in the DTD. */
#define MODEL_NAME "unit-state-monitor"



/** Specialized information for this model. */
typedef struct
{
  GPtrArray *production_types;
  guint *nunits_of_prodtype;
  gdouble nanimals;
  gdouble *nanimals_of_prodtype;
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
 * Before any simulations, count how many units there are of each production
 * type. Also declare this module's output variables.
 * 
 * @param self this module.
 * @param units a list of units.
 * @param queue for any new events this module creates.
 */
void
handle_before_any_simulations_event (struct adsm_module_t_ *self,
                                     UNT_unit_list_t *units,
                                     EVT_event_queue_t *queue)
{
  local_data_t *local_data;
  guint nprodtypes;
  guint nunits, i;
  UNT_unit_t *unit;

  #if DEBUG
    g_debug ("----- ENTER handle_before_any_simulations_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);

  nprodtypes = local_data->production_types->len;
  local_data->nunits_of_prodtype = g_new0 (guint, nprodtypes);
  local_data->nanimals_of_prodtype = g_new0 (gdouble, nprodtypes);
  nunits = UNT_unit_list_length (units);
  local_data->nanimals = 0;
  for (i = 0; i < nunits; i++)
    {
      unit = UNT_unit_list_get (units, i);
      local_data->nunits_of_prodtype[unit->production_type] += 1;
      local_data->nanimals += unit->size;
      local_data->nanimals_of_prodtype[unit->production_type] += unit->size;
    }

  adsm_declare_outputs (self, queue);

  #if DEBUG
    g_debug ("----- EXIT handle_before_any_simulations_event (%s)", MODEL_NAME);
  #endif

  return;
}



/**
 * Before each simulation, this module resets the counts to everyone
 * Susceptible, and deletes any record of the last day of disease left over
 * from a previous iteration.
 * 
 * @param self this module.
 * @param units a list of units.
 */
void
handle_before_each_simulation_event (struct adsm_module_t_ *self,
                                     UNT_unit_list_t *units)
{
  local_data_t *local_data;
  guint nunits, nprodtypes;
  const char *susceptible;
  UNT_production_type_t prodtype;
  const char *drill_down_list[3] = { NULL, NULL, NULL };

  #if DEBUG
    g_debug ("----- ENTER handle_before_each_simulation_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);

  /* First, zero all the counts. */
  RPT_reporting_zero (local_data->num_units_in_state);
  RPT_reporting_zero (local_data->num_units_in_state_by_prodtype);
  RPT_reporting_zero (local_data->num_animals_in_state);
  RPT_reporting_zero (local_data->num_animals_in_state_by_prodtype);

  /* Set all to Susceptible. */
  susceptible = UNT_state_name[Susceptible];
  nunits = UNT_unit_list_length (units);
  RPT_reporting_set_integer1 (local_data->num_units_in_state, nunits, susceptible);
  RPT_reporting_set_real1 (local_data->num_animals_in_state, local_data->nanimals, susceptible);
  nprodtypes = local_data->production_types->len;
  drill_down_list[0] = susceptible;
  for (prodtype = 0; prodtype < nprodtypes; prodtype++)
    {
      drill_down_list[1] = (char *) g_ptr_array_index (local_data->production_types, prodtype);
      RPT_reporting_set_integer (local_data->num_units_in_state_by_prodtype,
                                 local_data->nunits_of_prodtype[prodtype],
                                 drill_down_list);
      RPT_reporting_set_real (local_data->num_animals_in_state_by_prodtype,
                              local_data->nanimals_of_prodtype[prodtype],
                              drill_down_list);
    }

  RPT_reporting_set_null (local_data->last_day_of_disease, NULL);
  local_data->disease_end_recorded = FALSE;

  #if DEBUG
    g_debug ("----- EXIT handle_before_each_simulation_event (%s)", MODEL_NAME);
  #endif

  return;
}



/**
 * Responds to a Unit State Change event by updating the counts of units and
 * animals in each state.
 *
 * @param self this module.
 * @param event a Unit State Change event.
 */
void
handle_unit_state_change_event (struct adsm_module_t_ *self,
                                EVT_unit_state_change_event_t * event)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  const char *old_state;
  const char *new_state;
  const char *drill_down_list[3] = { NULL, NULL, NULL };

  #if DEBUG
    g_debug ("----- ENTER handle_unit_state_change_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);

  unit = event->unit;
  old_state = UNT_state_name[event->old_state];
  new_state = UNT_state_name[event->new_state];
  RPT_reporting_sub_integer1 (local_data->num_units_in_state, 1, old_state);
  RPT_reporting_add_integer1 (local_data->num_units_in_state, 1, new_state);
  RPT_reporting_sub_real1 (local_data->num_animals_in_state, unit->size, old_state);
  RPT_reporting_add_real1 (local_data->num_animals_in_state, unit->size, new_state);

  drill_down_list[0] = old_state;
  drill_down_list[1] = event->unit->production_type_name;
  RPT_reporting_sub_integer (local_data->num_units_in_state_by_prodtype, 1,
                             drill_down_list);
  RPT_reporting_sub_real (local_data->num_animals_in_state_by_prodtype, unit->size,
                          drill_down_list);
  drill_down_list[0] = new_state;
  RPT_reporting_add_integer (local_data->num_units_in_state_by_prodtype, 1,
                             drill_down_list);
  RPT_reporting_add_real (local_data->num_animals_in_state_by_prodtype, unit->size,
                          drill_down_list);

  #if DEBUG
    g_debug ("----- EXIT handle_unit_state_change_event (%s)", MODEL_NAME);
  #endif

  return;
}



/**
 * Responds to a New Day event by updating the average prevalence.
 *
 * @param self this module.
 * @param event a New Day event.
 * @param units a list of units.
 */
void
handle_new_day_event (struct adsm_module_t_ *self,
                      EVT_new_day_event_t *event,
                      UNT_unit_list_t *units)
{
  local_data_t *local_data;
  double prevalence_num, prevalence_denom;
  guint nunits, i;
  UNT_unit_t *unit;
  UNT_state_t state;
  gboolean active_infections;

  #if DEBUG
    g_debug ("----- ENTER handle_new_day_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);

  prevalence_num = prevalence_denom = 0;

  active_infections = FALSE;
  nunits = UNT_unit_list_length (units);
  for (i = 0; i < nunits; i++)
    {
      unit = UNT_unit_list_get (units, i);
      state = unit->state;

      if (state >= Latent && state <= InfectiousClinical)
        {
          active_infections = TRUE;
          prevalence_num += unit->size * unit->prevalence;
          prevalence_denom += unit->size;
        }
    }                   /* end loop over units */

  RPT_reporting_set_real (local_data->avg_prevalence, (prevalence_denom > 0) ?
                          prevalence_num / prevalence_denom : 0, NULL);

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
    case EVT_BeforeAnySimulations:
      handle_before_any_simulations_event (self, units, queue);
      break;
    case EVT_BeforeEachSimulation:
      handle_before_each_simulation_event (self, units);
      break;
    case EVT_UnitStateChange:
      handle_unit_state_change_event (self, &(event->u.unit_state_change));
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
  g_free (local_data->nunits_of_prodtype);
  g_free (local_data->nanimals_of_prodtype);
  g_free (local_data);
  g_ptr_array_free (self->outputs, /* free_seg = */ TRUE); /* also frees all output variables */
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Returns a new infection monitor.
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
    EVT_UnitStateChange,
    EVT_NewDay,
    0
  };
  guint n, i, j;
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
  self->to_string = to_string;
  self->printf = adsm_model_printf;
  self->fprintf = adsm_model_fprintf;
  self->free = local_free;

  local_data->num_units_in_state =
    RPT_new_reporting ("tsdU", RPT_group);
  local_data->num_units_in_state_by_prodtype =
    RPT_new_reporting ("tsdU", RPT_group);
  local_data->num_animals_in_state =
    RPT_new_reporting ("tsdA", RPT_group);
  local_data->num_animals_in_state_by_prodtype =
    RPT_new_reporting ("tsdA", RPT_group);
  local_data->avg_prevalence =
    RPT_new_reporting ("averagePrevalence", RPT_real);
  local_data->last_day_of_disease =
    RPT_new_reporting ("diseaseDuration", RPT_integer);
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
      RPT_reporting_set_real1 (local_data->num_animals_in_state, 0, UNT_state_name[i]);
      drill_down_list[0] = UNT_state_name[i];
      for (j = 0; j < n; j++)
        {
          drill_down_list[1] = (char *) g_ptr_array_index (units->production_type_names, j);
          RPT_reporting_set_integer (local_data->num_units_in_state_by_prodtype, 0, drill_down_list);
          RPT_reporting_set_real (local_data->num_animals_in_state_by_prodtype, 0, drill_down_list);
        }
    }

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file unit_state_monitor.c */
