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
#define local_free zone_monitor_free
#define handle_before_each_simulation_event zone_monitor_handle_before_each_simulation_event
#define handle_unit_zone_change_event zone_monitor_handle_unit_zone_change_event
#define handle_destruction_event zone_monitor_handle_destruction_event
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



/* Specialized information for this model. */
typedef struct
{
  int nzones;
  guint nprodtypes;
  projPJ projection; /* The map projection used to convert the units' latitudes
    and longitudes to x-y coordinates */
  RPT_reporting_t  **area;
  RPT_reporting_t  **perimeter;
  RPT_reporting_t  **num_separate_areas;
  RPT_reporting_t  **num_units;
  RPT_reporting_t ***num_units_by_prodtype;
  RPT_reporting_t  **num_unit_days;
  RPT_reporting_t ***num_unit_days_by_prodtype;
  RPT_reporting_t  **num_animal_days;
  RPT_reporting_t ***num_animal_days_by_prodtype;
  GPtrArray *cumul_outputs; /**< Cumulative outputs, is a list to make it easy
    to zero them all at once. */
  gboolean seen_request_for_zone_focus;
  guint num_units_at_start;
  guint *num_units_at_start_by_prodtype;
  gdouble num_animals_at_start;
  gdouble *num_animals_at_start_by_prodtype;
  guint *num_units_not_destroyed;
  guint **num_units_not_destroyed_by_prodtype;
  gdouble *num_animals_not_destroyed;
  gdouble **num_animals_not_destroyed_by_prodtype;
}
local_data_t;



/**
 * Before any simulations, record the total number of units and number of units
 * of each production type.  Also report the output variables this module is
 * tracking.
 *
 * @param self this module.
 * @param units a list of units.
 * @param queue for any new events this module generates.
 */
