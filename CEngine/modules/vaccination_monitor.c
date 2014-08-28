/** @file vaccination_monitor.c
 * Tracks the number of and reasons for vaccinations.
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
#define new vaccination_monitor_new
#define run vaccination_monitor_run
#define local_free vaccination_monitor_free
#define handle_before_each_simulation_event vaccination_monitor_handle_before_each_simulation_event
#define handle_new_day_event vaccination_monitor_handle_new_day_event
#define handle_declaration_of_vaccination_reasons_event vaccination_monitor_handle_declaration_of_vaccination_reasons_event
#define handle_vaccination_event vaccination_monitor_handle_vaccination_event

#include "module.h"

#include "vaccination_monitor.h"

#if STDC_HEADERS
#  include <string.h>
#endif

/** This must match an element name in the DTD. */
#define MODEL_NAME "vaccination-monitor"



/** Specialized information for this model. */
typedef struct
{
  GPtrArray *production_types;
  RPT_reporting_t *vaccination_occurred;
  RPT_reporting_t *first_vaccination;
  RPT_reporting_t *first_vaccination_by_reason;
  RPT_reporting_t *first_vaccination_by_prodtype;
  RPT_reporting_t *first_vaccination_by_reason_and_prodtype;
  RPT_reporting_t *num_units_vaccinated;
  RPT_reporting_t *num_units_vaccinated_by_reason;
  RPT_reporting_t *num_units_vaccinated_by_prodtype;
  RPT_reporting_t *num_units_vaccinated_by_reason_and_prodtype;
  RPT_reporting_t *cumul_num_units_vaccinated;
  RPT_reporting_t *cumul_num_units_vaccinated_by_reason;
  RPT_reporting_t *cumul_num_units_vaccinated_by_prodtype;
  RPT_reporting_t *cumul_num_units_vaccinated_by_reason_and_prodtype;
  RPT_reporting_t *num_animals_vaccinated;
  RPT_reporting_t *num_animals_vaccinated_by_reason;
  RPT_reporting_t *num_animals_vaccinated_by_prodtype;
  RPT_reporting_t *num_animals_vaccinated_by_reason_and_prodtype;
  RPT_reporting_t *cumul_num_animals_vaccinated;
  RPT_reporting_t *cumul_num_animals_vaccinated_by_reason;
  RPT_reporting_t *cumul_num_animals_vaccinated_by_prodtype;
  RPT_reporting_t *cumul_num_animals_vaccinated_by_reason_and_prodtype;
}
local_data_t;



/**
 * Before each simulation, zero the cumulative counts of vaccinations.
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
  RPT_reporting_zero (local_data->vaccination_occurred);
  RPT_reporting_set_null (local_data->first_vaccination, NULL);
  RPT_reporting_set_null (local_data->first_vaccination_by_reason, NULL);
  RPT_reporting_set_null (local_data->first_vaccination_by_prodtype, NULL);
  RPT_reporting_set_null (local_data->first_vaccination_by_reason_and_prodtype, NULL);
  RPT_reporting_zero (local_data->num_units_vaccinated);
  RPT_reporting_zero (local_data->num_units_vaccinated_by_reason);
  RPT_reporting_zero (local_data->num_units_vaccinated_by_prodtype);
  RPT_reporting_zero (local_data->num_units_vaccinated_by_reason_and_prodtype);
  RPT_reporting_zero (local_data->cumul_num_units_vaccinated);
  RPT_reporting_zero (local_data->cumul_num_units_vaccinated_by_reason);
  RPT_reporting_zero (local_data->cumul_num_units_vaccinated_by_prodtype);
  RPT_reporting_zero (local_data->cumul_num_units_vaccinated_by_reason_and_prodtype);
  RPT_reporting_zero (local_data->num_animals_vaccinated);
  RPT_reporting_zero (local_data->num_animals_vaccinated_by_reason);
  RPT_reporting_zero (local_data->num_animals_vaccinated_by_prodtype);
  RPT_reporting_zero (local_data->num_animals_vaccinated_by_reason_and_prodtype);
  RPT_reporting_zero (local_data->cumul_num_animals_vaccinated);
  RPT_reporting_zero (local_data->cumul_num_animals_vaccinated_by_reason);
  RPT_reporting_zero (local_data->cumul_num_animals_vaccinated_by_prodtype);
  RPT_reporting_zero (local_data->cumul_num_animals_vaccinated_by_reason_and_prodtype);

  #if DEBUG
    g_debug ("----- EXIT handle_before_each_simulation_event (%s)", MODEL_NAME);
  #endif

  return;
}



/**
 * On each new day, zero the daily counts of vaccinations.
 *
 * @param self the module.
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
      RPT_reporting_zero (local_data->num_units_vaccinated);
      RPT_reporting_zero (local_data->num_units_vaccinated_by_reason);
      RPT_reporting_zero (local_data->num_units_vaccinated_by_prodtype);
      RPT_reporting_zero (local_data->num_units_vaccinated_by_reason_and_prodtype);
      RPT_reporting_zero (local_data->num_animals_vaccinated);
      RPT_reporting_zero (local_data->num_animals_vaccinated_by_reason);
      RPT_reporting_zero (local_data->num_animals_vaccinated_by_prodtype);
      RPT_reporting_zero (local_data->num_animals_vaccinated_by_reason_and_prodtype);
    }

#if DEBUG
  g_debug ("----- EXIT handle_new_day_event (%s)", MODEL_NAME);
#endif
}



/**
 * Responds to a declaration of vaccination reasons by recording the potential
 * reasons for vaccination.
 *
 * @param self the model.
 * @param event a declaration of vaccination reasons event.
 */
