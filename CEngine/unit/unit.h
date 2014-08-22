/** @file unit.h
 * State information about a unit (herd, flock, etc.) of animals.
 *
 * A unit contains one production type and has a size, location (x and y),
 * state, and prevalence.  Modules may read these data fields, but they
 * should modify a unit only through the functions UNT_infect(),
 * UNT_vaccinate(), UNT_destroy(), and UNT_quarantine().
 * The first three functions correspond to the action labels on the
 * <a href="unit_8h.html#a42">unit state-transition diagram</a>.
 *
 * Because the events in one simulation day should be considered to happen
 * simultaneously, and because different sub-models may try to make conflicting
 * changes to a unit, the functions named above do not change a unit
 * immediately.  Instead, the request for a change is stored, and conflicts
 * between the change requests are resolved before any changes are applied.
 * See UNT_step() for details.
 *
 * Symbols from this module begin with UNT_.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 *
 * Copyright &copy; University of Guelph, 2003-2010
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#ifndef UNIT_H
#define UNIT_H

#if HAVE_CONFIG_H
#  include <config.h>
#endif

#include <stdio.h>

#if STDC_HEADERS
#  include <stdlib.h>
#endif

#include "rel_chart.h"
#include "spatial_search.h"
#include <glib.h>
#include <proj_api.h>
#include <sqlite3.h>

#ifdef USE_SC_GUILIB
#  include <production_type_data.h>
#  include <zone.h>
#endif


/**
 * Production types.
 */
typedef unsigned int UNT_production_type_t;



/**
 * Number of possible states (with respect to a disease) for a unit.
 *
 * @sa UNT_state_t
 */
#define UNT_NSTATES 7

/**
 * Possible states (with respect to a disease) for a unit.  The diagram below
 * is based on one from Mark Schoenbaum's presentation to the North American
 * Animal Health Committee's (NAAHC) Emergency Management Working Group at the
 * Disease Spread Modeling Workshop, Fort Collins, CO July 9-11, 2002.  The
 * single Infectious state has been split into two.
 *
 * @image html state-transition.png
 *
 * @sa UNT_valid_transition
 */
typedef enum
{
  Susceptible, Latent, InfectiousSubclinical, InfectiousClinical,
  NaturallyImmune, VaccineImmune, Destroyed
}
UNT_state_t;
extern const char *UNT_state_name[];
extern const char UNT_state_letter[];


typedef enum
{
  asUnspecified, asUnknown, asDetected, asTraceDirect, asTraceIndirect, asVaccinated, asDestroyed
}
UNT_apparent_status_t;


/**
 * Number of actions/changes that can be made to a unit.
 *
 * @sa UNT_change_request_type_t
 */
#define UNT_NCHANGE_REQUEST_TYPES 2

/**
 * Actions/changes that can be made to a unit.
 */
typedef enum
{
  Infect, Vaccinate
}
UNT_change_request_type_t;

/** A request to infect a unit. */
typedef struct
{
  int latent_period;
  int infectious_subclinical_period;
  int infectious_clinical_period;
  int immunity_period;
  unsigned int day_in_disease_cycle;
}
UNT_infect_change_request_t;



/** A request to vaccinate a unit. */
typedef struct
{
  int delay;
  int immunity_period;
}
UNT_vaccinate_change_request_t;



/** A supertype for all change requests. */
typedef struct
{
  UNT_change_request_type_t type;
  union
  {
    UNT_infect_change_request_t infect;
    UNT_vaccinate_change_request_t vaccinate;
  }
  u;
}
UNT_change_request_t;



/** Type of a unit's identifier. */
typedef char *UNT_id_t;


/** Complete state information for a unit. */
typedef struct
{
  unsigned int index;           /**< position in a unit list */
  UNT_production_type_t production_type;  
  gchar *production_type_name;  /**< in UTF-8 */
  UNT_id_t official_id;         /**< arbitrary identifier string */
  unsigned int size;            /**< number of animals */
  double latitude, longitude;
  double x;                     /**< x-coordinate on a km grid */
  double y;                     /**< y-coordinate on a km grid */
  UNT_state_t state;
  UNT_state_t initial_state;
  int days_in_initial_state;
  int days_left_in_initial_state;
  double prevalence;

  /* Remaining fields should be considered private. */

  gboolean quarantined;
  int days_in_state;

  gboolean in_vaccine_cycle;
  int immunity_start_countdown;
  int immunity_end_countdown;

  gboolean in_disease_cycle;
  int day_in_disease_cycle;
  int infectious_start_countdown;
  int clinical_start_countdown;   
  
  REL_chart_t *prevalence_curve;

  GSList *change_requests;
  gboolean destroy_change_request;
  gboolean quarantine_change_request;
  
#ifdef USE_SC_GUILIB  
  /*  This field is used on the SC version if the user wants to 
      write out the iteration summaries, as would be found in the Windows
      software.  This hooks into some of the "adsm_*" functions in order to set this
      data.  This allows for easy import of SC data into the PC database.
  */
  GPtrArray *production_types;  /**< Each item is a UNT_production_type_data_t structure */
  gboolean ever_infected;
  int day_first_infected;
  ZON_zone_t *zone;
  guint cum_infected, cum_detected, cum_destroyed, cum_vaccinated;
  UNT_apparent_status_t apparent_status;  
  guint apparent_status_day;
#endif    
}
UNT_unit_t;



