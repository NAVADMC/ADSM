/** @file trace_destruction_model.c
 * Module that simulates a policy of destroying units that have been found
 * through trace-out or trace-in.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @version 0.1
 * @date August 2007
 *
 * Copyright &copy; University of Guelph, 2007-2008
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
#define new trace_destruction_model_new
#define run trace_destruction_model_run
#define to_string trace_destruction_model_to_string
#define local_free trace_destruction_model_free
#define handle_trace_result_event trace_destruction_model_handle_trace_result_event

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

#include "trace_destruction_model.h"

#if !HAVE_ROUND && HAVE_RINT
#  define round rint
#endif

/* Temporary fix -- "round" and "rint" are in the math library on Red Hat 7.3,
 * but they're #defined so AC_CHECK_FUNCS doesn't find them. */
double round (double x);

/** This must match an element name in the DTD. */
#define MODEL_NAME "trace-destruction-model"



/** Specialized information for this model. */
typedef struct
{
  int *priority[ADSM_NCONTACT_TYPES][ADSM_NTRACE_DIRECTIONS]; /**< Priority
    for destroying a unit identified by trace.
    Use an expression of the form
    priority[contact_type][direction][production_type]
    to retrieve a value.
    Priority numbers start at 1 for the highest priority. If an element in this
    array is 0, then destruction is not used for that contact type/direction/
    production type combination.  */
  GPtrArray *production_types;
  GHashTable *priority_order_table; /**< A temporary structure that exists
    for use in the set_params functions. */
}
local_data_t;



/**
 * Responds to a trace result by ordering destruction actions.
 *
 * @param self the model.
 * @param units the list of units.
 * @param event a trace result event.
 * @param rng a random number generator.
 * @param queue for any new events the model creates.
 */
void
handle_trace_result_event (struct adsm_module_t_ *self, UNT_unit_list_t * units,
                           EVT_trace_result_event_t * event, RAN_gen_t * rng, EVT_event_queue_t * queue)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  int priority;
  EVT_event_t *destr_event;

