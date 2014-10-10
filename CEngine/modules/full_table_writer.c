/** @file full_table_writer.c
 * Writes out a table of values covering many aspects of the simulation, in
 * comma-separated values (csv) format.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 *
 * Copyright &copy; University of Guelph, 2009
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#if HAVE_CONFIG_H
#  include "config.h"
#endif

/* To avoid name clashes when multiple modules have the same interface. */
#define new full_table_writer_new
#define run full_table_writer_run
#define local_free full_table_writer_free
#define handle_before_any_simulations_event full_table_writer_handle_before_any_simulations_event
#define handle_declaration_of_outputs_event full_table_writer_handle_declaration_of_outputs_event
#define handle_before_each_simulation_event full_table_writer_handle_before_each_simulation_event
#define handle_new_day_event full_table_writer_handle_new_day_event
#define handle_end_of_day2_event full_table_writer_handle_end_of_day2_event

#include "module.h"
#include "module_util.h"

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

#include "full_table_writer.h"

#if !HAVE_ROUND && HAVE_RINT
#  define round rint
#endif

/* Temporary fix -- "round" and "rint" are in the math library on Red Hat 7.3,
 * but they're #defined so AC_CHECK_FUNCS doesn't find them. */
double round (double x);

/** This must match an element name in the DTD. */
#define MODEL_NAME "full-table-writer"



/* Specialized information for this model. */
typedef struct
{
  GIOChannel *channel; /* The output channel. */
  int run_number;
  gboolean printed_header;
  GString *buf;
}
local_data_t;



/**
 * Before any simulations, this module:
 * - sets the run number to zero
 * - sets the "printed header" flag to false.
 * - opens its output file and writes the table header
 *
 * @param self the model.
 * @param queue for any new events the model creates.
 */
