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
  double supp_radius; /**< Radius of suppressive ring. -1 if no suppressive
    ring is defined. */
  double prot_inner_radius; /**< Inner radius of protective ring. -1 if no
    protective ring is defined. */
  double prot_outer_radius; /**< Outer radius of protective ring. -1 if no
    protective ring is defined. */
}
param_block_t;



typedef struct
{
  GPtrArray *production_types; /**< Production type names. Each item in the
    array is a (char *). */
  param_block_t ***param_block; /**< Blocks of parameters.
    Use an expression of the form
    param_block[from_production_type][to_production_type]
    to get a pointer to a particular param_block. */
  double *max_supp_radius; /**< One value for each production type, giving the
    largest suppressive vaccination circle that can be triggered by a unit of
    that production type. Useful for doing outside-in vaccination order.
    max_supp_radius is initialized to -1, an invalid value, and will stay -1
    if no suppressive vaccination circles are defined. */
  double *min_prot_inner_radius; /**< One value for each production type,
    giving the smallest inner radius of any protective vaccination ring that can
    be triggered by a unit of that production type. Useful for doing inside-out
    vaccination ourder. min_prot_inner_radius is initialized to -1, an invalid
    value, and will stay -1 if no protective vaccination rings are defined. */
  double *max_prot_outer_radius; /**< One value for each production type,
    giving the largest outer radius of any protective vaccination ring that can
    be triggered by a unit of that production type. Useful for doing outside-in
    vaccination order. max_prot_outer_radius is initialized to -1, an invalid
    value, and will stay -1 if no protective vaccination rings are defined. */
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
  param_block_t *param_block;
  gboolean earlier_request_exists;
  gboolean earlier_request_was_suppressive;
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
  unit1 = callback_data->unit1;
  param_block = local_data->param_block[unit1->production_type][unit2->production_type];
  if (param_block == NULL)
    goto end;

  /* Avoid making the same request twice on a single day. Exception: allow a
   * second request if the new one is a suppressive circle and no previous
   * vaccination requests for this unit were suppressive circles. This
   * exception is made because being part of a suppressive circle is sort of an
   * "upgrade" in status: it means the unit cannot have its vaccination
   * canceled by the hole-punching effect of protective rings. */
  earlier_request_exists = g_hash_table_contains (local_data->requested_today, unit2);
  earlier_request_was_suppressive = (earlier_request_exists &&
    (gboolean) GPOINTER_TO_INT (g_hash_table_lookup (local_data->requested_today, unit2)));  
  if (earlier_request_was_suppressive)
    goto end;

  /* The spatial search returns all the units within the largest possible
   * vaccination ring around a unit of unit1's production type. However, the
   * settings for which units of unit2's production type get vaccinated may be
   * more restrictive. */
  distance = GIS_distance (unit1->x, unit1->y, unit2->x, unit2->y);

  /* Check distance against the suppressive circle radius.  If suppressive
   * vaccination is not in effect, supp_radius will be -1 and the check
   * distance < supp_radius will fail. */
  if (distance <= param_block->supp_radius + EPSILON)
    {
      #if DEBUG
        g_debug ("unit %s within suppressive circle, ordering unit vaccinated", unit2->official_id);
      #endif
      EVT_event_enqueue (callback_data->queue,
                         EVT_new_request_for_vaccination_event (unit2,
                                                                unit1, /* unit at center of ring */
                                                                callback_data->day,
                                                                ADSM_ControlSuppressiveRing,
                                                                distance,
                                                                local_data->max_supp_radius[unit1->production_type],
                                                                local_data->min_prot_inner_radius[unit1->production_type],
                                                                local_data->max_prot_outer_radius[unit1->production_type]));
      g_hash_table_insert (local_data->requested_today, unit2, GINT_TO_POINTER(TRUE));  
    }
  else if (param_block->prot_inner_radius >= 0
           && distance >= param_block->prot_inner_radius - EPSILON
           && distance <= param_block->prot_outer_radius + EPSILON)
    {
      #if DEBUG
        g_debug ("unit %s within protective ring, ordering unit vaccinated", unit2->official_id);
      #endif
      /* If we reached this place in the code, then there were no earlier
       * requests on this day to vaccinate unit2, OR all of the earlier
       * requests were for protective rings. If there were earlier requests for
       * protective rings, then we do not need to issue another
       * RequestForVaccination. */
      if (earlier_request_exists == FALSE)
        {
          EVT_event_enqueue (callback_data->queue,
                             EVT_new_request_for_vaccination_event (unit2,
                                                                    unit1, /* unit at center of ring */
                                                                    callback_data->day,
                                                                    ADSM_ControlProtectiveRing,
                                                                    distance,
                                                                    local_data->max_supp_radius[unit1->production_type],
                                                                    local_data->min_prot_inner_radius[unit1->production_type],
                                                                    local_data->max_prot_outer_radius[unit1->production_type]));
          g_hash_table_insert (local_data->requested_today, unit2, GINT_TO_POINTER(FALSE));
        }
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
  max_radius = MAX (local_data->max_supp_radius[unit->production_type],
                    local_data->max_prot_outer_radius[unit->production_type]);
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

  if (local_data->param_block[unit->production_type] != NULL)
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
  unsigned int nprod_types, i, j;
  param_block_t *param_block;

  local_data = (local_data_t *) (self->model_data);
  s = g_string_new (NULL);
  g_string_printf (s, "<%s", MODEL_NAME);

  /* Add the parameter block for each to-from combination of production
   * types, and show the max and min radius for each from-production-type. */
  nprod_types = local_data->production_types->len;
  for (i = 0; i < nprod_types; i++)
    {
      char *from_prodtype;
      if (local_data->param_block[i] == NULL)
        continue;

      from_prodtype = (char *) g_ptr_array_index (local_data->production_types, i);
      g_string_append_printf (s, "\n  for %s", from_prodtype);
      g_string_append_printf (s, "\n    size limits=%g (supp),%g-%g (prot)",
                              local_data->max_supp_radius[i],
                              local_data->min_prot_inner_radius[i],
                              local_data->max_prot_outer_radius[i]);

      for (j = 0; j < nprod_types; j++)
        {
          if (local_data->param_block[i][j] == NULL)
            continue;

          param_block = local_data->param_block[i][j];
          g_string_append_printf (s, "\n    for %s -> %s",
                                  from_prodtype,
                                  (char *) g_ptr_array_index (local_data->production_types, j));
          if (param_block->supp_radius > 0)
            g_string_append_printf (s, "\n      suppressive radius=%g",
                                    param_block->supp_radius);
          if (param_block->prot_inner_radius > 0)
            g_string_append_printf (s, "\n      protective radius=%g-%g",
                                    param_block->prot_inner_radius,
                                    param_block->prot_outer_radius);
        } /* end of loop over to-production-types */
    } /* end of loop over from-production-types */
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
  unsigned int nprod_types, i, j;

#if DEBUG
  g_debug ("----- ENTER free (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* Free each of the parameter blocks. */
  nprod_types = local_data->production_types->len;
  for (i = 0; i < nprod_types; i++)
    if (local_data->param_block[i] != NULL)
      {
        for (j = 0; j < nprod_types; j++)
          g_free (local_data->param_block[i][j]); /* g_free is safe on NULLs */
        /* Free this row of the 2D array. */
        g_free (local_data->param_block[i]);
      }
  /* Free the array of pointers to rows. */
  g_free (local_data->param_block);

  g_free (local_data->max_supp_radius);
  g_free (local_data->min_prot_inner_radius);
  g_free (local_data->max_prot_outer_radius);
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
  guint ring_rule_id;
  char *tmp_text;
  gboolean is_suppressive;
  double supp_radius, prot_outer_radius, prot_inner_radius;
  gboolean *trigger_production_type, *target_production_type;
  guint nprod_types, i, j;
  set_prodtype_args_t args;
  gchar *sql;
  char *sqlerr;
  param_block_t *param_block;

#if DEBUG
  g_debug ("----- ENTER set_params (%s)", MODEL_NAME);
#endif

  g_assert (g_hash_table_size (dict) == 3);

  self = (adsm_module_t *)data;
  local_data = (local_data_t *) (self->model_data);
  params = local_data->db;

  ring_rule_id = strtol(g_hash_table_lookup (dict, "id"), NULL, /* base */ 10);
  #if DEBUG
    g_debug ("creating ring rule with ID %u", ring_rule_id);
  #endif

  /* If there is just an outer radius, this is a suppressive circle, otherwise
   * this is a protective ring. */
  tmp_text = g_hash_table_lookup (dict, "inner_radius");
  if (tmp_text == NULL)
    {
      /* Suppressive circle */
      is_suppressive = TRUE;
      supp_radius = strtod(g_hash_table_lookup (dict, "outer_radius"), NULL);
      prot_inner_radius = prot_outer_radius = -1;
    }
  else
    {
      /* Protective ring */
      is_suppressive = FALSE;
      prot_outer_radius = strtod(g_hash_table_lookup (dict, "outer_radius"), NULL);
      prot_inner_radius = strtod(tmp_text, NULL);
      supp_radius = -1;
    }

  /* Fill in the production types that trigger this ring rule. */
  nprod_types = local_data->production_types->len;
  trigger_production_type = g_new0(gboolean, nprod_types);
  sql = g_strdup_printf ("SELECT prodtype.name AS prodtype "
                         "FROM ScenarioCreator_productiontype prodtype,ScenarioCreator_vaccinationringrule_trigger_group grp "
                         "WHERE grp.vaccinationringrule_id=%u "
                         "AND prodtype.id=grp.productiontype_id",
                         ring_rule_id);
  args.flags = trigger_production_type;
  args.production_types = local_data->production_types;
  sqlite3_exec_dict (params, sql,
                     set_prodtype, &args, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }
  g_free (sql);

  /* Fill in the production types that get vaccinated by this ring rule. */
  target_production_type = g_new0(gboolean, nprod_types);
  sql = g_strdup_printf ("SELECT prodtype.name AS prodtype "
                         "FROM ScenarioCreator_productiontype prodtype,ScenarioCreator_vaccinationringrule_target_group grp "
                         "WHERE grp.vaccinationringrule_id=%u "
                         "AND prodtype.id=grp.productiontype_id",
                         ring_rule_id);
  args.flags = target_production_type;
  sqlite3_exec_dict (params, sql,
                     set_prodtype, &args, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }
  g_free (sql);

  nprod_types = local_data->production_types->len;
  for (i = 0; i < nprod_types; i++)
    if (trigger_production_type[i] == TRUE)
      {
        /* If necessary, create a row in the 2D array for this trigger
         * production type. */
        if (local_data->param_block[i] == NULL)
          local_data->param_block[i] = g_new0 (param_block_t *, nprod_types);

        for (j = 0; j < nprod_types; j++)
          if (target_production_type[j] == TRUE)
            {
              /* Create a parameter block for this to-from production type
               * combination, or overwrite the existing one. */
              param_block = local_data->param_block[i][j];
              if (param_block == NULL)
                {
                  param_block = g_new (param_block_t, 1);
                  local_data->param_block[i][j] = param_block;
                  #if DEBUG
                    g_debug ("setting parameters for %s -> %s",
                             (char *) g_ptr_array_index (local_data->production_types, i),
                             (char *) g_ptr_array_index (local_data->production_types, j));
                  #endif
                  param_block->supp_radius = supp_radius;
                  param_block->prot_inner_radius = prot_inner_radius;
                  param_block->prot_outer_radius = prot_outer_radius;
                }
              else
                {
                  /* It's OK if one ring rule provides the suppressive circle
                   * parameters and another provides the protective ring
                   * parameters.  But warn if there is any overwriting. */
                  if (is_suppressive)
                    {
                      if (param_block->supp_radius >= 0
                          && param_block->supp_radius != supp_radius)
                        {
                          g_warning ("Both %g and %g given as suppressive circle radius for vaccination of %s units around detected %s units. Using the larger value.",
                                     param_block->supp_radius, supp_radius,
                                     (char *) g_ptr_array_index (local_data->production_types, j),
                                     (char *) g_ptr_array_index (local_data->production_types, i));
                          param_block->supp_radius = MAX(param_block->supp_radius, supp_radius);
                        }
                      else
                        param_block->supp_radius = supp_radius;
                    }
                  else
                    {
                      if (param_block->prot_inner_radius >= 0
                          && (param_block->prot_inner_radius != prot_inner_radius
                              || param_block->prot_outer_radius != prot_outer_radius))
                        {
                          g_warning ("Both %g-%g and %g-%g given as protective ring radius for vaccination of %s units around detected %s units. Using the widest ring.",
                                     param_block->prot_inner_radius, param_block->prot_outer_radius,
                                     prot_inner_radius, prot_outer_radius,
                                     (char *) g_ptr_array_index (local_data->production_types, j),
                                     (char *) g_ptr_array_index (local_data->production_types, i));
                          param_block->prot_inner_radius = MIN(param_block->prot_inner_radius, prot_inner_radius);
                          param_block->prot_outer_radius = MAX(param_block->prot_outer_radius, prot_outer_radius);
                        }
                      else
                        {
                          param_block->prot_inner_radius = prot_inner_radius;
                          param_block->prot_outer_radius = prot_outer_radius;
                        }
                    }
                }

              /* Keep track of the size limits of the suppressive circles and
               * protective rings for each production type. */
              if (is_suppressive)
                {
                  if (param_block->supp_radius > local_data->max_supp_radius[i])
                    local_data->max_supp_radius[i] = param_block->supp_radius;
                }
              else
                {
                  if (param_block->prot_outer_radius > local_data->max_prot_outer_radius[i])
                    local_data->max_prot_outer_radius[i] = param_block->prot_outer_radius;

                  if ((param_block->prot_inner_radius != 0)
                      && (local_data->min_prot_inner_radius[i] < 0 /* min value not yet initialized */
                          || (param_block->prot_inner_radius < local_data->min_prot_inner_radius[i])))
                    local_data->min_prot_inner_radius[i] = param_block->prot_inner_radius;
                }
            }
      }

  g_free (trigger_production_type);
  g_free (target_production_type);

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
     ZON_zone_list_t * zones, GError **error)
{
  adsm_module_t *self;
  local_data_t *local_data;
  EVT_event_type_t events_listened_for[] = {
    EVT_NewDay,
    EVT_Detection,
    0
  };
  guint nprod_types, i;
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

  /* local_data->param_block is a 2D array of parameter blocks, each block
   * holding the parameters for one to-from combination of production types.
   * Initially, all row pointers are NULL.  Rows will be created as needed in
   * the set_params function. */
  local_data->production_types = units->production_type_names;
  nprod_types = local_data->production_types->len;
  local_data->param_block = g_new0 (param_block_t **, nprod_types);

  /* Initialize a list of units for avoiding making two requests for the same
   * unit on the same day. */
  local_data->requested_today = g_hash_table_new (g_direct_hash, g_direct_equal);

  /* Initialize arrays to hold the size limits of the suppressive circles and
   * protective rings that can be triggered around each production type. */
  local_data->max_supp_radius = g_new (double, nprod_types);
  local_data->min_prot_inner_radius = g_new (double, nprod_types);
  local_data->max_prot_outer_radius = g_new (double, nprod_types);
  /* Initialize to invalid negative values. */
  for (i = 0; i < nprod_types; i++)
    {
      local_data->max_supp_radius[i] = -1;
      local_data->min_prot_inner_radius[i] = -1;
      local_data->max_prot_outer_radius[i] = -1;
    }

  /* Call the set_params function to read ring rules' details. */
  sql = "SELECT id,inner_radius,outer_radius FROM ScenarioCreator_vaccinationringrule";
  local_data->db = params;
  sqlite3_exec_dict (params, sql, set_params, self, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }
  local_data->db = NULL;

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file ring_vaccination_model.c */
