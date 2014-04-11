/** @file event.c
 * Functions for creating, destroying, printing, and manipulating events.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date March 2003
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

#if HAVE_MATH_H
#  include <math.h>
#endif

/* To avoid name clashes when dlpreopening multiple modules that have the same
 * global symbols (interface).  See sec. 18.4 of "GNU Autoconf, Automake, and
 * Libtool". */
#define EVT_free_event_as_GFunc event_LTX_EVT_free_event_as_GFunc

#if STDC_HEADERS
#  include <stdlib.h>
#endif

#include "spreadmodel.h"
#include "event.h"
#include "reporting.h"



/**
 * Names for the events of interest, terminated with a NULL sentinel.
 *
 * @sa EVT_event_type_t
 */
const char *EVT_event_type_name[] = {
  "BeforeAnySimulations",
  "OutputDirectory",
  "BeforeEachSimulation",
  "DeclarationOfVaccinationReasons",
  "DeclarationOfVaccineDelay",
  "DeclarationOfOutputs",
  "NewDay", "Exposure", "AttemptToInfect", "Infection", "Detection",
  "PublicAnnouncement", "Exam", "AttemptToTrace", "TraceResult", "Test",
  "TestResult",
  "RequestForVaccination", "CommitmentToVaccinate", "VaccinationCanceled",
  "Vaccination", "RequestForDestruction",
  "CommitmentToDestroy", "Destruction",
  "RequestForZoneFocus", "EndOfDay",
  "EndOfDay2",
  "LastDay",
  "Midnight",
  NULL
};



/**
 * Creates a new "before any simulations" event.
 *
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_before_any_simulations_event (void)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_BeforeAnySimulations;
  return event;
}



/**
 * Returns a text representation of a "before any simulations" event.
 *
 * @return a string.
 */
char *
EVT_before_any_simulations_event_to_string (void)
{
  return g_strdup ("<Before any simulations event>");
}



/**
 * Creates a new "output directory" event.
 *
 * @param output_dir a path (absolute or relative) to the output directory.
 *   The path is copied and can be freed after this event is created.
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_output_dir_event (char *output_dir)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_OutputDirectory;
  event->u.output_dir.output_dir = g_strdup(output_dir);
  return event;
}



/**
 * Returns a text representation of an "output directory" event.
 *
 * @param event an "output directory" event.
 * @return a string.
 */
char *
EVT_output_dir_event_to_string (EVT_output_dir_event_t * event)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<Output directory event dir=\"%s\">", event->output_dir);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new "before each simulation" event.
 *
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_before_each_simulation_event (void)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_BeforeEachSimulation;
  return event;
}



/**
 * Returns a text representation of a "before each simulation" event.
 *
 * @return a string.
 */
char *
EVT_before_each_simulation_event_to_string (void)
{
  return g_strdup ("<Before each simulation event>");
}



/**
 * Creates a new "declaration of vaccination reasons" event.
 *
 * @param reasons an array of ordinary C strings giving the reasons for which
 *   a model may request vaccinations.  The pointer to the array is copied so
 *   the strings and the array structure itself should not be freed after
 *   calling this function.
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_declaration_of_vaccination_reasons_event (GPtrArray * reasons)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_DeclarationOfVaccinationReasons;
  event->u.declaration_of_vaccination_reasons.reasons = reasons;
  return event;
}



/**
 * Returns a text representation of a declaration of vaccination reasons event.
 *
 * @param event a declaration of vaccination reasons event.
 * @return a string.
 */
char *
EVT_declaration_of_vaccination_reasons_event_to_string
  (EVT_declaration_of_vaccination_reasons_event_t * event)
{
  GString *s;
  char *chararray;
  int i;

  s = g_string_new ("<Declaration of vaccination reasons event\n  reasons=");
  for (i = 0; i < event->reasons->len; i++)
    g_string_append_printf (s, i == 0 ? "\"%s\"" : ",\"%s\"",
                            (char *) g_ptr_array_index (event->reasons, i));
  g_string_append_c (s, '>');

  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new "declaration of vaccine delay" event.
 *
 * @param production_type the production type this delay applies to.
 * @param production_type_name the production type as a string.
 * @param delay the number of days between being vaccinated and becoming
 *   immune.
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_declaration_of_vaccine_delay_event (UNT_production_type_t production_type,
                                            char * production_type_name,
                                            int delay)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_DeclarationOfVaccineDelay;
  event->u.declaration_of_vaccine_delay.production_type = production_type;
  event->u.declaration_of_vaccine_delay.production_type_name = production_type_name;
  event->u.declaration_of_vaccine_delay.delay = delay;
  return event;
}



/**
 * Returns a text representation of a declaration of vaccine delay event.
 *
 * @param event a declaration of vaccine delay event.
 * @return a string.
 */
