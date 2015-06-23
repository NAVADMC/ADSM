/** @file zone_model.c
 * Parameters that describe a zone.  Specifically,
 * <ul>
 *   <li> the zone's name
 *   <li> the zone's radius
 *   <li> the zone's surveillance level, where level 1 should correspond to the
 *     smallest radius and probably the most intensive surveillance, level 2
 *     should correspond to the second-smallest radius and probably the
 *     second-most intensive surveillance, and so on.
 * </ul>
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @version 0.1
 * @date October 2004
 *
 * Copyright &copy; University of Guelph, 2004-2008
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
#define new zone_model_new
#define run zone_model_run
#define to_string zone_model_to_string
#define local_free zone_model_free
#define handle_before_each_simulation_event zone_model_handle_before_each_simulation_event
#define handle_request_for_zone_focus_event zone_model_handle_request_for_zone_focus_event
#define handle_midnight_event zone_model_handle_midnight_event

#include "module.h"
#include "gis.h"
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

#include "zone_model.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "zone-model"



typedef struct
{
  UNT_unit_list_t * units;
  ZON_zone_list_t * zones;
  GQueue *pending_foci; /**< A list of foci that have yet to be added.  Each
    item in the queue will be a (UNT_unit_t *).  Because the events in one
    simulation day should be considered to happen simultaneously, changes to a
    zone are not processed mid-day; instead, they are stored and applied all at
    once at Midnight. */
}
local_data_t;



#define EPSILON 0.01 /* 10 m */



/**
 * Gets the minimum and maximum x- and y- coordinates of a polygon contour.
 *
 * @param contour a contour.
 * @param coord a location in which to store the minimum x, minimum y, maximum
 *   x, and maximum y coordinates, in that order.
 */
static void
gpc_contour_get_boundary (gpc_vertex_list * contour, double *coord)
{
  double minx, maxx, miny, maxy;
  gpc_vertex *vertex;
  int i;

  vertex = contour->vertex;
  minx = maxx = vertex->x;
  miny = maxy = vertex->y;
  vertex++;

  for (i = 1; i < contour->num_vertices; i++, vertex++)
    {
      if (vertex->x < minx)
        minx = vertex->x;
      else if (vertex->x > maxx)
        maxx = vertex->x;
      if (vertex->y < miny)
        miny = vertex->y;
      else if (vertex->y > maxy)
        maxy = vertex->y;
    }

  coord[0] = minx;
  coord[1] = miny;
  coord[2] = maxx;
  coord[3] = maxy;
}



/**
 * Before each simulation, this module resets the zones and deletes any
 * pending zone foci left over from a previous iteration.
 *
 * @param self this module
 * @param zones a zone list.
 */
