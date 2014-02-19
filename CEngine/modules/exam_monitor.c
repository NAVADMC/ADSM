/** @file exam_monitor.c
 * Records information on unit examinations: how many units are examined and
 * for what reasons.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date July 2009
 *
 * Copyright &copy; University of Guelph, 2009
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
#define new exam_monitor_new
#define run exam_monitor_run
#define reset exam_monitor_reset
#define events_listened_for exam_monitor_events_listened_for
#define is_listening_for exam_monitor_is_listening_for
#define has_pending_actions exam_monitor_has_pending_actions
#define has_pending_infections exam_monitor_has_pending_infections
#define to_string exam_monitor_to_string
#define local_printf exam_monitor_printf
#define local_fprintf exam_monitor_fprintf
#define local_free exam_monitor_free
#define handle_before_any_simulations_event exam_monitor_handle_before_any_simulations_event
#define handle_new_day_event exam_monitor_handle_new_day_event
#define handle_exam_event exam_monitor_handle_exam_event

#include "module.h"
#include "spreadmodel.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#include "exam_monitor.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "exam-monitor"



#define NEVENTS_LISTENED_FOR 3
EVT_event_type_t events_listened_for[] = { EVT_BeforeAnySimulations,
  EVT_NewDay, EVT_Exam };



/* Specialized information for this model. */
typedef struct
{
  GPtrArray *production_types;
  RPT_reporting_t *nunits_examined;
  RPT_reporting_t *nunits_examined_by_reason;
  RPT_reporting_t *nunits_examined_by_prodtype;
  RPT_reporting_t *nunits_examined_by_reason_and_prodtype;
  RPT_reporting_t *nanimals_examined;
  RPT_reporting_t *nanimals_examined_by_reason;
  RPT_reporting_t *nanimals_examined_by_prodtype;
  RPT_reporting_t *nanimals_examined_by_reason_and_prodtype;
  RPT_reporting_t *cumul_nunits_examined;
  RPT_reporting_t *cumul_nunits_examined_by_reason;
  RPT_reporting_t *cumul_nunits_examined_by_prodtype;
  RPT_reporting_t *cumul_nunits_examined_by_reason_and_prodtype;
  RPT_reporting_t *cumul_nanimals_examined;
  RPT_reporting_t *cumul_nanimals_examined_by_reason;
  RPT_reporting_t *cumul_nanimals_examined_by_prodtype;
  RPT_reporting_t *cumul_nanimals_examined_by_reason_and_prodtype;
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
 * On each new day, zero the daily counts of exams.
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

  /* Zero the daily counts. */
  RPT_reporting_zero (local_data->nunits_examined);
  RPT_reporting_zero (local_data->nunits_examined_by_reason);
  RPT_reporting_zero (local_data->nunits_examined_by_prodtype);
  RPT_reporting_zero (local_data->nunits_examined_by_reason_and_prodtype);
  RPT_reporting_zero (local_data->nanimals_examined);
  RPT_reporting_zero (local_data->nanimals_examined_by_reason);
  RPT_reporting_zero (local_data->nanimals_examined_by_prodtype);
  RPT_reporting_zero (local_data->nanimals_examined_by_reason_and_prodtype);

#if DEBUG
  g_debug ("----- EXIT handle_new_day_event (%s)", MODEL_NAME);
#endif
}



/**
 * Records an examination.
 *
 * @param self the model.
 * @param event an exam event.
 */
