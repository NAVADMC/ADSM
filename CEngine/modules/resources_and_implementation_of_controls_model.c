/** @file resources_and_implementation_of_controls_model.c
 * Module that simulates the actions and resources of government authorities in
 * an outbreak.
 *
 * This module has several responsibilities, detailed in the sections below.
 *
 * <b>Identifying an outbreak</b>
 *
 * When this module hears the first Detection event, it
 * <ol>
 *   <li>
 *     announces a PublicAnnouncement event
 *   <li>
 *     starts counting down days until a destruction program can begin
 * </ol>
 *
 * <b>Vaccinating units</b>
 *
 * This module picks up RequestForVaccination events and announces
 * CommitmentToVaccinate events.  The unit is placed in a waiting list (queue)
 * with a priority.  The first day on which a unit can be vaccinated is the
 * beginning of the authorities' vaccination program <em>or</em> the day after
 * the request for vaccination is made, whichever is later.
 *
 * See below for an explanation of how priorities work.
 *
 * If a unit to be vaccinated was vaccinated recently (within the number of
 * days specified in the parameters) the request will be discarded.
 *
 * <b>Destroying units</b>
 *
 * This module picks up RequestForDestruction events and announces
 * CommitmentToDestroy events.  The unit is placed in a waiting list (queue)
 * with a priority.  The first day on which a unit can be destroyed is the
 * beginning of the authorities' destruction program <em>or</em> the day after
 * the request for destruction is made, whichever is later.
 *
 * NB: This module never announces RequestForDestruction or
 * RequestForVaccination events.  Other modules (e.g.,
 * basic-destruction-model.c, ring-destruction-model.c) simulate policies that
 * decide which units are destroyed or vaccinated.  Those policy modules can be
 * included or excluded from simulations to try out different combinations of
 * policies.
 *
 * <b>The priority system</b>
 *
 * Vaccination and destruction follow a strict priority order.  Units on a
 * waiting list are prioritized by <i>production type</i>, <i>reason</i> for
 * vaccination or destruction, and <i>time waiting</i>.
 *
 * The model description document has a discussion with examples of how the
 * priority system works.  The discussion below is about how it is implemented
 * in code.  (It specifically discusses destruction, but the same points apply
 * to vaccination.)
 *
 * The implementation works like this: each request for destruction is placed
 * in one of several queues.  The order of the queues takes care of
 * prioritizing by <i>production type</i> and <i>reason</i>.  The queues are
 * processed in slightly different ways to take into account <i>time
 * waiting</i>.
 *
 * Consider a scenario where there are 3 production types (cattle, pigs, sheep)
 * and 4 possible reasons for destruction (basic, ring, trace direct, trace
 * indirect).  Suppose that time waiting is in last place, as in
 *
 * production type (cattle > pigs > sheep) > reason (basic > trace direct >
 * ring > trace indirect) > time waiting
 *
 * There would be 12 queues, numbered as follows:
 * -# basic destruction / cattle
 * -# trace direct destruction / cattle
 * -# ring destruction / cattle
 * -# trace indirect destruction / cattle
 * -# basic destruction / pigs
 * -# trace direct destruction / pigs
 * -# ring destruction / pigs
 * -# trace indirect destruction / pigs
 * -# basic destruction / sheep
 * -# trace direct destruction / sheep
 * -# ring destruction / sheep
 * -# trace indirect destruction / sheep
 *
 * On each day, this module will destroy every unit on list 1, then every unit
 * on list 2, etc., until the destruction capacity runs out.  Every waiting
 * cattle unit will be destroyed before any waiting pig unit, and among cattle
 * units, every unit that was chosen by the "basic" destruction rule will be
 * destroyed before any unit that was chosen by the "trace" destruction rule.
 * Time waiting is taken care of by the fact that each of the 12 lists is a
 * queue: new requests enter the queue at one end, requests that have been
 * waiting the longest pop out the other end.
 *
 * If reason for destruction is given priority over production type, as in
 *
 * reason (basic > trace direct > ring > trace indirect) > production type
 * (cattle > pigs > sheep) > time waiting
 *
 * The order of the queues would be:
 * -# basic destruction / cattle
 * -# basic destruction / pigs
 * -# basic destruction / sheep
 * -# trace direct destruction / cattle
 * -# trace direct destruction / pigs
 * -# trace direct destruction / sheep
 * -# ring destruction / cattle
 * -# ring destruction / pigs
 * -# ring destruction / sheep
 * -# trace indirect destruction / cattle
 * -# trace indirect destruction / pigs
 * -# trace indirect destruction / sheep
 *
 * Again, this situation is handled by destroying every unit on list 1, then
 * every unit on list 2, etc.
 *
 * Now suppose that time waiting is given first priority:
 *
 * time waiting > reason (basic > trace direct > ring > trace indirect) >
 * production type (cattle > pigs > sheep)
 *
 * The order of the queues would still be:
 * -# basic destruction / cattle
 * -# basic destruction / pigs
 * -# basic destruction / sheep
 * -# trace direct destruction / cattle
 * -# trace direct destruction / pigs
 * -# trace direct destruction / sheep
 * -# ring destruction / cattle
 * -# ring destruction / pigs
 * -# ring destruction / sheep
 * -# trace indirect destruction / cattle
 * -# trace indirect destruction / pigs
 * -# trace indirect destruction / sheep
 *
 * But what the program will do in this case is scan all 12 queues for the one
 * with the unit that has been waiting the longest, destroy that unit, and
 * repeat.  If 2 queues contain units that have been waiting for the same
 * amount of time, the one higher-up in the queue order is taken, thus making
 * reason and production type the 2nd and 3rd priorities.
 *
 * If time waiting is given second priority:
 *
 * reason (basic > trace direct > ring > trace indirect) > time waiting >
 * production type (cattle > pigs > sheep)
 *
 * The order of the queues would be exactly as above again:
 * -# | basic destruction / cattle
 * -# | basic destruction / pigs
 * -# | basic destruction / sheep
 * -# trace direct destruction / cattle
 * -# trace direct destruction / pigs
 * -# trace direct destruction / sheep
 * -# ring destruction / cattle
 * -# ring destruction / pigs
 * -# ring destruction / sheep
 * -# trace indirect destruction / cattle
 * -# trace indirect destruction / pigs
 * -# trace indirect destruction / sheep
 *
 * The program will scan the first 3 queues for the one with the unit that has
 * been waiting the longest, destroy that unit, and repeat.  If the first 3
 * queues are empty and destruction capacity still remains, the program will
 * move on to the next 3 queues.
 *
 * As a final example, if you want the same priorities:
 *
 * reason (basic > trace direct > ring > trace indirect) > time waiting >
 * production type (cattle > pigs > sheep)
 *
 * but you wish to exclude sheep from destruction, the order of the queues
 * would be:
 * -# | basic destruction / cattle
 * -# | basic destruction / pigs
 * -# |
 * -# trace direct destruction / cattle
 * -# trace direct destruction / pigs
 * -#
 * -# ring destruction / cattle
 * -# ring destruction / pigs
 * -#
 * -# trace indirect destruction / cattle
 * -# trace indirect destruction / pigs
 * -# &nbsp;
 *
 * Note the queue numbers.  This is done so that the program still knows how to
 * group the lists: 3 production types means group by 3's.
 *
 * There is another wrinkle to the data structures that maintainers should be
 * aware of.  The queues shown above are GQueue objects, which store
 * RequestForDestruction objects, as shown in the diagram below.  There are
 * additional pointers into the GQueue, stored in an array called
 * destruction_status.  The destruction_status array holds one pointer per
 * unit.  If the unit is awaiting destruction, the pointer points to the GList
 * node that stores the request to destroy that unit; if the unit is not
 * awaiting destruction, the pointer is null.
 *
 * @image html priority_queues.png
 *
 * The destruction_status array is useful for quickly finding out whether a
 * unit is awaiting destruction, so that when another request is made to
 * destroy that unit, and the new request has higher priority, the old request
 * can be discarded.  The corresponding array for vaccination is also useful
 * when a unit that is awaiting vaccination is destroyed and the request for
 * vaccination can be discarded.  The destruction_status and vaccination_status
 * arrays must be updated whenever requests are pushed into or popped from the
 * queues.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @version 0.1
 * @date June 2003
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

/* To avoid name clashes when multiple modules have the same interface. */
#define new resources_and_implementation_of_controls_model_new
#define run resources_and_implementation_of_controls_model_run
#define has_pending_actions resources_and_implementation_of_controls_model_has_pending_actions
#define to_string resources_and_implementation_of_controls_model_to_string
#define local_free resources_and_implementation_of_controls_model_free
#define handle_before_each_simulation_event resources_and_implementation_of_controls_model_handle_before_each_simulation_event
#define handle_new_day_event resources_and_implementation_of_controls_model_handle_new_day_event
#define handle_detection_event resources_and_implementation_of_controls_model_handle_detection_event
#define handle_request_for_destruction_event resources_and_implementation_of_controls_model_handle_request_for_destruction_event
#define handle_request_to_initiate_vaccination_event resources_and_implementation_of_controls_model_handle_request_to_initiate_vaccination_event
#define handle_request_for_vaccination_event resources_and_implementation_of_controls_model_handle_request_for_vaccination_event
#define handle_vaccination_event resources_and_implementation_of_controls_model_handle_vaccination_event
#define handle_request_to_terminate_vaccination_event resources_and_implementation_of_controls_model_handle_request_to_terminate_vaccination_event

#include "module.h"
#include "module_util.h"
#include "scorecard.h"
#include "sqlite3_exec_dict.h"
#include <limits.h>
#include <json-glib/json-glib.h>

#if STDC_HEADERS
#  include <string.h>
#endif

#if HAVE_STRINGS_H
#  include <strings.h>
#endif

#if HAVE_MATH_H
#  include <math.h>
#endif

#include "resources_and_implementation_of_controls_model.h"

#if !HAVE_ROUND && HAVE_RINT
#  define round rint
#endif

/* Temporary fix -- "round" and "rint" are in the math library on Red Hat 7.3,
 * but they're #defined so AC_CHECK_FUNCS doesn't find them. */
double round (double x);

/** This must match an element name in the DTD. */
#define MODEL_NAME "resources-and-implementation-of-controls-model"

#define EPSILON 0.01 /* for distance comparisons = 10 m */


/******************************************************************************
 * Prioritizers.
 *****************************************************************************/

/* Forward declaration for the prioritizer object defined below. */
struct adsm_prioritizer_t_;

/* Type of a function that compares two unit scorecards for priority. */
typedef int (*adsm_prioritizer_compare_t) (struct adsm_prioritizer_t_ *,
                                           USC_scorecard_t *,
                                           USC_scorecard_t *);

/* Type of a function that returns a string representation of a prioritizer object. */
typedef char *(*adsm_prioritizer_to_string_t) (struct adsm_prioritizer_t_ *);

/* Type of a function that frees a prioritizer object. */
typedef void (*adsm_prioritizer_free_t) (struct adsm_prioritizer_t_ *);

/**
 * A prioritizer object.  It knows how to sort two units into priority order
 * according to some stored criterion.
 */
typedef struct adsm_prioritizer_t_
{
  gpointer private; /* Specialized information for the particular type of prioritizer */
  adsm_prioritizer_compare_t compare;
  adsm_prioritizer_to_string_t to_string;
  adsm_prioritizer_free_t free;
}
adsm_prioritizer_t;



/* Prototypes for functions that create different types of prioritizer objects. */
static adsm_prioritizer_t *new_production_type_prioritizer (GPtrArray *, gchar **);
static adsm_prioritizer_t *new_time_waiting_prioritizer (gboolean oldest_first);
static adsm_prioritizer_t *new_size_prioritizer (gboolean largest_first);
static adsm_prioritizer_t *new_direction_prioritizer (gboolean outside_in);



/** Implementation for by-production-type prioritizer. ***********************/

/**
 * Compares two herd scorecards by production type and returns their priority
 * order.
 */
static int
adsm_production_type_prioritizer_compare (adsm_prioritizer_t *self,
                                          USC_scorecard_t *scorecard1,
                                          USC_scorecard_t *scorecard2)
{
  guint *priority;
  guint priority1, priority2;
  
  priority = (guint *) (self->private);
  priority1 = priority[scorecard1->unit->production_type];
  priority2 = priority[scorecard2->unit->production_type];
  #if DEBUG && 0
    g_debug ("comparing unit \"%s\" and \"%s\" by prodtype",
             scorecard1->unit->official_id,
             scorecard2->unit->official_id);
  #endif
  return (priority2 - priority1);
}

static char*
adsm_production_type_prioritizer_to_string (adsm_prioritizer_t *self)
{
  return g_strdup("<prioritizer by production type>");
}

/**
 * Frees any prioritizer that has a single memory block allocated for its
 * private data (no other dynamically allocated pieces).
 */
static void
adsm_free_prioritizer (adsm_prioritizer_t *self)
{
  if (self != NULL)
    {
      g_free (self->private);
      g_free (self);
    }
  return;  
}

/**
 * Creates a new by-production-type prioritizer.
 *
 * @param production_type_names a list of all production type names in the
 *   population. Each item in the array is a (char *).
 * @param prodtypes a list of production type names (char *) in priority order,
 *   highest priority first. This is a null-terminated array of the form
 *   returned by g_strsplit(). If this list omits any of the production types,
 *   those production types will go at the end of the list, all with the same
 *   priority. This list can be freed after using it in this function call.
 * @return a prioritizer object.
 */
