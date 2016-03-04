/** @file adsm.c
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


#include "adsm.h"
#include <glib.h>

#include "gis.h"
#include "rng.h"

/*-----------------------------------------------------------------------------
 * Required for the Windows DLL version of the ADSM core library
 *
 * Other implementations should ignore this block.
 *---------------------------------------------------------------------------*/
#ifdef DLL_EXPORTS
#include <windows.h>

BOOL APIENTRY
DllMain (HINSTANCE hInst /* Library instance handle. */ ,
         DWORD reason /* Reason this function is being called. */ ,
         LPVOID reserved /* Not used. */ )
{
  switch (reason)
    {
    case DLL_PROCESS_ATTACH:
      /* printf( "@@@ DLL LOADED @@@" ); */
      clear_adsm_fns ();
      clear_rng_fns ();
      break;
    case DLL_PROCESS_DETACH:
      break;
    case DLL_THREAD_ATTACH:
      break;
    case DLL_THREAD_DETACH:
      break;
    }

  /* Returns TRUE on success, FALSE on failure */
  return TRUE;
}

#endif /* DLL_EXPORTS */
/*------------------------------------------------------------------------------*/



/*-----------------------------------------------------------------------------
 * Functions for version tracking
 *---------------------------------------------------------------------------*/
/** Returns the current version of this application. */
DLL_API char *
current_version (void)
{
  int i;
  char* ret_val = NULL;

  /* DON'T FORGET: When updating the string constants below, also change
   * PACKAGE_STRING, PACKAGE_VERSION, and VERSION in config.h. 
   * Also don't forget to update the version number in configure.in */ 
  i = 0;

  if( 0 == i ) {
    ret_val = "3.2.19";
  }
  else if( 1 == i ) {
    /* All is right with the world: do nothing. */
  }
  else {
   /* Someone screwed something up. */
   g_assert( FALSE );
   ret_val = "0.0.0";
  }

  return ret_val;
}


/** Returns the version of the model specification that
    this application or DLL is intended to comply with */
DLL_API char *
specification_version (void)
{
  return "1.2.1";
}
/*---------------------------------------------------------------------------*/



/*-----------------------------------------------------------------------------
 * Functions used to set the function pointers
 *---------------------------------------------------------------------------*/
/* For the display of debugging information in the GUI */
DLL_API void
set_printf (TFnVoid_1_CharP fn)
{
  adsm_printf = fn;
}


DLL_API void
set_debug (TFnVoid_1_CharP fn)
{
  adsm_debug = fn;
}


/* For key simulation- and iteration-level events */
DLL_API void
set_sim_start (TFnVoid_0 fn)
{
  adsm_sim_start = fn;
}


DLL_API void
set_iteration_start (TFnVoid_1_Int fn)
{
  adsm_iteration_start = fn;
}


DLL_API void
set_day_start (TFnVoid_1_Int fn)
{
  adsm_day_start = fn;
}


DLL_API void
set_day_complete (TFnVoid_1_Int fn)
{
  adsm_day_complete = fn;
}


DLL_API void
set_disease_end (TFnVoid_1_Int fn)
{
  adsm_disease_end = fn;
}


DLL_API void
set_outbreak_end (TFnVoid_1_Int fn)
{
  adsm_outbreak_end = fn;
}


DLL_API void
set_iteration_complete (TFnVoid_1_Int fn)
{
  adsm_iteration_complete = fn;
}


DLL_API void
set_sim_complete (TFnVoid_1_Int fn)
{
  adsm_sim_complete = fn;
}


/* Used to update unit status and related events as an iteration runs */
DLL_API void
set_change_unit_state (TFnVoid_1_TUNTUpdate fn)
{
  adsm_change_unit_state = fn;
}


DLL_API void
set_infect_unit (TFnVoid_1_TUNTInfect fn)
{
  adsm_infect_unit = fn;
}


DLL_API void
set_expose_unit (TFnVoid_1_TUNTExpose fn)
{
  adsm_expose_unit = fn;
}


DLL_API void
set_detect_unit (TFnVoid_1_TUNTDetect fn)
{
  adsm_detect_unit = fn;
}


DLL_API void
set_trace_unit (TFnVoid_1_TUNTTrace fn)
{
  adsm_trace_unit = fn;
}


DLL_API void
set_examine_unit (TFnVoid_1_TUNTExam fn)
{
  adsm_examine_unit = fn; 
}


DLL_API void 
set_test_unit (TFnVoid_1_TUNTTest fn)
{
  adsm_test_unit = fn;  
}


DLL_API void 
set_queue_unit_for_destruction (TFnVoid_1_Int fn)
{
  adsm_queue_unit_for_destruction = fn; 
}


DLL_API void
set_destroy_unit (TFnVoid_1_TUNTControl fn)
{
  adsm_destroy_unit = fn;
}


DLL_API void 
set_queue_unit_for_vaccination (TFnVoid_1_Int fn)
{
  adsm_queue_unit_for_vaccination = fn; 
}


DLL_API void
set_vaccinate_unit (TFnVoid_1_TUNTControl fn)
{
  adsm_vaccinate_unit = fn;
}


DLL_API void
set_cancel_unit_vaccination (TFnVoid_1_TUNTControl fn)
{
  adsm_cancel_unit_vaccination = fn;
}


