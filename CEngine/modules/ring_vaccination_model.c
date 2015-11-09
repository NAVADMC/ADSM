/** @file ring_vaccination_model.c
 * Module that simulates a policy of vaccinating units within a certain
 * distance of a diseased unit.
 *
 * When a unit is detected as diseased, this module requests the vaccination of
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
#  include "config.h"
#endif

/* To avoid name clashes when multiple modules have the same interface. */
#define new ring_vaccination_model_new
#define factory ring_vaccination_model_factory
#define run ring_vaccination_model_run
#define to_string ring_vaccination_model_to_string
#define local_free ring_vaccination_model_free
#define handle_new_day_event ring_vaccination_model_handle_new_day_event
#define handle_detection_event ring_vaccination_model_handle_detection_event
#define check_and_choose ring_vaccination_model_check_and_choose

#include "module.h"
#include "module_util.h"
#include "gis.h"
#include "spatial_search.h"
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

#include "ring_vaccination_model.h"

#if !HAVE_ROUND && HAVE_RINT
#  define round rint
#endif

/* Temporary fix -- "round" and "rint" are in the math library on Red Hat 7.3,
 * but they're #defined so AC_CHECK_FUNCS doesn't find them. */
double round (double x);

/** This must match an element name in the DTD. */
#define MODEL_NAME "ring-vaccination-model"



#define EPSILON 0.01 /* 10 m */



typedef struct
{
  guint ring_rule_id;
  gboolean *trigger_production_type; /**< Which production types trigger
    creation of a ring. */
  gboolean *target_production_type; /**< Which production types inside the ring
    get vaccinated. */
  GPtrArray *production_types; /**< Production type names. Each item in the
    array is a (char *). */
  double supp_radius; /**< Radius of suppressive ring. -1 if no suppressive
    ring is defined. */
  double prot_inner_radius; /**< Inner radius of protective ring. -1 if no
    protective ring is defined. */
  double prot_outer_radius; /**< Outer radius of protective ring. -1 if no
    protective ring is defined. */
  GHashTable *requested_today; /**< A list of units for which this module made
    requests for vaccination today.  A unit can be in queue for vaccination
    more than once at a given time, but two requests for the same unit, for the
    same reason, on the same day will have identical priority and would be
    redundant. */      
  sqlite3 *db; /* Temporarily stash a pointer to the parameters database here
    so that it will be available to the set_params function. */
}
local_data_t;



/**
 * On each new day, this module clears its list of units for which it has
 * requested vaccinations.
 *
 * @param self this module.
 */
void
handle_new_day_event (struct adsm_module_t_ *self)
{
  local_data_t *local_data;
  
#if DEBUG
  g_debug ("----- ENTER handle_new_day_event (%s)", MODEL_NAME);
#endif
    
  local_data = (local_data_t *) (self->model_data);
  g_hash_table_remove_all (local_data->requested_today);

#if DEBUG
  g_debug ("----- EXIT handle_new_day_event (%s)", MODEL_NAME);
#endif

  return;
}



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
 * Check whether unit 2 should be part of the vaccination ring.
 */
void
check_and_choose (int id, gpointer arg)
{
  callback_t *callback_data;
  UNT_unit_t *unit2;
  UNT_unit_t *unit1;
  local_data_t *local_data;
  double distance;

#if DEBUG
  g_debug ("----- ENTER check_and_choose (%s)", MODEL_NAME);
#endif

  callback_data = (callback_t *) arg;
  unit2 = UNT_unit_list_get (callback_data->units, id);

  /* Is unit 2 already destroyed? */
  if (unit2->state == Destroyed)
    goto end;

  local_data = callback_data->local_data;

  /* Is unit 2 a production type that gets vaccinated? */
  if (local_data->target_production_type[unit2->production_type] == FALSE)
    goto end;

  /* Avoid making the same request twice on a single day. */
  if (g_hash_table_lookup (local_data->requested_today, unit2) != NULL)
    goto end;

  unit1 = callback_data->unit1;
  distance = GIS_distance (unit1->x, unit1->y, unit2->x, unit2->y);

  if (local_data->supp_radius >= 0)
    {
      #if DEBUG
        g_debug ("unit %s within suppressive circle, ordering unit vaccinated", unit2->official_id);
      #endif
      EVT_event_enqueue (callback_data->queue,
                         EVT_new_request_for_vaccination_event (unit2,
                                                                unit1, /* unit at center of ring */
                                                                callback_data->day,
                                                                ADSM_ControlRing,
                                                                distance,
                                                                local_data->supp_radius,
                                                                local_data->prot_inner_radius,
                                                                local_data->prot_outer_radius));
      g_hash_table_insert (local_data->requested_today, unit2, unit2);  
    }
  else if (local_data->prot_inner_radius >= 0
           && distance >= local_data->prot_inner_radius - EPSILON
           && distance <= local_data->prot_outer_radius + EPSILON)
    {
      #if DEBUG
        g_debug ("unit %s within protective ring, ordering unit vaccinated", unit2->official_id);
      #endif
      EVT_event_enqueue (callback_data->queue,
                         EVT_new_request_for_vaccination_event (unit2,
                                                                unit1, /* unit at center of ring */
                                                                callback_data->day,
                                                                ADSM_ControlRing,
                                                                distance,
                                                                local_data->supp_radius,
                                                                local_data->prot_inner_radius,
                                                                local_data->prot_outer_radius));
      g_hash_table_insert (local_data->requested_today, unit2, unit2);
    }

end:
#if DEBUG
  g_debug ("----- EXIT check_and_choose (%s)", MODEL_NAME);
#endif
  return;
}



