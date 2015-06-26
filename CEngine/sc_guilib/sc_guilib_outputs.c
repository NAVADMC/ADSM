/** @file sc_guilib_outputs.c
 *
 * @author Shaun Case <ShaunCase@colostate.edu><br>
 *   Animal Population Health Institute<br>
 *   College of Veterinary Medicine and Biomedical Sciences<br>
 *   Colorado State University<br>
 *   Fort Collins, CO 80523<br>
 *   USA
 * @version 0.1
 * @date February 2009
 *
 * Copyright &copy; 2005 - 2009 Animal Population Health Institute,
 * Colorado State University
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#if HAVE_CONFIG_H
#  include <config.h>
#endif

#ifdef USE_SC_GUILIB

#if STDC_HEADERS
#  include <string.h>
#endif

#if HAVE_STRINGS_H
#  include <strings.h>
#endif

#if HAVE_MATH_H
#  include <math.h>
#endif

#if defined( USE_MPI ) && !CANCEL_MPI
  #include <mpi.h>
#endif

#include <time.h>

#include "sc_guilib_outputs.h"
#include "sc_database.h"

void sc_change_unit_state( UNT_unit_t *_unit, UNT_update_t _update )
{
  PRT_production_type_data_t *_ptype;

#if DEBUG
  g_debug ("----- ENTER sc_change_unit_state");
#endif

  _ptype = (PRT_production_type_data_t *)g_ptr_array_index( _unit->production_types, _unit->production_type );
  
  switch( _update.state )
  {
    case Susceptible:
      _ptype->d_data.tsdUSusc = _ptype->d_data.tsdUSusc + 1;
      _ptype->d_data.tsdASusc = _ptype->d_data.tsdASusc + _unit->size;

      _ptype->data.tscUSusc = _ptype->data.tscUSusc + 1;
      _ptype->data.tscASusc = _ptype->data.tscASusc + _unit->size;
    break;

    case Latent:
      _ptype->d_data.tsdULat = _ptype->d_data.tsdULat + 1;
      _ptype->d_data.tsdALat = _ptype->d_data.tsdALat + _unit->size;

      _ptype->data.tscULat = _ptype->data.tscULat + 1;
      _ptype->data.tscALat = _ptype->data.tscALat + _unit->size;

    break;

    case InfectiousSubclinical:
      _ptype->d_data.tsdUSubc = _ptype->d_data.tsdUSubc + 1;
      _ptype->d_data.tsdASubc = _ptype->d_data.tsdASubc + _unit->size;

      _ptype->data.tscUSubc = _ptype->data.tscUSubc + 1;
      _ptype->data.tscASubc = _ptype->data.tscASubc + _unit->size;

    break;

    case InfectiousClinical:
      _ptype->d_data.tsdUClin = _ptype->d_data.tsdUClin + 1;
      _ptype->d_data.tsdAClin = _ptype->d_data.tsdAClin + _unit->size;

      _ptype->data.tscUClin = _ptype->data.tscUClin + 1;
      _ptype->data.tscAClin = _ptype->data.tscAClin + _unit->size;

    break;

    case NaturallyImmune:
      _ptype->d_data.tsdUNImm = _ptype->d_data.tsdUNImm + 1;
      _ptype->d_data.tsdANImm = _ptype->d_data.tsdANImm + _unit->size;

      _ptype->data.tscUNImm = _ptype->data.tscUNImm + 1;
      _ptype->data.tscANImm = _ptype->data.tscANImm + _unit->size;

    break;

    case VaccineImmune:
      _ptype->d_data.tsdUVImm = _ptype->d_data.tsdUVImm + 1;
      _ptype->d_data.tsdAVImm = _ptype->d_data.tsdAVImm + _unit->size;

      _ptype->data.tscUVImm = _ptype->data.tscUVImm + 1;
      _ptype->data.tscAVImm = _ptype->data.tscAVImm + _unit->size;
    break;

    case Destroyed:
      _ptype->d_data.tsdUDest = _ptype->d_data.tsdUDest + 1;
      _ptype->d_data.tsdADest = _ptype->d_data.tsdADest + _unit->size;

      _ptype->data.tscUDest = _ptype->data.tscUDest + 1;
      _ptype->data.tscADest = _ptype->data.tscADest + _unit->size;
    break;
  };

#if DEBUG
  g_debug ("----- EXIT sc_change_unit_state");
#endif
}

void sc_infect_unit( unsigned short int _day, UNT_unit_t *_unit, UNT_update_t _update )
{
  PRT_production_type_data_t *_ptype;
#if DEBUG
  g_debug ("----- ENTER sc_infect_unit");
#endif

#if DEBUG
  g_debug ("----- sc_infect_unit:  Day: %i, _unit.production_types: %lu, update.msg: %s",  _day, _unit->production_types, _update.msg);
  g_debug ("----- sc_infect_unit:  _unit.production_type (index): %i", _unit->production_type );
#endif

  _ptype = (PRT_production_type_data_t *)g_ptr_array_index( _unit->production_types, _unit->production_type );

  _unit->ever_infected = TRUE;
  _unit->day_first_infected = _day;

  if ( strncmp( _update.msg, "initially infected", 18 ) == 0 )
  {
    if ( 1 < _day )
    {
      /*  Delphi code does:
          raise exception.Create( '''Initial'' infection occurring after day 1.' );
      */

      g_critical ("'Initial' infection occurring after day 1.");
      /* To Exit or not to Exit??  */
    };

    _ptype->data.infcUIni = _ptype->data.infcUIni + 1;
    _ptype->data.infcAIni = _ptype->data.infcAIni + _unit->size;	
  }
  else
    if ( strncmp( _update.msg, "airborne spread", 15 ) == 0 )
    {
     _ptype->data.infcUAir = _ptype->data.infcUAir + 1;
     _ptype->data.infcAAir = _ptype->data.infcAAir + _unit->size;

     _ptype->d_data.infnUAir = _ptype->d_data.infnUAir + 1;
     _ptype->d_data.infnAAir = _ptype->d_data.infnAAir + _unit->size;
    }
    else
      if ( strncmp( _update.msg, "Direct Contact", 14 ) == 0 )
      {
        _ptype->data.infcUDir = _ptype->data.infcUDir + 1;
        _ptype->data.infcADir = _ptype->data.infcADir + _unit->size;

        _ptype->d_data.infnUDir = _ptype->d_data.infnUDir + 1;
        _ptype->d_data.infnADir = _ptype->d_data.infnADir + _unit->size;

      }
      else
        if ( strncmp( _update.msg, "Indirect Contact", 16 ) == 0 )
      	{
          _ptype->data.infcUInd = _ptype->data.infcUInd + 1;
          _ptype->data.infcAInd = _ptype->data.infcAInd + _unit->size;

          _ptype->d_data.infnUInd = _ptype->d_data.infnUInd + 1;
          _ptype->d_data.infnAInd = _ptype->d_data.infnAInd + _unit->size;

        }
        else
        {
          g_critical ("sc_infect_unit:  Unrecognized infection mechanism (%s)", _update.msg );
          /* To Exit or not to Exit??  */
        };
  
  _unit->cum_infected = _unit->cum_infected + 1;
