/** @file contact_spread_model.c
 * Module for contact spread.
 *
 * On each day, this module follows these steps:
 * <ol>
 *   <li>
 *     Look up a multiplier for the rate of movement of animals based on the
 *     number of days since a public announcement of an outbreak.  Use this
 *     multiplier to scale the movement rate specified in the parameters.
 *   <li>
 *     For each unit <i>A</i>,
 *     <ol>
 *       <li>
 *         Check whether <i>A</i> can be the source of an infection.  That is,
 *         is it Latent (applicable only for direct contact) or Infectious,
 *         and not quarantined?
 *       <li>
 *         If <i>A</i> cannot be a source, go on to the next unit.
 *       <li>
 *         Sample a number <i>N</i> from a Poisson distribution whose mean is
 *         the movement rate.
 *       <li>
 *         Create <i>N</i> exposures with <i>A</i> as the source.
 *     </ol>
 *   <li>
 *     For each exposure <i>E</i>,
 *     <ol>
 *       <li>
 *         Sample a number <i>TargetDistance</i> from the distance distribution
 *         specified in the parameters.
 *       <li>
 *         From all units that can be the target of an infection (that is,
 *         those that are not Destroyed), choose the unit
 *         <i>B</i> whose distance from the source is closest to
 *         <i>TargetDistance</i>.
 *       <li>
 *         Record the exposure of the target unit.  This exposure can be
 *         discovered by trace-back investigations.
 *       <li>
 *         Generate a random number <i>r</i> in [0,1].
 *       <li>
 *         If doing direct contact and <i>r</i> < the prevalence in the source
 *         unit, or if doing indirect contact and <i>r</i> < the probability of
 *         infection given exposure,
 *         <ol>
 *           <li>
 *             Infect the target unit.
 *         </ol>
 *     </ol>
 * </ol>
 *
 * These calculations come from the document <i>SpreadModel Version 3.0
 * Diagrams and pseudocoding</i>, by Mark A. Schoenbaum of the
 * <a href="http://www.aphis.usda.gov/">USDA</a> and Francisco Zagmutt-Vergara
 * of <a href="http://www.colostate.edu/">Colorado State University</a>.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 *
 * @author Shaun Case <ShaunCase@colostate.edu><br>
 *   Animal Population Health Institute<br>
 *   College of Veterinary Medicine and Biomedical Sciences<br>
 *   Colorado State University<br>
 *   Fort Collins, CO 80523<br>
 *   USA
 *
 * @date November 2003
 *
 * Copyright &copy; University of Guelph, and Colorado State University  2003-2009
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
#define new contact_spread_model_new
#define run contact_spread_model_run
#define has_pending_actions contact_spread_model_has_pending_actions
#define has_pending_infections contact_spread_model_has_pending_infections
#define to_string contact_spread_model_to_string
#define local_free contact_spread_model_free
#define handle_before_each_simulation_event contact_spread_model_handle_before_each_simulation_event
#define handle_new_day_event contact_spread_model_handle_new_day_event
#define handle_public_announcement_event contact_spread_model_handle_public_announcement_event
#define check_and_choose contact_spread_model_check_and_choose

#include "module.h"
#include "module_util.h"
#include "gis.h"
#include "spatial_search.h"
#include "sqlite3_exec_dict.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#if HAVE_STRINGS_H
#  include <strings.h>
#endif

#if HAVE_MATH_H
#  include <math.h>
#endif

#include "general.h"
#include "contact_spread_model.h"

#ifdef USE_SC_GUILIB
#  include <sc_adsm_outputs.h>
#endif

#if !HAVE_ROUND && HAVE_RINT
#  define round rint
#endif

double round (double x);

/** This must match an element name in the DTD. */
#define MODEL_NAME "contact-spread-model"



#define EPSILON 0.01



/**
 * Specialized information for this module.  There is a local_data_t structure
 * that holds global information, and the local_data_t structure contains an
 * array of param_block_t structures, each of which holds parameters specific
 * to one contact type/source production type/recipient production type
 * combination.
 */
typedef struct
{
  double movement_rate;
  double fixed_movement_rate;
  REL_chart_t *movement_control; /**< Movement control charts by source and
    recipient production type, used when the source unit is not inside a zone
    focus.  When the source unit is inside a zone focus, use the charts by
    zone and production type, in local_data_t below. */
  PDF_dist_t *distance_dist;
  PDF_dist_t *shipping_delay;
  gboolean latent_units_can_infect;
  gboolean subclinical_units_can_infect;
  double prob_infect;
}
param_block_t;



/* Specialized information for this model. */
typedef struct
{
  GPtrArray *production_types; /**< Each item in the list is a char *. */
  ZON_zone_list_t *zones;
  param_block_t ***param_block[ADSM_NCONTACT_TYPES]; /**< Blocks of parameters.
    Use an expression of the form
    param_block[contact_type][source_production_type][recipient_production_type]
    to get a pointer to a particular param_block. */
  REL_chart_t ***movement_control[ADSM_NCONTACT_TYPES]; /**< Movement control
    charts for units inside zones.  Use an expression of the form
    movement_control[contact_type][zone->level-1][source_production_type]
    to get a pointer to a particular chart. */
  double min_radius; /**< A minimum radius in which to look for neighbours when
    generating short-distance contacts. */
  GPtrArray *pending_infections; /**< An array to store delayed contacts.  Each
    item in the array is a GQueue of Exposure events.  (Actually
    a singly-linked list would suffice, but the GQueue syntax is much more
    readable than the GSList syntax.)  An index "rotates" through the array, so
    an event that is to happen in 1 day is placed in the GQueue that is 1 place
    ahead of the rotating index, an event that is to happen in 2 days is placed
    in the GQueue that is 2 places ahead of the rotating index, etc. */
  unsigned int npending_infections;
  unsigned int rotating_index; /**< To go with pending_infections. */
  gboolean outbreak_known;
  int public_announcement_day;
  sqlite3 *db; /* Temporarily stash a pointer to the parameters database here
    so that it will be available to the set_params function. */
}
local_data_t;



/**
 * Before each simulation, set "outbreak known" to no and delete any delayed
 * infections leftover from a previous iteration.
 *
 * @param self this module.
 */
void
handle_before_each_simulation_event (struct adsm_module_t_ *self)
{
  local_data_t *local_data;
  unsigned int i;
  GQueue *q;

  #if DEBUG
    g_debug ("----- ENTER handle_before_each_simulation_event (%s)", MODEL_NAME);
  #endif

  local_data = (local_data_t *) (self->model_data);
  local_data->outbreak_known = FALSE;
  local_data->public_announcement_day = 0;
  for (i = 0; i < local_data->pending_infections->len; i++)
    {
      q = (GQueue *) g_ptr_array_index (local_data->pending_infections, i);
      while (!g_queue_is_empty (q))
        EVT_free_event (g_queue_pop_head (q));
    }
  local_data->npending_infections = 0;
  local_data->rotating_index = 0;

  #if DEBUG
    g_debug ("----- EXIT handle_before_each_simulation_event (%s)", MODEL_NAME);
  #endif

  return;
}



/**
 * Special sub-structure for use with the callback function below.
 * 
 */
typedef struct
{
  ADSM_contact_type contact_type;
  unsigned int recipient_production_type;
  double movement_distance;
  UNT_unit_t *best_unit; /**< The current pick for best recipient. */
  ZON_zone_fragment_t *best_unit_zone; /**< The zone fragment best_unit is in. */
  double best_unit_difference; /**< The difference between the desired contact
    distance and the best distance found so far. */
  double min_difference; /**< The smallest value of best_unit_difference so
    far.  See the file drift.xml in the direct contact tests for an explanation
    of why this is needed. */
  double cumul_size;    
  gboolean try_again;  /*  Used if and when the RTree search method found no match */    
}sub_callback_t;


