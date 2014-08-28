/**
 * Writes out an ArcView shapefile that shows summary information over a whole
 * set of Monte Caro trials.
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
#define new summary_gis_writer_new
#define run summary_gis_writer_run
#define reset summary_gis_writer_reset
#define to_string summary_gis_writer_to_string
#define local_free summary_gis_writer_free
#define handle_output_dir_event summary_gis_writer_handle_output_dir_event
#define handle_before_any_simulations_event summary_gis_writer_handle_before_any_simulations_event
#define handle_before_each_simulation_event summary_gis_writer_handle_before_each_simulation_event
#define handle_infection_event summary_gis_writer_handle_infection_event
#define handle_vaccination_event summary_gis_writer_handle_vaccination_event
#define handle_destruction_event summary_gis_writer_handle_destruction_event

#include "module.h"
#include "gis.h"
#include <math.h>
#include <gpcl/gpc.h>
#include <shapefil.h>
#include <string.h>

#include "summary_gis_writer.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "summary-gis-writer"



#define DEFAULT_GRID_SIZE 10 /* km */



/* Specialized information for this module. */
typedef struct
{
  char *base_filename; /**< Base name for the ArcView output files, without the
    .shp at the end. */
  double grid_size; /**< Length in km of the side of a grid square. Only used
    if the modeler does not provide a file of boundaries. */
  GPtrArray *polys; /**< Each pointer is a (gpc_polygon *). The polygons are
    defined in projected x-y coordinates, not lat-long pairs. */
  guint max_nvertices; /**< Largest number of vertices in any polygon. */
  int *unit_map; /**< An array giving the polygon to which each unit maps.
    If the unit is not in any polygon, that entry is -1.  The length of this
    array is the number of units. */
  guint *unit_count; /**< A count of the number of units in each polygon.  The
    length of this array is the number of polgons. */
  guint nruns;
  GHashTable *infected; /**< If a unit has been infected during the current
    simulation run, it will be in this table as a key. Prevents double-counting. */
  GHashTable *vaccinated; /**< If a unit has been vaccinated during the current
    simulation run, it will be in this table as a key. Prevents double-counting. */
  GHashTable *destroyed; /**< If a unit has been destroyed during the current
    simulation run, it will be in this table as a key. Prevents double-counting. */
  double *ninfected; /**< Counts of the number of units in a polygon that were
    infected at any time during the current Monte Carlo run.  The length of
    this array is the number of polygons. */
  double *ndestroyed; /**< Counts of the number of units in a polygon that were
    destroyed during the current Monte Carlo run.  The length of this array is
    the number of polygons. */
  double *nvaccinated; /**< Counts of the number of units in a polygon that
    were vaccine immune at any time during the current Monte Carlo run.  The
    length of this array is the number of polygons. */
  projPJ projection; /**< The map projection used to convert between lat-long
    and x-y coordinates. */
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
handle_output_dir_event (struct adsm_module_t_ * self,
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



static void
map_units_to_polys (local_data_t *local_data, UNT_unit_list_t *units)
{
  guint nunits, i, npolys, j;
  int *map;
  guint *count;
  UNT_unit_t *unit;
  gpc_polygon *poly;
  gboolean found;
  guint units_not_in_any_poly = 0;

  #if DEBUG
    g_debug ("----- ENTER map_units_to_polys (%s)", MODEL_NAME);
  #endif

  npolys = local_data->polys->len;
  nunits = UNT_unit_list_length (units);
  map = local_data->unit_map;
  count = local_data->unit_count;

  /* Initialize all entries in the unit-to-polygon map to -1, meaning that the
   * unit isn't in any polygon. */
  for (i = 0; i < nunits; i++)
    map[i] = -1;

  for (i = 0; i < nunits; i++)
    {
      unit = UNT_unit_list_get (units, i);
      found = FALSE;
      for (j = 0; j < npolys && !found; j++)
        {
          poly = (gpc_polygon *) g_ptr_array_index (local_data->polys, j);
          if (GIS_point_in_polygon (poly, unit->x, unit->y))
            {
              found = TRUE;
              map[i] = j;
              count[j] += 1;
            }
        } /* end of loop over polygons */
      if (!found)
        units_not_in_any_poly++;
    } /* end of loop over units */

  #if DEBUG
    g_debug ("%u units not in any poly", units_not_in_any_poly);
  #endif

  #if DEBUG
    g_debug ("----- EXIT map_units_to_polys (%s)", MODEL_NAME);
  #endif

  return;
}



static void
create_grid (local_data_t *local_data, spatial_search_t *spatial_index)
{
  double dx, dy;
  guint h, v, npolys;
  double grid_min_x, grid_min_y;
  guint row, col;

  #if DEBUG
    g_debug ("----- ENTER create_grid (%s)", MODEL_NAME);
  #endif

  /* How many grid squares do we need to cover the horizontal and vertical
   * extents of the study area? */
  dx = spatial_index->max_x - spatial_index->min_x;
  dy = spatial_index->max_y - spatial_index->min_y;
  h = (guint)ceil(dx / local_data->grid_size);
  v = (guint)ceil(dy / local_data->grid_size);
  npolys = h * v;
  #if DEBUG
    g_debug ("creating %ux%u=%u grid squares to cover %g km x %g km area",
             h, v, npolys, dx, dy);
  #endif
  /* Define one corner of the grid. */
  grid_min_x = spatial_index->min_x - 0.5 * (h * local_data->grid_size - dx);
  grid_min_y = spatial_index->min_y - 0.5 * (v * local_data->grid_size - dy);

  /* Create the polygons. */
  for (row = 0; row < v; row++)
    {
      double y0, y1;
      y0 = grid_min_y + row * local_data->grid_size;
      y1 = y0 + local_data->grid_size;
      for (col = 0; col < h; col++)
        {
          double x0, x1;
          gpc_vertex_list *contour;
          gpc_polygon *grid_square;

          x0 = grid_min_x + col * local_data->grid_size;
          x1 = x0 + local_data->grid_size;
          contour = g_new (gpc_vertex_list, 1);
          contour->num_vertices = 4;
          contour->vertex = g_new (gpc_vertex, 4);
          contour->vertex[0].x = x0;
          contour->vertex[0].y = y0;
          contour->vertex[1].x = x1;
          contour->vertex[1].y = y0;
          contour->vertex[2].x = x1;
          contour->vertex[2].y = y1;
          contour->vertex[3].x = x0;
          contour->vertex[3].y = y1;
          /* Wrap the contour in a polygon object. */
          grid_square = gpc_new_polygon ();
          gpc_add_contour (grid_square, contour, 0);
          g_ptr_array_add (local_data->polys, grid_square);
        }
    }
  g_assert (local_data->polys->len == npolys);

  /* Now that we know the number of polygons, initialize the unit_count,
   * ninfected, nvaccinated, and ndestroyed arrays. */
  g_assert (local_data->unit_count == NULL);
  local_data->max_nvertices = 4;
  local_data->unit_count = g_new0 (guint, npolys);
  local_data->ninfected = g_new0 (double, npolys);
  local_data->nvaccinated = g_new0 (double, npolys);
  local_data->ndestroyed = g_new0 (double, npolys);

  #if DEBUG
    g_debug ("----- EXIT create_grid (%s)", MODEL_NAME);
  #endif

  return;
}


             
/**
 * Before any simulations, this module:
 * - creates a grid around the study area, if needed
 * - determines which units are in which grid squares
 *
 * @param self the model.
 * @param units a list of units.
 */
void
handle_before_any_simulations_event (struct adsm_module_t_ *self,
                                     UNT_unit_list_t *units)
{
  local_data_t *local_data;

  #if DEBUG
    g_debug ("----- ENTER handle_before_any_simulations_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);

  create_grid (local_data, units->spatial_index);
  map_units_to_polys (local_data, units);

  #if DEBUG
    g_debug ("----- EXIT handle_before_any_simulations_event (%s)", MODEL_NAME);
  #endif
  return;
}



/**
 * Before each simulation, this module zeroes its counts of infected,
 * vaccinated, and destroyed units.
 *
 * @param self this module.
 */
void
handle_before_each_simulation_event (struct adsm_module_t_ * self)
{
  local_data_t *local_data;

  #if DEBUG
    g_debug ("----- ENTER handle_before_each_simulation_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);
  g_hash_table_remove_all (local_data->infected);
  g_hash_table_remove_all (local_data->vaccinated);
  g_hash_table_remove_all (local_data->destroyed);
  local_data->nruns += 1;

  #if DEBUG
    g_debug ("----- EXIT handle_before_each_simulation_event (%s)", MODEL_NAME);
  #endif
}



/**
 * Responds to an infection event by recording which unit was infected.
 *
 * @param self this module.
 * @param event an infection event.
 */
void
handle_infection_event (struct adsm_module_t_ * self,
                        EVT_infection_event_t * event)
{
  local_data_t *local_data;
  UNT_unit_t *unit;

  #if DEBUG
    g_debug ("----- ENTER handle_infection_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);
  unit = event->infected_unit;
  if (g_hash_table_lookup (local_data->infected, unit) == NULL)
    {
      int poly;
      g_hash_table_insert (local_data->infected, unit, GINT_TO_POINTER(1));
      poly = local_data->unit_map[unit->index];
      if (poly >= 0)
        local_data->ninfected[poly] += 1;
    }

  #if DEBUG
    g_debug ("----- EXIT handle_infection_event (%s)", MODEL_NAME);
  #endif
}



/**
 * Responds to a vaccination event by recording which unit was vaccinated.
 *
 * @param self this module.
 * @param event a vaccination event.
 */
void
handle_vaccination_event (struct adsm_module_t_ * self,
                          EVT_vaccination_event_t * event)
{
  local_data_t *local_data;
  UNT_unit_t *unit;

  #if DEBUG
    g_debug ("----- ENTER handle_vaccination_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;
  if (g_hash_table_lookup (local_data->vaccinated, unit) == NULL)
    {
      int poly;
      g_hash_table_insert (local_data->vaccinated, unit, GINT_TO_POINTER(1));
      poly = local_data->unit_map[unit->index];
      if (poly >= 0)
        local_data->nvaccinated[poly] += 1;
    }

  #if DEBUG
    g_debug ("----- EXIT handle_vaccination_event (%s)", MODEL_NAME);
  #endif
}



/**
 * Responds to a destruction event by recording which unit was destroyed.
 *
 * @param self this module.
 * @param event a destruction event.
 */
void
handle_destruction_event (struct adsm_module_t_ * self,
                          EVT_destruction_event_t * event)
{
  local_data_t *local_data;

  #if DEBUG
    g_debug ("----- ENTER handle_destruction_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);
  g_hash_table_insert (local_data->destroyed, event->unit, GINT_TO_POINTER(1));

  #if DEBUG
    g_debug ("----- EXIT handle_destruction_event (%s)", MODEL_NAME);
  #endif
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
run (struct adsm_module_t_ *self, UNT_unit_list_t * units,
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
    case EVT_BeforeAnySimulations:
      handle_before_any_simulations_event (self, units);
      break;
    case EVT_BeforeEachSimulation:
      handle_before_each_simulation_event (self);
      break;
    case EVT_Infection:
      handle_infection_event (self, &(event->u.infection));
      break;
    case EVT_Vaccination:
      handle_vaccination_event (self, &(event->u.vaccination));
      break;
    case EVT_Destruction:
      handle_destruction_event (self, &(event->u.destruction));
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
reset (struct adsm_module_t_ *self)
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
to_string (struct adsm_module_t_ *self)
{
  local_data_t *local_data;
  GString *s;
  char *chararray;

  local_data = (local_data_t *) (self->model_data);
  s = g_string_new (NULL);
  g_string_sprintf (s, "<%s base_filename=\"%s.shp\" grid_size=%g>",
                    MODEL_NAME,
                    local_data->base_filename,
                    local_data->grid_size);

  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



static
void write_shapefile (local_data_t *local_data)
{
  guint npolys;

  char *shape_filename;
  SHPHandle shape_file = NULL;
  SHPObject *shape;
  double *vertex_x, *vertex_y;
  guint i, j;
  projUV p;

  char *dbf_filename;
  DBFHandle dbf_file = NULL;
  int nunits_field_index;
  int avg_ninfected_field_index;
  int avg_ndestroyed_field_index;
  int avg_nvaccinated_field_index;
  int avg_frinfected_field_index;
  int avg_frdestroyed_field_index;
  int avg_frvaccinated_field_index;

  #if DEBUG
    g_debug ("----- ENTER write_shapefile (%s)", MODEL_NAME);
  #endif

  vertex_x = g_new (double, local_data->max_nvertices);
  vertex_y = g_new (double, local_data->max_nvertices);

  /* We are going to write 2 files: the .shp file, containing the geometry of
   * the polygons, and the .dbf file, containing the numeric attributes
   * attached to the polygons. */

  shape_filename = g_strdup_printf ("%s.shp", local_data->base_filename);
  #if DEBUG
    g_debug ("creating new shapefile \"%s\"", shape_filename);
  #endif
  shape_file = SHPCreate (shape_filename, SHPT_POLYGON);
  g_assert (shape_file != NULL);

  npolys = local_data->polys->len;
  for (i = 0; i < npolys; i++)
    {
      gpc_polygon *poly;
      gpc_vertex_list *contour;

      poly = (gpc_polygon *) g_ptr_array_index (local_data->polys, i);
      g_assert (poly->num_contours == 1);
      contour = &(poly->contour[0]);
      for (j = 0; j < contour->num_vertices; j++)
        {
          /* The polygon vertices are in x-y coordinates.  We need to
           * "unproject" them back to lat-long. */
          p.u = contour->vertex[j].x;
          p.v = contour->vertex[j].y;
          p = pj_inv (p, local_data->projection);
          vertex_x[j] = p.u * RAD_TO_DEG;
          vertex_y[j] = p.v * RAD_TO_DEG;
        }
      shape = SHPCreateSimpleObject (SHPT_POLYGON, j, vertex_x, vertex_y, NULL);
      SHPWriteObject (shape_file, -1, shape);
      SHPDestroyObject (shape);
    }
  if (shape_file != NULL)
    SHPClose (shape_file);
  g_free (shape_filename);

  /* Now the attribute file */

  dbf_filename = g_strdup_printf ("%s.dbf", local_data->base_filename);
  #if DEBUG
    g_debug ("creating new attributes file \"%s\"", dbf_filename);
  #endif
  dbf_file = DBFCreate (dbf_filename);
  g_assert (dbf_file != NULL);

  /* Add attribute definitions. */
  #if DEBUG
    g_debug ("adding field definitions to DBF file \"%s\": nunits, avgninf, avgndest, avgnvacc, avgfrinf, avgfrdest, avgfrvacc",
             dbf_filename);
  #endif
  /* 9-digit integers should be enough to count # of units in a polygon. */
  nunits_field_index = DBFAddField (dbf_file, "nunits", FTInteger, 9, 0);
  /* 1 decimal place for average # of units infected or destroyed, 3 for
   * average fraction of units. */
  avg_ninfected_field_index = DBFAddField (dbf_file, "avgninf", FTDouble, 9, 1);
  avg_ndestroyed_field_index = DBFAddField (dbf_file, "avgndest", FTDouble, 9, 1);
  avg_nvaccinated_field_index = DBFAddField (dbf_file, "avgnvacc", FTDouble, 9, 1);
  avg_frinfected_field_index = DBFAddField (dbf_file, "avgfrinf", FTDouble, 9, 3);
  avg_frdestroyed_field_index = DBFAddField (dbf_file, "avgfrdest", FTDouble, 9, 3);
  avg_frvaccinated_field_index = DBFAddField (dbf_file, "avgfrvacc", FTDouble, 9, 3);

  /* Write the attributes to the file. */
  #if DEBUG
    g_debug ("writing attributes to \"%s\"", dbf_filename);
  #endif
  for (i = 0; i < npolys; i++)
    {
      guint nunits;

      /* Divide the counts by the number of runs to get the mean */
      local_data->ninfected[i] /= local_data->nruns;
      local_data->ndestroyed[i] /= local_data->nruns;
      local_data->nvaccinated[i] /= local_data->nruns;

      nunits = local_data->unit_count[i];
      DBFWriteIntegerAttribute (dbf_file, i, nunits_field_index, nunits);
      DBFWriteDoubleAttribute (dbf_file, i, avg_ninfected_field_index, local_data->ninfected[i]);
      DBFWriteDoubleAttribute (dbf_file, i, avg_ndestroyed_field_index, local_data->ndestroyed[i]);
      DBFWriteDoubleAttribute (dbf_file, i, avg_nvaccinated_field_index, local_data->nvaccinated[i]);
      DBFWriteDoubleAttribute (dbf_file, i, avg_frinfected_field_index, local_data->ninfected[i] / nunits);
      DBFWriteDoubleAttribute (dbf_file, i, avg_frdestroyed_field_index, local_data->ndestroyed[i] / nunits);
      DBFWriteDoubleAttribute (dbf_file, i, avg_frvaccinated_field_index, local_data->nvaccinated[i] / nunits);
    }
  if (dbf_file != NULL)
    DBFClose (dbf_file);
  g_free (dbf_filename);

  /* Clean up. */
  g_free (vertex_y);
  g_free (vertex_x);

  #if DEBUG
    g_debug ("----- EXIT write_shapefile (%s)", MODEL_NAME);
  #endif
  
  return;
}



static
void free_polygon_as_GDestroyNotify (gpointer data)
{
  gpc_polygon *poly;
  
  poly = (gpc_polygon *)data;
  gpc_free_polygon (poly);
  g_free (poly);
  return;
}



/**
 * Frees this module.
 *
 * @param self this module.
 */
void
local_free (struct adsm_module_t_ *self)
{
  local_data_t *local_data;

  #if DEBUG
    g_debug ("----- ENTER free (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);

  /* Write the polygons to a file. */
  write_shapefile (local_data);

  /* Free the dynamically-allocated parts. */
  g_free (local_data->base_filename);
  g_ptr_array_free (local_data->polys, TRUE); /* This frees the polygons too
    since we set a function for freeing elements when we created the GPtrArray */
  g_free (local_data->unit_map);
  g_free (local_data->unit_count);
  g_free (local_data->ninfected);
  g_free (local_data->nvaccinated);
  g_free (local_data->ndestroyed);
  g_hash_table_destroy (local_data->infected);
  g_hash_table_destroy (local_data->vaccinated);
  g_hash_table_destroy (local_data->destroyed);

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
static void
set_params (struct adsm_module_t_ *self, sqlite3 * params)
{
  local_data_t *local_data;
  gboolean success;

  #if DEBUG
    g_debug ("----- ENTER set_params (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);

  /* Get the base filename for the ArcView files.table.  If the filename is
   * omitted or blank, then "summary_gis" is used. */
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
    local_data->base_filename = g_strdup ("summary_gis");

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

  /* Get the length of the side of a grid square. */
  if (FALSE)
    {
      local_data->grid_size = DEFAULT_GRID_SIZE /* PAR_get_length (e, &success) */;
      if (success == FALSE)
        {
          g_warning ("setting grid square side length to %g", DEFAULT_GRID_SIZE);
          local_data->grid_size = DEFAULT_GRID_SIZE;
        }
      /* Length must be positive. */
      if (local_data->grid_size <= 0)
        {
          g_warning ("grid square side length cannot be negative or zero, setting to %g",
                     DEFAULT_GRID_SIZE);
          local_data->grid_size = DEFAULT_GRID_SIZE;
        }
    }
  else
    {
      local_data->grid_size = DEFAULT_GRID_SIZE;
    }

  #if DEBUG
    g_debug ("----- EXIT set_params (%s)", MODEL_NAME);
  #endif

  return;
}



/**
 * Returns a new summary GIS writer.
 */
adsm_module_t *
new (sqlite3 * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  adsm_module_t *self;
  local_data_t *local_data;
  EVT_event_type_t events_listened_for[] = {
    EVT_OutputDirectory,
    EVT_BeforeAnySimulations,
    EVT_BeforeEachSimulation,
    EVT_Infection,
    EVT_Vaccination,
    EVT_Destruction,
    0
  };

  #if DEBUG
    g_debug ("----- ENTER new (%s)", MODEL_NAME);
  #endif

  self = g_new (adsm_module_t, 1);
  local_data = g_new (local_data_t, 1);

  self->name = MODEL_NAME;
  self->events_listened_for = adsm_setup_events_listened_for (events_listened_for);
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

  local_data->polys = g_ptr_array_new_with_free_func(free_polygon_as_GDestroyNotify);
  local_data->max_nvertices = 0;
  local_data->projection = projection;
  local_data->unit_map = g_new(int, UNT_unit_list_length(units));
  local_data->nruns = 0;

  /* These arrays will be initialized when the number of polygons is known. */
  local_data->unit_count = NULL;
  local_data->ninfected = NULL;
  local_data->nvaccinated = NULL;
  local_data->ndestroyed = NULL;

  local_data->infected = g_hash_table_new (g_direct_hash, g_direct_equal);
  local_data->vaccinated = g_hash_table_new (g_direct_hash, g_direct_equal);
  local_data->destroyed = g_hash_table_new (g_direct_hash, g_direct_equal);

  #if DEBUG
    g_debug ("----- EXIT new (%s)", MODEL_NAME);
  #endif

  return self;
}

/* end of file summary_gis_writer.c */
