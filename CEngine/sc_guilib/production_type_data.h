/** @file production_type_data.h
 * Functions for creating, destroying, printing, and manipulating production types.
 *
 * @author Shaun Case <shaun.case@colostate.edu><br>
 *   Animal Population Health Institute<br>
 *   Department of Clinical Sciences, Colorado State University.<br>
 *   Fort Collins, Colorado  80524<br>
 *   USA
 * @version 0.1
 * @date February 2009
 *
 * Copyright &copy; Colorado State University and University of Guelph, Canada, 2003-2009
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 *
 */

#ifndef PRODUCTION_TYPE_DATA_H
#define PRODUCTION_TYPE_DATA_H


#if HAVE_CONFIG_H
#  include <config.h>
#endif

#if STDC_HEADERS
#  include <stdlib.h>
#endif

#ifdef USE_SC_GUILIB

#include <unistd.h>
#include <stdio.h>
#include <zone.h>
#include <unit.h>
#include <expat.h>
/* Expat 1.95 has this constant on my Debian system, but not on Hammerhead's
* Red Hat system.  ?? */
#ifndef XML_STATUS_ERROR
#  define XML_STATUS_ERROR 0
#endif

#include <glib.h>

typedef struct
{
    /*  These are handled by change_unit_state */
    unsigned long tscUSusc;
    unsigned long tscASusc;
    unsigned long tscULat;
    unsigned long tscALat;
    unsigned long tscUSubc;
    unsigned long tscASubc;
    unsigned long tscUClin;
    unsigned long tscAClin;
    unsigned long tscUNImm;
    unsigned long tscANImm;
    unsigned long tscUVImm;
    unsigned long tscAVImm;
    unsigned long tscUDest;
    unsigned long tscADest;

    /*  These are handled by infect_unit */
    unsigned long infcUIni;
    unsigned long infcAIni;
    unsigned long infcUAir;
    unsigned long infcAAir;
    unsigned long infcUDir;
    unsigned long infcADir;
    unsigned long infcUInd;
    unsigned long infcAInd;

    /*  These are handled by expose_unit */
    unsigned long expcUDir;
    unsigned long expcADir;
    unsigned long expcUInd;
    unsigned long expcAInd;

    /*  These are handled by attempt_trace_unit IFF sucess is set to (-1) */
    unsigned long trcUDir;
    unsigned long trcADir;
    unsigned long trcUInd;
    unsigned long trcAInd;

    /*  These are handled by attempt_trace_unit */
    unsigned long trcUDirp;
    unsigned long trcADirp;
    unsigned long trcUIndp;
    unsigned long trcAIndp;

    /*  These are handled by detect_unit */
    unsigned long detcUClin;
    unsigned long detcAClin;
    unsigned long firstDetection;

    /*  These are handled by destroy_unit */
    unsigned long descUIni;
    unsigned long descAIni;
    unsigned long descUDet;
    unsigned long descADet;
    unsigned long descUDir;
    unsigned long descADir;
    unsigned long descUInd;
    unsigned long descAInd;
    unsigned long descURing ;
    unsigned long descARing ;
    unsigned long firstDestruction;

    /*  These are handled by vaccinate_unit */
    unsigned long vaccUIni;
    unsigned long vaccAIni;
    unsigned long vaccURing ;
    unsigned long vaccARing ;
    unsigned long firstVaccination;

    /*  This is handled by make_zone_focus */
    unsigned long zoncFoci;
}
PRT_summary_data;

/*  Daily values */
typedef struct
{
  /**  daily counts for cause of infection */
  unsigned long infnUDir;
  unsigned long infnADir;
  unsigned long infnUAir;
  unsigned long infnAAir;
  unsigned long infnUInd;
  unsigned long infnAInd;

  /*  These are handled by change_unit_state */
  unsigned long tsdUSusc;
  unsigned long tsdASusc;
  unsigned long tsdULat;
  unsigned long tsdALat;
  unsigned long tsdUSubc;
  unsigned long tsdASubc;
  unsigned long tsdUClin;
  unsigned long tsdAClin;
  unsigned long tsdUNImm;
  unsigned long tsdANImm;
  unsigned long tsdUVImm;
  unsigned long tsdAVImm;
  unsigned long tsdUDest;
  unsigned long tsdADest;

  /*  These are handled by attempt_trace_unit IFF sucess is set to (-1) */
  unsigned long trnUDir;
  unsigned long trnADir;
  unsigned long trnUInd;
  unsigned long trnAInd;

  /**  daily counts for detection */
  unsigned long detnUClin;
  unsigned long detnAClin;

  /**  daily counts for destruction handled by destroy_unit*/
  unsigned long desnUAll;
  unsigned long desnAAll;

  /*  These are handled by vaccinate_unit */
  unsigned long vaccUAll;
  unsigned long vaccAAll;

  unsigned long zonnFoci;

  /**  daily counts of apparently infection units */
  unsigned long appUInfectious;
}
PRT_daily_data;

/** A production type structure. */
typedef struct
{
  char *name;             /**  Production Type Name, aka Description in NAADSM_PC */
  unsigned int id;        /**  Original Id from the NAADSM input file */
  PRT_summary_data data;  /** Summary data for a single iteration. */
  PRT_daily_data d_data;  /**  Daily summary data for epidemic curves */
}
PRT_production_type_data_t;

/**
 * A special structure for passing a partially completed production type list to Expat's
 * tag handler functions.
 */
typedef struct
{
  GPtrArray *production_types;
  PRT_production_type_data_t *production_type;
  GString *s; /**< for gathering character data */
  char *filename; /**< for reporting the XML file's name in errors */
  XML_Parser parser; /**< for reporting the line number in errors */
}
PRT_partial_production_type_list_t;

typedef struct{
  guint _run;
  guint _zone_level;
  GHashTable *_animalDays;
} by_zone_prod_data;


#define CLEAR_PRT_SUMMARY_DATA( x )  (memset( x, 0, sizeof( PRT_summary_data ) ))
#define CLEAR_PRT_DAILY_DATA( x )  (memset( x, 0, sizeof( PRT_daily_data ) ))

GPtrArray *PRT_load_production_type_list ( char *production_type_file );

void PRT_free_production_type_list ( GPtrArray * );

PRT_production_type_data_t *PRT_new_production_type_t( char *_name, int _id );

GPtrArray *PRT_load_production_type_list_from_stream (FILE *stream, const char *production_type_file);

void clear_production_type_list_data( GPtrArray *_production_type_list );

#endif
#endif