/**
 * Special structure for use with the callback function below.
 */
typedef struct
{
  struct adsm_module_t_ *self;
  UNT_unit_list_t *units;
  ZON_zone_list_t *zones;
  RAN_gen_t *rng;
  UNT_unit_t *unit1;
  ZON_zone_fragment_t *unit1_fragment;
  /**  This optimization repairs the fact that the RTree and the exhaustive
       searching is so time intensive, by altering the original algorithm to
       handle all contact/prodcution-type combinations at the same time during
       the iteration over the eligible unit list.  Prior to this, the search 
       was done once for each contact/production-type combination, thus compounding
       the search time consumption exponentially.  This is where the majority of
       the simulation time is spent, so reducing this complexity could significantly
       improve on performance for the simulation engine.  Reduction should be
       as a maximum: 
       Total_Time / [ number_of_contact_types X number_of_production_types X average( number_of_contacts_per_production_type ) ]     
       where number_of_contacts_per_production_type varies in number per [number_of_contact_types X number_of_production_types] pair
       
       For sufficiently diverse, i.e. worst case, scenario populations, this could be as big a difference
       as the differenc between O(n^4) and O(n[log(n)]), i.e. exponential 
       speed-up; best case scenario parameters would show a linear speed-up.  Either case,
       should be fairly dramatic improvements in time consumption....we'll se....        
   **/
  unsigned long contact_count;
  unsigned long production_type_count;
  /*  This is a 3-Dimensional matrix of contact-types, production-types, and 
   *  sub_callback_t structures, where the depth of the matrix, sub-callback_t element,
   *  is variable per [contact-type, production-type] pair.
   */
  GPtrArray ***_contacts; /* gpointer points to a sub_callback_t */    
  unsigned int num_unmatched_exposures;
} callback_t;



/**
 * Check whether unit 1 can infect unit 2 and if so, whether it beats the
 * best (so far) matching potential target unit.
 */
void
check_and_choose (int id, gpointer arg)
{
  callback_t *callback_data;
  UNT_unit_list_t *units;
  UNT_unit_t *unit2;
  UNT_unit_t *unit1;
  local_data_t *local_data;
  double distance;
  double difference;
  ZON_zone_fragment_t *unit1_fragment, *unit2_fragment;
  gboolean contact_forbidden;
  ADSM_contact_type contact_type;
  unsigned long index;

  callback_data = (callback_t *) arg;
  g_assert (callback_data != NULL);

  unit1 = callback_data->unit1;
  if ( id != unit1->index )
  {
    units = callback_data->units;
    unit2 = UNT_unit_list_get (units, id);
    if ( unit2->state != Destroyed )
    {
      local_data = ( local_data_t * ) ( callback_data->self->model_data );
      GPtrArray **_contacts_to_prodtype = (GPtrArray **)callback_data->_contacts[unit2->production_type];

      for ( contact_type = 0; contact_type < callback_data->contact_count; contact_type++ )
      {
        GPtrArray *_contacts;
        sub_callback_t *contact;

        /* If unit 2 is quarantined, it cannot be the recipient of a direct
         * contact. */
        if (contact_type == 0 && unit2->quarantined)
          continue;

        _contacts = _contacts_to_prodtype[contact_type];
  
        for ( index = 0; index < _contacts->len; index ++ )
        {              
          contact = g_ptr_array_index ( _contacts, index );

          /* This will be set to TRUE if the search within the circle is
           * running for the first time, or if the search within the
           * circle found nothing and we are now using exhaustive search.
           */
          if ( contact->try_again )
          { 
            distance = GIS_distance ( unit1->x, unit1->y, unit2->x, unit2->y );
            /* Is unit 2 closer to unit 1 than the best match so far? */
            difference = fabs ( contact->movement_distance - distance );
            if ( contact->best_unit == NULL )
            {                     
              contact->best_unit = unit2;
              contact->best_unit_zone = callback_data->zones->membership[unit2->index];
              contact->best_unit_difference = difference;
              contact->min_difference = difference;
              contact->cumul_size = unit2->size;
              /* A best_unit has been filled in where there previously
               * was NULL.  This means that we can decrement the count
               * of unmatched exposures. */
              callback_data->num_unmatched_exposures--;
            }
            else if ( fabs ( difference - contact->min_difference ) <= EPSILON )
            {                        
              /* When we find a second potential recipient unit the same distance from
               * the source as the current closest potential recipient, we first check
               * if contact with the new find is forbidden by quarantine or zone rules.
               * If so, we can ignore it.  Otherwise, check if contact with the old find
               * is forbidden by zone rules; if so, we can take the new find.
               * Otherwise, the new find has a 1 in 2 chance
               * of replacing the older find, if they are the same size.  (If the new
               * find is half the size of the old one, it has a 1 in 3 chance; if it is
               * twice the size of the old one, it has a 2 in 3 chance.)  If we find a
               * third potential recipient unit the same distance from the source, its
               * chance of replacing the older choice is its size divided by the sum of
               * its size and the sizes of all of the older choices.  This gives the
               * same result as recording all the potential recipient units and
               * choosing among them afterwards. */
              unit1_fragment = callback_data->unit1_fragment;
              unit2_fragment = callback_data->zones->membership[unit2->index];
    
    
              contact_forbidden = ( ( ZON_level ( unit2_fragment ) > ZON_level ( unit1_fragment ) )
                                    || ( ZON_level ( unit1_fragment ) - ZON_level ( unit2_fragment ) > 1 )
                                    || ( ( ZON_level ( unit1_fragment ) - ZON_level ( unit2_fragment ) == 1 )
                                         && !ZON_nests_in ( unit2_fragment, unit1_fragment ) )
                                    || ( ( ZON_level ( unit2_fragment ) == ZON_level ( unit1_fragment ) )
                                         && !ZON_same_fragment ( unit2_fragment, unit1_fragment ) ) );
    
              if ( !contact_forbidden )
              {
                /* Contact with this new find (unit 2) is not forbidden.
                 * Is contact with the old find forbidden? If so, take
                 * the new find. */
                contact_forbidden = ( ( ZON_level ( contact->best_unit_zone ) > ZON_level ( unit1_fragment ) )
                                    || ( ZON_level ( unit1_fragment ) - ZON_level ( contact->best_unit_zone ) > 1 )
                                    || ( ( ZON_level ( unit1_fragment ) - ZON_level ( contact->best_unit_zone ) == 1 )
                                         && !ZON_nests_in ( contact->best_unit_zone, unit1_fragment ) )
                                    || ( ( ZON_level ( contact->best_unit_zone ) == ZON_level ( unit1_fragment ) )
                                         && !ZON_same_fragment ( contact->best_unit_zone, unit1_fragment ) ) );
                if (contact_forbidden)
                  {
                    /* Contact with the old find is forbidden: take the
                     * new find. */
                    #if DEBUG
                      g_debug ( "----- check_and_choose - Optimized Version: Replacing best_unit with this unit because contact with best_unit was forbidden" );
                    #endif
                    contact->cumul_size -= contact->best_unit->size;
                    contact->cumul_size += unit2->size;

                    contact->best_unit = unit2;
                    contact->best_unit_zone = unit2_fragment;
                    contact->best_unit_difference = difference;
                    if ( difference < contact->min_difference )
                      contact->min_difference = difference;
                  }
                else
                  {
                    /* Neither contact with the old find nor contact
                     * with the new find is forbidden; choose between
                     * the two at random. */
                    contact->cumul_size += unit2->size;
    
                    if ( RAN_num ( callback_data->rng ) < unit2->size / contact->cumul_size )
                    {                        
                      #if DEBUG
                        g_debug ( "----- check_and_choose - Optimized Version: Replacing best_unit with this unit because of a random number draw" );
                      #endif                           
                      contact->best_unit = unit2;
                      contact->best_unit_difference = difference;
                      if ( difference < contact->min_difference )
                        contact->min_difference = difference;
                    }
                    else
                    {
                      #if DEBUG
                        g_debug ( "----- check_and_choose - Optimized Version: NOT replacing best_unit with this unit" );
                      #endif                           
                    };
                  }
              } /* end of case where contact with the new find (unit2) is not forbidden. */
              else
              {
                #if DEBUG
                  g_debug ( "----- check_and_choose - Optimized Version:  Contact forbidden by zone rules or quarantine rules" );
                #endif                        
              }
            } /* end of case where the new find is the same distance from the source as the current best find */
            else if ( difference < contact->min_difference )
            {
              contact->best_unit = unit2;
              contact->best_unit_difference = difference;
              contact->min_difference = difference;
              contact->cumul_size = unit2->size;
            }
            else
            {
              #if DEBUG
                g_debug ( "----- check_and_choose - Optimized Version:  No fit found" );
              #endif       
            };
          };  /* end if try_again = TRUE for this contact */
        };  /* end of loop over desired contacts */
      };  /* end of loop over contact types */
    }  /*  End if unit2 is not Destroyed */
  }; /* if unit2 != unit1 */

  return;
}



