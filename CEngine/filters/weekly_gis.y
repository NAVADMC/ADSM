%{
#if HAVE_CONFIG_H
#  include <config.h>
#endif

#include <stdio.h>
#include "unit.h"
#include <shapefil.h>

#if STDC_HEADERS
#  include <stdlib.h>
#  include <string.h>
#elif HAVE_STRINGS_H
#  include <strings.h>
#endif

#include <assert.h>

/** @file filters/weekly_gis.c
 * A filter that takes a state table (output from state_table_filter) and an
 * ArcView file (output from xml2shp) and creates new ArcView files giving
 * weekly snapshots of the state of each unit for the first Monte Carlo trial.
 *
 * Call it as
 *
 * <code>weekly_gis_filter ARCVIEW-SHP-FILE < STATE-TABLE-FILE</code>
 *
 * Weekly ArcView files are written to the current working directory.  Their
 * names are the same as the base ArcView file but with _dayxxxx appended.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date October 2005
 *
 * Copyright &copy; University of Guelph, 2005-2007
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#define YYERROR_VERBOSE
#define BUFFERSIZE 2048
#define COPY_BUFFERSIZE 8192

/* int yydebug = 1; must also compile with --debug to use this */
int yylex(void);
int yyerror (char const *s);
char errmsg[BUFFERSIZE];

unsigned int nunits;
unsigned int last_day; /**< The most recent run number we have seen in the
  table. */
GArray *last_day_states; /**< Each item is of type UNT_state_t. */
const char *arcview_shp_filename;
char *arcview_base_name;
char *arcview_shx_filename = NULL;
char *arcview_dbf_filename = NULL;
gboolean done;



void
copy (const char *src_filename, const char *dest_filename)
{
  FILE *src, *dest;
  static char buffer [COPY_BUFFERSIZE];
  size_t len = 1;

  src = fopen (src_filename, "r");
  dest = fopen (dest_filename, "w");
  while (!feof (src))
    {
      len = fread (buffer, sizeof(char), COPY_BUFFERSIZE, src);
      if (len > 0)
        fwrite (buffer, sizeof(char), len, dest);    
    }
  fclose (dest);
  fclose (src);

  return;
}



/**
 * Creates ArcView files showing the units in the given states.
 */
void
make_arcview (GArray *states, unsigned int day)
{
  char *tmp_shp_filename;
  char *tmp_shx_filename;
  char *tmp_dbf_filename;
  DBFHandle dbf_file;
  int state_field;
  unsigned int i;
  UNT_state_t state;

  tmp_shp_filename = g_strdup_printf ("%s_day%04u.shp", arcview_base_name, day);
  tmp_shx_filename = g_strdup_printf ("%s_day%04u.shx", arcview_base_name, day);
  tmp_dbf_filename = g_strdup_printf ("%s_day%04u.dbf", arcview_base_name, day);

  copy (arcview_shp_filename, tmp_shp_filename);
  copy (arcview_shx_filename, tmp_shx_filename);
  copy (arcview_dbf_filename, tmp_dbf_filename);

  /* Write the unit states into the DBF file. */
  dbf_file = DBFOpen (tmp_dbf_filename, "rb+");
  state_field = DBFGetFieldIndex (dbf_file, "state");
  for (i = 0; i < nunits; i++)
    {
      state = g_array_index (states, UNT_state_t, i);
      DBFWriteStringAttribute (dbf_file, i, state_field,
			       UNT_state_name[state]);
    }
  DBFClose (dbf_file);

  /* Clean up. */
  g_free (tmp_shp_filename);
  g_free (tmp_shx_filename);
  g_free (tmp_dbf_filename);

  return;
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
%type <ival> unit_seqs
%type <lval> state_codes
%%
state_table:
    header_line NEWLINE data_lines NEWLINE
    { }
  ;

header_line:
    RUN COMMA DAY COMMA unit_seqs
    {
      nunits = $5;
      #if DEBUG
        g_debug ("# units = %u", nunits);      
      #endif
    }
  ;

unit_seqs:
    unit_seqs COMMA INT
    {
      /* Increment the count of units. */
      $$ = $1 + 1;
    }
  | INT
    {
      /* Initialize the count of units. */
      $$ = 1;
    }
  ;

data_lines:
    data_lines NEWLINE data_line
    { }
  | data_line
    { }
  ;

data_line:
    INT COMMA INT COMMA state_codes
    {
      unsigned int run, day;
      
      run = $1;

      /* We only create ArcView files for the first Monte Carlo run.  If we're
       * onto the second run, check whether the final day of the last run needs
       * to be written out.  After that, abort the parse. */
      if (run > 1)
	{
	  done = TRUE;
	  YYACCEPT;
	}

      /* Output an ArcView file for day 1, 8, 15, etc. */
      day = $3;
      if (day % 7 == 1)
	make_arcview ($5, day);

      if (last_day_states != NULL)
	g_array_free (last_day_states, TRUE);
      last_day_states = $5;
      last_day = day;
    }
  ;

state_codes:
    state_codes COMMA INT
    {
      $$ = $1;
      g_array_append_val ($$, $3);
    }
  | INT
    {
      /* Initialize an array of state codes. */
      $$ = g_array_sized_new (FALSE, FALSE, sizeof(UNT_state_t), nunits);
      g_array_append_val ($$, $1);
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

  /* Get the command-line options and arguments.  There should be one command-
   * line argument, the name of the ArcView .shp file. */
  context = g_option_context_new ("");
  g_option_context_add_main_entries (context, options, /* translation = */ NULL);
  if (!g_option_context_parse (context, &argc, &argv, &option_error))
    {
      g_error ("option parsing failed: %s\n", option_error->message);
    }
  if (argc >= 2)
    arcview_shp_filename = argv[1];
  else
    arcview_shp_filename = NULL;
  if (arcview_shp_filename == NULL
      || !g_str_has_suffix (arcview_shp_filename, ".shp"))
    {
      g_error ("Need the name of an ArcView shape (.shp) file.");
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

  /* Get the base part (without the .shp) of the ArcView file name. */
  arcview_base_name = g_strndup (arcview_shp_filename,
				 strlen(arcview_shp_filename) - 4);
  #if DEBUG
    g_debug ("base part of ArcView file name = \"%s\"", arcview_base_name);
  #endif
  arcview_shx_filename = g_strdup_printf ("%s.shx", arcview_base_name);
  arcview_dbf_filename = g_strdup_printf ("%s.dbf", arcview_base_name);

  nunits = 0;
  done = FALSE;
  last_day_states = NULL;

  /* Call the parser. */
  if (yyin == NULL)
    yyin = stdin;
  while (!feof(yyin) && !done)
    yyparse();

  /* We want ArcView files for the final day.  If the final day was 1 plus a
   * multiple of 7, then the files have already been made.  If not, make
   * them. */
  if (last_day % 7 != 1)
    make_arcview (last_day_states, last_day);

  /* Clean up. */
  g_free (arcview_base_name);
  g_free (arcview_shx_filename);
  g_free (arcview_dbf_filename);
  if (last_day_states != NULL)
    g_array_free (last_day_states, TRUE);

  return EXIT_SUCCESS;
}

/* end of file weekly_gis.y */
