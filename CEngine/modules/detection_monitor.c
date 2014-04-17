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
#define reset detection_monitor_reset
#define events_listened_for detection_monitor_events_listened_for
#define local_free detection_monitor_free
#define handle_before_any_simulations_event detection_monitor_handle_before_any_simulations_event
#define handle_new_day_event detection_monitor_handle_new_day_event
#define handle_detection_event detection_monitor_handle_detection_event

#include "module.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#include "detection_monitor.h"

#include "spreadmodel.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "detection-monitor"



#define NEVENTS_LISTENED_FOR 3
EVT_event_type_t events_listened_for[] =
  { EVT_BeforeAnySimulations, EVT_NewDay, EVT_Detection };



/**
 * A struct that records how many times a unit has been detected on one day,
 * and holds the means of detection that is currently recorded for that unit.
 */
typedef struct
{
  unsigned int count;
  const char *means;
}
count_and_means_t;



/* Specialized information for this model. */
typedef struct
{
  GPtrArray *production_types;
  RPT_reporting_t *detection_occurred;
  RPT_reporting_t *first_detection;
  RPT_reporting_t *first_detection_by_means;
  RPT_reporting_t *first_detection_by_prodtype;
  RPT_reporting_t *first_detection_by_means_and_prodtype;
  RPT_reporting_t *last_detection;
  RPT_reporting_t *last_detection_by_means;
  RPT_reporting_t *last_detection_by_prodtype;
  RPT_reporting_t *last_detection_by_means_and_prodtype;
  RPT_reporting_t *nunits_detected;
  RPT_reporting_t *nunits_detected_by_means;
  RPT_reporting_t *nunits_detected_by_prodtype;
  RPT_reporting_t *nunits_detected_by_means_and_prodtype;
  RPT_reporting_t *nanimals_detected;
  RPT_reporting_t *nanimals_detected_by_means;
  RPT_reporting_t *nanimals_detected_by_prodtype;
  RPT_reporting_t *nanimals_detected_by_means_and_prodtype;
  RPT_reporting_t *cumul_nunits_detected;
  RPT_reporting_t *cumul_nunits_detected_by_means;
  RPT_reporting_t *cumul_nunits_detected_by_prodtype;
  RPT_reporting_t *cumul_nunits_detected_by_means_and_prodtype;
  RPT_reporting_t *cumul_nunits_detected_uniq;
  RPT_reporting_t *cumul_nanimals_detected;
  RPT_reporting_t *cumul_nanimals_detected_by_means;
  RPT_reporting_t *cumul_nanimals_detected_by_prodtype;
  RPT_reporting_t *cumul_nanimals_detected_by_means_and_prodtype;
  GHashTable *detected; /**< A table for tracking detections of unique units.
    If a unit has been detected, it will be in the.  The key is the unit
    (UNT_unit_t *), and the associated value is irrelevant. */
  GHashTable *detected_today; /**< A table for tracking multiple detections of
    a unit on one day.  If a unit has been detected today, it will be in the
    table.  The key is the unit (UNT_unit_t *), and the associated value is a
    pointer to a count_and_means_t struct. */
  RPT_reporting_t *first_detection_by_means_yesterday;
  RPT_reporting_t *first_detection_by_means_and_prodtype_yesterday;
  RPT_reporting_t *last_detection_by_means_yesterday;
  RPT_reporting_t *last_detection_by_means_and_prodtype_yesterday;
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
 * On each new day, zero the daily counts of detections.
 *
 * @param self the module.
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
  RPT_reporting_zero (local_data->nunits_detected);
  RPT_reporting_zero (local_data->nunits_detected_by_means);
  RPT_reporting_zero (local_data->nunits_detected_by_prodtype);
  RPT_reporting_zero (local_data->nunits_detected_by_means_and_prodtype);
  RPT_reporting_zero (local_data->nanimals_detected);
  RPT_reporting_zero (local_data->nanimals_detected_by_means);
  RPT_reporting_zero (local_data->nanimals_detected_by_prodtype);
  RPT_reporting_zero (local_data->nanimals_detected_by_means_and_prodtype);

  /* Empty the table that tracks multiple detections of a unit on one day. */
  g_hash_table_remove_all (local_data->detected_today);

  /* Make a backup copy of the first & last days of detection recorded so far.
   * We need this in case we "change our mind" about the means of detection for
   * a particular unit. */
  RPT_free_reporting (local_data->first_detection_by_means_yesterday);
  local_data->first_detection_by_means_yesterday =
    RPT_clone_reporting (local_data->first_detection_by_means);
  RPT_free_reporting (local_data->first_detection_by_means_and_prodtype_yesterday);
  local_data->first_detection_by_means_and_prodtype_yesterday =
    RPT_clone_reporting (local_data->first_detection_by_means_and_prodtype);
  RPT_free_reporting (local_data->last_detection_by_means_yesterday);
  local_data->last_detection_by_means_yesterday =
    RPT_clone_reporting (local_data->last_detection_by_means);
  RPT_free_reporting (local_data->last_detection_by_means_and_prodtype_yesterday);
  local_data->last_detection_by_means_and_prodtype_yesterday =
    RPT_clone_reporting (local_data->last_detection_by_means_and_prodtype);

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
handle_detection_event (struct spreadmodel_model_t_ *self, EVT_detection_event_t * event,
                        RAN_gen_t * rng)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  const char *means;
  const char *drill_down_list[3] = { NULL, NULL, NULL };
  UNT_detect_t detection;
  gpointer p;
  count_and_means_t *previous_detection;

#if DEBUG
  g_debug ("----- ENTER handle_detection_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;

  means = SPREADMODEL_detection_reason_abbrev[event->means];

  detection.unit_index = unit->index;
  detection.reason = event->means;
  detection.test_result = event->test_result;
  
#ifdef USE_SC_GUILIB
  sc_detect_unit( event->day, unit, detection );
#else  
  if (NULL != spreadmodel_detect_unit)
    {
      spreadmodel_detect_unit (detection);
    }
#endif  

  /* A unit can be detected multiple times on one day, by different means of
   * detection.  Handle the outputs that are not broken down by means of
   * detection first. */
  if (RPT_reporting_is_null (local_data->first_detection, NULL))
    {
      RPT_reporting_set_integer (local_data->first_detection, event->day, NULL);
      RPT_reporting_set_integer (local_data->detection_occurred, 1, NULL);
    } 
  if (RPT_reporting_is_null1 (local_data->first_detection_by_prodtype, unit->production_type_name))
    RPT_reporting_set_integer1 (local_data->first_detection_by_prodtype, event->day, unit->production_type_name);
  RPT_reporting_set_integer (local_data->last_detection, event->day, NULL);
  RPT_reporting_set_integer1 (local_data->last_detection_by_prodtype, event->day, unit->production_type_name);  

  p = g_hash_table_lookup (local_data->detected_today, unit);
  if (p == NULL)
    {
      /* This unit has not been detected already today. */
      if (RPT_reporting_is_null1 (local_data->first_detection_by_means, means))
        RPT_reporting_set_integer1 (local_data->first_detection_by_means, event->day, means);
      RPT_reporting_set_integer1 (local_data->last_detection_by_means, event->day, means);
      RPT_reporting_add_integer (local_data->nunits_detected, 1, NULL);
      RPT_reporting_add_integer1 (local_data->nunits_detected_by_means, 1, means);
      RPT_reporting_add_integer1 (local_data->nunits_detected_by_prodtype, 1, unit->production_type_name);
      RPT_reporting_add_integer (local_data->nanimals_detected, unit->size, NULL);
      RPT_reporting_add_integer1 (local_data->nanimals_detected_by_means, unit->size, means);
      RPT_reporting_add_integer1 (local_data->nanimals_detected_by_prodtype, unit->size, unit->production_type_name);
      RPT_reporting_add_integer (local_data->cumul_nunits_detected, 1, NULL);
      RPT_reporting_add_integer1 (local_data->cumul_nunits_detected_by_means, 1, means);
      RPT_reporting_add_integer1 (local_data->cumul_nunits_detected_by_prodtype, 1, unit->production_type_name);
      RPT_reporting_add_integer (local_data->cumul_nanimals_detected, unit->size, NULL);
      RPT_reporting_add_integer1 (local_data->cumul_nanimals_detected_by_means, unit->size, means);
      RPT_reporting_add_integer1 (local_data->cumul_nanimals_detected_by_prodtype, unit->size, unit->production_type_name);
      drill_down_list[0] = means;
      drill_down_list[1] = unit->production_type_name;
      if (RPT_reporting_is_null (local_data->first_detection_by_means_and_prodtype, drill_down_list))
        RPT_reporting_set_integer (local_data->first_detection_by_means_and_prodtype, event->day, drill_down_list);
      if (local_data->last_detection_by_means_and_prodtype->frequency != RPT_never)
        RPT_reporting_set_integer (local_data->last_detection_by_means_and_prodtype, event->day, drill_down_list);
      RPT_reporting_add_integer (local_data->nunits_detected_by_means_and_prodtype, 1, drill_down_list);
      if (local_data->nanimals_detected_by_means_and_prodtype->frequency != RPT_never)
        RPT_reporting_add_integer (local_data->nanimals_detected_by_means_and_prodtype, unit->size, drill_down_list);
      if (local_data->cumul_nunits_detected_by_means_and_prodtype->frequency != RPT_never)
        RPT_reporting_add_integer (local_data->cumul_nunits_detected_by_means_and_prodtype, 1, drill_down_list);
      if (local_data->cumul_nanimals_detected_by_means_and_prodtype->frequency != RPT_never)
        RPT_reporting_add_integer (local_data->cumul_nanimals_detected_by_means_and_prodtype, unit->size, drill_down_list);

      previous_detection = g_new (count_and_means_t, 1);
      previous_detection->count = 1;
      previous_detection->means = means;
      g_hash_table_insert (local_data->detected_today, unit, previous_detection);
    } /* end of case where the unit has not been detected already today */
  else
    {
      /* This unit has been detected already today. */
      previous_detection = (count_and_means_t *) p;
      if (previous_detection->means != means) /* static strings: if they match, the pointers will be identical */
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
                       r, P, previous_detection->means, means);
#endif
              /* We have changed our mind about what means of detection to
               * report for this unit.  Decrement the count of detections by
               * the old means. */
              RPT_reporting_sub_integer1 (local_data->nunits_detected_by_means, 1, previous_detection->means);
              RPT_reporting_sub_integer1 (local_data->nanimals_detected_by_means, unit->size, previous_detection->means);
              RPT_reporting_sub_integer1 (local_data->cumul_nunits_detected_by_means, 1, previous_detection->means);
              RPT_reporting_sub_integer1 (local_data->cumul_nanimals_detected_by_means, unit->size, previous_detection->means);
              if (RPT_reporting_get_integer1 (local_data->nunits_detected_by_means, previous_detection->means) == 0)
                {
                  /* We counted detections by a particular means today, but then
                   * we changed our mind and un-counted them all.  Restore
                   * yesterday's values for first & last detection by that means. */
                  if (RPT_reporting_is_null1 (local_data->first_detection_by_means_yesterday, previous_detection->means))
                    RPT_reporting_set_null1 (local_data->first_detection_by_means, previous_detection->means);
                  else
                    RPT_reporting_set_integer1 (local_data->first_detection_by_means,
                                                RPT_reporting_get_integer1 (local_data->first_detection_by_means_yesterday, previous_detection->means),
                                                previous_detection->means);
                  if (RPT_reporting_is_null1 (local_data->last_detection_by_means_yesterday, previous_detection->means))
                    RPT_reporting_set_null1 (local_data->last_detection_by_means, previous_detection->means);
                  else
                    RPT_reporting_set_integer1 (local_data->last_detection_by_means,
                                                RPT_reporting_get_integer1 (local_data->last_detection_by_means_yesterday, previous_detection->means),
                                                previous_detection->means);
                }
              drill_down_list[0] = previous_detection->means;
              drill_down_list[1] = unit->production_type_name;
              RPT_reporting_sub_integer (local_data->nunits_detected_by_means_and_prodtype, 1, drill_down_list);
              if (local_data->nanimals_detected_by_means_and_prodtype->frequency != RPT_never)
                RPT_reporting_sub_integer (local_data->nanimals_detected_by_means_and_prodtype, unit->size, drill_down_list);
              if (local_data->cumul_nunits_detected_by_means_and_prodtype->frequency != RPT_never)
                RPT_reporting_sub_integer (local_data->cumul_nunits_detected_by_means_and_prodtype, 1, drill_down_list);
              if (local_data->cumul_nanimals_detected_by_means_and_prodtype->frequency != RPT_never)
                RPT_reporting_sub_integer (local_data->cumul_nanimals_detected_by_means_and_prodtype, unit->size, drill_down_list);
              if (RPT_reporting_get_integer (local_data->nunits_detected_by_means_and_prodtype, drill_down_list) == 0)
                {
                  /* We counted detections by a particular combination of means
                   * and production type today, but then we changed our mind
                   * and un-counted them all.  Restore yesterday's values for
                   * first & last detection by that combination of means and
                   * production type. */
                  if (RPT_reporting_is_null (local_data->first_detection_by_means_and_prodtype_yesterday, drill_down_list))
                    RPT_reporting_set_null (local_data->first_detection_by_means_and_prodtype, drill_down_list);
                  else
                    RPT_reporting_set_integer (local_data->first_detection_by_means_and_prodtype,
                                               RPT_reporting_get_integer (local_data->first_detection_by_means_and_prodtype_yesterday, drill_down_list),
                                               drill_down_list);
                  if (RPT_reporting_is_null (local_data->last_detection_by_means_and_prodtype_yesterday, drill_down_list))
                    RPT_reporting_set_null (local_data->last_detection_by_means_and_prodtype, drill_down_list);
                  else
                    RPT_reporting_set_integer (local_data->last_detection_by_means_and_prodtype,
                                               RPT_reporting_get_integer (local_data->last_detection_by_means_and_prodtype_yesterday, drill_down_list),
                                               drill_down_list);
                }

              /* Increment the count of detections by the new means. */
              if (RPT_reporting_is_null1 (local_data->first_detection_by_means, means))
                RPT_reporting_set_integer1 (local_data->first_detection_by_means, event->day, means);
              RPT_reporting_set_integer1 (local_data->last_detection_by_means, event->day, means);
              RPT_reporting_add_integer1 (local_data->nunits_detected_by_means, 1, means);
              RPT_reporting_add_integer1 (local_data->nanimals_detected_by_means, unit->size, means);
              RPT_reporting_add_integer1 (local_data->cumul_nunits_detected_by_means, 1, means);
              RPT_reporting_add_integer1 (local_data->cumul_nanimals_detected_by_means, unit->size, means);
              drill_down_list[0] = means;
              if (RPT_reporting_is_null (local_data->first_detection_by_means_and_prodtype, drill_down_list))
                RPT_reporting_set_integer (local_data->first_detection_by_means_and_prodtype, event->day, drill_down_list);
              if (local_data->last_detection_by_means_and_prodtype->frequency != RPT_never)
                RPT_reporting_set_integer (local_data->last_detection_by_means_and_prodtype, event->day, drill_down_list);
              RPT_reporting_add_integer (local_data->nunits_detected_by_means_and_prodtype, 1, drill_down_list);
              if (local_data->nanimals_detected_by_means_and_prodtype->frequency != RPT_never)
                RPT_reporting_add_integer (local_data->nanimals_detected_by_means_and_prodtype, unit->size, drill_down_list);
              if (local_data->cumul_nunits_detected_by_means_and_prodtype->frequency != RPT_never)
                RPT_reporting_add_integer (local_data->cumul_nunits_detected_by_means_and_prodtype, 1, drill_down_list);
              if (local_data->cumul_nanimals_detected_by_means_and_prodtype->frequency != RPT_never)
                RPT_reporting_add_integer (local_data->cumul_nanimals_detected_by_means_and_prodtype, unit->size, drill_down_list);
            } /* end of case where previously recorded means of detection is replaced */
          else
            {
#if DEBUG
              g_debug ("r (%g) >= P (%g), not replacing recorded means \"%s\" with \"%s\"",
                       r, P, previous_detection->means, means);
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
      RPT_reporting_add_integer (local_data->cumul_nunits_detected_uniq, 1, NULL);
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
  RPT_reporting_zero (local_data->detection_occurred);
  RPT_reporting_set_null (local_data->first_detection, NULL);
  RPT_reporting_set_null (local_data->first_detection_by_means, NULL);
  RPT_reporting_set_null (local_data->first_detection_by_prodtype, NULL);
  RPT_reporting_set_null (local_data->first_detection_by_means_and_prodtype, NULL);
  RPT_reporting_set_null (local_data->last_detection, NULL);
  RPT_reporting_set_null (local_data->last_detection_by_means, NULL);
  RPT_reporting_set_null (local_data->last_detection_by_prodtype, NULL);
  RPT_reporting_set_null (local_data->last_detection_by_means_and_prodtype, NULL);
  RPT_reporting_zero (local_data->cumul_nunits_detected);
  RPT_reporting_zero (local_data->cumul_nunits_detected_by_means);
  RPT_reporting_zero (local_data->cumul_nunits_detected_by_prodtype);
  RPT_reporting_zero (local_data->cumul_nunits_detected_by_means_and_prodtype);
  RPT_reporting_zero (local_data->cumul_nunits_detected_uniq);
  RPT_reporting_zero (local_data->cumul_nanimals_detected);
  RPT_reporting_zero (local_data->cumul_nanimals_detected_by_means);
  RPT_reporting_zero (local_data->cumul_nanimals_detected_by_prodtype);
  RPT_reporting_zero (local_data->cumul_nanimals_detected_by_means_and_prodtype);
  g_hash_table_remove_all (local_data->detected);

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
  RPT_free_reporting (local_data->detection_occurred);
  RPT_free_reporting (local_data->first_detection);
  RPT_free_reporting (local_data->first_detection_by_means);
  RPT_free_reporting (local_data->first_detection_by_prodtype);
  RPT_free_reporting (local_data->first_detection_by_means_and_prodtype);
  RPT_free_reporting (local_data->last_detection);
  RPT_free_reporting (local_data->last_detection_by_means);
  RPT_free_reporting (local_data->last_detection_by_prodtype);
  RPT_free_reporting (local_data->last_detection_by_means_and_prodtype);
  RPT_free_reporting (local_data->nunits_detected);
  RPT_free_reporting (local_data->nunits_detected_by_means);
  RPT_free_reporting (local_data->nunits_detected_by_prodtype);
  RPT_free_reporting (local_data->nunits_detected_by_means_and_prodtype);
  RPT_free_reporting (local_data->nanimals_detected);
  RPT_free_reporting (local_data->nanimals_detected_by_means);
  RPT_free_reporting (local_data->nanimals_detected_by_prodtype);
  RPT_free_reporting (local_data->nanimals_detected_by_means_and_prodtype);
  RPT_free_reporting (local_data->cumul_nunits_detected);
  RPT_free_reporting (local_data->cumul_nunits_detected_by_means);
  RPT_free_reporting (local_data->cumul_nunits_detected_by_prodtype);
  RPT_free_reporting (local_data->cumul_nunits_detected_by_means_and_prodtype);
  RPT_free_reporting (local_data->cumul_nunits_detected_uniq);
  RPT_free_reporting (local_data->cumul_nanimals_detected);
  RPT_free_reporting (local_data->cumul_nanimals_detected_by_means);
  RPT_free_reporting (local_data->cumul_nanimals_detected_by_prodtype);
  RPT_free_reporting (local_data->cumul_nanimals_detected_by_means_and_prodtype);

  g_hash_table_destroy (local_data->detected);
  g_hash_table_destroy (local_data->detected_today);
  RPT_free_reporting (local_data->first_detection_by_means_yesterday);
  RPT_free_reporting (local_data->first_detection_by_means_and_prodtype_yesterday);
  RPT_free_reporting (local_data->last_detection_by_means_yesterday);
  RPT_free_reporting (local_data->last_detection_by_means_and_prodtype_yesterday);

  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Returns a new detection monitor.
 */
spreadmodel_model_t *
new (sqlite3 * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  spreadmodel_model_t *self;
  local_data_t *local_data;
  unsigned int i, j;         /* loop counters */
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
  self->run = run;
  self->reset = reset;
  self->is_listening_for = spreadmodel_model_is_listening_for;
  self->has_pending_actions = spreadmodel_model_answer_no;
  self->has_pending_infections = spreadmodel_model_answer_no;
  self->to_string = spreadmodel_model_to_string_default;
  self->printf = spreadmodel_model_printf;
  self->fprintf = spreadmodel_model_fprintf;
  self->free = local_free;

  local_data->detection_occurred =
    RPT_new_reporting ("detOccurred", RPT_integer, RPT_daily);
  local_data->first_detection =
    RPT_new_reporting ("firstDetection", RPT_integer, RPT_daily);
  local_data->first_detection_by_means =
    RPT_new_reporting ("firstDetection", RPT_group, RPT_daily);
  local_data->first_detection_by_prodtype =
    RPT_new_reporting ("firstDetection", RPT_group, RPT_daily);
  local_data->first_detection_by_means_and_prodtype =
    RPT_new_reporting ("firstDetection", RPT_group, RPT_daily);
  local_data->last_detection =
    RPT_new_reporting ("lastDetection", RPT_integer, RPT_daily);
  local_data->last_detection_by_means =
    RPT_new_reporting ("lastDetection", RPT_group, RPT_daily);
  local_data->last_detection_by_prodtype =
    RPT_new_reporting ("lastDetection", RPT_group, RPT_daily);
  local_data->last_detection_by_means_and_prodtype =
    RPT_new_reporting ("lastDetection", RPT_group, RPT_daily);
  local_data->nunits_detected =
    RPT_new_reporting ("detnUAll", RPT_integer, RPT_daily);
  local_data->nunits_detected_by_means =
    RPT_new_reporting ("detnU", RPT_group, RPT_daily);
  local_data->nunits_detected_by_prodtype =
    RPT_new_reporting ("detnU", RPT_group, RPT_daily);
  local_data->nunits_detected_by_means_and_prodtype =
    RPT_new_reporting ("detnU", RPT_group, RPT_daily);
  local_data->nanimals_detected =
    RPT_new_reporting ("detnAAll", RPT_integer, RPT_daily);
  local_data->nanimals_detected_by_means =
    RPT_new_reporting ("detnA", RPT_group, RPT_daily);
  local_data->nanimals_detected_by_prodtype =
    RPT_new_reporting ("detnA", RPT_group, RPT_daily);
  local_data->nanimals_detected_by_means_and_prodtype =
    RPT_new_reporting ("detnA", RPT_group, RPT_daily);
  local_data->cumul_nunits_detected =
    RPT_new_reporting ("detcUAll", RPT_integer, RPT_daily);
  local_data->cumul_nunits_detected_by_means =
    RPT_new_reporting ("detcU", RPT_group, RPT_daily);
  local_data->cumul_nunits_detected_by_prodtype =
    RPT_new_reporting ("detcU", RPT_group, RPT_daily);
  local_data->cumul_nunits_detected_by_means_and_prodtype =
    RPT_new_reporting ("detcU", RPT_group, RPT_daily);
  local_data->cumul_nunits_detected_uniq =
    RPT_new_reporting ("detcUqAll", RPT_integer, RPT_daily);
  local_data->cumul_nanimals_detected =
    RPT_new_reporting ("detcAAll", RPT_integer, RPT_daily);
  local_data->cumul_nanimals_detected_by_means =
    RPT_new_reporting ("detcA", RPT_group, RPT_daily);
  local_data->cumul_nanimals_detected_by_prodtype =
    RPT_new_reporting ("detcA", RPT_group, RPT_daily);
  local_data->cumul_nanimals_detected_by_means_and_prodtype =
    RPT_new_reporting ("detcA", RPT_group, RPT_daily);
  g_ptr_array_add (self->outputs, local_data->detection_occurred);
  g_ptr_array_add (self->outputs, local_data->first_detection);
  g_ptr_array_add (self->outputs, local_data->first_detection_by_means);
  g_ptr_array_add (self->outputs, local_data->first_detection_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->first_detection_by_means_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->last_detection);
  g_ptr_array_add (self->outputs, local_data->last_detection_by_means);
  g_ptr_array_add (self->outputs, local_data->last_detection_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->last_detection_by_means_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->nunits_detected);
  g_ptr_array_add (self->outputs, local_data->nunits_detected_by_means);
  g_ptr_array_add (self->outputs, local_data->nunits_detected_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->nunits_detected_by_means_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->nanimals_detected);
  g_ptr_array_add (self->outputs, local_data->nanimals_detected_by_means);
  g_ptr_array_add (self->outputs, local_data->nanimals_detected_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->nanimals_detected_by_means_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_detected);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_detected_by_means);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_detected_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_detected_by_means_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_detected_uniq);
  g_ptr_array_add (self->outputs, local_data->cumul_nanimals_detected);
  g_ptr_array_add (self->outputs, local_data->cumul_nanimals_detected_by_means);
  g_ptr_array_add (self->outputs, local_data->cumul_nanimals_detected_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_nanimals_detected_by_means_and_prodtype);

  /* Set the reporting frequency for the output variables. */

  /* Initialize the categories in the output variables. */
  local_data->production_types = units->production_type_names;
  for (i = 0; i < local_data->production_types->len; i++)
    {
      prodtype_name = (char *) g_ptr_array_index (local_data->production_types, i);
      RPT_reporting_set_integer1 (local_data->first_detection_by_prodtype, 0, prodtype_name);
      RPT_reporting_set_integer1 (local_data->last_detection_by_prodtype, 0, prodtype_name);
      RPT_reporting_set_integer1 (local_data->nunits_detected_by_prodtype, 0, prodtype_name);
      RPT_reporting_set_integer1 (local_data->nanimals_detected_by_prodtype, 0, prodtype_name);
      RPT_reporting_set_integer1 (local_data->cumul_nunits_detected_by_prodtype, 0, prodtype_name);
      RPT_reporting_set_integer1 (local_data->cumul_nanimals_detected_by_prodtype, 0, prodtype_name);
    }
  for (i = 0; i < SPREADMODEL_NDETECTION_REASONS; i++)
    {
      const char *means;
      const char *drill_down_list[3] = { NULL, NULL, NULL };
      if ((SPREADMODEL_detection_reason)i == SPREADMODEL_DetectionReasonUnspecified)
        continue;
      means = SPREADMODEL_detection_reason_abbrev[i];
      /* Two function calls for the first_detection and last_detection
       * variables: one to establish the type of the sub-variables (they are
       * integers), and one to clear them to "null" (they have no meaningful
       * value until a detection occurs). */
      RPT_reporting_add_integer1 (local_data->first_detection_by_means, 0, means);
      RPT_reporting_set_null1 (local_data->first_detection_by_means, means);
      RPT_reporting_add_integer1 (local_data->last_detection_by_means, 0, means);
      RPT_reporting_set_null1 (local_data->last_detection_by_means, means);
      RPT_reporting_add_integer1 (local_data->nunits_detected_by_means, 0, means);
      RPT_reporting_add_integer1 (local_data->cumul_nunits_detected_by_means, 0, means);
      RPT_reporting_add_integer1 (local_data->nanimals_detected_by_means, 0, means);
      RPT_reporting_add_integer1 (local_data->cumul_nanimals_detected_by_means, 0, means);
      drill_down_list[0] = means;
      for (j = 0; j < local_data->production_types->len; j++)
        {
          drill_down_list[1] = (char *) g_ptr_array_index (local_data->production_types, j);
          RPT_reporting_add_integer (local_data->first_detection_by_means_and_prodtype, 0,
                                     drill_down_list);
          RPT_reporting_set_null (local_data->first_detection_by_means_and_prodtype,
                                  drill_down_list);
          RPT_reporting_add_integer (local_data->last_detection_by_means_and_prodtype, 0,
                                     drill_down_list);
          RPT_reporting_set_null (local_data->last_detection_by_means_and_prodtype,
                                  drill_down_list);
          RPT_reporting_add_integer (local_data->nunits_detected_by_means_and_prodtype, 0,
                                     drill_down_list);
          RPT_reporting_add_integer (local_data->cumul_nunits_detected_by_means_and_prodtype, 0,
                                     drill_down_list);
          RPT_reporting_add_integer (local_data->nanimals_detected_by_means_and_prodtype, 0,
                                     drill_down_list);
          RPT_reporting_add_integer (local_data->cumul_nanimals_detected_by_means_and_prodtype, 0,
                                     drill_down_list);
        }
    }

  /* Initialize a table to track detections of unique units. */
  local_data->detected = g_hash_table_new (g_direct_hash, g_direct_equal);

  /* Initialize a table to track multiple detections of a unit on one day. */
  local_data->detected_today = g_hash_table_new_full (g_direct_hash, g_direct_equal, NULL, g_free);

  /* These variables hold a backup copy of the first & last days of detection
   * recorded so far.  They are needed in case we "change our mind" about the
   * means of detection for a particular unit. */
  local_data->first_detection_by_means_yesterday = NULL;
  local_data->first_detection_by_means_and_prodtype_yesterday = NULL;
  local_data->last_detection_by_means_yesterday = NULL;
  local_data->last_detection_by_means_and_prodtype_yesterday = NULL;

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file detection_monitor.c */