typedef struct
{
  struct adsm_module_t_ *self;
  UNT_unit_list_t *units;
  ZON_zone_list_t *zones;
  EVT_new_day_event_t *event;
  RAN_gen_t *rng;
  EVT_event_queue_t *queue;   
  PDF_dist_t *_poisson;
  unsigned long new_infections;
  unsigned long exposure_attempts;
} new_day_event_hash_table_data;


void new_day_event_handler( gpointer key, gpointer value, gpointer user_data );

/**
 * Optimized Version:
 * Responds to a new day event by releasing any pending contacts and
 * stochastically generating exposures and infections.  This optimized version
 * calls a glib hash_table foreach function for each infectious unit in the 
 * list, which in turn does the work found in the non-optimized version of this
 * function.  This foreach call should be altered to an OMP pragma around a
 * for loop to utilize a parallel implementation of this loop, in future revisions.
 *
 * @param self the model.
 * @param units a list of units.
 * @param zones the zone list.
 * @param event a new day event.
 * @param rng a random number generator.
 * @param queue for any new events the model creates.
 */
void
handle_new_day_event (struct adsm_module_t_ *self, UNT_unit_list_t * units,
                      ZON_zone_list_t * zones, EVT_new_day_event_t * event,
                      RAN_gen_t * rng, EVT_event_queue_t * queue)
{
  local_data_t *local_data;
  EVT_event_t *pending_event;
  PDF_dist_t *poisson;
  new_day_event_hash_table_data *foreach_callback_data;
  GQueue *q;

#if DEBUG
  g_debug ("----- ENTER handle_new_day_event (%s) - Optimized Version", MODEL_NAME);
#endif

  /******                                                      ******/
  /* This is all the same as the previous version of this function */
  /******                                                    ******/
  local_data = (local_data_t *) (self->model_data);

  /* Release any pending (due to shipping delays) events. */
  local_data->rotating_index =
    (local_data->rotating_index + 1) % local_data->pending_infections->len;
  q = (GQueue *) g_ptr_array_index (local_data->pending_infections, local_data->rotating_index);
  while (!g_queue_is_empty (q))
    {
      /* Remove the event from this model's internal queue and place it in the
       * simulation's event queue. */
      pending_event = (EVT_event_t *) g_queue_pop_head (q);
#ifndef WIN_DLL
      /* Double-check that the event is coming out on the correct day. */
      g_assert (pending_event->u.exposure.day == event->day);
#endif
      EVT_event_enqueue (queue, pending_event);
      local_data->npending_infections--;
    }
  
  /* Allocate a distribution that will be used to pick the number of exposures
   * from a source. */
  poisson = PDF_new_poisson_dist ( 1.0 );

    /******                                                    ******/
   /*           Begin optimization additions/changes               */
  /******                                                    ******/

  foreach_callback_data = g_new( new_day_event_hash_table_data, 1 );

  /*  Fill in the user_data to be sent to the foreach hash table call */
  foreach_callback_data->self = self;
  foreach_callback_data->units = units;
  foreach_callback_data->zones = zones;
  foreach_callback_data->event = event;
  foreach_callback_data->rng = rng;
  foreach_callback_data->queue = queue; 
  foreach_callback_data->_poisson = poisson; 

  /*  Iterate over the infectious units.  This is a shortened list compared to the entire unit list */
  g_hash_table_foreach( _iteration.infectious_units, new_day_event_handler, foreach_callback_data );  
    
  /*  Free memory used by the user_data structure */
  g_free( foreach_callback_data );

  /* Free memory used by the Poisson distribution */
  PDF_free_dist (poisson);

#if DEBUG
  g_debug ("----- EXIT handle_new_day_event (%s) - Optimized Version", MODEL_NAME);
#endif
}

/**
 * Responds to a new day event by releasing any pending contacts and
 * stochastically generating exposures and infections.
 * This is the optimized version, which builds matrices of exposure attempt/production_type/contact_type
 * combinations, and sends them to the optimized version of check_and_choose.
 *
 * @param key       Unused, but required by g_hash_table_foreach()
 * @param value     A Pointer to the infectious unit, (source unit).
 * @param user_data A Pointer to the foreach_callback_data structure, as passed by the optimized handle_new_day_event() function.
 */
