/** @file modules/test/shell.c
 * A simple shell to exercise modules.  It provides a way to run the
 * simulation with small herd files and special parameter files, so that a
 * suite of tests can be scripted.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date November 2003
 *
 * Copyright &copy; University of Guelph, 2003-2009
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <glib.h>
#include <glib/gprintf.h>

#if !HAVE_GETLINE
/* getline is a GNU extension; if it's not found at configure time, a fallback
 * implementation will go into libreplace, and we need a prototype here. */
ssize_t getline (char **, size_t *, FILE *);
#endif

#define PROMPT "> "



int
main (int argc, char *argv[])
{
  char *buf = NULL;
  size_t bufsize = 0;
  ssize_t len;
  gchar** tokens;
  GString *cmd = NULL;

  cmd = g_string_new (NULL);
  printf (PROMPT);
  while (1)
    {
      len = getline (&buf, &bufsize, stdin);
      if (len == -1)
        break;
      /* Get rid of the \n at the end of buf. */
      buf[len - 1] = '\0';
      tokens = g_strsplit (buf, " ", 0);
      if (g_ascii_strncasecmp (tokens[0], "stochastic", 10) == 0)
        {
          /* Stochastic test */
          g_string_printf (cmd, "test/miniadsm -V 0 -p %s %s",
                           tokens[1], tokens[2]);
          system (cmd->str);
        }
      else
        {
          /* Deterministic test */
          g_string_printf (cmd, "test/miniadsm -r 0.5 -V 0 -p %s %s",
                           tokens[0], tokens[1]);
          system (cmd->str);
        }
      printf (PROMPT);
      g_strfreev (tokens);
    }
  g_string_free (cmd, TRUE);
  free (buf);

  return EXIT_SUCCESS;
}

/* end of file shell.c */
