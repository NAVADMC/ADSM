/** @file trace_quarantine_model.c
 * Module that simulates a policy of quarantining units that have been found
 * through trace-out or trace-in.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @version 0.1
 * @date August 2007
 *
 * Copyright &copy; University of Guelph, 2007
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
#define new trace_quarantine_model_new
#define run trace_quarantine_model_run
#define reset trace_quarantine_model_reset
#define events_listened_for trace_quarantine_model_events_listened_for
#define to_string trace_quarantine_model_to_string
#define local_free trace_quarantine_model_free
#define handle_trace_result_event trace_quarantine_model_handle_trace_result_event

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

#include "trace_quarantine_model.h"

#include "spreadmodel.h"

/** This must match an element name in the DTD. */
#define MODEL_NAME "trace-quarantine-model"



#define NEVENTS_LISTENED_FOR 1
EVT_event_type_t events_listened_for[] = { EVT_TraceResult };



/** Specialized information for this model. */
typedef struct
{
  SPREADMODEL_contact_type contact_type;
  SPREADMODEL_trace_direction direction;
  gboolean *production_type;
  GPtrArray *production_types;
}
local_data_t;



/**
 * Responds to a trace result by ordering quarantine.
 *
 * @param self the model.
 * @param units the list of units.
 * @param event a trace result event.
 */
void
handle_trace_result_event (struct spreadmodel_model_t_ *self, UNT_unit_list_t * units,
                           EVT_trace_result_event_t * event)
{
  local_data_t *local_data;
  UNT_unit_t *unit;

#if DEBUG
  g_debug ("----- ENTER handle_trace_result_event (%s)", MODEL_NAME);
#endif

  local_data = (local_data_t *) (self->model_data);

  if (event->traced == FALSE || event->contact_type != local_data->contact_type)
    goto end;

  if (local_data->direction == SPREADMODEL_TraceForwardOrOut)
    unit = event->exposed_unit;
  else
    unit = event->exposing_unit;

  if (local_data->production_type[unit->production_type] == FALSE)
    goto end;

#if DEBUG
  g_debug ("requesting quarantine of unit \"%s\"", unit->official_id);
#endif

  UNT_quarantine (unit);

end:
#if DEBUG
  g_debug ("----- EXIT handle_trace_result_event (%s)", MODEL_NAME);
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
run (struct spreadmodel_model_t_ *self, UNT_unit_list_t * units, ZON_zone_list_t * zones,
     EVT_event_t * event, RAN_gen_t * rng, EVT_event_queue_t * queue)
{
#if DEBUG
  g_debug ("----- ENTER run (%s)", MODEL_NAME);
#endif

  switch (event->type)
    {
    case EVT_TraceResult:
      handle_trace_result_event (self, units, &(event->u.trace_result));
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
  char *chararray;
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
  g_string_append_printf (s, " units found by %s %s>",
    SPREADMODEL_contact_type_name[local_data->contact_type],
    SPREADMODEL_trace_direction_name[local_data->direction]);

  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Frees this model.  Does not free the contact type name or production type
 * names.
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
  g_free (local_data->production_type);
  g_free (local_data);
  g_ptr_array_free (self->outputs, TRUE);
  g_free (self);

#if DEBUG
  g_debug ("----- EXIT free (%s)", MODEL_NAME);
#endif
}



/**
 * Returns a new trace destruction model.
 */
spreadmodel_model_t *
new (scew_element * params, UNT_unit_list_t * units, projPJ projection,
     ZON_zone_list_t * zones)
{
  spreadmodel_model_t *self;
  local_data_t *local_data;
  scew_attribute *attr;
  XML_Char const *attr_text;

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
  self->is_listening_for = spreadmodel_model_is_listening_for;
  self->has_pending_actions = spreadmodel_model_answer_no;
  self->has_pending_infections = spreadmodel_model_answer_no;
  self->to_string = to_string;
  self->printf = spreadmodel_model_printf;
  self->fprintf = spreadmodel_model_fprintf;
  self->free = local_free;

  /* Make sure the right XML subtree was sent. */
  g_assert (strcmp (scew_element_name (params), MODEL_NAME) == 0);

#if DEBUG
  g_debug ("setting contact type");
#endif
  attr = scew_element_attribute_by_name (params, "contact-type");
  g_assert (attr != NULL);
  attr_text = scew_attribute_value (attr);
  if (strcmp (attr_text, "direct") == 0)
    local_data->contact_type = SPREADMODEL_DirectContact;
  else if (strcmp (attr_text, "indirect") == 0)
    local_data->contact_type = SPREADMODEL_IndirectContact;
  else
    g_assert_not_reached ();

#if DEBUG
  g_debug ("setting trace direction");
#endif
  attr = scew_element_attribute_by_name (params, "direction");
  g_assert (attr != NULL);
  attr_text = scew_attribute_value (attr);
  if (strcmp (attr_text, "out") == 0)
    local_data->direction = SPREADMODEL_TraceForwardOrOut;
  else if (strcmp (attr_text, "in") == 0)
    local_data->direction = SPREADMODEL_TraceBackOrIn;
  else
    g_assert_not_reached ();

#if DEBUG
  g_debug ("setting production types");
#endif
  local_data->production_types = units->production_type_names;
  local_data->production_type =
    spreadmodel_read_prodtype_attribute (params, "production-type", units->production_type_names);

#if DEBUG
  g_debug ("----- EXIT new (%s)", MODEL_NAME);
#endif

  return self;
}

/* end of file trace_quarantine_model.c */
