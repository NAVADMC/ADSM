/** @file xml2shp.c
 *
 * A filter that turns a SHARCSpread xml population file into an ArcView file.
 *
 * call it as
 *
 * <code>xml2shp POPULATION-FILE [SHP-FILE]</code>
 *
 * SHP-FILE is the base name for the 3 ArcView files.  For example, if SHP-FILE
 * is "popdata", this program will output files named popdata.shp,
 * popdata.shx, and popdata.dbf.  If SHP-FILE is omitted, the output files
 * will have the same name as the population file, but with .shp, .shx, and .dbf
 * extensions.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date October 2005
 *
 * Copyright &copy; University of Guelph, 2005-2008
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#if HAVE_CONFIG_H
#  include <config.h>
#endif

#include <stdio.h>
#include "unit.h"
#include <shapefil.h>

#if STDC_HEADERS
#  include <stdlib.h>
#  include <string.h>
#endif
#if HAVE_STRINGS_H
#  include <strings.h>
#endif



#define NATTRIBUTES 5



/**
 * A log handler that simply discards messages.
 */
void
silent_log_handler (const gchar * log_domain, GLogLevelFlags log_level,
                    const gchar * message, gpointer user_data)
{
  ;
}



/**
 * Returns the length of the longest unit state name.
 */
