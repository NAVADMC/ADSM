/** @file economic_model.c
 * Module that tallies costs of an outbreak.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date June 2003
 *
 * Copyright &copy; University of Guelph, 2003-2006
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 *
 * @todo Add a baseline vaccination capacity and increase in cost past the
 *   baseline.
 */

#if HAVE_CONFIG_H
#  include "config.h"
#endif

/* To avoid name clashes when multiple modules have the same interface. */
#define new economic_model_new
#define run economic_model_run
#define to_string economic_model_to_string
#define local_free economic_model_free
#define handle_before_each_simulation_event economic_model_handle_before_each_simulation_event
#define handle_new_day_event economic_model_handle_new_day_event
#define handle_vaccination_event economic_model_handle_vaccination_event
#define handle_destruction_event economic_model_handle_destruction_event

#include "module.h"
#include "module_util.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#if HAVE_STRINGS_H
#  include <strings.h>
#endif

#include "economic_model.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "economic-model"



/* Parameters for the cost of destruction. */
typedef struct
{
  double appraisal;
  double euthanasia;
  double indemnification;
  double carcass_disposal;
  double cleaning_disinfecting;
}
destruction_cost_data_t;



/* Parameters for the cost of vaccination. */
typedef struct
{
  double vaccination_fixed;
  double vaccination;
  unsigned int baseline_capacity, capacity_used;
  double extra_vaccination;
}
vaccination_cost_data_t;



/* Specialized information for this model. */
typedef struct
{
  GPtrArray *production_types; /**< Each item in the list is a char *. */
  ZON_zone_list_t *zones;

  /* Array [production type] of *destruction_cost_data_t.  If an entry
   * is NULL, no parameters are specified for that production type. */
  destruction_cost_data_t **destruction_cost_params;
  /* Array [production type] of *vaccination_cost_data_t.  If an entry
   * is NULL, no parameters are specified for that production type. */
  vaccination_cost_data_t **vaccination_cost_params;
  /* Array [zone type][production type] of double.  If a row is NULL,
   * no parameters are specified for that zone type.  If the
   * surveillance cost is ever reformulated to have more parameters,
   * create a structure as was done for destruction and vaccination
   * costs. */
  double **surveillance_cost_param;

  /*
  RPT_reporting_t *total_cost;
  RPT_reporting_t *appraisal_cost;
  RPT_reporting_t *euthanasia_cost;
  RPT_reporting_t *indemnification_cost;
  RPT_reporting_t *carcass_disposal_cost;
  RPT_reporting_t *cleaning_disinfecting_cost;
  RPT_reporting_t *vaccination_cost;
  RPT_reporting_t *surveillance_cost;
  */
  RPT_reporting_t *cumul_total_cost;
  RPT_reporting_t *cumul_appraisal_cost;
  RPT_reporting_t *cumul_euthanasia_cost;
  RPT_reporting_t *cumul_indemnification_cost;
  RPT_reporting_t *cumul_carcass_disposal_cost;
  RPT_reporting_t *cumul_cleaning_disinfecting_cost;
  RPT_reporting_t *cumul_destruction_subtotal;
  RPT_reporting_t *cumul_vaccination_setup_cost;
  RPT_reporting_t *cumul_vaccination_cost;
  RPT_reporting_t *cumul_vaccination_subtotal;
  RPT_reporting_t *cumul_surveillance_cost;
}
local_data_t;



/**
 * Before each simulation, this module resets its recorded costs to zero.
 *
 * @param self the model.
 */
