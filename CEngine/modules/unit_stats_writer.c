/** @file unit_stats_writer.c
 * Writes out a table giving the final state of each unit in comma-separated
 * values (csv) format.
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
#define new unit_stats_writer_new
#define run unit_stats_writer_run
#define to_string unit_stats_writer_to_string
#define local_free unit_stats_writer_free
#define handle_before_each_simulation_change_event unit_stats_writer_handle_before_each_simulation_event
#define handle_unit_state_change_event unit_stats_writer_handle_unit_state_change_event
#define handle_request_for_zone_focus_event unit_stats_writer_handle_request_for_zone_focus_event
#define handle_vaccination_event unit_stats_writer_handle_vaccination_event
#define handle_destruction_event unit_stats_writer_handle_destruction_event
#define handle_end_of_day2_event unit_stats_writer_handle_end_of_day2_event

#include "module.h"
#include "module_util.h"

#include <unistd.h>

#if STDC_HEADERS
#  include <string.h>
#endif

#if HAVE_MATH_H
#  include <math.h>
#endif

#if HAVE_STRINGS_H
#  include <strings.h>
#endif

#include "unit_stats_writer.h"

#if !HAVE_ROUND && HAVE_RINT
#  define round rint
#endif

double round (double x);

/** This must match an element name in the DTD. */
#define MODEL_NAME "unit-stats-writer"



/* These valued are or'd together to store what happened to the unit during the
 * iteration. */
#define WAS_INFECTED 1 << 0
#define WAS_ZONE_FOCUS 1 << 1
#define WAS_VACCINATED 1 << 2
#define WAS_DESTROYED 1 << 3



/* Specialized information for this module. */
typedef struct
{
  sqlite3 *db; /* Keeps a pointer to the database for writing. */
  int run_number;
  GHashTable *what_happened; /* Key = unit (UNT_unit_t *), value = an integer,
    converted using GUINT_TO_POINTER, storing what happened to the unit during
    the iteration. */
}
local_data_t;



/**
 * Before each simulation, this module deletes any records left over from a
 * previous iteration.
 *
 * @param self this module.
 */
