/** @file table_writer.c
 * Writes out a table giving the count, mean, standard deviation, median, and
 * quartiles for each variable, in comma-separated values (csv) format.
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
#define new table_writer_new
#define set_params table_writer_set_params
#define run table_writer_run
#define reset table_writer_reset
#define events_listened_for table_writer_events_listened_for
#define to_string table_writer_to_string
#define local_free table_writer_free
#define handle_output_dir_event table_writer_handle_output_dir_event
#define handle_declaration_of_outputs_event table_writer_handle_declaration_of_outputs_event
#define handle_end_of_day2_event table_writer_handle_end_of_day2_event

#include "module.h"
#include "module_util.h"
#include <gsl/gsl_statistics_double.h>
#include <gsl/gsl_sort.h>

#include <unistd.h>

#if STDC_HEADERS
#  include <string.h>
#endif

#if HAVE_MATH_H
#  include <math.h>
#endif

#if HAVE_STRINGS_H
#  include <strings.h>
#endif

#include "table_writer.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "table-writer"



#define NEVENTS_LISTENED_FOR 3
EVT_event_type_t events_listened_for[] = {
  EVT_OutputDirectory,
  EVT_DeclarationOfOutputs,
  EVT_EndOfDay2
};



/**
 * An output variable, its fully-expanded name, and a list of its values.
 */
typedef struct
{
  RPT_reporting_t *output;
  char *name;
  GArray *values;
}
output_values_t;



/**
 * Creates an output_values_t object.
 *
 * @param output an output variable. The pointer will be copied.
 * @param name the output variable's name. The string will be duplicated so
 *   the original can be freed after the call to this function.
 * @return an output_values_t object. Free it with free_output_values().
 */
static output_values_t *
new_output_values (RPT_reporting_t *output, char *name)
{
  output_values_t *output_values;

  output_values = g_new (output_values_t, 1);  
  output_values->output = output;
  output_values->name = g_strdup (name);
  switch (RPT_reporting_get_type (output))
  {
    case RPT_integer:
    case RPT_real:
      output_values->values = g_array_new (/* zero_terminated = */ FALSE,
                                           /* clear = */ FALSE,
                                           sizeof (double));
      break;
    default:
      g_assert_not_reached();      
  }
  
  return output_values;
}


 
/**
 * Frees an output_values_t object. Typed as a GDestroyNotify function so that
 * it can be used as the element_free_func in a GPtrArray.
 *
 * Does not free the output variable itself (the RPT_reporting_t object); that
 * is assumed to not belong to us.
 */
static void
free_output_values (gpointer data)
{
  output_values_t *output_values;

  output_values = (output_values_t *) data;
  if (output_values != NULL)
    {
      g_free (output_values->name);
      g_array_free (output_values->values, /* free_segment = */ TRUE);
      g_free (output_values);
    }
  return;
}



/* Specialized information for this model. */
typedef struct
{
  char *filename; /**< with the .csv extension */
  GIOChannel *channel; /**< The open file. */
  gboolean channel_is_stdout;
  GPtrArray *output_values; /**< A structure to accumulate output variable
    values so that we can do the median, quartiles, etc. after the simulation
    has finished. Each item is a pointer to an output_values_t object. */
}
local_data_t;



/**
 * Responds to an "output directory" event by prepending the directory to the
 * its output filename.
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
  if (local_data->channel_is_stdout == FALSE)
    {
      tmp = local_data->filename;
      local_data->filename = g_build_filename (event->output_dir, tmp, NULL);
      g_free (tmp);
      #if DEBUG
        g_debug ("filename is now %s", local_data->filename);
      #endif
    }

  #if DEBUG
    g_debug ("----- EXIT handle_output_dir_event (%s)", MODEL_NAME);
  #endif
  return;
}



/**
 * Responds to an "declaration of outputs" event by adding the output
 * variable(s) to its list of outputs to report.
 *
 * @param self this module.
 * @param event a declaration of outputs event.
 */
