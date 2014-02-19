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
#include "airborne_spread_exponential_model.h"
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
#include "test_model.h"
#include "test_monitor.h"
#include "trace_back_destruction_model.h"
#include "trace_back_monitor.h"
#include "trace_back_zone_focus_model.h"
#include "trace_destruction_model.h"
#include "trace_exam_model.h"
#include "trace_model.h"
#include "trace_monitor.h"
#include "trace_quarantine_model.h"
#include "trace_zone_focus_model.h"
#include "vaccination_monitor.h"
#include "vaccination_list_monitor.h"
#include "vaccine_model.h"
#include "zone_model.h"
#include "zone_monitor.h"

#include "spreadmodel.h"



struct model_load_info_t
{
  const char *model_name;
  spreadmodel_model_new_t model_instantiation_fn;
  spreadmodel_model_is_singleton_t model_singleton_fn;
};


struct model_load_info_t model_list[] = {
  {"airborne-spread-model", (void*)&airborne_spread_model_new,
    airborne_spread_model_is_singleton},
  {"airborne-spread-exponential-model", (void*)&airborne_spread_exponential_model_new,
    airborne_spread_exponential_model_is_singleton},
  #ifndef WIN_DLL
    {"apparent-events-table-writer", (void*)&apparent_events_table_writer_new, apparent_events_table_writer_is_singleton},
  #endif
  {"basic-destruction-model", (void*)&basic_destruction_model_new, NULL},
  {"basic-zone-focus-model", (void*)&basic_zone_focus_model_new, NULL},     
  {"conflict-resolver", (void*)&conflict_resolver_new, NULL},
  {"contact-recorder-model", (void*)&contact_recorder_model_new,
    contact_recorder_model_is_singleton},
  {"contact-spread-model", (void*)&contact_spread_model_new, contact_spread_model_is_singleton},
  {"destruction-list-monitor", (void*)&destruction_list_monitor_new, NULL},
  {"destruction-monitor", (void*)&destruction_monitor_new, NULL},
  {"detection-model", (void*)&detection_model_new, detection_model_is_singleton},
  {"detection-monitor", (void*)&detection_monitor_new, NULL},
  {"disease-model", (void*)&disease_model_new, NULL},
  {"economic-model", (void*)&economic_model_new, economic_model_is_singleton},
  {"exam-monitor", (void*)&exam_monitor_new, NULL},
  {"exposure-monitor", (void*)&exposure_monitor_new, NULL},
  #ifndef WIN_DLL
    {"exposures-table-writer", (void*)&exposures_table_writer_new, exposures_table_writer_is_singleton},
  #endif
  #ifndef WIN_DLL
    {"full-table-writer", (void*)&full_table_writer_new, full_table_writer_is_singleton},
  #endif
  {"infection-monitor", (void*)&infection_monitor_new, NULL},
  {"quarantine-model", (void*)&quarantine_model_new, NULL},
  {"resources-and-implementation-of-controls-model",
    (void*)&resources_and_implementation_of_controls_model_new, NULL},
  {"ring-destruction-model", (void*)&ring_destruction_model_new, NULL},
  {"ring-vaccination-model", (void*)&ring_vaccination_model_new, ring_vaccination_model_is_singleton},
  {"test-model", (void*)&test_model_new, NULL},
  {"test-monitor", (void*)&test_monitor_new, NULL},
  {"trace-back-destruction-model", (void*)&trace_back_destruction_model_new, NULL},
  {"trace-back-monitor", (void*)&trace_back_monitor_new, NULL},
  {"trace-back-zone-focus-model", (void*)&trace_back_zone_focus_model_new, NULL},
  {"trace-destruction-model", (void*)&trace_destruction_model_new, NULL},
  {"trace-exam-model", (void*)&trace_exam_model_new, NULL},
  {"trace-model", (void*)&trace_model_new, NULL},
  {"trace-monitor", (void*)&trace_monitor_new, NULL},
  {"trace-quarantine-model", (void*)&trace_quarantine_model_new, NULL},
  {"trace-zone-focus-model", (void*)&trace_zone_focus_model_new, NULL},
  {"vaccination-list-monitor", (void*)&vaccination_list_monitor_new, NULL},
  {"vaccination-monitor", (void*)&vaccination_monitor_new, NULL},
  {"vaccine-model", (void*)&vaccine_model_new, NULL},
  {"zone-model", (void*)&zone_model_new, zone_model_is_singleton},
  {"zone-monitor", (void*)&zone_monitor_new, NULL}    
};

int model_list_count = (sizeof (model_list) / sizeof (struct model_load_info_t));

int
model_name_cmp (const void *c1, const void *c2)
{
  return strcmp (((const struct model_load_info_t *)c1)->model_name,
                 ((const struct model_load_info_t *)c2)->model_name);
}


struct model_load_info_t *
find_model (const char *name)
{
  struct model_load_info_t target;
  target.model_name = name;

  return bsearch (&target, model_list, model_list_count, sizeof (struct model_load_info_t), model_name_cmp      /*AR  "warning: passing arg 5 of `bsearch' from incompatible pointer type" */
    );
}


