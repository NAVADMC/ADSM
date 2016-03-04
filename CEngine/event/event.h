/** @file event.h
 * Events that can occur in the simulation.
 *
 * One goal of this system is to be able to treat modules as interchangeable,
 * mix-and-match parts.  We use an Observer or Publish-Subscribe system where
 * modules announce any changes they make to units (events) and listen for
 * events announced by other sub-models.
 *
 * @image html events.png
 *
 * Many ADSM events correspond to real-world events, for example, the
 * <i>Exposure</i> and <i>TestResult</i> events.
 * Three events are used to control timing:
 * <i>NewDay</i> is the event that initiates all daily processes,
 * <i>EndOfDay</i> is issued when all events that result (chain-reaction style)
 * from the NewDay event have wound down,
 * and <i>Midnight</i> is an event that occurs between simulation days,
 * when units change state and zones change shape.
 * The EndOfDay event is a useful signal for modules that write output,
 * because it signals that counts will not change past this point,
 * <i>e.g.</i>, all Detections that are going to occur today have occurred.
 *
 * @image html clock_24_hour.png
 *
 * Symbols from this module begin with EVT_.
 *
 * @sa event_manager.h
 * @sa model.h
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

#ifndef EVENT_H
#define EVENT_H

#include <stdio.h>
#include "adsm.h"
#include "rng.h"

#if STDC_HEADERS
#  include <stdlib.h>
#endif

#include <glib.h>



/** Events of interest. */
typedef enum
{
  EVT_UnknownEvent,
  EVT_BeforeAnySimulations,
  EVT_OutputDirectory,
  EVT_BeforeEachSimulation,
  EVT_DeclarationOfVaccineDelay,
  EVT_DeclarationOfOutputs,
  EVT_NewDay, EVT_Exposure, EVT_Infection,
  EVT_Detection,
  EVT_Quarantine,
  EVT_PublicAnnouncement, EVT_Exam, EVT_AttemptToTrace,
  EVT_TraceResult, EVT_Test, EVT_TestResult,
  EVT_RequestToInitiateVaccination,
  EVT_VaccinationInitiated,
  EVT_RequestForVaccination,
  EVT_CommitmentToVaccinate, EVT_VaccinationCanceled,
  EVT_Vaccination,
  EVT_RequestToTerminateVaccination,
  EVT_VaccinationTerminated,
  EVT_RequestForDestruction, EVT_CommitmentToDestroy,
  EVT_Destruction, EVT_RequestForZoneFocus, EVT_EndOfDay,
  EVT_EndOfDay2,
  EVT_Midnight,
  EVT_UnitStateChange,
  EVT_UnitZoneChange,
  EVT_NEVENT_TYPES
}
EVT_event_type_t;

extern const char *EVT_event_type_name[];



/**
 * A "before any simulations" event.  This event signals modules to do initial
 * setup.
 */
typedef struct
{
  int dummy; /**< to avoid a "struct has no members" warning */
}
EVT_before_any_simulations_event_t;



/**
 * An "output directory" event.  This event signals modules that produce file
 * output to write to a specific directory.
 */
typedef struct
{
  char *output_dir;
}
EVT_output_dir_event_t;



/**
 * A "before each simulation" event.  This event signals modules to do per-
 * simulation setup.
 */
typedef struct
{
  int iteration_number;
}
EVT_before_each_simulation_event_t;



/**
 * A "declaration of vaccine delay" event.  The vaccine module uses this event
 * to communicate how long the delay to vaccine immunity is for their
 * production type.  This bit of information is needed in the conflict resolver
 * module to handle one special case.
 */
typedef struct
{
  UNT_production_type_t production_type;
  char *production_type_name;
  int delay;
}
EVT_declaration_of_vaccine_delay_event_t;



/**
 * A "declaration of outputs" event.  Modules that track outputs use this event
 * to communicate which outputs they track, in case other modules want to use
 * or aggregate those outputs.
 */
typedef struct
{
  GPtrArray *outputs; /**< array of pointers to RPT_reporting_t objects */
}
EVT_declaration_of_outputs_event_t;



/** A "new day" event. */
typedef struct
{
  int day; /**< day of the simulation */
}
EVT_new_day_event_t;