void
handle_declaration_of_outputs_event (struct spreadmodel_model_t_ * self,
                                     EVT_declaration_of_outputs_event_t *event)
{
  local_data_t *local_data;
  unsigned int i, j;
  RPT_reporting_t *output;
  GArray *subvars;
  RPT_reporting_flattened_t *subvar;

  #if DEBUG
    g_debug ("----- ENTER handle_declaration_of_outputs_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);
  for (i = 0; i < event->outputs->len; i++)
    {
      output = (RPT_reporting_t *) g_ptr_array_index (event->outputs, i);

      /* Skip the outputs that are never reported. */
      if (output->frequency == RPT_never)
        continue;

      /* Get the output in "flattened" form. */
      subvars = RPT_reporting_flatten (output);
            
      for (j = 0; j < subvars->len; j++)
        {
          subvar = &g_array_index (subvars, RPT_reporting_flattened_t, j);
          /* Add this sub-variable to this module's tracking list. */
          g_ptr_array_add (local_data->output_values,
                           new_output_values (subvar->reporting, subvar->name));
        } /* end of loop over sub-variables within one output variable */
      RPT_free_flattened_reporting (subvars);

    } /* end of loop over output variables in declaration event */

  #if DEBUG
    g_debug ("%s now tracking %u output variables", MODEL_NAME, local_data->output_values->len);
  #endif

  #if DEBUG
    g_debug ("----- EXIT handle_declaration_of_outputs_event (%s)", MODEL_NAME);
  #endif
  return;
}



/**
 * Responds to an end of day event on the last day of the simulation by
 * copying the output variable values.
 *
 * @param self this module.
 * @param event an end of day 2 event.
 */
void
handle_end_of_day2_event (struct spreadmodel_model_t_ * self,
                          EVT_end_of_day2_event_t * event)
{
  local_data_t *local_data;
  guint i;
  output_values_t *output_value;
  RPT_reporting_t *output;
  double value;

#if DEBUG
  g_debug ("----- ENTER handle_end_of_day2_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* An end-of-day event is currently used to set up the initially infected,
   * vaccinated, and destroyed units.  That will appear as "day 0", i.e.,
   * before the first day of the simulation.  Ignore day 0. */
  if (event->done && event->day >0)
    {
      for (i = 0; i < local_data->output_values->len; i++)
        {
          output_value = g_ptr_array_index (local_data->output_values, i);
          output = output_value->output;
          if (RPT_reporting_is_null (output, NULL))
            continue;
          if (RPT_reporting_get_type (output) == RPT_integer)
            value = (double) RPT_reporting_get_integer (output, NULL);
          else if (RPT_reporting_get_type (output) == RPT_real)
            value = RPT_reporting_get_real (output, NULL);
          g_array_append_val (output_value->values, value);
        } /* end of loop over tracked output variables */
    } /* end of if last day */

#if DEBUG
  g_debug ("----- EXIT handle_end_of_day2_event (%s)", MODEL_NAME);
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
    case EVT_DeclarationOfOutputs:
      handle_declaration_of_outputs_event (self, &(event->u.declaration_of_outputs));
      break;
    case EVT_EndOfDay2:
      handle_end_of_day2_event (self, &(event->u.end_of_day2));
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
 * Resets this module after a simulation run.
 *
 * @param self the model.
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
  g_string_sprintf (s, "<%s filename=\"%s\">", MODEL_NAME, local_data->filename);

  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



static void
print_table (local_data_t *local_data)
{
  GError *error = NULL;
  GString *buf;
  guint i;
  output_values_t *output_value;
  guint nvalues;
  double *data_segment;
  double mean, stddev, lo, hi, p05, p10, p25, median, p75, p90, p95;

  #if DEBUG
    g_debug ("----- ENTER print_table (%s)", MODEL_NAME);
  #endif

  if (local_data->channel_is_stdout)
    {
      #ifdef G_OS_UNIX
        local_data->channel = g_io_channel_unix_new (STDOUT_FILENO);
      #endif
      #ifdef G_OS_WIN32
        local_data->channel = g_io_channel_win32_new_fd (STDOUT_FILENO);
      #endif
    }
  else
    {
      local_data->channel = g_io_channel_new_file (local_data->filename, "w", &error);
      if (local_data->channel == NULL)
        {
          g_error ("%s: %s error when attempting to open file \"%s\"",
                   MODEL_NAME, error->message, local_data->filename);
        }
    }

  g_io_channel_write_chars (local_data->channel,
                            "Output,Number of occurrences,Mean,StdDev,Low,High,p5,p10,p25,p50 (Median),p75,p90,p95\n",
                            -1 /* assume null-terminated string */, NULL, &error);
  g_io_channel_flush (local_data->channel, &error);
  buf = g_string_new (NULL);
  for (i = 0; i < local_data->output_values->len; i++)
    {
      output_value = g_ptr_array_index (local_data->output_values, i);
      nvalues = output_value->values->len;
      data_segment = (double *)(output_value->values->data);
      if (nvalues == 0)
        {
          mean = stddev = 0;
          lo = p05 = p10 = p25 = median = p75 = p90 = p95 = hi = 0;
        }
      else
        {
          mean = gsl_stats_mean (data_segment, 1, nvalues);
          /* The formula for standard deviation contains a 1/(N-1), so if there
           * is only 1 value, we just list standard deviation as 0. */
          if (nvalues == 1)
            stddev = 0;
          else
            stddev = gsl_stats_sd_m (data_segment, 1, nvalues, mean);

          /* Sort the values in preparation for doing median and quantiles. */
          gsl_sort (data_segment, 1, nvalues);

          /* Now that it's sorted, low and high are easy. */
          lo = g_array_index (output_value->values, double, 0);
          hi = g_array_index (output_value->values, double, nvalues - 1);

          median = gsl_stats_median_from_sorted_data (data_segment, 1, nvalues);
          p05 = gsl_stats_quantile_from_sorted_data (data_segment, 1, nvalues, 0.05);
          p10 = gsl_stats_quantile_from_sorted_data (data_segment, 1, nvalues, 0.10);
          p25 = gsl_stats_quantile_from_sorted_data (data_segment, 1, nvalues, 0.25);
          p75 = gsl_stats_quantile_from_sorted_data (data_segment, 1, nvalues, 0.75);
          p90 = gsl_stats_quantile_from_sorted_data (data_segment, 1, nvalues, 0.90);
          p95 = gsl_stats_quantile_from_sorted_data (data_segment, 1, nvalues, 0.95);
        }

      g_string_printf (buf, "%s,%d,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g\n",
                       output_value->name, nvalues,
                       mean, stddev, lo, hi,
                       p05, p10, p25, median, p75, p90, p95);
      g_io_channel_write_chars (local_data->channel, buf->str, 
                                -1 /* assume null-terminated string */,
                                NULL, &error);
    }
  g_io_channel_flush (local_data->channel, &error);
  g_string_free (buf, TRUE);
  
  return;
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
  GError *error = NULL;

  #if DEBUG
    g_debug ("----- ENTER free (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);

  /* Print the table. */
  print_table (local_data);

  /* Flush and close the file. */
  if (local_data->channel_is_stdout)
    g_io_channel_flush (local_data->channel, &error);
  else
    g_io_channel_shutdown (local_data->channel, /* flush = */ TRUE, &error);

  /* Free the dynamically-allocated parts. */
  g_free (local_data->filename);
  g_ptr_array_free (local_data->output_values, /* free_seg = */ TRUE); /* We
    set an element_free_func on this array, so this call will also properly
    free the array contents. */
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
set_params (struct spreadmodel_model_t_ *self, PAR_parameter_t * params)
{
  local_data_t *local_data;
  scew_element *e;

  #if DEBUG
    g_debug ("----- ENTER set_params (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);

  /* Make sure the right XML subtree was sent. */
  g_assert (strcmp (scew_element_name (params), MODEL_NAME) == 0);

  /* Get the filename for the table.  If the filename is omitted, blank, '-',
   * or 'stdout' (case insensitive), then the table is written to standard
   * output. */
  e = scew_element_by_name (params, "filename");
  if (e == NULL)
    {
      local_data->filename = g_strdup ("stdout"); /* just so we have something
        to display, and to free later */
      local_data->channel_is_stdout = TRUE;    
    }
  else
    {
      local_data->filename = PAR_get_text (e);
      if (local_data->filename == NULL
          || g_ascii_strcasecmp (local_data->filename, "") == 0
          || g_ascii_strcasecmp (local_data->filename, "-") == 0
          || g_ascii_strcasecmp (local_data->filename, "stdout") == 0)
        {
          local_data->channel_is_stdout = TRUE;
        }
      else
        {
          char *tmp;
          if (!g_str_has_suffix(local_data->filename, ".csv"))
            {
              tmp = local_data->filename;
              local_data->filename = g_strdup_printf("%s.csv", tmp);
              g_free(tmp);
            }
          tmp = local_data->filename;
          local_data->filename = spreadmodel_insert_node_number_into_filename (local_data->filename);
          g_free(tmp);
          local_data->channel_is_stdout = FALSE;
        }
    }

  #if DEBUG
    g_debug ("----- EXIT set_params (%s)", MODEL_NAME);
  #endif

  return;
}



/**
 * Returns a new table writer.
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
  self->outputs = g_ptr_array_new ();
  self->model_data = local_data;
  self->set_params = table_writer_set_params;
  self->run = run;
  self->reset = reset;
  self->is_singleton = spreadmodel_model_answer_yes;
  self->is_listening_for = spreadmodel_model_is_listening_for;
  self->has_pending_actions = spreadmodel_model_answer_no;
  self->has_pending_infections = spreadmodel_model_answer_no;
  self->to_string = to_string;
  self->printf = spreadmodel_model_printf;
  self->fprintf = spreadmodel_model_fprintf;
  self->free = local_free;

  /* Send the XML subtree to the set_params function to read the parameters. */
  self->set_params (self, params);

  /* This module maintains no output variables of its own.  Before any
   * simulations begin, we will gather all the output variables available from
   * other modules. */
  local_data->output_values = g_ptr_array_new_with_free_func (free_output_values);

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file table_writer.c */
