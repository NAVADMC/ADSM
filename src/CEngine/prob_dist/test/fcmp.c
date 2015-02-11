/** @file prob_dist/test/fcmp.c
 * An approximate comparison program for real numbers.
 *
 * This program is used in the test suite because Tcl lacks the C functions
 * needed to write a robust floating-point comparison function.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @version 0.1
 * @date July 2003
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

#include <stdio.h>

#if STDC_HEADERS
#  include <stdlib.h>
#endif

#include <glib.h>
#include <gsl/gsl_math.h>

#if HAVE_ERRNO_H
#  include <errno.h>
#endif



int
main (int argc, char *argv[])
{
  double a, b, epsilon;

  g_assert (argc == 4);
  a = strtod (argv[1], NULL);
  g_assert (errno != ERANGE);
  b = strtod (argv[2], NULL);
  g_assert (errno != ERANGE);
  epsilon = strtod (argv[3], NULL);
  g_assert (errno != ERANGE);

  printf ("%i\n", gsl_fcmp (a, b, epsilon));
  return EXIT_SUCCESS;
}

/* end of file fcmp.c */