void
handle_declaration_of_vaccination_reasons_event (struct adsm_module_t_ *self,
                                                 EVT_declaration_of_vaccination_reasons_event_t *
                                                 event)
{
  local_data_t *local_data;
  unsigned int n, i, j;
  const char *reason;
  const char *drill_down_list[3] = { NULL, NULL, NULL };
  
#if DEBUG
  g_debug ("----- ENTER handle_declaration_of_vaccination_reasons_event (%s)", MODEL_NAME);
#endif
    
  local_data = (local_data_t *) (self->model_data);

  /* If any potential reason is not already present in our reporting variables,
   * add it, with an initial count of 0 vaccinations. */
  n = event->reasons->len;
  for (i = 0; i < n; i++)
    {
      reason = (char *) g_ptr_array_index (event->reasons, i);
      /* Two function calls for the first_vaccination variable: one to
       * establish the type of the sub-variable (it's an integer), and one to
       * clear it to "null" (it has no meaningful value until a vaccination
       * occurs). */
      RPT_reporting_add_integer1 (local_data->first_vaccination_by_reason, 0, reason);
      RPT_reporting_set_null1 (local_data->first_vaccination_by_reason, reason);
      RPT_reporting_add_integer1 (local_data->num_units_vaccinated_by_reason, 0, reason);
      RPT_reporting_add_integer1 (local_data->cumul_num_units_vaccinated_by_reason, 0, reason);
      RPT_reporting_add_integer1 (local_data->num_animals_vaccinated_by_reason, 0, reason);
      RPT_reporting_add_integer1 (local_data->cumul_num_animals_vaccinated_by_reason, 0, reason);

      drill_down_list[0] = reason;
      for (j = 0; j < local_data->production_types->len; j++)
        {
          drill_down_list[1] = (char *) g_ptr_array_index (local_data->production_types, j);
          RPT_reporting_add_integer (local_data->first_vaccination_by_reason_and_prodtype, 0,
                                     drill_down_list);
          RPT_reporting_set_null (local_data->first_vaccination_by_reason_and_prodtype,
                                  drill_down_list);
          RPT_reporting_add_integer (local_data->num_units_vaccinated_by_reason_and_prodtype, 0,
                                     drill_down_list);
          RPT_reporting_add_integer (local_data->cumul_num_units_vaccinated_by_reason_and_prodtype, 0,
                                     drill_down_list);
          RPT_reporting_add_integer (local_data->num_animals_vaccinated_by_reason_and_prodtype, 0,
                                     drill_down_list);
          RPT_reporting_add_integer (local_data->cumul_num_animals_vaccinated_by_reason_and_prodtype, 0,
                                     drill_down_list);
        }
    }

#if DEBUG
  g_debug ("----- EXIT handle_declaration_of_vaccination_reasons_event (%s)", MODEL_NAME);
#endif
}



/**
 * Responds to a vaccination by recording it.
 *
 * @param self the model.
 * @param event a vaccination event.
 */
