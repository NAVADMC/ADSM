%{
#if HAVE_CONFIG_H
#  include <config.h>
#endif

#include "reporting.h"
#include <stdio.h>

#if STDC_HEADERS
#  include <stdlib.h>
#endif

#if HAVE_STRING_H
#  include <string.h>
#endif

/** @file filters/full_table.c
 * A filter that turns SHARCSpread output into a table.
 *
 * Call it as
 *
 * <code>table_filter < LOG-FILE</code>
 *
 * The table is written to standard output in comma-separated values format.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date May 2004
 *
 * Copyright &copy; University of Guelph, 2004-2009
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

/** @page filters Output filters
 * The chart below shows the workflow for generating output on the
 * supercomputer.  Input files are orange.  Output files are blue for tables,
 * green for plots and images, and purple for Arcview GIS files.  Temporary
 * intermediate files are grey.
 *
 * @image html filters_flowchart.png
 */

#define YYERROR_VERBOSE
#define BUFFERSIZE 2048

/* int yydebug = 1; must also compile with --debug to use this */
int yylex(void);
int yyerror (char const *s);
char errmsg[BUFFERSIZE];

typedef struct
{
  gboolean is_null;
  double value;
  GString *svalue;
} output_value_t;

GPtrArray *output_names; /**< Names of output variables.  The names are
  GStrings. */
GData *output_values; /**< The output variable values.  It is a Keyed Data List
  that associates a variable name with an output_value_t structure. */
int current_node; /**< The most recent node number we have seen in the
  simulator output. */
int current_run; /**< The most recent run number we have seen in the output. */
int current_day; /**< The most recent day we have seen in the output. */
gboolean printed_header; /**< Whether we have printed the header line for the
  table or not. */



/**
 * Frees an output_value_t structure, defined above.  Typed as a GDestroyNotify
 * so that it can be used as the destroy_func in a Keyed Data List.
 */
void
free_output_value (gpointer data)
{
  output_value_t *output_value;
  if (data != NULL)
    {
      output_value = (output_value_t *) data;
      if (output_value->svalue != NULL)
        g_string_free (output_value->svalue, TRUE);
      g_free (output_value);
    }
  return;
}



/**
 * Wraps GLib's g_string_free function so that it can be used with a Pointer
 * Array's foreach function.
 */
void
g_string_free_as_GFunc (gpointer data, gpointer user_data)
{
  g_string_free ((GString *) data, TRUE);
}



/**
 * Returns a copy of the given text, transformed into CamelCase.
 *
 * @param text the original text.
 * @param capitalize_first if TRUE, the first character of the text will be
 *   capitalized.
 * @return a newly-allocated string.  If the "text" parameter is NULL, the
 *   return value will also be NULL.
 */
char *
camelcase (char *text, gboolean capitalize_first)
{
  char *newtext; /* Address of the newly-allocated CamelCase string. */
  char *newchar; /* Pointer to the current character of the new string, as we
    are building it. */
  gboolean last_was_space;

  newtext = NULL;
  if (text != NULL)
    {
      newtext = g_new (char, strlen(text)+1); /* +1 to leave room for the '\0' at the end */
      last_was_space = capitalize_first;
      for (newchar = newtext; *text != '\0'; text++)
        {
          if (g_ascii_isspace (*text))
            {
              last_was_space = TRUE;
              continue;
            }
          if (last_was_space && g_ascii_islower(*text))
            *newchar++ = g_ascii_toupper (*text);
          else
            *newchar++ = *text;
          last_was_space = FALSE;
        }
      /* End the new string with a null character. */
      *newchar = '\0';
    }
  return newtext;
}



/**
 * Adds all the values stored in an RPT_reporting_t structure to the list of
 * output values for today.  This function is typed as a GDataForeachFunc so
 * that it can easily be called recursively on the sub-variables.
 *
 * @param key_id use 0.
 * @param data an output variable, cast to a gpointer.
 * @param user_data the output variable's name as seen so far.  Used when
 *   recursively drilling down into sub-variables.  Use NULL for the top-level
 *   call.
 */
void
add_values (GQuark key_id, gpointer data, gpointer user_data)
{
  RPT_reporting_t *reporting;
  GString *name_so_far, *name;
  char *camel;
  output_value_t *tmp;
#if DEBUG
  unsigned int nnames, i;
  char *output_name;
  GString *s;
#endif

  reporting = (RPT_reporting_t *) data;
  name_so_far = (GString *) user_data;  

  /* Find the variable's name. */
  if (name_so_far == NULL)
    name = g_string_new (reporting->name);
  else
    {
      name = g_string_new (name_so_far->str);
      camel = camelcase (reporting->name, /* capitalize first = */ TRUE); 
      g_string_append_printf (name, "%s", camel);
      g_free (camel);
    }

  if (reporting->type == RPT_group)
    {
      g_datalist_foreach ((GData **) (&reporting->data), add_values, name);
      g_string_free (name, TRUE);
    }
  else
    {
      /* If we haven't printed the header yet (we're processing the very first
       * line of input), record the output variable's name. */
      if (!printed_header)
        g_ptr_array_add (output_names, name);

      /* Record the output variable's value. */
      tmp = g_new (output_value_t, 1);
      if (reporting->is_null)
        {
          tmp->is_null = TRUE;
          tmp->svalue = NULL;
        }
      else if (reporting->type == RPT_integer)
        {
          tmp->is_null = FALSE;
          tmp->value = (double)(*((long *)(reporting->data)));
          tmp->svalue = NULL;
        }
      else if (reporting->type == RPT_real)
        {
          tmp->is_null = FALSE;
          tmp->value = *((double *)(reporting->data));
          tmp->svalue = NULL;
        }
      else if (reporting->type == RPT_text)
        {
          tmp->is_null = FALSE;
          tmp->value = 0;
          tmp->svalue = g_string_new (((GString *)reporting->data)->str);
        }
      /* We shouldn't see repeats of the same data item on the same day. */
      if (g_datalist_get_data (&output_values, name->str) != NULL)
        g_error ("should not be seeing \"%s\" twice", name->str);

      g_datalist_set_data_full (&output_values, name->str, tmp, free_output_value);

      #if DEBUG
        /* Sanity check - make sure this variable is in the header. */
        nnames = output_names->len;
        for (i = 0; i < nnames; i++)
          {
            output_name = ((GString *) g_ptr_array_index (output_names, i))->str;
            if (strcmp (name->str, output_name) == 0)
              break;
          }
        if (i == nnames)
          {
            g_error ("name \"%s\" not in header", name->str);
          }
      #endif

      #if DEBUG
        s = g_string_new (NULL);
        g_string_printf (s, "value for \"%s\" now = ", name->str);
        if (tmp->is_null)
          g_string_append_printf (s, "null");
        else if (tmp->svalue != NULL)
          g_string_append_printf (s, "'%s'", tmp->svalue->str);
        else
          g_string_append_printf (s, "%g", tmp->value);
        g_debug ("%s", s->str);
        g_string_free (s, TRUE);
      #endif

      if (printed_header)
        g_string_free (name, TRUE);
    }
  return;
}



/**
 * Prints the stored output values.
 */
void
print_values ()
{
  static int run = 0; /* A run identifier that increases each time we print one
    complete Monte Carlo run.  This is distinct from the per-node run numbers
    in the simulator output. */
  unsigned int nnames, i;
  char *name;
  output_value_t *value;

  if (current_day == 1)
    run++;

  printf ("%u,%u", run, current_day);
  /* Output the values in the order that the variables appeared in the table
   * header line. */
  nnames = output_names->len;
  for (i = 0; i < nnames; i++)
    {
      printf (",");
      name = ((GString *) g_ptr_array_index (output_names, i))->str;
      value = (output_value_t *) (g_datalist_get_data (&output_values, name));
      /* Not every output variable is reported on every day, so sometimes the
       * value will be NULL. */
      if (value == NULL || value->is_null)
        continue;
      if (value->svalue == NULL)
        printf ("%g", value->value);
      else
        printf ("\"%s\"", value->svalue->str);
    }
  printf ("\n");
  
  return;
}



/**
 * Clears the stored output values.
 */
void
clear_values ()
{
  g_datalist_clear (&output_values);
}

%}

