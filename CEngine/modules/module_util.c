/** @file module_util.c
 * Helper functions for sub-models.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
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

#include "module_util.h"
#include "gis.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#if HAVE_STRINGS_H
#  include <strings.h>
#endif

#define EPSILON 0.001



/**
 * Compares a text string against a list of production type names. Returns the
 * position of the matching name in the list.
 */
guint
spreadmodel_read_prodtype (char *text, GPtrArray * production_type_names)
{
  gchar *normalized;
  guint nprod_types;
  guint loc;

  #if DEBUG
    g_debug ("----- ENTER spreadmodel_read_prodtype");
  #endif

  /* The text is assumed to be UTF-8. Normalize it to allow for comparison. */
  normalized = g_utf8_normalize (text, -1, G_NORMALIZE_DEFAULT);
  g_assert (normalized != NULL);

  nprod_types = production_type_names->len;
  for (loc = 0; loc < nprod_types; loc++)
    {
      if (g_utf8_collate (normalized, g_ptr_array_index (production_type_names, loc)) == 0)
        break;
    }
  g_free (normalized);

  if (loc == nprod_types)
    g_error ("text \"%s\" did not match any production type", text);

  #if DEBUG
    g_debug ("----- EXIT spreadmodel_read_prodtype");
  #endif

  return loc;
}



/**
 * Compares a text string against a list of production type names. Returns the
 * position of the matching name in the list.
 */
guint
spreadmodel_read_zone (char *text, ZON_zone_list_t * zones)
{
  gchar *normalized;
  guint nzones;
  guint loc;

  #if DEBUG
    g_debug ("----- ENTER spreadmodel_read_zone");
  #endif

  /* The text is assumed to be UTF-8. Normalize it to allow for comparison. */
  normalized = g_utf8_normalize (text, -1, G_NORMALIZE_DEFAULT);
  g_assert (normalized != NULL);

  nzones = ZON_zone_list_length (zones);
  for (loc = 0; loc < nzones; loc++)
    {
      if (g_utf8_collate (normalized, ZON_zone_list_get (zones, loc)->name) == 0)
        break;
    }
  g_free (normalized);

  if (loc == nzones)
    g_error ("text \"%s\" did not match any zone", text);

  #if DEBUG
    g_debug ("----- EXIT spreadmodel_read_zone");
  #endif

  return loc;
}



/**
 * Extends a rotating array.
 *
 * There are several places in the model where we want to delay actions.  It is
 * useful to have an array in which you can easily store events that you want
 * to retrieve 1 day from now, 2 days, etc.  An index "rotates" through the
 * array, so an event that is to happen in 1 day is stored 1 place ahead of the
 * rotating index, an event that is to happen in 2 days is stored 2 places
 * ahead of the rotating index, etc.  Sometimes you don't know in advance how
 * many places ahead you will need, and so you need to extend a rotating array.
 *
 * The array "rotates" so there are additional steps beyond simply extending
 * the array.  The first figure below shows the case when there is room at the
 * end of the newly-extended array for all items before and including the rotating index.
 * (Darker blue indicates events that will be reached sooner.)
 * So given an array of length <i>n</i> (1), we (2) add null entries to the
 * end, (3) copy the items up to and including the rotating index to the new space at
 * the end, and (4) overwrite the spaces up to and including the rotating index with null
 * entries.
 *
 * The second figure shows the case when there is not room at the end of the
 * extended array for all items before and including the rotating index.  Given an array of
 * length <i>n</i> (1), we (2) add null entries to the end, (3) copy as many
 * items as we can from before the rotating index to the new space at the end,
 * (4) copy the remaining entries before and including the rotating index to the start of the
 * array, and (5) overwrite the spaces up to and including the rotating index with null
 * entries.
 *
 * @image html extend_array_1.png "Extending the array when there is room at the end for all items before the index"
 *
 * @image html extend_array_2.png "Extending the array when there is not room at the end for all items before the index"
 *
 * @param array the pending results array
 * @param length the new length
 * @param index the current location of the rotating index
 */
