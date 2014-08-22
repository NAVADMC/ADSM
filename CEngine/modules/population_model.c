/** @file population_model.c
 * A special module, always loaded, that encapsulates the list of units.  It
 * gathers requests for changes to units and disambiguates the results of
 * (potentially) conflicting requests.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date January 2005
 *
 * Copyright &copy; University of Guelph, 2005-2009
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
#define new population_model_new
#define run population_model_run
#define reset population_model_reset
#define events_listened_for population_model_events_listened_for
#define local_free population_model_free
#define handle_before_each_simulation_event population_model_handle_before_each_simulation_event
#define handle_midnight_event population_model_handle_midnight_event
#define handle_new_day_event population_model_handle_new_day_event
#define handle_declaration_of_vaccine_delay_event population_model_handle_declaration_of_vaccine_delay_event
#define handle_exposure_event population_model_handle_exposure_event
#define handle_vaccination_event population_model_handle_vaccination_event
#define handle_destruction_event population_model_handle_destruction_event
#define handle_end_of_day_event population_model_handle_end_of_day_event
#define EVT_free_event_as_GFunc population_model_EVT_free_event_as_GFunc

#include "module.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#if HAVE_STRINGS_H
#  include <strings.h>
#endif

#if HAVE_MATH_H
#  include <math.h>
#endif

#include "general.h"
#include "population_model.h"

#ifdef COGRID
double trunc ( double x )
{
  return floor( x );
}
#else
/* Temporary fix -- missing from math header file? */
double trunc (double);
#endif

#define MODEL_NAME "population-model"



#define NEVENTS_LISTENED_FOR 7
EVT_event_type_t events_listened_for[] = { EVT_BeforeEachSimulation, EVT_Midnight,
  EVT_DeclarationOfVaccineDelay,
  EVT_Exposure, EVT_Vaccination, EVT_Destruction,
  EVT_EndOfDay
};



/* Specialized information for this model. */
typedef struct
{
  GHashTable *adequate_exposures; /**< Gathers adequate exposures.  Keys are
    indices into the unit list (unsigned int), values are GSLists. */
  GHashTable *vacc_or_dest; /**< Gathers vaccinations and/or destructions that
    may conflict with infections.  Keys are units (UNT_unit_t *), values are
    unimportant (presence of a key is all we ever test). */
  GPtrArray *production_types;
  gboolean *vaccine_0_delay; /**< An array of flags, one for each production
    type.  The flag is TRUE if the delay to vaccine immunity for that
    production type is 0. */
}
local_data_t;



/**
 * Wraps EVT_free_event so that it can be used in GLib calls.
 *
 * @param data a pointer to an EVT_event_t structure, but cast to a gpointer.
 * @param user_data not used, pass NULL.
 */
void
EVT_free_event_as_GFunc (gpointer data, gpointer user_data)
{
  EVT_free_event ((EVT_event_t *) data);
}



/**
 * Responds to a declaration of vaccine delay by recording whether the delay is
 * 0 for this production type.  This information is needed so that this module
 * can handle a special case that occurs when the vaccine delay is 0.
 *
 * @param self the model.
 * @param event a declaration of vaccine delay event.
 */