%union {
  int ival;
  float fval;
  char *sval;
  RPT_reporting_t *rval;
  GSList *lval;
}

%token NODE RUN DAY POLYGON
%token COMMA COLON EQ LBRACE RBRACE LPAREN RPAREN DQUOTE NEWLINE
%token <ival> INT
%token <fval> FLOAT
%token <sval> VARNAME STRING
%type <rval> value subvar
%type <lval> subvars
%type <sval> contours contour coords coord
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
      unsigned int i;

      /* If this was the first line read, print the table header. */
      if (!printed_header)
        {
          printf ("Run,Day");
          for (i = 0; i < output_names->len; i++)
            printf (",%s", ((GString *) g_ptr_array_index (output_names,i))->str);
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
    { }
  | INT
    { }
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
      $3->name = $1;

      /* At this point we have built, in a bottom-up fashion, one complete
       * output variable, stored in an RPT_reporting_t structure.  So we have a
       * tree-style represention of something like, for example,
       * 
       * num-units-in-each-state={'Susceptible':20,'Latent':10}
       *
       * What we want for the summary table is something like:
       *
       * num-units-in-each-state:Susceptible = 20, ...
       * num-units-in-each-state:Latent = 10, ...
       *
       * So we call a function that drills down into the RPT_reporting_t
       * structure and adds whatever sub-variables it finds, with their values,
       * to the master list of outputs.
       */
      add_values (0, $3, NULL);
      RPT_free_reporting ($3);
    }
  ;