char *
EVT_declaration_of_vaccine_delay_event_to_string
  (EVT_declaration_of_vaccine_delay_event_t * event)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_printf (s, "<Declaration of vaccine delay event for \"%s\" delay=%i>",
                   event->production_type_name, event->delay);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new "declaration of outputs" event.
 *
 * @param outputs an array of pointers to RPT_reporting_t objects.  The pointer
 *   to the array is copied so the array structure should not be freed after
 *   calling this function.
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_declaration_of_outputs_event (GPtrArray * outputs)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_DeclarationOfOutputs;
  event->u.declaration_of_outputs.outputs = outputs;
  return event;
}



/**
 * Returns a text representation of a declaration of outputs event.
 *
 * @param event a declaration of outputs event.
 * @return a string.
 */
char *
EVT_declaration_of_outputs_event_to_string (EVT_declaration_of_outputs_event_t * event)
{
  GString *s;
  char *chararray;
  int i;

  s = g_string_new ("<Declaration of outputs event\n  outputs=");
  for (i = 0; i < event->outputs->len; i++)
    g_string_append_printf (s, i == 0 ? "\"%s\"" : ",\"%s\"",
                            ((RPT_reporting_t *) g_ptr_array_index (event->outputs, i))->name);
  g_string_append_c (s, '>');

  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new "new day" event.
 *
 * @param day the day of the simulation.
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_new_day_event (int day)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_NewDay;
  event->u.new_day.day = day;
  return event;
}



/**
 * Returns a text representation of a new day event.
 *
 * @param event a new day event.
 * @return a string.
 */
char *
EVT_new_day_event_to_string (EVT_new_day_event_t * event)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<New day event day=%i>", event->day);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new "exposure" event.
 *
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_exposure_event (UNT_unit_t * exposing_unit, UNT_unit_t * exposed_unit,
                        int day, SPREADMODEL_contact_type contact_type, gboolean traceable,
                        gboolean adequate, int delay)
{
  EVT_event_t *event;
  
  event = g_new (EVT_event_t, 1);
  event->type = EVT_Exposure;
  event->u.exposure.exposing_unit = exposing_unit;
  event->u.exposure.exposed_unit = exposed_unit;
  event->u.exposure.day = day;

  event->u.exposure.contact_type = contact_type;
  event->u.exposure.traceable = traceable;
  event->u.exposure.traced = FALSE;
  event->u.exposure.adequate = adequate;
  event->u.exposure.initiated_day = day;
  event->u.exposure.delay = delay;
  return event;
}



/**
 * Returns a text representation of an exposure event.
 *
 * @param event an exposure event.
 * @return a string.
 */
char *
EVT_exposure_event_to_string (EVT_exposure_event_t * event)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<Exposure event units=\"%s\"->\"%s\" (%s) day=%i traceable=%i>",
                    event->exposing_unit->official_id,
                    event->exposed_unit->official_id,
                    SPREADMODEL_contact_type_name[event->contact_type], event->day, event->traceable);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new "attempt to infect" event.
 *
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_attempt_to_infect_event (UNT_unit_t * infecting_unit,
                                 UNT_unit_t * infected_unit, int day,
                                 SPREADMODEL_contact_type contact_type)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_AttemptToInfect;
  event->u.attempt_to_infect.infecting_unit = infecting_unit;
  event->u.attempt_to_infect.infected_unit = infected_unit;
  event->u.attempt_to_infect.day = day;
  event->u.attempt_to_infect.contact_type = contact_type;
  /* The following three items cause this to be a normal infection, one that
   * starts from the start rather than being added to the simulation in-
   * progress. */
  event->u.attempt_to_infect.override_initial_state = Latent;
  event->u.attempt_to_infect.override_days_in_state = 0;
  event->u.attempt_to_infect.override_days_left_in_state = 0;

  return event;
}



/**
 * Returns a text representation of an attempt to infect event.
 *
 * @param event an attempt to infect event.
 * @return a string.
 */
char *
EVT_attempt_to_infect_event_to_string (EVT_attempt_to_infect_event_t * event)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<Attempt to infect event unit=\"%s\" day=%i",
                    event->infected_unit->official_id, event->day);
  if (event->override_initial_state > Susceptible)
    {
      g_string_append_printf (s, "\n start %s", UNT_state_name[event->override_initial_state]);
 
      if (event->override_days_in_state > 0)
        g_string_append_printf (s, " %i days elapsed", event->override_days_in_state);

      if (event->override_days_left_in_state > 0)
        g_string_append_printf (s, " %i days left", event->override_days_left_in_state);
    }
  g_string_append_c (s, '>');

  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new "infection" event.
 *
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_infection_event (UNT_unit_t * infecting_unit, UNT_unit_t * infected_unit,
                         int day, SPREADMODEL_contact_type contact_type)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_Infection;
  event->u.infection.infecting_unit = infecting_unit;
  event->u.infection.infected_unit = infected_unit;
  event->u.infection.day = day;
  event->u.infection.contact_type = contact_type;

  return event;
}



