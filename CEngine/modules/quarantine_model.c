/** @file quarantine_model.c
 * Module that simulates a policy of quarantining diseased units and units that
 * are going to be destroyed.
 *
 * When a diseased unit is reported to the authorities, or a unit is requested
 * destroyed, this module quarantines the unit.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @version 0.1
 * @date November 2003
 *
 * Copyright &copy; University of Guelph, 2003-2006
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#if HAVE_CONFIG_H
#  include <config.h>
#endif

/* To avoid name clashes when multiple modules have the same interface. */
#define new quarantine_model_new
#define run quarantine_model_run
#define reset quarantine_model_reset
#define events_listened_for quarantine_model_events_listened_for
#define local_free quarantine_model_free
#define handle_detection_event quarantine_model_handle_detection_event
#define handle_request_for_destruction_event quarantine_model_handle_request_for_destruction_event

#include "module.h"

#if STDC_HEADERS
#  include <string.h>
#endif

#include "quarantine_model.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "quarantine-model"



#define NEVENTS_LISTENED_FOR 2
EVT_event_type_t events_listened_for[] = { EVT_Detection,
  EVT_RequestForDestruction
};



/** Specialized information for this model. */
typedef struct
{
  int dummy;                    /* to prevent "struct has no members" warnings */
}
local_data_t;



/**
 * Responds to a detection by quarantining the unit.
 *
 * @param self the model.
 * @param event a detection event.
 */
void
handle_detection_event (struct spreadmodel_model_t_ *self, EVT_detection_event_t * event)
{
#if DEBUG
  g_debug ("----- ENTER handle_detection_event (%s)", MODEL_NAME);
#endif

#if DEBUG
  g_debug ("quarantining unit %s", event->unit->official_id);
#endif
  UNT_quarantine (event->unit);

#if DEBUG
  g_debug ("----- EXIT handle_detection_event (%s)", MODEL_NAME);
#endif
}



/**
 * Responds to a request for destruction event by quarantining the unit.
 *
 * @param self the model.
 * @param event a request for destruction event.
 */
void
handle_request_for_destruction_event (struct spreadmodel_model_t_ *self,
                                      EVT_request_for_destruction_event_t * event)
{
#if DEBUG
  g_debug ("----- ENTER handle_request_for_destruction_event (%s)", MODEL_NAME);
#endif

#if DEBUG
  g_debug ("quarantining unit %s", event->unit->official_id);
#endif
  UNT_quarantine (event->unit);

#if DEBUG
  g_debug ("----- EXIT handle_request_for_destruction_event (%s)", MODEL_NAME);
#endif
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
run (struct spreadmodel_model_t_ *self, UNT_unit_list_t * units, ZON_zone_list_t * zones,
     EVT_event_t * event, RAN_gen_t * rng, EVT_event_queue_t * queue)
{
#if DEBUG
  g_debug ("----- ENTER run (%s)", MODEL_NAME);
#endif

  switch (event->type)
    {
    case EVT_Detection:
      handle_detection_event (self, &(event->u.detection));
      break;
    case EVT_RequestForDestruction:
      handle_request_for_destruction_event (self, &(event->u.request_for_destruction));
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
 * Resets this model after a simulation run.
 *
 * @param self the model.
 */
void
reset (struct spreadmodel_model_t_ *self)
{
#if DEBUG
  g_debug ("----- ENTER reset (%s)", MODEL_NAME);
#endif

  /* Nothing to do. */

#if DEBUG
  g_debug ("----- EXIT reset (%s)", MODEL_NAME);
#endif
}



/**
 * Frees this model.
 *
 * @param self the model.
 */
void
local_free (struct spreadmodel_model_t_ *self)
{
  local_data_t *local_data;

#if DEBUG
  g_debug ("----- ENTER free (%s)", MODEL_NAME);
#endif

  /* Free the dynamically-allocated parts. */
  local_data = (local_data_t *) (self->model_data);
  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Returns a new quarantine model.
 */
spreadmodel_model_t *
new (scew_element * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  spreadmodel_model_t *self;
  local_data_t *local_data;

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
  self->has_pending_actions = spreadmodel_model_answer_no;
  self->has_pending_infections = spreadmodel_model_answer_no;
  self->to_string = spreadmodel_model_to_string_default;
  self->printf = spreadmodel_model_printf;
  self->fprintf = spreadmodel_model_fprintf;
  self->free = local_free;

  /* Make sure the right XML subtree was sent. */
  g_assert (strcmp (scew_element_name (params), MODEL_NAME) == 0);

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file quarantine_model.c */
