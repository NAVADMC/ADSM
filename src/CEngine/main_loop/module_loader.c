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
#  include "config.h"
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
#include "number_of_detections_vaccination_trigger.h"
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
 * @param error a location in which an error can be placed.
 * @return the number of models loaded.
 */
int
adsm_load_modules (sqlite3 *scenario_db, UNT_unit_list_t * units,
                   projPJ projection, ZON_zone_list_t * zones,
                   unsigned int *ndays, unsigned int *nruns,
                   adsm_module_t *** models, GPtrArray * outputs,
                   guint *_exit_conditions,
                   GError **error)
{
  GPtrArray *instantiation_fns;
  gboolean instantiation_failures;
  GError *instantiation_error = NULL;
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
  adsm_module_t *model;
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

  /* Modules will be instantiated based on which features are active in the
   * scenario. Start by gathering a list of function pointers for the
   * instantiation functions. */
  instantiation_fns = g_ptr_array_new();

  if (PAR_get_int (scenario_db, "SELECT COUNT(*) FROM ScenarioCreator_diseaseprogressionassignment") >= 1)
    {
      g_ptr_array_add (instantiation_fns, disease_model_new);
    }

  if (PAR_get_boolean (scenario_db, "SELECT include_airborne_spread FROM ScenarioCreator_disease"))
    {
      g_ptr_array_add (instantiation_fns, airborne_spread_model_new);
    }

  disable_all_controls = PAR_get_boolean (scenario_db, "SELECT disable_all_controls FROM ScenarioCreator_controlmasterplan");

  /* Instantiate the zone module even if disable_all_controls is true. This
   * prevents dangling references when there are movement control charts,
   * detection multipliers, etc. attached to zones. */
  include_zones = (PAR_get_int (scenario_db, "SELECT COUNT(*) FROM ScenarioCreator_zone") >= 1);
  if (include_zones)
    {
      g_ptr_array_add (instantiation_fns, zone_model_new);
    }
  /* But now we set include_zones to false if disable_all_controls is true.
   * In the code below, this will prevent instantiation of any modules that
   * actually trigger zone creation. */
  include_zones = include_zones && (!disable_all_controls);

  if (PAR_get_boolean (scenario_db, "SELECT (include_direct_contact_spread=1 OR include_indirect_contact_spread=1) FROM ScenarioCreator_disease"))
    {
      g_ptr_array_add (instantiation_fns, contact_spread_model_new);
    }

  include_detection = (!disable_all_controls) && (PAR_get_int (scenario_db, "SELECT COUNT(*) FROM ScenarioCreator_controlprotocol protocol,ScenarioCreator_protocolassignment assignment WHERE assignment.control_protocol_id=protocol.id AND use_detection=1") >= 1);
  if (include_detection)
    {
      g_ptr_array_add (instantiation_fns, detection_model_new);
      g_ptr_array_add (instantiation_fns, quarantine_model_new);
    }

  if (include_zones && include_detection)
    {
      g_ptr_array_add (instantiation_fns, basic_zone_focus_model_new);
    }

  include_tracing = (!disable_all_controls) && (PAR_get_int (scenario_db, "SELECT COUNT(*) FROM ScenarioCreator_controlprotocol protocol,ScenarioCreator_protocolassignment assignment WHERE assignment.control_protocol_id=protocol.id AND use_tracing=1") >= 1);
  if (include_tracing)
    {
      g_ptr_array_add (instantiation_fns, contact_recorder_model_new);
      g_ptr_array_add (instantiation_fns, trace_model_new);
      g_ptr_array_add (instantiation_fns, trace_quarantine_model_new);
    }

  if (include_zones && include_tracing)
    {
      g_ptr_array_add (instantiation_fns, trace_zone_focus_model_new);
    }

  include_exams = (!disable_all_controls) && (PAR_get_int (scenario_db, "SELECT COUNT(*) FROM ScenarioCreator_controlprotocol protocol,ScenarioCreator_protocolassignment assignment WHERE assignment.control_protocol_id=protocol.id AND (examine_direct_back_traces=1 OR examine_direct_forward_traces=1 OR examine_indirect_back_traces=1 OR examine_indirect_forward_traces = 1)") >= 1);
  if (include_exams)
    {
      g_ptr_array_add (instantiation_fns, trace_exam_model_new);
    }

  include_testing = (!disable_all_controls) && (PAR_get_int (scenario_db, "SELECT COUNT(*) FROM ScenarioCreator_controlprotocol protocol,ScenarioCreator_protocolassignment assignment WHERE assignment.control_protocol_id=protocol.id AND use_testing=1") >= 1);
  if (include_testing)
    {
      g_ptr_array_add (instantiation_fns, test_model_new);
    }

  include_vaccination = (!disable_all_controls) && (PAR_get_int (scenario_db, "SELECT COUNT(*) FROM ScenarioCreator_controlprotocol protocol,ScenarioCreator_protocolassignment assignment WHERE assignment.control_protocol_id=protocol.id AND vaccine_immune_period_id IS NOT NULL") >= 1);
  if (include_vaccination)
    {
      g_ptr_array_add (instantiation_fns, vaccine_model_new);
      g_ptr_array_add (instantiation_fns, ring_vaccination_model_new);
      g_ptr_array_add (instantiation_fns, number_of_detections_vaccination_trigger_new);
    }

  include_destruction = (!disable_all_controls) && (PAR_get_int (scenario_db, "SELECT COUNT(*) FROM ScenarioCreator_controlprotocol protocol,ScenarioCreator_protocolassignment assignment WHERE assignment.control_protocol_id=protocol.id AND (use_destruction=1 OR destruction_is_a_ring_target=1 OR destroy_direct_back_traces=1 OR destroy_direct_forward_traces=1 OR destroy_indirect_back_traces=1 OR destroy_indirect_forward_traces=1)") >= 1);
  if (include_destruction)
    {
      g_ptr_array_add (instantiation_fns, basic_destruction_model_new);
      g_ptr_array_add (instantiation_fns, ring_destruction_model_new);
    }

  if (include_tracing && include_destruction)
    {
      g_ptr_array_add (instantiation_fns, trace_destruction_model_new);
    }

  if (include_detection || include_vaccination || include_destruction)
    {
      g_ptr_array_add (instantiation_fns, resources_and_implementation_of_controls_model_new);
    }

  /* Main output, the table of output variable values. */
  g_ptr_array_add (instantiation_fns, full_table_writer_new);
  g_ptr_array_add (instantiation_fns, unit_state_monitor_new);
  g_ptr_array_add (instantiation_fns, exposure_monitor_new);
  g_ptr_array_add (instantiation_fns, infection_monitor_new);
  g_ptr_array_add (instantiation_fns, destruction_monitor_new);
  g_ptr_array_add (instantiation_fns, destruction_list_monitor_new);
  g_ptr_array_add (instantiation_fns, zone_monitor_new);
  if (include_detection)
    {
      g_ptr_array_add (instantiation_fns, detection_monitor_new);
      g_ptr_array_add (instantiation_fns, trace_monitor_new);
    }
  if (include_exams)
    {
      g_ptr_array_add (instantiation_fns, exam_monitor_new);
    }
  if (include_testing)
    {
      g_ptr_array_add (instantiation_fns, test_monitor_new);
    }
  if (include_vaccination)
    {
      g_ptr_array_add (instantiation_fns, vaccination_monitor_new);
      g_ptr_array_add (instantiation_fns, vaccination_list_monitor_new);
    }

  include_economic = PAR_get_boolean (scenario_db, "SELECT (cost_track_zone_surveillance=1 OR cost_track_vaccination=1 OR cost_track_destruction=1) FROM ScenarioCreator_outputsettings");
  if (include_economic)
    {
      g_ptr_array_add (instantiation_fns, economic_model_new);
    }

  /* Supplemental outputs. */
  if (PAR_get_boolean (scenario_db, "SELECT (save_daily_unit_states=1) FROM ScenarioCreator_outputsettings"))
    {
      g_ptr_array_add (instantiation_fns, state_table_writer_new);
    }
  if (PAR_get_boolean (scenario_db, "SELECT (save_daily_exposures=1) FROM ScenarioCreator_outputsettings"))
    {
      g_ptr_array_add (instantiation_fns, exposures_table_writer_new);
    }
  if (PAR_get_boolean (scenario_db, "SELECT (save_daily_events=1) FROM ScenarioCreator_outputsettings"))
    {
      g_ptr_array_add (instantiation_fns, apparent_events_table_writer_new);
    }
  if (PAR_get_boolean (scenario_db, "SELECT (save_map_output=1) FROM ScenarioCreator_outputsettings"))
    {
      g_ptr_array_add (instantiation_fns, weekly_gis_writer_new);
    }

  /* Population model is always added. */
  g_ptr_array_add (instantiation_fns, population_model_new);

  /* Instantiate the modules. If creation of any of them fails, output a
   * warning. */
  nmodels = instantiation_fns->len;
  *models = g_new (adsm_module_t *, nmodels);
  instantiation_failures = FALSE;
  for (i = 0; i < nmodels; i++)
    {
      adsm_model_new_t instantiation_fn;

      instantiation_fn = g_ptr_array_index (instantiation_fns, i);
      (*models)[i] = instantiation_fn (scenario_db, units, projection, zones, &instantiation_error);
      if (instantiation_error)
        {
          g_warning ("%s", instantiation_error->message);
          g_clear_error (&instantiation_error);
          instantiation_failures = TRUE;
        }
      else
        {
          #if DEBUG
            model = (*models)[i];
            s = model->to_string (model);
            g_debug ("%s", s);
            g_free (s);
          #endif
        }
    }

  if (instantiation_failures)
    {
      g_set_error (error, g_quark_from_string(G_LOG_DOMAIN), 0,
                   "One or more modules could not be initialized");
    }

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
