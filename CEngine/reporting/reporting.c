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
  "unknown_type", "integer", "real", NULL
};



/**
 * Creates a new output variable structure.
 *
 * @param name the variable's name.  Should not contain commas, single quotes
 *   ('), double quotes ("), newlines, or carriage returns.  The text is copied
 *   so the original string can be freed after calling this function.
 * @param type the variable's data type.
 * @return a pointer to a newly-created, initialized RPT_reporting_t structure.
 */
RPT_reporting_t *
RPT_new_reporting (const char *name, RPT_type_t type)
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
    default:
      g_assert_not_reached ();
    }
  reporting->is_null = FALSE;

  return reporting;
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
  char *chararray;

#if DEBUG
  g_debug ("----- ENTER RPT_reporting_value_to_string");
#endif

  s = g_string_new (NULL);
  /* Represent an output variable that is null (has no meaningful value yet)
   * by an empty string, except in the case of a group variable that has sub-
   * categories.  We'll handle that case below. */
  if (reporting->is_null)
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
  g_string_printf (s, "<%s output variable \"%s\">",
                   RPT_type_name[reporting->type], reporting->name);

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
 * Sets the value of an integer output variable.
 *
 * @param reporting an output variable.
 * @param value the new value.
 */
void
RPT_reporting_set_integer (RPT_reporting_t * reporting, long value)
{
  g_assert (reporting->type == RPT_integer);
  *((long *) reporting->data) = value;
  reporting->is_null=FALSE;
  return;
}



/**
 * Adds to the value of an integer output variable.
 *
 * @param reporting an output variable.
 * @param value the amount to add. 
 */
void
RPT_reporting_add_integer (RPT_reporting_t * reporting, long value)
{
  g_assert (reporting->type == RPT_integer);
  *((long *) reporting->data) += value;
  reporting->is_null = FALSE;
  return;
}



/**
 * Retrieves the value of an integer output variable.
 *
 * @param reporting an output variable.
 * @returns the value.
 */
long
RPT_reporting_get_integer (RPT_reporting_t * reporting)
{
  long value;
  g_assert (reporting->type == RPT_integer);
  value = *((long *) reporting->data);
  return value;
}



/**
 * Sets the value of a real output variable.
 *
 * @param reporting an output variable.
 * @param value the new value. 
 */
void
RPT_reporting_set_real (RPT_reporting_t * reporting, double value)
{
  g_assert (reporting->type == RPT_real);
  *((double *) reporting->data) = value;
  reporting->is_null = FALSE;
  return;
}



/**
 * Adds to the value of a real output variable.
 *
 * @param reporting an output variable.
 * @param value the amount to add. 
 */
void
RPT_reporting_add_real (RPT_reporting_t * reporting, double value)
{
  g_assert (reporting->type == RPT_real);
  *((double *) reporting->data) += value;
  reporting->is_null = FALSE;
  return;
}



/**
 * Retrieves the value of a real output variable.
 *
 * @param reporting an output variable.
 * @returns the value.
 */
double
RPT_reporting_get_real (RPT_reporting_t * reporting)
{
  double value;

  g_assert (reporting->type == RPT_real);
  value = *((double *) reporting->data);
  return value;
}



/**
 * Wraps RPT_reporting_set_null so that it can be used with the foreach
 * function of a GLib Pointer Array.
 *
 * @param data an output variable, cast to a gpointer.
 * @param user_data not used, pass NULL.
 */
void
RPT_reporting_set_null_as_GFunc (gpointer data, gpointer user_data)
{
  RPT_reporting_set_null ((RPT_reporting_t *) data);
}



/**
 * Sets the value of an output variable to "null".
 *
 * @param reporting an output variable.
 */
void
RPT_reporting_set_null (RPT_reporting_t * reporting)
{
  reporting->is_null = TRUE;
}



/**
 * Wraps RPT_reporting_zero so that it can be used with the foreach function of
 * a GLib Pointer Array.
 *
 * @param data an output variable, cast to a gpointer.
 * @param user_data not used, pass NULL.
 */
void
RPT_reporting_zero_as_GFunc (gpointer data, gpointer user_data)
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
    default:
      g_assert_not_reached ();
    }

  return;
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

#if DEBUG
  g_debug ("----- ENTER RPT_reporting_get_type");
#endif

  if (reporting == NULL)
    type = RPT_unknown_type;
  else
    type = reporting->type;

#if DEBUG
  g_debug ("----- EXIT RPT_reporting_get_type");
