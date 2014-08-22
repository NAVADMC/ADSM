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
#define handle_new_day_event zone_monitor_handle_new_day_event
#define handle_request_for_zone_focus_event zone_monitor_handle_request_for_zone_focus_event

#include "module.h"
#include "gis.h"

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
EVT_event_type_t events_listened_for[] = {
  EVT_BeforeAnySimulations,
  EVT_RequestForZoneFocus,
  EVT_NewDay
};



/* Specialized information for this model. */
typedef struct
{
  int nzones;
  projPJ projection; /* The map projection used to convert the units' latitudes
    and longitudes to x-y coordinates */
  RPT_reporting_t *area;
  RPT_reporting_t *perimeter;
  RPT_reporting_t *num_separate_areas;
  RPT_reporting_t *num_units;
  RPT_reporting_t *num_units_by_prodtype;
  RPT_reporting_t *num_unit_days;
  RPT_reporting_t *num_unit_days_by_prodtype;
  RPT_reporting_t *num_animal_days;
  RPT_reporting_t *num_animal_days_by_prodtype;
  gboolean seen_request_for_zone_focus;
}
local_data_t;



/**
 * Responds to a request for zone focus event by setting a flag indicating that
 * the area and perimeter will have to be re-calculated.
 *
 * @param self this module.
 */