void
handle_before_any_simulations_event (struct adsm_module_t_ *self,
                                     UNT_unit_list_t *units,
                                     EVT_event_queue_t *queue)
{
  local_data_t *local_data;
  guint nunits, nprodtypes, i;

  #if DEBUG
    g_debug ("----- ENTER handle_before_any_simulations_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);
  
  nunits = UNT_unit_list_length (units);
  local_data->num_units_at_start = nunits;
  local_data->num_animals_at_start = 0; /* will count them in the loop below */

  nprodtypes = units->production_type_names->len;
  local_data->num_units_at_start_by_prodtype = g_new0 (guint, nprodtypes);
  local_data->num_animals_at_start_by_prodtype = g_new0 (gdouble, nprodtypes);
  for (i = 0; i < nunits; i++)
    {
      UNT_unit_t *unit;
      double nanimals;
      unit = UNT_unit_list_get (units, i);
      nanimals = (double)(unit->size);
      local_data->num_units_at_start_by_prodtype[unit->production_type] += 1;
      local_data->num_animals_at_start += nanimals;
      local_data->num_animals_at_start_by_prodtype[unit->production_type] += nanimals;
    }

  adsm_declare_outputs (self, queue);

  #if DEBUG
    g_debug ("----- EXIT handle_before_any_simulations_event (%s)", MODEL_NAME);
  #endif

  return;
}



/**
 * Before each simulation, reset the recorded statistics to zero.
 *
 * @param self this module.
 */
void
handle_before_each_simulation_event (struct adsm_module_t_ *self)
{
  local_data_t *local_data;
  guint background_zone_index, zone_index;
  UNT_production_type_t prodtype;

  #if DEBUG
    g_debug ("----- ENTER handle_before_each_simulation_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);

  /* Reset the counts to all units in the background zone. */
  g_ptr_array_foreach (local_data->cumul_outputs, RPT_reporting_zero_as_GFunc, NULL);
  background_zone_index = local_data->nzones - 1;
  RPT_reporting_set_integer (local_data->num_units[background_zone_index],
                             local_data->num_units_at_start);
  for (prodtype = 0; prodtype < local_data->nprodtypes; prodtype++)
    {
      RPT_reporting_set_integer (local_data->num_units_by_prodtype[background_zone_index][prodtype],
                                 local_data->num_units_at_start_by_prodtype[prodtype]);
    }

  for (zone_index = 0; zone_index < local_data->nzones; zone_index++)
    {
      local_data->num_units_not_destroyed[zone_index] = 0;
      local_data->num_animals_not_destroyed[zone_index] = 0;
      for (prodtype = 0; prodtype < local_data->nprodtypes; prodtype++)
        {
          local_data->num_units_not_destroyed_by_prodtype[zone_index][prodtype] = 0;
          local_data->num_animals_not_destroyed_by_prodtype[zone_index][prodtype] = 0;
        }
    }
  local_data->num_units_not_destroyed[background_zone_index] = local_data->num_units_at_start;
  local_data->num_animals_not_destroyed[background_zone_index] = local_data->num_animals_at_start;
  for (prodtype = 0; prodtype < local_data->nprodtypes; prodtype++)
    {
      local_data->num_units_not_destroyed_by_prodtype[background_zone_index][prodtype] =
        local_data->num_units_at_start_by_prodtype[prodtype];
      local_data->num_animals_not_destroyed_by_prodtype[background_zone_index][prodtype] =
        local_data->num_animals_at_start_by_prodtype[prodtype];
    }

  local_data->seen_request_for_zone_focus = FALSE;

  #if DEBUG
    g_debug ("----- EXIT handle_before_each_simulation_event (%s)", MODEL_NAME);
  #endif

  return;
}



/**
 * Responds to a unit zone change event by updating the counts of units in each
 * zone.
 *
 * @param self this module.
 * @param event a unit zone change event.
 */
void
handle_unit_zone_change_event (struct adsm_module_t_ *self,
                               EVT_unit_zone_change_event_t *event)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  guint old_zone_index, new_zone_index;
  UNT_production_type_t prodtype;
  double nanimals;

  #if DEBUG
    g_debug ("----- ENTER handle_unit_zone_change_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;
  prodtype = unit->production_type;
  old_zone_index =  event->old_zone->level - 1;
  new_zone_index =  event->new_zone->level - 1;
  RPT_reporting_sub_integer (local_data->num_units[old_zone_index], 1);
  RPT_reporting_add_integer (local_data->num_units[new_zone_index], 1);
  RPT_reporting_sub_integer (local_data->num_units_by_prodtype[old_zone_index][prodtype], 1);
  RPT_reporting_add_integer (local_data->num_units_by_prodtype[new_zone_index][prodtype], 1);

  if (unit->state != Destroyed)
    {
      /* Update the counts of how many non-destroyed units and animals are in
       * each zone. */
      local_data->num_units_not_destroyed[old_zone_index] -= 1;
      local_data->num_units_not_destroyed[new_zone_index] += 1;
      local_data->num_units_not_destroyed_by_prodtype[old_zone_index][prodtype] -= 1;
      local_data->num_units_not_destroyed_by_prodtype[new_zone_index][prodtype] += 1;
      nanimals = (double)(unit->size);
      local_data->num_animals_not_destroyed[old_zone_index] -= nanimals;
      local_data->num_animals_not_destroyed[new_zone_index] += nanimals;
      local_data->num_animals_not_destroyed_by_prodtype[old_zone_index][prodtype] -= nanimals;
      local_data->num_animals_not_destroyed_by_prodtype[new_zone_index][prodtype] += nanimals;      
    }

  #if DEBUG
    g_debug ("----- EXIT handle_unit_zone_change_event (%s)", MODEL_NAME);
  #endif

  return;
}



/**
 * Responds to a destruction event by updating the counts of units in each
 * zone.
 *
 * @param self this module.
 * @param event a destruction event.
 */
void
handle_destruction_event (struct adsm_module_t_ *self,
                          ZON_zone_list_t *zones,
                          EVT_destruction_event_t *event)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  UNT_production_type_t prodtype;
  double nanimals;
  ZON_zone_t *zone;
  guint zone_index;

  #if DEBUG
    g_debug ("----- ENTER handle_destruction_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;
  prodtype = unit->production_type;
  nanimals = (double)(unit->size);
  zone = zones->membership[unit->index]->parent;
  zone_index = zone->level - 1;

  local_data->num_units_not_destroyed[zone_index] -= 1;
  local_data->num_units_not_destroyed_by_prodtype[zone_index][prodtype] -= 1;
  local_data->num_animals_not_destroyed[zone_index] -= nanimals;
  local_data->num_animals_not_destroyed_by_prodtype[zone_index][prodtype] -= nanimals;

  #if DEBUG
    g_debug ("----- EXIT handle_destruction_event (%s)", MODEL_NAME);
  #endif

  return;
}



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
  guint zone_index;
  UNT_production_type_t prodtype;

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
          RPT_reporting_set_real (local_data->area[i], area);

          perimeter = ZON_update_perimeter (zone);
          RPT_reporting_set_real (local_data->perimeter[i], perimeter);
          if (NULL != adsm_record_zone_perimeter)
            adsm_record_zone_perimeter (zone->level, perimeter);           

          RPT_reporting_set_integer (local_data->num_separate_areas[i],
                                     zone->poly->num_contours);
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
              RPT_reporting_set_real (local_data->area[i], zone->area);
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

  /* Update the number of unit-days and animals-days spent in each zone. */
  for (zone_index = 0; zone_index < local_data->nzones; zone_index++)
    {
      RPT_reporting_add_integer (local_data->num_unit_days[zone_index],
                                 local_data->num_units_not_destroyed[zone_index]);
      RPT_reporting_add_real (local_data->num_animal_days[zone_index],
                              local_data->num_animals_not_destroyed[zone_index]);
      for (prodtype = 0; prodtype < local_data->nprodtypes; prodtype++)
        {
          RPT_reporting_add_integer (local_data->num_unit_days_by_prodtype[zone_index][prodtype],
                                     local_data->num_units_not_destroyed_by_prodtype[zone_index][prodtype]);
          RPT_reporting_add_real (local_data->num_animal_days_by_prodtype[zone_index][prodtype],
                                  local_data->num_animals_not_destroyed_by_prodtype[zone_index][prodtype]);
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
      handle_before_any_simulations_event (self, units, queue);
      break;
    case EVT_BeforeEachSimulation:
      handle_before_each_simulation_event (self);
      break;
    case EVT_UnitZoneChange:
      handle_unit_zone_change_event (self, &(event->u.unit_zone_change));
      break;
    case EVT_Destruction:
      handle_destruction_event (self, zones, &(event->u.destruction));
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
  g_free (local_data);
  g_ptr_array_free (self->outputs, /* free_seg = */ TRUE); /* also frees all output variables */
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
  GPtrArray *zone_names;
  guint i;
  ZON_zone_t *zone;

#if DEBUG
  g_debug ("----- ENTER new (%s)", MODEL_NAME);
#endif

  self = g_new (adsm_module_t, 1);
  local_data = g_new (local_data_t, 1);
  EVT_event_type_t events_listened_for[] = {
    EVT_BeforeAnySimulations,
    EVT_BeforeEachSimulation,
    EVT_UnitZoneChange,
    EVT_Destruction,
    EVT_RequestForZoneFocus,
    EVT_NewDay,
    0
  };

  self->name = MODEL_NAME;
  self->events_listened_for = adsm_setup_events_listened_for (events_listened_for);
  self->outputs = g_ptr_array_new_with_free_func ((GDestroyNotify)RPT_free_reporting);
  self->model_data = local_data;
  self->run = run;
  self->is_listening_for = adsm_model_is_listening_for;
  self->has_pending_actions = adsm_model_answer_no;
  self->has_pending_infections = adsm_model_answer_no;
  self->to_string = adsm_module_to_string_default;
  self->printf = adsm_model_printf;
  self->fprintf = adsm_model_fprintf;
  self->free = local_free;

  local_data->projection = projection;
  local_data->cumul_outputs = g_ptr_array_new();
  local_data->nprodtypes = units->production_type_names->len;

  /* Make a list of the zone names, including the background zone.  This
   * temporary list will be used below to initialize sub-categories in the
   * output variables. */
  local_data->nzones = ZON_zone_list_length (zones);
  zone_names = g_ptr_array_sized_new (local_data->nzones);
  for (i = 0; i < local_data->nzones; i++)
    {
      zone = ZON_zone_list_get (zones, i);
      g_ptr_array_add (zone_names, zone->name);
    }
  {
    RPT_bulk_create_t outputs[] = {
      /* zoneArea, zonePerimeter, and numSeparateAreas do not include the
       * background zone, hence the "nzones - 1" for the number of
       * subcategories. */
      { &local_data->area, "zoneArea%s", RPT_real,
        RPT_GPtrArray, zone_names, local_data->nzones - 1,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->perimeter, "zonePerimeter%s", RPT_real,
        RPT_GPtrArray, zone_names, local_data->nzones - 1,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->num_separate_areas, "numSeparateAreas%s", RPT_integer,
        RPT_GPtrArray, zone_names, local_data->nzones - 1,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      /* unitsInZone does include the background zone. */
      { &local_data->num_units, "unitsInZone%s", RPT_integer,
        RPT_GPtrArray, zone_names, local_data->nzones,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->num_units_by_prodtype, "unitsInZone%s%s", RPT_integer,
        RPT_GPtrArray, zone_names, local_data->nzones,
        RPT_GPtrArray, units->production_type_names, local_data->nprodtypes,
        self->outputs, local_data->cumul_outputs },

      { &local_data->num_unit_days, "unitDaysInZone%s", RPT_integer,
        RPT_GPtrArray, zone_names, local_data->nzones,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->num_unit_days_by_prodtype, "unitDaysInZone%s%s", RPT_integer,
        RPT_GPtrArray, zone_names, local_data->nzones,
        RPT_GPtrArray, units->production_type_names, local_data->nprodtypes,
        self->outputs, local_data->cumul_outputs },

      { &local_data->num_animal_days, "animalDaysInZone%s", RPT_real,
        RPT_GPtrArray, zone_names, local_data->nzones,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->num_animal_days_by_prodtype, "animalDaysInZone%s%s", RPT_real,
        RPT_GPtrArray, zone_names, local_data->nzones,
        RPT_GPtrArray, units->production_type_names, local_data->nprodtypes,
        self->outputs, local_data->cumul_outputs },

      { NULL }
    };  
    RPT_bulk_create (outputs);
  }

  g_ptr_array_free (zone_names, /* free_seg = */ TRUE);

  local_data->num_units_not_destroyed = g_new (guint, local_data->nzones);
  local_data->num_animals_not_destroyed = g_new (gdouble, local_data->nzones);
  local_data->num_units_not_destroyed_by_prodtype = g_new (guint *, local_data->nzones);
  local_data->num_animals_not_destroyed_by_prodtype = g_new (gdouble *, local_data->nzones);
  for (i = 0; i < local_data->nzones; i++)
    {
      local_data->num_units_not_destroyed_by_prodtype[i] = g_new (guint, local_data->nprodtypes);
      local_data->num_animals_not_destroyed_by_prodtype[i] = g_new (gdouble, local_data->nprodtypes);
    }
  
#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file zone_monitor.c */