/** An "exposure" event. */
typedef struct
{
  UNT_unit_t *exposing_unit;
  UNT_unit_t *exposed_unit;
  int day;       /**< day of the simulation */
  ADSM_contact_type contact_type;
  gboolean traceable;
  gboolean traced;
  gboolean adequate;
  int initiated_day;
  int delay;
  UNT_state_t override_initial_state; /**< when using an exposure event to
    specify an in-progress infection, set this to the unit's state (Latent,
    InfectiousSubclinical, or InfectiousClinical). */
  int override_days_in_state; /**< when using an exposure event to specify an
    in-progress infection, use a non-zero value here to give the number of days
    a unit has been in its current state. */
  int override_days_left_in_state; /**< when using an exposure event to
    specify an in-progress infection, use a non-zero value here to give the
    number of days until the unit transitions to the next state.  A zero value
    means that the number should be chosen from the probability distributions
    given in the disease model parameters. */
}
EVT_exposure_event_t;



/** An "infection" event. */
typedef struct
{
  UNT_unit_t *infecting_unit;
  UNT_unit_t *infected_unit;
  int day; /**< day of the simulation */
  ADSM_contact_type contact_type;
  UNT_state_t override_initial_state; /**< when using an infection event to
    specify an in-progress infection, set this to the unit's state (Latent,
    InfectiousSubclinical, or InfectiousClinical). */
  int override_days_in_state; /**< when using an infection event to specify an
    in-progress infection, use a non-zero value here to give the number of days
    a unit has been in its current state. */
  int override_days_left_in_state; /**< when using an infection event to
    specify an in-progress infection, use a non-zero value here to give the
    number of days until the unit transitions to the next state.  A zero value
    means that the number should be chosen from the probability distributions
    given in the disease model parameters. */
}
EVT_infection_event_t;



/** A "detection" event. */
typedef struct
{
  UNT_unit_t *unit;
  int day; /**< day of the simulation */
  ADSM_detection_reason means; /**< how the unit was detected */
  ADSM_test_result test_result; /**< If detection was by diagnostic testing, what was the test result? **/
}
EVT_detection_event_t;



/** A "quarantine" event. */
typedef struct
{
  UNT_unit_t *unit;
  int day; /**< day of the simulation */
}
EVT_quarantine_event_t;



/** A "public announcement" event. */
typedef struct
{
  int day;
}
EVT_public_announcement_event_t;



/** An "exam" event. */
typedef struct
{
  UNT_unit_t *unit;
  int day;
  ADSM_control_reason reason;
  double detection_multiplier;
  gboolean test_if_no_signs;
}
EVT_exam_event_t;



/** An "attempt to trace" event. */
typedef struct
{
  UNT_unit_t *unit;
  int day;
  ADSM_contact_type contact_type;
  ADSM_trace_direction direction;
  int trace_period;
}
EVT_attempt_to_trace_event_t;



/** A "trace result" event. */
typedef struct
{
  UNT_unit_t *exposing_unit;
  UNT_unit_t *exposed_unit;
  ADSM_contact_type contact_type;
  ADSM_trace_direction direction;
  int day;
  int initiated_day;
  gboolean traced;
}
EVT_trace_result_event_t;


/** A "test" event. */
typedef struct
{
  UNT_unit_t *unit;
  int day;
  ADSM_control_reason reason;
}
EVT_test_event_t;



/** A "test result" event. */
typedef struct
{
  UNT_unit_t *unit;
  int day;
  gboolean positive;
  gboolean correct; /**< enables tracking true and false positives and negatives */
  ADSM_control_reason reason;
}
EVT_test_result_event_t;



/** A "request to initiate vaccination" event. */
typedef struct
{
  int day;
  guint trigger_id;
  char *trigger_name;
}
EVT_request_to_initiate_vaccination_event_t;



/** A "vaccination initiated" event. */
typedef struct
{
  int day;
  guint trigger_id;
}
EVT_vaccination_initiated_event_t;



/** A "request for vaccination" event. */
typedef struct
{
  UNT_unit_t *unit;
  UNT_unit_t *focus_unit; /**< The unit at the center of the ring */
  int day;
  ADSM_control_reason reason; /**< why vaccination was requested */
  int day_commitment_made; /**< the day on which a commitment to fulfil this
    request was made. */
  double distance_from_ring_center;
  double supp_radius; /**< the radius of the suppressive circle around the
    focus unit, or -1 if no suppressive vaccination is done around the focus
    unit **/
  double prot_inner_radius; /**< the inner radius of the protective ring around
    the focus herd, or -1 if no protective vaccination is done around the focus
    herd **/
  double prot_outer_radius; /**< the outer radius of the protective ring around
    the focus herd, or -1 if no protective vaccination is done around the focus
    herd **/
}
EVT_request_for_vaccination_event_t;



