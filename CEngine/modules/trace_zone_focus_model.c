/** @file trace_zone_focus_model.c
 * Module that simulates a policy of establishing a zone focus around diseased
 * units.
 *
 * When a unit is detected as diseased, this module requests that a zone focus
 * be established around it.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @version 0.1
 * @date June 2006
 *
 * Copyright &copy; University of Guelph, 2006
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
#define new trace_zone_focus_model_new
#define run trace_zone_focus_model_run
#define to_string trace_zone_focus_model_to_string
#define local_free trace_zone_focus_model_free
#define handle_trace_result_event trace_zone_focus_model_handle_trace_result_event

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

#include "trace_zone_focus_model.h"

#if !HAVE_ROUND && HAVE_RINT
#  define round rint
#endif

/* Temporary fix -- "round" and "rint" are in the math library on Red Hat 7.3,
 * but they're #defined so AC_CHECK_FUNCS doesn't find them. */
double round (double x);

/** This must match an element name in the DTD. */
#define MODEL_NAME "trace-zone-focus-model"



/** Specialized information for this model. */
typedef struct
{
  gboolean *create_zone[ADSM_NCONTACT_TYPES]; /**< Whether or not to
    create a zone around a unit.  Use an expression of the form
    trace_period[contact_type][production_type]
    to retrieve a value. */
  GPtrArray *production_types;
}
local_data_t;



/**
 * Responds to a trace result by ordering a zone focus to be established.
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
  ADSM_control_reason reason;

#if DEBUG
  g_debug ("----- ENTER trace_result_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  if (event->direction == ADSM_TraceForwardOrOut)
    unit = event->exposed_unit;
  else
    unit = event->exposing_unit;

  if (local_data->create_zone[event->contact_type][unit->production_type] == TRUE)
    {
      #if DEBUG
        g_debug ("ordering a zone focus around unit \"%s\"", unit->official_id);
      #endif
      if (event->contact_type == ADSM_DirectContact)
        {
          if (event->direction == ADSM_TraceForwardOrOut)
            reason = ADSM_ControlTraceForwardDirect;
          else if (event->direction == ADSM_TraceBackOrIn)
            reason = ADSM_ControlTraceBackDirect;
          else
            g_assert_not_reached();
        }
      else if (event->contact_type == ADSM_IndirectContact)
        {
          if (event->direction == ADSM_TraceForwardOrOut)
            reason = ADSM_ControlTraceForwardIndirect;
          else if (event->direction == ADSM_TraceBackOrIn)
            reason = ADSM_ControlTraceBackIndirect;
          else
            g_assert_not_reached();
        }
      else
        {
          g_assert_not_reached();
        }
      EVT_event_enqueue (queue, EVT_new_request_for_zone_focus_event (unit, event->day, reason));
    }

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
run (struct adsm_module_t_ *self, UNT_unit_list_t * units,
     ZON_zone_list_t * zones, EVT_event_t * event, RAN_gen_t * rng, EVT_event_queue_t * queue)
{
#if DEBUG
  g_debug ("----- ENTER run (%s)", MODEL_NAME);
#endif

  switch (event->type)
    {
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
  guint i, j;
  char *chararray;
  local_data_t *local_data;

  local_data = (local_data_t *) (self->model_data);
  s = g_string_new (NULL);
  g_string_sprintf (s, "<%s create zones around", MODEL_NAME);
  for (i = 0; i < local_data->production_types->len; i++)
    {
      for (j = 0; j < ADSM_NCONTACT_TYPES; j++)
        {
          if (local_data->create_zone[j][i] == TRUE)
            {
              g_string_append_printf (s, "\n  %s found by trace of %s",
                                      (char *) g_ptr_array_index (local_data->production_types, i),
                                      ADSM_contact_type_name[j]);
             
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
 * Frees this model.  Does not free the production type names.
 *
 * @param self the model.
 */
void
local_free (struct adsm_module_t_ *self)
{
  local_data_t *local_data;
  guint i;

#if DEBUG
  g_debug ("----- ENTER free (%s)", MODEL_NAME);
#endif

  /* Free the dynamically-allocated parts. */
  local_data = (local_data_t *) (self->model_data);
  for (i = 0; i < ADSM_NCONTACT_TYPES; i++)
    {
      g_free (local_data->create_zone[i]);
    }
  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Adds a set of production type specific parameters to a trace zone focus model.
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
  guint production_type;
  long int tmp;

  #if DEBUG
    g_debug ("----- ENTER set_params (%s)", MODEL_NAME);
  #endif

  self = (adsm_module_t *)data;
  local_data = (local_data_t *) (self->model_data);

  g_assert (ncols == 3);

  /* Find out which production type these parameters apply to. */
  production_type = adsm_read_prodtype (value[0], local_data->production_types);

  errno = 0;
  tmp = strtol (value[1], NULL, /* base */ 10);
  g_assert (errno != ERANGE && errno != EINVAL);
  g_assert (tmp == 0 || tmp == 1);
  if (tmp == 1)
    {
      local_data->create_zone[ADSM_DirectContact][production_type] = TRUE;
    }
  errno = 0;
  tmp = strtol (value[2], NULL, /* base */ 10);
  g_assert (errno != ERANGE && errno != EINVAL);
  g_assert (tmp == 0 || tmp == 1);
  if (tmp == 1)
    {
      local_data->create_zone[ADSM_IndirectContact][production_type] = TRUE;
    }

  #if DEBUG
    g_debug ("----- EXIT set_params (%s)", MODEL_NAME);
  #endif

  return 0;
}



/**
 * Returns a new trace zone focus model.
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
  guint nprod_types, i;
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

  /* Initialize the 2D array of booleans. */
  local_data->production_types = units->production_type_names;
  nprod_types = local_data->production_types->len;
  for (i = 0; i < ADSM_NCONTACT_TYPES; i++)
    {
      local_data->create_zone[i] = g_new0 (gboolean, nprod_types);
    }

  /* Call the set_params function to read the production type specific
   * parameters. */
  sqlite3_exec (params,
                "SELECT prodtype.name,direct_trace_is_a_zone_trigger,indirect_trace_is_a_zone_trigger FROM ScenarioCreator_productiontype prodtype,ScenarioCreator_controlprotocol protocol, ScenarioCreator_protocolassignment xref WHERE prodtype.id=xref.production_type_id AND xref.control_protocol_id=protocol.id",
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

/* end of file trace_zone_focus_model.c */