void
handle_before_each_simulation_event (struct adsm_module_t_ *self)
{
  local_data_t *local_data = (local_data_t *) (self->model_data);
  unsigned int nprod_types = local_data->production_types->len;
  unsigned int i;

  #if DEBUG
    g_debug ("----- ENTER handle_before_each_simulation_event (%s)", MODEL_NAME);
  #endif

  g_ptr_array_foreach (self->outputs, RPT_reporting_zero_as_GFunc, NULL);

  if (local_data->vaccination_cost_params)
    {
      for (i = 0; i < nprod_types; i++)
        {
          if (local_data->vaccination_cost_params[i])
            {
              local_data->vaccination_cost_params[i]->capacity_used = 0;
            }
        }
    }

  #if DEBUG
    g_debug ("----- EXIT handle_before_each_simulation_event (%s)", MODEL_NAME);
  #endif

  return;
}



/**
 * Responds to a new day event by updating the reporting variables.
 *
 * @param self the model.
 * @param units a list of units.
 * @param zones a list of zones.
 * @param event a new day event.
 */
void
handle_new_day_event (struct adsm_module_t_ *self, UNT_unit_list_t * units,
                      ZON_zone_list_t * zones, EVT_new_day_event_t * event)
{
  local_data_t *local_data = (local_data_t *) (self->model_data);

#if DEBUG
  g_debug ("----- ENTER handle_new_day_event (%s)", MODEL_NAME);
#endif

  /* Zero the daily counts. */
  /*
  RPT_reporting_zero (local_data->total_cost);
  RPT_reporting_zero (local_data->appraisal_cost);
  RPT_reporting_zero (local_data->euthanasia_cost);
  RPT_reporting_zero (local_data->indemnification_cost);
  RPT_reporting_zero (local_data->carcass_disposal_cost);
  RPT_reporting_zero (local_data->cleaning_disinfecting_cost);
  RPT_reporting_zero (local_data->vaccination_cost);
  RPT_reporting_zero (local_data->surveillance_cost);
  */

  /* This is an expensive cost calculation, so only do it if the user
   * will see any benefit from it. */
  if (local_data->surveillance_cost_param)
    {
      double **surveillance_cost_param = local_data->surveillance_cost_param;
      unsigned int nunits = zones->membership_length;
      unsigned int i;
      double cost = 0;
      
      for (i = 0; i < nunits; i++)
        {
          ZON_zone_t *zone = zones->membership[i]->parent;
          unsigned int zone_index = zone->level - 1;
          UNT_unit_t *unit = UNT_unit_list_get (units, i);

          if (surveillance_cost_param[zone_index] &&
              /* TODO.  This should probably be the authority's view
               * of whether the unit has been destroyed or not. */
              (unit->state != Destroyed))
            {
              cost =
                surveillance_cost_param[zone_index][unit->production_type] *
                (double) (unit->size);
              /*
              RPT_reporting_add_real (local_data->surveillance_cost, cost);
              RPT_reporting_add_real (local_data->total_cost, cost);
              */
              RPT_reporting_add_real (local_data->cumul_surveillance_cost, cost);
              RPT_reporting_add_real (local_data->cumul_total_cost, cost);
            }
        }
    }

#if DEBUG
  g_debug ("----- EXIT handle_new_day_event (%s)", MODEL_NAME);
#endif
}



/**
 * Responds to a vaccination event by computing its cost.
 *
 * @param self the model.
 * @param event a vaccination event.
 */
void
handle_vaccination_event (struct adsm_module_t_ *self, EVT_vaccination_event_t * event)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  double cost, sum = 0;

