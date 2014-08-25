/** @file unit.c
 * Functions for creating, destroying, printing, and manipulating units.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 *
  * @author Shaun Case <ShaunCase@colostate.edu><br>
 *   Animal Population Health Institute<br>
 *   College of Veterinary Medicine and Biomedical Sciences<br>
 *   Colorado State University<br>
 *   Fort Collins, CO 80523<br>
 *   USA
 *
 * Copyright &copy; University of Guelph, 2003-2010
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 *
 * @todo Take SCEW out of the Makefile.
 */


#if HAVE_CONFIG_H
#  include <config.h>
#endif

/* To avoid name clashes when dlpreopening multiple modules that have the same
 * global symbols (interface).  See sec. 18.4 of "GNU Autoconf, Automake, and
 * Libtool". */
#define free_as_GFunc unit_LTX_free_as_GFunc

#define G_LOG_DOMAIN "unit"

#include <unistd.h>
#include <stdio.h>
#include "unit.h"
#include "sqlite3_exec_dict.h"

#if STDC_HEADERS
#  include <stdlib.h>
#  include <string.h>
#endif

#if HAVE_STRINGS_H
#  include <strings.h>
#endif

#if HAVE_CTYPE_H
#  include <ctype.h>
#endif

#if HAVE_MATH_H
#  include <math.h>
#endif

/* Temporary fix -- missing from math header file? */
double trunc (double);

#if HAVE_ERRNO_H
#  include <errno.h>
#endif

#define EPSILON 0.001

#include "adsm.h"

#ifdef USE_SC_GUILIB
#  include <sc_guilib_outputs.h>
#endif



/**
 * A table of all valid state transitions.
 *
 * @sa UNT_state_t
 */
  const gboolean UNT_valid_transition[][UNT_NSTATES] = {
    {FALSE, TRUE, TRUE, TRUE, FALSE, TRUE, TRUE}, /* Susceptible -> Latent, InfectiousSubclinical, InfectiousClinical, VaccineImmune or Destroyed */
    {FALSE, FALSE, TRUE, TRUE, FALSE, FALSE, TRUE},       /* Latent -> InfectiousSubclinical, InfectiousClinical or Destroyed */
    {FALSE, FALSE, FALSE, TRUE, FALSE, FALSE, TRUE},      /* InfectiousSubclinical -> InfectiousClinical or Destroyed */
    {FALSE, FALSE, FALSE, FALSE, TRUE, FALSE, TRUE},      /* InfectiousClinical -> NaturallyImmune or Destroyed */
    {TRUE, FALSE, FALSE, FALSE, FALSE, FALSE, TRUE},      /* NaturallyImmune -> Susceptible or Destroyed */
    {TRUE, FALSE, FALSE, FALSE, FALSE, FALSE, TRUE},      /* VaccineImmune -> Susceptible or Destroyed */
    {FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE},    /* Destroyed -> <<emptyset>> */
  };

/**
 * Names for the possible states (with respect to a disease) for a unit,
 * terminated with a NULL sentinel.
 *
 * @sa UNT_state_t
 */
const char *UNT_state_name[] = {
  "Susc", "Lat", "Subc", "Clin", "NImm", "VImm", "Dest", NULL
};

/**
 * Single-letter codes for the possible states (with respect to a disease) for
 * a unit, terminated with a NULL sentinel.
 *
 * @sa UNT_state_t
 */
const char UNT_state_letter[] = {
  'S', 'L', 'B', 'C', 'N', 'V', 'D', '\0'
};



/**
 * Names for the fields in a unit structure, terminated with a NULL sentinel.
 *
 * @sa UNT_unit_t
 */
const char *UNT_unit_field_name[] = {
  "ProductionType", "UnitSize", "Lat", "Lon", "state", NULL
};



/**
 * Wraps free so that it can be used in GLib calls.
 *
 * @param data a pointer to anything, cast to a gpointer.
 * @param user_data not used, pass NULL.
 */
void
free_as_GFunc (gpointer data, gpointer user_data)
{
  free (data);
}



/**
 * Changes the state of a unit.  This function checks if the transition is
 * valid.
 *
 * @param unit a unit.
 * @param new_state the new state.
 * @param infectious_units a list of infectious units, which may change as a
 *   result of this operation.
 */
void
UNT_change_state (UNT_unit_t * unit, UNT_state_t new_state,
                  GHashTable *infectious_units)
{
  UNT_state_t state;

  state = unit->state;
  if (UNT_valid_transition[state][new_state])
    {
      unit->state = new_state;
      unit->days_in_state = 0;

      switch( new_state )
      {
        case Susceptible:
          UNT_remove_unit_from_infectious_list( unit, infectious_units );
        break;

        case Latent:
        case InfectiousSubclinical:
        case InfectiousClinical:
          UNT_add_unit_to_infectious_list( unit, infectious_units );
        break;

        case NaturallyImmune:
        case VaccineImmune:
          UNT_remove_unit_from_infectious_list( unit, infectious_units );
        break;

        case Destroyed:
          /*  UNT_remove_unit_from_suscpetible_rtree( unit );  */
          UNT_remove_unit_from_infectious_list( unit, infectious_units );
        break;
      };

#if DEBUG
      g_debug ("unit \"%s\" is now %s", unit->official_id,
               UNT_state_name[unit->state]);
#endif
    }
  else
    {
      ;
#if DEBUG
      g_debug ("%s->%s transition for unit \"%s\" was not possible",
               UNT_state_name[state], UNT_state_name[new_state], unit->official_id);
#endif
    }
}



/**
 * Creates a new infection change request.
 *
 * @param latent_period the number of days to spend latent.
 * @param infectious_subclinical_period the number of days to spend infectious
 *   without visible signs.
 * @param infectious_clinical_period the number of days to spend infectious
 *   with visible signs.
 * @param immunity_period how many days the unit's natural immunity lasts
 *   after recovery.
* @param day_in_disease_cycle how many days into the disease cycle the unit
 *   should start.  Normally 0, but sometimes used to create an initially
 *   infected unit that has already been diseased for a while when the
 *   simulation begins.
  * @return a pointer to a newly-created UNT_change_request_t structure.
 */
