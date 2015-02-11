%{
#if HAVE_CONFIG_H
#  include <config.h>
#endif

#include <rel_chart.h>
#include <glib.h>

#define PROMPT "> "

/** @file rel_chart/test/shell.c
 * A simple shell to exercise librel_chart.  It provides a way to create
 * relationship charts and call the functions offered by the
 * <a href="rel__chart_8h.html">relationship chart library</a>, so that
 * a suite of tests can be scripted.
 *
 * The commands are:
 * <ul>
 *   <li>
 *     <code>chart (x1,y1,x2,y2,...)</code>
 *
 *     Creates a <a href="structREL__chart__t.html">relationship chart</a>.
 *   <li>
 *     <code>lookup (x)</code>
 *
 *     Returns the <i>y</i>-value for a given <i>x</i> value from the most
 *     recently created relationship chart.
 *   <li>
 *     <code>range</code>
 *     Returns the lowest and highest <i>y</i>-values in the most recently
 *     created relationship chart. 
 * </ul>
 *
 * The shell exits on EOF (Ctrl+D if you're typing commands into it
 * interactively in Unix).
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date September 2003
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

REL_chart_t *current_chart = NULL;

void g_free_as_GFunc (gpointer data, gpointer user_data);
%}

%union {
  double fval;
  GSList *lval;
}

%token CHART
%token LOOKUP RANGE
%token LPAREN RPAREN COMMA
%token <fval> NUM
%type <lval> num_list

%%

commands :
    command commands
  | command
  ;

command :
    new_command
  | function_call
  ;

new_command :
    CHART LPAREN num_list RPAREN
    {
      int npoints;
      double *x, *y, *px, *py;
      GSList *iter;

      REL_free_chart (current_chart);

      npoints = g_slist_length ($3);
      if (npoints % 2 != 0)
	{
	  g_warning ("number of arguments must be even");
	  current_chart = NULL;
	}
      else
	{
	  npoints /= 2;
	  /* Copy the arguments into two arrays, then free the argument list
	   * structure. */
	  x = g_new (double, npoints);
	  y = g_new (double, npoints);
	  for (iter = $3, px = x, py = y; iter != NULL; iter = g_slist_next (iter))
	    {
	      *px++ = *((double *)(iter->data));
	      iter = g_slist_next (iter);
	      *py++ = *((double *)(iter->data));	      
	    }
	  g_slist_foreach ($3, g_free_as_GFunc, NULL);
	  g_slist_free ($3);

	  current_chart = REL_new_chart (x, y, npoints);
	  g_free (x);
	  g_free (y);
	}
      REL_printf_chart (current_chart);
      printf ("\n%s", PROMPT);
      fflush (stdout);
    }
  ;

function_call :
    LOOKUP LPAREN NUM RPAREN
    {
      printf ("%g\n%s", REL_chart_lookup ($3, current_chart), PROMPT);
      fflush (stdout);
    }
  | RANGE
    {
      printf ("%g %g\n%s", REL_chart_min (current_chart),
	      REL_chart_max (current_chart), PROMPT);
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
  g_log_set_handler ("rel_chart", G_LOG_LEVEL_MESSAGE | G_LOG_LEVEL_INFO | G_LOG_LEVEL_DEBUG, silent_log_handler, NULL);

  printf (PROMPT);
  if (yyin == NULL)
    yyin = stdin;
  while (!feof(yyin))
    yyparse();

  return EXIT_SUCCESS;
}

/* end of file shell.y */
