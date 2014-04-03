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
#include "conflict_resolver.h"
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
#include "vaccination_monitor.h"
#include "vaccination_list_monitor.h"
#include "vaccine_model.h"
#include "weekly_gis_writer.h"
#include "zone_model.h"
#include "zone_monitor.h"

#include "spreadmodel.h"



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
      if (g_ascii_strcasecmp (exit_condition_text, "diseaseEnd") == 0)
        ret_val = ret_val | STOP_ON_DISEASE_END;

      else if (g_ascii_strcasecmp (exit_condition_text, "firstDetection") == 0)
        ret_val = ret_val | STOP_ON_FIRST_DETECTION;
    }
  
  return ret_val;
}



/**
 * Instantiates a set of modules based on information in a parameter database.
 *
 * @param parameter_db a connection to the parameter database.
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
 * @param outputs a list of output variables to report.  Their names should
 *   correspond to output elements in the parameter file.
 * @param _exit_conditions a location in which to store a set of flags
 *   (combined with bitwise-or) specifying when the simulation should end
 *   (e.g., at the first detection, or when all disease is gone).
 * @return the number of models loaded.
 */
int
spreadmodel_load_modules (sqlite3 *parameter_db, UNT_unit_list_t * units,
                          projPJ projection, ZON_zone_list_t * zones,
                          unsigned int *ndays, unsigned int *nruns,
                          spreadmodel_model_t *** models, GPtrArray * outputs,
                          guint *_exit_conditions )
{
  GPtrArray *tmp_models;
  const char *model_name;       /* name of a model */
  GHashTable *singletons;       /* stores the "singleton" modules (for which
                                   there can be only one instance).  Keys are
                                   model names (char *) and data are pointers
                                   to models. */
  spreadmodel_model_new_t model_instantiation_fn;
  spreadmodel_model_t *model;
  gboolean include_zones;
  gboolean include_detection;
  gboolean include_tracing;
  gboolean include_exams;
  gboolean include_testing;
  gboolean include_vaccination;
  gboolean include_destruction;
  int nmodels;
  int i;                        /* loop counter */
  const XML_Char *variable_name;
  unsigned int nzones;
#if DEBUG
  char *s;
#endif

#if DEBUG
  g_debug ("----- ENTER spreadmodel_load_models");
#endif

  *ndays = (unsigned int) PAR_get_int (parameter_db, "SELECT days FROM ScenarioCreator_outputsettings");
  *nruns = (unsigned int) PAR_get_int (parameter_db, "SELECT iterations FROM ScenarioCreator_outputsettings");
  
  /*  This isn't a mandatory parameter.  If this field is NULL, the default is
      STOP_NORMAL. */
  *_exit_conditions = get_exit_condition (PAR_get_text (parameter_db, "SELECT early_stop_criteria FROM ScenarioCreator_outputsettings"));

  singletons = g_hash_table_new (g_str_hash, g_str_equal);

  /* Instantiate modules based on which features are active in the scenario. */
  tmp_models = g_ptr_array_new();

  if (PAR_get_int (parameter_db, "SELECT COUNT(*) FROM ScenarioCreator_diseasereactionassignment") >= 1)
    {
      g_ptr_array_add (tmp_models,
                       disease_model_new (parameter_db, units, projection, zones));
    }

  if (PAR_get_boolean (parameter_db, "SELECT include_airborne_spread FROM ScenarioCreator_scenario"))
    {
      g_ptr_array_add (tmp_models,
                       airborne_spread_model_new (parameter_db, units, projection, zones));
    }

  include_zones = PAR_get_boolean (parameter_db, "SELECT _include_zones FROM ScenarioCreator_controlmasterplan");
  if (include_zones)
    {
      g_ptr_array_add (tmp_models,
                       zone_model_new (parameter_db, units, projection, zones));
    }

  if (PAR_get_boolean (parameter_db, "SELECT include_contact_spread FROM ScenarioCreator_scenario"))
    {
      g_ptr_array_add (tmp_models,
                       contact_spread_model_new (parameter_db, units, projection, zones));
    }

  include_detection = PAR_get_boolean (parameter_db, "SELECT _include_detection FROM ScenarioCreator_controlmasterplan");
  if (include_detection)
    {
      g_ptr_array_add (tmp_models,
                       detection_model_new (parameter_db, units, projection, zones));
      g_ptr_array_add (tmp_models,
                       quarantine_model_new (parameter_db, units, projection, zones));
    }

  if (include_zones && include_detection)
    {
      g_ptr_array_add (tmp_models,
                       basic_zone_focus_model_new (parameter_db, units, projection, zones));
    }

  include_tracing = PAR_get_boolean (parameter_db, "SELECT _include_tracing FROM ScenarioCreator_controlmasterplan");
  if (include_tracing)
    {
      g_ptr_array_add (tmp_models,
                       contact_recorder_model_new (parameter_db, units, projection, zones));
      g_ptr_array_add (tmp_models,
                       trace_model_new (parameter_db, units, projection, zones));
      g_ptr_array_add (tmp_models,
                       trace_quarantine_model_new (parameter_db, units, projection, zones));
    }

  if (include_zones && include_tracing)
    {
      g_ptr_array_add (tmp_models,
                       trace_zone_focus_model_new (parameter_db, units, projection, zones));
    }

  include_exams = PAR_get_boolean (parameter_db, "SELECT _include_tracing_unit_exam FROM ScenarioCreator_controlmasterplan");
  if (include_exams)
    {
      g_ptr_array_add (tmp_models,
                       trace_exam_model_new (parameter_db, units, projection, zones));
    }

  include_testing = PAR_get_boolean (parameter_db, "SELECT _include_tracing_testing FROM ScenarioCreator_controlmasterplan");
  if (include_testing)
    {
      g_ptr_array_add (tmp_models,
                       test_model_new (parameter_db, units, projection, zones));
    }

  include_vaccination = PAR_get_boolean (parameter_db, "SELECT _include_vaccination FROM ScenarioCreator_controlmasterplan");
  if (include_vaccination)
    {
      g_ptr_array_add (tmp_models,
                       vaccine_model_new (parameter_db, units, projection, zones));
      g_ptr_array_add (tmp_models,
                       ring_vaccination_model_new (parameter_db, units, projection, zones));
    }

  include_destruction = PAR_get_boolean (parameter_db, "SELECT _include_destruction FROM ScenarioCreator_controlmasterplan");
  if (include_destruction)
    {
      g_ptr_array_add (tmp_models,
                       basic_destruction_model_new (parameter_db, units, projection, zones));
      g_ptr_array_add (tmp_models,
                       ring_destruction_model_new (parameter_db, units, projection, zones));
    }

  if (include_tracing && include_destruction)
    {
      g_ptr_array_add (tmp_models,
                       trace_destruction_model_new (parameter_db, units, projection, zones));
    }

  if (include_vaccination || include_destruction)
    {
      g_ptr_array_add (tmp_models,
                       resources_and_implementation_of_controls_model_new (parameter_db, units, projection, zones));
    }
  
  if (PAR_get_boolean (parameter_db, "SELECT daily_states_filename IS NOT NULL FROM ScenarioCreator_outputsettings"))
    {
      g_ptr_array_add (tmp_models,
                       state_table_writer_new (parameter_db, units, projection, zones));
    }

  /* Conflict resolver is always added. */
  g_ptr_array_add (tmp_models, conflict_resolver_new (NULL, units, projection, zones));

  #if DEBUG
    for (i = 0; i < tmp_models->len; i++)
      {
        model = g_ptr_array_index (tmp_models, i);
        s = model->to_string (model);
        g_debug ("%s", s);
        g_free (s);
      }
  #endif

  if (FALSE)
    {
      /* If there is already an instance of this kind of module, and this kind
       * of module is a "singleton" module (only one instance of it can exist),
       * then pass the parameters to the existing instance.  Otherwise, create
       * a new instance. */
      model = g_hash_table_lookup (singletons, model_name);
      if (model != NULL)
        {
          #if DEBUG
            g_debug ("adding parameters to existing instance");
          #endif
          model->set_params (model, NULL);
        }
      else
        {
          /* Get the module's "new" function (to instantiate a model object). */

          #if DEBUG
            g_debug ("\"new\" function = <%p>", model_instantiation_fn);
          #endif

          if (model->is_singleton)
            g_hash_table_insert (singletons, (gpointer) model_name, (gpointer) model);

        } /* end of case where a new model instance is created */

    }                           /* end of loop over models */

  /* We can free the hash table structure without freeing the keys (because the
   * keys are model names, which are static strings) or the values (because the
   * values are model instances, which persist after this function ends). */
  g_hash_table_destroy (singletons);

  /* If table output is turned on, set the reporting frequency for the output
   * variables. */
  if (FALSE)
    {
      if (strcmp (variable_name, "num-units-in-each-state") == 0)
        variable_name = "tsdU";
      else if (strcmp (variable_name, "num-animals-in-each-state") == 0)
        variable_name = "tsdA";
      else if (strcmp (variable_name, "time-to-end-of-outbreak") == 0)
        variable_name = "outbreakDuration";
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
  g_debug ("----- EXIT spreadmodel_load_models");
#endif

  /* The caller wants just the array of pointers to models. Discard the
   * GPtrArray objects that wraps that array. */
  nmodels = tmp_models->len;
  *models = (spreadmodel_model_t **) (tmp_models->pdata);
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
spreadmodel_unload_modules (int nmodels, spreadmodel_model_t ** models)
{
  spreadmodel_model_t *model;
  int i;                        /* loop counter */

#if DEBUG
  g_debug ("----- ENTER spreadmodel_unload_models");
#endif

  /* Free each model. */
  for (i = 0; i < nmodels; i++)
    {
      model = models[i];
      model->free (model);
    }
  g_free (models);

#if DEBUG
  g_debug ("----- EXIT spreadmodel_unload_models");
#endif
}

/* end of file module_loader.c */
