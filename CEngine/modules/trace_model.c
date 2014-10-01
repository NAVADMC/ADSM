/** @file trace_model.c
 * Module that simulates a policy of requesting traces when a unit is detected
 * as diseased.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @version 0.1
 * @date August 2007
 *
 * Copyright &copy; University of Guelph, 2007
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
#define new trace_model_new
#define run trace_model_run
#define to_string trace_model_to_string
#define local_free trace_model_free
#define handle_detection_event trace_model_handle_detection_event

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

#include "trace_model.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "trace-model"



/** Specialized information for this model. */
typedef struct
{
  int *trace_period[ADSM_NCONTACT_TYPES][ADSM_NTRACE_DIRECTIONS]; /**< Number
    of days back we are interested in tracing.  Use an expression of the form
    trace_period[contact_type][direction][production_type]
    to get a particular value.  A negative number means "don't trace". */
  GPtrArray *production_types;
}
local_data_t;



/**
 * Responds to a detection by requesting traces.
 *
 * @param self the model.
 * @param units the list of units.
 * @param event a detection event.
 * @param rng a random number generator.
 * @param queue for any new events the model creates.
 */
void
handle_detection_event (struct adsm_module_t_ *self, UNT_unit_list_t * units,
                        EVT_detection_event_t * event, RAN_gen_t * rng, EVT_event_queue_t * queue)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  ADSM_contact_type contact_type;
  ADSM_trace_direction direction;
  int trace_period;