/**
 * Extracts the premature exit condition for the simulation.
 *
 * @param e a "exit-condition" element from the simulation parameters.
 * @return exit condition.
 */
unsigned int
get_exit_condition (scew_element * e)
{
  unsigned int ret_val = STOP_NORMAL;
  
  if ( e != NULL )
  {
    if ( scew_element_by_name ( e, "disease-end") != NULL )
	  ret_val = ret_val | STOP_ON_DISEASE_END;
	
	if ( scew_element_by_name ( e, "first-detection") != NULL )
	  ret_val = ret_val | STOP_ON_FIRST_DETECTION;	
  };
  
  return ret_val;
}

/**
 * Extracts the number of days the simulation is to last.
 *
 * @param e a "num-days" element from the simulation parameters.
 * @return the number of days.
 */
unsigned int
get_num_days (scew_element * e)
{
  long int tmp;

  tmp = strtol (scew_element_contents (e), NULL, 10);   /* base 10 */
  g_assert (errno != ERANGE && errno != EINVAL);
  return (unsigned int) tmp;
}



/**
 * Extracts the number of Monte Carlo runs for the simulation.
 *
 * @param e a "num-runs" element from the simulation parameters.
 * @return the number of runs.
 */
unsigned int
get_num_runs (scew_element * e)
{
  long int tmp;

  tmp = strtol (scew_element_contents (e), NULL, 10);   /* base 10 */
  g_assert (errno != ERANGE && errno != EINVAL);
  return (unsigned int) tmp;
}



/**
 * Instantiates a set of modules based on information in a parameter file.
 *
 * @param parameter_file name of the parameter file.
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
spreadmodel_load_modules (const char *parameter_file, UNT_unit_list_t * units,
                          projPJ projection, ZON_zone_list_t * zones,
                          unsigned int *ndays, unsigned int *nruns,
                          spreadmodel_model_t *** models, GPtrArray * outputs,
                          guint *_exit_conditions )
{
  scew_reader *reader;          /* to read the parameter file */
  scew_parser *parser;          /* to parse the parameter file */
  scew_error err;               /* parser error code */
  scew_tree *tree;              /* parameter tree */
  scew_element *params;         /* root of the parameter tree */
  scew_element *e;              /* a subtree of the parameter tree */
  scew_list *ee;                /* a list of subtrees */
  scew_list *iter;
  scew_element *model_spec;     /* a subtree for a model */
  const char *model_name;       /* name of a model */
  struct model_load_info_t *model_load_info;
  spreadmodel_model_is_singleton_t model_is_singleton_fn;
  gboolean singleton;
  GHashTable *singletons;       /* stores the "singleton" modules (for which
                                   there can be only one instance).  Keys are
                                   model names (char *) and data are pointers
                                   to models. */
  spreadmodel_model_new_t model_instantiation_fn;
  spreadmodel_model_t *model;
  int nmodels;
  int nloaded = 0;
  int i, j;                     /* loop counters */
  RPT_reporting_t *output;
  const XML_Char *variable_name;
  unsigned int nzones;
#if DEBUG
  char *s;
#endif

#if DEBUG
  g_debug ("----- ENTER spreadmodel_load_models");
