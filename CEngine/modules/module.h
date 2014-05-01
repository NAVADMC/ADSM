/** @file module.h
 * Common interface for modules.
 *
 * The simulator design treats modules as interchangeable, mix-and-match
 * parts &mdash; "building blocks".  A "simulation" is then the sum of the
 * actions of the active modules.
 *
 * @image html building_blocks.png
 *
 * <small>(Image copyright information below)</small>
 *
 * Each module has a "new" function that creates and initializes an instance of
 * the module.  The new function must fill in a set of function pointers so
 * that the module's functions can be called in an object-oriented style, e.g.,
 * <code>model->printf(model)</code>. See the adsm_module_t_ structure
 * for a list of these functions.
 *
 * <small>Image copyright information:
 * <ul>
 *  <li>disease image (virus) is "Bluetongue virus" by Flickr user AJC1.
 *    Released under a Creative Commons Attribution-Noncommercial 2.0 Generic
 *    license.</li>
 *  <li>airborne spread image (sky) is "Landscape Under a Stormy Sky" by Vincent
 *    Van Gogh.  Public domain image (copyright expired).</li>
 *  <li>direct contact image (cow) is "When bovines attack" by Flickr user tricky.
 *    Released under a Creative Commons Attribution-Noncommercial-Share Alike
 *    2.0 Generic license.</li>
 *  <li>indirect contact image (truck) is "truck" by Flickr user rickabbo.
 *    Released under a Creative Commons Attribution 2.0 Generic license.</li>
 *  <li>detection image (Sherlock Holmes items) is by Wikimedia Commons user
 *    Alterego.  Released under the GNU Free Documentation License.</li>
 *  <li>vaccination image (vials) is "Let me stabilize you" by Flickr user
 *    Pulpolux.  Released under a Creative Commons Attribution-Noncommercial
 *    2.0 Generic license.</li>
 *  <li>destruction image (guillotine) is "Death Hangs in the Air" by Flickr user
 *    buck82.  Released under a Creative Commons Attribution-Noncommercial 2.0
 *    Generic license.</li>
 * </ul>
 * </small>
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#ifndef MODULE_H
#define MODULE_H

#include "unit.h"
#include "event.h"
#include "parameter.h"
#include "reporting.h"
#include "zone.h"
#include "rng.h"



struct adsm_module_t_;



/** Type of a function that creates and sets parameters for a model. */
typedef struct adsm_module_t_ *(*adsm_model_new_t) (sqlite3 *,
                                                                 UNT_unit_list_t *,
                                                                 projPJ,
                                                                 ZON_zone_list_t *);



/** Type of a function that frees a model. */
typedef void (*adsm_model_free_t) (struct adsm_module_t_ *);



/** Type of a function that runs a model. */
typedef void (*adsm_model_run_t) (struct adsm_module_t_ *,
                                         UNT_unit_list_t *, ZON_zone_list_t *,
                                         EVT_event_t *, RAN_gen_t *, EVT_event_queue_t *);



/** Type of a function that resets a model after one simulation run. */
typedef void (*adsm_model_reset_t) (struct adsm_module_t_ *);



/**
 * Type of a function that reports whether a model is listening for a given
 * event type.
 */
typedef gboolean (*adsm_model_is_listening_for_t) (struct adsm_module_t_ *, EVT_event_type_t);



/**
 * Type of a function that reports whether a model has any pending actions to
 * carry out.
 */
typedef gboolean (*adsm_model_has_pending_actions_t) (struct adsm_module_t_ *);



/**
 * Type of a function that reports whether a model has any pending infections
 * to cause.
 */
typedef gboolean (*adsm_model_has_pending_infections_t) (struct adsm_module_t_ *);



/** Type of a function that returns a string representation of a model. */
typedef char *(*adsm_module_to_string_t) (struct adsm_module_t_ *);



/** Type of a function that prints a model. */
typedef int (*adsm_model_printf_t) (struct adsm_module_t_ *);



/** Type of a function that prints a model to a stream. */
typedef int (*adsm_model_fprintf_t) (FILE *, struct adsm_module_t_ *);



/** A simulator module. */
typedef struct adsm_module_t_
{
  char *name; /**< A short name for the model. */
  EVT_event_type_t *events_listened_for; /**< A list of events the model listens for. */
  unsigned int nevents_listened_for; /**< Length of events_listened_for. */
  GPtrArray *outputs; /**< A list of the model's output variables. */
  void *model_data; /**< Specialized information for the particular model. */
  adsm_model_run_t run; /**< A function that runs the model. */
  adsm_model_reset_t reset; /**< A function that resets the model after one simulation run. */
  adsm_model_is_listening_for_t is_listening_for; /**< A function that reports whether the model is listening for a given event type.*/
  adsm_model_has_pending_actions_t has_pending_actions; /**< A function that reports whether the model has any pending actions to carry out.*/
  adsm_model_has_pending_infections_t has_pending_infections; /**< A function
    that reports whether the model has any pending infections to cause. */
  adsm_module_to_string_t to_string; /**< A function that returns a string representation of the model. */
  adsm_model_printf_t printf; /**< A function that prints the model. */
  adsm_model_fprintf_t fprintf; /**< A function that prints the model to a stream. */
  adsm_model_free_t free; /**< A function that frees the model. */
}
adsm_module_t;

/* Some methods that tend to be the same for most of the modules. */
gboolean adsm_model_is_listening_for (struct adsm_module_t_ *, EVT_event_type_t);
char *adsm_module_to_string_default (struct adsm_module_t_ *);
int adsm_model_fprintf (FILE *, struct adsm_module_t_ *);
int adsm_model_printf (struct adsm_module_t_ *);
gboolean adsm_model_answer_yes (struct adsm_module_t_ *);
gboolean adsm_model_answer_no (struct adsm_module_t_ *);

#endif /* !MODULE_H */
