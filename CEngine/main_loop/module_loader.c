/** @file module_loader.c
 * Functions for instantiating simulator modules.
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

#include "module_loader.h"
#include "gis.h"
#include "reporting.h"

#if STDC_HEADERS
#  include <string.h>
#elif HAVE_STRINGS_H
#  include <strings.h>
#endif

#if HAVE_UNISTD_H
#  include <unistd.h>
#endif

#if HAVE_ERRNO_H
#  include <errno.h>
#endif

#include "airborne_spread_model.h"
#include "apparent_events_table_writer.h"
#include "basic_destruction_model.h"
#include "basic_zone_focus_model.h"
#include "contact_recorder_model.h"
#include "contact_spread_model.h"
#include "destruction_monitor.h"
#include "destruction_list_monitor.h"
#include "detection_model.h"
#include "detection_monitor.h"
#include "disease_model.h"
#include "economic_model.h"
#include "exam_monitor.h"
#include "exposure_monitor.h"
#include "exposures_table_writer.h"
#include "full_table_writer.h"
#include "infection_monitor.h"
#include "population_model.h"
#include "quarantine_model.h"
#include "resources_and_implementation_of_controls_model.h"
#include "ring_destruction_model.h"
#include "ring_vaccination_model.h"
#include "state_table_writer.h"
#include "summary_gis_writer.h"
#include "table_writer.h"
#include "test_model.h"
#include "test_monitor.h"
#include "trace_destruction_model.h"
#include "trace_exam_model.h"
#include "trace_model.h"
#include "trace_monitor.h"
#include "trace_quarantine_model.h"
#include "trace_zone_focus_model.h"
#include "unit_state_monitor.h"
#include "vaccination_monitor.h"
#include "vaccination_list_monitor.h"
#include "vaccine_model.h"
#include "weekly_gis_writer.h"
#include "zone_model.h"
#include "zone_monitor.h"

#include "adsm.h"



/**
 * Extracts the premature exit condition for the simulation.
 *
 * @param exit_condition_text a text string describing the early exit condition.
 * @return exit condition.
 */
unsigned int
get_exit_condition (char *exit_condition_text)
{
  unsigned int ret_val = STOP_NORMAL;
  
  if (exit_condition_text != NULL)
    {
      if (g_ascii_strcasecmp (exit_condition_text, "disease-end") == 0)
        ret_val = ret_val | STOP_ON_DISEASE_END;

      else if (g_ascii_strcasecmp (exit_condition_text, "first-detection") == 0)
        ret_val = ret_val | STOP_ON_FIRST_DETECTION;
    }
    /** TODO implement options: "outbreak-end",  "'stop-days"*/
  
  return ret_val;
}



/**
 * Instantiates a set of modules based on information in a scenario database.
 *
 * @param scenario_db a connection to the scenario database.
 * @param units a list of units.
 * @param projection the map projection used to convert the units from latitude
 *   and longitude and x and y.
 * @param zones a list of zones.  This can be empty at first, as it may be
 *   populated while reading the parameters.
 * @param ndays a location in which to store the number of days the simulation
 *   lasts.
 * @param nruns a location in which to store the number of Monte Carlo runs of
 *   the simulation.
 * @param models a location in which to store the address of the array of
 *   pointers to models.
 * @param outputs a list of output variables to report.
 * @param _exit_conditions a location in which to store a set of flags
 *   (combined with bitwise-or) specifying when the simulation should end
 *   (e.g., at the first detection, or when all disease is gone).
 * @return the number of models loaded.
 */