/**
 * Returns a text representation of an infection event.
 *
 * @param event an infection event.
 * @return a string.
 */
char *
EVT_infection_event_to_string (EVT_infection_event_t * event)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<Infection event unit=\"%s\" day=%i",
                    event->infected_unit->official_id, event->day);
  if (event->override_initial_state > Susceptible)
    {
      g_string_append_printf (s, "\n start %s", UNT_state_name[event->override_initial_state]);

      if (event->override_days_in_state > 0)
        g_string_append_printf (s, " %i days elapsed", event->override_days_in_state);

      if (event->override_days_left_in_state > 0)
        g_string_append_printf (s, " %i days left", event->override_days_left_in_state);
    }
  g_string_append_c (s, '>');

  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new "detection" event.
 *
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_detection_event (UNT_unit_t * unit, int day,
                         SPREADMODEL_detection_reason means,
                         SPREADMODEL_test_result test_result)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_Detection;
  event->u.detection.unit = unit;
  event->u.detection.day = day;
  event->u.detection.means = means;
  event->u.detection.test_result = test_result;
  return event;
}



/**
 * Returns a text representation of a detection event.
 *
 * @param event a detection event.
 * @return a string.
 */
char *
EVT_detection_event_to_string (EVT_detection_event_t * event)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<Detection event unit=\"%s\" day=%i>", event->unit->official_id,
                    event->day);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new "public announcement" event.
 *
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_public_announcement_event (int day)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_PublicAnnouncement;
  event->u.public_announcement.day = day;
  return event;
}



/**
 * Returns a text representation of a public announcement event.
 *
 * @param event a public announcement event.
 * @return a string.
 */
char *
EVT_public_announcement_event_to_string (EVT_public_announcement_event_t * event)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<Public announcement event day=%i>", event->day);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new "exam" event.
 *
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_exam_event (UNT_unit_t * unit, int day, SPREADMODEL_control_reason reason,
                    double detection_multiplier, gboolean test_if_no_signs)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_Exam;
  event->u.exam.unit = unit;
  event->u.exam.day = day;
  event->u.exam.reason = reason;
  event->u.exam.detection_multiplier = detection_multiplier;
  event->u.exam.test_if_no_signs = test_if_no_signs;
  return event;
}



/**
 * Returns a text representation of an exam event.
 *
 * @param event an exam event.
 * @return a string.
 */
char *
EVT_exam_event_to_string (EVT_exam_event_t * event)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<Exam event unit=\"%s\" day=%i detection multiplier=%g test if no signs=%s>",
                    event->unit->official_id, event->day,
                    event->detection_multiplier,
                    event->test_if_no_signs ? "yes" : "no");
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new "attempt to trace" event.
 *
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_attempt_to_trace_event (UNT_unit_t * unit, int day,
                                SPREADMODEL_contact_type contact_type,
                                SPREADMODEL_trace_direction direction,
                                int trace_period)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_AttemptToTrace;
  event->u.attempt_to_trace.unit = unit;
  event->u.attempt_to_trace.day = day;
  event->u.attempt_to_trace.contact_type = contact_type;
  event->u.attempt_to_trace.direction = direction;
  event->u.attempt_to_trace.trace_period = trace_period;
  return event;
}



/**
 * Returns a text representation of an attempt to trace event.
 *
 * @param event an attempt to trace event.
 * @return a string.
 */
char *
EVT_attempt_to_trace_event_to_string (EVT_attempt_to_trace_event_t * event)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<Attempt to trace event unit=\"%s\" (%s) day=%i %s direction=%s>",
                    event->unit->official_id,
                    event->unit->production_type_name,
                    event->day,
                    SPREADMODEL_contact_type_abbrev[event->contact_type],
                    SPREADMODEL_trace_direction_abbrev[event->direction]);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new "trace result" event.
 *
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_trace_result_event (UNT_unit_t * exposing_unit,
                            UNT_unit_t * exposed_unit,
                            SPREADMODEL_contact_type contact_type,
                            SPREADMODEL_trace_direction direction,
                            int day, int initiated_day, gboolean traced)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_TraceResult;
  event->u.trace_result.exposing_unit = exposing_unit;
  event->u.trace_result.exposed_unit = exposed_unit;
  event->u.trace_result.contact_type = contact_type;
  event->u.trace_result.direction = direction;
  event->u.trace_result.day = day;
  event->u.trace_result.initiated_day = initiated_day;
  event->u.trace_result.traced = traced;
  return event;
}



/**
 * Returns a text representation of a trace result event.
 *
 * @param event a trace result event.
 * @return a string.
 */
