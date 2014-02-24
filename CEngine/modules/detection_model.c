/** @file detection_model.c
 * Module that simulates a farmer or veterinarian detecting signs of disease.
 *
 * On each day, this module follows these steps:
 * <ol>
 *   <li>
 *     Look up the probability <i>p</i><sub>1</sub> that a farmer or
 *     veterinarian will detect signs of disease based on the number of days
 *     since a public announcement of an outbreak.
 *   <li>
 *     For each InfectiousClinical unit,
 *     <ol>
 *       <li>
 *         Look up the probability <i>p</i><sub>2</sub> that a farmer or
 *         veterinarian will detect signs of disease based on the number of
 *         days the unit has been InfectiousClinical.
 *       <li>
 *         If the unit is not inside a zone focus,
 *         <ol>
 *           <li>
 *             Compute the probability of detection <i>P</i> =
 *             <i>p</i><sub>1</sub> &times; <i>p</i><sub>2</sub>.
 *         </ol>
 *       <li>
 *         If the unit is inside a zone focus, <i>p</i><sub>1</sub> is assumed
 *         to be 1 and a multiplier may be applied to <i>p</i><sub>2</sub> to
 *         simulate increased scrutiny.
 *         <ol>
 *           <li>
 *             Compute the probability of detection <i>P</i> =
 *             <i>p</i><sub>2</sub> &times; zone multiplier.
 *         </ol>
 *       <li>
 *         Generate a random number <i>r</i> in [0,1).
 *       <li>
 *         If <i>r</i> < <i>P</i>, report a detection to the authorities.
 *     </ol>
 * </ol>
 *
 * This module also listens for requests for a visual
 * inspection.  Such a request might happen when a visit is made to perform
 * tracing, for example.  The request may have a multiplier to simulate
 * increased scrutiny.  The probability of detection <i>P</i> =
 * <i>p</i><sub>2</sub> &times; request multiplier.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date June 2003
 *
 * Copyright &copy; University of Guelph, 2003-2008
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 *
 * @todo Reset detected flag when unit goes naturally immune.
 */

#if HAVE_CONFIG_H
#  include <config.h>
#endif

/* To avoid name clashes when multiple modules have the same interface. */
#define new detection_model_new
#define set_params detection_model_set_params
#define run detection_model_run
#define reset detection_model_reset
#define events_listened_for detection_model_events_listened_for
#define to_string detection_model_to_string
#define local_free detection_model_free
#define handle_new_day_event detection_model_handle_new_day_event
#define handle_exam_event detection_model_handle_exam_event
#define handle_public_announcement_event detection_model_handle_public_announcement_event

#include "module.h"
#include "module_util.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#if HAVE_STRINGS_H
#  include <strings.h>
#endif

#include "detection_model.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "detection-model"



#define NEVENTS_LISTENED_FOR 3
EVT_event_type_t events_listened_for[] = {
  EVT_NewDay, EVT_PublicAnnouncement, EVT_Exam };



/* Specialized information for this model. */
typedef struct
{
  REL_chart_t *prob_report_vs_days_clinical;
  REL_chart_t *prob_report_vs_days_since_outbreak;
}
param_block_t;



typedef struct
{
  GPtrArray *production_types; /**< Each item in the list is a char *. */
  ZON_zone_list_t *zones;
  param_block_t **param_block; /**< Blocks of parameters.  Use an expression
    of the form param_block[production_type] to get a pointer to a particular
    param_block. */
  double **zone_multiplier; /**< A 2D array of multipliers.  Use an expression
    of the form zone_multiplier[zone->level-1][production_type] to get a
    particular multiplier. */
  gboolean outbreak_known;
  int public_announcement_day;
  gboolean *detected;
  unsigned int nunits; /**< Number of units.  Stored here because it is also
    the length of the detected flag array. */
  double *prob_report_from_awareness; /**< An array with the probability of
    reporting due to one value per production type.  The array is initialized
    in the reset function, and the values are re-calculated each day once an
    outbreak is known. */
}
local_data_t;



/**
 * Responds to a new day event by stochastically generating detections.
 *
 * @param self the model.
 * @param units a unit list.
 * @param zones a zone list.
 * @param event a new day event.
 * @param rng a random number generator.
 * @param queue for any new events the model creates.
 */
