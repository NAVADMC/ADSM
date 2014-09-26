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
#  include "config.h"
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
adsm_read_prodtype (char *text, GPtrArray * production_type_names)
{
  gchar *normalized;
  guint nprod_types;
  guint loc;

  #if DEBUG
    g_debug ("----- ENTER adsm_read_prodtype");
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
    g_debug ("----- EXIT adsm_read_prodtype");
  #endif

  return loc;
}



/**
 * Compares a text string against a list of production type names. Returns the
 * position of the matching name in the list.
 */
guint
adsm_read_zone (char *text, ZON_zone_list_t * zones)
{
  gchar *normalized;
  guint nzones;
  guint loc;

  #if DEBUG
    g_debug ("----- ENTER adsm_read_zone");
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
    g_debug ("----- EXIT adsm_read_zone");
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
adsm_extend_rotating_array (GPtrArray * array, unsigned int length, unsigned int index)
{
  unsigned int old_length, diff;
  unsigned int i;
#if DEBUG
  GString *s;
  GQueue *q;
#endif

#if DEBUG
  g_debug ("----- ENTER adsm_extend_rotating_array");
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
  g_debug ("----- EXIT adsm_extend_rotating_array");
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
 * Modify a provided file name.  Inserts the given number just before the file
 * extension, or at the end of the filename if there is no file extension.
 */
char *
adsm_insert_number_into_filename (const char *filename, int number)
{
  GString *s;
  char *last_dot;

  s = g_string_new (NULL);
  last_dot = strrchr (filename, '.');
  if (last_dot == NULL)
    {
      /* No file extension; just append the number. */
      g_string_printf (s, "%s%i", filename, number);
    }
  else
    {
      /* Insert the number just before the extension. */
      g_string_insert_len (s, -1, filename, last_dot - filename);
      g_string_append_printf (s, "%i", number);
      g_string_insert_len (s, -1, last_dot, strlen (filename) - (last_dot - filename));
    }

  /* don't return the wrapper object */
  return g_string_free (s, FALSE);
}



/**
 * Fills in an array with the production types by priority order. This function
 * will be called once per production type, with the first call containing the
 * highest-priority production type.
 *
 * @param data a GPtrArray in which to store the production type names. The
 *   production type names are copied from the query result and should be freed
 *   using g_free().
 * @param ncols number of columns in the SQL query result.
 * @param values values returned by the SQL query, all in text form.
 * @param colname names of columns in the SQL query result.
 * @return 0
 */
static int
read_prodtype_order_callback (void *data, int ncols, char **value, char **colname)
{
  GPtrArray *prodtype_order;
  
  g_assert (ncols == 1);
  prodtype_order = (GPtrArray *)data;
  g_ptr_array_add (prodtype_order, g_strdup(value[0]));
  
  return 0;
}



/**
 * Fills in an array with the reasons in priority order.
 *
 * @param data location of an array in which to store the reasons.
 * @param ncols number of columns in the SQL query result.
 * @param values values returned by the SQL query, all in text form.
 * @param colname names of columns in the SQL query result.
 * @return 0
 */
static int
read_reason_order_callback (void *data, int ncols, char **value, char **colname)
{
  ADSM_control_reason *reason_order;
  guint priority;
  gchar **tokens, **iter;

  g_assert (ncols == 1);
  reason_order = (ADSM_control_reason *)data;
  /* The reason order is given in a comma-separated string in value[0]. */
  tokens = g_strsplit (value[0], ",", 0);
  for (iter = tokens, priority = 0; *iter != NULL; iter++)
    {
      ADSM_control_reason reason;
      g_strstrip (*iter);
      for (reason = 0; reason < ADSM_NCONTROL_REASONS; reason++)
        {
          if (strcmp (*iter, ADSM_control_reason_name[reason]) == 0)
            break;
        }
      g_assert (reason < ADSM_NCONTROL_REASONS);
      reason_order[priority++] = reason;
    }
  g_strfreev (tokens);

  return 0;
}



/**
 * Finds out whether reason has priority over production type.
 *
 * @param data pointer to a boolean in which to store the answer.
 * @param ncols number of columns in the SQL query result.
 * @param values values returned by the SQL query, all in text form.
 * @param colname names of columns in the SQL query result.
 * @return 0
 */
static int
read_primary_order_callback (void *data, int ncols, char **value, char **colname)
{
  gboolean *reason_has_priority_over_prodtype;
  gchar *reason_loc, *prodtype_loc;
 
  g_assert (ncols == 1);
  reason_has_priority_over_prodtype = (gboolean *)data;
  reason_loc = strstr (value[0], "reason");
  prodtype_loc = strstr (value[0], "production type");
  *reason_has_priority_over_prodtype = (reason_loc < prodtype_loc);

  return 0;
}



#if DEBUG
static void
build_priority_debug_string (gpointer key,
                             gpointer value,
                             gpointer user_data)
{
  char *prodtype_reason_combo;
  guint priority;
  GString *s;

  prodtype_reason_combo = (char *)key;
  priority = GPOINTER_TO_UINT(value);
  s = (GString *)user_data;
  
  if (s->len == 0)
    {
      g_string_append_c (s, '{');
    }
  else
    {
      g_string_append_c (s, ',');
    }
  g_string_append_printf (s, "%s:%u", prodtype_reason_combo, priority);

  return;
}
#endif

/**
 * Reads the destruction priority order from the parameters database. Returns
 * a GHashTable in which keys are strings (char *) of the form
 * "production type,reason". Reason is one of the strings from
 * ADSM_control_reason_name. Values are ints stored using
 * GUINT_TO_POINTER.
 *
 * The hash table has a key_destroy_func and value_destroy_func set, so a call
 * to g_hash_table_destroy will fully clean up all memory used.
 */ 
GHashTable *
adsm_read_priority_order (sqlite3 *params)
{
  GHashTable *table;
  gboolean reason_has_priority_over_prodtype;
  ADSM_control_reason *reason_order; /**< An array containing the
    elements in the enumeration ADSM_control_reason, in order of
    descending priority (that is, the highest priority reason is at the start
    of the list). */
  GPtrArray *prodtype_order; /**< A GPtrArray containing production type names
    (char *) in order of descending priority (that is, the highest priority
    production type is at the start of the list). */
  guint priority;
  guint i, j;
  char *sqlerr;

  /* First find out if reason has priority over production type. */
  sqlite3_exec (params,
                "SELECT destruction_priority_order FROM ScenarioCreator_controlmasterplan",
                read_primary_order_callback, &reason_has_priority_over_prodtype, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }
  #if DEBUG
    if (reason_has_priority_over_prodtype)
      g_debug ("reason has priority over production type");
    else
      g_debug ("production type has priority over reason");
  #endif

  /* Next get the relative ordering of reasons. */
  reason_order = g_new0 (ADSM_control_reason, ADSM_NCONTROL_REASONS);
  sqlite3_exec (params,
                "SELECT destruction_reason_order FROM ScenarioCreator_controlmasterplan",
                read_reason_order_callback, reason_order, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }
  #if DEBUG
  {
    GString *s;
    int i;
    s = g_string_new (NULL);
    for (i = 0; i < ADSM_NCONTROL_REASONS; i++)
      {
        if (i > 0)
          g_string_append_c (s, ',');
        g_string_append_printf (s, "%s", ADSM_control_reason_name[reason_order[i]]);
      }
    g_debug ("reason order (highest priority first): %s", s->str);
    g_string_free (s, TRUE);
  }
  #endif

  /* Next get the relative ordering of production types. */
  prodtype_order = g_ptr_array_new_with_free_func (g_free);
  sqlite3_exec (params,
                "SELECT prodtype.name FROM ScenarioCreator_productiontype prodtype,ScenarioCreator_controlprotocol protocol,ScenarioCreator_protocolassignment xref WHERE prodtype.id=xref.production_type_id AND xref.control_protocol_id=protocol.id ORDER BY destruction_priority ASC",
                read_prodtype_order_callback, prodtype_order, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }
  #if DEBUG
  {
    GString *s;
    int i;
    s = g_string_new (NULL);
    for (i = 0; i < prodtype_order->len; i++)
      {
        if (i > 0)
          g_string_append_c (s, ',');
        g_string_append_printf (s, "%s", (char *)g_ptr_array_index(prodtype_order, i));
      }
    g_debug ("production type order (highest priority first): %s", s->str);
    g_string_free (s, TRUE);
  }
  #endif

  /* Create the hash table to return. */
  table = g_hash_table_new_full (g_str_hash, g_str_equal, g_free, NULL);
  priority = 1;
  if (reason_has_priority_over_prodtype)
    {
      for (i = 0; i < ADSM_NCONTROL_REASONS; i++)
        {
          const char *reason;
          reason = ADSM_control_reason_name[reason_order[i]];
          for (j = 0; j < prodtype_order->len; j++)
            {
              char *prodtype;
              char *key;
              prodtype = (char *)g_ptr_array_index(prodtype_order, j);
              key = g_strdup_printf ("%s,%s", prodtype, reason);
              g_hash_table_replace (table, key, GUINT_TO_POINTER(priority++));
            }
        }
    }
  else
    {
      for (i = 0; i < prodtype_order->len; i++)
        {
          char *prodtype;
          prodtype = (char *)g_ptr_array_index(prodtype_order, i);
          for (j = 0; j < ADSM_NCONTROL_REASONS; j++)
            {
              const char *reason;
              char *key;
              reason = ADSM_control_reason_name[reason_order[j]];
              key = g_strdup_printf ("%s,%s", prodtype, reason);
              g_hash_table_replace (table, key, GUINT_TO_POINTER(priority++));
            }
        }              
    }

  #if DEBUG
  {
    GString *s;
    s = g_string_new (NULL);
    g_hash_table_foreach (table, build_priority_debug_string, s);
    g_string_append_c (s, '}');
    g_debug ("priority order = %s", s->str);
    g_string_free (s, TRUE);
  }
  #endif

  /* Clean up */
  g_free (reason_order);
  g_ptr_array_free (prodtype_order, /* free_seg = */ TRUE);

  return table;
}

/* end of file module_util.c */