UNT_change_request_t *
UNT_new_infect_change_request (int latent_period,
                               int infectious_subclinical_period,
                               int infectious_clinical_period,
                               int immunity_period,
                               unsigned int day_in_disease_cycle)
{
  UNT_change_request_t *request;

  request = g_new (UNT_change_request_t, 1);
  request->type = Infect;
  request->u.infect.latent_period = latent_period;
  request->u.infect.infectious_subclinical_period = infectious_subclinical_period;
  request->u.infect.infectious_clinical_period = infectious_clinical_period;
  request->u.infect.immunity_period = immunity_period;
  request->u.infect.day_in_disease_cycle = day_in_disease_cycle;
  return request;
}



/**
 * Carries out an infection change request.
 *
 * @param unit a unit.
 * @param request an infection change request.
 * @param infectious_units a list of infectious units, which may change as a
 *   result of this operation.
 */
void
UNT_apply_infect_change_request (UNT_unit_t * unit,
                                 UNT_infect_change_request_t * request,
                                 GHashTable * infectious_units)
{
  int infectious_start_day, clinical_start_day,
    immunity_start_day, immunity_end_day;

#if DEBUG
  g_debug ("----- ENTER UNT_apply_infect_change_request");
#endif

  if (unit->state != Susceptible)
    goto end;

  /* If the unit has been vaccinated but has not yet developed immunity, cancel
   * the progress of the vaccine. */
  unit->in_vaccine_cycle = FALSE;

  unit->in_disease_cycle = TRUE;
  unit->day_in_disease_cycle = request->day_in_disease_cycle;

#if DEBUG
  g_debug ("requested disease progression = day %u in (%i,%i,%i,%i)",
           request->day_in_disease_cycle,
           request->latent_period, request->infectious_subclinical_period,
           request->infectious_clinical_period, request->immunity_period);
#endif

  /* Compute the day for each state transition. */
  infectious_start_day = request->latent_period;
  clinical_start_day = infectious_start_day + request->infectious_subclinical_period;
  immunity_start_day = clinical_start_day + request->infectious_clinical_period;
  immunity_end_day = immunity_start_day + request->immunity_period;

  /* Advance the countdowns if the day_in_disease_cycle has been set. */
  if (request->day_in_disease_cycle >= immunity_end_day)
    {
      unit->in_disease_cycle = FALSE;
    }
  else if (request->day_in_disease_cycle >= immunity_start_day)
    {
      UNT_change_state (unit, Latent, infectious_units);
      UNT_change_state (unit, InfectiousClinical, infectious_units);
      UNT_change_state (unit, NaturallyImmune, infectious_units);
      unit->days_in_state = request->day_in_disease_cycle - immunity_start_day;
      unit->infectious_start_countdown = -1;
      unit->clinical_start_countdown = -1;
      unit->immunity_start_countdown = -1;
      unit->immunity_end_countdown = immunity_end_day - request->day_in_disease_cycle;
    }
  else if (request->day_in_disease_cycle >= clinical_start_day)
    {
      UNT_change_state (unit, Latent, infectious_units);
      UNT_change_state (unit, InfectiousClinical, infectious_units);
      unit->days_in_state = request->day_in_disease_cycle - clinical_start_day;
      unit->infectious_start_countdown = -1;
      unit->clinical_start_countdown = -1;
      unit->immunity_start_countdown = immunity_start_day - request->day_in_disease_cycle;
      unit->immunity_end_countdown = immunity_end_day - request->day_in_disease_cycle;
    }
  else if (request->day_in_disease_cycle >= infectious_start_day)
    {
      UNT_change_state (unit, Latent, infectious_units);
      UNT_change_state (unit, InfectiousSubclinical, infectious_units);
      unit->days_in_state = request->day_in_disease_cycle - infectious_start_day;
      unit->infectious_start_countdown = -1;
      unit->clinical_start_countdown = clinical_start_day - request->day_in_disease_cycle;
      unit->immunity_start_countdown = immunity_start_day - request->day_in_disease_cycle;
      unit->immunity_end_countdown = immunity_end_day - request->day_in_disease_cycle;
    }
  else
    {
      UNT_change_state (unit, Latent, infectious_units);
      unit->days_in_state = request->day_in_disease_cycle;
      unit->infectious_start_countdown = infectious_start_day - request->day_in_disease_cycle;
      unit->clinical_start_countdown = clinical_start_day - request->day_in_disease_cycle;
      unit->immunity_start_countdown = immunity_start_day - request->day_in_disease_cycle;
      unit->immunity_end_countdown = immunity_end_day - request->day_in_disease_cycle;
    }

#if DEBUG
  g_debug ("infectious start countdown=%i", unit->infectious_start_countdown);
  g_debug ("clinical start countdown=%i", unit->clinical_start_countdown);
  g_debug ("immunity start countdown=%i", unit->immunity_start_countdown);
  g_debug ("immunity end countdown=%i", unit->immunity_end_countdown);
  g_debug ("in disease cycle=%s", unit->in_disease_cycle ? "true" : "false");
  g_debug ("day in disease cycle=%u", unit->day_in_disease_cycle);
#endif

end:
#if DEBUG
  g_debug ("----- EXIT UNT_apply_infect_change_request");
#endif
  return;
}



/**
 * Creates a new vaccination change request.
 *
 * @param delay the number of days before the immunity begins.
 * @param immunity_period the number of days the immunity lasts.
 * @return a pointer to a newly-created UNT_change_request_t structure.
 */
