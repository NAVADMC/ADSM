/** @file destruction_wait_time_vaccination_trigger.c
 * Module that requests initiation of a vaccination program once a certain
 * number of detections (possibly restricted to a subset of production types)
 * have occurred over the last n days.
 *
 * @author nharve01@uoguelph.ca<br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
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
#define new destruction_wait_time_vaccination_trigger_new
#define factory destruction_wait_time_vaccination_trigger_factory
#define run destruction_wait_time_vaccination_trigger_run
#define to_string destruction_wait_time_vaccination_trigger_to_string
#define local_free destruction_wait_time_vaccination_trigger_free
#define handle_before_each_simulation_event destruction_wait_time_vaccination_trigger_handle_before_each_simulation_event
#define handle_new_day_event destruction_wait_time_vaccination_trigger_handle_new_day_event
#define handle_commitment_to_destroy_event destruction_wait_time_vaccination_trigger_handle_commitment_to_destroy_event
#define handle_destruction_event destruction_wait_time_vaccination_trigger_handle_destruction_event
#define handle_end_of_day_event destruction_wait_time_vaccination_trigger_handle_end_of_day_event
#define handle_vaccination_terminated_event destruction_wait_time_vaccination_trigger_handle_vaccination_terminated_event

#include "module.h"
#include "module_util.h"
#include "sqlite3_exec_dict.h"
#include "destruction_wait_time_vaccination_trigger.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "destruction-wait-time-vaccination-trigger"



/** Specialized information for this module. */
typedef struct
{
  guint trigger_id;
  gboolean *production_type; /**< Which production types we are interested in
    counting. */
  GPtrArray *production_types; /**< Production type names. Each item in the
    array is a (char *). */
  guint num_days; /**< Number of days back we count requests for destruction,
    plus one */
  guint *num_requests; /**< An array of size num_days. The count of requests
    made on simulation day "d" is in location (d % num_days). */
  GHashTable *requests; /**< Records the day on which Commitment to Destroy
    events are heard for particular units. Keys are unit pointers (UNT_unit_t *),
    values are days transformed with GINT_TO_POINTER. */
  sqlite3 *db; /* Temporarily stash a pointer to the parameters database here
    so that it will be available to the set_params function. */
}
local_data_t;



/**
 * Before each simulation, start with no requests for destruction recorded.
 *
 * @param self this module.
 */
