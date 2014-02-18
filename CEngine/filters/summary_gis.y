%{
#if HAVE_CONFIG_H
#  include <config.h>
#endif

#include <stdio.h>
#include "unit.h"
#include "gis.h"
#include <shapefil.h>
#include <gpcl/gpc.h>

#if STDC_HEADERS
#  include <stdlib.h>
#  include <unistd.h>
#  include <string.h>
#elif HAVE_STRINGS_H
#  include <strings.h>
#endif

#if HAVE_MATH_H
#  include <math.h>
#endif

#include <assert.h>

#define GRID_SIDE_LENGTH 10
#define DEGREE_DISTANCE 111.31949 /**< 1/360th of equatorial radius, in km */

/** @file filters/summary_gis.c
 * A filter that takes a state table (output from state_table_filter), a population
 * file, and optionally an ArcView file of polygons, and creates an ArcView
 * file showing summary information over a whole set of Monte Carlo trials.
 *
 * Call it as
 *
 * <code>summary_gis_filter POPULATION-FILE OUTPUT-ARCVIEW-FILE [POLYGON-FILE] < STATE-TABLE-FILE</code>
 *
 * For example,
 *
 * <code>summary_gis_filter population.xml run01.shp < run01_states.txt</code>
 *
 * would output ArcView files named run01.shp, run01.shx, and run01.dbf, based
 * on the unit locations in population.xml and the unit states in run01_states.txt.
 * Temporary files named run01_grid.shp, run01_grid.shx, and run01_grid.dbf
 * would be created with default 10x10 km grid squares.
 *
 * As another example,
 *
 * <code>summary_gis_filter population.xml run01.shp counties.shp < run01_states.txt</code>
 *
 * would output ArcView files named run01.shp, run01.shx, and run01.dbf, based
 * on the unit locations in population.xml and the unit states in run01_states.txt.
 * The map would be divided into the polygons given in counties.shp, and the
 * ArcView files would preserve all the original attributes on the counties
 * objects.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 *
 * Copyright &copy; University of Guelph, 2005-2011
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#define YYERROR_VERBOSE
#define BUFFERSIZE 2048
#define COPY_BUFFERSIZE 8192 /**< arbitrary chunk size for copying files */

/* int yydebug = 1; must also compile with --debug to use this */
int yylex(void);
int yyerror (char const *s);
char errmsg[BUFFERSIZE];

unsigned int nunits; /**< Number of units. */
unsigned int npolys; /**< Number of polygons. */
unsigned int *unit_count = NULL; /**< A count of the number of units in each
  polygon.  The length of this array is the number of polgons. */
int *unit_map = NULL; /**< An array giving the polygon to which each unit maps.
  If the unit is not in any polygon, that entry is -1.  The length of this
  array is the number of units. */
gboolean *infected = NULL; /**< Flags indicating whether each unit was infected
  at any time during the current Monte Carlo run.  The length of this array is
  the number of units. */
gboolean *destroyed = NULL; /**< Flags indicating whether each unit was
  destroyed during the current Monte Carlo run.  The length of this array is
  the number of units. */
gboolean *vimmune = NULL; /**< Flags indicating whether each unit was
  vaccine immune at any time during the current Monte Carlo run.  The length of
  this array is the number of units. */
double *ninfected; /**< Counts of the number of units in a polygon that were
  infected at any time during the current Monte Carlo run.  The length of this
  array is the number of polygons. */
double *ndestroyed; /**< Counts of the number of units in a polygon that were
  destroyed during the current Monte Carlo run.  The length of this array is
  the number of polygons. */
double *nvimmune; /**< Counts of the number of units in a polygon that were
  vaccine immune at any time during the current Monte Carlo run.  The length of
  this array is the number of polygons. */
unsigned int last_run = 0; /**< The most recent run number we have seen in the
  table. */
const char *arcview_shp_filename;



void
copy (const char *src_filename, const char *dest_filename)
{
  FILE *src = NULL;
  FILE *dest = NULL;
  static char buffer [COPY_BUFFERSIZE];
  size_t len = 1;

  src = fopen (src_filename, "r");
  if (src == NULL)
    goto end;

  dest = fopen (dest_filename, "w");
  if (dest == NULL)
    goto end;

  while (!feof (src))
    {
      len = fread (buffer, sizeof(char), COPY_BUFFERSIZE, src);
      if (len > 0)
        fwrite (buffer, sizeof(char), len, dest);
    }

end:
  /* Clean up. */
  if (dest != NULL)
    fclose (dest);
  if (src != NULL)
    fclose (src);

  return;
}



/**
 * Returns the approximate distance in km between points 1 and 2.  Latitudes
 * and longitudes must be given in degrees.  The calculation is from the
 * Aviation Formulary by Ed Williams (http://williams.best.vwh.net/avform.htm).
 *
 * @param lat1 latitude of point 1, in degrees.
 * @param lon1 longitude of point 1, in degrees.
 * @param lat2 latitude of point 2, in degrees.
 * @param lon2 longitude of point 2, in degrees.
 * @return the distance (in km) between points 1 and 2.
 */
double
approx_distance (double lat1, double lon1, double lat2, double lon2)
{
  double dlat, dlon;
  double x;

  dlat = lat2 - lat1;
  dlon = fabs (lon2 - lon1);
  /* Handle the case where the shortest line between the points crosses the
   * +180/-180 line. */
  if (dlon > 180)
    dlon = 360 - dlon;

  x = dlon * cos (DEG_TO_RAD * lat1);
  return sqrt (x * x + dlat * dlat) * DEGREE_DISTANCE;
}


/**
 * Turns an Shapelib shape object into a gpc polygon object.  The vertices are
 * copied, so the original shape object can be destroyed after calling this
 * function.
 *
 * @param shape a Shapelib shape object.
 * @return a gpc polygon object.
 */
gpc_polygon *
shape_to_poly (SHPObject *shape)
{
  gpc_polygon *poly;
  int ncontours;
  int i, j, start, end;
  gpc_vertex_list *contour;

  /* Initialize a polygon object. */
  poly = g_new (gpc_polygon, 1);
  poly->num_contours = 0;
  poly->hole = NULL;
  poly->contour = NULL;

  if (shape == NULL)
    goto end;

  ncontours = shape->nParts;
  if (ncontours == 0)
    goto end;

  poly->num_contours = ncontours;
  poly->hole = g_new0 (int, ncontours); /* assume no holes */
  poly->contour = g_new (gpc_vertex_list, ncontours);
  for (i = 0; i < ncontours; i++)
    {
      contour = &(poly->contour[i]);

      /* Allocate the vertices for the contour. */
      start = shape->panPartStart[i];
      if (i < (ncontours - 1))
	end = shape->panPartStart [i+1];
      else
	end = shape->nVertices;
      contour->num_vertices = end - start;
      contour->vertex = g_new (gpc_vertex, contour->num_vertices);

      /* Copy the vertices. */
      for (j = start; j < end; j++)
	{
	  contour->vertex[j-start].x = shape->padfX[j];
	  contour->vertex[j-start].y = shape->padfY[j];
	} /* end of loop over vertices */
    } /* end of loop over contours */

end:
  return poly;
}



/**
 * Creates ArcView files containing a grid that covers the units.  Sets the
 * global npolys to a count of polygons.  Allocates and fills in the global
 * unit_count (number of units in each polygon) array.  Fills in the global
 * unit-to-polygon mapping array unit_map.
 *
 * @param units a list of units.
 * @param shape_filename the name (ending with .shp) of the grid file to
 *   write.
 */
void
create_polys_as_grid (UNT_unit_list_t *units, char *shape_filename)
{
  unsigned int nunits, i;
  UNT_unit_t *unit;
  double min_lat, max_lat, min_lon, max_lon;
  double width, height;
  double lat_step, lon_step, lat, lon;
  SHPHandle shape_file = NULL;
  SHPObject *shape;
  double vertex_x[4], vertex_y[4];
  GArray *tmp_unit_count = NULL;
  gboolean no_units_yet;

#if DEBUG
  g_debug ("----- ENTER create_polys_as_grid");
#endif

  nunits = UNT_unit_list_length (units);
  for (i = 0; i < nunits; i++)
    {
      unit = UNT_unit_list_get (units, i);
      unit->x = unit->longitude;
      unit->y = unit->latitude;
    }
  /* Find the minimum and maximum latitude and longitude. */
  unit = UNT_unit_list_get (units, 0);
  min_lat = max_lat = unit->latitude;
  min_lon = max_lon = unit->longitude;
  for (i = 1; i < nunits; i++)
    {
      unit = UNT_unit_list_get (units, i);
      if (unit->latitude < min_lat)
        min_lat = unit->latitude;
      else if (unit->latitude > max_lat)
        max_lat = unit->latitude;        
      if (unit->longitude < min_lon)
        min_lon = unit->longitude;
      else if (unit->longitude > max_lon)
        max_lon = unit->longitude;
    }
  #if DEBUG
    g_debug ("units bound by (lat,lon) (%.1f,%.1f),(%.1f,%.1f)",
             min_lat, min_lon, max_lat, max_lon);
  #endif

  /* Work out the step size for the grid. */
  height = approx_distance (min_lat, min_lon, max_lat, min_lon);
  lat_step = GRID_SIDE_LENGTH / height * (max_lat - min_lat);
  #if DEBUG
    g_debug ("extent of units from min to max latitude (up-down) = %.2f km",
             height);
    g_debug ("latitude step to get %i km grid squares = %.3f",
             GRID_SIDE_LENGTH, lat_step);
  #endif
  width = (approx_distance (min_lat, min_lon, min_lat, max_lon)
	    + approx_distance (max_lat, min_lon, max_lat, max_lon)) * 0.5;
  lon_step = GRID_SIDE_LENGTH / width * (max_lon - min_lon);
  #if DEBUG
    g_debug ("extent of units from min to max longitude (left-right) = %.2f km",
             width);
    g_debug ("longitude step to get %i km grid squares = %.3f",
             GRID_SIDE_LENGTH, lon_step);
  #endif

  npolys = 0;
  tmp_unit_count = g_array_new (/* zero-terminated = */ FALSE,
				/* clear = */ TRUE,
				sizeof (unsigned int));
  #if DEBUG
    g_debug ("creating new shapefile \"%s\"", shape_filename);
  #endif
  shape_file = SHPCreate (shape_filename, SHPT_POLYGON);
  for (lat = max_lat; lat > min_lat; lat -= lat_step)
    for (lon = min_lon; lon < max_lon; lon += lon_step)
      {
	/* Find the units that are in this polygon. */
	no_units_yet = TRUE;
	for (i = 0; i < nunits; i++)
	  {
	    if (unit_map[i] >= 0)
	      continue;

	    unit = UNT_unit_list_get (units, i);
	    if (unit->latitude > lat || unit->latitude <= (lat - lat_step)
		|| unit->longitude < lon || unit->longitude >= (lon + lon_step))
	      continue;

	    if (no_units_yet)
	      {
		/* This is the first unit we've discovered in this grid square.
		 * Start a count in the unit-to-polygon mapping array. */
		no_units_yet = FALSE;
		npolys += 1;
		g_array_set_size (tmp_unit_count, npolys);
	      }
	    unit_map[i] = npolys - 1;
	    g_array_index (tmp_unit_count, unsigned int, npolys - 1) += 1;

	  } /* end of loop over units */

	/* If there were no units in this grid square, don't bother recording
	 * it. */
	if (no_units_yet)
	  continue;

	/* Fill in the vertex array needed for writing the grid square to an
	 * ArcView file.  Start at the upper-left corner, proceed clockwise. */
        vertex_x[0] = lon;
	vertex_y[0] = lat;
        vertex_x[1] = lon + lon_step;
	vertex_y[1] = lat;
        vertex_x[2] = lon + lon_step;
	vertex_y[2] = lat - lat_step;
        vertex_x[3] = lon;
	vertex_y[3] = lat - lat_step;
	shape = SHPCreateSimpleObject (SHPT_POLYGON, 4, vertex_x, vertex_y, NULL);
	SHPWriteObject (shape_file, -1, shape);
	SHPDestroyObject (shape);
      }

  /* Take the memory block holding the counts of the number of units in each
   * polygon out of its temporary wrapper. */
  unit_count = (unsigned int *) (tmp_unit_count->data);
  g_array_free (tmp_unit_count, FALSE);

  /* Clean up. */
  if (shape_file != NULL)
    SHPClose (shape_file);

#if DEBUG
  g_debug ("----- EXIT create_polys_as_grid");
#endif

  return;
}



/**
 * Reads a set of polygons from an ArcView shapefile.  Sets the global npolys
 * to a count of polygons.  Allocates and fills in the global unit_count
 * (number of units in each polygon) array.  Fills in the global
 * unit-to-polygon mapping array unit_map.
 *
 * @param units a list of units.
 * @param shape_filename name of an ArcView .shp file.
 */
void
read_polys_from_file (UNT_unit_list_t *units, char *shape_filename)
{
  unsigned int i;
  SHPHandle shape_file = NULL;
  int nshapes;
  int shape_type;
  int shape_index;
  SHPObject *shape = NULL;
  gpc_polygon *poly;
  UNT_unit_t *unit;
#if DEBUG
  GString *s;
#endif

#if DEBUG
  g_debug ("----- ENTER read_polys_from_file");
#endif

  #if DEBUG
    g_debug ("opening shape file \"%s\"", shape_filename);
  #endif
  shape_file = SHPOpen (shape_filename, "rb");
  if (shape_file == NULL)
    {
      g_warning ("could not open shape file \"%s\"", shape_filename);
      goto end;
    }

  /* Verify that the shape file contains polygons. */
  #if DEBUG
    g_debug ("checking that shape file contains polygons");
  #endif
  SHPGetInfo (shape_file, &nshapes, &shape_type, NULL, NULL);
  if (shape_type != SHPT_POLYGON)
    {
      g_warning ("shape file must contain polygons");
      goto end;
    }

  /* Go through the shapes.  Turn them into gpc_polygon objects (because that's
   * what the point-in-polygon test in the GIS functions module expects) and
   * check which (if any) units they contain. */
  #if DEBUG
    g_debug ("checking which polygons contain which units");
  #endif
  npolys = nshapes;
  unit_count = g_new0 (unsigned int, npolys);
  for (shape_index = 0; shape_index < nshapes; shape_index++)
    {
      shape = SHPReadObject (shape_file, shape_index);
      poly = shape_to_poly (shape);
      SHPDestroyObject (shape);

      for (i = 0; i < nunits; i++)
	{
	  if (unit_map[i] >= 0)
	    continue;

	  unit = UNT_unit_list_get (units, i);
	  if (GIS_point_in_polygon (poly, unit->longitude, unit->latitude))
	    {
	      unit_map[i] = shape_index;
	      unit_count[shape_index] += 1;
	    }
	} /* end of loop over units */

      gpc_free_polygon (poly);

    } /* end of loop over shapes */

  #if DEBUG
    s = g_string_new (NULL);
    for (i = 0; i < npolys; i++)
      {
        if (i > 0)
          g_string_append_c (s, ',');
        g_string_append_printf (s, "%u", unit_count[i]);
      }
    g_debug ("count of units in each poly = %s", s->str);
    g_string_free (s, TRUE);
  #endif

end:
  /* Clean up. */
  if (shape_file != NULL)
    SHPClose (shape_file);

#if DEBUG
  g_debug ("----- EXIT read_polys_from_file");
#endif

  return;
}



void
write_polys_with_stats (const char *input_shp_filename, const char *output_shp_filename)
{
  char *input_base_filename; /**< Without the .shp ending. */
  char *output_base_filename; /**< Without the .shp ending. */
  char *input_shx_filename;
  char *output_shx_filename;
  char *input_dbf_filename;
  char *output_dbf_filename;
  DBFHandle input_dbf_file = NULL;
  DBFHandle output_dbf_file = NULL;
  int nfields, nrecords;
  int field;
  int i;
  DBFFieldType field_type;
  char name[12]; /**< max size is 11 + terminating null char */
  int width;
  int decimals;
  int nunits_field_index;
  int avg_ninfected_field_index;
  int avg_ndestroyed_field_index;
  int avg_nvimmune_field_index;
  int avg_frinfected_field_index;
  int avg_frdestroyed_field_index;
  int avg_frvimmune_field_index;
  const char *field_value_string;
  int field_value_int;
  double field_value_double;

#if DEBUG
  g_debug ("----- ENTER write_polys_with_stats");
#endif

  /* Simply copy the .shp and .shx files.  They remain the same, it's just the
   * attributes in the DBF file that are augmented. */
  #if DEBUG
    g_debug ("copying \"%s\" to \"%s\"", input_shp_filename, output_shp_filename);
  #endif
  copy (input_shp_filename, output_shp_filename);

  input_base_filename = g_strndup (input_shp_filename,
				   strlen (input_shp_filename) - 4);
  output_base_filename = g_strndup (output_shp_filename,
				    strlen (output_shp_filename) - 4);
  input_shx_filename = g_strdup_printf ("%s.shx", input_base_filename);
  output_shx_filename = g_strdup_printf ("%s.shx", output_base_filename);
  #if DEBUG
    g_debug ("copying \"%s\" to \"%s\"", input_shx_filename, output_shx_filename);
  #endif
  copy (input_shx_filename, output_shx_filename);

  /* Open the input DBF file for reading. */
  input_dbf_filename = g_strdup_printf ("%s.dbf", input_base_filename);
  input_dbf_file = DBFOpen (input_dbf_filename, "rb");
  if (input_dbf_file == NULL)
    g_warning ("no DBF file named \"%s\", will continue without it",
	       input_dbf_filename);
  /* Open a new output DBF file for writing. */
  output_dbf_filename = g_strdup_printf ("%s.dbf", output_base_filename);
  output_dbf_file = DBFCreate (output_dbf_filename);

  /* Copy the existing attribute definitions. */
  if (input_dbf_file != NULL)
    nfields = DBFGetFieldCount (input_dbf_file);
  else
    nfields = 0;
  #if DEBUG
    g_debug ("copying %i field definitions from input DBF file \"%s\" to output DBF file \"%s\"",
             nfields, input_dbf_filename, output_dbf_filename);
  #endif
  for (field = 0; field < nfields; field++)
    {
      field_type = DBFGetFieldInfo (input_dbf_file, field, name, &width,
				    &decimals);
      DBFAddField (output_dbf_file, name, field_type, width, decimals);
    }

  /* Add new attribute definitions. */
  #if DEBUG
    g_debug ("adding field definitions to output DBF file \"%s\": nunits, avgninf, avgndest, avgfrinf, avgfrdest",
             output_dbf_filename);
  #endif
  /* 9-digit integers should be enough to count # of units in a polygon. */
  nunits_field_index = DBFAddField (output_dbf_file, "nunits", FTInteger, 9, 0);
  /* 1 decimal place for average # of units infected or destroyed, 3 for
   * average fraction of units. */
  avg_ninfected_field_index = DBFAddField (output_dbf_file, "avgninf",
					   FTDouble, 9, 1);
  avg_ndestroyed_field_index = DBFAddField (output_dbf_file, "avgndest",
					    FTDouble, 9, 1);
  avg_nvimmune_field_index = DBFAddField (output_dbf_file, "avgnvimm",
					    FTDouble, 9, 1);
  avg_frinfected_field_index = DBFAddField (output_dbf_file, "avgfrinf",
					    FTDouble, 9, 3);
  avg_frdestroyed_field_index = DBFAddField (output_dbf_file, "avgfrdest",
					     FTDouble, 9, 3);
  avg_frvimmune_field_index = DBFAddField (output_dbf_file, "avgfrvimm",
					     FTDouble, 9, 3);

  /* Copy the data records from the old file to the new. */
  /* First a sanity check: is the number of records the same as the number of
   * polygons? */
  if (input_dbf_file != NULL)
    {
      nrecords = DBFGetRecordCount (input_dbf_file);
      if (nrecords != npolys)
        g_warning ("# of records in file (%i) != number of polygons (%u)", nrecords, npolys);
      #if DEBUG
        else
          g_debug ("# of records in file (%i) = number of polygons (%u)", nrecords, npolys);
      #endif
    }
  #if DEBUG
    g_debug ("copying data from \"%s\" to \"%s\"", input_dbf_filename, output_dbf_filename);
  #endif
  for (i = 0; i < npolys; i++)
    {
      for (field = 0; field < nfields; field++)
        {
	  field_type = DBFGetFieldInfo (input_dbf_file, field, NULL, NULL, NULL);
	  if (field_type == FTString)
	    {
	      field_value_string = DBFReadStringAttribute (input_dbf_file, i, field);
	      DBFWriteStringAttribute (output_dbf_file, i, field, field_value_string);
	    }
	  else if (field_type == FTInteger)
	    {
	      field_value_int = DBFReadIntegerAttribute (input_dbf_file, i, field);
	      DBFWriteIntegerAttribute (output_dbf_file, i, field, field_value_int);
	    }
	  else if (field_type == FTDouble)
	    {
	      field_value_double = DBFReadDoubleAttribute (input_dbf_file, i, field);
	      DBFWriteDoubleAttribute (output_dbf_file, i, field, field_value_double);
	    }
	}
    }
  /* Write the new data attributes to the file. */
  #if DEBUG
    g_debug ("writing new attributes to \"%s\"", output_dbf_filename);
  #endif
  for (i = 0; i < npolys; i++)
    {
      DBFWriteIntegerAttribute (output_dbf_file, i, nunits_field_index,
 	unit_count[i]);
      DBFWriteDoubleAttribute (output_dbf_file, i, avg_ninfected_field_index,
        ninfected[i]);
      DBFWriteDoubleAttribute (output_dbf_file, i, avg_ndestroyed_field_index,
        ndestroyed[i]);
      DBFWriteDoubleAttribute (output_dbf_file, i, avg_nvimmune_field_index,
        nvimmune[i]);
      DBFWriteDoubleAttribute (output_dbf_file, i, avg_frinfected_field_index,
        ninfected[i] / unit_count[i]);
      DBFWriteDoubleAttribute (output_dbf_file, i, avg_frdestroyed_field_index,
        ndestroyed[i] / unit_count[i]);
      DBFWriteDoubleAttribute (output_dbf_file, i, avg_frvimmune_field_index,
        nvimmune[i] / unit_count[i]);
    }

  /* Clean up. */
  if (input_dbf_file != NULL)
    DBFClose (input_dbf_file);
  DBFClose (output_dbf_file);
  g_free (input_base_filename);
  g_free (input_shx_filename);
  g_free (input_dbf_filename);
  g_free (output_base_filename);
  g_free (output_shx_filename);
  g_free (output_dbf_filename);

#if DEBUG
  g_debug ("----- EXIT write_polys_with_stats");
#endif
  return;
}



/**
 * Counts the number of units in each polygon that were infected during a Monte
 * Carlo trial.
 */
void
record_infections (void)
{
  unsigned int unit_index;
  int poly_index;

  for (unit_index = 0; unit_index < nunits; unit_index++)
    {
      poly_index = unit_map[unit_index];
      if (poly_index == -1) /* unit is not in any polygon */
        continue;

      if (infected[unit_index])
	ninfected[poly_index] += 1;
    }
}



/**
 * Counts the number of units in each polygon that were destroyed during a
 * Monte Carlo trial.
 */
void
record_destructions (void)
{
  unsigned int unit_index;
  int poly_index;

  for (unit_index = 0; unit_index < nunits; unit_index++)
    {
      poly_index = unit_map[unit_index];
      if (poly_index == -1) /* unit is not in any polygon */
        continue;

      if (destroyed[unit_index])
	ndestroyed[poly_index] += 1;
    }
}



/**
 * Counts the number of units in each polygon that were vaccine immune during a
 * Monte Carlo trial.
 */
void
record_vimmune (void)
{
  unsigned int unit_index;
  int poly_index;

  for (unit_index = 0; unit_index < nunits; unit_index++)
    {
      poly_index = unit_map[unit_index];
      if (poly_index == -1) /* unit is not in any polygon */
        continue;

      if (vimmune[unit_index])
	nvimmune[poly_index] += 1;
    }
}



/**
 * Resets the flags that show which units were infected during a Monte Carlo
 * trial to all false.
 */
void
clear_infected_flags (void)
{
  unsigned int i;

  for (i = 0; i < nunits; i++)
    infected[i] = FALSE;
}



/**
 * Resets the flags that show which units were destroyed during a Monte Carlo
 * trial to all false.
 */
void
clear_destroyed_flags (void)
{
  unsigned int i;

  for (i = 0; i < nunits; i++)
    destroyed[i] = FALSE;
}



/**
 * Resets the flags that show which units were vaccine immune during a Monte
 * Carlo trial to all false.
 */
void
clear_vimmune_flags (void)
{
  unsigned int i;

  for (i = 0; i < nunits; i++)
    vimmune[i] = FALSE;
}

%}

