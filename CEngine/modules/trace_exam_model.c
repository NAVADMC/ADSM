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
#  include "config.h"
#endif

/* To avoid name clashes when multiple modules have the same interface. */
#define new trace_exam_model_new
#define run trace_exam_model_run
#define to_string trace_exam_model_to_string
#define local_free trace_exam_model_free
#define handle_before_each_simulation_event trace_exam_model_handle_before_each_simulation_event
#define handle_detection_event trace_exam_model_handle_detection_event
#define handle_trace_result_event trace_exam_model_handle_trace_result_event

#include "module.h"
#include "module_util.h"
#include "sqlite3_exec_dict.h"

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

/** This must match an element name in the DTD. */
#define MODEL_NAME "trace-exam-model"



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
  param_block_t **param_block[ADSM_NCONTACT_TYPES][ADSM_NTRACE_DIRECTIONS]; /**< Blocks
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
 * Before each simulation, the module deletes any records of detections or
 * exams left over from a previous iteration.
 *
 * @param self this module.
 */
void
handle_before_each_simulation_event (struct adsm_module_t_ *self)
{
  local_data_t *local_data;

  #if DEBUG
    g_debug ("----- ENTER handle_before_each_simulation_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);
  g_hash_table_remove_all (local_data->detected_or_examined);

  #if DEBUG
    g_debug ("----- EXIT handle_before_each_simulation_event (%s)", MODEL_NAME);
  #endif

  return;
}



/**
 * Records detections so that we can avoid doing exams for already-detected
 * units.
 *
 * @param self this module.
 * @param event a detection event.
 */
void
handle_detection_event (struct adsm_module_t_ *self,
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
handle_trace_result_event (struct adsm_module_t_ *self,
                           EVT_trace_result_event_t * event, EVT_event_queue_t * queue)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  param_block_t *param_block;
  detection_exam_day_t *details;
  ADSM_control_reason reason;

#if DEBUG
  g_debug ("----- ENTER handle_trace_result_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  if (event->traced == FALSE)
    goto end;

  if (event->direction == ADSM_TraceForwardOrOut)
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

  if (event->contact_type == ADSM_DirectContact)
    {
      if (event->direction == ADSM_TraceForwardOrOut)
        reason = ADSM_ControlTraceForwardDirect;
      else
        reason = ADSM_ControlTraceBackDirect;
    }
  else
    {
      if (event->direction == ADSM_TraceForwardOrOut)
        reason = ADSM_ControlTraceForwardIndirect;
      else
        reason = ADSM_ControlTraceBackIndirect;
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
run (struct adsm_module_t_ *self, UNT_unit_list_t * units, ZON_zone_list_t * zones,
     EVT_event_t * event, RAN_gen_t * rng, EVT_event_queue_t * queue)
{
#if DEBUG
  g_debug ("----- ENTER run (%s)", MODEL_NAME);
#endif

  switch (event->type)
    {
    case EVT_BeforeEachSimulation:
      handle_before_each_simulation_event (self);
      break;
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
 * Returns a text representation of this model.
 *
 * @param self the model.
 * @return a string.
 */
char *
to_string (struct adsm_module_t_ *self)
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
      for (j = 0; j < ADSM_NTRACE_DIRECTIONS; j++)
        {
          for (k = 0; k < ADSM_NCONTACT_TYPES; k++)
            {
              param_block_t *param_block;
              param_block = local_data->param_block[k][j][i];
              if (param_block != NULL)
                {
                  g_string_append_printf (s, "\n  %s found by %s of %s",
                                        (char *) g_ptr_array_index (local_data->production_types, i),
                                        ADSM_trace_direction_name[j],
                                        ADSM_contact_type_name[k]);
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
local_free (struct adsm_module_t_ *self)
{
  local_data_t *local_data;
  guint contact_type, direction, nprod_types, i;

#if DEBUG
  g_debug ("----- ENTER free (%s)", MODEL_NAME);
#endif

  /* Free the dynamically-allocated parts. */
  local_data = (local_data_t *) (self->model_data);
  nprod_types = local_data->production_types->len;
  for (contact_type = 0; contact_type < ADSM_NCONTACT_TYPES; contact_type++)
    {
      for (direction = 0; direction < ADSM_NTRACE_DIRECTIONS; direction++)
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
 * @param dict the SQL query result as a GHashTable in which key = colname,
 *   value = value, both in (char *) format.
 * @return 0
 */
static int
set_params (void *data, GHashTable *dict)
{
  adsm_module_t *self;
  local_data_t *local_data;
  guint production_type;

  #if DEBUG
    g_debug ("----- ENTER set_params (%s)", MODEL_NAME);
  #endif

  self = (adsm_module_t *)data;
  local_data = (local_data_t *) (self->model_data);

  g_assert (g_hash_table_size (dict) == 13);

  /* Find out which production type these parameters apply to. */
  production_type =
    adsm_read_prodtype (g_hash_table_lookup (dict, "prodtype"),
                        local_data->production_types);

  /* Read the parameters. */
  local_data->param_block[ADSM_DirectContact][ADSM_TraceForwardOrOut][production_type]
    = make_param_block (g_hash_table_lookup (dict, "examine_direct_forward_traces"),
                        g_hash_table_lookup (dict, "exam_direct_forward_success_multiplier"),
                        g_hash_table_lookup (dict, "test_direct_forward_traces"));

  local_data->param_block[ADSM_DirectContact][ADSM_TraceBackOrIn][production_type]
    = make_param_block (g_hash_table_lookup (dict, "examine_direct_back_traces"),
                        g_hash_table_lookup (dict, "exam_direct_back_success_multiplier"),
                        g_hash_table_lookup (dict, "test_direct_back_traces"));

  local_data->param_block[ADSM_IndirectContact][ADSM_TraceForwardOrOut][production_type]
    = make_param_block (g_hash_table_lookup (dict, "examine_indirect_forward_traces"),
                        g_hash_table_lookup (dict, "exam_indirect_forward_success_multiplier"),
                        g_hash_table_lookup (dict, "test_indirect_forward_traces"));

  local_data->param_block[ADSM_IndirectContact][ADSM_TraceBackOrIn][production_type]
    = make_param_block (g_hash_table_lookup (dict, "examine_indirect_back_traces"),
                        g_hash_table_lookup (dict, "examine_indirect_back_success_multiplier"),
                        g_hash_table_lookup (dict, "test_indirect_back_traces"));
  
  #if DEBUG
    g_debug ("----- EXIT set_params (%s)", MODEL_NAME);
  #endif

  return 0;
}



/**
 * Returns a new trace exam model.
 */
adsm_module_t *
new (sqlite3 * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones, GError **error)
{
  adsm_module_t *self;
  local_data_t *local_data;
  EVT_event_type_t events_listened_for[] = {
    EVT_BeforeEachSimulation,
    EVT_Detection,
    EVT_TraceResult,
    0
  };
  guint contact_type, direction, nprod_types;
  char *sqlerr;

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
  self->to_string = to_string;
  self->printf = adsm_model_printf;
  self->fprintf = adsm_model_fprintf;
  self->free = local_free;

  /* Initialize a table to track already-detected and already-examined units. */
  local_data->detected_or_examined = g_hash_table_new_full (g_direct_hash, g_direct_equal, NULL, g_free);

  /* Initialize the 3D array of parameter blocks. */
  local_data->production_types = units->production_type_names;
  nprod_types = local_data->production_types->len;
  for (contact_type = 0; contact_type < ADSM_NCONTACT_TYPES; contact_type++)
    {
      for (direction = 0; direction < ADSM_NTRACE_DIRECTIONS; direction++)
        {
          local_data->param_block[contact_type][direction] = g_new0 (param_block_t *, nprod_types);
        }    
    }

  /* Call the set_params function to read the production type specific
   * parameters. */
  sqlite3_exec_dict (params,
                     "SELECT prodtype.name AS prodtype,examine_direct_forward_traces,exam_direct_forward_success_multiplier,test_direct_forward_traces,examine_direct_back_traces,exam_direct_back_success_multiplier,test_direct_back_traces,examine_indirect_forward_traces,exam_indirect_forward_success_multiplier,test_indirect_forward_traces,examine_indirect_back_traces,examine_indirect_back_success_multiplier,test_indirect_back_traces "
                     "FROM ScenarioCreator_productiontype prodtype,ScenarioCreator_controlprotocol protocol,ScenarioCreator_protocolassignment xref "
                     "WHERE prodtype.id=xref.production_type_id "
                     "AND xref.control_protocol_id=protocol.id",
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