char *
EVT_trace_result_event_to_string (EVT_trace_result_event_t * event)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<Trace result event units=\"%s\" (%s)->\"%s\" (%s) day=%i initiated_day=%i %s direction=%s trace=%s>",
                    event->exposing_unit->official_id,
                    event->exposing_unit->production_type_name,
                    event->exposed_unit->official_id,
                    event->exposed_unit->production_type_name,
                    event->day,
                    event->initiated_day,
                    SPREADMODEL_contact_type_abbrev[event->contact_type],
                    SPREADMODEL_trace_direction_abbrev[event->direction],
                    event->traced == TRUE ? "succeeded" : "failed");
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new "test" event.
 *
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_test_event (UNT_unit_t * unit, int day, SPREADMODEL_control_reason reason)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_Test;
  event->u.test.unit = unit;
  event->u.test.day = day;
  event->u.test.reason = reason;
  return event;
}



/**
 * Returns a text representation of a test event.
 *
 * @param event a test event.
 * @return a string.
 */
char *
EVT_test_event_to_string (EVT_test_event_t * event)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<Test event unit=\"%s\" day=%i>",
		    event->unit->official_id, event->day);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new "test result" event.
 *
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_test_result_event (UNT_unit_t * unit, int day,
                           gboolean positive, gboolean correct,
                           SPREADMODEL_control_reason reason)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_TestResult;
  event->u.test_result.unit = unit;
  event->u.test_result.day = day;
  event->u.test_result.positive = positive;
  event->u.test_result.correct = correct;
  event->u.test_result.reason = reason;
  return event;
}



/**
 * Returns a text representation of a test result event.
 *
 * @param event a test result event.
 * @return a string.
 */
char *
EVT_test_result_event_to_string (EVT_test_result_event_t * event)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<Test result event unit=\"%s\" day=%i %s %s>",
                    event->unit->official_id, event->day,
                    event->correct ? "true" : "false",
                    event->positive ? "positive" : "negative");
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new "request for vaccination" event.
 *
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_request_for_vaccination_event (UNT_unit_t * unit,
                                       int day,
                                       char *reason,
                                       int priority,
                                       gboolean cancel_on_detection,
                                       int min_days_before_next)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_RequestForVaccination;
  event->u.request_for_vaccination.unit = unit;
  event->u.request_for_vaccination.day = day;
  event->u.request_for_vaccination.reason = reason;
  event->u.request_for_vaccination.priority = priority;
  event->u.request_for_vaccination.cancel_on_detection = cancel_on_detection;
  event->u.request_for_vaccination.min_days_before_next = min_days_before_next;
  event->u.request_for_vaccination.day_commitment_made = 0; /* default */
  return event;
}



/**
 * Returns a text representation of a request for vaccination event.
 *
 * @param event a request for vaccination event.
 * @return a string.
 */
char *EVT_request_for_vaccination_event_to_string (EVT_request_for_vaccination_event_t * event)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<Request for vaccination event unit=\"%s\" day=%i priority=%i cancel on detection=%s>",
                    event->unit->official_id, event->day, event->priority,
                    event->cancel_on_detection ? "yes" : "no");
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new "commitment to vaccinate" event.
 *
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_commitment_to_vaccinate_event (UNT_unit_t * unit, int day)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_CommitmentToVaccinate;
  event->u.commitment_to_vaccinate.unit = unit;
  event->u.commitment_to_vaccinate.day = day;
  return event;
}



/**
 * Returns a text representation of a commitment to vaccinate event.
 *
 * @param event a commitment to vaccinate event.
 * @return a string.
 */
char *EVT_commitment_to_vaccinate_event_to_string (EVT_commitment_to_vaccinate_event_t * event)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<Commitment to vaccinate event unit=\"%s\" day=%i>",
                    event->unit->official_id, event->day);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new "vaccination canceled" event.
 *
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_vaccination_canceled_event (UNT_unit_t * unit, int day,
                                    int day_commitment_made)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_VaccinationCanceled;
  event->u.vaccination_canceled.unit = unit;
  event->u.vaccination_canceled.day = day;
  event->u.vaccination_canceled.day_commitment_made = day_commitment_made;
  return event;
}



/**
 * Returns a text representation of a vaccination canceled event.
 *
 * @param event a vaccination canceled event.
 * @return a string.
 */
char *
EVT_vaccination_canceled_event_to_string (EVT_vaccination_canceled_event_t * event)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<Vaccination canceled event unit=\"%s\" day=%i>",
                    event->unit->official_id, event->day);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}




