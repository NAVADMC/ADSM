/** @file zone_monitor.c
 * Tracks the shape, area, and perimeter of zones, number of units in each zone,
 * and number of animal-days spent in each zone.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @version 0.1
 * @date Feb 2007
 *
 * Copyright &copy; University of Guelph, 2007-2009
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
#define new zone_monitor_new
#define run zone_monitor_run
#define reset zone_monitor_reset
#define events_listened_for zone_monitor_events_listened_for
#define local_free zone_monitor_free
#define handle_before_any_simulations_event zone_monitor_handle_before_any_simulations_event
#define handle_new_day_event zone_monitor_handle_new_day_event
#define handle_last_day_event zone_monitor_handle_last_day_event

#include "module.h"
#include "gis.h"
#include "spreadmodel.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#if HAVE_MATH_H
#  include <math.h>
#endif

#if HAVE_STRINGS_H
#  include <strings.h>
#endif

#include "zone_monitor.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "zone-monitor"



#define NEVENTS_LISTENED_FOR 3
EVT_event_type_t events_listened_for[] = { EVT_BeforeAnySimulations, EVT_NewDay,
  EVT_LastDay };



/* Specialized information for this model. */
typedef struct
{
  int nzones;
  projPJ projection; /* The map projection used to convert the units' latitudes
    and longitudes to x-y coordinates */
  RPT_reporting_t *area;
  RPT_reporting_t *max_area;
  RPT_reporting_t *max_area_day;
  RPT_reporting_t *final_area;
  RPT_reporting_t *perimeter;
  RPT_reporting_t *max_perimeter;
  RPT_reporting_t *max_perimeter_day;
  RPT_reporting_t *final_perimeter;
  RPT_reporting_t *num_separate_areas;
  RPT_reporting_t *num_units;
  RPT_reporting_t *num_units_by_prodtype;
  RPT_reporting_t *num_unit_days;
  RPT_reporting_t *num_unit_days_by_prodtype;
  RPT_reporting_t *num_animal_days;
  RPT_reporting_t *num_animal_days_by_prodtype;
}
local_data_t;



/**
 * Before any simulations, this module announces the outputs it tracks, in case
 * other modules want to use or aggregate those outputs.
 *
 * @param self this module.
 * @param queue for any new events the model creates.
 */