#if DEBUG
  g_debug ("----- EXIT sc_infect_unit");
#endif
}


void sc_expose_unit( UNT_unit_t *_exposed_unit, UNT_update_t _update )
{
  PRT_production_type_data_t *_ptype;
#if DEBUG
  g_debug ("----- ENTER sc_expose_unit");
#endif
  _ptype = (PRT_production_type_data_t *)g_ptr_array_index( _exposed_unit->production_types, _exposed_unit->production_type );

  if ( strncmp( _update.msg, "Direct Contact", 14 ) == 0 )
  {
    _ptype->data.expcUDir = _ptype->data.expcUDir + 1;
    _ptype->data.expcADir = _ptype->data.expcADir + _exposed_unit->size;
  }
  else
    if ( strncmp( _update.msg, "Indirect Contact", 16 ) == 0 )
    {
      _ptype->data.expcUInd = _ptype->data.expcUInd + 1;
      _ptype->data.expcAInd = _ptype->data.expcAInd + _exposed_unit->size;
    }
    else
    {
      g_critical ("sc_expose_unit:  Unrecognized exposure mechanism (%s)", _update.msg );
      /* To Exit or not to Exit??  */
    };

#if DEBUG
  g_debug ("----- EXIT sc_expose_unit");
#endif
}

void sc_attempt_trace_unit( UNT_unit_t *_exposed_unit, UNT_update_t _update )
{
  PRT_production_type_data_t *_ptype;
#if DEBUG
  g_debug ("----- ENTER sc_attempt_trace_unit");
#endif
  _ptype = (PRT_production_type_data_t *)g_ptr_array_index( _exposed_unit->production_types, _exposed_unit->production_type );

  if ( strncmp( _update.msg, "Direct Contact", 14 ) == 0 )
  {
    _ptype->data.trcUDirp = _ptype->data.trcUDirp + 1;
    _ptype->data.trcADirp = _ptype->data.trcADirp + _exposed_unit->size;

    if ( -1 == _update.success )
    {
      _ptype->d_data.trnUDir = _ptype->d_data.trnUDir + 1;
      _ptype->d_data.trnADir = _ptype->d_data.trnADir + _exposed_unit->size;

      _ptype->data.trcUDir = _ptype->data.trcUDir + 1;
      _ptype->data.trcADir = _ptype->data.trcADir + _exposed_unit->size;
	  if ( _exposed_unit->apparent_status != asDestroyed )
		_exposed_unit->apparent_status = asTraceDirect;
    };
  }
  else
    if ( strncmp( _update.msg, "Indirect Contact", 16 ) == 0 )
    {
      _ptype->data.trcUIndp = _ptype->data.trcUIndp + 1;
      _ptype->data.trcAIndp = _ptype->data.trcAIndp + _exposed_unit->size;

      if ( -1 == _update.success )
      {
        _ptype->d_data.trnUInd = _ptype->d_data.trnUInd + 1;
        _ptype->d_data.trnAInd = _ptype->d_data.trnAInd + _exposed_unit->size;

        _ptype->data.trcUInd = _ptype->data.trcUInd + 1;
        _ptype->data.trcAInd = _ptype->data.trcAInd + _exposed_unit->size;
		if ( _exposed_unit->apparent_status != asDestroyed )
		  _exposed_unit->apparent_status = asTraceIndirect;
      }
    }
    else
    {
      g_critical ("sc_attempt_trace_unit:  Unrecognized trace reason (%s)", _update.msg );
      /* To Exit or not to Exit??  */
    };

#if DEBUG
  g_debug ("----- EXIT sc_attempt_trace_unit");
#endif
}

