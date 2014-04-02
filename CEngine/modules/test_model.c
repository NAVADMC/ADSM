/** @file test_model.c
 * Module that encapsulates knowledge about a test for disease.
 * <ul>
 *   <li> how long the test requires to get a result
 *   <li> the sensitivity of the test
 *   <li> the specificity of the test
 * </ul>
 *
 * When this module hears a Test event, it checks the unit and decides on a
 * test result.  Depending on the delay parameter, it may announce a TestResult
 * event immediately, or on a subsequent day.  If the result is positive and
 * the unit has not already been detected, it announces a Detection event.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @version 0.1
 * @date July 2005
 *
 * Copyright &copy; University of Guelph, 2003-2009
 */

#if HAVE_CONFIG_H
#  include <config.h>
#endif

/* To avoid name clashes when multiple modules have the same interface. */
#define new test_model_new
#define run test_model_run
#define reset test_model_reset
#define events_listened_for test_model_events_listened_for
#define has_pending_actions test_model_has_pending_actions
#define to_string test_model_to_string
#define local_free test_model_free
#define handle_new_day_event test_model_handle_new_day_event
#define handle_detection_event test_model_handle_detection_event
#define handle_test_event test_model_handle_test_event

#include "module.h"
#include "module_util.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#if HAVE_STRINGS_H
#  include <strings.h>
#endif

#if HAVE_MATH_H
#  include <math.h>
#endif

#include "test_model.h"

#if !HAVE_ROUND && HAVE_RINT
#  define round rint
#endif

/* Temporary fix -- "round" and "rint" are in the math library on Red Hat 7.3,
 * but they're #defined so AC_CHECK_FUNCS doesn't find them. */
double round (double x);

/** This must match an element name in the DTD. */
#define MODEL_NAME "test-model"



#define NEVENTS_LISTENED_FOR 3
EVT_event_type_t events_listened_for[] = { EVT_NewDay,
  EVT_Detection, EVT_Test };



#define NOT_DETECTED_TEST_ORDERED 1
#define DETECTED_NO_TEST_ORDERED 2
#define DETECTED_TEST_ORDERED 3



/* Specialized information for this model. */
typedef struct
{
  PDF_dist_t *delay;
  double sensitivity; /**< The probability that the test will correctly give a
    positive result for a diseased or recovered (naturally immune) unit. */
  double specificity; /**< The probability that the test will correctly give a
    negative result for a healthy unit. */
}
param_block_t;



typedef struct
{
  GPtrArray *production_types;
  param_block_t **param_block; /**< Blocks of parameters.  Use an expression of
    the form
    param_block[production_type]
    to get a pointer to a particular parameter block. */
  GPtrArray *pending_results; /**< An array to store delayed test results.
    Each item in the array is a GQueue of TestResult and Detection events.
    (Actually a singly-linked list would suffice, but the GQueue syntax is much
    more readable than the GSList syntax.)  An index "rotates" through the
    array, so a result that is to be released in 1 day is placed in the GQueue
    that is 1 place ahead of the rotating index, a result that is to be
    released in 2 days is placed in the GQueue that is 2 places ahead of the
    rotating index, etc. */
  unsigned int npending_results; /**< The number of pending results. */
  unsigned int rotating_index;
  GHashTable *detection_status; /**< A table recording detected units.  We only
    track detections for units that are currently undergoing tests, so that we
    know whether an eventual positive test result should trigger a new
    Detection or not. */
  sqlite3 *db; /* Temporarily stash a pointer to the parameters database here
    so that it will be available to the set_params function. */
}
local_data_t;



/**
 * Used in handle_new_day_event below to remove any occurrences of
 * DETECTED_NO_TEST_ORDERED from the detection_status table.
 *
 * @param key a unit (UNT_unit_t *).
 * @param value an integer, one of NOT_DETECTED_TEST_ORDERED,
 *   DETECTED_NO_TEST_ORDERED, or DETECTED_TEST_ORDERED.
 * @param user_data not needed, pass NULL.
 * @return TRUE if the value is DETECTED_NO_TEST_ORDERED, FALSE otherwise.
 */
gboolean
not_needed_in_detection_status (gpointer key, gpointer value, gpointer user_data)
{
  return (GPOINTER_TO_INT(value) == DETECTED_NO_TEST_ORDERED);
}



/**
 * Responds to a new day event by releasing any pending test results.
 *
 * @param self the model.
 * @param event a new day event.
 * @param queue for any new events the model creates.
 */
