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
  double detection_multiplier;
  gboolean test_if_no_signs;
}
param_block_t;



typedef struct
{
  GPtrArray *production_types; /**< Each item in the list is a char *. */
  param_block_t **param_block[SPREADMODEL_NCONTACT_TYPES][SPREADMODEL_NTRACE_DIRECTIONS]; /**< Blocks
    of parameters.  Use an expression of the form
    param_block[contact_type][direction][production_type]
    to get a pointer to a particular parameter block. */
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
  param_block_t *param_block;
  detection_exam_day_t *details;
  SPREADMODEL_control_reason reason;

#if DEBUG
  g_debug ("----- ENTER handle_trace_result_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  if (event->traced == FALSE)
    goto end;

  if (event->direction == SPREADMODEL_TraceForwardOrOut)
    unit = event->exposed_unit;
  else
    unit = event->exposing_unit;

  if (unit->state == Destroyed)
    goto end;

  param_block =
    local_data->param_block[event->contact_type][event->direction][unit->production_type];
  if (param_block == NULL)
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
                                                param_block->detection_multiplier,
                                                param_block->test_if_no_signs));
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
  unsigned int i, j, k;
  char *chararray;
  local_data_t *local_data;

  local_data = (local_data_t *) (self->model_data);
  s = g_string_new (NULL);
  g_string_sprintf (s, "<%s do exams for", MODEL_NAME);
  for (i = 0; i < local_data->production_types->len; i++)
    {
      for (j = 0; j < SPREADMODEL_NTRACE_DIRECTIONS; j++)
        {
          for (k = 0; k < SPREADMODEL_NCONTACT_TYPES; k++)
            {
              param_block_t *param_block;
              param_block = local_data->param_block[k][j][i];
              if (param_block != NULL)
                {
                  g_string_append_printf (s, "\n  %s found by %s of %s",
                                        (char *) g_ptr_array_index (local_data->production_types, i),
                                        SPREADMODEL_trace_direction_name[j],
                                        SPREADMODEL_contact_type_name[k]);
                }
            }
        }
    }
  g_string_append_c (s, '>');

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
  guint contact_type, direction, nprod_types, i;

#if DEBUG
  g_debug ("----- ENTER free (%s)", MODEL_NAME);
#endif

  /* Free the dynamically-allocated parts. */
  local_data = (local_data_t *) (self->model_data);
  nprod_types = local_data->production_types->len;
  for (contact_type = 0; contact_type < SPREADMODEL_NCONTACT_TYPES; contact_type++)
    {
      for (direction = 0; direction < SPREADMODEL_NTRACE_DIRECTIONS; direction++)
        {
          for (i = 0; i < nprod_types; i++)
            {
              param_block_t *param_block;
              param_block = local_data->param_block[contact_type][direction][i];
              if (param_block != NULL)
                g_free (param_block);
            }
          g_free (local_data->param_block[contact_type][direction]);
        }
    }

  g_hash_table_destroy (local_data->detected_or_examined);
  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



static param_block_t *
make_param_block (char *examine, char *success_multiplier, char *test)
{
  long int tmp;
  param_block_t *p = NULL;

  tmp = strtol (examine, NULL, /* base */ 10);
  g_assert (errno != ERANGE && errno != EINVAL);
  g_assert (tmp == 0 || tmp == 1);
  if (tmp == 1)
    {
      p = g_new (param_block_t, 1);
      errno = 0;
      p->detection_multiplier = strtod (success_multiplier, NULL);
      g_assert (errno != ERANGE);
      if (p->detection_multiplier < 0)
        {
          g_warning ("%s: detection multiplier cannot be negative, setting to 1 (no effect)",
                     MODEL_NAME);
          p->detection_multiplier = 1;
        }
      else if (p->detection_multiplier < 1)
        {
          g_warning ("%s: detection multiplier is less than 1, will result in lower probability of detection resulting from an exam",
                     MODEL_NAME);
        }

      tmp = strtol (test, NULL, /* base */ 10);
      g_assert (errno != ERANGE && errno != EINVAL);
      g_assert (tmp == 0 || tmp == 1);
      p->test_if_no_signs = (tmp == 1);
    }

  return p;  
}



