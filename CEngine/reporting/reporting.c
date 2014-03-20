/** @file reporting.c
 * Functions for creating, destroying, printing, and manipulating reporting
 * variables.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date February 2004
 *
 * Copyright &copy; University of Guelph, 2004-2009
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#if HAVE_CONFIG_H
#  include <config.h>
#endif

#include "reporting.h"

#if STDC_HEADERS
#  include <stdlib.h>
#  include <string.h>
#endif

#if HAVE_STRINGS_H
#  include <strings.h>
#endif



/**
 * Names for the possible output variable types, terminated with a NULL
 * sentinel.
 *
 * @sa RPT_type_t
 */
const char *RPT_type_name[] = {
  "integer", "real", "group", "unknown_type", NULL
};



/**
 * Names for the possible reporting frequencies for an output variable,
 * terminated with a NULL sentinel.
 *
 * @sa RPT_frequency_t
 */
const char *RPT_frequency_name[] = { "never", "once", "daily", NULL };



/**
 * The number of days between reporting, corresponding to the possible
 * reporting frequencies for an output variable.
 *
 * @sa RPT_frequency_t
 */
const int RPT_frequency_day[] = { 0, 0, 1 };



/**
 * Creates a new output variable structure.
 *
 * @param name the variable's name.  Should not contain commas, single quotes
 *   ('), double quotes ("), newlines, or carriage returns.  The text is copied
 *   so the original string can be freed after calling this function.
 * @param type the variable's data type.
 * @param frequency how often the variable is reported.
 * @return a pointer to a newly-created, initialized RPT_reporting_t structure.
 */
RPT_reporting_t *
RPT_new_reporting (const char *name, RPT_type_t type, RPT_frequency_t frequency)
{
  RPT_reporting_t *reporting;

  reporting = g_new (RPT_reporting_t, 1);

  if (name != NULL
      && (strchr (name, ',') != NULL
          || strchr (name, '\'') != NULL
          || strchr (name, '"') != NULL
          || strchr (name, '\n') != NULL || strchr (name, '\r') != NULL))
    g_warning
      ("variable name \"%s\" contains a comma, quote, or newline; this may cause problems when parsing the simulation output",
       name);
  reporting->name = g_strdup (name);
  reporting->type = type;
  switch (type)
    {
    case RPT_integer:
      reporting->data = g_new0 (long, 1);
      break;
    case RPT_real:
      reporting->data = g_new0 (double, 1);
      break;
    case RPT_group:
      g_datalist_init ((GData **) (&reporting->data));
      break;
    default:
      g_assert_not_reached ();
    }
  reporting->frequency = frequency;
  reporting->days = RPT_frequency_day[frequency];
  reporting->is_null = FALSE;

  return reporting;
}



/**
 * A structure for use with the function stitch_names, below.
 */
typedef struct
{
  GString *name_so_far;
  GPtrArray *names;
}
RPT_stitch_names_t;



/**
 * Returns all the names in an output variable.  This function is mostly useful
 * for output variables with sub-categories (and maybe sub-sub-categories,
 * etc.).  The function is typed as a GDataForeachFunc so that it can easily be
 * called recursively on the sub-categories.
 *
 * @param key_id use 0.
 * @param data an output variable, cast to a gpointer.
 * @param user_data a RPT_stitch_names_t structure, containing the output
 *   variable's name as seen so far (a GString, which should be NULL for the
 *   top-level call), and the GPtrArray into which the complete variable names
 *   (in char * format) should be copied.
 */
void
stitch_names (GQuark key_id, gpointer data, gpointer user_data)
{
  RPT_reporting_t *reporting;
  RPT_stitch_names_t *passed_to_me, *to_pass;
  GString *name_so_far;
  GPtrArray *names;
  GString *name;

#if DEBUG
  g_debug ("----- ENTER stitch_names");
#endif

  reporting = (RPT_reporting_t *) data;
  passed_to_me = (RPT_stitch_names_t *) user_data;
  name_so_far = passed_to_me->name_so_far;
  names = passed_to_me->names;

  if (reporting != NULL)
    {
      if (name_so_far == NULL)
        name = g_string_new (reporting->name);
      else
        {
          name = g_string_new (name_so_far->str);
          g_string_append_printf (name, " %s", reporting->name);
        }

      if (reporting->type != RPT_group)
        {
          /* We've reached the end of a chain of recursive calls -- this
           * variable has no sub-categories.  Add its completed name to the
           * list. */
          g_ptr_array_add (names, name->str);
#if DEBUG
          g_debug ("adding completed name \"%s\"", name->str);
#endif
          g_string_free (name, FALSE);
        }
      else
        {
#if DEBUG
          g_debug ("going into sub-categories for \"%s\"", name->str);
#endif
          to_pass = g_new (RPT_stitch_names_t, 1);
          to_pass->names = names;
          to_pass->name_so_far = name;
          g_datalist_foreach ((GData **) (&reporting->data), stitch_names, to_pass);
          g_string_free (name, TRUE);
          g_free (to_pass);
        }
    }

#if DEBUG
  g_debug ("----- EXIT stitch_names");
#endif
  return;
}



/**
 * A structure for use with the function stitch, below.
 */
typedef struct
{
  GPtrArray *strings;
  char *format;
}
RPT_stitch_t;



/**
 * This function is meant to be used with the foreach function of a GLib Keyed
 * Data List, specifically, the Keyed Data List used in "group" output
 * variables.  It adds strings of the form "'variable-name':value" to a Pointer
 * Array.
 *
 * @param key_id the key.  Resolved to a string, the name of an output
 *   variable.
 * @param data an output variable, cast to a gpointer.
 * @param user_data a pointer to an RPT_stitch_t structure, cast to a gpointer.
 */
void
stitch (GQuark key_id, gpointer data, gpointer user_data)
{
  RPT_stitch_t *to_pass;
  RPT_reporting_t *reporting;
  GString *s;
  char *substring, *chararray;

#if DEBUG
  g_debug ("----- ENTER stitch");
#endif

  reporting = (RPT_reporting_t *) data;
  to_pass = (RPT_stitch_t *) user_data;

  /* Append the variable name, in single quotes, to the string we're
   * building. */
  s = g_string_new (NULL);
  g_string_printf (s, "'%s'", g_quark_to_string (key_id));

  /* Append a colon and the value to the string we're building. */
  substring = RPT_reporting_value_to_string (reporting, to_pass->format);
  g_string_sprintfa (s, ":%s", substring);
  g_free (substring);

  /* Append the completed string, but not the wrapper object, to the list. */
  chararray = s->str;
  g_string_free (s, FALSE);
  g_ptr_array_add (to_pass->strings, chararray);

#if DEBUG
  g_debug ("----- EXIT stitch");
#endif
}



/**
 * Returns all the names in an output variable.  This function is mostly useful
 * for output variables with sub-categories (and maybe sub-sub-categories,
 * etc.).
 *
 * @param reporting an output variable.
 * @return a list of names, in (char *) format.  These names have been copied
 *   so they may be freed with g_free once you are finished with them.
 */
