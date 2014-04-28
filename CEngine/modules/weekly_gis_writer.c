/**
 * Writes out ArcView shapefiles giving weekly snapshots of the unit states and
 * the zones for the first Monte Carlo iteration.
 *
 * Unit state files are the same as the base file name but with _dayxxxx
 * appended. Zone files are the same as the base file name but with
 * _zones_dayxxxx appended.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
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
#define new weekly_gis_writer_new
#define run weekly_gis_writer_run
#define reset weekly_gis_writer_reset
#define events_listened_for weekly_gis_writer_events_listened_for
#define to_string weekly_gis_writer_to_string
#define local_free weekly_gis_writer_free
#define handle_output_dir_event weekly_gis_writer_handle_output_dir_event
#define handle_new_day_event weekly_gis_writer_handle_new_day_event

#include "module.h"
#include <shapefil.h>
#include <string.h>

#include "weekly_gis_writer.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "weekly-gis-writer"



#define NEVENTS_LISTENED_FOR 2
EVT_event_type_t events_listened_for[] = {
  EVT_OutputDirectory,
  EVT_NewDay
};



/* Specialized information for this module. */
typedef struct
{
  char *base_filename; /**< Base name for the ArcView output files, without the
    .shp at the end. */
  projPJ projection; /**< The map projection used to convert between lat-long
    and x-y coordinates. */
  guint seen_day_1; /**< A count of how many times a New Day event with day
    number 1 has been seen. Useful for ignoring everything past the first
    Monte Carlo iteration. */
  guint max_state_name_length; /**< The length of the longest disease state
    name. Used to set the width of the state field in the ArcView attribute
    (.dbf) file.*/
  guint max_prod_type_length; /**< The length of the longest production type
    name. Used to set the width of the field in the ArcView attribute (.dbf)
    file. */
  guint max_unit_id_length; /**< The length of the longest unit ID. Used to set
    the width of the name field in the ArcView attribute (.dbf) file. */
  guint max_zone_name_length; /**< The length of the longest zone name. Used to
    set the width of the name field in the ArcView attribute (.dbf) file. */
}
local_data_t;



/**
 * Responds to an "output directory" event by prepending the directory to
 * its base output filename.
 *
 * @param self this module.
 * @param event an output directory event.
 */