static adsm_prioritizer_t *
new_production_type_prioritizer (GPtrArray *production_type_names,
                                 char **prodtypes)
{
  adsm_prioritizer_t *self;
  guint *priority;
  guint i, j, n;
  char *prodtype;

  #if DEBUG
    g_debug ("----- ENTER new_production_type_prioritizer");
  #endif

  self = g_new (adsm_prioritizer_t, 1);
  self->compare = adsm_production_type_prioritizer_compare;
  self->to_string = adsm_production_type_prioritizer_to_string;
  self->free = adsm_free_prioritizer;
  /* The private data in this type of prioritizer object is an array.  It is
   * indexed by production type number, and the value found in the array is
   * the numeric priority of that production type (lower number = higher
   * priority). */
  n = production_type_names->len;
  priority = g_new (guint, n);
  /* Initialize the array with low-priority numbers. These will provide a
   * default for production types not found in the "prodtypes" list. */
  for (i = 0; i < n; i++)
    {
      priority[i] = n;
    }
  i = 0; /* "i" will hold the priority number in this loop */
  for (i = 0; prodtypes[i] != NULL; i++)
    {
      prodtype = prodtypes[i];
      /* Find the number for this production type name. */
      for (j = 0; j < n; j++)
        {
          if (strcasecmp (prodtype, g_ptr_array_index (production_type_names, j)) == 0)
            break;
        }
      if (j == n)
        {
          g_error ("\"%s\" is not a production type", prodtype);
        }
      #if DEBUG
        g_debug ("production type \"%s\" has priority %u", prodtype, i);
      #endif
      priority[j] = i;
    }
  self->private = (gpointer) priority;
  #if DEBUG
    g_debug ("----- EXIT new_production_type_prioritizer");
  #endif
  return self;
}

/** Implementation for by-time-waiting prioritizer. **************************/

/**
 * Compares two herd scorecards by time waiting and returns their priority
 * order.
 */
static int
adsm_time_waiting_prioritizer_compare (adsm_prioritizer_t *self,
                                       USC_scorecard_t *scorecard1,
                                       USC_scorecard_t *scorecard2)
{
  gboolean oldest_first;
  EVT_event_t *request1, *request2;
  int day1, day2;
  
  oldest_first = *((gboolean *) (self->private));
  if (oldest_first)
    {
      request1 = USC_scorecard_vaccination_request_peek_oldest (scorecard1);
      request2 = USC_scorecard_vaccination_request_peek_oldest (scorecard2);
    }
  else
    {
      request1 = USC_scorecard_vaccination_request_peek_newest (scorecard1);
      request2 = USC_scorecard_vaccination_request_peek_newest (scorecard2);
    }
  g_assert (request1 != NULL);
  g_assert (request2 != NULL);
  day1 = request1->u.request_for_vaccination.day_commitment_made;
  day2 = request2->u.request_for_vaccination.day_commitment_made;
  #if DEBUG && 0
    g_debug ("comparing time waiting (%s first) for unit \"%s\" (%i) and \"%s\" (%i)",
             oldest_first ? "oldest" : "newest",
             scorecard1->unit->official_id, day1,
             scorecard2->unit->official_id, day2);
  #endif
  return (day2 - day1) * (oldest_first ? 1 : -1);
}

static char*
adsm_time_waiting_prioritizer_to_string (adsm_prioritizer_t *self)
{
  return g_strdup("<prioritizer by time waiting>");
}

/**
 * Creates a new by-time-waiting prioritizer.
 *
 * @param oldest_first TRUE if older requests for vaccination have higher
 *   priority, FALSE if newer requests have higher priority.
 * @return a prioritizer object.
 */
static adsm_prioritizer_t *
new_time_waiting_prioritizer (gboolean oldest_first_flag)
{
  adsm_prioritizer_t *self;
  gboolean *oldest_first;

  #if DEBUG
    g_debug ("----- ENTER new_time_waiting_type_prioritizer");
  #endif

  self = g_new (adsm_prioritizer_t, 1);
  self->compare = adsm_time_waiting_prioritizer_compare;
  self->to_string = adsm_time_waiting_prioritizer_to_string;
  self->free = adsm_free_prioritizer;
  /* The private data in this type of prioritizer object is a gboolean, saying
   * whether older requests have higher priority. */
  oldest_first = g_new (gboolean, 1);
  *oldest_first = oldest_first_flag;
  self->private = (gpointer) oldest_first;
  #if DEBUG
    g_debug ("----- EXIT new_time_waiting_prioritizer");
  #endif
  return self;
}

/** Implementation for by-size prioritizer. *****************************/

/**
 * Compares two scorecards by unit size and returns their priority order.
 */
static int
adsm_size_prioritizer_compare (adsm_prioritizer_t *self,
                               USC_scorecard_t *scorecard1,
                               USC_scorecard_t *scorecard2)
{
  gboolean largest_first;
  unsigned int size1, size2;
  
  largest_first = *((gboolean *) (self->private));
  size1 = scorecard1->unit->size;
  size2 = scorecard2->unit->size;
  #if DEBUG
    g_debug ("comparing size (%s first) for unit \"%s\" (%u) and \"%s\" (%u)",
             largest_first ? "largest" : "smallest",
             scorecard1->unit->official_id, size1,
             scorecard2->unit->official_id, size2);
  #endif
  return (size1 - size2) * (largest_first ? 1 : -1);
}

static char*
adsm_size_prioritizer_to_string (adsm_prioritizer_t *self)
{
  return g_strdup("<prioritizer by size>");
}

/**
 * Creates a new by-size prioritizer.
 *
 * @param largest_first TRUE if larger units have higher priority, FALSE if
 *   smaller units have higher priority.
 * @return a prioritizer object.
 */
static adsm_prioritizer_t *
new_size_prioritizer (gboolean largest_first_flag)
{
  adsm_prioritizer_t *self;
  gboolean *largest_first;

  #if DEBUG
    g_debug ("----- ENTER new_size_prioritizer");
  #endif

  self = g_new (adsm_prioritizer_t, 1);
  self->compare = adsm_size_prioritizer_compare;
  self->to_string = adsm_size_prioritizer_to_string;
  self->free = adsm_free_prioritizer;
  /* The private data in this type of prioritizer object is a gboolean, saying
   * whether larger units have higher priority. */
  largest_first = g_new (gboolean, 1);
  *largest_first = largest_first_flag;
  self->private = (gpointer) largest_first;
  #if DEBUG
    g_debug ("----- EXIT new_size_prioritizer");
  #endif
  return self;
}

/** Implementation for by-direction prioritizer. *****************************/

/**
 * Compares two scorecards by distance from vaccination ring center and
 * returns their priority order.
 */
static int
adsm_direction_prioritizer_compare (adsm_prioritizer_t *self,
                                    USC_scorecard_t *scorecard1,
                                    USC_scorecard_t *scorecard2)
{
  gboolean outside_in;
  double distance1, distance2, diff;
  int result;
  
  outside_in = *((gboolean *) (self->private));
  if (outside_in)
    {
      distance1 = scorecard1->distance_from_vacc_ring_outside;
      distance2 = scorecard2->distance_from_vacc_ring_outside;
      #if DEBUG && 0
        g_debug ("comparing distance (outside-in) for unit \"%s\" (%.2f from edge) and \"%s\" (%.2f from edge)",
                 scorecard1->unit->official_id, distance1,
                 scorecard2->unit->official_id, distance2);
      #endif
    }
  else
    {
      distance1 = scorecard1->distance_from_vacc_ring_inside;
      distance2 = scorecard2->distance_from_vacc_ring_inside;
      #if DEBUG && 0
        g_debug ("comparing distance (inside-out) for unit \"%s\" (%.2f from edge) and \"%s\" (%.2f from edge)",
                 scorecard1->unit->official_id, distance1,
                 scorecard2->unit->official_id, distance2);
      #endif
    }
  diff = distance2 - distance1;
  if (fabs(diff) < EPSILON)
    result = 0;
  else if (diff > 0)
    result = 1;
  else
    result = -1;
  return result;
}

static char*
adsm_direction_prioritizer_to_string (adsm_prioritizer_t *self)
{
  return g_strdup("<prioritizer by direction>");
}

/**
 * Creates a new by-direction prioritizer.
 *
 * @param outside_in TRUE for outside-in order, FALSE for inside-out order.
 * @return a prioritizer object.
 */
static adsm_prioritizer_t *
new_direction_prioritizer (gboolean outside_in_flag)
{
  adsm_prioritizer_t *self;
  gboolean *outside_in;

  #if DEBUG
    g_debug ("----- ENTER new_direction_prioritizer");
  #endif

  self = g_new (adsm_prioritizer_t, 1);
  self->compare = adsm_direction_prioritizer_compare;
  self->to_string = adsm_direction_prioritizer_to_string;
  self->free = adsm_free_prioritizer;
  /* The private data in this type of prioritizer object is a gboolean, saying
   * whether units to the outside of the ring have higher priority. */
  outside_in = g_new (gboolean, 1);
  *outside_in = outside_in_flag;
  self->private = (gpointer) outside_in;
  #if DEBUG
    g_debug ("----- EXIT new_direction_prioritizer");
  #endif
  return self;
}

/*****************************************************************************/

/**
 * This function, typed as a GDestroyNotify function, frees a prioritizer.
 */
static void
free_prioritizer (gpointer data)
{
  adsm_prioritizer_t *self;
  self = (adsm_prioritizer_t *) data;
  if (self != NULL)
    self->free (self);
  return;
}

/**
 * This function, typed as required for g_ptr_array_sort_with_data(), sorts
 * an array of scorecards using a chain of prioritizers.
 *
 * @param thunk the chain (GSList *) of prioritizers
 * @param c1 the first scorecard to be compared
 * @param c2 the second scorecard to be compared
 * @return -1 if c1 has a higher priority than c2, +1 if c2 has a higher
 *   priority than c1, and 0 if their priorities are equal.
 */
gint
prioritizer_chain_compare (gconstpointer a, gconstpointer b, gpointer user_data)
{
  GSList *prioritizer_chain, *iter;
  adsm_prioritizer_t *prioritizer;
  USC_scorecard_t *scorecard1, *scorecard2;
  gint result = 0;

  #if DEBUG && 0
    g_debug ("----- ENTER prioritizer_chain_compare");
  #endif  
  prioritizer_chain = (GSList *) user_data;
  scorecard1 = *((USC_scorecard_t **) a);
  scorecard2 = *((USC_scorecard_t **) b);
  for (iter = prioritizer_chain; iter != NULL; iter = g_slist_next(iter))
    {
      prioritizer = (adsm_prioritizer_t *) (iter->data);
      #if DEBUG && 0
        g_debug ("getting prioritizer from chain");
      #endif
      result = prioritizer->compare (prioritizer, scorecard1, scorecard2);
      #if DEBUG && 0
        g_debug ("result = %i", result);
      #endif
      if (result != 0)
        break;
      /* Otherwise continue down the chain */
    }
  return result;
}