#endif

  parser = scew_parser_create ();
  if (parser == NULL)
    return 0;

  /* This test isn't foolproof because the file could be deleted in the split-
   * second before scew_parser_load_file tries to open it. */
  if (g_file_test (parameter_file, G_FILE_TEST_EXISTS) == FALSE)
    {
      g_error ("parameter file \"%s\" not found", parameter_file);
    }

  reader = scew_reader_file_create (parameter_file);
  g_assert (reader != NULL);
  tree = scew_parser_load (parser, reader);
  if (tree == NULL)
    {
      err = scew_error_code ();
      if (err == scew_error_expat)
        g_error ("parameter file \"%s\" could not be parsed: %s on line %i", parameter_file,
                 scew_error_expat_string (scew_error_expat_code (parser)),
                 scew_error_expat_line (parser));
      else
        g_error ("parameter file \"%s\" could not be parsed: %s", parameter_file,
                 scew_error_string (err));
    }
  scew_reader_close (reader);
  scew_reader_free (reader);

  params = scew_tree_root (tree);

  g_assert (params != NULL);

  #if DEBUG
    g_debug ("root has %u children", scew_element_count (params));
    for (i = 0; i < scew_element_count (params); i++)
      g_debug ("child %i name=\"%s\"", i,
               scew_element_name (scew_element_by_index (params, i)));
  #endif

  g_assert (scew_element_by_name (params, "num-days") != NULL);
  *ndays = get_num_days (scew_element_by_name (params, "num-days"));
  g_assert (scew_element_by_name (params, "num-runs") != NULL);
  *nruns = get_num_runs (scew_element_by_name (params, "num-runs"));
  
  /*  This isn't a mandatory parameter.  If this element is NULL, the function
      will return "0" for "no premature exit" */
  *_exit_conditions = get_exit_condition( scew_element_by_name ( params, "exit-condition" ) );

  /* Get the number of sub-models that will run in the simulation. */
  e = scew_element_by_name (params, "models");
  nmodels = (int) scew_element_count (e);

  #if DEBUG
    g_debug ("%i sub-models in parameters", nmodels);
  #endif

  singletons = g_hash_table_new (g_str_hash, g_str_equal);

  /* Instantiate each model. */

  /*AR Just in case the order of model_list should get screwed up by a
   *  forgetful programmer (not that I know anyone like that)...  */
  qsort (model_list, model_list_count, sizeof (struct model_load_info_t), model_name_cmp);

  *models = g_new (spreadmodel_model_t *, nmodels);
  for (i = 0; i < nmodels; i++)
    {
      model_spec = scew_element_by_index (e, (unsigned int) i);
      model_name = scew_element_name (model_spec);
      #if DEBUG
        g_debug ("loading model %i, \"%s\"", i + 1, model_name);
      #endif

      /* Find the model in the array */
      model_load_info = find_model (model_name);

      if (NULL == model_load_info)
        {
          g_warning ("Model %s not found in model list.", model_name);
          continue;
        }
      #if DEBUG
        g_debug ("Model = <%p>", model_load_info);
      #endif

      /* If this is a "singleton" module (only one instance of it can exist),
       * check whether there is already an instance.  If so, pass the
       * parameters to the existing instance.  If not, create a new instance. */
      model_is_singleton_fn = model_load_info->model_singleton_fn;
      singleton = (model_is_singleton_fn != NULL && model_is_singleton_fn () == TRUE);


      #if DEBUG
        g_debug ("module %s a singleton", singleton ? "is" : "is not");
      #endif
      model = NULL;
      if (singleton)
        model = (spreadmodel_model_t *) g_hash_table_lookup (singletons, model_name);

      if (model != NULL)
        {
          /* Send the additional parameters to the already-instantiated
           * model. */
          #if DEBUG
            g_debug ("adding parameters to existing instance");
          #endif
          model->set_params (model, model_spec);
        }
      else
        {
          /* Get the module's "new" function (to instantiate a model object). */
          model_instantiation_fn = model_load_info->model_instantiation_fn;

          #if DEBUG
            g_debug ("\"new\" function = <%p>", model_instantiation_fn);
          #endif

          model = model_instantiation_fn (model_spec, units, projection, zones);

          /* Add the model's output variables to the list of reporting variables. */
          for (j = 0; j < model->outputs->len; j++)
            g_ptr_array_add (outputs, g_ptr_array_index (model->outputs, j));

          (*models)[nloaded++] = model;

          if (singleton)
            g_hash_table_insert (singletons, (gpointer) model_name, (gpointer) model);

        } /* end of case where a new model instance is created */

      #if DEBUG
        s = model->to_string (model);
        g_debug ("%s", s);
        g_free (s);
      #endif
    }                           /* end of loop over models */

  /* We can free the hash table structure without freeing the keys (because the
   * keys are model names, which are static strings) or the values (because the
   * values are model instances, which persist after this function ends). */
  g_hash_table_destroy (singletons);

  /* Set the reporting frequency for the output variables. */
  ee = scew_element_list_by_name (params, "output");
#if DEBUG
  g_debug ("%i output variables", scew_list_size (ee));
#endif
  for (iter = ee; iter != NULL; iter = scew_list_next(iter))
    {
      e = (scew_element *) scew_list_data (iter);
      variable_name = scew_element_contents (scew_element_by_name (e, "variable-name"));
      /* Starting at version 3.2 we accept either the old, verbose output
       * variable names or the new shorter ones.  These lines are a kludge to
       * re-map some of the old names. */
      if (strcmp (variable_name, "num-units-in-each-state") == 0)
        variable_name = "tsdU";
      else if (strcmp (variable_name, "num-animals-in-each-state") == 0)
        variable_name = "tsdA";
      else if (strcmp (variable_name, "time-to-end-of-outbreak") == 0)
        variable_name = "outbreakDuration";

      /* Do the outputs include a variable with this name? */
      for (j = 0; j < outputs->len; j++)
        {
          output = (RPT_reporting_t *) g_ptr_array_index (outputs, j);
          if (strcmp (output->name, variable_name) == 0)
            break;
        }
      if (j == outputs->len)
        g_warning ("no output variable named \"%s\", ignoring", variable_name);
      else
        {
          RPT_reporting_set_frequency (output,
                                       RPT_string_to_frequency (scew_element_contents
                                                                (scew_element_by_name
                                                                 (e, "frequency"))));
#if DEBUG
          g_debug ("report \"%s\" %s", variable_name, RPT_frequency_name[output->frequency]);
#endif
        }
    }
  scew_list_free (ee);

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

  /* Clean up. */
  scew_parser_free (parser);

#if DEBUG
  g_debug ("----- EXIT spreadmodel_load_models");
#endif

  return nloaded;
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
