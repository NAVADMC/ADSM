%{
#if HAVE_CONFIG_H
#  include <config.h>
#endif

#include "unit.h"
#include <stdio.h>

#if STDC_HEADERS
#  include <stdlib.h>
#endif

/** @file filters/state_table.c
 * A filter that turns SHARCSpread output into a table of unit states.
 *
 * Call it as
 *
 * <code>state_table_filter < LOG-FILE</code>
 *
 * The table is written to standard output in comma-separated values format.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date January 2005
 *
 * Copyright &copy; University of Guelph, 2004-2007
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#define YYERROR_VERBOSE
#define BUFFERSIZE 2048

/* int yydebug = 1; must also compile with --debug to use this */
int yylex(void);
int yyerror (char const *s);
char errmsg[BUFFERSIZE];

GArray *unit_states; /**< The unit states. */
int current_node; /**< The most recent node number we have seen in the
  simulator output. */
int current_run; /**< The most recent run number we have seen in the output. */
int current_day; /**< The most recent day we have seen in the output. */
gboolean printed_header; /**< Whether we have printed the header line for the
  table or not. */



/**
 * Prints the stored output values.
 */
void
print_values ()
{
  static int run = 0; /* A run identifier than increases each time we print one
    complete Monte Carlo run.  This is distinct from the per-node run numbers
    in the simulator output. */
  unsigned int nunits, i;

  if (current_day == 1)
    run++;

  printf ("%u,%u", run, current_day);
  /* Output the state codes. */
  nunits = unit_states->len;
  for (i = 0; i < nunits; i++)
    printf (",%i", g_array_index (unit_states, UNT_state_t, i));
  printf ("\n");
  fflush (stdout);

  return;
}



/**
 * Clears the stored output values.
 */
void
clear_values ()
{
  g_array_set_size (unit_states, 0);
}

%}

%union {
  int ival;
  float fval;
  char *sval;
  GArray *lval;
}

%token NODE RUN DAY POLYGON
%token COMMA COLON EQ LBRACE RBRACE LPAREN RPAREN DQUOTE NEWLINE
%token <ival> INT
%token <fval> FLOAT
%token <sval> VARNAME STRING
%type <lval> state_codes
%%
output_lines :
    output_lines output_line
    { }
  | output_line
    { }
  ;

output_line:
    tracking_line NEWLINE data_line NEWLINE
    {
      unsigned int nunits,i;

      /* If this was the first line read, print the table header. */
      if (!printed_header)
        {
          printf ("Run,Day");
          nunits = unit_states->len;
          for (i = 0; i < nunits; i++)
            printf (",%i", i);
          printf ("\n");
          fflush (stdout);
          printed_header = TRUE;
        }
      print_values();
      clear_values();
    }
  ;

tracking_line:
    NODE INT RUN INT
    {
      int node = $2;
      int run = $4;

      /* When we see that the node number or run number has changed, we know
       * the output from one Monte Carlo trial is over, so we reset the day. */
      if (node != current_node || run != current_run)
        {
          current_day = 1;
          #if DEBUG
            g_debug ("now on day 1 (node %i, run %i)", node, run);
          #endif
        }
      else
        {
          current_day++;
        }
      current_node = node;
      current_run = run;
    }
  ;

data_line:
    state_codes vars
    { }
  | state_codes
    { }
  | vars
    { }
  |
    { }
  ;

state_codes:
    state_codes INT
    {
      g_array_append_val (unit_states, $2);
    }
  | INT
    {
      g_array_append_val (unit_states, $1);
    }
  ;

vars:
    vars var
    { }
  | var
    { }
  ;       

var:
    VARNAME EQ value
    {
      /* The varname token's value is set with a g_strdup, so we need to free
       * it. */
      g_free ($1);
    }
  ;

value:
    INT
    { }
  | FLOAT
    { }
  | STRING
    {
      /* The string token's value is set with a g_strndup, so we need to free
       * it. */
      g_free ($1);
    }
  | POLYGON LPAREN RPAREN
    { }
  | POLYGON LPAREN contours RPAREN
    { }
  | LBRACE RBRACE
    { }
  | LBRACE subvars RBRACE
    { }
  ;

subvars:
    subvars COMMA subvar
    { }
  | subvar
    { }
  ;

subvar:
    STRING COLON value
    {
      /* The string token's value is set with a g_strndup, so we need to free
       * it. */
      g_free ($1);
    }
  ;

contours:
    contours contour
    { }
  | contour
    { }
  ;

contour:
    LPAREN coords RPAREN
    { }
  ;

coords:
    coords COMMA coord
    { }
  | coord
    { }
  ;

coord:
    FLOAT FLOAT
    { }
  | FLOAT INT
    { }
  | INT FLOAT
    { }
  | INT INT
    { }
  ;

%%
extern FILE *yyin;
extern int yylineno, tokenpos;
extern char linebuf[];

/* Simple yyerror from _lex & yacc_ by Levine, Mason & Brown. */
int
yyerror (char const *s)
{
  fprintf (stderr, "Error in output (line %d): %s:\n%s\n", yylineno, s, linebuf);
  fprintf (stderr, "%*s\n", 1+tokenpos, "^");
  return 0;
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
  int verbosity = 0;
  GError *option_error = NULL;
  GOptionContext *context;
  GOptionEntry options[] = {
    { "verbosity", 'V', 0, G_OPTION_ARG_INT, &verbosity, "Message verbosity level (0 = simulation output only, 1 = all debugging output)", NULL },
    { NULL }
  };

  context = g_option_context_new ("");
  g_option_context_add_main_entries (context, options, /* translation = */ NULL);
  if (!g_option_context_parse (context, &argc, &argv, &option_error))
    {
      g_error ("option parsing failed: %s\n", option_error->message);
    }
  g_option_context_free (context);

  /* Set the verbosity level. */
  if (verbosity < 1)
    {
      g_log_set_handler (NULL, G_LOG_LEVEL_DEBUG, silent_log_handler, NULL);
      g_log_set_handler ("unit", G_LOG_LEVEL_DEBUG, silent_log_handler, NULL);
    }
  #if DEBUG
    g_debug ("verbosity = %i", verbosity);
  #endif

  unit_states = g_array_new (/* zero_terminated = */ FALSE,
                             /* clear = */ FALSE,
                             /* element_size = */ sizeof(UNT_state_t));
  /* Initialize the current node to "-1" so that whatever node appears first in
   * the simulator output will signal the parser that output from a new node is
   * beginning, that the current day needs to be reset, etc. */
  current_node = -1;
  /* We have not yet printed the table header line. */
  printed_header = FALSE;

  /* Call the parser to fill in the unit_states array. */
  if (yyin == NULL)
    yyin = stdin;
  while (!feof(yyin))
    yyparse();

  /* Clean up. */
  g_array_free (unit_states, TRUE);
  
  return EXIT_SUCCESS;
}

/* end of file state_table.y */