/** Specialized information for this model. */
typedef struct
{
  unsigned int nunits;          /* Number of units. */
  unsigned int nprod_types;     /* Number of production types. */

  gboolean outbreak_known; /**< TRUE once the authorities are aware of the
    outbreak; FALSE otherwise. */
  int first_detection_day; /** The day of the first detection.  Only defined if
    outbreak_known is TRUE. */

  GHashTable *scorecard_for_unit; /**< Keys are units (UNT_unit_t *), data is
    scorecards (USC_scorecard_t *). */

  /* Parameters concerning destruction. */
  int destruction_program_delay; /**< The number of days between
    recognizing and outbreak and beginning a destruction program. */
  int destruction_program_begin_day; /**< The day of the simulation on which
    the destruction program begins.  Only defined if outbreak_known is TRUE. */
  REL_chart_t *destruction_capacity; /**< The maximum number of units the
    authorities can destroy in a day. */
  gboolean destruction_capacity_goes_to_0; /**< A flag indicating that at some
    point destruction capacity drops to 0 and remains there. */
  int destruction_capacity_0_day; /**< The day on which the destruction
    capacity drops to 0.  Only defined if destruction_capacity_goes_to_0 =
    TRUE. */
  gboolean no_more_destructions; /**< A flag indicating that on this day and
    forward, there is no capacity to do destructions.  Useful for deciding
    whether a simulation can exit early even if there destructions queued up. */
  GList **destruction_status; /**< A pointer for each unit.  If the unit is not
    awaiting destruction, the pointer will be NULL.  If the unit is awaiting
    destruction, the pointer is to a node in pending_destructions.  Note that
    the pointer is to a GList structure in a GQueue; the actual
    RequestForDestruction event can be found by following the GList structure's
    "data" pointer. */
  unsigned int ndestroyed_today; /**< The number of units the authorities
    have destroyed on a given day. */
  GPtrArray *pending_destructions; /**< Prioritized lists of units to be
    destroyed.  Each item is a pointer to a GQueue, and each item in the GQueue
    is a RequestForDestruction event. */
  int destruction_prod_type_priority;
  int destruction_time_waiting_priority;
  int destruction_reason_priority;
  GHashTable *destroyed_today; /**< Records the units destroyed today.  Useful
    for ignoring new requests for destruction or vaccination coming in from
    other modules that don't know which units are being destroyed today.  The
    key is a unit pointer (UNT_unit_t *) and the value is unimportant (presence
    or absence of a key is all we ever test). */

  /* Parameters concerning vaccination. */
  int first_detection_day_for_vaccination; /** The day of the first detection.
    Starts at -1, is changed to a value > 0 when the first detection occurs,
    and is reset to -1 if the vaccination program is terminated. */
  gboolean vaccination_active;
  guint vaccination_program_initiation_count; /**< This value starts at 0, and
    is incremented each time the vaccination program is initiated. */
  int vaccination_retrospective_days;
  int vaccination_initiated_day; /**< This value starts as -1, and is set on the day that
    the vaccination_active flag is set to TRUE.  Its value will be the day before
    the first vaccinations happen. */
  int vaccination_terminated_day; /**< This value starts as -1, and is set on the day
    that the vaccination_active flag is set to FALSE.  Its value will be the day on which
    the last vaccination happen. */
  REL_chart_t *vaccination_capacity; /**< The maximum number of units the
    authorities can vaccinate in a day. */
  REL_chart_t *vaccination_capacity_on_restart; /**< The maximum number of
    units the authorities can vaccinate in a day. Chart for the second (and
    subsequent) times the vaccination program is initiated, when ramp-up of
    resources may be faster. */
  int base_day_for_vaccination_capacity; /** The day that corresponds to x=0
    on the vaccination capacity chart. See the function
    handle_request_to_initiate_vaccination_event for detailed notes on how this
    base day is set. */
  gboolean vaccination_capacity_goes_to_0; /**< A flag indicating that at some
    point vaccination capacity drops to 0 and remains there. */
  int vaccination_capacity_0_day; /**< The day on which the vaccination
    capacity drops to 0.  Only defined if vaccination_capacity_goes_to_0 =
    TRUE. */
  gboolean no_more_vaccinations; /**< A flag indicating that on this day and
    forward, there is no capacity to do vaccinations.  Useful for deciding
    whether a simulation can exit early even if there vaccinations queued up. */
  unsigned int nvaccinated_today; /**< The number of units the
    authorities have vaccinated on a given day. */
  gboolean *cancel_vaccination_on_detection; /**< An array with one entry per
    production type */
  int *day_last_vaccinated; /**< Records the day when each unit
   was last vaccinated.  Also prevents double-counting units against the
   vaccination capacity. */

  /* Parameters used to prioritize vaccination. */
  GSList *vaccination_prioritizers; /**< Each item is a (naadsm_prioritizer_t *). */
  gboolean round_robin; /**< Whether to divide resources between active foci. */
  gboolean first_round_robin; /**< TRUE when a vaccination program starts or
    re-starts. */
  GPtrArray *active_vaccination_rings; /**< A list of active vaccination rings
    (USC_vaccination_ring_t *). */
  guint current_vaccination_ring; /**< An index into active_vaccination_rings.
    It loops around that list to implement round-robin priority. */
  GHashTable *round_robin_buckets; /**< A set of "buckets" used to sort
    scorecards into vaccination rings during round-robin scheduling. The keys
    are units (UNT_unit_t *) -- the same ones found in active_vaccination_rings --
    and the associated values are GQueues of scorecards. Within each GQueue,
    the highest-priority scorecards are at the top. */
  GHashTable *vaccination_set; /**< A hash table storing the set of units
    currently awaiting vaccination. Keys are units (UNT_unit_t *), associated
    values are scorecards. */
  GPtrArray *scorecards_sorted; /**< An array containing the scorecards of
    herds currently awaiting vaccination. The array is maintained in sorted
    order, with the highest-priority herds at the end. */
  GHashTable *removed_from_vaccination_set_today; /**< A hash table storing
    units that have been removed from the hash table vaccination_set but have
    not yet been removed from the list scorecards_sorted.  Keeping this
    information around enables us to use a fast once-a-day sweep to remove
    scorecards from the sorted list (the function clean_up_scorecard_list)
    while still keeping the list in sorted order. */

  guint *min_time_between_vaccinations; /**< An array with one entry per
    production type */
  int *min_next_vaccination_day;
}
local_data_t;



/**
 * Retrieves the scorecard for a unit. Returns NULL if there is currently no
 * scorecard for the unit.
 */
static USC_scorecard_t *
get_scorecard_for_unit (struct adsm_module_t_ *self, UNT_unit_t * unit)
{
  local_data_t *local_data;
  local_data = (local_data_t *) (self->model_data);
  return (USC_scorecard_t *) g_hash_table_lookup (local_data->scorecard_for_unit, unit);
}



/**
 * Retrieves the scorecard for a unit, creating one if it doesn't already
 * exist.
 */
static USC_scorecard_t *
get_or_make_scorecard_for_unit (struct adsm_module_t_ *self, UNT_unit_t * unit)
{
  local_data_t *local_data;
  gpointer p;
  USC_scorecard_t *scorecard;

  local_data = (local_data_t *) (self->model_data);
  p = g_hash_table_lookup (local_data->scorecard_for_unit, unit);
  if (p == NULL)
    {
      scorecard = USC_new_scorecard (unit);
      g_hash_table_insert (local_data->scorecard_for_unit, unit, scorecard);
    }
  else
    scorecard = (USC_scorecard_t *) p;

  return scorecard;
}



/**
 * Cancels vaccinations for a unit.
 *
 * @param self this module.
 * @param unit a unit.
 * @param day the current simulation day.
 * @param older_than only delete vaccination requests older than this number of
 *   days. This is how "retrospective" vaccination is accomplished. If 0, all
 *   vaccination requests are deleted.
 * @param queue for any new events the function creates.
 */
