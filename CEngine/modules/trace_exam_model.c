/** @file trace_exam_model.c
 * Module that simulates a visual inspection of a unit that has been found
 * through trace forward or trace back.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @version 0.1
 * @date March 2008
 *
 * Copyright &copy; University of Guelph, 2008-2009
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
#define new trace_exam_model_new
#define run trace_exam_model_run
#define reset trace_exam_model_reset
#define events_listened_for trace_exam_model_events_listened_for
#define to_string trace_exam_model_to_string
#define local_free trace_exam_model_free
#define handle_detection_event trace_exam_model_handle_detection_event
#define handle_trace_result_event trace_exam_model_handle_trace_result_event

#include "module.h"
#include "module_util.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#if HAVE_STRINGS_H
#  include <strings.h>
#endif

#if HAVE_MATH_H
#  include <math.h>
#endif

#include "trace_exam_model.h"

#include "spreadmodel.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "trace-exam-model"



#define NEVENTS_LISTENED_FOR 2
EVT_event_type_t events_listened_for[] = {
  EVT_Detection, EVT_TraceResult };



/**
 * A structure to track the first day on which a unit was detected and/or
 * examined.
 */
typedef struct
{
  int day_detected;
  int day_examined;
}
detection_exam_day_t;



/** Specialized information for this model. */
typedef struct
{
  SPREADMODEL_contact_type contact_type;
  SPREADMODEL_trace_direction direction;
  gboolean *production_type;
  GPtrArray *production_types;
  double detection_multiplier;
  gboolean test_if_no_signs;
  GHashTable *detected_or_examined; /**< Tracks already-detected and already-
    examined units.  The key is a unit (UNT_unit_t *), the associated data is a
    struct holding the days on which the first detection and/or exam occurred
    (detection_exam_day_t *). */
}
local_data_t;



/**
 * Records detections so that we can avoid doing exams for already-detected
 * units.
 *
 * @param self this module.
 * @param event a detection event.
 */
void
handle_detection_event (struct spreadmodel_model_t_ *self,
                        EVT_detection_event_t * event)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  detection_exam_day_t *details;

#if DEBUG
  g_debug ("----- ENTER handle_detection_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;
  details = g_hash_table_lookup (local_data->detected_or_examined, unit);
  if (details == NULL)
    {
      /* This unit has never been detected or examined before. */    	
      details = g_new (detection_exam_day_t, 1);
      details->day_detected = event->day;
      details->day_examined = 0;
      g_hash_table_insert (local_data->detected_or_examined, unit, details);
    }
  else if (details->day_detected == 0)
    {
   	  /* This unit has been examined before, but not detected. */
   	  details->day_detected = event->day;
    }

#if DEBUG
  g_debug ("----- EXIT handle_detection_event (%s)", MODEL_NAME);
#endif
  return;
}



/**
 * Responds to a trace result by creating an exam event.
 *
 * @param self the model.
 * @param event a trace result event.
 * @param queue for any new events the model creates.
 */
void
handle_trace_result_event (struct spreadmodel_model_t_ *self,
                           EVT_trace_result_event_t * event, EVT_event_queue_t * queue)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  detection_exam_day_t *details;
  SPREADMODEL_control_reason reason;

#if DEBUG
  g_debug ("----- ENTER handle_trace_result_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  if (event->traced == FALSE || event->contact_type != local_data->contact_type
      || event->direction != local_data->direction)
    goto end;

  if (local_data->direction == SPREADMODEL_TraceForwardOrOut)
    unit = event->exposed_unit;
  else
    unit = event->exposing_unit;

  if (unit->state == Destroyed
      || local_data->production_type[unit->production_type] == FALSE)
    goto end;

  /* If the unit has already been examined on a previous day, or today by this
   * module, do not do another exam.  If the unit has already been detected on
   * a previous day, do not do an exam. */
  details = (detection_exam_day_t *) g_hash_table_lookup (local_data->detected_or_examined, unit);
  if (details != NULL
      && (details->day_examined > 0
          || (details->day_detected > 0 && details->day_detected < event->day)
         )
     )
    goto end;

  if (event->contact_type == SPREADMODEL_DirectContact)
    {
      if (event->direction == SPREADMODEL_TraceForwardOrOut)
        reason = SPREADMODEL_ControlTraceForwardDirect;
      else
        reason = SPREADMODEL_ControlTraceBackDirect;
    }
  else
    {
      if (event->direction == SPREADMODEL_TraceForwardOrOut)
        reason = SPREADMODEL_ControlTraceForwardIndirect;
      else
        reason = SPREADMODEL_ControlTraceBackIndirect;
    }

  EVT_event_enqueue (queue, EVT_new_exam_event (unit, event->day, reason,
                                                local_data->detection_multiplier,
                                                local_data->test_if_no_signs));
  if (details == NULL)
    {
      /* This unit has never been detected or examined before. */    	
      details = g_new (detection_exam_day_t, 1);
      details->day_detected = 0;
      details->day_examined = event->day;
      g_hash_table_insert (local_data->detected_or_examined, unit, details);
    }
  else
    {
   	  /* This unit has been detected today, so it already has a record in the
   	   * table.  (We still do an exam, though, because we can't assume that
   	   * the detection came "first"). */
      details->day_examined = event->day;
    }

end:
#if DEBUG
  g_debug ("----- EXIT handle_trace_result_event (%s)", MODEL_NAME);
#endif
  return;
}



