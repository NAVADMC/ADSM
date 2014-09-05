/** @file detection_monitor.c
 * Records the day on which the first detection occurred.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @version 0.1
 * @date June 2004
 *
 * Copyright &copy; University of Guelph, 2004-2009
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
#define new detection_monitor_new
#define run detection_monitor_run
#define local_free detection_monitor_free
#define handle_before_each_simulation_event detection_monitor_handle_before_each_simulation_event
#define handle_new_day_event detection_monitor_handle_new_day_event
#define handle_detection_event detection_monitor_handle_detection_event

#include "module.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#include "detection_monitor.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "detection-monitor"



/**
 * A struct that records how many times a unit has been detected on one day,
 * and holds the means of detection that is currently recorded for that unit.
 */
typedef struct
{
  unsigned int count;
  ADSM_detection_reason means;
}
count_and_means_t;



/* Specialized information for this model. */
typedef struct
{
  GPtrArray *production_types;
  RPT_reporting_t   *detection_occurred;
  RPT_reporting_t   *first_detection;
  RPT_reporting_t  **first_detection_by_means;
  RPT_reporting_t  **first_detection_by_prodtype;
  RPT_reporting_t ***first_detection_by_means_and_prodtype;
  RPT_reporting_t   *last_detection;
  RPT_reporting_t  **last_detection_by_means;
  RPT_reporting_t  **last_detection_by_prodtype;
  RPT_reporting_t ***last_detection_by_means_and_prodtype;
  RPT_reporting_t   *nunits_detected;
  RPT_reporting_t  **nunits_detected_by_means;
  RPT_reporting_t  **nunits_detected_by_prodtype;
  RPT_reporting_t ***nunits_detected_by_means_and_prodtype;
  RPT_reporting_t   *nanimals_detected;
  RPT_reporting_t  **nanimals_detected_by_means;
  RPT_reporting_t  **nanimals_detected_by_prodtype;
  RPT_reporting_t ***nanimals_detected_by_means_and_prodtype;
  RPT_reporting_t   *cumul_nunits_detected;
  RPT_reporting_t  **cumul_nunits_detected_by_means;
  RPT_reporting_t  **cumul_nunits_detected_by_prodtype;
  RPT_reporting_t ***cumul_nunits_detected_by_means_and_prodtype;
  RPT_reporting_t   *cumul_nunits_detected_uniq;
  RPT_reporting_t   *cumul_nanimals_detected;
  RPT_reporting_t  **cumul_nanimals_detected_by_means;
  RPT_reporting_t  **cumul_nanimals_detected_by_prodtype;
  RPT_reporting_t ***cumul_nanimals_detected_by_means_and_prodtype;
  GPtrArray *daily_outputs; /**< Daily outputs, in a list to make it easy to
    zero them all at once. */
  GPtrArray *cumul_outputs; /**< Cumulative outputs, is a list to make it easy
    to zero them all at once. */
  GPtrArray *null_outputs; /**< Outputs that start out null, in a list to make
    it easy set them null all at once. */
  GHashTable *detected; /**< A table for tracking detections of unique units.
    If a unit has been detected, it will be in the.  The key is the unit
    (UNT_unit_t *), and the associated value is irrelevant. */
  GHashTable *detected_today; /**< A table for tracking multiple detections of
    a unit on one day.  If a unit has been detected today, it will be in the
    table.  The key is the unit (UNT_unit_t *), and the associated value is a
    pointer to a count_and_means_t struct. */
  RPT_reporting_t  **first_detection_by_means_yesterday;
  RPT_reporting_t ***first_detection_by_means_and_prodtype_yesterday;
  RPT_reporting_t  **last_detection_by_means_yesterday;
  RPT_reporting_t ***last_detection_by_means_and_prodtype_yesterday;
}
local_data_t;



