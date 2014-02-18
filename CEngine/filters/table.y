%{
#if HAVE_CONFIG_H
#  include <config.h>
#endif

#include "reporting.h"
#include <stdio.h>
#include <gsl/gsl_statistics_double.h>
#include <gsl/gsl_sort.h>

#if STDC_HEADERS
#  include <stdlib.h>
#  include <string.h>
#elif HAVE_STRINGS_H
#  include <strings.h>
#endif

#include <assert.h>

/** @file filters/table.c
 * A filter that turns SHARCSpread output into a summary table.
 *
 * Call it as
 *
 * <code>table_filter < LOG-FILE</code>
 *
 * The summary table is written to standard output in comma-separated values
 * format.
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

#define YYERROR_VERBOSE
#define BUFFERSIZE 2048
/* #define DEBUG 1 */

/* int yydebug = 1; must also compile with --debug to use this */
int yylex(void);
int yyerror (char const *s);
char errmsg[BUFFERSIZE];

typedef struct
{
  unsigned int run;
  unsigned int day;
  double value;
} run_day_value_triple_t;

GPtrArray *output_names; /**< Names of output variables.  The names are
  GStrings. */
GPtrArray *output_values; /**< The output variable values.  Each item in the
  list is for one node.  The items are Keyed Data Lists that associate a
  variable name with a GArray of run-day-value triples. */
unsigned int current_node;
GArray *current_run; /**< The most recent run number we have seen in the output
  from each node. */
GArray *current_day; /**< The most recent day we have seen in the output from
  each node. */
gboolean first_output;



/**
 * Wraps GLib's g_array_free function so that it can be used as the
 * GDestroyNotify function in a Keyed Data List.
 */
void
g_array_free_as_GDestroyNotify (gpointer data)
{
  g_array_free ((GArray *) data, TRUE);
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
 * Wraps g_ascii_strcasecmp so that it can be used as a GCompareFunc to
 * sort a Pointer Array of GStrings.
 */
gint
g_ascii_strcasecmp_as_GCompareFunc (gconstpointer a, gconstpointer b)
{
  char *s1, *s2;

  s1 = (*((GString **) a))->str;
  s2 = (*((GString **) b))->str;
  return g_ascii_strcasecmp (s1, s2);  
}



/**
 * Adds all the values stored in an RPT_reporting_t structure to the master
 * list of outputs.  This function is typed as a GDataForeachFunc so that
 * it can easily be called recursively on the sub-variables.
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
  GArray *values;
  GData **node_output_values;
  gboolean new_name = FALSE;
  run_day_value_triple_t tmp;
  unsigned int nnames, i;

  reporting = (RPT_reporting_t *) data;
  name_so_far = (GString *) user_data;  

  /* Find the variable's name. */
  if (name_so_far == NULL)
    name = g_string_new (reporting->name);
  else
    {
      name = g_string_new (name_so_far->str);
      g_string_append_printf (name, ":%s", reporting->name);
    }

  switch (reporting->type)
    {
    case RPT_integer:
      /* Check whether the list of output variable names already contains this
       * variable. */
      nnames = output_names->len;
      for (i = 0; i < nnames; i++)
	if (g_string_equal (name, g_ptr_array_index (output_names, i)))
	  break;
      if (i == nnames)
	{
	  new_name = TRUE;
	  g_ptr_array_add (output_names, name);	  
	}

      tmp.run = g_array_index (current_run, unsigned int, current_node);
      tmp.day = g_array_index (current_day, unsigned int, current_node);
      tmp.value = (double)(*((long *)(reporting->data)));

      node_output_values = (GData **)(&g_ptr_array_index (output_values, current_node));
      values = (GArray *) (g_datalist_get_data (node_output_values, name->str));
      /* If no values have been recorded for this node and variable before,
       * create a new list. */
      if (values == NULL)
	{
	  values = g_array_new (FALSE, FALSE, sizeof (run_day_value_triple_t));
	  g_datalist_set_data_full (node_output_values, name->str, values,
				    g_array_free_as_GDestroyNotify);
	  g_array_append_val (values, tmp);
	}	  
      /* If values have been recorded for this node and variable, check the
       * most recent one.  If it is for the current day, add to it; otherwise,
       * replace it. */
      else
        {
	  if (g_array_index (values, run_day_value_triple_t, values->len - 1).run == tmp.run)
	    {
	      if (g_array_index (values, run_day_value_triple_t, values->len - 1).day == tmp.day)
		g_array_index (values, run_day_value_triple_t, values->len - 1).value += tmp.value;
	      else
		{
		  g_array_index (values, run_day_value_triple_t, values->len - 1).day = tmp.day;
		  g_array_index (values, run_day_value_triple_t, values->len - 1).value = tmp.value;
		}
	    }
	  else
	    g_array_append_val (values, tmp);
        }
      break;

    case RPT_real:
      /* Check whether the list of output variable names already contains this
       * variable. */
      nnames = output_names->len;
      for (i = 0; i < nnames; i++)
	if (g_string_equal (name, g_ptr_array_index (output_names, i)))
	  break;
      if (i == nnames)
	{
	  new_name = TRUE;
	  g_ptr_array_add (output_names, name);	  
	}

      tmp.run = g_array_index (current_run, unsigned int, current_node);
      tmp.day = g_array_index (current_day, unsigned int, current_node);
      tmp.value = *((double *)(reporting->data));

      node_output_values = (GData **)(&g_ptr_array_index (output_values, current_node));
      values = (GArray *) (g_datalist_get_data (node_output_values, name->str));
      /* If no values have been recorded for this node and variable before,
       * create a new list. */
      if (values == NULL)
	{
	  values = g_array_new (FALSE, FALSE, sizeof (run_day_value_triple_t));
	  g_datalist_set_data_full (node_output_values, name->str, values,
				    g_array_free_as_GDestroyNotify);
	  g_array_append_val (values, tmp);
	}	  
      /* If values have been recorded for this node and variable, check the
       * most recent one.  If it is for the current day, add to it; otherwise,
       * replace it. */
      else
        {
	  if (g_array_index (values, run_day_value_triple_t, values->len - 1).run == tmp.run)
	    {
	      if (g_array_index (values, run_day_value_triple_t, values->len - 1).day == tmp.day)
		g_array_index (values, run_day_value_triple_t, values->len - 1).value += tmp.value;
	      else
		{
		  g_array_index (values, run_day_value_triple_t, values->len - 1).day = tmp.day;
		  g_array_index (values, run_day_value_triple_t, values->len - 1).value = tmp.value;
		}
	    }
	  else
	    g_array_append_val (values, tmp);
        }
      break;

    case RPT_text:
      break;

    case RPT_group:
      g_datalist_foreach ((GData **) (&reporting->data), add_values, name);
      break;

    default:
      g_assert_not_reached ();
    }

  if (!new_name)
    g_string_free (name, TRUE);
}



/**
 * Clears the stored output values for one node.
 */
void
clear_values (unsigned int node)
{
  GData **node_output_values;

  node_output_values = (GData **)(&g_ptr_array_index (output_values, node));
  g_datalist_clear (node_output_values);
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
%%
output_lines :
    output_lines output_line
    { }
  | output_line
    { }
  ;

output_line:
    tracking_line NEWLINE data_line NEWLINE
    { }
  ;

tracking_line:
    NODE INT RUN INT
    {
      unsigned int node = $2;
      unsigned int run = $4;
      GData *new_list;

      /* If we haven't seen output from this node before, we need to extend the
       * tracking lists for current run and current day, and create a new
       * Keyed Data List to hold output values for the new node. */
      if ((node + 1) > current_run->len)
        {
	  g_array_set_size (current_run, node + 1);

	  g_array_set_size (current_day, node + 1);
	  g_array_index (current_day, unsigned int, node) = 1;

	  g_ptr_array_set_size (output_values, node + 1);
	  /* Initialize the new entry to an empty Keyed Data List. */
	  g_datalist_init (&new_list);
	  g_ptr_array_index (output_values, node) = new_list;
	}
      else
	{
	  /* Since output from a single node is sequential, when we see that the
	   * run number has changed, we know the output from one Monte Carlo trial
	   * is over.  So we reset the day for that node. */
	  if (run != g_array_index (current_run, unsigned int, node))
            {
	      g_array_index (current_run, unsigned int, node) = run;
	      g_array_index (current_day, unsigned int, node) = 1;
	    }
	  else
	    g_array_index (current_day, unsigned int, node) ++;
	}
      current_node = node;
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
      if ($3 != NULL)
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
      else
        g_free ($1);
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
    /* The parser contains rules for parsing polygons, because they may appear
     * in the output, but we do nothing with them. */
  | POLYGON LPAREN RPAREN
    {
      $$ = NULL;
    }
  | POLYGON LPAREN contours RPAREN
    {
      $$ = NULL;
    }
  | LBRACE RBRACE
    {
      $$ = NULL;
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

/* The parser contains rules for parsing polygons, because they may appear in
 * the output, but we do nothing with them. */

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
  unsigned int noutputs, nvalues;
  unsigned int i, j;
  char *s;
  GData **node_output_values;
  GArray *node_values, *values;
  double value;
  double mean, stddev, lo, hi, p05, p10, p25, median, p75, p90, p95;
  GError *option_error = NULL;
  GOptionContext *context;
  GOptionEntry options[] = {
    { "verbosity", 'V', 0, G_OPTION_ARG_INT, &verbosity, "Message verbosity level (0 = simulation output only, 1 = all debugging output)", NULL },
    { NULL }
  };
#if DEBUG
  GString *tmp;
#endif

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
  output_values = g_ptr_array_new ();
  current_run = g_array_sized_new (FALSE, TRUE, sizeof (unsigned int), 1);
  current_day = g_array_sized_new (FALSE, TRUE, sizeof (unsigned int), 1);

  /* Call the parser to fill the output_names and output_values arrays. */
  if (yyin == NULL)
    yyin = stdin;
  while (!feof(yyin))
    yyparse();

  /* Print the header line for the table. */
  printf ("Output,Number of occurrences,Mean,StdDev,Low,High,p5,p10,p25,p50 (Median),p75,p90,p95\n");

  /* Alphabetize the output variable names. */
  g_ptr_array_sort (output_names, g_ascii_strcasecmp_as_GCompareFunc);

  values = g_array_new (/* zero_terminated = */ FALSE,
			/* clear = */ FALSE,
			sizeof (double));
  noutputs = output_names->len;
  for (i = 0; i < noutputs; i++)
    {
      s = ((GString *) g_ptr_array_index (output_names, i))->str;
      printf ("%s", s);

      /* Combine the values for this output variable from each node into one
       * big list. */
      g_array_set_size (values, 0);
      for (current_node = 0; current_node < output_values->len; current_node++)
	{
	  node_output_values = (GData **)(&g_ptr_array_index (output_values, current_node));
	  node_values = (GArray *) (g_datalist_get_data (node_output_values, s));
	  if (node_values == NULL)
	    continue;
	  for (j = 0; j < node_values->len; j++)
	    {
	      value = g_array_index (node_values, run_day_value_triple_t, j).value;
	      g_array_append_val (values, value);
	    }
	}

      nvalues = values->len;
      printf (",%u", nvalues);

      if (nvalues == 0)
        {
          mean = stddev = 0;
          lo = p05 = p10 = p25 = median = p75 = p90 = p95 = hi = 0;
        }
      else
        {
          mean = gsl_stats_mean ((double *)(values->data), 1, nvalues);
          /* The formula for standard deviation contains a 1/(N-1), so if there
           * is only 1 value, we just list standard deviation as 0. */
          if (nvalues == 1)
            stddev = 0;
          else
            stddev = gsl_stats_sd_m ((double *)(values->data), 1, nvalues, mean);

          /* Sort the values in preparation for doing median and quantiles. */
          gsl_sort ((double *)(values->data), 1, nvalues);

          /* Now that it's sorted, low and high are easy. */
          lo = g_array_index (values, double, 0);
          hi = g_array_index (values, double, nvalues - 1);

          median = gsl_stats_median_from_sorted_data ((double *)(values->data), 1, nvalues);
          p05 = gsl_stats_quantile_from_sorted_data ((double *)(values->data), 1, nvalues, 0.05);
          p10 = gsl_stats_quantile_from_sorted_data ((double *)(values->data), 1, nvalues, 0.10);
          p25 = gsl_stats_quantile_from_sorted_data ((double *)(values->data), 1, nvalues, 0.25);
          p75 = gsl_stats_quantile_from_sorted_data ((double *)(values->data), 1, nvalues, 0.75);
          p90 = gsl_stats_quantile_from_sorted_data ((double *)(values->data), 1, nvalues, 0.90);
          p95 = gsl_stats_quantile_from_sorted_data ((double *)(values->data), 1, nvalues, 0.95);
        }

      printf (",%g,%g", mean, stddev);
      printf (",%g,%g", lo, hi);
      printf (",%g,%g,%g,%g,%g,%g,%g\n", p05, p10, p25, median, p75, p90, p95);

#if DEBUG
      fflush (stdout);
      tmp = g_string_new (NULL);
      for (j = 0; j < nvalues; j++)
	g_string_append_printf (tmp, " %g", g_array_index (values, double, j));
      g_debug ("%s", tmp->str);
      g_string_free (tmp, TRUE);
#endif
    }

  /* Clean up. */
  g_array_free (current_run, TRUE);
  g_array_free (current_day, TRUE);
  g_ptr_array_foreach (output_names, g_string_free_as_GFunc, NULL);
  g_ptr_array_free (output_names, TRUE);
  for (i = 0; i < output_values->len; i++)
    g_datalist_clear ((GData **) (&g_ptr_array_index (output_values, i)));
  g_ptr_array_free (output_values, TRUE);

  return EXIT_SUCCESS;
}

/* end of file table.y */
