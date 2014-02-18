%{
#if HAVE_CONFIG_H
#  include <config.h>
#endif

#if HAVE_STRINGS_H
#  include <strings.h>
#endif

#include <unit.h>
#include <glib.h>
#include <math.h>

#define PROMPT "> "

/** @file unit/test/shell.c
 * A simple shell to exercise libunit.  It provides a way to create units and
 * call the functions offered by the <a href="unit_8h.html">library</a>, so
 * that a suite of tests can be scripted.
 *
 * The commands are:
 * <ul>
 *   <li>
 *     <code>unit (type,size,lat,long)</code>
 *
 *     Adds a unit to the test set.  The first argument may be any string,
 *     e.g., "Beef Cattle", "Swine".  The units are numbered starting from 0.
 *     They start as Susceptible.
 *   <li>
 *     <code>infect (unit,latent,infectious_subclinical,infectious_clinical,immunity)</code>
 *
 *     Starts the progression of the disease in the given unit.  The next four
 *     arguments (all integers) give the number of days the unit spends in each
 *     state.
 *   <li>
 *     <code>vaccinate (unit,delay,immunity)</code>
 *
 *     Vaccinates the given unit.  The argument <i>delay</i> gives the number
 *     of days the vaccine requires to take effect.  The animals are immune to
 *     the disease for the number of days given by the argument
 *     <i>immunity</i>.
 *   <li>
 *     <code>destroy (unit)</code>
 *
 *     Destroys the given unit.
 *   <li>
 *     <code>step</code>
 *
 *     Step forward one day.  The output of this command is a space-separated
 *     list of the unit states.
 *   <li>
 *     <code>reset</code>
 *
 *     Erase all currently entered units.
 * </ul>
 *
 * The shell exits on EOF (Ctrl+D if you're typing commands into it
 * interactively in Unix).
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date July 2003
 *
 * Copyright &copy; University of Guelph, 2003-2006
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

UNT_unit_list_t *current_units = NULL;
GPtrArray *production_type_names = NULL;
GHashTable *dummy; /* The UNT_step function, which advances a unit's state, has
  as an argument a hash table of infectious units, which is updated at the same
  time as the state change.  In this small test program, we don't need to do
  that, but we still need a hash table to pass to UNT_step. */


void g_free_as_GFunc (gpointer data, gpointer user_data);
%}

%union {
  int ival;
  double fval;
  char *sval;
  GSList *lval;
}

%token UNIT INFECT VACCINATE DESTROY STEP RESET
%token INT FLOAT STRING
%token LPAREN RPAREN COMMA
%token <ival> INT
%token <fval> REAL
%token <sval> STRING
%type <fval> real
%%

commands :
    command commands
  | command
  ;

command :
    new_command
  | infect_command
  | vaccinate_command
  | destroy_command
  | step_command
  | reset_command
  ;

new_command :
    UNIT LPAREN STRING COMMA INT COMMA real COMMA real RPAREN
    {
      UNT_unit_t *unit;
      int i;
      
      /* Find the production type name in the list of names encountered so far.
       * If it's not there, add it. */
      for (i = 0; i < production_type_names->len; i++)
	if (strcasecmp ($3, g_ptr_array_index (production_type_names, i)) == 0)
	  break;
      if (i == production_type_names->len)
	g_ptr_array_add (production_type_names, $3);
      else
	free ($3);

      unit = UNT_new_unit (i, g_ptr_array_index (production_type_names, i), $5, $7, $9);
      UNT_unit_list_append (current_units, unit);
      
      UNT_printf_unit (unit);
      free (unit);
      printf ("\n%s", PROMPT);
      fflush (stdout);
    }
  ;

infect_command:
    INFECT LPAREN INT COMMA INT COMMA INT COMMA INT COMMA INT RPAREN
    {
      g_assert (0 <= $3 && $3 < UNT_unit_list_length (current_units));
      UNT_infect (UNT_unit_list_get (current_units, $3), $5, $7, $9, $11, 0);
      printf ("%s", PROMPT);
      fflush (stdout);
    }
  ;

vaccinate_command:
    VACCINATE LPAREN INT COMMA INT COMMA INT RPAREN
    {
      g_assert (0 <= $3 && $3 < UNT_unit_list_length (current_units));
      UNT_vaccinate (UNT_unit_list_get (current_units, $3), $5, $7);
      printf ("%s", PROMPT);
      fflush (stdout);
    }
  ;

destroy_command:
    DESTROY LPAREN INT RPAREN
    {
      g_assert (0 <= $3 && $3 < UNT_unit_list_length (current_units));
      UNT_destroy (UNT_unit_list_get (current_units, $3));
      printf ("%s", PROMPT);
      fflush (stdout);
    }
  ;

step_command :
    STEP
    {
      unsigned int nunits;
      int i;
      
      nunits = UNT_unit_list_length (current_units);
      g_assert (nunits > 0);
      
      for (i = 0; i < nunits; i++)
        UNT_step (UNT_unit_list_get (current_units, i), dummy);

      printf ("%s", UNT_state_name[UNT_unit_list_get (current_units, 0)->state]);
      for (i = 1; i < nunits; i++)
        printf (" %s",  UNT_state_name[UNT_unit_list_get (current_units, i)->state]);
      printf ("\n%s", PROMPT);
      fflush (stdout);
    }
  ;

reset_command :
    RESET
    {
      UNT_free_unit_list (current_units);
      current_units = UNT_new_unit_list ();
      printf ("%s", PROMPT);
      fflush (stdout);
    }
  ;

real:
    INT
    {
      $$ = (double) $1; 
    }
  | REAL
    {
      $$ = $1;
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
  g_log_set_handler ("unit", G_LOG_LEVEL_MESSAGE | G_LOG_LEVEL_INFO | G_LOG_LEVEL_DEBUG, silent_log_handler, NULL);

  current_units = UNT_new_unit_list ();
  production_type_names = g_ptr_array_new ();
  dummy = g_hash_table_new (g_direct_hash, g_direct_equal);

  printf (PROMPT);
  if (yyin == NULL)
    yyin = stdin;
  while (!feof(yyin))
    yyparse();

  return EXIT_SUCCESS;
}

/* end of file shell.y */
