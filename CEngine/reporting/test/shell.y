%{
#if HAVE_CONFIG_H
#  include <config.h>
#endif

#if HAVE_STRINGS_H
#  include <strings.h>
#endif

#include <reporting.h>
#include <glib.h>
#include <math.h>
#include <stdlib.h>

#define PROMPT "> "



/** @file reporting/test/shell.c
 * A simple shell to exercise libreporting.  It provides a way to create
 * output variables and call the functions offered by the
 * <a href="reporting_8h.html">library</a>, so that a suite of tests can be
 * scripted.
 *
 * The commands are:
 * <ul>
 *   <li>
 *     <code>variable (name)</code>
 *
 *     Creates a new output variable.  The argument may be any string,
 *     e.g., <code>"x"</code>, <code>"variable_1"</code>.
 *   <li>
 *     <code>set (value,category,sub-category,...)</code>
 *
 *     Sets the value of the most recently created variable.  There can be an
 *     arbitrary number of sub-categories, or, the category and sub-categories
 *     can be omitted altogether.
 *   <li>
 *     <code>add (value,category,sub-category,...)</code>
 *
 *     Adds the value to the most recently created variable.  Same comments
 *     apply as for <code>set</code>.
 *   <li>
 *     <code>subtract (value,category,sub-category,...)</code>
 *
 *     Subtracts the value from the most recently created variable.  Not
 *     available for text variables.  Same comments apply as for
 *     <code>set</code>.
 *   <li>
 *     <code>get (category,sub-category,...)</code>
 *
 *     Retrieves the value of the most recently created variable.  Same
 *     comments apply as for <code>set</code>.
 * </ul>
 *
 * The shell exits on EOF (Ctrl+D if you're typing commands into it
 * interactively in Unix).
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date August 2004
 *
 * Copyright &copy; University of Guelph, 2004-2006
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

RPT_reporting_t *current_variable = NULL;
char *tentative_name = NULL;



void g_free_as_GFunc (gpointer data, gpointer user_data);

%}

%union {
  gboolean bval;
  int ival;
  double fval;
  char *sval;
  GSList *lval;
}

%token VARIABLE SET ADD SUBTRACT GET
%token LPAREN RPAREN COMMA
%token <ival> INT
%token <fval> REAL
%token <sval> STRING
%token <bval> BOOL
%type <fval> real

%%

commands :
    command commands
  | command
  ;

command :
    new_command
  | set_command
  | add_command
  | subtract_command
  | get_command
  ;

new_command :
    VARIABLE LPAREN STRING RPAREN
    {
      RPT_free_reporting (current_variable);
      current_variable = NULL;

      /* The variable will be created when it is first assigned to and we can
       * see its type.  Until then, just record the name. */
      tentative_name = $3;

      printf ("%s", PROMPT);
      fflush (stdout);
    }
  ;

set_command:
    SET LPAREN INT RPAREN
    {
      /* Integer, no subcategories. */
      char *s;

      RPT_free_reporting (current_variable);
      current_variable = RPT_new_reporting (tentative_name, RPT_integer);
      RPT_reporting_set_integer (current_variable, $3, NULL);
      s = RPT_reporting_value_to_string (current_variable, NULL);
      printf ("%s\n%s", s, PROMPT);
      free (s);
      fflush (stdout);
    }
  ;

add_command:
    ADD LPAREN INT RPAREN
    {
      /* Integer, no subcategories. */
      char *s;

      if (current_variable == NULL)
        current_variable = RPT_new_reporting (tentative_name, RPT_integer);
      RPT_reporting_add_integer (current_variable, $3, NULL);
      s = RPT_reporting_value_to_string (current_variable, NULL);
      printf ("%s\n%s", s, PROMPT);
      free (s);
      fflush (stdout);
    }
  ;

subtract_command:
    SUBTRACT LPAREN INT RPAREN
    {
      char *s;

      /* Integer, no subcategories. */
      if (current_variable == NULL)
	current_variable = RPT_new_reporting (tentative_name, RPT_integer);
      RPT_reporting_sub_integer (current_variable, $3, NULL);
      s = RPT_reporting_value_to_string (current_variable, NULL);
      printf ("%s\n%s", s, PROMPT);
      free (s);
      fflush (stdout);
    }
  ;

get_command :
    GET LPAREN RPAREN
    {
      char *s;

      s = RPT_reporting_value_to_string (current_variable, NULL);
      printf ("%s\n%s", s, PROMPT);
      free (s);
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
  g_log_set_handler ("reporting", G_LOG_LEVEL_MESSAGE | G_LOG_LEVEL_INFO | G_LOG_LEVEL_DEBUG, silent_log_handler, NULL);

  printf (PROMPT);
  if (yyin == NULL)
    yyin = stdin;
  while (!feof(yyin))
    yyparse();

  return EXIT_SUCCESS;
}

/* end of file shell.y */
