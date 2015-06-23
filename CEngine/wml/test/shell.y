%{
#if HAVE_CONFIG_H
#  include <config.h>
#endif

#include <wml.h>
#include <glib.h>
#include <stdio.h>
#include <stdlib.h>

#define PROMPT "> "

/** @file wml/test/shell.c
 * A simple shell to exercise libwml.  It provides a way to create sets of
 * points and call the functions ported from the <a href="wml_8h.html">Wild
 * Magic Library</a>, so that a suite of tests can be scripted.
 *
 * The commands are:
 * <ul>
 *   <li>
 *     <code>pointset (x1,y1,x2,y2,...)</code>
 *
 *     Creates a set of points.
 *   <li>
 *     <code>hull</code>
 *
 *     Finds the convex hull around the most recently created point set.  The
 *     output from this command is a list of point indices, separated by
 *     spaces.
 * </ul>
 *
 * The shell exits on EOF (Ctrl+D if you're typing commands into it
 * interactively in Unix).
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date December 2003
 *
 * Copyright &copy; University of Guelph, 2003-2006
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 *
 * @todo Trap errors so that we can check that some functions abort when their
 *   preconditions are violated.
 */

#define YYERROR_VERBOSE
#define BUFFERSIZE 2048

/* int yydebug = 1; must also compile with --debug to use this */
int yylex(void);
int yyerror (char const *s);
char errmsg[BUFFERSIZE];

GArray *current_points = NULL;

void g_free_as_GFunc (gpointer data, gpointer user_data);
%}

%union {
  double fval;
  GSList *lval;
}

%token POINTSET HULL
%token LPAREN RPAREN COMMA
%token <fval> NUM
%type <lval> num_list

%%

commands :
    command commands
  | command
  ;

command :
    pointset_command
  | function_call
  ;

pointset_command :
    POINTSET LPAREN num_list RPAREN
    {
      int npoints;
      WML_Vector2 v;
      GSList *iter;
#if DEBUG
      int i;
      char *s;
#endif

      if (current_points != NULL)
	g_array_free (current_points, TRUE);

      npoints = g_slist_length ($3);
      if (npoints % 2 != 0)
	{
	  g_warning ("number of arguments must be even");
	  current_points = NULL;
	}
      else
	{
	  /* Copy the arguments into an array, then free the argument list
	   * structure. */
	  current_points = g_array_sized_new (FALSE, FALSE, sizeof(WML_Vector2), npoints);
	  for (iter = $3; iter != NULL; )
	    {
	      v.X = *((double *)(iter->data));
	      iter = g_slist_next (iter);
	      v.Y = *((double *)(iter->data));
	      iter = g_slist_next (iter);
	      g_array_append_val (current_points, v);
	    }
	  g_slist_foreach ($3, g_free_as_GFunc, NULL);
	  g_slist_free ($3);
	}
#if DEBUG
      for (i = 0; i < current_points->len; i++)
	{
	  s = WML_Vector2_to_string (&g_array_index (current_points, WML_Vector2, i));
	  if (i > 0)
	    printf (",");
	  printf ("%s", s);
	  free (s);
	}
#endif
      printf ("\n%s", PROMPT);
      fflush (stdout);
    }
  ;

function_call :
    HULL
    {
      WML_ConvexHull2 *hull;
      int npoints, i;
      int *indices;
      
      hull = WML_new_ConvexHull2 (current_points->len, (WML_Vector2 *)(current_points->data), TRUE);
      npoints = WML_ConvexHull2_GetQuantity (hull);
      indices = WML_ConvexHull2_GetIndices (hull);
      if (npoints > 0)
	printf ("%i", indices[0]);
      for (i = 1; i < npoints; i++)
	printf (" %i", indices[i]);
      WML_free_ConvexHull2 (hull);
      printf ("\n%s", PROMPT);
      fflush (stdout);
    }
  ;

num_list:
    num_list COMMA NUM
    {
      double *d;
      
      /* Append to a linked list of doubles. */
      d = g_new (double, 1);
      *d = $3;
      $$ = g_slist_append ($1, d);
    }
  | NUM
    {
      double *d;
      
      /* Initialize a linked list of doubles. */
      d = g_new (double, 1);
      *d = $1;
      $$ = g_slist_append (NULL, d);
    }
  ;

%%

extern FILE *yyin;
extern int tokenpos;
extern char linebuf[];

/* Simple yyerror from _lex & yacc_ by Levine, Mason & Brown. */
int
yyerror (char const *s)
{
  g_error ("%s\n%s\n%*s", s, linebuf, 1+tokenpos, "^");
  return 0;
}



/**
 * Wraps free so that it can be used in GLib calls.
 *
 * @param data a pointer cast to a gpointer.
 * @param user_data not used, pass NULL.
 */
void
g_free_as_GFunc (gpointer data, gpointer user_data)
{
  g_free (data);
}



/**
 * A log handler that simply discards messages.
 */
void
silent_log_handler (const gchar * log_domain, GLogLevelFlags log_level,
		    const gchar * message, gpointer user_data)
{
  ;
}



int
main (int argc, char *argv[])
{
  g_log_set_handler ("wml", G_LOG_LEVEL_MESSAGE | G_LOG_LEVEL_INFO | G_LOG_LEVEL_DEBUG, silent_log_handler, NULL);

  printf (PROMPT);
  if (yyin == NULL)
    yyin = stdin;
  while (!feof(yyin))
    yyparse();

  return EXIT_SUCCESS;
}

/* end of file shell.y */
