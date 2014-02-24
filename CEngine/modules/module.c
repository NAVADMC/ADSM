/** @file module.c
 * Implementations of default methods for simulator modules.
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

#if HAVE_CONFIG_H
#  include <config.h>
#endif

#include "module.h"



/**
 * Reports whether a module is listening for a given event type.
 *
 * @param self the module.
 * @param event_type an event type.
 * @return TRUE if the module is listening for the event type.
 */
gboolean
spreadmodel_model_is_listening_for (struct spreadmodel_model_t_ *self, EVT_event_type_t event_type)
{
  int i;

  for (i = 0; i < self->nevents_listened_for; i++)
    if (self->events_listened_for[i] == event_type)
      return TRUE;
  return FALSE;
}



/**
 * Returns a text representation of a module, containing just the module name.
 *
 * @param self the module.
 * @return a string. Must be freed using g_free().
 */
char *
spreadmodel_model_to_string_default (struct spreadmodel_model_t_ *self)
{
  GString *s;
  char *chararray;

  s = g_string_new (NULL);
  g_string_sprintf (s, "<%s>", self->name);

  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Prints a module to a stream.
 *
 * @param stream a stream to write to.
 * @param self the module.
 * @return the number of characters printed (not including the trailing '\\0').
 */
int
spreadmodel_model_fprintf (FILE * stream, struct spreadmodel_model_t_ *self)
{
  char *s;
  int nchars_written;

  s = self->to_string (self);
  nchars_written = fprintf (stream, "%s", s);
  free (s);
  return nchars_written;
}



/**
 * Prints a module.
 *
 * @param self the module.
 * @return the number of characters printed (not including the trailing '\\0').
 */
int
spreadmodel_model_printf (struct spreadmodel_model_t_ *self)
{
  return spreadmodel_model_fprintf (stdout, self);
}



/**
 * Returns TRUE. Useful for filling in the function pointers for yes/no
 * questions that a module can answer, such as whether the module has pending
 * actions.
 *
 * @param self the module.
 * @return TRUE.
 */
gboolean
spreadmodel_model_answer_yes (struct spreadmodel_model_t_ * self)
{
  return TRUE;
}



/**
 * Returns FALSE. Useful for filling in the function pointers for yes/no
 * questions that a module can answer, such as whether the module has pending
 * actions.
 *
 * @param self the module.
 * @return FALSE.
 */
gboolean
spreadmodel_model_answer_no (struct spreadmodel_model_t_ * self)
{
  return FALSE;
}

/* end of file module.c */
