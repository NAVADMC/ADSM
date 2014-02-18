/** @file event_manager.h
 * Interface for event_manager.c.  The event manager is a singleton object that
 * handles all communication among sub-models.  See spreadmodel_create_event() for
 * a flowchart describing its actions.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date April 2003
 *
 * Copyright &copy; University of Guelph, 2003-2011
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#ifndef EVENT_MANAGER_H
#define EVENT_MANAGER_H

#include "module.h"
#include "event.h"



/**
 * An object that manages communication among sub-models.  It queries
 * sub-models as to what events they listen for and runs them when those events
 * occur.
 * 
 * This is a Singleton object; only one need exist.
 */
typedef struct
{
  int nmodels;
  spreadmodel_model_t **models;
  EVT_event_queue_t *queue;
  GSList *listeners[EVT_NEVENT_TYPES]; /** which models are listening for which events */
}
spreadmodel_event_manager_t;



/* Prototypes. */
spreadmodel_event_manager_t *spreadmodel_new_event_manager (spreadmodel_model_t **, int);
void spreadmodel_free_event_manager (spreadmodel_event_manager_t *);
void spreadmodel_create_event (spreadmodel_event_manager_t *, EVT_event_t *,
                               UNT_unit_list_t *, ZON_zone_list_t *, RAN_gen_t *);
                          

#endif /* !EVENT_MANAGER_H */
