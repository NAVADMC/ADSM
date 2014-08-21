/** @file test_monitor.c
 * Records information on diagnostic testing: how many units are tested, for
 * reasons, and how many true positives, false positives, etc. occur.
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
#define new test_monitor_new
#define run test_monitor_run
#define reset test_monitor_reset
#define events_listened_for test_monitor_events_listened_for
#define local_free test_monitor_free
#define handle_new_day_event test_monitor_handle_new_day_event
#define handle_test_event test_monitor_handle_test_event
#define handle_test_result_event test_monitor_handle_test_result_event

#include "module.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#include "test_monitor.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "test-monitor"



#define NEVENTS_LISTENED_FOR 4
EVT_event_type_t events_listened_for[] = { EVT_BeforeAnySimulations,
EVT_NewDay, EVT_Test, EVT_TestResult };



/* Specialized information for this model. */
typedef struct
{
  GPtrArray *production_types;
  RPT_reporting_t *cumul_nunits_tested;
  RPT_reporting_t *cumul_nunits_tested_by_reason;
  RPT_reporting_t *cumul_nunits_tested_by_prodtype;
  RPT_reporting_t *cumul_nunits_tested_by_reason_and_prodtype;
  RPT_reporting_t *nunits_truepos;
  RPT_reporting_t *nunits_truepos_by_prodtype;
  RPT_reporting_t *nunits_trueneg;
  RPT_reporting_t *nunits_trueneg_by_prodtype;
  RPT_reporting_t *nunits_falsepos;
  RPT_reporting_t *nunits_falsepos_by_prodtype;
  RPT_reporting_t *nunits_falseneg;
  RPT_reporting_t *nunits_falseneg_by_prodtype;
  RPT_reporting_t *cumul_nunits_truepos;
  RPT_reporting_t *cumul_nunits_truepos_by_prodtype;
  RPT_reporting_t *cumul_nunits_trueneg;
  RPT_reporting_t *cumul_nunits_trueneg_by_prodtype;
  RPT_reporting_t *cumul_nunits_falsepos;
  RPT_reporting_t *cumul_nunits_falsepos_by_prodtype;
  RPT_reporting_t *cumul_nunits_falseneg;
  RPT_reporting_t *cumul_nunits_falseneg_by_prodtype;
  RPT_reporting_t *cumul_nanimals_tested;
  RPT_reporting_t *cumul_nanimals_tested_by_reason;
  RPT_reporting_t *cumul_nanimals_tested_by_prodtype;
  RPT_reporting_t *cumul_nanimals_tested_by_reason_and_prodtype;
}
local_data_t;



/**
 * On each new day, zero the daily counts of true positives, false positives,
 * etc.
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
  RPT_reporting_zero (local_data->nunits_truepos);
  RPT_reporting_zero (local_data->nunits_truepos_by_prodtype);
  RPT_reporting_zero (local_data->nunits_trueneg);
  RPT_reporting_zero (local_data->nunits_trueneg_by_prodtype);
  RPT_reporting_zero (local_data->nunits_falsepos);
  RPT_reporting_zero (local_data->nunits_falsepos_by_prodtype);
  RPT_reporting_zero (local_data->nunits_falseneg);
  RPT_reporting_zero (local_data->nunits_falseneg_by_prodtype);

  #if DEBUG
    g_debug ("----- EXIT handle_new_day_event (%s)", MODEL_NAME);
  #endif
  
  return;
}



/**
 * Records a test.
 *
 * @param self the model.
 * @param event a test event.
 */
void
handle_test_event (struct adsm_module_t_ *self, EVT_test_event_t * event)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  const char *reason;
  const char *drill_down_list[3] = { NULL, NULL, NULL };

#if DEBUG
  g_debug ("----- ENTER handle_test_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;
  reason = ADSM_control_reason_abbrev[event->reason];

  RPT_reporting_add_integer (local_data->cumul_nunits_tested, 1, NULL);
  RPT_reporting_add_integer1 (local_data->cumul_nunits_tested_by_reason, 1, reason);
  RPT_reporting_add_integer1 (local_data->cumul_nunits_tested_by_prodtype, 1, unit->production_type_name);
  RPT_reporting_add_integer (local_data->cumul_nanimals_tested, unit->size, NULL);
  RPT_reporting_add_integer1 (local_data->cumul_nanimals_tested_by_reason, unit->size, reason);
  RPT_reporting_add_integer1 (local_data->cumul_nanimals_tested_by_prodtype, unit->size, unit->production_type_name);
  drill_down_list[0] = reason;
  drill_down_list[1] = unit->production_type_name;
  RPT_reporting_add_integer (local_data->cumul_nunits_tested_by_reason_and_prodtype, 1, drill_down_list);
  RPT_reporting_add_integer (local_data->cumul_nanimals_tested_by_reason_and_prodtype, unit->size, drill_down_list);

#if DEBUG
  g_debug ("----- EXIT handle_test_event (%s)", MODEL_NAME);
#endif
}



