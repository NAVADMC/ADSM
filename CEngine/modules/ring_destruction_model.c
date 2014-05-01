/** @file ring_destruction_model.c
 * Module that simulates a policy of destroying units within a certain
 * distance of a diseased unit.
 *
 * When a unit is detected as diseased, this module requests the destruction of
 * all units within a given radius of the diseased unit.
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
#define new ring_destruction_model_new
#define run ring_destruction_model_run
#define reset ring_destruction_model_reset
#define events_listened_for ring_destruction_model_events_listened_for
#define to_string ring_destruction_model_to_string
#define local_free ring_destruction_model_free
#define handle_detection_event ring_destruction_model_handle_detection_event
#define check_and_choose ring_destruction_model_check_and_choose

#include "module.h"
#include "module_util.h"
#include "gis.h"
#include "spatial_search.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#if HAVE_STRINGS_H
#  include <strings.h>
#endif

#if HAVE_MATH_H
#  include <math.h>
#endif

#include "ring_destruction_model.h"

#if !HAVE_ROUND && HAVE_RINT
#  define round rint
#endif

/* Temporary fix -- "round" and "rint" are in the math library on Red Hat 7.3,
 * but they're #defined so AC_CHECK_FUNCS doesn't find them. */
double round (double x);

/** This must match an element name in the DTD. */
#define MODEL_NAME "ring-destruction-model"



#define NEVENTS_LISTENED_FOR 1
EVT_event_type_t events_listened_for[] = { EVT_Detection };



#define EPSILON 0.01 /* 10 m */



/** Specialized information for this model. */
typedef struct
{
  gboolean triggers_ring;
  double radius;
  gboolean include_in_ring;
  int priority;
}
param_block_t;



typedef struct
{
  GPtrArray *production_types;
  param_block_t **param_block;
  GHashTable *priority_order_table; /**< A temporary structure that exists
    for use in the set_params functions. */
}
local_data_t;



/**
 * Special structure for use with the callback function below.
 */
typedef struct
{
  local_data_t *local_data;
  UNT_unit_list_t *units;
  UNT_unit_t *unit1;
  int day;
  EVT_event_queue_t *queue;
} callback_t;



/**
 * Check whether unit 2 should be part of the destruction ring.
 */
void
check_and_choose (int id, gpointer arg)
{
  callback_t *callback_data;
  UNT_unit_t *unit2;
  UNT_unit_t *unit1;
  local_data_t *local_data;
  param_block_t *param_block;

#if DEBUG
  g_debug ("----- ENTER check_and_choose (%s)", MODEL_NAME);
#endif

  callback_data = (callback_t *) arg;
  unit2 = UNT_unit_list_get (callback_data->units, id);

  /* Are unit 1 and unit 2 the same? */
  unit1 = callback_data->unit1;
  if (unit1 == unit2)
    goto end;

  local_data = callback_data->local_data;

  /* Is unit 2 the production type we're interested in, and not already
   * destroyed? */
  param_block = local_data->param_block[unit2->production_type];
  if (param_block == NULL
      || param_block->include_in_ring == FALSE
      || unit2->state == Destroyed)
    goto end;

#if DEBUG
  g_debug ("unit \"%s\" within radius, ordering unit destroyed", unit2->official_id);
#endif
  EVT_event_enqueue (callback_data->queue,
                     EVT_new_request_for_destruction_event (unit2,
                                                            callback_data->day,
                                                            "Ring",
                                                            param_block->priority));

end:
#if DEBUG
  g_debug ("----- EXIT check_and_choose (%s)", MODEL_NAME);
#endif
  return;
}



