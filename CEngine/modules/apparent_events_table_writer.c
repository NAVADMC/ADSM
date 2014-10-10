/** @file apparent_events_table_writer.c
 * Writes out a table of detections, vaccinations, and destructions in comma-
 * separated value (csv) format.
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
 *
 * @todo check errno after opening the file for writing.
 */

#if HAVE_CONFIG_H
#  include "config.h"
#endif

/* To avoid name clashes when multiple modules have the same interface. */
#define new apparent_events_table_writer_new
#define run apparent_events_table_writer_run
#define to_string apparent_events_table_writer_to_string
#define local_free apparent_events_table_writer_free
#define handle_output_dir_event apparent_events_table_writer_handle_output_dir_event
#define handle_before_each_simulation_event apparent_events_table_writer_handle_before_each_simulation_event
#define handle_detection_event apparent_events_table_writer_handle_detection_event
#define handle_exam_event apparent_events_table_writer_handle_exam_event
#define handle_attempt_to_trace_event apparent_events_table_writer_handle_attempt_to_trace_event
#define handle_trace_result_event apparent_events_table_writer_handle_trace_result_event
#define handle_vaccination_event apparent_events_table_writer_handle_vaccination_event
#define handle_destruction_event apparent_events_table_writer_handle_destruction_event

#include "module.h"
#include "module_util.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#if HAVE_MATH_H
#  include <math.h>
#endif

#if HAVE_STRINGS_H
#  include <strings.h>
#endif

#if HAVE_UNISTD_H
#  include <unistd.h>
#endif

#include "apparent_events_table_writer.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "apparent-events-table-writer"



/* Specialized information for this model. */
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
 * @param self the model.
 * @param event a "Before Each Simulation" event.
 */
void
handle_before_each_simulation_event (struct adsm_module_t_ * self,
                                     EVT_before_each_simulation_event_t * event)
{
  local_data_t *local_data;
  char *tmp_filename;
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
               MODEL_NAME, error->message, local_data->filename);
    }

  g_free (tmp_filename);

  g_io_channel_write_chars (local_data->channel,
                            "Run,Day,Type,Reason,ID,Production type,Size,Lat,Lon,Zone\n",
                            -1 /* assume null-terminated string */,
                            NULL, &error);
  g_io_channel_flush (local_data->channel, &error);

#if DEBUG
  g_debug ("----- EXIT handle_before_each_simulation_event (%s)", MODEL_NAME);
#endif
}



/**
 * Responds to a detection event by writing a table row.
 *
 * @param self the model.
 * @param event a detection event.
 * @param zones the list of zones.
 */