#endif
  return type;
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
      copy = RPT_new_reporting (original->name, original->type);
      copy->is_null = original->is_null;
      switch (original->type)
        {
        case RPT_integer:
          RPT_reporting_set_integer (copy, RPT_reporting_get_integer (original));
          break;
        case RPT_real:
          RPT_reporting_set_real (copy, RPT_reporting_get_real (original));
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



void
RPT_bulk_create (RPT_bulk_create_t *output_specs)
{
  RPT_bulk_create_t *output_spec;
  GPtrArray *camelcased1 = NULL;
  GPtrArray *camelcased2 = NULL;

  for (output_spec = output_specs; output_spec->loc != NULL; output_spec++)
    {
      guint i;

      /* Make CamelCased versions of the subcategory names. */
      if (output_spec->subcategory1_type != RPT_NoSubcategory)
        {
          gchar *original_name;

          camelcased1 = g_ptr_array_new_with_free_func (g_free);
          for (i = 0; i < output_spec->subcategory1_count; i++)
            {
              if (output_spec->subcategory1_type == RPT_CharArray)
                original_name = ((char **)(output_spec->subcategory1_name))[i];
              else
                original_name = g_ptr_array_index ((GPtrArray *)(output_spec->subcategory1_name), i);
              g_ptr_array_add (camelcased1,
                               camelcase (original_name, /* capitalize_first = */ TRUE));
            } /* end of loop to created CamelCased versions of subcategory 1 names */
          if (output_spec->subcategory2_type != RPT_NoSubcategory)
            {
              camelcased2 = g_ptr_array_new_with_free_func (g_free);
              for (i = 0; i < output_spec->subcategory2_count; i++)
                {
                  if (output_spec->subcategory2_type == RPT_CharArray)
                    original_name = ((char **)(output_spec->subcategory2_name))[i];
                  else
                    original_name = g_ptr_array_index ((GPtrArray *)(output_spec->subcategory2_name), i);
                  g_ptr_array_add (camelcased2,
                                   camelcase (original_name, /* capitalize_first = */ TRUE));
                } /* end of loop to created capitalized versions of subcategory 2 names */
            } /* end of if there is a subcategory 2 */
        } /* end of if there is a subcategory 1 */

      if (output_spec->subcategory1_type == RPT_NoSubcategory
          && output_spec->subcategory2_type == RPT_NoSubcategory)
        {
          /* This is a single output variable. */
          RPT_reporting_t *reporting;
          
          reporting = RPT_new_reporting (output_spec->format, output_spec->type);
          if (output_spec->membership1)
            g_ptr_array_add (output_spec->membership1, reporting);
          if (output_spec->membership2)
            g_ptr_array_add (output_spec->membership2, reporting);
          
          *((RPT_reporting_t **)(output_spec->loc)) = reporting;
        } /* end of creating a single output variable */

      else if (output_spec->subcategory1_type != RPT_NoSubcategory
               && output_spec->subcategory2_type == RPT_NoSubcategory)
        {
          /* Create an array of output variables. */
          RPT_reporting_t **reporting;
          guint n;
          gchar *output_name;

          n = output_spec->subcategory1_count;
          reporting = g_new0 (RPT_reporting_t *, n);
          for (i = 0; i < output_spec->subcategory1_count; i++)
            {
              output_name = g_strdup_printf (output_spec->format,
                                             g_ptr_array_index (camelcased1, i));
              reporting[i] = RPT_new_reporting (output_name, output_spec->type);
              g_free (output_name);
              if (output_spec->membership1)
                g_ptr_array_add (output_spec->membership1, reporting[i]);
              if (output_spec->membership2)
                g_ptr_array_add (output_spec->membership2, reporting[i]);
            } /* end of loop over array */

          *((RPT_reporting_t ***)(output_spec->loc)) = reporting;
        } /* end of creating an array of output variables */

      else if (output_spec->subcategory1_type != RPT_NoSubcategory
               && output_spec->subcategory2_type != RPT_NoSubcategory)
        {
          /* This is a 2D array of output variables. */
          RPT_reporting_t ***reporting = NULL;
          guint nrows, ncols, row, col;
          gchar *output_name;

          nrows = output_spec->subcategory1_count;
          ncols = output_spec->subcategory2_count;
          reporting = g_new0 (RPT_reporting_t **, nrows);
          for (row = 0; row < output_spec->subcategory1_count; row++)
            {
              reporting[row] = g_new0 (RPT_reporting_t *, ncols);
              for (col = 0; col < output_spec->subcategory2_count; col++)
                {
                  output_name = g_strdup_printf (output_spec->format,
                                                 g_ptr_array_index (camelcased1, row),
                                                 g_ptr_array_index (camelcased2, col)); 
                  reporting[row][col] = RPT_new_reporting (output_name, output_spec->type);
                  g_free (output_name);
                  if (output_spec->membership1)
                    g_ptr_array_add (output_spec->membership1, reporting[row][col]);
                  if (output_spec->membership2)
                    g_ptr_array_add (output_spec->membership2, reporting[row][col]);
                } /* end of loop over cols */              
            } /* end of loop over rows */

          *((RPT_reporting_t ****)(output_spec->loc)) = reporting;
        } /* end of creating a 2D array of output variables */

      else
        {
          g_assert_not_reached();
        }

      if (camelcased1 != NULL)
        {
          g_ptr_array_free (camelcased1, /* free_seg = */ TRUE);
          camelcased1 = NULL;
          if (camelcased2 != NULL)
            {
              g_ptr_array_free (camelcased2, /* free_seg = */ TRUE);
              camelcased2 = NULL;
            }
        }

    } /* end of loop over reporting variables to bulk create */

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