void
handle_before_each_simulation_event (struct adsm_module_t_ *self)
{
  local_data_t *local_data;

  #if DEBUG
    g_debug ("----- ENTER handle_before_each_simulation_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);
  g_hash_table_remove_all (local_data->what_happened);

  #if DEBUG
    g_debug ("----- EXIT handle_before_each_simulation_event (%s)", MODEL_NAME);
  #endif

  return;
}



/**
 * Responds to a Unit State Change to an infected state by recording that the
 * unit was infected during this iteration.
 *
 * @param self this module.
 * @param event a Unit State Change event.
 */
void
handle_unit_state_change_event (struct adsm_module_t_ * self,
                                EVT_unit_state_change_event_t * event)
{
  local_data_t *local_data;
  gpointer p;
  guint what_happened = 0;

  #if DEBUG
    g_debug ("----- ENTER handle_unit_state_change_event (%s)", MODEL_NAME);
  #endif

  /* We are only interested in state changes to an infected state. */
  if (event->new_state == Latent
      || event->new_state == InfectiousSubclinical
      || event->new_state == InfectiousClinical)
    {
      local_data = (local_data_t *) (self->model_data);
      p = g_hash_table_lookup (local_data->what_happened, event->unit);
      if (p != NULL)
        {
          what_happened = GPOINTER_TO_UINT(p);
        }
      g_hash_table_replace (local_data->what_happened, event->unit,
                            GUINT_TO_POINTER(what_happened | WAS_INFECTED));
    }

  #if DEBUG
    g_debug ("----- EXIT handle_unit_state_change_event (%s)", MODEL_NAME);
  #endif

  return;
}



/**
 * Responds to a RequestForZoneFocus event by recording that a zone was created
 * around the unit during this iteration.
 *
 * @param self this module.
 * @param event a Request For Zone Focus event.
 */
void
handle_request_for_zone_focus_event (struct adsm_module_t_ * self,
                                     EVT_request_for_zone_focus_event_t * event)
{
  local_data_t *local_data;
  gpointer p;
  guint what_happened = 0;

  #if DEBUG
    g_debug ("----- ENTER handle_request_for_zone_focus_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);
  p = g_hash_table_lookup (local_data->what_happened, event->unit);
  if (p != NULL)
    {
      what_happened = GPOINTER_TO_UINT(p);
    }
  g_hash_table_replace (local_data->what_happened, event->unit,
                        GUINT_TO_POINTER(what_happened | WAS_ZONE_FOCUS));

  #if DEBUG
    g_debug ("----- EXIT handle_request_for_zone_focus_event (%s)", MODEL_NAME);
  #endif

  return;
}



/**
 * Responds to a Vaccination event by recording that the unit was vaccinated
 * during this iteration.
 *
 * @param self this module.
 * @param event a Vaccination event.
 */
void
handle_vaccination_event (struct adsm_module_t_ * self,
                          EVT_vaccination_event_t * event)
{
  local_data_t *local_data;
  gpointer p;
  guint what_happened = 0;

  #if DEBUG
    g_debug ("----- ENTER handle_vaccination_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);
  p = g_hash_table_lookup (local_data->what_happened, event->unit);
  if (p != NULL)
    {
      what_happened = GPOINTER_TO_UINT(p);
    }
  g_hash_table_replace (local_data->what_happened, event->unit,
                        GUINT_TO_POINTER(what_happened | WAS_VACCINATED));

  #if DEBUG
    g_debug ("----- EXIT handle_vaccination_event (%s)", MODEL_NAME);
  #endif

  return;
}



/**
 * Responds to a Destruction event by recording that the unit was destroyed
 * during this iteration.
 *
 * @param self this module.
 * @param event a Destruction event.
 */
void
handle_destruction_event (struct adsm_module_t_ * self,
                          EVT_destruction_event_t * event)
{
  local_data_t *local_data;
  gpointer p;
  guint what_happened = 0;

  #if DEBUG
    g_debug ("----- ENTER handle_destruction_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);
  p = g_hash_table_lookup (local_data->what_happened, event->unit);
  if (p != NULL)
    {
      what_happened = GPOINTER_TO_UINT(p);
    }
  g_hash_table_replace (local_data->what_happened, event->unit,
                        GUINT_TO_POINTER(what_happened | WAS_DESTROYED));

  #if DEBUG
    g_debug ("----- EXIT handle_destruction_event (%s)", MODEL_NAME);
  #endif

  return;
}



/**
 * Updates the record for one unit in the database.
 *
 * @param key a unit
 * @param value an integer changed to a pointer using GUINT_TO_POINTER
 * @param an open database
 */
static void
update_what_happened (gpointer key, gpointer value, gpointer user_data)
{
  UNT_unit_t *unit;
  guint what_happened;
  sqlite3 *db;
  gchar *sql;
  char *sqlerr = NULL;

  unit = (UNT_unit_t *) key;
  what_happened = GPOINTER_TO_UINT(value);
  db = (sqlite3 *) user_data;
  sql =
    g_strdup_printf ("UPDATE Results_unitstats "
                     " SET cumulative_infected=cumulative_infected+%u,"
                     " cumulative_zone_focus=cumulative_zone_focus+%u,"
                     " cumulative_vaccinated=cumulative_vaccinated+%u,"
                     " cumulative_destroyed=cumulative_destroyed+%u"
                     " WHERE unit_id=%u",
                     (what_happened & WAS_INFECTED) ? 1 : 0,
                     (what_happened & WAS_ZONE_FOCUS) ? 1 : 0,
                     (what_happened & WAS_VACCINATED) ? 1 : 0,
                     (what_happened & WAS_DESTROYED) ? 1 : 0,
                     unit->db_id);
  sqlite3_exec (db, sql, NULL, NULL, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }
  g_free (sql);

  return;
}



/**
 * Responds to an end of day event on the last day of the simulation by writing
 * what happened to each unit to the database.
 *
 * @param self this module.
 * @param event an end of day 2 event.
 */
void
handle_end_of_day2_event (struct adsm_module_t_ * self,
                          EVT_end_of_day2_event_t * event)
{
  local_data_t *local_data;
  char *sqlerr = NULL;

  #if DEBUG
    g_debug ("----- ENTER handle_end_of_day2_event (%s)", MODEL_NAME);
  #endif

  if (event->done && event->day > 0)
    {
      local_data = (local_data_t *) (self->model_data);

      sqlite3_exec (local_data->db, "BEGIN TRANSACTION", NULL, NULL, &sqlerr);
      if (sqlerr)
        {
          g_error ("%s", sqlerr);
        }

      g_hash_table_foreach (local_data->what_happened, update_what_happened,
                            local_data->db);

      sqlite3_exec (local_data->db, "COMMIT TRANSACTION", NULL, NULL, &sqlerr);
      if (sqlerr)
        {
         g_error ("%s", sqlerr);
        }
    }

  #if DEBUG
    g_debug ("----- EXIT handle_end_of_day2_event (%s)", MODEL_NAME);
  #endif

  return;
}



/**
 * Runs this module.
 *
 * @param self this module.
 * @param units a list of units.
 * @param zones a list of zones.
 * @param event the event that caused this module to run.
 * @param rng a random number generator.
 * @param queue for any new events this module creates.
 */
void
run (struct adsm_module_t_ *self, UNT_unit_list_t * units,
     ZON_zone_list_t * zones, EVT_event_t * event, RAN_gen_t * rng, EVT_event_queue_t * queue)
{
  #if DEBUG
    g_debug ("----- ENTER run (%s)", MODEL_NAME);
  #endif

  switch (event->type)
    {
    case EVT_BeforeEachSimulation:
      handle_before_each_simulation_event (self);
      break;
    case EVT_UnitStateChange:
      handle_unit_state_change_event (self, &(event->u.unit_state_change));
      break;
    case EVT_RequestForZoneFocus:
      handle_request_for_zone_focus_event (self, &(event->u.request_for_zone_focus));
      break;
    case EVT_Vaccination:
      handle_vaccination_event (self, &(event->u.vaccination));
      break;
    case EVT_Destruction:
      handle_destruction_event (self, &(event->u.destruction));
      break;
    case EVT_EndOfDay2:
      handle_end_of_day2_event (self, &(event->u.end_of_day2));
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

  local_data = (local_data_t *) (self->model_data);
  s = g_string_new (NULL);
  g_string_sprintf (s, "<%s>", MODEL_NAME);

  /* don't return the wrapper object */
  return g_string_free (s, /* free_segment = */ FALSE);
}



/**
 * Frees this module.
 *
 * @param self this module.
 */
void
local_free (struct adsm_module_t_ *self)
{
  local_data_t *local_data;

  #if DEBUG
    g_debug ("----- ENTER free (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);
  g_hash_table_destroy (local_data->what_happened);

  #if DEBUG
    g_debug ("----- EXIT free (%s)", MODEL_NAME);
  #endif
  
  return;
}



/**
 * Returns a new unit stats writer.
 */
adsm_module_t *
new (sqlite3 * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  adsm_module_t *self;
  local_data_t *local_data;
  EVT_event_type_t events_listened_for[] = {
    EVT_BeforeEachSimulation,
    EVT_UnitStateChange,
    EVT_RequestForZoneFocus,
    EVT_Vaccination,
    EVT_Destruction,
    EVT_EndOfDay2,
    0
  };

  #if DEBUG
    g_debug ("----- ENTER new (%s)", MODEL_NAME);
  #endif

  self = g_new (adsm_module_t, 1);
  local_data = g_new (local_data_t, 1);

  self->name = MODEL_NAME;
  self->events_listened_for = adsm_setup_events_listened_for (events_listened_for);
  self->outputs = g_ptr_array_sized_new (0);
  self->model_data = local_data;
  self->run = run;
  self->is_listening_for = adsm_model_is_listening_for;
  self->has_pending_actions = adsm_model_answer_no;
  self->has_pending_infections = adsm_model_answer_no;
  self->to_string = to_string;
  self->printf = adsm_model_printf;
  self->fprintf = adsm_model_fprintf;
  self->free = local_free;

  local_data->db = params;
  local_data->what_happened = g_hash_table_new (g_direct_hash, g_direct_equal);

  #if DEBUG
    g_debug ("----- EXIT new (%s)", MODEL_NAME);
  #endif

  return self;
}

/* end of file unit_stats_writer.c */