value:
    INT
    {
      $$ = RPT_new_reporting (NULL, RPT_integer, RPT_never);
      RPT_reporting_set_integer ($$, $1, NULL);
    }
  | FLOAT
    {
      $$ = RPT_new_reporting (NULL, RPT_real, RPT_never);
      RPT_reporting_set_real ($$, $1, NULL);
    }
  | STRING
    {
      $$ = RPT_new_reporting (NULL, RPT_text, RPT_never);
      RPT_reporting_set_text ($$, $1, NULL);
      /* The string token's value is set with a g_strndup, so we need to free
       * it after copying it into the RPT_reporting structure. */
      g_free ($1);
    }
  | POLYGON LPAREN RPAREN
    {
      $$ = RPT_new_reporting (NULL, RPT_text, RPT_never);
      RPT_reporting_set_text ($$, "POLYGON()", NULL);
    }
  | POLYGON LPAREN contours RPAREN
    {
      char *s;
      $$ = RPT_new_reporting (NULL, RPT_text, RPT_never);
      s = g_strdup_printf ("POLYGON(%s)", $3);
      g_free ($3);
      RPT_reporting_set_text ($$, s, NULL);
      g_free (s);
    }
  | LBRACE RBRACE
    {
      $$ = RPT_new_reporting (NULL, RPT_integer, RPT_never);
      RPT_reporting_set_null ($$, NULL);
    }
  | LBRACE subvars RBRACE
    {
      GSList *iter;

      $$ = RPT_new_reporting (NULL, RPT_group, RPT_never);
      for (iter = $2; iter != NULL; iter = g_slist_next (iter))
	RPT_reporting_splice ($$, (RPT_reporting_t *) (iter->data));

      /* Now that the sub-variables have been attached to a newly-created group
       * reporting variable, free the linked list structure that contained
       * them. */
      g_slist_free ($2);
    }
  ;

subvars:
    subvars COMMA subvar
    {
      $$ = g_slist_append ($1, $3);
    }
  | subvar
    {
      /* Initialize a linked list of subvars. */
      $$ = g_slist_append (NULL, $1);
    }
  ;

subvar:
    STRING COLON value
    {
      $$ = $3;
      if ($$ != NULL)
        $$->name = $1;
      else
        g_free ($1);
    }
  ;

contours:
    contours contour
    {
      $$ = g_strdup_printf ("%s %s", $1, $2);
      g_free ($1);
      g_free ($2);
    }
  | contour
    {
      $$ = $1;
    }
  ;

contour:
    LPAREN coords RPAREN
    {
      $$ = g_strdup_printf ("(%s)", $2);
      g_free ($2);
    }
  ;

coords:
    coords COMMA coord
    {
      $$ = g_strdup_printf ("%s,%s", $1, $3);
      g_free ($1);
      g_free ($3);
    }
  | coord
    {
      $$ = $1;
    }
  ;

coord:
    FLOAT FLOAT
    {
      $$ = g_strdup_printf ("%g %g", $1, $2);
    }
  | FLOAT INT
    {
      $$ = g_strdup_printf ("%g %i", $1, $2);
    }
  | INT FLOAT
    {
      $$ = g_strdup_printf ("%i %g", $1, $2);
    }
  | INT INT
    {
      $$ = g_strdup_printf ("%i %i", $1, $2);
    }
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
      g_log_set_handler ("reporting", G_LOG_LEVEL_DEBUG, silent_log_handler, NULL);
    }
  #if DEBUG
    g_debug ("verbosity = %i", verbosity);
  #endif

  output_names = g_ptr_array_new ();
  g_datalist_init (&output_values);
  /* Initialize the current node to "-1" so that whatever node appears first in
   * the simulator output will signal the parser that output from a new node is
   * beginning, that the current day needs to be reset, etc. */
  current_node = -1;
  /* We have not yet printed the table header line. */
  printed_header = FALSE;

  /* Call the parser. */
  if (yyin == NULL)
    yyin = stdin;
  while (!feof(yyin))
    yyparse();

  /* Clean up. */
  g_ptr_array_foreach (output_names, g_string_free_as_GFunc, NULL);
  g_ptr_array_free (output_names, TRUE);
  g_datalist_clear (&output_values);

  return EXIT_SUCCESS;
}

/* end of file full_table.y */
