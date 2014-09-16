/** @file airborne_spread_model.c
 * Module for airborne spread.
 *
 * This module has 4 parameters:
 * <ul>
 *   <li>
 *     The probability of infection at 1 km distance.
 *   <li>
 *     Whether probability of infection falls off linearly or exponentially
 *     with distance from the source.
 *   <li>
 *     The area at risk of exposure, given as a range (<i>start</i> and <i>end</i>) in
 *     degrees, following the navigation and surveying convention that
 *     N=0/360&deg;, E=90&deg;, S=180&deg;, and W=270&deg;.
 *
 *     Note that <i>start</i> can be greater than <i>end</i>.  For example, to
 *     get north winds (from the north), you might use <i>start</i>=135,
 *     <i>end</i>=225, but for south winds, you would use <i>start</i>=315,
 *     <i>end</i>=45 (see figure below).
 *   <li>
 *     The maximum distance of spread, in km, for the linear dropoff formula.
 * </ul>
 *
 * @image html directions.png "Parameters for north winds (left) and south winds (right)"
 *
 * This module pre-calculates some values for use during the simulation run.
 * It builds a histogram of sizes, then for each unit <i>A</i>, it
 * calculates <i>SizeFactor</i>(<i>A</i>) = (area under the histogram from
 * 0 to size of unit <i>A</i>) &times; 2.
 *
 * On each day, this module follows these steps:
 * <ol>
 *   <li>
 *     For each pair of units <i>A</i> and <i>B</i>,
 *     <ol>
 *       <li>
 *         Check whether <i>A</i> or <i>B</i> can be the source of an
 *         infection.  That is, is it Infectious?
 *       <li>
 *         Check whether <i>A</i> or <i>B</i> can be the target of an
 *         infection.  That is, is it Susceptible?
 *       <li>
 *         If <i>A</i> can be the source and <i>B</i> can be the target, or
 *         vice versa, continue; otherwise, go on to the next pair of units.
 *       <li>
 *         If using linear dropoff and
 *         the distance between <i>A</i> and <i>B</i> < the maximum
 *         distance specified in the parameters, continue; otherwise, go on to
 *         the next pair of units.
 *       <li>
 *         If the heading from the source unit to the target unit is inside the
 *         area at risk of exposure specified in the parameters, continue;
 *         otherwise, go on to the next pair of units.
 *       <li>
 *         Compute the probability of infection <i>P</i> =
 *         <i>SizeFactor</i>(<i>A</i>)
 *         &times; prevalence in <i>A</i>
 *         &times; <i>DistanceFactor</i>(<i>A</i>,<i>B</i>)
 *         &times; <i>SizeFactor</i>(<i>B</i>).
 *       <li>
 *         Generate a random number <i>r</i> in [0,1).
 *       <li>
 *         If <i>r</i> < <i>P</i>,
 *         <ol>
 *           <li>
 *             Infect the target unit.
 *             NB: This infection will not be discovered by trace-back
 *             investigations.
 *         </ol>
 *     </ol>
 * </ol>
 * where
 * <ul>
 *   <li>
 *     If using linear dropoff:
 *     <i>DistanceFactor</i>(<i>A</i>,<i>B</i>) = (probability of infection at 1 km)
 *     &times; (maximum distance of spread -
 *     distance from <i>A</i> to <i>B</i>) / (maximum distance of spread - 1)
 *   <li>
 *     If using exponential dropoff:
 *     <i>DistanceFactor</i>(<i>A</i>,<i>B</i>) = (probability of infection at 1 km)<sup>distance from <i>A</i> to <i>B</i></sup>
 * </ul>
 *
 * @image html airborne.png
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
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
#define new airborne_spread_model_new
#define run airborne_spread_model_run
#define has_pending_actions airborne_spread_model_has_pending_actions
#define has_pending_infections airborne_spread_model_has_pending_infections
#define to_string airborne_spread_model_to_string
#define local_free airborne_spread_model_free
#define handle_before_each_simulation_event airborne_spread_model_handle_before_each_simulation_event
#define handle_new_day_event airborne_spread_model_handle_new_day_event
#define check_and_infect airborne_spread_model_check_and_infect

#include "module.h"
#include "module_util.h"
#include "gis.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#if HAVE_STRINGS_H
#  include <strings.h>
#endif

#if HAVE_MATH_H
#  include <math.h>
#endif

#include "spatial_search.h"

#include "airborne_spread_model.h"

#if !HAVE_ROUND && HAVE_RINT
#  define round rint
#endif

double round (double x);

/** This must match an element name in the DTD. */
#define MODEL_NAME "airborne-spread-model"



