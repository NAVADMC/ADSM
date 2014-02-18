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
#  include <config.h>
#endif

/* To avoid name clashes when multiple modules have the same interface. */
#define is_singleton ring_vaccination_model_is_singleton
#define new ring_vaccination_model_new
#define set_params ring_vaccination_model_set_params
#define run ring_vaccination_model_run
#define reset ring_vaccination_model_reset
#define events_listened_for ring_vaccination_model_events_listened_for
#define is_listening_for ring_vaccination_model_is_listening_for
#define has_pending_actions ring_vaccination_model_has_pending_actions
#define has_pending_infections ring_vaccination_model_has_pending_infections
#define to_string ring_vaccination_model_to_string
#define local_printf ring_vaccination_model_printf
#define local_fprintf ring_vaccination_model_fprintf
#define local_free ring_vaccination_model_free
#define handle_before_any_simulations_event ring_vaccination_model_handle_before_any_simulations_event
#define handle_new_day_event ring_vaccination_model_handle_new_day_event
#define handle_detection_event ring_vaccination_model_handle_detection_event
#define check_and_choose ring_vaccination_model_check_and_choose

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

#include "ring_vaccination_model.h"

#if !HAVE_ROUND && HAVE_RINT
#  define round rint
#endif

/* Temporary fix -- "round" and "rint" are in the math library on Red Hat 7.3,
 * but they're #defined so AC_CHECK_FUNCS doesn't find them. */
double round (double x);

/** This must match an element name in the DTD. */
#define MODEL_NAME "ring-vaccination-model"



#define NEVENTS_LISTENED_FOR 3
EVT_event_type_t events_listened_for[] = { EVT_BeforeAnySimulations, EVT_NewDay, EVT_Detection };



#define EPSILON 0.01 /* 10 m */



/** Specialized information for this model. */
typedef struct
{
  int priority;
  unsigned int min_time_between_vaccinations; /**< The minimum number of days
    until a unit may be revaccinated. */
  double radius;
  gboolean vaccinate_detected_units_defined; /**< Whether the parameters
    explicitly define vaccinate-detected-units.  Needed for backwards
    compatibility. */
  gboolean vaccinate_detected_units;
}
param_block_t;



typedef struct
{
  GPtrArray *production_types;
  param_block_t ***param_block; /**< Blocks of parameters.
    Use an expression of the form
    param_block[from_production_type][to_production_type]
    to get a pointer to a particular param_block. */
  double *max_radius; /**< One value for each production type, giving the
    largest vaccination ring that can be triggered by a unit of that production
    type. */
  GHashTable *detected_units; /**< A list of detected units.  The pointer to
    the UNT_unit_t structure is the key. */
  GHashTable *requested_today; /**< A list of units for which this module made
    requests for vaccination today.  A unit can be in queue for vaccination
    more than once at a given time, but two requests for the same unit, for the
    same reason, on the same day will have identical priority and would be
    redundant. */      
}
local_data_t;



/**
 * Before any simulations, this module declares all the reasons for which it
 * may request a vaccination.
 *
 * @param queue for any new events the model creates.
 */
void
handle_before_any_simulations_event (EVT_event_queue_t * queue)
{
  GPtrArray *reasons;
  
#if DEBUG
  g_debug ("----- ENTER handle_before_any_simulations_event (%s)", MODEL_NAME);
#endif

  reasons = g_ptr_array_sized_new (1);
  g_ptr_array_add (reasons, "Ring");
  EVT_event_enqueue (queue, EVT_new_declaration_of_vaccination_reasons_event (reasons));

  /* Note that we don't clean up the GPtrArray.  It will be freed along with
   * the declaration event after all interested sub-models have processed the
   * event. */

#if DEBUG
  g_debug ("----- EXIT handle_before_any_simulations_event (%s)", MODEL_NAME);
#endif

  return;
}



/**
 * On each new day, this module clears its list of units for which it has
 * requested vaccinations.
 *
 * @param self this module.
 */
void
handle_new_day_event (struct spreadmodel_model_t_ *self)
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

#if DEBUG
  g_debug ("----- ENTER check_and_choose (%s)", MODEL_NAME);