/**
 * Creates a new "vaccination" event for setting a unit's immunity state
 * in-progress.
 *
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_inprogress_immunity_event (UNT_unit_t * unit,
                                   int day, char *reason,
                                   UNT_state_t start_in_state,
                                   int days_in_state, int days_left_in_state)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_Vaccination;
  event->u.vaccination.unit = unit;
  event->u.vaccination.day = day;
  event->u.vaccination.reason = reason;
  event->u.vaccination.day_commitment_made = day;
  event->u.vaccination.override_initial_state = start_in_state;
  event->u.vaccination.override_days_in_state = days_in_state;
  event->u.vaccination.override_days_left_in_state = days_left_in_state;

  return event;
}



/**
 * Creates a new "vaccination" event.
 *
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_vaccination_event (UNT_unit_t * unit, int day, char *reason,
                           int day_commitment_made)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_Vaccination;
  event->u.vaccination.unit = unit;
  event->u.vaccination.day = day;
  event->u.vaccination.reason = reason;
  event->u.vaccination.day_commitment_made = day_commitment_made;
  /* The following three items cause this to be a normal immunity, one that
   * starts from the start rather than being added to the simulation in-
   * progress. */
  event->u.vaccination.override_initial_state = Susceptible;
  event->u.vaccination.override_days_in_state = 0;
  event->u.vaccination.override_days_left_in_state = 0;
  return event;
}



/**
 * Returns a text representation of a vaccination event.
 *
 * @param event a vaccination event.
 * @return a string.
 */
char *
EVT_vaccination_event_to_string (EVT_vaccination_event_t * event)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<Vaccination event unit=\"%s\" day=%i",
                    event->unit->official_id, event->day);
  if (event->override_initial_state == VaccineImmune)
    {
      g_string_append_printf (s, "\n start %s", UNT_state_name[event->override_initial_state]);

      if (event->override_days_in_state > 0)
        g_string_append_printf (s, " %i days elapsed", event->override_days_in_state);

      if (event->override_days_left_in_state > 0)
        g_string_append_printf (s, " %i days left", event->override_days_left_in_state);
    }
  g_string_append_c (s, '>');

  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new "request for destruction" event.
 *
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_request_for_destruction_event (UNT_unit_t * unit,
                                       int day,
                                       char *reason, int priority)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_RequestForDestruction;
  event->u.request_for_destruction.unit = unit;
  event->u.request_for_destruction.day = day;
  event->u.request_for_destruction.reason = reason;
  event->u.request_for_destruction.priority = priority;
  event->u.request_for_destruction.day_commitment_made = 0; /* default */
  return event;
}



/**
 * Returns a text representation of a request for destruction event.
 *
 * @param event a request for destruction event.
 * @return a string.
 */
char *EVT_request_for_destruction_event_to_string (EVT_request_for_destruction_event_t * event)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s,
                    "<Request for destruction event unit=\"%s\" day=%i priority=%i>",
                    event->unit->official_id, event->day, event->priority);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new "commitment to destroy" event.
 *
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_commitment_to_destroy_event (UNT_unit_t * unit, int day)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_CommitmentToDestroy;
  event->u.commitment_to_destroy.unit = unit;
  event->u.commitment_to_destroy.day = day;
  return event;
}



/**
 * Returns a text representation of a commitment to destroy event.
 *
 * @param event a commitment to destroy event.
 * @return a string.
 */
char *
EVT_commitment_to_destroy_event_to_string (EVT_commitment_to_destroy_event_t * event)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<Commitment to destroy event unit=\"%s\" day=%i>",
                    event->unit->official_id, event->day);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new "destruction" event.
 *
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_destruction_event (UNT_unit_t * unit, int day, char *reason,
                           int day_commitment_made)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_Destruction;
  event->u.destruction.unit = unit;
  event->u.destruction.day = day;
  event->u.destruction.reason = reason;
  event->u.destruction.day_commitment_made = day_commitment_made;
  return event;
}



/**
 * Returns a text representation of a destruction event.
 *
 * @param event a destruction event.
 * @return a string.
 */
char *
EVT_destruction_event_to_string (EVT_destruction_event_t * event)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<Destruction event unit=\"%s\" day=%i>", event->unit->official_id,
                    event->day);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new "request for zone focus" event.
 *
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_request_for_zone_focus_event (UNT_unit_t * unit, int day, char *reason)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_RequestForZoneFocus;
  event->u.request_for_zone_focus.unit = unit;
  event->u.request_for_zone_focus.day = day;
  event->u.request_for_zone_focus.reason = reason;
  return event;
}



/**
 * Returns a text representation of a request for zone focus event.
 *
 * @param event a request for zone focus event.
 * @return a string.
 */
char *
EVT_request_for_zone_focus_event_to_string (EVT_request_for_zone_focus_event_t * event)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s,
                    "<Request for zone focus event unit=\"%s\" day=%i>",
                    event->unit->official_id, event->day);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new "end of day" event.
 *
 * @param day the day of the simulation.
 * @param done whether the simulation is over or not.
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_end_of_day_event (int day, gboolean done)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_EndOfDay;
  event->u.end_of_day.day = day;
  event->u.end_of_day.done = done;
  return event;
}