UNT_change_request_t *
UNT_new_vaccinate_change_request (int delay, int immunity_period)
{
  UNT_change_request_t *request;

  request = g_new (UNT_change_request_t, 1);
  request->type = Vaccinate;
  request->u.vaccinate.delay = delay;
  request->u.vaccinate.immunity_period = immunity_period;
  return request;
}



/**
 * Carries out a vaccination change request.
 *
 * @param unit a unit.
 * @param request a vaccination change request.
 * @param infectious_units a list of infectious units.
 */
void
UNT_apply_vaccinate_change_request (UNT_unit_t * unit,
                                    UNT_vaccinate_change_request_t * request,
                                    GHashTable * infectious_units)
{
  unsigned int delay;

#if DEBUG
  g_debug ("----- ENTER UNT_apply_vaccinate_change_request");
#endif

  /* If the unit is Susceptible and not already in the vaccine cycle, then we
   * start the vaccine cycle (i.e. delayed transition to Vaccine Immune). */
  if (unit->state == Susceptible && !unit->in_vaccine_cycle)
    {
      delay = request->delay;
      unit->immunity_start_countdown = delay;

      delay += request->immunity_period;
      unit->immunity_end_countdown = delay;

      unit->in_vaccine_cycle = TRUE;
    }
  /* If the unit is already Vaccine Immune, we re-set the time left for the
   * immunity according to the new parameter. */
  else if (unit->state == VaccineImmune)
    {
      delay = request->immunity_period;
      unit->immunity_end_countdown = delay;
    }

#if DEBUG
  g_debug ("----- EXIT UNT_apply_vaccinate_change_request");
#endif
  return;
}



/**
 * Carries out a destruction change request.
 *
 * @param unit a unit.
 * @param infectious_units a list of infectious units, which may change as a
 *   result of this operation.
 */
void
UNT_apply_destroy_change_request (UNT_unit_t * unit,
                                  GHashTable *infectious_units)
{
#if DEBUG
  g_debug ("----- ENTER UNT_apply_destroy_change_request");
#endif

  unit->in_vaccine_cycle = FALSE;
  unit->in_disease_cycle = FALSE;

  UNT_change_state (unit, Destroyed, infectious_units);

#if DEBUG
  g_debug ("----- EXIT UNT_apply_destroy_change_request");
#endif
}



/**
 * Carries out a change request.
 *
 * @param unit a unit.
 * @param request a change request.
 * @param infectious_units a list of infectious units, which may change as a
 *   result of this operation.
 */
void
UNT_apply_change_request (UNT_unit_t * unit,
                          UNT_change_request_t * request,
                          GHashTable *infectious_units)
{
  switch (request->type)
    {
    case Infect:
      UNT_apply_infect_change_request (unit, &(request->u.infect), infectious_units);
      break;
    case Vaccinate:
      UNT_apply_vaccinate_change_request (unit, &(request->u.vaccinate), infectious_units);
      break;
    default:
      g_assert_not_reached ();
    }
}



/**
 * Registers a request for a change to a unit.
 */
void
UNT_unit_add_change_request (UNT_unit_t * unit, UNT_change_request_t * request)
{
  unit->change_requests = g_slist_append (unit->change_requests, request);
}



/**
 * Deletes a change request structure from memory.
 *
 * @param request a change request.
 */
void
UNT_free_change_request (UNT_change_request_t * request)
{
  g_free (request);
}



/**
 * Wraps UNT_free_change_request so that it can be used in GLib calls.
 *
 * @param data a pointer to a UNT_change_request_t structure, but cast to a
 *   gpointer.
 * @param user_data not used, pass NULL.
 */
void
UNT_free_change_request_as_GFunc (gpointer data, gpointer user_data)
{
  UNT_free_change_request ((UNT_change_request_t *) data);
}



/**
 * Removes all change requests from a unit.
 *
 * @param unit a unit.
 */
void
UNT_unit_clear_change_requests (UNT_unit_t * unit)
{
  g_slist_foreach (unit->change_requests, UNT_free_change_request_as_GFunc, NULL);
  g_slist_free (unit->change_requests);
  unit->change_requests = NULL;
  unit->destroy_change_request = FALSE;
  unit->quarantine_change_request = FALSE;
}



void
UNT_unit_set_latitude (UNT_unit_t * unit, double lat)
{
  if (lat < -90)
    {
      g_warning ("latitude %g is out of bounds, setting to -90", lat);
      unit->latitude = -90;
    }
  else if (lat > 90)
    {
      g_warning ("latitude %g is out of bounds, setting to 90", lat);
      unit->latitude = 90;
    }
  else
    unit->latitude = lat;
}



void
UNT_unit_set_longitude (UNT_unit_t * unit, double lon)
{
  while (lon < -180)
    lon += 360;
  while (lon > 180)
    lon -= 360;
  unit->longitude = lon;
}



/**
 * Creates a new unit structure.
 *
 * @param production_type type of animals.
 * @param production_type_name type of animals.
 * @param size number of animals.
 * @param x x-coordinate of the unit's location.
 * @param y y-coordinate of the unit's location.
 * @return a pointer to a newly-created, initialized UNT_unit_t structure.
 */