GPtrArray *
RPT_reporting_names (RPT_reporting_t *reporting)
{
  GPtrArray *names;
  RPT_stitch_names_t *to_pass;

#if DEBUG
  g_debug ("----- ENTER RPT_reporting_names");
#endif

  names = g_ptr_array_new();
  to_pass = g_new (RPT_stitch_names_t, 1);
  to_pass->names = names;
  to_pass->name_so_far = NULL;
  stitch_names (0, (gpointer) reporting, (gpointer) to_pass);
  g_free (to_pass);

#if DEBUG
  g_debug ("----- EXIT RPT_reporting_names");
#endif

  return names;
}



/**
 * Returns all the values in an output variable, in (char *) string format.  
 * This function is mostly useful for output variables with sub-categories
 * (and maybe sub-sub-categories, etc.).  The function is typed as a
 * GDataForeachFunc so that it can easily be called recursively on the
 * sub-categories.
 *
 * @param key_id use 0.
 * @param data an output variable, cast to a gpointer.
 * @param user_data a GPtrArray (cast to a gpointer) into which the values (in
 *   char * format) should be copied.
 */
void
stitch_values (GQuark key_id, gpointer data, gpointer user_data)
{
  RPT_reporting_t *reporting;
  GPtrArray *values;

#if DEBUG
  g_debug ("----- ENTER stitch_values");
#endif

  reporting = (RPT_reporting_t *) data;
  values = (GPtrArray *) user_data;

  /* It's important that this function traverses in the same order as
   * stitch_names. */
  if (reporting != NULL)
    {
#if DEBUG
      g_debug ("variable or subcategory name = \"%s\"", reporting->name);
#endif
      if (reporting->type != RPT_group)
        {
          /* We've reached the end of a chain of recursive calls -- this
           * variable has no sub-categories.  Add its value to the list. */
          g_ptr_array_add (values, RPT_reporting_value_to_string (reporting, NULL));
        }
      else
        {
          g_datalist_foreach ((GData **) (&reporting->data), stitch_values, values);
        }
    }

#if DEBUG
  g_debug ("----- EXIT stitch_values");
#endif
  return;
}



/**
 * Returns all the values in an output variable, in (char *) string format.
 * This function is mostly useful for output variables with sub-categories (and
 * maybe sub-sub-categories, etc.).
 *
 * @param reporting an output variable.
 * @return a list of values, in (char *) format.  These names have been copied
 *   so they may be freed with g_free once you are finished with them.
 */
GPtrArray *
RPT_reporting_values_as_strings (RPT_reporting_t *reporting)
{
  GPtrArray *values;

#if DEBUG
  g_debug ("----- ENTER RPT_reporting_values_as_strings");
#endif

  values = g_ptr_array_new();
  stitch_values (0, (gpointer) reporting, (gpointer) values);

#if DEBUG
  g_debug ("----- EXIT RPT_reporting_values_as_strings");
#endif

  return values;
}



/**
 * Sums the number of values in an output variable.  This function is mostly
 * useful for output variables with sub-categories (and maybe
 * sub-sub-categories, etc.).  The function is typed as a GDataForeachFunc so
 * that it can easily be called recursively on the sub-categories.
 *
 * @param key_id use 0.
 * @param data an output variable, cast to a gpointer.
 * @param user_data a pointer to an integer (cast to a gpointer) which holds
 *   the running sum.
 */
void
stitch_counts (GQuark key_id, gpointer data, gpointer user_data)
{
  RPT_reporting_t *reporting;
  unsigned int *sum;

#if DEBUG
  g_debug ("----- ENTER stitch_counts");
#endif

  reporting = (RPT_reporting_t *) data;
  sum = (unsigned int *) user_data;

  if (reporting != NULL)
    {
      if (reporting->type != RPT_group)
        {
          /* We've reached the end of a chain of recursive calls -- this
           * variable has no sub-categories.  Add 1. */
          *sum = *sum + 1;
        }
      else
        {
          g_datalist_foreach ((GData **) (&reporting->data), stitch_counts, sum);
        }
    }

#if DEBUG
  g_debug ("----- EXIT stitch_counts");
#endif
  return;
}



/**
 * Sums the number of values in an output variable.  This function is mostly
 * useful for output variables with sub-categories (and maybe
 * sub-sub-categories, etc.).
 *
 * @param reporting an output variable.
 * @return a list of values, in (char *) format.  These names have been copied
 *   so they may be freed with g_free once you are finished with them.
 */
unsigned int
RPT_reporting_var_count (RPT_reporting_t *reporting)
{
  unsigned int sum;

#if DEBUG
  g_debug ("----- ENTER RPT_reporting_var_count");
#endif

  sum = 0;
  stitch_counts (0, (gpointer) reporting, (gpointer) (&sum));

#if DEBUG
  g_debug ("----- EXIT RPT_reporting_var_count");
#endif

  return sum;
}



/**
 * A callback function for use with the function g_datalist_size, below.  It
 * increments a counter.
 *
 * @param key_id a key.
 * @param data the data element associated with the key.
 * @param user_data pointer to a count of elements (type guint).
 */
void
count_as_GDataForeachFunc (GQuark key_id, gpointer data, gpointer user_data)
{
  guint *size;
  
  size = (guint *) user_data;
  *size += 1;
  return;
}



/**
 * Returns the number of elements contained in a GLib Keyed Data List.
 * Strangely, there's no function for this in GLib.
 *
 * @param datalist a Keyed Data List.
 * @return the number of elements in the list.
 */
guint
g_datalist_size (GData **datalist)
{
   guint size;
   
   size = 0;
   g_datalist_foreach (datalist, count_as_GDataForeachFunc, &size);
   return size;
}



/**
 * Returns whether a GLib Keyed Data List is empty.
 *
 * @param datalist a Keyed Data List.
 * @return TRUE if the list contains no elements, FALSE otherwise.
 */
gboolean
g_datalist_is_empty (GData **datalist)
{
  return (g_datalist_size (datalist) == 0);
}



/**
 * Returns a text representation of the current value of an output variable.
 *
 * @param reporting an output variable.
 * @param format a printf-style format string.  If NULL, will default to "%i"
 *   for integer variables, "%g" for real variables, and ""%s"" for text
 *   variables.
 * @return a string.
 */
char *
RPT_reporting_value_to_string (RPT_reporting_t * reporting, char *format)
{
  GString *s;
  char *substring, *chararray;
  RPT_stitch_t to_pass;
  unsigned int i;

#if DEBUG
  g_debug ("----- ENTER RPT_reporting_value_to_string");
#endif

  s = g_string_new (NULL);
  /* Represent an output variable that is null (has no meaningful value yet)
   * by an empty string, except in the case of a group variable that has sub-
   * categories.  We'll handle that case below. */
  if (RPT_reporting_is_null (reporting, NULL)
      && (reporting->type != RPT_group
          || g_datalist_is_empty ((GData **) (&reporting->data))))
    {
      g_string_printf (s, "");
    }
  else
    switch (reporting->type)
      {
      case RPT_integer:
        if (format == NULL)
          format = "%i";
        g_string_printf (s, format, *((long *) reporting->data));
        break;
      case RPT_real:
        if (format == NULL)
          format = "%g";
        g_string_printf (s, format, *((double *) reporting->data));
        break;
      case RPT_group:
        g_string_append_c (s, '{');
        to_pass.strings = g_ptr_array_new ();
        to_pass.format = format;
        g_datalist_foreach ((GData **) (&reporting->data), stitch, &to_pass);
        /* Append the string for each variable in the group, separated by commas,
         * to the string we're building.  Free the substrings as we go. */
        for (i = 0; i < to_pass.strings->len; i++)
          {
            substring = (char *) g_ptr_array_index (to_pass.strings, i);
            g_string_append_printf (s, i > 0 ? ",%s" : "%s", substring);
            g_free (substring);
          }
        g_ptr_array_free (to_pass.strings, TRUE);
        g_string_append_c (s, '}');
        break;
      default:
        g_assert_not_reached ();
      }
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);