/**
 * Returns a text representation of an end of day event.
 *
 * @param event an end of day event.
 * @return a string.
 */
char *
EVT_end_of_day_event_to_string (EVT_end_of_day_event_t * event)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<End of day event day=%i>", event->day);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new "end of day 2" event.
 *
 * @param day the day of the simulation.
 * @param done whether the simulation is over or not.
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_end_of_day2_event (int day, gboolean done)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_EndOfDay2;
  event->u.end_of_day2.day = day;
  event->u.end_of_day2.done = done;
  return event;
}



/**
 * Returns a text representation of an "end of day 2" event.
 *
 * @param event an end of day 2 event.
 * @return a string.
 */
char *
EVT_end_of_day2_event_to_string (EVT_end_of_day2_event_t * event)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<End of day 2 event day=%i>", event->day);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new "last day" event.
 *
 * @param day the day of the simulation.
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_last_day_event (int day)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_LastDay;
  event->u.last_day.day = day;
  return event;
}



/**
 * Returns a text representation of a last day event.
 *
 * @param event a last day event.
 * @return a string.
 */
char *
EVT_last_day_event_to_string (EVT_last_day_event_t * event)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<Last day event day=%i>", event->day);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Creates a new "midnight" event.
 *
 * @param day the day of the simulation.
 * @return a pointer to a newly-created EVT_event_t structure.
 */
EVT_event_t *
EVT_new_midnight_event (int day)
{
  EVT_event_t *event;

  event = g_new (EVT_event_t, 1);
  event->type = EVT_Midnight;
  event->u.midnight.day = day;
  return event;
}



/**
 * Returns a text representation of a midnight event.
 *
 * @param event a midnight event.
 * @return a string.
 */
char *
EVT_midnight_event_to_string (EVT_midnight_event_t * event)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<Midnight event day=%i>", event->day);
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Deletes an event from memory.
 *
 * @param event an event.
 */
void
EVT_free_event (EVT_event_t * event)
{
  if (event == NULL)
    return;

  switch (event->type)
    {
    case EVT_BeforeAnySimulations:
    case EVT_BeforeEachSimulation:
    case EVT_DeclarationOfVaccineDelay:
    case EVT_NewDay:
    case EVT_Exposure:
    case EVT_AttemptToInfect:
    case EVT_Infection:
    case EVT_Detection:
    case EVT_PublicAnnouncement:
    case EVT_Exam:
    case EVT_AttemptToTrace:
    case EVT_TraceResult:
    case EVT_Test:
    case EVT_TestResult:
    case EVT_RequestForVaccination:
    case EVT_CommitmentToVaccinate:
    case EVT_VaccinationCanceled:
    case EVT_Vaccination:
    case EVT_RequestForDestruction:
    case EVT_CommitmentToDestroy:
    case EVT_Destruction:
    case EVT_RequestForZoneFocus:
    case EVT_EndOfDay:
    case EVT_EndOfDay2:
    case EVT_LastDay:
    case EVT_Midnight:
      /* No dynamically-allocated parts to free. */
      break;
    case EVT_OutputDirectory:
      g_free (event->u.output_dir.output_dir);
      break;
    case EVT_DeclarationOfVaccinationReasons:
      /* Note that we do not free the C strings in the array of vaccination
       * reasons, because we assume they are static strings. */
      g_ptr_array_free (event->u.declaration_of_vaccination_reasons.reasons, TRUE);
      break;
    case EVT_DeclarationOfOutputs:
      /* Note that we free the GPtrArray structure that holds the list of
       * reporting variables, but we do not free the reporting variables
       * themselves.  We assume that will be done when the module owning those
       * reporting variables is freed. */
      g_ptr_array_free (event->u.declaration_of_outputs.outputs, TRUE);
      break;
    case EVT_NEVENT_TYPES:
      g_assert_not_reached();
    }
  g_free (event);
}



/**
 * Makes a deep copy of an event.
 *
 * @param event an event.
 * @return a deep copy of the event.
 */