%union {
  int ival;
  float fval;
  char *sval;
  GArray *lval;
}

%token NODE RUN DAY POLYGON
%token COMMA COLON EQ LBRACE RBRACE LPAREN RPAREN DQUOTE NEWLINE
%token <ival> INT
%token <fval> FLOAT
%token <sval> VARNAME STRING
%type <ival> unit_seqs state_codes
%%
state_table:
    header_line NEWLINE data_lines NEWLINE
    { }
  ;

header_line:
    RUN COMMA DAY COMMA unit_seqs
    {
      if ($5 != nunits)
        {
          g_error ("number of units in state table (%i) does not match number of units in population file (%u)",
                   $5, nunits);
        }
    }
  ;

unit_seqs:
    unit_seqs COMMA INT
    {
      /* Increment the count of units. */
      $$ = $1 + 1;
    }
  | INT
    {
      /* Initialize the count of units. */
      $$ = 1;
    }
  ;

data_lines:
    data_lines NEWLINE data_line
    { }
  | data_line
    { }
  ;

data_line:
    INT COMMA INT COMMA state_codes
    {
      unsigned int run;

      run = $1;

      if (run > last_run)
        {
	  /* We just started looking at the output for a new Monte Carlo trial.
	   * Save the results from the previous Monte Carlo trial (unless of
	   * course this is the very start of the output). */
      #if DEBUG
	    g_debug ("started reading results for run #%u", run);
      #endif
	  if (run > 1)
	    {
	      record_infections();
	      record_destructions();
	      record_vimmune();
	      clear_infected_flags();
	      clear_destroyed_flags();
	      clear_vimmune_flags();
	    }
	  last_run = run;
	}
    }
  ;