void
handle_before_any_simulations_event (struct spreadmodel_model_t_ * self,
                                     EVT_event_queue_t * queue)
{
  GPtrArray *outputs;
  unsigned int i;

#if DEBUG
  g_debug ("----- ENTER handle_before_any_simulations_event (%s)", MODEL_NAME);
#endif

  /* Create a GPtrArray containing pointers to all the outputs this module
   * tracks. */
  outputs = g_ptr_array_new ();
  for (i = 0; i < self->outputs->len; i++)
    g_ptr_array_add (outputs, g_ptr_array_index (self->outputs, i));
  EVT_event_enqueue (queue, EVT_new_declaration_of_outputs_event (outputs));

  /* Note that we don't clean up the GPtrArray.  It will be freed along with
   * the declaration event after all interested sub-models have processed the
   * event. */

#if DEBUG
  g_debug ("----- EXIT handle_before_any_simulations_event (%s)", MODEL_NAME);
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
handle_new_day_event (struct spreadmodel_model_t_ *self, UNT_unit_list_t * units,
                      ZON_zone_list_t * zones, EVT_new_day_event_t * event)
{
  local_data_t *local_data;
  gboolean area_due, perimeter_due, num_areas_due, num_units_due;
  int i;
  ZON_zone_t *zone, *next_smaller_zone;
  gchar *name;
  double area;
  double perimeter;
  unsigned int nunits;
  UNT_unit_t *unit;
  const char *drill_down_list[3] = { NULL, NULL, NULL };

#if DEBUG
  g_debug ("----- ENTER handle_new_day_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  area_due = local_data->area->frequency == RPT_daily
             || local_data->max_area_day->frequency != RPT_never;
  perimeter_due = local_data->perimeter->frequency == RPT_daily
                  || local_data->max_perimeter_day->frequency != RPT_never;
  num_areas_due = RPT_reporting_due (local_data->num_separate_areas, event->day);
  num_units_due = (RPT_reporting_due (local_data->num_units, event->day)
                   || RPT_reporting_due (local_data->num_units_by_prodtype, event->day));

  for (i = 0; i < local_data->nzones - 1; i++)
    {
      zone = ZON_zone_list_get (zones, i);
      name = zone->name->str;

      if (area_due)
        {
          area = ZON_update_area (zone);
          RPT_reporting_set_real1 (local_data->area, area, name);
        }

      if (perimeter_due)
        {
          perimeter = ZON_update_perimeter (zone);
          RPT_reporting_set_real1 (local_data->perimeter, perimeter, name);
          /* If the zone has grown, record the new maximum perimeter. */
          if (perimeter > 0
              && (RPT_reporting_is_null1 (local_data->max_perimeter, name)
                  || (perimeter > RPT_reporting_get_real1 (local_data->max_perimeter, name))))
            {
              RPT_reporting_set_real1 (local_data->max_perimeter, perimeter, name);
              RPT_reporting_set_integer1 (local_data->max_perimeter_day, event->day, name);
            } 
            
			    if (NULL != spreadmodel_record_zone_perimeter)
			     spreadmodel_record_zone_perimeter (zone->level, perimeter);           
        }

      if (num_areas_due)
        RPT_reporting_set_integer1 (local_data->num_separate_areas,
                                    zone->poly->num_contours, name);
    }

  /* In the loop above, the area of each zone polygon was computed.  But since
   * zones are nested inside of each other, that's not exactly what we want:
   * we want the area displayed for an "outer" zone to exclude the area of the
   * smaller "inner" zones.  So we do that computation here. */
  if (area_due)
    {
      /* Start with the next-to-last zone, because the last one is the
       * "background" zone. */
      for (i = local_data->nzones - 2; i >= 0; i--)
        {
          zone = ZON_zone_list_get (zones, i);
          name = zone->name->str;
          if (i > 0)
            {
              next_smaller_zone = ZON_zone_list_get (zones, i - 1);
              zone->area -= next_smaller_zone->area;
              RPT_reporting_set_real1 (local_data->area, zone->area, name);
            }
          /* If the zone has grown, record the new maximum area. */
          if (zone->area > 0
              && (RPT_reporting_is_null1 (local_data->max_area_day, name)
                  || (zone->area > RPT_reporting_get_real1 (local_data->max_area, name))))
            {
              RPT_reporting_set_real1 (local_data->max_area, zone->area, name);
              RPT_reporting_set_integer1 (local_data->max_area_day, event->day, name);
            }
#ifdef USE_SC_GUILIB
		      sc_record_zone_area( event->day, zone );
#else		  
          if (NULL != spreadmodel_record_zone_area)     
			     spreadmodel_record_zone_area (zone->level, zone->area);
#endif		  
        }

      /* Don't forget to report the smallest zone to the GUI! */
      zone = ZON_zone_list_get (zones, 0);		  
#ifdef USE_SC_GUILIB
      sc_record_zone_area( event->day, zone );
#else		  
      if (NULL != spreadmodel_record_zone_area)
        {  
          spreadmodel_record_zone_area (zone->level, zone->area);
        };
#endif	  
    }

  if (num_units_due
      || local_data->num_unit_days->frequency != RPT_never
      || local_data->num_animal_days->frequency != RPT_never)
    {
      nunits = zones->membership_length;
      RPT_reporting_zero (local_data->num_units);
      RPT_reporting_zero (local_data->num_units_by_prodtype);
      for (i = 0; i < nunits; i++)
        {
          zone = zones->membership[i]->parent;
          name = zone->name->str;
          RPT_reporting_add_integer1 (local_data->num_units, 1, name);
          unit = UNT_unit_list_get (units, i);
          drill_down_list[0] = name;
          drill_down_list[1] = unit->production_type_name;
          RPT_reporting_add_integer (local_data->num_units_by_prodtype, 1, drill_down_list);
          if (unit->state != Destroyed)
            {
              RPT_reporting_add_integer1 (local_data->num_unit_days, 1, name);
              RPT_reporting_add_integer1 (local_data->num_animal_days, unit->size, name);
              RPT_reporting_add_integer (local_data->num_unit_days_by_prodtype, 1,
                                         drill_down_list);
              RPT_reporting_add_integer (local_data->num_animal_days_by_prodtype, unit->size,
                                         drill_down_list);
            }
        }
    }

#if DEBUG
  g_debug ("----- EXIT handle_new_day_event (%s)", MODEL_NAME);
#endif
}



/**
 * Responds to a last day event by computing output variables that are only
 * needed on the last day.
 *
 * @param self the model.
 * @param units a list of units.
 * @param zones a list of zones.
 * @param event a last day event.
 */
void
handle_last_day_event (struct spreadmodel_model_t_ *self, UNT_unit_list_t * units,
                       ZON_zone_list_t * zones, EVT_last_day_event_t * event)
{
  local_data_t *local_data;
  gboolean skip_area, skip_perimeter, skip_num_areas, skip_num_units;
  int i;
  ZON_zone_t *zone, *next_smaller_zone;
  double area;
  double perimeter;
  unsigned int nunits;
  UNT_unit_t *unit;
  const char *drill_down_list[3] = { NULL, NULL, NULL };

#if DEBUG
  g_debug ("----- ENTER handle_last_day_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* Some of the output variables are computationally intensive.  If they're
   * reported "never", or if they were already computed today by
   * handle_new_day_event, don't bother to compute them. */
  skip_area = local_data->final_area->frequency == RPT_never
    && local_data->area->frequency == RPT_never
    && local_data->max_area->frequency == RPT_never;
  skip_perimeter = local_data->final_perimeter->frequency == RPT_never
    && local_data->perimeter->frequency == RPT_never
    && local_data->max_perimeter->frequency == RPT_never;
  skip_num_areas = local_data->num_separate_areas->frequency == RPT_never
    || RPT_reporting_due (local_data->num_separate_areas, event->day);
  skip_num_units = local_data->num_units->frequency == RPT_never
    || (RPT_reporting_due (local_data->num_units, event->day)
        && RPT_reporting_due (local_data->num_units_by_prodtype, event->day));

  /* We don't have to worry about num_unit_days or num_animal_days because,
   * unless they are set to be reported "never", they will be updated every day
   * by handle_new_day_event. */

  for (i = 0; i < local_data->nzones - 1; i++)
    {
      gchar *name;
      zone = ZON_zone_list_get (zones, i);
      name = zone->name->str;

      if (!skip_area)
        {
          area = ZON_update_area (zone);
          RPT_reporting_set_real1 (local_data->area, area, name);
        }

      if (!skip_perimeter)
        {
          perimeter = ZON_update_perimeter (zone);
          RPT_reporting_set_real1 (local_data->perimeter, perimeter, name);
          if (local_data->final_perimeter->frequency != RPT_never)
            {
              RPT_reporting_set_real1 (local_data->final_perimeter, perimeter, name);
            }
          /* If the zone has grown, record the new maximum perimeter. */
          if (perimeter > 0
              && (RPT_reporting_is_null1 (local_data->max_perimeter, name)
                  || (perimeter > RPT_reporting_get_real1 (local_data->max_perimeter, name))))
            {
              RPT_reporting_set_real1 (local_data->max_perimeter, perimeter, name);
              RPT_reporting_set_integer1 (local_data->max_perimeter_day, event->day, name);
            }
          RPT_reporting_set_real1 (local_data->final_perimeter, perimeter, name);
        }

      if (!skip_num_areas)
        RPT_reporting_set_integer1 (local_data->num_separate_areas,
                                    zone->poly->num_contours, name);
    }

  if (!skip_area)
    {
      /* Start with the next-to-last zone, because the last one is the
       * "background" zone. */
      for (i = local_data->nzones - 2; i >= 0; i--)
        {
          gchar *name;
          zone = ZON_zone_list_get (zones, i);
          name = zone->name->str;
          if (i > 0)
            {
              next_smaller_zone = ZON_zone_list_get (zones, i - 1);
              zone->area -= next_smaller_zone->area;
              RPT_reporting_set_real1 (local_data->area, zone->area, name);
            }
          if (local_data->final_area->frequency != RPT_never)
            {
              RPT_reporting_set_real1 (local_data->final_area, zone->area, name);
            }
          /* If the zone has grown, record the new maximum area. */
          if (zone->area > 0
              && (RPT_reporting_is_null1 (local_data->max_area_day, name)
                  || (zone->area > RPT_reporting_get_real1 (local_data->max_area, name))))
            {
              RPT_reporting_set_real1 (local_data->max_area, zone->area, name);
              RPT_reporting_set_integer1 (local_data->max_area_day, event->day, name);
            }
        }
    }

  if (!skip_num_units)
    {
      nunits = zones->membership_length;
      RPT_reporting_zero (local_data->num_units);    
      RPT_reporting_zero (local_data->num_units_by_prodtype);    
      for (i = 0; i < nunits; i++)
        {
          zone = zones->membership[i]->parent;
          RPT_reporting_add_integer1 (local_data->num_units, 1, zone->name->str);
          unit = UNT_unit_list_get (units, i);
          drill_down_list[0] = zone->name->str;
          drill_down_list[1] = unit->production_type_name;
          RPT_reporting_add_integer (local_data->num_units_by_prodtype, 1, drill_down_list);
        }
    }

#if DEBUG
  g_debug ("----- EXIT handle_last_day_event (%s)", MODEL_NAME);
#endif
}



/**
 * Runs this model.
 *
 * @param self the model.
 * @param units a list of units.
 * @param zones a list of zones.
 * @param event the event that caused the model to run.
 * @param rng a random number generator.
 * @param queue for any new events the model creates.
 */
void
run (struct spreadmodel_model_t_ *self, UNT_unit_list_t * units,
     ZON_zone_list_t * zones, EVT_event_t * event, RAN_gen_t * rng, EVT_event_queue_t * queue)
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
      handle_new_day_event (self, units, zones, &(event->u.new_day));
      break;
    case EVT_LastDay:
      handle_last_day_event (self, units, zones, &(event->u.last_day));
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
  /* RPT_reporting_zero preserves sub-cateogories but sets all numbers to 0. */
  RPT_reporting_zero (local_data->area);
  RPT_reporting_zero (local_data->max_area);
  RPT_reporting_set_null (local_data->max_area_day, NULL);
  RPT_reporting_set_null (local_data->final_area, NULL);
  RPT_reporting_zero (local_data->perimeter);
  RPT_reporting_zero (local_data->max_perimeter);
  RPT_reporting_set_null (local_data->max_perimeter_day, NULL);
  RPT_reporting_set_null (local_data->final_perimeter, NULL);
  RPT_reporting_zero (local_data->num_separate_areas);
  RPT_reporting_zero (local_data->num_units);
  RPT_reporting_zero (local_data->num_units_by_prodtype);
  RPT_reporting_zero (local_data->num_unit_days);
  RPT_reporting_zero (local_data->num_unit_days_by_prodtype);
  RPT_reporting_zero (local_data->num_animal_days);
  RPT_reporting_zero (local_data->num_animal_days_by_prodtype);

#if DEBUG
  g_debug ("----- EXIT reset (%s)", MODEL_NAME);
#endif
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
  RPT_free_reporting (local_data->area);
  RPT_free_reporting (local_data->max_area);
  RPT_free_reporting (local_data->max_area_day);
  RPT_free_reporting (local_data->final_area);
  RPT_free_reporting (local_data->perimeter);
  RPT_free_reporting (local_data->max_perimeter);
  RPT_free_reporting (local_data->max_perimeter_day);
  RPT_free_reporting (local_data->final_perimeter);
  RPT_free_reporting (local_data->num_separate_areas);
  RPT_free_reporting (local_data->num_units);
  RPT_free_reporting (local_data->num_units_by_prodtype);
  RPT_free_reporting (local_data->num_unit_days);
  RPT_free_reporting (local_data->num_unit_days_by_prodtype);
  RPT_free_reporting (local_data->num_animal_days);
  RPT_free_reporting (local_data->num_animal_days_by_prodtype);
  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Returns a new zone monitor.
 */
spreadmodel_model_t *
new (scew_element * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  spreadmodel_model_t *self;
  local_data_t *local_data;
  scew_element const *e;
  scew_list *ee, *iter;
  const XML_Char *variable_name;
  RPT_frequency_t freq;
  gboolean success;
  gboolean broken_down;
  unsigned int nprod_types;
  int i, j;
  ZON_zone_t *zone;
  const char *drill_down_list[3] = { NULL, NULL, NULL };

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
  self->is_singleton = TRUE;
  self->is_listening_for = spreadmodel_model_is_listening_for;
  self->has_pending_actions = spreadmodel_model_answer_no;
  self->has_pending_infections = spreadmodel_model_answer_no;
  self->to_string = spreadmodel_model_to_string_default;
  self->printf = spreadmodel_model_printf;
  self->fprintf = spreadmodel_model_fprintf;
  self->free = local_free;

  /* Make sure the right XML subtree was sent. */
  g_assert (strcmp (scew_element_name (params), MODEL_NAME) == 0);

  local_data->area = RPT_new_reporting ("zoneArea", RPT_group, RPT_never);
  local_data->max_area = RPT_new_reporting ("maxZoneArea", RPT_group, RPT_never);
  local_data->max_area_day = RPT_new_reporting ("maxZoneAreaDay", RPT_group, RPT_never);
  local_data->final_area = RPT_new_reporting ("finalZoneArea", RPT_group, RPT_never);
  local_data->perimeter = RPT_new_reporting ("zonePerimeter", RPT_group, RPT_never);
  local_data->max_perimeter = RPT_new_reporting ("maxZonePerimeter", RPT_group, RPT_never);
  local_data->max_perimeter_day = RPT_new_reporting ("maxZonePerimeterDay", RPT_group, RPT_never);
  local_data->final_perimeter = RPT_new_reporting ("finalZonePerimeter", RPT_group, RPT_never);
  local_data->num_separate_areas =
    RPT_new_reporting ("num-separate-areas", RPT_group, RPT_never);
  local_data->num_units = RPT_new_reporting ("unitsInZone", RPT_group, RPT_never);
  local_data->num_units_by_prodtype = RPT_new_reporting ("unitsInZone", RPT_group, RPT_never);
  local_data->num_unit_days = RPT_new_reporting ("unitDaysInZone", RPT_group, RPT_never);
  local_data->num_unit_days_by_prodtype = RPT_new_reporting ("unitDaysInZone", RPT_group, RPT_never);
  local_data->num_animal_days = RPT_new_reporting ("animalDaysInZone", RPT_group, RPT_never);
  local_data->num_animal_days_by_prodtype = RPT_new_reporting ("animalDaysInZone", RPT_group, RPT_never);
  g_ptr_array_add (self->outputs, local_data->area);
  g_ptr_array_add (self->outputs, local_data->max_area);
  g_ptr_array_add (self->outputs, local_data->max_area_day);
  g_ptr_array_add (self->outputs, local_data->final_area);
  g_ptr_array_add (self->outputs, local_data->perimeter);
  g_ptr_array_add (self->outputs, local_data->max_perimeter);
  g_ptr_array_add (self->outputs, local_data->max_perimeter_day);
  g_ptr_array_add (self->outputs, local_data->final_perimeter);
  g_ptr_array_add (self->outputs, local_data->num_separate_areas);
  g_ptr_array_add (self->outputs, local_data->num_units);
  g_ptr_array_add (self->outputs, local_data->num_units_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->num_unit_days);
  g_ptr_array_add (self->outputs, local_data->num_unit_days_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->num_animal_days);
  g_ptr_array_add (self->outputs, local_data->num_animal_days_by_prodtype);

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
      if (strcmp (variable_name, "zoneArea") == 0
               || strcmp (variable_name, "zone-area") == 0)
        {
          RPT_reporting_set_frequency (local_data->area, freq);
        }
      else if (strcmp (variable_name, "maxZoneArea") == 0)
        {
          RPT_reporting_set_frequency (local_data->max_area, freq);
        }
      else if (strcmp (variable_name, "maxZoneAreaDay") == 0)
        {
          RPT_reporting_set_frequency (local_data->max_area_day, freq);
        }
      else if (strcmp (variable_name, "finalZoneArea") == 0)
        {
          RPT_reporting_set_frequency (local_data->final_area, freq);
        }
      else if (strcmp (variable_name, "zonePerimeter") == 0)
        {
          RPT_reporting_set_frequency (local_data->perimeter, freq);
        }
      else if (strcmp (variable_name, "maxZonePerimeter") == 0)
        {
          RPT_reporting_set_frequency (local_data->max_perimeter, freq);
        }
      else if (strcmp (variable_name, "maxZonePerimeterDay") == 0)
        {
          RPT_reporting_set_frequency (local_data->max_perimeter_day, freq);
        }
      else if (strcmp (variable_name, "finalZonePerimeter") == 0)
        {
          RPT_reporting_set_frequency (local_data->final_perimeter, freq);
        }
      else if (strcmp (variable_name, "num-separate-areas") == 0)
        {
          RPT_reporting_set_frequency (local_data->num_separate_areas, freq);
        }
      else if (strcmp (variable_name, "unitsInZone") == 0
               || strncmp (variable_name, "num-units-in-zone", 17) == 0)
        {
          RPT_reporting_set_frequency (local_data->num_units, freq);
          if (broken_down)
            RPT_reporting_set_frequency (local_data->num_units_by_prodtype, freq);
        }
      else if (strcmp (variable_name, "unitDaysInZone") == 0)
        {
          RPT_reporting_set_frequency (local_data->num_unit_days, freq);
          if (broken_down)
            RPT_reporting_set_frequency (local_data->num_unit_days_by_prodtype, freq);
        }
      else if (strcmp (variable_name, "animalDaysInZone") == 0
               || strncmp (variable_name, "num-animal-days-in-zone", 23) == 0)
        {
          RPT_reporting_set_frequency (local_data->num_animal_days, freq);
          if (broken_down)
            RPT_reporting_set_frequency (local_data->num_animal_days_by_prodtype, freq);
        }
      else
        g_warning ("no output variable named \"%s\", ignoring", variable_name);        
    }
  scew_list_free (ee);

  local_data->nzones = ZON_zone_list_length (zones);
  local_data->projection = projection;

  /* Initialize the categories in the output variables. */
  nprod_types = units->production_type_names->len;
  for (i = 0; i < local_data->nzones; i++)
    {
      gchar *name;
      zone = ZON_zone_list_get (zones, i);
      name = zone->name->str;

      if (i < local_data->nzones - 1)
        {
          RPT_reporting_set_real1 (local_data->area, 0, name);
          RPT_reporting_set_real1 (local_data->max_area, 0, name);
          RPT_reporting_set_integer1 (local_data->max_area_day, 0, name);
          RPT_reporting_set_real1 (local_data->final_area, 0, zone->name->str);
          RPT_reporting_set_real1 (local_data->perimeter, 0, zone->name->str);
          RPT_reporting_set_real1 (local_data->max_perimeter, 0, zone->name->str);
          RPT_reporting_set_integer1 (local_data->max_perimeter_day, 0, zone->name->str);
          RPT_reporting_set_real1 (local_data->final_perimeter, 0, zone->name->str);
          RPT_reporting_set_integer1 (local_data->num_separate_areas, 0, zone->name->str);
        }
      RPT_reporting_set_integer1 (local_data->num_units, 0, zone->name->str);
      RPT_reporting_set_integer1 (local_data->num_unit_days, 0, zone->name->str);
      RPT_reporting_set_integer1 (local_data->num_animal_days, 0, zone->name->str);

      drill_down_list[0] = zone->name->str;
      for (j = 0; j < nprod_types; j++)
        {
          drill_down_list[1] = (char *) g_ptr_array_index (units->production_type_names, j);
          RPT_reporting_set_integer (local_data->num_units_by_prodtype, 0, drill_down_list);
          RPT_reporting_set_integer (local_data->num_unit_days_by_prodtype, 0, drill_down_list);
          RPT_reporting_set_integer (local_data->num_animal_days_by_prodtype, 0, drill_down_list);
        }
    }

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file zone_monitor.c */