#if DEBUG
  g_debug ("----- ENTER handle_vaccination_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  unit = event->unit;

  if (local_data->vaccination_cost_params &&
      local_data->vaccination_cost_params[unit->production_type])
    {
      vaccination_cost_data_t *params = local_data->vaccination_cost_params[unit->production_type];

      /* Fixed cost for the unit. */
      cost = params->vaccination_fixed;
      RPT_reporting_add_real (local_data->cumul_vaccination_setup_cost, cost);
      sum += cost;

      /* Per-animal cost. */
      cost = params->vaccination * unit->size;

      if (params->capacity_used > params->baseline_capacity)
        {
          cost += params->extra_vaccination * unit->size;
        }
      else
        {
          params->capacity_used += unit->size;
          if (params->capacity_used > params->baseline_capacity)
            cost += params->extra_vaccination *
              (params->capacity_used - params->baseline_capacity);
        }
      /*
      RPT_reporting_add_real (local_data->vaccination_cost, cost);
      */
      RPT_reporting_add_real (local_data->cumul_vaccination_cost, cost);
      sum += cost;

      /*
      RPT_reporting_add_real (local_data->total_cost, cost);
      */
      RPT_reporting_add_real (local_data->cumul_vaccination_subtotal, sum);
      RPT_reporting_add_real (local_data->cumul_total_cost, sum);
    }

#if DEBUG
  g_debug ("----- EXIT handle_vaccination_event (%s)", MODEL_NAME);
#endif
}



/**
 * Responds to a destruction event by computing its cost.
 *
 * @param self the model.
 * @param event a destruction event.
 */
void
handle_destruction_event (struct adsm_module_t_ *self, EVT_destruction_event_t * event)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  unsigned int size;
  double cost, sum = 0;