int
max_state_name_length (void)
{
  int i;
  int len;
  int max = 0;

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
int
max_prod_type_length (UNT_unit_list_t * units)
{
  int i, n;
  GPtrArray *names;
  int len;
  int max = 0;

  names = units->production_type_names;
  n = names->len;
  for (i = 0; i < n; i++)
    {
      len = strlen ((char *) g_ptr_array_index (names, i));
      if (len > max)
        max = len;
    }
  return max;
}



/**
 * Returns the length of the longest unit ID string.
 */
int
max_unit_id_length (UNT_unit_list_t * units)
{
  unsigned int i, n;
  UNT_unit_t *unit;
  int len;
  int max = 0;

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



void
write_units (SHPHandle shape_file, DBFHandle attribute_file, int *attribute_id,
             UNT_unit_list_t * units, double *minbound, double *maxbound)
{
  UNT_unit_t *unit;
  SHPObject *unit_shape;
  int shape_id;
  double x, y;
  unsigned int n, i;

  /* The 1 in the argument list is the number of points. */
  unit_shape = SHPCreateSimpleObject (SHPT_POINT, 1, &x, &y, NULL);

  n = UNT_unit_list_length (units);
  for (i = 0; i < n; i++)
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

      unit_shape->padfX[0] = x;
      unit_shape->padfY[0] = y;
      SHPComputeExtents (unit_shape);
      /* The -1 is the library's code for creating a new object in the
       * shapefile as opposed to overwriting an existing one. */
      shape_id = SHPWriteObject (shape_file, -1, unit_shape);
      /* Sequence number */
      DBFWriteIntegerAttribute (attribute_file, shape_id, attribute_id[0], i);
      /* Herd ID */
      if (unit->official_id != NULL)
        DBFWriteStringAttribute (attribute_file, shape_id, attribute_id[1], unit->official_id);
      else
        DBFWriteStringAttribute (attribute_file, shape_id, attribute_id[1], "");
      /* Production type */
      DBFWriteStringAttribute (attribute_file, shape_id, attribute_id[2],
                               unit->production_type_name);
      /* Number of animals */
      DBFWriteIntegerAttribute (attribute_file, shape_id, attribute_id[3], unit->size);
      /* Number of state */
      DBFWriteStringAttribute (attribute_file, shape_id, attribute_id[4],
                               UNT_state_name[unit->initial_state]);
    }
  SHPDestroyObject (unit_shape);
}



int
main (int argc, char *argv[])
{
  const char *population_file_name = NULL;    /* name of the population file */
  char *arcview_file_name = NULL;       /* base name of the ArcView files */
  char *dot_location;
  char *attribute_file_name;
  int verbosity = 0;
  UNT_unit_list_t *units;
  unsigned int nunits;
  SHPHandle shape_file;
  DBFHandle attribute_file;
  int attribute_id[NATTRIBUTES];
  double minbound[2], maxbound[2];
  GError *option_error = NULL;
  GOptionContext *context;
  GOptionEntry options[] = {
    { "verbosity", 'V', 0, G_OPTION_ARG_INT, &verbosity, "Message verbosity level (0 = simulation output only, 1 = all debugging output)", NULL },
    { NULL }
  };

  /* Get the command-line options and arguments.  There should be two command-
   * line arguments, the name of the population file and the base name for the ArcView
   * output files. */
  context = g_option_context_new ("");
  g_option_context_add_main_entries (context, options, /* translation = */ NULL);
  if (!g_option_context_parse (context, &argc, &argv, &option_error))
    {
      g_error ("option parsing failed: %s\n", option_error->message);
    }

  /* Set the verbosity level. */
  if (verbosity < 1)
    {
      g_log_set_handler (NULL, G_LOG_LEVEL_DEBUG, silent_log_handler, NULL);
      g_log_set_handler ("unit", G_LOG_LEVEL_DEBUG, silent_log_handler, NULL);
    }
  #if DEBUG
    g_debug ("verbosity = %i", verbosity);
  #endif

  if (argc >= 2)
    population_file_name = argv[1];
  else
    {
      g_error ("Need the name of a population file.");
    }

  if (argc >= 3)
    arcview_file_name = g_strdup (argv[2]);
  else
    {
      char *population_file_base_name;

      /* Construct the ArcView file name based on the population file name. */
      population_file_base_name = g_path_get_basename (population_file_name);
      /* The population file name is expected to end in '.xml'. */
      dot_location = rindex (population_file_base_name, '.');
      if (dot_location == NULL)
        arcview_file_name = g_strdup (population_file_base_name);
      else
        arcview_file_name = g_strndup (population_file_base_name, dot_location - population_file_base_name);
      #if DEBUG
        g_debug ("using base name \"%s\" for ArcView files", arcview_file_name);
      #endif
      g_free (population_file_base_name);
    }
  g_option_context_free (context);
#ifdef USE_SC_GUILIB
  units = UNT_load_unit_list (population_file_name, NULL);
#else
  units = UNT_load_unit_list (population_file_name);
#endif
  nunits = UNT_unit_list_length (units);

#if DEBUG
  g_debug ("%i units read", nunits);
#endif
  if (nunits == 0)
    {
      g_error ("no units in file %s", population_file_name);
    }

  /* Initialize the shape and DBF (attribute) files for writing. */
  /* Something odd: if there are periods in the base file name, SHPCreate will
   * remove anything after the last period, which will create shp and shx
   * filenames that don't match the dbf filename.  As a workaround, if there is
   * a period in arcview_file_name, add '.tmp' to the end of the filename to
   * give SHPCreate something harmless to remove. */
  dot_location = index (arcview_file_name, '.');
  if (dot_location == NULL)
    {
      shape_file = SHPCreate (arcview_file_name, SHPT_POINT);
    }
  else
    {
      char *tmp_arcview_file_name;
      tmp_arcview_file_name = g_strdup_printf ("%s.tmp", arcview_file_name);
      shape_file = SHPCreate (tmp_arcview_file_name, SHPT_POINT);
      g_free (tmp_arcview_file_name);
    }
  attribute_file_name = g_strdup_printf ("%s.dbf", arcview_file_name);
  attribute_file = DBFCreate (attribute_file_name);
#if DEBUG
  g_debug ("longest state name = %i chars", max_state_name_length ());
  g_debug ("longest production type name = %i chars", max_prod_type_length (units));
  g_debug ("longest unit ID = %i chars", max_unit_id_length (units));
#endif
  attribute_id[0] = DBFAddField (attribute_file, "seq", FTInteger, 9, 0);
  attribute_id[1] =
    DBFAddField (attribute_file, "id", FTString, MAX (1, max_unit_id_length (units)), 0);
  attribute_id[2] =
    DBFAddField (attribute_file, "prodtype", FTString, max_prod_type_length (units), 0);
  attribute_id[3] = DBFAddField (attribute_file, "size", FTInteger, 9, 0);
  attribute_id[4] = DBFAddField (attribute_file, "status", FTString, max_state_name_length (), 0);

  write_units (shape_file, attribute_file, attribute_id, units, minbound, maxbound);

  /* Check the computed extents against the ones cached in the SHPHandle
   * object. */
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
  UNT_free_unit_list (units);
  SHPClose (shape_file);
  g_free (arcview_file_name);
  g_free (attribute_file_name);
  DBFClose (attribute_file);

  return EXIT_SUCCESS;
}

/* end of file xml2shp.c */