void new_day_event_handler( gpointer key, gpointer value, gpointer user_data )
{
  local_data_t *local_data;
  double disease_control_factors;
  double rate;
  PDF_dist_t *poisson;
  unsigned int nunits;          /* number of units */
  ADSM_contact_type contact_type;
  param_block_t **contact_type_block;
  UNT_unit_t *unit1, *unit2;
  unsigned int nprod_types, i, j, k;
  param_block_t *param_block;
  unsigned int unit2_index;
  unsigned int zone_index;
  REL_chart_t *control_chart;
  int nexposures;
  EVT_event_t *exposure;
  callback_t callback_data;
  gboolean contact_forbidden;
  double r, P;
  gboolean contact_is_adequate;
  ZON_zone_fragment_t *background_zone, *unit1_fragment, *unit2_fragment;
  int shipping_delay;
  int delay_index;
  GQueue *q;
  GPtrArray ***_contacts;

  struct adsm_module_t_ *self;
  UNT_unit_list_t *units;
  ZON_zone_list_t *zones;
  EVT_new_day_event_t *event;
  RAN_gen_t *rng;
  EVT_event_queue_t *queue;  
  unsigned long sum_exposures;
  double max_distance;
  
  
#if DEBUG
  g_debug ("----- ENTER new_day_event_handler - Optimized Version" );
#endif
  
  max_distance = 0.0;  
  sum_exposures = 0;

  new_day_event_hash_table_data *foreach_callback_data = (new_day_event_hash_table_data *) user_data;
  
  self = foreach_callback_data->self;
  units = foreach_callback_data->units;
  zones = foreach_callback_data->zones;
  event = foreach_callback_data->event;
  rng = foreach_callback_data->rng;
  queue = foreach_callback_data->queue;  

  local_data = (local_data_t *) (self->model_data);

  /*  Set the usual items for this function from the check_and_choose callback structure*/
  callback_data.self = self;
  callback_data.units = units;
  callback_data.zones = zones;
  callback_data.rng = rng;

  poisson = foreach_callback_data->_poisson;
  background_zone = ZON_zone_list_get_background ( zones );
  nprod_types = local_data->production_types->len;
  nunits = UNT_unit_list_length ( units );
    
  unit1 = (UNT_unit_t *) value;
  unit1_fragment = zones->membership[unit1->index];
  callback_data.unit1_fragment = unit1_fragment;      
  callback_data.unit1 = unit1;

  #if DEBUG
    g_debug ("new_day_event_handler:  unit \"%s\" is %s (%i), state is %s",
             unit1->official_id, unit1->production_type_name,
             unit1->production_type, UNT_state_name[unit1->state]);
  #endif

  /*  How many contact types do we have?  */
  j = 0;
  for ( contact_type = ADSM_DirectContact; contact_type <= ADSM_IndirectContact; contact_type++ )
    j++;

  /*  Begin building 1-dimension of the attempted exposure matrix */
  _contacts = g_new( GPtrArray **, nprod_types );
  
  /*  Set some more callback data for check_and_choose to use */
  callback_data.contact_count = j;
  callback_data.production_type_count = nprod_types;
  callback_data._contacts = _contacts; 

  /*  Iterate over all contact/production-type pairs and build the remaining dimensions of the matrix of desired matches for exposure attempts */
  for (i = 0; i < nprod_types; i++)
  {        
    _contacts[i] = g_new( GPtrArray *, callback_data.contact_count );
    for ( j = 0, contact_type = ADSM_DirectContact; contact_type <= ADSM_IndirectContact; j++, contact_type++ )
    {
      contact_type_block = local_data->param_block[contact_type][unit1->production_type];

      /*  Create this element of the 2nd Dimension of the exposure attempt matrix */
      _contacts[i][j] = g_ptr_array_new();

      if (contact_type_block != NULL)
      {
        /*  Get this combination, contact_type/production_type, param_block from memory */              
        param_block = contact_type_block[i];

        if ( param_block != NULL )
        {
          #if DEBUG
            g_debug ("new_day_event_handler: %s/%s",
                     (char *) g_ptr_array_index (local_data->production_types, i),
                     ADSM_contact_type_name[contact_type]);
          #endif

          /*  Can this exposure attempt happen? */
          if ( !((unit1->quarantined) && (contact_type == ADSM_DirectContact)) )
          {
            /*  Check spread parameters to see if this unit's state can spread for this contact type */ 
            if ( (unit1->state == Latent && param_block->latent_units_can_infect == TRUE) || 
                 (unit1->state == InfectiousSubclinical && param_block->subclinical_units_can_infect == TRUE)
                 || ( (unit1->state != Latent) && (unit1->state != InfectiousSubclinical) )
               )
            { 
              /*  Okay, this unit CAN spread disease for this contact/production_type pair 
                  Establish the parameters of this exposure attempt.  */
                
                
              /* Compute a multiplier to reduce the rate of movement once the
               * community is aware of an outbreak. */
              if ( !local_data->outbreak_known )
                disease_control_factors = REL_chart_lookup (0, param_block->movement_control);
              else if (ZON_same_zone (background_zone, unit1_fragment))
                disease_control_factors =
                  REL_chart_lookup (event->day - local_data->public_announcement_day,
                                    param_block->movement_control);
              else
              {
                zone_index = ZON_level (unit1_fragment) - 1;
                #if DEBUG
                  g_debug ("zone index = %u", zone_index);
                #endif
                control_chart =
                  local_data->movement_control[contact_type][zone_index][unit1->production_type];
                if (control_chart == NULL)
                {
                  #if DEBUG
                    g_debug ("new_day_event_handler:  unit is in \"%s\" zone, no special control chart for %s units in this zone",
                             unit1_fragment->parent->name, unit1->production_type_name);
                  #endif
                  control_chart = param_block->movement_control;
                }
                else
                {
                  #if DEBUG
                    g_debug ("new_day_event_handler:  unit is in \"%s\" zone, using special control chart for %s units in this zone",
                             unit1_fragment->parent->name, unit1->production_type_name);
                  #endif
                  ;
                }
                disease_control_factors =
                  REL_chart_lookup (event->day - local_data->public_announcement_day,
                                    control_chart);
              }; /*  END Compute a multiplier */


              /* Pick the number of exposures from this source.
               * If a fixed number of movements is specified, use it.
               * Otherwise, pick a number from the Poisson distribution. */
              if (param_block->fixed_movement_rate > 0)
              {
                rate = param_block->fixed_movement_rate * disease_control_factors;
                #if DEBUG
                  g_debug ("new_day_event_handler:  contact rate = %g (fixed) * %g = %g",
                           param_block->fixed_movement_rate, disease_control_factors, rate);
                #endif
                nexposures = (int) ((event->day + 1) * rate) - (int) (event->day * rate);
                sum_exposures = sum_exposures + nexposures;
              }
              else
              {
                rate = param_block->movement_rate * disease_control_factors;
                #if DEBUG
                  g_debug ("new_day_event_handler:  contact rate = %g * %g = %g",
                           param_block->movement_rate, disease_control_factors, rate);
                #endif
                poisson->u.poisson.mu = rate;
                nexposures = (int) (PDF_random (poisson, rng));
                sum_exposures = sum_exposures + nexposures;                          
              }
              #if DEBUG
                if (nexposures > 0)
                {
                  g_debug ("new_day_event_handler: Day %i, want %i %ss from unit \"%s\" to production_type \"%s\"",
                           event->day, nexposures, 
                           ADSM_contact_type_name[contact_type],
                           unit1->official_id,
                           (char *) g_ptr_array_index (local_data->production_types, i));
                }
              #endif

              /*  Now create and fillin the 3rd and final dimension of the 
                  exposure attempt matrix, to be used by check_and_choose  */
              for ( k = 0; k < nexposures; k++ )
              {
                /*  Allocate some memory for this data */  
                sub_callback_t *sub_callback = g_new(sub_callback_t, 1);

                /*  Add the pointer to this data to the matrix */ 
                g_ptr_array_add( _contacts[i][j], sub_callback );

                sub_callback->try_again = TRUE;
                sub_callback->contact_type = contact_type;
                sub_callback->recipient_production_type = i;
                sub_callback->best_unit = NULL;
                sub_callback->movement_distance = PDF_random (param_block->distance_dist, rng);
                if (sub_callback->movement_distance < 0)
                  sub_callback->movement_distance = 0;

                /*  Use maximum distance desired for the bounding box in RTree */
                if ( sub_callback->movement_distance > max_distance )
                  max_distance = sub_callback->movement_distance;
                #if DEBUG
                  g_debug ( "new_day_event_handler:  contact of %g km",sub_callback->movement_distance );
                #endif  

              };  /*  END nexposures for loop */                
            } /* end of if current state can create exposures */
          } /* end of if quarantine not in effect */
          else
          {
#if DEBUG
            g_debug ( "new_day_event_handler:  Unit1 is quarantined and this is direct contact" );
#endif                    
          };
        }
      }
        
    }; /* end of loop over contact types */
  }; /* end of loop over recipient production types */

  if ( sum_exposures > 0 )
  {
#if DEBUG
    g_debug ( "new_day_event_handler:  Total exposures sought for this unit: %lu", sum_exposures );
#endif          

    callback_data.num_unmatched_exposures = sum_exposures;
    spatial_search_circle_by_id (units->spatial_index, unit1->index,
                                 MAX(local_data->min_radius, max_distance*2.0 + EPSILON),
                                 check_and_choose, &callback_data);

    /* A re-search using the exhaustive method is necessary if some
     * exposures remain unmatched. */
    if (callback_data.num_unmatched_exposures > 0)
    {
      /*  Iterate over the results and reset "try_again" status based on each 
          match's status.  A re-search using the exhaustive method may be necessary... */
      for( i = 0; i < nprod_types; i++ )
      {
        for( j = 0, contact_type = ADSM_DirectContact; contact_type <= ADSM_IndirectContact; j++, contact_type++ )
        {
          GPtrArray *t_array = NULL;
          t_array = _contacts[i][j];
                
          for( k = 0; k < t_array->len; k++ )
          {                       
            sub_callback_t *tsub = g_ptr_array_index( t_array, k );
            /*  Did we not find a match?? */ 
            tsub->try_again = ( tsub->best_unit == NULL );
          }
        };
      }
#if DEBUG
      g_debug ( "new_day_event_handler:  Using exhaustive search" );
#endif
      /*  Iterate over the entire list of units and find matches for each 
          needed exposure, using the check_and_choose function */
      for (unit2_index = 0; unit2_index < nunits; unit2_index++)
      {
        check_and_choose (unit2_index, &callback_data);
      };
    };


    /*  Okay, now we "should" have all the "best" fit's for each desired 
        contact/production-type pair, items.  */
    /*  Iterate over the results and post exposure and infection events 
        when applicable, and simultaneously delete dynamic memory used */
    for( i = 0; i < nprod_types; i++ )
    {
      for( j = 0, contact_type = ADSM_DirectContact; contact_type <= ADSM_IndirectContact; j++, contact_type++ )
      {
        GPtrArray *t_array;

        contact_type_block = local_data->param_block[contact_type][unit1->production_type];

        if ( contact_type_block != NULL )
        {
          t_array = _contacts[i][j];

          param_block = contact_type_block[i];

          if ( param_block != NULL )
          {
            /*  Iterate over each exposure attempt for this contact/production_type pair */ 
            for( k = 0; k < t_array->len; k++ )
            {
              sub_callback_t *tsub = g_ptr_array_index( t_array, k );
              if (tsub->best_unit != NULL)
              {
                /*  Create exposure and infection events here  */

                /* An eligible recipient unit (correct production type, not
                 * Destroyed, in range, etc... ) was found. */
                unit2 = tsub->best_unit;
#if DEBUG
                g_debug ("new_day_event_handler:  unit \"%s\" within %g km of %g",
                         unit2->official_id,
                         tsub->best_unit_difference, tsub->movement_distance);
#endif
                /* Check whether contact with this unit is forbidden by the
                 * zone rules. */
                unit2_fragment = zones->membership[unit2->index];
                contact_forbidden = FALSE;
                if ( ZON_level ( unit2_fragment ) > ZON_level ( unit1_fragment ) )
                {
                  contact_forbidden = TRUE;
#if DEBUG
                  g_debug ("new_day_event_handler: contact forbidden: contact from unit \"%s\" in \"%s\" zone, level %i to unit \"%s\" in \"%s\" zone, level %i would violate higher-to-lower rule",
                           unit1->official_id,
                           unit1_fragment->parent->name,
                           unit1_fragment->parent->level,
                           unit2->official_id,
                           unit2_fragment->parent->name,
                           unit2_fragment->parent->level);
#endif
                }
                else if ( ZON_level ( unit2_fragment ) == ZON_level ( unit1_fragment ) )
                {
                  if ( !ZON_same_fragment ( unit2_fragment, unit1_fragment ) )
                  {
                    contact_forbidden = TRUE;
#if DEBUG
                    g_debug ("new_day_event_handler: contact forbidden: contact from unit \"%s\" to unit \"%s\" in separate foci of \"%s\" zone would violate separate foci rule",
                             unit1->official_id, unit2->official_id, unit1_fragment->parent->name);
#endif
                  }
                }
                else /* ZON_level ( unit2_fragment ) < ZON_level ( unit1_fragment ) */
                {
                  if ( ZON_level ( unit1_fragment ) - ZON_level ( unit2_fragment ) > 1 )
                  {
                    contact_forbidden = TRUE;
#if DEBUG
                    g_debug ("new_day_event_handler: contact forbidden: contact from unit \"%s\" in \"%s\" zone, level %i to unit \"%s\" in non-adjacent \"%s\" zone, level %i",
                             unit1->official_id,
                             unit1_fragment->parent->name,
                             unit1_fragment->parent->level,
                             unit2->official_id,
                             unit2_fragment->parent->name,
                             unit2_fragment->parent->level);
#endif
                  }
                  else if ( !ZON_nests_in ( unit2_fragment, unit1_fragment ) )
                  {
                    contact_forbidden = TRUE;
#if DEBUG
                    g_debug ("new_day_event_handler: contact forbidden: contact from unit \"%s\" in \"%s\" zone, level %i to unit \"%s\" in non-nested focus of \"%s\" zone, level %i",
                             unit1->official_id,
                             unit1_fragment->parent->name,
                             unit1_fragment->parent->level,
                             unit2->official_id,
                             unit2_fragment->parent->name,
                             unit2_fragment->parent->level);
#endif
                  }
                }

                /* If none of the zone rules forbade contact, create the exposure. */
                if ( !contact_forbidden )
                {
                  /* Announce the exposure. */
#if DEBUG
                  g_debug ("new_day_event_handler:  unit \"%s\" unit exposed", unit2->official_id);
#endif

                  /* Is the exposure adequate (i.e., will it cause infection in a susceptible unit)? */
                  if (contact_type == ADSM_DirectContact && unit1->prevalence_curve != NULL)
                    P = unit1->prevalence;
                  else
                    P = param_block->prob_infect;
                  r = RAN_num (rng);
                  contact_is_adequate = (r < P);

                  shipping_delay = (int) round (PDF_random (param_block->shipping_delay, rng));  
                  exposure = EVT_new_exposure_event (unit1, unit2, event->day,
                                                     contact_type, TRUE, 
                                                     contact_is_adequate, shipping_delay);
                  exposure->u.exposure.contact_type = contact_type; /* This seems redundant (exposure.cause does the same thing), but there's probably a reason.... */
                        
                  if (shipping_delay <= 0)
                  {
                    EVT_event_enqueue (queue, exposure);
                  }
                  else
                  {
                    exposure->u.exposure.day += shipping_delay;
                    if (shipping_delay > local_data->pending_infections->len)
                    {
                      adsm_extend_rotating_array (local_data->pending_infections,
                                                         shipping_delay, local_data->rotating_index);
                    }

                    delay_index = (local_data->rotating_index + shipping_delay) % local_data->pending_infections->len;
                    q = (GQueue *) g_ptr_array_index (local_data->pending_infections, delay_index);
                    g_queue_push_tail (q, exposure);
                    local_data->npending_infections++;
                  };

                  /* If contact was adequate, queue an attempt to infect. */
                  if( contact_is_adequate )
                  {
#if DEBUG
                    g_debug ("new_day_event_handler:  r (%g) < P (%g), unit \"%s\" infected", r, P,
                             unit2->official_id);
#endif
                    ;
                  }
                  else
                  {
#if DEBUG
                    g_debug ("new_day_event_handler:  r (%g) >= P (%g), unit \"%s\" not infected", r,
                             P, unit2->official_id);
#endif
                  };
                } /* contact was not forbidden */
              } 
              else  /*  hmmm no match was found... */
              {
#if DEBUG
                g_debug ("new_day_event_handler:  no recipient can be found at ~%g km from unit \"%s\" for this instance of this contact_type / production_type pair" ,
                         tsub->movement_distance, unit1->official_id);
#endif
                ;
              };  /*  END if a unit match was found */
                  
              /*  Free the structure memory stored at this location in this GPtrArray  */
              g_free( tsub );
                    
            };  /*  END for loop iteration over this GPtrArray  */
          };

          /* Free memory for GPtrArray */
          g_ptr_array_free( t_array, TRUE );
          _contacts[i][j] = NULL; /* just in case */

        }; /*  END iteration over production_types  */
      };

      /* Free memory for this row */
      g_free( _contacts[i] );
    }; /*  END iteration over contact_types  */
  } /*  END if contact count > 0 */
  else
  {
    /* Free memory */
    for (i = 0; i < nprod_types; i++)
    {
      for( j = 0, contact_type = ADSM_DirectContact; contact_type <= ADSM_IndirectContact; contact_type++, j++ )
      {
        g_ptr_array_free (_contacts[i][j], TRUE);
      }
      g_free( _contacts[i] );
    }
  }
  g_free( _contacts );
  _contacts = NULL;  /*  just in case */
  
#if DEBUG
  g_debug ("----- EXIT new_day_event_handler - Optimized Version" );
#endif  
 }