state_codes:
    state_codes COMMA INT
    {
      unsigned int unit_index;
      UNT_state_t state;

      unit_index = $1 + 1;
      state = $3;
      /* Set a flag that indicates if the unit was ever diseased or was
       * destroyed during this Monte Carlo trial. */
      if (state == Latent || state == InfectiousSubclinical
	  || state == InfectiousClinical)
	infected[unit_index] = TRUE;
      else if (state == Destroyed)
        destroyed[unit_index] = TRUE;
      else if (state == VaccineImmune)
        vimmune[unit_index] = TRUE;
      $$ = unit_index;
    }
  | INT
    {
      unsigned int unit_index;
      UNT_state_t state;

      /* This state code is for the unit with index 0 (numbering from 0 to
       * nunits-1). */
      unit_index = 0;
      state = $1;
      /* Set a flag that indicates if the unit was ever diseased or was
       * destroyed during this Monte Carlo trial. */
      if (state == Latent || state == InfectiousSubclinical
	  || state == InfectiousClinical)
	infected[unit_index] = TRUE;
      else if (state == Destroyed)
        destroyed[unit_index] = TRUE;
      else if (state == VaccineImmune)
        vimmune[unit_index] = TRUE;
      $$ = unit_index;
    }
  ;

%%
extern FILE *yyin;
extern int yylineno, tokenpos;
extern char linebuf[];

