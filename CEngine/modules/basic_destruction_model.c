/** @file basic_destruction_model.c
 * Module that simulates a policy of destroying diseased units.
 *
 * When a unit is detected as diseased, this module requests the destruction of
 * the unit.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date September 2003
 *
 * Copyright &copy; University of Guelph, 2003-2009
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
#define new basic_destruction_model_new
#define run basic_destruction_model_run
#define reset basic_destruction_model_reset
#define events_listened_for basic_destruction_model_events_listened_for
#define to_string basic_destruction_model_to_string
#define local_free basic_destruction_model_free
#define handle_detection_event basic_destruction_model_handle_detection_event

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

#include "basic_destruction_model.h"

#if !HAVE_ROUND && HAVE_RINT
#  define round rint
#endif

/* Temporary fix -- "round" and "rint" are in the math library on Red Hat 7.3,
 * but they're #defined so AC_CHECK_FUNCS doesn't find them. */
double round (double x);

/** This must match an element name in the DTD. */
#define MODEL_NAME "basic-destruction-model"



#define NEVENTS_LISTENED_FOR 1
EVT_event_type_t events_listened_for[] = { EVT_Detection };



/** Specialized information for this model. */
typedef struct
{
  int *priority; /**< The priority associated with each production type. The
    priority numbers start at 1 for the highest priority. If an element in this
    array is 0, then basic destruction is not used for that production type. */
  GPtrArray *production_types;
  GHashTable *priority_order_table; /**< A temporary structure that exists
    for use in the set_params functions. */
}
local_data_t;



/**
 * Responds to a detection by ordering destruction actions.
 *
 * @param self the model.
 * @param units the list of units.
 * @param event a report event.
 * @param queue for any new events the model creates.
 */
void
handle_detection_event (struct adsm_module_t_ *self, UNT_unit_list_t * units,
                        EVT_detection_event_t * event, EVT_event_queue_t * queue)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  int priority;

#if DEBUG
  g_debug ("----- ENTER handle_detection_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;

  /* Check whether the unit is a production type we're interested in, and that
   * it is not already destroyed.  We can "detect" a destroyed unit because of
   * test result delays -- if a test comes back positive and the unit has been
   * pre-emptively destroyed in the meantime, that is still a "detection". */
  priority = local_data->priority[unit->production_type];
  if (priority > 0 && unit->state != Destroyed)
    {
      #if DEBUG
        g_debug ("ordering unit \"%s\" destroyed", event->unit->official_id);
      #endif
      EVT_event_enqueue (queue,
                         EVT_new_request_for_destruction_event (event->unit,
                                                                event->day,
                                                                "Det",
                                                                priority));
    }

#if DEBUG
  g_debug ("----- EXIT handle_detection_event (%s)", MODEL_NAME);
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
    case EVT_Detection:
      handle_detection_event (self, units, &(event->u.detection), queue);
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
reset (struct adsm_module_t_ *self)
{
#if DEBUG
  g_debug ("----- ENTER reset (%s)", MODEL_NAME);
#endif

  /* Nothing to do. */

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
to_string (struct adsm_module_t_ *self)
{
  local_data_t *local_data;
  GString *s;
  guint nprod_types, i;
  char *chararray;

  local_data = (local_data_t *) (self->model_data);
  s = g_string_new (NULL);
  g_string_sprintf (s, "<%s", MODEL_NAME);

  nprod_types = local_data->production_types->len;
  for (i = 0; i < nprod_types; i++)
    {
      if (local_data->priority[i] > 0)
        {
          g_string_append_printf (s, "\n  for %s",
                                  (char *) g_ptr_array_index (local_data->production_types, i));
          g_string_append_printf (s, "\n    priority=%d", local_data->priority[i]);
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

#if DEBUG
  g_debug ("----- ENTER free (%s)", MODEL_NAME);
#endif

  /* Free the dynamically-allocated parts. */
  local_data = (local_data_t *) (self->model_data);
  g_free (local_data->priority);
  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Adds a set of parameters to a basic destruction model. This function will be
 * called once for each production type that has basic destruction enabled.
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
  char *key;
  gpointer p;
  guint priority;

  #if DEBUG
    g_debug ("----- ENTER set_params (%s)", MODEL_NAME);
  #endif

  self = (adsm_module_t *)data;
  local_data = (local_data_t *) (self->model_data);

  g_assert (ncols == 1);

  /* Priority numbers are stored in a hash table keyed by strings of the form
   * "production type,reason". */
  production_type_name = value[0];
  key = g_strdup_printf ("%s,%s", production_type_name,
                         ADSM_control_reason_name[ADSM_ControlDetection]);
  p = g_hash_table_lookup (local_data->priority_order_table, key);
  g_assert (p != NULL);
  priority = GPOINTER_TO_UINT(p);
  g_free (key);  

  production_type_id = adsm_read_prodtype(production_type_name, local_data->production_types);
  local_data->priority[production_type_id] = priority;

  return 0;
}



/**
 * Returns a new basic destruction model.
 */
adsm_module_t *
new (sqlite3 * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  adsm_module_t *self;
  local_data_t *local_data;
  guint nprod_types;
  char *sqlerr;

#if DEBUG
  g_debug ("----- ENTER new (%s)", MODEL_NAME);
#endif

  self = g_new (adsm_module_t, 1);
  local_data = g_new (local_data_t, 1);

  self->name = MODEL_NAME;
  self->events_listened_for = events_listened_for;
  self->nevents_listened_for = NEVENTS_LISTENED_FOR;
  self->outputs = g_ptr_array_new ();
  self->model_data = local_data;
  self->run = run;
  self->reset = reset;
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
  local_data->priority = g_new0 (int, nprod_types);

  /* Get a table that shows the priority order for combinations of production
   * type and reason for destruction. */
  local_data->priority_order_table = adsm_read_priority_order (params);

  sqlite3_exec (params,
                "SELECT prodtype.name FROM ScenarioCreator_productiontype prodtype,ScenarioCreator_controlprotocol protocol,ScenarioCreator_protocolassignment xref WHERE prodtype.id=xref.production_type_id AND xref.control_protocol_id=protocol.id AND use_destruction=1",
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

/* end of file basic_destruction_model.c */
