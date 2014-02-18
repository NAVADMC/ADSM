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
  GString *cmd = NULL;
  int tmp_file;
  char *tmp_filename;
  GError *error;

  cmd = g_string_new (NULL);
  printf (PROMPT);
  while (1)
    {
      len = getline (&buf, &bufsize, stdin);
      if (len == -1)
        break;
      if (g_ascii_strncasecmp (buf, "stochastic variables", 20) == 0)
        {
          /* Get a temporary filename.  The simulation output will be sent to
           * this file, then processed by the full table filter. */
          tmp_file = g_file_open_tmp (NULL, &tmp_filename, &error);
          close (tmp_file);

          /* Get rid of the \n at the end of buf. */
          buf[len - 1] = '\0';

          /* Run the simulator. */
          g_string_printf (cmd, "test/minispreadmodel -V 0 -o %s -p %s",
                           tmp_filename, &buf[21]);
          system (cmd->str);

          /* Get a table of the output variable values. */
          g_string_printf (cmd, "../filters/full_table_filter < %s", tmp_filename);
          system (cmd->str);

          /* Remove the temporary file. */
          unlink (tmp_filename);
          g_free (tmp_filename);
        }
      else if (g_ascii_strncasecmp (buf, "stochastic", 10) == 0)
        {
          g_string_printf (cmd, "test/minispreadmodel -V 0 -p %s", &buf[11]);
          system (cmd->str);
        }
      else if (g_ascii_strncasecmp (buf, "variables", 9) == 0)
        {
          /* Get a temporary filename.  The simulation output will be sent to
           * this file, then processed by the full table filter. */
          tmp_file = g_file_open_tmp (NULL, &tmp_filename, &error);
          close (tmp_file);

          /* Get rid of the \n at the end of buf. */
          buf[len - 1] = '\0';

          /* Run the simulator. */
          g_string_printf (cmd, "test/minispreadmodel -r 0.5 -V 0 -o %s -p %s",
                           tmp_filename, &buf[10]);
          system (cmd->str);

          /* Get a table of the output variable values. */
          g_string_printf (cmd, "../filters/full_table_filter < %s", tmp_filename);
          system (cmd->str);

          /* Remove the temporary file. */
          unlink (tmp_filename);
          g_free (tmp_filename);
        }
      else
        {
          g_string_printf (cmd, "test/minispreadmodel -r 0.5 -V 0 -p %s", buf);
          system (cmd->str);
        }
      printf (PROMPT);
    }
  g_string_free (cmd, TRUE);
  free (buf);

  return EXIT_SUCCESS;
}

/* end of file shell.c */