#if DEBUG
  g_debug ("----- EXIT RPT_reporting_value_to_string");
#endif

  return chararray;
}



/**
 * Returns a text representation of an output variable.
 *
 * @param reporting an output variable.
 * @return a string.
 */
char *
RPT_reporting_to_string (RPT_reporting_t * reporting)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_printf (s, "<%s output variable \"%s\"",
                   RPT_type_name[reporting->type], reporting->name);

  g_string_append_printf (s, " \n reported %s ", RPT_frequency_name[reporting->frequency]);

  g_string_append_c (s, '>');

  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Prints an output variable to a stream.
 *
 * @param stream an output stream to write to.  If NULL, defaults to stdout.
 * @param reporting an output variable.
 * @return the number of characters written.
 */
int
RPT_fprintf_reporting (FILE * stream, RPT_reporting_t * reporting)
{
  char *s;
  int nchars_written;

  s = RPT_reporting_to_string (reporting);
  nchars_written = fprintf (stream ? stream : stdout, "%s", s);
  free (s);
  return nchars_written;
}



/**
 * Deletes an output variable structure from memory.
 *
 * @param reporting an output variable.  If NULL, nothing is deleted.
 */
void
RPT_free_reporting (RPT_reporting_t * reporting)
{
#if DEBUG
  g_debug ("----- ENTER RPT_free_reporting");
#endif

  if (reporting != NULL)
    {
      g_free (reporting->name);
      switch (reporting->type)
        {
        case RPT_integer:
        case RPT_real:
          g_free (reporting->data);
          break;
        case RPT_group:
          g_datalist_clear ((GData **) (&reporting->data));
          break;
        default:
          g_assert_not_reached ();
        }
      g_free (reporting);
    }

#if DEBUG
  g_debug ("----- EXIT RPT_free_reporting");
#endif
  return;
}



/**
 * Wraps RPT_free_reporting so that it can be used as the destroy function in
 * a keyed data list.
 */
void
RPT_free_reporting_as_GDestroyNotify (gpointer data)
{
  RPT_free_reporting ((RPT_reporting_t *) data);
}



/**
 * Sets the reporting frequency for an output variable.
 *
 * @param reporting an output variable.
 * @param frequency how often the variable is reported.
 */
void
RPT_reporting_set_frequency (RPT_reporting_t * reporting, RPT_frequency_t frequency)
{
  reporting->frequency = frequency;
  reporting->days = RPT_frequency_day[frequency];
}



/**
 * Sets the value of an integer output variable.
 *
 * @param reporting an output variable.
 * @param value the new value. 
 * @param subelement_name a null-terminated array of strings used to "drill
 *   down" through group output variables.  If NULL, <i>reporting</i> is
 *   assumed to be an integer output variable.
 */
void
RPT_reporting_set_integer (RPT_reporting_t * reporting, long value, const char **subelement_name)
{
  GData **group;
  RPT_reporting_t *subelement;

  if (subelement_name == NULL || subelement_name[0] == NULL)
    {
      g_assert (reporting->type == RPT_integer);
      *((long *) reporting->data) = value;
    }
  else
    {
      if (reporting->type != RPT_group)
        g_error ("Attempting to drill down to subelement \"%s\" of variable \"%s\", but \"%s\" is type %s, not group",
                 subelement_name[0], reporting->name, reporting->name,
                 RPT_type_name[reporting->type]);
      group = (GData **) (&reporting->data);
      subelement = (RPT_reporting_t *) (g_datalist_get_data (group, subelement_name[0]));
      /* If there isn't already a subelement by this name, create one. */
      if (subelement == NULL)
        {
          if (subelement_name[1] == NULL)
            /* The current subelement name is the last one in the list; the
             * next output variable down will be an integer variable. */
            subelement = RPT_new_reporting (subelement_name[0], RPT_integer,
                                            reporting->frequency);
          else
            /* There are more subelement names in the list; the next output
             * variable down will be another group variable. */
            subelement = RPT_new_reporting (subelement_name[0], RPT_group,
                                            reporting->frequency);
          g_datalist_set_data_full (group, subelement_name[0], subelement,
                                    RPT_free_reporting_as_GDestroyNotify);
        }
      RPT_reporting_set_integer (subelement, value, &(subelement_name[1]));
    }

  reporting->is_null=FALSE;
  return;
}



/**
 * Sets the value of an integer output variable (alternate version for group
 * variables only 1 level deep).
 *
 * @param reporting an output variable.
 * @param value the new value. 
 * @param subelement_name a string used to choose one element from a group
 *   output variable.  If NULL, <i>reporting</i> is assumed to be an integer
 *   output variable.
 */
void
RPT_reporting_set_integer1 (RPT_reporting_t * reporting, long value, const char *subelement_name)
{
  GData **group;
  RPT_reporting_t *subelement;

  if (subelement_name == NULL)
    {
      g_assert (reporting->type == RPT_integer);
      *((long *) reporting->data) = value;
    }
  else
    {
      if (reporting->type != RPT_group)
        g_error ("Attempting to drill down to subelement \"%s\" of variable \"%s\", but \"%s\" is type %s, not group",
                 subelement_name[0], reporting->name, reporting->name,
                 RPT_type_name[reporting->type]);
      group = (GData **) (&reporting->data);
      subelement = (RPT_reporting_t *) (g_datalist_get_data (group, subelement_name));
      /* If there isn't already a subelement by this name, create one. */
      if (subelement == NULL)
        {
          subelement = RPT_new_reporting (subelement_name, RPT_integer,
                                          reporting->frequency);
          g_datalist_set_data_full (group, subelement_name, subelement,
                                    RPT_free_reporting_as_GDestroyNotify);
        }
      RPT_reporting_set_integer (subelement, value, NULL);
    }

  reporting->is_null = FALSE;
  return;
}



/**
 * Adds to the value of an integer output variable.
 *
 * @param reporting an output variable.
 * @param value the amount to add. 
 * @param subelement_name a null-terminated array of strings used to "drill
 *   down" through group output variables.  If NULL, <i>reporting</i> is
 *   assumed to be an integer output variable.
 */
