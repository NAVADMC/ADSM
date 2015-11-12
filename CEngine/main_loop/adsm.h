/** @file adsm.h
 *
 * @author Aaron Reeves <Aaron.Reeves@colostate.edu><br>
 *   Animal Population Health Institute<br>
 *   College of Veterinary Medicine and Biomedical Sciences<br>
 *   Colorado State University<br>
 *   Fort Collins, CO 80523<br>
 *   USA
 * @version 0.1
 * @date June 2005
 *
 * Copyright &copy; 2005 - 2009 Animal Population Health Institute,
 * Colorado State University
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#ifndef ADSM_H
#define ADSM_H

#if defined(DLL_EXPORTS)
# define DLL_API __declspec( dllexport )
#elif defined(DLL_IMPORTS)
# define DLL_API __declspec( dllimport )
#else
# define DLL_API
#endif

#include <glib.h>
#include <sqlite3.h>

#include "unit.h"
#include "zone.h"


/*  Defines for premature stopping of the simulation  */
#define STOP_NORMAL              ((guint) 0x0000 )
#define STOP_ON_DISEASE_END      ((guint) 0x0001 )
#define STOP_ON_FIRST_DETECTION  ((guint) 0x0002 )

#define get_stop_on_disease_end( x )     ((guint)( ((guint)x) & STOP_ON_DISEASE_END ))
#define get_stop_on_first_detection( x ) ((guint)( ((guint)x) & STOP_ON_FIRST_DETECTION ))


/* Enums used by the library to interact with calling applications.   */
/* ------------------------------------------------------------------ */
/* Used to indicate success of failure of exposures, traces, and detection by exams */
typedef enum {
  ADSM_SuccessUnspecified,
  ADSM_SuccessTrue,
  ADSM_SuccessFalse
} ADSM_success;

/* Used to indicate trace direction  */
typedef enum {
  ADSM_TraceNeither,
  ADSM_TraceForwardOrOut,
  ADSM_TraceBackOrIn,
  ADSM_NTRACE_DIRECTIONS
} ADSM_trace_direction;
extern const char *ADSM_trace_direction_name[];
extern const char *ADSM_trace_direction_abbrev[];

/* Used to indicate type of exposure, contact, or infection  */
typedef enum {
  ADSM_UnspecifiedInfectionType,
  ADSM_DirectContact,
  ADSM_IndirectContact,
  ADSM_AirborneSpread,
  ADSM_InitiallyInfected
} ADSM_contact_type;
#define ADSM_NCONTACT_TYPES 5
extern const char *ADSM_contact_type_name[];
extern const char *ADSM_contact_type_abbrev[];

/* Used to indicate diagnostic test results  */
typedef enum {
  ADSM_TestUnspecified,
  ADSM_TestTruePositive,
  ADSM_TestTrueNegative,
  ADSM_TestFalsePositive,
  ADSM_TestFalseNegative
} ADSM_test_result;

/* Used to indicate reasons for detection  */
typedef enum {
  ADSM_DetectionReasonUnspecified,
  ADSM_DetectionClinicalSigns,
  ADSM_DetectionDiagnosticTest,
  ADSM_NDETECTION_REASONS
} ADSM_detection_reason;
extern const char *ADSM_detection_reason_abbrev[];


/* Used to indicate reasons for control activities  */
typedef enum {
  ADSM_ControlReasonUnspecified,
  ADSM_ControlRing,
  ADSM_ControlTraceForwardDirect,
  ADSM_ControlTraceForwardIndirect,
  ADSM_ControlTraceBackDirect,
  ADSM_ControlTraceBackIndirect,
  ADSM_ControlDetection,
  ADSM_ControlInitialState,
  ADSM_ControlSuppressiveRing,
  ADSM_ControlProtectiveRing,
  ADSM_NCONTROL_REASONS
} ADSM_control_reason;
extern const char *ADSM_control_reason_name[];
extern const char *ADSM_control_reason_abbrev[];

/* Used when a unit's actual disease state changes */
/* FIXME: Consider combining with the appropriate enum type used internally */
typedef enum {
  ADSM_StateSusceptible,
  ADSM_StateLatent,
  ADSM_StateInfectiousSubclinical,
  ADSM_StateInfectiousClinical,
  ADSM_StateNaturallyImmune,
  ADSM_StateVaccineImmune,
  ADSM_StateDestroyed,
  ADSM_StateUnspecified
} ADSM_disease_state;

/* =================================================================================== */
/* FIXME: Consider combining these structs with the similar structs defined in event.h */
/* =================================================================================== */
/** Struct used by callers of the ADSM library when a unit's actual disease state has changed */
typedef struct
{
  unsigned int unit_index;  /* Index into the unit list of the unit that's changed */
  ADSM_disease_state state;
  #ifdef USE_SC_GUILIB
    char *msg;
    int success;
  #endif
}
UNT_update_t;


