/** @file modules/test/shell2.c
 * A simple shell to look up stored output from test runs.  It enables the
 * suite of tests to be run on output generated at another time on another
 * platform, e.g., from SpreadModel on Windows.
 *
 * Each line of input should be of the form
 *
 * test/HERD-FILE test/model.CATEGORY/PARAM-FILE
 *
 * The script will strip the .xml extensions from the herd and parameter file
 * names and create a filename
 *
 * FOLDER/CATEGORY__HERD-FILE__PARAM-FILE.txt
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
#include <regex.h>
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
  gint tmp_file;
  char *tmp_filename;
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
          g_string_printf (cmd, "test/minispreadmodel -V 0 --model-dir=.. -h %s", &buf[11]);
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
          g_string_printf (cmd, "test/minispreadmodel-fixed-rng -V 0 --model-dir=.. -h %s > %s",
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
          regex_t regex;
          regmatch_t match[3];
          int errcode;
          size_t errlength;
          char *errmsg;
          char *s;

          filename = g_string_new (NULL);
          errcode = regcomp (&regex, "test/([^.]+)\\.xml", REG_EXTENDED);
          if (errcode != 0)
            {
              errlength = regerror (errcode, &regex, NULL, 0);
              errmsg = g_new (char, errlength);
              regerror (errcode, &regex, errmsg, errlength);
              g_warning
                ("regular expression did not compile because: %s\nreturning string not split",
                 errmsg);
              g_free (errmsg);
            }
          errcode = regexec (&regex, buf, 3, match, 0);
          s = g_strndup (buf + match[1].rm_so, match[1].rm_eo - match[1].rm_so);
          g_string_printf (filename, "__%s", s);
          free (s);

          errcode = regcomp (&regex, "test/model.([^/]+)/([^.]+)\\.xml", REG_EXTENDED);
          if (errcode != 0)
            {
              errlength = regerror (errcode, &regex, NULL, 0);
              errmsg = g_new (char, errlength);
              regerror (errcode, &regex, errmsg, errlength);
              g_warning
                ("regular expression did not compile because: %s\nreturning string not split",
                 errmsg);
              g_free (errmsg);
            }
          errcode = regexec (&regex, buf, 3, match, 0);
          s = g_strndup (buf + match[1].rm_so, match[1].rm_eo - match[1].rm_so);
          g_string_prepend (filename, s);
          free (s);
          s = g_strndup (buf + match[2].rm_so, match[2].rm_eo - match[2].rm_so);
          g_string_append_printf (filename, "__%s.txt", s);
          free (s);

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