/* Simple yyerror from _lex & yacc_ by Levine, Mason & Brown. */
int
yyerror (char const *s)
{
  fprintf (stderr, "Error in input (line %d): %s:\n%s\n", yylineno, s, linebuf);
  fprintf (stderr, "%*s\n", 1+tokenpos, "^");
  return 0;
}



/**
 * A log handler that simply discards messages.
 */
void
silent_log_handler (const gchar * log_domain, GLogLevelFlags log_level,
		    const gchar * message, gpointer user_data)
{
  ;
}



int
main (int argc, char *argv[])
{
  int verbosity = 0;
  GError *option_error = NULL;
  GOptionContext *context;
  GOptionEntry options[] = {
    { "verbosity", 'V', 0, G_OPTION_ARG_INT, &verbosity, "Message verbosity level (0 = simulation output only, 1 = all debugging output)", NULL },
    { NULL }
  };
  const char *population_filename = NULL;
  char *arcview_base_name;
  char *polygon_shp_filename;
  gboolean created_grid;
  UNT_unit_list_t *units;
  int i;

  /* Get the command-line options and arguments.  There should be at least 2
   * command-line arguments, the name of the population file to read, and the name of
   * the ArcView .shp file to write.  There may also be a third argument, the
   * name of a polygon file to base the output map on. */
  context = g_option_context_new ("");
  g_option_context_add_main_entries (context, options, /* translation = */ NULL);
  if (!g_option_context_parse (context, &argc, &argv, &option_error))
    {
      g_error ("option parsing failed: %s\n", option_error->message);
    }
  if (argc >= 2)
    population_filename = argv[1];
  else
    {
      g_error ("Need the name of a population file.");
    }

  if (argc >= 3)
    arcview_shp_filename = argv[2];
  else
    arcview_shp_filename = NULL;
  if (arcview_shp_filename == NULL
      || !g_str_has_suffix (arcview_shp_filename, ".shp"))
    {
      g_error ("Need the name of an ArcView shape (.shp) file.");
    }

  if (argc >= 4)
    polygon_shp_filename = argv[3];
  else
    polygon_shp_filename = NULL;  
  g_option_context_free (context);

  /* Set the verbosity level. */
  if (verbosity < 1)
    {
      g_log_set_handler (NULL, G_LOG_LEVEL_DEBUG, silent_log_handler, NULL);
      g_log_set_handler ("unit", G_LOG_LEVEL_DEBUG, silent_log_handler, NULL);
    }
  #if DEBUG
    g_debug ("verbosity = %i", verbosity);
  #endif
  g_log_set_handler ("unit", G_LOG_LEVEL_DEBUG, silent_log_handler, NULL);

  /* Get the base part (without the .shp) of the ArcView file name. */
  arcview_base_name = g_strndup (arcview_shp_filename,
                                 strlen(arcview_shp_filename) - 4);
  #if DEBUG
    g_debug ("base part of ArcView file name = \"%s\"", arcview_base_name);
  #endif

  /* Read in the population file. */
#ifdef USE_SC_GUILIB
  units = UNT_load_unit_list (population_filename, NULL);
#else
  units = UNT_load_unit_list (population_filename);
#endif
  nunits = UNT_unit_list_length (units);
  #if DEBUG
    g_debug ("%u units read from \"%s\"", nunits, population_filename);
  #endif
  /* Create an array to hold a mapping to units to polygons.  Initialize all
   * entries to -1, meaning that the unit isn't in any polygon.  The proper
   * values will be filled in when we either read in a polygon file or create a
   * default grid, below. */
  #if DEBUG
    g_debug ("initializing unit-to-polygon mapping array");
  #endif
  unit_map = g_new0 (int, nunits);
  for (i = 0; i < nunits; i++)
    unit_map[i] = -1;

  /* If no polygon file was specified, create a grid.  Also get a mapping of
   * which units are in which polygon. */
  if (polygon_shp_filename == NULL)
    {
      created_grid = TRUE;
      polygon_shp_filename = g_strdup_printf ("%s_grid.shp", arcview_base_name);
      create_polys_as_grid (units, polygon_shp_filename);
    }
  else
    {
      created_grid = FALSE;
      read_polys_from_file (units, polygon_shp_filename);
    }

  /* Initialize arrays of flags showing whether a particular unit was infected,
   * destroyed, or vaccine immune in a particular run. */
  infected = g_new0 (gboolean, nunits);
  destroyed = g_new0 (gboolean, nunits);
  vimmune = g_new0 (gboolean, nunits);
  /* Initialize arrays of counts of infected, destroyed, or vaccine immune
   * units in each polygon in a particular run. */
  ninfected = g_new0 (double, npolys);
  ndestroyed = g_new0 (double, npolys);
  nvimmune = g_new0 (double, npolys);

  /* Call the parser.  It will go through the unit states file and populate the
   * ninfected and ndestroyed arrays. */
  if (yyin == NULL)
    yyin = stdin;
  while (!feof(yyin))
    yyparse();

  /* Record stats for the final run. */
  record_infections();
  record_destructions();
  /* The variable last_run stores a count of the number of Monte Carlo trials.
   * Use it to get a mean number of units infected, destroyed, and vaccine
   * immune per polygon per trial. */
  for (i = 0; i < npolys; i++)
    {
      ninfected[i] /= last_run;
      ndestroyed[i] /= last_run;
      nvimmune[i] /= last_run;
    }

#if DEBUG
  {
    GString *s;

    s = g_string_new (NULL);
    for (i = 0; i < npolys; i++)
      {
	if (i > 0)
          g_string_append_c (s, ',');
	g_string_append_printf (s, "%.0f", ninfected[i]);
      }
    g_debug ("mean # of infected units in each poly = %s", s->str);
    g_string_free (s, TRUE);

    s = g_string_new (NULL);
    for (i = 0; i < npolys; i++)
      {
	if (i > 0)
          g_string_append_c (s, ',');
	g_string_append_printf (s, "%.0f", ndestroyed[i]);
      }
    g_debug ("mean # of destroyed units in each poly = %s", s->str);
    g_string_free (s, TRUE);

    s = g_string_new (NULL);
    for (i = 0; i < npolys; i++)
      {
        if (i > 0)
          g_string_append_c (s, ',');
        g_string_append_printf (s, "%.0f", nvimmune[i]);
      }
    g_debug ("mean # of vaccine immune units in each poly = %s", s->str);
    g_string_free (s, TRUE);
  }
#endif

  /* Create a copy of the polygon files (or the generated grid files) and
   * populate the DBF file with the simulation summary info. */
  write_polys_with_stats (polygon_shp_filename, arcview_shp_filename);

  /* Clean up. */
  g_free (arcview_base_name);
  if (created_grid == TRUE)
    g_free (polygon_shp_filename);
  if (unit_map != NULL)
    g_free (unit_map);
  if (unit_count != NULL)
    g_free (unit_count);
  if (infected != NULL)
    g_free (infected);
  if (destroyed != NULL)
    g_free (destroyed);
  if (vimmune != NULL)
    g_free (vimmune);
  if (ninfected != NULL)
    g_free (ninfected);
  if (ndestroyed != NULL)
    g_free (ndestroyed);
  if (nvimmune != NULL)
    g_free (nvimmune);

  return EXIT_SUCCESS;
}

/* end of file summary_gis.y */