/** Struct used by callers of the ADSM library when a unit is infected */
typedef struct
{
  unsigned int unit_index;
  ADSM_contact_type infection_source_type;
}
UNT_infect_t;


/** Struct used by callers of the ADSM library when a detection occurs. */
typedef struct
{
  unsigned int unit_index;
  ADSM_detection_reason reason;
  ADSM_test_result test_result;
}
UNT_detect_t;


/** Struct used by callers of the ADSM library when a unit is destroyed or vaccinated. */
typedef struct
{
  unsigned int unit_index;
  ADSM_control_reason reason;
  int day_commitment_made;
}
UNT_control_t;

  
/** Struct used by callers of the ADSM library when an exposure
 * has occurred.  If an "attempt to infect" event is generated, 
 * the attempt is considered successful.
 *
 * Note that exposures may preceed infection by some period
 * of time.
*/
typedef struct
{
  unsigned int src_index;
  ADSM_disease_state src_state;
  unsigned int dest_index;
  ADSM_disease_state dest_state;
  int initiated_day;
  int finalized_day;
  ADSM_success is_adequate;
  ADSM_contact_type exposure_method;
}
UNT_expose_t;


/** Struct used by callers of the ADSM library when a unit is traced. */
typedef struct
{
  unsigned int identified_index;
  ADSM_disease_state identified_state;
  unsigned int origin_index;
  ADSM_disease_state origin_state;
  int day;
  int initiated_day;
  ADSM_success success;
  ADSM_trace_direction trace_type;
  ADSM_contact_type contact_type;
}
UNT_trace_t;


/** Struct used by callers of the ADSM library when a unit is examined after tracing. */
typedef struct
{
  int unit_index;
  ADSM_trace_direction trace_type;
  ADSM_contact_type contact_type;
  ADSM_success disease_detected;
}
UNT_exam_t;


/** Struct used by callers of the ADSM library when a unit is diagnostically tested after tracing. */
typedef struct
{
  int unit_index;
  ADSM_test_result test_result;
  ADSM_trace_direction trace_type;
  ADSM_contact_type contact_type;
}
UNT_test_t;          
       
          
/** Notification for the GUI that a unit's zone designation has changed. */
typedef struct
{
  unsigned int unit_index;
  unsigned int zone_level;  
}
UNT_zone_t;


/* Function to start the simulation */
DLL_API void
run_sim_main (sqlite3 *scenario_db,
              const char *output_dir,
              double fixed_rng_value, int verbosity, int seed,
              int starting_iteration_number,
              gboolean dry_run,
              GError **);


/* Functions for version tracking */
/* ------------------------------ */
/** Returns the current version of this application. */
DLL_API char *current_version (void);

/** Returns the version of the model specification that
this application or DLL is intended to comply with */
DLL_API char *specification_version (void);


/* Function pointer types */
/*------------------------*/
typedef void (*TFnVoid_1_CharP) (char *);
typedef void (*TFnVoid_1_Int) (int);
typedef void (*TFnVoid_1_TUNTUpdate) (UNT_update_t);
typedef void (*TFnVoid_1_TUNTInfect) (UNT_infect_t);
typedef void (*TFnVoid_1_TUNTDetect) (UNT_detect_t);
typedef void (*TFnVoid_1_TUNTControl) (UNT_control_t);
typedef void (*TFnVoid_1_TUNTExpose) (UNT_expose_t);
typedef void (*TFnVoid_1_TUNTTrace) (UNT_trace_t);
typedef void (*TFnVoid_1_TUNTExam) (UNT_exam_t);
typedef void (*TFnVoid_1_TUNTTest) (UNT_test_t);
typedef void (*TFnVoid_1_TUNTZone) (UNT_zone_t);
typedef void (*TFnVoid_0) (void);
typedef int (*TFnInt_0) (void);
typedef void (*TFnVoid_1_TUNTPerimeterList) (ZON_zone_list_t *);
typedef void (*TFnVoid_2_Int_Double) (int, double);
typedef void (*TFnVoid_5_Int_Int_Int_Int_Int) (int, int, int, int, int);

/* Function pointers */
/*-------------------*/
/* For the display of debugging information in the GUI */
TFnVoid_1_CharP adsm_printf;
TFnVoid_1_CharP adsm_debug;

/* For key simulation- and iteration-level events */
TFnVoid_0 adsm_sim_start;
TFnVoid_1_Int adsm_iteration_start;
TFnVoid_1_Int adsm_day_start;
TFnVoid_1_Int adsm_day_complete;
TFnVoid_1_Int adsm_disease_end;
TFnVoid_1_Int adsm_outbreak_end;
TFnVoid_1_Int adsm_iteration_complete;
TFnVoid_1_Int adsm_sim_complete;

/* Used to determine whether the user wants to interrupt a running simulation */
TFnInt_0 adsm_simulation_stop;