#if DEBUG
  g_debug ("----- ENTER handle_destruction_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  unit = event->unit;
  size = unit->size;

  if (local_data->destruction_cost_params &&
      local_data->destruction_cost_params[unit->production_type])
    {
      destruction_cost_data_t *params = local_data->destruction_cost_params[unit->production_type];

      cost = params->appraisal;
      /* RPT_reporting_add_real (local_data->appraisal_cost, cost); */
      RPT_reporting_add_real (local_data->cumul_appraisal_cost, cost);
      sum += cost;

      cost = size * params->euthanasia;
      /* RPT_reporting_add_real (local_data->euthanasia_cost, cost); */
      RPT_reporting_add_real (local_data->cumul_euthanasia_cost, cost);
      sum += cost;

      cost = size * params->indemnification;
      /* RPT_reporting_add_real (local_data->indemnification_cost, cost); */
      RPT_reporting_add_real (local_data->cumul_indemnification_cost, cost);
      sum += cost;

      cost = size * params->carcass_disposal;
      /* RPT_reporting_add_real (local_data->carcass_disposal_cost, cost); */
      RPT_reporting_add_real (local_data->cumul_carcass_disposal_cost, cost);
      sum += cost;

      cost = params->cleaning_disinfecting;
      /* RPT_reporting_add_real (local_data->cleaning_disinfecting_cost, cost); */
      RPT_reporting_add_real (local_data->cumul_cleaning_disinfecting_cost, cost);
      sum += cost;

      /* RPT_reporting_add_real (local_data->total_cost, sum); */
      RPT_reporting_add_real (local_data->cumul_destruction_subtotal, sum);
      RPT_reporting_add_real (local_data->cumul_total_cost, sum);
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
      handle_new_day_event (self, units, zones, &(event->u.new_day));
      break;
    case EVT_Vaccination:
      handle_vaccination_event (self, &(event->u.vaccination));
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
 * Returns a text representation of this model.
 *
 * @param self the model.
 * @return a string.
 */
char *
to_string (struct adsm_module_t_ *self)
{
  GString *s;
  unsigned int i, j;
  char *chararray;
  local_data_t *local_data = (local_data_t *) (self->model_data);
  unsigned int nzones = ZON_zone_list_length (local_data->zones);
  unsigned int nprod_types = local_data->production_types->len;
  destruction_cost_data_t **destruction_cost_params = local_data->destruction_cost_params;
  vaccination_cost_data_t **vaccination_cost_params = local_data->vaccination_cost_params;
  double **surveillance_cost_param = local_data->surveillance_cost_param;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<%s", MODEL_NAME);
  for (i = 0; i < nprod_types; i++)
    {
      if ((destruction_cost_params &&
           destruction_cost_params[i]) ||
          (vaccination_cost_params &&
           vaccination_cost_params[i]))
        {
          g_string_append_printf (s, "\n  for %s",
                                  (char *) g_ptr_array_index (local_data->production_types, i));

          if (destruction_cost_params &&
              destruction_cost_params[i])
            {
              destruction_cost_data_t *params = local_data->destruction_cost_params[i];

              g_string_sprintfa (s, "\n    appraisal (per unit)=%g\n", params->appraisal);
              g_string_sprintfa (s, "    euthanasia (per animal)=%g\n", params->euthanasia);
              g_string_sprintfa (s, "    indemnification (per animal)=%g\n", params->indemnification);
              g_string_sprintfa (s, "    carcass-disposal (per animal)=%g\n", params->carcass_disposal);
              g_string_sprintfa (s, "    cleaning-disinfecting (per unit)=%g", params->cleaning_disinfecting);
            }

          if (vaccination_cost_params &&
              vaccination_cost_params[i])
            {
              vaccination_cost_data_t *params = local_data->vaccination_cost_params[i];

              g_string_sprintfa (s, "\n    vaccination-fixed (per unit)=%g\n", params->vaccination_fixed);
              g_string_sprintfa (s, "    vaccination (per animal)=%g\n", params->vaccination);
              g_string_sprintfa (s, "    baseline-capacity=%u\n", params->baseline_capacity);
              g_string_sprintfa (s, "    additional-vaccination (per animal)=%g", params->extra_vaccination);
            }
        }
    }

  if (surveillance_cost_param)
    {
      for (i = 0; i < nzones; i++)
        {
          if (surveillance_cost_param[i])
            {
              for (j = 0; j < nprod_types; j++)
                {
                  if (surveillance_cost_param[i][j] != 0)
                    {
                      g_string_append_printf (s, "\n for %s in %s",
                                              (char *) g_ptr_array_index (local_data->production_types, j),
                                              ZON_zone_list_get (local_data->zones, i)->name);
                      g_string_sprintfa (s, "\n  surveillance (per animal, per day)=%g", surveillance_cost_param[i][j]);
                    }
                }
            }
        }
    }

  g_string_append_c (s, '>');

  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Frees this model.  Does not free the production type name.
 *
 * @param self the model.
 */
void
local_free (struct adsm_module_t_ *self)
{
  local_data_t *local_data = (local_data_t *) (self->model_data);
  unsigned int nzones = ZON_zone_list_length (local_data->zones);
  unsigned int nprod_types = local_data->production_types->len;
  unsigned int i;

#if DEBUG
  g_debug ("----- ENTER free (%s)", MODEL_NAME);
#endif

  /* Free the dynamically-allocated parts. */
  if (local_data->destruction_cost_params)
    {
      for (i = 0; i < nprod_types; i++)
        {
          if (local_data->destruction_cost_params[i])
            {
              g_free (local_data->destruction_cost_params[i]);
              local_data->destruction_cost_params[i] = NULL;
            }
        }
      g_free (local_data->destruction_cost_params);
      local_data->destruction_cost_params = NULL;
    }

  if (local_data->vaccination_cost_params)
    {
      for (i = 0; i < nprod_types; i++)
        {
          if (local_data->vaccination_cost_params[i])
            {
              g_free (local_data->vaccination_cost_params[i]);
              local_data->vaccination_cost_params[i] = NULL;
            }
        }
      g_free (local_data->vaccination_cost_params);
      local_data->vaccination_cost_params = NULL;
    }

  if (local_data->surveillance_cost_param)
    {
      for (i = 0; i < nzones; i++)
        {
          if (local_data->surveillance_cost_param[i])
            {
              g_free (local_data->surveillance_cost_param[i]);
              local_data->surveillance_cost_param[i] = NULL;
            }
        }
      g_free (local_data->surveillance_cost_param);
      local_data->surveillance_cost_param = NULL;
    }

  /*
  RPT_free_reporting (local_data->total_cost);
  RPT_free_reporting (local_data->appraisal_cost);
  RPT_free_reporting (local_data->euthanasia_cost);
  RPT_free_reporting (local_data->indemnification_cost);
  RPT_free_reporting (local_data->carcass_disposal_cost);
  RPT_free_reporting (local_data->cleaning_disinfecting_cost);
  RPT_free_reporting (local_data->vaccination_cost);
  RPT_free_reporting (local_data->surveillance_cost);
  */

  g_free (local_data);
  g_ptr_array_free (self->outputs, /* free_seg = */ TRUE); /* also frees all output variables */
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Adds a set of parameters to an economic model.
 *
 * @param data this module ("self"), but cast to a void *.
 * @param ncols number of columns in the SQL query result.
 * @param values values returned by the SQL query, all in text form.
 * @param colname names of columns in the SQL query result.
 * @return 0
 */
static int
set_params (void *data, int ncols, char **value, char **colname)
{
  adsm_module_t *self;
  local_data_t *local_data;
  guint production_type_id;
  destruction_cost_data_t *d;
  vaccination_cost_data_t *v;

#if DEBUG
  g_debug ("----- ENTER set_params (%s)", MODEL_NAME);
#endif

  g_assert (ncols == 10);

  self = (adsm_module_t *)data;
  local_data = (local_data_t *) (self->model_data);

  /* Find out which production type these parameters apply to. */
  production_type_id =
    adsm_read_prodtype (value[0], local_data->production_types);

  /* Destruction Cost Parameters */
  if (value[1] != NULL)
    {
      if (local_data->destruction_cost_params == NULL)
        {
          local_data->destruction_cost_params =
            g_new0 (destruction_cost_data_t *, local_data->production_types->len);
        }

      /* Check that we are not overwriting an existing parameter block (that would
       * indicate a bug). */
      g_assert (local_data->destruction_cost_params[production_type_id] == NULL);

      /* Create a new parameter block. */
      d = g_new (destruction_cost_data_t, 1);
      local_data->destruction_cost_params[production_type_id] = d;

      errno = 0;
      d->appraisal = strtod (value[1], NULL);
      g_assert (errno != ERANGE);
      errno = 0;
      d->euthanasia = strtod (value[2], NULL);
      g_assert (errno != ERANGE);
      errno = 0;
      d->indemnification = strtod (value[3], NULL);
      g_assert (errno != ERANGE);
      errno = 0;
      d->carcass_disposal = strtod (value[4], NULL);
      g_assert (errno != ERANGE);
      errno = 0;
      d->cleaning_disinfecting = strtod (value[5], NULL);
      g_assert (errno != ERANGE);
    }

  /* Vaccination Cost Parameters */

  if (value[6] != NULL)
    {
      if (local_data->vaccination_cost_params == NULL)
        {
          local_data->vaccination_cost_params =
            g_new0 (vaccination_cost_data_t *, local_data->production_types->len);
        }

      /* Check that we are not overwriting an existing parameter block (that would
       * indicate a bug). */
      g_assert (local_data->vaccination_cost_params[production_type_id] == NULL);

      /* Create a new parameter block. */
      v = g_new (vaccination_cost_data_t, 1);
      local_data->vaccination_cost_params[production_type_id] = v;

      errno = 0;
      v->baseline_capacity = strtol (value[6], NULL, /* base */ 10);
      g_assert (errno != ERANGE && errno != EINVAL);  
      errno = 0;
      v->vaccination = strtod (value[7], NULL);
      g_assert (errno != ERANGE);
      errno = 0;
      v->extra_vaccination = strtod (value[8], NULL);
      g_assert (errno != ERANGE);
      errno = 0;
      v->vaccination_fixed = strtod (value[9], NULL);
      g_assert (errno != ERANGE);

      /* No vaccinations have been performed yet. */
      v->capacity_used = 0;
    }

  return 0;
}



/**
 * Adds a set of zone/production type combination specific parameters to an
 * economic model.
 *
 * @param data this module ("self"), but cast to a void *.
 * @param ncols number of columns in the SQL query result.
 * @param values values returned by the SQL query, all in text form.
 * @param colname names of columns in the SQL query result.
 * @return 0
 */
static int
set_zone_params (void *data, int ncols, char **value, char **colname)
{
  adsm_module_t *self;
  local_data_t *local_data;
  guint zone_id, production_type_id;

  #if DEBUG
    g_debug ("----- ENTER set_zone_params (%s)", MODEL_NAME);
  #endif

  g_assert (ncols == 3);

  self = (adsm_module_t *)data;
  local_data = (local_data_t *) (self->model_data);

  /* Find out which zone/production type combination these parameters apply
   * to. */
  zone_id = adsm_read_zone (value[0], local_data->zones);
  production_type_id = adsm_read_prodtype (value[1], local_data->production_types);

  /* Create a paramater block if needed. */
  if (local_data->surveillance_cost_param == NULL)
    {
      guint nzones;
      nzones = ZON_zone_list_length (local_data->zones);
      local_data->surveillance_cost_param = g_new0 (double *, nzones);
    }
  if (local_data->surveillance_cost_param[zone_id] == NULL)
    {
      guint nprod_types;
      nprod_types = local_data->production_types->len;
      local_data->surveillance_cost_param[zone_id] = g_new0 (double, nprod_types);
    }

  /* Read the parameter. */
  errno = 0;
  local_data->surveillance_cost_param[zone_id][production_type_id] = strtod (value[2], NULL);
  g_assert (errno != ERANGE);

  #if DEBUG
    g_debug ("----- EXIT set_zone_params (%s)", MODEL_NAME);
  #endif

  return 0;
}



/**
 * Returns a new economic model.
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
    EVT_Vaccination,
    EVT_Destruction,
    0
  };
  char *sqlerr;

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

  /* local_data->destruction_cost_params, ->vaccination_cost_params
   * hold 1D arrays of pointers to parameter blocks (indexed by
   * [production_type]).  local_data->surveillance_cost_param holds a
   * 2D array of pointers to parameter blocks (indexed by
   * [zone_type][production_type]).  Initially, all pointers are
   * NULL.  Pointers will be created as needed in the set_params
   * function. */
  local_data->production_types = units->production_type_names;
  local_data->zones = zones;
  local_data->destruction_cost_params = NULL;
  local_data->vaccination_cost_params = NULL;
  local_data->surveillance_cost_param = NULL;

  /*
  local_data->total_cost = RPT_new_reporting ("total-cost", RPT_real, RPT_never);
  local_data->appraisal_cost =
    RPT_new_reporting ("appraisal-cost", RPT_real, RPT_never);
  local_data->euthanasia_cost =
    RPT_new_reporting ("euthanasia-cost", RPT_real, RPT_never);
  local_data->indemnification_cost =
    RPT_new_reporting ("indemnification-cost", RPT_real, RPT_never);
  local_data->carcass_disposal_cost =
    RPT_new_reporting ("carcass-disposal-cost", RPT_real, RPT_never);
  local_data->cleaning_disinfecting_cost =
    RPT_new_reporting ("cleaning-and-disinfecting-cost", RPT_real, RPT_never);
  local_data->vaccination_cost =
    RPT_new_reporting ("vaccination-cost", RPT_real, RPT_never);
  local_data->surveillance_cost =
    RPT_new_reporting ("surveillance-cost", RPT_real, RPT_never);
  */
  local_data->cumul_total_cost =
    RPT_new_reporting ("costsTotal", RPT_real);
  local_data->cumul_appraisal_cost =
    RPT_new_reporting ("destrAppraisal", RPT_real);
  local_data->cumul_euthanasia_cost =
    RPT_new_reporting ("destrEuthanasia", RPT_real);
  local_data->cumul_indemnification_cost =
    RPT_new_reporting ("destrIndemnification", RPT_real);
  local_data->cumul_carcass_disposal_cost =
    RPT_new_reporting ("destrDisposal", RPT_real);
  local_data->cumul_cleaning_disinfecting_cost =
    RPT_new_reporting ("destrCleaning", RPT_real);
  local_data->cumul_destruction_subtotal =
    RPT_new_reporting ("destrSubtotal", RPT_real);
  local_data->cumul_vaccination_setup_cost =
    RPT_new_reporting ("vaccSetup", RPT_real);
  local_data->cumul_vaccination_cost =
    RPT_new_reporting ("vaccVaccination", RPT_real);
  local_data->cumul_vaccination_subtotal =
    RPT_new_reporting ("vaccSubtotal", RPT_real);
  local_data->cumul_surveillance_cost =
    RPT_new_reporting ("costSurveillance", RPT_real);
  /*
  g_ptr_array_add (self->outputs, local_data->total_cost);
  g_ptr_array_add (self->outputs, local_data->appraisal_cost);
  g_ptr_array_add (self->outputs, local_data->euthanasia_cost);
  g_ptr_array_add (self->outputs, local_data->indemnification_cost);
  g_ptr_array_add (self->outputs, local_data->carcass_disposal_cost);
  g_ptr_array_add (self->outputs, local_data->cleaning_disinfecting_cost);
  g_ptr_array_add (self->outputs, local_data->vaccination_cost);
  g_ptr_array_add (self->outputs, local_data->surveillance_cost);
  */
  g_ptr_array_add (self->outputs, local_data->cumul_total_cost);
  g_ptr_array_add (self->outputs, local_data->cumul_appraisal_cost);
  g_ptr_array_add (self->outputs, local_data->cumul_euthanasia_cost);
  g_ptr_array_add (self->outputs, local_data->cumul_indemnification_cost);
  g_ptr_array_add (self->outputs, local_data->cumul_carcass_disposal_cost);
  g_ptr_array_add (self->outputs, local_data->cumul_cleaning_disinfecting_cost);
  g_ptr_array_add (self->outputs, local_data->cumul_destruction_subtotal);
  g_ptr_array_add (self->outputs, local_data->cumul_vaccination_setup_cost);
  g_ptr_array_add (self->outputs, local_data->cumul_vaccination_cost);
  g_ptr_array_add (self->outputs, local_data->cumul_vaccination_subtotal);
  g_ptr_array_add (self->outputs, local_data->cumul_surveillance_cost);

  /* Call the set_params function to read the production type specific
   * parameters. */
  sqlite3_exec (params,
                "SELECT prodtype.name,cost_of_destruction_appraisal_per_unit,cost_of_euthanasia_per_animal,cost_of_indemnification_per_animal,cost_of_carcass_disposal_per_animal,cost_of_destruction_cleaning_per_unit,vaccination_demand_threshold,cost_of_vaccination_baseline_per_animal,cost_of_vaccination_additional_per_animal,cost_of_vaccination_setup_per_unit FROM ScenarioCreator_productiontype prodtype,ScenarioCreator_controlprotocol protocol,ScenarioCreator_protocolassignment xref WHERE prodtype.id=xref.production_type_id AND xref.control_protocol_id=protocol.id AND use_cost_accounting=1",
                set_params, self, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }

  /* Call the set_zone_params function to read the zone/production type
   * combination specific parameters. */
  sqlite3_exec (params,
                "SELECT zone.name,prodtype.name,cost_of_surveillance_per_animal_day "
                "FROM ScenarioCreator_zone zone,ScenarioCreator_productiontype prodtype,ScenarioCreator_zoneeffectassignment pairing,ScenarioCreator_zoneeffect effect "
                "WHERE zone.id=pairing.zone_id "
                "AND prodtype.id=pairing.production_type_id "
                "AND effect.id=pairing.effect_id",
                set_zone_params, self, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file economic_model.c */
