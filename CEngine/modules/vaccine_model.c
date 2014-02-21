/** @file vaccine_model.c
 * Module that encapsulates knowledge about a vaccine.  Specifically,
 * <ul>
 *   <li> how long the vaccine requires to produce immunity
 *   <li> how long the unit remains immune
 * </ul>
 *
 * When this module hears a Vaccination event, it decides how long the vaccine
 * will require to take effect and how long the unit will remain immune by
 * sampling from the distributions given as parameters.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @version 0.1
 * @date May 2003
 *
 * Copyright &copy; University of Guelph, 2003-2008
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
#define new vaccine_model_new
#define run vaccine_model_run
#define reset vaccine_model_reset
#define events_listened_for vaccine_model_events_listened_for
#define to_string vaccine_model_to_string
#define local_free vaccine_model_free
#define handle_before_any_simulations_event vaccine_model_handle_before_any_simulations_event
#define handle_vaccination_event vaccine_model_handle_vaccination_event

#include "module.h"
#include "module_util.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#if HAVE_MATH_H
#  include <math.h>
#endif

#if HAVE_STRINGS_H
#  include <strings.h>
#endif

#include "vaccine_model.h"

#if !HAVE_ROUND && HAVE_RINT
#  define round rint
#endif

/* Temporary fix -- "round" and "rint" are in the math library on Red Hat 7.3,
 * but they're #defined so AC_CHECK_FUNCS doesn't find them. */
double round (double x);

/** This must match an element name in the DTD. */
#define MODEL_NAME "vaccine-model"



#define NEVENTS_LISTENED_FOR 2
EVT_event_type_t events_listened_for[] = { EVT_BeforeAnySimulations,
  EVT_Vaccination };



#define EPSILON 0.01



/* Specialized information for this model. */
typedef struct
{
  gboolean *production_type;
  GPtrArray *production_types;
  double delay;
  PDF_dist_t *immunity_period;
}
local_data_t;



/**
 * Before any simulations, this module declares the number of days between
 * between being vaccinated and becoming immune.  One instance of this module
 * may handle several production types, so one response is issued for each
 * production type that the instance handles.
 *
 * @param self this module.
 * @param queue for any new events the module creates.
 */
void
handle_before_any_simulations_event (struct spreadmodel_model_t_ * self,
                                     EVT_event_queue_t * queue)
{
  local_data_t *local_data;
  unsigned int i;
  char * production_type_name;
  
#if DEBUG
  g_debug ("----- ENTER handle_before_any_simulations_event (%s)", MODEL_NAME);
#endif
    
  local_data = (local_data_t *) (self->model_data);
  for (i = 0; i < local_data->production_types->len; i++)
    if (local_data->production_type[i] == TRUE)
      {
        production_type_name = (char *) g_ptr_array_index (local_data->production_types, i);
        EVT_event_enqueue (queue,
                           EVT_new_declaration_of_vaccine_delay_event (i,
                                                                       production_type_name,
                                                                       local_data->delay));
      }

#if DEBUG
  g_debug ("----- EXIT handle_before_any_simulations_event (%s)", MODEL_NAME);
#endif
  return;
}



/**
 * Responds to an vaccination event by changing the unit's state from
 * susceptible to vaccine immune.
 *
 * @param self the model.
 * @param event a vaccination event.
 * @param rng a random number generator.
 */