DLL_API void
set_make_zone_focus( TFnVoid_1_Int fn )
{
  adsm_make_zone_focus = fn;
}


DLL_API void
set_record_zone_change (TFnVoid_1_TUNTZone fn )
{
  adsm_record_zone_change = fn;
}


DLL_API void
set_record_zone_area (TFnVoid_2_Int_Double fn)
{
  adsm_record_zone_area = fn;
}


DLL_API void
set_record_zone_perimeter (TFnVoid_2_Int_Double fn)
{
  adsm_record_zone_perimeter = fn;
}


/* Used by the GUI to access zone perimeters during a running simulation */
DLL_API void
set_set_zone_perimeters( TFnVoid_1_TUNTPerimeterList fn)
{
   adsm_set_zone_perimeters = fn;
}


DLL_API unsigned int
get_zone_list_length( ZON_zone_list_t *zones )
{
  if (zones == NULL)
    return 0;
  else
    return ZON_zone_list_length (zones);
}


DLL_API ZON_zone_t *
get_zone_from_list( ZON_zone_list_t * zones, int i)
{
  if (zones == NULL)
    return NULL;
  else
    return ZON_zone_list_get (zones, i);
}


/* Used to write daily unit state output, when desired */
DLL_API void
set_show_all_states (TFnVoid_1_CharP fn)
{
  adsm_show_all_states = fn;
}


/* Used to write daily unit prevalence output, when desired */
DLL_API void
set_show_all_prevalences (TFnVoid_1_CharP fn)
{
  adsm_show_all_prevalences = fn;
}


/* Used to write daily unit zone output, when desired */
/* This function will need to be re-implemented if it is ever needed again. */
/*
DLL_API void
set_show_all_zones (TFnVoid_1_CharP fn)
{
  adsm_show_all_zones = fn;
}
*/

/* Used to determine whether the user wants to interrupt a running simulation */
DLL_API void
set_simulation_stop (TFnInt_0 fn)
{
  adsm_simulation_stop = fn;
}


DLL_API void
set_display_g_message (TFnVoid_1_CharP fn)
{
  adsm_display_g_message = fn;  
}


DLL_API void
set_report_search_hits (TFnVoid_5_Int_Int_Int_Int_Int fn)
{
  adsm_report_search_hits = fn;
}
/*---------------------------------------------------------------------------*/



/*-----------------------------------------------------------------------------
 * Function pointer helpers
 *---------------------------------------------------------------------------*/
void
clear_adsm_fns (void)
{
  set_printf (NULL);
  set_debug (NULL);

  set_sim_start (NULL);
  set_iteration_start (NULL);
  set_day_start (NULL);
  set_day_complete (NULL);
  set_iteration_complete (NULL);
  set_disease_end (NULL);
  set_outbreak_end (NULL);
  set_sim_complete (NULL);

  set_change_unit_state (NULL);
  set_infect_unit (NULL);
  set_expose_unit (NULL);
  set_detect_unit (NULL);
  set_trace_unit (NULL);
  set_examine_unit (NULL);
  set_test_unit (NULL);
  set_queue_unit_for_destruction (NULL);
  set_destroy_unit (NULL);
  set_queue_unit_for_vaccination (NULL);
  set_vaccinate_unit (NULL);
  set_cancel_unit_vaccination (NULL);
  set_make_zone_focus (NULL);
  set_record_zone_change (NULL);
  set_record_zone_area (NULL);
  set_record_zone_perimeter (NULL);

  set_set_zone_perimeters( NULL );

  set_show_all_states (NULL);
  set_show_all_prevalences (NULL);
  /* set_show_all_zones (NULL); */

  set_simulation_stop (NULL);
  set_display_g_message (NULL);

  set_report_search_hits (NULL);
}

void
adsm_log_handler(const gchar *log_domain, GLogLevelFlags log_level, const gchar *message, gpointer user_data)
{
  if( NULL != adsm_display_g_message )
    adsm_display_g_message( (gchar*) message ); 
}
/*---------------------------------------------------------------------------*/



/*-----------------------------------------------------------------------------
 * Fully spelled out and abbreviated names for enums.
 *---------------------------------------------------------------------------*/
const char *ADSM_trace_direction_name[] = {
  "Trace Neither", "Trace Forward or Out", "Trace Back or In", NULL
};

const char *ADSM_trace_direction_abbrev[] = {
  "Neither", "Fwd", "Back", NULL
};

const char *ADSM_contact_type_name[] = {
  "Unknown", "Direct Contact", "Indirect Contact", "Airborne Spread",
  "Initially Infected", NULL
};

const char *ADSM_contact_type_abbrev[] = {
  "Unkn", "Dir", "Ind", "Air", "Ini", NULL
};

const char *ADSM_detection_reason_abbrev[] = {
  "Unkn", "Clin", "Test", NULL
};

const char *ADSM_control_reason_name[] = {
  "Unspecified", "Ring", "Trace fwd direct", "Trace fwd indirect",
  "Trace back direct", "Trace back indirect", "Basic", "Initial state",
  "Suppressive Ring", "Protective Ring",
  NULL
};

const char *ADSM_control_reason_abbrev[] = {
  "Unsp", "Ring", "DirFwd", "IndFwd", "DirBack", "IndBack", "Det", "Ini",
  "SuppRing", "ProtRing", NULL
};

/*---------------------------------------------------------------------------*/