UNT_unit_t *
UNT_new_unit (UNT_production_type_t production_type,
              gchar *production_type_name, unsigned int size, double x, double y)
{
  UNT_unit_t *unit;

  unit = g_new (UNT_unit_t, 1);

  unit->index = 0;
  unit->official_id = NULL;
  unit->production_type = production_type;
  unit->production_type_name = production_type_name;
  if (size < 1)
    {
      g_warning ("unit cannot have zero size, setting to 1");
      unit->size = 1;
    }
  else
    unit->size = size;
  unit->x = x;
  unit->y = y;
  unit->state = unit->initial_state = Susceptible;
  unit->days_in_state = 0;
  unit->days_in_initial_state = 0;
  unit->days_left_in_initial_state = 0;
  unit->quarantined = FALSE;
  unit->prevalence = 0;

  unit->in_vaccine_cycle = FALSE;
  unit->in_disease_cycle = FALSE;
  unit->prevalence_curve = NULL;
  unit->change_requests = NULL;
  unit->quarantine_change_request = FALSE;
  unit->destroy_change_request = FALSE;
  
  unit->db_id = 0;
  
#ifdef USE_SC_GUILIB
  unit->production_types = NULL;
  unit->ever_infected = FALSE;
  unit->day_first_infected = 0;
  unit->zone = NULL;
#endif

#ifdef USE_SC_GUILIB
  unit->production_types = NULL;
  unit->ever_infected = FALSE;
  unit->day_first_infected = 0;
  unit->zone = NULL;
  unit->cum_infected = 0;
  unit->cum_detected = 0;
  unit->cum_destroyed = 0;
  unit->cum_vaccinated = 0;
  unit->apparent_status = asUnknown;
  unit->apparent_status_day = 0;
#endif

#ifdef USE_SC_GUILIB
  unit->production_types = NULL;
  unit->ever_infected = FALSE;
  unit->day_first_infected = 0;
  unit->zone = NULL;
  unit->cum_infected = 0;
  unit->cum_detected = 0;
  unit->cum_destroyed = 0;
  unit->cum_vaccinated = 0;
  unit->apparent_status = asUnknown;
  unit->apparent_status_day = 0;
#endif

  return unit;
}



/**
 * Converts latitude and longitude to x and y coordinates on a map.
 *
 * @param unit a unit.
 * @param projection a map projection.  If NULL, the longitude will be copied
 *   unchanged to x and the latitude to y.  Otherwise, x and y will be filled
 *   in with projected coordinates.
 */
void
UNT_unit_project (UNT_unit_t * unit, projPJ projection)
{
  projUV p;

  if (projection == NULL)
    {
      unit->x = unit->longitude;
      unit->y = unit->latitude;
    }
  else
    {
      p.u = unit->longitude * DEG_TO_RAD;
      p.v = unit->latitude * DEG_TO_RAD;
      p = pj_fwd (p, projection);
      unit->x = p.u;
      unit->y = p.v;
    }

  return;
}



/**
 * Converts x and y coordinates on a map to latitude and longitude.
 *
 * @param unit a unit.
 * @param projection a map projection.  If NULL, the x-coordinate will be
 *   copied to longitude (and will be restricted to the range -180 to 180
 *   inclusive if necessary) and the y-coordinate will be copied to latitude
 *   (all will be restricted to the range -90 to 90 if necessary).
 */
void
UNT_unit_unproject (UNT_unit_t * unit, projPJ projection)
{
  projUV p;

  if (projection == NULL)
    {
      UNT_unit_set_longitude (unit, unit->x);
      UNT_unit_set_latitude (unit, unit->y);
    }
  else
    {
	  p.u = unit->x;
	  p.v = unit->y;
	  p = pj_inv (p, projection);
      UNT_unit_set_longitude (unit, p.u * RAD_TO_DEG);
      UNT_unit_set_latitude (unit, p.v * RAD_TO_DEG);
    }
#if DEBUG
  g_debug ("unit \"%s\" x,y %.1f,%.1f -> lat,lon %.3f,%.3f",
           unit->official_id, unit->x, unit->y,
           unit->latitude, unit->longitude);
#endif
  return;
}



/**
 * Returns a text representation of a unit.
 *
 * @param unit a unit.
 * @return a string.
 */
char *
UNT_unit_to_string (UNT_unit_t * unit)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<%s unit id=%s size=%u x=%g y=%g",
                    unit->production_type_name, unit->official_id, unit->size, unit->x, unit->y);

  /* Print the state, plus days left if applicable. */
  g_string_append_printf (s, "\n %s", UNT_state_name[unit->state]);
  if (unit->days_left_in_initial_state > 0)
    g_string_append_printf (s, " (%i days left) ", unit->days_left_in_initial_state);

  /* Print delayed transitions. */
#if 0
  for (iter = unit->delayed_transitions; iter != NULL; iter = g_list_next (iter))
    {
      transition = (UNT_delayed_transition_t *) (iter->data);
      substring = UNT_delayed_transition_to_string (transition);
      g_string_sprintfa (s, "\n %s", substring);
      free (substring);
    }
#endif
  g_string_append_c (s, '>');

  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Prints a unit to a stream.
 *
 * @param stream an output stream to write to.  If NULL, defaults to stdout.
 * @param unit a unit.
 * @return the number of characters written.
 */
int
UNT_fprintf_unit (FILE * stream, UNT_unit_t * unit)
{
  char *s;
  int nchars_written;

  s = UNT_unit_to_string (unit);
  nchars_written = fprintf (stream ? stream : stdout, "%s", s);
  free (s);
  return nchars_written;
}



/**
 * Deletes a unit structure from memory.  Does not free the production type
 * name string.
 *
 * @param unit a unit.
 * @param free_segment if TRUE, also frees the dynamically-allocated parts of
 *   the unit structure.
 */
void
UNT_free_unit (UNT_unit_t * unit, gboolean free_segment)
{
  if (free_segment == TRUE)
    {
      g_free (unit->official_id);
      UNT_unit_clear_change_requests (unit);
      /* We do not free the prevalence chart, because it is assumed to belong
       * to the disease module. */
    }
  g_free (unit);
}



/**
 * Creates a new, empty unit list.
 *
 * @return a pointer to a newly-created, empty UNT_unit_list_t structure.
 */
UNT_unit_list_t *
UNT_new_unit_list (void)
{
  UNT_unit_list_t *units;

  units = g_new (UNT_unit_list_t, 1);
  units->list = g_array_new (FALSE, FALSE, sizeof (UNT_unit_t));
#ifdef USE_SC_GUILIB
  units->production_types = NULL;
#endif
  units->production_type_names = g_ptr_array_new ();
  units->projection = NULL;

  return units;
}