void
handle_vaccination_event (struct spreadmodel_model_t_ *self,
                          EVT_vaccination_event_t * event, RAN_gen_t * rng)
{
  local_data_t *local_data;
  int delay, immunity_period;
  
#if DEBUG
  g_debug ("----- ENTER handle_vaccination_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  #if DEBUG
    g_debug ("override initial state = (%i)", event->override_initial_state);
  #endif

  if (event->override_initial_state == VaccineImmune)
    delay = 0;
  else
    delay = local_data->delay;
  #if DEBUG
    g_debug ("vaccine will take %hu days to take effect", delay);
  #endif

  if (event->override_initial_state == VaccineImmune && event->override_days_left_in_state > 0)
    immunity_period = event->override_days_left_in_state;
  else
    {
      immunity_period = (int) round (PDF_random (local_data->immunity_period, rng));
      if (immunity_period < 0)
        {
          #if DEBUG
            g_debug ("%s distribution returned %i for immunity period, using 0 instead",
                     PDF_dist_type_name[local_data->immunity_period->type], immunity_period);
          #endif
          immunity_period = 0;
        }
    }
  #if DEBUG
    g_debug ("vaccine immunity will last %hu days", immunity_period);
  #endif

  UNT_vaccinate (event->unit, delay, immunity_period);

#if DEBUG
  g_debug ("----- EXIT handle_vaccination_event (%s)", MODEL_NAME);
#endif
}



/**
 * Runs this model.
 *
 * Side effects: may change the state of one or more units in list.
 *
 * @param self the model.
 * @param units a list of units.
 * @param zones a list of zones.
 * @param event the event that caused the model to run.
 * @param rng a random number generator.
 * @param queue for any new events the model creates.
 */
void
run (struct spreadmodel_model_t_ *self, UNT_unit_list_t * units, ZON_zone_list_t * zones,
     EVT_event_t * event, RAN_gen_t * rng, EVT_event_queue_t * queue)
{
  local_data_t *local_data;
  EVT_vaccination_event_t *vaccination_event;

#if DEBUG
  g_debug ("----- ENTER run (%s)", MODEL_NAME);
#endif

  switch (event->type)
    {
    case EVT_BeforeAnySimulations:
      handle_before_any_simulations_event (self, queue);
      break;
    case EVT_Vaccination:
      local_data = (local_data_t *) (self->model_data);
      vaccination_event = &(event->u.vaccination);
      if (local_data->production_type[vaccination_event->unit->production_type] == TRUE)
        {
          handle_vaccination_event (self, vaccination_event, rng);
        }
      else
        {
          #if DEBUG
            g_debug ("unit is %s, sub-model does not apply",
                     vaccination_event->unit->production_type_name);
          #endif
          ;
        }
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
#if DEBUG
  g_debug ("----- ENTER reset (%s)", MODEL_NAME);
#endif

  /* Nothing to do. */

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
  GString *s;
  gboolean already_names;
  unsigned int i;
  char *substring, *chararray;
  local_data_t *local_data;

  local_data = (local_data_t *) (self->model_data);
  s = g_string_new (NULL);
  g_string_sprintf (s, "<%s for ", MODEL_NAME);
  already_names = FALSE;
  for (i = 0; i < local_data->production_types->len; i++)
    if (local_data->production_type[i] == TRUE)
      {
        if (already_names)
          g_string_append_printf (s, ",%s",
                                  (char *) g_ptr_array_index (local_data->production_types, i));
        else
          {
            g_string_append_printf (s, "%s",
                                    (char *) g_ptr_array_index (local_data->production_types, i));
            already_names = TRUE;
          }
      }

  g_string_sprintfa (s, "\n  delay=%g\n", local_data->delay);

  substring = PDF_dist_to_string (local_data->immunity_period);
  g_string_sprintfa (s, "  immunity-period=%s>\n", substring);
  g_free (substring);

  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Frees this model.  Does not free the production type names.
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
  g_free (local_data->production_type);
  PDF_free_dist (local_data->immunity_period);
  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Returns a new vaccine model.
 */
spreadmodel_model_t *
new (scew_element * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  spreadmodel_model_t *self;
  local_data_t *local_data;
  scew_element *e;
  gboolean success;

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
  self->to_string = to_string;
  self->printf = spreadmodel_model_printf;
  self->fprintf = spreadmodel_model_fprintf;
  self->free = local_free;

  /* Make sure the right XML subtree was sent. */
  g_assert (strcmp (scew_element_name (params), MODEL_NAME) == 0);

  #if DEBUG
    g_debug ("setting production types");
  #endif
  local_data->production_types = units->production_type_names;
  local_data->production_type =
    spreadmodel_read_prodtype_attribute (params, "production-type", units->production_type_names);

  e = scew_element_by_name (params, "delay");
  if (e != NULL)
    {
      local_data->delay = PAR_get_time (e, &success);
      if (success == FALSE)
        {
          g_warning ("setting vaccine model delay parameter to 0 days");
          local_data->delay = 0;
        }
      /* The delay cannot be negative. */
      if (local_data->delay < 0)
        {
          g_warning ("vaccine model delay parameter cannot be negative, setting to 0 days");
          local_data->delay = 0;
        }
    }
  else
    {
      g_warning ("vaccine model delay parameter missing, setting to 0 days");
      local_data->delay = 0;
    }

  e = scew_element_by_name (params, "immunity-period");
  if (e != NULL)
    {
      local_data->immunity_period = PAR_get_PDF (e);
      /* No part of the immunity period distribution should be negative. */
      if (local_data->immunity_period->has_inf_lower_tail == FALSE
          && PDF_cdf (-EPSILON, local_data->immunity_period) > 0)
        {
          g_warning
            ("vaccine model immunity period distribution should not include negative values");
        }
    }
  else
    {
      local_data->immunity_period = PDF_new_point_dist (1);
      g_warning ("vaccine model immunity period parameter missing, setting to 1 day");
    }

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file vaccine_model.c */
