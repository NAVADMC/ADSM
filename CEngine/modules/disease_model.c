/** @file disease_model.c
 * Module that encapsulates knowledge about a disease.
 *
 * When a unit is infected, this module changes the unit's state to Latent.  It
 * decides how long the unit will remain latent, infectious without clinical
 * signs, infectious with clinical signs, and immune by sampling from the
 * distributions given as parameters.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date April 2003
 *
 * Copyright &copy; University of Guelph, 2003-2009
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
#define new disease_model_new
#define set_params disease_model_set_params
#define run disease_model_run
#define reset disease_model_reset
#define events_listened_for disease_model_events_listened_for
#define to_string disease_model_to_string
#define local_free disease_model_free
#define handle_infection_event disease_model_handle_infection_event

#include "module.h"
#include "module_util.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#if HAVE_STRINGS_H
#  include <strings.h>
#endif

#if HAVE_MATH_H
#  include <math.h>
#endif

#include "disease_model.h"

#if !HAVE_ROUND && HAVE_RINT
#  define round rint
#endif

/* Temporary fix -- "round" and "rint" are in the math library on Red Hat 7.3,
 * but they're #defined so AC_CHECK_FUNCS doesn't find them. */
double round (double x);

/** This must match an element name in the DTD. */
#define MODEL_NAME "disease-model"



#define NEVENTS_LISTENED_FOR 1
EVT_event_type_t events_listened_for[] = { EVT_Infection };



extern const char *PDF_dist_type_name[];



/* Specialized information for this model. */
typedef struct
{
  PDF_dist_t *latent_period;
  PDF_dist_t *infectious_subclinical_period;
  PDF_dist_t *infectious_clinical_period;
  PDF_dist_t *immunity_period;
  REL_chart_t *prevalence;
}
param_block_t;



typedef struct
{
  GPtrArray *production_types; /**< Each item in the list is a char *. */
  param_block_t **param_block; /**< Blocks of parameters.  Use an expression of
    the form param_block[production_type] to get a pointer to a particular
    param_block. */
  RPT_reporting_t *elapsed_time;
  sqlite3 *db; /* Temporarily stash a pointer to the parameters database here
    so that it will be available to the set_params function. */
}
local_data_t;



/**
 * Attaches the relevant prevalence chart to each unit structure.
 *
 * @param self the model.
 * @param units the unit list.
 */
void
attach_prevalence_charts (struct spreadmodel_model_t_ *self,
			  UNT_unit_list_t *units)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  unsigned int nunits;
  unsigned int i;
  param_block_t *param_block;

#if DEBUG
  g_debug ("----- ENTER attach_prevalence_charts (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  
  nunits = UNT_unit_list_length (units);
  for (i = 0; i < nunits; i++)
    {
      unit = UNT_unit_list_get (units, i);
      param_block = local_data->param_block[unit->production_type];
      if (param_block != NULL)
        unit->prevalence_curve = param_block->prevalence;
    }

#if DEBUG
  g_debug ("----- EXIT attach_prevalence_charts (%s)", MODEL_NAME);
#endif
  return;
}



/**
 * Responds to an infection event by changing the unit's state from susceptible
 * to infected.
 *
 * @param self the model.
 * @param event an infection event.
 * @param rng a random number generator.
 */
void
handle_infection_event (struct spreadmodel_model_t_ *self,
                        EVT_infection_event_t * event, RAN_gen_t * rng)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  param_block_t *param_block;
  int latent_period, infectious_subclinical_period, infectious_clinical_period, immunity_period;
  unsigned int day_in_disease_cycle;

