/** @file infection_monitor.c
 * Tracks the cause of infections.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @version 0.1
 * @date August 2004
 *
 * Copyright &copy; University of Guelph, 2004-2009
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
#define new infection_monitor_new
#define run infection_monitor_run
#define reset infection_monitor_reset
#define events_listened_for infection_monitor_events_listened_for
#define to_string infection_monitor_to_string
#define local_free infection_monitor_free
#define handle_before_any_simulations_event infection_monitor_handle_before_any_simulations_event
#define handle_new_day_event infection_monitor_handle_new_day_event
#define handle_infection_event infection_monitor_handle_infection_event
#define handle_detection_event infection_monitor_handle_detection_event

#include "module.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#if HAVE_MATH_H
#  include <math.h>
#endif


#include "infection_monitor.h"

/* 
infection-monitor.c needs access to the functions defined in spreadmodel.h,
even when compiled as a *nix executable (in which case, 
the functions defined will all be NULL). 
*/
#include "spreadmodel.h"

#include "general.h"

#ifdef USE_SC_GUILIB
#  include <sc_spreadmodel_outputs.h>
#endif

#if !HAVE_ROUND && HAVE_RINT
#  define round rint
#endif

double round (double x);

/** This must match an element name in the DTD. */
#define MODEL_NAME "infection-monitor"



#define NEVENTS_LISTENED_FOR 4
EVT_event_type_t events_listened_for[] =
  { EVT_BeforeAnySimulations,
    EVT_NewDay, EVT_Infection,
    EVT_Detection };



/** Specialized information for this model. */
typedef struct
{
  GPtrArray *production_types;
  RPT_reporting_t *num_units_infected;
  RPT_reporting_t *num_units_infected_by_cause;
  RPT_reporting_t *num_units_infected_by_prodtype;
  RPT_reporting_t *num_units_infected_by_cause_and_prodtype;
  RPT_reporting_t *cumul_num_units_infected;
  RPT_reporting_t *cumul_num_units_infected_by_cause;
  RPT_reporting_t *cumul_num_units_infected_by_prodtype;
  RPT_reporting_t *cumul_num_units_infected_by_cause_and_prodtype;
  RPT_reporting_t *num_animals_infected;
  RPT_reporting_t *num_animals_infected_by_cause;
  RPT_reporting_t *num_animals_infected_by_prodtype;
  RPT_reporting_t *num_animals_infected_by_cause_and_prodtype;
  RPT_reporting_t *cumul_num_animals_infected;
  RPT_reporting_t *cumul_num_animals_infected_by_cause;
  RPT_reporting_t *cumul_num_animals_infected_by_prodtype;
  RPT_reporting_t *cumul_num_animals_infected_by_cause_and_prodtype;
  gboolean detection_occurred;
  int detection_day;
  RPT_reporting_t *first_det_u_inf;
  RPT_reporting_t *first_det_a_inf;
  RPT_reporting_t *ratio;
  unsigned int nrecent_days; /**< The time period over which to compare recent
    infections.  A value of 14 would mean to report the number of new
    infections in the last 2 weeks over the number of new infections in the
    2 weeks before that. */
  unsigned int *nrecent_infections; /**< The number of new infections on each
    day in the recent past.  The length of this array is nrecent_days * 2. */
  unsigned int recent_day_index; /**< The current index into the
    nrecent_infections array.  The index "rotates" through the array, arriving
    back at the beginning and starting to overwrite old values every
    nrecent_days * 2 days. */
  unsigned int numerator, denominator;
}
local_data_t;



/**
 * Before any simulations, this module announces the output variables it is
 * recording.
 *
 * @param self this module.
 * @param queue for any new events this function creates.
 */