void
RPT_reporting_add_integer (RPT_reporting_t * reporting, long value, const char **subelement_name)
{
  GData **group;
  RPT_reporting_t *subelement;

  if (subelement_name == NULL || subelement_name[0] == NULL)
    {
      g_assert (reporting->type == RPT_integer);
      *((long *) reporting->data) += value;
    }
  else
    {
      if (reporting->type != RPT_group)
        g_error ("Attempting to drill down to subelement \"%s\" of variable \"%s\", but \"%s\" is type %s, not group",
                 subelement_name[0], reporting->name, reporting->name,
                 RPT_type_name[reporting->type]);
      group = (GData **) (&reporting->data);
      subelement = (RPT_reporting_t *) (g_datalist_get_data (group, subelement_name[0]));
      /* If there isn't already a subelement by this name, create one. */
      if (subelement == NULL)
        {
          if (subelement_name[1] == NULL)
            /* The current subelement name is the last one in the list; the
             * next output variable down will be an integer variable. */
            subelement = RPT_new_reporting (subelement_name[0], RPT_integer,
                                            reporting->frequency);
          else
            /* There are more subelement names in the list; the next output
             * variable down will be another group variable. */
            subelement = RPT_new_reporting (subelement_name[0], RPT_group,
                                            reporting->frequency);
          g_datalist_set_data_full (group, subelement_name[0], subelement,
                                    RPT_free_reporting_as_GDestroyNotify);
        }
      RPT_reporting_add_integer (subelement, value, &(subelement_name[1]));
    }

  reporting->is_null = FALSE;
  return;
}



/**
 * Adds to the value of an integer output variable (alternate version for group
 * variables only 1 level deep).
 *
 * @param reporting an output variable.
 * @param value the amount to add. 
 * @param subelement_name a string used to choose one element from a group
 *   output variable.  If NULL, <i>reporting</i> is assumed to be an integer
 *   output variable.
 */
void
RPT_reporting_add_integer1 (RPT_reporting_t * reporting, long value, const char *subelement_name)
{
  GData **group;
  RPT_reporting_t *subelement;

  if (subelement_name == NULL)
    {
      g_assert (reporting->type == RPT_integer);
      *((long *) reporting->data) += value;
    }
  else
    {
      if (reporting->type != RPT_group)
        g_error ("Attempting to drill down to subelement \"%s\" of variable \"%s\", but \"%s\" is type %s, not group",
                 subelement_name[0], reporting->name, reporting->name,
                 RPT_type_name[reporting->type]);
      group = (GData **) (&reporting->data);
      subelement = (RPT_reporting_t *) (g_datalist_get_data (group, subelement_name));
      /* If there isn't already a subelement by this name, create one. */
      if (subelement == NULL)
        {
          subelement = RPT_new_reporting (subelement_name, RPT_integer,
                                          reporting->frequency);
          g_datalist_set_data_full (group, subelement_name, subelement,
                                    RPT_free_reporting_as_GDestroyNotify);
        }
      RPT_reporting_add_integer (subelement, value, NULL);
    }

  reporting->is_null = FALSE;
  return;
}



/**
 * Retrieves the value of an integer output variable.
 *
 * @param reporting an output variable.
 * @param subelement_name a null-terminated array of strings used to "drill
 *   down" through group output variables.  If NULL, <i>reporting</i> is
 *   assumed to be an integer output variable.
 * @returns the value, or 0 if a non-existent subelement was specified.
 */
long
RPT_reporting_get_integer (RPT_reporting_t * reporting, const char **subelement_name)
{
  GData **group;
  RPT_reporting_t *subelement;
  long value = 0;

  if (subelement_name == NULL || subelement_name[0] == NULL)
    {
      g_assert (reporting->type == RPT_integer);
      value = *((long *) reporting->data);
    }
  else
    {
      if (reporting->type != RPT_group)
        g_error ("Attempting to drill down to subelement \"%s\" of variable \"%s\", but \"%s\" is type %s, not group",
                 subelement_name[0], reporting->name, reporting->name,
                 RPT_type_name[reporting->type]);
      group = (GData **) (&reporting->data);
      subelement = (RPT_reporting_t *) (g_datalist_get_data (group, subelement_name[0]));
      if (subelement != NULL)
        value = RPT_reporting_get_integer (subelement, &(subelement_name[1]));
    }

  return value;
}



/**
 * Retrieves the value of an integer output variable (alternate version for
 * group variables only 1 level deep).
 *
 * @param reporting an output variable.
 * @param subelement_name a string used to choose one element from a group
 *   output variable.  If NULL, <i>reporting</i> is assumed to be an integer
 *   output variable.
 * @returns the value, or 0 if a non-existent subelement was specified.
 */
long
RPT_reporting_get_integer1 (RPT_reporting_t * reporting, const char *subelement_name)
{
  GData **group;
  RPT_reporting_t *subelement;
  long value = 0;

  if (subelement_name == NULL)
    {
      g_assert (reporting->type == RPT_integer);
      value = *((long *) reporting->data);
    }
  else
    {
      if (reporting->type != RPT_group)
        g_error ("Attempting to drill down to subelement \"%s\" of variable \"%s\", but \"%s\" is type %s, not group",
                 subelement_name[0], reporting->name, reporting->name,
                 RPT_type_name[reporting->type]);
      group = (GData **) (&reporting->data);
      subelement = (RPT_reporting_t *) (g_datalist_get_data (group, subelement_name));
      if (subelement != NULL)
        value = RPT_reporting_get_integer (subelement, NULL);
    }

  return value;
}



/**
 * Sets the value of a real output variable.
 *
 * @param reporting an output variable.
 * @param value the new value. 
 * @param subelement_name a null-terminated array of strings used to "drill
 *   down" through group output variables.  If NULL, <i>reporting</i> is
 *   assumed to be a real output variable.
 */
void
RPT_reporting_set_real (RPT_reporting_t * reporting, double value, const char **subelement_name)
{
  GData **group;
  RPT_reporting_t *subelement;

  if (subelement_name == NULL || subelement_name[0] == NULL)
    {
      g_assert (reporting->type == RPT_real);
      *((double *) reporting->data) = value;
    }
  else
    {
      if (reporting->type != RPT_group)
        g_error ("Attempting to drill down to subelement \"%s\" of variable \"%s\", but \"%s\" is type %s, not group",
                 subelement_name[0], reporting->name, reporting->name,
                 RPT_type_name[reporting->type]);
      group = (GData **) (&reporting->data);
      subelement = (RPT_reporting_t *) (g_datalist_get_data (group, subelement_name[0]));
      /* If there isn't already a subelement by this name, create one. */
      if (subelement == NULL)
        {
          if (subelement_name[1] == NULL)
            /* The current subelement name is the last one in the list; the
             * next output variable down will be an real variable. */
            subelement = RPT_new_reporting (subelement_name[0], RPT_real,
                                            reporting->frequency);
          else
            /* There are more subelement names in the list; the next output
             * variable down will be another group variable. */
            subelement = RPT_new_reporting (subelement_name[0], RPT_group,
                                            reporting->frequency);
          g_datalist_set_data_full (group, subelement_name[0], subelement,
                                    RPT_free_reporting_as_GDestroyNotify);
        }
      RPT_reporting_set_real (subelement, value, &(subelement_name[1]));
    }

  reporting->is_null = FALSE;
  return;
}



/**
 * Sets the value of a real output variable (alternate version for group
 * variables only 1 level deep).
 *
 * @param reporting an output variable.
 * @param value the new value. 
 * @param subelement_name a string used to choose one element from a group
 *   output variable.  If NULL, <i>reporting</i> is assumed to be a real output
 *   variable.
 */
