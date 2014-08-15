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
#define run detection_model_run
#define reset detection_model_reset
#define events_listened_for detection_model_events_listened_for
#define to_string detection_model_to_string
#define local_free detection_model_free
#define handle_new_day_event detection_model_handle_new_day_event
#define handle_exam_event detection_model_handle_exam_event
#define handle_public_announcement_event detection_model_handle_public_announcement_event
#define handle_detection_event detection_model_handle_detection_event

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



#define NEVENTS_LISTENED_FOR 4
EVT_event_type_t events_listened_for[] = {
  EVT_NewDay, EVT_PublicAnnouncement, EVT_Exam, EVT_Detection };



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
  GHashTable *detected;
  double *prob_report_from_awareness; /**< An array with the probability of
    reporting due to one value per production type.  The array is initialized
    in the reset function, and the values are re-calculated each day once an
    outbreak is known. */
  sqlite3 *db; /* Temporarily stash a pointer to the parameters database here
    so that it will be available to the set_params function. */
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
handle_new_day_event (struct adsm_module_t_ *self, UNT_unit_list_t * units,
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
                 UNT_state_name[unit->state], g_hash_table_lookup(local_data->detected, unit) ? "already" : "not");
      #endif
      /* Check whether the unit has already been detected.  If so, go on to the
       * next unit. */
      if (g_hash_table_lookup(local_data->detected, unit))
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
          /* There was no diagnostic test, so ADSM_TestUnspecified is a legitimate value here. */
          EVT_event_enqueue (queue,
                             EVT_new_detection_event (unit, event->day,
                                                      ADSM_DetectionClinicalSigns,
                                                      ADSM_TestUnspecified));
          g_hash_table_insert (local_data->detected, unit, GINT_TO_POINTER(1));
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
handle_exam_event (struct adsm_module_t_ *self, UNT_unit_list_t * units,
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
             g_hash_table_lookup (local_data->detected, unit) ? "already" : "not");
  #endif

  /* Check whether the unit has already been detected.  If so, abort. */
  if (g_hash_table_lookup (local_data->detected, unit))
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
          /* There was no diagnostic test, so ADSM_TestUnspecified is a legitimate value here. */
          EVT_event_enqueue (queue,
                             EVT_new_detection_event (unit, event->day,
                                                      ADSM_DetectionClinicalSigns,
                                                      ADSM_TestUnspecified));
          g_hash_table_insert (local_data->detected, unit, GINT_TO_POINTER(1));
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
handle_public_announcement_event (struct adsm_module_t_ *self,
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
 * Other modules may be capable of producing detection events (for example, the
 * test module). If they do, record the detection so that this module does not
 * issue duplicates on subsequent days.
 *
 * @param self this module.
 * @param event a detection event.
 */
void
handle_detection_event (struct adsm_module_t_ *self,
                        EVT_detection_event_t * event)
{
  local_data_t *local_data;

  #if DEBUG
    g_debug ("----- ENTER handle_detection_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);
  g_hash_table_insert (local_data->detected, event->unit, GINT_TO_POINTER(1));

  #if DEBUG
    g_debug ("----- EXIT handle_detection_event (%s)", MODEL_NAME);
  #endif

  return;
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
run (struct adsm_module_t_ *self, UNT_unit_list_t * units, ZON_zone_list_t * zones,
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
    case EVT_Detection:
      handle_detection_event (self, &(event->u.detection));
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
reset (struct adsm_module_t_ *self)
{
  local_data_t *local_data;
  int nprod_types, i;
  param_block_t *param_block;

#if DEBUG
  g_debug ("----- ENTER reset (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  g_hash_table_remove_all (local_data->detected);
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
to_string (struct adsm_module_t_ *self)
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
local_free (struct adsm_module_t_ *self)
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

  g_hash_table_destroy (local_data->detected);
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
  sqlite3 *params;
  guint production_type;
  param_block_t *p;
  guint rel_id;

#if DEBUG
  g_debug ("----- ENTER set_params (%s)", MODEL_NAME);
#endif

  self = (adsm_module_t *)data;
  local_data = (local_data_t *) (self->model_data);
  params = local_data->db;

  g_assert (ncols == 3);

  /* Find out which production type these parameters apply to. */
  production_type =
    adsm_read_prodtype (value[0], local_data->production_types);

  /* Check that we are not overwriting an existing parameter block (that would
   * indicate a bug). */
  g_assert (local_data->param_block[production_type] == NULL);

  /* Create a new parameter block. */
  p = g_new (param_block_t, 1);
  local_data->param_block[production_type] = p;

  /* Read the parameters. */
  errno = 0;
  rel_id = strtol (value[1], NULL, /* base */ 10);
  g_assert (errno != ERANGE && errno != EINVAL);  
  p->prob_report_vs_days_clinical = PAR_get_relchart (params, rel_id);

  errno = 0;
  rel_id = strtol (value[2], NULL, /* base */ 10);
  g_assert (errno != ERANGE && errno != EINVAL);  
  p->prob_report_vs_days_since_outbreak = PAR_get_relchart (params, rel_id);

#if DEBUG
  g_debug ("----- EXIT set_params (%s)", MODEL_NAME);
#endif

  return 0;
}



/**
 * Adds a set of zone/production type combination specific parameters to a
 * detection model.
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
  guint zone, production_type;
  double multiplier;

  #if DEBUG
    g_debug ("----- ENTER set_zone_params (%s)", MODEL_NAME);
  #endif

  self = (adsm_module_t *)data;
  local_data = (local_data_t *) (self->model_data);

  g_assert (ncols == 3);

  /* Find out which zone/production type combination these parameters apply
   * to. */
  zone = adsm_read_zone (value[0], local_data->zones);
  production_type = adsm_read_prodtype (value[1], local_data->production_types);

  /* Read the parameter. */
  errno = 0;
  multiplier = strtod (value[2], NULL);
  g_assert (errno != ERANGE);
  /* The zone multiplier cannot be negative. */
  if (multiplier < 0)
    {
      g_error ("%s: zone multiplier cannot be negative", MODEL_NAME);
    }
  /* The zone multiplier is allowed to be less than 1, but this may not be what
   * the modeler intended. */
  if (multiplier < 1)
    {
      g_warning ("%s: zone multiplier is less than 1, will result in slower detection inside zone",
                 MODEL_NAME);
    }

  local_data->zone_multiplier[zone][production_type] = multiplier;

  #if DEBUG
    g_debug ("----- EXIT set_zone_params (%s)", MODEL_NAME);
  #endif

  return 0;
}



/**
 * Returns a new detection model.
 */
adsm_module_t *
new (sqlite3 * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  adsm_module_t *self;
  local_data_t *local_data;
  unsigned int nprod_types, nzones, i, j;
  char *sqlerr;

#if DEBUG
  g_debug ("----- ENTER new (%s)", MODEL_NAME);
#endif

  self = g_new (adsm_module_t, 1);
  local_data = g_new (local_data_t, 1);

  self->name = MODEL_NAME;
  self->events_listened_for = events_listened_for;
  self->nevents_listened_for = NEVENTS_LISTENED_FOR;
  self->outputs = g_ptr_array_new ();
  self->model_data = local_data;
  self->run = run;
  self->reset = reset;
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

  /* Initialize the set of detected units. */
  local_data->detected = g_hash_table_new (NULL, NULL);
  /* No outbreak has been announced yet. */
  local_data->outbreak_known = FALSE;
  local_data->public_announcement_day = 0;

  /* Allocate an array for the probability of reporting due to community
   * awareness of an outbreak.  It will be initialized in the reset
   * function. */
  local_data->prob_report_from_awareness = g_new (double, nprod_types);

  /* Call the set_params function to read the production type specific
   * parameters. */
  local_data->db = params;
  sqlite3_exec (params,
                "SELECT prodtype.name,detection_probability_for_observed_time_in_clinical_id,detection_probability_report_vs_first_detection_id FROM ScenarioCreator_productiontype prodtype,ScenarioCreator_controlprotocol protocol,ScenarioCreator_protocolassignment xref WHERE prodtype.id=xref.production_type_id AND xref.control_protocol_id=protocol.id AND use_detection=1",
                set_params, self, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }
  local_data->db = NULL;

  /* Call the set_zone_params function to read the zone/production type
   * combination specific parameters. */
  sqlite3_exec (params,
                "SELECT zone.name,prodtype.name,zone_detection_multiplier "
                "FROM ScenarioCreator_zone zone,ScenarioCreator_productiontype prodtype,ScenarioCreator_zoneeffectassignment pairing,ScenarioCreator_zoneeffect effect "
                "WHERE zone.id=pairing.zone_id "
                "AND prodtype.id=pairing.production_type_id "
                "AND effect.id=pairing.effect_id "
                "AND zone_detection_multiplier IS NOT NULL",
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

/* end of file detection_model.c */