#endif

  callback_data = (callback_t *) arg;
  unit2 = UNT_unit_list_get (callback_data->units, id);

  /* Is unit 2 already destroyed? */
  if (unit2->state == Destroyed)
    goto end;

  local_data = callback_data->local_data;
  unit1 = callback_data->unit1;

  /* Is unit 2 a production type we're interested in? */
  param_block = local_data->param_block[unit1->production_type][unit2->production_type];
  if (param_block == NULL)
    goto end;

  /* Are unit 1 and unit 2 the same? */
  if (unit1 == unit2 && param_block->vaccinate_detected_units_defined == FALSE)
    goto end;

  /* Do we want to exclude units that are known to be infected? */
  if (param_block->vaccinate_detected_units == FALSE)
    {
      /* We know unit2 is infected if it's the one that triggered this
       * vaccination ring, or if it has been detected. */
      if (unit1 == unit2
          || g_hash_table_lookup (local_data->detected_units, unit2) != NULL)
        goto end;
    }

  /* Avoid making the same request twice on a single day. */
  if (g_hash_table_lookup (local_data->requested_today, unit2) != NULL)
    goto end;

#if DEBUG
  g_debug ("unit %s within radius, ordering unit vaccinated", unit2->official_id);
#endif
  EVT_event_enqueue (callback_data->queue,
                     EVT_new_request_for_vaccination_event (unit2,
                                                            callback_data->day,
                                                            "Ring",
                                                            param_block->priority,
                                                            param_block->vaccinate_detected_units_defined && !(param_block->vaccinate_detected_units),
                                                            param_block->min_time_between_vaccinations));
  g_hash_table_insert (local_data->requested_today, unit2, unit2);

end:
#if DEBUG
  g_debug ("----- EXIT check_and_choose (%s)", MODEL_NAME);
#endif
  return;
}