void
handle_before_any_simulations_event (struct spreadmodel_model_t_ *self,
                                     EVT_event_queue_t *queue)
{
  unsigned int n, i;
  RPT_reporting_t *output;
  GPtrArray *outputs = NULL;

  n = self->outputs->len;
  for (i = 0; i < n; i++)
    {
      output = (RPT_reporting_t *) g_ptr_array_index (self->outputs, i);
      if (output->frequency != RPT_never)
        {
          if (outputs == NULL)
            outputs = g_ptr_array_new();
          g_ptr_array_add (outputs, output);
        }
    }

  if (outputs != NULL)
    EVT_event_enqueue (queue, EVT_new_declaration_of_outputs_event (outputs));
  /* We don't free the pointer array, that will be done when the event is freed
   * after all interested modules have processed it. */

  return;
}



/**
 * On each new day, zero the daily counts of infections and does some setup for
 * calculating the reproduction number R.
 *
 * @param self the model.
 * @param event a new day event.
 */
void
handle_new_day_event (struct spreadmodel_model_t_ *self, EVT_new_day_event_t * event)
{
  local_data_t *local_data;
  unsigned int current, hi, i, count;
#if DEBUG
  GString *s;
#endif

#if DEBUG
  g_debug ("----- ENTER handle_new_day_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* Zero the daily counts. */
  if (event->day > 1)
    {
      RPT_reporting_zero (local_data->num_units_infected);
      RPT_reporting_zero (local_data->num_units_infected_by_cause);
      RPT_reporting_zero (local_data->num_units_infected_by_prodtype);
      RPT_reporting_zero (local_data->num_units_infected_by_cause_and_prodtype);
      RPT_reporting_zero (local_data->num_animals_infected);
      RPT_reporting_zero (local_data->num_animals_infected_by_cause);
      RPT_reporting_zero (local_data->num_animals_infected_by_prodtype);
      RPT_reporting_zero (local_data->num_animals_infected_by_cause_and_prodtype);
    }

  /* Move the pointer for the current day's infection count ahead. */
  hi = local_data->nrecent_days * 2;
  if (event->day == 1)
    {
      current = local_data->recent_day_index;
    }
  else
    {
      current = (local_data->recent_day_index + 1) % hi;
      local_data->recent_day_index = current;
      /* Zero the current day's count. */
      local_data->nrecent_infections[current] = 0;
    }

  /* Compute the denominator of the infection ratio for today. */
  local_data->denominator = 0;
  /* The numbers that sum to the denominator start at 1 past the current point
   * and continue for the period defined by nrecent_days. */
  for (i = (current + 1) % hi, count = 0;
       count < local_data->nrecent_days; i = (i + 1) % hi, count++)
    local_data->denominator += local_data->nrecent_infections[i];

  /* Compute the numerator, minus the current day's infections (which are yet
   * to happen). */
  local_data->numerator = 0;
  for (count = 0; count < local_data->nrecent_days; i = (i + 1) % hi, count++)
    local_data->numerator += local_data->nrecent_infections[i];

#if DEBUG
  s = g_string_new (NULL);
  g_string_append_printf (s, "at beginning of day %i counts of recent infections = [", event->day);
  for (i = 0; i < hi; i++)
    {
      if (i > 0)
        g_string_append_c (s, ',');
      g_string_append_printf (s, i == current ? "(%u)" : "%u", local_data->nrecent_infections[i]);
    }
  g_string_append_c (s, ']');
  g_debug ("%s", s->str);
  g_string_free (s, TRUE);
  g_debug ("denominator = sum from %u to %u (inclusive) = %u",
           (current + 1) % hi, (current + local_data->nrecent_days) % hi, local_data->denominator);
#endif

  /* Set the ratio of recent infections to infections before that.  If there
   * are no detections in the current day, this will be the value that will be
   * reported at the end of the day.  Note that the value is undefined until a
   * certain number of days has passed, e.g., if we are reporting new infection
   * this week over new infections last week, the value will be undefined until
   * 2 weeks have passed. */
  if (event->day >= (local_data->nrecent_days * 2) && local_data->denominator > 0)
    RPT_reporting_set_real (local_data->ratio,
                            1.0 * local_data->numerator / local_data->denominator, NULL);

#if DEBUG
  g_debug ("----- EXIT handle_new_day_event (%s)", MODEL_NAME);
#endif
}



/**
 * Responds to the first detection event by recording the day on which it
 * occurred.
 *
 * @param self this module.
 * @param event a detection event.
 */
void
handle_detection_event (struct spreadmodel_model_t_ *self, 
                        EVT_detection_event_t * event)
{
  local_data_t *local_data;

#if DEBUG
  g_debug ("----- ENTER handle_detection_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  if (!local_data->detection_occurred)
    {
      #if DEBUG
        g_debug ("recording first detection on day %i", event->day);
      #endif
      local_data->detection_occurred = TRUE;
      local_data->detection_day = event->day;
      /* Copy the current value from infcUAll to firstDetUInfAll and from
       * from infcAAll to firstDetAInfAll.  Any subsequent infections on the
       * day of first detection will also be included in the firstDet output
       * variables. */
      RPT_reporting_set_integer (
        local_data->first_det_u_inf,
        RPT_reporting_get_integer(local_data->cumul_num_units_infected, NULL),
        NULL
      );
      RPT_reporting_set_integer (
        local_data->first_det_a_inf,
        RPT_reporting_get_integer(local_data->cumul_num_animals_infected, NULL),
        NULL
      );
    }

#if DEBUG
  g_debug ("----- EXIT handle_detection_event (%s)", MODEL_NAME);
#endif
  return;
}



/**
 * Responds to an infection event by recording it.
 *
 * @param self the model.
 * @param event an infection event.
 */
void
handle_infection_event (struct spreadmodel_model_t_ *self, EVT_infection_event_t * event)
{
  local_data_t *local_data;
  UNT_unit_t *infecting_unit, *infected_unit;
  const char *cause;
  const char *drill_down_list[3] = { NULL, NULL, NULL };
  unsigned int count;
  UNT_infect_t update;
#if DEBUG
  GString *s;
#endif

#if DEBUG
  g_debug ("----- ENTER handle_infection_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  infecting_unit = event->infecting_unit;
  infected_unit = event->infected_unit;

  cause = SPREADMODEL_contact_type_abbrev[event->contact_type];

  update.unit_index = infected_unit->index;
  update.infection_source_type = event->contact_type;
  
#ifdef USE_SC_GUILIB
  sc_infect_unit( event->day, infected_unit, update );
#else
  if (NULL != spreadmodel_infect_unit)
    {
      spreadmodel_infect_unit (update);
    }
#endif
#if UNDEFINED
  printf ("unit at index %d INFECTED by method %s\n", infected_unit->index, cause);
#endif

  /* Update the counts of infections.  Note that initially infected units are
   * not included in many of the counts.  They will not be part of infnUAll or
   * infnU broken down by production type.  They will be part of infnUIni and
   * infnUIni broken down by production type. */
  if (event->contact_type != SPREADMODEL_InitiallyInfected)
    {
      RPT_reporting_add_integer  (local_data->num_units_infected, 1, NULL);
      RPT_reporting_add_integer1 (local_data->num_units_infected_by_prodtype, 1, infected_unit->production_type_name);
      RPT_reporting_add_integer  (local_data->num_animals_infected, infected_unit->size, NULL);
      RPT_reporting_add_integer1 (local_data->num_animals_infected_by_prodtype, infected_unit->size, infected_unit->production_type_name);
      RPT_reporting_add_integer  (local_data->cumul_num_units_infected, 1, NULL);
      RPT_reporting_add_integer1 (local_data->cumul_num_units_infected_by_prodtype, 1, infected_unit->production_type_name);
      RPT_reporting_add_integer  (local_data->cumul_num_animals_infected, infected_unit->size, NULL);
      RPT_reporting_add_integer1 (local_data->cumul_num_animals_infected_by_prodtype, infected_unit->size, infected_unit->production_type_name);
    }
  RPT_reporting_add_integer1 (local_data->num_units_infected_by_cause, 1, cause);
  RPT_reporting_add_integer1 (local_data->num_animals_infected_by_cause, infected_unit->size, cause);
  RPT_reporting_add_integer1 (local_data->cumul_num_units_infected_by_cause, 1, cause);
  RPT_reporting_add_integer1 (local_data->cumul_num_animals_infected_by_cause, infected_unit->size, cause);
  drill_down_list[0] = cause;
  drill_down_list[1] = infected_unit->production_type_name;
  if (local_data->num_units_infected_by_cause_and_prodtype->frequency != RPT_never)
    RPT_reporting_add_integer (local_data->num_units_infected_by_cause_and_prodtype, 1, drill_down_list);
  if (local_data->num_animals_infected_by_cause_and_prodtype->frequency != RPT_never)
    RPT_reporting_add_integer (local_data->num_animals_infected_by_cause_and_prodtype, infected_unit->size,
                               drill_down_list);
  if (local_data->cumul_num_units_infected_by_cause_and_prodtype->frequency != RPT_never)
    RPT_reporting_add_integer (local_data->cumul_num_units_infected_by_cause_and_prodtype, 1,
                               drill_down_list);
  if (local_data->cumul_num_animals_infected_by_cause_and_prodtype->frequency != RPT_never)
    RPT_reporting_add_integer (local_data->cumul_num_animals_infected_by_cause_and_prodtype,
                               infected_unit->size, drill_down_list);

  /* Infections that occur on the same day as the first detection are included
   * in the value of the firstDet output variables. */
  if (local_data->detection_occurred
      && (local_data->detection_day == event->day))
    {
      RPT_reporting_add_integer (local_data->first_det_u_inf, 1, NULL);
      RPT_reporting_add_integer (local_data->first_det_a_inf, infected_unit->size, NULL);
    }

  /* Update the ratio of recent infections to infections before that.  Note
   * that the value is undefined until a certain number of days has passed,
   * e.g., if we are reporting new infection this week over new infections last
   * week, the value will be undefined until 2 weeks have passed. */
  local_data->nrecent_infections[local_data->recent_day_index]++;
  count = local_data->nrecent_infections[local_data->recent_day_index];
#if DEBUG
  s = g_string_new (NULL);
  g_string_append_printf (s, "recent infection[%u] now = %u", local_data->recent_day_index, count);
#endif
  if (event->day >= local_data->nrecent_days * 2)
    {
      if (local_data->denominator > 0)
        {
          RPT_reporting_set_real (local_data->ratio,
                                  1.0 * (local_data->numerator + count) / local_data->denominator,
                                  NULL);
#if DEBUG
          g_string_append_printf (s, ", ratio %u/%u = %g",
                                  local_data->numerator + count,
                                  local_data->denominator,
                                  RPT_reporting_get_real (local_data->ratio, NULL));
#endif
        }
      else
        {
#if DEBUG
          g_string_append_printf (s, ", denominator=0, ratio remains at old value of %g",
                                  RPT_reporting_get_real (local_data->ratio, NULL));
#endif
          ;
        }
    }
  else
    {
#if DEBUG
      g_string_append_printf (s, ", no ratio before day %u", local_data->nrecent_days * 2);
#endif
      ;
    }
#if DEBUG
  g_debug ("%s", s->str);
  g_string_free (s, TRUE);
#endif

#if DEBUG
  g_debug ("----- EXIT handle_infection_event (%s)", MODEL_NAME);
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
      handle_before_any_simulations_event (self, queue);
      break;
    case EVT_NewDay:
      handle_new_day_event (self, &(event->u.new_day));
      break;
    case EVT_Infection:
      handle_infection_event (self, &(event->u.infection));
      break;
    case EVT_Detection:
      handle_detection_event (self, &(event->u.detection));
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
  unsigned int i;

#if DEBUG
  g_debug ("----- ENTER reset (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  RPT_reporting_zero (local_data->num_units_infected);
  RPT_reporting_zero (local_data->num_units_infected_by_cause);
  RPT_reporting_zero (local_data->num_units_infected_by_prodtype);
  RPT_reporting_zero (local_data->num_units_infected_by_cause_and_prodtype);
  RPT_reporting_zero (local_data->cumul_num_units_infected);
  RPT_reporting_zero (local_data->cumul_num_units_infected_by_cause);
  RPT_reporting_zero (local_data->cumul_num_units_infected_by_prodtype);
  RPT_reporting_zero (local_data->cumul_num_units_infected_by_cause_and_prodtype);
  RPT_reporting_zero (local_data->num_animals_infected);
  RPT_reporting_zero (local_data->num_animals_infected_by_cause);
  RPT_reporting_zero (local_data->num_animals_infected_by_prodtype);
  RPT_reporting_zero (local_data->num_animals_infected_by_cause_and_prodtype);
  RPT_reporting_zero (local_data->cumul_num_animals_infected);
  RPT_reporting_zero (local_data->cumul_num_animals_infected_by_cause);
  RPT_reporting_zero (local_data->cumul_num_animals_infected_by_prodtype);
  RPT_reporting_zero (local_data->cumul_num_animals_infected_by_cause_and_prodtype);
  local_data->detection_occurred = FALSE;
  /* The output variables for units and animals infected at first detection
   * have no value until there is a detection. */
  RPT_reporting_set_null (local_data->first_det_u_inf, NULL);
  RPT_reporting_set_null (local_data->first_det_a_inf, NULL);
  RPT_reporting_set_null (local_data->ratio, NULL);
  for (i = 0; i < local_data->nrecent_days * 2; i++)
    local_data->nrecent_infections[i] = 0;

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
to_string (struct spreadmodel_model_t_ *self)
{
  local_data_t *local_data;
  GString *s;
  char *chararray;

  local_data = (local_data_t *) (self->model_data);
  s = g_string_new (NULL);
  g_string_sprintf (s, "<%s ratio-period=%u>", MODEL_NAME, local_data->nrecent_days);

  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Frees this model.
 *
 * @param self the model.
 */
void
local_free (struct spreadmodel_model_t_ *self)
{
  local_data_t *local_data;

#if DEBUG
  g_debug ("----- ENTER free (%s)", MODEL_NAME);
#endif

  /* Free the dynamically-allocated parts. */
  local_data = (local_data_t *) (self->model_data);
  RPT_free_reporting (local_data->num_units_infected);
  RPT_free_reporting (local_data->num_units_infected_by_cause);
  RPT_free_reporting (local_data->num_units_infected_by_prodtype);
  RPT_free_reporting (local_data->num_units_infected_by_cause_and_prodtype);
  RPT_free_reporting (local_data->cumul_num_units_infected);
  RPT_free_reporting (local_data->cumul_num_units_infected_by_cause);
  RPT_free_reporting (local_data->cumul_num_units_infected_by_prodtype);
  RPT_free_reporting (local_data->cumul_num_units_infected_by_cause_and_prodtype);
  RPT_free_reporting (local_data->num_animals_infected);
  RPT_free_reporting (local_data->num_animals_infected_by_cause);
  RPT_free_reporting (local_data->num_animals_infected_by_prodtype);
  RPT_free_reporting (local_data->num_animals_infected_by_cause_and_prodtype);
  RPT_free_reporting (local_data->cumul_num_animals_infected);
  RPT_free_reporting (local_data->cumul_num_animals_infected_by_cause);
  RPT_free_reporting (local_data->cumul_num_animals_infected_by_prodtype);
  RPT_free_reporting (local_data->cumul_num_animals_infected_by_cause_and_prodtype);
  RPT_free_reporting (local_data->first_det_u_inf);
  RPT_free_reporting (local_data->first_det_a_inf);
  RPT_free_reporting (local_data->ratio);

  g_free (local_data->nrecent_infections);

  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Returns a new infection monitor.
 */
spreadmodel_model_t *
new (scew_element * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  spreadmodel_model_t *self;
  local_data_t *local_data;
  scew_element *e;
  scew_list *ee, *iter;
  unsigned int n;
  const XML_Char *variable_name;
  RPT_frequency_t freq;
  gboolean success;
  gboolean broken_down;
  unsigned int i, j;      /* loop counters */
  char *prodtype_name;

#if DEBUG
  g_debug ("----- ENTER new (%s)", MODEL_NAME);
#endif

  self = g_new (spreadmodel_model_t, 1);
  local_data = g_new (local_data_t, 1);

  self->name = MODEL_NAME;
  self->events_listened_for = events_listened_for;
  self->nevents_listened_for = NEVENTS_LISTENED_FOR;
  self->outputs = g_ptr_array_sized_new (18);
  self->model_data = local_data;
  self->set_params = NULL;
  self->run = run;
  self->reset = reset;
  self->is_singleton = TRUE;
  self->is_listening_for = spreadmodel_model_is_listening_for;
  self->has_pending_actions = spreadmodel_model_answer_no;
  self->has_pending_infections = spreadmodel_model_answer_no;
  self->to_string = to_string;
  self->printf = spreadmodel_model_printf;
  self->fprintf = spreadmodel_model_fprintf;
  self->free = local_free;

  /* Make sure the right XML subtree was sent. */
  g_assert (strcmp (scew_element_name (params), MODEL_NAME) == 0);

  e = scew_element_by_name (params, "ratio-period");
  if (e != NULL)
    {
      local_data->nrecent_days = (int) round (PAR_get_time (e, &success));
      if (success == FALSE)
        {
          g_warning ("%s: setting ratio period to 2 weeks", MODEL_NAME);
          local_data->nrecent_days = 14;
        }
      if (local_data->nrecent_days < 1)
        {
          g_warning ("%s: ratio period cannot be less than 1, setting to 2 weeks", MODEL_NAME);
          local_data->nrecent_days = 14;
        }
    }
  else
    {
      g_warning ("%s: ratio period missing, setting 2 to weeks", MODEL_NAME);
      local_data->nrecent_days = 14;
    }

  local_data->num_units_infected =
    RPT_new_reporting ("infnUAll", RPT_integer, RPT_never);
  local_data->num_units_infected_by_cause =
    RPT_new_reporting ("infnU", RPT_group, RPT_never);
  local_data->num_units_infected_by_prodtype =
    RPT_new_reporting ("infnU", RPT_group, RPT_never);
  local_data->num_units_infected_by_cause_and_prodtype =
    RPT_new_reporting ("infnU", RPT_group, RPT_never);
  local_data->cumul_num_units_infected =
    RPT_new_reporting ("infcUAll", RPT_integer, RPT_never);
  local_data->cumul_num_units_infected_by_cause =
    RPT_new_reporting ("infcU", RPT_group, RPT_never);
  local_data->cumul_num_units_infected_by_prodtype =
    RPT_new_reporting ("infcU", RPT_group, RPT_never);
  local_data->cumul_num_units_infected_by_cause_and_prodtype =
    RPT_new_reporting ("infcU", RPT_group, RPT_never);
  local_data->num_animals_infected =
    RPT_new_reporting ("infnAAll", RPT_integer, RPT_never);
  local_data->num_animals_infected_by_cause =
    RPT_new_reporting ("infnA", RPT_group, RPT_never);
  local_data->num_animals_infected_by_prodtype =
    RPT_new_reporting ("infnA", RPT_group, RPT_never);
  local_data->num_animals_infected_by_cause_and_prodtype =
    RPT_new_reporting ("infnA", RPT_group, RPT_never);
  local_data->cumul_num_animals_infected =
    RPT_new_reporting ("infcAAll", RPT_integer, RPT_never);
  local_data->cumul_num_animals_infected_by_cause =
    RPT_new_reporting ("infcA", RPT_group, RPT_never);
  local_data->cumul_num_animals_infected_by_prodtype =
    RPT_new_reporting ("infcA", RPT_group, RPT_never);
  local_data->cumul_num_animals_infected_by_cause_and_prodtype =
    RPT_new_reporting ("infcA", RPT_group, RPT_never);
  local_data->first_det_u_inf =
    RPT_new_reporting ("firstDetUInfAll", RPT_integer, RPT_never);
  local_data->first_det_a_inf =
    RPT_new_reporting ("firstDetAInfAll", RPT_integer, RPT_never);
  local_data->ratio = RPT_new_reporting ("ratio", RPT_real, RPT_never);
  g_ptr_array_add (self->outputs, local_data->num_units_infected);
  g_ptr_array_add (self->outputs, local_data->num_units_infected_by_cause);
  g_ptr_array_add (self->outputs, local_data->num_units_infected_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->num_units_infected_by_cause_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_num_units_infected);
  g_ptr_array_add (self->outputs, local_data->cumul_num_units_infected_by_cause);
  g_ptr_array_add (self->outputs, local_data->cumul_num_units_infected_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_num_units_infected_by_cause_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->num_animals_infected);
  g_ptr_array_add (self->outputs, local_data->num_animals_infected_by_cause);
  g_ptr_array_add (self->outputs, local_data->num_animals_infected_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->num_animals_infected_by_cause_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_num_animals_infected);
  g_ptr_array_add (self->outputs, local_data->cumul_num_animals_infected_by_cause);
  g_ptr_array_add (self->outputs, local_data->cumul_num_animals_infected_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_num_animals_infected_by_cause_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->first_det_u_inf);
  g_ptr_array_add (self->outputs, local_data->first_det_a_inf);
  g_ptr_array_add (self->outputs, local_data->ratio);

  /* Set the reporting frequency for the output variables. */
  ee = scew_element_list_by_name (params, "output");
#if DEBUG
  g_debug ("%u output variables", scew_list_size(ee));
#endif
  for (iter = ee; iter != NULL; iter = scew_list_next(iter))
    {
      e = (scew_element *) scew_list_data (iter);
      variable_name = scew_element_contents (scew_element_by_name (e, "variable-name"));
      freq = RPT_string_to_frequency (scew_element_contents
                                      (scew_element_by_name (e, "frequency")));
      broken_down = PAR_get_boolean (scew_element_by_name (e, "broken-down"), &success);
      if (!success)
      	broken_down = FALSE;
      broken_down = broken_down || (g_strstr_len (variable_name, -1, "-by-") != NULL); 
      /* Starting at version 3.2 we accept either the old, verbose output
       * variable names or the new shorter ones. */
      if (strcmp (variable_name, "infnU") == 0
          || strncmp (variable_name, "num-units-infected", 18) == 0)
        {
          RPT_reporting_set_frequency (local_data->num_units_infected, freq);
          if (broken_down)
            {
              RPT_reporting_set_frequency (local_data->num_units_infected_by_cause, freq);
              RPT_reporting_set_frequency (local_data->num_units_infected_by_prodtype, freq);
              RPT_reporting_set_frequency (local_data->num_units_infected_by_cause_and_prodtype, freq);
            }
        }
      else if (strcmp (variable_name, "infcU") == 0
               || strncmp (variable_name, "cumulative-num-units-infected", 29) == 0)
        {
          RPT_reporting_set_frequency (local_data->cumul_num_units_infected, freq);
          if (broken_down)
            {
              RPT_reporting_set_frequency (local_data->cumul_num_units_infected_by_cause, freq);
              RPT_reporting_set_frequency (local_data->cumul_num_units_infected_by_prodtype, freq);
              RPT_reporting_set_frequency (local_data->cumul_num_units_infected_by_cause_and_prodtype, freq);
            }
        }
      else if (strcmp (variable_name, "infnA") == 0
               || strncmp (variable_name, "num-animals-infected", 20) == 0)
        {
          RPT_reporting_set_frequency (local_data->num_animals_infected, freq);
          if (broken_down)
            {
              RPT_reporting_set_frequency (local_data->num_animals_infected_by_cause, freq);
              RPT_reporting_set_frequency (local_data->num_animals_infected_by_prodtype, freq);
              RPT_reporting_set_frequency (local_data->num_animals_infected_by_cause_and_prodtype, freq);
            }
        }
      else if (strcmp (variable_name, "infcA") == 0
               || strncmp (variable_name, "cumulative-num-animals-infected", 31) == 0)
        {
          RPT_reporting_set_frequency (local_data->cumul_num_animals_infected, freq);
          if (broken_down)
            {
              RPT_reporting_set_frequency (local_data->cumul_num_animals_infected_by_cause, freq);
              RPT_reporting_set_frequency (local_data->cumul_num_animals_infected_by_prodtype, freq);
              RPT_reporting_set_frequency (local_data->cumul_num_animals_infected_by_cause_and_prodtype, freq);
            }
        }
      else if (strcmp (variable_name, "firstDetUInf") == 0)
        {
          RPT_reporting_set_frequency (local_data->first_det_u_inf, freq);
        }
      else if (strcmp (variable_name, "firstDetAInf") == 0)
        {
          RPT_reporting_set_frequency (local_data->first_det_a_inf, freq);
        }
      else if (strcmp (variable_name, "ratio") == 0)
        {
          RPT_reporting_set_frequency (local_data->ratio, freq);
        }
      else
        g_warning ("no output variable named \"%s\", ignoring", variable_name);        
    }
  scew_list_free (ee);

  /* Initialize the output variables. */
  local_data->production_types = units->production_type_names;
  n = local_data->production_types->len;
  for (i = 0; i < n; i++)
    {
      prodtype_name = (char *) g_ptr_array_index (local_data->production_types, i);
      RPT_reporting_add_integer1 (local_data->num_units_infected_by_prodtype, 0, prodtype_name);
      RPT_reporting_add_integer1 (local_data->cumul_num_units_infected_by_prodtype, 0, prodtype_name);
      RPT_reporting_add_integer1 (local_data->num_animals_infected_by_prodtype, 0, prodtype_name);
      RPT_reporting_add_integer1 (local_data->cumul_num_animals_infected_by_prodtype, 0, prodtype_name);
    }
  for (i = 0; i < SPREADMODEL_NCONTACT_TYPES; i++)
    {
      const char *cause;
      const char *drill_down_list[3] = { NULL, NULL, NULL };
      if ((SPREADMODEL_contact_type)i == SPREADMODEL_UnspecifiedInfectionType)
        continue;
      cause = SPREADMODEL_contact_type_abbrev[i]; 
      RPT_reporting_add_integer1 (local_data->num_units_infected_by_cause, 0, cause);
      RPT_reporting_add_integer1 (local_data->cumul_num_units_infected_by_cause, 0, cause);
      RPT_reporting_add_integer1 (local_data->num_animals_infected_by_cause, 0, cause);
      RPT_reporting_add_integer1 (local_data->cumul_num_animals_infected_by_cause, 0, cause);
      drill_down_list[0] = cause;
      for (j = 0; j < n; j++)
        {
          drill_down_list[1] = (char *) g_ptr_array_index (local_data->production_types, j);
          RPT_reporting_add_integer (local_data->num_units_infected_by_cause_and_prodtype, 0, drill_down_list);
          RPT_reporting_add_integer (local_data->cumul_num_units_infected_by_cause_and_prodtype, 0, drill_down_list);
          RPT_reporting_add_integer (local_data->num_animals_infected_by_cause_and_prodtype, 0, drill_down_list);
          RPT_reporting_add_integer (local_data->cumul_num_animals_infected_by_cause_and_prodtype, 0, drill_down_list);
        }
    }

  /* A list to store the number of new infections on each day for the recent
   * past. */
  local_data->nrecent_infections = g_new0 (unsigned int, local_data->nrecent_days * 2);
  local_data->recent_day_index = 0;

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file infection_monitor.c */
