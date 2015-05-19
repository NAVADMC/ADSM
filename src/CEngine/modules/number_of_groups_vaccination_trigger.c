/** @file number_of_groups_vaccination_trigger.c
 * Module that requests initiation of a vaccination program once detections
 * have occurred in a certain number of production type subsets.
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
#define new number_of_groups_vaccination_trigger_new
#define factory number_of_groups_vaccination_trigger_factory
#define run number_of_groups_vaccination_trigger_run
#define to_string number_of_groups_vaccination_trigger_to_string
#define local_free number_of_groups_vaccination_trigger_free
#define handle_before_each_simulation_event number_of_groups_vaccination_trigger_handle_before_each_simulation_event
#define handle_new_day_event number_of_groups_vaccination_trigger_handle_new_day_event
#define handle_detection_event number_of_groups_vaccination_trigger_handle_detection_event
#define handle_vaccination_terminated_event number_of_groups_vaccination_trigger_handle_vaccination_terminated_event

#include "module.h"
#include "module_util.h"
#include "sqlite3_exec_dict.h"
#include "number_of_groups_vaccination_trigger.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "number-of-groups-vaccination-trigger"



/** Specialized information for this module. */
typedef struct
{
  guint trigger_id;
  GArray **production_type_in_groups; /**< Which groups a given production
    type is in. production_type_in_groups[prodtype] gives a GArray of guints,
    each guint being a group index. */
  GPtrArray *production_types; /**< Production type names. Each item in the
    array is a (char *). */
  guint num_groups; /**< How many production type groups there are. */
  gboolean *detection_in_group; /**< Whether a detection has been recorded in
    a group. Test whether detection_in_group[group] == TRUE. */
  guint num_groups_involved; /**< How many groups have detections been recorded
    in. */
  guint threshold; /**< The number of groups at which we initiate detection. */
  GHashTable *detected; /**< Units detected so far.  Hash table used as a set
    data type to eliminate duplicates (e.g., a single unit can create detection
    events both by clinical signs and by lab test).  Keys are unit pointers
    (UNT_unit_t *), values are unimportant (presence or absence of a key is all
    we ever test. */
  sqlite3 *db; /* Temporarily stash a pointer to the parameters database here
    so that it will be available to the set_params function. */
}
local_data_t;



/**
 * Before each simulation, start with no detections recorded.
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
  g_hash_table_remove_all (local_data->detected);
  for (i = 0; i < local_data->num_groups; i++)
    {
      local_data->detection_in_group[i] = FALSE;
    }
  local_data->num_groups_involved = 0;

  #if DEBUG
    g_debug ("----- EXIT handle_before_each_simulation_event (%s)", MODEL_NAME);
  #endif
}



/**
 * Responds to a detection event by counting it, and sending out an
 * InitiateVaccination event if the threshold has been crossed.
 *
 * @param self this module.
 * @param event a detection event.
 * @param queue for any new events this module creates.
 */
void
handle_detection_event (struct adsm_module_t_ *self,
                        EVT_detection_event_t *event,
                        EVT_event_queue_t *queue)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  GArray *unit_groups;
  guint i;
  guint group;
  gboolean already_triggered;

  #if DEBUG
    g_debug ("----- ENTER handle_detection_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;
  
  /* Process this event only if this unit hasn't been detected before. */
  if (g_hash_table_lookup (local_data->detected, unit) == NULL)
    {
      g_hash_table_insert (local_data->detected, unit, GINT_TO_POINTER(1));
      unit_groups = local_data->production_type_in_groups[unit->production_type];
      for (i = 0, already_triggered = FALSE;
           (i < unit_groups->len) && (!already_triggered);
           i++)
        {
          group = g_array_index (unit_groups, guint, i);
          if (local_data->detection_in_group[group] == FALSE)
            {
              /* This is the first detection in a new group. */
              local_data->detection_in_group[group] = TRUE;
              local_data->num_groups_involved++;
              if (local_data->num_groups_involved == local_data->threshold)
                {
                  #if DEBUG
                    g_debug ("%u groups involved, requesting initiation of vaccination program",
                             local_data->num_groups_involved);
                  #endif
                  /* Note that these messages can be sent even if a vaccination
                   * program is currently active. To keep the trigger modules
                   * simple, it's the resources model's problem to ignore
                   * multiple/redundant requests to initiate vaccination. */
                  EVT_event_enqueue (queue,
                    EVT_new_request_to_initiate_vaccination_event (event->day,
                                                                   local_data->trigger_id,
                                                                   MODEL_NAME));
                  already_triggered = TRUE;
                }      
            } /* end of "if this group has no detections yet" */
        } /* end of loop over groups this production type is in */
   } /* end of if unit has not been detected before and trigger is interested in this production type */          

  #if DEBUG
    g_debug ("----- EXIT handle_detection_event (%s)", MODEL_NAME);
  #endif
  return;
}