EVT_event_t *
EVT_clone_event (EVT_event_t * event)
{
  EVT_event_t *clone;

  if (event == NULL)
    return NULL;

  switch (event->type)
    {
    case EVT_Exposure:
      {
        EVT_exposure_event_t *e;
        e = &(event->u.exposure);
        clone = EVT_new_exposure_event (e->exposing_unit, e->exposed_unit,
                                        e->day, e->contact_type, e->traceable, e->adequate, e->delay);
        break;
      }
    case EVT_AttemptToInfect:
      {
        EVT_attempt_to_infect_event_t *e;
        e = &(event->u.attempt_to_infect);
        clone = EVT_new_attempt_to_infect_event (e->infecting_unit,
                                                 e->infected_unit, e->day, e->contact_type);
        clone->u.attempt_to_infect.override_initial_state = e->override_initial_state;
        clone->u.attempt_to_infect.override_days_in_state = e->override_days_in_state;
        clone->u.attempt_to_infect.override_days_left_in_state = e->override_days_left_in_state;
        break;
      }
    case EVT_RequestForVaccination:
      {
        EVT_request_for_vaccination_event_t *e;
        e = &(event->u.request_for_vaccination);
        clone = EVT_new_request_for_vaccination_event (e->unit, e->day,
                                                       e->reason, e->priority,
                                                       e->cancel_on_detection,
                                                       e->min_days_before_next);
        break;
      }
    case EVT_Vaccination:
      {
        EVT_vaccination_event_t *e;
        e = &(event->u.vaccination);
        clone = EVT_new_vaccination_event (e->unit, e->day, e->reason, e->day_commitment_made);
        clone->u.vaccination.override_initial_state = e->override_initial_state;
        clone->u.vaccination.override_days_in_state = e->override_days_in_state;
        clone->u.vaccination.override_days_left_in_state = e->override_days_left_in_state;
        break;
      }
    case EVT_RequestForDestruction:
      {
        EVT_request_for_destruction_event_t *e;
        e = &(event->u.request_for_destruction);
        clone = EVT_new_request_for_destruction_event (e->unit, e->day, e->reason, e->priority);
        break;
      }
    case EVT_Destruction:
      {
        EVT_destruction_event_t *e;
        e = &(event->u.destruction);
        clone = EVT_new_destruction_event (e->unit, e->day, e->reason, e->day_commitment_made);
        break;
      }
    default:
      g_assert_not_reached ();
    }

  return clone;
}



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
 * Returns a text representation of an event.
 *
 * @param event an event.
 * @return a string.
 */
char *
EVT_event_to_string (EVT_event_t * event)
{
  char *s;

  switch (event->type)
    {
    case EVT_BeforeAnySimulations:
      s = EVT_before_any_simulations_event_to_string ();
      break;
    case EVT_OutputDirectory:
      s = EVT_output_dir_event_to_string (&(event->u.output_dir));
      break;
    case EVT_BeforeEachSimulation:
      s = EVT_before_each_simulation_event_to_string ();
      break;
    case EVT_DeclarationOfVaccinationReasons:
      s =
        EVT_declaration_of_vaccination_reasons_event_to_string (&
                                                                (event->u.
                                                                 declaration_of_vaccination_reasons));
      break;
    case EVT_DeclarationOfVaccineDelay:
      s =
        EVT_declaration_of_vaccine_delay_event_to_string (&(event->u.declaration_of_vaccine_delay));
      break;
    case EVT_DeclarationOfOutputs:
      s = EVT_declaration_of_outputs_event_to_string (&(event->u.declaration_of_outputs));
      break;
    case EVT_NewDay:
      s = EVT_new_day_event_to_string (&(event->u.new_day));
      break;
    case EVT_Exposure:
      s = EVT_exposure_event_to_string (&(event->u.exposure));
      break;
    case EVT_AttemptToInfect:
      s = EVT_attempt_to_infect_event_to_string (&(event->u.attempt_to_infect));
      break;
    case EVT_Infection:
      s = EVT_infection_event_to_string (&(event->u.infection));
      break;
    case EVT_Detection:
      s = EVT_detection_event_to_string (&(event->u.detection));
      break;
    case EVT_PublicAnnouncement:
      s = EVT_public_announcement_event_to_string (&(event->u.public_announcement));
      break;
    case EVT_Exam:
      s = EVT_exam_event_to_string (&(event->u.exam));
      break;
    case EVT_AttemptToTrace:
      s = EVT_attempt_to_trace_event_to_string (&(event->u.attempt_to_trace));
      break;
    case EVT_TraceResult:
      s = EVT_trace_result_event_to_string (&(event->u.trace_result));
      break;
    case EVT_Test:
      s = EVT_test_event_to_string (&(event->u.test));
      break;
    case EVT_TestResult:
      s = EVT_test_result_event_to_string (&(event->u.test_result));
      break;
    case EVT_RequestForVaccination:
      s = EVT_request_for_vaccination_event_to_string (&(event->u.request_for_vaccination));
      break;
    case EVT_CommitmentToVaccinate:
      s = EVT_commitment_to_vaccinate_event_to_string (&(event->u.commitment_to_vaccinate));
      break;
    case EVT_VaccinationCanceled:
      s = EVT_vaccination_canceled_event_to_string (&(event->u.vaccination_canceled));
      break;
    case EVT_Vaccination:
      s = EVT_vaccination_event_to_string (&(event->u.vaccination));
      break;
    case EVT_RequestForDestruction:
      s = EVT_request_for_destruction_event_to_string (&(event->u.request_for_destruction));
      break;
    case EVT_CommitmentToDestroy:
      s = EVT_commitment_to_destroy_event_to_string (&(event->u.commitment_to_destroy));
      break;
    case EVT_Destruction:
      s = EVT_destruction_event_to_string (&(event->u.destruction));
      break;
    case EVT_RequestForZoneFocus:
      s = EVT_request_for_zone_focus_event_to_string (&(event->u.request_for_zone_focus));
      break;
    case EVT_EndOfDay:
      s = EVT_end_of_day_event_to_string (&(event->u.end_of_day));
      break;
    case EVT_EndOfDay2:
      s = EVT_end_of_day2_event_to_string (&(event->u.end_of_day2));
      break;
    case EVT_LastDay:
      s = EVT_last_day_event_to_string (&(event->u.last_day));
      break;
    case EVT_Midnight:
      s = EVT_midnight_event_to_string (&(event->u.midnight));
      break;
    default:
      g_assert_not_reached ();
    }

  return s;
}