/**
 * Deletes a unit list from memory.
 *
 * @param units a unit list.
 */
void
UNT_free_unit_list (UNT_unit_list_t * units)
{
  UNT_unit_t *unit;
  unsigned int nunits;
  int i;                        /* loop counter */

#if DEBUG
  g_debug ("----- ENTER UNT_free_unit_list");
#endif

  if (units == NULL)
    goto end;

  /* Free the dynamic parts of each unit structure. */
  nunits = UNT_unit_list_length (units);
  for (i = 0; i < nunits; i++)
    {
      unit = UNT_unit_list_get (units, i);
      g_free (unit->official_id);
      g_slist_foreach (unit->change_requests, UNT_free_change_request_as_GFunc, NULL);
    }

  /* Free the unit structures. */
  g_array_free (units->list, TRUE);

  /* Free the production type names. */
  for (i = 0; i < units->production_type_names->len; i++)
    g_free (g_ptr_array_index (units->production_type_names, i));
  g_ptr_array_free (units->production_type_names, TRUE);

  /* Free the projection. */
  if (units->projection != NULL)
    pj_free (units->projection);

  /* Finally, free the unit list structure. */
  g_free (units);

end:
#if DEBUG
  g_debug ("----- EXIT UNT_free_unit_list");
#endif
  return;
}



/**
 * Converts the latitude and longitude values to x and y coordinates on a map.
 *
 * @param units a unit list.
 * @param projection a map projection.  If NULL, the longitudes will be copied
 *   unchanged to x-coordinates and the latitudes to y-coordinates.
 */
void
UNT_unit_list_project (UNT_unit_list_t * units, projPJ projection)
{
  unsigned int nunits, i;

#if DEBUG
  g_debug ("----- ENTER UNT_unit_list_project");
#endif

  nunits = UNT_unit_list_length (units);
  for (i = 0; i < nunits; i++)
    {
      UNT_unit_project (UNT_unit_list_get (units, i), projection);
    }

#if DEBUG
  g_debug ("----- EXIT UNT_unit_list_project");
#endif

  return;
}


/**
 * Retrieves one unit from the database.
 *
 * @param data pointer to a UNT_unit_list_t structure.
 * @param dict the SQL query result as a GHashTable in which key = colname,
 *   value = value, both in (char *) format.
 * @return 0
 */
static int
UNT_load_unit_callback (void *data, GHashTable *dict)
{
  UNT_unit_list_t *units;
  UNT_unit_t *unit;
  GPtrArray *production_type_names;
  char *production_type_name;
  unsigned int i;
  UNT_production_type_t production_type_id;
  unsigned int size;

  units = (UNT_unit_list_t *) data;

  /* Production type */
  production_type_names = units->production_type_names;
  production_type_name = g_hash_table_lookup (dict, "name");
  for (i = 0; i < production_type_names->len; i++)
    {
      if (g_utf8_collate (production_type_name,
                          g_ptr_array_index (production_type_names, i)) == 0)
        {
          break;
        }
    }
  if (i == production_type_names->len)
    {
      /* We haven't encountered this production type before; add its name to
       * the list. */
      g_ptr_array_add (production_type_names, g_strdup(production_type_name));
      #if DEBUG
        g_debug ("  adding new production type \"%s\"", production_type_name);
      #endif
    }
  /* This next assignment loses the pointer to the production type name in the
   * row returned by the query. But that is OK, because that string is owned
   * by and will be freed by the SQLite library. */
  production_type_name = (char *) g_ptr_array_index (production_type_names, i);
  production_type_id = i;

  /* Size */
  {
    long tmp;
    errno = 0;
    tmp = strtol (g_hash_table_lookup (dict, "initial_size"), NULL, 10); /* base 10 */
    g_assert (errno != ERANGE && errno != EINVAL);
    g_assert (1 <= tmp && tmp <= UINT_MAX);
    size = (unsigned int) tmp;
  }

  unit = UNT_new_unit (production_type_id, production_type_name, size, 0, 0);

  /* Location */
  {
    double lat, lon;

    errno = 0;
    lat = strtod (g_hash_table_lookup (dict, "latitude"), NULL);
    g_assert (errno != ERANGE);
    UNT_unit_set_latitude (unit, lat);

    errno = 0;
    lon = strtod (g_hash_table_lookup (dict, "longitude"), NULL);
    g_assert (errno != ERANGE);
    UNT_unit_set_longitude (unit, lon);
  }

  /* Initial state */
  {
    char *state_code;
    UNT_state_t state;
    
    state_code = g_hash_table_lookup (dict, "initial_state");
    if (g_ascii_strncasecmp (state_code, "S", 1) == 0)
      state = Susceptible;
    else if (g_ascii_strncasecmp (state_code, "L", 1) == 0)
      state = Latent;
    else if (g_ascii_strncasecmp (state_code, "B", 1) == 0)
      state = InfectiousSubclinical;
    else if (g_ascii_strncasecmp (state_code, "C", 1) == 0)
      state = InfectiousClinical;
    else if (g_ascii_strncasecmp (state_code, "N", 1) == 0)
      state = NaturallyImmune;
    else if (g_ascii_strncasecmp (state_code, "V", 1) == 0)
      state = VaccineImmune;
    else if (g_ascii_strncasecmp (state_code, "D", 1) == 0)
      state = Destroyed;
    else
      {
        g_warning ("\"%s\" is not a valid unit state, defaulting to Susceptible",
                   state_code);
        state = Susceptible;
      }

    unit->state = unit->initial_state = state;
    #ifdef USE_SC_GUILIB
	  if ( state == Destroyed )
		unit->apparent_status = asDestroyed;
	  else if ( state == VaccineImmune )
		unit->apparent_status = asVaccinated;
	  else
		unit->apparent_status = asUnknown;

	  unit->apparent_status_day = 0;
	#endif
  }
  
  /* Official ID (arbitrary name attached to this unit) */
  unit->official_id = g_strdup (g_hash_table_lookup (dict, "user_notes"));

  /* Database ID */
  {
    long tmp;
    errno = 0;
    tmp = strtol (g_hash_table_lookup (dict, "id"), NULL, 10); /* base 10 */
    g_assert (errno != ERANGE && errno != EINVAL);
    g_assert (1 <= tmp && tmp <= G_MAXUINT);
    unit->db_id = (guint) tmp;
  }

  /* days-in-status and days-left-in-status tags */
  {
    char *days;
    long tmp;

    days = g_hash_table_lookup (dict, "days_in_initial_state");
    if (days != NULL)
      {
        errno = 0;
        tmp = strtol (days, NULL, /* base */ 10);
        g_assert (errno != ERANGE && errno != EINVAL);
        g_assert (0 <= tmp && tmp <= INT_MAX);
        unit->days_in_initial_state = (int) tmp;
      }

    days = g_hash_table_lookup (dict, "days_left_in_initial_state");        
    if (days != NULL)
      {
        errno = 0;
        tmp = strtol (days, NULL, /* base */ 10);
        g_assert (errno != ERANGE && errno != EINVAL);
        g_assert (0 <= tmp && tmp <= INT_MAX);
        unit->days_left_in_initial_state = (int) tmp;
      }
  }

  UNT_unit_list_append (units, unit);
  UNT_free_unit (unit, FALSE);

  return 0;
}



