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
#define local_free exam_monitor_free
#define handle_new_day_event exam_monitor_handle_new_day_event
#define handle_exam_event exam_monitor_handle_exam_event

#include "module.h"

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
 * On each new day, zero the daily counts of exams.
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
handle_exam_event (struct adsm_module_t_ *self, EVT_exam_event_t *event)
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
  
  if ( event->reason == ADSM_ControlTraceForwardDirect )
    {
      exam.trace_type = ADSM_TraceForwardOrOut;
      exam.contact_type = ADSM_DirectContact;
    }
  else if( event->reason == ADSM_ControlTraceBackDirect )
    {
      exam.trace_type = ADSM_TraceBackOrIn;
      exam.contact_type = ADSM_DirectContact;
    }
  else if( event->reason == ADSM_ControlTraceForwardIndirect ) 
    {
      exam.trace_type = ADSM_TraceForwardOrOut;
      exam.contact_type = ADSM_IndirectContact;      
    }
  else if( event->reason == ADSM_ControlTraceBackIndirect )
    {
      exam.trace_type = ADSM_TraceBackOrIn;
      exam.contact_type = ADSM_IndirectContact;        
    }
  else
    {
      g_error( "Unrecognized event reason (%s) in exam-monitor.handle_exam_event",
               ADSM_control_reason_name[event->reason] );
    }

  #ifdef USE_SC_GUILIB
    sc_examine_unit( event->unit, exam );
  #else
    if (NULL != adsm_examine_unit)
      adsm_examine_unit (exam);
  #endif


  /* Record the exam in the SC version */
  /* --------------------------------- */
  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;
  reason = ADSM_control_reason_abbrev[event->reason];

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
  RPT_reporting_add_integer (local_data->nunits_examined_by_reason_and_prodtype, 1, drill_down_list);
  RPT_reporting_add_integer (local_data->nanimals_examined_by_reason_and_prodtype, unit->size, drill_down_list);
  RPT_reporting_add_integer (local_data->cumul_nunits_examined_by_reason_and_prodtype, 1, drill_down_list);
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
run (struct adsm_module_t_ *self, UNT_unit_list_t * units, ZON_zone_list_t * zones,
     EVT_event_t * event, RAN_gen_t * rng, EVT_event_queue_t * queue)
{
#if DEBUG
  g_debug ("----- ENTER run (%s)", MODEL_NAME);
#endif

  switch (event->type)
    {
    case EVT_BeforeAnySimulations:
      adsm_declare_outputs (self, queue);
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
reset (struct adsm_module_t_ *self)
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
 * Frees this model.
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
adsm_module_t *
new (sqlite3 * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  adsm_module_t *self;
  local_data_t *local_data;
  unsigned int i, j;         /* loop counters */
  char *prodtype_name;

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

  local_data->nunits_examined =
    RPT_new_reporting ("exmnUAll", RPT_integer);
  local_data->nunits_examined_by_reason =
    RPT_new_reporting ("exmnU", RPT_group);
  local_data->nunits_examined_by_prodtype =
    RPT_new_reporting ("exmnU", RPT_group);
  local_data->nunits_examined_by_reason_and_prodtype =
    RPT_new_reporting ("exmnU", RPT_group);
  local_data->nanimals_examined =
    RPT_new_reporting ("exmnAAll", RPT_integer);
  local_data->nanimals_examined_by_reason =
    RPT_new_reporting ("exmnA", RPT_group);
  local_data->nanimals_examined_by_prodtype =
    RPT_new_reporting ("exmnA", RPT_group);
  local_data->nanimals_examined_by_reason_and_prodtype =
    RPT_new_reporting ("exmnA", RPT_group);
  local_data->cumul_nunits_examined =
    RPT_new_reporting ("exmcUAll", RPT_integer);
  local_data->cumul_nunits_examined_by_reason =
    RPT_new_reporting ("exmcU", RPT_group);
  local_data->cumul_nunits_examined_by_prodtype =
    RPT_new_reporting ("exmcU", RPT_group);
  local_data->cumul_nunits_examined_by_reason_and_prodtype =
    RPT_new_reporting ("exmcU", RPT_group);
  local_data->cumul_nanimals_examined =
    RPT_new_reporting ("exmcAAll", RPT_integer);
  local_data->cumul_nanimals_examined_by_reason =
    RPT_new_reporting ("exmcA", RPT_group);
  local_data->cumul_nanimals_examined_by_prodtype =
    RPT_new_reporting ("exmcA", RPT_group);
  local_data->cumul_nanimals_examined_by_reason_and_prodtype =
    RPT_new_reporting ("exmcA", RPT_group);
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

  /* Initialize the categories in the output variables. */
  local_data->production_types = units->production_type_names;
  for (i = 0; i < local_data->production_types->len; i++)
    {
      prodtype_name = (char *) g_ptr_array_index (local_data->production_types, i);
      RPT_reporting_set_integer1 (local_data->nunits_examined_by_prodtype, 0, prodtype_name);
      RPT_reporting_set_integer1 (local_data->nanimals_examined_by_prodtype, 0, prodtype_name);
      RPT_reporting_set_integer1 (local_data->cumul_nunits_examined_by_prodtype, 0, prodtype_name);
      RPT_reporting_set_integer1 (local_data->cumul_nanimals_examined_by_prodtype, 0, prodtype_name);
    }
  for (i = 0; i < ADSM_NCONTROL_REASONS; i++)
    {
      const char *reason;
      const char *drill_down_list[3] = { NULL, NULL, NULL };
      if ((ADSM_control_reason)i == ADSM_ControlReasonUnspecified
          || (ADSM_control_reason)i == ADSM_ControlInitialState)
        continue;
      reason = ADSM_control_reason_abbrev[i]; 
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