void
handle_new_day_event (struct spreadmodel_model_t_ *self, UNT_unit_list_t * units,
                      ZON_zone_list_t * zones, EVT_new_day_event_t * event,
                      RAN_gen_t * rng, EVT_event_queue_t * queue)
{
  local_data_t *local_data;
  unsigned int lookup_day;
  unsigned int nprod_types;
  param_block_t *param_block;
  UNT_unit_t *unit;
  unsigned int nunits;
  unsigned int prod_type;
  ZON_zone_fragment_t *background_zone, *fragment;
  ZON_zone_t *zone;
  double prob_report_from_signs, *prob_report_from_awareness;
  double P, r;
  unsigned int i;

#if DEBUG
  g_debug ("----- ENTER handle_new_day_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* For each production type, compute the probability that the disease would 
   * be noticed, based on community awareness of an outbreak. */
  prob_report_from_awareness = local_data->prob_report_from_awareness;
  nprod_types = local_data->production_types->len;
  if (local_data->outbreak_known)
    {
      lookup_day = event->day - local_data->public_announcement_day;
      for (i = 0; i < nprod_types; i++)
        {
          param_block = local_data->param_block[i];

          if (param_block == NULL)
            continue;

          prob_report_from_awareness[i] =
            REL_chart_lookup (lookup_day, param_block->prob_report_vs_days_since_outbreak);
        }
    }

  background_zone = ZON_zone_list_get_background (zones);

  nunits = UNT_unit_list_length (units);
  for (i = 0; i < nunits; i++)
    {
      unit = UNT_unit_list_get (units, i);

      /* Check whether the unit is showing clinical signs of disease and is a
       * production type we're interested in.  If not, go on to the next
       * unit. */
      prod_type = unit->production_type;
      param_block = local_data->param_block[prod_type];
      if (unit->state != InfectiousClinical || param_block == NULL)
        continue;

      /* Find which zone the unit is in. */
      fragment = zones->membership[unit->index];
      zone = fragment->parent;

      #if DEBUG
        g_debug ("unit \"%s\" is %s, in zone \"%s\", state is %s, %s detected",
                 unit->official_id,
                 unit->production_type_name,
                 zone->name,
                 UNT_state_name[unit->state], local_data->detected[i] ? "already" : "not");
      #endif
      /* Check whether the unit has already been detected.  If so, go on to the
       * next unit. */
      if (local_data->detected[i])
        continue;

      /* Compute the probability that the disease would be noticed, based
       * on clinical signs.  This is multiplied with the probability
       * computed above. */
      #if DEBUG
        g_debug ("using chart value for day %i in clinical state", unit->days_in_state);
      #endif
      prob_report_from_signs =
        REL_chart_lookup (unit->days_in_state, param_block->prob_report_vs_days_clinical);

      if (ZON_same_zone (background_zone, fragment))
        {
          P = prob_report_from_signs * prob_report_from_awareness[prod_type];
          #if DEBUG
            g_debug ("P = %g * %g", prob_report_from_signs, prob_report_from_awareness[prod_type]);
          #endif
        }
      else
        {
          P = prob_report_from_signs * local_data->zone_multiplier[zone->level - 1][prod_type];
          #if DEBUG
            g_debug ("P = %g * %g",
                     prob_report_from_signs, local_data->zone_multiplier[zone->level - 1][prod_type]);
          #endif
        }
      r = RAN_num (rng);
      if (r < P)
        {
          #if DEBUG
            g_debug ("r (%g) < P (%g)", r, P);
            g_debug ("unit \"%s\" detected and reported", unit->official_id);
          #endif
          /* There was no diagnostic test, so SPREADMODEL_TestUnspecified is a legitimate value here. */
          EVT_event_enqueue (queue,
                             EVT_new_detection_event (unit, event->day,
                                                      SPREADMODEL_DetectionClinicalSigns,
                                                      SPREADMODEL_TestUnspecified));
          local_data->detected[unit->index] = TRUE;
        }
      else
        {
          #if DEBUG
            g_debug ("r (%g) >= P (%g), not detected", r, P);
          #endif
          ;
        }
    }                           /* end of loop over units */

#if DEBUG
  g_debug ("----- EXIT handle_new_day_event (%s)", MODEL_NAME);
#endif
}



/**
 * Responds to an exam event by potentially generating a detection.
 *
 * @param self the model.
 * @param units a unit list.
 * @param event a new day event.
 * @param rng a random number generator.
 * @param queue for any new events the model creates.
 */
void
handle_exam_event (struct spreadmodel_model_t_ *self, UNT_unit_list_t * units,
                   EVT_exam_event_t * event, RAN_gen_t * rng,
                   EVT_event_queue_t * queue)
{
  local_data_t *local_data;
  param_block_t *param_block;
  UNT_unit_t *unit;
  unsigned int prod_type;
  double prob_report_from_signs;
  double P, r;

#if DEBUG
  g_debug ("----- ENTER handle_exam_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;

  /* Check whether the unit is a production type we're interested in.  If not,
   * abort. */
  prod_type = unit->production_type;
  param_block = local_data->param_block[prod_type];
  if (param_block == NULL)
    goto end;

  #if DEBUG
    g_debug ("unit \"%s\" is %s, state is %s, %s detected",
             unit->official_id,
             unit->production_type_name,
             UNT_state_name[unit->state],
             local_data->detected[unit->index] ? "already" : "not");
  #endif

  /* Check whether the unit has already been detected.  If so, abort. */
  if (local_data->detected[unit->index])
    goto end;

  /* Check whether the unit is showing clinical signs of disease. */
  if (unit->state == InfectiousClinical)
    {
      /* Compute the probability that the disease would be noticed, based on
       * clinical signs and the request multiplier. */
      prob_report_from_signs =
        REL_chart_lookup (unit->days_in_state, param_block->prob_report_vs_days_clinical);

      P = prob_report_from_signs * event->detection_multiplier;
      #if DEBUG
        g_debug ("P = %g * %g", prob_report_from_signs, event->detection_multiplier);
      #endif
      r = RAN_num (rng);
      if (r < P)
        {
          #if DEBUG
            g_debug ("r (%g) < P (%g)", r, P);
            g_debug ("unit \"%s\" detected and reported", unit->official_id);
          #endif
          /* There was no diagnostic test, so SPREADMODEL_TestUnspecified is a legitimate value here. */
          EVT_event_enqueue (queue,
                             EVT_new_detection_event (unit, event->day,
                                                      SPREADMODEL_DetectionClinicalSigns,
                                                      SPREADMODEL_TestUnspecified));
          local_data->detected[unit->index] = TRUE;
        }
      else
        {
          #if DEBUG
            g_debug ("r (%g) >= P (%g), not detected", r, P);
          #endif
          if (event->test_if_no_signs == TRUE)
            EVT_event_enqueue (queue, EVT_new_test_event (unit, event->day, event->reason));
        }
    } /* end of case where unit is Infectious Clinical */
  else
    {
      if (event->test_if_no_signs == TRUE)
        EVT_event_enqueue (queue, EVT_new_test_event (unit, event->day, event->reason));
    }

end:
#if DEBUG
  g_debug ("----- EXIT handle_exam_event (%s)", MODEL_NAME);
#endif
  return;
}



/**
 * Records the day on which the outbreak is publically announced.  This is
 * important because the probability of detection increases with community
 * awareness of an outbreak.
 *
 * @param self the model.
 * @param event a public announcement event.
 */
void
handle_public_announcement_event (struct spreadmodel_model_t_ *self,
                                  EVT_public_announcement_event_t * event)
{
  local_data_t *local_data;

#if DEBUG
  g_debug ("----- ENTER handle_public_announcement_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  if (local_data->outbreak_known == FALSE)
    {
      local_data->outbreak_known = TRUE;
      local_data->public_announcement_day = event->day;
      #if DEBUG
        g_debug ("community is now aware of outbreak, detection more likely");
      #endif
    }

#if DEBUG
  g_debug ("----- EXIT handle_public_announcement_event (%s)", MODEL_NAME);
#endif
}



/**
 * Runs this model.
 *
 * Side effects: may change the state of one or more units in list.
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
    case EVT_NewDay:
      handle_new_day_event (self, units, zones, &(event->u.new_day), rng, queue);
      break;
    case EVT_Exam:
      handle_exam_event (self, units, &(event->u.exam), rng, queue);
      break;
    case EVT_PublicAnnouncement:
      handle_public_announcement_event (self, &(event->u.public_announcement));
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
  int nprod_types, i;
  param_block_t *param_block;

#if DEBUG
  g_debug ("----- ENTER reset (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  for (i = 0; i < local_data->nunits; i++)
    local_data->detected[i] = FALSE;
  local_data->outbreak_known = FALSE;
  local_data->public_announcement_day = 0;

  nprod_types = local_data->production_types->len;
  for (i = 0; i < nprod_types; i++)
    {
      param_block = local_data->param_block[i];
      if (param_block == NULL)
        continue;

      local_data->prob_report_from_awareness[i] =
        REL_chart_lookup (0, param_block->prob_report_vs_days_since_outbreak);
    }

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
  local_data_t *local_data;
  unsigned int nprod_types, nzones, i, j;
  param_block_t *param_block;
  char *substring, *chararray;
  ZON_zone_t *zone;

  local_data = (local_data_t *) (self->model_data);
  s = g_string_new (NULL);
  g_string_printf (s, "<%s", MODEL_NAME);

  /* Add the parameter block for each production type. */
  nprod_types = local_data->production_types->len;
  nzones = ZON_zone_list_length (local_data->zones);
  for (i = 0; i < nprod_types; i++)
    {
      param_block = local_data->param_block[i];
      if (param_block == NULL)
        continue;

      g_string_append_printf (s, "\n  for %s",
                              (char *) g_ptr_array_index (local_data->production_types, i));

      substring = REL_chart_to_string (param_block->prob_report_vs_days_clinical);
      g_string_append_printf (s, "\n    prob-report-vs-days-clinical=%s", substring);
      g_free (substring);

      substring = REL_chart_to_string (param_block->prob_report_vs_days_since_outbreak);
      g_string_append_printf (s, "\n    prob-report-vs-days-since-outbreak=%s", substring);
      g_free (substring);

      for (j = 0; j < nzones; j++)
        {
          zone = ZON_zone_list_get (local_data->zones, j);
          g_string_append_printf (s, "\n    prob-multiplier for \"%s\" zone=%g",
                                  zone->name, local_data->zone_multiplier[j][i]);
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
local_free (struct spreadmodel_model_t_ *self)
{
  local_data_t *local_data;
  unsigned int nprod_types, nzones, i;
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

      REL_free_chart (param_block->prob_report_vs_days_clinical);
      REL_free_chart (param_block->prob_report_vs_days_since_outbreak);
      g_free (param_block);
    }
  g_free (local_data->param_block);

  /* Free the 2D array of zone multipliers. */
  nzones = ZON_zone_list_length (local_data->zones);
  for (i = 0; i < nzones; i++)
    g_free (local_data->zone_multiplier[i]);
  g_free (local_data->zone_multiplier);

  g_free (local_data->detected);
  g_free (local_data->prob_report_from_awareness);
  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Adds a set of parameters to a detection model.
 */
void
set_params (struct spreadmodel_model_t_ *self, PAR_parameter_t * params)
{
  local_data_t *local_data;
  param_block_t t;
  scew_element const *e;
  gboolean success;
  double zone_multiplier;
  gboolean *production_type;
  gboolean *zone;
  unsigned int nprod_types, nzones, i, j;

#if DEBUG
  g_debug ("----- ENTER set_params (%s)", MODEL_NAME);
#endif

  /* Make sure the right XML subtree was sent. */
  g_assert (strcmp (scew_element_name (params), MODEL_NAME) == 0);

  local_data = (local_data_t *) (self->model_data);

  /* Read the parameters and store them in a temporary param_block_t
   * structure. */

  e = scew_element_by_name (params, "prob-report-vs-time-clinical");
  if (e != NULL)
    {
      t.prob_report_vs_days_clinical = PAR_get_relationship_chart (e);
    }
  else
    {
      /* Default to 0 = no detection. */
      t.prob_report_vs_days_clinical = REL_new_point_chart (0);
    }

  e = scew_element_by_name (params, "prob-report-vs-time-since-outbreak");
  if (e != NULL)
    {
      t.prob_report_vs_days_since_outbreak = PAR_get_relationship_chart (e);
    }
  else
    {
      /* Default to 1 = public knowledge of outbreak has o effect. */
      t.prob_report_vs_days_since_outbreak = REL_new_point_chart (1);
    }

  e = scew_element_by_name (params, "zone-prob-multiplier");
  if (e != NULL)
    {
      zone_multiplier = PAR_get_unitless (e, &success);
      if (success == FALSE)
        {
          g_warning ("%s: setting zone multiplier to 1 (no effect)", MODEL_NAME);
          zone_multiplier = 1;
        }
      else if (zone_multiplier < 0)
        {
          g_warning ("%s: zone multiplier cannot be negative, setting to 1 (no effect)",
                     MODEL_NAME);
          zone_multiplier = 1;
        }
      else if (zone_multiplier < 1)
        {
          g_warning ("%s: zone multiplier is less than 1, will result in slower detection inside zone",
                     MODEL_NAME);
        }      
    }
  else
    {
      zone_multiplier = 1;
    }

  /* Find out which production types, or which production type-zone
   * combinations, these parameters apply to. */
  production_type =
    spreadmodel_read_prodtype_attribute (params, "production-type", local_data->production_types);
  if (scew_element_attribute_by_name (params, "zone") != NULL)
    zone = spreadmodel_read_zone_attribute (params, local_data->zones);
  else
    zone = NULL;

  /* Copy the parameters to the appropriate place. */
  nprod_types = local_data->production_types->len;
  nzones = ZON_zone_list_length (local_data->zones);
  if (zone == NULL)
    {
      /* These parameters are detection charts by production type. */

      param_block_t *param_block;

      for (i = 0; i < nprod_types; i++)
        {
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
              REL_free_chart (param_block->prob_report_vs_days_clinical);
              REL_free_chart (param_block->prob_report_vs_days_since_outbreak);
            }
          param_block->prob_report_vs_days_clinical =
            REL_clone_chart (t.prob_report_vs_days_clinical);
          param_block->prob_report_vs_days_since_outbreak =
            REL_clone_chart (t.prob_report_vs_days_since_outbreak);
        }
    }
  else
    {
      /* These parameters are the multiplier by production type-zone. */

      for (i = 0; i < nzones; i++)
        {
          if (zone[i] == FALSE)
            continue;

          for (j = 0; j < nprod_types; j++)
            {
              if (production_type[j] == FALSE)
                continue;

              #if DEBUG
                g_debug ("setting multiplier for %s in \"%s\" zone",
                         (char *) g_ptr_array_index (local_data->production_types, j),
                         ZON_zone_list_get (local_data->zones, i)->name);
              #endif
              local_data->zone_multiplier[i][j] = zone_multiplier;
            }
        }
    }

  g_free (production_type);
  if (zone != NULL)
    g_free (zone);
  REL_free_chart (t.prob_report_vs_days_clinical);
  REL_free_chart (t.prob_report_vs_days_since_outbreak);

#if DEBUG
  g_debug ("----- EXIT set_params (%s)", MODEL_NAME);
#endif

  return;
}



/**
 * Returns a new detection model.
 */
spreadmodel_model_t *
new (scew_element * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  spreadmodel_model_t *self;
  local_data_t *local_data;
  unsigned int nprod_types, nzones, i, j;

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
  self->set_params = set_params;
  self->run = run;
  self->reset = reset;
  self->is_singleton = spreadmodel_model_answer_yes;
  self->is_listening_for = spreadmodel_model_is_listening_for;
  self->has_pending_actions = spreadmodel_model_answer_no;
  self->has_pending_infections = spreadmodel_model_answer_no;
  self->to_string = to_string;
  self->printf = spreadmodel_model_printf;
  self->fprintf = spreadmodel_model_fprintf;
  self->free = local_free;

  /* local_data->param_block holds an array of parameter blocks, where each
   * block holds the parameters for one production type.  Initially, all
   * pointers are NULL.  Blocks will be created as needed in the set_params
   * function. */
  local_data->production_types = units->production_type_names;
  nprod_types = local_data->production_types->len;
  local_data->param_block = g_new0 (param_block_t *, nprod_types);

  /* local_data->zone_multiplier is a 2D array of detection multipliers.  The
   * first level of indexing is by zone (rows), then by production type
   * (columns).  The values are initialized to 1. */
  local_data->zones = zones;
  nzones = ZON_zone_list_length (zones);
  local_data->zone_multiplier = g_new (double *, nzones);

  for (i = 0; i < nzones; i++)
    {
      local_data->zone_multiplier[i] = g_new (double, nprod_types);
      for (j = 0; j < nprod_types; j++)
        local_data->zone_multiplier[i][j] = 1.0;
    }

  /* Initialize the array of detected flags (one per unit) to all FALSE. */
  local_data->nunits = UNT_unit_list_length (units);
  local_data->detected = g_new0 (gboolean, local_data->nunits);
  /* No outbreak has been announced yet. */
  local_data->outbreak_known = FALSE;
  local_data->public_announcement_day = 0;

  /* Allocate an array for the probability of reporting due to community
   * awareness of an outbreak.  It will be initialized in the reset
   * function. */
  local_data->prob_report_from_awareness = g_new (double, nprod_types);

  /* Send the XML subtree to the init function to read the production type
   * combination specific parameters. */
  self->set_params (self, params);

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file detection_model.c */