/**
 * Adds a set of production type specific parameters to a trace exam model.
 *
 * @param data this module ("self"), but cast to a void *.
 * @param ncols number of columns in the SQL query result.
 * @param values values returned by the SQL query, all in text form.
 * @param colname names of columns in the SQL query result.
 * @return 0
 */
static int
set_params (void *data, int ncols, char **value, char **colname)
{
  spreadmodel_model_t *self;
  local_data_t *local_data;
  guint production_type;

  #if DEBUG
    g_debug ("----- ENTER set_params (%s)", MODEL_NAME);
  #endif

  self = (spreadmodel_model_t *)data;
  local_data = (local_data_t *) (self->model_data);

  g_assert (ncols == 13);

  /* Find out which production type these parameters apply to. */
  production_type = spreadmodel_read_prodtype (value[0], local_data->production_types);

  /* Read the parameters. */
  local_data->param_block[SPREADMODEL_DirectContact][SPREADMODEL_TraceForwardOrOut][production_type]
    = make_param_block (value[1], value[2], value[3]);

  local_data->param_block[SPREADMODEL_DirectContact][SPREADMODEL_TraceBackOrIn][production_type]
    = make_param_block (value[4], value[5], value[6]);

  local_data->param_block[SPREADMODEL_IndirectContact][SPREADMODEL_TraceForwardOrOut][production_type]
    = make_param_block (value[7], value[8], value[9]);

  local_data->param_block[SPREADMODEL_IndirectContact][SPREADMODEL_TraceBackOrIn][production_type]
    = make_param_block (value[10], value[11], value[12]);
  
  #if DEBUG
    g_debug ("----- EXIT set_params (%s)", MODEL_NAME);
  #endif

  return 0;
}



/**
 * Returns a new trace exam model.
 */
spreadmodel_model_t *
new (sqlite3 * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  spreadmodel_model_t *self;
  local_data_t *local_data;
  guint contact_type, direction, nprod_types;
  char *sqlerr;

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
  self->is_listening_for = spreadmodel_model_is_listening_for;
  self->has_pending_actions = spreadmodel_model_answer_no;
  self->has_pending_infections = spreadmodel_model_answer_no;
  self->to_string = to_string;
  self->printf = spreadmodel_model_printf;
  self->fprintf = spreadmodel_model_fprintf;
  self->free = local_free;

  /* Initialize a table to track already-detected and already-examined units. */
  local_data->detected_or_examined = g_hash_table_new_full (g_direct_hash, g_direct_equal, NULL, g_free);

  /* Initialize the 3D array of parameter blocks. */
  local_data->production_types = units->production_type_names;
  nprod_types = local_data->production_types->len;
  for (contact_type = 0; contact_type < SPREADMODEL_NCONTACT_TYPES; contact_type++)
    {
      for (direction = 0; direction < SPREADMODEL_NTRACE_DIRECTIONS; direction++)
        {
          local_data->param_block[contact_type][direction] = g_new0 (param_block_t *, nprod_types);
        }    
    }

  /* Call the set_params function to read the production type specific
   * parameters. */
  sqlite3_exec (params,
                "SELECT prodtype.name,examine_direct_forward_traces,exam_direct_forward_success_multiplier,test_direct_forward_traces,examine_direct_back_traces,exam_direct_back_success_multiplier,test_direct_back_traces,examine_indirect_forward_traces,exam_indirect_forward_success_multiplier,test_indirect_forward_traces,examine_indirect_back_traces,exam_indirect_back_success_multiplier,test_indirect_back_traces FROM ScenarioCreator_productiontype prodtype,ScenarioCreator_controlprotocol protocol, ScenarioCreator_protocolassignment xref WHERE prodtype.id=xref.production_type_id AND xref.control_protocol_id=protocol.id",
                set_params, self, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file trace_exam_model.c */