void
handle_vaccination_event (struct adsm_module_t_ *self, EVT_vaccination_event_t * event)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  const char *reason;
  const char *drill_down_list[3] = { NULL, NULL, NULL };
  UNT_control_t update;
  
#if DEBUG
  g_debug ("----- ENTER handle_vaccination_event (%s)", MODEL_NAME);
#endif 
  
  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;

  update.unit_index = unit->index;
  update.day_commitment_made = event->day_commitment_made;
  update.reason = event->reason;
  
#ifdef USE_SC_GUILIB
  sc_vaccinate_unit( event->day, unit, update );
#else  
  if (NULL != adsm_vaccinate_unit)
    {
      adsm_vaccinate_unit (update);
    }
#endif  

  reason = ADSM_control_reason_abbrev[event->reason];
  drill_down_list[0] = reason;
  drill_down_list[1] = unit->production_type_name;
  
  /* Initially vaccinated units do not count as the first vaccination. */
  if (event->reason != ADSM_ControlInitialState)
    {
      if (RPT_reporting_is_null (local_data->first_vaccination, NULL))
        {
          RPT_reporting_set_integer (local_data->first_vaccination, event->day, NULL);
          RPT_reporting_set_integer (local_data->vaccination_occurred, 1, NULL);
        }
      if (RPT_reporting_is_null1 (local_data->first_vaccination_by_reason, reason))
        RPT_reporting_set_integer1 (local_data->first_vaccination_by_reason, event->day, reason);
      if (RPT_reporting_is_null1 (local_data->first_vaccination_by_prodtype, unit->production_type_name))
        RPT_reporting_set_integer1 (local_data->first_vaccination_by_prodtype, event->day, unit->production_type_name);  
      if (RPT_reporting_is_null (local_data->first_vaccination_by_reason_and_prodtype, drill_down_list))
        RPT_reporting_set_integer (local_data->first_vaccination_by_reason_and_prodtype, event->day, drill_down_list);

      /* Initially vaccinated units also are not included in many of the
       * counts.  They will not be part of vacnUAll or vacnU broken down by
       * production type.  They will be part of vacnUIni and vacnUIni broken
       * down by production type. */
      RPT_reporting_add_integer  (local_data->num_units_vaccinated, 1, NULL);
      RPT_reporting_add_integer1 (local_data->num_units_vaccinated_by_prodtype, 1, unit->production_type_name);
      RPT_reporting_add_integer  (local_data->num_animals_vaccinated, unit->size, NULL);
      RPT_reporting_add_integer1 (local_data->num_animals_vaccinated_by_prodtype, unit->size, unit->production_type_name);
      RPT_reporting_add_integer  (local_data->cumul_num_units_vaccinated, 1, NULL);
      RPT_reporting_add_integer1 (local_data->cumul_num_units_vaccinated_by_prodtype, 1, unit->production_type_name);
      RPT_reporting_add_integer  (local_data->cumul_num_animals_vaccinated, unit->size, NULL);
      RPT_reporting_add_integer1 (local_data->cumul_num_animals_vaccinated_by_prodtype, unit->size, unit->production_type_name);
    }
  RPT_reporting_add_integer1 (local_data->num_units_vaccinated_by_reason, 1, reason);
  RPT_reporting_add_integer1 (local_data->num_animals_vaccinated_by_reason, unit->size, reason);
  RPT_reporting_add_integer1 (local_data->cumul_num_units_vaccinated_by_reason, 1, reason);
  RPT_reporting_add_integer1 (local_data->cumul_num_animals_vaccinated_by_reason, unit->size, reason);
  RPT_reporting_add_integer (local_data->num_units_vaccinated_by_reason_and_prodtype, 1, drill_down_list);
  RPT_reporting_add_integer (local_data->num_animals_vaccinated_by_reason_and_prodtype, unit->size,
                             drill_down_list);
  RPT_reporting_add_integer (local_data->cumul_num_units_vaccinated_by_reason_and_prodtype, 1,
                             drill_down_list);
  RPT_reporting_add_integer (local_data->cumul_num_animals_vaccinated_by_reason_and_prodtype, unit->size,
                             drill_down_list);