void
handle_request_for_zone_focus_event (struct adsm_module_t_ *self)
{
  local_data_t *local_data;

  #if DEBUG
    g_debug ("----- ENTER handle_request_for_zone_focus_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);
  local_data->seen_request_for_zone_focus = TRUE;

  #if DEBUG
    g_debug ("----- EXIT handle_request_for_zone_focus_event (%s)", MODEL_NAME);
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
  local_data_t *local_data;
  int i;
  ZON_zone_t *zone;
  double area;
  double perimeter;
  unsigned int nunits;
  UNT_unit_t *unit;
  const char *drill_down_list[3] = { NULL, NULL, NULL };

#if DEBUG
  g_debug ("----- ENTER handle_new_day_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* Recalculate the area and perimeter only if the seen_request_for_zone_focus
   * flag is set. */
  if (local_data->seen_request_for_zone_focus)
    {
      for (i = 0; i < local_data->nzones - 1; i++)
        {
          zone = ZON_zone_list_get (zones, i);

          area = ZON_update_area (zone);
          RPT_reporting_set_real1 (local_data->area, area, zone->name);

          perimeter = ZON_update_perimeter (zone);
          RPT_reporting_set_real1 (local_data->perimeter, perimeter, zone->name);
          if (NULL != adsm_record_zone_perimeter)
            adsm_record_zone_perimeter (zone->level, perimeter);           

          RPT_reporting_set_integer1 (local_data->num_separate_areas,
                                      zone->poly->num_contours, zone->name);
        }

      /* In the loop above, the area of each zone polygon was computed.  But since
       * zones are nested inside of each other, that's not exactly what we want:
       * we want the area displayed for an "outer" zone to exclude the area of the
       * smaller "inner" zones.  So we do that computation here.
       *
       * Start with the next-to-last zone, because the last one is the
       * "background" zone. */
      for (i = local_data->nzones - 2; i >= 0; i--)
        {
          ZON_zone_t *next_smaller_zone;
          zone = ZON_zone_list_get (zones, i);
          if (i > 0)
            {
              next_smaller_zone = ZON_zone_list_get (zones, i - 1);
              zone->area -= next_smaller_zone->area;
              RPT_reporting_set_real1 (local_data->area, zone->area, zone->name);
            }
          #ifdef USE_SC_GUILIB
            sc_record_zone_area( event->day, zone );
          #else
            if (NULL != adsm_record_zone_area)     
              adsm_record_zone_area (zone->level, zone->area);
          #endif
        }

      /* Don't forget to report the smallest zone to the GUI! */
      zone = ZON_zone_list_get (zones, 0);		  
      #ifdef USE_SC_GUILIB
        sc_record_zone_area( event->day, zone );
      #else		  
        if (NULL != adsm_record_zone_area)
          {  
            adsm_record_zone_area (zone->level, zone->area);
          };
      #endif
      
      local_data->seen_request_for_zone_focus = FALSE;
    } /* end of if seen_request_for_zone_focus flag is set */

  nunits = zones->membership_length;
  RPT_reporting_zero (local_data->num_units);
  RPT_reporting_zero (local_data->num_units_by_prodtype);
  for (i = 0; i < nunits; i++)
    {
      zone = zones->membership[i]->parent;
      RPT_reporting_add_integer1 (local_data->num_units, 1, zone->name);
      unit = UNT_unit_list_get (units, i);
      drill_down_list[0] = zone->name;
      drill_down_list[1] = unit->production_type_name;
      RPT_reporting_add_integer (local_data->num_units_by_prodtype, 1, drill_down_list);
      if (unit->state != Destroyed)
        {
          RPT_reporting_add_integer1 (local_data->num_unit_days, 1, zone->name);
          RPT_reporting_add_integer1 (local_data->num_animal_days, unit->size, zone->name);
          RPT_reporting_add_integer (local_data->num_unit_days_by_prodtype, 1,
                                     drill_down_list);
          RPT_reporting_add_integer (local_data->num_animal_days_by_prodtype, unit->size,
                                     drill_down_list);
        }
    }

#if DEBUG
  g_debug ("----- EXIT handle_new_day_event (%s)", MODEL_NAME);
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
run (struct adsm_module_t_ *self, UNT_unit_list_t * units,
     ZON_zone_list_t * zones, EVT_event_t * event, RAN_gen_t * rng, EVT_event_queue_t * queue)
{
#if DEBUG
  g_debug ("----- ENTER run (%s)", MODEL_NAME);
#endif

  switch (event->type)
    {
    case EVT_BeforeAnySimulations:
      adsm_declare_outputs (self, queue);
      break;
    case EVT_RequestForZoneFocus:
      handle_request_for_zone_focus_event (self);
      break;
    case EVT_NewDay:
      handle_new_day_event (self, units, zones, &(event->u.new_day));
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

#if DEBUG
  g_debug ("----- ENTER reset (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  /* RPT_reporting_zero preserves sub-cateogories but sets all numbers to 0. */
  RPT_reporting_zero (local_data->area);
  RPT_reporting_zero (local_data->perimeter);
  RPT_reporting_zero (local_data->num_separate_areas);
  RPT_reporting_zero (local_data->num_units);
  RPT_reporting_zero (local_data->num_units_by_prodtype);
  RPT_reporting_zero (local_data->num_unit_days);
  RPT_reporting_zero (local_data->num_unit_days_by_prodtype);
  RPT_reporting_zero (local_data->num_animal_days);
  RPT_reporting_zero (local_data->num_animal_days_by_prodtype);

  local_data->seen_request_for_zone_focus = FALSE;

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
local_free (struct adsm_module_t_ *self)
{
  local_data_t *local_data;

#if DEBUG
  g_debug ("----- ENTER free (%s)", MODEL_NAME);
#endif

  /* Free the dynamically-allocated parts. */
  local_data = (local_data_t *) (self->model_data);
  RPT_free_reporting (local_data->area);
  RPT_free_reporting (local_data->perimeter);
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
adsm_module_t *
new (sqlite3 * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  adsm_module_t *self;
  local_data_t *local_data;
  unsigned int nprod_types;
  int i, j;
  ZON_zone_t *zone;
  const char *drill_down_list[3] = { NULL, NULL, NULL };

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
  self->to_string = adsm_module_to_string_default;
  self->printf = adsm_model_printf;
  self->fprintf = adsm_model_fprintf;
  self->free = local_free;

  local_data->area = RPT_new_reporting ("zoneArea", RPT_group);
  local_data->perimeter = RPT_new_reporting ("zonePerimeter", RPT_group);
  local_data->num_separate_areas =
    RPT_new_reporting ("numSeparateAreas", RPT_group);
  local_data->num_units = RPT_new_reporting ("unitsInZone", RPT_group);
  local_data->num_units_by_prodtype = RPT_new_reporting ("unitsInZone", RPT_group);
  local_data->num_unit_days = RPT_new_reporting ("unitDaysInZone", RPT_group);
  local_data->num_unit_days_by_prodtype = RPT_new_reporting ("unitDaysInZone", RPT_group);
  local_data->num_animal_days = RPT_new_reporting ("animalDaysInZone", RPT_group);
  local_data->num_animal_days_by_prodtype = RPT_new_reporting ("animalDaysInZone", RPT_group);
  g_ptr_array_add (self->outputs, local_data->area);
  g_ptr_array_add (self->outputs, local_data->perimeter);
  g_ptr_array_add (self->outputs, local_data->num_separate_areas);
  g_ptr_array_add (self->outputs, local_data->num_units);
  g_ptr_array_add (self->outputs, local_data->num_units_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->num_unit_days);
  g_ptr_array_add (self->outputs, local_data->num_unit_days_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->num_animal_days);
  g_ptr_array_add (self->outputs, local_data->num_animal_days_by_prodtype);

  local_data->nzones = ZON_zone_list_length (zones);
  local_data->projection = projection;

  /* Initialize the categories in the output variables. */
  nprod_types = units->production_type_names->len;
  for (i = 0; i < local_data->nzones; i++)
    {
      zone = ZON_zone_list_get (zones, i);

      if (i < local_data->nzones - 1)
        {
          RPT_reporting_set_real1 (local_data->area, 0, zone->name);
          RPT_reporting_set_real1 (local_data->perimeter, 0, zone->name);
          RPT_reporting_set_integer1 (local_data->num_separate_areas, 0, zone->name);
        }
      RPT_reporting_set_integer1 (local_data->num_units, 0, zone->name);
      RPT_reporting_set_integer1 (local_data->num_unit_days, 0, zone->name);
      RPT_reporting_set_integer1 (local_data->num_animal_days, 0, zone->name);

      drill_down_list[0] = zone->name;
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