/**
 * Responds to a vaccination terminated event by resetting the count of groups
 * with detections to zero. (Leaves the set of detected herds alone, though,
 * since we still need that to avoid re-counting a duplicate detection.)
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
  for (i = 0; i < local_data->num_groups; i++)
    {
      local_data->detection_in_group[i] = FALSE;
    }
  local_data->num_groups_involved = 0;

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
    case EVT_Detection:
      handle_detection_event (self, &(event->u.detection), queue);
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
  GArray **group_contains_production_types;
  unsigned int i, j;

  #if DEBUG
    g_debug ("----- ENTER to_string (%s)", MODEL_NAME);
  #endif
  local_data = (local_data_t *) (self->model_data);
  s = g_string_new (NULL);
  g_string_sprintf (s, "<%s groups=[", MODEL_NAME);
  /* The groups are stored so that you can look up groups given production
   * type. Here, we want to go in the other direction (loop over the groups and
   * list production types) so we temporarily create a new mapping. */
  group_contains_production_types = g_new0 (GArray *, local_data->num_groups);  
  for (i = 0; i < local_data->num_groups; i++)
    {
      group_contains_production_types[i] =
        g_array_new (/* zero_terminated = */ FALSE, /* clear = */ FALSE, sizeof (guint));
    }
  for (i = 0; i < local_data->production_types->len; i++)
    {
      GArray *groups;
      groups = local_data->production_type_in_groups[i];
      if (groups != NULL)
        {
          for (j = 0; j < groups->len; j++)
            {
              guint group;
              group = g_array_index (groups, guint, j);
              g_array_append_val (group_contains_production_types[group], i);
            }
        }
    }
  /* Now list each group as part of the output string we're building. */
  for (i = 0; i < local_data->num_groups; i++)
    {
      GArray *production_types;
      g_string_append_printf (s, i == 0 ? "(" : ", (");
      production_types = group_contains_production_types[i];
      for (j = 0; j < production_types->len; j++)
        {
          UNT_production_type_t production_type;
          production_type = g_array_index (production_types, guint, j);
          g_string_append_printf (s, "%s%s", j == 0 ? "" : ",",
                                  (char *) g_ptr_array_index (local_data->production_types, production_type));
        }
      g_string_append_c (s, ')');
    }
  g_string_append_printf (s, "] threshold=%u groups involved", local_data->threshold);
  g_string_append_c (s, '>');
  /* Free the temporary mapping object, group_contains_production_types,
   * created above. */
  for (i = 0; i < local_data->num_groups; i++)
    {
      g_array_free (group_contains_production_types[i], /* free_segment = */ TRUE);
    }
  g_free (group_contains_production_types);

  #if DEBUG
    g_debug ("----- EXIT to_string (%s)", MODEL_NAME);
  #endif
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
  guint i;

  #if DEBUG
    g_debug ("----- ENTER free (%s)", MODEL_NAME);
  #endif

  /* Free the dynamically-allocated parts. */
  local_data = (local_data_t *) (self->model_data);
  for (i = 0; i < local_data->production_types->len; i++)
    {
      g_array_free (local_data->production_type_in_groups[i], /* free_segment = */ TRUE);
    }
  g_free (local_data->detection_in_group);
  g_hash_table_destroy (local_data->detected);
  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

  #if DEBUG
    g_debug ("----- EXIT free (%s)", MODEL_NAME);
  #endif
}



/**
 * A type to hold arguments to set_group_prodtype().
 */
typedef struct
{
  gboolean *flags;
  GPtrArray *production_types;
}
set_group_prodtype_args_t;



static int
set_group_prodtype (void *data, GHashTable *dict)
{
  set_group_prodtype_args_t *args;
  char *production_type_name;
  guint production_type_id;

  args = data;
  /* We receive the production type as a name (string). Get the production type
   * ID by looking it up in the array production_types. Then set the boolean
   * flag for that production type ID in the group. */
  production_type_name = g_hash_table_lookup (dict, "prodtype");
  production_type_id =
    adsm_read_prodtype (production_type_name, args->production_types);
  #if DEBUG
     g_debug ("----- add production type ID %u (\"%s\")", production_type_id,
              production_type_name);
  #endif
  args->flags[production_type_id] = TRUE;
  return 0;
}



/**
 * A type to hold arguments to create_group().
 */
typedef struct
{
  sqlite3 *params;
  GQueue *groups;
  GPtrArray *production_types;
}
create_group_args_t;



