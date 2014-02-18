/** @file destruction_monitor.c
 * Tracks the number of and reasons for destructions.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @version 0.1
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
#define new destruction_monitor_new
#define run destruction_monitor_run
#define reset destruction_monitor_reset
#define events_listened_for destruction_monitor_events_listened_for
#define is_listening_for destruction_monitor_is_listening_for
#define has_pending_actions destruction_monitor_has_pending_actions
#define has_pending_infections destruction_monitor_has_pending_infections
#define to_string destruction_monitor_to_string
#define local_printf destruction_monitor_printf
#define local_fprintf destruction_monitor_fprintf
#define local_free destruction_monitor_free
#define handle_before_any_simulations_event destruction_monitor_handle_before_any_simulations_event
#define handle_new_day_event destruction_monitor_handle_new_day_event
#define handle_declaration_of_destruction_reasons_event destruction_monitor_handle_declaration_of_destruction_reasons_event
#define handle_destruction_event destruction_monitor_handle_destruction_event

#include "module.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#include "destruction_monitor.h"

#include "spreadmodel.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "destruction-monitor"



#define NEVENTS_LISTENED_FOR 4
EVT_event_type_t events_listened_for[] =
  { EVT_BeforeAnySimulations, EVT_NewDay, EVT_DeclarationOfDestructionReasons, EVT_Destruction };



/** Specialized information for this model. */
typedef struct
{
  GPtrArray *production_types;
  RPT_reporting_t *destructions;
  RPT_reporting_t *destruction_occurred;
  RPT_reporting_t *first_destruction;
  RPT_reporting_t *first_destruction_by_reason;
  RPT_reporting_t *first_destruction_by_prodtype;
  RPT_reporting_t *first_destruction_by_reason_and_prodtype;
  RPT_reporting_t *num_units_destroyed;
  RPT_reporting_t *num_units_destroyed_by_reason;
  RPT_reporting_t *num_units_destroyed_by_prodtype;
  RPT_reporting_t *num_units_destroyed_by_reason_and_prodtype;
  RPT_reporting_t *cumul_num_units_destroyed;
  RPT_reporting_t *cumul_num_units_destroyed_by_reason;
  RPT_reporting_t *cumul_num_units_destroyed_by_prodtype;
  RPT_reporting_t *cumul_num_units_destroyed_by_reason_and_prodtype;
  RPT_reporting_t *num_animals_destroyed;
  RPT_reporting_t *num_animals_destroyed_by_reason;
  RPT_reporting_t *num_animals_destroyed_by_prodtype;
  RPT_reporting_t *num_animals_destroyed_by_reason_and_prodtype;
  RPT_reporting_t *cumul_num_animals_destroyed;
  RPT_reporting_t *cumul_num_animals_destroyed_by_reason;
  RPT_reporting_t *cumul_num_animals_destroyed_by_prodtype;
  RPT_reporting_t *cumul_num_animals_destroyed_by_reason_and_prodtype;
  GString *target;              /* a temporary string used repeatedly. */
  gboolean reasons_declared;
  gboolean first_day;
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
 * On each new day, zero the daily counts of destructions.
 *
 * @param self the model.
 * @param event a new day event.
 */
void
handle_new_day_event (struct spreadmodel_model_t_ *self, EVT_new_day_event_t * event)
{
  local_data_t *local_data;

#if DEBUG
  g_debug ("----- ENTER handle_new_day_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* Zero the daily counts. */
  if (event->day > 1)
    {
      RPT_reporting_zero (local_data->destructions);
      RPT_reporting_zero (local_data->num_units_destroyed);
      RPT_reporting_zero (local_data->num_units_destroyed_by_reason);
      RPT_reporting_zero (local_data->num_units_destroyed_by_prodtype);
      RPT_reporting_zero (local_data->num_units_destroyed_by_reason_and_prodtype);
      RPT_reporting_zero (local_data->num_animals_destroyed);
      RPT_reporting_zero (local_data->num_animals_destroyed_by_reason);
      RPT_reporting_zero (local_data->num_animals_destroyed_by_prodtype);
      RPT_reporting_zero (local_data->num_animals_destroyed_by_reason_and_prodtype);
    }

  /* If no reasons for destruction have been declared, turn off the first-
   * destruction-by-reason output variables. */
  if (local_data->first_day == TRUE)
    {
      local_data->first_day = FALSE;
      if (local_data->reasons_declared == FALSE)
        {
           RPT_reporting_set_frequency (local_data->first_destruction_by_reason, RPT_never);
           RPT_reporting_set_frequency (local_data->first_destruction_by_reason_and_prodtype, RPT_never);
        }
    }

#if DEBUG
  g_debug ("----- EXIT handle_new_day_event (%s)", MODEL_NAME);
#endif
}



/**
 * Responds to a declaration of destruction reasons by recording the potential
 * reasons for destruction.
 *
 * @param self the model.
 * @param event a declaration of destruction reasons event.
 */
void
handle_declaration_of_destruction_reasons_event (struct spreadmodel_model_t_ *self,
                                                 EVT_declaration_of_destruction_reasons_event_t *
                                                 event)
{
  local_data_t *local_data;
  unsigned int n, i, j;
  const char *reason;
  const char *drill_down_list[3] = { NULL, NULL, NULL };

#if DEBUG
  g_debug ("----- ENTER handle_declaration_of_destruction_reasons_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* If any potential reason is not already present in our reporting variables,
   * add it, with an initial count of 0 destructions. */
  n = event->reasons->len;
  if (n > 0)
    local_data->reasons_declared = TRUE;
  for (i = 0; i < n; i++)
    {
      reason = (char *) g_ptr_array_index (event->reasons, i);
      RPT_reporting_append_text1 (local_data->destructions, "", reason);
      /* Two function calls for the first_destruction variable: one to
       * establish the type of the sub-variable (it's an integer), and one to
       * clear it to "null" (it has no meaningful value until a destruction
       * occurs). */
      RPT_reporting_add_integer1 (local_data->first_destruction_by_reason, 0, reason);
      RPT_reporting_set_null1 (local_data->first_destruction_by_reason, reason);
      RPT_reporting_add_integer1 (local_data->num_units_destroyed_by_reason, 0, reason);
      RPT_reporting_add_integer1 (local_data->cumul_num_units_destroyed_by_reason, 0, reason);
      RPT_reporting_add_integer1 (local_data->num_animals_destroyed_by_reason, 0, reason);
      RPT_reporting_add_integer1 (local_data->cumul_num_animals_destroyed_by_reason, 0, reason);

      drill_down_list[0] = reason;
      for (j = 0; j < local_data->production_types->len; j++)
        {
          drill_down_list[1] = (char *) g_ptr_array_index (local_data->production_types, j);
          RPT_reporting_add_integer (local_data->first_destruction_by_reason_and_prodtype, 0,
                                     drill_down_list);
          RPT_reporting_set_null (local_data->first_destruction_by_reason_and_prodtype,
                                  drill_down_list);
          RPT_reporting_add_integer (local_data->num_units_destroyed_by_reason_and_prodtype, 0,
                                     drill_down_list);
          RPT_reporting_add_integer (local_data->cumul_num_units_destroyed_by_reason_and_prodtype, 0,
                                     drill_down_list);
          RPT_reporting_add_integer (local_data->num_animals_destroyed_by_reason_and_prodtype, 0,
                                     drill_down_list);
          RPT_reporting_add_integer (local_data->cumul_num_animals_destroyed_by_reason_and_prodtype, 0,
                                     drill_down_list);
        }
    }

#if DEBUG
  g_debug ("----- EXIT handle_declaration_of_destruction_reasons_event (%s)", MODEL_NAME);
#endif
}



/**
 * Responds to a destruction by recording it.
 *
 * @param self the model.
 * @param event a destruction event.
 */
void
handle_destruction_event (struct spreadmodel_model_t_ *self, EVT_destruction_event_t * event)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  char *peek;
  gboolean first_of_cause;
  const char *drill_down_list[3] = { NULL, NULL, NULL };
  UNT_control_t update;

#if DEBUG
  g_debug ("----- ENTER handle_destruction_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;

  peek = RPT_reporting_get_text1 (local_data->destructions, event->reason);
  first_of_cause = (peek == NULL) || (strlen (peek) == 0);

  g_string_printf (local_data->target, first_of_cause ? "%u" : ",%u", unit->index);
  RPT_reporting_append_text1 (local_data->destructions, local_data->target->str, event->reason);

  update.unit_index = unit->index;
  update.day_commitment_made = event->day_commitment_made;
  
  if( 0 == strcmp( "Det", event->reason ) )
    update.reason = SPREADMODEL_ControlDetection;
  else if( 0 == strcmp( "Ring", event->reason ) )
    update.reason = SPREADMODEL_ControlRing;
  else if( 0 == strcmp( "DirFwd", event->reason ) )
    update.reason = SPREADMODEL_ControlTraceForwardDirect;
  else if( 0 == strcmp( "IndFwd", event->reason ) )
    update.reason = SPREADMODEL_ControlTraceForwardIndirect;     
  else if( 0 == strcmp( "DirBack", event->reason ) )
    update.reason = SPREADMODEL_ControlTraceBackDirect;
  else if( 0 == strcmp( "IndBack", event->reason ) )
    update.reason = SPREADMODEL_ControlTraceBackIndirect;
  else if( 0 == strcmp( "Ini", event->reason ) )
    update.reason = SPREADMODEL_ControlInitialState;
  else
    {
      g_error( "Unrecognized reason for destruction (%s) in handle_destruction_event", event->reason );
      update.reason = 0;   
    }      
  
#ifdef USE_SC_GUILIB
  sc_destroy_unit( event->day, unit, update );
#else
  if (NULL != spreadmodel_destroy_unit)
    {
      spreadmodel_destroy_unit (update);
    }
#endif  

  drill_down_list[0] = event->reason;
  drill_down_list[1] = unit->production_type_name;
  /* Initially destroyed units do not count as the first destruction. */
  if (strcmp (event->reason, "Ini") != 0)
    {
      if (RPT_reporting_is_null (local_data->first_destruction, NULL))
        {
          RPT_reporting_set_integer (local_data->first_destruction, event->day, NULL);
          RPT_reporting_set_integer (local_data->destruction_occurred, 1, NULL);
        }
      if (RPT_reporting_is_null1 (local_data->first_destruction_by_reason, event->reason))
        RPT_reporting_set_integer1 (local_data->first_destruction_by_reason, event->day, event->reason);
      if (RPT_reporting_is_null1 (local_data->first_destruction_by_prodtype, unit->production_type_name))
        RPT_reporting_set_integer1 (local_data->first_destruction_by_prodtype, event->day, unit->production_type_name);  
      if (RPT_reporting_is_null (local_data->first_destruction_by_reason_and_prodtype, drill_down_list))
        RPT_reporting_set_integer (local_data->first_destruction_by_reason_and_prodtype, event->day, drill_down_list);

      /* Initially destroyed units also are not included in many of the counts.
       * They will not be part of desnUAll or desnU broken down by production
       * type.  They will be part of desnUIni and desnUIni broken down by
       * production type. */
      RPT_reporting_add_integer  (local_data->num_units_destroyed, 1, NULL);
      RPT_reporting_add_integer1 (local_data->num_units_destroyed_by_prodtype, 1, unit->production_type_name);
      RPT_reporting_add_integer  (local_data->num_animals_destroyed, unit->size, NULL);
      RPT_reporting_add_integer1 (local_data->num_animals_destroyed_by_prodtype, unit->size, unit->production_type_name);
      RPT_reporting_add_integer  (local_data->cumul_num_units_destroyed, 1, NULL);
      RPT_reporting_add_integer1 (local_data->cumul_num_units_destroyed_by_prodtype, 1, unit->production_type_name);
      RPT_reporting_add_integer  (local_data->cumul_num_animals_destroyed, unit->size, NULL);
      RPT_reporting_add_integer1 (local_data->cumul_num_animals_destroyed_by_prodtype, unit->size, unit->production_type_name);
    }
  RPT_reporting_add_integer1 (local_data->num_units_destroyed_by_reason, 1, event->reason);
  RPT_reporting_add_integer1 (local_data->num_animals_destroyed_by_reason, unit->size, event->reason);
  RPT_reporting_add_integer1 (local_data->cumul_num_units_destroyed_by_reason, 1, event->reason);
  RPT_reporting_add_integer1 (local_data->cumul_num_animals_destroyed_by_reason, unit->size, event->reason);
  if (local_data->num_units_destroyed_by_reason_and_prodtype->frequency != RPT_never)
    RPT_reporting_add_integer (local_data->num_units_destroyed_by_reason_and_prodtype, 1, drill_down_list);
  if (local_data->num_animals_destroyed_by_reason_and_prodtype->frequency != RPT_never)
    RPT_reporting_add_integer (local_data->num_animals_destroyed_by_reason_and_prodtype, unit->size,
                               drill_down_list);
  if (local_data->cumul_num_units_destroyed_by_reason_and_prodtype->frequency != RPT_never)
    RPT_reporting_add_integer (local_data->cumul_num_units_destroyed_by_reason_and_prodtype, 1,
                               drill_down_list);
  if (local_data->cumul_num_animals_destroyed_by_reason_and_prodtype->frequency != RPT_never)
    RPT_reporting_add_integer (local_data->cumul_num_animals_destroyed_by_reason_and_prodtype, unit->size,
                               drill_down_list);

#if DEBUG
  g_debug ("----- EXIT handle_destruction_event (%s)", MODEL_NAME);
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
    case EVT_DeclarationOfDestructionReasons:
      handle_declaration_of_destruction_reasons_event (self,
                                                       &(event->u.
                                                         declaration_of_destruction_reasons));
      break;
    case EVT_Destruction:
      handle_destruction_event (self, &(event->u.destruction));
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
  RPT_reporting_zero (local_data->destructions);
  RPT_reporting_zero (local_data->destruction_occurred);
  RPT_reporting_set_null (local_data->first_destruction, NULL);
  RPT_reporting_set_null (local_data->first_destruction_by_reason, NULL);
  RPT_reporting_set_null (local_data->first_destruction_by_prodtype, NULL);
  RPT_reporting_set_null (local_data->first_destruction_by_reason_and_prodtype, NULL);
  RPT_reporting_zero (local_data->num_units_destroyed);
  RPT_reporting_zero (local_data->num_units_destroyed_by_reason);
  RPT_reporting_zero (local_data->num_units_destroyed_by_prodtype);
  RPT_reporting_zero (local_data->num_units_destroyed_by_reason_and_prodtype);
  RPT_reporting_zero (local_data->cumul_num_units_destroyed);
  RPT_reporting_zero (local_data->cumul_num_units_destroyed_by_reason);
  RPT_reporting_zero (local_data->cumul_num_units_destroyed_by_prodtype);
  RPT_reporting_zero (local_data->cumul_num_units_destroyed_by_reason_and_prodtype);
  RPT_reporting_zero (local_data->num_animals_destroyed);
  RPT_reporting_zero (local_data->num_animals_destroyed_by_reason);
  RPT_reporting_zero (local_data->num_animals_destroyed_by_prodtype);
  RPT_reporting_zero (local_data->num_animals_destroyed_by_reason_and_prodtype);
  RPT_reporting_zero (local_data->cumul_num_animals_destroyed);
  RPT_reporting_zero (local_data->cumul_num_animals_destroyed_by_reason);
  RPT_reporting_zero (local_data->cumul_num_animals_destroyed_by_prodtype);
  RPT_reporting_zero (local_data->cumul_num_animals_destroyed_by_reason_and_prodtype);

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
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<%s>", MODEL_NAME);

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
  RPT_free_reporting (local_data->destructions);
  RPT_free_reporting (local_data->destruction_occurred);
  RPT_free_reporting (local_data->first_destruction);
  RPT_free_reporting (local_data->first_destruction_by_reason);
  RPT_free_reporting (local_data->first_destruction_by_prodtype);
  RPT_free_reporting (local_data->first_destruction_by_reason_and_prodtype);
  RPT_free_reporting (local_data->num_units_destroyed);
  RPT_free_reporting (local_data->num_units_destroyed_by_reason);
  RPT_free_reporting (local_data->num_units_destroyed_by_prodtype);
  RPT_free_reporting (local_data->num_units_destroyed_by_reason_and_prodtype);
  RPT_free_reporting (local_data->cumul_num_units_destroyed);
  RPT_free_reporting (local_data->cumul_num_units_destroyed_by_reason);
  RPT_free_reporting (local_data->cumul_num_units_destroyed_by_prodtype);
  RPT_free_reporting (local_data->cumul_num_units_destroyed_by_reason_and_prodtype);
  RPT_free_reporting (local_data->num_animals_destroyed);
  RPT_free_reporting (local_data->num_animals_destroyed_by_reason);
  RPT_free_reporting (local_data->num_animals_destroyed_by_prodtype);
  RPT_free_reporting (local_data->num_animals_destroyed_by_reason_and_prodtype);
  RPT_free_reporting (local_data->cumul_num_animals_destroyed);
  RPT_free_reporting (local_data->cumul_num_animals_destroyed_by_reason);
  RPT_free_reporting (local_data->cumul_num_animals_destroyed_by_prodtype);
  RPT_free_reporting (local_data->cumul_num_animals_destroyed_by_reason_and_prodtype);

  g_string_free (local_data->target, TRUE);

  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Returns a new destruction monitor.
 */
spreadmodel_model_t *
new (scew_element * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  spreadmodel_model_t *self;
  local_data_t *local_data;
  scew_element *e, **ee;
  unsigned int n;
  const XML_Char *variable_name;
  RPT_frequency_t freq;
  gboolean success;
  gboolean broken_down;
  unsigned int i;      /* loop counter */
  char *prodtype_name;
  const char *drill_down_list[3] = { NULL, NULL, NULL };

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
  self->run = run;
  self->reset = reset;
  self->is_listening_for = is_listening_for;
  self->has_pending_actions = has_pending_actions;
  self->has_pending_infections = has_pending_infections;
  self->to_string = to_string;
  self->printf = local_printf;
  self->fprintf = local_fprintf;
  self->free = local_free;

  /* Make sure the right XML subtree was sent. */
  g_assert (strcmp (scew_element_name (params), MODEL_NAME) == 0);

  local_data->destructions = RPT_new_reporting ("destructions", RPT_group, RPT_never);
  local_data->destruction_occurred =
    RPT_new_reporting ("destrOccurred", RPT_integer, RPT_never);
  local_data->first_destruction =
    RPT_new_reporting ("firstDestruction", RPT_integer, RPT_never);
  local_data->first_destruction_by_reason =
    RPT_new_reporting ("firstDestruction", RPT_group, RPT_never);
  local_data->first_destruction_by_prodtype =
    RPT_new_reporting ("firstDestruction", RPT_group, RPT_never);
  local_data->first_destruction_by_reason_and_prodtype =
    RPT_new_reporting ("firstDestruction", RPT_group, RPT_never);
  local_data->num_units_destroyed =
    RPT_new_reporting ("desnUAll", RPT_integer, RPT_never);
  local_data->num_units_destroyed_by_reason =
    RPT_new_reporting ("desnU", RPT_group, RPT_never);
  local_data->num_units_destroyed_by_prodtype =
    RPT_new_reporting ("desnU", RPT_group, RPT_never);
  local_data->num_units_destroyed_by_reason_and_prodtype =
    RPT_new_reporting ("desnU", RPT_group, RPT_never);
  local_data->cumul_num_units_destroyed =
    RPT_new_reporting ("descUAll", RPT_integer, RPT_never);
  local_data->cumul_num_units_destroyed_by_reason =
    RPT_new_reporting ("descU", RPT_group, RPT_never);
  local_data->cumul_num_units_destroyed_by_prodtype =
    RPT_new_reporting ("descU", RPT_group, RPT_never);
  local_data->cumul_num_units_destroyed_by_reason_and_prodtype =
    RPT_new_reporting ("descU", RPT_group, RPT_never);
  local_data->num_animals_destroyed =
    RPT_new_reporting ("desnAAll", RPT_integer, RPT_never);
  local_data->num_animals_destroyed_by_reason =
    RPT_new_reporting ("desnA", RPT_group, RPT_never);
  local_data->num_animals_destroyed_by_prodtype =
    RPT_new_reporting ("desnA", RPT_group, RPT_never);
  local_data->num_animals_destroyed_by_reason_and_prodtype =
    RPT_new_reporting ("desnA", RPT_group, RPT_never);
  local_data->cumul_num_animals_destroyed =
    RPT_new_reporting ("descAAll", RPT_integer, RPT_never);
  local_data->cumul_num_animals_destroyed_by_reason =
    RPT_new_reporting ("descA", RPT_group, RPT_never);
  local_data->cumul_num_animals_destroyed_by_prodtype =
    RPT_new_reporting ("descA", RPT_group, RPT_never);
  local_data->cumul_num_animals_destroyed_by_reason_and_prodtype =
    RPT_new_reporting ("descA", RPT_group, RPT_never);
  g_ptr_array_add (self->outputs, local_data->destructions);
  g_ptr_array_add (self->outputs, local_data->destruction_occurred);
  g_ptr_array_add (self->outputs, local_data->first_destruction);
  g_ptr_array_add (self->outputs, local_data->first_destruction_by_reason);
  g_ptr_array_add (self->outputs, local_data->first_destruction_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->first_destruction_by_reason_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->num_units_destroyed);
  g_ptr_array_add (self->outputs, local_data->num_units_destroyed_by_reason);
  g_ptr_array_add (self->outputs, local_data->num_units_destroyed_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->num_units_destroyed_by_reason_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_num_units_destroyed);
  g_ptr_array_add (self->outputs, local_data->cumul_num_units_destroyed_by_reason);
  g_ptr_array_add (self->outputs, local_data->cumul_num_units_destroyed_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_num_units_destroyed_by_reason_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->num_animals_destroyed);
  g_ptr_array_add (self->outputs, local_data->num_animals_destroyed_by_reason);
  g_ptr_array_add (self->outputs, local_data->num_animals_destroyed_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->num_animals_destroyed_by_reason_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_num_animals_destroyed);
  g_ptr_array_add (self->outputs, local_data->cumul_num_animals_destroyed_by_reason);
  g_ptr_array_add (self->outputs, local_data->cumul_num_animals_destroyed_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_num_animals_destroyed_by_reason_and_prodtype);

  /* Set the reporting frequency for the output variables. */
  ee = scew_element_list (params, "output", &n);
#if DEBUG
  g_debug ("%u output variables", n);
#endif
  for (i = 0; i < n; i++)
    {
      e = ee[i];
      variable_name = scew_element_contents (scew_element_by_name (e, "variable-name"));
      freq = RPT_string_to_frequency (scew_element_contents
                                      (scew_element_by_name (e, "frequency")));
      broken_down = PAR_get_boolean (scew_element_by_name (e, "broken-down"), &success);
      if (!success)
      	broken_down = FALSE;
      broken_down = broken_down || (g_strstr_len (variable_name, -1, "-by-") != NULL); 
      /* Starting at version 3.2 we accept either the old, verbose output
       * variable names or the new shorter ones. */
      if (strcmp (variable_name, "destructions") == 0)
        {
          RPT_reporting_set_frequency (local_data->destructions, freq);
        }
      else if (strcmp (variable_name, "destrOccurred") == 0)
        {
          RPT_reporting_set_frequency (local_data->destruction_occurred, freq);
        }
      else if (strcmp (variable_name, "firstDestruction") == 0)
        {
          RPT_reporting_set_frequency (local_data->first_destruction, freq);
          if (broken_down)
            {
              RPT_reporting_set_frequency (local_data->first_destruction_by_reason, freq);
              RPT_reporting_set_frequency (local_data->first_destruction_by_prodtype, freq);
              RPT_reporting_set_frequency (local_data->first_destruction_by_reason_and_prodtype, freq);
            }
        }
      else if (strcmp (variable_name, "desnU") == 0
               || strncmp (variable_name, "num-units-destroyed", 19) == 0)
        {
          RPT_reporting_set_frequency (local_data->num_units_destroyed, freq);
          if (broken_down)
            {
              RPT_reporting_set_frequency (local_data->num_units_destroyed_by_reason, freq);
              RPT_reporting_set_frequency (local_data->num_units_destroyed_by_prodtype, freq);
              RPT_reporting_set_frequency (local_data->num_units_destroyed_by_reason_and_prodtype, freq);
            }
        }
      else if (strcmp (variable_name, "descU") == 0
               || strncmp (variable_name, "cumulative-num-units-destroyed", 30) == 0)
        {
          RPT_reporting_set_frequency (local_data->cumul_num_units_destroyed, freq);
          if (broken_down)
            {
              RPT_reporting_set_frequency (local_data->cumul_num_units_destroyed_by_reason, freq);
              RPT_reporting_set_frequency (local_data->cumul_num_units_destroyed_by_prodtype, freq);
              RPT_reporting_set_frequency (local_data->cumul_num_units_destroyed_by_reason_and_prodtype, freq);
            }
        }
      else if (strcmp (variable_name, "desnA") == 0
               || strncmp (variable_name, "num-animals-destroyed", 21) == 0)
        {
          RPT_reporting_set_frequency (local_data->num_animals_destroyed, freq);
          if (broken_down)
            {
              RPT_reporting_set_frequency (local_data->num_animals_destroyed_by_reason, freq);
              RPT_reporting_set_frequency (local_data->num_animals_destroyed_by_prodtype, freq);
              RPT_reporting_set_frequency (local_data->num_animals_destroyed_by_reason_and_prodtype, freq);
            }
        }
      else if (strcmp (variable_name, "descA") == 0
               || strncmp (variable_name, "cumulative-num-animals-destroyed", 32) == 0)
        {
          RPT_reporting_set_frequency (local_data->cumul_num_animals_destroyed, freq);
          if (broken_down)
            {
              RPT_reporting_set_frequency (local_data->cumul_num_animals_destroyed_by_reason, freq);
              RPT_reporting_set_frequency (local_data->cumul_num_animals_destroyed_by_prodtype, freq);
              RPT_reporting_set_frequency (local_data->cumul_num_animals_destroyed_by_reason_and_prodtype, freq);
            }
        }
      else
        g_warning ("no output variable named \"%s\", ignoring", variable_name);        
    }
  free (ee);

  /* Initialize the output variables we already know about. */
  local_data->production_types = units->production_type_names;
  n = local_data->production_types->len;
  drill_down_list[0] = "Ini";
  RPT_reporting_add_integer1 (local_data->num_units_destroyed_by_reason, 0, drill_down_list[0]);
  RPT_reporting_add_integer1 (local_data->cumul_num_units_destroyed_by_reason, 0, drill_down_list[0]);
  RPT_reporting_add_integer1 (local_data->num_animals_destroyed_by_reason, 0, drill_down_list[0]);
  RPT_reporting_add_integer1 (local_data->cumul_num_animals_destroyed_by_reason, 0, drill_down_list[0]);
  for (i = 0; i < n; i++)
    {
      prodtype_name = (char *) g_ptr_array_index (local_data->production_types, i);
      RPT_reporting_add_integer1 (local_data->first_destruction_by_prodtype, 0, prodtype_name);
      RPT_reporting_add_integer1 (local_data->num_units_destroyed_by_prodtype, 0, prodtype_name);
      RPT_reporting_add_integer1 (local_data->cumul_num_units_destroyed_by_prodtype, 0, prodtype_name);
      RPT_reporting_add_integer1 (local_data->num_animals_destroyed_by_prodtype, 0, prodtype_name);
      RPT_reporting_add_integer1 (local_data->cumul_num_animals_destroyed_by_prodtype, 0, prodtype_name);
      drill_down_list[1] = prodtype_name;
      RPT_reporting_add_integer (local_data->num_units_destroyed_by_reason_and_prodtype, 0, drill_down_list);
      RPT_reporting_add_integer (local_data->cumul_num_units_destroyed_by_reason_and_prodtype, 0, drill_down_list);
      RPT_reporting_add_integer (local_data->num_animals_destroyed_by_reason_and_prodtype, 0, drill_down_list);
      RPT_reporting_add_integer (local_data->cumul_num_animals_destroyed_by_reason_and_prodtype, 0, drill_down_list);
    }

  local_data->target = g_string_new (NULL);
  local_data->reasons_declared = FALSE;
  local_data->first_day = TRUE;

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file destruction_monitor.c */
