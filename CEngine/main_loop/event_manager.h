/** @file event_manager.h
 * Interface for event_manager.c.  The event manager is a singleton object that
 * handles all communication among sub-models.  See adsm_create_event() for
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
  adsm_module_t **models;
  EVT_event_queue_t *queue;
  GSList *listeners[EVT_NEVENT_TYPES]; /** which models are listening for which events */
}
adsm_event_manager_t;



/* Prototypes. */
adsm_event_manager_t *adsm_new_event_manager (adsm_module_t **, int);
void adsm_free_event_manager (adsm_event_manager_t *);
void adsm_create_event (adsm_event_manager_t *, EVT_event_t *,
                               UNT_unit_list_t *, ZON_zone_list_t *, RAN_gen_t *);
                          

#endif /* !EVENT_MANAGER_H */