void
spreadmodel_extend_rotating_array (GPtrArray * array, unsigned int length, unsigned int index)
{
  unsigned int old_length, diff;
  unsigned int i;
#if DEBUG
  GString *s;
  GQueue *q;
#endif

#if DEBUG
  g_debug ("----- ENTER spreadmodel_extend_rotating_array");
#endif

  old_length = array->len;
  if (old_length >= length)
    goto end;

#if DEBUG
  s = g_string_new ("old array = [");
  for (i = 0; i < old_length; i++)
    {
      if (i > 0)
        g_string_append_c (s, ',');
      if (i == index)
        g_string_append_c (s, '(');
      q = (GQueue *) g_ptr_array_index (array, i);
      if (q == NULL)
        g_string_append_c (s, 'x');
      else
        g_string_append_printf (s, "%u", g_queue_get_length (q));
      if (i == index)
        g_string_append_c (s, ')');
    }
  g_string_append_c (s, ']');
  g_debug ("%s", s->str);
  g_string_free (s, TRUE);
#endif

  g_ptr_array_set_size (array, length);

  /* Move as many items as possible from the start of the list to the new end
   * of the list. */
  diff = length - old_length;
  for (i = 0; i < diff; i++)
    if (i <= index)
      {
        #if DEBUG
          g_debug ("copying item at pos %u to pos %u", i, old_length + i);
        #endif
        g_ptr_array_index (array, old_length + i) = g_ptr_array_index (array, i);
      }
    else
      {
        #if DEBUG
          g_debug ("adding empty item at pos %u", old_length + i);
        #endif
        g_ptr_array_index (array, old_length + i) = g_queue_new ();
      }

  /* If there are still items sitting just before or at the rotating index
   * position, move them down to the start of the list. */
  for (i = 0; i + diff <= index; i++)
    {
      #if DEBUG
        g_debug ("copying item at pos %u to pos %u", i + diff, i);
      #endif
      g_ptr_array_index (array, i) = g_ptr_array_index (array, i + diff);
    }
  for (; i <= index; i++)
    {
      #if DEBUG
        g_debug ("adding empty item at pos %u", i);
      #endif
      g_ptr_array_index (array, i) = g_queue_new ();
    }

#if DEBUG
  s = g_string_new ("new array = [");
  for (i = 0; i < length; i++)
    {
      if (i > 0)
        g_string_append_c (s, ',');
      if (i == index)
        g_string_append_c (s, '(');
      q = (GQueue *) g_ptr_array_index (array, i);
      if (q == NULL)
        g_string_append_c (s, 'x');
      else
        g_string_append_printf (s, "%u", g_queue_get_length (q));
      if (i == index)
        g_string_append_c (s, ')');
    }
  g_string_append_c (s, ']');
  g_debug ("%s", s->str);
  g_string_free (s, TRUE);
#endif

end:
#if DEBUG
  g_debug ("----- EXIT spreadmodel_extend_rotating_array");
#endif

  return;
}



/**
 * The g_queue_free function from GLib, cast to the format of a GDestroyNotify
 * function.
 */
void
g_queue_free_as_GDestroyNotify (gpointer data)
{
  g_queue_free ((GQueue *) data);
}



/**
 * Modify a provided output file name.  If the program is compiled without MPI
 * support, this just returns a string copy of <i>filename</i>.  If the program
 * is compiled with MPI support, this inserts the node number just before the
 * file extension, or at the end of the filename if there is no file extension.
 */
char *
spreadmodel_insert_node_number_into_filename (const char *filename)
{
#if HAVE_MPI && !CANCEL_MPI
  GString *s;
  char *last_dot;
  char *chararray;

  s = g_string_new (NULL);
  last_dot = rindex (filename, '.');
  if (last_dot == NULL)
    {
      /* No file extension; just append the MPI node number. */
      g_string_printf (s, "%s%i", filename, me.rank);
    }
  else
    {
      /* Insert the MPI node number just before the extension. */
      g_string_insert_len (s, -1, filename, last_dot - filename);
      g_string_append_printf (s, "%i", me.rank);
      g_string_insert_len (s, -1, last_dot, strlen (filename) - (last_dot - filename));
    }

  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
#else
  return g_strdup (filename);
#endif
}

/* end of file module_util.c */
