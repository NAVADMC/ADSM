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
#  include "config.h"
#endif

/* To avoid name clashes when multiple modules have the same interface. */
#define new vaccine_model_new
#define run vaccine_model_run
#define to_string vaccine_model_to_string
#define local_free vaccine_model_free
#define handle_before_any_simulations_event vaccine_model_handle_before_any_simulations_event
#define handle_vaccination_event vaccine_model_handle_vaccination_event

#include "module.h"
#include "module_util.h"
#include "sqlite3_exec_dict.h"

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



#define EPSILON 0.01



/* Specialized information for this model. */
typedef struct
{
  double delay;
  PDF_dist_t *immunity_period;
}
param_block_t;



typedef struct
{
  GPtrArray *production_types;
  param_block_t **param_block; /**< Blocks of parameters.  Use an expression
    of the form param_block[production_type] to get a pointer to a particular
    param_block. */
  sqlite3 *db; /* Temporarily stash a pointer to the parameters database here
    so that it will be available to the set_params function. */
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
handle_before_any_simulations_event (struct adsm_module_t_ * self,
                                     EVT_event_queue_t * queue)
{
  local_data_t *local_data;
  unsigned int nprod_types, i;
  param_block_t *param_block;
  char * production_type_name;
  
#if DEBUG
  g_debug ("----- ENTER handle_before_any_simulations_event (%s)", MODEL_NAME);
#endif
    
  local_data = (local_data_t *) (self->model_data);
  nprod_types = local_data->production_types->len;
  for (i = 0; i < nprod_types; i++)
    {
      param_block = local_data->param_block[i];

      if (param_block != NULL)
        {
          production_type_name = (char *) g_ptr_array_index (local_data->production_types, i);
          EVT_event_enqueue (queue,
                             EVT_new_declaration_of_vaccine_delay_event (i,
                                                                         production_type_name,
                                                                         param_block->delay));
        }
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
handle_vaccination_event (struct adsm_module_t_ *self,
                          EVT_vaccination_event_t * event, RAN_gen_t * rng)
{
  local_data_t *local_data;
  param_block_t *param_block;
  int delay, immunity_period;
  
#if DEBUG
  g_debug ("----- ENTER handle_vaccination_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  param_block = local_data->param_block[event->unit->production_type];
  if (param_block != NULL)
    {
      #if DEBUG
        g_debug ("override initial state = (%i)", event->override_initial_state);
      #endif

      if (event->override_initial_state == VaccineImmune)
        delay = 0;
      else
        delay = param_block->delay;
      #if DEBUG
        g_debug ("vaccine will take %hu days to take effect", delay);
      #endif

      if (event->override_initial_state == VaccineImmune && event->override_days_left_in_state > 0)
        immunity_period = event->override_days_left_in_state;
      else
        {
          immunity_period = (int) round (PDF_random (param_block->immunity_period, rng));
          if (immunity_period < 0)
            {
              #if DEBUG
                g_debug ("%s distribution returned %i for immunity period, using 0 instead",
                         PDF_dist_type_name[param_block->immunity_period->type], immunity_period);
              #endif
              immunity_period = 0;
            }
        }
      #if DEBUG
        g_debug ("vaccine immunity will last %hu days", immunity_period);
      #endif

      UNT_vaccinate (event->unit, delay, immunity_period);
  }

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
run (struct adsm_module_t_ *self, UNT_unit_list_t * units, ZON_zone_list_t * zones,
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
    case EVT_Vaccination:
      handle_vaccination_event (self, &(event->u.vaccination), rng);
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
  GString *s;
  local_data_t *local_data;
  unsigned int nprod_types, i;
  param_block_t *param_block;
  char *substring, *chararray;

  local_data = (local_data_t *) (self->model_data);
  s = g_string_new (NULL);
  g_string_printf (s, "<%s", MODEL_NAME);

  /* Add the parameter block for each production type. */
  nprod_types = local_data->production_types->len;
  for (i = 0; i < nprod_types; i++)
    {
      param_block = local_data->param_block[i];
      if (param_block == NULL)
        continue;

      g_string_append_printf (s, "\n  for %s",
                              (char *) g_ptr_array_index (local_data->production_types, i));

      g_string_append_printf (s, "\n    delay=%g", param_block->delay);

      substring = PDF_dist_to_string (param_block->immunity_period);
      g_string_append_printf (s, "\n    immunity-period=%s", substring);
      g_free (substring);
    }
  g_string_append_c (s, '>');

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
local_free (struct adsm_module_t_ *self)
{
  local_data_t *local_data;
  unsigned int nprod_types, i;
  param_block_t *param_block;

#if DEBUG
  g_debug ("----- ENTER free (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* Free each of the parameter blocks. */
  nprod_types = local_data->production_types->len;
  for (i = 0; i < nprod_types; i++)
    {
      param_block = local_data->param_block[i];
      if (param_block != NULL)
        {
          PDF_free_dist (param_block->immunity_period);
          g_free (param_block);
        }
    }
  g_free (local_data->param_block);

  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Adds a set of parameters to a vaccine model.
 *
 * @param data this module ("self"), but cast to a void *.
 * @param dict the SQL query result as a GHashTable in which key = colname,
 *   value = value, both in (char *) format.
 * @return 0
 */
static int
set_params (void *data, GHashTable *dict)
{
  adsm_module_t *self;
  local_data_t *local_data;
  sqlite3 *params;
  guint production_type_id;
  param_block_t *p;
  guint pdf_id;

  #if DEBUG
    g_debug ("----- ENTER set_params (%s)", MODEL_NAME);
  #endif

  g_assert (g_hash_table_size (dict) == 3);

  self = (adsm_module_t *)data;
  local_data = (local_data_t *) (self->model_data);
  params = local_data->db;

  /* Find out which production types these parameters apply to. */
  production_type_id =
    adsm_read_prodtype (g_hash_table_lookup (dict, "prodtype"),
                        local_data->production_types);

  /* Check that we are not overwriting an existing parameter block (that would
   * indicate a bug). */
  g_assert (local_data->param_block[production_type_id] == NULL);

  /* Create a new parameter block. */
  p = g_new (param_block_t, 1);
  local_data->param_block[production_type_id] = p;

  /* Read the parameters. */
  errno = 0;
  p->delay = strtod (g_hash_table_lookup (dict, "days_to_immunity"), NULL);
  g_assert (errno != ERANGE);
  /* The delay cannot be negative. */
  if (p->delay < 0)
    {
      g_warning ("vaccine model delay parameter cannot be negative, setting to 0 days");
      p->delay = 0;
    }

  errno = 0;
  pdf_id = strtol (g_hash_table_lookup (dict, "vaccine_immune_period_id"), NULL, /* base */ 10);
  g_assert (errno != ERANGE && errno != EINVAL);  
  p->immunity_period = PAR_get_PDF (params, pdf_id);
  /* No part of the immunity period distribution should be negative. */
  if (p->immunity_period->has_inf_lower_tail == FALSE
      && PDF_cdf (-EPSILON, p->immunity_period) > 0)
    {
      g_warning
        ("vaccine model immunity period distribution should not include negative values");
    }

  #if DEBUG
    g_debug ("----- EXIT set_params (%s)", MODEL_NAME);
  #endif

  return 0;
}



/**
 * Returns a new vaccine model.
 */
adsm_module_t *
new (sqlite3 * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones, GError **error)
{
  adsm_module_t *self;
  local_data_t *local_data;
  EVT_event_type_t events_listened_for[] = {
    EVT_BeforeAnySimulations,
    EVT_Vaccination,
    0
  };
  guint nprod_types;
  char *sqlerr;

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
  self->to_string = to_string;
  self->printf = adsm_model_printf;
  self->fprintf = adsm_model_fprintf;
  self->free = local_free;

  /* local_data->param_block holds an array of parameter blocks, where each
   * block holds the parameters for one production type.  Initially, all
   * pointers are NULL.  Blocks will be created as needed in the set_params
   * function. */
  local_data->production_types = units->production_type_names;
  nprod_types = local_data->production_types->len;
  local_data->param_block = g_new0 (param_block_t *, nprod_types);

  /* Call the set_params function to read the production type specific
   * parameters. */
  local_data->db = params;
  sqlite3_exec_dict (params,
                     "SELECT prodtype.name AS prodtype,days_to_immunity,vaccine_immune_period_id "
                     "FROM ScenarioCreator_productiontype prodtype,ScenarioCreator_controlprotocol vaccine,ScenarioCreator_protocolassignment xref "
                     "WHERE prodtype.id=xref.production_type_id "
                     "AND xref.control_protocol_id=vaccine.id "
                     "AND vaccine_immune_period_id IS NOT NULL",
                     set_params, self, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }
  local_data->db = NULL;

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file vaccine_model.c */
