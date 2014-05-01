/** @file modules/test/shell2.c
 * A simple shell to look up stored output from test runs.  It enables the
 * suite of tests to be run on output generated at another time on another
 * platform, e.g., from ADSM on Windows.
 *
 * Each line of input should be of the form
 *
 * test/POPULATION-FILE test/module.CATEGORY/PARAM-FILE
 *
 * The script will strip the .xml extensions from the population and parameter file
 * names and create a filename
 *
 * FOLDER/CATEGORY__POPULATION-FILE__PARAM-FILE.txt
 *
 * (where FOLDER is a constant specified below).  It will then print the
 * contents of that file to standard output.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date October 2004
 *
 * Copyright &copy; University of Guelph, 2004-2006
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
#include "replace.h"

#define FOLDER "sm_output"
#define PROMPT "> "



int
main (int argc, char *argv[])
{
  char *buf = NULL;
  size_t bufsize = 0;
  ssize_t len;
  GString *cmd = NULL, *filename = NULL;
  GError *error;

  cmd = g_string_new (NULL);
  printf (PROMPT);
  while (1)
    {
      len = getline (&buf, &bufsize, stdin);
      if (len == -1)
        break;
      if (g_ascii_strncasecmp (buf, "stochastic", 10) == 0)
        {
          g_string_printf (cmd, "test/miniadsm -V 0 --model-dir=.. -h %s", &buf[11]);
          system (cmd->str);
        }
      else if (g_ascii_strncasecmp (buf, "variables", 9) == 0)
        {
          gint tmp_file;
          char *tmp_filename;

          /* Get a temporary filename.  The simulation output will be sent to
           * this file, then processed by the full table filter. */
          tmp_file = g_file_open_tmp (NULL, &tmp_filename, &error);
          close (tmp_file);

          /* Get rid of the \n at the end of buf. */
          buf[len - 1] = '\0';

          /* Run the simulator. */
          g_string_printf (cmd, "test/miniadsm-fixed-rng -V 0 --model-dir=.. -h %s > %s",
                           &buf[10], tmp_filename);
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
          GRegex *regex;
          GError *error = NULL;
          GMatchInfo *match = NULL;

          filename = g_string_new (NULL);
          /* Match out the population file name. */
          regex = g_regex_new ("test/([^.]+)\\.xml", 0, 0, &error);
          if (error != NULL)
            {
              g_error ("regular expression did not compile because: %s",
                       error->message);
            }
          g_regex_match (regex, buf, 0, &match);
          g_assert (g_match_info_matches(match));
          g_string_printf (filename, "__%s", g_match_info_fetch (match, 1));
          g_printf ("%s\n", filename->str);
          g_match_info_free (match);
          g_regex_unref (regex);

          /* Match out the category name and parameter file name. */
          regex = g_regex_new ("test/module.([^/]+)/([^.]+)\\.xml", 0, 0, &error);
          if (error != NULL)
            {
              g_error ("regular expression did not compile because: %s",
                       error->message);
            }
          g_regex_match (regex, buf, 0, &match);
          g_assert (g_match_info_matches(match));
          g_string_prepend (filename, g_match_info_fetch (match, 1));
          g_string_append_printf (filename, "__%s.txt", g_match_info_fetch (match, 2));
          g_match_info_free (match);
          g_regex_unref (regex);

          g_string_printf (cmd, "cat test/%s/%s", FOLDER, filename->str);
          g_string_free (filename, TRUE);
          system (cmd->str);
        }
      printf (PROMPT);
    }
  g_string_free (cmd, TRUE);
  free (buf);

  return EXIT_SUCCESS;
}

/* end of file shell2.c */