#if DEBUG
  g_debug ("----- EXIT handle_vaccination_event (%s)", MODEL_NAME);
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
    case EVT_DeclarationOfVaccinationReasons:
      handle_declaration_of_vaccination_reasons_event (self,
                                                       &(event->u.
                                                         declaration_of_vaccination_reasons));
      break;
    case EVT_Vaccination:
      handle_vaccination_event (self, &(event->u.vaccination));
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
  RPT_free_reporting (local_data->vaccination_occurred);
  RPT_free_reporting (local_data->first_vaccination);
  RPT_free_reporting (local_data->first_vaccination_by_reason);
  RPT_free_reporting (local_data->first_vaccination_by_prodtype);
  RPT_free_reporting (local_data->first_vaccination_by_reason_and_prodtype);
  RPT_free_reporting (local_data->num_units_vaccinated);
  RPT_free_reporting (local_data->num_units_vaccinated_by_reason);
  RPT_free_reporting (local_data->num_units_vaccinated_by_prodtype);
  RPT_free_reporting (local_data->num_units_vaccinated_by_reason_and_prodtype);
  RPT_free_reporting (local_data->cumul_num_units_vaccinated);
  RPT_free_reporting (local_data->cumul_num_units_vaccinated_by_reason);
  RPT_free_reporting (local_data->cumul_num_units_vaccinated_by_prodtype);
  RPT_free_reporting (local_data->cumul_num_units_vaccinated_by_reason_and_prodtype);
  RPT_free_reporting (local_data->num_animals_vaccinated);
  RPT_free_reporting (local_data->num_animals_vaccinated_by_reason);
  RPT_free_reporting (local_data->num_animals_vaccinated_by_prodtype);
  RPT_free_reporting (local_data->num_animals_vaccinated_by_reason_and_prodtype);
  RPT_free_reporting (local_data->cumul_num_animals_vaccinated);
  RPT_free_reporting (local_data->cumul_num_animals_vaccinated_by_reason);
  RPT_free_reporting (local_data->cumul_num_animals_vaccinated_by_prodtype);
  RPT_free_reporting (local_data->cumul_num_animals_vaccinated_by_reason_and_prodtype);

  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Returns a new vaccination monitor.
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
    EVT_DeclarationOfVaccinationReasons,
    EVT_Vaccination,
    0
  };
  unsigned int n;
  unsigned int i;      /* loop counter */
  char *prodtype_name;
  const char *drill_down_list[3] = { NULL, NULL, NULL };

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
  self->is_listening_for = adsm_model_is_listening_for;
  self->has_pending_actions = adsm_model_answer_no;
  self->has_pending_infections = adsm_model_answer_no;
  self->to_string = adsm_module_to_string_default;
  self->printf = adsm_model_printf;
  self->fprintf = adsm_model_fprintf;
  self->free = local_free;

  local_data->vaccination_occurred =
    RPT_new_reporting ("vaccOccurred", RPT_integer);
  local_data->first_vaccination =
    RPT_new_reporting ("firstVaccination", RPT_integer);
  local_data->first_vaccination_by_reason =
    RPT_new_reporting ("firstVaccination", RPT_group);
  local_data->first_vaccination_by_prodtype =
    RPT_new_reporting ("firstVaccination", RPT_group);
  local_data->first_vaccination_by_reason_and_prodtype =
    RPT_new_reporting ("firstVaccination", RPT_group);
  local_data->num_units_vaccinated =
    RPT_new_reporting ("vacnUAll", RPT_integer);
  local_data->num_units_vaccinated_by_reason =
    RPT_new_reporting ("vacnU", RPT_group);
  local_data->num_units_vaccinated_by_prodtype =
    RPT_new_reporting ("vacnU", RPT_group);
  local_data->num_units_vaccinated_by_reason_and_prodtype =
    RPT_new_reporting ("vacnU", RPT_group);
  local_data->cumul_num_units_vaccinated =
    RPT_new_reporting ("vaccUAll", RPT_integer);
  local_data->cumul_num_units_vaccinated_by_reason =
    RPT_new_reporting ("vaccU", RPT_group);
  local_data->cumul_num_units_vaccinated_by_prodtype =
    RPT_new_reporting ("vaccU", RPT_group);
  local_data->cumul_num_units_vaccinated_by_reason_and_prodtype =
    RPT_new_reporting ("vaccU", RPT_group);
  local_data->num_animals_vaccinated =
    RPT_new_reporting ("vacnAAll", RPT_integer);
  local_data->num_animals_vaccinated_by_reason =
    RPT_new_reporting ("vacnA", RPT_group);
  local_data->num_animals_vaccinated_by_prodtype =
    RPT_new_reporting ("vacnA", RPT_group);
  local_data->num_animals_vaccinated_by_reason_and_prodtype =
    RPT_new_reporting ("vacnA", RPT_group);
  local_data->cumul_num_animals_vaccinated =
    RPT_new_reporting ("vaccAAll", RPT_integer);
  local_data->cumul_num_animals_vaccinated_by_reason =
    RPT_new_reporting ("vaccA", RPT_group);
  local_data->cumul_num_animals_vaccinated_by_prodtype =
    RPT_new_reporting ("vaccA", RPT_group);
  local_data->cumul_num_animals_vaccinated_by_reason_and_prodtype =
    RPT_new_reporting ("vaccA", RPT_group);
  g_ptr_array_add (self->outputs, local_data->vaccination_occurred);
  g_ptr_array_add (self->outputs, local_data->first_vaccination);
  g_ptr_array_add (self->outputs, local_data->first_vaccination_by_reason);
  g_ptr_array_add (self->outputs, local_data->first_vaccination_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->first_vaccination_by_reason_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->num_units_vaccinated);
  g_ptr_array_add (self->outputs, local_data->num_units_vaccinated_by_reason);
  g_ptr_array_add (self->outputs, local_data->num_units_vaccinated_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->num_units_vaccinated_by_reason_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_num_units_vaccinated);
  g_ptr_array_add (self->outputs, local_data->cumul_num_units_vaccinated_by_reason);
  g_ptr_array_add (self->outputs, local_data->cumul_num_units_vaccinated_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_num_units_vaccinated_by_reason_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->num_animals_vaccinated);
  g_ptr_array_add (self->outputs, local_data->num_animals_vaccinated_by_reason);
  g_ptr_array_add (self->outputs, local_data->num_animals_vaccinated_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->num_animals_vaccinated_by_reason_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_num_animals_vaccinated);
  g_ptr_array_add (self->outputs, local_data->cumul_num_animals_vaccinated_by_reason);
  g_ptr_array_add (self->outputs, local_data->cumul_num_animals_vaccinated_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_num_animals_vaccinated_by_reason_and_prodtype);

  /* Set the reporting frequency for the output variables. */

  /* Initialize the output variables we already know about. */
  local_data->production_types = units->production_type_names;
  n = local_data->production_types->len;
  drill_down_list[0] = "Ini";
  RPT_reporting_add_integer1 (local_data->num_units_vaccinated_by_reason, 0, drill_down_list[0]);
  RPT_reporting_add_integer1 (local_data->cumul_num_units_vaccinated_by_reason, 0, drill_down_list[0]);
  RPT_reporting_add_integer1 (local_data->num_animals_vaccinated_by_reason, 0, drill_down_list[0]);
  RPT_reporting_add_integer1 (local_data->cumul_num_animals_vaccinated_by_reason, 0, drill_down_list[0]);
  for (i = 0; i < n; i++)
    {
      prodtype_name = (char *) g_ptr_array_index (local_data->production_types, i);
      RPT_reporting_add_integer1 (local_data->first_vaccination_by_prodtype, 0, prodtype_name);
      RPT_reporting_add_integer1 (local_data->num_units_vaccinated_by_prodtype, 0, prodtype_name);
      RPT_reporting_add_integer1 (local_data->cumul_num_units_vaccinated_by_prodtype, 0, prodtype_name);
      RPT_reporting_add_integer1 (local_data->num_animals_vaccinated_by_prodtype, 0, prodtype_name);
      RPT_reporting_add_integer1 (local_data->cumul_num_animals_vaccinated_by_prodtype, 0, prodtype_name);
      drill_down_list[1] = prodtype_name;
      RPT_reporting_add_integer (local_data->num_units_vaccinated_by_reason_and_prodtype, 0, drill_down_list);
      RPT_reporting_add_integer (local_data->cumul_num_units_vaccinated_by_reason_and_prodtype, 0, drill_down_list);
      RPT_reporting_add_integer (local_data->num_animals_vaccinated_by_reason_and_prodtype, 0, drill_down_list);
      RPT_reporting_add_integer (local_data->cumul_num_animals_vaccinated_by_reason_and_prodtype, 0, drill_down_list);
    }

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file vaccination_monitor.c */