/**
 * Prints an event.
 *
 * @param stream a stream to write to.  If NULL, defaults to stdout.
 * @param event an event.
 * @return the number of characters printed (not including the trailing '\\0').
 */
int
EVT_fprintf_event (FILE * stream, EVT_event_t * event)
{
  char *s;
  int nchars_written = 0;

  s = EVT_event_to_string (event);
  nchars_written = fprintf (stream ? stream : stdout, "%s", s);
  free (s);
  return nchars_written;
}



/**
 * Creates a new, empty event queue.
 *
 * @return a pointer to a newly-created event queue.
 */
EVT_event_queue_t *
EVT_new_event_queue (void)
{
  EVT_event_queue_t *queue;
  
  queue = g_new(EVT_event_queue_t, 1);
  queue->current_wave = g_ptr_array_new();
  queue->next_wave = g_ptr_array_new();
  return queue;
}



/**
 * Retrieves the next event from an event queue.  Returns NULL if the queue is
 * empty.
 *
 * @param queue an event queue.
 * @param rng a random number generator.
 * @return an event.
 */
EVT_event_t *
EVT_event_dequeue (EVT_event_queue_t *queue, RAN_gen_t *rng)
{
  EVT_event_t *event;
  GPtrArray *tmp;

  if (queue->current_wave->len == 0)
    {
#if DEBUG
      g_debug ("next wave");
#endif
      tmp = queue->current_wave;
      queue->current_wave = queue->next_wave;
      queue->next_wave = tmp;
    }  
  if (queue->current_wave->len == 0)
    event = NULL;
  else
    {
      guint i;
      /* Pick one randomly */
      i = (guint) floor (RAN_num(rng) * (queue->current_wave->len));
      event = (EVT_event_t *) g_ptr_array_remove_index_fast (queue->current_wave, i);
    }

  return event;
}



/**
 * Deletes an event queue from memory.
 *
 * @param queue an event queue.
 */
void
EVT_free_event_queue (EVT_event_queue_t * queue)
{
  if (queue == NULL)
    return;

  g_ptr_array_foreach (queue->current_wave, EVT_free_event_as_GFunc, NULL);
  g_ptr_array_free (queue->current_wave, TRUE);
  g_ptr_array_foreach (queue->next_wave, EVT_free_event_as_GFunc, NULL);
  g_ptr_array_free (queue->next_wave, TRUE);
  g_free (queue);
}



/**
 * Returns a text representation of an event queue.
 *
 * @param queue an event queue.
 * @return a string.
 */
char *
EVT_event_queue_to_string (EVT_event_queue_t * queue)
{
  guint i, n;                  /* iterator over events in the list */
  EVT_event_t *event;
  GString *s;
  char *substring, *chararray;

  s = g_string_new ("<event queue (starting with next)=\n");

  n = queue->current_wave->len;
  for (i = 0; i < n; i++)
    {
      event = (EVT_event_t *) g_ptr_array_index (queue->current_wave, i);
      substring = EVT_event_to_string (event);
      g_string_append (s, substring);
      g_string_append_c (s, '\n');
      g_free (substring);
    }
  n = queue->next_wave->len;
  for (i = 0; i < n; i++)
    {
      event = (EVT_event_t *) g_ptr_array_index (queue->next_wave, i);
      substring = EVT_event_to_string (event);
      g_string_append (s, substring);
      g_string_append_c (s, '\n');
      g_free (substring);
    }
  g_string_append (s, ">");
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Prints an event queue.
 *
 * @param stream a stream to write to.
 * @param queue an event queue.
 * @return the number of characters printed (not including the trailing '\\0').
 */
int
EVT_fprintf_event_queue (FILE * stream, EVT_event_queue_t * queue)
{
  char *s;
  int nchars_written;

  s = EVT_event_queue_to_string (queue);
  nchars_written = fprintf (stream, "%s", s);
  free (s);
  return nchars_written;
}

/* end of file event.c */
