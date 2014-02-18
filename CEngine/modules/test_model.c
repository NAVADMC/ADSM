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
#define is_singleton test_model_is_singleton
#define new test_model_new
#define run test_model_run
#define reset test_model_reset
#define events_listened_for test_model_events_listened_for
#define is_listening_for test_model_is_listening_for
#define has_pending_actions test_model_has_pending_actions
#define has_pending_infections test_model_has_pending_infections
#define to_string test_model_to_string
#define local_printf test_model_printf
#define local_fprintf test_model_fprintf
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
  gboolean *production_type;
  GPtrArray *production_types;
  PDF_dist_t *delay;
  double sensitivity; /**< The probability that the test will correctly give a
    positive result for a diseased or recovered (naturally immune) unit. */
  double specificity; /**< The probability that the test will correctly give a
    negative result for a healthy unit. */
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
  if (local_data->production_type[unit->production_type] == FALSE)
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
  if (local_data->production_type[unit->production_type] == FALSE)
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
      positive = (r < local_data->sensitivity);
      correct = positive;
#if DEBUG
      if (r < local_data->sensitivity)
        g_string_append_printf (s, ", r (%g) < sensitivity (%g) -> positive",
				r, local_data->sensitivity);
      else
        g_string_append_printf (s, ", r (%g) >= sensitivity (%g) -> negative",
				r, local_data->sensitivity);
#endif
      break;
    case Susceptible:
    case VaccineImmune:
      r = RAN_num (rng);
      positive = (r >= local_data->specificity);
      correct = !positive;
#if DEBUG
      if (r < local_data->specificity)
        g_string_append_printf (s, ", r (%g) < specificity (%g) -> negative",
				r, local_data->specificity);
      else
        g_string_append_printf (s, ", r (%g) >= specificity (%g) -> positive",
				r, local_data->specificity);
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
  delay = (int) round (PDF_random (local_data->delay, rng));
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
 * Reports whether this model is listening for a given event type.
 *
 * @param self the model.
 * @param event_type an event type.
 * @return TRUE if the model is listening for the event type.
 */
gboolean
is_listening_for (struct spreadmodel_model_t_ *self, EVT_event_type_t event_type)
{
  int i;

  for (i = 0; i < self->nevents_listened_for; i++)
    if (self->events_listened_for[i] == event_type)
      return TRUE;
  return FALSE;
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
 * Reports whether this model has any pending infections to cause.
 *
 * @param self the model.
 * @return TRUE if the model has pending infections.
 */
gboolean
has_pending_infections (struct spreadmodel_model_t_ * self)
{
  return FALSE;
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
  GString *s;
  gboolean already_names;
  unsigned int i;
  char *substring, *chararray;
  local_data_t *local_data;

  local_data = (local_data_t *) (self->model_data);
  s = g_string_new (NULL);
  g_string_sprintf (s, "<%s for ", MODEL_NAME);
  already_names = FALSE;
  for (i = 0; i < local_data->production_types->len; i++)
    if (local_data->production_type[i] == TRUE)
      {
        if (already_names)
	  g_string_append_printf (s, ",%s",
	 			  (char *) g_ptr_array_index (local_data->production_types, i));
	else
	  {			  
	    g_string_append_printf (s, "%s",
	 			    (char *) g_ptr_array_index (local_data->production_types, i));
	    already_names = TRUE;
	  }
      }

  substring = PDF_dist_to_string (local_data->delay);
  g_string_sprintfa (s, "\n  delay=%s\n", substring);
  g_free (substring);

  g_string_sprintfa (s, "  sensitivity=%g\n", local_data->sensitivity);
  g_string_sprintfa (s, "  specificity=%g>", local_data->specificity);

  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Prints this model to a stream.
 *
 * @param stream a stream to write to.
 * @param self the model.
 * @return the number of characters printed (not including the trailing '\\0').
 */
int
local_fprintf (FILE * stream, struct spreadmodel_model_t_ *self)
{
  char *s;
  int nchars_written;

  s = to_string (self);
  nchars_written = fprintf (stream, "%s", s);
  free (s);
  return nchars_written;
}



/**
 * Prints this model.
 *
 * @param self the model.
 * @return the number of characters printed (not including the trailing '\\0').
 */
int
local_printf (struct spreadmodel_model_t_ *self)
{
  return local_fprintf (stdout, self);
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
  GQueue *q;
  unsigned int i;
  
#if DEBUG
  g_debug ("----- ENTER free (%s)", MODEL_NAME);
#endif

  /* Free the dynamically-allocated parts. */
  local_data = (local_data_t *) (self->model_data);
  g_free (local_data->production_type);

  PDF_free_dist (local_data->delay);

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
 * Returns whether this model is a singleton or not.
 */
gboolean
is_singleton (void)
{
  return FALSE;
}



/**
 * Returns a new test model.
 */
spreadmodel_model_t *
new (scew_element * params, UNT_unit_list_t *units, projPJ projection,
     ZON_zone_list_t *zones)
{
  spreadmodel_model_t *self;
  local_data_t *local_data;
  scew_element *e;
  gboolean success;

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
  self->is_listening_for = is_listening_for;
  self->has_pending_actions = has_pending_actions;
  self->has_pending_infections = has_pending_infections;
  self->to_string = to_string;
  self->printf = local_printf;
  self->fprintf = local_fprintf;
  self->free = local_free;

  /* Make sure the right XML subtree was sent. */
  g_assert (strcmp (scew_element_name (params), MODEL_NAME) == 0);

#if DEBUG
  g_debug ("setting production types");
#endif
  local_data->production_types = units->production_type_names;
  local_data->production_type = spreadmodel_read_prodtype_attribute (params, "production-type", units->production_type_names);

  e = scew_element_by_name (params, "delay");
  if (e != NULL)
    {
      local_data->delay = PAR_get_PDF (e);
    }
  else
    {
      g_warning ("%s: delay parameter missing, setting to 0 days", MODEL_NAME);
      local_data->delay = PDF_new_point_dist (0);
    }

  e = scew_element_by_name (params, "sensitivity");
  if (e != NULL)
    {
      local_data->sensitivity = PAR_get_probability (e, &success);
      if (success == FALSE)
	{
	  g_warning ("%s: setting sensitivity to 1", MODEL_NAME);
	  local_data->sensitivity = 1.0;
	}
    }
  else
    {
      local_data->sensitivity = 1.0;
      g_warning ("%s: sensitivity parameter missing, setting to 1", MODEL_NAME);
    }

  e = scew_element_by_name (params, "specificity");
  if (e != NULL)
    {
      local_data->specificity = PAR_get_probability (e, &success);
      if (success == FALSE)
	{
	  g_warning ("%s: setting specificity to 1", MODEL_NAME);
	  local_data->specificity = 1.0;
	}
    }
  else
    {
      local_data->specificity = 1.0;
      g_warning ("%s: specificity parameter missing, setting to 1", MODEL_NAME);
    }

    /* Initialize an array for delayed test results.  We don't know yet how
     * long the array needs to be, since that will depend on values we sample
     * from the delay distribution, so we initialize it to length 1. */
    local_data->pending_results = g_ptr_array_new ();
    g_ptr_array_add (local_data->pending_results, g_queue_new());
    local_data->npending_results = 0;
    local_data->rotating_index = 0;

    local_data->detection_status = g_hash_table_new (g_direct_hash, g_direct_equal);

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file test_model.c */