#if DEBUG
  g_debug ("----- ENTER handle_detection_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;
  for (contact_type = 0; contact_type < ADSM_NCONTACT_TYPES; contact_type++)
    {
      for (direction = 0; direction < ADSM_NTRACE_DIRECTIONS; direction++)
        {
          trace_period =
            local_data->trace_period[contact_type][direction][unit->production_type];
          if (trace_period >= 0)
            {
              #if DEBUG
                g_debug ("unit \"%s\" request to %s %ss", 
                         unit->official_id,
                         ADSM_trace_direction_name[direction],
                         ADSM_contact_type_name[contact_type]);
              #endif
              EVT_event_enqueue (queue,
                EVT_new_attempt_to_trace_event (unit, event->day,
                                                contact_type, direction, trace_period));
            }
        }
    }

#if DEBUG
  g_debug ("----- EXIT handle_detection_event (%s)", MODEL_NAME);
#endif
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
    case EVT_Detection:
      handle_detection_event (self, units, &(event->u.detection), rng, queue);
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
  unsigned int i;
  char *chararray;
  local_data_t *local_data;

  local_data = (local_data_t *) (self->model_data);
  s = g_string_new (NULL);
  g_string_append_printf (s, "<%s on detection of", MODEL_NAME);
  for (i = 0; i < local_data->production_types->len; i++)
    {
      ADSM_contact_type contact_type;
      ADSM_trace_direction direction;
      int trace_period;

      g_string_append_printf (s, "\n  %s:",
                              (char *) g_ptr_array_index (local_data->production_types, i));
      for (contact_type = 0; contact_type < ADSM_NCONTACT_TYPES; contact_type++)
        {
          for (direction = 0; direction < ADSM_NTRACE_DIRECTIONS; direction++)
            {
              trace_period =
                local_data->trace_period[contact_type][direction][i];
              if (trace_period >= 0)
                {
                  g_string_append_printf (s, " %s %s %i days",
                                          ADSM_trace_direction_name[direction],
                                          ADSM_contact_type_name[contact_type],
                                          trace_period);
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
          g_free (local_data->trace_period[i][j]);
        }    
    }
  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Adds a set of production type specific parameters to a trace model.
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
  char *tmp_text;
  long int trace_period;
  long int tmp;

  #if DEBUG
    g_debug ("----- ENTER set_params (%s)", MODEL_NAME);
  #endif

  self = (adsm_module_t *)data;
  local_data = (local_data_t *) (self->model_data);

  g_assert (g_hash_table_size (dict) == 7);

  /* Find out which production type these parameters apply to. */
  production_type =
    adsm_read_prodtype (g_hash_table_lookup (dict, "prodtype"),
                        local_data->production_types);

  /* Read the parameters. */
  tmp_text = g_hash_table_lookup (dict, "direct_trace_period");
  if (tmp_text != NULL)
    {
      errno = 0;
      trace_period = strtol (tmp_text, NULL, /* base */ 10);
      g_assert (errno != ERANGE && errno != EINVAL);
      if (trace_period >= 0)
        {
          tmp_text = g_hash_table_lookup (dict, "trace_direct_forward");
          if (tmp_text != NULL)
            {
              errno = 0;
              tmp = strtol (tmp_text, NULL, /* base */ 10);
              g_assert (errno != ERANGE && errno != EINVAL);
              g_assert (tmp == 0 || tmp == 1);
              if (tmp == 1)
                {
                  local_data->trace_period[ADSM_DirectContact][ADSM_TraceForwardOrOut][production_type] = trace_period;
                }
            }
          tmp_text = g_hash_table_lookup (dict, "trace_direct_back");
          if (tmp_text != NULL)
            {
              errno = 0;
              tmp = strtol (tmp_text, NULL, /* base */ 10);
              g_assert (errno != ERANGE && errno != EINVAL);
              g_assert (tmp == 0 || tmp == 1);
              if (tmp == 1)
                {
                  local_data->trace_period[ADSM_DirectContact][ADSM_TraceBackOrIn][production_type] = trace_period;
                }
            }
        }
    }

  tmp_text = g_hash_table_lookup (dict, "indirect_trace_period");
  if (tmp_text != NULL)
    {
      errno = 0;
      trace_period = strtol (tmp_text, NULL, /* base */ 10);
      g_assert (errno != ERANGE && errno != EINVAL);
      if (trace_period >= 0)
        {
          tmp_text = g_hash_table_lookup (dict, "trace_indirect_forward");
          if (tmp_text != NULL)
            {
              errno = 0;
              tmp = strtol (tmp_text, NULL, /* base */ 10);
              g_assert (errno != ERANGE && errno != EINVAL);
              g_assert (tmp == 0 || tmp == 1);
              if (tmp == 1)
                {
                  local_data->trace_period[ADSM_IndirectContact][ADSM_TraceForwardOrOut][production_type] = trace_period;
                }
            }
          tmp_text = g_hash_table_lookup (dict, "trace_indirect_back");
          if (tmp_text != NULL)
            {
              errno = 0;
              tmp = strtol (tmp_text, NULL, /* base */ 10);
              g_assert (errno != ERANGE && errno != EINVAL);
              g_assert (tmp == 0 || tmp == 1);
              if (tmp == 1)
                {
                  local_data->trace_period[ADSM_IndirectContact][ADSM_TraceBackOrIn][production_type] = trace_period;
                }
            }
        }
    }

  #if DEBUG
    g_debug ("----- EXIT set_params (%s)", MODEL_NAME);
  #endif

  return 0;
}



/**
 * Returns a new trace model.
 */
adsm_module_t *
new (sqlite3 * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  adsm_module_t *self;
  local_data_t *local_data;
  EVT_event_type_t events_listened_for[] = {
    EVT_Detection,
    0
  };
  guint nprod_types, i, j, k;
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

  /* Initialize the 3D array of trace periods. */
  local_data->production_types = units->production_type_names;
  nprod_types = local_data->production_types->len;
  for (i = 0; i < ADSM_NCONTACT_TYPES; i++)
    {
      for (j = 0; j < ADSM_NTRACE_DIRECTIONS; j++)
        {
          local_data->trace_period[i][j] = g_new (int, nprod_types);
          for (k = 0; k < nprod_types; k++)
            {
              local_data->trace_period[i][j][k] = -1;
            }
        }    
    }

  /* Call the set_params function to read the production type specific
   * parameters. */
  sqlite3_exec_dict (params,
                     "SELECT prodtype.name AS prodtype,direct_trace_period,trace_direct_forward,trace_direct_back,indirect_trace_period,trace_indirect_forward,trace_indirect_back "
                     "FROM ScenarioCreator_productiontype prodtype,ScenarioCreator_controlprotocol protocol,ScenarioCreator_protocolassignment xref "
                     "WHERE prodtype.id=xref.production_type_id "
                     "AND xref.control_protocol_id=protocol.id "
                     "AND (trace_direct_forward=1 OR trace_direct_back=1 OR trace_indirect_forward=1 OR trace_indirect_back=1)",
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

/* end of file trace_model.c */