void
handle_before_each_simulation_event (struct adsm_module_t_ *self,
                                     ZON_zone_list_t * zones)
{
  local_data_t *local_data;

  #if DEBUG
    g_debug ("----- ENTER handle_before_each_simulation_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);

  ZON_zone_list_reset (zones);

  /* Empty the list of pending zone foci.  We just need to free the queue nodes
   * themselves, not the UNT_unit_t structures that they point to. */
  while (!g_queue_is_empty (local_data->pending_foci))
    g_queue_pop_head (local_data->pending_foci);

  #if DEBUG
    g_debug ("----- EXIT handle_before_each_simulation_event (%s)", MODEL_NAME);
  #endif

  return;
}



/**
 * Special structure for use with the callback functions below.
 */
typedef struct
{
  double x, y;
  UNT_unit_list_t *units;
  UNT_unit_t *unit;
  ZON_zone_list_t *zones;
  EVT_event_queue_t *queue;
  int day;
  ZON_zone_fragment_t **fragment_containing_focus;
  gpc_vertex_list *hole;
  ZON_zone_fragment_t *hole_fragment;
  #if DEBUG
    int *n_search_hits;
    int zone_index;
  #endif
} callback_t;



/**
 * Check whether the unit's distance to the focus is within the radius
 * assigned to each zone.  If so, update the unit-to-zone assignment.
 */
static void
check_circle_and_rezone (int id, gpointer arg)
{
  callback_t *callback_data;
  UNT_unit_t *unit;
  double distance_sq;
  ZON_zone_list_t *zones;
  unsigned int nzones;
  ZON_zone_t *zone;
  ZON_zone_fragment_t *current_fragment;
  int current_level;
  int i;
  UNT_zone_t zone_update;
  #if DEBUG
    gboolean update_zones = TRUE;
    GString *s;
  #endif

  #if DEBUG
    g_debug ("----- ENTER check_circle_and_rezone");
  #endif

  callback_data = (callback_t *) arg;
  unit = UNT_unit_list_get (callback_data->units, id);

  #if DEBUG
    g_debug ("checking unit \"%s\"", unit->official_id);
  #endif

  distance_sq = GIS_distance_sq (unit->x, unit->y,
                                 callback_data->x, callback_data->y);
  /* Check if the distance is within the radius of any of the zone rings,
   * starting with the smallest ring.  Skip the last zone in the list because
   * it will be the "background" zone. */
  zones = callback_data->zones;
  nzones = ZON_zone_list_length (zones);
  for (i = 0; i < nzones - 1; i++)
    {
      zone = ZON_zone_list_get (zones, i);
      if (distance_sq - zone->radius_sq <= zone->epsilon_sq)
        {
          /* The unit is inside this zone ring. */
          #if DEBUG
            g_debug ("unit \"%s\" is inside the radius (%.2g km) for zone \"%s\" (level %i)",
                     unit->official_id, zone->radius, zone->name, zone->level);

            callback_data->n_search_hits[i]++;
          #endif
          /* update_zones is ignored, unless testing and debugging are being conducted. */
          #if DEBUG
            if( TRUE == update_zones )
              {
          #endif
                /* Find out the surveillance level of the zone the unit is currently
                 * in.  If the unit is currently in a lower-priority level (the level
                 * number is higher), update the unit's zone membership. */
                current_fragment = zones->membership[unit->index];
                current_level = current_fragment->parent->level;
                if (current_level > zone->level)
                  {
                    #if DEBUG
                      s = g_string_new (NULL);
                      g_string_printf (s, "unit \"%s\" was in zone \"%s\" (level %i)",
                                       unit->official_id, current_fragment->parent->name, current_level);
                    #endif
                    zones->membership[unit->index] = callback_data->fragment_containing_focus[i];
                    EVT_event_enqueue (callback_data->queue,
                                       EVT_new_unit_zone_change_event (unit,
                                                                       current_fragment->parent,
                                                                       zone,
                                                                       callback_data->day));

                    zone_update.unit_index = unit->index;
                    zone_update.zone_level = zone->level;

                    #ifdef USE_SC_GUILIB
                      sc_record_zone_change( unit, zone );
                    #else				  
                      if( NULL != adsm_record_zone_change )
                        {
                          adsm_record_zone_change( zone_update );
                        };
                    #endif				  
                    #if DEBUG
                      g_string_append_printf (s, ", now in zone \"%s\" (level %i)",
                                              zone->name, zone->level);
                      g_debug ("%s", s->str);
                      g_string_free (s, TRUE);
                    #endif
                  }
                else
                  {
                    #if DEBUG
                      g_debug ("unit \"%s\" remains in zone \"%s\" (level %i)",
                               unit->official_id, current_fragment->parent->name, current_level);
                    #endif
                  }
          #if DEBUG
              }
          #endif
          break;
        }
    }

  #if DEBUG
    g_debug ("----- EXIT check_circle_and_rezone");
  #endif

  return;
}



/**
 * Check whether the unit's location is inside the given polygon.  If so,
 * update the unit-to-zone assignment.
 */
static void
check_poly_and_rezone (int id, gpointer arg)
{
  callback_t *callback_data;
  UNT_unit_t *unit;
  gpc_vertex_list *poly;
  ZON_zone_fragment_t *current_fragment;
  ZON_zone_t *zone;
  ZON_zone_list_t *zones;
  int current_level;
  UNT_zone_t zone_update;
  #if DEBUG
    gboolean update_zones = TRUE;
    GString *s;
  #endif

  #if DEBUG
    g_debug ("----- ENTER check_poly_and_rezone");
  #endif

  callback_data = (callback_t *) arg;
  unit = UNT_unit_list_get (callback_data->units, id);

  #if DEBUG
    g_debug ("checking unit \"%s\"", unit->official_id);
  #endif

  poly = callback_data->hole;

  /* Check if the unit's location is inside the polygon. */
  if (GIS_point_in_contour (poly, unit->x, unit->y))
    {
      zone = callback_data->hole_fragment->parent;
      #if DEBUG
        g_debug ("unit \"%s\" is inside the hole in zone \"%s\" (level %i)",
                 unit->official_id, zone->name, zone->level);

        callback_data->n_search_hits[callback_data->zone_index]++;
      #endif

      /* update_zones is ignored, unless testing and debugging are being conducted. */
      #if DEBUG
        if( TRUE == update_zones )
          {
        #endif
            /* Find out the surveillance level of the zone the unit is currently in.
             * If the unit is currently in a lower-priority level (the level number
             * number is higher), update the unit's zone membership. */
            zones = callback_data->zones;
            current_fragment = zones->membership[unit->index];
            current_level = current_fragment->parent->level;
            if (current_level > zone->level)
              {
                #if DEBUG
                  s = g_string_new (NULL);
                  g_string_printf (s, "unit \"%s\" was in zone \"%s\" (level %i)",
                                   unit->official_id, current_fragment->parent->name, current_level);
                #endif
                zones->membership[unit->index] = callback_data->hole_fragment;
                EVT_event_enqueue (callback_data->queue,
                                   EVT_new_unit_zone_change_event (unit,
                                                                   current_fragment->parent,
                                                                   zone,
                                                                   callback_data->day));

                zone_update.unit_index = unit->index;
                zone_update.zone_level = zone->level;

                #ifdef USE_SC_GUILIB
                  sc_record_zone_change( unit, zone );
                #else			  
			      if( NULL != adsm_record_zone_change )
                    {
                      adsm_record_zone_change( zone_update );
                    };
                #endif			  

                #if DEBUG
                  g_string_append_printf (s, ", now in zone \"%s\" (level %i)", zone->name, zone->level);
                  g_debug ("%s", s->str);
                  g_string_free (s, TRUE);
                #endif
              }
        #if DEBUG
          }
        #endif
    }

  #if DEBUG
    g_debug ("----- EXIT check_poly_and_rezone");
  #endif

  return;
}



/**
 * Responds to a request for zone focus event by adding a new zone focus (to
 * come into the effect at Mignight) to the zone list.
 *
 * @param self this module.
 * @param event a request for zone focus event.
 * @param zones the zone list.
 */
void
handle_request_for_zone_focus_event (struct adsm_module_t_ *self,
                                     EVT_request_for_zone_focus_event_t * event,
                                     ZON_zone_list_t * zones)
{
  local_data_t *local_data;
  UNT_unit_t *unit;

  #if DEBUG
    g_debug ("----- ENTER handle_request_for_zone_focus_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;
  #if DEBUG
    g_debug ("adding pending zone focus at x=%g, y=%g", unit->x, unit->y);
  #endif
  g_queue_push_tail (local_data->pending_foci, unit);

  #ifdef USE_SC_GUILIB
    sc_make_zone_focus( event->day, unit );
  #else
    if( NULL != adsm_make_zone_focus )
      adsm_make_zone_focus (unit->index);
  #endif

  #if DEBUG
    g_debug ("----- EXIT handle_request_for_zone_focus_event (%s)", MODEL_NAME);
  #endif
}



/**
 * Responds to a midnight event by updating the zone shapes and unit-to-zone
 * assignments.
 *
 * @param self the model.
 * @param units a unit list.
 * @param zones a zone list.
 * @param event a midnight event.
 * @param queue for any new events the module generates.
 */
void
handle_midnight_event (struct adsm_module_t_ *self,
                       UNT_unit_list_t * units,
                       ZON_zone_list_t * zones,
                       EVT_midnight_event_t * event,
                       EVT_event_queue_t *queue)
{
  local_data_t *local_data;
  unsigned int nzones;
  double x, y;
  UNT_unit_t *pending_focus;
  callback_t callback_data;
  ZON_zone_t *zone;
  double distance;
  gpc_polygon **holes;
  int nholes;
  gpc_vertex_list *hole;
  double boundary[4];
  double hole_size;
  int i, j;

  #if DEBUG
    int report_array_size;
    int *nHitsCircle;
    int *nHitsPoly;
  #endif

  #if DEBUG
    g_debug ("----- ENTER handle_midnight_event (%s)", MODEL_NAME);
  #endif

  /* If there is just a "background" zone, we have nothing to do. */
  nzones = ZON_zone_list_length (zones);
  if (nzones == 1)
    {
      #if DEBUG
        g_debug ("there is only a background zone, nothing to do");
      #endif
      goto end;
    }

  #if DEBUG
    /* For debugging purposes, these arrays can be used to count the number of 
     * search hits produced by each mechanism. */
    report_array_size = nzones - 1;
    nHitsCircle = g_new0( int, report_array_size );
    nHitsPoly = g_new0( int, report_array_size );
  #endif

  local_data = (local_data_t *) (self->model_data);

  callback_data.units = units;
  callback_data.zones = zones;
  callback_data.queue = queue;
  callback_data.day = event->day;

  while (!g_queue_is_empty (local_data->pending_foci))
    {
      pending_focus = (UNT_unit_t *) g_queue_pop_head (local_data->pending_foci);
      x = pending_focus->x;
      y = pending_focus->y;
      #if DEBUG
        g_debug ("focus to add at x=%g, y=%g", x, y);
      #endif

      /* Update the shape of each zone, and get pointers to the zone fragments
       * in which the focus lies. */
      callback_data.fragment_containing_focus = g_new (ZON_zone_fragment_t *, nzones);
      holes = g_new0 (gpc_polygon *, nzones);
      for (i = 0; i < nzones-1; i++)
        {
          zone = ZON_zone_list_get (zones, i);
          #if DEBUG
            g_debug ("adding focus to zone \"%s\" (level %i)", zone->name, zone->level);
          #endif
          callback_data.fragment_containing_focus[i] =
            ZON_zone_add_focus (zone, x, y, &holes[i]);
        }
      for (i = 0; i < nzones-2; i++)
        {
          callback_data.fragment_containing_focus[i]->nests_in =
            callback_data.fragment_containing_focus[i+1];
        }

      /* Update the assignments of units to zone fragments. */
      /* First, draw the circles around the focus. */
      callback_data.x = x;
      callback_data.y = y;
      
      /* Find the distances to other units. */
      /* The search area should be the radius of the largest zone.  Remember
       * that the largest zone is the next-to-last item in the zone list. */
      distance = ZON_zone_list_get (zones, nzones - 2)->radius + EPSILON;
      #if DEBUG
        callback_data.n_search_hits = nHitsCircle;
      #endif
      spatial_search_circle_by_xy (units->spatial_index, x, y, distance,
                                   check_circle_and_rezone, &callback_data);

      /* Next, fill in any "holes", starting with the zone with the highest
       * priority. */
      for (i = 0; i < nzones; i++)
        {
          if (holes[i] == NULL)
            continue;
          zone = ZON_zone_list_get (zones, i);
          nholes = holes[i]->num_contours;
          #if DEBUG
            g_debug ("filling in %i hole(s) in zone \"%s\" (level %i)",
                     nholes, zone->name, zone->level);

            callback_data.zone_index = i;
          #endif

          for (j = 0; j < nholes; j++)
            {
              hole = &(holes[i]->contour[j]);
              gpc_contour_get_boundary (hole, boundary);
              hole_size = MIN (boundary[2] - boundary[0], boundary[3] - boundary[1]);
              callback_data.hole = hole;
              callback_data.hole_fragment = callback_data.fragment_containing_focus[i];

              #if DEBUG
                callback_data.n_search_hits = nHitsPoly;
              #endif
              spatial_search_rectangle (units->spatial_index,
                                        boundary[0] - EPSILON, boundary[1] - EPSILON,
                                        boundary[2] + EPSILON, boundary[3] + EPSILON,
                                        check_poly_and_rezone, &callback_data);
            }                   /* end of loop over holes */
        }                       /* end of loop over zones */

      /* Clean up. */
      g_free (callback_data.fragment_containing_focus);
      for (i = 0; i < nzones; i++)
        {
          if (holes[i] == NULL)
            continue;
          else if (holes[i]->num_contours == 0)
            /* gpc_free_polygon doesn't like polygons with zero contours! */
            free (holes[i]);
          else
            gpc_free_polygon (holes[i]);
        }
      g_free (holes);
    }                           /* end of loop over pending foci */

  #if DEBUG
    if( NULL != adsm_report_search_hits )
      {
        for( i = 0; i < report_array_size; ++i )
          adsm_report_search_hits( ZON_zone_list_get( zones, i )->level,
                                   nHitsCircle[i], nHitsCircle[i],
                                   nHitsPoly[i], nHitsPoly[i] );
      }

    g_free( nHitsCircle );
    g_free( nHitsPoly );
  #endif

end:
  #if DEBUG
    g_debug ("----- EXIT handle_midnight_event (%s)", MODEL_NAME);
  #endif

  return;
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
    case EVT_BeforeEachSimulation:
      handle_before_each_simulation_event (self, zones);
      break;
    case EVT_RequestForZoneFocus:
      handle_request_for_zone_focus_event (self, &(event->u.request_for_zone_focus), zones);
      break;
    case EVT_Midnight:
      handle_midnight_event(self, units, zones, &(event->u.midnight), queue);
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
  local_data_t *local_data;
  GString *s;
  guint nzones, i;
  ZON_zone_t *zone;

  local_data = (local_data_t *) (self->model_data);
  s = g_string_new (NULL);
  g_string_append_printf (s, "<%s", MODEL_NAME);
  nzones = ZON_zone_list_length (local_data->zones);
  for (i = 0; i < nzones; i++)
    {
      zone = ZON_zone_list_get (local_data->zones, i);
      g_string_append_printf (s, "\n  \"%s\" level=%i radius=%.2f",
                              zone->name, zone->level, zone->radius);
    }
  g_string_append_c (s, '>');

  /* don't return the wrapper object */
  return g_string_free (s, /* free_segment = */ FALSE);
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

  /* When freeing pending_foci, we just need to free the queue structure
   * itself, not the UNT_unit_t structures that each queue node points to. */
  g_queue_free (local_data->pending_foci);

  g_free (local_data);
  g_ptr_array_free (self->outputs, /* free_seg = */ TRUE); /* also frees all output variables */
  g_free (self);

  #if DEBUG
    g_debug ("----- EXIT free (%s)", MODEL_NAME);
  #endif
}



/**
 * Adds a set of parameters to a zone model.
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
  local_data_t *local_data = NULL;
  gchar *name;
  double radius;
  ZON_zone_t *zone = NULL;

  #if DEBUG
    g_debug ("----- ENTER set_params (%s)", MODEL_NAME);
  #endif

  self = (adsm_module_t *)data;
  local_data = (local_data_t *) (self->model_data);

  name = g_hash_table_lookup (dict, "name");
  if (name != NULL)
    {
      name = g_utf8_normalize (name, -1, G_NORMALIZE_DEFAULT);
      g_assert (name != NULL);
    }
  else
    {
      name = g_strdup ("unnamed zone");
    }

  errno = 0;
  radius = strtod (g_hash_table_lookup (dict, "radius"), NULL);
  g_assert (errno != ERANGE);
  /* Radius must be positive. */
  if (radius < 0)
    {
      g_warning ("zone radius cannot be negative, setting to 0");
      radius = 0;
    }

  zone = ZON_new_zone (name, radius);
  g_free (name);

  /* Add the zone object to the zone list. */
  ZON_zone_list_append (local_data->zones, zone);

  #if DEBUG
    g_debug ("----- EXIT set_params (%s)", MODEL_NAME);
  #endif

  return 0;
}



/**
 * Returns a new zone model.
 */
adsm_module_t *
new (sqlite3 * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones, GError **error)
{
  adsm_module_t *self;
  local_data_t *local_data;
  EVT_event_type_t events_listened_for[] = {
    EVT_BeforeEachSimulation,
    EVT_RequestForZoneFocus,
    EVT_Midnight,
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

  local_data->units = units;
  local_data->zones = zones;
  local_data->pending_foci = g_queue_new ();

  /* Call the set_params function to read the production type combination
   * specific parameters. */
  sqlite3_exec_dict (params,
                     "SELECT name,radius FROM ScenarioCreator_zone ORDER BY radius",
                     set_params, self, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }

  #if DEBUG
    g_debug ("----- EXIT new (%s)", MODEL_NAME);
  #endif

  return self;
}

/* end of file zone_model.c */