static int
create_group (void *data, GHashTable *dict)
{
  create_group_args_t *args;
  guint production_type_group_id;
  guint nprod_types;
  gboolean *flags;
  set_group_prodtype_args_t set_group_prodtype_args;
  gchar *sql;
  char *sqlerr;

  args = data;
  /* We receive the production type group ID as a string. */
  production_type_group_id =
    strtol(g_hash_table_lookup (dict, "productiongroup_id"), NULL, /* base */ 10);
  #if DEBUG
     g_debug ("----- ENTER create_group (group_id=%u)", production_type_group_id);
  #endif

  nprod_types = args->production_types->len;
  flags = g_new0 (gboolean, nprod_types);
  sql = g_strdup_printf ("SELECT name AS prodtype "
                         "FROM ScenarioCreator_productiongroup_group grp,ScenarioCreator_productiontype prodtype "
                         "WHERE grp.productiontype_id=prodtype.id "
                         "AND productiongroup_id=%u", production_type_group_id);
  set_group_prodtype_args.flags = flags;
  set_group_prodtype_args.production_types = args->production_types;
  sqlite3_exec_dict (args->params, sql, set_group_prodtype,
                     &set_group_prodtype_args, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }
  g_free (sql);

  g_queue_push_tail (args->groups, flags);
  #if DEBUG
     g_debug ("----- EXIT create_group (group_id=%u)", production_type_group_id);
  #endif
  return 0;
}



/**
 * Adds a set of parameters to a number-of-detections vaccination trigger module.
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
  guint trigger_id;
  GQueue *tmp_groups; /* Each item is of type (gboolean *). */
  create_group_args_t args;
  gchar *sql;
  char *sqlerr;
  guint i, j;

  #if DEBUG
    g_debug ("----- ENTER set_params (%s)", MODEL_NAME);
  #endif

  self = (adsm_module_t *)data;
  local_data = (local_data_t *) (self->model_data);
  params = local_data->db;

  local_data->threshold = strtol(g_hash_table_lookup (dict, "number_of_groups"), NULL, /* base */ 10);
  #if DEBUG
    g_debug ("threshold is %u groups with detections", local_data->threshold);
  #endif

  /* Read in the groups. */
  tmp_groups = g_queue_new();
  trigger_id = strtol(g_hash_table_lookup (dict, "id"), NULL, /* base */ 10);
  sql = g_strdup_printf ("SELECT productiongroup_id "
                         "FROM ScenarioCreator_spreadbetweengroups_relevant_groups "
                         "WHERE spreadbetweengroups_id=%u", trigger_id);
  args.params = params;
  args.groups = tmp_groups;
  args.production_types = local_data->production_types;
  sqlite3_exec_dict (params, sql, create_group, &args, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }
  g_free (sql);
  local_data->num_groups = g_queue_get_length(tmp_groups);
  #if DEBUG
    g_debug ("number of groups = %u", local_data->num_groups);
  #endif

  for (i = 0; !g_queue_is_empty(tmp_groups); i++)
    {
      gboolean *production_type;
      /* Get the temporary array of booleans (1 boolean per production type)
       * that we just constructed. This temporary array represents the
       * production types that are in the ith group. */
      production_type = g_queue_pop_head (tmp_groups);
      for (j = 0; j < local_data->production_types->len; j++)
        if (production_type[j] == TRUE)
          g_array_append_val (local_data->production_type_in_groups[j], i);      
      g_free (production_type);
    }
  g_queue_free (tmp_groups);

  /* Array of booleans to track which groups have had a detection. */
  local_data->detection_in_group = g_new0 (gboolean, local_data->num_groups);

  #if DEBUG
    g_debug ("----- EXIT set_params (%s)", MODEL_NAME);
  #endif

  return 0;
}



/**
 * Returns a new number-of-groups vaccination trigger module.
 */
adsm_module_t *
new (sqlite3 * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones, gpointer user_data, GError **error)
{
  adsm_module_t *self;
  local_data_t *local_data;
  EVT_event_type_t events_listened_for[] = {
    EVT_BeforeEachSimulation,
    EVT_Detection,
    EVT_VaccinationTerminated,
    0
  };
  guint i;
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
  local_data->production_type_in_groups = g_new0 (GArray *, local_data->production_types->len);
  for (i = 0; i < local_data->production_types->len; i++)
    {
      local_data->production_type_in_groups[i] =
        g_array_new (/* zero_terminated = */ FALSE, /* clear = */ FALSE, sizeof (guint));
    }

  /* A hash table (used as set data type) for counting unique detected units. */
  local_data->detected = g_hash_table_new (g_direct_hash, g_direct_equal);

  /* Call the set_params function to read trigger's details. */
  trigger_id = GPOINTER_TO_UINT(user_data);
  local_data->trigger_id = trigger_id;
  sql = g_strdup_printf ("SELECT id,number_of_groups "
                         "FROM ScenarioCreator_spreadbetweengroups "
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
    number_of_groups_vaccination_trigger_new (args->params, args->units,
      args->projection, args->zones, GUINT_TO_POINTER(trigger_id), args->error);

  /* Add the new module to the list returned by the factory. */
  args->triggers = g_slist_prepend (args->triggers, module);

  return 0;
}



/**
 * Returns one or more new number-of-groups vaccination trigger modules.
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
                     "SELECT id FROM ScenarioCreator_spreadbetweengroups",
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

/* end of file number_of_groups_vaccination_trigger.c */