void
handle_detection_event (struct adsm_module_t_ *self,
                        EVT_detection_event_t * event,
                        ZON_zone_list_t *zones)
{
  local_data_t *local_data;
  ZON_zone_fragment_t *zone, *background_zone;
  GError *error = NULL;

#if DEBUG
  g_debug ("----- ENTER handle_detection_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  zone = zones->membership[event->unit->index];
  background_zone = ZON_zone_list_get_background (zones);

  /* The data fields are: run, day, type, reason, ID, production type, size,
   * latitude, longitude, zone. */
  g_string_printf (local_data->buf,
                   "%i,%i,Detection,%s,%s,%s,%u,%g,%g,%s\n",
                   local_data->run_number,
                   event->day,
                   ADSM_detection_reason_abbrev[event->means],
                   event->unit->official_id,
                   event->unit->production_type_name,
                   event->unit->size,
                   event->unit->latitude,
                   event->unit->longitude,
                   ZON_same_zone (zone, background_zone) ? "" : zone->parent->name);
  g_io_channel_write_chars (local_data->channel, local_data->buf->str, 
                            -1 /* assume null-terminated string */,
                            NULL, &error);

#if DEBUG
  g_debug ("----- EXIT handle_detection_event (%s)", MODEL_NAME);
#endif
  return;
}



/**
 * Responds to an exam event by writing a table row.
 *
 * @param self this module.
 * @param event an exam event.
 * @param zones the list of zones.
 */
void
handle_exam_event (struct adsm_module_t_ *self,
                   EVT_exam_event_t * event,
                   ZON_zone_list_t *zones)
{
  local_data_t *local_data;
  ZON_zone_fragment_t *zone, *background_zone;
  GError *error = NULL;

#if DEBUG
  g_debug ("----- ENTER handle_exam_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  zone = zones->membership[event->unit->index];
  background_zone = ZON_zone_list_get_background (zones);

  /* The data fields are: run, day, type, reason, ID, production type, size,
   * latitude, longitude, zone. */
  g_string_printf (local_data->buf,
                   "%i,%i,Exam,%s,%s,%s,%u,%g,%g,%s\n",
                   local_data->run_number,
                   event->day,
                   ADSM_control_reason_abbrev[event->reason],
                   event->unit->official_id,
                   event->unit->production_type_name,
                   event->unit->size,
                   event->unit->latitude,
                   event->unit->longitude,
                   ZON_same_zone (zone, background_zone) ? "" : zone->parent->name);
  g_io_channel_write_chars (local_data->channel, local_data->buf->str, 
                            -1 /* assume null-terminated string */,
                            NULL, &error);

#if DEBUG
  g_debug ("----- EXIT handle_exam_event (%s)", MODEL_NAME);
#endif
  return;
}



/**
 * Responds to an attempt to trace event by writing a table row.
 *
 * @param self this module.
 * @param event an attempt to trace event.
 * @param zones the list of zones.
 */
void
handle_attempt_to_trace_event (struct adsm_module_t_ *self,
                               EVT_attempt_to_trace_event_t * event,
                               ZON_zone_list_t *zones)
{
  local_data_t *local_data;
  ZON_zone_fragment_t *zone, *background_zone;
  GError *error = NULL;

#if DEBUG
  g_debug ("----- ENTER handle_attempt_to_trace_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  zone = zones->membership[event->unit->index];
  background_zone = ZON_zone_list_get_background (zones);

  /* The data fields are: run, day, type, reason, ID, production type, size,
   * latitude, longitude, zone. */
  g_string_printf (local_data->buf,
                   "%i,%i,TraceInitiated,%s%s,%s,%s,%u,%g,%g,%s\n",
                   local_data->run_number,
                   event->day,
                   ADSM_contact_type_abbrev[event->contact_type],
                   ADSM_trace_direction_abbrev[event->direction],
                   event->unit->official_id,
                   event->unit->production_type_name,
                   event->unit->size,
                   event->unit->latitude,
                   event->unit->longitude,
                   ZON_same_zone (zone, background_zone) ? "" : zone->parent->name);
  g_io_channel_write_chars (local_data->channel, local_data->buf->str, 
                            -1 /* assume null-terminated string */,
                            NULL, &error);

#if DEBUG
  g_debug ("----- EXIT handle_attempt_to_trace_event (%s)", MODEL_NAME);
#endif
  return;
}



/**
 * Responds to a trace result event by writing a table row.
 *
 * @param self this module.
 * @param event a trace result event.
 * @param zones the list of zones.
 */
void
handle_trace_result_event (struct adsm_module_t_ *self,
                           EVT_trace_result_event_t * event,
                           ZON_zone_list_t *zones)
{
  local_data_t *local_data;
  ZON_zone_fragment_t *zone, *background_zone;
  UNT_unit_t *identified_unit, *originating_unit;
  char *preposition = NULL;
  GError *error = NULL;

#if DEBUG
  g_debug ("----- ENTER handle_trace_result_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* If this is a trace forward/out, then the "identified unit" is the
   * recipient of the exposure. If this is a trace back/in, then the
   * "identified unit" is the source of the exposure.  */
  if (event->direction == ADSM_TraceForwardOrOut)
    {
      originating_unit = event->exposing_unit;
      identified_unit = event->exposed_unit;
      preposition = "From";
    }
  else if (event->direction == ADSM_TraceBackOrIn)
    {
      originating_unit = event->exposed_unit;
      identified_unit = event->exposing_unit;
      preposition = "To";
    }
  else
    g_assert_not_reached();

  zone = zones->membership[event->exposed_unit->index];
  background_zone = ZON_zone_list_get_background (zones);

  /* The data fields are: run, day, type, reason, ID, production type, size,
   * latitude, longitude, zone. */
  g_string_printf (local_data->buf,
                   "%i,%i,TraceFound,%s%s%s,%s,%s,%u,%g,%g,%s\n",
                   local_data->run_number,
                   event->day,
                   ADSM_contact_type_abbrev[event->contact_type],
                   preposition,
                   originating_unit->official_id,
                   identified_unit->official_id,
                   identified_unit->production_type_name,
                   identified_unit->size,
                   identified_unit->latitude,
                   identified_unit->longitude,
                   ZON_same_zone (zone, background_zone) ? "" : zone->parent->name);
  g_io_channel_write_chars (local_data->channel, local_data->buf->str, 
                            -1 /* assume null-terminated string */,
                            NULL, &error);

#if DEBUG
  g_debug ("----- EXIT handle_trace_result_event (%s)", MODEL_NAME);
#endif
  return;
}



/**
 * Responds to a vaccination event by writing a table row.
 *
 * @param self the model.
 * @param event a vaccination event.
 * @param zones the list of zones.
 */
void
handle_vaccination_event (struct adsm_module_t_ *self,
                          EVT_vaccination_event_t * event,
                          ZON_zone_list_t *zones)
{
  local_data_t *local_data;
  ZON_zone_fragment_t *zone, *background_zone;
  GError *error = NULL;

#if DEBUG
  g_debug ("----- ENTER handle_vaccination_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  zone = zones->membership[event->unit->index];
  background_zone = ZON_zone_list_get_background (zones);

  /* The data fields are: run, day, type, reason, ID, production type, size,
   * latitude, longitude, zone. */
  g_string_printf (local_data->buf,
                   "%i,%i,Vaccination,%s,%s,%s,%u,%g,%g,%s\n",
                   local_data->run_number,
                   event->day,
                   ADSM_control_reason_abbrev[event->reason],
                   event->unit->official_id,
                   event->unit->production_type_name,
                   event->unit->size,
                   event->unit->latitude,
                   event->unit->longitude,
                   ZON_same_zone (zone, background_zone) ? "" : zone->parent->name);
  g_io_channel_write_chars (local_data->channel, local_data->buf->str, 
                            -1 /* assume null-terminated string */,
                            NULL, &error);

#if DEBUG
  g_debug ("----- EXIT handle_vaccination_event (%s)", MODEL_NAME);
#endif
  return;
}



/**
 * Responds to a destruction event by writing a table row.
 *
 * @param self the model.
 * @param event a destruction event.
 * @param zones the list of zones.
 */
void
handle_destruction_event (struct adsm_module_t_ *self,
                          EVT_destruction_event_t * event,
                          ZON_zone_list_t *zones)
{
  local_data_t *local_data;
  ZON_zone_fragment_t *zone, *background_zone;
  GError *error = NULL;

#if DEBUG
  g_debug ("----- ENTER handle_destruction_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  zone = zones->membership[event->unit->index];
  background_zone = ZON_zone_list_get_background (zones);

  /* The data fields are: run, day, type, reason, ID, production type, size,
   * latitude, longitude, zone. */
  g_string_printf (local_data->buf,
                   "%i,%i,Destruction,%s,%s,%s,%u,%g,%g,%s\n",
                   local_data->run_number,
                   event->day,
                   ADSM_control_reason_abbrev[event->reason],
                   event->unit->official_id,
                   event->unit->production_type_name,
                   event->unit->size,
                   event->unit->latitude,
                   event->unit->longitude,
                   ZON_same_zone (zone, background_zone) ? "" : zone->parent->name);
  g_io_channel_write_chars (local_data->channel, local_data->buf->str, 
                            -1 /* assume null-terminated string */,
                            NULL, &error);

#if DEBUG
  g_debug ("----- EXIT handle_destruction_event (%s)", MODEL_NAME);
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
    case EVT_OutputDirectory:
      handle_output_dir_event (self, &(event->u.output_dir));
      break;
    case EVT_BeforeEachSimulation:
      handle_before_each_simulation_event (self, &(event->u.before_each_simulation));
      break;
    case EVT_Detection:
      handle_detection_event (self, &(event->u.detection), zones);
      break;
    case EVT_Exam:
      handle_exam_event (self, &(event->u.exam), zones);
      break;
    case EVT_AttemptToTrace:
      handle_attempt_to_trace_event (self, &(event->u.attempt_to_trace), zones);
      break;
    case EVT_TraceResult:
      handle_trace_result_event (self, &(event->u.trace_result), zones);
      break;
    case EVT_Vaccination:
      handle_vaccination_event (self, &(event->u.vaccination), zones);
      break;
    case EVT_Destruction:
      handle_destruction_event (self, &(event->u.destruction), zones);
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
 * Returns a text representation of this model.
 *
 * @param self the model.
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
 * Returns a new apparent events table writer.
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
    EVT_Detection,
    EVT_Exam,
    EVT_AttemptToTrace,
    EVT_TraceResult,
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

  local_data->filename = g_strdup ("daily_events_.csv");
  local_data->channel = NULL;

  local_data->buf = g_string_new (NULL);

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file apparent_events_table_writer.c */