void
handle_new_day_event (struct spreadmodel_model_t_ *self,
		      EVT_new_day_event_t *event,
		      EVT_event_queue_t *queue)
{
  local_data_t *local_data;
  GQueue *q;
  EVT_event_t *result;
  gpointer p;
  UNT_unit_t *unit, *last_unit;

#if DEBUG
  g_debug ("----- ENTER handle_new_day_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* Delete any detections we recorded yesterday that did not match up with
   * orders for tests. */
  g_hash_table_foreach_remove (local_data->detection_status,
                               not_needed_in_detection_status, NULL);

  /* Release any test results that were delayed until today. */
  local_data->rotating_index = (local_data->rotating_index + 1) % local_data->pending_results->len;
  q = (GQueue *) g_ptr_array_index (local_data->pending_results,
				    local_data->rotating_index);
  last_unit = NULL;
  while (!g_queue_is_empty (q))
    {
      result = (EVT_event_t *) g_queue_pop_head (q);

#ifndef WIN_DLL
      /* Double-check that the event is coming out on the correct day. */
      if (result->type == EVT_TestResult)
        g_assert (result->u.test_result.day == event->day);
      else
        g_assert (result->u.detection.day == event->day);
#endif

      /* The events in the queue come in ones or twos -- either a TestResult
       * with no Detection, or a TestResult paired with a detection.  We want
       * to delete the unit from the detection_status table once we've seen
       * all the events for this unit. */
      if (result->type == EVT_TestResult)
        unit = result->u.test_result.unit;
      else
        unit = result->u.detection.unit;
      if (unit != last_unit && last_unit != NULL)
        g_hash_table_remove (local_data->detection_status, last_unit);
      last_unit = unit;       

      if (result->type == EVT_TestResult)
        {
#if DEBUG
          g_debug ("test result for unit \"%s\" now ready",
                   result->u.test_result.unit->official_id);
#endif
          EVT_event_enqueue (queue, result);
        }
      else
        {
          /* Release the Detection only if it's a new one. */
          p = g_hash_table_lookup (local_data->detection_status,
                                   result->u.detection.unit);
          if (GPOINTER_TO_INT(p) != DETECTED_TEST_ORDERED)
            {
              result->u.detection.day = event->day;
              EVT_event_enqueue (queue, result);
            }
          else
            EVT_free_event (result);
        }
      local_data->npending_results--;
    }
  if (last_unit != NULL)
    g_hash_table_remove (local_data->detection_status, last_unit);

#if DEBUG
  g_debug ("----- EXIT handle_new_day_event (%s)", MODEL_NAME);
#endif
}



/**
 * Responds to a detection event by recording it.
 *
 * @param self this module.
 * @param event a detection event.
 */
void
handle_detection_event (struct spreadmodel_model_t_ *self,
                        EVT_detection_event_t *event)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  gpointer p;
  int detection_status;

#if DEBUG
  g_debug ("----- ENTER handle_detection_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  unit = event->unit;
  if (local_data->param_block[unit->production_type] == NULL)
    goto end;

  p = g_hash_table_lookup (local_data->detection_status, unit);
  if (p == NULL)
    {
      /* This unit has not been detected and does not have a test ordered. */
      g_hash_table_insert (local_data->detection_status, unit,
                           GINT_TO_POINTER(DETECTED_NO_TEST_ORDERED));
    }
  else
    {
      /* This unit has been detected before or has a test ordered.  The only
       * case we need to worry about is changing "not detected" to "detected". */
      detection_status = GPOINTER_TO_INT(p);
      if (detection_status == NOT_DETECTED_TEST_ORDERED)
        g_hash_table_insert (local_data->detection_status, unit,
                             GINT_TO_POINTER(DETECTED_TEST_ORDERED));
    }

end:
#if DEBUG
  g_debug ("----- EXIT handle_detection_event (%s)", MODEL_NAME);
#endif
  return;
}



/**
 * Responds to a test event by deciding what the test result will be.
 *
 * @param self the model.
 * @param event a test event.
 * @param rng a random number generator.
 * @param queue for any new events the model creates.
 */
void
handle_test_event (struct spreadmodel_model_t_ *self,
		   EVT_test_event_t *event,
                   RAN_gen_t *rng,
		   EVT_event_queue_t *queue)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  param_block_t *param_block;
  double r;
  gboolean positive, correct;
  EVT_event_t *result, *detection;
  int delay;
  int delay_index;
  GQueue *q;
  SPREADMODEL_test_result test_result;
  gpointer p;
  int detection_status;
#if DEBUG
  GString *s;
#endif

#if DEBUG
  g_debug ("----- ENTER handle_test_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  unit = event->unit;
  param_block = local_data->param_block[unit->production_type];
  if (param_block == NULL)
    goto end;

#if DEBUG
  s = g_string_new (NULL);
  g_string_printf (s, "unit \"%s\" is %s", unit->official_id,
        	       UNT_state_name [unit->state]);
#endif
  switch (unit->state)
    {
    case Latent:
    case InfectiousSubclinical:
    case InfectiousClinical:
    case NaturallyImmune:
      r = RAN_num (rng);
      positive = (r < param_block->sensitivity);
      correct = positive;
#if DEBUG
      if (r < param_block->sensitivity)
        g_string_append_printf (s, ", r (%g) < sensitivity (%g) -> positive",
				r, param_block->sensitivity);
      else
        g_string_append_printf (s, ", r (%g) >= sensitivity (%g) -> negative",
				r, param_block->sensitivity);
#endif
      break;
    case Susceptible:
    case VaccineImmune:
      r = RAN_num (rng);
      positive = (r >= param_block->specificity);
      correct = !positive;
#if DEBUG
      if (r < param_block->specificity)
        g_string_append_printf (s, ", r (%g) < specificity (%g) -> negative",
				r, param_block->specificity);
      else
        g_string_append_printf (s, ", r (%g) >= specificity (%g) -> positive",
				r, param_block->specificity);
#endif
      break;
    case Destroyed:
      positive = FALSE;
      correct = TRUE;
#if DEBUG
      g_string_append_printf (s, " -> negative");
#endif
      break;        
    }
#if DEBUG
  g_debug ("%s", s->str);
  g_string_free (s, TRUE);
#endif

  if( positive && correct )
    test_result = SPREADMODEL_TestTruePositive;
  else if( positive && !( correct) )
    test_result = SPREADMODEL_TestFalsePositive;
  else if( !(positive) && correct )
    test_result = SPREADMODEL_TestTrueNegative;
  else
    test_result = SPREADMODEL_TestFalseNegative;

  result = EVT_new_test_result_event (unit, event->day, positive, correct, event->reason);
  if (positive)
    detection = EVT_new_detection_event (unit, event->day, SPREADMODEL_DetectionDiagnosticTest, test_result);
  else
    detection = NULL;
  delay = (int) round (PDF_random (param_block->delay, rng));
  /* If there is no delay, release the test result immediately; otherwise, add
   * it to a list to be released on a future day. */
  if (delay <= 0)
    {
      EVT_event_enqueue (queue, result);
      if (detection)
        EVT_event_enqueue (queue, detection);
    }
  else
    {
      result->u.test_result.day += delay;
      if (delay > local_data->pending_results->len)
        spreadmodel_extend_rotating_array (local_data->pending_results, delay,
                                           local_data->rotating_index);
      delay_index = (local_data->rotating_index + delay) % local_data->pending_results->len;
      q = (GQueue *) g_ptr_array_index (local_data->pending_results, delay_index);
#if DEBUG
      g_debug ("queueing at position %i (%i + %i mod %u)",
               delay_index, local_data->rotating_index, delay,
               local_data->pending_results->len);
#endif
      g_queue_push_head (q, result);
      local_data->npending_results++;
      if (detection)
        {
          detection->u.detection.day += delay;
          g_queue_push_head (q, detection);
          local_data->npending_results++;
        }
      p = g_hash_table_lookup (local_data->detection_status, unit);
      if (p == NULL)
        g_hash_table_insert (local_data->detection_status, unit,
                             GINT_TO_POINTER(NOT_DETECTED_TEST_ORDERED));
      else
        {
          detection_status = GPOINTER_TO_INT(p);
          if (detection_status == DETECTED_NO_TEST_ORDERED)
            g_hash_table_insert (local_data->detection_status, unit,
                                 GINT_TO_POINTER(DETECTED_TEST_ORDERED));
        }
    }

end:
#if DEBUG
  g_debug ("----- EXIT handle_test_event (%s)", MODEL_NAME);
#endif
  return;
}



/**
 * Runs this model.
 *
 * @param self the model.
 * @param units a list of units.
 * @param zones a list of zones.
 * @param event the event that caused the model to run.
 * @param rng a random number generator.
 * @param queue for any new events the model creates.
 */
void
run (struct spreadmodel_model_t_ *self, UNT_unit_list_t *units, ZON_zone_list_t *zones,
     EVT_event_t * event, RAN_gen_t * rng, EVT_event_queue_t * queue)
{
#if DEBUG
  g_debug ("----- ENTER run (%s)", MODEL_NAME);
#endif

  switch (event->type)
    {
    case EVT_NewDay:
      handle_new_day_event (self, &(event->u.new_day), queue);
      break;
    case EVT_Detection:
      handle_detection_event (self, &(event->u.detection));
      break;
    case EVT_Test:
      handle_test_event (self, &(event->u.test), rng, queue);
      break;
    default:
      g_error ("%s has received a %s event, which it does not listen for.  This should never happen.  Please contact the developer.",
	       MODEL_NAME, EVT_event_type_name[event->type]);
    }

#if DEBUG
  g_debug ("----- EXIT run (%s)", MODEL_NAME);
#endif
}



/**
 * Resets this model after a simulation run.
 *
 * @param self the model.
 */
void
reset (struct spreadmodel_model_t_ *self)
{
  local_data_t *local_data;
  GQueue *q;
  unsigned int i;

#if DEBUG
  g_debug ("----- ENTER reset (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  for (i = 0; i < local_data->pending_results->len; i++)
    {
      q = (GQueue *) g_ptr_array_index (local_data->pending_results, i);
      while (!g_queue_is_empty (q))
	EVT_free_event (g_queue_pop_head (q));      
    }
  local_data->npending_results = 0;
  local_data->rotating_index = 0;

  g_hash_table_remove_all (local_data->detection_status);

#if DEBUG
  g_debug ("----- EXIT reset (%s)", MODEL_NAME);
#endif
}



/**
 * Reports whether this model has any pending actions to carry out.
 *
 * @param self the model.
 * @return TRUE if the model has pending actions.
 */
gboolean
has_pending_actions (struct spreadmodel_model_t_ *self)
{
  local_data_t *local_data;

  local_data = (local_data_t *) (self->model_data);
  return (local_data->npending_results > 0);
}



/**
 * Returns a text representation of this model.
 *
 * @param self the model.
 * @return a string.
 */
char *
to_string (struct spreadmodel_model_t_ *self)
{
  local_data_t *local_data;
  GString *s;
  guint nprod_types, i;
  param_block_t *param_block;
  char *substring, *chararray;

  local_data = (local_data_t *) (self->model_data);
  s = g_string_new (NULL);
  g_string_sprintf (s, "<%s", MODEL_NAME);

  /* Add the parameter block for each production type. */
  nprod_types = local_data->production_types->len;
  for (i = 0; i < nprod_types; i++)
    {
      param_block = local_data->param_block[i];
      if (param_block == NULL)
        continue;

      g_string_append_printf (s, "\n  for %s",
                              (char *) g_ptr_array_index (local_data->production_types, i));

      substring = PDF_dist_to_string (param_block->delay);
      g_string_append_printf (s, "\n    delay=%s\n", substring);
      g_free (substring);

      g_string_append_printf (s, "    sensitivity=%g\n", param_block->sensitivity);
      g_string_append_printf (s, "    specificity=%g>", param_block->specificity);
    }
  g_string_append_c (s, '>');

  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Frees this model.  Does not free the production type names.
 *
 * @param self the model.
 */
void
local_free (struct spreadmodel_model_t_ *self)
{
  local_data_t *local_data;
  guint nprod_types, i;
  param_block_t *param_block;
  GQueue *q;
  
#if DEBUG
  g_debug ("----- ENTER free (%s)", MODEL_NAME);
#endif

  /* Free the dynamically-allocated parts. */
  local_data = (local_data_t *) (self->model_data);

  nprod_types = local_data->production_types->len;
  for (i = 0; i < nprod_types; i++)
    {
      param_block = local_data->param_block[i];
      if (param_block != NULL)
        {
          PDF_free_dist (param_block->delay);
          g_free (param_block);
        }
    }
  g_free (local_data->param_block);

  for (i = 0; i < local_data->pending_results->len; i++)
    {
      q = (GQueue *) g_ptr_array_index (local_data->pending_results, i);
      while (!g_queue_is_empty (q))
	EVT_free_event (g_queue_pop_head (q));
      g_queue_free (q);
    }
  g_ptr_array_free (local_data->pending_results, TRUE);

  g_hash_table_destroy (local_data->detection_status);
  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Adds a set of production type specific parameters to a test model.
 *
 * @param data this module ("self"), but cast to a void *.
 * @param ncols number of columns in the SQL query result.
 * @param values values returned by the SQL query, all in text form.
 * @param colname names of columns in the SQL query result.
 * @return 0
 */
static int
set_params (void *data, int ncols, char **value, char **colname)
{
  spreadmodel_model_t *self;
  local_data_t *local_data;
  sqlite3 *params;
  guint production_type;
  param_block_t *p;
  guint pdf_id;

  #if DEBUG
    g_debug ("----- ENTER set_params (%s)", MODEL_NAME);
  #endif

  self = (spreadmodel_model_t *)data;
  local_data = (local_data_t *) (self->model_data);
  params = local_data->db;

  g_assert (ncols == 4);

  /* Find out which production type these parameters apply to. */
  production_type =
    spreadmodel_read_prodtype (value[0], local_data->production_types);

  /* Check that we are not overwriting an existing parameter block (that would
   * indicate a bug). */
  g_assert (local_data->param_block[production_type] == NULL);

  /* Create a new parameter block. */
  p = g_new (param_block_t, 1);
  local_data->param_block[production_type] = p;

  /* Read the parameters. */
  errno = 0;
  pdf_id = strtol (value[1], NULL, /* base */ 10);
  g_assert (errno != ERANGE && errno != EINVAL);  
  p->delay = PAR_get_PDF (params, pdf_id);

  errno = 0;
  p->sensitivity = strtod (value[2], NULL);
  g_assert (errno != ERANGE);
  g_assert (p->sensitivity >= 0 && p->sensitivity <= 1);

  errno = 0;
  p->specificity = strtod (value[3], NULL);
  g_assert (errno != ERANGE);
  g_assert (p->specificity >= 0 && p->specificity <= 1);

#if DEBUG
  g_debug ("----- EXIT set_params (%s)", MODEL_NAME);
#endif

  return 0;
}



/**
 * Returns a new test model.
 */
spreadmodel_model_t *
new (sqlite3 * params, UNT_unit_list_t *units, projPJ projection,
     ZON_zone_list_t *zones)
{
  spreadmodel_model_t *self;
  local_data_t *local_data;
  guint nprod_types;
  char *sqlerr;

#if DEBUG
  g_debug ("----- ENTER new (%s)", MODEL_NAME);
#endif

  self = g_new (spreadmodel_model_t, 1);
  local_data = g_new (local_data_t, 1);

  self->name = MODEL_NAME;
  self->events_listened_for = events_listened_for;
  self->nevents_listened_for = NEVENTS_LISTENED_FOR;
  self->outputs = g_ptr_array_new ();
  self->model_data = local_data;
  self->run = run;
  self->reset = reset;
  self->is_singleton = FALSE;
  self->is_listening_for = spreadmodel_model_is_listening_for;
  self->has_pending_actions = has_pending_actions;
  self->has_pending_infections = spreadmodel_model_answer_no;
  self->to_string = to_string;
  self->printf = spreadmodel_model_printf;
  self->fprintf = spreadmodel_model_fprintf;
  self->free = local_free;

  /* Initialize an array for delayed test results.  We don't know yet how
   * long the array needs to be, since that will depend on values we sample
   * from the delay distribution, so we initialize it to length 1. */
  local_data->pending_results = g_ptr_array_new ();
  g_ptr_array_add (local_data->pending_results, g_queue_new());
  local_data->npending_results = 0;
  local_data->rotating_index = 0;

  local_data->detection_status = g_hash_table_new (g_direct_hash, g_direct_equal);

  /* Initialize the array of parameter blocks. */
  local_data->production_types = units->production_type_names;
  nprod_types = local_data->production_types->len;
  local_data->param_block = g_new0 (param_block_t *, nprod_types);

  /* Call the set_params function to read the production type specific
   * parameters. */
  local_data->db = params;
  sqlite3_exec (params,
                "SELECT prodtype.name,test_delay_id,test_sensitivity,test_specificity FROM ScenarioCreator_productiontype prodtype,ScenarioCreator_controlprotocol protocol, ScenarioCreator_protocolassignment xref WHERE prodtype.id=xref.production_type_id AND xref.control_protocol_id=protocol.id",
                set_params, self, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }
  local_data->db = NULL;

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file test_model.c */