void
RPT_reporting_set_real1 (RPT_reporting_t * reporting, double value, const char *subelement_name)
{
  GData **group;
  RPT_reporting_t *subelement;

  if (subelement_name == NULL)
    {
      g_assert (reporting->type == RPT_real);
      *((double *) reporting->data) = value;
    }
  else
    {
      if (reporting->type != RPT_group)
        g_error ("Attempting to drill down to subelement \"%s\" of variable \"%s\", but \"%s\" is type %s, not group",
                 subelement_name[0], reporting->name, reporting->name,
                 RPT_type_name[reporting->type]);
      group = (GData **) (&reporting->data);
      subelement = (RPT_reporting_t *) (g_datalist_get_data (group, subelement_name));
      /* If there isn't already a subelement by this name, create one. */
      if (subelement == NULL)
        {
          subelement = RPT_new_reporting (subelement_name, RPT_real,
                                          reporting->frequency);
          g_datalist_set_data_full (group, subelement_name, subelement,
                                    RPT_free_reporting_as_GDestroyNotify);
        }
      RPT_reporting_set_real (subelement, value, NULL);
    }

  reporting->is_null = FALSE;
  return;
}



/**
 * Adds to the value of a real output variable.
 *
 * @param reporting an output variable.
 * @param value the amount to add. 
 * @param subelement_name a null-terminated array of strings used to "drill
 *   down" through group output variables.  If NULL, <i>reporting</i> is
 *   assumed to be a real output variable.
 */
void
RPT_reporting_add_real (RPT_reporting_t * reporting, double value, const char **subelement_name)
{
  GData **group;
  RPT_reporting_t *subelement;

  if (subelement_name == NULL || subelement_name[0] == NULL)
    {
      g_assert (reporting->type == RPT_real);
      *((double *) reporting->data) += value;
    }
  else
    {
      if (reporting->type != RPT_group)
        g_error ("Attempting to drill down to subelement \"%s\" of variable \"%s\", but \"%s\" is type %s, not group",
                 subelement_name[0], reporting->name, reporting->name,
                 RPT_type_name[reporting->type]);
      group = (GData **) (&reporting->data);
      subelement = (RPT_reporting_t *) (g_datalist_get_data (group, subelement_name[0]));
      /* If there isn't already a subelement by this name, create one. */
      if (subelement == NULL)
        {
          if (subelement_name[1] == NULL)
            /* The current subelement name is the last one in the list; the
             * next output variable down will be an integer variable. */
            subelement = RPT_new_reporting (subelement_name[0], RPT_real,
                                            reporting->frequency);
          else
            /* There are more subelement names in the list; the next output
             * variable down will be another group variable. */
            subelement = RPT_new_reporting (subelement_name[0], RPT_group,
                                            reporting->frequency);
          g_datalist_set_data_full (group, subelement_name[0], subelement,
                                    RPT_free_reporting_as_GDestroyNotify);
        }
      RPT_reporting_add_real (subelement, value, &(subelement_name[1]));
    }

  reporting->is_null = FALSE;
  return;
}



/**
 * Adds to the value of a real output variable (alternate version for group
 * variables only 1 level deep).
 *
 * @param reporting an output variable.
 * @param value the amount to add. 
 * @param subelement_name a string used to choose one element from a group
 *   output variable.  If NULL, <i>reporting</i> is assumed to be a real output
 *   variable.
 */
void
RPT_reporting_add_real1 (RPT_reporting_t * reporting, double value, const char *subelement_name)
{
  GData **group;
  RPT_reporting_t *subelement;

  if (subelement_name == NULL)
    {
      g_assert (reporting->type == RPT_real);
      *((double *) reporting->data) += value;
    }
  else
    {
      if (reporting->type != RPT_group)
        g_error ("Attempting to drill down to subelement \"%s\" of variable \"%s\", but \"%s\" is type %s, not group",
                 subelement_name[0], reporting->name, reporting->name,
                 RPT_type_name[reporting->type]);
      group = (GData **) (&reporting->data);
      subelement = (RPT_reporting_t *) (g_datalist_get_data (group, subelement_name));
      /* If there isn't already a subelement by this name, create one. */
      if (subelement == NULL)
        {
          subelement = RPT_new_reporting (subelement_name, RPT_real,
                                          reporting->frequency);
          g_datalist_set_data_full (group, subelement_name, subelement,
                                    RPT_free_reporting_as_GDestroyNotify);
        }
      RPT_reporting_add_real (subelement, value, NULL);
    }

  reporting->is_null = FALSE;
  return;
}



/**
 * Retrieves the value of a real output variable.
 *
 * @param reporting an output variable.
 * @param subelement_name a null-terminated array of strings used to "drill
 *   down" through group output variables.  If NULL, <i>reporting</i> is
 *   assumed to be an real output variable.
 * @returns the value, or 0 if a non-existent subelement was specified.
 */
double
RPT_reporting_get_real (RPT_reporting_t * reporting, const char **subelement_name)
{
  GData **group;
  RPT_reporting_t *subelement;
  double value = 0;

  if (subelement_name == NULL || subelement_name[0] == NULL)
    {
      g_assert (reporting->type == RPT_real);
      value = *((double *) reporting->data);
    }
  else
    {
      if (reporting->type != RPT_group)
        g_error ("Attempting to drill down to subelement \"%s\" of variable \"%s\", but \"%s\" is type %s, not group",
                 subelement_name[0], reporting->name, reporting->name,
                 RPT_type_name[reporting->type]);
      group = (GData **) (&reporting->data);
      subelement = (RPT_reporting_t *) (g_datalist_get_data (group, subelement_name[0]));
      if (subelement != NULL)
        value = RPT_reporting_get_real (subelement, &(subelement_name[1]));
    }

  return value;
}



/**
 * Retrieves the value of a real output variable (alternate version for group
 * variables only 1 level deep).
 *
 * @param reporting an output variable.
 * @param subelement_name a string used to choose one element from a group
 *   output variable.  If NULL, <i>reporting</i> is assumed to be a real
 *   output variable.
 * @returns the value, or 0 if a non-existent subelement was specified.
 */
double
RPT_reporting_get_real1 (RPT_reporting_t * reporting, const char *subelement_name)
{
  GData **group;
  RPT_reporting_t *subelement;
  double value = 0;

  if (subelement_name == NULL)
    {
      g_assert (reporting->type == RPT_real);
      value = *((double *) reporting->data);
    }
  else
    {
      if (reporting->type != RPT_group)
        g_error ("Attempting to drill down to subelement \"%s\" of variable \"%s\", but \"%s\" is type %s, not group",
                 subelement_name[0], reporting->name, reporting->name,
                 RPT_type_name[reporting->type]);
      group = (GData **) (&reporting->data);
      subelement = (RPT_reporting_t *) (g_datalist_get_data (group, subelement_name));
      if (subelement != NULL)
        value = RPT_reporting_get_real (subelement, NULL);
    }

  return value;
}



/**
 * Wraps RPT_reporting_set_null so that it can be used with the foreach
 * function of a GLib Keyed Data List, specifically, the Keyed Data List used
 * in "group" output variables.
 *
 * @param key_id the key.  Resolved to a string, the name of an output
 *   variable.
 * @param data an output variable, cast to a gpointer.
 * @param user_data not used, pass NULL.
 */
