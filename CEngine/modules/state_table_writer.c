/** @file state_table_writer.c
 * Writes out a table of unit states in comma-separated values (csv) format.
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
 *
 * @todo check errno after opening the file for writing.
 */

#if HAVE_CONFIG_H
#  include "config.h"
#endif

/* To avoid name clashes when multiple modules have the same interface. */
#define new state_table_writer_new
#define run state_table_writer_run
#define to_string state_table_writer_to_string
#define local_free state_table_writer_free
#define handle_output_dir_event state_table_writer_handle_output_dir_event
#define handle_before_each_simulation_event state_table_writer_handle_before_each_simulation_event
#define handle_new_day_event state_table_writer_handle_new_day_event

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

#include "state_table_writer.h"

#if !HAVE_ROUND && HAVE_RINT
#  define round rint
#endif

double round (double x);

/** This must match an element name in the DTD. */
#define MODEL_NAME "state-table-writer"



/* Specialized information for this module. */
typedef struct
{
  char *filename; /* The base filename, with the .csv extension */
  GIOChannel *channel; /* The open file. */
  int run_number;
  GString *buf;
}
local_data_t;



/**
 * Responds to an "output directory" event by prepending the directory to the
 * base output filename.
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
  tmp = local_data->filename;
  local_data->filename = g_build_filename (event->output_dir, tmp, NULL);
  g_free (tmp);
  #if DEBUG
    g_debug ("filename is now %s", local_data->filename);
  #endif

#if DEBUG
  g_debug ("----- EXIT handle_output_dir_event (%s)", MODEL_NAME);
#endif
  return;
}



/**
 * Before each simulation, this module opens its output file and writes the
 * table header.
 *
 * @param self this module.
 * @param units a list of units.
 * @param event a "Before Each Simulation" event.
 */
void
handle_before_each_simulation_event (struct adsm_module_t_ * self,
                                     UNT_unit_list_t * units,
                                     EVT_before_each_simulation_event_t * event)
{
  local_data_t *local_data;
  char *tmp_filename;
  unsigned int nunits, i;
  GError *error = NULL;

#if DEBUG
  g_debug ("----- ENTER handle_before_each_simulation_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  local_data->run_number = event->iteration_number;

  /* If there is a file open from the previous simulation, flush and close that
   * file. */
  if (local_data->channel != NULL)
    {
      g_io_channel_shutdown (local_data->channel, /* flush = */ TRUE, &error);
      local_data->channel = NULL;
    }

  /* Make a new filename that includes the iteration number. */
  tmp_filename = adsm_insert_number_into_filename (local_data->filename, event->iteration_number);

  local_data->channel = g_io_channel_new_file (tmp_filename, "w", &error);
  if (local_data->channel == NULL)
    {
      g_error ("%s: %s error when attempting to open file \"%s\"",
               MODEL_NAME, error->message, tmp_filename);
    }

  g_free (tmp_filename);

  g_string_printf (local_data->buf, "Run,Day");
  nunits = UNT_unit_list_length (units);
  for (i = 0; i < nunits; i++) /* columns = units */
    g_string_append_printf (local_data->buf, ",%u", i);
  g_string_append_c (local_data->buf, '\n');
  g_io_channel_write_chars (local_data->channel, local_data->buf->str, 
                            -1 /* assume null-terminated string */,
                            NULL, &error);
  g_io_channel_flush (local_data->channel, &error);

#if DEBUG
  g_debug ("----- EXIT handle_before_each_simulation_event (%s)", MODEL_NAME);
#endif
}



/**
 * Responds to a new day event by writing a table row.
 *
 * @param self this module.
 * @param units a list of units.
 * @param event a new day event.
 */
void
handle_new_day_event (struct adsm_module_t_ * self,
                      UNT_unit_list_t * units,
                      EVT_new_day_event_t * event)
{
  local_data_t *local_data;
  unsigned int nunits, i;
  UNT_unit_t *unit;
  GError *error = NULL;

#if DEBUG
  g_debug ("----- ENTER handle_new_day_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  nunits = UNT_unit_list_length (units);

  /* The first two fields are run and day. */
  g_string_printf (local_data->buf, "%i,%i", local_data->run_number, event->day);
  for (i = 0; i < nunits; i++)
    {
      unit = UNT_unit_list_get (units, i);
      g_string_append_printf (local_data->buf, ",%c", UNT_state_letter[unit->state]);
    } /* end of loop over units */

  g_string_append_c (local_data->buf, '\n');
  g_io_channel_write_chars (local_data->channel, local_data->buf->str, 
                            -1 /* assume null-terminated string */,
                            NULL, &error);

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
    case EVT_BeforeEachSimulation:
      handle_before_each_simulation_event (self, units, &(event->u.before_each_simulation));
      break;
    case EVT_NewDay:
      handle_new_day_event (self, units, &(event->u.new_day));
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
  g_string_sprintf (s, "<%s filename=\"%s\">", MODEL_NAME, local_data->filename);

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
local_free (struct adsm_module_t_ *self)
{
  local_data_t *local_data;
  GError *error = NULL;

#if DEBUG
  g_debug ("----- ENTER free (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* Flush and close the file. */
  if (local_data->channel != NULL)
    {
      g_io_channel_shutdown (local_data->channel, /* flush = */ TRUE, &error);
    }

  /* Free the dynamically-allocated parts. */
  g_string_free (local_data->buf, TRUE);
  g_free (local_data->filename);
  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Returns a new state table writer.
 */
adsm_module_t *
new (sqlite3 * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones, GError **error)
{
  adsm_module_t *self;
  local_data_t *local_data;
  EVT_event_type_t events_listened_for[] = {
    EVT_OutputDirectory,
    EVT_BeforeEachSimulation,
    EVT_NewDay,
    0
  };

#if DEBUG
  g_debug ("----- ENTER new (%s)", MODEL_NAME);
#endif

  self = g_new (adsm_module_t, 1);
  local_data = g_new (local_data_t, 1);

  self->name = MODEL_NAME;
  self->events_listened_for = adsm_setup_events_listened_for (events_listened_for);
  self->outputs = g_ptr_array_sized_new (0);
  self->model_data = local_data;
  self->run = run;
  self->is_listening_for = adsm_model_is_listening_for;
  self->has_pending_actions = adsm_model_answer_no;
  self->has_pending_infections = adsm_model_answer_no;
  self->to_string = to_string;
  self->printf = adsm_model_printf;
  self->fprintf = adsm_model_fprintf;
  self->free = local_free;

  local_data->filename = g_strdup ("states_.csv");
  local_data->channel = NULL;

  local_data->buf = g_string_new (NULL);

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file state_table_writer.c */