void sc_detect_unit( unsigned short int _day, UNT_unit_t *_unit, UNT_update_t _update )
{
  PRT_production_type_data_t *_ptype;
#if DEBUG
  g_debug ("----- ENTER sc_detect_unit");
#endif
  _ptype = (PRT_production_type_data_t *)g_ptr_array_index( _unit->production_types, _unit->production_type );

  _ptype->data.detcUClin = _ptype->data.detcUClin + 1;
  _ptype->data.detcAClin = _ptype->data.detcAClin + _unit->size;

  _ptype->d_data.detnUClin = _ptype->d_data.detnUClin + 1;
  _ptype->d_data.detnAClin = _ptype->d_data.detnAClin + _unit->size;
  _ptype->d_data.appUInfectious = _ptype->d_data.appUInfectious + 1;

   if ( -1 ==  _ptype->data.firstDetection )
   {
      _ptype->data.firstDetection = _day;
   };

  _unit->cum_detected = _unit->cum_detected + 1;
  _unit->apparent_status = asDetected;
  _unit->apparent_status_day = _day;
  
#if DEBUG
  g_debug ("----- EXIT sc_detect_unit");
#endif
}


void sc_destroy_unit( unsigned short int _day, UNT_unit_t *_unit, UNT_update_t _update )
{
  PRT_production_type_data_t *_ptype;
#if DEBUG
  g_debug ("----- ENTER sc_destroy_unit");
#endif
  _ptype = (PRT_production_type_data_t *)g_ptr_array_index( _unit->production_types, _unit->production_type );

  if ( -1 == _ptype->data.firstDestruction )
  {
    _ptype->data.firstDestruction = _day;
  };

  if ( strncmp( _update.msg, "trace out-indirect contact", 26 ) == 0 )
  {
    _ptype->data.descUInd = _ptype->data.descUInd + 1;
    _ptype->data.descAInd = _ptype->data.descAInd + _unit->size;
  }
  else
    if ( strncmp( _update.msg, "trace out-direct contact", 24 ) == 0 )
    {
      _ptype->data.descUDir = _ptype->data.descUDir + 1;
      _ptype->data.descADir = _ptype->data.descADir + _unit->size;
    }
    else
      if ( strncmp( _update.msg, "ring destruction", 16 ) == 0 )
      {
        _ptype->data.descURing = _ptype->data.descURing + 1;
        _ptype->data.descARing = _ptype->data.descARing + _unit->size;
      }
      else
        if ( strncmp( _update.msg, "reported diseased", 17 ) == 0 )
        {
          _ptype->data.descUDet = _ptype->data.descUDet + 1;
          _ptype->data.descADet = _ptype->data.descADet + _unit->size;
        }
        else
          if ( strncmp( _update.msg, "initially destroyed", 19 ) == 0 )
          {
            _ptype->data.descUIni = _ptype->data.descUIni + 1;
            _ptype->data.descAIni = _ptype->data.descAIni + _unit->size;
          }
          else
          {
            g_critical ("sc_destroy_unit:  Unrecognized destruction reason (%s)", _update.msg );
            /* To Exit or not to Exit??  */
          };

  _unit->cum_destroyed = _unit->cum_destroyed + 1;
  
  _ptype->d_data.desnUAll = _ptype->d_data.desnUAll + 1;
  _ptype->d_data.desnAAll = _ptype->d_data.desnAAll + _unit->size;
  _unit->apparent_status = asDestroyed;
  _unit->apparent_status_day = _day;
  
  /* If this unit was previously "enzoned", it can be taken out of the list now. */
  g_ptr_array_remove( _iteration._unitsInZones, _unit );
  _unit->zone = NULL;

#if DEBUG
  g_debug ("----- EXIT sc_destroy_unit");
#endif
}