/**
 * Records a test result.
 *
 * @param self the model.
 * @param event a test result event.
 */
void
handle_test_result_event (struct adsm_module_t_ * self,
                          EVT_test_result_event_t * event)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  UNT_test_t test;

#if DEBUG
  g_debug ("----- ENTER handle_test_result_event (%s)", MODEL_NAME);
#endif

  /* Record the test in the GUI */
  /* -------------------------- */
  test.unit_index = event->unit->index;

  if( event->reason == ADSM_ControlTraceForwardDirect )
    {
      test.contact_type = ADSM_DirectContact;
      test.trace_type = ADSM_TraceForwardOrOut;  
    }
  else if( event->reason == ADSM_ControlTraceBackDirect )
    {
      test.contact_type = ADSM_DirectContact;
      test.trace_type = ADSM_TraceBackOrIn;    
    }
  else if( event->reason == ADSM_ControlTraceForwardIndirect )
    {
      test.contact_type = ADSM_IndirectContact;
      test.trace_type = ADSM_TraceForwardOrOut;    
    }
  else if( event->reason == ADSM_ControlTraceBackIndirect )
    {
      test.contact_type = ADSM_IndirectContact;
      test.trace_type = ADSM_TraceBackOrIn;    
    }
  else
    {
      g_error( "Unrecognized event reason (%s) in test-monitor.handle_test_result_event",
               ADSM_control_reason_name[event->reason] );  
    } 

  if( event->positive && event->correct )
    test.test_result = ADSM_TestTruePositive;
  else if( event->positive && !(event->correct) )
    test.test_result = ADSM_TestFalsePositive;
  else if( !(event->positive) && event->correct )
    test.test_result = ADSM_TestTrueNegative;
  else if( !(event->positive) && !(event->correct) )
    test.test_result = ADSM_TestFalseNegative;
    
  #ifdef USE_SC_GUILIB
    sc_test_unit( event->unit, test );
  #else
    if (NULL != adsm_test_unit) 
      adsm_test_unit (test);
  #endif

  /* Record the test in the SC version */
  /* --------------------------------- */
  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;

  if (event->positive)
    {
      if (event->correct)
        {
          RPT_reporting_add_integer (local_data->nunits_truepos, 1, NULL);
          RPT_reporting_add_integer1 (local_data->nunits_truepos_by_prodtype, 1, unit->production_type_name);
          RPT_reporting_add_integer (local_data->cumul_nunits_truepos, 1, NULL);
          RPT_reporting_add_integer1 (local_data->cumul_nunits_truepos_by_prodtype, 1, unit->production_type_name);
        }
      else
        {
          RPT_reporting_add_integer (local_data->nunits_falsepos, 1, NULL);
          RPT_reporting_add_integer1 (local_data->nunits_falsepos_by_prodtype, 1, unit->production_type_name);
          RPT_reporting_add_integer (local_data->cumul_nunits_falsepos, 1, NULL);
          RPT_reporting_add_integer1 (local_data->cumul_nunits_falsepos_by_prodtype, 1, unit->production_type_name);
        }
    }
  else /* test result was negative */
    {
      if (event->correct)
        {
          RPT_reporting_add_integer (local_data->nunits_trueneg, 1, NULL);
          RPT_reporting_add_integer1 (local_data->nunits_trueneg_by_prodtype, 1, unit->production_type_name);
          RPT_reporting_add_integer (local_data->cumul_nunits_trueneg, 1, NULL);
          RPT_reporting_add_integer1 (local_data->cumul_nunits_trueneg_by_prodtype, 1, unit->production_type_name);
        }
      else
        {
          RPT_reporting_add_integer (local_data->nunits_falseneg, 1, NULL);
          RPT_reporting_add_integer1 (local_data->nunits_falseneg_by_prodtype, 1, unit->production_type_name);
          RPT_reporting_add_integer (local_data->cumul_nunits_falseneg, 1, NULL);
          RPT_reporting_add_integer1 (local_data->cumul_nunits_falseneg_by_prodtype, 1, unit->production_type_name);
        }
    }