/** A "commitment to vaccinate" event. */
typedef struct
{
  UNT_unit_t *unit;
  int day;
}
EVT_commitment_to_vaccinate_event_t;



/** A "vaccination canceled" event. */
typedef struct
{
  UNT_unit_t *unit;
  int day;
  int day_commitment_made; /**< the day on which a commitment to do this
    vaccination was made. */  
}
EVT_vaccination_canceled_event_t;



/** A "vaccination" event. */
typedef struct
{
  UNT_unit_t *unit;
  int day;
  ADSM_control_reason reason; /**< why vaccination was requested */
  int day_commitment_made; /**< the day on which a commitment to do this
    vaccination was made. */
  UNT_state_t override_initial_state; /**< when using a vaccination event to
    specify in-progress immunity, set this to VaccineImmune. */
  int override_days_in_state; /**< when using a vaccination event to specify
    in-progress immunity, use a non-zero value here to give the number of days
    a unit has been in its current state. */
  int override_days_left_in_state; /**< when using a vaccination event to
    specify in-progress immunity, use a non-zero value here to give the number
    of days until the unit transitions to the next state.  A zero value means
    that the number should be chosen from the probability distribution given
    in the disease model parameters. */
}
EVT_vaccination_event_t;



/** A "request to terminate vaccination" event. */
typedef struct
{
  int day;
}
EVT_request_to_terminate_vaccination_event_t;



/** A "vaccination terminated" event. */
typedef struct
{
  int day;
}
EVT_vaccination_terminated_event_t;



/** A "request for destruction" event. */
typedef struct
{
  UNT_unit_t *unit;
  int day;
  int priority;
  ADSM_control_reason reason; /**< why destruction was requested */
  int day_commitment_made; /**< the day on which a commitment to fulfil this
    request was made. */
}
EVT_request_for_destruction_event_t;



/** A "commitment to destroy" event. */
typedef struct
{
  UNT_unit_t *unit;
  int day;
}
EVT_commitment_to_destroy_event_t;



/** A "destruction" event. */
typedef struct
{
  UNT_unit_t *unit;
  int day;
  ADSM_control_reason reason; /**< why destruction was requested */
  int day_commitment_made; /**< the day on which a commitment to do this
    destruction was made. */
}
EVT_destruction_event_t;



/** A "request for zone focus" event. */
typedef struct
{
  UNT_unit_t *unit;
  int day;
  ADSM_control_reason reason; /**< why a zone focus was requested */
}
EVT_request_for_zone_focus_event_t;



/**
 * An "end of day" event.  Only the conflict resolver module should ever
 * respond to this event, otherwise the "end of day" could create more
 * potentially conflicting events and we'd need a second conflict resolver...
 */
typedef struct
{
  int day; /**< day of the simulation */
  gboolean done; /**< indicates whether the simulation is done or not.  The
    decision as to whether the simulation is "done" may depend on the maximum
    number of days being reached, the first detection being reached, the
    absence of disease, or other exit conditions. */
}
EVT_end_of_day_event_t;



/**
 * An "end of day 2" event.  Only the full table writer module should ever
 * respond to this event.  This is a kludge added to make sure the infection
 * events announced from the conflict resolver module are counted before the
 * full table writer writes the day's output variable values.
 */
typedef struct
{
  int day; /**< day of the simulation */
  gboolean done; /**< indicates whether the simulation is done or not.  The
    decision as to whether the simulation is "done" may depend on the maximum
    number of days being reached, the first detection being reached, the
    absence of disease, or other exit conditions. */
}
EVT_end_of_day2_event_t;



/**
 * A "last day" event.  This event is specifically for alerting modules to
 * compute the values of output variables that were only requested for the last
 * day of output.
 */
typedef struct
{
  int day; /**< day of the simulation */
}
EVT_last_day_event_t;



/**
 * A "midnight" event.  This event is specifically for triggering things that
 * happen between simulation days. */
typedef struct
{
  int day; /**< simulation day that begins just after midnight */
}
EVT_midnight_event_t;



/** A "unit state change" event. */
typedef struct
{
  UNT_unit_t *unit;
  UNT_state_t old_state;
  UNT_state_t new_state;
  int day; /**< simulation day on which the new state applies */
}
EVT_unit_state_change_event_t;