void
handle_output_dir_event (struct spreadmodel_model_t_ * self,
                         EVT_output_dir_event_t *event)
{
  local_data_t *local_data;
  char *tmp;

  #if DEBUG
    g_debug ("----- ENTER handle_output_dir_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);

  tmp = local_data->base_filename;
  local_data->base_filename = g_build_filename (event->output_dir, tmp, NULL);
  g_free (tmp);
  #if DEBUG
    g_debug ("base filename is now %s", local_data->base_filename);
  #endif

  #if DEBUG
    g_debug ("----- EXIT handle_output_dir_event (%s)", MODEL_NAME);
  #endif
  return;
}



/**
 * Returns the length of the longest unit state name.
 */
static guint
max_state_name_length (void)
{
  guint i;
  guint len;
  guint max = 0;

  for (i = 0; i < UNT_NSTATES; i++)
    {
      len = strlen (UNT_state_name[i]);
      if (len > max)
        max = len;
    }
  return max;
}



/**
 * Returns the length of the longest production type name.
 */
static guint
max_prod_type_length (GPtrArray *production_type_names)
{
  guint i, n;
  guint len;
  guint max = 0;

  n = production_type_names->len;
  for (i = 0; i < n; i++)
    {
      len = strlen ((char *) g_ptr_array_index (production_type_names, i));
      if (len > max)
        max = len;
    }
  return max;
}



/**
 * Returns the length of the longest unit ID.
 */
static guint
max_unit_id_length (UNT_unit_list_t * units)
{
  guint i, n;
  UNT_unit_t *unit;
  guint len;
  guint max = 0;

  n = UNT_unit_list_length (units);
  for (i = 0; i < n; i++)
    {
      unit = UNT_unit_list_get (units, i);
      len = (unit->official_id != NULL) ? strlen (unit->official_id) : 0;
      if (len > max)
        max = len;
    }
  return max;
}



/**
 * Returns the length of the longest zone name.
 */
static guint
max_zone_name_length (ZON_zone_list_t *zones)
{
  guint i, n;
  ZON_zone_t *zone;
  guint len;
  guint max = 0;

  n = ZON_zone_list_length (zones);
  for (i = 0; i < n; i++)
    {
      zone = ZON_zone_list_get (zones, i);
      len = g_utf8_strlen (zone->name, -1);
      if (len > max)
        max = len;
    }
  return max;
}



static void
write_units_shapefile (local_data_t *local_data,
                       UNT_unit_list_t *units,
                       int day)
{
  guint nunits, i;
  UNT_unit_t *unit;
  double x, y;
  double minbound[2], maxbound[2];

  char *shape_filename;
  SHPHandle shape_file = NULL;
  SHPObject *loc;
  int shape_id;

  char *dbf_filename;
  DBFHandle dbf_file = NULL;
  int attribute_id[5];

  #if DEBUG
    g_debug ("----- ENTER write_units_shapefile (%s)", MODEL_NAME);
  #endif

  /* We are going to write 2 files: the .shp file, containing the locations of
   * the units, and the .dbf file, containing the numeric and text attributes
   * attached to the units. */

  shape_filename = g_strdup_printf ("%s_day%04i.shp", local_data->base_filename, day);
  #if DEBUG
    g_debug ("creating new shapefile \"%s\"", shape_filename);
  #endif
  shape_file = SHPCreate (shape_filename, SHPT_POINT); /* will contain points */
  g_assert (shape_file != NULL);

  dbf_filename = g_strdup_printf ("%s_day%04i.dbf", local_data->base_filename, day);
  #if DEBUG
    g_debug ("creating new attributes file \"%s\"", dbf_filename);
  #endif
  dbf_file = DBFCreate (dbf_filename);
  g_assert (dbf_file != NULL);
  attribute_id[0] = DBFAddField (dbf_file, "seq", FTInteger, 9, 0);
  attribute_id[1] = DBFAddField (dbf_file, "id", FTString, MAX (1, local_data->max_unit_id_length), 0);
  attribute_id[2] = DBFAddField (dbf_file, "prodtype", FTString, local_data->max_prod_type_length, 0);
  attribute_id[3] = DBFAddField (dbf_file, "size", FTInteger, 9, 0);
  attribute_id[4] = DBFAddField (dbf_file, "status", FTString, local_data->max_state_name_length, 0);

  /* The 1 in the argument list is the number of points. */
  loc = SHPCreateSimpleObject (SHPT_POINT, 1, &x, &y, NULL);

  nunits = UNT_unit_list_length (units);
  for (i = 0; i < nunits; i++)
    {
      unit = UNT_unit_list_get (units, i);
      x = unit->longitude;
      y = unit->latitude;

      /* Keep track of the minimum and maximum x and y values, in case the
       * shapefile library gets them wrong. */
      if (i == 0)
        {
          minbound[0] = maxbound[0] = x;
          minbound[1] = maxbound[1] = y;
        }
      else
        {
          if (x < minbound[0])
            minbound[0] = x;
          else if (x > maxbound[0])
            maxbound[0] = x;
          if (y < minbound[1])
            minbound[1] = y;
          else if (y > maxbound[1])
            maxbound[1] = y;
        }

      loc->padfX[0] = x;
      loc->padfY[0] = y;
      SHPComputeExtents (loc);
      /* The -1 is the library's code for creating a new object in the
       * shapefile as opposed to overwriting an existing one. */
      shape_id = SHPWriteObject (shape_file, -1, loc);
      DBFWriteIntegerAttribute (dbf_file, shape_id, attribute_id[0], i);
      if (unit->official_id != NULL)
        DBFWriteStringAttribute (dbf_file, shape_id, attribute_id[1], unit->official_id);
      else
        DBFWriteStringAttribute (dbf_file, shape_id, attribute_id[1], "");
      DBFWriteStringAttribute (dbf_file, shape_id, attribute_id[2], unit->production_type_name);
      DBFWriteIntegerAttribute (dbf_file, shape_id, attribute_id[3], unit->size);
      DBFWriteStringAttribute (dbf_file, shape_id, attribute_id[4], UNT_state_name[unit->state]);
    }

  /* Sometimes the shapefile library gets the extents wrong. Check the computed
   * extents against the ones cached in the SHPHandle object. */
  if (minbound[0] != shape_file->adBoundsMin[0])
    {
      g_warning ("minimum x in SHPHandle (%g) != computed min (%g)", shape_file->adBoundsMin[0],
                 minbound[0]);
      shape_file->adBoundsMin[0] = minbound[0];
    }
  if (maxbound[0] != shape_file->adBoundsMax[0])
    {
      g_warning ("maximum x in SHPHandle (%g) != computed max (%g)", shape_file->adBoundsMax[0],
                 maxbound[0]);
      shape_file->adBoundsMax[0] = maxbound[0];
    }
  if (minbound[1] != shape_file->adBoundsMin[1])
    {
      g_warning ("minimum y in SHPHandle (%g) != computed min (%g)", shape_file->adBoundsMin[1],
                 minbound[1]);
      shape_file->adBoundsMin[1] = minbound[1];
    }
  if (maxbound[1] != shape_file->adBoundsMax[1])
    {
      g_warning ("maximum y in SHPHandle (%g) != computed max (%g)", shape_file->adBoundsMax[1],
                 maxbound[1]);
      shape_file->adBoundsMax[1] = maxbound[1];
    }

  /* Clean up. */
  SHPDestroyObject (loc);
  if (shape_file != NULL)
    SHPClose (shape_file);
  g_free (shape_filename);
  if (dbf_file != NULL)
    DBFClose (dbf_file);
  g_free (dbf_filename);

  #if DEBUG
    g_debug ("----- EXIT write_units_shapefile (%s)", MODEL_NAME);
  #endif
  
  return;
}



static void
write_zones_shapefile (local_data_t *local_data,
                       ZON_zone_list_t *zones,
                       int day)
{
  guint nzones;
  int i;
  unsigned int j, k;
  ZON_zone_t *zone;

  char *shape_filename;
  SHPHandle shape_file = NULL;
  SHPObject *shape;
  int shape_id;

  char *dbf_filename;
  DBFHandle dbf_file = NULL;
  int name_field;

  #if DEBUG
    g_debug ("----- ENTER write_zones_shapefile (%s)", MODEL_NAME);
  #endif

  /* We are going to write 2 files: the .shp file, containing the locations of
   * the units, and the .dbf file, containing the numeric and text attributes
   * attached to the units. */

  shape_filename = g_strdup_printf ("%s_zones_day%04i.shp", local_data->base_filename, day);
  #if DEBUG
    g_debug ("creating new shapefile \"%s\"", shape_filename);
  #endif
  shape_file = SHPCreate (shape_filename, SHPT_POLYGON);
  g_assert (shape_file != NULL);

  dbf_filename = g_strdup_printf ("%s_zones_day%04i.dbf", local_data->base_filename, day);
  #if DEBUG
    g_debug ("creating new attributes file \"%s\"", dbf_filename);
  #endif
  dbf_file = DBFCreate (dbf_filename);
  g_assert (dbf_file != NULL);
  name_field = DBFAddField (dbf_file, "name", FTString, local_data->max_zone_name_length, 0);

  nzones = ZON_zone_list_length (zones);
  for (i = nzones - 1; i >= 0; i--)
    {
      gpc_polygon *poly;
      int *panPartStart;
      int nVertices;
      double *padfX, *padfY;
      int vert_index;
      gchar *name;

      zone = ZON_zone_list_get (zones, i);
      poly = zone->poly;
      if (poly == NULL || poly->num_contours == 0)
        continue;

      /* The Shapefile format requires the vertices for all contours to be
       * combined in a single array of x values and a single array of y values.
       * Get a count of the vertices and allocate the arrays. */
      panPartStart = g_new (int, poly->num_contours);
      nVertices = 0;
      for (j = 0; j < poly->num_contours; j++)
        {
          panPartStart[j] = nVertices;
          nVertices += poly->contour[j].num_vertices;
        }
      padfX = g_new (double, nVertices);
      padfY = g_new (double, nVertices);

      /* Copy the vertices into the separate x and y arrays. */
      for (j = 0, vert_index = 0; j < poly->num_contours; j++)
        {
          gpc_vertex_list *contour;
          gpc_vertex *vertex;
          unsigned int n;
          projUV p;

          contour = &(poly->contour[j]);
          n = contour->num_vertices;
          for (k = 0; k < n; k++)
            {
              vertex = &(contour->vertex[k]);

              /* The polygon vertices are in x-y coordinates.  We need to
               * "unproject" them back to lat-long. */
              p.u = vertex->x;
              p.v = vertex->y;
              p = pj_inv (p, local_data->projection);
              padfX[vert_index] = p.u * RAD_TO_DEG;
              padfY[vert_index] = p.v * RAD_TO_DEG;
              vert_index++;
            }
        }
      
      shape = SHPCreateObject (SHPT_POLYGON, -1, poly->num_contours,
                               panPartStart, NULL, nVertices, padfX, padfY,
                               NULL, NULL);
      /* The -1 is the library's code for creating a new object in the
       * shapefile as opposed to overwriting an existing one. */
      shape_id = SHPWriteObject (shape_file, -1, shape);
      /* Convert the zone's name from UTF-8 to ISO-8859-1. (Will this work or
       * does it need to be ASCII?) */
      name = g_convert_with_fallback (zone->name, -1, "ISO-8859-1", "UTF-8", "?", NULL, NULL, NULL);
      DBFWriteStringAttribute (dbf_file, shape_id, name_field, name);
      g_free (name);
      #if DEBUG
        g_debug ("wrote shape for \"%s\" zone", zone->name);
      #endif

      SHPDestroyObject (shape);
      g_free (panPartStart);
      g_free (padfX);
      g_free (padfY);
    }

  /* Clean up. */
  if (shape_file != NULL)
    SHPClose (shape_file);
  g_free (shape_filename);
  if (dbf_file != NULL)
    DBFClose (dbf_file);
  g_free (dbf_filename);

  #if DEBUG
    g_debug ("----- EXIT write_zones_shapefile (%s)", MODEL_NAME);
  #endif
  
  return;
}



/**
 * Responds to an "new day" event by writing GIS files for the units states
 * and the zones.
 *
 * @param self this module.
 * @param event a new day event.
 * @param units the list of units.
 * @param zones the list of zones. 
 */
void
handle_new_day_event (struct spreadmodel_model_t_ * self,
                      EVT_new_day_event_t *event,
                      UNT_unit_list_t *units,
                      ZON_zone_list_t *zones)
{
  local_data_t *local_data;

  #if DEBUG
    g_debug ("----- ENTER handle_new_day_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);

  if (event->day == 1)
    local_data->seen_day_1 += 1;

  if ((local_data->seen_day_1 < 2) && (event->day % 7 == 1))
    {
      write_units_shapefile (local_data, units, event->day);
      write_zones_shapefile (local_data, zones, event->day);
    }
    
  #if DEBUG
    g_debug ("----- EXIT handle_new_day_event (%s)", MODEL_NAME);
  #endif
  return;
}




/**
 * Runs this module.
 *
 * @param self this module.
 * @param units a list of units.
 * @param zones a list of zones.
 * @param event the event that caused this module to run.
 * @param rng a random number generator.
 * @param queue for any new events this module creates.
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
    case EVT_OutputDirectory:
      handle_output_dir_event (self, &(event->u.output_dir));
      break;
    case EVT_NewDay:
      handle_new_day_event (self, &(event->u.new_day), units, zones);
      break;
    default:
      g_error
        ("%s has received a %s event, which it does not listen for.  This should never happen.  Please contact the developer.",
         MODEL_NAME, EVT_event_type_name[event->type]);
    }

  #if DEBUG
    g_debug ("----- EXIT run (%s)", MODEL_NAME);
  #endif
  return;
}



/**
 * Resets this module after a simulation run.
 *
 * @param self this module.
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
  return;
}



/**
 * Returns a text representation of this module.
 *
 * @param self this module.
 * @return a string.
 */
char *
to_string (struct spreadmodel_model_t_ *self)
{
  local_data_t *local_data;
  GString *s;
  char *chararray;

  local_data = (local_data_t *) (self->model_data);
  s = g_string_new (NULL);
  g_string_sprintf (s, "<%s base_filename=\"%s.shp\"/\"%s_zones.shp\">",
                    MODEL_NAME,
                    local_data->base_filename,
                    local_data->base_filename);

  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Frees this module.
 *
 * @param self this module.
 */
void
local_free (struct spreadmodel_model_t_ *self)
{
  local_data_t *local_data;

  #if DEBUG
    g_debug ("----- ENTER free (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);

  /* Free the dynamically-allocated parts. */
  g_free (local_data->base_filename);

  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

  #if DEBUG
    g_debug ("----- EXIT free (%s)", MODEL_NAME);
  #endif
}



/**
 * Set the parameters for this module.
 */
void
set_params (struct spreadmodel_model_t_ *self, sqlite3 * params)
{
  local_data_t *local_data;

  #if DEBUG
    g_debug ("----- ENTER set_params (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);

  /* Get the base filename for the ArcView files.  If the filename is omitted
   * or blank, then "weekly_gis" is used. */
  local_data->base_filename = NULL;
  if (FALSE)
    {
      local_data->base_filename = NULL; /* PAR_get_text (e); */
      if (local_data->base_filename != NULL
          && g_ascii_strcasecmp (local_data->base_filename, "") == 0)
        {
          g_free (local_data->base_filename);
          local_data->base_filename = NULL;
        }
    }
  if (local_data->base_filename == NULL)
    local_data->base_filename = g_strdup ("weekly_gis");

  /* If there is a ".shp" already at the end of the filename, remove it. */
  if (g_str_has_suffix (local_data->base_filename, ".shp")) 
    {
      char *tmp;
      size_t len;
      len = strlen (local_data->base_filename);
      tmp = local_data->base_filename;
      local_data->base_filename = g_strndup (local_data->base_filename, len-4);
      g_free (tmp);
    }

  #if DEBUG
    g_debug ("----- EXIT set_params (%s)", MODEL_NAME);
  #endif

  return;
}



/**
 * Returns a new weekly GIS writer.
 */
spreadmodel_model_t *
new (sqlite3 * params, UNT_unit_list_t * units, projPJ projection,
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
  self->outputs = g_ptr_array_new ();
  self->model_data = local_data;
  self->run = run;
  self->reset = reset;
  self->is_listening_for = spreadmodel_model_is_listening_for;
  self->has_pending_actions = spreadmodel_model_answer_no;
  self->has_pending_infections = spreadmodel_model_answer_no;
  self->to_string = to_string;
  self->printf = spreadmodel_model_printf;
  self->fprintf = spreadmodel_model_fprintf;
  self->free = local_free;

  local_data->projection = projection;
  local_data->seen_day_1 = 0;
  local_data->max_state_name_length = max_state_name_length();
  local_data->max_prod_type_length = max_prod_type_length (units->production_type_names);
  local_data->max_unit_id_length = max_unit_id_length (units);
  local_data->max_zone_name_length = max_zone_name_length (zones);

  #if DEBUG
    g_debug ("----- EXIT new (%s)", MODEL_NAME);
  #endif

  return self;
}

/* end of file weekly_gis_writer.c */