#define EPSILON 0.01



/* Specialized information for this model. */
typedef struct
{
  double prob_spread_1km;
  double wind_dir_start, wind_dir_end;
  gboolean wind_range_crosses_0;
  double max_spread;
  PDF_dist_t *delay;
}
param_block_t;



typedef struct
{
  GPtrArray *production_types; /**< Each item in the list is a char *. */
  param_block_t ***param_block;
  gboolean use_exponential_dropoff; /**< If TRUE, uses the exponential dropoff
    formula; if FALSE, uses the linear dropoff formula. */
  double *max_spread;
  double *size_factor;
  GPtrArray *pending_infections; /**< An array to store delayed contacts.  Each
    item in the array is a GQueue of Exposure events.  (Actually
    a singly-linked list would suffice, but the GQueue syntax is much more
    readable than the GSList syntax.)  An index "rotates" through the array, so
    an event that is to happen in 1 day is placed in the GQueue that is 1 place
    ahead of the rotating index, an event that is to happen in 2 days is placed
    in the GQueue that is 2 places ahead of the rotating index, etc. */
  unsigned int npending_exposures;
  unsigned int npending_infections;
  unsigned int rotating_index; /**< To go with pending_infections. */
  sqlite3 *db; /* Temporarily stash a pointer to the parameters database here
    so that it will be available to the set_params function. */
}
local_data_t;



/**
 * Computes the size factor for each unit.
 *
 * @param units a list of units.
 * @return an array containing the size factor for each unit.
 */
static double *
build_size_factor_list (UNT_unit_list_t * units)
{
  UNT_unit_t *unit;
  unsigned int nunits;          /* number of units */
  unsigned int max_size = 0;    /* size of largest unit */
  gsl_histogram *histogram;
  PDF_dist_t *size_dist;
  double *size_factor;
  unsigned int i;               /* loop counter */
#if DEBUG
  char *s;
#endif

#if DEBUG
  g_debug ("----- ENTER build_size_factor_list");
#endif

  nunits = UNT_unit_list_length (units);
  size_factor = g_new (double, nunits);

  /* Find the largest unit. */
  for (i = 0; i < nunits; i++)
    {
      unit = UNT_unit_list_get (units, i);
      if (unit->size > max_size)
        max_size = unit->size;
    }
#if DEBUG
  g_debug ("largest number of animals = %u", max_size);
#endif

  /* Build a histogram. */
  histogram = gsl_histogram_alloc (MIN(200,max_size));
  g_assert (histogram != NULL);
  gsl_histogram_set_ranges_uniform (histogram, 0.5, (double) max_size + 0.5);
  for (i = 0; i < nunits; i++)
    {
      unit = UNT_unit_list_get (units, i);
      gsl_histogram_increment (histogram, (double) (unit->size));
    }
  size_dist = PDF_new_histogram_dist (histogram);
  gsl_histogram_free (histogram);
  g_assert (size_dist != NULL);

#if DEBUG
  s = PDF_dist_to_string (size_dist);
  g_debug ("size distribution =\n%s", s);
  g_free (s);
#endif

  /* Compute the size factors. */
  for (i = 0; i < nunits; i++)
    {
      unit = UNT_unit_list_get (units, i);
      size_factor[i] = PDF_cdf (unit->size, size_dist) * 2;
    }

  PDF_free_dist (size_dist);

#if DEBUG
  g_debug ("----- EXIT build_size_factor_list");
#endif

  return size_factor;
}