void
ring_destroy (struct adsm_module_t_ *self, UNT_unit_list_t * units,
              UNT_unit_t * unit, double radius, int day, EVT_event_queue_t * queue)
{
  local_data_t *local_data;
  callback_t callback_data;

#if DEBUG
  g_debug ("----- ENTER ring_destroy (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  callback_data.local_data = local_data;
  callback_data.units = units;
  callback_data.unit1 = unit;
  callback_data.day = day;
  callback_data.queue = queue;

  /* Find the distances to other units. */
  spatial_search_circle_by_id (units->spatial_index, unit->index,
                               radius + EPSILON,
                               check_and_choose, &callback_data);

#if DEBUG
  g_debug ("----- EXIT ring_destroy (%s)", MODEL_NAME);
#endif
}



/**
 * Responds to a detection by ordering destruction actions.
 *
 * @param self the model.
 * @param units a list of units.
 * @param event a detection event.
 * @param queue for any new events the model creates.
 */
void
handle_detection_event (struct adsm_module_t_ *self, UNT_unit_list_t * units,
                        EVT_detection_event_t * event, EVT_event_queue_t * queue)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  param_block_t *param_block;

#if DEBUG
  g_debug ("----- ENTER handle_detection_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;

  param_block = local_data->param_block[unit->production_type];
  if (param_block != NULL && param_block->triggers_ring == TRUE)
    ring_destroy (self, units, unit, param_block->radius, event->day, queue);

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
  param_block_t *param_block;
  gboolean already_names;
  char *chararray;

  local_data = (local_data_t *) (self->model_data);
  s = g_string_new (NULL);
  g_string_printf (s, "<%s", MODEL_NAME);

  nprod_types = local_data->production_types->len;
  for (i = 0; i < nprod_types; i++)
    {
      param_block = local_data->param_block[i];
      if (param_block != NULL && param_block->triggers_ring)
        {
          g_string_append_printf (s, "\n  %s triggers %g km ring",
                                  (char *) g_ptr_array_index (local_data->production_types, i),
                                  param_block->radius);
        }
    }
  already_names = FALSE;
  g_string_append_printf (s, "\n  included in ring: ");
  for (i = 0; i < nprod_types; i++)
    {
      param_block = local_data->param_block[i];
      if (param_block != NULL && param_block->include_in_ring)
        {
          if (already_names)
            g_string_append_c (s, ',');
          else
            already_names = TRUE;
          g_string_append_printf (s, "%s",
                                  (char *) g_ptr_array_index (local_data->production_types, i));
        }
    }
  if (!already_names)
    g_string_append_printf (s, "none");

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
  guint nprod_types, i;

#if DEBUG
  g_debug ("----- ENTER free (%s)", MODEL_NAME);
#endif

  /* Free the dynamically-allocated parts. */
  local_data = (local_data_t *) (self->model_data);

  nprod_types = local_data->production_types->len;
  for (i = 0; i < nprod_types; i++)
    {
      if (local_data->param_block[i] != NULL)
        g_free (local_data->param_block[i]);
    }
  g_free (local_data->param_block);
  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Adds a set of parameters to a ring destruction model.
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
  param_block_t *p;
  long int tmp;

  #if DEBUG
    g_debug ("----- ENTER set_params (%s)", MODEL_NAME);
  #endif

  g_assert (ncols == 4);

  self = (adsm_module_t *)data;
  local_data = (local_data_t *) (self->model_data);

  /* Find out which production type these parameters apply to. */
  production_type_name = value[0];
  production_type_id = adsm_read_prodtype (production_type_name, local_data->production_types);

  /* Check that we are not overwriting an existing parameter block (that would
   * indicate a bug). */
  g_assert (local_data->param_block[production_type_id] == NULL);

  /* Create a new parameter block. */
  p = g_new (param_block_t, 1);
  local_data->param_block[production_type_id] = p;

  /* Read the parameters. */
  errno = 0;
  tmp = strtol (value[1], NULL, /* base */ 10);
  g_assert (errno != ERANGE && errno != EINVAL);
  g_assert (tmp == 0 || tmp == 1);
  p->triggers_ring = (tmp == 1);
  
  if (p->triggers_ring)
    {
      errno = 0;
      p->radius = strtod (value[2], NULL);
      g_assert (errno != ERANGE);
      /* Radius must be positive. */
      if (p->radius < 0)
        {
          g_warning ("%s: radius cannot be negative, setting to 0", MODEL_NAME);
          p->radius = 0;
        }
    }

  errno = 0;
  tmp = strtol (value[3], NULL, /* base */ 10);
  g_assert (errno != ERANGE && errno != EINVAL);
  g_assert (tmp == 0 || tmp == 1);
  p->include_in_ring = (tmp == 1);

  if (p->include_in_ring)
    {
      char *key;
      gpointer ptr;

      key = g_strdup_printf ("%s,%s", production_type_name,
                             SPREADMODEL_control_reason_name[SPREADMODEL_ControlRing]);
      ptr = g_hash_table_lookup (local_data->priority_order_table, key);
      g_assert (ptr != NULL);
      p->priority = GPOINTER_TO_UINT(ptr);
      g_free (key);
    }

  return 0;
}



/**
 * Returns a new ring destruction model.
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

  /* Initialize an array to hold parameter blocks. */
  local_data->production_types = units->production_type_names;
  nprod_types = local_data->production_types->len;
  local_data->param_block = g_new0 (param_block_t *, nprod_types);

  /* Get a table that shows the priority order for combinations of production
   * type and reason for destruction. */
  local_data->priority_order_table = adsm_read_priority_order (params);
  sqlite3_exec (params,
                "SELECT prodtype.name,destruction_is_a_ring_trigger,destruction_ring_radius,destruction_is_a_ring_target FROM ScenarioCreator_productiontype prodtype,ScenarioCreator_controlprotocol protocol,ScenarioCreator_protocolassignment xref WHERE prodtype.id=xref.production_type_id AND xref.control_protocol_id=protocol.id AND (destruction_is_a_ring_trigger=1 OR destruction_is_a_ring_target=1)",
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

/* end of file ring_destruction_model.c */