/* Used to update unit state and related events as an iteration runs */
TFnVoid_1_TUNTUpdate adsm_change_unit_state;
TFnVoid_1_TUNTInfect adsm_infect_unit;
TFnVoid_1_TUNTDetect adsm_detect_unit;
TFnVoid_1_TUNTExpose adsm_expose_unit;
TFnVoid_1_TUNTTrace adsm_trace_unit;
TFnVoid_1_TUNTExam adsm_examine_unit;
TFnVoid_1_TUNTTest adsm_test_unit;
TFnVoid_1_Int adsm_queue_unit_for_destruction;
TFnVoid_1_TUNTControl adsm_destroy_unit;
TFnVoid_1_Int adsm_queue_unit_for_vaccination;
TFnVoid_1_TUNTControl adsm_vaccinate_unit;
TFnVoid_1_TUNTControl adsm_cancel_unit_vaccination;
TFnVoid_1_Int adsm_make_zone_focus;
TFnVoid_1_TUNTZone adsm_record_zone_change;
TFnVoid_2_Int_Double adsm_record_zone_area;
TFnVoid_2_Int_Double adsm_record_zone_perimeter;

/* Used by the GUI to access zone information during a running simulation */
TFnVoid_1_TUNTPerimeterList adsm_set_zone_perimeters;

/* Used to write daily unit state output, when desired */
TFnVoid_1_CharP adsm_show_all_states;

/* Used to write daily unit prevalence output, when desired */
TFnVoid_1_CharP adsm_show_all_prevalences;

/* Used to display g_warnings, etc., in the GUI */
TFnVoid_1_CharP adsm_display_g_message;

/* Used to write daily unit zone output, when desired */
/* This function will need to be re-implemented if it is ever needed again. */
/* TFnVoid_1_CharP adsm_show_all_zones; */

TFnVoid_5_Int_Int_Int_Int_Int adsm_report_search_hits;


/* Functions used to set the function pointers */
/*---------------------------------------------*/
DLL_API void set_printf (TFnVoid_1_CharP fn);
DLL_API void set_debug (TFnVoid_1_CharP fn);

DLL_API void set_sim_start (TFnVoid_0 fn);
DLL_API void set_iteration_start (TFnVoid_1_Int fn);
DLL_API void set_day_start (TFnVoid_1_Int fn);
DLL_API void set_day_complete (TFnVoid_1_Int fn);
DLL_API void set_disease_end (TFnVoid_1_Int fn);
DLL_API void set_outbreak_end (TFnVoid_1_Int fn);
DLL_API void set_iteration_complete (TFnVoid_1_Int fn);
DLL_API void set_sim_complete (TFnVoid_1_Int fn);

DLL_API void set_change_unit_state (TFnVoid_1_TUNTUpdate fn);
DLL_API void set_infect_unit (TFnVoid_1_TUNTInfect fn);
DLL_API void set_expose_unit (TFnVoid_1_TUNTExpose fn);
DLL_API void set_detect_unit (TFnVoid_1_TUNTDetect fn);
DLL_API void set_trace_unit (TFnVoid_1_TUNTTrace fn);
DLL_API void set_examine_unit (TFnVoid_1_TUNTExam fn);
DLL_API void set_test_unit (TFnVoid_1_TUNTTest fn);
DLL_API void set_queue_unit_for_destruction (TFnVoid_1_Int fn);
DLL_API void set_destroy_unit (TFnVoid_1_TUNTControl fn);
DLL_API void set_queue_unit_for_vaccination (TFnVoid_1_Int fn);
DLL_API void set_vaccinate_unit (TFnVoid_1_TUNTControl fn);
DLL_API void set_cancel_unit_vaccination (TFnVoid_1_TUNTControl fn);
DLL_API void set_make_zone_focus( TFnVoid_1_Int fn );
DLL_API void set_record_zone_change (TFnVoid_1_TUNTZone fn);
DLL_API void set_record_zone_area (TFnVoid_2_Int_Double fn);
DLL_API void set_record_zone_perimeter (TFnVoid_2_Int_Double fn);

DLL_API void set_set_zone_perimeters( TFnVoid_1_TUNTPerimeterList fn);
DLL_API unsigned int get_zone_list_length( ZON_zone_list_t *zones );
DLL_API ZON_zone_t *get_zone_from_list( ZON_zone_list_t * zones, int i);

DLL_API void set_show_all_states (TFnVoid_1_CharP fn);
DLL_API void set_show_all_prevalences (TFnVoid_1_CharP fn);

/* This function will need to be re-implemented if it is ever needed again. */
/* DLL_API void set_show_all_zones (TFnVoid_1_CharP fn); */

DLL_API void set_display_g_message (TFnVoid_1_CharP fn);

DLL_API void set_simulation_stop (TFnInt_0 fn);

DLL_API void set_report_search_hits (TFnVoid_5_Int_Int_Int_Int_Int fn);


/* Function pointer helpers */
/*--------------------------*/
void clear_adsm_fns (void);
void adsm_log_handler(const gchar *log_domain, GLogLevelFlags log_level, const gchar *message, gpointer user_data);

#endif /* ADSM_H */