/** A "unit zone change" event. */
typedef struct
{
  UNT_unit_t *unit;
  ZON_zone_t *old_zone;
  ZON_zone_t *new_zone;
  int day; /**< simulation day on which the new zone membership applies */
}
EVT_unit_zone_change_event_t;



/** A supertype for all events. */
typedef struct
{
  EVT_event_type_t type;
  union
  {
    EVT_before_any_simulations_event_t before_any_simulations;
    EVT_output_dir_event_t output_dir;
    EVT_before_each_simulation_event_t before_each_simulation;
    EVT_declaration_of_vaccine_delay_event_t declaration_of_vaccine_delay;
    EVT_declaration_of_outputs_event_t declaration_of_outputs;
    EVT_new_day_event_t new_day;
    EVT_exposure_event_t exposure;
    EVT_infection_event_t infection;
    EVT_detection_event_t detection;
    EVT_quarantine_event_t quarantine;
    EVT_public_announcement_event_t public_announcement;
    EVT_exam_event_t exam;
    EVT_attempt_to_trace_event_t attempt_to_trace;
    EVT_trace_result_event_t trace_result;
    EVT_test_event_t test;
    EVT_test_result_event_t test_result;
    EVT_request_to_initiate_vaccination_event_t request_to_initiate_vaccination;
    EVT_vaccination_initiated_event_t vaccination_initiated;
    EVT_request_for_vaccination_event_t request_for_vaccination;
    EVT_commitment_to_vaccinate_event_t commitment_to_vaccinate;
    EVT_vaccination_canceled_event_t vaccination_canceled;
    EVT_vaccination_event_t vaccination;
    EVT_request_to_terminate_vaccination_event_t request_to_terminate_vaccination;
    EVT_vaccination_terminated_event_t vaccination_terminated;
    EVT_request_for_destruction_event_t request_for_destruction;
    EVT_commitment_to_destroy_event_t commitment_to_destroy;
    EVT_destruction_event_t destruction;
    EVT_request_for_zone_focus_event_t request_for_zone_focus;
    EVT_end_of_day_event_t end_of_day;
    EVT_end_of_day2_event_t end_of_day2;
    EVT_midnight_event_t midnight;
    EVT_unit_state_change_event_t unit_state_change;
    EVT_unit_zone_change_event_t unit_zone_change;
  }
  u;
}
EVT_event_t;



/** A pool of events. */
typedef struct
{
  GPtrArray *current_wave;
  GPtrArray *next_wave;
} EVT_event_queue_t;



/* Prototypes. */
EVT_event_t *EVT_new_before_any_simulations_event (void);
EVT_event_t *EVT_new_output_dir_event (char *);
EVT_event_t *EVT_new_before_each_simulation_event (int iteration_number);
EVT_event_t *EVT_new_declaration_of_vaccination_reasons_event (GPtrArray * reasons);
EVT_event_t *EVT_new_declaration_of_vaccine_delay_event (UNT_production_type_t,
                                                         char * production_type_name,
                                                         int);
EVT_event_t *EVT_new_declaration_of_outputs_event (GPtrArray *);
EVT_event_t *EVT_new_new_day_event (int day);
EVT_event_t *EVT_new_exposure_event (UNT_unit_t * exposing_unit,
                                     UNT_unit_t * exposed_unit,
                                     int day,
                                     ADSM_contact_type,
                                     gboolean traceable,
                                     gboolean adequate,
                                     int delay);
EVT_event_t *EVT_new_attempt_to_infect_event (UNT_unit_t * infecting_unit,
                                              UNT_unit_t * infected_unit,
                                              int day, ADSM_contact_type);
EVT_event_t *EVT_new_infection_event (UNT_unit_t * infecting_unit,
                                      UNT_unit_t * infected_unit,
                                      int day, ADSM_contact_type);
EVT_event_t *EVT_new_detection_event (UNT_unit_t *, int day,
                                      ADSM_detection_reason,
                                      ADSM_test_result);
EVT_event_t *EVT_new_quarantine_event (UNT_unit_t *, int day);
EVT_event_t *EVT_new_public_announcement_event (int day);
EVT_event_t *EVT_new_exam_event (UNT_unit_t *,
                                 int day,
                                 ADSM_control_reason,
                                 double detection_multiplier,
                                 gboolean test_if_no_signs);
EVT_event_t *EVT_new_attempt_to_trace_event (UNT_unit_t *,
                                             int day,
                                             ADSM_contact_type,
                                             ADSM_trace_direction,
                                             int trace_period);