void
ring_vaccinate (struct adsm_module_t_ *self, UNT_unit_list_t * units, UNT_unit_t * unit,
                int day, EVT_event_queue_t * queue)
{
  local_data_t *local_data;
  callback_t callback_data;
  double max_radius;

#if DEBUG
  g_debug ("----- ENTER ring_vaccinate (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  callback_data.local_data = local_data;
  callback_data.units = units;
  callback_data.unit1 = unit;
  callback_data.day = day;
  callback_data.queue = queue;

  /* Find the distances to other units. */
  max_radius = MAX (local_data->supp_radius,
                    local_data->prot_outer_radius);
  spatial_search_circle_by_id (units->spatial_index, unit->index,
                               max_radius + EPSILON,
                               check_and_choose, &callback_data);

#if DEBUG
  g_debug ("----- EXIT ring_vaccinate (%s)", MODEL_NAME);
#endif
}



/**
 * Responds to a detection by ordering vaccination actions.
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
  
#if DEBUG
  g_debug ("----- ENTER handle_detection_event (%s)", MODEL_NAME);
#endif
    
  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;

  if (local_data->trigger_production_type[unit->production_type] == TRUE)
    ring_vaccinate (self, units, unit, event->day, queue);

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
    case EVT_NewDay:
      handle_new_day_event (self);
      break;
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
 * Returns a text representation of this model.
 *
 * @param self the model.
 * @return a string.
 */
char *
to_string (struct adsm_module_t_ *self)
{
  GString *s;
  local_data_t *local_data;
  unsigned int nprod_types, i;
  gboolean first;

  local_data = (local_data_t *) (self->model_data);
  s = g_string_new (NULL);
  g_string_printf (s, "<%s", MODEL_NAME);

  g_string_append_printf (s, " detection of");
  nprod_types = local_data->production_types->len;
  first = TRUE;
  for (i = 0; i < nprod_types; i++)
    {
      if (local_data->trigger_production_type[i] == TRUE)
        {
          g_string_append_printf(s, first ? " %s" : ",%s",
                                 (char *) g_ptr_array_index (local_data->production_types, i));
          first = FALSE;
        }
    }
  g_string_append_printf (s, " causes vaccination of");
  first = TRUE;
  for (i = 0; i < nprod_types; i++)
    {
      if (local_data->target_production_type[i] == TRUE)
        {
          g_string_append_printf(s, first ? " %s" : ",%s",
                                 (char *) g_ptr_array_index (local_data->production_types, i));
          first = FALSE;
        }
    }
  if (local_data->supp_radius > 0)
    g_string_append_printf (s, " within %g km suppressive circle",
                            local_data->supp_radius);
  if (local_data->prot_inner_radius > 0)
    g_string_append_printf (s, " within %g-%g km protective ring",
                            local_data->prot_inner_radius,
                            local_data->prot_outer_radius);
      
  g_string_append_c (s, '>');

  /* don't return the wrapper object */
  return g_string_free (s, /* free_segment = */ FALSE);
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

  local_data = (local_data_t *) (self->model_data);

  g_free (local_data->trigger_production_type);
  g_free (local_data->target_production_type);
  g_hash_table_destroy (local_data->requested_today);
  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * A type to hold arguments to set_prodtype().
 */
typedef struct
{
  gboolean *flags;
  GPtrArray *production_types;
}
set_prodtype_args_t;



static int
set_prodtype (void *data, GHashTable *dict)
{
  set_prodtype_args_t *args;
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
 * Adds a set of parameters to a ring vaccination model.
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
  double outer_radius;
  char *tmp_text;
  guint nprod_types;
  guint ring_rule_id;
  set_prodtype_args_t args;
  gchar *sql;
  char *sqlerr;

#if DEBUG
  g_debug ("----- ENTER set_params (%s)", MODEL_NAME);
#endif

  g_assert (g_hash_table_size (dict) == 3);

  self = (adsm_module_t *)data;
  local_data = (local_data_t *) (self->model_data);
  params = local_data->db;

  /* If there is just an outer radius, this is a suppressive circle, otherwise
   * this is a protective ring. */
  outer_radius = strtod(g_hash_table_lookup (dict, "outer_radius"), NULL);
  /* Radius must be positive. */
  if (outer_radius < 0)
    {
      g_warning ("%s: radius cannot be negative, setting to 0", MODEL_NAME);
      outer_radius = 0;
    }

  tmp_text = g_hash_table_lookup (dict, "inner_radius");
  if (tmp_text == NULL)
    {
      /* Suppressive circle */
      local_data->supp_radius = outer_radius;
      local_data->prot_inner_radius = local_data->prot_outer_radius = -1;
    }
  else
    {
      /* Protective ring */
      local_data->prot_outer_radius = outer_radius;
      local_data->prot_inner_radius = strtod(tmp_text, NULL);
      local_data->supp_radius = -1;
    }

  /* Fill in the production types that trigger this ring rule. */
  nprod_types = local_data->production_types->len;
  local_data->trigger_production_type = g_new0(gboolean, nprod_types);
  ring_rule_id = strtol(g_hash_table_lookup (dict, "id"), NULL, /* base */ 10);
  sql = g_strdup_printf ("SELECT prodtype.name AS prodtype "
                         "FROM ScenarioCreator_productiontype prodtype,ScenarioCreator_vaccinationringrule_trigger_group grp "
                         "WHERE grp.vaccinationringrule_id=%u "
                         "AND prodtype.id=grp.productiontype_id",
                         ring_rule_id);
  args.flags = local_data->trigger_production_type;
  args.production_types = local_data->production_types;
  sqlite3_exec_dict (params, sql,
                     set_prodtype, &args, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }
  g_free (sql);

  /* Fill in the production types that get vaccinated by this ring rule. */
  local_data->target_production_type = g_new0(gboolean, nprod_types);
  sql = g_strdup_printf ("SELECT prodtype.name AS prodtype "
                         "FROM ScenarioCreator_productiontype prodtype,ScenarioCreator_vaccinationringrule_target_group grp "
                         "WHERE grp.vaccinationringrule_id=%u "
                         "AND prodtype.id=grp.productiontype_id",
                         ring_rule_id);
  args.flags = local_data->target_production_type;
  sqlite3_exec_dict (params, sql,
                     set_prodtype, &args, &sqlerr);
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
 * Returns a new ring vaccination model.
 */
adsm_module_t *
new (sqlite3 * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones, gpointer user_data, GError **error)
{
  adsm_module_t *self;
  local_data_t *local_data;
  EVT_event_type_t events_listened_for[] = {
    EVT_NewDay,
    EVT_Detection,
    0
  };
  guint ring_rule_id;
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

  /* Initialize a list of units for avoiding making two requests for the same
   * unit on the same day. */
  local_data->requested_today = g_hash_table_new (g_direct_hash, g_direct_equal);

  /* Call the set_params function to read ring rule's details. */
  ring_rule_id = GPOINTER_TO_UINT(user_data);
  local_data->ring_rule_id = ring_rule_id;
  sql = g_strdup_printf ("SELECT id,inner_radius,outer_radius "
                         "FROM ScenarioCreator_vaccinationringrule "
                         "WHERE id=%u", ring_rule_id);
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
 * A type to hold arguments to create_ring_rule().
 */
typedef struct
{
  sqlite3 *params;
  UNT_unit_list_t *units;
  projPJ projection;
  ZON_zone_list_t * zones;
  GError **error;
  GSList *ring_rules;  
}
create_ring_rule_args_t;



/**
 * The function receives a ring rule ID and calls "new" to instantiate that
 * ring rule.
 */
static int
create_ring_rule (void *data, GHashTable *dict)
{
  create_ring_rule_args_t *args;
  guint ring_rule_id;
  adsm_module_t *module;

  args = data;
  
  /* We receive the ring rule ID as a name (string). */
  ring_rule_id = strtol(g_hash_table_lookup (dict, "id"), NULL, /* base */ 10);
  #if DEBUG
    g_debug ("creating ring rule with ID %u", ring_rule_id);
  #endif

  /* Call the "new" function to instantiate a module for the ring rule with
   * that ID. */
  module =
    ring_vaccination_model_new (args->params, args->units,
      args->projection, args->zones, GUINT_TO_POINTER(ring_rule_id), args->error);

  /* Add the new module to the list returned by the factory. */
  args->ring_rules = g_slist_prepend (args->ring_rules, module);

  return 0;
}



/**
 * Returns one or more new ring vaccination rules.
 */
GSList *
factory (sqlite3 * params, UNT_unit_list_t * units, projPJ projection,
         ZON_zone_list_t * zones, GError **error)
{
  GSList *modules;
  create_ring_rule_args_t args;
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
  args.ring_rules = NULL;
  sqlite3_exec_dict (params,
                     "SELECT id FROM ScenarioCreator_vaccinationringrule",
                     create_ring_rule, &args, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }
  modules = args.ring_rules;

  #if DEBUG
    g_debug ("----- EXIT factory (%s)", MODEL_NAME);
  #endif

  return modules;
}

/* end of file ring_vaccination_model.c */