void sc_vaccinate_unit( unsigned short int _day, UNT_unit_t *_unit, UNT_update_t _update )
{
  PRT_production_type_data_t *_ptype;
#if DEBUG
  g_debug ("----- ENTER sc_vaccinate_unit");
#endif
 _ptype = (PRT_production_type_data_t *)g_ptr_array_index( _unit->production_types, _unit->production_type );

  if ( -1 == _ptype->data.firstVaccination )
  {
    _ptype->data.firstVaccination = _day;
  };

  if ( strncmp( _update.msg, "ring vaccination", 16 ) == 0 )
  {
    _ptype->data.vaccURing = _ptype->data.vaccURing + 1;
    _ptype->data.vaccARing = _ptype->data.vaccARing + _unit->size;
  }
  else
    if ( strncmp( _update.msg, "initially immune", 16 ) == 0 )
    {
      _ptype->data.vaccUIni = _ptype->data.vaccUIni + 1;
      _ptype->data.vaccAIni = _ptype->data.vaccAIni + _unit->size;
    }
    else
    {
      g_critical ("sc_vaccinate_unit:  Unrecognized vaccination reason (%s)", _update.msg );
      /* To Exit or not to Exit??  */
    };

  _ptype->d_data.vaccUAll = _ptype->d_data.vaccUAll + 1;
  _ptype->d_data.vaccAAll = _ptype->d_data.vaccAAll + _unit->size;
  _unit->apparent_status = asVaccinated;
  _unit->apparent_status_day = _day;
  
  _unit->cum_vaccinated = _unit->cum_vaccinated + 1;  
  
#if DEBUG
  g_debug ("----- EXIT sc_vaccinate_unit");
#endif
}

void sc_make_zone_focus( unsigned short int _day, UNT_unit_t *_unit )
{
  PRT_production_type_data_t *_ptype;
#if DEBUG
  g_debug ("----- ENTER sc_make_zone_focus");
#endif
  _iteration.zoneFociCreated = TRUE;

  _ptype = (PRT_production_type_data_t *)g_ptr_array_index( _unit->production_types, _unit->production_type );

  _ptype->data.zoncFoci = _ptype->data.zoncFoci + 1;
  _ptype->d_data.zonnFoci = _ptype->d_data.zonnFoci + 1;

#if DEBUG
  g_debug ("----- EXIT sc_make_zone_focus");
#endif
}