#if DEBUG
  g_debug ("----- ENTER handle_infection_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  unit = event->infected_unit;
  param_block = local_data->param_block[unit->production_type];
  if (param_block == NULL)
    {
#if DEBUG
      g_debug ("unit is %s, sub-model does not apply", unit->production_type_name);
#endif
      goto end;
    }

  day_in_disease_cycle = 0;

  /* Latent period. */
  latent_period = (int) round (PDF_random (param_block->latent_period, rng));
  if (latent_period < 0)
    {
      #if DEBUG
        g_debug ("%s distribution returned %i for latent period, using 0 instead",
                 PDF_dist_type_name[param_block->latent_period->type], latent_period);
      #endif
      latent_period = 0;
    }
  if (event->override_initial_state == Latent)
    {
      if (event->override_days_in_state > 0 && event->override_days_left_in_state > 0)
        {
          /* Override both the days elapsed and the days left in the latent
           * period. */
          latent_period = event->override_days_in_state + event->override_days_left_in_state;
          day_in_disease_cycle = event->override_days_in_state;
        }
      else if (event->override_days_in_state > 0)
        {
          /* Override just the days elapsed in the latent period.  If the given
           * value is greater than the sampled length of the latent period,
           * extend the latent period. */
          latent_period = MAX(latent_period, event->override_days_in_state);
          day_in_disease_cycle = event->override_days_in_state;
        }
      else if (event->override_days_left_in_state > 0)
        {
          /* Override just the days left in the latent period.  If the given
           * value is greater than the sampled length of the latent period,
           * extend the latent period. */
          latent_period = MAX(latent_period, event->override_days_left_in_state);
          day_in_disease_cycle = latent_period - event->override_days_left_in_state;
        }
    }
#if DEBUG
  g_debug ("latent period will last %i days", latent_period);
#endif

  /* Infectious subclinical period. */
  infectious_subclinical_period =
    (int) round (PDF_random (param_block->infectious_subclinical_period, rng));
  if (infectious_subclinical_period < 0)
    {
      #if DEBUG
        g_debug ("%s distribution returned %i for infectious subclinical period, using 0 instead",
                 PDF_dist_type_name[param_block->infectious_subclinical_period->type],
                 infectious_subclinical_period);
      #endif
      infectious_subclinical_period = 0;
    }
  if (event->override_initial_state == InfectiousSubclinical)
    {
      day_in_disease_cycle = latent_period;
      if (event->override_days_in_state > 0 && event->override_days_left_in_state > 0)
        {
          /* Override both the days elapsed and the days left in the infectious
           * subclinical period. */
          infectious_subclinical_period = event->override_days_in_state + event->override_days_left_in_state;
          day_in_disease_cycle += event->override_days_in_state;
        }
      else if (event->override_days_in_state > 0)
        {
          /* Override just the days elapsed in the infectious subclinical
           * period.  If the given value is greater than the sampled length of
           * the infectious subclinical period, extend the infectious
           * subclinical period. */
          infectious_subclinical_period = MAX(infectious_subclinical_period, event->override_days_in_state);
          day_in_disease_cycle += event->override_days_in_state;
        }
      else if (event->override_days_left_in_state > 0)
        {
          /* Override just the days left in the infectious subclinical period.
           * If the given value is greater than the sampled length of the
           * infectious subclinical period, extend the infectious subclinical
           * period. */
          infectious_subclinical_period = MAX(infectious_subclinical_period, event->override_days_left_in_state);
          day_in_disease_cycle += (infectious_subclinical_period - event->override_days_left_in_state);
        }
    }
#if DEBUG
  g_debug ("infectiousness (with no visible signs) will last %i days", infectious_subclinical_period);
#endif

  /* Infectious clinical period. */
  infectious_clinical_period =
    (int) round (PDF_random (param_block->infectious_clinical_period, rng));
  if (infectious_clinical_period < 0)
    {
      #if DEBUG
        g_debug ("%s distribution returned %i for infectious clinical period, using 0 instead",
                 PDF_dist_type_name[param_block->infectious_clinical_period->type],
                 infectious_clinical_period);
      #endif
      infectious_clinical_period = 0;
    }
  if (event->override_initial_state == InfectiousClinical)
    {
      day_in_disease_cycle = latent_period + infectious_subclinical_period;
      if (event->override_days_in_state > 0 && event->override_days_left_in_state > 0)
        {
          /* Override both the days elapsed and the days left in the infectious
           * clinical period. */
          infectious_clinical_period = event->override_days_in_state + event->override_days_left_in_state;
          day_in_disease_cycle += event->override_days_in_state;
        }
      else if (event->override_days_in_state > 0)
        {
          /* Override just the days elapsed in the infectious clinical period.
           * If the given value is greater than the sampled length of the
           * infectious clinical period, extend the infectious clinical period. */
          infectious_clinical_period = MAX(infectious_clinical_period, event->override_days_in_state);
          day_in_disease_cycle += event->override_days_in_state;
        }
      else if (event->override_days_left_in_state > 0)
        {
          /* Override just the days left in the infectious clinical period.  If
           * the given value is greater than the sampled length of the
           * infectious clinical period, extend the infectious clinical period. */
          infectious_clinical_period = MAX(infectious_clinical_period, event->override_days_left_in_state);
          day_in_disease_cycle += (infectious_clinical_period - event->override_days_left_in_state);
        }
    }
#if DEBUG
  g_debug ("infectiousness (with visible signs) will last %i days", infectious_clinical_period);
#endif

  /* Natural immunity period. */
  immunity_period = (int) round (PDF_random (param_block->immunity_period, rng));
  if (immunity_period < 0)
    {
      #if DEBUG
        g_debug ("%s distribution returned %i for immunity period, using 0 instead",
                 PDF_dist_type_name[param_block->immunity_period->type], immunity_period);
      #endif
      immunity_period = 0;
    }
  if (event->override_initial_state == NaturallyImmune)
    {
      day_in_disease_cycle = latent_period + infectious_subclinical_period + infectious_clinical_period;
      if (event->override_days_in_state > 0 && event->override_days_left_in_state > 0)
        {
          /* Override both the days elapsed and the days left in the immunity
           * period. */
          immunity_period = event->override_days_in_state + event->override_days_left_in_state;
          day_in_disease_cycle += event->override_days_in_state;
        }
      else if (event->override_days_in_state > 0)
        {
          /* Override just the days elapsed in the immunity period.  If the
           * given value is greater than the sampled length of the immunity
           * period, extend the immunity period. */
          immunity_period = MAX(immunity_period, event->override_days_in_state);
          day_in_disease_cycle += event->override_days_in_state;
        }
      else if (event->override_days_left_in_state > 0)
        {
          /* Override just the days left in the immunity period.  If the given
           * value is greater than the sampled length of the immunity period,
           * extend the immunity period. */
          immunity_period = MAX(immunity_period, event->override_days_left_in_state);
          day_in_disease_cycle += (immunity_period - event->override_days_left_in_state);
        }
    }
#if DEBUG
  g_debug ("natural immunity will last %i days", immunity_period);
#endif

  UNT_infect (event->infected_unit, latent_period, infectious_subclinical_period,
              infectious_clinical_period, immunity_period, day_in_disease_cycle);

end:
#if DEBUG
  g_debug ("----- EXIT handle_infection_event (%s)", MODEL_NAME);
#endif
  return;
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
#if DEBUG
  g_debug ("----- ENTER run (%s)", MODEL_NAME);
#endif

  switch (event->type)
    {
    case EVT_Infection:
      handle_infection_event (self, &(event->u.infection), rng);
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
  unsigned int nprod_types, i;
  param_block_t *param_block;
  char *substring, *chararray;
  local_data_t *local_data;

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

      substring = PDF_dist_to_string (param_block->latent_period);
      g_string_sprintfa (s, "\n    latent-period=%s", substring);
      g_free (substring);

      substring = PDF_dist_to_string (param_block->infectious_subclinical_period);
      g_string_sprintfa (s, "\n    infectious-subclinical-period=%s", substring);
      g_free (substring);

      substring = PDF_dist_to_string (param_block->infectious_clinical_period);
      g_string_sprintfa (s, "\n    infectious-clinical-period=%s", substring);
      g_free (substring);

      substring = PDF_dist_to_string (param_block->immunity_period);
      g_string_sprintfa (s, "\n    immunity-period=%s", substring);
      g_free (substring);

      if (param_block->prevalence != NULL)
        {
          substring = REL_chart_to_string (param_block->prevalence);
          g_string_append_printf (s, "\n    prevalence=%s", substring);
          g_free (substring);
        }
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
local_free (struct spreadmodel_model_t_ *self)
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
      if (param_block == NULL)
        continue;

      PDF_free_dist (param_block->latent_period);
      PDF_free_dist (param_block->infectious_subclinical_period);
      PDF_free_dist (param_block->infectious_clinical_period);
      PDF_free_dist (param_block->immunity_period);
      REL_free_chart (param_block->prevalence);
      g_free (param_block);
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
 * Adds a set of parameters to a disease model.
 *
 * @param data this module ("self"), but cast to a void *.
 * @param ncols number of columns in the SQL query result.
 * @param values values returned by the SQL query, all in text form.
 * @param colname names of columns in the SQL query result.
 * @return 0
 */
static int
set_params_s (void *data, int ncols, char **value, char **colname)
{
  spreadmodel_model_t *self;
  local_data_t *local_data;
  sqlite3 *params;
  param_block_t t;
  guint pdf_id, rel_id;
  gboolean *production_type;
  unsigned int nprod_types, i;

#if DEBUG
  g_debug ("----- ENTER set_params (%s)", MODEL_NAME);
#endif

  self = (spreadmodel_model_t *)data;
  local_data = (local_data_t *) (self->model_data);
  params = local_data->db;

  /* Read the parameters and store them in a temporary param_block_t
   * structure. */
  g_assert (ncols == 6);
  pdf_id = strtol(value[1], NULL, /* base */ 10);
  t.latent_period = PAR_get_PDF (params, pdf_id);
  pdf_id = strtol(value[2], NULL, /* base */ 10);
  t.infectious_subclinical_period = PAR_get_PDF (params, pdf_id);
  pdf_id = strtol(value[3], NULL, /* base */ 10);
  t.infectious_clinical_period = PAR_get_PDF (params, pdf_id);
  pdf_id = strtol(value[4], NULL, /* base */ 10);
  t.immunity_period = PAR_get_PDF (params, pdf_id);
  if (value[5] != NULL)
    {
      rel_id = strtol(value[5], NULL, /* base */ 10);
      t.prevalence = PAR_get_relchart (params, rel_id);
      if (REL_chart_min (t.prevalence) < 0)
        {
          g_error ("Y-values <0 are not allowed in a prevalence chart");
        }
      if (REL_chart_max (t.prevalence) > 1)
        {
          g_error ("Y-values >1 are not allowed in a prevalence chart");
        }
      /* Scale and translate so that the x-values go from 0 to 1. */
      REL_chart_set_domain (t.prevalence, 0, 1);
    }
  else
    {
      /* Don't use prevalence, use the old behaviour. */
      t.prevalence = NULL;
    }

  /* Find out which production types these parameters apply to. */
  production_type =
    spreadmodel_read_prodtype_attribute (value[0], local_data->production_types);

  /* Copy the parameters to the appropriate place. */
  nprod_types = local_data->production_types->len;
  for (i = 0; i < nprod_types; i++)
    {
      param_block_t *param_block;

      if (production_type[i] == FALSE)
        continue;

      /* Create a parameter block for this production type, or overwrite
       * the existing one. */
      param_block = local_data->param_block[i];
      if (param_block == NULL)
        {
          #if DEBUG
            g_debug ("setting parameters for %s",
                     (char *) g_ptr_array_index (local_data->production_types, i));
          #endif
          param_block = g_new (param_block_t, 1);
          local_data->param_block[i] = param_block;
        }
      else
        {
          g_warning ("overwriting previous parameters for %s",
                     (char *) g_ptr_array_index (local_data->production_types, i));
          PDF_free_dist (param_block->latent_period);
          PDF_free_dist (param_block->infectious_subclinical_period);
          PDF_free_dist (param_block->infectious_clinical_period);
          PDF_free_dist (param_block->immunity_period);
          REL_free_chart (param_block->prevalence); /* safe even if NULL */
        }
      param_block->latent_period = PDF_clone_dist (t.latent_period);
      param_block->infectious_subclinical_period = PDF_clone_dist (t.infectious_subclinical_period);
      param_block->infectious_clinical_period = PDF_clone_dist (t.infectious_clinical_period);
      param_block->immunity_period = PDF_clone_dist (t.immunity_period);
      param_block->prevalence = REL_clone_chart (t.prevalence);
    }

  g_free (production_type);
  PDF_free_dist (t.latent_period);
  PDF_free_dist (t.infectious_subclinical_period);
  PDF_free_dist (t.infectious_clinical_period);
  PDF_free_dist (t.immunity_period);
  REL_free_chart (t.prevalence); /* safe even if NULL */

#if DEBUG
  g_debug ("----- EXIT set_params (%s)", MODEL_NAME);
#endif

  return 0;
}



/**
 * Returns a new disease model.
 */
spreadmodel_model_t *
new (sqlite3 * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  spreadmodel_model_t *self;
  local_data_t *local_data;
  unsigned int nprod_types;
  char *sqlerr;

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
  /* self->set_params = set_params; */
  self->run = run;
  self->reset = reset;
  self->is_singleton = TRUE;
  self->is_listening_for = spreadmodel_model_is_listening_for;
  self->has_pending_actions = spreadmodel_model_answer_no;
  self->has_pending_infections = spreadmodel_model_answer_no;
  self->to_string = to_string;
  self->printf = spreadmodel_model_printf;
  self->fprintf = spreadmodel_model_fprintf;
  self->free = local_free;

  local_data->production_types = units->production_type_names;
  nprod_types = local_data->production_types->len;
  local_data->param_block = g_new0 (param_block_t *, nprod_types);

  /* Call the set_params function to read the production type combination
   * specific parameters. */
  local_data->db = params;
  sqlite3_exec (params,
                "SELECT prodtype.name,disease_latent_period_pdf_id,disease_subclinical_period_pdf_id,disease_clinical_period_pdf_id,disease_immune_period_pdf_id,disease_prevalence_relid_id FROM ScenarioCreator_productiontype prodtype,ScenarioCreator_diseasereactionassignment xref,ScenarioCreator_diseasereaction disease WHERE prodtype.id=xref.production_type_id AND xref.reaction_id = disease.id",
                set_params_s, self, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }
  local_data->db = NULL;

  /* Attach the relevant prevalence chart to each unit structure. */
  attach_prevalence_charts (self, units);

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file disease_model.c */