void
RPT_reporting_set_null_as_GDataForeachFunc (GQuark key_id, gpointer data, gpointer user_data)
{
#if DEBUG
  g_debug ("----- ENTER RPT_reporting_set_null_as_GDataForeachFunc");
#endif

  RPT_reporting_set_null ((RPT_reporting_t *) data, NULL);

#if DEBUG
  g_debug ("----- EXIT RPT_reporting_set_null_as_GDataForeachFunc");
#endif
}



/**
 * Sets the value of an output variable to "null".
 *
 * @param reporting an output variable.
 * @param subelement_name a null-terminated array of strings used to "drill
 *   down" through group output variables.  Use NULL if the output variable is
 *   not a group variable, or if you want all sub-categories set to NULL.
 */
void
RPT_reporting_set_null (RPT_reporting_t * reporting, const char **subelement_name)
{
  GData **group;
  RPT_reporting_t *subelement;

  if (subelement_name == NULL || subelement_name[0] == NULL)
    {
      if (reporting->type == RPT_group)
        g_datalist_foreach ((GData **) (&reporting->data),
                            RPT_reporting_set_null_as_GDataForeachFunc, NULL);
      else
        RPT_reporting_reset (reporting);
      reporting->is_null = TRUE;
    }
  else
    {
      if (reporting->type != RPT_group)
        g_error ("Attempting to drill down to subelement \"%s\" of variable \"%s\", but \"%s\" is type %s, not group",
                 subelement_name[0], reporting->name, reporting->name,
                 RPT_type_name[reporting->type]);
      group = (GData **) (&reporting->data);
      subelement = (RPT_reporting_t *) (g_datalist_get_data (group, subelement_name[0]));
      /* If there isn't already a subelement by this name, create one. */
      if (subelement == NULL)
        {
          if (subelement_name[1] == NULL)
            /* The current subelement name is the last one in the list; the
             * next output variable down will be an integer variable. */
            subelement = RPT_new_reporting (subelement_name[0], RPT_integer,
                                            reporting->frequency);
          else
            /* There are more subelement names in the list; the next output
             * variable down will be another group variable. */
            subelement = RPT_new_reporting (subelement_name[0], RPT_group,
                                            reporting->frequency);
          g_datalist_set_data_full (group, subelement_name[0], subelement,
                                    RPT_free_reporting_as_GDestroyNotify);
        }
      RPT_reporting_set_null (subelement, &(subelement_name[1]));
    }
}



/**
 * Sets the value of an output variable to "null" (alternate version for group
 * variables only 1 level deep).
 *
 * @param reporting an output variable.
 * @param subelement_name a string used to choose one element from a group
 *   output variable.  Use NULL if the output variable is not a group variable,
 *   or if you want all sub-categories set to NULL.
 */
void
RPT_reporting_set_null1 (RPT_reporting_t * reporting, const char *subelement_name)
{
  GData **group;
  RPT_reporting_t *subelement;

  if (subelement_name == NULL)
    {
      if (reporting->type == RPT_group)
        g_datalist_foreach ((GData **) (&reporting->data),
                            RPT_reporting_set_null_as_GDataForeachFunc, NULL);
      else
        RPT_reporting_reset (reporting);
      reporting->is_null = TRUE;
    }
  else
    {
      if (reporting->type != RPT_group)
        g_error ("Attempting to drill down to subelement \"%s\" of variable \"%s\", but \"%s\" is type %s, not group",
                 subelement_name[0], reporting->name, reporting->name,
                 RPT_type_name[reporting->type]);
      group = (GData **) (&reporting->data);
      subelement = (RPT_reporting_t *) (g_datalist_get_data (group, subelement_name));
      /* If there isn't already a subelement by this name, create one. */
      if (subelement == NULL)
        {
          subelement = RPT_new_reporting (subelement_name, RPT_integer,
                                          reporting->frequency);
          g_datalist_set_data_full (group, subelement_name, subelement,
                                    RPT_free_reporting_as_GDestroyNotify);
        }
      RPT_reporting_set_null (subelement, NULL);
    }
}



/**
 * Checks whether an output variable is null.
 *
 * @param reporting an output variable.
 * @param subelement_name a null-terminated array of strings used to "drill
 *   down" through group output variables.  Use NULL if the output variable is
 *   not a group variable, or if you want to know if all sub-categories are
 *   null.
 * @returns TRUE if the variable is null, FALSE otherwise.
 */
gboolean
RPT_reporting_is_null (RPT_reporting_t * reporting, const char **subelement_name)
{
  GData **group;
  RPT_reporting_t *subelement;
  gboolean answer = TRUE;

  if (subelement_name == NULL || subelement_name[0] == NULL)
    {
      answer = (reporting->is_null);
    }
  else
    {
      if (reporting->type != RPT_group)
        g_error ("Attempting to drill down to subelement \"%s\" of variable \"%s\", but \"%s\" is type %s, not group",
                 subelement_name[0], reporting->name, reporting->name,
                 RPT_type_name[reporting->type]);
      group = (GData **) (&reporting->data);
      subelement = (RPT_reporting_t *) (g_datalist_get_data (group, subelement_name[0]));
      if (subelement != NULL)
        answer = RPT_reporting_is_null (subelement, &(subelement_name[1]));
    }

  return answer;
}



/**
 * Checks whether an output variable is null (alternate version for group
 * variables only 1 level deep).
 *
 * @param reporting an output variable.
 * @param subelement_name a string used to choose one element from a group
 *   output variable.  Use NULL if you want to know if all sub-categories are
 *   null.
 * @returns TRUE if the variable is null, FALSE otherwise.
 */
gboolean
RPT_reporting_is_null1 (RPT_reporting_t * reporting, const char *subelement_name)
{
  GData **group;
  RPT_reporting_t *subelement;
  gboolean answer = TRUE;

  if (subelement_name == NULL)
    {
      answer = (reporting->is_null);
    }
  else
    {
      if (reporting->type != RPT_group)
        g_error ("Attempting to drill down to subelement \"%s\" of variable \"%s\", but \"%s\" is type %s, not group",
                 subelement_name[0], reporting->name, reporting->name,
                 RPT_type_name[reporting->type]);
      group = (GData **) (&reporting->data);
      subelement = (RPT_reporting_t *) (g_datalist_get_data (group, subelement_name));
      if (subelement != NULL)
        answer = RPT_reporting_is_null (subelement, NULL);
    }

  return answer;
}



/**
 * Splices an existing output variable into another as a sub-variable.
 *
 * @param reporting an output variable.
 * @param subvar another output variable, to be added to <i>reporting</i> as a
 *   child.
 */
void
RPT_reporting_splice (RPT_reporting_t * reporting, RPT_reporting_t * subvar)
{
  GData **group;
  RPT_reporting_t *tmp;

  if (subvar == NULL)
    return;

  if (reporting->type != RPT_group)
    {
      g_error
        ("attempting to insert reporting variable \"%s\" into reporting variable \"%s\", which is of type %s, not group.",
         subvar->name, reporting->name, RPT_type_name[reporting->type]);
    }
  group = (GData **) (&reporting->data);

  /* Check for an existing sub-variable with the same name.  If one exists,
   * destroy it. */
  tmp = (RPT_reporting_t *) (g_datalist_get_data (group, subvar->name));
  RPT_free_reporting (tmp);

  g_datalist_set_data_full (group, subvar->name, subvar, RPT_free_reporting_as_GDestroyNotify);

  return;
}



