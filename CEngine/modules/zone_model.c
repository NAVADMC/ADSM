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
#  include <config.h>
#endif

/* To avoid name clashes when multiple modules have the same interface. */
#define is_singleton zone_model_is_singleton
#define new zone_model_new
#define set_params zone_model_set_params
#define run zone_model_run
#define reset zone_model_reset
#define events_listened_for zone_model_events_listened_for
#define is_listening_for zone_model_is_listening_for
#define has_pending_actions zone_model_has_pending_actions
#define has_pending_infections zone_model_has_pending_infections
#define to_string zone_model_to_string
#define local_printf zone_model_printf
#define local_fprintf zone_model_fprintf
#define local_free zone_model_free
#define handle_midnight_event zone_model_handle_midnight_event
#define handle_new_day_event zone_model_handle_new_day_event

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

#include "zone_model.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "zone-model"



#define NEVENTS_LISTENED_FOR 2
EVT_event_type_t events_listened_for[] = {
  EVT_Midnight,
  EVT_NewDay
};



/* Specialized information for this model. */
typedef struct
{
  ZON_zone_t *zone;
  RPT_reporting_t *num_fragments;
  RPT_reporting_t *num_holes_filled;
  RPT_reporting_t *cumul_num_holes_filled;
}
param_block_t;