/**
 * Before each simulation, this module deletes any delayed exposures left over
 * from a previous iteration.
 *
 * @param self this module.
 */
void
handle_before_each_simulation_event (struct adsm_module_t_ *self)
{
  local_data_t *local_data;
  unsigned int i;
  GQueue *q;

  #if DEBUG
    g_debug ("----- ENTER handle_before_each_simulation (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);
  for (i = 0; i < local_data->pending_infections->len; i++)
    {
      q = (GQueue *) g_ptr_array_index (local_data->pending_infections, i);
      while (!g_queue_is_empty (q))
        EVT_free_event (g_queue_pop_head (q));
    }
  local_data->npending_exposures = 0;
  local_data->npending_infections = 0;
  local_data->rotating_index = 0;

  #if DEBUG
    g_debug ("----- EXIT handle_before_each_simulation (%s)", MODEL_NAME);
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
  RAN_gen_t *rng;
  EVT_event_queue_t *queue;
} callback_t;



/**
 * Check whether unit 1 can infect unit 2 and if so, attempt to infect unit 2.
 */
gboolean
check_and_infect (int id, gpointer arg)
{
  callback_t *callback_data;
  UNT_unit_list_t *units;
  UNT_unit_t *unit1, *unit2;
  local_data_t *local_data;
  gboolean unit2_can_be_target;
  param_block_t *param_block;
  double max_spread, distance, heading;
  double distance_factor, unit1_size_factor, unit2_size_factor;
  int day;
  EVT_event_t *exposure;
  RAN_gen_t *rng;
  double r, P;
  int delay;
  int delay_index;
  GQueue *q;
  gboolean exposure_is_adequate;
#if DEBUG
  GString *s;
#endif

#if DEBUG
  g_debug ("----- ENTER check_and_infect (%s)", MODEL_NAME);
#endif

  callback_data = (callback_t *) arg;
  units = callback_data->units;
  unit1 = callback_data->unit1;
  unit2 = UNT_unit_list_get (units, id);

  /* Are unit 1 and unit 2 the same? */
  if (unit1 == unit2)
    goto end;

  local_data = (callback_data->local_data);

  /* Can unit 2 be the target of an exposure? */
  #if DEBUG
    s = g_string_new (NULL);
    g_string_sprintf (s, "unit \"%s\" is %s, state is %s: ",
                      unit2->official_id, unit2->production_type_name,
                      UNT_state_name[unit2->state]);
  #endif
  param_block = local_data->param_block[unit1->production_type][unit2->production_type];
  unit2_can_be_target = (
    param_block != NULL 
    && unit2->state != Destroyed
  );
  #if DEBUG
    g_string_sprintfa (s, "%s be target", unit2_can_be_target ? "can" : "cannot");
    g_debug ("%s", s->str);
    g_string_free (s, TRUE);
  #endif
  if (!unit2_can_be_target)
    goto end;

  /* Is unit 2 within the area at risk of exposure? */
  heading = GIS_heading (unit1->x, unit1->y, unit2->x, unit2->y);
  if (param_block->wind_range_crosses_0
      ? (param_block->wind_dir_start - heading > EPSILON
         && heading - param_block->wind_dir_end >=
         EPSILON) : (param_block->wind_dir_start - heading > EPSILON
                     || heading - param_block->wind_dir_end >= EPSILON))
    {
      #if DEBUG
        g_debug ("  unit \"%s\" outside wind angles (%g)", unit2->official_id, heading);
      #endif
      goto end;
    }
  #if DEBUG
    g_debug ("  unit \"%s\" within wind angles (%g)", unit2->official_id, heading);
  #endif

  distance = GIS_distance (unit1->x, unit1->y, unit2->x, unit2->y);
  if (local_data->use_exponential_dropoff)
    {
      distance_factor = pow (param_block->prob_spread_1km, distance);
    }
  else
    {
      max_spread = param_block->max_spread;
      distance_factor = param_block->prob_spread_1km * (max_spread - distance) / (max_spread - 1);
    }
  unit1_size_factor = local_data->size_factor[unit1->index];
  unit2_size_factor = local_data->size_factor[unit2->index];
  #if DEBUG
    g_debug ("  P = %g * %g * %g * %g",
             unit1_size_factor, unit1->prevalence, distance_factor, unit2_size_factor);
  #endif

  rng = callback_data->rng;
  P = unit1_size_factor * unit1->prevalence * distance_factor * unit2_size_factor;
  r = RAN_num (rng);
  exposure_is_adequate = (r < P); 

  /* Record (queue) the exposure, whether it was adequate or not
   * (Most event handlers will ignore exposures by airborne spread,
   * which are not traceable). */
  day = callback_data->day;
  delay = (int) round (PDF_random (param_block->delay, rng));
  exposure = EVT_new_exposure_event (unit1, unit2, day,
                                     ADSM_AirborneSpread,
                                     FALSE, exposure_is_adequate, delay);
  exposure->u.exposure.contact_type = ADSM_AirborneSpread;
                                      
  if (delay <= 0)
    {
      EVT_event_enqueue (callback_data->queue, exposure);  
    }
  else
    {
      exposure->u.exposure.day += delay;
      if (delay > local_data->pending_infections->len)
        {
          adsm_extend_rotating_array (local_data->pending_infections,
                                             delay, local_data->rotating_index);
        }
    
      delay_index = (local_data->rotating_index + delay) % local_data->pending_infections->len;
      q = (GQueue *) g_ptr_array_index (local_data->pending_infections, delay_index);
      g_queue_push_tail (q, exposure);
      local_data->npending_exposures++;
      if (exposure_is_adequate)
        local_data->npending_infections++;
      #if DEBUG
        g_debug ("npending_exposures now %u, npending_infections now %u", local_data->npending_exposures, local_data->npending_infections);
      #endif
    }

end:
#if DEBUG
  g_debug ("----- EXIT check_and_infect (%s)", MODEL_NAME);
#endif
  return TRUE; /* A return value of FALSE would stop the spatial search early,
    which we don't want to do. */
}



/**
 * Responds to a new day event by releasing any pending infections and
 * stochastically generating infections.
 *
 * @param self the model.
 * @param units a list of units.
 * @param event a new day event.
 * @param rng a random number generator.
 * @param queue for any new events the model creates.
 */
void
handle_new_day_event (struct adsm_module_t_ *self, UNT_unit_list_t * units,
                      EVT_new_day_event_t * event, RAN_gen_t * rng, EVT_event_queue_t * queue)
{
  local_data_t *local_data;
  UNT_unit_t *unit1;
  unsigned int nunits;          /* number of units */
  unsigned int unit1_index;
  gboolean unit1_can_be_source;
  GQueue *q;
  EVT_event_t *pending_event;
  callback_t callback_data;
#if DEBUG
  GString *s;
#endif

#if DEBUG
  g_debug ("----- ENTER handle_new_day_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* Release any pending (due to airborne transport delays) events. */
  local_data->rotating_index =
    (local_data->rotating_index + 1) % local_data->pending_infections->len;
  q = (GQueue *) g_ptr_array_index (local_data->pending_infections, local_data->rotating_index);
  while (!g_queue_is_empty (q))
    {
      /* Remove the event from this model's internal queue and place it in the
       * simulation's event queue. */
      pending_event = (EVT_event_t *) g_queue_pop_head (q);
#ifndef WIN_DLL
      /* Double-check that the event is coming out on the correct day. */
      g_assert (pending_event->u.exposure.day == event->day);
#endif
      EVT_event_enqueue (queue, pending_event);
      local_data->npending_exposures--;
      if (pending_event->u.exposure.adequate)
        local_data->npending_infections--;
      #if DEBUG
        g_debug ("npending_exposures now %u, npending_infections now %u", local_data->npending_exposures, local_data->npending_infections);
      #endif
    }

  /* Initialize a data structure used by the callback function. */
  callback_data.local_data = local_data;
  callback_data.units = units;
  callback_data.day = event->day;
  callback_data.rng = rng;
  callback_data.queue = queue;

  nunits = UNT_unit_list_length (units);
  for (unit1_index = 0; unit1_index < nunits; unit1_index++)
    {
      unit1 = UNT_unit_list_get (units, unit1_index);

      /* Can this unit be the source of an exposure? */
#if DEBUG
      s = g_string_new (NULL);
      g_string_sprintf (s, "unit \"%s\" is %s, state is %s: ",
                        unit1->official_id, unit1->production_type_name,
                        UNT_state_name[unit1->state]);
#endif
      unit1_can_be_source =
        local_data->param_block[unit1->production_type] != NULL
        && (unit1->state == InfectiousSubclinical || unit1->state == InfectiousClinical);
#if DEBUG
      g_string_sprintfa (s, "%s be source", unit1_can_be_source ? "can" : "cannot");
      if (unit1_can_be_source)
        g_debug ("%s", s->str);
      g_string_free (s, TRUE);
#endif
      if (!unit1_can_be_source)
        continue;

      callback_data.unit1 = unit1;
      spatial_search_circle_by_id (units->spatial_index, unit1_index,
                                   local_data->max_spread[unit1->production_type] + EPSILON,
                                   check_and_infect, &callback_data);
    }

#if DEBUG
  g_debug ("----- EXIT handle_new_day_event (%s)", MODEL_NAME);
#endif

  return;
}



/**
 * Runs this model.
 *
 * Side effects: may change the state of one or more units in list.
 *
 * @param self the model.
 * @param units a list of units.
 * @param zones a list of zones.
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
    case EVT_BeforeEachSimulation:
      handle_before_each_simulation_event (self);
      break;
    case EVT_NewDay:
      handle_new_day_event (self, units, &(event->u.new_day), rng, queue);
      break;
    default:
      g_error
        ("%s has received a %s event, which it does not listen for.  This should never happen.  Please contact the developer.",
         MODEL_NAME, EVT_event_type_name[event->type]);
    }

#if DEBUG
  g_debug ("----- EXIT run (%s)", MODEL_NAME);
#endif

  return;
}



/**
 * Reports whether this model has any pending actions to carry out.
 *
 * @param self the model.
 * @return TRUE if the model has pending actions.
 */
gboolean
has_pending_actions (struct adsm_module_t_ * self)
{
  local_data_t *local_data;

  local_data = (local_data_t *) (self->model_data);
  return (local_data->npending_exposures > 0 || local_data->npending_infections > 0);
}



/**
 * Reports whether this model has any pending infections to cause.
 *
 * @param self the model.
 * @return TRUE if the model has pending infections.
 */
gboolean
has_pending_infections (struct adsm_module_t_ * self)
{
  local_data_t *local_data;

  local_data = (local_data_t *) (self->model_data);
  return (local_data->npending_infections > 0);
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
  char *substring, *chararray;

  local_data = (local_data_t *) (self->model_data);
  s = g_string_new (NULL);
  g_string_printf (s, "<%s %s", MODEL_NAME,
                   local_data->use_exponential_dropoff ? "exponential" : "linear");

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
            g_string_append_printf (s, "\n    prob-spread-1km=%g", param_block->prob_spread_1km);
            g_string_append_printf (s, "\n    wind-direction=(%g,%g)",
                                    param_block->wind_dir_start, param_block->wind_dir_end);
            if (local_data->use_exponential_dropoff == FALSE)
              {
                g_string_append_printf (s, "\n    max-spread=%g", param_block->max_spread);
              }

            substring = PDF_dist_to_string (param_block->delay);
            g_string_append_printf (s, "\n    delay=%s", substring);
            g_free (substring);
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
  unsigned int nprod_types, i, j;
  GQueue *q;
  param_block_t *param_block;

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
          if (local_data->param_block[i][j] != NULL)
            {
              param_block = local_data->param_block[i][j];
              /* Free the dynamically-allocated parts of the parameter block. */
              PDF_free_dist (param_block->delay);
              /* Free the parameter block itself. */
              g_free (param_block);
            }
        /* Free this row of the 2D array. */
        g_free (local_data->param_block[i]);
      }
  /* Free the array of pointers to rows. */
  g_free (local_data->param_block);

  g_free (local_data->max_spread);
  g_free (local_data->size_factor);

  for (i = 0; i < local_data->pending_infections->len; i++)
    {
      q = (GQueue *) g_ptr_array_index (local_data->pending_infections, i);
      while (!g_queue_is_empty (q))
        EVT_free_event (g_queue_pop_head (q));
      g_queue_free (q);
    }
  g_ptr_array_free (local_data->pending_infections, TRUE);

  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Adds a set of parameters to an airborne spread model.
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
  sqlite3 *params;
  UNT_production_type_t from_production_type, to_production_type;
  param_block_t *p;
  char *endptr;
  guint pdf_id;

#if DEBUG
  g_debug ("----- ENTER set_params (%s)", MODEL_NAME);
#endif

  self = (adsm_module_t *)data;
  local_data = (local_data_t *) (self->model_data);
  params = local_data->db;

  g_assert (ncols == 7);

  /* Find out which to-from production type combination these parameters apply
   * to. */
  from_production_type =
    adsm_read_prodtype (value[0], local_data->production_types);
  to_production_type =
    adsm_read_prodtype (value[1], local_data->production_types);

  /* If necessary, create a row in the 2D array for this from-production-type. */
  if (local_data->param_block[from_production_type] == NULL)
    {
      local_data->param_block[from_production_type] =
        g_new0 (param_block_t *, local_data->production_types->len);
    }
  /* Check that we are not overwriting an existing parameter block (that would
   * indicate a bug). */
  g_assert (local_data->param_block[from_production_type][to_production_type] == NULL);

  /* Create a new parameter block. */
  p = g_new (param_block_t, 1);
  local_data->param_block[from_production_type][to_production_type] = p;  

  /* Read the parameters. */
  p->prob_spread_1km = strtod (value[2], &endptr);
  if (errno == ERANGE || endptr == value[2] || p->prob_spread_1km < 0)
    {
      g_warning ("setting probability of spread at 1 km to 0");
      p->prob_spread_1km = 0;
    }
  p->prob_spread_1km = CLAMP (p->prob_spread_1km, 0, 1);

  p->wind_dir_start = strtod (value[3], &endptr);
  if (errno == ERANGE || endptr == value[3])
    {
      g_warning ("setting start of area at risk of exposure to 0");
      p->wind_dir_start = 0;
    }
  /* Force the angle into the range [0,360). */
  while (p->wind_dir_start < 0)
    p->wind_dir_start += 360;
  while (p->wind_dir_start >= 360)
    p->wind_dir_start -= 360;

  p->wind_dir_end = strtod (value[4], &endptr);
  if (errno == ERANGE || endptr == value[4])
    {
      g_warning ("setting end of area at risk of exposure to 360");
      p->wind_dir_end = 360;
    }
  /* Force the angle into the range [0,360]. */
  while (p->wind_dir_end < 0)
    p->wind_dir_end += 360;
  while (p->wind_dir_end > 360)
    p->wind_dir_end -= 360;

  /* Note that start > end is allowed.  See the header comment. */
  p->wind_range_crosses_0 = (p->wind_dir_start > p->wind_dir_end);

  /* Setting both start and end to 0 seems like a sensible way to turn off
   * airborne spread, but headings close to north will "sneak through" this
   * restriction because we allow a little wiggle room for rounding errors. If
   * the user tries this, instead set prob-spread-1km=0. */
  if (p->wind_dir_start == 0 && p->wind_dir_end == 0)
    p->prob_spread_1km = 0;

  if (local_data->use_exponential_dropoff)
    {
      /* The exponential falloff curve never actually gets to 0, but we set the
       * maximum distance as the distance at which the probability drops to 1
       * in a million.  The constant 4 is needed in the calculation because the
       * probability formula includes multipliers (the size factors) that may
       * boost the probability by as much as 4 times. */
      if (p->prob_spread_1km > 0)
        p->max_spread = log (1.0/1000000 / 4) / log (p->prob_spread_1km);
      else
        p->max_spread = 0;
    }
  else
    {
      p->max_spread = strtod (value[5], &endptr);
      if (errno == ERANGE || endptr == value[5])
        {
          g_warning ("setting maximum distance of spread to 0");
          p->max_spread = 0;
        }
    }
  /* The maximum spread distance cannot be negative. */
  if (p->max_spread < 0)
    {
      g_warning ("maximum distance of spread cannot be negative, setting to 0");
      p->max_spread = 0;
    }
  /* Setting the maximum spread distance to 0 seems like a sensible way to turn
   * off airborne spread, but max-spread <= 1 doesn't make sense in the
   * formula.  If the user tries this, instead set max-spread=2,
   * prob-spread-1km=0. */
  if (p->max_spread <= 1)
    {
      g_warning ("maximum distance of spread is less than or equal to 1 km: no airborne spread will be used");
      p->max_spread = 2;
      p->prob_spread_1km = 0;
    }
  /* Keep track of the maximum distance of spread from each production type.
   * This determines whether we will use the R-tree index when looking for
   * units to spread infection to. */
  if (p->max_spread > local_data->max_spread[from_production_type])
    local_data->max_spread[from_production_type] = p->max_spread;

  if (value[6] != NULL)
    {
      errno = 0;
      pdf_id = strtol (value[6], NULL, /* base */ 10);
      g_assert (errno != ERANGE && errno != EINVAL);
      p->delay = PAR_get_PDF (params, pdf_id);
    }
  else
    p->delay = PDF_new_point_dist (0);

#if DEBUG
  g_debug ("----- EXIT set_params (%s)", MODEL_NAME);
#endif

  return 0;
}



/**
 * Returns a new airborne spread model.
 */
adsm_module_t *
new (sqlite3 *params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  adsm_module_t *self;
  local_data_t *local_data;
  EVT_event_type_t events_listened_for[] = {
    EVT_BeforeEachSimulation,
    EVT_NewDay,
    0
  };
  unsigned int nprod_types, i;
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
  self->has_pending_actions = has_pending_actions;
  self->has_pending_infections = has_pending_infections;
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

  /* Compute the size factors. */
  local_data->size_factor = build_size_factor_list (units);

  /* Initialize an array to hold the maximum distance of spread from each
   * production type. */
  local_data->max_spread = g_new (double, nprod_types);
  for (i = 0; i < nprod_types; i++)
    local_data->max_spread[i] = 1;

  /* Initialize an array for delayed contacts.  We don't know yet how long the
   * the array needs to be, since that will depend on values we sample from the
   * delay distribution, so we initialize it to length 1. */
  local_data->pending_infections = g_ptr_array_new ();
  g_ptr_array_add (local_data->pending_infections, g_queue_new ());
  local_data->npending_exposures = 0;
  local_data->npending_infections = 0;
  local_data->rotating_index = 0;

  local_data->use_exponential_dropoff = PAR_get_boolean (params, "SELECT use_airborne_exponential_decay FROM ScenarioCreator_disease");
  /* Call the set_params function to read the production type combination
   * specific parameters. */
  local_data->db = params;
  sqlite3_exec (params,
                "SELECT src_prodtype.name,dest_prodtype.name,spread_1km_probability,exposure_direction_start,exposure_direction_end,max_distance,transport_delay_id "
                "FROM ScenarioCreator_productiontype src_prodtype,ScenarioCreator_productiontype dest_prodtype,ScenarioCreator_productiontypepairtransmission pairing,ScenarioCreator_airbornespread airborne "
                "WHERE src_prodtype.id=pairing.source_production_type_id "
                "AND dest_prodtype.id=pairing.destination_production_type_id "
                "AND pairing.airborne_spread_id = airborne.id",
                set_params, self, &sqlerr);
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

/* end of file airborne_spread_model.c */
