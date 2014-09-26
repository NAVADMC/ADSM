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
#  include "config.h"
#endif

/* To avoid name clashes when multiple modules have the same interface. */
#define new test_monitor_new
#define run test_monitor_run
#define local_free test_monitor_free
#define handle_before_each_simulation_event test_monitor_handle_before_each_simulation_event
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



/* Specialized information for this model. */
typedef struct
{
  GPtrArray *production_types;
  RPT_reporting_t   *nunits_tested;
  RPT_reporting_t  **nunits_tested_by_reason;
  RPT_reporting_t  **nunits_tested_by_prodtype;
  RPT_reporting_t ***nunits_tested_by_reason_and_prodtype;
  RPT_reporting_t   *cumul_nunits_tested;
  RPT_reporting_t  **cumul_nunits_tested_by_reason;
  RPT_reporting_t  **cumul_nunits_tested_by_prodtype;
  RPT_reporting_t ***cumul_nunits_tested_by_reason_and_prodtype;
  RPT_reporting_t   *nunits_truepos;
  RPT_reporting_t  **nunits_truepos_by_prodtype;
  RPT_reporting_t   *nunits_trueneg;
  RPT_reporting_t  **nunits_trueneg_by_prodtype;
  RPT_reporting_t   *nunits_falsepos;
  RPT_reporting_t  **nunits_falsepos_by_prodtype;
  RPT_reporting_t   *nunits_falseneg;
  RPT_reporting_t  **nunits_falseneg_by_prodtype;
  RPT_reporting_t   *cumul_nunits_truepos;
  RPT_reporting_t  **cumul_nunits_truepos_by_prodtype;
  RPT_reporting_t   *cumul_nunits_trueneg;
  RPT_reporting_t  **cumul_nunits_trueneg_by_prodtype;
  RPT_reporting_t   *cumul_nunits_falsepos;
  RPT_reporting_t  **cumul_nunits_falsepos_by_prodtype;
  RPT_reporting_t   *cumul_nunits_falseneg;
  RPT_reporting_t  **cumul_nunits_falseneg_by_prodtype;
  RPT_reporting_t   *cumul_nanimals_tested;
  RPT_reporting_t  **cumul_nanimals_tested_by_reason;
  RPT_reporting_t  **cumul_nanimals_tested_by_prodtype;
  RPT_reporting_t ***cumul_nanimals_tested_by_reason_and_prodtype;
  GPtrArray *daily_outputs; /**< Daily outputs, in a list to make it easy to
    zero them all at once. */
  GPtrArray *cumul_outputs; /**< Cumulative outputs, is a list to make it easy
    to zero them all at once. */
}
local_data_t;