/**
 * Before each simulation, zero the cumulative counts of detections.
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
  g_ptr_array_foreach (local_data->cumul_outputs, RPT_reporting_zero_as_GFunc, NULL);
  g_ptr_array_foreach (local_data->null_outputs, RPT_reporting_set_null_as_GFunc, NULL);
  g_hash_table_remove_all (local_data->detected);

  #if DEBUG
    g_debug ("----- EXIT handle_before_each_simulation_event (%s)", MODEL_NAME);
  #endif

  return;
}



/**
 * On each new day, zero the daily counts of detections.
 *
 * @param self the module.
 */
void
handle_new_day_event (struct adsm_module_t_ *self)
{
  local_data_t *local_data;
  ADSM_detection_reason means;
  guint nprodtypes;
  UNT_production_type_t prodtype;

#if DEBUG
  g_debug ("----- ENTER handle_new_day_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* Zero the daily counts. */
  g_ptr_array_foreach (local_data->daily_outputs, RPT_reporting_zero_as_GFunc, NULL);

  /* Empty the table that tracks multiple detections of a unit on one day. */
  g_hash_table_remove_all (local_data->detected_today);

  /* Make a backup copy of the first & last days of detection recorded so far.
   * We need this in case we "change our mind" about the means of detection for
   * a particular unit. */
  nprodtypes = local_data->production_types->len;
  for (means = 0; means < ADSM_NDETECTION_REASONS; means++)
    {
      RPT_free_reporting (local_data->first_detection_by_means_yesterday[means]);
      local_data->first_detection_by_means_yesterday[means] =
        RPT_clone_reporting (local_data->first_detection_by_means[means]);
      RPT_free_reporting (local_data->last_detection_by_means_yesterday[means]);
      local_data->last_detection_by_means_yesterday[means] =
        RPT_clone_reporting (local_data->last_detection_by_means[means]);
      for (prodtype = 0; prodtype < nprodtypes; prodtype++)
        {
          RPT_free_reporting (local_data->first_detection_by_means_and_prodtype_yesterday[means][prodtype]);
          local_data->first_detection_by_means_and_prodtype_yesterday[means][prodtype] =
            RPT_clone_reporting (local_data->first_detection_by_means_and_prodtype[means][prodtype]);
          RPT_free_reporting (local_data->last_detection_by_means_and_prodtype_yesterday[means][prodtype]);
          local_data->last_detection_by_means_and_prodtype_yesterday[means][prodtype] =
            RPT_clone_reporting (local_data->last_detection_by_means_and_prodtype[means][prodtype]);
        }
    }

#if DEBUG
  g_debug ("----- EXIT handle_new_day_event (%s)", MODEL_NAME);
#endif
}



/**
 * Records a detection.  Updates the day of first detection and day of last
 * detection, if needed.
 *
 * @param self the model.
 * @param event a detection event.
 * @param rng a random number generator.
 */
void
handle_detection_event (struct adsm_module_t_ *self, EVT_detection_event_t * event,
                        RAN_gen_t * rng)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  UNT_production_type_t prodtype;
  double nanimals;
  ADSM_detection_reason means;
  UNT_detect_t detection;
  gpointer p;
  count_and_means_t *previous_detection;

#if DEBUG
  g_debug ("----- ENTER handle_detection_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;
  prodtype = unit->production_type;
  nanimals = (double)(unit->size);
  means = event->means;

  detection.unit_index = unit->index;
  detection.reason = means;
  detection.test_result = event->test_result;
  
#ifdef USE_SC_GUILIB
  sc_detect_unit( event->day, unit, detection );
#else  
  if (NULL != adsm_detect_unit)
    {
      adsm_detect_unit (detection);
    }
#endif  

  /* A unit can be detected multiple times on one day, by different means of
   * detection.  Handle the outputs that are not broken down by means of
   * detection first. */
  if (local_data->first_detection->is_null)
    {
      RPT_reporting_set_integer (local_data->first_detection, event->day);
      RPT_reporting_set_integer (local_data->detection_occurred, 1);
    } 
  if (local_data->first_detection_by_prodtype[prodtype]->is_null)
    RPT_reporting_set_integer (local_data->first_detection_by_prodtype[prodtype], event->day);
  RPT_reporting_set_integer (local_data->last_detection, event->day);
  RPT_reporting_set_integer (local_data->last_detection_by_prodtype[prodtype], event->day);  

  p = g_hash_table_lookup (local_data->detected_today, unit);
  if (p == NULL)
    {
      /* This unit has not been detected already today. */
      if (local_data->first_detection_by_means[means]->is_null)
        RPT_reporting_set_integer (local_data->first_detection_by_means[means], event->day);
      if (local_data->first_detection_by_means_and_prodtype[means][prodtype]->is_null)
        RPT_reporting_set_integer (local_data->first_detection_by_means_and_prodtype[means][prodtype], event->day);
      RPT_reporting_set_integer (local_data->last_detection_by_means[means], event->day);
      RPT_reporting_set_integer (local_data->last_detection_by_means_and_prodtype[means][prodtype], event->day);
      RPT_reporting_add_integer (local_data->nunits_detected, 1);
      RPT_reporting_add_integer (local_data->nunits_detected_by_means[means], 1);
      RPT_reporting_add_integer (local_data->nunits_detected_by_prodtype[prodtype], 1);
      RPT_reporting_add_integer (local_data->nunits_detected_by_means_and_prodtype[means][prodtype], 1);
      RPT_reporting_add_real (local_data->nanimals_detected, nanimals);
      RPT_reporting_add_real (local_data->nanimals_detected_by_means[means], nanimals);
      RPT_reporting_add_real (local_data->nanimals_detected_by_prodtype[prodtype], nanimals);
      RPT_reporting_add_real (local_data->nanimals_detected_by_means_and_prodtype[means][prodtype], nanimals);
      RPT_reporting_add_integer (local_data->cumul_nunits_detected, 1);
      RPT_reporting_add_integer (local_data->cumul_nunits_detected_by_means[means], 1);
      RPT_reporting_add_integer (local_data->cumul_nunits_detected_by_prodtype[prodtype], 1);
      RPT_reporting_add_integer (local_data->cumul_nunits_detected_by_means_and_prodtype[means][prodtype], 1);
      RPT_reporting_add_real (local_data->cumul_nanimals_detected, nanimals);
      RPT_reporting_add_real (local_data->cumul_nanimals_detected_by_means[means], nanimals);
      RPT_reporting_add_real (local_data->cumul_nanimals_detected_by_prodtype[prodtype], nanimals);
      RPT_reporting_add_real (local_data->cumul_nanimals_detected_by_means_and_prodtype[means][prodtype], nanimals);

      previous_detection = g_new (count_and_means_t, 1);
      previous_detection->count = 1;
      previous_detection->means = means;
      g_hash_table_insert (local_data->detected_today, unit, previous_detection);
    } /* end of case where the unit has not been detected already today */
  else
    {
      /* This unit has been detected already today. */
      previous_detection = (count_and_means_t *) p;
      if (previous_detection->means != means)
        {
          /* This detection is by a different means than the means currently
           * recorded for this unit.  Decide whether to "change our mind" about
           * what means of detection to report for this unit. */
          double P, r;

          P = 1.0 / (previous_detection->count + 1);
          r = RAN_num (rng);
          if (r < P)
            {
#if DEBUG
              g_debug ("r (%g) < P (%g), replacing recorded means \"%s\" with \"%s\"",
                       r, P,
                       ADSM_detection_reason_abbrev[previous_detection->means],
                       ADSM_detection_reason_abbrev[means]);
#endif
              /* We have changed our mind about what means of detection to
               * report for this unit.  Decrement the count of detections by
               * the old means. */
              RPT_reporting_sub_integer (local_data->nunits_detected_by_means[previous_detection->means], 1);
              RPT_reporting_sub_real (local_data->nanimals_detected_by_means[previous_detection->means], nanimals);
              RPT_reporting_sub_integer (local_data->cumul_nunits_detected_by_means[previous_detection->means], 1);
              RPT_reporting_sub_real (local_data->cumul_nanimals_detected_by_means[previous_detection->means], nanimals);
              if (RPT_reporting_get_integer (local_data->nunits_detected_by_means[previous_detection->means]) == 0)
                {
                  /* We counted detections by a particular means today, but then
                   * we changed our mind and un-counted them all.  Restore
                   * yesterday's values for first & last detection by that means. */
                  if (local_data->first_detection_by_means_yesterday[previous_detection->means]->is_null)
                    RPT_reporting_set_null (local_data->first_detection_by_means[previous_detection->means]);
                  else
                    RPT_reporting_set_integer (local_data->first_detection_by_means[previous_detection->means],
                                                RPT_reporting_get_integer (local_data->first_detection_by_means_yesterday[previous_detection->means]));
                  if (local_data->last_detection_by_means_yesterday[previous_detection->means]->is_null)
                    RPT_reporting_set_null (local_data->last_detection_by_means[previous_detection->means]);
                  else
                    RPT_reporting_set_integer (local_data->last_detection_by_means[previous_detection->means],
                                                RPT_reporting_get_integer (local_data->last_detection_by_means_yesterday[previous_detection->means]));
                }
              RPT_reporting_sub_integer (local_data->nunits_detected_by_means_and_prodtype[previous_detection->means][prodtype], 1);
              RPT_reporting_sub_real (local_data->nanimals_detected_by_means_and_prodtype[previous_detection->means][prodtype], nanimals);
              RPT_reporting_sub_integer (local_data->cumul_nunits_detected_by_means_and_prodtype[previous_detection->means][prodtype], 1);
              RPT_reporting_sub_real (local_data->cumul_nanimals_detected_by_means_and_prodtype[previous_detection->means][prodtype], nanimals);
              if (RPT_reporting_get_integer (local_data->nunits_detected_by_means_and_prodtype[previous_detection->means][prodtype]) == 0)
                {
                  /* We counted detections by a particular combination of means
                   * and production type today, but then we changed our mind
                   * and un-counted them all.  Restore yesterday's values for
                   * first & last detection by that combination of means and
                   * production type. */
                  if (local_data->first_detection_by_means_and_prodtype_yesterday[previous_detection->means][prodtype]->is_null)
                    RPT_reporting_set_null (local_data->first_detection_by_means_and_prodtype[previous_detection->means][prodtype]);
                  else
                    RPT_reporting_set_integer (local_data->first_detection_by_means_and_prodtype[previous_detection->means][prodtype],
                                               RPT_reporting_get_integer (local_data->first_detection_by_means_and_prodtype_yesterday[previous_detection->means][prodtype]));
                  if (local_data->last_detection_by_means_and_prodtype_yesterday[previous_detection->means][prodtype]->is_null)
                    RPT_reporting_set_null (local_data->last_detection_by_means_and_prodtype[previous_detection->means][prodtype]);
                  else
                    RPT_reporting_set_integer (local_data->last_detection_by_means_and_prodtype[previous_detection->means][prodtype],
                                               RPT_reporting_get_integer (local_data->last_detection_by_means_and_prodtype_yesterday[previous_detection->means][prodtype]));
                }

              /* Increment the count of detections by the new means. */
              if (local_data->first_detection_by_means[means]->is_null)
                RPT_reporting_set_integer (local_data->first_detection_by_means[means], event->day);
              if (local_data->first_detection_by_means_and_prodtype[means][prodtype]->is_null)
                RPT_reporting_set_integer (local_data->first_detection_by_means_and_prodtype[means][prodtype], event->day);
              RPT_reporting_set_integer (local_data->last_detection_by_means[means], event->day);
              RPT_reporting_set_integer (local_data->last_detection_by_means_and_prodtype[means][prodtype], event->day);
              RPT_reporting_add_integer (local_data->nunits_detected_by_means[means], 1);
              RPT_reporting_add_integer (local_data->cumul_nunits_detected_by_means[means], 1);
              RPT_reporting_add_integer (local_data->nunits_detected_by_means_and_prodtype[means][prodtype], 1);
              RPT_reporting_add_integer (local_data->cumul_nunits_detected_by_means_and_prodtype[means][prodtype], 1);
              RPT_reporting_add_real (local_data->nanimals_detected_by_means[means], nanimals);
              RPT_reporting_add_real (local_data->cumul_nanimals_detected_by_means[means], nanimals);
              RPT_reporting_add_real (local_data->nanimals_detected_by_means_and_prodtype[means][prodtype], nanimals);
              RPT_reporting_add_real (local_data->cumul_nanimals_detected_by_means_and_prodtype[means][prodtype], nanimals);
            } /* end of case where previously recorded means of detection is replaced */
          else
            {
#if DEBUG
              g_debug ("r (%g) >= P (%g), not replacing recorded means \"%s\" with \"%s\"",
                       r, P,
                       ADSM_detection_reason_abbrev[previous_detection->means],
                       ADSM_detection_reason_abbrev[means]);
#endif
              ;
            } /* end of case where previously recorded means of detection is not replaced */
        } /* end of case where previously recorded means of detection does not match the current detection event */
      previous_detection->count += 1;
    } /* end of case where the unit has been detected already today */

  /* Handle counts of unique detected units. */
  p = g_hash_table_lookup (local_data->detected, unit);
  if (p == NULL)
    {
      /* This unit has not been detected before in this simulation. */
      g_hash_table_insert (local_data->detected, unit, GINT_TO_POINTER(1));
      RPT_reporting_add_integer (local_data->cumul_nunits_detected_uniq, 1);
    }

#if DEBUG
  g_debug ("----- EXIT handle_detection_event (%s)", MODEL_NAME);
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
      handle_new_day_event (self);
      break;
    case EVT_Detection:
      handle_detection_event (self, &(event->u.detection), rng);
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
  ADSM_detection_reason means;
  guint nprodtypes;
  UNT_production_type_t prodtype;

#if DEBUG
  g_debug ("----- ENTER free (%s)", MODEL_NAME);
#endif

  /* Free the dynamically-allocated parts. */
  local_data = (local_data_t *) (self->model_data);

  g_ptr_array_free (local_data->daily_outputs, /* free_seg = */ TRUE);
  g_ptr_array_free (local_data->cumul_outputs, /* free_seg = */ TRUE);
  g_ptr_array_free (local_data->null_outputs, /* free_seg = */ TRUE);
  g_hash_table_destroy (local_data->detected);
  g_hash_table_destroy (local_data->detected_today);
  nprodtypes = local_data->production_types->len;
  for (means = 0; means < ADSM_NDETECTION_REASONS; means++)
    {
      RPT_free_reporting (local_data->first_detection_by_means_yesterday[means]);
      RPT_free_reporting (local_data->last_detection_by_means_yesterday[means]);
      for (prodtype = 0; prodtype < nprodtypes; prodtype++)
        {
          RPT_free_reporting (local_data->first_detection_by_means_and_prodtype_yesterday[means][prodtype]);
          RPT_free_reporting (local_data->last_detection_by_means_and_prodtype_yesterday[means][prodtype]);
        }
    }

  g_free (local_data);
  g_ptr_array_free (self->outputs, /* free_seg = */ TRUE); /* also frees most of the output variables */
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Returns a new detection monitor.
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
    EVT_Detection,
    0
  };
  guint nprodtypes;
  ADSM_detection_reason means;

#if DEBUG
  g_debug ("----- ENTER new (%s)", MODEL_NAME);
#endif

  self = g_new (adsm_module_t, 1);
  local_data = g_new (local_data_t, 1);

  self->name = MODEL_NAME;
  self->events_listened_for = adsm_setup_events_listened_for (events_listened_for);
  self->outputs = g_ptr_array_new();
  self->model_data = local_data;
  self->run = run;
  self->is_listening_for = adsm_model_is_listening_for;
  self->has_pending_actions = adsm_model_answer_no;
  self->has_pending_infections = adsm_model_answer_no;
  self->to_string = adsm_module_to_string_default;
  self->printf = adsm_model_printf;
  self->fprintf = adsm_model_fprintf;
  self->free = local_free;

  local_data->daily_outputs = g_ptr_array_new();
  local_data->cumul_outputs = g_ptr_array_new();
  local_data->null_outputs = g_ptr_array_new();
  local_data->production_types = units->production_type_names;
  nprodtypes = local_data->production_types->len;
  {
    RPT_bulk_create_t outputs[] = {
      { &local_data->detection_occurred, "detOccurred", RPT_integer,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->first_detection, "firstDetection", RPT_integer,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->null_outputs },

      { &local_data->first_detection_by_means, "firstDetection%s", RPT_integer,
        RPT_CharArray, ADSM_detection_reason_abbrev, ADSM_NDETECTION_REASONS,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->null_outputs },

      { &local_data->first_detection_by_prodtype, "firstDetection%s", RPT_integer,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->null_outputs },

      { &local_data->first_detection_by_means_and_prodtype, "firstDetection%s%s", RPT_integer,
        RPT_CharArray, ADSM_detection_reason_abbrev, ADSM_NDETECTION_REASONS,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        self->outputs, local_data->null_outputs },

      { &local_data->last_detection, "lastDetection", RPT_integer,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->null_outputs },

      { &local_data->last_detection_by_means, "lastDetection%s", RPT_integer,
        RPT_CharArray, ADSM_detection_reason_abbrev, ADSM_NDETECTION_REASONS,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->null_outputs },

      { &local_data->last_detection_by_prodtype, "lastDetection%s", RPT_integer,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->null_outputs },

      { &local_data->last_detection_by_means_and_prodtype, "lastDetection%s%s", RPT_integer,
        RPT_CharArray, ADSM_detection_reason_abbrev, ADSM_NDETECTION_REASONS,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        self->outputs, local_data->null_outputs },

      { &local_data->nunits_detected, "detnUAll", RPT_integer,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->nunits_detected_by_means, "detnU%s", RPT_integer,
        RPT_CharArray, ADSM_detection_reason_abbrev, ADSM_NDETECTION_REASONS,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->nunits_detected_by_prodtype, "detnU%s", RPT_integer,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->nunits_detected_by_means_and_prodtype, "detnU%s%s", RPT_integer,
        RPT_CharArray, ADSM_detection_reason_abbrev, ADSM_NDETECTION_REASONS,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        self->outputs, local_data->daily_outputs },

      { &local_data->cumul_nunits_detected, "detcUAll", RPT_integer,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nunits_detected_by_means, "detcU%s", RPT_integer,
        RPT_CharArray, ADSM_detection_reason_abbrev, ADSM_NDETECTION_REASONS,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nunits_detected_by_prodtype, "detcU%s", RPT_integer,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nunits_detected_by_means_and_prodtype, "detcU%s%s", RPT_integer,
        RPT_CharArray, ADSM_detection_reason_abbrev, ADSM_NDETECTION_REASONS,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nunits_detected_uniq, "detcUqAll", RPT_integer,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->nanimals_detected, "detnAAll", RPT_real,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->nanimals_detected_by_means, "detnA%s", RPT_real,
        RPT_CharArray, ADSM_detection_reason_abbrev, ADSM_NDETECTION_REASONS,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->nanimals_detected_by_prodtype, "detnA%s", RPT_real,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->nanimals_detected_by_means_and_prodtype, "detnA%s%s", RPT_real,
        RPT_CharArray, ADSM_detection_reason_abbrev, ADSM_NDETECTION_REASONS,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        self->outputs, local_data->daily_outputs },

      { &local_data->cumul_nanimals_detected, "detcAAll", RPT_real,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nanimals_detected_by_means, "detcA%s", RPT_real,
        RPT_CharArray, ADSM_detection_reason_abbrev, ADSM_NDETECTION_REASONS,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nanimals_detected_by_prodtype, "detcA%s", RPT_real,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nanimals_detected_by_means_and_prodtype, "detcA%s%s", RPT_real,
        RPT_CharArray, ADSM_detection_reason_abbrev, ADSM_NDETECTION_REASONS,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        self->outputs, local_data->cumul_outputs },

      { NULL }
    };  
    RPT_bulk_create (outputs);
  }

  /* Dispose of a few output variables we aren't interested in, to keep the
   * output neater. */
  g_ptr_array_remove_fast (self->outputs, local_data->first_detection_by_means[ADSM_DetectionReasonUnspecified] );
  g_ptr_array_remove_fast (self->outputs, local_data->last_detection_by_means[ADSM_DetectionReasonUnspecified] );
  g_ptr_array_remove_fast (self->outputs, local_data->nunits_detected_by_means[ADSM_DetectionReasonUnspecified] );
  g_ptr_array_remove_fast (self->outputs, local_data->cumul_nunits_detected_by_means[ADSM_DetectionReasonUnspecified] );
  g_ptr_array_remove_fast (self->outputs, local_data->nanimals_detected_by_means[ADSM_DetectionReasonUnspecified] );
  g_ptr_array_remove_fast (self->outputs, local_data->cumul_nanimals_detected_by_means[ADSM_DetectionReasonUnspecified] );
  for (UNT_production_type_t prodtype = 0; prodtype < nprodtypes; prodtype++)
    {
      g_ptr_array_remove_fast (self->outputs, local_data->first_detection_by_means_and_prodtype[ADSM_DetectionReasonUnspecified][prodtype] );
      g_ptr_array_remove_fast (self->outputs, local_data->last_detection_by_means_and_prodtype[ADSM_DetectionReasonUnspecified][prodtype] );
      g_ptr_array_remove_fast (self->outputs, local_data->nunits_detected_by_means_and_prodtype[ADSM_DetectionReasonUnspecified][prodtype] );
      g_ptr_array_remove_fast (self->outputs, local_data->cumul_nunits_detected_by_means_and_prodtype[ADSM_DetectionReasonUnspecified][prodtype] );
      g_ptr_array_remove_fast (self->outputs, local_data->nanimals_detected_by_means_and_prodtype[ADSM_DetectionReasonUnspecified][prodtype] );
      g_ptr_array_remove_fast (self->outputs, local_data->cumul_nanimals_detected_by_means_and_prodtype[ADSM_DetectionReasonUnspecified][prodtype] );
    }

  /* Initialize a table to track detections of unique units. */
  local_data->detected = g_hash_table_new (g_direct_hash, g_direct_equal);

  /* Initialize a table to track multiple detections of a unit on one day. */
  local_data->detected_today = g_hash_table_new_full (g_direct_hash, g_direct_equal, NULL, g_free);

  /* These variables hold a backup copy of the first & last days of detection
   * recorded so far.  They are needed in case we "change our mind" about the
   * means of detection for a particular unit. */
  local_data->first_detection_by_means_yesterday = g_new0 (RPT_reporting_t *, ADSM_NDETECTION_REASONS);
  local_data->last_detection_by_means_yesterday = g_new0 (RPT_reporting_t *, ADSM_NDETECTION_REASONS);
  local_data->first_detection_by_means_and_prodtype_yesterday = g_new (RPT_reporting_t **, ADSM_NDETECTION_REASONS);
  local_data->last_detection_by_means_and_prodtype_yesterday = g_new (RPT_reporting_t **, ADSM_NDETECTION_REASONS);
  for (means = 0; means < ADSM_NDETECTION_REASONS; means++)
    {
      local_data->first_detection_by_means_and_prodtype_yesterday[means] = g_new0 (RPT_reporting_t *, nprodtypes);
      local_data->last_detection_by_means_and_prodtype_yesterday[means] = g_new0 (RPT_reporting_t *, nprodtypes);
    }

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file detection_monitor.c */