void
handle_before_any_simulations_event (struct adsm_module_t_ * self,
                                     EVT_event_queue_t * queue)
{
  local_data_t *local_data;

#if DEBUG
  g_debug ("----- ENTER handle_before_any_simulations_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  local_data->printed_header = FALSE;

  #ifdef G_OS_UNIX
    local_data->channel = g_io_channel_unix_new (STDOUT_FILENO);
  #endif
  #ifdef G_OS_WIN32
    local_data->channel = g_io_channel_win32_new_fd (STDOUT_FILENO);
  #endif

#if DEBUG
  g_debug ("----- EXIT handle_before_any_simulations_event (%s)", MODEL_NAME);
#endif
}



/**
 * Responds to an "declaration of outputs" event by adding the output
 * variable(s) to its list of outputs to report.
 *
 * @param self the model.
 * @param event a declaration of outputs event.
 */
void
handle_declaration_of_outputs_event (struct adsm_module_t_ * self,
                                     EVT_declaration_of_outputs_event_t *event)
{
  unsigned int n, i;

#if DEBUG
  g_debug ("----- ENTER handle_declaration_of_outputs_event (%s)", MODEL_NAME);
#endif

  n = event->outputs->len;
  for (i = 0; i < n; i++)
    g_ptr_array_add (self->outputs, g_ptr_array_index (event->outputs, i));
#if DEBUG
  g_debug ("%s now has %u output variables", MODEL_NAME, self->outputs->len);
#endif

#if DEBUG
  g_debug ("----- EXIT handle_declaration_of_outputs_event (%s)", MODEL_NAME);
#endif
}



/**
 * Before each simulation, this module increments its "run number".
 *
 * @event a Before Each Simulation event.
 * @param self the model.
 */
void
handle_before_each_simulation_event (struct adsm_module_t_ * self,
                                     EVT_before_each_simulation_event_t * event)
{
  local_data_t *local_data;

#if DEBUG
  g_debug ("----- ENTER handle_before_each_simulation_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  local_data->run_number = event->iteration_number;

#if DEBUG
  g_debug ("----- EXIT handle_before_each_simulation_event (%s)", MODEL_NAME);
#endif
}



/**
 * On the first "new day" event of a set of simulations, we write the table
 * header.  It would be nicer to do this before any simulations begin, but we
 * need to be sure that the output variables have been initialized with all
 * causes of infection, reasons for destruction, etc. before the table header
 * is written.
 *
 * @param self the model.
 * @param event a new day event.
 */
void
handle_new_day_event (struct adsm_module_t_ * self, EVT_new_day_event_t * event)
{
  local_data_t *local_data;
  unsigned int i;
  RPT_reporting_t *reporting;
  char *camel;
  GError *error = NULL;

#if DEBUG
  g_debug ("----- ENTER handle_new_day_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* Print the table header, if we haven't already. */
  if (!local_data->printed_header)
    {
      /* The first two fields are run and day. */
      g_string_printf (local_data->buf, "Run,Day");

      /* Output the other variables in the order they were created in the
       * new() function. */
      for (i = 0; i < self->outputs->len; i++)
        {
          reporting = (RPT_reporting_t *) g_ptr_array_index (self->outputs, i);
          camel = camelcase (reporting->name, /* capitalize first = */ FALSE); 
          g_string_append_printf (local_data->buf, ",%s", camel);
          g_free (camel);
        }
      g_string_append_c (local_data->buf, '\n');
      g_io_channel_write_chars (local_data->channel, local_data->buf->str, 
                                -1 /* assume null-terminated string */,
                                NULL, &error);
      g_io_channel_flush (local_data->channel, &error);

      local_data->printed_header = TRUE;
    }  

#if DEBUG
  g_debug ("----- EXIT handle_new_day_event (%s)", MODEL_NAME);
#endif
  return;
}



/**
 * Responds to an end of day event by writing a table row.
 *
 * @param self the model.
 * @param event an end of day event.
 */
void
handle_end_of_day2_event (struct adsm_module_t_ * self,
                          EVT_end_of_day2_event_t * event)
{
  local_data_t *local_data;
  unsigned int i;
  RPT_reporting_t *reporting;
  char *value;
  GError *error = NULL;

#if DEBUG
  g_debug ("----- ENTER handle_end_of_day2_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* An end-of-day event is currently used to set up the initially infected,
   * vaccinated, and destroyed units.  That will appear as "day 0", i.e.,
   * before the first day of the simulation.  Don't print a row for day 0. */
  if (event->day > 0)
    {
      /* The first two fields are run and day. */
      g_string_printf (local_data->buf, "%i,%i", local_data->run_number, event->day);

      /* Output the other variables in the order they were created in the
       * new() function. */
      for (i = 0; i < self->outputs->len; i++)
        {
          reporting = (RPT_reporting_t *) g_ptr_array_index (self->outputs, i);
          value = RPT_reporting_value_to_string (reporting, NULL);
          g_string_append_printf (local_data->buf, ",%s", value);
          g_free (value);
        } /* end of loop over output variables */
      g_string_append_c (local_data->buf, '\n');
      g_io_channel_write_chars (local_data->channel, local_data->buf->str, 
                                -1 /* assume null-terminated string */,
                                NULL, &error);
    }

#if DEBUG
  g_debug ("----- EXIT handle_end_of_day2_event (%s)", MODEL_NAME);
#endif
  return;
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
run (struct adsm_module_t_ *self, UNT_unit_list_t * units,
     ZON_zone_list_t * zones, EVT_event_t * event, RAN_gen_t * rng, EVT_event_queue_t * queue)
{
#if DEBUG
  g_debug ("----- ENTER run (%s)", MODEL_NAME);
#endif

  switch (event->type)
    {
    case EVT_BeforeAnySimulations:
      handle_before_any_simulations_event (self, queue);
      break;
    case EVT_DeclarationOfOutputs:
      handle_declaration_of_outputs_event (self, &(event->u.declaration_of_outputs));
      break;
    case EVT_BeforeEachSimulation:
      handle_before_each_simulation_event (self, &(event->u.before_each_simulation));
      break;
    case EVT_NewDay:
      handle_new_day_event (self, &(event->u.new_day));
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
 * Frees this model.
 *
 * @param self the model.
 */
void
local_free (struct adsm_module_t_ *self)
{
  local_data_t *local_data;
  GError *error = NULL;

#if DEBUG
  g_debug ("----- ENTER free (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* Flush any remaining output. */
  g_io_channel_flush (local_data->channel, &error);

  /* Free the dynamically-allocated parts. */
  g_string_free (local_data->buf, TRUE);
  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Returns a new full table writer.
 */
adsm_module_t *
new (sqlite3 * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones, GError **error)
{
  adsm_module_t *self;
  local_data_t *local_data;
  EVT_event_type_t events_listened_for[] = {
    EVT_BeforeAnySimulations,
    EVT_DeclarationOfOutputs,
    EVT_BeforeEachSimulation,
    EVT_NewDay,
    EVT_EndOfDay2,
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
  self->is_listening_for = adsm_model_is_listening_for;
  self->has_pending_actions = adsm_model_answer_no;
  self->has_pending_infections = adsm_model_answer_no;
  self->to_string = adsm_module_to_string_default;
  self->printf = adsm_model_printf;
  self->fprintf = adsm_model_fprintf;
  self->free = local_free;

  /* This module maintains no output variables of its own.  Before any
   * simulations begin, we will gather all the output variables available from
   * other modules. */

  local_data->buf = g_string_new (NULL);

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file full_table_writer.c */