void
handle_exam_event (struct spreadmodel_model_t_ *self, EVT_exam_event_t *event)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  const char *reason;
  const char *drill_down_list[3] = { NULL, NULL, NULL };
  UNT_exam_t exam;

  #if DEBUG
    g_debug ("----- ENTER handle_exam_event (%s)", MODEL_NAME);
  #endif

  /* Record the exam in the GUI */
  /* -------------------------- */
  exam.unit_index = event->unit->index;
  
  if ( event->reason == SPREADMODEL_ControlTraceForwardDirect )
    {
      exam.trace_type = SPREADMODEL_TraceForwardOrOut;
      exam.contact_type = SPREADMODEL_DirectContact;
    }
  else if( event->reason == SPREADMODEL_ControlTraceBackDirect )
    {
      exam.trace_type = SPREADMODEL_TraceBackOrIn;
      exam.contact_type = SPREADMODEL_DirectContact;
    }
  else if( event->reason == SPREADMODEL_ControlTraceForwardIndirect ) 
    {
      exam.trace_type = SPREADMODEL_TraceForwardOrOut;
      exam.contact_type = SPREADMODEL_IndirectContact;      
    }
  else if( event->reason == SPREADMODEL_ControlTraceBackIndirect )
    {
      exam.trace_type = SPREADMODEL_TraceBackOrIn;
      exam.contact_type = SPREADMODEL_IndirectContact;        
    }
  else
    {
      g_error( "Unrecognized event reason (%s) in exam-monitor.handle_exam_event",
               SPREADMODEL_control_reason_name[event->reason] );
    }

  #ifdef USE_SC_GUILIB
    sc_examine_unit( event->unit, exam );
  #else
    if (NULL != spreadmodel_examine_unit)
      spreadmodel_examine_unit (exam);
  #endif


  /* Record the exam in the SC version */
  /* --------------------------------- */
  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;
  reason = SPREADMODEL_control_reason_abbrev[event->reason];

  RPT_reporting_add_integer (local_data->nunits_examined, 1, NULL);
  RPT_reporting_add_integer1 (local_data->nunits_examined_by_reason, 1, reason);
  RPT_reporting_add_integer1 (local_data->nunits_examined_by_prodtype, 1, unit->production_type_name);
  RPT_reporting_add_integer (local_data->nanimals_examined, unit->size, NULL);
  RPT_reporting_add_integer1 (local_data->nanimals_examined_by_reason, unit->size, reason);
  RPT_reporting_add_integer1 (local_data->nanimals_examined_by_prodtype, unit->size, unit->production_type_name);
  RPT_reporting_add_integer (local_data->cumul_nunits_examined, 1, NULL);
  RPT_reporting_add_integer1 (local_data->cumul_nunits_examined_by_reason, 1, reason);
  RPT_reporting_add_integer1 (local_data->cumul_nunits_examined_by_prodtype, 1, unit->production_type_name);
  RPT_reporting_add_integer (local_data->cumul_nanimals_examined, unit->size, NULL);
  RPT_reporting_add_integer1 (local_data->cumul_nanimals_examined_by_reason, unit->size, reason);
  RPT_reporting_add_integer1 (local_data->cumul_nanimals_examined_by_prodtype, unit->size, unit->production_type_name);
  drill_down_list[0] = reason;
  drill_down_list[1] = unit->production_type_name;
  if (local_data->nunits_examined_by_reason_and_prodtype->frequency != RPT_never)
    RPT_reporting_add_integer (local_data->nunits_examined_by_reason_and_prodtype, 1, drill_down_list);
  if (local_data->nanimals_examined_by_reason_and_prodtype->frequency != RPT_never)
    RPT_reporting_add_integer (local_data->nanimals_examined_by_reason_and_prodtype, unit->size, drill_down_list);
  if (local_data->cumul_nunits_examined_by_reason_and_prodtype->frequency != RPT_never)
    RPT_reporting_add_integer (local_data->cumul_nunits_examined_by_reason_and_prodtype, 1, drill_down_list);
  if (local_data->cumul_nanimals_examined_by_reason_and_prodtype->frequency != RPT_never)
    RPT_reporting_add_integer (local_data->cumul_nanimals_examined_by_reason_and_prodtype, unit->size, drill_down_list);

#if DEBUG
  g_debug ("----- EXIT handle_exam_event (%s)", MODEL_NAME);
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
      handle_new_day_event (self);
      break;
    case EVT_Exam:
      handle_exam_event (self, &(event->u.exam));
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
  RPT_reporting_zero (local_data->cumul_nunits_examined);
  RPT_reporting_zero (local_data->cumul_nunits_examined_by_reason);
  RPT_reporting_zero (local_data->cumul_nunits_examined_by_prodtype);
  RPT_reporting_zero (local_data->cumul_nunits_examined_by_reason_and_prodtype);
  RPT_reporting_zero (local_data->cumul_nanimals_examined);
  RPT_reporting_zero (local_data->cumul_nanimals_examined_by_reason);
  RPT_reporting_zero (local_data->cumul_nanimals_examined_by_prodtype);
  RPT_reporting_zero (local_data->cumul_nanimals_examined_by_reason_and_prodtype);

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
  RPT_free_reporting (local_data->nunits_examined);
  RPT_free_reporting (local_data->nunits_examined_by_reason);
  RPT_free_reporting (local_data->nunits_examined_by_prodtype);
  RPT_free_reporting (local_data->nunits_examined_by_reason_and_prodtype);
  RPT_free_reporting (local_data->nanimals_examined);
  RPT_free_reporting (local_data->nanimals_examined_by_reason);
  RPT_free_reporting (local_data->nanimals_examined_by_prodtype);
  RPT_free_reporting (local_data->nanimals_examined_by_reason_and_prodtype);
  RPT_free_reporting (local_data->cumul_nunits_examined);
  RPT_free_reporting (local_data->cumul_nunits_examined_by_reason);
  RPT_free_reporting (local_data->cumul_nunits_examined_by_prodtype);
  RPT_free_reporting (local_data->cumul_nunits_examined_by_reason_and_prodtype);
  RPT_free_reporting (local_data->cumul_nanimals_examined);
  RPT_free_reporting (local_data->cumul_nanimals_examined_by_reason);
  RPT_free_reporting (local_data->cumul_nanimals_examined_by_prodtype);
  RPT_free_reporting (local_data->cumul_nanimals_examined_by_reason_and_prodtype);

  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Returns a new exam monitor.
 */