/**
 * Resets an output variable.  Integer and real output variables are set to 0.
 * Group output variables have all sub-variables cleared.  Contrast this with
 * RPT_reporting_zero(), which sets sub-variables to 0 rather than removing
 * them entirely.
 *
 * @sa RPT_reporting_zero
 *
 * @param reporting an output variable.
 */
void
RPT_reporting_reset (RPT_reporting_t * reporting)
{
#if DEBUG
  g_debug ("----- ENTER RPT_reporting_reset");
#endif

  switch (reporting->type)
    {
    case RPT_integer:
      *((long *) reporting->data) = 0;
      break;
    case RPT_real:
      *((double *) reporting->data) = 0;
      break;
    case RPT_group:
      g_datalist_clear ((GData **) (&reporting->data));
      break;
    default:
      g_assert_not_reached ();
    }
  reporting->is_null = FALSE;

#if DEBUG
  g_debug ("----- EXIT RPT_reporting_reset");
#endif
}



/**
 * Wraps RPT_reporting_zero so that it can be used with the foreach function of
 * a GLib Keyed Data List, specifically, the Keyed Data List used in "group"
 * output variables.
 *
 * @param key_id the key.  Resolved to a string, the name of an output
 *   variable.
 * @param data an output variable, cast to a gpointer.
 * @param user_data not used, pass NULL.
 */
void
RPT_reporting_zero_as_GDataForeachFunc (GQuark key_id, gpointer data, gpointer user_data)
{
  RPT_reporting_zero ((RPT_reporting_t *) data);
}



/**
 * Zeroes an output variable.  Integer and real output variables are set to 0.
 * Group output variables have all sub-variables (and sub-sub-variables, etc.)
 * set to 0.  Contrast this with RPT_reporting_reset(), which removes
 * sub-variables entirely rather than setting them to 0.
 *
 * @sa RPT_reporting_reset
 *
 * @param reporting an output variable.
 */
void
RPT_reporting_zero (RPT_reporting_t * reporting)
{
  switch (reporting->type)
    {
    case RPT_integer:
      *((long *) reporting->data) = 0;
      break;
    case RPT_real:
      *((double *) reporting->data) = 0;
      break;
    case RPT_group:
      g_datalist_foreach ((GData **) (&reporting->data),
                          RPT_reporting_zero_as_GDataForeachFunc, NULL);
      break;
    default:
      g_assert_not_reached ();
    }

  return;
}



/**
 * Returns the RPT_frequency_t matching a given string.
 *
 * @param s a string.
 * @return the RPT_frequency_t enumeration value matching <i>s</i>, or
 *   RPT_never if s does not match any enumeration value.
 */
RPT_frequency_t
RPT_string_to_frequency (const char *s)
{
  RPT_frequency_t type;

  for (type = RPT_once; type < RPT_NFREQUENCIES; type++)
    if (strcmp (RPT_frequency_name[type], s) == 0)
      return type;

  return RPT_never;
}



/**
 * Reports whether an output variable should be reported on the given day,
 * FALSE otherwise.
 *
 * @param reporting an output variable.
 * @param day a day.
 * @return TRUE if the variable should be reported on the given day, FALSE
 *   otherwise.
 */
gboolean
RPT_reporting_due (RPT_reporting_t * reporting, unsigned int day)
{
  return (reporting->days) > 0 && (day % reporting->days == 0);
}



/**
 * This function is meant to be used with the foreach function of a GLib Keyed
 * Data List, specifically, the Keyed Data List used to store output variables
 * with sub-variables.  The function receives an output variable.  If the
 * output variable has a simple type (RPT_integer or RPT_real), this function
 * returns that; if the output variable is an RPT_group type, this function
 * recursively calls RPT_reporting_get_type to drill down to the base type.
 */
void
find_type (GQuark key_id, gpointer data, gpointer user_data)
{
  RPT_reporting_t *reporting;
  RPT_type_t *type;

  type = (RPT_type_t *) user_data;
  if (*type != RPT_unknown_type)
    return;

  reporting = (RPT_reporting_t *) data;
  #if DEBUG
    g_debug ("find_type checking sub-variable \"%s\"", reporting->name);
  #endif
  *type = RPT_reporting_get_type (reporting);
}



/**
 * Returns the base type of an output variable.
 *
 * @param reporting an output variable.
 * @return the type.
 */
RPT_type_t
RPT_reporting_get_type (RPT_reporting_t * reporting)
{
  RPT_type_t type;
  GData **group;

#if DEBUG
  g_debug ("----- ENTER RPT_reporting_get_type");
#endif
  type = RPT_unknown_type;

  if (reporting == NULL)
    goto end;

  type = reporting->type;
  if (type != RPT_group)
    goto end;

  type = RPT_unknown_type;
  group = (GData **) (&reporting->data);
  /* A GLib Keyed Data List provides only one way to get at items if you don't
   * know the keys: a foreach function.  So we use a foreach to drill down into
   * the sub-variables to find the base type.  You can see from the "find_type"
   * function above that it stops after finding the base type -- it doesn't
   * actually go through each sub-variable. */
  g_datalist_foreach (group, find_type, &type);

end:
#if DEBUG
  g_debug ("----- EXIT RPT_reporting_get_type");
#endif
  return type;
}



/**
 * This function is meant to be used with the foreach function of a GLib Keyed
 * Data List, specifically, the Keyed Data List used to store output variables
 * with sub-variables.  The function receives an output variable.  It clones
 * that output variable, and inserts the clone into the parent.
 *
 * @param key_id a numeric identifier, not used.
 * @param data an output variable (RPT_reporting_t * cast to a gpointer).
 * @param user_data the parent variable (RPT_reporting_t * cast to a gpointer).
 */
void
deep_copy (GQuark key_id, gpointer data, gpointer user_data)
{
  RPT_reporting_t *reporting, *parent, *copy;

  reporting = (RPT_reporting_t *) data;
  parent = (RPT_reporting_t *) user_data;

#if DEBUG
  g_debug ("  copying item \"%s\"", reporting->name);
#endif

  copy = RPT_clone_reporting (reporting);

#if DEBUG
  g_debug ("  attaching to parent \"%s\"", parent->name);
#endif

  g_datalist_set_data_full ((GData **) (&parent->data),
                            copy->name, copy,
                            RPT_free_reporting_as_GDestroyNotify);

  return;
}



/**
 * Makes a deep copy of an output variable.
 *
 * @param original an output variable.
 * @return a deep copy of the variable.
 */