/**
 * Records the day on which the outbreak is publically announced.  This is
 * important because the movement rate decreases with community awareness of an
 * outbreak.
 *
 * @param self the model.
 * @param event a public announcement event.
 */
void
handle_public_announcement_event (struct adsm_module_t_ *self,
                                  EVT_public_announcement_event_t * event)
{
  local_data_t *local_data;

#if DEBUG
  g_debug ("----- ENTER handle_public_announcement_event (%s)", MODEL_NAME);
#endif
  local_data = (local_data_t *) (self->model_data);
  if (local_data->outbreak_known == FALSE)
    {
      local_data->outbreak_known = TRUE;
      local_data->public_announcement_day = event->day;
#if DEBUG
      g_debug ("community is now aware of outbreak, movement will slow");
#endif
    }

#if DEBUG
  g_debug ("----- EXIT handle_public_announcement_event (%s)", MODEL_NAME);
#endif
}



/**
 * Runs this model.
 *
 * Side effects: may change the state of one or more units in list.
 *
 * @param self the model.
 * @param units a list of units.
 * @param zones a list of zones.
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
      handle_new_day_event (self, units, zones, &(event->u.new_day), rng, queue);
      break;
    case EVT_PublicAnnouncement:
      handle_public_announcement_event (self, &(event->u.public_announcement));
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

  local_data = (local_data_t *) (self->model_data);
  return (local_data->npending_infections > 0);
}



/**
 * Reports whether this model has any pending infections to cause.
 *
 * @param self the model.
 * @return TRUE if the model has pending infections.
 */