void sc_iteration_start( GPtrArray *_production_types, UNT_unit_list_t *units, unsigned int _run )
{
#if DEBUG
  g_debug ("----- ENTER sc_iteration_start");
#endif

  clear_production_type_list_data( _production_types );
  _iteration.diseaseEndDay = -1;
  _iteration.outbreakEndDay = -1;
  _iteration.zoneFociCreated = FALSE;

  if ( _iteration._unitsInZones->len > 0 )
  {
    g_ptr_array_free( _iteration._unitsInZones, TRUE );
    _iteration._unitsInZones = g_ptr_array_new();
  };

  /*  clear_unit_zones_list( _iteration._unitsInZones );  */


  write_outIteration_SQL( _run );

#if DEBUG
  g_debug ("----- EXIT sc_iteration_start");
#endif
}

void sc_day_start( GPtrArray *_production_types )
{
  int i;
  PRT_production_type_data_t *p_data;
#if DEBUG
  g_debug ("----- ENTER sc_day_start");
#endif

  if ( _production_types != NULL )
  {
    for( i = 0; i < _production_types->len; i++ )
    {
      p_data = (PRT_production_type_data_t*)(g_ptr_array_index (_production_types, i ));
      if ( p_data != NULL )
      {
        CLEAR_PRT_DAILY_DATA( &(p_data->d_data) );
      };
    };
  };
#if DEBUG
  g_debug ("----- EXIT sc_day_start");
#endif
}

void sc_iteration_complete( ZON_zone_list_t *_zones, UNT_unit_list_t *_units, GPtrArray *_production_types, unsigned int _run )
{
  int i;
  ZON_zone_t *_zone;
  UNT_unit_t *_unit;
#if DEBUG
  g_debug ("----- ENTER sc_iteration_complete");
#endif
  write_production_type_list_results_SQL( _production_types, _run );
  /* write_units_ever_infected_SQL( _units ); */
  write_outIterationByZone_SQL( _run, _zones );
  write_outIterationByZoneAndProductiontype_SQL( _run, _zones );
  write_outIterationByHerd_SQL( _run, _units );
  update_outIteration_SQL( _run );  
  fflush(NULL);

#if DEBUG
  g_debug ("----- EXIT sc_iteration_complete");
#endif
}

void sc_sim_start( UNT_unit_list_t *units, GPtrArray *production_types, ZON_zone_list_t *zones )
{
  _scenario.start_time = time( NULL );
  _iteration.zoneFociCreated = FALSE;
  _iteration._unitsInZones = g_ptr_array_new();

  write_scenario_SQL();  
  write_job_SQL();
  write_production_types_SQL( production_types );
  write_zones_SQL( zones );
  write_dyn_unit_SQL( units );

  fflush(NULL);  
}

void sc_sim_complete( int _status, UNT_unit_list_t *units, GPtrArray *production_types, ZON_zone_list_t *zones )
{
 char startDay[50];
 char stopDay[50];
 struct tm *local_time;
#if DEBUG
  g_debug ("----- ENTER sc_sim_complete");
#endif
  _scenario.end_time = time( NULL );

 local_time = localtime( &_scenario.start_time );
 sprintf( startDay, "%04d%02d%02d%02d%02d%02d", local_time->tm_year + 1900, local_time->tm_mon + 1, 
		  local_time->tm_mday, local_time->tm_hour, local_time->tm_min, local_time->tm_sec );
  
 local_time = localtime( &_scenario.end_time );  
 sprintf( stopDay, "%04d%02d%02d%02d%02d%02d", local_time->tm_year + 1900, local_time->tm_mon + 1, 
		  local_time->tm_mday, local_time->tm_hour, local_time->tm_min, local_time->tm_sec );
  
 startDay[ strlen( startDay )] = '\0';
 stopDay[ strlen( stopDay )] = '\0';

 update_dyn_unit_SQL( units ) ;
  
  if ( -1 == _status )    /*  normal completion */
  {
    g_print("INSERT INTO outGeneral ( jobID, outGeneralID, simulationStartTime, simulationEndTime, completedIterations, version, lastUpdated ) VALUES ( %s, '%s', '%s', '%s', %lu, '%s', '%s');\n",
             _scenario.scenarioId, _scenario.scenarioId, startDay, stopDay,
             _scenario.iterations_completed, _scenario.version,
             stopDay );
  };

  g_print( "UPDATE scenario set isComplete=%s, lastUpdated='%s' WHERE scenarioID=%s;\n",
           ((_status == -1 )? "TRUE":"FALSE"), stopDay,
           _scenario.scenarioId );

#if DEBUG
  g_debug ("----- EXIT sc_sim_complete");
#endif
}