void
cancel_vaccination (struct adsm_module_t_ *self,
                    UNT_unit_t * unit, int day,
                    int older_than,
                    EVT_event_queue_t * queue)
{
  local_data_t *local_data;
  USC_scorecard_t *scorecard;
  EVT_event_t *request;
  EVT_request_for_vaccination_event_t *details;
  EVT_event_t *cancellation_event;
  
#if DEBUG
  g_debug ("----- ENTER cancel_vaccination (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* If the unit is on the vaccination waiting list, remove the vaccination requests. */
  scorecard = get_scorecard_for_unit (self, unit);
  if (scorecard != NULL && scorecard->is_awaiting_vaccination)
    {
      while (TRUE)
        {
          request = USC_scorecard_vaccination_request_peek_oldest (scorecard);
          if (request == NULL)
            break; /* no more vaccination requests to process */
          details = &(request->u.request_for_vaccination);
          /* Stop the loop if we have reached the most recent vaccination
           * requests, the ones newer than the argument "older_than". The
           * day>0 condition is needed here because this function is called
           * when resetting this module, when day=0, and we want the loop to
           * remove all the vaccination requests in that case. */
          if (day > 0 && (day - details->day_commitment_made) <= older_than)
            break; /* no more in the right date range to process */
          USC_scorecard_vaccination_request_pop_oldest (scorecard);

          /* Now the vaccination request is removed from the scorecard.  Send out
           * a cancellation message, then free the request object. */
          cancellation_event = EVT_new_vaccination_canceled_event (unit, day, details->day_commitment_made);
          EVT_free_event (request);
          if (queue != NULL)
            EVT_event_enqueue (queue, cancellation_event);
        }
      if (request == NULL) /* means that list of vaccination requests was found to be empty above */
        {
          g_hash_table_remove (local_data->vaccination_set, unit);
          g_hash_table_insert (local_data->removed_from_vaccination_set_today, unit, GINT_TO_POINTER(1));
        }
    }

#if DEBUG
  g_debug ("----- EXIT cancel_vaccination (%s)", MODEL_NAME);
#endif
  return;
}



void
destroy (struct adsm_module_t_ *self, UNT_unit_t * unit,
         int day, ADSM_control_reason reason, int day_commitment_made,
         EVT_event_queue_t * queue)
{
  local_data_t *local_data;

#if DEBUG
  g_debug ("----- ENTER destroy (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* Destroy the unit. */

  /* If the unit is already Destroyed, it should not be destroyed again. */
  g_assert (unit->state != Destroyed);

#if DEBUG
  g_debug ("destroying unit \"%s\"", unit->official_id);
#endif
  UNT_destroy (unit);
  EVT_event_enqueue (queue, EVT_new_destruction_event (unit, day, reason, day_commitment_made));
  g_hash_table_insert (local_data->destroyed_today, unit, unit);
  local_data->ndestroyed_today++;

  /* Take the unit off the vaccination waiting list, if needed. */
  cancel_vaccination (self, unit, day, /* older_than = */ 0, queue);

#if DEBUG
  g_debug ("----- EXIT destroy (%s)", MODEL_NAME);
#endif
  return;
}



void
destroy_by_priority (struct adsm_module_t_ *self, int day,
                     EVT_event_queue_t * queue)
{
  local_data_t *local_data;
  unsigned int destruction_capacity;
  EVT_event_t *pending_destruction;
  EVT_request_for_destruction_event_t *details;
  unsigned int npriorities;
  unsigned int priority;
  int request_day, oldest_request_day;
  int oldest_request_index;
  GQueue *q;

#if DEBUG
  g_debug ("----- ENTER destroy_by_priority (%s)", MODEL_NAME);
#endif

  /* Eliminate compiler warnings about uninitialized values */
  oldest_request_day = INT_MAX;

  local_data = (local_data_t *) (self->model_data);

  /* Look up the destruction capacity (which may increase as the outbreak
   * progresses). */
  destruction_capacity =
    (unsigned int)
    round (REL_chart_lookup
           (day - local_data->first_detection_day - 1, local_data->destruction_capacity));

  /* Check whether the destruction capacity has dropped to 0 for good. */
  if (local_data->destruction_capacity_goes_to_0
      && (day - local_data->first_detection_day - 1) >=
      local_data->destruction_capacity_0_day)
    {
      local_data->no_more_destructions = TRUE;
#if DEBUG
      g_debug ("no more destructions after this day");
#endif
    }

  /* We use the destruction lists in different ways according to the user-
   * specified priority scheme.
   *
   * If time waiting has first priority,
   */
  if (local_data->destruction_time_waiting_priority == 1)
    {
      npriorities = local_data->pending_destructions->len;
      while (local_data->ndestroyed_today < destruction_capacity)
        {
          /* Find the unit that has been waiting the longest.  Favour units
           * higher up in the lists. */
          oldest_request_index = -1;
          for (priority = 0; priority < npriorities; priority++)
            {
              q = (GQueue *) g_ptr_array_index (local_data->pending_destructions, priority);
              if (g_queue_is_empty (q))
                continue;

              pending_destruction = (EVT_event_t *) g_queue_peek_head (q);

              /* When we put the destruction on the waiting list, we stored the
               * day it was requested. */
              request_day = pending_destruction->u.request_for_destruction.day;
              if (oldest_request_index == -1 || request_day < oldest_request_day)
                {
                  oldest_request_index = priority;
                  oldest_request_day = request_day;
                }
            }
          /* If we couldn't find any request that can be carried out today,
           * stop the loop. */
          if (oldest_request_index < 0)
            break;

          q = (GQueue *) g_ptr_array_index (local_data->pending_destructions, oldest_request_index);
          pending_destruction = (EVT_event_t *) g_queue_pop_head (q);
          details = &(pending_destruction->u.request_for_destruction);
          local_data->destruction_status[details->unit->index] = NULL;

          destroy (self, details->unit, day, details->reason, details->day_commitment_made, queue);
          EVT_free_event (pending_destruction);
        }
    }                           /* end case where time waiting has 1st priority. */

  else if (local_data->destruction_time_waiting_priority == 2)
    {
      int start, end, step;

      npriorities = local_data->pending_destructions->len;
      if (local_data->destruction_prod_type_priority == 1)
        step = ADSM_NCONTROL_REASONS;
      else
        step = local_data->nprod_types;
      start = 0;
      end = MIN (start + step, npriorities);

      while (local_data->ndestroyed_today < destruction_capacity)
        {
          /* Find the unit that has been waiting the longest.  Favour units
           * higher up in the lists. */
          oldest_request_index = -1;
          for (priority = start; priority < end; priority++)
            {
              q = (GQueue *) g_ptr_array_index (local_data->pending_destructions, priority);
              if (g_queue_is_empty (q))
                continue;

              pending_destruction = (EVT_event_t *) g_queue_peek_head (q);

              /* When we put the destruction on the waiting list, we stored the
               * day it was requested. */
              request_day = pending_destruction->u.request_for_destruction.day;
              if (oldest_request_index == -1 || request_day < oldest_request_day)
                {
                  oldest_request_index = priority;
                  oldest_request_day = request_day;
                }
            }
          /* If we couldn't find any request that can be carried out today,
           * advance to the next block of lists. */
          if (oldest_request_index < 0)
            {
              start += step;
              if (start >= npriorities)
                break;
              end = MIN (start + step, npriorities);
              continue;
            }

          q = (GQueue *) g_ptr_array_index (local_data->pending_destructions, oldest_request_index);
          pending_destruction = (EVT_event_t *) g_queue_pop_head (q);
          details = &(pending_destruction->u.request_for_destruction);
          local_data->destruction_status[details->unit->index] = NULL;

          destroy (self, details->unit, day, details->reason, details->day_commitment_made, queue);
          EVT_free_event (pending_destruction);
        }
    }                           /* end case where time waiting has 2nd priority. */

  else
    {
      npriorities = local_data->pending_destructions->len;
      for (priority = 0;
           priority < npriorities && local_data->ndestroyed_today < destruction_capacity;
           priority++)
        {
          q = (GQueue *) g_ptr_array_index (local_data->pending_destructions, priority);
#if DEBUG
          if (!g_queue_is_empty (q))
            g_debug ("destroying priority %i units", priority + 1);
#endif
          while (!g_queue_is_empty (q) && local_data->ndestroyed_today < destruction_capacity)
            {
              pending_destruction = (EVT_event_t *) g_queue_pop_head (q);
              details = &(pending_destruction->u.request_for_destruction);
              local_data->destruction_status[details->unit->index] = NULL;

              destroy (self, details->unit, day, details->reason, details->day_commitment_made, queue);
              EVT_free_event (pending_destruction);
            }
        }
    }                           /* end case where time waiting has 3rd priority. */

#if DEBUG
  g_debug ("----- EXIT destroy_by_priority (%s)", MODEL_NAME);
#endif
}



static void
clean_up_scorecard_list (GHashTable *vaccination_set, GPtrArray *scorecards_sorted)
{
  gboolean writing;
  guint length, read_index, write_index;
  USC_scorecard_t *scorecard;

  #if DEBUG
    g_debug ("----- ENTER clean_up_scorecard_list");
  #endif

  read_index = write_index = 0;
  writing = FALSE;
  length = scorecards_sorted->len;
  while (read_index < length)
    {
      scorecard = (USC_scorecard_t *) g_ptr_array_index (scorecards_sorted, read_index);
      if (scorecard->is_awaiting_vaccination)
        {
          if (writing)
            {
              g_ptr_array_index (scorecards_sorted, write_index) = scorecard;
              write_index++;
            }
        }
      else
        {
          #if DEBUG
            g_debug ("removing unit \"%s\"", scorecard->unit->official_id);
          #endif
          g_hash_table_remove (vaccination_set, scorecard->unit);
          /* We have found at least 1 scorecard to remove, so set the "writing"
           * flag to TRUE. */
          if (!writing)
            {
              writing = TRUE;
              write_index = read_index;
            }
        }
      read_index++;
    }
  if (writing)
    g_ptr_array_set_size (scorecards_sorted, write_index);

  g_assert (g_hash_table_size (vaccination_set) == scorecards_sorted->len);

  #if DEBUG
    g_debug ("removed %i scorecards", length - scorecards_sorted->len);
  #endif

  #if DEBUG
    g_debug ("----- EXIT clean_up_scorecard_list");
  #endif

  return;
}



void
vaccinate (struct adsm_module_t_ *self, UNT_unit_t * unit,
           int day, ADSM_control_reason reason, int day_commitment_made,
           EVT_event_queue_t * queue)
{
  local_data_t *local_data;
  unsigned int last_vaccination, days_since_last_vaccination;

#if DEBUG
  g_debug ("----- ENTER vaccinate (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* If the unit is already Destroyed, it should not be vaccinated. */
  g_assert (unit->state != Destroyed);

  /* If the unit has already been vaccinated recently, we can ignore the
   * request. */
  if (day < local_data->min_next_vaccination_day[unit->index])
    {
      last_vaccination = local_data->day_last_vaccinated[unit->index];
      days_since_last_vaccination = day - last_vaccination;
#if DEBUG
      g_debug ("unit \"%s\" was vaccinated %u days ago, will not re-vaccinate",
               unit->official_id, days_since_last_vaccination);
#endif
      EVT_event_enqueue (queue, EVT_new_vaccination_canceled_event (unit, day, day_commitment_made));
      goto end;
    }

  /* Vaccinate the unit. */
#if DEBUG
  g_debug ("vaccinating unit \"%s\"", unit->official_id);
#endif
  EVT_event_enqueue (queue, EVT_new_vaccination_event (unit, day, reason, day_commitment_made));
  local_data->nvaccinated_today++;
  local_data->min_next_vaccination_day[unit->index] = day + local_data->min_time_between_vaccinations[unit->production_type];

end:
#if DEBUG
  g_debug ("----- EXIT vaccinate (%s)", MODEL_NAME);
#endif
  return;
}



/**
 * The function g_queue_clear, but matching the GHFunc prototype. Used in the
 * function empty_round_robin_buckets to empty the buckets of scorecards.
 */
static void
g_queue_clear_as_GHFunc (gpointer key, gpointer value, gpointer user_data)
{
  g_queue_clear ((GQueue *)value);
}



/**
 * Removes all items from the GQueues (but does not free the GQueues themselves)
 * in the buckets of scorecards used for round-robin priority.
 */
static void
empty_round_robin_buckets (GHashTable *round_robin_buckets)
{
  g_hash_table_foreach (round_robin_buckets, g_queue_clear_as_GHFunc, NULL);
  return;
}



/**
 * Looks through a list of USC_vaccination_ring_t objects and returns the index
 * of the one that is centered on the given unit.
 *
 * @param rings a GPtrArray containing USC_vaccination_ring_t pointers.
 * @param unit the unit to look for
 * @return the index at which the ring centered on the given unit is found.
 *   If no such ring is found, this will equal rings->len (an illegal location).
 */
static guint
find_vaccination_ring_with_unit (GPtrArray *rings, UNT_unit_t *unit)
{
  USC_vaccination_ring_t *ring;
  guint loc;
  for (loc = 0; loc < rings->len; loc ++)
    {
      ring = (USC_vaccination_ring_t *) g_ptr_array_index (rings, loc);
      if (ring->unit_at_center == unit)
        break;
    }
  return loc;
}



/**
 * Counts how many units in vaccination_set are assigned to each ring in
 * active_vaccination_rings.  This is part of the process of expiring finished
 * rings.  Typed as a GHFunc so that it can be used with the foreach function
 * of a GHashTable.
 *
 * @param key a unit (UNT_unit_t *), cast to a gpointer. Not used.
 * @param value a scorecard (USC_scorecard_t *), cast to a gpointer
 * @param user_data a GHashTable where key = unit at center of vaccination ring
 *   and value = count of units currently assigned to the ring (as
 *   GUINT_TO_POINTER)
 */
void
count_units_in_active_vaccination_rings (gpointer key,
                                         gpointer value,
                                         gpointer user_data)
{
  USC_scorecard_t *scorecard;
  GHashTable *ring_count;
  guint count;

  scorecard = value;
  ring_count = user_data;
  if (g_hash_table_contains (ring_count, scorecard->unit_at_vacc_ring_center))
    {
      count = 1 +
        GPOINTER_TO_UINT (g_hash_table_lookup (ring_count,
                                               scorecard->unit_at_vacc_ring_center));
    }
  else
    {
      count = 1;
    }
  g_hash_table_insert (ring_count, scorecard->unit_at_vacc_ring_center,
                       GUINT_TO_POINTER (count));
  return;  
}



void
vaccinate_by_priority (struct adsm_module_t_ *self, int day,
                       EVT_event_queue_t * queue)
{
  local_data_t *local_data;
  REL_chart_t *capacity_chart;
  unsigned int vaccination_capacity;
  guint nscorecards;
  guint i;
  USC_scorecard_t *scorecard;

#if DEBUG
  g_debug ("----- ENTER vaccinate_by_priority (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* Look up the vaccination capacity (which may increase as the outbreak
   * progresses). */
  if (local_data->vaccination_program_initiation_count <= 1)
    capacity_chart = local_data->vaccination_capacity;
  else
    capacity_chart = local_data->vaccination_capacity_on_restart;
  vaccination_capacity =
    (unsigned int)
    round (REL_chart_lookup
           (day - local_data->base_day_for_vaccination_capacity - 1, capacity_chart));

  /* Check whether the vaccination capacity has dropped to 0 for good. */
  if (local_data->vaccination_capacity_goes_to_0
      && (day - local_data->base_day_for_vaccination_capacity) >=
      local_data->vaccination_capacity_0_day)
    {
      local_data->no_more_vaccinations = TRUE;
#if DEBUG
      g_debug ("no more vaccinations after this day");
#endif
    }

  clean_up_scorecard_list (local_data->vaccination_set, local_data->scorecards_sorted);
  g_hash_table_remove_all (local_data->removed_from_vaccination_set_today);
  nscorecards = g_hash_table_size (local_data->vaccination_set);
  if (vaccination_capacity > 0 && nscorecards > 0)
    {
      /* Sort the list of scorecards into priority order. */
      g_assert (local_data->scorecards_sorted->len == nscorecards);
      #if DEBUG
        g_debug ("%u units on vaccination list", nscorecards);
      #endif
      #if DEBUG
        g_debug ("sorting the list");
      #endif
      g_ptr_array_sort_with_data (local_data->scorecards_sorted,
                                  prioritizer_chain_compare,
                                  (gpointer) (local_data->vaccination_prioritizers));
      #if DEBUG
        g_debug ("done sorting the list");
      #endif

      /* The scorecards of herds awaiting vaccination are now sorted into
       * priority order, with the highest-priority ones at the end.  Now do
       * the vaccinations.  There are 2 cases below, the simple case where we
       * process the list from highest-priority to lowest-priority, and the
       * more complicated round-robin case where we share resources between
       * active vaccination rings. */
      i = 0; /* Index _backwards_ into priority list (we process from the end). */
      if (local_data->round_robin == FALSE)
        {
          while (local_data->nvaccinated_today < vaccination_capacity
             && i < nscorecards)
            {
              UNT_unit_t *unit;
              EVT_event_t *request;
              EVT_request_for_vaccination_event_t *details;

              scorecard = g_ptr_array_index (local_data->scorecards_sorted, nscorecards - 1 - i);
              unit = scorecard->unit;
              if (scorecard->distance_from_vacc_ring_outside < DBL_MAX)
                {
                  request = USC_scorecard_vaccination_request_pop_oldest (scorecard);
                  g_assert (request != NULL);
                  details = &(request->u.request_for_vaccination);
                  vaccinate (self, details->unit, day, details->reason,
                             details->day_commitment_made, queue);

                  /* If this scorecard contains no more requests for vaccination,
                   * then we can remove it from the vaccination set. */
                  if (USC_scorecard_vaccination_request_peek_oldest (scorecard) == NULL)
                    {
                      g_hash_table_remove (local_data->vaccination_set, unit);
                      g_hash_table_insert (local_data->removed_from_vaccination_set_today, unit, GINT_TO_POINTER(1));
                    }
                }
              else
                {
                  /* This unit was found to be inside the hole in a vaccination
                   * ring. Remove it from the vaccination set. */
                  #if DEBUG
                    g_debug ("unit \"%s\" found to be inside the hole in a vaccination ring",
                             unit->official_id);
                  #endif
                  cancel_vaccination (self, unit, day, /* older_than = */ 0, queue);
                }

              i += 1;      
            } /* end of loop to do vaccinations */
        } /* end of case with no round-robin */
      else
        {
          UNT_unit_t *desired_focus;
          guint bucket_count = 0;
    
          /* Round-robin priority */
          empty_round_robin_buckets (local_data->round_robin_buckets);
          bucket_count = 0;
          /* Initialize which ring we want a unit from. If we only just
           * started (or re-started) the vaccination program, pick the ring
           * containing the highest-priority unit to begin. */
          if (local_data->first_round_robin)
            {
              if (i < nscorecards)
                {
                  g_assert (local_data->active_vaccination_rings->len > 0);
                  scorecard = g_ptr_array_index (local_data->scorecards_sorted, nscorecards - 1 - i);
                  local_data->current_vaccination_ring = 
                    find_vaccination_ring_with_unit (local_data->active_vaccination_rings, scorecard->unit_at_vacc_ring_center);
                  g_assert (local_data->current_vaccination_ring < local_data->active_vaccination_rings->len);
                }
              else
                local_data->current_vaccination_ring = 0;
              local_data->first_round_robin = FALSE;
            }
          desired_focus = ((USC_vaccination_ring_t *)
            g_ptr_array_index (local_data->active_vaccination_rings,
                               local_data->current_vaccination_ring))->unit_at_center;
          #if DEBUG
            g_debug ("want a unit in ring around unit \"%s\" (focus %u)",
                     desired_focus->official_id,
                     local_data->current_vaccination_ring);
          #endif
          while (local_data->nvaccinated_today < vaccination_capacity
                 && (i < nscorecards || bucket_count > 0))
            {
              gboolean found;
              GQueue *bucket;
              UNT_unit_t *unit;
              EVT_event_t *request;
              EVT_request_for_vaccination_event_t *details;

              found = FALSE;
              /* Do we have a scorecard waiting in the bucket for that ring? */
              bucket =
                (GQueue *) g_hash_table_lookup (local_data->round_robin_buckets,
                                                desired_focus);
              if (bucket != NULL)
                {
                  scorecard = g_queue_pop_head (bucket);
                  if (scorecard != NULL)
                    {
                      /* Yes - hold on to that scorecard, we will use it below */
                      bucket_count--;
                      found = TRUE;
                      #if DEBUG
                        g_debug ("took one from the bucket for unit \"%s\" (bucket count now %u)",
                                 desired_focus->official_id,
                                 bucket_count);
                      #endif
                    }
                }
                    
              /* If not, is the scorecard at position i in the priority list in
               * the desired ring? */
              if (!found)
                {
                  if (i < nscorecards)
                    {
                      scorecard = g_ptr_array_index (local_data->scorecards_sorted, nscorecards - 1 - i);
                      if (scorecard->unit_at_vacc_ring_center == desired_focus)
                        {
                          /* Yes - hold on to that scorecard, we will use it below */
                          found = TRUE;
                          #if DEBUG
                            g_debug ("found one at position %u from end", i);
                          #endif
                          i++;
                        }
                    }
                }

              /* If one of those 2 lookups worked, process that scorecard. */
              if (found)
                {
                  unit = scorecard->unit;
                  if (scorecard->distance_from_vacc_ring_outside < DBL_MAX)
                    {
                      request = USC_scorecard_vaccination_request_pop_oldest (scorecard);
                      g_assert (request != NULL);
                      details = &(request->u.request_for_vaccination);
                      vaccinate (self, details->unit, day, details->reason,
                                 details->day_commitment_made, queue);

                      /* If this scorecard contains no more requests for vaccination,
                       * then we can remove it from the vaccination set. */
                      if (USC_scorecard_vaccination_request_peek_oldest (scorecard) == NULL)
                        {
                          g_hash_table_remove (local_data->vaccination_set, unit);
                          g_hash_table_insert (local_data->removed_from_vaccination_set_today, unit, GINT_TO_POINTER(1));
                        }
                      /* Advance which ring we want a unit from. */
                      local_data->current_vaccination_ring =
                        (local_data->current_vaccination_ring + 1) % (local_data->active_vaccination_rings->len);
                      desired_focus = ((USC_vaccination_ring_t *)
                        g_ptr_array_index (local_data->active_vaccination_rings,
                                           local_data->current_vaccination_ring))->unit_at_center;
                      #if DEBUG
                        g_debug ("want a unit in ring around unit \"%s\" (focus %u)",
                                 desired_focus->official_id,
                                 local_data->current_vaccination_ring);
                      #endif
                    }
                  else
                    {
                      /* This unit was found to be inside the hole in a vaccination
                       * ring. Remove it from the vaccination set. */
                      #if DEBUG
                        g_debug ("unit \"%s\" found to be inside the hole in a vaccination ring",
                                 unit->official_id);
                      #endif
                      cancel_vaccination (self, unit, day, /* older_than = */ 0, queue);
                    }
                }
              else
                {
                  /* If neither of the lookups worked, then there are 2 choices:
                   * 1 - If we haven't gone all the way down the priority list
                   *     yet, then we put the scorecard at the current position
                   *     into the bucket for the ring it belongs to, and keep
                   *     going down the priority list, looking for a scorecard
                   *     in the desired ring.
                   * 2 - If we *have* gone all the way down the priority list,
                   *     then the only scorecards remaining to look at are the
                   *     ones in the buckets, and we have clearly run out of
                   *     scorecards in the desired ring, because we checked
                   *     that bucket just a moment ago. So we advance to the
                   *     next ring in round-robin sequence.
                   */
                  if (i < nscorecards)
                    {
                      scorecard = g_ptr_array_index (local_data->scorecards_sorted, nscorecards - 1 - i);
                      bucket = (GQueue *)
                        g_hash_table_lookup (local_data->round_robin_buckets,
                                             scorecard->unit_at_vacc_ring_center);
                      g_assert (bucket != NULL);
                      g_queue_push_tail (bucket, scorecard);
                      bucket_count++;
                      #if DEBUG
                        g_debug ("scorecard at position %u from end is in ring around \"%s\", putting scorecard in bucket (bucket count now %u)",
                                 i, scorecard->unit_at_vacc_ring_center->official_id,
                                 bucket_count);
                      #endif
                      i++;
                    }
                  else
                    {
                      UNT_unit_t *old_desired_focus;
                      /* Advance which ring we want a unit from. */
                      old_desired_focus = desired_focus;
                      local_data->current_vaccination_ring =
                        (local_data->current_vaccination_ring + 1) % (local_data->active_vaccination_rings->len);
                      desired_focus = ((USC_vaccination_ring_t *)
                        g_ptr_array_index (local_data->active_vaccination_rings,
                                           local_data->current_vaccination_ring))->unit_at_center;
                      #if DEBUG
                        g_debug ("no units left around unit \"%s\", now want a unit in ring around unit \"%s\"",
                                 old_desired_focus->official_id,
                                 desired_focus->official_id);
                      #endif
                    }   
                }
            } /* end of while loop over all capacity or all waiting units */
        } /* end of case with round-robin */        

      /* Now expire any rings in active_vaccination_rings that no longer
       * contain any units. */
      if (local_data->active_vaccination_rings->len > 0)
        {
          GHashTable *ring_count; /**< Key = unit at center, value = count of
            units as GUINT_TO_POINTER. */
          #if DEBUG
            g_debug ("looking for expired vaccination rings");
          #endif
          ring_count = g_hash_table_new (g_direct_hash, g_direct_equal);
          g_hash_table_foreach (local_data->vaccination_set,
                                count_units_in_active_vaccination_rings,
                                ring_count);
          /* Step backwards over the active_vaccination_rings array, deleting any
           * expired ones. */
          i = local_data->active_vaccination_rings->len - 1;
          while (TRUE)
            {
              USC_vaccination_ring_t *ring;
              ring = g_ptr_array_index (local_data->active_vaccination_rings, i);
              if (!g_hash_table_contains (ring_count, ring->unit_at_center))
                {
                  /* This ring has expired. */
                  #if DEBUG
                    g_debug ("vaccination ring around unit \"%s\" has expired, removing",
                             ring->unit_at_center->official_id);
                  #endif
                  g_ptr_array_remove_index (local_data->active_vaccination_rings, i);
                  /* This g_ptr_array has a destroy function defined, so the
                   * USC_vaccination_ring_t object will be properly freed by
                   * the remove_index function. */
                }
              else
                {
                  #if DEBUG
                    g_debug ("vaccination ring around unit \"%s\" still contains %u units",
                             ring->unit_at_center->official_id,
                             GPOINTER_TO_UINT (g_hash_table_lookup (ring_count,
                                                                    ring->unit_at_center)));
                  #endif
                  ;
                }
              if (i == 0)
                break;
              else
                i--;
            }
          g_hash_table_destroy (ring_count);
          /* Make sure we didn't just leave current_vaccination_ring past the
           * end of the array */
          if (local_data->active_vaccination_rings->len > 0
              && local_data->current_vaccination_ring >= local_data->active_vaccination_rings->len)
            {
              local_data->current_vaccination_ring = 0;
            }
        } /* end of deleting expired vaccination rings */

    } /* end of if vaccination capacity > 0 */

#if DEBUG
  g_debug ("----- EXIT vaccinate_by_priority (%s)", MODEL_NAME);
#endif
}



/**
 * Removes all pending vaccination from the queues.  If queue is not NULL,
 * issues VaccinationCanceled events.  (This function is called when resetting
 * or freeing the module, and in those cases we don't need it to send events to
 * the event queue.)
 */
static void
clear_all_pending_vaccinations (struct adsm_module_t_ *self,
                                int day,
                                EVT_event_queue_t *queue)
{
  local_data_t *local_data;
  GList *units_awaiting_vaccination, *iter;
  UNT_unit_t *unit;

  #if DEBUG
    g_debug ("----- ENTER clear_all_pending_vaccinations (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);

  /* Units that are awaiting vaccination are present as keys in
   * local_data->vaccination_set.  Get a list of those units and call
   * cancel_vaccination on each of them.  (Can't use g_hash_table_foreach in
   * this case because cancel_vaccination modifies the hash table.) */
  units_awaiting_vaccination = g_hash_table_get_keys (local_data->vaccination_set);
  #if DEBUG
    g_debug ("%u units in vaccination_set", g_list_length (units_awaiting_vaccination));
  #endif
  for (iter = g_list_first (units_awaiting_vaccination) ;
       iter != NULL ;
       iter = g_list_next (iter))
    {
      unit = (UNT_unit_t *)(iter->data);
      #if DEBUG
        g_debug ("unit \"%s\"", unit->official_id);
      #endif
      cancel_vaccination (self, unit, day,
                          local_data->vaccination_retrospective_days,
                          queue);
    }
  g_list_free (units_awaiting_vaccination);
  #if DEBUG
    g_debug ("----- EXIT clear_all_pending_vaccinations (%s)", MODEL_NAME);
  #endif
  return;
}



/**
 * Before each simulation, this module sets "outbreak known" to no and deletes
 * any queued vaccinations or destructions left over from a previous iteration.
 *
 * @param self this module.
 */
void
handle_before_each_simulation_event (struct adsm_module_t_ *self)
{
  local_data_t *local_data;
  unsigned int npriorities;
  GQueue *q;
  int i;

  local_data = (local_data_t *) (self->model_data);

  #if DEBUG
    g_debug ("----- ENTER handle_before_each_simulation_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);
  local_data->outbreak_known = FALSE;
  local_data->destruction_program_begin_day = 0;

  npriorities = local_data->pending_destructions->len;
  for (i = 0; i < local_data->nunits; i++)
    local_data->destruction_status[i] = NULL;
  local_data->ndestroyed_today = 0;
  for (i = 0; i < npriorities; i++)
    {
      q = (GQueue *) g_ptr_array_index (local_data->pending_destructions, i);
      while (!g_queue_is_empty (q))
        EVT_free_event (g_queue_pop_head (q));
    }
  local_data->no_more_destructions = FALSE;
  g_hash_table_remove_all (local_data->destroyed_today);

  local_data->first_detection_day_for_vaccination = -1;
  local_data->vaccination_program_initiation_count = 0;
  local_data->vaccination_active = FALSE;
  local_data->vaccination_initiated_day = -1;
  local_data->vaccination_terminated_day = -1;
  /* Empty the prioritized pending vaccinations lists. */
  clear_all_pending_vaccinations (self, /* day = */ 0, /* event queue = */ NULL);
  g_ptr_array_set_size (local_data->scorecards_sorted, 0);
  g_hash_table_remove_all (local_data->removed_from_vaccination_set_today);
  local_data->nvaccinated_today = 0;

  /* Note that clearing out scorecard_for_unit has to be done after calling
   * clear_all_pending_vaccinations. */
  g_hash_table_remove_all (local_data->scorecard_for_unit);

  for (i = 0; i < local_data->nunits; i++)
    {
      local_data->day_last_vaccinated[i] = 0;
      local_data->min_next_vaccination_day[i] = 0;
    }
  local_data->no_more_vaccinations = FALSE;
  /* The active_vaccination_rings GPtrArray has a free function defined, so
   * the USC_vaccination_ring_t objects it stores will be properly disposed of
   * when the array is truncated to zero size. */
  g_ptr_array_set_size (local_data->active_vaccination_rings, 0);
  g_hash_table_remove_all (local_data->round_robin_buckets);

  #if DEBUG
    g_debug ("----- EXIT handle_before_each_simulation_event (%s)", MODEL_NAME);
  #endif

  return;
}



/**
 * Responds to a new day event by carrying out any queued destructions or
 * vaccinations.
 *
 * @param self the model.
 * @param event a new day event.
 * @param units a unit list.
 * @param queue for any new events the model creates.
 */
void
handle_new_day_event (struct adsm_module_t_ *self,
                      EVT_new_day_event_t * event,
                      UNT_unit_list_t * units,
                      EVT_event_queue_t * queue)
{
  local_data_t *local_data;

#if DEBUG
  g_debug ("----- ENTER handle_new_day_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  g_hash_table_remove_all (local_data->destroyed_today);

  /* Destroy any waiting units, as many as possible before destruction capacity
   * runs out. */
  local_data->ndestroyed_today = 0;
  if (local_data->outbreak_known && (event->day >= local_data->destruction_program_begin_day))
    destroy_by_priority (self, event->day, queue);

  local_data->nvaccinated_today = 0;
  if (local_data->vaccination_active == FALSE)
    {
      /* If we haven't initiated a vaccination program yet, remove any
       * requests for vaccination that happened as a result of detections
       * yesterday. */
      #if DEBUG
        g_debug ("vaccination program not initiated yet, deleting yesterday's requests to vaccinate");
      #endif
      clear_all_pending_vaccinations (self, event->day, queue);
    }
  else
    {
      /* Vaccinate any waiting units, as many as possible before vaccination
       * capacity runs out. */
      vaccinate_by_priority (self, event->day, queue);
    }

#if DEBUG
  g_debug ("----- EXIT handle_new_day_event (%s)", MODEL_NAME);
#endif
}



/**
 * Responds to the first detection event by announcing an outbreak and
 * initiating a destruction program.
 *
 * @param self the model.
 * @param event a detection event.
 * @param queue for any new events the model creates.
 */
void
handle_detection_event (struct adsm_module_t_ *self,
                        EVT_detection_event_t * event, EVT_event_queue_t * queue)
{
  local_data_t *local_data;
  UNT_unit_t *unit;
  USC_scorecard_t *scorecard;
  EVT_event_t *request;

#if DEBUG
  g_debug ("----- ENTER handle_detection_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  if (!local_data->outbreak_known)
    {
      local_data->outbreak_known = TRUE;
      local_data->first_detection_day = event->day;

#if DEBUG
      g_debug ("announcing outbreak");
#endif
      EVT_event_enqueue (queue, EVT_new_public_announcement_event (event->day));

      local_data->destruction_program_begin_day =
        event->day + local_data->destruction_program_delay + 1;
#if DEBUG
      g_debug ("destruction program delayed %i days (will begin on day %i)",
               local_data->destruction_program_delay, local_data->destruction_program_begin_day);
#endif
    }

  /* We keep track of a "first detection day" separately for vaccination.  This is
   * because vaccination capacity ramps up relative to 1st detection day, _but_ if the
   * vaccination program is terminated and then later re-started, vaccination capacity
   * will then ramp up relative to 1st detection day _post termination of the previous
   * vaccination program_. */
  if (local_data->first_detection_day_for_vaccination == -1)
    {      
      local_data->first_detection_day_for_vaccination = event->day;
    }

  unit = event->unit;
  scorecard = get_or_make_scorecard_for_unit (self, unit);
  USC_record_detection_as_diseased (scorecard, event->day);

  /* If the unit is awaiting vaccination, and the request(s) can be canceled by
   * detection, remove the unit from the waiting list.
   * We only need to check one entry in the scorecard's records of vaccination
   * requests to see if vaccination(s) can be canceled. */
  request = USC_scorecard_vaccination_request_peek_oldest (scorecard);
  if (request != NULL)
    {
      #if DEBUG
        g_debug ("unit \"%s\" in vaccination queue", unit->official_id);
      #endif
      if (local_data->cancel_vaccination_on_detection[unit->production_type])
        {
          cancel_vaccination (self, unit, event->day,
                              /* older_than = */ 0,
                              queue);
        }
    }

#if DEBUG
  g_debug ("----- EXIT handle_detection_event (%s)", MODEL_NAME);
#endif
}



/**
 * Responds to an unclaimed request for destruction event by committing to do
 * the destruction.
 *
 * @param self the model.
 * @param e a request for destruction event.  The event is copied if needed, so
 *   the original structure may be freed after the call to this function.
 * @param queue for any new events the model creates.
 */
void
handle_request_for_destruction_event (struct adsm_module_t_ *self,
                                      EVT_event_t * e, EVT_event_queue_t * queue)
{
  local_data_t *local_data;
  EVT_request_for_destruction_event_t *event, *old_request;
  UNT_unit_t *unit;
  unsigned int i;
  GQueue *q;
  EVT_event_t *event_copy;
  gboolean replace;

#if DEBUG
  g_debug ("----- ENTER handle_request_for_destruction_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);
  event = &(e->u.request_for_destruction);

  /* If this unit is being destroyed today, then ignore the request. */
  unit = event->unit;
  if (g_hash_table_lookup (local_data->destroyed_today, unit) != NULL)
    goto end;

  /* There may be more than one request to destroy the same unit.  If this is
   * the first request for this unit, just put it onto the appropriate waiting
   * list. */
  i = unit->index;
  if (local_data->destruction_status[i] == NULL)
    {
#if DEBUG
        g_debug ("no existing request to (potentially) replace");
        g_debug ("authorities commit to destroy unit \"%s\"", unit->official_id);
#endif
      EVT_event_enqueue (queue, EVT_new_commitment_to_destroy_event (unit, event->day));
      /* If the list of pending destruction queues is not long enough (that is,
       * this event has a lower priority than any we've seen before), extend
       * the list of pending destruction queues. */
      while (local_data->pending_destructions->len < event->priority)
        g_ptr_array_add (local_data->pending_destructions, g_queue_new ());

      q = (GQueue *) g_ptr_array_index (local_data->pending_destructions, event->priority - 1);
      event_copy = EVT_clone_event (e);
      event_copy->u.request_for_destruction.day_commitment_made = event->day;
      g_queue_push_tail (q, event_copy);
      /* Store a pointer to the GQueue link that contains this request. */
      local_data->destruction_status[i] = g_queue_peek_tail_link (q);
    }
  else
    {
      /* If this is not the first request to destroy this unit, we must decide
       * decide whether or not to replace the existing request.  We replace the
       * existing request if the new request is higher in the priority
       * system. */

      old_request =
        &(((EVT_event_t *) (local_data->destruction_status[i]->data))->u.request_for_destruction);

      if (local_data->destruction_time_waiting_priority == 1)
        {
          /* Replace the old request if this new request has the same time
           * waiting and a higher priority number.  (The less-than sign in
           * comparing the priority numbers is intentional -- 1 is "higher"
           * than 2.) */

          replace = (event->day == old_request->day) && (event->priority < old_request->priority);
        }
      else if (local_data->destruction_time_waiting_priority == 3)
        {
          /* Replace the old request if this new request has a higher priority
           * number.  (The less-than sign in comparing the priority numbers is
           * intentional -- 1 is "higher" than 2.) */

          replace = (event->priority < old_request->priority);
        }
      else
        {
          /* Replace the old request if this new request is in a higher "block"
           * of priority numbers, or if the new request has the same time
           * waiting and a higher priority number. */

          int step;
          int old_request_block, event_block;

          if (local_data->destruction_prod_type_priority == 1)
            step = ADSM_NCONTROL_REASONS;
          else
            step = local_data->nprod_types;

          /* Integer division... */
          old_request_block = (old_request->priority - 1) / step;
          event_block = (event->priority - 1) / step;

          replace = (event_block < old_request_block)
            || ((event->day == old_request->day) && (event->priority < old_request->priority));
        }
#if DEBUG
      g_debug ("current request %s old one", replace ? "replaces" : "does not replace");
      if (replace)
        {
          char *s;

          s = EVT_event_to_string ((EVT_event_t *) (local_data->destruction_status[i]->data));
          g_debug ("old request = %s", s);
          g_free (s);

          s = EVT_event_to_string (e);
          g_debug ("new request = %s", s);
          g_free (s);
        }
#endif

      if (replace)
        {
          GList *old_link;

          /* Delete both the old RequestForDestruction structure and the GQueue
           * link that holds it. */
          q =
            (GQueue *) g_ptr_array_index (local_data->pending_destructions,
                                          old_request->priority - 1);
          old_link = local_data->destruction_status[i];
          EVT_free_event ((EVT_event_t *) (old_link->data));
          old_request = NULL;
          g_queue_delete_link (q, old_link);

          /* Add the new request to the appropriate GQueue. */
          q = (GQueue *) g_ptr_array_index (local_data->pending_destructions, event->priority - 1);
          event_copy = EVT_clone_event (e);
          event_copy->u.request_for_destruction.day_commitment_made = event->day;
          g_queue_push_tail (q, event_copy);
          local_data->destruction_status[i] = g_queue_peek_tail_link (q);
        }
    }

end:
#if DEBUG
  g_debug ("----- EXIT handle_request_for_destruction_event (%s)", MODEL_NAME);
#endif
  return;
}



/**
 * Responds to a request to initiate vaccination event by setting a flag indicating that
 * the first vaccinations can occur tomorrow (resources permitting).
 *
 * @param self this module.
 * @param event a request to initiate vaccination event.
 * @param queue for any new events the module creates.
 */
void
handle_request_to_initiate_vaccination_event (struct adsm_module_t_ *self,
                                              EVT_request_to_initiate_vaccination_event_t * event,
                                              EVT_event_queue_t *queue)
{
  local_data_t *local_data;
  REL_chart_t *capacity;
  double zero_day;

  #if DEBUG
    g_debug ("----- ENTER handle_request_to_initiate_vaccination_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);
  /* Avoid attempting to stop and start on the same day. */
  if (local_data->vaccination_active == FALSE
      && event->day > local_data->vaccination_terminated_day)
    {
      local_data->vaccination_active = TRUE;
      local_data->vaccination_initiated_day = event->day;
      local_data->vaccination_program_initiation_count += 1;
      #if DEBUG
        g_debug ("initiating vaccination, day %i, time #%i", event->day, local_data->vaccination_program_initiation_count);
      #endif
      EVT_event_enqueue (queue, EVT_new_vaccination_initiated_event (event->day, event->trigger_id));

      /* Set the base day for vaccination capacity. Normally, the vaccination
       * capacity is relative to the day of first detection. If a vaccination
       * program was initiated, then ended, and now re-started, the vaccination
       * capacity is relative to the day of first detection post-ending of the
       * vaccination program. In the unusual case that a vaccination program is
       * re-started and there have been no new detections post-ending of the
       * vaccination program, the vaccination capacity will be relative to
       * today. */
      if (local_data->first_detection_day_for_vaccination > 0)
        local_data->base_day_for_vaccination_capacity = local_data->first_detection_day_for_vaccination;
      else
        local_data->base_day_for_vaccination_capacity = event->day;

      /* There are a couple of flags/values that are used in this module to decide
       * whether we have hit a point where no more vaccinations can be done.  Set them
       * now. */
      if (local_data->vaccination_program_initiation_count == 1)
        capacity = local_data->vaccination_capacity;
      else
        capacity = local_data->vaccination_capacity_on_restart;
      local_data->vaccination_capacity_goes_to_0 = REL_chart_zero_at_right (capacity, &zero_day);
      if (local_data->vaccination_capacity_goes_to_0)
        {
          local_data->vaccination_capacity_0_day = (int) ceil (zero_day);
          #if DEBUG
            g_debug ("vaccination capacity drops to 0 on and after the %ith day since 1st detection",
                     local_data->vaccination_capacity_0_day + 1);
          #endif
        }
      local_data->no_more_vaccinations = FALSE;

      /* Set a flag that is used with round-robin priority order, to let the
       * system know that it needs to pick a ring to start in. */
      local_data->first_round_robin = TRUE;
    }
  #if DEBUG
    g_debug ("----- EXIT handle_request_to_initiate_vaccination_event (%s)", MODEL_NAME);
  #endif

  return;
}



/**
 * Wraps the function USC_scorecard_register_vaccination_ring as a GFunc so
 * that it can be used with g_ptr_array_foreach.
 *
 * @param data a ring (USC_vaccination_ring_t *), cast to a gpointer.
 * @param user_data a scorecard (USC_scorecard_t *), cast to a gpointer.
 */
void
USC_scorecard_register_vaccination_ring_as_GFunc (gpointer data,
                                                  gpointer user_data)
{
  USC_vaccination_ring_t *ring;
  USC_scorecard_t *scorecard;

  ring = (USC_vaccination_ring_t *) data;
  scorecard = (USC_scorecard_t *) user_data;
  USC_scorecard_register_vaccination_ring (scorecard, ring);
  return;
}



/**
 * Wraps the function USC_scorecard_register_vaccination_ring as a GHFunc so
 * that it can be used with g_hash_table_foreach.
 *
 * @param key a unit (UNT_unit_t *), cast to a gpointer. This is ignored.
 * @param value the unit's scorecard (USC_scorecard_t *), cast to a gpointer.
 * @param user_data a ring (USC_vaccination_ring_t *), cast to a gpointer.
 */
void
USC_scorecard_register_vaccination_ring_as_GHFunc (gpointer key,
                                                   gpointer value,
                                                   gpointer user_data)
{
  USC_scorecard_t *scorecard;
  USC_vaccination_ring_t *ring;
  
  scorecard = (USC_scorecard_t *) value;
  ring = (USC_vaccination_ring_t *) user_data;
  USC_scorecard_register_vaccination_ring (scorecard, ring);
  return;
}



/**
 * Responds to a request for vaccination event by committing to do the
 * vaccination.
 *
 * @param self the model.
 * @param e a request for vaccination event.  The event is copied if needed, so
 *   the original structure may be freed after the call to this function.
 * @param queue for any new events the model creates.
 */
void
handle_request_for_vaccination_event (struct adsm_module_t_ *self,
                                      EVT_event_t * e, EVT_event_queue_t * queue)
{
  local_data_t *local_data;
  EVT_request_for_vaccination_event_t *event;
  UNT_unit_t *unit;
  USC_scorecard_t *scorecard;
  GQueue *bucket;
  
#if DEBUG
  g_debug ("----- ENTER handle_request_for_vaccination_event (%s)", MODEL_NAME);
#endif
    
  local_data = (local_data_t *) (self->model_data);
  event = &(e->u.request_for_vaccination);

  /* If this unit has been destroyed today, or this unit has been detected
   * and we do not want to vaccinate detected units, then ignore the request. */
  unit = event->unit;
  if (g_hash_table_lookup (local_data->destroyed_today, unit) != NULL)
    goto end;
  scorecard = get_scorecard_for_unit (self, unit);
  if (scorecard != NULL
      && local_data->cancel_vaccination_on_detection[unit->production_type]
      && scorecard->is_detected_as_diseased)
    goto end;

  if (TRUE)
    {
      /* There may be more than one request to vaccinate the same unit.  We
       * keep all of them. */
#if DEBUG
      g_debug ("authorities commit to vaccinate unit \"%s\"", unit->official_id);
#endif
      EVT_event_enqueue (queue, EVT_new_commitment_to_vaccinate_event (unit, event->day));
      event->day_commitment_made = event->day;

      /* The unit to be vaccinated goes into the set to be prioritized for
       * vaccination. */
      scorecard = get_or_make_scorecard_for_unit (self, unit);
      USC_scorecard_register_vaccination_request (scorecard, e);

      /* Is this unit new to the vaccination set? If so it has to be checked
       * against all active vaccination rings to determine its outside-in/
       * inside-out distance. */
      if (g_hash_table_lookup (local_data->vaccination_set, unit) == NULL)
        {
          g_hash_table_insert (local_data->vaccination_set, unit, scorecard);
          /* Add the unit's scorecard to the list scorecards_sorted. One
           * exception: if this unit was removed from the vaccination set today
           * (we're re-adding it), then the unit's scorecard will still be in
           * scorecards_sorted. */
          if (g_hash_table_lookup (local_data->removed_from_vaccination_set_today, unit) != NULL)
            {
              g_assert (g_hash_table_remove (local_data->removed_from_vaccination_set_today, unit) == TRUE);
            }
          else
            {
              g_ptr_array_add (local_data->scorecards_sorted, scorecard);
            }
        }
        g_ptr_array_foreach (local_data->active_vaccination_rings,
                             USC_scorecard_register_vaccination_ring_as_GFunc,
                             scorecard);

    }

  /* The request is registered on the unit's scorecard, which may change the
   * ring the unit belongs to (w.r.t. round-robin prioritization). */

  /* The focus unit (the unit at the center of the vaccination ring or circle)
   * is used to track active vaccination rings.  Does this focus unit
   * represent a new active vaccination ring?  If so:
   * - a new ring is added to the data structure active_vaccination_rings
   * - a new bucket is added to the data structure for doing round-robin
   *   priority
   * - all scorecards of units awaiting vaccination are checked to see if this
   *   new ring alters their outside-in/inside-out distance. */
  bucket = (GQueue *)
    g_hash_table_lookup (local_data->round_robin_buckets, event->focus_unit);
  if (bucket == NULL)
    {
      USC_vaccination_ring_t *ring;

      #if DEBUG
        g_debug ("Ring around unit \"%s\" is a new ring", event->focus_unit->official_id);
      #endif
      /* Record the ring details (unit at center, inner and outer radius) in
       * in the active_vaccination_rings array. */
      ring = g_new (USC_vaccination_ring_t, 1);
      ring->unit_at_center = event->focus_unit;
      ring->supp_radius = event->supp_radius;
      ring->prot_inner_radius = event->prot_inner_radius;
      ring->prot_outer_radius = event->prot_outer_radius;
      g_ptr_array_add (local_data->active_vaccination_rings, ring);

      /* Add a new bucket to the round robin buckets. */
      bucket = g_queue_new();
      g_hash_table_insert (local_data->round_robin_buckets, event->focus_unit, bucket);

      /* Check the units awaiting vaccination to see if their outside-in/
       * inside-out distance changes. */
      g_hash_table_foreach (local_data->vaccination_set,
                            USC_scorecard_register_vaccination_ring_as_GHFunc,
                            ring);
    }

end:
#if DEBUG
  g_debug ("----- EXIT handle_request_for_vaccination_event (%s)", MODEL_NAME);
#endif

  return;
}



/**
 * Responds to a vaccination event by noting the day on which the unit was
 * vaccinated.
 *
 * @param self the model.
 * @param event a vaccination event.
 */
void
handle_vaccination_event (struct adsm_module_t_ *self, EVT_vaccination_event_t * event)
{
  local_data_t *local_data;

#if DEBUG
  g_debug ("----- ENTER handle_vaccination_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  local_data->day_last_vaccinated[event->unit->index] = event->day;

#if DEBUG
  g_debug ("----- EXIT handle_vaccination_event (%s)", MODEL_NAME);
#endif
}



/**
 * Responds to a request to terminate vaccination event by un-setting the flag indicating
 * that vaccination is active.
 *
 * @param self this module.
 * @param event a request to terminate vaccination event.
 * @param queue for any new events this module creates.
 */
void
handle_request_to_terminate_vaccination_event (struct adsm_module_t_ *self,
                                               EVT_request_to_terminate_vaccination_event_t * event,
                                               EVT_event_queue_t * queue)
{
  local_data_t *local_data;

  #if DEBUG
    g_debug ("----- ENTER handle_request_to_terminate_vaccination_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);
  /* Avoid attempting to stop and start on the same day. */
  if (local_data->vaccination_active == TRUE
      && event->day > local_data->vaccination_initiated_day)
    {
      local_data->vaccination_active = FALSE;
      local_data->vaccination_terminated_day = event->day;
      #if DEBUG
        g_debug ("terminating vaccination, day %i\n", event->day);
      #endif
      EVT_event_enqueue (queue, EVT_new_vaccination_terminated_event (event->day));
      /* No need to clear out the pending vaccinations.  That will be done when the next
       * NewDay event arrives. */
      local_data->first_detection_day_for_vaccination = -1;
    }

  #if DEBUG
    g_debug ("----- EXIT handle_request_to_terminate_vaccination_event (%s)", MODEL_NAME);
  #endif

  return;
}



/**
 * Runs this model.
 *
 * @param self the model.
 * @param units a unit list.
 * @param zones a zone list.
 * @param event the event that caused the model to run.
 * @param rng a random number generator.
 * @param queue for any new events the model creates.
 */
void
run (struct adsm_module_t_ *self, UNT_unit_list_t * units, ZON_zone_list_t * zones,
     EVT_event_t * event, RAN_gen_t * rng, EVT_event_queue_t * queue)
{
#if DEBUG
  g_debug ("----- ENTER run (%s)", MODEL_NAME);
#endif

  switch (event->type)
    {
    case EVT_BeforeEachSimulation:
      handle_before_each_simulation_event (self);
      break;
    case EVT_NewDay:
      handle_new_day_event (self, &(event->u.new_day), units, queue);
      break;
    case EVT_Detection:
      handle_detection_event (self, &(event->u.detection), queue);
      break;
    case EVT_RequestForDestruction:
      handle_request_for_destruction_event (self, event, queue);
      break;
    case EVT_RequestToInitiateVaccination:
      handle_request_to_initiate_vaccination_event (self, &(event->u.request_to_initiate_vaccination), queue);
      break;
    case EVT_RequestForVaccination:
      handle_request_for_vaccination_event (self, event, queue);
      break;
    case EVT_Vaccination:
      handle_vaccination_event (self, &(event->u.vaccination));
      break;
    case EVT_RequestToTerminateVaccination:
      handle_request_to_terminate_vaccination_event (self, &(event->u.request_to_terminate_vaccination), queue);
      break;
    default:
      g_error
        ("%s has received a %s event, which it does not listen for.  This should never happen.  Please contact the developer.",
         MODEL_NAME, EVT_event_type_name[event->type]);
    }

#if DEBUG
  g_debug ("----- EXIT run (%s)", MODEL_NAME);
#endif
}



/**
 * Reports whether this model has any pending actions to carry out.
 *
 * @param self the model.
 * @return TRUE if the model has pending actions.
 */
gboolean
has_pending_actions (struct adsm_module_t_ * self)
{
  local_data_t *local_data;
  unsigned int npriorities;
  GQueue *q;
  int i;
  gboolean has_actions = FALSE;

  local_data = (local_data_t *) (self->model_data);

  /* We only bother checking for pending vaccinations if the vaccination
   * program has been initiated and if there is or will be capacity to
   * vaccinate. */
  if (local_data->vaccination_active
      && !local_data->no_more_vaccinations
      && g_hash_table_size (local_data->vaccination_set) > 0)
    {
      has_actions = TRUE;
    }

  if (!local_data->no_more_destructions)
    {
      npriorities = local_data->pending_destructions->len;
      for (i = 0; i < npriorities; i++)
        {
          q = (GQueue *) g_ptr_array_index (local_data->pending_destructions, i);
          if (!g_queue_is_empty (q))
            {
              has_actions = TRUE;
              break;
            }
        }
    }

  return has_actions;
}



/**
 * Returns a text representation of this model.
 *
 * @param self the model.
 * @return a string.
 */
char *
to_string (struct adsm_module_t_ *self)
{
  GString *s;
  GString *prioritizer_list;
  char *substring;
  local_data_t *local_data;

  local_data = (local_data_t *) (self->model_data);
  s = g_string_new (NULL);
  g_string_sprintf (s, "<%s", MODEL_NAME);

  g_string_sprintfa (s, "\n  destruction-program-delay=%i", local_data->destruction_program_delay);

  substring = REL_chart_to_string (local_data->destruction_capacity);
  g_string_sprintfa (s, "\n  destruction-capacity=%s", substring);
  g_free (substring);

  substring = REL_chart_to_string (local_data->vaccination_capacity);
  g_string_sprintfa (s, "\n  vaccination-capacity=%s", substring);
  g_free (substring);

  substring = REL_chart_to_string (local_data->vaccination_capacity_on_restart);
  g_string_sprintfa (s, "\n  vaccination-capacity-on-restart=%s", substring);
  g_free (substring);

  prioritizer_list = g_string_new("[");
  {
    GSList *iter;
    adsm_prioritizer_t *prioritizer;
    gboolean first = TRUE;
    for (iter = local_data->vaccination_prioritizers; iter != NULL; iter = g_slist_next(iter))
      {
        prioritizer = iter->data;
        substring = prioritizer->to_string(prioritizer);
        g_string_append_printf (prioritizer_list, first ? "%s" : ",%s", substring);
        first = FALSE;
        g_free(substring);
      }
  }
  g_string_append_c(prioritizer_list, ']');
  g_string_append_printf (s, "\n  vaccination priorities=%s", prioritizer_list->str);
  g_string_free(prioritizer_list, TRUE);
  
  g_string_append_c (s, '>');

  /* don't return the wrapper object */
  return g_string_free (s, FALSE);
}



/**
 * Frees this model.
 *
 * @param self the model.
 */
void
local_free (struct adsm_module_t_ *self)
{
  local_data_t *local_data;
  unsigned int npriorities;
  GQueue *q;
  int i;

#if DEBUG
  g_debug ("----- ENTER free (%s)", MODEL_NAME);
#endif

  /* Free the dynamically-allocated parts. */
  local_data = (local_data_t *) (self->model_data);
  REL_free_chart (local_data->destruction_capacity);
  g_free (local_data->destruction_status);
  npriorities = local_data->pending_destructions->len;
  for (i = 0; i < npriorities; i++)
    {
      q = (GQueue *) g_ptr_array_index (local_data->pending_destructions, i);
      while (!g_queue_is_empty (q))
        EVT_free_event (g_queue_pop_head (q));
      g_queue_free (q);
    }
  g_ptr_array_free (local_data->pending_destructions, TRUE);
  g_hash_table_destroy (local_data->destroyed_today);

  g_slist_free_full (local_data->vaccination_prioritizers, free_prioritizer);
  REL_free_chart (local_data->vaccination_capacity);
  REL_free_chart (local_data->vaccination_capacity_on_restart);
  clear_all_pending_vaccinations (self, /* day = */ 0, /* event queue = */ NULL);
  g_hash_table_destroy (local_data->vaccination_set);
  g_hash_table_destroy (local_data->removed_from_vaccination_set_today);
  g_ptr_array_free (local_data->scorecards_sorted, TRUE);
  g_free (local_data->cancel_vaccination_on_detection);
  g_free (local_data->day_last_vaccinated);
  g_free (local_data->min_time_between_vaccinations);
  g_free (local_data->min_next_vaccination_day);
  /* The active_vaccination_rings GPtrArray has a free function defined, so
   * the USC_vaccination_ring_t objects it stores will be properly disposed of
   * when the array is freed. */
  g_ptr_array_free (local_data->active_vaccination_rings, TRUE);
  g_hash_table_destroy (local_data->round_robin_buckets);
  /* clear_all_pending_vaccinations calls get_scorecard_for_unit, so the
   * unit-to-scorecard map cannot be deleted until after
   * clear_all_pending_vaccinations. */   
  g_hash_table_destroy (local_data->scorecard_for_unit);
  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



typedef struct
{
  adsm_module_t *self;
  UNT_unit_list_t *units;
  sqlite3 *db;
  GError **error;
}
set_params_args_t;



/**
 * Reads the global parameters for a resources and implementation of controls
 * model.
 *
 * @param data a set_params_args_t structure, containing this module ("self")
 *   and a GError pointer to fill in if errors occur.
 * @param dict the SQL query result as a GHashTable in which key = colname,
 *   value = value, both in (char *) format.
 * @return 0
 */
static int
set_global_params (void *data, GHashTable *dict)
{
  set_params_args_t *args;
  adsm_module_t *self;
  GError **error;
  local_data_t *local_data;
  UNT_unit_list_t *units;
  sqlite3 *params;
  char *tmp_text;
  guint rel_id;
  double dummy;
  gchar **tokens, **iter;
  guint ntokens;

  #if DEBUG
    g_debug ("----- ENTER set_global_params (%s)", MODEL_NAME);
  #endif

  args = data;
  self = args->self;
  local_data = (local_data_t *) (self->model_data);
  units = args->units;
  params = args->db;
  error = args->error;

  g_assert (g_hash_table_size (dict) == 7);

  tmp_text = g_hash_table_lookup (dict, "destruction_program_delay");
  if (tmp_text != NULL)
    {
      errno = 0;
      local_data->destruction_program_delay = (int) strtol (tmp_text, NULL, /* base */ 10);
      g_assert (errno != ERANGE && errno != EINVAL);
    }
  else
    {
      local_data->destruction_program_delay = 0;
    }

  tmp_text = g_hash_table_lookup (dict, "destruction_capacity_id");
  if (tmp_text != NULL)
    {
      errno = 0;
      rel_id = strtol (tmp_text, NULL, /* base */ 10);
      g_assert (errno != ERANGE && errno != EINVAL);  
      local_data->destruction_capacity = PAR_get_relchart (params, rel_id);
    }
  else
    {
      local_data->destruction_capacity = REL_new_point_chart (0);
    }
  /* Set a flag if the destruction capacity chart at some point drops to 0 and
   * stays there. */
  local_data->destruction_capacity_goes_to_0 =
    REL_chart_zero_at_right (local_data->destruction_capacity, &dummy);
  if (local_data->destruction_capacity_goes_to_0)
    {
      local_data->destruction_capacity_0_day = (int) ceil (dummy) - 1;
      #if DEBUG
        g_debug ("destruction capacity drops to 0 on and after day %i",
                 local_data->destruction_capacity_0_day);
      #endif
    }

  /* The destruction priority order is given in a comma-separated string in the
   * column "destruction_priority_order". */
  tmp_text = g_hash_table_lookup (dict, "destruction_priority_order");
  tokens = g_strsplit (tmp_text, ",", 0);
  /* Go through the comma-separated tokens and see if they match what is
   * expected. */ 
  local_data->destruction_prod_type_priority = 0;
  local_data->destruction_reason_priority = 0;
  local_data->destruction_time_waiting_priority = 0;
  for (iter = tokens, ntokens = 0; *iter != NULL; iter++)
    {
      ntokens++;
      g_strstrip (*iter);
      if (g_ascii_strcasecmp(*iter, "production type") == 0)
        local_data->destruction_prod_type_priority = ntokens;
      else if (g_ascii_strcasecmp(*iter, "reason") == 0)
        local_data->destruction_reason_priority = ntokens;
      else if (g_ascii_strcasecmp(*iter, "time waiting") == 0)
        local_data->destruction_time_waiting_priority = ntokens;
    }
  /* At the end of that loop, we should have counted 3 tokens, and filled in a
   * nonzero value for each of the destruction_XXX_priority variables. */
  if (!(ntokens == 3
        && local_data->destruction_prod_type_priority > 0
        && local_data->destruction_reason_priority > 0
        && local_data->destruction_time_waiting_priority > 0))
    {
      g_set_error (error, ADSM_MODULE_ERROR, 0,
                   "\"%s\" is not a valid destruction priority order: "
                   "must be some ordering of reason, time waiting, production type",
                   tmp_text);
    }
  g_strfreev (tokens);

  tmp_text = g_hash_table_lookup (dict, "vaccination_capacity_id");
  if (tmp_text != NULL)
    {
      errno = 0;
      rel_id = strtol (tmp_text, NULL, /* base */ 10);
      g_assert (errno != ERANGE && errno != EINVAL);  
      local_data->vaccination_capacity = PAR_get_relchart (params, rel_id);
    }
  else
    {
      local_data->vaccination_capacity = REL_new_point_chart (0);
    }

  tmp_text = g_hash_table_lookup (dict, "restart_vaccination_capacity_id");
  if (tmp_text != NULL)
    {
      errno = 0;
      rel_id = strtol (tmp_text, NULL, /* base */ 10);
      g_assert (errno != ERANGE && errno != EINVAL);  
      local_data->vaccination_capacity_on_restart = PAR_get_relchart (params, rel_id);
    }
  else
    {
      /* If a vaccination capacity chart is not specified for a restarted
       * vaccination program, just re-use the same chart as before. */
      local_data->vaccination_capacity_on_restart = REL_clone_chart (local_data->vaccination_capacity);
    }

  /* The vaccination priority order is given in JSON format in the column
   * "vaccination_priority_order". */
  local_data->vaccination_prioritizers = NULL;
  local_data->round_robin = TRUE;
  tmp_text = g_hash_table_lookup (dict, "vaccination_priority_order");
  {
    JsonParser *json_parser;

    json_parser = json_parser_new();
    if (json_parser_load_from_data (json_parser, tmp_text, -1, error))
      {
        JsonNode *node;

        node = json_parser_get_root(json_parser);
        if (JSON_NODE_HOLDS_OBJECT(node))
          {
            GList *members, *iter;
            adsm_prioritizer_t *prioritizer;
            JsonObject *json_object = json_node_get_object(node);
            members = json_object_get_members(json_object);
            for (iter = members; iter != NULL; iter = g_list_next(iter))
              {
                const gchar *member;

                member = iter->data;
                prioritizer = NULL;
                if (g_ascii_strcasecmp (member, "production type") == 0)
                  {
                    gchar **tokens;
                    guint n, i;
                    JsonArray *production_types = json_object_get_array_member(json_object, member);
                    n = json_array_get_length(production_types);
                    tokens = g_new0(gchar *, n+1);
                    for (i = 0; i < n; i++)
                      {
                        tokens[i] = (gchar *)json_array_get_string_element(production_types, i);
                      }
                    /* Final one is already NULL because we used g_new0 */
                    prioritizer = new_production_type_prioritizer (units->production_type_names,
                                                                   tokens);
                    g_free(tokens); /* Don't try to free the individual tokens,
                      they're owned by the JSON object */
                  }
                else if (g_ascii_strcasecmp (member, "reason") == 0)
                  {
                  }
                else if (g_ascii_strcasecmp (member, "days holding") == 0)
                  {
                    JsonArray *json_array = json_object_get_array_member(json_object, member);
                    const gchar *first_item = json_array_get_string_element(json_array, 0);
                    gboolean oldest_first = (g_ascii_strcasecmp (first_item, "oldest") == 0);
                    prioritizer = new_time_waiting_prioritizer (oldest_first);
                  }
                else if (g_ascii_strcasecmp (member, "size") == 0)
                  {
                    JsonArray *json_array = json_object_get_array_member(json_object, member);
                    const gchar *first_item = json_array_get_string_element(json_array, 0);
                    gboolean largest_first = (g_ascii_strcasecmp (first_item, "largest") == 0);
                    prioritizer = new_size_prioritizer (largest_first);
                  }
                else if (g_ascii_strcasecmp (member, "direction") == 0)
                  {
                    JsonArray *json_array = json_object_get_array_member(json_object, member);
                    const gchar *first_item = json_array_get_string_element(json_array, 0);
                    gboolean outside_in = (g_ascii_strcasecmp (first_item, "outside-in") == 0);
                    prioritizer = new_direction_prioritizer (outside_in);
                  }
                if (prioritizer != NULL)
                  {
                    local_data->vaccination_prioritizers =
                      g_slist_prepend (local_data->vaccination_prioritizers, prioritizer);
                    #if DEBUG
                      g_debug ("now %u prioritizers in chain", g_slist_length (local_data->vaccination_prioritizers));
                    #endif
                  }
              } /* end of loop over top-level members in JSON structure */
            g_list_free(members);
          } /* end of check for JSON "object" type at top level */
        /* The list of prioritizers is a singly-linked list and it was built by
         * prepends, so now it must be reversed. */
        local_data->vaccination_prioritizers = g_slist_reverse (local_data->vaccination_prioritizers);
      } /* end of if JSON parse was successful */
    g_object_unref(json_parser);
  }

  tmp_text = g_hash_table_lookup (dict, "vaccinate_retrospective_days");
  if (tmp_text != NULL)
    {
      errno = 0;
      local_data->vaccination_retrospective_days = strtol (tmp_text, NULL, /* base */ 10);
      g_assert (errno != ERANGE && errno != EINVAL);  
    }
  else
    {
      local_data->vaccination_retrospective_days = 0;
    }

  #if DEBUG
    g_debug ("----- EXIT set_global_params (%s)", MODEL_NAME);
  #endif

  return 0;
}



/**
 * Adds production type specific parameters to a resources and implementation
 * of controls model.
 *
 * @param data a set_params_args_t structure, containing this module ("self")
 *   and a GError pointer to fill in if errors occur.
 * @param dict the SQL query result as a GHashTable in which key = colname,
 *   value = value, both in (char *) format.
 * @return 0
 */
static int
set_prodtype_params (void *data, GHashTable *dict)
{
  set_params_args_t *args;
  adsm_module_t *self;
  GError **error;
  local_data_t *local_data;
  UNT_unit_list_t *units;
  sqlite3 *params;
  guint production_type;
  char *tmp_text;
  long int tmp;

#if DEBUG
  g_debug ("----- ENTER set_prodtype_params (%s)", MODEL_NAME);
#endif

  args = data;
  self = args->self;
  local_data = (local_data_t *) (self->model_data);
  units = args->units;
  params = args->db;
  error = args->error;

  g_assert (g_hash_table_size (dict) == 3);

  /* Find out which production type these parameters apply to. */
  production_type =
    adsm_read_prodtype (g_hash_table_lookup (dict, "prodtype"),
                        units->production_type_names);

  /* Read the parameters. */
  tmp_text = g_hash_table_lookup (dict, "vaccinate_detected_units");  /* database field cannot be null */
  errno = 0;
  tmp = strtol (tmp_text, NULL, /* base */ 10);
  g_assert (errno != ERANGE && errno != EINVAL);
  g_assert (tmp == 0 || tmp == 1);
  local_data->cancel_vaccination_on_detection[production_type] = (tmp == 0);

  tmp_text = g_hash_table_lookup (dict, "minimum_time_between_vaccinations"); /* database field can be null */
  if (tmp_text != NULL)
    {
      errno = 0;
      local_data->min_time_between_vaccinations[production_type] = (guint) strtol (tmp_text, NULL, /* base */ 10);
      g_assert (errno != ERANGE && errno != EINVAL);
    }

#if DEBUG
  g_debug ("----- EXIT set_prodtype_params (%s)", MODEL_NAME);
#endif

  return 0;
}



/**
 * Returns a new resources and implementation of controls model.
 */
adsm_module_t *
new (sqlite3 * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones, GError **error)
{
  adsm_module_t *self;
  local_data_t *local_data;
  EVT_event_type_t events_listened_for[] = {
    EVT_BeforeEachSimulation,
    EVT_NewDay,
    EVT_Detection,
    EVT_RequestForDestruction,
    EVT_RequestToInitiateVaccination,
    EVT_RequestForVaccination,
    EVT_Vaccination,
    EVT_RequestToTerminateVaccination,
    0
  };
  set_params_args_t set_params_args;
  char *sqlerr;

#if DEBUG
  g_debug ("----- ENTER new (%s)", MODEL_NAME);
#endif

  self = g_new (adsm_module_t, 1);
  local_data = g_new (local_data_t, 1);

  self->name = MODEL_NAME;
  self->events_listened_for = adsm_setup_events_listened_for (events_listened_for);
  self->outputs = g_ptr_array_new ();
  self->model_data = local_data;
  self->run = run;
  self->is_listening_for = adsm_model_is_listening_for;
  self->has_pending_actions = has_pending_actions;
  self->has_pending_infections = adsm_model_answer_no;
  self->to_string = to_string;
  self->printf = adsm_model_printf;
  self->fprintf = adsm_model_fprintf;
  self->free = local_free;

  local_data->nunits = UNT_unit_list_length (units);
  local_data->nprod_types = units->production_type_names->len;

  /* No outbreak has been detected yet. */
  local_data->outbreak_known = FALSE;
  local_data->destruction_program_begin_day = 0;

  local_data->scorecard_for_unit =
    g_hash_table_new_full (g_direct_hash, g_direct_equal,
                           /* key_destroy_func = */ NULL, /* do not destroy units */
                           /* value_destroy_func = */ USC_free_scorecard_as_GDestroyNotify);

  /* No units have been destroyed or slated for destruction yet. */
  local_data->destruction_status = g_new0 (GList *, local_data->nunits);
  local_data->ndestroyed_today = 0;
  local_data->pending_destructions = g_ptr_array_new ();
  local_data->no_more_destructions = FALSE;
  local_data->destroyed_today = g_hash_table_new (g_direct_hash, g_direct_equal);

  /* No units have been vaccinated or slated for vaccination yet. */
  local_data->vaccination_set = g_hash_table_new (g_direct_hash, g_direct_equal);
  local_data->removed_from_vaccination_set_today = g_hash_table_new (g_direct_hash, g_direct_equal);
  local_data->scorecards_sorted = g_ptr_array_new ();
  local_data->nvaccinated_today = 0;
  local_data->cancel_vaccination_on_detection = g_new0 (gboolean, local_data->nprod_types);
  local_data->day_last_vaccinated = g_new0 (int, local_data->nunits);
  local_data->min_time_between_vaccinations = g_new0 (guint, local_data->nprod_types);
  local_data->min_next_vaccination_day = g_new0 (int, local_data->nunits);
  local_data->no_more_vaccinations = FALSE;
  local_data->active_vaccination_rings = g_ptr_array_new_with_free_func (g_free);
  local_data->round_robin_buckets = 
    g_hash_table_new_full (g_direct_hash, g_direct_equal,
                           /* key_destroy_func = */ NULL,
                           /* value_destroy_func = */ g_queue_free_as_GDestroyNotify);

  /* Call the set_global_params function to read the global parameters. */
  set_params_args.self = self;
  set_params_args.units = units;
  set_params_args.db = params;
  set_params_args.error = error;
  sqlite3_exec_dict (params,
                     "SELECT destruction_program_delay,destruction_capacity_id,destruction_priority_order,"
                     "vaccination_capacity_id,restart_vaccination_capacity_id,vaccination_priority_order,"
                     "vaccinate_retrospective_days "
                     "FROM ScenarioCreator_controlmasterplan",
                     set_global_params, &set_params_args, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }

  /* Call the set_prodtype_params function to read the production type specific
   * parameters. */
  sqlite3_exec_dict (params,
                     "SELECT prodtype.name AS prodtype,vaccinate_detected_units,minimum_time_between_vaccinations "
                     "FROM ScenarioCreator_productiontype prodtype,ScenarioCreator_controlprotocol protocol,ScenarioCreator_protocolassignment xref "
                     "WHERE prodtype.id=xref.production_type_id "
                     "AND xref.control_protocol_id=protocol.id",
                     set_prodtype_params, &set_params_args, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file resources_and_implementation_of_controls_model.c */
