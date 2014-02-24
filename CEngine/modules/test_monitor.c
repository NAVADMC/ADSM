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
#define handle_before_any_simulations_event test_monitor_handle_before_any_simulations_event
#define handle_test_event test_monitor_handle_test_event
#define handle_test_result_event test_monitor_handle_test_result_event

#include "module.h"
#include "spreadmodel.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#include "test_monitor.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "test-monitor"



#define NEVENTS_LISTENED_FOR 3
EVT_event_type_t events_listened_for[] = { EVT_BeforeAnySimulations,
EVT_Test, EVT_TestResult };



/* Specialized information for this model. */
typedef struct
{
  GPtrArray *production_types;
  RPT_reporting_t *cumul_nunits_tested;
  RPT_reporting_t *cumul_nunits_tested_by_reason;
  RPT_reporting_t *cumul_nunits_tested_by_prodtype;
  RPT_reporting_t *cumul_nunits_tested_by_reason_and_prodtype;
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
 * Records a test.
 *
 * @param self the model.
 * @param event a test event.
 */
void
handle_test_event (struct spreadmodel_model_t_ *self, EVT_test_event_t * event)
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
  reason = SPREADMODEL_control_reason_abbrev[event->reason];

  RPT_reporting_add_integer (local_data->cumul_nunits_tested, 1, NULL);
  RPT_reporting_add_integer1 (local_data->cumul_nunits_tested_by_reason, 1, reason);
  RPT_reporting_add_integer1 (local_data->cumul_nunits_tested_by_prodtype, 1, unit->production_type_name);
  RPT_reporting_add_integer (local_data->cumul_nanimals_tested, unit->size, NULL);
  RPT_reporting_add_integer1 (local_data->cumul_nanimals_tested_by_reason, unit->size, reason);
  RPT_reporting_add_integer1 (local_data->cumul_nanimals_tested_by_prodtype, unit->size, unit->production_type_name);
  drill_down_list[0] = reason;
  drill_down_list[1] = unit->production_type_name;
  if (local_data->cumul_nunits_tested_by_reason_and_prodtype->frequency != RPT_never)
    RPT_reporting_add_integer (local_data->cumul_nunits_tested_by_reason_and_prodtype, 1, drill_down_list);
  if (local_data->cumul_nanimals_tested_by_reason_and_prodtype->frequency != RPT_never)
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
handle_test_result_event (struct spreadmodel_model_t_ * self,
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

  if( event->reason == SPREADMODEL_ControlTraceForwardDirect )
    {
      test.contact_type = SPREADMODEL_DirectContact;
      test.trace_type = SPREADMODEL_TraceForwardOrOut;  
    }
  else if( event->reason == SPREADMODEL_ControlTraceBackDirect )
    {
      test.contact_type = SPREADMODEL_DirectContact;
      test.trace_type = SPREADMODEL_TraceBackOrIn;    
    }
  else if( event->reason == SPREADMODEL_ControlTraceForwardIndirect )
    {
      test.contact_type = SPREADMODEL_IndirectContact;
      test.trace_type = SPREADMODEL_TraceForwardOrOut;    
    }
  else if( event->reason == SPREADMODEL_ControlTraceBackIndirect )
    {
      test.contact_type = SPREADMODEL_IndirectContact;
      test.trace_type = SPREADMODEL_TraceBackOrIn;    
    }
  else
    {
      g_error( "Unrecognized event reason (%s) in test-monitor.handle_test_result_event",
               SPREADMODEL_control_reason_name[event->reason] );  
    } 

  if( event->positive && event->correct )
    test.test_result = SPREADMODEL_TestTruePositive;
  else if( event->positive && !(event->correct) )
    test.test_result = SPREADMODEL_TestFalsePositive;
  else if( !(event->positive) && event->correct )
    test.test_result = SPREADMODEL_TestTrueNegative;
  else if( !(event->positive) && !(event->correct) )
    test.test_result = SPREADMODEL_TestFalseNegative;
    
  #ifdef USE_SC_GUILIB
    sc_test_unit( event->unit, test );
  #else
    if (NULL != spreadmodel_test_unit) 
      spreadmodel_test_unit (test);
  #endif

  /* Record the test in the SC version */
  /* --------------------------------- */
  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;

  if (event->positive)
    {
      if (event->correct)
        {
          RPT_reporting_add_integer (local_data->cumul_nunits_truepos, 1, NULL);
          RPT_reporting_add_integer1 (local_data->cumul_nunits_truepos_by_prodtype, 1, unit->production_type_name);
        }
      else
        {
          RPT_reporting_add_integer (local_data->cumul_nunits_falsepos, 1, NULL);
          RPT_reporting_add_integer1 (local_data->cumul_nunits_falsepos_by_prodtype, 1, unit->production_type_name);
        }
    }
  else /* test result was negative */
    {
      if (event->correct)
        {
          RPT_reporting_add_integer (local_data->cumul_nunits_trueneg, 1, NULL);
          RPT_reporting_add_integer1 (local_data->cumul_nunits_trueneg_by_prodtype, 1, unit->production_type_name);
        }
      else
        {
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
reset (struct spreadmodel_model_t_ *self)
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
local_free (struct spreadmodel_model_t_ *self)
{
  local_data_t *local_data;

#if DEBUG
  g_debug ("----- ENTER free (%s)", MODEL_NAME);
#endif

  /* Free the dynamically-allocated parts. */
  local_data = (local_data_t *) (self->model_data);
  RPT_free_reporting (local_data->cumul_nunits_tested);
  RPT_free_reporting (local_data->cumul_nunits_tested_by_reason);
  RPT_free_reporting (local_data->cumul_nunits_tested_by_prodtype);
  RPT_free_reporting (local_data->cumul_nunits_tested_by_reason_and_prodtype);
  RPT_free_reporting (local_data->cumul_nunits_truepos);
  RPT_free_reporting (local_data->cumul_nunits_truepos_by_prodtype);
  RPT_free_reporting (local_data->cumul_nunits_trueneg);
  RPT_free_reporting (local_data->cumul_nunits_trueneg_by_prodtype);
  RPT_free_reporting (local_data->cumul_nunits_falsepos);
  RPT_free_reporting (local_data->cumul_nunits_falsepos_by_prodtype);
  RPT_free_reporting (local_data->cumul_nunits_falseneg);
  RPT_free_reporting (local_data->cumul_nunits_falseneg_by_prodtype);
  RPT_free_reporting (local_data->cumul_nanimals_tested);
  RPT_free_reporting (local_data->cumul_nanimals_tested_by_reason);
  RPT_free_reporting (local_data->cumul_nanimals_tested_by_prodtype);
  RPT_free_reporting (local_data->cumul_nanimals_tested_by_reason_and_prodtype);

  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Returns a new test monitor.
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
  self->set_params = NULL;
  self->run = run;
  self->reset = reset;
  self->is_singleton = spreadmodel_model_answer_yes;
  self->is_listening_for = spreadmodel_model_is_listening_for;
  self->has_pending_actions = spreadmodel_model_answer_no;
  self->has_pending_infections = spreadmodel_model_answer_no;
  self->to_string = spreadmodel_model_to_string_default;
  self->printf = spreadmodel_model_printf;
  self->fprintf = spreadmodel_model_fprintf;
  self->free = local_free;

  /* Make sure the right XML subtree was sent. */
  g_assert (strcmp (scew_element_name (params), MODEL_NAME) == 0);

  local_data->cumul_nunits_tested =
    RPT_new_reporting ("tstcUAll", RPT_integer, RPT_never);
  local_data->cumul_nunits_tested_by_reason =
    RPT_new_reporting ("tstcU", RPT_group, RPT_never);
  local_data->cumul_nunits_tested_by_prodtype =
    RPT_new_reporting ("tstcU", RPT_group, RPT_never);
  local_data->cumul_nunits_tested_by_reason_and_prodtype =
    RPT_new_reporting ("tstcU", RPT_group, RPT_never);
  local_data->cumul_nunits_truepos =
    RPT_new_reporting ("tstcUTruePos", RPT_integer, RPT_never);
  local_data->cumul_nunits_truepos_by_prodtype =
    RPT_new_reporting ("tstcUTruePos", RPT_group, RPT_never);
  local_data->cumul_nunits_trueneg =
    RPT_new_reporting ("tstcUTrueNeg", RPT_integer, RPT_never);
  local_data->cumul_nunits_trueneg_by_prodtype =
    RPT_new_reporting ("tstcUTrueNeg", RPT_group, RPT_never);
  local_data->cumul_nunits_falsepos =
    RPT_new_reporting ("tstcUFalsePos", RPT_integer, RPT_never);
  local_data->cumul_nunits_falsepos_by_prodtype =
    RPT_new_reporting ("tstcUFalsePos", RPT_group, RPT_never);
  local_data->cumul_nunits_falseneg =
    RPT_new_reporting ("tstcUFalseNeg", RPT_integer, RPT_never);
  local_data->cumul_nunits_falseneg_by_prodtype =
    RPT_new_reporting ("tstcUFalseNeg", RPT_group, RPT_never);
  local_data->cumul_nanimals_tested =
    RPT_new_reporting ("tstcAAll", RPT_integer, RPT_never);
  local_data->cumul_nanimals_tested_by_reason =
    RPT_new_reporting ("tstcA", RPT_group, RPT_never);
  local_data->cumul_nanimals_tested_by_prodtype =
    RPT_new_reporting ("tstcA", RPT_group, RPT_never);
  local_data->cumul_nanimals_tested_by_reason_and_prodtype =
    RPT_new_reporting ("tstcA", RPT_group, RPT_never);
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
      if (strcmp (variable_name, "tstcU") == 0)
        {
          RPT_reporting_set_frequency (local_data->cumul_nunits_tested, freq);
          if (success == TRUE && broken_down == TRUE)
            {
              RPT_reporting_set_frequency (local_data->cumul_nunits_tested_by_reason, freq);
              RPT_reporting_set_frequency (local_data->cumul_nunits_tested_by_prodtype, freq);
              RPT_reporting_set_frequency (local_data->cumul_nunits_tested_by_reason_and_prodtype, freq);
            }
        }
      else if (strcmp (variable_name, "tstcUTruePos") == 0)
        {
          RPT_reporting_set_frequency (local_data->cumul_nunits_truepos, freq);
          if (success == TRUE && broken_down == TRUE)
            RPT_reporting_set_frequency (local_data->cumul_nunits_truepos_by_prodtype, freq);
        }
      else if (strcmp (variable_name, "tstcUTrueNeg") == 0)
        {
          RPT_reporting_set_frequency (local_data->cumul_nunits_trueneg, freq);
          if (success == TRUE && broken_down == TRUE)
            RPT_reporting_set_frequency (local_data->cumul_nunits_trueneg_by_prodtype, freq);
        }
      else if (strcmp (variable_name, "tstcUFalsePos") == 0)
        {
          RPT_reporting_set_frequency (local_data->cumul_nunits_falsepos, freq);
          if (success == TRUE && broken_down == TRUE)
            RPT_reporting_set_frequency (local_data->cumul_nunits_falsepos_by_prodtype, freq);
        }
      else if (strcmp (variable_name, "tstcUFalseNeg") == 0)
        {
          RPT_reporting_set_frequency (local_data->cumul_nunits_falseneg, freq);
          if (success == TRUE && broken_down == TRUE)
            RPT_reporting_set_frequency (local_data->cumul_nunits_falseneg_by_prodtype, freq);
        }
      else if (strcmp (variable_name, "tstcA") == 0)
        {
          RPT_reporting_set_frequency (local_data->cumul_nanimals_tested, freq);
          if (success == TRUE && broken_down == TRUE)
            {
              RPT_reporting_set_frequency (local_data->cumul_nanimals_tested_by_reason, freq);
              RPT_reporting_set_frequency (local_data->cumul_nanimals_tested_by_prodtype, freq);
              RPT_reporting_set_frequency (local_data->cumul_nanimals_tested_by_reason_and_prodtype, freq);
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
      RPT_reporting_set_integer1 (local_data->cumul_nunits_tested_by_prodtype, 0, prodtype_name);
      RPT_reporting_set_integer1 (local_data->cumul_nunits_truepos_by_prodtype, 0, prodtype_name);
      RPT_reporting_set_integer1 (local_data->cumul_nunits_trueneg_by_prodtype, 0, prodtype_name);
      RPT_reporting_set_integer1 (local_data->cumul_nunits_falsepos_by_prodtype, 0, prodtype_name);
      RPT_reporting_set_integer1 (local_data->cumul_nunits_falseneg_by_prodtype, 0, prodtype_name);
      RPT_reporting_set_integer1 (local_data->cumul_nanimals_tested_by_prodtype, 0, prodtype_name);
    }
  for (i = 0; i < SPREADMODEL_NCONTROL_REASONS; i++)
    {
      const char *reason;
      const char *drill_down_list[3] = { NULL, NULL, NULL };
      if ((SPREADMODEL_control_reason)i == SPREADMODEL_ControlReasonUnspecified
          || (SPREADMODEL_control_reason)i == SPREADMODEL_ControlRing
          || (SPREADMODEL_control_reason)i == SPREADMODEL_ControlDetection
          || (SPREADMODEL_control_reason)i == SPREADMODEL_ControlInitialState)
        continue;
      reason = SPREADMODEL_control_reason_abbrev[i];
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