#if DEBUG
  g_debug ("----- ENTER handle_trace_result_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* Some trace result events describe a contact that the trace investigation
   * failed to find.  Those are tracked in simulation statistics, but this
   * module is not interested in them. */
  if (event->traced == FALSE)
    goto end;

  if (event->direction == ADSM_TraceForwardOrOut)
    unit = event->exposed_unit;
  else
    unit = event->exposing_unit;
  if (unit->state == Destroyed)
    goto end;

  priority = local_data->priority[event->contact_type][event->direction][unit->production_type];
  if (priority == 0)
    goto end;

  /* Now that we know this is a trace result we are interested in, issue
   * destruction requests. */
  if (event->direction == ADSM_TraceForwardOrOut)
    {
      if (event->contact_type == ADSM_DirectContact)
        destr_event = EVT_new_request_for_destruction_event (unit, event->day, ADSM_ControlTraceForwardDirect, priority);
      else /* indirect */
        destr_event = EVT_new_request_for_destruction_event (unit, event->day, ADSM_ControlTraceForwardIndirect, priority);
    }
  else
    {
      if (event->contact_type == ADSM_DirectContact)
        destr_event = EVT_new_request_for_destruction_event (unit, event->day, ADSM_ControlTraceBackDirect, priority);
      else /* indirect */
        destr_event = EVT_new_request_for_destruction_event (unit, event->day, ADSM_ControlTraceBackIndirect, priority);
    }
#if DEBUG
  g_debug ("requesting destruction of unit \"%s\"", unit->official_id);
#endif
  EVT_event_enqueue (queue, destr_event);

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
    case EVT_TraceResult:
      handle_trace_result_event (self, units, &(event->u.trace_result), rng, queue);
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
  guint i;
  ADSM_contact_type contact_type;
  ADSM_trace_direction direction;

  local_data = (local_data_t *) (self->model_data);
  s = g_string_new (NULL);
  g_string_sprintf (s, "<%s", MODEL_NAME);
  for (i = 0; i < local_data->production_types->len; i++)
    {
      for (direction = 0; direction < ADSM_NTRACE_DIRECTIONS; direction++)
        {
          for (contact_type = 0; contact_type < ADSM_NCONTACT_TYPES; contact_type++)
            {
              int priority;
              priority = local_data->priority[contact_type][direction][i];
              if (priority > 0)
                g_string_append_printf (s, "  for %s units found by %s %s",
                                        (char *) g_ptr_array_index (local_data->production_types, i),
                                        ADSM_trace_direction_name[direction],
                                        ADSM_contact_type_name[contact_type]);
            }
        }
    }
  g_string_append_c (s, '>');

  /* Discard the wrapper object and return the string inside. */
  return g_string_free (s, FALSE);
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
  guint i, j;

#if DEBUG
  g_debug ("----- ENTER free (%s)", MODEL_NAME);
#endif

  /* Free the dynamically-allocated parts. */
  local_data = (local_data_t *) (self->model_data);
  for (i = 0; i < ADSM_NCONTACT_TYPES; i++)
    {
      for (j = 0; j < ADSM_NTRACE_DIRECTIONS; j++)
        {
          g_free (local_data->priority[i][j]);
        }
    }
  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



static int
get_priority (GHashTable *priority_order_table,
              char *production_type_name,
              ADSM_control_reason reason,
              char *boolean_as_text)
{
  int priority = 0;
  long int tmp;

  errno = 0;
  tmp = strtol (boolean_as_text, NULL, /* base */ 10);
  g_assert (errno != ERANGE && errno != EINVAL);
  g_assert (tmp == 0 || tmp == 1);

  if (tmp == 1)
    {
      char *key;
      gpointer ptr;
      key = g_strdup_printf ("%s,%s", production_type_name,
                             ADSM_control_reason_name[reason]);
      ptr = g_hash_table_lookup (priority_order_table, key);
      g_assert (ptr != NULL);
      priority = GPOINTER_TO_UINT(ptr);
      g_free (key);
    }

  return priority;
}
              
              
/**
 * Adds a set of parameters to a trace destruction model.
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
  adsm_module_t *self;
  local_data_t *local_data;
  char *production_type_name;
  guint production_type_id;

  #if DEBUG
    g_debug ("----- ENTER set_params (%s)", MODEL_NAME);
  #endif

  g_assert (ncols == 5);

  self = (adsm_module_t *)data;
  local_data = (local_data_t *) (self->model_data);

  /* Find out which production type these parameters apply to. */
  production_type_name = value[0];
  production_type_id = adsm_read_prodtype (production_type_name, local_data->production_types);

  local_data->priority[ADSM_DirectContact][ADSM_TraceBackOrIn][production_type_id]
    = get_priority (local_data->priority_order_table, production_type_name,
                    ADSM_ControlTraceBackDirect, value[1]);

  local_data->priority[ADSM_DirectContact][ADSM_TraceForwardOrOut][production_type_id]
    = get_priority (local_data->priority_order_table, production_type_name,
                    ADSM_ControlTraceForwardDirect, value[2]);

  local_data->priority[ADSM_IndirectContact][ADSM_TraceBackOrIn][production_type_id]
    = get_priority (local_data->priority_order_table, production_type_name,
                    ADSM_ControlTraceBackIndirect, value[3]);

  local_data->priority[ADSM_IndirectContact][ADSM_TraceForwardOrOut][production_type_id]
    = get_priority (local_data->priority_order_table, production_type_name,
                    ADSM_ControlTraceForwardIndirect, value[4]);

  return 0;
}



/**
 * Returns a new trace destruction model.
 */
adsm_module_t *
new (sqlite3 * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  adsm_module_t *self;
  local_data_t *local_data;
  EVT_event_type_t events_listened_for[] = {
    EVT_TraceResult,
    0
  };
  guint nprod_types, i, j;
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

  /* Initialize an array to hold priorities. */
  local_data->production_types = units->production_type_names;
  nprod_types = local_data->production_types->len;
  for (i = 0; i < ADSM_NCONTACT_TYPES; i++)
    {
      for (j = 0; j < ADSM_NTRACE_DIRECTIONS; j++)
        {
          local_data->priority[i][j] = g_new0 (int, nprod_types);
        }
    }

  /* Get a table that shows the priority order for combinations of production
   * type and reason for destruction. */
  local_data->priority_order_table = adsm_read_priority_order (params);
  sqlite3_exec (params,
                "SELECT prodtype.name,destroy_direct_back_traces,destroy_direct_forward_traces,destroy_indirect_back_traces,destroy_indirect_forward_traces FROM ScenarioCreator_productiontype prodtype,ScenarioCreator_controlprotocol protocol,ScenarioCreator_protocolassignment xref WHERE prodtype.id=xref.production_type_id AND xref.control_protocol_id=protocol.id AND (destroy_direct_back_traces=1 OR destroy_direct_forward_traces=1 OR destroy_indirect_back_traces=1 OR destroy_indirect_forward_traces=1)",
                set_params, self, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }

  g_hash_table_destroy (local_data->priority_order_table);
  local_data->priority_order_table = NULL;

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file trace_destruction_model.c */