/**
 * Loads a unit list from a scenario database.  Use UNT_unit_list_project() to
 * convert the lats and lons to a flat map.  Also, a bounding rectangle has not
 * been computed; use either UNT_unit_list_unoriented_bounding_box() or
 * UNT_unit_list_oriented_bounding_box to fill that in.
 *
 * @param db a scenario database.
 * @return a unit list.
 */
UNT_unit_list_t *
#ifdef USE_SC_GUILIB
UNT_load_unit_list (sqlite3 *db, GPtrArray *production_types)
#else
UNT_load_unit_list (sqlite3 *db)
#endif
{
  UNT_unit_list_t *units;
  char *sqlerr;

#if DEBUG
  g_debug ("----- ENTER UNT_load_unit_list");
#endif

  units = UNT_new_unit_list ();
#ifdef USE_SC_GUILIB
  units->production_types = production_types;
#endif

  sqlite3_exec_dict (db, "SELECT unit.id,name,latitude,longitude,initial_state,days_in_initial_state,days_left_in_initial_state,initial_size,user_notes FROM ScenarioCreator_unit unit,ScenarioCreator_productiontype prodtype where unit.production_type_id=prodtype.id",
                     UNT_load_unit_callback, units, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }

#if DEBUG
  g_debug ("----- EXIT UNT_load_unit_list");
#endif
  return units;
}



/**
 * Appends a unit to a unit list.  NB: The contents of the unit structure are
 * shallow-copied into an array, so you may free the unit structure <em>but not
 * its dynamically-allocated children</em> after adding it to a unit list.
 *
 * @param units a unit list.
 * @param unit a unit.
 * @return the new length of the unit list.
 */
unsigned int
UNT_unit_list_append (UNT_unit_list_t * units, UNT_unit_t * unit)
{
  GArray *list;
  unsigned int new_length;

  list = units->list;
  g_array_append_val (list, *unit);
  new_length = UNT_unit_list_length (units);

  /* Now make the pointer point to the copy in the unit list. */
  unit = &g_array_index (list, UNT_unit_t, new_length - 1);

  /* Set the list index number for the unit. */
  unit->index = new_length - 1;

  return new_length;
}



/**
 * Returns a text string containing a unit list.
 *
 * @param units a unit list.
 * @return a string.
 */
