#if HAVE_CONFIG_H
#  include <config.h>
#endif

#if STDC_HEADERS
#  include <stdlib.h>
#  include <string.h>
#endif

#include <general.h>

/*  New Scenario and Iteration storage areas  */
  MAIN_scenario _scenario;
  MAIN_iteration _iteration;
/*  END New Scenario and Iteration storage areas  */


const char UNT_APPARENT_STATE_CHAR[7] = {'u', 'U', 'E', 'T', 'I', 'V', 'D'};
const char UNT_STATE_CHAR[UNT_NSTATES] = {'S', 'L', 'B', 'C', 'N', 'V', 'D'};

void init_MAIN_structs()
{
  _scenario.scenarioId = NULL;
  _scenario.description = NULL;
#ifndef HAVE_STRING_H
  _scenario.version[0] = '\0';
#else
  memset( _scenario.version, 0, 50 );
#endif
  _scenario.nruns = 0;
  _scenario.random_seed = 0;
  _scenario.iterations_completed = 0;
  _scenario.start_time = 0;
  _scenario.end_time = 0;
  _scenario.total_processor_time = 0.0;

  _iteration.diseaseEndDay = 0;
  _iteration.outbreakEndDay = 0;
  _iteration.zoneFociCreated = FALSE;
  _iteration._unitsInZones = NULL;
  _iteration.infectious_units = NULL;
}