spreadmodel_model_t *
new (scew_element * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  spreadmodel_model_t *self;
  local_data_t *local_data;
  scew_element *e;
  scew_list *ee, *iter;
  const XML_Char *variable_name;
  RPT_frequency_t freq;
  gboolean success;
  gboolean broken_down;
  unsigned int i, j;         /* loop counters */
  char *prodtype_name;

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

  local_data->nunits_examined =
    RPT_new_reporting ("exmnUAll", RPT_integer, RPT_never);
  local_data->nunits_examined_by_reason =
    RPT_new_reporting ("exmnU", RPT_group, RPT_never);
  local_data->nunits_examined_by_prodtype =
    RPT_new_reporting ("exmnU", RPT_group, RPT_never);
  local_data->nunits_examined_by_reason_and_prodtype =
    RPT_new_reporting ("exmnU", RPT_group, RPT_never);
  local_data->nanimals_examined =
    RPT_new_reporting ("exmnAAll", RPT_integer, RPT_never);
  local_data->nanimals_examined_by_reason =
    RPT_new_reporting ("exmnA", RPT_group, RPT_never);
  local_data->nanimals_examined_by_prodtype =
    RPT_new_reporting ("exmnA", RPT_group, RPT_never);
  local_data->nanimals_examined_by_reason_and_prodtype =
    RPT_new_reporting ("exmnA", RPT_group, RPT_never);
  local_data->cumul_nunits_examined =
    RPT_new_reporting ("exmcUAll", RPT_integer, RPT_never);
  local_data->cumul_nunits_examined_by_reason =
    RPT_new_reporting ("exmcU", RPT_group, RPT_never);
  local_data->cumul_nunits_examined_by_prodtype =
    RPT_new_reporting ("exmcU", RPT_group, RPT_never);
  local_data->cumul_nunits_examined_by_reason_and_prodtype =
    RPT_new_reporting ("exmcU", RPT_group, RPT_never);
  local_data->cumul_nanimals_examined =
    RPT_new_reporting ("exmcAAll", RPT_integer, RPT_never);
  local_data->cumul_nanimals_examined_by_reason =
    RPT_new_reporting ("exmcA", RPT_group, RPT_never);
  local_data->cumul_nanimals_examined_by_prodtype =
    RPT_new_reporting ("exmcA", RPT_group, RPT_never);
  local_data->cumul_nanimals_examined_by_reason_and_prodtype =
    RPT_new_reporting ("exmcA", RPT_group, RPT_never);
  g_ptr_array_add (self->outputs, local_data->nunits_examined);
  g_ptr_array_add (self->outputs, local_data->nunits_examined_by_reason);
  g_ptr_array_add (self->outputs, local_data->nunits_examined_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->nunits_examined_by_reason_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->nanimals_examined);
  g_ptr_array_add (self->outputs, local_data->nanimals_examined_by_reason);
  g_ptr_array_add (self->outputs, local_data->nanimals_examined_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->nanimals_examined_by_reason_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_examined);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_examined_by_reason);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_examined_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_examined_by_reason_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_nanimals_examined);
  g_ptr_array_add (self->outputs, local_data->cumul_nanimals_examined_by_reason);
  g_ptr_array_add (self->outputs, local_data->cumul_nanimals_examined_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_nanimals_examined_by_reason_and_prodtype);

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
      if (strcmp (variable_name, "exmnU") == 0)
        {
          RPT_reporting_set_frequency (local_data->nunits_examined, freq);
          if (success == TRUE && broken_down == TRUE)
            {
              RPT_reporting_set_frequency (local_data->nunits_examined_by_reason, freq);
              RPT_reporting_set_frequency (local_data->nunits_examined_by_prodtype, freq);
              RPT_reporting_set_frequency (local_data->nunits_examined_by_reason_and_prodtype, freq);
            }
        }
      else if (strcmp (variable_name, "exmnA") == 0)
        {
          RPT_reporting_set_frequency (local_data->nanimals_examined, freq);
          if (success == TRUE && broken_down == TRUE)
            {
              RPT_reporting_set_frequency (local_data->nanimals_examined_by_reason, freq);
              RPT_reporting_set_frequency (local_data->nanimals_examined_by_prodtype, freq);
              RPT_reporting_set_frequency (local_data->nanimals_examined_by_reason_and_prodtype, freq);
            }
        }
      else if (strcmp (variable_name, "exmcU") == 0)
        {
          RPT_reporting_set_frequency (local_data->cumul_nunits_examined, freq);
          if (success == TRUE && broken_down == TRUE)
            {
              RPT_reporting_set_frequency (local_data->cumul_nunits_examined_by_reason, freq);
              RPT_reporting_set_frequency (local_data->cumul_nunits_examined_by_prodtype, freq);
              RPT_reporting_set_frequency (local_data->cumul_nunits_examined_by_reason_and_prodtype, freq);
            }
        }
      else if (strcmp (variable_name, "exmcA") == 0)
        {
          RPT_reporting_set_frequency (local_data->cumul_nanimals_examined, freq);
          if (success == TRUE && broken_down == TRUE)
            {
              RPT_reporting_set_frequency (local_data->cumul_nanimals_examined_by_reason, freq);
              RPT_reporting_set_frequency (local_data->cumul_nanimals_examined_by_prodtype, freq);
              RPT_reporting_set_frequency (local_data->cumul_nanimals_examined_by_reason_and_prodtype, freq);
            }
        }
      else
        g_warning ("no output variable named \"%s\", ignoring", variable_name);
    }
  scew_list_free (ee);

  /* Initialize the categories in the output variables. */
  local_data->production_types = units->production_type_names;
  for (i = 0; i < local_data->production_types->len; i++)
    {
      prodtype_name = (char *) g_ptr_array_index (local_data->production_types, i);
      RPT_reporting_set_integer1 (local_data->cumul_nunits_examined_by_prodtype, 0, prodtype_name);
      RPT_reporting_set_integer1 (local_data->cumul_nanimals_examined_by_prodtype, 0, prodtype_name);
    }
  for (i = 0; i < SPREADMODEL_NCONTROL_REASONS; i++)
    {
      const char *reason;
      const char *drill_down_list[3] = { NULL, NULL, NULL };
      if ((SPREADMODEL_control_reason)i == SPREADMODEL_ControlReasonUnspecified
          || (SPREADMODEL_control_reason)i == SPREADMODEL_ControlInitialState)
        continue;
      reason = SPREADMODEL_control_reason_abbrev[i]; 
      RPT_reporting_add_integer1 (local_data->nunits_examined_by_reason, 0, reason);
      RPT_reporting_add_integer1 (local_data->nanimals_examined_by_reason, 0, reason);
      RPT_reporting_add_integer1 (local_data->cumul_nunits_examined_by_reason, 0, reason);
      RPT_reporting_add_integer1 (local_data->cumul_nanimals_examined_by_reason, 0, reason);
      drill_down_list[0] = reason;
      for (j = 0; j < local_data->production_types->len; j++)
        {
          drill_down_list[1] = (char *) g_ptr_array_index (local_data->production_types, j);
          RPT_reporting_add_integer (local_data->nunits_examined_by_reason_and_prodtype, 0,
                                     drill_down_list);
          RPT_reporting_add_integer (local_data->nanimals_examined_by_reason_and_prodtype, 0,
                                     drill_down_list);
          RPT_reporting_add_integer (local_data->cumul_nunits_examined_by_reason_and_prodtype, 0,
                                     drill_down_list);
          RPT_reporting_add_integer (local_data->cumul_nanimals_examined_by_reason_and_prodtype, 0,
                                     drill_down_list);
        }
    }

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file exam_monitor.c */
