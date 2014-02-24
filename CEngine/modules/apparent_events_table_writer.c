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
#  include <config.h>
#endif

/* To avoid name clashes when multiple modules have the same interface. */
#define new apparent_events_table_writer_new
#define run apparent_events_table_writer_run
#define reset apparent_events_table_writer_reset
#define events_listened_for apparent_events_table_writer_events_listened_for
#define to_string apparent_events_table_writer_to_string
#define local_free apparent_events_table_writer_free
#define handle_output_dir_event apparent_events_table_writer_handle_output_dir_event
#define handle_before_any_simulations_event apparent_events_table_writer_handle_before_any_simulations_event
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

#include "apparent_events_table_writer.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "apparent-events-table-writer"



#define NEVENTS_LISTENED_FOR 9
EVT_event_type_t events_listened_for[] = {
  EVT_OutputDirectory,
  EVT_BeforeAnySimulations,
  EVT_BeforeEachSimulation,
  EVT_Detection,
  EVT_Exam,
  EVT_AttemptToTrace,
  EVT_TraceResult,
  EVT_Vaccination,
  EVT_Destruction
};



/* Specialized information for this model. */
typedef struct
{
  char *filename; /* with the .csv extension */
  FILE *stream; /* The open file. */
  gboolean stream_is_stdout;
  int run_number;
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
  if (local_data->stream_is_stdout == FALSE)
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
 * Before any simulations, this module sets the run number to zero, opens its
 * output file and writes the table header.
 *
 * @param self the model.
 */
void
handle_before_any_simulations_event (struct spreadmodel_model_t_ * self)
{
  local_data_t *local_data;

#if DEBUG
  g_debug ("----- ENTER handle_before_any_simulations_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  if (!local_data->stream_is_stdout)
    {
      errno = 0;
      local_data->stream = fopen (local_data->filename, "w");
      if (errno != 0)
        {
          g_error ("%s: %s error when attempting to open file \"%s\"",
                   MODEL_NAME, strerror(errno), local_data->filename);
        }
    }
  fprintf (local_data->stream, "Run,Day,Type,Reason,ID,Production type,Size,Lat,Lon,Zone\n");
  fflush (local_data->stream);

  /* This count will be incremented for each new simulation. */
  local_data->run_number = 0;

#if DEBUG
  g_debug ("----- EXIT handle_before_any_simulations_event (%s)", MODEL_NAME);
#endif
}



/**
 * Before each simulation, this module increments its "run number".
 *
 * @param self the model.
 */
void
handle_before_each_simulation_event (struct spreadmodel_model_t_ * self)
{
  local_data_t *local_data;

#if DEBUG
  g_debug ("----- ENTER handle_before_each_simulation_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  local_data->run_number++;

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
handle_detection_event (struct spreadmodel_model_t_ *self,
                        EVT_detection_event_t * event,
                        ZON_zone_list_t *zones)
{
  local_data_t *local_data;
  ZON_zone_fragment_t *zone, *background_zone;

#if DEBUG
  g_debug ("----- ENTER handle_detection_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  zone = zones->membership[event->unit->index];
  background_zone = ZON_zone_list_get_background (zones);

  /* The data fields are: run, day, type, reason, ID, production type, size,
   * latitude, longitude, zone. */
  fprintf (local_data->stream,
           "%i,%i,Detection,%s,%s,%s,%u,%g,%g,%s\n",
           local_data->run_number,
           event->day,
           SPREADMODEL_detection_reason_abbrev[event->means],
           event->unit->official_id,
           event->unit->production_type_name,
           event->unit->size,
           event->unit->latitude,
           event->unit->longitude,
           ZON_same_zone (zone, background_zone) ? "" : zone->parent->name);

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
handle_exam_event (struct spreadmodel_model_t_ *self,
                   EVT_exam_event_t * event,
                   ZON_zone_list_t *zones)
{
  local_data_t *local_data;
  ZON_zone_fragment_t *zone, *background_zone;

#if DEBUG
  g_debug ("----- ENTER handle_exam_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  zone = zones->membership[event->unit->index];
  background_zone = ZON_zone_list_get_background (zones);

  /* The data fields are: run, day, type, reason, ID, production type, size,
   * latitude, longitude, zone. */
  fprintf (local_data->stream,
           "%i,%i,Exam,%s,%s,%s,%u,%g,%g,%s\n",
           local_data->run_number,
           event->day,
           SPREADMODEL_control_reason_abbrev[event->reason],
           event->unit->official_id,
           event->unit->production_type_name,
           event->unit->size,
           event->unit->latitude,
           event->unit->longitude,
           ZON_same_zone (zone, background_zone) ? "" : zone->parent->name);

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
handle_attempt_to_trace_event (struct spreadmodel_model_t_ *self,
                               EVT_attempt_to_trace_event_t * event,
                               ZON_zone_list_t *zones)
{
  local_data_t *local_data;
  ZON_zone_fragment_t *zone, *background_zone;

#if DEBUG
  g_debug ("----- ENTER handle_attempt_to_trace_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  zone = zones->membership[event->unit->index];
  background_zone = ZON_zone_list_get_background (zones);

  /* The data fields are: run, day, type, reason, ID, production type, size,
   * latitude, longitude, zone. */
  fprintf (local_data->stream,
           "%i,%i,TraceInitiated,%s%s,%s,%s,%u,%g,%g,%s\n",
           local_data->run_number,
           event->day,
           SPREADMODEL_contact_type_abbrev[event->contact_type],
           SPREADMODEL_trace_direction_abbrev[event->direction],
           event->unit->official_id,
           event->unit->production_type_name,
           event->unit->size,
           event->unit->latitude,
           event->unit->longitude,
           ZON_same_zone (zone, background_zone) ? "" : zone->parent->name);

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
handle_trace_result_event (struct spreadmodel_model_t_ *self,
                           EVT_trace_result_event_t * event,
                           ZON_zone_list_t *zones)
{
  local_data_t *local_data;
  ZON_zone_fragment_t *zone, *background_zone;
  UNT_unit_t *identified_unit, *originating_unit;
  char *preposition = NULL;

#if DEBUG
  g_debug ("----- ENTER handle_trace_result_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* If this is a trace forward/out, then the "identified unit" is the
   * recipient of the exposure. If this is a trace back/in, then the
   * "identified unit" is the source of the exposure.  */
  if (event->direction == SPREADMODEL_TraceForwardOrOut)
    {
      originating_unit = event->exposing_unit;
      identified_unit = event->exposed_unit;
      preposition = "From";
    }
  else if (event->direction == SPREADMODEL_TraceBackOrIn)
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
  fprintf (local_data->stream,
           "%i,%i,TraceFound,%s%s%s,%s,%s,%u,%g,%g,%s\n",
           local_data->run_number,
           event->day,
           SPREADMODEL_contact_type_abbrev[event->contact_type],
           preposition,
           originating_unit->official_id,
           identified_unit->official_id,
           identified_unit->production_type_name,
           identified_unit->size,
           identified_unit->latitude,
           identified_unit->longitude,
           ZON_same_zone (zone, background_zone) ? "" : zone->parent->name);

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
handle_vaccination_event (struct spreadmodel_model_t_ *self,
                          EVT_vaccination_event_t * event,
                          ZON_zone_list_t *zones)
{
  local_data_t *local_data;
  ZON_zone_fragment_t *zone, *background_zone;

#if DEBUG
  g_debug ("----- ENTER handle_vaccination_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  zone = zones->membership[event->unit->index];
  background_zone = ZON_zone_list_get_background (zones);

  /* The data fields are: run, day, type, reason, ID, production type, size,
   * latitude, longitude, zone. */
  fprintf (local_data->stream,
           "%i,%i,Vaccination,%s,%s,%s,%u,%g,%g,%s\n",
           local_data->run_number,
           event->day,
           event->reason,
           event->unit->official_id,
           event->unit->production_type_name,
           event->unit->size,
           event->unit->latitude,
           event->unit->longitude,
           ZON_same_zone (zone, background_zone) ? "" : zone->parent->name);

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
handle_destruction_event (struct spreadmodel_model_t_ *self,
                          EVT_destruction_event_t * event,
                          ZON_zone_list_t *zones)
{
  local_data_t *local_data;
  ZON_zone_fragment_t *zone, *background_zone;

#if DEBUG
  g_debug ("----- ENTER handle_destruction_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  zone = zones->membership[event->unit->index];
  background_zone = ZON_zone_list_get_background (zones);

  /* The data fields are: run, day, type, reason, ID, production type, size,
   * latitude, longitude, zone. */
  fprintf (local_data->stream,
           "%i,%i,Destruction,%s,%s,%s,%u,%g,%g,%s\n",
           local_data->run_number,
           event->day,
           event->reason,
           event->unit->official_id,
           event->unit->production_type_name,
           event->unit->size,
           event->unit->latitude,
           event->unit->longitude,
           ZON_same_zone (zone, background_zone) ? "" : zone->parent->name);

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
    case EVT_BeforeAnySimulations:
      handle_before_any_simulations_event (self);
      break;
    case EVT_BeforeEachSimulation:
      handle_before_each_simulation_event (self);
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
 * Resets this model after a simulation run.
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
 * Returns a text representation of this model.
 *
 * @param self the model.
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



/**
 * Frees this model.
 *
 * @param self the model.
 */
void
local_free (struct spreadmodel_model_t_ *self)
{
  local_data_t *local_data;

#if DEBUG
  g_debug ("----- ENTER free (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* Flush and close the file. */
  if (local_data->stream_is_stdout)
    fflush (local_data->stream);
  else
    fclose (local_data->stream);

  /* Free the dynamically-allocated parts. */
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
spreadmodel_model_t *
new (scew_element * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  spreadmodel_model_t *self;
  local_data_t *local_data;
  scew_element const *e;

#if DEBUG
  g_debug ("----- ENTER new (%s)", MODEL_NAME);
#endif

  self = g_new (spreadmodel_model_t, 1);
  local_data = g_new (local_data_t, 1);

  self->name = MODEL_NAME;
  self->events_listened_for = events_listened_for;
  self->nevents_listened_for = NEVENTS_LISTENED_FOR;
  self->outputs = g_ptr_array_sized_new (0);
  self->model_data = local_data;
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
      local_data->stream = stdout;
      local_data->stream_is_stdout = TRUE;    
    }
  else
    {
      local_data->filename = PAR_get_text (e);
      if (local_data->filename == NULL
          || g_ascii_strcasecmp (local_data->filename, "") == 0
          || g_ascii_strcasecmp (local_data->filename, "-") == 0
          || g_ascii_strcasecmp (local_data->filename, "stdout") == 0)
        {
          local_data->stream = stdout;
          local_data->stream_is_stdout = TRUE;
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
          local_data->stream_is_stdout = FALSE;
        }
    }

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file apparent_events_table_writer.c */