typedef struct
{
  UNT_unit_list_t * units;
  ZON_zone_list_t * zones;

  GPtrArray * param_blocks;
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
 * Special structure for use with the callback functions below.
 */
typedef struct
{
  double x, y;
  UNT_unit_list_t *units;
  UNT_unit_t *unit;
  ZON_zone_list_t *zones;
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

                  zone_update.unit_index = unit->index;
                  zone_update.zone_level = zone->level;
				  
#ifdef USE_SC_GUILIB
                  sc_record_zone_change( unit, zone );
#else				  
                  if( NULL != spreadmodel_record_zone_change )
                    {
                      spreadmodel_record_zone_change( zone_update );
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

              zone_update.unit_index = unit->index;
              zone_update.zone_level = zone->level;
			  
#ifdef USE_SC_GUILIB
			  sc_record_zone_change( unit, zone );
#else			  
			  if( NULL != spreadmodel_record_zone_change )
                {
                  spreadmodel_record_zone_change( zone_update );
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
 * Responds to a midnight event by updating the zone shapes and unit-to-zone
 * assignments.
 *
 * @param self the model.
 * @param units a unit list.
 * @param zones a zone list.
 * @param event a midnight event.
 */
void
handle_midnight_event (struct spreadmodel_model_t_ *self,
                       UNT_unit_list_t * units,
                       ZON_zone_list_t * zones,
                       EVT_midnight_event_t * event)
{
  unsigned int nzones;
  double x, y;
  ZON_pending_focus_t *pending_focus;
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

  while (!g_queue_is_empty (zones->pending_foci))
    {
      pending_focus = (ZON_pending_focus_t *) g_queue_pop_head (zones->pending_foci);
      x = pending_focus->x;
      y = pending_focus->y;
      #if DEBUG
        g_debug ("focus to add at x=%g, y=%g", x, y);
      #endif
      g_free (pending_focus);

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
      callback_data.units = units;
      callback_data.zones = zones;
      
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
  if( NULL != spreadmodel_report_search_hits )
    {
      for( i = 0; i < report_array_size; ++i )
        spreadmodel_report_search_hits( ZON_zone_list_get( zones, i )->level,
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
 */
static void param_block_reporting (gpointer data, gpointer user_data)
{
  param_block_t *param_block = (param_block_t *) data;
  ZON_zone_t *zone = param_block->zone;

  if (param_block->num_fragments->frequency != RPT_never)
    RPT_reporting_set_integer1 (param_block->num_fragments,
                                g_queue_get_length (zone->fragments),
                                zone->name);
  if (param_block->num_holes_filled->frequency != RPT_never)
    RPT_reporting_set_integer1 (param_block->num_holes_filled,
                                zone->nholes_filled, zone->name);
  if (param_block->cumul_num_holes_filled->frequency != RPT_never)
    RPT_reporting_add_integer1 (param_block->cumul_num_holes_filled,
                                zone->nholes_filled, zone->name);
}



/**
 * Responds to a new day event by updating the reporting variables.
 *
 * @param self the model.
 * @param event a new day event.
 */
void
handle_new_day_event (struct spreadmodel_model_t_ *self, EVT_new_day_event_t * event)
{
  local_data_t *local_data;

#if DEBUG
  g_debug ("----- ENTER handle_new_day_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  g_ptr_array_foreach (local_data->param_blocks,
                       param_block_reporting,
                       NULL);

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
run (struct spreadmodel_model_t_ *self, UNT_unit_list_t * units,
     ZON_zone_list_t * zones, EVT_event_t * event, RAN_gen_t * rng, EVT_event_queue_t * queue)
{
#if DEBUG
  g_debug ("----- ENTER run (%s)", MODEL_NAME);
#endif

  switch (event->type)
    {
    case EVT_NewDay:
      handle_new_day_event (self, &(event->u.new_day));
      break;
    case EVT_Midnight:
      handle_midnight_event(self, units, zones, &(event->u.midnight));
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
 */
static void param_block_reset_reporting (gpointer data, gpointer user_data)
{
  param_block_t *param_block = (param_block_t *) data;

  RPT_reporting_zero (param_block->num_fragments);
  RPT_reporting_zero (param_block->cumul_num_holes_filled);
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

  g_ptr_array_foreach (local_data->param_blocks,
                       param_block_reset_reporting,
                       NULL);

#if DEBUG
  g_debug ("----- EXIT reset (%s)", MODEL_NAME);
#endif
}



/**
 * Reports whether this model is listening for a given event type.
 *
 * @param self the model.
 * @param event_type an event type.
 * @return TRUE if the model is listening for the event type.
 */
gboolean
is_listening_for (struct spreadmodel_model_t_ *self, EVT_event_type_t event_type)
{
  int i;

  for (i = 0; i < self->nevents_listened_for; i++)
    if (self->events_listened_for[i] == event_type)
      return TRUE;
  return FALSE;
}



/**
 * Reports whether this model has any pending actions to carry out.
 *
 * @param self the model.
 * @return TRUE if the model has pending actions.
 */
gboolean
has_pending_actions (struct spreadmodel_model_t_ * self)
{
  return FALSE;
}



/**
 * Reports whether this model has any pending infections to cause.
 *
 * @param self the model.
 * @return TRUE if the model has pending infections.
 */
gboolean
has_pending_infections (struct spreadmodel_model_t_ * self)
{
  return FALSE;
}



/**
 */
static void param_block_to_string (gpointer data, gpointer user_data)
{
  param_block_t *param_block = (param_block_t *) data;
  ZON_zone_t *zone = param_block->zone;
  GString *s = (GString *) user_data;

  zone = param_block->zone;

  g_string_append_printf (s,
                          "<\"%s\" level=%i radius=%.2f >\n",
                          zone->name,
                          zone->level,
                          zone->radius);
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
  char *chararray;
  local_data_t *local_data;

  local_data = (local_data_t *) (self->model_data);
  s = g_string_new (NULL);

  g_string_printf(s, "<%s\n", MODEL_NAME);
  g_ptr_array_foreach (local_data->param_blocks, param_block_to_string, s);
  g_string_printf(s, ">");

  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Prints this model to a stream.
 *
 * @param stream a stream to write to.
 * @param self the model.
 * @return the number of characters printed (not including the trailing '\\0').
 */
int
local_fprintf (FILE * stream, struct spreadmodel_model_t_ *self)
{
  char *s;
  int nchars_written;

  s = to_string (self);
  nchars_written = fprintf (stream, "%s", s);
  free (s);
  return nchars_written;
}



/**
 * Prints this model.
 *
 * @param self the model.
 * @return the number of characters printed (not including the trailing '\\0').
 */
int
local_printf (struct spreadmodel_model_t_ *self)
{
  return local_fprintf (stdout, self);
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
#if 0
  RPT_free_reporting (local_data->num_fragments);
  RPT_free_reporting (local_data->num_holes_filled);
  RPT_free_reporting (local_data->cumul_num_holes_filled);
#endif
  g_ptr_array_free (local_data->param_blocks, TRUE);
  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Returns whether this model is a singleton or not.
 */
gboolean
is_singleton (void)
{
  return TRUE;
}



/**
 * Adds a set of parameters to a zone model.
 */
void
set_params (struct spreadmodel_model_t_ *self, PAR_parameter_t * params)
{
  local_data_t *local_data = NULL;
  param_block_t *param_block = NULL;
  scew_element const *e;
  scew_element **ee;
  unsigned int noutputs;
  RPT_reporting_t *output;
  const XML_Char *variable_name;
  gboolean success;
  int i, j;
  char *tmp, *name;
  int level;
  double radius;

#if DEBUG
  g_debug ("----- ENTER set_params (%s)", MODEL_NAME);
#endif

  /* Make sure the right XML subtree was sent. */
  g_assert (strcmp (scew_element_name (params), MODEL_NAME) == 0);

  local_data = (local_data_t *) (self->model_data);

  param_block = g_new0 (param_block_t, 1);

  e = scew_element_by_name (params, "name");
  if (e != NULL)
    {
      /* Expat stores the text as UTF-8.  Convert to ISO-8859-1. */
      tmp = PAR_get_text (e);
      name = g_convert_with_fallback (tmp, -1, "ISO-8859-1", "UTF-8", "?", NULL, NULL, NULL);
      g_assert (name != NULL);
      g_free (tmp);
    }
  else
    name = g_strdup ("unnamed zone");

  e = scew_element_by_name (params, "level");
  if (e != NULL)
    {
      level = PAR_get_unitless (e, &success);
      if (success == FALSE)
        {
          /* This value will be re-assigned later, when the zone is added to
           * the zone list. */
          level = -1;
        }
    }
  else
    level = -1;

  e = scew_element_by_name (params, "radius");
  if (e != NULL)
    {
      radius = PAR_get_length (e, &success);
      if (success == FALSE)
        {
          g_warning ("setting zone radius to 0");
          radius = 0;
        }
      /* Radius must be positive. */
      if (radius < 0)
        {
          g_warning ("zone radius cannot be negative, setting to 0");
          radius = 0;
        }
    }
  else
    {
      g_warning ("zone radius missing, setting to 0");
      radius = 0;
    }

  param_block->zone = ZON_new_zone (name, level, radius);

  {
    GString * s = g_string_new (NULL);

    g_string_printf (s, "%s-num-fragments", name);
    param_block->num_fragments =
      RPT_new_reporting (s->str, RPT_group, RPT_never);

    g_string_printf (s, "%s-num-holes-filled", name);
    param_block->num_holes_filled =
      RPT_new_reporting (s->str, RPT_group, RPT_never);

    g_string_printf (s, "%s-cumulative-num-holes-filled", name);
    param_block->cumul_num_holes_filled =
      RPT_new_reporting (s->str, RPT_group, RPT_never);

    g_string_free(s, TRUE);
  }
  g_free (name);

  g_ptr_array_add (self->outputs, param_block->num_fragments);
  g_ptr_array_add (self->outputs, param_block->num_holes_filled);
  g_ptr_array_add (self->outputs, param_block->cumul_num_holes_filled);

  /* Set the reporting frequency for the output variables. */
  ee = scew_element_list (params, "output", &noutputs);
#if DEBUG
  g_debug ("%i output variables", noutputs);
#endif
  for (i = 0; i < noutputs; i++)
    {
      GString * long_variable_name = g_string_new (NULL);

      e = ee[i];
      variable_name = scew_element_contents (scew_element_by_name (e, "variable-name"));
      g_string_printf (long_variable_name, "%s-%s", name, variable_name);
      /* Do the outputs include a variable with this name? */
      for (j = 0; j < self->outputs->len; j++)
        {
          output = (RPT_reporting_t *) g_ptr_array_index (self->outputs, j);
          if ((strcmp (output->name, variable_name) == 0) ||
              (strcmp (output->name, long_variable_name->str) == 0))
            break;
        }
      if (j == self->outputs->len)
        g_warning ("no output variable named \"%s\", ignoring", variable_name);
      else
        {
          RPT_reporting_set_frequency (output,
                                       RPT_string_to_frequency (scew_element_contents
                                                                (scew_element_by_name
                                                                 (e, "frequency"))));
#if DEBUG
          g_debug ("report \"%s\" %s", variable_name, RPT_frequency_name[output->frequency]);
#endif
        }

      g_string_free(long_variable_name, TRUE);
    }
  free (ee);

  /* Add the zone object to the zone list. */
  ZON_zone_list_append (local_data->zones, param_block->zone);

  /* Add the param_block to the list (for the singleton model). */
  g_ptr_array_add (local_data->param_blocks, param_block);

#if DEBUG
  g_debug ("----- EXIT set_params (%s)", MODEL_NAME);
#endif

  return;
}



/**
 * Returns a new zone model.
 */
spreadmodel_model_t *
new (scew_element * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  spreadmodel_model_t *self;
  local_data_t *local_data;

#if DEBUG
  g_debug ("----- ENTER new (%s)", MODEL_NAME);
#endif

  self = g_new (spreadmodel_model_t, 1);
  local_data = g_new (local_data_t, 1);

  self->name = MODEL_NAME;
  self->events_listened_for = events_listened_for;
  self->nevents_listened_for = NEVENTS_LISTENED_FOR;
  self->outputs = g_ptr_array_sized_new (3);
  self->model_data = local_data;
  self->set_params = set_params;
  self->run = run;
  self->reset = reset;
  self->is_listening_for = is_listening_for;
  self->has_pending_actions = has_pending_actions;
  self->has_pending_infections = has_pending_infections;
  self->to_string = to_string;
  self->printf = local_printf;
  self->fprintf = local_fprintf;
  self->free = local_free;

  local_data->units = units;
  local_data->zones = zones;

  local_data->param_blocks = g_ptr_array_new();

  /* Send the XML subtree to the init function to read the production type
   * combination specific parameters. */
  self->set_params (self, params);

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file zone_model.c */