void
handle_before_each_simulation_event (struct adsm_module_t_ *self)
{
  local_data_t *local_data;
  guint i;

  #if DEBUG
    g_debug ("----- ENTER handle_before_each_simulation_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);
  g_hash_table_remove_all (local_data->requests);
  for (i = 0; i < local_data->num_days; i++)
    {
      local_data->num_requests[i] = 0;
    }

  #if DEBUG
    g_debug ("----- EXIT handle_before_each_simulation_event (%s)", MODEL_NAME);
  #endif
}



/**
 * Responds to a new day event by dropping the oldest count and initializing
 * today's count to 0.
 *
 * @param self this module.
 * @param event a detection event.
 */
void
handle_new_day_event (struct adsm_module_t_ *self,
                      EVT_new_day_event_t *event)
{
  local_data_t *local_data;

  #if DEBUG
    g_debug ("----- ENTER handle_new_day_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);
  /* The num_requests array looks like this:
   *
   *           event->day
   *               |
   *               v
   * +---+---+---+---+---+
   * |-3 |-2 |-1 | 0 |-4 |
   * +---+---+---+---+---+
   *                   ^
   *                   |
   *         If this entry is >0 at end
   *         of day, initiate vaccination.
   */

  /* Zero today's count of requests for destruction (it replaces the oldest
   * count in the array). */
  local_data->num_requests[event->day % local_data->num_days] = 0;

  #if DEBUG
    g_debug ("----- EXIT handle_new_day_event (%s)", MODEL_NAME);
  #endif
  return;
}



/**
 * Responds to a Commitment to Destroy event by counting it.
 *
 * @param self this module.
 * @param event a commitment to destroy event.
 */
void
handle_commitment_to_destroy_event (struct adsm_module_t_ *self,
                                    EVT_commitment_to_destroy_event_t *event)
{
  local_data_t *local_data;
  UNT_unit_t *unit;

  #if DEBUG
    g_debug ("----- ENTER handle_commitment_to_destroy_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;

  /* This if statement ensures that only the oldest request for each unit is
   * stored. */
  if (local_data->production_type[unit->production_type] == TRUE
      && g_hash_table_lookup (local_data->requests, unit) == NULL)
    {
      g_hash_table_insert (local_data->requests, unit, GINT_TO_POINTER(event->day));
      local_data->num_requests[event->day % local_data->num_days] += 1;
    }

  #if DEBUG
    g_debug ("----- EXIT handle_commitment_to_destroy_event (%s)", MODEL_NAME);
  #endif
  return;
}



/**
 * Responds to a Destruction event by decrementing the count of unfulfilled
 * Commitment to Destroy events.
 *
 * @param self this module.
 * @param event a destruction event.
 */
void
handle_destruction_event (struct adsm_module_t_ *self,
                          EVT_destruction_event_t *event)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  int commitment_day;

  #if DEBUG
    g_debug ("----- ENTER handle_destruction_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;

  if (local_data->production_type[unit->production_type] == TRUE)
    {
      /* Note that we may see Destruction events for units that are *not* in
       * the table.  This can happen after the table is cleared upon
       * termination of the vaccination program. */
      if (g_hash_table_lookup (local_data->requests, unit) != NULL)
        {
          commitment_day = GPOINTER_TO_INT(g_hash_table_lookup (local_data->requests, unit));
          local_data->num_requests[commitment_day % local_data->num_days] -= 1;
          g_hash_table_remove (local_data->requests, unit);
        }
    }

  #if DEBUG
    g_debug ("----- EXIT handle_destruction_event (%s)", MODEL_NAME);
  #endif
  return;
}



/**
 * Responds to an End of Day event by checking if there are units that have
 * been waiting for the prescribed number of days, and if so, issuing an
 * Initiate Vaccination event. 
 *
 * @param self this module.
 * @param event an end of day event.
 * @param queue for any new events this module creates.
 */
void
handle_end_of_day_event (struct adsm_module_t_ *self,
                         EVT_end_of_day_event_t *event,
                         EVT_event_queue_t *queue)
{
  local_data_t *local_data;
  guint num_oldest_requests;

  #if DEBUG
    g_debug ("----- ENTER handle_end_of_day_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);

  num_oldest_requests = local_data->num_requests[(event->day + 1) % local_data->num_days];
  if (num_oldest_requests > 0)
    {
      #if DEBUG
        g_debug ("%u units have been waiting %u days, requesting initiation of vaccination program",
                 num_oldest_requests, local_data->num_days - 1);
      #endif
      EVT_event_enqueue (queue,
        EVT_new_request_to_initiate_vaccination_event (event->day,
                                                       local_data->trigger_id,
                                                       MODEL_NAME));
    }

  #if DEBUG
    g_debug ("----- EXIT handle_end_of_day_event (%s)", MODEL_NAME);
  #endif
  return;
}



/**
 * Responds to a vaccination terminated event by clearing the records of
 * unfulfilled Commitment to Destroy events.  Will start anew with any
 * Commitment to Destroy events that arrive after the vaccination program has
 * been ended.
 *
 * @param self this module.
 * @param event a vaccination terminated event.
 */
void
handle_vaccination_terminated_event (struct adsm_module_t_ *self,
                                     EVT_vaccination_terminated_event_t *event)
{
  local_data_t *local_data;
  guint i;

  #if DEBUG
    g_debug ("----- ENTER handle_vaccination_terminated_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);  
  g_hash_table_remove_all (local_data->requests);
  for (i = 0; i < local_data->num_days; i++)
    {
      local_data->num_requests[i] = 0;
    }

  #if DEBUG
    g_debug ("----- EXIT handle_vaccination_terminated_event (%s)", MODEL_NAME);
  #endif
  return;
}



/**
 * Runs this module.
 *
 * @param self this module.
 * @param units a unit list.
 * @param zones a zone list.
 * @param event the event that caused this module to run.
 * @param rng a random number generator.
 * @param queue for any new events this module creates.
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
    case EVT_NewDay:
      handle_new_day_event (self, &(event->u.new_day));
      break;
    case EVT_CommitmentToDestroy:
      handle_commitment_to_destroy_event (self, &(event->u.commitment_to_destroy));
      break;
    case EVT_Destruction:
      handle_destruction_event (self, &(event->u.destruction));
      break;
    case EVT_EndOfDay:
      handle_end_of_day_event (self, &(event->u.end_of_day), queue);
      break;
    case EVT_VaccinationTerminated:
      handle_vaccination_terminated_event (self, &(event->u.vaccination_terminated));
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
 * Returns a text representation of this module.
 *
 * @param self this module.
 * @return a string.
 */
char *
to_string (struct adsm_module_t_ *self)
{
  local_data_t *local_data;
  GString *s;
  gboolean already_names;
  guint i;

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
  g_string_append_printf (s, " max wait time=%u days", local_data->num_days - 1);
  g_string_append_c (s, '>');

  /* don't return the wrapper object */
  return g_string_free (s, /* free_segment = */ FALSE);
}



/**
 * Frees this module.
 *
 * @param self the module.
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
  g_free (local_data->production_type);
  g_free (local_data->num_requests);
  g_hash_table_destroy (local_data->requests);
  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

  #if DEBUG
    g_debug ("----- EXIT free (%s)", MODEL_NAME);
  #endif
}



/**
 * A type to hold arguments to set_trigger_prodtype().
 */
typedef struct
{
  gboolean *flags;
  GPtrArray *production_types;
}
set_trigger_prodtype_args_t;



static int
set_trigger_prodtype (void *data, GHashTable *dict)
{
  set_trigger_prodtype_args_t *args;
  guint production_type_id;

  args = data;
  /* We receive the production type as a name (string). Get the production type
   * ID by looking it up in the array production_types. Then set the boolean
   * flag for that production type ID in the trigger. */
  production_type_id =
    adsm_read_prodtype (g_hash_table_lookup (dict, "prodtype"),
                        args->production_types);
  args->flags[production_type_id] = TRUE;
  return 0;
}



/**
 * Adds a set of parameters to a destruction-wait-time vaccination trigger module.
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
  sqlite3 *params;
  guint nprod_types;
  guint trigger_id;
  set_trigger_prodtype_args_t args;
  gchar *sql;
  char *sqlerr;

  #if DEBUG
    g_debug ("----- ENTER set_params (%s)", MODEL_NAME);
  #endif

  self = (adsm_module_t *)data;
  local_data = (local_data_t *) (self->model_data);
  params = local_data->db;

  local_data->num_days = strtol(g_hash_table_lookup (dict, "days"), NULL, /* base */ 10);
  /* All the arithmetic on num_days from now on will actually need the value
   * num_days+1, so just add 1 right now. */
  local_data->num_days += 1;

  /* An array to hold per-day counts of unfulfilled Commitment to Destroy events
   * over the last num_days days. */
  local_data->num_requests = g_new (guint, local_data->num_days);

  /* Fill in the production types that this trigger counts. */
  nprod_types = local_data->production_types->len;
  local_data->production_type = g_new(gboolean, nprod_types);
  trigger_id = strtol(g_hash_table_lookup (dict, "id"), NULL, /* base */ 10);
  sql = g_strdup_printf ("SELECT prodtype.name AS prodtype "
                         "FROM ScenarioCreator_productiontype prodtype,ScenarioCreator_destructionwaittime_trigger_group trigger "
                         "WHERE trigger.destructionwaittime_id=%u "
                         "AND prodtype.id=trigger.productiontype_id",
                         trigger_id);
  args.flags = local_data->production_type;
  args.production_types = local_data->production_types;
  sqlite3_exec_dict (params, sql,
                     set_trigger_prodtype, &args, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }
  g_free (sql);

  #if DEBUG
    g_debug ("----- EXIT set_params (%s)", MODEL_NAME);
  #endif

  return 0;
}



/**
 * Returns a new destruction-wait-time vaccination trigger module.
 */
adsm_module_t *
new (sqlite3 * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones, gpointer user_data, GError **error)
{
  adsm_module_t *self;
  local_data_t *local_data;
  EVT_event_type_t events_listened_for[] = {
    EVT_BeforeEachSimulation,
    EVT_NewDay,
    EVT_CommitmentToDestroy,
    EVT_Destruction,
    EVT_EndOfDay,
    EVT_VaccinationTerminated,
    0
  };
  guint trigger_id;
  char *sql;
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

  local_data->production_types = units->production_type_names;

  /* A hash table (used as set data type) for recording the day on which
   * Commitment to Destroy events are heard. */
  local_data->requests = g_hash_table_new (g_direct_hash, g_int_equal);

  /* Call the set_params function to read trigger's details. */
  trigger_id = GPOINTER_TO_UINT(user_data);
  local_data->trigger_id = trigger_id;
  sql = g_strdup_printf ("SELECT id,days "
                         "FROM ScenarioCreator_destructionwaittime "
                         "WHERE id=%u", trigger_id);
  local_data->db = params;
  sqlite3_exec_dict (params, sql, set_params, self, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }
  local_data->db = NULL;
  g_free (sql);

  #if DEBUG
    g_debug ("----- EXIT new (%s)", MODEL_NAME);
  #endif

  return self;
}



/**
 * A type to hold arguments to create_trigger().
 */
typedef struct
{
  sqlite3 *params;
  UNT_unit_list_t *units;
  projPJ projection;
  ZON_zone_list_t * zones;
  GError **error;
  GSList *triggers;  
}
create_trigger_args_t;



/**
 * The function receives a trigger ID and calls "new" to instantiate that
 * trigger.
 */
static int
create_trigger (void *data, GHashTable *dict)
{
  create_trigger_args_t *args;
  guint trigger_id;
  adsm_module_t *module;

  args = data;
  
  /* We receive the trigger ID as a name (string). */
  trigger_id = strtol(g_hash_table_lookup (dict, "id"), NULL, /* base */ 10);
  #if DEBUG
    g_debug ("creating trigger with ID %u", trigger_id);
  #endif

  /* Call the "new" function to instantiate a module for the trigger with that
   * ID. */
  module =
    destruction_wait_time_vaccination_trigger_new (args->params, args->units,
      args->projection, args->zones, GUINT_TO_POINTER(trigger_id), args->error);

  /* Add the new module to the list returned by the factory. */
  args->triggers = g_slist_prepend (args->triggers, module);

  return 0;
}



/**
 * Returns one or more new destruction-wait-time vaccination trigger modules.
 */
GSList *
factory (sqlite3 * params, UNT_unit_list_t * units, projPJ projection,
         ZON_zone_list_t * zones, GError **error)
{
  GSList *modules;
  create_trigger_args_t args;
  char *sqlerr;

  #if DEBUG
    g_debug ("----- ENTER factory (%s)", MODEL_NAME);
  #endif

  /* Call the set_params function to read the individual triggers. Because
   * sqlite3_exec_dict callback functions have only 1 parameter available for
   * user data, we pack all the arguments set_params will need into a structure
   * to pass. */
  args.params = params;
  args.units = units;
  args.projection = projection;
  args.zones = zones;
  args.error = error;
  args.triggers = NULL;
  sqlite3_exec_dict (params,
                     "SELECT id FROM ScenarioCreator_destructionwaittime",
                     create_trigger, &args, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }
  modules = args.triggers;

  #if DEBUG
    g_debug ("----- EXIT factory (%s)", MODEL_NAME);
  #endif

  return modules;
}

/* end of file destruction_wait_time_vaccination_trigger.c */