#if DEBUG
  g_debug ("----- EXIT handle_test_result_event (%s)", MODEL_NAME);
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
    case EVT_Test:
      handle_test_event (self, &(event->u.test));
      break;
    case EVT_TestResult:
      handle_test_result_event (self, &(event->u.test_result));
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
  RPT_reporting_zero (local_data->cumul_nunits_tested);
  RPT_reporting_zero (local_data->cumul_nunits_tested_by_reason);
  RPT_reporting_zero (local_data->cumul_nunits_tested_by_prodtype);
  RPT_reporting_zero (local_data->cumul_nunits_tested_by_reason_and_prodtype);
  RPT_reporting_zero (local_data->cumul_nunits_truepos);
  RPT_reporting_zero (local_data->cumul_nunits_truepos_by_prodtype);
  RPT_reporting_zero (local_data->cumul_nunits_trueneg);
  RPT_reporting_zero (local_data->cumul_nunits_trueneg_by_prodtype);
  RPT_reporting_zero (local_data->cumul_nunits_falsepos);
  RPT_reporting_zero (local_data->cumul_nunits_falsepos_by_prodtype);
  RPT_reporting_zero (local_data->cumul_nunits_falseneg);
  RPT_reporting_zero (local_data->cumul_nunits_falseneg_by_prodtype);
  RPT_reporting_zero (local_data->cumul_nanimals_tested);
  RPT_reporting_zero (local_data->cumul_nanimals_tested_by_reason);
  RPT_reporting_zero (local_data->cumul_nanimals_tested_by_prodtype);
  RPT_reporting_zero (local_data->cumul_nanimals_tested_by_reason_and_prodtype);

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
  g_free (local_data);
  /* Because a free function was specified when creating the pointer array
   * self->outputs, freeing self->outputs will also properly dispose of all
   * of the output variables contained in the array. */
  g_ptr_array_free (self->outputs, /* free_seg = */ TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Returns a new test monitor.
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
  self->outputs = g_ptr_array_new_with_free_func ((GDestroyNotify)RPT_free_reporting);
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

  local_data->cumul_nunits_tested =
    RPT_new_reporting ("tstcUAll", RPT_integer);
  local_data->cumul_nunits_tested_by_reason =
    RPT_new_reporting ("tstcU", RPT_group);
  local_data->cumul_nunits_tested_by_prodtype =
    RPT_new_reporting ("tstcU", RPT_group);
  local_data->cumul_nunits_tested_by_reason_and_prodtype =
    RPT_new_reporting ("tstcU", RPT_group);

  g_ptr_array_add (self->outputs,
    local_data->nunits_truepos =
      RPT_new_reporting ("tstnUTruePos", RPT_integer));
  g_ptr_array_add (self->outputs,
    local_data->nunits_truepos_by_prodtype =
      RPT_new_reporting ("tstnUTruePos", RPT_group));
  g_ptr_array_add (self->outputs,
    local_data->nunits_trueneg =
      RPT_new_reporting ("tstnUTrueNeg", RPT_integer));
  g_ptr_array_add (self->outputs,
    local_data->nunits_trueneg_by_prodtype =
      RPT_new_reporting ("tstnUTrueNeg", RPT_group));
  g_ptr_array_add (self->outputs,
    local_data->nunits_falsepos =
      RPT_new_reporting ("tstnUFalsePos", RPT_integer));
  g_ptr_array_add (self->outputs,
    local_data->nunits_falsepos_by_prodtype =
      RPT_new_reporting ("tstnUFalsePos", RPT_group));
  g_ptr_array_add (self->outputs,
    local_data->nunits_falseneg =
      RPT_new_reporting ("tstnUFalseNeg", RPT_integer));
  g_ptr_array_add (self->outputs,
    local_data->nunits_falseneg_by_prodtype =
      RPT_new_reporting ("tstnUFalseNeg", RPT_group));

  local_data->cumul_nunits_truepos =
    RPT_new_reporting ("tstcUTruePos", RPT_integer);
  local_data->cumul_nunits_truepos_by_prodtype =
    RPT_new_reporting ("tstcUTruePos", RPT_group);
  local_data->cumul_nunits_trueneg =
    RPT_new_reporting ("tstcUTrueNeg", RPT_integer);
  local_data->cumul_nunits_trueneg_by_prodtype =
    RPT_new_reporting ("tstcUTrueNeg", RPT_group);
  local_data->cumul_nunits_falsepos =
    RPT_new_reporting ("tstcUFalsePos", RPT_integer);
  local_data->cumul_nunits_falsepos_by_prodtype =
    RPT_new_reporting ("tstcUFalsePos", RPT_group);
  local_data->cumul_nunits_falseneg =
    RPT_new_reporting ("tstcUFalseNeg", RPT_integer);
  local_data->cumul_nunits_falseneg_by_prodtype =
    RPT_new_reporting ("tstcUFalseNeg", RPT_group);
  local_data->cumul_nanimals_tested =
    RPT_new_reporting ("tstcAAll", RPT_integer);
  local_data->cumul_nanimals_tested_by_reason =
    RPT_new_reporting ("tstcA", RPT_group);
  local_data->cumul_nanimals_tested_by_prodtype =
    RPT_new_reporting ("tstcA", RPT_group);
  local_data->cumul_nanimals_tested_by_reason_and_prodtype =
    RPT_new_reporting ("tstcA", RPT_group);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_tested);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_tested_by_reason);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_tested_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_tested_by_reason_and_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_truepos);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_truepos_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_trueneg);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_trueneg_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_falsepos);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_falsepos_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_falseneg);
  g_ptr_array_add (self->outputs, local_data->cumul_nunits_falseneg_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_nanimals_tested);
  g_ptr_array_add (self->outputs, local_data->cumul_nanimals_tested_by_reason);
  g_ptr_array_add (self->outputs, local_data->cumul_nanimals_tested_by_prodtype);
  g_ptr_array_add (self->outputs, local_data->cumul_nanimals_tested_by_reason_and_prodtype);

  /* Set the reporting frequency for the output variables. */

  /* Initialize the categories in the output variables. */
  local_data->production_types = units->production_type_names;
  for (i = 0; i < local_data->production_types->len; i++)
    {
      prodtype_name = (char *) g_ptr_array_index (local_data->production_types, i);
      RPT_reporting_set_integer1 (local_data->cumul_nunits_tested_by_prodtype, 0, prodtype_name);
      RPT_reporting_set_integer1 (local_data->nunits_truepos_by_prodtype, 0, prodtype_name);
      RPT_reporting_set_integer1 (local_data->nunits_trueneg_by_prodtype, 0, prodtype_name);
      RPT_reporting_set_integer1 (local_data->nunits_falsepos_by_prodtype, 0, prodtype_name);
      RPT_reporting_set_integer1 (local_data->nunits_falseneg_by_prodtype, 0, prodtype_name);
      RPT_reporting_set_integer1 (local_data->cumul_nunits_truepos_by_prodtype, 0, prodtype_name);
      RPT_reporting_set_integer1 (local_data->cumul_nunits_trueneg_by_prodtype, 0, prodtype_name);
      RPT_reporting_set_integer1 (local_data->cumul_nunits_falsepos_by_prodtype, 0, prodtype_name);
      RPT_reporting_set_integer1 (local_data->cumul_nunits_falseneg_by_prodtype, 0, prodtype_name);
      RPT_reporting_set_integer1 (local_data->cumul_nanimals_tested_by_prodtype, 0, prodtype_name);
    }
  for (i = 0; i < ADSM_NCONTROL_REASONS; i++)
    {
      const char *reason;
      const char *drill_down_list[3] = { NULL, NULL, NULL };
      if ((ADSM_control_reason)i == ADSM_ControlReasonUnspecified
          || (ADSM_control_reason)i == ADSM_ControlRing
          || (ADSM_control_reason)i == ADSM_ControlDetection
          || (ADSM_control_reason)i == ADSM_ControlInitialState)
        continue;
      reason = ADSM_control_reason_abbrev[i];
      RPT_reporting_add_integer1 (local_data->cumul_nunits_tested_by_reason, 0, reason);
      RPT_reporting_add_integer1 (local_data->cumul_nanimals_tested_by_reason, 0, reason);
      drill_down_list[0] = reason;
      for (j = 0; j < local_data->production_types->len; j++)
        {
          drill_down_list[1] = (char *) g_ptr_array_index (local_data->production_types, j);
          RPT_reporting_add_integer (local_data->cumul_nunits_tested_by_reason_and_prodtype, 0,
                                     drill_down_list);
          RPT_reporting_add_integer (local_data->cumul_nanimals_tested_by_reason_and_prodtype, 0,
                                     drill_down_list);
        }
    }

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file test_monitor.c */