gboolean
has_pending_infections (struct adsm_module_t_ * self)
{
  local_data_t *local_data;

  local_data = (local_data_t *) (self->model_data);
  return (local_data->npending_infections > 0);
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
  local_data_t *local_data;
  ADSM_contact_type contact_type;
  param_block_t ***contact_type_block;
  REL_chart_t ***contact_type_chart;
  unsigned int nprod_types, nzones, i, j;
  param_block_t *param_block;
  REL_chart_t *chart;
  char *substring, *chararray;

  local_data = (local_data_t *) (self->model_data);
  s = g_string_new (NULL);
  g_string_append_printf (s, "<%s", MODEL_NAME);

  /* Add the parameter block for each to-from combination of production
   * types. */
  nprod_types = local_data->production_types->len;
  for (contact_type = ADSM_DirectContact; contact_type <= ADSM_IndirectContact; contact_type++)
    {
      contact_type_block = local_data->param_block[contact_type];
      for (i = 0; i < nprod_types; i++)
        if (contact_type_block[i] != NULL)
          for (j = 0; j < nprod_types; j++)
            if (contact_type_block[i][j] != NULL)
              {
                param_block = contact_type_block[i][j];
                g_string_append_printf (s, "\n  for %s -> %s (%s)",
                                        (char *) g_ptr_array_index (local_data->production_types,
                                                                    i),
                                        (char *) g_ptr_array_index (local_data->production_types,
                                                                    j),
                                        ADSM_contact_type_name[contact_type]);
                if (param_block->fixed_movement_rate > 0)
                  g_string_append_printf (s, "\n    fixed-movement-rate=%g",
                                          param_block->fixed_movement_rate);
                else
                  g_string_append_printf (s, "\n    movement-rate=%g", param_block->movement_rate);

                substring = PDF_dist_to_string (param_block->distance_dist);
                g_string_append_printf (s, "\n    distance=%s", substring);
                g_free (substring);

                substring = PDF_dist_to_string (param_block->shipping_delay);
                g_string_append_printf (s, "\n    delay=%s", substring);
                g_free (substring);

                g_string_append_printf (s, "\n    prob-infect=%g", param_block->prob_infect);

                substring = REL_chart_to_string (param_block->movement_control);
                g_string_append_printf (s, "\n    movement-control=%s", substring);
                g_free (substring);

                g_string_append_printf (s, "\n    latent-units-can-infect=%s",
                                        param_block->latent_units_can_infect ? "true" : "false");
                g_string_append_printf (s, "\n    subclinical-units-can-infect=%s",
                                        param_block->
                                        subclinical_units_can_infect ? "true" : "false");
              }
    }

  /* Add the movement control chart for each production type-zone
   * combination. */
  nzones = ZON_zone_list_length (local_data->zones);
  for (contact_type = ADSM_DirectContact; contact_type <= ADSM_IndirectContact; contact_type++)
    {
      contact_type_chart = local_data->movement_control[contact_type];
      for (i = 0; i < nzones; i++)
        for (j = 0; j < nprod_types; j++)
          if (contact_type_chart[i][j] != NULL)
            {
              chart = contact_type_chart[i][j];
              g_string_append_printf (s, "\n  for %s in \"%s\" zone (%s)",
                                      (char *) g_ptr_array_index (local_data->production_types,
                                                                  j),
                                      ZON_zone_list_get (local_data->zones, i)->name,
                                      ADSM_contact_type_name[contact_type]);
              substring = REL_chart_to_string (chart);
              g_string_append_printf (s, "\n    movement-control=%s", substring);
              g_free (substring);
            }
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
local_free (struct adsm_module_t_ *self)
{
  local_data_t *local_data;
  unsigned int nprod_types, nzones, i, j;
  ADSM_contact_type contact_type;
  param_block_t ***contact_type_block;
  param_block_t *param_block;
  REL_chart_t ***contact_type_chart;
  GQueue *q;

#if DEBUG
  g_debug ("----- ENTER free (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  /* Free each of the parameter blocks. */
  nprod_types = local_data->production_types->len;
  for (contact_type = ADSM_DirectContact; contact_type <= ADSM_IndirectContact; contact_type++)
    {
      contact_type_block = local_data->param_block[contact_type];
      for (i = 0; i < nprod_types; i++)
        if (contact_type_block[i] != NULL)
          {
            for (j = 0; j < nprod_types; j++)
              if (contact_type_block[i][j] != NULL)
                {
                  param_block = contact_type_block[i][j];
                  /* Free the dynamically-allocated parts of the parameter block. */
                  PDF_free_dist (param_block->distance_dist);
                  PDF_free_dist (param_block->shipping_delay);
                  REL_free_chart (param_block->movement_control);
                  /* Free the parameter block itself. */
                  g_free (param_block);
                }
            /* Free this row of the 2D array. */
            g_free (contact_type_block[i]);
          }
      /* Free the array of pointers to rows. */
      g_free (contact_type_block);
    }

  /* Free the movement control charts for units inside zones. */
  nzones = ZON_zone_list_length (local_data->zones);
  for (contact_type = ADSM_DirectContact; contact_type <= ADSM_IndirectContact; contact_type++)
    {
      contact_type_chart = local_data->movement_control[contact_type];
      for (i = 0; i < nzones; i++)
        {
          for (j = 0; j < nprod_types; j++)
            REL_free_chart (contact_type_chart[i][j]);

          /* Free this row of the 2D array. */
          g_free (contact_type_chart[i]);

        }
      /* Free the array of pointers to rows. */
      g_free (contact_type_chart);
    }

  /* Free any pending infections. */
  for (i = 0; i < local_data->pending_infections->len; i++)
    {
      q = (GQueue *) g_ptr_array_index (local_data->pending_infections, i);
      while (!g_queue_is_empty (q))
        EVT_free_event (g_queue_pop_head (q));
      g_queue_free (q);
    }
  g_ptr_array_free (local_data->pending_infections, TRUE);

  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Adds a set of from-production-type/to-production-type combination specific
 * parameters to a contact spread model.
 *
 * @param data this module ("self"), but cast to a void *.
 * @param dict the SQL query result as a GHashTable in which key = colname,
 *   value = value, both in (char *) format.
 * @return 0
 */
static int
set_params (void *data, GHashTable *dict)
{
  adsm_module_t *self;
  local_data_t *local_data;
  sqlite3 *params;
  guint from_production_type, to_production_type;
  char *tmp_text;
  ADSM_contact_type contact_type;
  param_block_t ***contact_type_block;
  param_block_t *p;
  long int tmp;
  gboolean use_fixed_contact_rate;
  guint pdf_id, rel_id;

#if DEBUG
  g_debug ("----- ENTER set_params (%s)", MODEL_NAME);
#endif

  self = (adsm_module_t *)data;
  local_data = (local_data_t *) (self->model_data);
  params = local_data->db;

  g_assert (g_hash_table_size (dict) == 11);

  /* Find out which to-from production type combination these parameters apply
   * to. */
  from_production_type =
    adsm_read_prodtype (g_hash_table_lookup (dict, "src_prodtype"),
                        local_data->production_types);
  to_production_type =
    adsm_read_prodtype (g_hash_table_lookup (dict, "dest_prodtype"),
                        local_data->production_types);

  /* Find out whether these parameters are for direct or indirect contact. */
  tmp_text = g_hash_table_lookup (dict, "contact_type");
  if (strcmp (tmp_text, "direct") == 0)
    contact_type = ADSM_DirectContact;
  else if (strcmp (tmp_text, "indirect") == 0)
    contact_type = ADSM_IndirectContact;
  else
    g_assert_not_reached ();

  /* If necessary, create a row in the 2D array for this from-production-type. */
  contact_type_block = local_data->param_block[contact_type];
  if (contact_type_block[from_production_type] == NULL)
    {
      contact_type_block[from_production_type] =
        g_new0 (param_block_t *, local_data->production_types->len);
    }
  /* Check that we are not overwriting an existing parameter block (that would
   * indicate a bug). */
  g_assert (contact_type_block[from_production_type][to_production_type] == NULL);

  /* Create a new parameter block. */
  p = g_new (param_block_t, 1);
  contact_type_block[from_production_type][to_production_type] = p;

  /* Read the parameters. */
  errno = 0;
  tmp = strtol (g_hash_table_lookup (dict, "use_fixed_contact_rate"), NULL, /* base */ 10);
  g_assert (errno != ERANGE && errno != EINVAL);
  g_assert (tmp == 0 || tmp == 1);
  use_fixed_contact_rate = (tmp == 1);
  errno = 0;
  p->movement_rate = strtod (g_hash_table_lookup (dict, "contact_rate"), NULL);
  g_assert (errno != ERANGE);
  if (use_fixed_contact_rate)
    {
      /* If fixed_movement_rate >= 0, use it instead of the Poisson distribution */
      p->fixed_movement_rate = p->movement_rate;
    }
  else
    {
      p->fixed_movement_rate = -1;
    }
  /* The movement rate cannot be negative. */
  if (p->movement_rate < 0)
    {
      g_warning ("movement rate cannot be negative, setting to 0");
      p->movement_rate = 0;
    }

  errno = 0;
  pdf_id = strtol (g_hash_table_lookup (dict, "distance_distribution_id"), NULL, /* base */ 10);
  g_assert (errno != ERANGE && errno != EINVAL);
  p->distance_dist = PAR_get_PDF (params, pdf_id);
  /* No part of the distance distribution can be negative. */
  if (!p->distance_dist->has_inf_lower_tail)
    {
      g_assert (PDF_cdf (-EPSILON, p->distance_dist) == 0);
    }

  tmp_text = g_hash_table_lookup (dict, "transport_delay_id");
  if (tmp_text != NULL)
    {
      errno = 0;
      pdf_id = strtol (tmp_text, NULL, /* base */ 10);
      g_assert (errno != ERANGE && errno != EINVAL);
      p->shipping_delay = PAR_get_PDF (params, pdf_id);
    }
  else
    p->shipping_delay = PDF_new_point_dist (0);

  errno = 0;
  p->prob_infect = strtod (g_hash_table_lookup (dict, "infection_probability"), NULL);
  g_assert (errno != ERANGE);
  g_assert (p->prob_infect >= 0 && p->prob_infect <= 1);

  errno = 0;
  rel_id = strtol (g_hash_table_lookup (dict, "movement_control_id"), NULL, /* base */ 10);
  g_assert (errno != ERANGE && errno != EINVAL);  
  p->movement_control = PAR_get_relchart (params, rel_id);
  /* The movement rate multiplier cannot go negative. */
  g_assert (REL_chart_min (p->movement_control) >= 0);

  errno = 0;
  tmp = strtol (g_hash_table_lookup (dict, "latent_animals_can_infect_others"), NULL, /* base */ 10);
  g_assert (errno != ERANGE && errno != EINVAL);
  g_assert (tmp == 0 || tmp == 1);
  p->latent_units_can_infect = (tmp == 1);

  errno = 0;
  tmp = strtol (g_hash_table_lookup (dict, "subclinical_animals_can_infect_others"), NULL, /* base */ 10);
  g_assert (errno != ERANGE && errno != EINVAL);
  g_assert (tmp == 0 || tmp == 1);
  p->subclinical_units_can_infect = (tmp == 1);

#if DEBUG
  g_debug ("----- EXIT set_params (%s)", MODEL_NAME);
#endif

  return 0;
}



/**
 * Adds a set of zone/production type combination specific parameters to a
 * contact spread model.
 *
 * @param data this module ("self"), but cast to a void *.
 * @param dict the SQL query result as a GHashTable in which key = colname,
 *   value = value, both in (char *) format.
 * @return 0
 */
static int
set_zone_params (void *data, GHashTable *dict)
{
  adsm_module_t *self;
  local_data_t *local_data;
  sqlite3 *params;
  guint zone, production_type;
  char *tmp_text;
  ADSM_contact_type contact_type;
  REL_chart_t ***contact_type_chart;
  guint rel_id;
  REL_chart_t *movement_control;

  #if DEBUG
    g_debug ("----- ENTER set_zone_params (%s)", MODEL_NAME);
  #endif

  self = (adsm_module_t *)data;
  local_data = (local_data_t *) (self->model_data);
  params = local_data->db;

  g_assert (g_hash_table_size (dict) == 4);

  /* Find out which zone/production type combination these parameters apply
   * to. */
  zone = adsm_read_zone (g_hash_table_lookup (dict, "zone"), local_data->zones);
  production_type = adsm_read_prodtype (g_hash_table_lookup (dict, "prodtype"),
                                       local_data->production_types);

  /* Find out whether these parameters are for direct or indirect contact. */
  tmp_text = g_hash_table_lookup (dict, "contact_type");
  if (strcmp (tmp_text, "direct") == 0)
    contact_type = ADSM_DirectContact;
  else if (strcmp (tmp_text, "indirect") == 0)
    contact_type = ADSM_IndirectContact;
  else
    g_assert_not_reached ();

  /* Check that we are not overwriting an existing chart (that would
   * indicate a bug). */
  contact_type_chart = local_data->movement_control[contact_type];
  g_assert (contact_type_chart[zone][production_type] == NULL);

  /* Read the parameter. */
  errno = 0;
  rel_id = strtol (g_hash_table_lookup (dict, "zone_direct_movement_id"), NULL, /* base */ 10);
  g_assert (errno != ERANGE && errno != EINVAL);  
  movement_control = PAR_get_relchart (params, rel_id);
  /* The movement rate multiplier cannot go negative. */
  g_assert (REL_chart_min (movement_control) >= 0);
  contact_type_chart[zone][production_type] = movement_control;

  #if DEBUG
    g_debug ("----- EXIT set_zone_params (%s)", MODEL_NAME);
  #endif

  return 0;
}



/**
 * A callback function used with estimate_density() below. It receives a
 * pointer to a guint and increments that guint.
 *
 * @param id not used.
 * @param data a pointer to a counter (guint *), cast to a gpointer.
 */
static void
estimate_density_count_unit (int id, gpointer data)
{
  guint *count;
  count = (guint *) data;
  *count += 1;
  return;
}



/**
 * Estimate the density of the population by counting units in a rectangle in
 * the center of the study area. Hopefully this will not be wildly off.
 *
 * @param units a list of units.
 */
static double
estimate_density (UNT_unit_list_t *units)
{
  double side_length = 25; /* km */
  double center_x, center_y;
  double x1, y1, x2, y2;
  guint count = 0;
  double density;
  
  center_x = units->min_x + 0.5 * (units->max_x - units->min_x);
  center_y = units->min_y + 0.5 * (units->max_y - units->min_y);
  x1 = center_x - (side_length / 2.0);
  y1 = center_y - (side_length / 2.0);
  x2 = center_x + (side_length / 2.0);
  y2 = center_y + (side_length / 2.0);
  spatial_search_rectangle (units->spatial_index, x1, y1, x2, y2,
                            estimate_density_count_unit, &count);
  density = count / (side_length * side_length);
  #if DEBUG
    g_debug ("estimated density = %u units/%.0f sq km = %.2f units/sq km",
             count, side_length * side_length, density);
  #endif
  return density;
}



/**
 * Returns a new contact spread model.
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
    EVT_PublicAnnouncement,
    0
  };
  unsigned int nprod_types, nzones, i;
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
  self->has_pending_infections = has_pending_infections;
  self->to_string = to_string;
  self->printf = adsm_model_printf;
  self->fprintf = adsm_model_fprintf;
  self->free = local_free;

  /* local_data->param_block holds two 2D arrays of parameter blocks, where
   * each block holds the parameters for one to-from combination of production
   * types.  The first level of indexing is by contact type, then by source
   * production type (rows), then by recipient production type (columns).
   * Initially, all row pointers are NULL.  Rows will be created as needed in
   * the set_params function. */
  local_data->production_types = units->production_type_names;
  nprod_types = local_data->production_types->len;
  for (i = 0; i < ADSM_NCONTACT_TYPES; i++)
    local_data->param_block[i] = NULL;
  local_data->param_block[ADSM_DirectContact] = g_new0 (param_block_t **, nprod_types);
  local_data->param_block[ADSM_IndirectContact] = g_new0 (param_block_t **, nprod_types);

  /* local_data->movement_control holds movement control charts by zone and
   * production type.  The first level of indexing is by contact type, then by
   * zone (rows), then by source production type (columns).  Initially, the
   * rows contain all NULL pointers. */
  local_data->zones = zones;
  nzones = ZON_zone_list_length (zones);
  for (i = 0; i < ADSM_NCONTACT_TYPES; i++)
    local_data->movement_control[i] = NULL;
  local_data->movement_control[ADSM_DirectContact] = g_new0 (REL_chart_t **, nzones);
  for (i = 0; i < nzones; i++)
    local_data->movement_control[ADSM_DirectContact][i] = g_new0 (REL_chart_t *, nprod_types);
  local_data->movement_control[ADSM_IndirectContact] = g_new0 (REL_chart_t **, nzones);
  for (i = 0; i < nzones; i++)
    local_data->movement_control[ADSM_IndirectContact][i] = g_new0 (REL_chart_t *, nprod_types);

  /* No outbreak has been announced yet. */
  local_data->outbreak_known = FALSE;
  local_data->public_announcement_day = 0;

  /* Initialize an array for delayed contacts.  We don't know yet how long the
   * the array needs to be, since that will depend on values we sample from the
   * delay distribution, so we initialize it to length 1. */
  local_data->pending_infections = g_ptr_array_new ();
  g_ptr_array_add (local_data->pending_infections, g_queue_new ());
  local_data->npending_infections = 0;
  local_data->rotating_index = 0;

  /* Call the set_params function to read the from-production-type/
   * to-production-type combination specific parameters. */
  local_data->db = params;
  sqlite3_exec_dict (params,
                     "SELECT src_prodtype.name AS src_prodtype,dest_prodtype.name AS dest_prodtype,\"direct\" AS contact_type,use_fixed_contact_rate,contact_rate,distance_distribution_id,transport_delay_id,infection_probability,movement_control_id,latent_animals_can_infect_others,subclinical_animals_can_infect_others "
                     "FROM ScenarioCreator_productiontype src_prodtype,ScenarioCreator_productiontype dest_prodtype,ScenarioCreator_productiontypepairtransmission pairing,ScenarioCreator_directspread direct "
                     "WHERE src_prodtype.id=pairing.source_production_type_id "
                     "AND dest_prodtype.id=pairing.destination_production_type_id "
                     "AND pairing.direct_contact_spread_id = direct.id "
                     "UNION SELECT src_prodtype.name AS src_prodtype,dest_prodtype.name AS dest_prodtype,\"indirect\" AS contact_type,use_fixed_contact_rate,contact_rate,distance_distribution_id,transport_delay_id,infection_probability,movement_control_id,0 AS latent_animals_can_infect_others,subclinical_animals_can_infect_others "
                     "FROM ScenarioCreator_productiontype src_prodtype,ScenarioCreator_productiontype dest_prodtype,ScenarioCreator_productiontypepairtransmission pairing,ScenarioCreator_indirectspread indirect "
                     "WHERE src_prodtype.id=pairing.source_production_type_id "
                     "AND dest_prodtype.id=pairing.destination_production_type_id "
                     "AND pairing.indirect_contact_spread_id = indirect.id",
                     set_params, self, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }

  /* Call the set_zone_params function to read the zone/production type
   * combination specific parameters. */
  sqlite3_exec_dict (params,
                    "SELECT zone.name AS zone,prodtype.name AS prodtype,\"direct\" AS contact_type,zone_direct_movement_id "
                    "FROM ScenarioCreator_zone zone,ScenarioCreator_productiontype prodtype,ScenarioCreator_zoneeffectassignment pairing,ScenarioCreator_zoneeffect effect "
                    "WHERE zone.id=pairing.zone_id "
                    "AND prodtype.id=pairing.production_type_id "
                    "AND effect.id=pairing.effect_id "
                    "AND zone_direct_movement_id IS NOT NULL "
                    "UNION SELECT zone.name AS zone,prodtype.name AS prodtype,\"indirect\" AS contact_type,zone_indirect_movement_id "
                    "FROM ScenarioCreator_zone zone,ScenarioCreator_productiontype prodtype,ScenarioCreator_zoneeffectassignment pairing,ScenarioCreator_zoneeffect effect "
                    "WHERE zone.id=pairing.zone_id "
                    "AND prodtype.id=pairing.production_type_id "
                    "AND effect.id=pairing.effect_id "
                    "AND zone_indirect_movement_id IS NOT NULL",
                    set_zone_params, self, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }
  local_data->db = NULL;

  /* Set a minimum radius in which to look for neighbours when generating
   * short-distance contacts. Experimentally, a radius in which you expect to
   * find three dozen units seems to work well. */
  {
    double density, area_for_3_doz_units;

    density = estimate_density (units);
    area_for_3_doz_units = 3 * 12 / density;
    local_data->min_radius = sqrt (area_for_3_doz_units / M_PI);
    #if DEBUG
      g_debug ("minimum radius = %g km", local_data->min_radius);
    #endif
  }
  
#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file contact_spread_model.c */