int
adsm_load_modules (sqlite3 *scenario_db, UNT_unit_list_t * units,
                   projPJ projection, ZON_zone_list_t * zones,
                   unsigned int *ndays, unsigned int *nruns,
                   adsm_module_t *** models, GPtrArray * outputs,
                   guint *_exit_conditions )
{
  GPtrArray *tmp_models;
  adsm_module_t *model;
  gboolean disable_all_controls;
  gboolean include_zones;
  gboolean include_detection;
  gboolean include_tracing;
  gboolean include_exams;
  gboolean include_testing;
  gboolean include_vaccination;
  gboolean include_destruction;
  gboolean include_economic;
  int nmodels;
  int i;                        /* loop counter */
  unsigned int nzones;
#if DEBUG
  char *s;
#endif

#if DEBUG
  g_debug ("----- ENTER adsm_load_models");
#endif

  *ndays = (unsigned int) PAR_get_int (scenario_db, "SELECT days FROM ScenarioCreator_outputsettings");
  *nruns = (unsigned int) PAR_get_int (scenario_db, "SELECT iterations FROM ScenarioCreator_outputsettings");
  
  /*  This isn't a mandatory parameter.  If this field is NULL, the default is
      STOP_NORMAL. */
  *_exit_conditions = get_exit_condition (PAR_get_text (scenario_db, "SELECT stop_criteria FROM ScenarioCreator_outputsettings"));

  /* Instantiate modules based on which features are active in the scenario. */
  tmp_models = g_ptr_array_new();

  if (PAR_get_int (scenario_db, "SELECT COUNT(*) FROM ScenarioCreator_diseaseprogressionassignment") >= 1)
    {
      g_ptr_array_add (tmp_models,
                       disease_model_new (scenario_db, units, projection, zones));
    }

  if (PAR_get_boolean (scenario_db, "SELECT include_airborne_spread FROM ScenarioCreator_disease"))
    {
      g_ptr_array_add (tmp_models,
                       airborne_spread_model_new (scenario_db, units, projection, zones));
    }

  disable_all_controls = PAR_get_boolean (scenario_db, "SELECT disable_all_controls FROM ScenarioCreator_controlmasterplan");

  include_zones = (!disable_all_controls) && (PAR_get_int (scenario_db, "SELECT COUNT(*) FROM ScenarioCreator_zone") >= 1);
  if (include_zones)
    {
      g_ptr_array_add (tmp_models,
                       zone_model_new (scenario_db, units, projection, zones));
    }

  if (PAR_get_boolean (scenario_db, "SELECT include_contact_spread FROM ScenarioCreator_disease"))
    {
      g_ptr_array_add (tmp_models,
                       contact_spread_model_new (scenario_db, units, projection, zones));
    }

  include_detection = (!disable_all_controls) && (PAR_get_int (scenario_db, "SELECT COUNT(*) FROM ScenarioCreator_controlprotocol protocol,ScenarioCreator_protocolassignment assignment WHERE assignment.control_protocol_id=protocol.id AND use_detection=1") >= 1);
  if (include_detection)
    {
      g_ptr_array_add (tmp_models,
                       detection_model_new (scenario_db, units, projection, zones));
      g_ptr_array_add (tmp_models,
                       quarantine_model_new (scenario_db, units, projection, zones));
    }

  if (include_zones && include_detection)
    {
      g_ptr_array_add (tmp_models,
                       basic_zone_focus_model_new (scenario_db, units, projection, zones));
    }

  include_tracing = (!disable_all_controls) && (PAR_get_int (scenario_db, "SELECT COUNT(*) FROM ScenarioCreator_controlprotocol protocol,ScenarioCreator_protocolassignment assignment WHERE assignment.control_protocol_id=protocol.id AND use_tracing=1") >= 1);
  if (include_tracing)
    {
      g_ptr_array_add (tmp_models,
                       contact_recorder_model_new (scenario_db, units, projection, zones));
      g_ptr_array_add (tmp_models,
                       trace_model_new (scenario_db, units, projection, zones));
      g_ptr_array_add (tmp_models,
                       trace_quarantine_model_new (scenario_db, units, projection, zones));
    }

  if (include_zones && include_tracing)
    {
      g_ptr_array_add (tmp_models,
                       trace_zone_focus_model_new (scenario_db, units, projection, zones));
    }

  include_exams = (!disable_all_controls) && (PAR_get_int (scenario_db, "SELECT COUNT(*) FROM ScenarioCreator_controlprotocol protocol,ScenarioCreator_protocolassignment assignment WHERE assignment.control_protocol_id=protocol.id AND (examine_direct_back_traces=1 OR examine_direct_forward_traces=1 OR examine_indirect_back_traces=1 OR examine_indirect_forward_traces = 1)") >= 1);
  if (include_exams)
    {
      g_ptr_array_add (tmp_models,
                       trace_exam_model_new (scenario_db, units, projection, zones));
    }

  include_testing = (!disable_all_controls) && (PAR_get_int (scenario_db, "SELECT COUNT(*) FROM ScenarioCreator_controlprotocol protocol,ScenarioCreator_protocolassignment assignment WHERE assignment.control_protocol_id=protocol.id AND use_testing=1") >= 1);
  if (include_testing)
    {
      g_ptr_array_add (tmp_models,
                       test_model_new (scenario_db, units, projection, zones));
    }

  include_vaccination = (!disable_all_controls) && (PAR_get_int (scenario_db, "SELECT COUNT(*) FROM ScenarioCreator_controlprotocol protocol,ScenarioCreator_protocolassignment assignment WHERE assignment.control_protocol_id=protocol.id AND vaccine_immune_period_id IS NOT NULL") >= 1);
  if (include_vaccination)
    {
      g_ptr_array_add (tmp_models,
                       vaccine_model_new (scenario_db, units, projection, zones));
      g_ptr_array_add (tmp_models,
                       ring_vaccination_model_new (scenario_db, units, projection, zones));
    }

  include_destruction = (!disable_all_controls) && (PAR_get_int (scenario_db, "SELECT COUNT(*) FROM ScenarioCreator_controlprotocol protocol,ScenarioCreator_protocolassignment assignment WHERE assignment.control_protocol_id=protocol.id AND (use_destruction=1 OR destruction_is_a_ring_target=1 OR destroy_direct_back_traces=1 OR destroy_direct_forward_traces=1 OR destroy_indirect_back_traces=1 OR destroy_indirect_forward_traces=1)") >= 1);
  if (include_destruction)
    {
      g_ptr_array_add (tmp_models,
                       basic_destruction_model_new (scenario_db, units, projection, zones));
      g_ptr_array_add (tmp_models,
                       ring_destruction_model_new (scenario_db, units, projection, zones));
    }

  if (include_tracing && include_destruction)
    {
      g_ptr_array_add (tmp_models,
                       trace_destruction_model_new (scenario_db, units, projection, zones));
    }

  if (include_detection || include_vaccination || include_destruction)
    {
      g_ptr_array_add (tmp_models,
                       resources_and_implementation_of_controls_model_new (scenario_db, units, projection, zones));
    }

  /* Main output, the table of output variable values. */
  g_ptr_array_add (tmp_models,
                   full_table_writer_new (scenario_db, units, projection, zones));
  g_ptr_array_add (tmp_models,
                   unit_state_monitor_new (scenario_db, units, projection, zones));
  g_ptr_array_add (tmp_models,
                   exposure_monitor_new (scenario_db, units, projection, zones));
  g_ptr_array_add (tmp_models,
                   infection_monitor_new (scenario_db, units, projection, zones));
  g_ptr_array_add (tmp_models,
                   destruction_monitor_new (scenario_db, units, projection, zones));
  g_ptr_array_add (tmp_models,
                   destruction_list_monitor_new (scenario_db, units, projection, zones));
  g_ptr_array_add (tmp_models,
                   zone_monitor_new (scenario_db, units, projection, zones));
  if (include_detection)
    {
      g_ptr_array_add (tmp_models,
                       detection_monitor_new (scenario_db, units, projection, zones));
      g_ptr_array_add (tmp_models,
                       trace_monitor_new (scenario_db, units, projection, zones));
    }
  if (include_exams)
    {
      g_ptr_array_add (tmp_models,
                       exam_monitor_new (scenario_db, units, projection, zones));
    }
  if (include_testing)
    {
      g_ptr_array_add (tmp_models,
                       test_monitor_new (scenario_db, units, projection, zones));
    }
  if (include_vaccination)
    {
      g_ptr_array_add (tmp_models,
                       vaccination_monitor_new (scenario_db, units, projection, zones));
      g_ptr_array_add (tmp_models,
                       vaccination_list_monitor_new (scenario_db, units, projection, zones));
    }

  include_economic = PAR_get_boolean (scenario_db, "SELECT (cost_track_zone_surveillance=1 OR cost_track_vaccination=1 OR cost_track_destruction=1) FROM ScenarioCreator_outputsettings");
  if (include_economic)
    {
      g_ptr_array_add (tmp_models,
                       economic_model_new (scenario_db, units, projection, zones));
    }

  /* Supplemental outputs. */
  if (PAR_get_boolean (scenario_db, "SELECT (save_daily_unit_states=1) FROM ScenarioCreator_outputsettings"))
    {
      g_ptr_array_add (tmp_models,
                       state_table_writer_new (scenario_db, units, projection, zones));
    }
  if (PAR_get_boolean (scenario_db, "SELECT (save_daily_exposures=1) FROM ScenarioCreator_outputsettings"))
    {
      g_ptr_array_add (tmp_models,
                       exposures_table_writer_new (scenario_db, units, projection, zones));
    }
  if (PAR_get_boolean (scenario_db, "SELECT (save_daily_events=1) FROM ScenarioCreator_outputsettings"))
    {
      g_ptr_array_add (tmp_models,
                       apparent_events_table_writer_new (scenario_db, units, projection, zones));
    }
  if (PAR_get_boolean (scenario_db, "SELECT (save_map_output=1) FROM ScenarioCreator_outputsettings"))
    {
      g_ptr_array_add (tmp_models,
                       weekly_gis_writer_new (scenario_db, units, projection, zones));
      g_ptr_array_add (tmp_models,
                       summary_gis_writer_new (scenario_db, units, projection, zones));
    }

  /* Population model is always added. */
  g_ptr_array_add (tmp_models, population_model_new (NULL, units, projection, zones));

  #if DEBUG
    for (i = 0; i < tmp_models->len; i++)
      {
        model = g_ptr_array_index (tmp_models, i);
        s = model->to_string (model);
        g_debug ("%s", s);
        g_free (s);
      }
  #endif

  /* Make sure the zones' surveillance level numbers start at 1 and are
   * consecutive, because we're going to use them as list indices later. */
  nzones = ZON_zone_list_length (zones);
  for (i = 0; i < nzones; i++)
    ZON_zone_list_get (zones, i)->level = i + 1;

#if DEBUG
  g_debug ("final number of zones = %u", nzones);
  s = ZON_zone_list_to_string (zones);
  g_debug ("final zone list =\n%s", s);
  g_free (s);
  g_debug ("zone operations %s use R-tree", zones->use_rtree_index ? "will" : "will not");
#endif

#if DEBUG
  g_debug ("----- EXIT adsm_load_models");
#endif

  /* The caller wants just the array of pointers to models. Discard the
   * GPtrArray objects that wraps that array. */
  nmodels = tmp_models->len;
  *models = (adsm_module_t **) (tmp_models->pdata);
  g_ptr_array_free (tmp_models, /* free_seg = */ FALSE);

  return nmodels;
}



/**
 * Frees all memory and resources used by a set of modules.
 *
 * @param nmodels the number of models.
 * @param models an array of models.
 */
void
adsm_unload_modules (int nmodels, adsm_module_t ** models)
{
  adsm_module_t *model;
  int i;                        /* loop counter */

#if DEBUG
  g_debug ("----- ENTER adsm_unload_models");
#endif

  /* Free each model. */
  for (i = 0; i < nmodels; i++)
    {
      model = models[i];
      model->free (model);
    }
  g_free (models);

#if DEBUG
  g_debug ("----- EXIT adsm_unload_models");
#endif
}

/* end of file module_loader.c */