char *
UNT_unit_list_to_string (UNT_unit_list_t * units)
{
  GString *s;
  char *substring, *chararray;
  unsigned int nunits;
  unsigned int i;               /* loop counter */

  s = g_string_new (NULL);

  nunits = UNT_unit_list_length (units);
  if (nunits > 0)
    {
      substring = UNT_unit_to_string (UNT_unit_list_get (units, 0));
      g_string_assign (s, substring);
      g_free (substring);
      for (i = 1; i < nunits; i++)
        {
          substring = UNT_unit_to_string (UNT_unit_list_get (units, i));
          g_string_append_printf (s, "\n%s", substring);
          g_free (substring);
        }
    }
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Prints a unit list to a stream.
 *
 * @param stream an output stream to write to.  If NULL, defaults to stdout.
 * @param units a unit list.
 * @return the number of characters written.
 */
int
UNT_fprintf_unit_list (FILE * stream, UNT_unit_list_t * units)
{
  char *s;
  int nchars_written;

  g_debug ("----- ENTER UNT_fprintf_unit_list");

  if (!stream)
    stream = stdout;

  s = UNT_unit_list_to_string (units);
  nchars_written = fprintf (stream, "%s", s);
  free (s);

  g_debug ("----- EXIT UNT_fprintf_unit_list");

  return nchars_written;
}



/**
 * Returns a text string giving the state of each unit.
 *
 * @param units a unit list.
 * @return a string.
 */
char *
UNT_unit_list_summary_to_string (UNT_unit_list_t * units)
{
  GString *s;
  char *chararray;
  unsigned int nunits;          /* number of units */
  unsigned int i;               /* loop counter */

  nunits = UNT_unit_list_length (units);
  s = g_string_new (NULL);
  g_string_sprintf (s, "%i", UNT_unit_list_get (units, 0)->state);
  for (i = 1; i < nunits; i++)
    g_string_sprintfa (s, " %i", UNT_unit_list_get (units, i)->state);

  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}


/**
 * Returns a text string giving the prevalence of each infected unit.
 *
 * @param units a unit list.
 * @param day the simulation day for which the prevalence is being recorded.
 * @return a string.
 */
char *
UNT_unit_list_prevalence_to_string (UNT_unit_list_t * units, unsigned int day)
{
  GString *s;
  char *chararray;
  unsigned int nunits;          /* number of units */
  unsigned int i;               /* loop counter */
  gboolean first_infected_found;
  int unit_state;

  first_infected_found = FALSE;
  nunits = UNT_unit_list_length (units);
  s = g_string_new (NULL);


  for (i = 0; i < nunits; i++)
    {
      unit_state = UNT_unit_list_get (units, i)->state;

      if ((Latent == unit_state)
          || (InfectiousSubclinical == unit_state) || (InfectiousClinical == unit_state))
        {
          if (FALSE == first_infected_found)
            {
              first_infected_found = TRUE;

              g_string_sprintf (s, "%i, %s, s%is, %f",  /* The second and third "s"'s in the string look
                                                         * funny, but they're there for a reason. */
                                day,
                                UNT_unit_list_get (units, i)->official_id,
                                unit_state, UNT_unit_list_get (units, i)->prevalence);
            }
          else
            {
              g_string_sprintfa (s, "\r\n%i, %s, s%is, %f",     /* The second and third "s"'s in the string look
                                                                 * funny, but they're there for a reason. */
                                 day,
                                 UNT_unit_list_get (units, i)->official_id,
                                 unit_state, UNT_unit_list_get (units, i)->prevalence);
            }
        }
    }

  if (FALSE == first_infected_found)
    g_string_sprintf (s, "%i, (No infected units)", day);

  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Resets a unit to alive, Susceptible, and not quarantined.
 *
 * @param unit a unit.
 */
void
UNT_reset (UNT_unit_t * unit)
{
  unit->state = Susceptible;
  unit->days_in_state = 0;
  unit->quarantined = FALSE;
  unit->in_vaccine_cycle = FALSE;
  unit->in_disease_cycle = FALSE;
#ifdef USE_SC_GUILIB
  unit->ever_infected = FALSE;
  unit->day_first_infected = 0;
  unit->zone = NULL;
  unit->apparent_status = asUnknown;
  unit->apparent_status_day = 0;
#endif
  UNT_unit_clear_change_requests (unit);
}



/**
 * Advances a unit's state by one time step (day).
 *
 * This function is called <em>before</em> any sub-models that may be operating.
 * It carries out changes or delayed transitions that the models may have set.
 *
 * This function resolves conflicts among changes set by sub-models.  For
 * example, with sub-models operating largely independently, it may be possible
 * for a unit to be infected in the morning, vaccinated at noon, and
 * destroyed later in the day!
 *
 * The conflict resolution rules implemented here say:
 * <ol>
 *   <li>
 *     An order to quarantine is processed first.
 *   <li>
 *     Infection, vaccination, and destruction are processed next.  If both
 *     infection and vaccination, both infection and destruction, both
 *     vaccination and destruction, or all three are pending, the order in
 *     which they happen is chosen randomly.  If more than one disease spread
 *     sub-model has caused an infection, one cause and its associated
 *     parameters (latent period, etc.) is chosen randomly.  Similarly, if more
 *     than one sub-model has requestion destruction or vaccination, one
 *     reason for the action is chosen randomly.
 *   <li>
 *     Biological processes happening inside the animals (e.g., the natural
 *     progression of the disease or the process of gaining immunity from a
 *     vaccine) are processed last.
 * </ol>
 *
 * @param unit a unit.
 * @param infectious_units the set of infectious units.
 * @return the state of the unit.
 */
UNT_state_t
UNT_step (UNT_unit_t * unit, GHashTable *infectious_units)
{
  UNT_state_t old_state;
  GSList *iter;
  UNT_change_request_t *request;

  old_state = unit->state;
  unit->days_in_state++;

  if (unit->quarantine_change_request)
    unit->quarantined = TRUE;

  if (unit->destroy_change_request)
    UNT_apply_destroy_change_request (unit, infectious_units);

  /* Apply requested changes in the order in which they occur. */
  for (iter = unit->change_requests; iter != NULL; iter = g_slist_next (iter))
    {
      request = (UNT_change_request_t *) (iter->data);
      UNT_apply_change_request (unit, request, infectious_units);
    }
  UNT_unit_clear_change_requests (unit);

  /* Take any delayed transitions. */
  if (unit->in_vaccine_cycle)
    {
      if (unit->immunity_start_countdown-- == 0)
        UNT_change_state (unit, VaccineImmune, infectious_units);
      if (unit->immunity_end_countdown-- == 0)
        {
          UNT_change_state (unit, Susceptible, infectious_units);
          unit->in_vaccine_cycle = FALSE;
        }
    }

  if (unit->in_disease_cycle)
    {
      if (unit->immunity_start_countdown > 0)
        {
          if (unit->prevalence_curve == NULL)
            {
              unit->prevalence = 1;
              #if DEBUG
                g_debug ("prevalence = 1");
              #endif
            }
          else
            {
              unit->prevalence = REL_chart_lookup ((0.5 + unit->day_in_disease_cycle) /
                                                   (unit->day_in_disease_cycle +
                                                    unit->immunity_start_countdown),
                                                   unit->prevalence_curve);
              #if DEBUG
                g_debug ("prevalence = lookup((%i+0.5)/(%i+%i))=%g",
                         unit->day_in_disease_cycle,
                         unit->day_in_disease_cycle, unit->immunity_start_countdown, unit->prevalence);
              #endif
            }
        }
      else
        {
          unit->prevalence = 0;
          #if DEBUG
            g_debug ("prevalence = 0");
          #endif
        }

      unit->day_in_disease_cycle++;
      if (unit->infectious_start_countdown-- == 0)
        UNT_change_state (unit, InfectiousSubclinical, infectious_units);
      if (unit->clinical_start_countdown-- == 0)
        UNT_change_state (unit, InfectiousClinical, infectious_units);
      if (unit->immunity_start_countdown-- == 0)
        UNT_change_state (unit, NaturallyImmune, infectious_units);
      if (unit->immunity_end_countdown-- == 0)
        {
          UNT_change_state (unit, Susceptible, infectious_units);
          unit->in_disease_cycle = FALSE;
        }   
    }

  if (unit->state != old_state)
    {
      UNT_update_t update;
      update.unit_index = unit->index;
      update.state = (ADSM_disease_state) unit->state;
#ifdef USE_SC_GUILIB
      sc_change_unit_state ( unit, update );
#else
      if (NULL != adsm_change_unit_state)
        {
          adsm_change_unit_state (update);
        }
#endif
    }

  return unit->state;
}



/**
 * Infects a unit with a disease.
 *
 * @param unit the unit to be infected.
 * @param latent_period the number of days to spend latent.
 * @param infectious_subclinical_period the number of days to spend infectious
 *   without visible signs.
 * @param infectious_clinical_period the number of days to spend infectious
 *   with visible signs.
 * @param immunity_period how many days the unit's natural immunity lasts
 *   after recovery
 * @param day_in_disease_cycle how many days into the disease cycle the unit
 *   should start.  Normally 0, but sometimes used to create an initially
 *   infected unit that has already been diseased for a while when the
 *   simulation begins.
 */
void
UNT_infect (UNT_unit_t * unit,
            int latent_period,
            int infectious_subclinical_period,
            int infectious_clinical_period,
            int immunity_period,
            unsigned int day_in_disease_cycle)
{
  UNT_unit_add_change_request (unit,
                               UNT_new_infect_change_request
                               (latent_period, infectious_subclinical_period,
                                infectious_clinical_period, immunity_period,
                                day_in_disease_cycle));
}



/**
 * Vaccinates a unit against a disease.
 *
 * @param unit the unit to be vaccinated.
 * @param delay the number of days before immunity begins.
 * @param immunity_period the number of days the immunity lasts.
 */
void
UNT_vaccinate (UNT_unit_t * unit, int delay, int immunity_period)
{
  UNT_unit_add_change_request (unit, UNT_new_vaccinate_change_request (delay, immunity_period));
}



/**
 * Quarantines a unit.
 *
 * @param unit the unit to be quarantined.
 */
void
UNT_quarantine (UNT_unit_t * unit)
{
  unit->quarantine_change_request = TRUE;
}



/**
 * Destroys a unit.
 *
 * @param unit the unit to be destroyed.
 */
void
UNT_destroy (UNT_unit_t * unit)
{
  unit->destroy_change_request = TRUE;
}



/**
 * Removes a unit from the infectious list.
 *
 * @param unit the unit to be removed.
 * @param infectious_units the set of infectious units.
 */
void
UNT_remove_unit_from_infectious_list( UNT_unit_t *unit,
                                      GHashTable *infectious_units )
{
  if ( ( unit != NULL ) && ( infectious_units != NULL ) )
    g_hash_table_remove( infectious_units, GUINT_TO_POINTER(unit->index) );
}



/**
 * Adds a unit to the infectious list.
 *
 * @param unit the unit to be added.
 * @param infectious_units the set of infectious units.
 */
void
UNT_add_unit_to_infectious_list( UNT_unit_t *unit,
                                 GHashTable *infectious_units )
{
  if ( ( unit != NULL ) && ( infectious_units != NULL ) )
  {
    if ( g_hash_table_lookup( infectious_units, GUINT_TO_POINTER(unit->index) ) == NULL )
      g_hash_table_insert( infectious_units, GUINT_TO_POINTER(unit->index), (gpointer)unit );
  };
}


/**
 * Returns the units with a given state.
 *
 * @param units a unit list.
 * @param state the desired state.
 * @param list a location in which to store the address of a list of pointers
 *   to units.
 * @return the number of units with the given state.
 */
unsigned int
UNT_unit_list_get_by_state (UNT_unit_list_t * units, UNT_state_t state, UNT_unit_t *** list)
{
  unsigned int nunits;
  UNT_unit_t *unit;
  unsigned int count = 0;
  unsigned int i;

  /* Count the units with the given state. */
  nunits = UNT_unit_list_length (units);
  for (i = 0; i < nunits; i++)
    if (UNT_unit_list_get (units, i)->state == state)
      count++;

  if (count == 0)
    (*list) = NULL;
  else
    {
      /* Allocate and fill the array. */
      *list = g_new (UNT_unit_t *, count);
      count = 0;
      for (i = 0; i < nunits; i++)
        {
          unit = UNT_unit_list_get (units, i);
          if (unit->state == state)
            (*list)[count++] = unit;
        }
    }
  return count;
}


/**
 * Returns the units with a given initial state.
 *
 * @param units a unit list.
 * @param state the desired state.
 * @param list a location in which to store the address of a list of pointers
 *   to units.
 * @return the number of units with the given state.
 */
unsigned int
UNT_unit_list_get_by_initial_state (UNT_unit_list_t * units, UNT_state_t state, UNT_unit_t *** list)
{
  unsigned int nunits;
  UNT_unit_t *unit;
  unsigned int count = 0;
  unsigned int i;

  /* Count the units with the given state. */
  nunits = UNT_unit_list_length (units);
  for (i = 0; i < nunits; i++)
    if (UNT_unit_list_get (units, i)->initial_state == state)
      count++;

  if (count == 0)
    (*list) = NULL;
  else
    {
      /* Allocate and fill the array. */
      *list = g_new (UNT_unit_t *, count);
      count = 0;
      for (i = 0; i < nunits; i++)
        {
          unit = UNT_unit_list_get (units, i);
          if (unit->initial_state == state)
            (*list)[count++] = unit;
        }
    }
  return count;
}

/* end of file unit.c */