/** A list of units. */
typedef struct
{
  GArray *list; /**< Each item is a UNT_unit_t structure. */
  GPtrArray *production_type_names; /**< Each item is a (gchar *) pointer and is in UTF-8. */
  
#ifdef USE_SC_GUILIB  
  /*  This field is used on the SC version if the user wants to 
      write out the iteration summaries, as would be found in the Windows
      software.  This hooks into some of the "adsm_*" functions in order to set this
      data.  This allows for easy import of SC data into the PC database.
  */
  GPtrArray *production_types;  /**< Each item is a UNT_production_type_data_t structure */
#endif   

  spatial_search_t *spatial_index;

  projPJ projection; /**< The projection used to convert between the latitude,
    longitude and x,y locations of the units.  Note that the projection object
    works in meters, while the x,y locations are stored in kilometers. */
}
UNT_unit_list_t;



/* Prototypes. */

UNT_unit_list_t *UNT_new_unit_list (void);

#ifdef USE_SC_GUILIB 
  UNT_unit_list_t *UNT_load_unit_list ( sqlite3 *, GPtrArray *production_types );
#else
  UNT_unit_list_t *UNT_load_unit_list (sqlite3 *);
#endif


void UNT_free_unit_list (UNT_unit_list_t *);
unsigned int UNT_unit_list_append (UNT_unit_list_t *, UNT_unit_t *);

/**
 * Returns the number of units in a unit list.
 *
 * @param U a unit list.
 * @return the number of units in the list.
 */
#define UNT_unit_list_length(U) (U->list->len)

/**
 * Returns the ith unit in a unit list.
 *
 * @param U a unit list.
 * @param I the index of the unit to retrieve.
 * @return the ith unit.
 */
#define UNT_unit_list_get(U,I) (&g_array_index(U->list,UNT_unit_t,I))

unsigned int UNT_unit_list_get_by_state (UNT_unit_list_t *, UNT_state_t, UNT_unit_t ***);
unsigned int UNT_unit_list_get_by_initial_state (UNT_unit_list_t *, UNT_state_t, UNT_unit_t ***);
void UNT_unit_list_project (UNT_unit_list_t *, projPJ);
void UNT_unit_list_build_spatial_index (UNT_unit_list_t *);
char *UNT_unit_list_to_string (UNT_unit_list_t *);
int UNT_printf_unit_list (UNT_unit_list_t *);
int UNT_fprintf_unit_list (FILE *, UNT_unit_list_t *);
char *UNT_unit_list_summary_to_string (UNT_unit_list_t *);
char *UNT_unit_list_prevalence_to_string (UNT_unit_list_t *, unsigned int day);

UNT_unit_t *UNT_new_unit (UNT_production_type_t, gchar *production_type_name,
                          unsigned int size, double x, double y);
void UNT_free_unit (UNT_unit_t *, gboolean free_segment);
char *UNT_unit_to_string (UNT_unit_t *);
int UNT_fprintf_unit (FILE *, UNT_unit_t *);

#define UNT_printf_unit(H) UNT_fprintf_unit(stdout,H)

void UNT_reset (UNT_unit_t *);
UNT_state_t UNT_step (UNT_unit_t *, GHashTable *infectious_units);
void UNT_infect (UNT_unit_t *, int latent_period,
                 int infectious_subclinical_period,
                 int infectious_clinical_period,
                 int immunity_period,
                 unsigned int day_in_disease_cycle);
void UNT_vaccinate (UNT_unit_t *, int delay, int immunity_period);
void UNT_quarantine (UNT_unit_t *);
void UNT_lift_quarantine (UNT_unit_t *);
void UNT_destroy (UNT_unit_t *);

void UNT_remove_unit_from_infectious_list( UNT_unit_t *, GHashTable * ); 
void UNT_add_unit_to_infectious_list( UNT_unit_t *, GHashTable * );   

#endif /* !UNIT_H */