void
ring_vaccinate (struct spreadmodel_model_t_ *self, UNT_unit_list_t * units, UNT_unit_t * unit,
                int day, EVT_event_queue_t * queue)
{
  local_data_t *local_data;
  callback_t callback_data;

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
  spatial_search_circle_by_id (units->spatial_index, unit->index,
                               local_data->max_radius[unit->production_type] + EPSILON,
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
handle_detection_event (struct spreadmodel_model_t_ *self, UNT_unit_list_t * units,
                        EVT_detection_event_t * event, EVT_event_queue_t * queue)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  
#if DEBUG
  g_debug ("----- ENTER handle_detection_event (%s)", MODEL_NAME);
#endif
    
  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;
  g_hash_table_insert (local_data->detected_units, (gpointer)unit, (gpointer)unit);

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
run (struct spreadmodel_model_t_ *self, UNT_unit_list_t * units, ZON_zone_list_t * zones,
     EVT_event_t * event, RAN_gen_t * rng, EVT_event_queue_t * queue)
{
#if DEBUG
  g_debug ("----- ENTER run (%s)", MODEL_NAME);
#endif

  switch (event->type)
    {
    case EVT_BeforeAnySimulations:
      handle_before_any_simulations_event (queue);
      break;
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
 * Resets this model after a simulation run.
 *
 * @param self the model.
 */
void
reset (struct spreadmodel_model_t_ *self)
{
  local_data_t *local_data;

#if DEBUG
  g_debug ("----- ENTER reset (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  g_hash_table_remove_all (local_data->detected_units);

#if DEBUG
  g_debug ("----- EXIT reset (%s)", MODEL_NAME);
#endif
}



/**
 * Reports whether this model is listening for a given event type.
 *
 * @param self the model.
 * @param event_type an event type.
 * @return TRUE if the model is listening for the event type.
 */
gboolean
is_listening_for (struct spreadmodel_model_t_ *self, EVT_event_type_t event_type)
{
  int i;

  for (i = 0; i < self->nevents_listened_for; i++)
    if (self->events_listened_for[i] == event_type)
      return TRUE;
  return FALSE;
}



/**
 * Reports whether this model has any pending actions to carry out.
 *
 * @param self the model.
 * @return TRUE if the model has pending actions.
 */
gboolean
has_pending_actions (struct spreadmodel_model_t_ * self)
{
  return FALSE;
}



/**
 * Reports whether this model has any pending infections to cause.
 *
 * @param self the model.
 * @return TRUE if the model has pending infections.
 */
gboolean
has_pending_infections (struct spreadmodel_model_t_ * self)
{
  return FALSE;
}



/**
 * Returns a text representation of this model.
 *
 * @param self the model.
 * @return a string.
 */
char *
to_string (struct spreadmodel_model_t_ *self)
{
  GString *s;
  local_data_t *local_data;
  unsigned int nprod_types, i, j;
  param_block_t *param_block;
  char *chararray;

  local_data = (local_data_t *) (self->model_data);
  s = g_string_new (NULL);
  g_string_printf (s, "<%s", MODEL_NAME);

  /* Add the parameter block for each to-from combination of production
   * types. */
  nprod_types = local_data->production_types->len;
  for (i = 0; i < nprod_types; i++)
    if (local_data->param_block[i] != NULL)
      for (j = 0; j < nprod_types; j++)
        if (local_data->param_block[i][j] != NULL)
          {
            param_block = local_data->param_block[i][j];
            g_string_append_printf (s, "\n  for %s -> %s",
                                    (char *) g_ptr_array_index (local_data->production_types, i),
                                    (char *) g_ptr_array_index (local_data->production_types, j));
            g_string_append_printf (s, "\n    priority=%i", param_block->priority);
            g_string_append_printf (s, "\n    radius=%g", param_block->radius);
            g_string_append_printf (s, "\n    min-time-between-vaccinations=%u",
                                    param_block->min_time_between_vaccinations);
          }
  g_string_append_c (s, '>');

  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Prints this model to a stream.
 *
 * @param stream a stream to write to.
 * @param self the model.
 * @return the number of characters printed (not including the trailing '\\0').
 */
int
local_fprintf (FILE * stream, struct spreadmodel_model_t_ *self)
{
  char *s;
  int nchars_written;

  s = to_string (self);
  nchars_written = fprintf (stream, "%s", s);
  free (s);
  return nchars_written;
}



/**
 * Prints this model.
 *
 * @param self the model.
 * @return the number of characters printed (not including the trailing '\\0').
 */
int
local_printf (struct spreadmodel_model_t_ *self)
{
  return local_fprintf (stdout, self);
}



/**
 * Frees this model.  Does not free the production type names.
 *
 * @param self the model.
 */
void
local_free (struct spreadmodel_model_t_ *self)
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
          g_free (local_data->param_block[i][j]);
        /* Free this row of the 2D array. */
        g_free (local_data->param_block[i]);
      }
  /* Free the array of pointers to rows. */
  g_free (local_data->param_block);

  g_free (local_data->max_radius);
  g_hash_table_destroy (local_data->detected_units);
  g_hash_table_destroy (local_data->requested_today);
  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Returns whether this model is a singleton or not.
 */
gboolean
is_singleton (void)
{
  return TRUE;
}



/**
 * Adds a set of parameters to a ring vaccination model.
 */
void
set_params (struct spreadmodel_model_t_ *self, PAR_parameter_t * params)
{
  local_data_t *local_data;
  gboolean *from_production_type, *to_production_type;
  unsigned int nprod_types, i, j;
  param_block_t *param_block;
  scew_element const *e;
  scew_attribute *attr;
  gboolean success;

#if DEBUG
  g_debug ("----- ENTER set_params (%s)", MODEL_NAME);
#endif

  /* Make sure the right XML subtree was sent. */
  g_assert (strcmp (scew_element_name (params), MODEL_NAME) == 0);

  local_data = (local_data_t *) (self->model_data);

  /* Find out which to-from production type combinations these parameters apply
   * to. */
  from_production_type =
    spreadmodel_read_prodtype_attribute (params, "from-production-type", local_data->production_types);
  /* Temporary support for older parameter files that only had a
   * "production-type" attribute and implied "from-any" functionality. */
  attr = scew_attribute_by_name (params, "production-type");
  if (attr != NULL)
    to_production_type =
      spreadmodel_read_prodtype_attribute (params, "production-type", local_data->production_types);
  else
    to_production_type =
      spreadmodel_read_prodtype_attribute (params, "to-production-type", local_data->production_types);

  nprod_types = local_data->production_types->len;
  for (i = 0; i < nprod_types; i++)
    if (from_production_type[i] == TRUE)
      for (j = 0; j < nprod_types; j++)
        if (to_production_type[j] == TRUE)
          {
            /* If necessary, create a row in the 2D array for this from-
             * production type. */
            if (local_data->param_block[i] == NULL)
              local_data->param_block[i] = g_new0 (param_block_t *, nprod_types);

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
              }
            else
              {
                g_warning ("overwriting previous parameters for %s -> %s",
                           (char *) g_ptr_array_index (local_data->production_types, i),
                           (char *) g_ptr_array_index (local_data->production_types, j));
              }

            e = scew_element_by_name (params, "priority");
            if (e != NULL)
              {
                param_block->priority = (int) round (PAR_get_unitless (e, &success));
                if (success == FALSE)
                  {
                    g_warning ("%s: setting priority to 1", MODEL_NAME);
                    param_block->priority = 1;
                  }
                if (param_block->priority < 1)
                  {
                    g_warning ("%s: priority cannot be less than 1, setting to 1", MODEL_NAME);
                    param_block->priority = 1;
                  }
              }
            else
              {
                g_warning ("%s: priority missing, setting to 1", MODEL_NAME);
                param_block->priority = 1;
              }

		    e = scew_element_by_name (params, "radius");
		    if (e != NULL)
		      {
		        param_block->radius = PAR_get_length (e, &success);
		        if (success == FALSE)
		          {
		            g_warning ("%s: setting radius to 0", MODEL_NAME);
		            param_block->radius = 0;
		          }
		        /* Radius must be positive. */
		        if (param_block->radius < 0)
		          {
		            g_warning ("%s: radius cannot be negative, setting to 0", MODEL_NAME);
		            param_block->radius = 0;
		          }
		      }
		    else
		      {
		        g_warning ("%s: radius missing, setting to 0", MODEL_NAME);
		        param_block->radius = 0;
		      }

		    e = scew_element_by_name (params, "min-time-between-vaccinations");
		    if (e != NULL)
		      {
		        param_block->min_time_between_vaccinations = (int) (PAR_get_time (e, &success));
		        if (success == FALSE)
		          {
		            g_warning ("%s: setting minimum time between vaccinations to 31 days", MODEL_NAME);
		            param_block->min_time_between_vaccinations = 31;
		          }
		      }
		    else
		      {
		        g_warning ("%s: minimum time between vaccinations parameter missing, setting to 31 days",
		                   MODEL_NAME);
		        param_block->min_time_between_vaccinations = 31;
		      }

		    e = scew_element_by_name (params, "vaccinate-detected-units");
		    if (e != NULL)
		      {
		        param_block->vaccinate_detected_units_defined = TRUE;
		        param_block->vaccinate_detected_units = PAR_get_boolean (e, &success);
		        if (success == FALSE)
		          {
		            param_block->vaccinate_detected_units = TRUE; /* default */
		          }
		      }
		    else
		      {
		        param_block->vaccinate_detected_units_defined = FALSE;
		        param_block->vaccinate_detected_units = TRUE; /* default */
		      }

            /* Keep track of the maximum distance of spread from each
             * production type.  This determines whether we will use the R-tree
             * index when looking for units to spread infection to. */
            if (param_block->radius > local_data->max_radius[i])
              local_data->max_radius[i] = param_block->radius;
          }

  g_free (from_production_type);
  g_free (to_production_type);

#if DEBUG
  g_debug ("----- EXIT set_params (%s)", MODEL_NAME);
#endif

  return;
}



/**
 * Returns a new ring vaccination model.
 */
spreadmodel_model_t *
new (scew_element * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  spreadmodel_model_t *self;
  local_data_t *local_data;
  unsigned int nprod_types;

#if DEBUG
  g_debug ("----- ENTER new (%s)", MODEL_NAME);
#endif

  self = g_new (spreadmodel_model_t, 1);
  local_data = g_new (local_data_t, 1);

  self->name = MODEL_NAME;
  self->events_listened_for = events_listened_for;
  self->nevents_listened_for = NEVENTS_LISTENED_FOR;
  self->outputs = g_ptr_array_new ();
  self->model_data = local_data;
  self->set_params = set_params;
  self->run = run;
  self->reset = reset;
  self->is_listening_for = is_listening_for;
  self->has_pending_actions = has_pending_actions;
  self->has_pending_infections = has_pending_infections;
  self->to_string = to_string;
  self->printf = local_printf;
  self->fprintf = local_fprintf;
  self->free = local_free;

  /* local_data->param_block is a 2D array of parameter blocks, each block
   * holding the parameters for one to-from combination of production types.
   * Initially, all row pointers are NULL.  Rows will be created as needed in
   * the set_params function. */
  local_data->production_types = units->production_type_names;
  nprod_types = local_data->production_types->len;
  local_data->param_block = g_new0 (param_block_t **, nprod_types);

  /* Initialize a list of detected units. */
  local_data->detected_units = g_hash_table_new (g_direct_hash, g_direct_equal);

  /* Initialize a list of units for avoiding making two requests for the same
   * unit on the same day. */
  local_data->requested_today = g_hash_table_new (g_direct_hash, g_direct_equal);

  /* Initialize an array to hold the radius of the largest vaccination ring
   * that can be triggered around each production type. */
  local_data->max_radius = g_new0 (double, nprod_types);

  /* Send the XML subtree to the init function to read the production type
   * combination specific parameters. */
  self->set_params (self, params);

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file ring_vaccination_model.c */
