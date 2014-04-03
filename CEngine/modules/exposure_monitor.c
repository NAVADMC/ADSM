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
#  include <config.h>
#endif

/* To avoid name clashes when multiple modules have the same interface. */
#define new exposure_monitor_new
#define run exposure_monitor_run
#define reset exposure_monitor_reset
#define events_listened_for exposure_monitor_events_listened_for
#define local_free exposure_monitor_free
#define handle_before_any_simulations_event exposure_monitor_handle_before_any_simulations_event
#define handle_new_day_event exposure_monitor_handle_new_day_event
#define handle_exposure_event exposure_monitor_handle_exposure_event

#include "module.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#include "exposure_monitor.h"

#include "spreadmodel.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "exposure-monitor"



#define NEVENTS_LISTENED_FOR 3
EVT_event_type_t events_listened_for[] = { EVT_BeforeAnySimulations, EVT_NewDay, EVT_Exposure };



/** Specialized information for this model. */
typedef struct
{
  GPtrArray *production_types;
  RPT_reporting_t *num_units_exposed;
  RPT_reporting_t *num_units_exposed_by_cause;
  RPT_reporting_t *num_units_exposed_by_prodtype;
  RPT_reporting_t *num_units_exposed_by_cause_and_prodtype;
  RPT_reporting_t *cumul_num_units_exposed;
  RPT_reporting_t *cumul_num_units_exposed_by_cause;
  RPT_reporting_t *cumul_num_units_exposed_by_prodtype;
  RPT_reporting_t *cumul_num_units_exposed_by_cause_and_prodtype;
  RPT_reporting_t *num_animals_exposed;
  RPT_reporting_t *num_animals_exposed_by_cause;
  RPT_reporting_t *num_animals_exposed_by_prodtype;
  RPT_reporting_t *num_animals_exposed_by_cause_and_prodtype;
  RPT_reporting_t *cumul_num_animals_exposed;
  RPT_reporting_t *cumul_num_animals_exposed_by_cause;
  RPT_reporting_t *cumul_num_animals_exposed_by_prodtype;
  RPT_reporting_t *cumul_num_animals_exposed_by_cause_and_prodtype;
  RPT_reporting_t *num_adequate_exposures;
  RPT_reporting_t *cumul_num_adequate_exposures;
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
 * On each new day, zero the daily counts of exposures.
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
  RPT_reporting_zero (local_data->num_units_exposed);
  RPT_reporting_zero (local_data->num_units_exposed_by_cause);
  RPT_reporting_zero (local_data->num_units_exposed_by_prodtype);
  RPT_reporting_zero (local_data->num_units_exposed_by_cause_and_prodtype);
  RPT_reporting_zero (local_data->num_animals_exposed);
  RPT_reporting_zero (local_data->num_animals_exposed_by_cause);
  RPT_reporting_zero (local_data->num_animals_exposed_by_prodtype);
  RPT_reporting_zero (local_data->num_animals_exposed_by_cause_and_prodtype);
  RPT_reporting_zero (local_data->num_adequate_exposures);

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
handle_exposure_event (struct spreadmodel_model_t_ *self, EVT_exposure_event_t * event)
{
  local_data_t *local_data;
  UNT_unit_t *exposing_unit, *exposed_unit;
  const char *cause;
  const char *drill_down_list[3] = { NULL, NULL, NULL };
  UNT_expose_t update;
  
#if DEBUG
  g_debug ("----- ENTER handle_exposure_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  exposing_unit = event->exposing_unit;
  exposed_unit = event->exposed_unit;

  cause = SPREADMODEL_contact_type_abbrev[event->contact_type];
                                
  update.src_index = exposing_unit->index;
  update.src_state = (SPREADMODEL_disease_state) exposing_unit->state;
  update.dest_index = exposed_unit->index;
  update.dest_state = (SPREADMODEL_disease_state) exposed_unit->state;
  
  update.initiated_day = (int) event->initiated_day;
  update.finalized_day = (int) event->initiated_day + event->delay;
  
  if( TRUE == event->adequate )
    update.is_adequate = SPREADMODEL_SuccessTrue;
  else
    update.is_adequate = SPREADMODEL_SuccessFalse;
  
  switch (event->contact_type)
    {
      case SPREADMODEL_DirectContact:
      case SPREADMODEL_IndirectContact:
      case SPREADMODEL_AirborneSpread:
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
  if (NULL != spreadmodel_expose_unit)
    {
      spreadmodel_expose_unit (update);
    }
#endif  

#if UNDEFINED
  printf ("unit at index %d exposed by method %s\n", event->exposed_unit->index, cause);
#endif

  /* Update the counts of exposures. */
  RPT_reporting_add_integer  (local_data->num_units_exposed, 1, NULL);
  RPT_reporting_add_integer1 (local_data->num_units_exposed_by_cause, 1, cause);
  RPT_reporting_add_integer1 (local_data->num_units_exposed_by_prodtype, 1, exposed_unit->production_type_name);
  RPT_reporting_add_integer  (local_data->num_animals_exposed, exposed_unit->size, NULL);
  RPT_reporting_add_integer1 (local_data->num_animals_exposed_by_cause, exposed_unit->size, cause);
  RPT_reporting_add_integer1 (local_data->num_animals_exposed_by_prodtype, exposed_unit->size, exposed_unit->production_type_name);
  RPT_reporting_add_integer  (local_data->cumul_num_units_exposed, 1, NULL);
  RPT_reporting_add_integer1 (local_data->cumul_num_units_exposed_by_cause, 1, cause);
  RPT_reporting_add_integer1 (local_data->cumul_num_units_exposed_by_prodtype, 1, exposed_unit->production_type_name);
  RPT_reporting_add_integer  (local_data->cumul_num_animals_exposed, exposed_unit->size, NULL);
  RPT_reporting_add_integer1 (local_data->cumul_num_animals_exposed_by_cause, exposed_unit->size,
                              cause);
  RPT_reporting_add_integer1 (local_data->cumul_num_animals_exposed_by_prodtype, exposed_unit->size,
                              exposed_unit->production_type_name);
  drill_down_list[0] = cause;
  drill_down_list[1] = exposed_unit->production_type_name;
  if (local_data->num_units_exposed_by_cause_and_prodtype->frequency != RPT_never)
    RPT_reporting_add_integer (local_data->num_units_exposed_by_cause_and_prodtype, 1, drill_down_list);
  if (local_data->num_animals_exposed_by_cause_and_prodtype->frequency != RPT_never)
    RPT_reporting_add_integer (local_data->num_animals_exposed_by_cause_and_prodtype, exposed_unit->size,
                               drill_down_list);
  if (local_data->cumul_num_units_exposed_by_cause_and_prodtype->frequency != RPT_never)
    RPT_reporting_add_integer (local_data->cumul_num_units_exposed_by_cause_and_prodtype, 1, drill_down_list);
  if (local_data->cumul_num_animals_exposed_by_cause_and_prodtype->frequency != RPT_never)
    RPT_reporting_add_integer (local_data->cumul_num_animals_exposed_by_cause_and_prodtype,
                               exposed_unit->size, drill_down_list);
  if (event->adequate)
    {
      RPT_reporting_add_integer (local_data->num_adequate_exposures, 1, NULL);
      RPT_reporting_add_integer (local_data->cumul_num_adequate_exposures, 1, NULL);
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
  RPT_reporting_zero (local_data->cumul_num_units_exposed);
  RPT_reporting_zero (local_data->cumul_num_units_exposed_by_cause);
  RPT_reporting_zero (local_data->cumul_num_units_exposed_by_prodtype);
  RPT_reporting_zero (local_data->cumul_num_units_exposed_by_cause_and_prodtype);
  RPT_reporting_zero (local_data->cumul_num_animals_exposed);
  RPT_reporting_zero (local_data->cumul_num_animals_exposed_by_cause);
  RPT_reporting_zero (local_data->cumul_num_animals_exposed_by_prodtype);
  RPT_reporting_zero (local_data->cumul_num_animals_exposed_by_cause_and_prodtype);
  RPT_reporting_zero (local_data->cumul_num_adequate_exposures);

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

#if DEBUG
  g_debug ("----- ENTER free (%s)", MODEL_NAME);
#endif

  /* Free the dynamically-allocated parts. */
  local_data = (local_data_t *) (self->model_data);
  RPT_free_reporting (local_data->num_units_exposed);
  RPT_free_reporting (local_data->num_units_exposed_by_cause);
  RPT_free_reporting (local_data->num_units_exposed_by_prodtype);
  RPT_free_reporting (local_data->num_units_exposed_by_cause_and_prodtype);
  RPT_free_reporting (local_data->cumul_num_units_exposed);
  RPT_free_reporting (local_data->cumul_num_units_exposed_by_cause);
  RPT_free_reporting (local_data->cumul_num_units_exposed_by_prodtype);
  RPT_free_reporting (local_data->cumul_num_units_exposed_by_cause_and_prodtype);
  RPT_free_reporting (local_data->num_animals_exposed);
  RPT_free_reporting (local_data->num_animals_exposed_by_cause);
  RPT_free_reporting (local_data->num_animals_exposed_by_prodtype);
  RPT_free_reporting (local_data->num_animals_exposed_by_cause_and_prodtype);
  RPT_free_reporting (local_data->cumul_num_animals_exposed);
  RPT_free_reporting (local_data->cumul_num_animals_exposed_by_cause);
  RPT_free_reporting (local_data->cumul_num_animals_exposed_by_prodtype);
  RPT_free_reporting (local_data->cumul_num_animals_exposed_by_cause_and_prodtype);
  RPT_free_reporting (local_data->num_adequate_exposures);
  RPT_free_reporting (local_data->cumul_num_adequate_exposures);

  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Returns a new exposure monitor.
 */
spreadmodel_model_t *
new (scew_element * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  spreadmodel_model_t *self;
  local_data_t *local_data;
  scew_element *e;
  scew_list *ee, *iter;
  unsigned int n;
  const XML_Char *variable_name;
  RPT_frequency_t freq;
  gboolean success;
  gboolean broken_down;
  unsigned int i, j;      /* loop counters */
  char *prodtype_name;

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
  self->set_params = NULL;
  self->run = run;
  self->reset = reset;
  self->is_listening_for = spreadmodel_model_is_listening_for;
  self->has_pending_actions = spreadmodel_model_answer_no;
  self->has_pending_infections = spreadmodel_model_answer_no;
  self->to_string = spreadmodel_model_to_string_default;
  self->printf = spreadmodel_model_printf;
  self->fprintf = spreadmodel_model_fprintf;
  self->free = local_free;

  /* Make sure the right XML subtree was sent. */
  g_assert (strcmp (scew_element_name (params), MODEL_NAME) == 0);

  local_data->num_units_exposed =
    RPT_new_reporting ("expnUAll", RPT_integer, RPT_never);
  local_data->num_units_exposed_by_cause =
    RPT_new_reporting ("expnU", RPT_group, RPT_never);
  local_data->num_units_exposed_by_prodtype =
    RPT_new_reporting ("expnU", RPT_group, RPT_never);
  local_data->num_units_exposed_by_cause_and_prodtype =
    RPT_new_reporting ("expnU", RPT_group, RPT_never);
  local_data->cumul_num_units_exposed =
    RPT_new_reporting ("expcUAll", RPT_integer, RPT_never);
  local_data->cumul_num_units_exposed_by_cause =
    RPT_new_reporting ("expcU", RPT_group, RPT_never);
  local_data->cumul_num_units_exposed_by_prodtype =
    RPT_new_reporting ("expcU", RPT_group, RPT_never);
  local_data->cumul_num_units_exposed_by_cause_and_prodtype =
    RPT_new_reporting ("expcU", RPT_group, RPT_never);
  local_data->num_animals_exposed =
    RPT_new_reporting ("expnAAll", RPT_integer, RPT_never);
  local_data->num_animals_exposed_by_cause =
    RPT_new_reporting ("expnA", RPT_group, RPT_never);
  local_data->num_animals_exposed_by_prodtype =
    RPT_new_reporting ("expnA", RPT_group, RPT_never);
  local_data->num_animals_exposed_by_cause_and_prodtype =
    RPT_new_reporting ("expnA", RPT_group, RPT_never);
  local_data->cumul_num_animals_exposed =
    RPT_new_reporting ("expcAAll", RPT_integer, RPT_never);
  local_data->cumul_num_animals_exposed_by_cause =
    RPT_new_reporting ("expcA", RPT_group, RPT_never);
  local_data->cumul_num_animals_exposed_by_prodtype =
    RPT_new_reporting ("expcA", RPT_group, RPT_never);
  local_data->cumul_num_animals_exposed_by_cause_and_prodtype =
    RPT_new_reporting ("expcA", RPT_group, RPT_never);
  local_data->num_adequate_exposures =
    RPT_new_reporting ("adqnUAll", RPT_integer, RPT_never);
  local_data->cumul_num_adequate_exposures =
    RPT_new_reporting ("adqcUAll", RPT_integer, RPT_never);
  g_ptr_array_add (self->outputs, local_data->num_units_exposed);
  g_ptr_array_add (self->outputs, local_data->num_units_exposed_by_cause);
  g_ptr_array_add (self->outputs, local_data->num_units_exposed_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->num_units_exposed_by_cause_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_num_units_exposed);
  g_ptr_array_add (self->outputs, local_data->cumul_num_units_exposed_by_cause);
  g_ptr_array_add (self->outputs, local_data->cumul_num_units_exposed_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_num_units_exposed_by_cause_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->num_animals_exposed);
  g_ptr_array_add (self->outputs, local_data->num_animals_exposed_by_cause);
  g_ptr_array_add (self->outputs, local_data->num_animals_exposed_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->num_animals_exposed_by_cause_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_num_animals_exposed);
  g_ptr_array_add (self->outputs, local_data->cumul_num_animals_exposed_by_cause);
  g_ptr_array_add (self->outputs, local_data->cumul_num_animals_exposed_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_num_animals_exposed_by_cause_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->num_adequate_exposures);
  g_ptr_array_add (self->outputs, local_data->cumul_num_adequate_exposures);

  /* Set the reporting frequency for the output variables. */
  ee = scew_element_list_by_name (params, "output");
#if DEBUG
  g_debug ("%u output variables", scew_list_size(ee));
#endif
  for (iter = ee; iter != NULL; iter = scew_list_next(iter))
    {
      e = (scew_element *) scew_list_data (iter);
      variable_name = scew_element_contents (scew_element_by_name (e, "variable-name"));
      freq = RPT_string_to_frequency (scew_element_contents
                                      (scew_element_by_name (e, "frequency")));
      broken_down = PAR_get_boolean (scew_element_by_name (e, "broken-down"), &success);
      if (!success)
      	broken_down = FALSE;
      broken_down = broken_down || (g_strstr_len (variable_name, -1, "-by-") != NULL); 
      /* Starting at version 3.2 we accept either the old, verbose output
       * variable names or the new shorter ones. */
      if (strcmp (variable_name, "expnU") == 0
          || strncmp (variable_name, "num-units-exposed", 17) == 0)
        {
          RPT_reporting_set_frequency (local_data->num_units_exposed, freq);
          if (broken_down)
            {
              RPT_reporting_set_frequency (local_data->num_units_exposed_by_cause, freq);
              RPT_reporting_set_frequency (local_data->num_units_exposed_by_prodtype, freq);
              RPT_reporting_set_frequency (local_data->num_units_exposed_by_cause_and_prodtype, freq);
            }
        }
      else if (strcmp (variable_name, "expcU") == 0
               || strncmp (variable_name, "cumulative-num-units-exposed", 28) == 0)
        {
          RPT_reporting_set_frequency (local_data->cumul_num_units_exposed, freq);
          if (broken_down)
            {
              RPT_reporting_set_frequency (local_data->cumul_num_units_exposed_by_cause, freq);
              RPT_reporting_set_frequency (local_data->cumul_num_units_exposed_by_prodtype, freq);
              RPT_reporting_set_frequency (local_data->cumul_num_units_exposed_by_cause_and_prodtype, freq);
            }
        }
      else if (strcmp (variable_name, "expnA") == 0
               || strncmp (variable_name, "num-animals-exposed", 19) == 0)
        {
          RPT_reporting_set_frequency (local_data->num_animals_exposed, freq);
          if (broken_down)
            {
              RPT_reporting_set_frequency (local_data->num_animals_exposed_by_cause, freq);
              RPT_reporting_set_frequency (local_data->num_animals_exposed_by_prodtype, freq);
              RPT_reporting_set_frequency (local_data->num_animals_exposed_by_cause_and_prodtype, freq);
            }
        }
      else if (strcmp (variable_name, "expcA") == 0
               || strncmp (variable_name, "cumulative-num-animals-exposed", 30) == 0)
        {
          RPT_reporting_set_frequency (local_data->cumul_num_animals_exposed, freq);
          if (broken_down)
            {
              RPT_reporting_set_frequency (local_data->cumul_num_animals_exposed_by_cause, freq);
              RPT_reporting_set_frequency (local_data->cumul_num_animals_exposed_by_prodtype, freq);
              RPT_reporting_set_frequency (local_data->cumul_num_animals_exposed_by_cause_and_prodtype, freq);
            }
        }
      else if (strcmp (variable_name, "adqnU") == 0)
        {
          RPT_reporting_set_frequency (local_data->num_adequate_exposures, freq);
        }
      else if (strcmp (variable_name, "adqcU") == 0)
        {
          RPT_reporting_set_frequency (local_data->cumul_num_adequate_exposures, freq);
        }
      else
        g_warning ("no output variable named \"%s\", ignoring", variable_name);        
    }
  scew_list_free (ee);

  /* Initialize the output variables. */
  local_data->production_types = units->production_type_names;
  n = local_data->production_types->len;
  for (i = 0; i < n; i++)
    {
      prodtype_name = (char *) g_ptr_array_index (local_data->production_types, i);
      RPT_reporting_add_integer1 (local_data->num_units_exposed_by_prodtype, 0, prodtype_name);
      RPT_reporting_add_integer1 (local_data->cumul_num_units_exposed_by_prodtype, 0, prodtype_name);
      RPT_reporting_add_integer1 (local_data->num_animals_exposed_by_prodtype, 0, prodtype_name);
      RPT_reporting_add_integer1 (local_data->cumul_num_animals_exposed_by_prodtype, 0, prodtype_name);
    }
  for (i = 0; i < SPREADMODEL_NCONTACT_TYPES; i++)
    {
      const char *cause;
      const char *drill_down_list[3] = { NULL, NULL, NULL };
      if ((SPREADMODEL_contact_type)i == SPREADMODEL_UnspecifiedInfectionType
          || (SPREADMODEL_contact_type)i == SPREADMODEL_InitiallyInfected)
        continue;
      cause = SPREADMODEL_contact_type_abbrev[i];
      RPT_reporting_add_integer1 (local_data->num_units_exposed_by_cause, 0, cause);
      RPT_reporting_add_integer1 (local_data->cumul_num_units_exposed_by_cause, 0, cause);
      RPT_reporting_add_integer1 (local_data->num_animals_exposed_by_cause, 0, cause);
      RPT_reporting_add_integer1 (local_data->cumul_num_animals_exposed_by_cause, 0, cause);
      drill_down_list[0] = cause;
      for (j = 0; j < n; j++)
        {
          drill_down_list[1] = (char *) g_ptr_array_index (local_data->production_types, j);
          RPT_reporting_add_integer (local_data->num_units_exposed_by_cause_and_prodtype, 0, drill_down_list);
          RPT_reporting_add_integer (local_data->cumul_num_units_exposed_by_cause_and_prodtype, 0,
                                     drill_down_list);
          RPT_reporting_add_integer (local_data->num_animals_exposed_by_cause_and_prodtype, 0,
                                     drill_down_list);
          RPT_reporting_add_integer (local_data->cumul_num_animals_exposed_by_cause_and_prodtype, 0,
                                     drill_down_list);
        }
    }

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file exposure_monitor.c */