void
handle_declaration_of_vaccine_delay_event (struct adsm_module_t_ *self,
                                           EVT_declaration_of_vaccine_delay_event_t *event)
{
  local_data_t *local_data;

#if DEBUG
  g_debug ("----- ENTER handle_declaration_of_vaccine_delay_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* We're only interested if the delay is 0. */
  if (event->delay == 0)
    {
      local_data->vaccine_0_delay[event->production_type] = TRUE;
#if DEBUG
      g_debug ("production type \"%s\" has 0 vaccine delay",
               event->production_type_name);
#endif
    }

#if DEBUG
  g_debug ("----- EXIT handle_declaration_of_vaccine_delay_event (%s)", MODEL_NAME);
#endif
  return;
}



/**
 * Before each simulation, this module sets up the units' initial states.
 *
 * @param self this module.
 * @param units the list of units.
 * @param queue for any new events this module generates.
 */
void
handle_before_each_simulation_event (struct adsm_module_t_ * self,
                                     UNT_unit_list_t * units,
                                     EVT_event_queue_t * queue)
{
  unsigned int nunits, i;
  UNT_unit_t *unit;
  EVT_event_t *event;

#if DEBUG
  g_debug ("----- ENTER handle_before_each_simulation_event (%s)", MODEL_NAME);
#endif

  /* Set each unit's initial state.  We don't need to go through the usual
   * conflict resolution steps here. */
  nunits = UNT_unit_list_length (units);
  for (i = 0; i < nunits; i++)
    {
      unit = UNT_unit_list_get (units, i);
      UNT_reset (unit);
      switch (unit->initial_state)
        {
        case Susceptible:
          break;
        case Latent:
        case InfectiousSubclinical:
        case InfectiousClinical:
        case NaturallyImmune:
          event = EVT_new_exposure_event (NULL, unit, 0, ADSM_InitiallyInfected,
                                          /* traceable = */ FALSE,
                                          /* adequate = */ TRUE,
                                          /* delay = */ 0);
          event->u.exposure.override_initial_state = unit->initial_state;
          event->u.exposure.override_days_in_state = unit->days_in_initial_state;
          event->u.exposure.override_days_left_in_state = unit->days_left_in_initial_state;
          EVT_event_enqueue (queue, event);
          break;
        case VaccineImmune:
          event = EVT_new_inprogress_immunity_event (unit, 0, "Ini",
                                                     unit->initial_state,
                                                     unit->days_in_initial_state,
                                                     unit->days_left_in_initial_state);
          EVT_event_enqueue (queue, event);
          break;
        case Destroyed:
          UNT_destroy (unit);
          event = EVT_new_destruction_event (unit, 0, "Ini", -1);
          EVT_event_enqueue (queue, event);
          break;
        default:
          g_assert_not_reached ();
        }
    } /* end of loop over units */

#if DEBUG
  g_debug ("----- EXIT handle_before_each_simulation_event (%s)", MODEL_NAME);
#endif

  return;
} 



/**
 * Responds to a "midnight" event by making the units change state.
 *
 * @param self this module.
 * @param event the "midnight" event.
 * @param units the list of units.
 * @param rng a random number generator.
 * @param queue for any new events this module creates.
 */
void
handle_midnight_event (struct adsm_module_t_ *self,
                       EVT_midnight_event_t * event,
                       UNT_unit_list_t * units,
                       RAN_gen_t * rng,
                       EVT_event_queue_t * queue)
{
  local_data_t *local_data;
  unsigned int nunits, i;
  UNT_unit_t *unit;

#if DEBUG
  g_debug ("----- ENTER handle_midnight_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  nunits = UNT_unit_list_length (units);
  for (i = 0; i < nunits; i++)
    {
      unit = UNT_unit_list_get (units, i);
      /* _iteration is a global variable defined in general.c */
      UNT_step (unit, _iteration.infectious_units);
    }

#if DEBUG
  g_debug ("----- EXIT handle_midnight_event (%s)", MODEL_NAME);
#endif
}



/**
 * Responds to an adequate exposure event by recording it.
 *
 * @param self the model.
 * @param event an exposure event.
 */
void
handle_exposure_event (struct adsm_module_t_ *self, EVT_event_t * event)
{
  local_data_t *local_data;
  UNT_unit_t *unit;

#if DEBUG
  g_debug ("----- ENTER handle_exposure_event (%s)", MODEL_NAME);
#endif

  if (event->u.exposure.adequate == TRUE)
    {
      local_data = (local_data_t *) (self->model_data);
      unit = event->u.exposure.exposed_unit;
      g_hash_table_insert (local_data->adequate_exposures,
                           GUINT_TO_POINTER(unit->index),
                           g_slist_prepend (g_hash_table_lookup (local_data->adequate_exposures, GUINT_TO_POINTER(unit->index)),
                                            EVT_clone_event (event)));
      #if DEBUG
        g_debug ("now %u adequate exposures to unit \"%s\"",
                 g_slist_length (g_hash_table_lookup (local_data->adequate_exposures, GUINT_TO_POINTER(unit->index))), unit->official_id);
      #endif
    }

#if DEBUG
  g_debug ("----- EXIT handle_exposure_event (%s)", MODEL_NAME);
#endif

}



/**
 * Responds to a vaccination event by recording that the unit was vaccinated,
 * but only if units of that production type have a zero delay to immunity.
 *
 * @param self the model.
 * @param event a vaccination event.
 */
void
handle_vaccination_event (struct adsm_module_t_ * self,
                          EVT_vaccination_event_t * event)
{
  local_data_t *local_data;
  UNT_unit_t *unit;

#if DEBUG
  g_debug ("----- ENTER handle_vaccination_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;
  if (local_data->vaccine_0_delay[unit->production_type] == TRUE)
    {
#if DEBUG
      /* There should never be more than one Vaccination event, or both
       * Vaccination and Destruction events, for a unit on a single day. */
      g_assert (g_hash_table_lookup (local_data->vacc_or_dest, unit) == NULL);
#endif
      g_hash_table_insert (local_data->vacc_or_dest, unit, unit);
    }

#if DEBUG
  g_debug ("----- EXIT handle_vaccination_event (%s)", MODEL_NAME);
#endif
}



/**
 * Responds to a destruction event by recording the unit that was destroyed.
 *
 * @param self the model.
 * @param event a destruction event.
 */
void
handle_destruction_event (struct adsm_module_t_ * self,
                          EVT_destruction_event_t * event)
{
  local_data_t *local_data;
  UNT_unit_t *unit;

#if DEBUG
  g_debug ("----- ENTER handle_destruction_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;
#if DEBUG
  /* There should never be more than one Destruction event, or both Vaccination
   * and Destruction events, for a unit on a single day. */
  g_assert (g_hash_table_lookup (local_data->vacc_or_dest, unit) == NULL);
#endif
  g_hash_table_insert (local_data->vacc_or_dest, unit, unit);

#if DEBUG
  g_debug ("----- EXIT handle_destruction_event (%s)", MODEL_NAME);
#endif
}



/**
 * A struct to hold arguments for the function resolve_conflicts below.
 * Because that function is typed as a GHFunc, arguments need to be grouped
 * together and passed as a single pointer named user_data.
 */
typedef struct
{
  UNT_unit_list_t *units;
  GHashTable *vacc_or_dest;
  RAN_gen_t *rng;
  EVT_event_queue_t *queue;
}
resolve_conflicts_args_t;



/**
 * Resolve any conflicts between infection and vaccination or destruction for a
 * single unit.  This function is typed as a GHFunc so that it can be called
 * for each key (unit index) in the adequate_exposures table.
 *
 * @param key a unit (UNT_unit_t * cast to a gpointer).
 * @param value a list of attempts to infect (GSList * in which each list node
 *   contains an EVT_event_t *, cast to a gpointer).
 * @param user_data pointer to a resolve_conflicts_args_t structure.
 */  
void
resolve_conflicts (gpointer key, gpointer value, gpointer user_data)
{
  resolve_conflicts_args_t *args;
  UNT_unit_t *unit;
  GSList *adequate_exposures;
  unsigned int n;
  unsigned int attempt_num;
  EVT_event_t *attempt, *e;

  args = (resolve_conflicts_args_t *) user_data;
  unit = UNT_unit_list_get (args->units, GPOINTER_TO_UINT(key));
  adequate_exposures = (GSList *) value;

  /* If vaccination (with 0 delay to immunity) or destruction has occurred,
   * cancel the infection with probability 1/2.  Note that vaccination and
   * destruction will not both occur. */
  if (g_hash_table_lookup (args->vacc_or_dest, unit) != NULL
      && RAN_num (args->rng) < 0.5)
    {
#if DEBUG
      g_debug ("vaccination or destruction cancels infection for unit \"%s\"", unit->official_id);
#endif
      ;
    }
  else if (!unit->in_disease_cycle)
    {
      /* An infection is going to go ahead.  If there is more than one
       * competing cause of infection, choose one randomly. */
      n = g_slist_length (adequate_exposures);
      if (n > 1)
        {
          attempt_num = (unsigned int) trunc (RAN_num (args->rng) * n);
          attempt = (EVT_event_t *) (g_slist_nth (adequate_exposures, attempt_num)->data);
        }
      else
        {
          attempt = (EVT_event_t *) (adequate_exposures->data);
        }
      e = EVT_new_infection_event (attempt->u.exposure.exposing_unit,
                                   unit,
                                   attempt->u.exposure.day,
                                   attempt->u.exposure.contact_type);
      e->u.infection.override_initial_state =
        attempt->u.exposure.override_initial_state;
      e->u.infection.override_days_in_state =
        attempt->u.exposure.override_days_in_state;
      e->u.infection.override_days_left_in_state =
        attempt->u.exposure.override_days_left_in_state;
      EVT_event_enqueue (args->queue, e);
    }
  /* Free the list of attempts to infect this unit.  This leaves a dangling
   * pointer in the hash table, but that's OK, because the hash table will be
   * cleared out at the end of handle_end_of_day_event. */
  g_slist_foreach (adequate_exposures, EVT_free_event_as_GFunc, NULL);
  g_slist_free (adequate_exposures);
  return;
}



/**
 * Responds to an end of day event by resolving competing requests for changes
 * and making one unambiguous change to the unit.
 *
 * @param self the model.
 * @param units the list of units.
 * @param rng a random number generator.
 * @param queue for any new events the model creates.
 */
void
handle_end_of_day_event (struct adsm_module_t_ *self, UNT_unit_list_t * units,
                         RAN_gen_t * rng, EVT_event_queue_t * queue)
{
  local_data_t *local_data;
  resolve_conflicts_args_t resolve_conflicts_args;

#if DEBUG
  g_debug ("----- ENTER handle_end_of_day_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  resolve_conflicts_args.units = units;
  resolve_conflicts_args.vacc_or_dest = local_data->vacc_or_dest;
  resolve_conflicts_args.rng = rng;
  resolve_conflicts_args.queue = queue;
  g_hash_table_foreach (local_data->adequate_exposures, resolve_conflicts, &resolve_conflicts_args);
  /* Each value (list of attempts to infect a particular unit) in the
   * adequate_exposures table got freed by resolve_conflicts.  But we still
   * need to clear all the keys (unit indices) from that table. */
  g_hash_table_remove_all (local_data->adequate_exposures);
  g_hash_table_remove_all (local_data->vacc_or_dest);

#if DEBUG
  g_debug ("----- EXIT handle_end_of_day_event (%s)", MODEL_NAME);
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
    case EVT_BeforeEachSimulation:
      handle_before_each_simulation_event (self, units, queue);
      break;
    case EVT_Midnight:
      handle_midnight_event (self, &(event->u.midnight), units, rng, queue);
      break;
    case EVT_DeclarationOfVaccineDelay:
      handle_declaration_of_vaccine_delay_event (self, &(event->u.declaration_of_vaccine_delay));
      break;
    case EVT_Exposure:
      handle_exposure_event (self, event);
      break;
    case EVT_Vaccination:
      handle_vaccination_event (self, &(event->u.vaccination));
      break;
    case EVT_Destruction:
      handle_destruction_event (self, &(event->u.destruction));
      break;
    case EVT_EndOfDay:
      handle_end_of_day_event (self, units, rng, queue);
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
 * Frees this model.  Does not free the production type name.
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

  g_hash_table_destroy (local_data->adequate_exposures);
  g_hash_table_destroy (local_data->vacc_or_dest);

  /* Free the list of vaccine delay flags. */
  g_free (local_data->vaccine_0_delay);

  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Returns a new population model.
 */
adsm_module_t *
new (sqlite3 * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  adsm_module_t *self;
  local_data_t *local_data;

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
  self->to_string = adsm_module_to_string_default;
  self->printf = adsm_model_printf;
  self->fprintf = adsm_model_fprintf;
  self->free = local_free;

  local_data->adequate_exposures = g_hash_table_new (g_direct_hash, g_direct_equal);
  local_data->vacc_or_dest = g_hash_table_new (g_direct_hash, g_direct_equal);
  local_data->production_types = units->production_type_names;
  local_data->vaccine_0_delay = g_new0 (gboolean, units->production_type_names->len);

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file population_model.c */