EVT_event_t *EVT_new_trace_result_event (UNT_unit_t * exposing_unit,
                                         UNT_unit_t * exposed_unit,
                                         ADSM_contact_type,
                                         ADSM_trace_direction,
                                         int day, int initiated_day, gboolean traced);
EVT_event_t *EVT_new_test_event (UNT_unit_t *,
                                 int day,
                                 ADSM_control_reason);
EVT_event_t *EVT_new_test_result_event (UNT_unit_t *,
                                        int day,
                                        gboolean positive,
                                        gboolean correct,
                                        ADSM_control_reason);
EVT_event_t *EVT_new_request_to_initiate_vaccination_event (int day,
                                                            guint trigger_id,
                                                            char *trigger_name);
EVT_event_t *EVT_new_vaccination_initiated_event (int day,
                                                  guint trigger_id);
EVT_event_t *EVT_new_request_for_vaccination_event (UNT_unit_t *,
                                                    UNT_unit_t *focus_unit,
                                                    int day,
                                                    ADSM_control_reason,
                                                    double distance_from_ring_center,
                                                    double supp_radius,
                                                    double prot_inner_radius,
                                                    double prot_outer_radius);
EVT_event_t *EVT_new_commitment_to_vaccinate_event (UNT_unit_t *, int day);
EVT_event_t *EVT_new_vaccination_canceled_event (UNT_unit_t *, int day,
                                                 int day_commitment_made);
EVT_event_t *EVT_new_inprogress_immunity_event (UNT_unit_t * unit,
                                                int day,
                                                ADSM_control_reason,
                                                UNT_state_t start_in_state,
                                                int days_in_state,
                                                int days_left_in_state);
EVT_event_t *EVT_new_vaccination_event (UNT_unit_t *, int day,
                                        ADSM_control_reason,
                                        int day_commitment_made);
EVT_event_t *EVT_new_request_to_terminate_vaccination_event (int day);
EVT_event_t *EVT_new_vaccination_terminated_event (int day);
EVT_event_t *EVT_new_request_for_destruction_event (UNT_unit_t *,
                                                    int day,
                                                    ADSM_control_reason, int priority);
EVT_event_t *EVT_new_commitment_to_destroy_event (UNT_unit_t *, int day);
EVT_event_t *EVT_new_destruction_event (UNT_unit_t *, int day, ADSM_control_reason,
                                        int day_commitment_made);
EVT_event_t *EVT_new_request_for_zone_focus_event (UNT_unit_t *,
                                                   int day, ADSM_control_reason);
EVT_event_t *EVT_new_end_of_day_event (int day, gboolean done);
EVT_event_t *EVT_new_end_of_day2_event (int day, gboolean done);
EVT_event_t *EVT_new_midnight_event (int day);
EVT_event_t *EVT_new_unit_state_change_event (UNT_unit_t *,
                                              UNT_state_t old_state,
                                              UNT_state_t new_state,
                                              int day);
EVT_event_t *EVT_new_unit_zone_change_event (UNT_unit_t *,
                                             ZON_zone_t *old_zone,
                                             ZON_zone_t *new_zone,
                                             int day);

void EVT_free_event (EVT_event_t *);
EVT_event_t *EVT_clone_event (EVT_event_t *);
char *EVT_event_to_string (EVT_event_t *);
int EVT_fprintf_event (FILE *, EVT_event_t *);

#define EVT_printf_event(E) EVT_fprintf_event(stdout,E)

EVT_event_queue_t *EVT_new_event_queue (void);

/**
 * Adds an event to an event queue.
 *
 * @param Q an event queue.
 * @param E an event.
 */
#define EVT_event_enqueue(Q,E) g_ptr_array_add((Q)->next_wave,E)

/**
 * Returns whether an event queue is empty.
 *
 * @param Q an event queue.
 * @return TRUE if the queue is empty, FALSE otherwise.
 */
#define EVT_event_queue_is_empty(Q) ((Q)->current_wave->len == 0 && (Q)->next_wave->len == 0)

EVT_event_t *EVT_event_dequeue (EVT_event_queue_t *, RAN_gen_t *);
void EVT_free_event_queue (EVT_event_queue_t *);
char *EVT_event_queue_to_string (EVT_event_queue_t *);
int EVT_fprintf_event_queue (FILE *, EVT_event_queue_t *);

#define EVT_printf_event_queue(Q) EVT_fprintf_event_queue(stdout,Q)

void EVT_free_event_as_GFunc (gpointer data, gpointer user_data);

#endif /* !EVENT_H */