RPT_reporting_t *
RPT_clone_reporting (RPT_reporting_t * original)
{
  RPT_reporting_t *copy;

#if DEBUG
  g_debug ("----- ENTER RPT_clone_reporting");
#endif

  copy = NULL;

  if (original != NULL)
    {
      copy = RPT_new_reporting (original->name, original->type, original->frequency);
      copy->is_null = original->is_null;
      switch (original->type)
        {
        case RPT_integer:
          RPT_reporting_set_integer (copy, RPT_reporting_get_integer (original, NULL), NULL);
          break;
        case RPT_real:
          RPT_reporting_set_real (copy, RPT_reporting_get_real (original, NULL), NULL);
          break;
        case RPT_group:
          g_datalist_foreach ((GData **) (&original->data), deep_copy, copy);
          break;
        default:
          g_assert_not_reached ();
        }
      copy->is_null = original->is_null;
    }

#if DEBUG
  g_debug ("----- EXIT RPT_clone_reporting");
#endif

  return copy;
}



/**
 * A struct for use with the function RPT_reporting_flatten() below.
 */
typedef struct
{
  GString *name_so_far; /* Should be NULL for the top-level call. */
  GArray *flattened;
}
RPT_reporting_flatten_args_t;


 
/**
 * This is the recursive part of the function RPT_reporting_flatten().  This
 * function is typed as a GDataForeachFunc so that it can easily be called
 * recursively on the sub-variables.
 *
 * @param key_id use 0.
 * @param data an output variable (RPT_reporting_t *), cast to a gpointer.
 * @param user_data a pointer to an RPT_reporting_flatten_args_t struct, cast
 *   to a gpointer.
 */
static void
RPT_reporting_flatten_recursive (GQuark key_id, gpointer data, gpointer user_data)
{
  RPT_reporting_t *reporting;
  RPT_reporting_flatten_args_t *incoming_args;
  RPT_reporting_flatten_args_t outgoing_args;
  GString *name_so_far;
  GArray *flattened;
  GString *name;
  char *camel;

  /* Unpack the incoming function parameters. */
  reporting = (RPT_reporting_t *) data;
  incoming_args = (RPT_reporting_flatten_args_t *) user_data;
  name_so_far = incoming_args->name_so_far;
  flattened = incoming_args->flattened;

  /* Find the variable's name. */
  if (name_so_far == NULL)
    name = g_string_new (reporting->name);
  else
    {
      name = g_string_new (name_so_far->str);
      camel = camelcase (reporting->name, /* capitalize first = */ TRUE); 
      g_string_append_printf (name, "%s", camel);
      g_free (camel);
    }
  #if DEBUG
    g_debug ("name = \"%s\"", name->str);
  #endif

  if (reporting->type == RPT_group)
    {
      outgoing_args.name_so_far = name;
      outgoing_args.flattened = flattened;
      #if DEBUG
        g_debug ("doing recursive call");
      #endif
      g_datalist_foreach ((GData **) (&reporting->data), RPT_reporting_flatten_recursive, &outgoing_args);
      g_string_free (name, TRUE);
    }
  else
    {
      RPT_reporting_flattened_t new_item;
      #if DEBUG
        g_debug ("found leaf output variable");
      #endif
      new_item.name = name->str;
      g_string_free (name, FALSE);
      new_item.reporting = reporting;
      g_array_append_val (flattened, new_item);
    }
  return;
}



/**
 * Produce a "flattened" version of an output variable.
 *
 * Conceptually, this function turns this:
 *   infnU
 *   - Dir
 *     - Cattle=1
 *     - Sheep=2
 *   - Ind
 *     - Cattle=3
 *     - Sheep=4
 *   - Air
 *     - Cattle=5
 *     - Sheep=6
 * into this:
 *   infnUDirCattle=1, infnUDirSheep=2, infnUIndCattle=3, infnUIndSheep=4,
 *   infnUAirCattle=5, infnUAirSheep=6
 *
 * The data structure returned from this function contains pointers into the
 * output variable, so the output variable must not be freed while this data
 * structure is in use.
 *
 * @param reporting an output variable.
 * @return a newly-allocated GArray in which each item is an RPT_reporting_flattened_t
 *   struct.  Each of those structs contains a fully expanded variable name
 *   (e.g. "infnUDirCattle") and a pointer to the sub-variable.  The sub-variable
 *   is guaranteed to be a base type (i.e. not group).  The GArray should be
 *   freed with RPT_free_flattened_reporting().
 */
GArray *
RPT_reporting_flatten (RPT_reporting_t * reporting)
{
  GArray *flattened;
  RPT_reporting_flatten_args_t args;
 
  #if DEBUG
    g_debug ("----- ENTER RPT_reporting_flatten");
  #endif
  flattened = g_array_new (/* zero-terminated = */ FALSE,
                           /* clear = */ FALSE,
                           sizeof (RPT_reporting_flattened_t));

  /* This function is just a tiny function that sets up the return value (a
   * GArray) and then calls a recursive function, RPT_reporting_flatten_recursive(),
   * to do the actual work.
   *
   * The reason for having this tiny function is to present a more understandable
   * function prototype to the outside world. */
  args.name_so_far = NULL;
  args.flattened = flattened;
  RPT_reporting_flatten_recursive (0, (gpointer) reporting, (gpointer) (&args));

  #if DEBUG
  {
    GString *s;
    guint i;
    s = g_string_new (NULL);
    for (i = 0; i < flattened->len; i++)
      {
        g_string_append_printf (s, "%s%s",
                                i == 0 ? "" : ", ",
                                g_array_index (flattened, RPT_reporting_flattened_t, i).name);
      }
    g_debug ("Names found = %s", s->str);
    g_string_free (s, TRUE);
  }
  #endif

  #if DEBUG
    g_debug ("----- EXIT RPT_reporting_flatten");
  #endif
  return flattened;
}



/**
 * Frees the data structure returned by RPT_reporting_flatten.
 */
void
RPT_free_flattened_reporting (GArray *flattened)
{
  guint i;
  RPT_reporting_flattened_t *item;

  if (flattened != NULL)
    {
      for (i = 0; i < flattened->len; i++)
        {
          item = &g_array_index (flattened, RPT_reporting_flattened_t, i);
          g_free (item->name);
          /* Do not free the output variable field (item->reporting), that was
           * not allocated by us. */
        }
      g_array_free (flattened, /* free_segment = */ TRUE);
    }
  return;
}



/**
 * Returns a copy of the given text, transformed into CamelCase.
 *
 * @param text the original text.
 * @param capitalize_first if TRUE, the first character of the text will be
 *   capitalized.
 * @return a newly-allocated string.  If the "text" parameter is NULL, the
 *   return value will also be NULL.
 */
char *
camelcase (char *text, gboolean capitalize_first)
{
  char *newtext; /* Address of the newly-allocated CamelCase string. */
  char *newchar; /* Pointer to the current character of the new string, as we
    are building it. */
  gboolean last_was_space;

  newtext = NULL;
  if (text != NULL)
    {
      newtext = g_new (char, strlen(text)+1); /* +1 to leave room for the '\0' at the end */
      last_was_space = capitalize_first;
      for (newchar = newtext; *text != '\0'; text++)
        {
          if (g_ascii_isspace (*text))
            {
              last_was_space = TRUE;
              continue;
            }
          if (last_was_space && g_ascii_islower(*text))
            *newchar++ = g_ascii_toupper (*text);
          else
            *newchar++ = *text;
          last_was_space = FALSE;
        }
      /* End the new string with a null character. */
      *newchar = '\0';
    }
  return newtext;
}

/* end of file reporting.c */