void sc_disease_end( int _day )
{

#if DEBUG
  g_debug ("----- ENTER sc_disease_end");
#endif
  if ( -1 == _iteration.diseaseEndDay )
    _iteration.diseaseEndDay = _day;

#if DEBUG
  g_debug ("----- EXIT sc_disease_end");
#endif
}


void sc_outbreak_end( int _day )
{

#if DEBUG
  g_debug ("----- ENTER sc_outbreak_end");
#endif
  if ( -1 == _iteration.outbreakEndDay )
    _iteration.outbreakEndDay = _day;

#if DEBUG
  g_debug ("----- EXIT sc_outbreak_end");
#endif
}


void sc_record_zone_area ( unsigned short int _day, ZON_zone_t *_zone )
{

#if DEBUG
  g_debug ("----- ENTER sc_record_zone_area");
#endif
  if ( _zone->max_area < _zone->area )
  {
    _zone->max_area = _zone->area;
    _zone->max_day = _day;
  };

#if DEBUG
  g_debug ("----- EXIT sc_record_zone_area");
#endif
}

void sc_record_zone_change( UNT_unit_t *_unit, ZON_zone_t *_zone )
{
#if DEBUG
  g_debug ("----- ENTER sc_record_zone_change");
#endif
    /* Set the _unit to be in this Zone */
    if ( _zone == NULL )
      g_critical ("----- sc_record_zone_change:  _zone is NULL !!");

    _unit->zone = _zone;

    /*  This is faster than iterating over the list ourselves to find if
    *  this unit was already included in this current list....just remove it
    *  and then add it.
    */
    g_ptr_array_remove ( _iteration._unitsInZones, _unit );
    g_ptr_array_add( _iteration._unitsInZones, _unit );

#if DEBUG
  g_debug ("----- EXIT sc_record_zone_change");
#endif
}

void sc_day_complete( guint _day, guint _run, GPtrArray *_production_types, ZON_zone_list_t * _zones )
{
  guint i, list_len, _prod_type;
  UNT_unit_t *_unit;
  ZON_zone_t *_zone;

#if DEBUG && defined( USE_MPI ) && !CANCEL_MPI
double s_start_time = MPI_Wtime();
double s_end_time = s_start_time;
#endif

#if DEBUG
  g_debug ("----- ENTER sc_day_complete");
#endif
  
  list_len = _iteration._unitsInZones->len;
  /* Update the number of units and animals of each production type in each zone */
  for ( i = 0; i < list_len; i++ )
  {
    _unit = (UNT_unit_t *)g_ptr_array_index( _iteration._unitsInZones, i );
    if ( _unit != NULL )
    {
      _zone = _unit->zone;
      _prod_type = ((PRT_production_type_data_t *)g_ptr_array_index( _unit->production_types, _unit->production_type ))->id;
      addToZoneTotals( _day, _zone, _prod_type, _unit->size );
    }
    else
    {
      g_critical( "----- sc_day_complete:  NULL Herd pointer found in _iteration._unitInZones list, at index %i !", i);
    }
  };

  /* Output the daily totals for epi curve table */
  write_epi_curve_daily_data_SQL( _production_types, _run, _day );
  write_out_daily_by_production_type_SQL( _day, _run, _production_types );
  write_outDailyByZone_SQL( _day, _run, _zones );
  fflush(NULL);

#if DEBUG
  g_debug ("----- EXIT sc_day_complete");
#endif

#if DEBUG && defined( USE_MPI ) && !CANCEL_MPI
  s_end_time = MPI_Wtime();
  g_debug( "sc_day_complete:  took %g seconds\n", (double)(s_end_time - s_start_time) );
#endif
}

void clear_unit_zones_list( GPtrArray *_unitsInZones )
{
  unsigned int i;
#if DEBUG
  g_debug ("----- ENTER clear_unit_zones_list");
#endif

  if ( _unitsInZones != NULL )
  {
    if ( _unitsInZones->len > 0 )
      g_ptr_array_remove_range( _unitsInZones, 0, _unitsInZones->len );
  };

#if DEBUG
  g_debug ("----- EXIT clear_unit_zones_list");
#endif
}
#endif