/**
 * Runs this model.
 *
 * @param self the model.
 * @param units a unit list.
 * @param zones a zone list.
 * @param event the event that caused the model to run.
 * @param rng a random number generator.
 * @param queue for any new events the model creates.
 */
void
run (struct spreadmodel_model_t_ *self, UNT_unit_list_t * units, ZON_zone_list_t * zones,
     EVT_event_t * event, RAN_gen_t * rng, EVT_event_queue_t * queue)
{
#if DEBUG
  g_debug ("----- ENTER run (%s)", MODEL_NAME);
#endif

  switch (event->type)
    {
    case EVT_Detection:
      handle_detection_event (self, &(event->u.detection));
      break;
    case EVT_TraceResult:
      handle_trace_result_event (self, &(event->u.trace_result), queue);
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
  local_data_t *local_data;

#if DEBUG
  g_debug ("----- ENTER reset (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  g_hash_table_remove_all (local_data->detected_or_examined);

#if DEBUG
  g_debug ("----- EXIT reset (%s)", MODEL_NAME);
#endif
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
  GString *s;
  gboolean already_names;
  unsigned int i;
  char *chararray;
  local_data_t *local_data;

  local_data = (local_data_t *) (self->model_data);
  s = g_string_new (NULL);
  g_string_sprintf (s, "<%s for ", MODEL_NAME);
  already_names = FALSE;
  for (i = 0; i < local_data->production_types->len; i++)
    if (local_data->production_type[i] == TRUE)
      {
        if (already_names)
          g_string_append_printf (s, ",%s",
                                  (char *) g_ptr_array_index (local_data->production_types, i));
        else
          {
            g_string_append_printf (s, "%s",
                                    (char *) g_ptr_array_index (local_data->production_types, i));
            already_names = TRUE;
          }
      }
  g_string_append_printf (s, " units found by %s %s>",
    SPREADMODEL_contact_type_name[local_data->contact_type],
    SPREADMODEL_trace_direction_name[local_data->direction]);

  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Frees this model.  Does not free the contact type name or production type
 * names.
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

  /* Free the dynamically-allocated parts. */
  local_data = (local_data_t *) (self->model_data);
  g_free (local_data->production_type);
  g_hash_table_destroy (local_data->detected_or_examined);
  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Returns a new trace exam model.
 */
spreadmodel_model_t *
new (scew_element * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  spreadmodel_model_t *self;
  local_data_t *local_data;
  scew_attribute *attr;
  XML_Char const *attr_text;
  scew_element const *e;
  gboolean success;

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
  self->run = run;
  self->reset = reset;
  self->is_singleton = FALSE;
  self->is_listening_for = spreadmodel_model_is_listening_for;
  self->has_pending_actions = spreadmodel_model_answer_no;
  self->has_pending_infections = spreadmodel_model_answer_no;
  self->to_string = to_string;
  self->printf = spreadmodel_model_printf;
  self->fprintf = spreadmodel_model_fprintf;
  self->free = local_free;

  /* Make sure the right XML subtree was sent. */
  g_assert (strcmp (scew_element_name (params), MODEL_NAME) == 0);

#if DEBUG
  g_debug ("setting contact type");
#endif
  attr = scew_element_attribute_by_name (params, "contact-type");
  g_assert (attr != NULL);
  attr_text = scew_attribute_value (attr);
  if (strcmp (attr_text, "direct") == 0)
    local_data->contact_type = SPREADMODEL_DirectContact;
  else if (strcmp (attr_text, "indirect") == 0)
    local_data->contact_type = SPREADMODEL_IndirectContact;
  else
    g_assert_not_reached ();

#if DEBUG
  g_debug ("setting trace direction");
#endif
  attr = scew_element_attribute_by_name (params, "direction");
  g_assert (attr != NULL);
  attr_text = scew_attribute_value (attr);
  if (strcmp (attr_text, "out") == 0)
    local_data->direction = SPREADMODEL_TraceForwardOrOut;
  else if (strcmp (attr_text, "in") == 0)
    local_data->direction = SPREADMODEL_TraceBackOrIn;
  else
    g_assert_not_reached ();

  e = scew_element_by_name (params, "detection-multiplier");
  if (e != NULL)
    {
      local_data->detection_multiplier = PAR_get_unitless (e, &success);
      if (success == FALSE)
        {
          g_warning ("%s: setting detection multiplier to 1 (no effect)", MODEL_NAME);
          local_data->detection_multiplier = 1;
        }
      if (local_data->detection_multiplier < 0)
        {
          g_warning ("%s: detection multiplier cannot be negative, setting to 1 (no effect)",
                     MODEL_NAME);
          local_data->detection_multiplier = 1;
        }
      else if (local_data->detection_multiplier < 1)
        {
          g_warning ("%s: detection multiplier is less than 1, will result in lower probability of detection resulting from an exam",
                     MODEL_NAME);
        }
    }
  else
    {
      local_data->detection_multiplier = 1;
    }

  /* Default to FALSE if parameter is not present. */
  local_data->test_if_no_signs = PAR_get_boolean (scew_element_by_name (params, "test-if-no-signs"), &success);

#if DEBUG
  g_debug ("setting production types");
#endif
  local_data->production_types = units->production_type_names;
  local_data->production_type =
    spreadmodel_read_prodtype_attribute (params, "production-type", units->production_type_names);

  /* Initialize a table to track already-detected and already-examined units. */
  local_data->detected_or_examined = g_hash_table_new_full (g_direct_hash, g_direct_equal, NULL, g_free);

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file trace_exam_model.c */
