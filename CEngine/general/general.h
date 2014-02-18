#ifndef GENERAL_H
#define GENERAL_H
#if HAVE_CONFIG_H
#  include <config.h>
#endif

#if STDC_HEADERS
#  include <stdlib.h>
#endif

#include <glib.h>

#include <unit.h>
#include <zone.h>



typedef struct
{
  char        *scenarioId;
  char        *description;
  char         version[50];
  unsigned long nruns;
  unsigned long random_seed;
  unsigned long iterations_completed;
  unsigned long start_time;
  unsigned long end_time;
  double total_processor_time;
} MAIN_scenario;

typedef struct
{
  int diseaseEndDay;
  int outbreakEndDay;
  gboolean zoneFociCreated;
  GPtrArray *_unitsInZones;
  GHashTable *infectious_units;  /*  Currently defined as Latent, Infectious Subclinical,
                                 or Infectious Clinical. GHashTable is used because it is very fast
                                 and allows for easy removal and/or testing of items presence over
                                 GArray or GPtrArray */
  guint current_day;
  gboolean first_detection;
} MAIN_iteration;

/*  New Scenario and Iteration storage areas (stored in main.c data space ) */
extern  MAIN_scenario _scenario;
extern  MAIN_iteration _iteration;
/*  END New Scenario and Iteration storage areas  */

void init_MAIN_structs();

#endif