/**
 * Before each simulation, zero the cumulative counts of tests.
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
  g_ptr_array_foreach (local_data->cumul_outputs, RPT_reporting_zero_as_GFunc, NULL);

  #if DEBUG
    g_debug ("----- EXIT handle_before_each_simulation_event (%s)", MODEL_NAME);
  #endif

  return;
}



/**
 * On each new day, zero the daily counts of units tested, true positives,
 * false positives, etc.
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
  g_ptr_array_foreach (local_data->daily_outputs, RPT_reporting_zero_as_GFunc, NULL);

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
  ADSM_control_reason reason;
  UNT_production_type_t prodtype;
  double nanimals;

#if DEBUG
  g_debug ("----- ENTER handle_test_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;
  reason = event->reason;
  prodtype = unit->production_type;
  nanimals = (double)(unit->size);
  RPT_reporting_add_integer (local_data->nunits_tested, 1);
  RPT_reporting_add_integer (local_data->nunits_tested_by_reason[reason], 1);
  RPT_reporting_add_integer (local_data->nunits_tested_by_prodtype[prodtype], 1);
  RPT_reporting_add_integer (local_data->nunits_tested_by_reason_and_prodtype[reason][prodtype], 1);
  RPT_reporting_add_integer (local_data->cumul_nunits_tested, 1);
  RPT_reporting_add_integer (local_data->cumul_nunits_tested_by_reason[reason], 1);
  RPT_reporting_add_integer (local_data->cumul_nunits_tested_by_prodtype[prodtype], 1);
  RPT_reporting_add_integer (local_data->cumul_nunits_tested_by_reason_and_prodtype[reason][prodtype], 1);
  RPT_reporting_add_real (local_data->cumul_nanimals_tested, nanimals);
  RPT_reporting_add_real (local_data->cumul_nanimals_tested_by_reason[reason], nanimals);
  RPT_reporting_add_real (local_data->cumul_nanimals_tested_by_prodtype[prodtype], nanimals);
  RPT_reporting_add_real (local_data->cumul_nanimals_tested_by_reason_and_prodtype[reason][prodtype], nanimals);

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
  UNT_production_type_t prodtype;

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
  prodtype = unit->production_type;

  if (event->positive)
    {
      if (event->correct)
        {
          RPT_reporting_add_integer (local_data->nunits_truepos, 1);
          RPT_reporting_add_integer (local_data->nunits_truepos_by_prodtype[prodtype], 1);
          RPT_reporting_add_integer (local_data->cumul_nunits_truepos, 1);
          RPT_reporting_add_integer (local_data->cumul_nunits_truepos_by_prodtype[prodtype], 1);
        }
      else
        {
          RPT_reporting_add_integer (local_data->nunits_falsepos, 1);
          RPT_reporting_add_integer (local_data->nunits_falsepos_by_prodtype[prodtype], 1);
          RPT_reporting_add_integer (local_data->cumul_nunits_falsepos, 1);
          RPT_reporting_add_integer (local_data->cumul_nunits_falsepos_by_prodtype[prodtype], 1);
        }
    }
  else /* test result was negative */
    {
      if (event->correct)
        {
          RPT_reporting_add_integer (local_data->nunits_trueneg, 1);
          RPT_reporting_add_integer (local_data->nunits_trueneg_by_prodtype[prodtype], 1);
          RPT_reporting_add_integer (local_data->cumul_nunits_trueneg, 1);
          RPT_reporting_add_integer (local_data->cumul_nunits_trueneg_by_prodtype[prodtype], 1);
        }
      else
        {
          RPT_reporting_add_integer (local_data->nunits_falseneg, 1);
          RPT_reporting_add_integer (local_data->nunits_falseneg_by_prodtype[prodtype], 1);
          RPT_reporting_add_integer (local_data->cumul_nunits_falseneg, 1);
          RPT_reporting_add_integer (local_data->cumul_nunits_falseneg_by_prodtype[prodtype], 1);
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
    case EVT_BeforeEachSimulation:
      handle_before_each_simulation_event (self);
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
  g_ptr_array_free (local_data->daily_outputs, /* free_seg = */ TRUE);
  g_ptr_array_free (local_data->cumul_outputs, /* free_seg = */ TRUE);
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
  EVT_event_type_t events_listened_for[] = {
    EVT_BeforeAnySimulations,
    EVT_BeforeEachSimulation,
    EVT_NewDay,
    EVT_Test,
    EVT_TestResult,
    0
  };
  guint nprodtypes;
  ADSM_control_reason reason;
  UNT_production_type_t prodtype;

#if DEBUG
  g_debug ("----- ENTER new (%s)", MODEL_NAME);
#endif

  self = g_new (adsm_module_t, 1);
  local_data = g_new (local_data_t, 1);

  self->name = MODEL_NAME;
  self->events_listened_for = adsm_setup_events_listened_for (events_listened_for);
  self->outputs = g_ptr_array_new();
  self->model_data = local_data;
  self->run = run;
  self->is_listening_for = adsm_model_is_listening_for;
  self->has_pending_actions = adsm_model_answer_no;
  self->has_pending_infections = adsm_model_answer_no;
  self->to_string = adsm_module_to_string_default;
  self->printf = adsm_model_printf;
  self->fprintf = adsm_model_fprintf;
  self->free = local_free;

  local_data->daily_outputs = g_ptr_array_new();
  local_data->cumul_outputs = g_ptr_array_new();
  local_data->production_types = units->production_type_names;
  nprodtypes = local_data->production_types->len;
  {
    RPT_bulk_create_t outputs[] = {
      { &local_data->nunits_tested, "tstnU", RPT_integer,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->nunits_tested_by_reason, "tstnU%s", RPT_integer,
        RPT_CharArray, ADSM_control_reason_abbrev, ADSM_NCONTROL_REASONS,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->nunits_tested_by_prodtype, "tstnU%s", RPT_integer,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->nunits_tested_by_reason_and_prodtype, "tstnU%s%s", RPT_integer,
        RPT_CharArray, ADSM_control_reason_abbrev, ADSM_NCONTROL_REASONS,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        self->outputs, local_data->daily_outputs },

      { &local_data->cumul_nunits_tested, "tstcU", RPT_integer,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nunits_tested_by_reason, "tstcU%s", RPT_integer,
        RPT_CharArray, ADSM_control_reason_abbrev, ADSM_NCONTROL_REASONS,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nunits_tested_by_prodtype, "tstcU%s", RPT_integer,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nunits_tested_by_reason_and_prodtype, "tstcU%s%s", RPT_integer,
        RPT_CharArray, ADSM_control_reason_abbrev, ADSM_NCONTROL_REASONS,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nanimals_tested, "tstcA", RPT_real,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nanimals_tested_by_reason, "tstcA%s", RPT_real,
        RPT_CharArray, ADSM_control_reason_abbrev, ADSM_NCONTROL_REASONS,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nanimals_tested_by_prodtype, "tstcA%s", RPT_real,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nanimals_tested_by_reason_and_prodtype, "tstcA%s%s", RPT_real,
        RPT_CharArray, ADSM_control_reason_abbrev, ADSM_NCONTROL_REASONS,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        self->outputs, local_data->cumul_outputs },

      { &local_data->nunits_truepos, "tstnUTruePos", RPT_integer,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->nunits_truepos_by_prodtype, "tstnUTruePos%s", RPT_integer,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->nunits_trueneg, "tstnUTrueNeg", RPT_integer,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->nunits_trueneg_by_prodtype, "tstnUTrueNeg%s", RPT_integer,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->nunits_falsepos, "tstnUFalsePos", RPT_integer,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->nunits_falsepos_by_prodtype, "tstnUFalsePos%s", RPT_integer,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->nunits_falseneg, "tstnUFalseNeg", RPT_integer,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->nunits_falseneg_by_prodtype, "tstnUFalseNeg%s", RPT_integer,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->daily_outputs },

      { &local_data->cumul_nunits_truepos, "tstcUTruePos", RPT_integer,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nunits_truepos_by_prodtype, "tstcUTruePos%s", RPT_integer,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nunits_trueneg, "tstcUTrueNeg", RPT_integer,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nunits_trueneg_by_prodtype, "tstcUTrueNeg%s", RPT_integer,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nunits_falsepos, "tstcUFalsePos", RPT_integer,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nunits_falsepos_by_prodtype, "tstcUFalsePos%s", RPT_integer,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nunits_falseneg, "tstcUFalseNeg", RPT_integer,
        RPT_NoSubcategory, NULL, 0,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { &local_data->cumul_nunits_falseneg_by_prodtype, "tstcUFalseNeg%s", RPT_integer,
        RPT_GPtrArray, local_data->production_types, nprodtypes,
        RPT_NoSubcategory, NULL, 0,
        self->outputs, local_data->cumul_outputs },

      { NULL }
    };  
    RPT_bulk_create (outputs);
  }

  /* The reasons for zones, vaccination, and destruction are all in the enum
   * ADSM_control_reasons.  Dispose of the reasons that don't apply to tests,
   * to keep the output neater. */
  for (reason = 0; reason < ADSM_NCONTROL_REASONS; reason++)
    {
      if (!(reason == ADSM_ControlTraceForwardDirect
            || reason == ADSM_ControlTraceForwardIndirect
            || reason == ADSM_ControlTraceBackDirect
            || reason ==  ADSM_ControlTraceBackIndirect))
        {
          g_ptr_array_remove_fast (self->outputs, local_data->nunits_tested_by_reason[reason] );
          g_ptr_array_remove_fast (self->outputs, local_data->cumul_nunits_tested_by_reason[reason] );
          g_ptr_array_remove_fast (self->outputs, local_data->cumul_nanimals_tested_by_reason[reason] );
          for (prodtype = 0; prodtype < nprodtypes; prodtype++)
            {
              g_ptr_array_remove_fast (self->outputs, local_data->nunits_tested_by_reason_and_prodtype[reason][prodtype] );
              g_ptr_array_remove_fast (self->outputs, local_data->cumul_nunits_tested_by_reason_and_prodtype[reason][prodtype] );
              g_ptr_array_remove_fast (self->outputs, local_data->cumul_nanimals_tested_by_reason_and_prodtype[reason][prodtype] );
            }
        }
    }

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file test_monitor.c */
