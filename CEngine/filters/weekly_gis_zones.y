%{
#if HAVE_CONFIG_H
#  include <config.h>
#endif

#include <stdio.h>
#include <glib.h>
#include <gpcl/gpc.h>
#include <shapefil.h>

#if STDC_HEADERS
#  include <stdlib.h>
#  include <string.h>
#elif HAVE_STRINGS_H
#  include <strings.h>
#endif

/** @file filters/weekly_gis_zones.c
 * A filter that takes a table of zone shapes (output from full_table_filter,
 * just the polygon columns) and creates ArcView files giving weekly snapshots
 * of the zone shapes for the first Monte Carlo trial.
 *
 * Call it as
 *
 * <code>weekly_gis_zones_filter SHP-FILE < TABLE-FILE</code>
 *
 * If you're starting with a full table file, containing other columns along
 * with the polygon columns, a convenient way to call this filter is:
 *
 * <code>cat TABLE-FILE | python extract_columns.py "zone-shape" |
 * weekly_gis_zones_filter SHP-FILE</code>
 *
 * Weekly ArcView files are written to the current working directory.  SHP-FILE
 * is the base name for the 3 ArcView files.  For example, if SHP-FILE is
 * "abc", this program will output files named abc_dayxxxx.shp,
 * abc_dayxxxx.shx, and abc_dayxxxx.dbf, where xxxx is the simulation day.
 *
 * During parsing, this program stores the polygons as gpc_polygon objects
 * because they're convenient to build up piece by piece.  When it's time to
 * write the polygons to disk, the program converts them to SHPObject objects.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date November 2006
 *
 * Copyright &copy; University of Guelph, 2006-2007
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

unsigned int nzones;
GPtrArray *zone_names; /**< Each item is of type GString. */
unsigned int max_zone_name_length; /**< The length of the longest zone name.
  Used to set the width of the name field in the ArcView attribute (.dbf)
  file. */
unsigned int last_day; /**< The most recent run number we have seen in the
  table. */
GPtrArray *last_day_zones; /**< Each item is a pointer to a gpc_polygon. */
const char *arcview_shp_filename = NULL;
char *arcview_base_name;
gboolean done;



/**
 * Wraps g_string_free so that it can be used in GLib calls.
 *
 * @param data a pointer to a GString, but cast to a gpointer.
 * @param user_data not used, pass NULL.
 */
void
g_string_free_as_GFunc (gpointer data, gpointer user_data)
{
  g_string_free ((GString *) data, TRUE);
}



/**
 * Wraps gpc_free_polygon so that it can be used in GLib calls.
 *
 * @param data a pointer to a gpc_polygon, but cast to a gpointer.
 * @param user_data not used, pass NULL.
 */
void
gpc_free_polygon_as_GFunc (gpointer data, gpointer user_data)
{
  if (data != NULL)
    gpc_free_polygon ((gpc_polygon *) data);
}



/**
 * Creates ArcView files showing the zones.
 *
 * @param zones a list of zones.  Each item is a gpc_polygon object.  The
 *   zones are ordered from highest level (smallest) to lowest level (largest).
 * @param day the day of the simulation.
 */
void
make_arcview (GPtrArray *zones, unsigned int day)
{
  char *tmp_shp_filename;
  char *tmp_dbf_filename;
  SHPHandle shape_file;
  DBFHandle attribute_file;
  int name_field;
  int i;
  unsigned int j, k, n;
  char *zone_name;
  gpc_polygon *poly;
  gpc_vertex_list *contour;
  gpc_vertex *vertex;
  int *panPartStart;
  int nVertices;
  double *padfX, *padfY;
  int vert_index;
  SHPObject *shape;
  int shape_id;

  tmp_shp_filename = g_strdup_printf ("%s_day%04u.shp", arcview_base_name, day);
  tmp_dbf_filename = g_strdup_printf ("%s_day%04u.dbf", arcview_base_name, day);

  /* Initialize the shape and DBF (attribute) files for writing. */
  shape_file = SHPCreate (tmp_shp_filename, SHPT_POLYGON);
  #if DEBUG
    g_debug ("opened shapefile \"%s\" for writing", tmp_shp_filename);
  #endif
  attribute_file = DBFCreate (tmp_dbf_filename);
  name_field = DBFAddField (attribute_file, "name", FTString, max_zone_name_length, 0);

  /* Write the zones into the shapefile from lowest level (largest) to highest
   * level (smallest).  If it were done the other way around, the smaller zone
   * shapes would be hidden behind the larger ones. */
  for (i = nzones - 1; i >= 0; i--)
    {
      poly = (gpc_polygon *) g_ptr_array_index (zones, i);
      if (poly == NULL || poly->num_contours == 0)
        continue;

      /* The Shapefile format requires the vertices for all contours to be
       * combined in a single array of x values and a single array of y values.
       * Get a count of the vertices and allocate the arrays. */
      panPartStart = g_new (int, poly->num_contours);
      nVertices = 0;
      for (j = 0; j < poly->num_contours; j++)
        {
          panPartStart[j] = nVertices;
          nVertices += poly->contour[j].num_vertices;
        }
      padfX = g_new (double, nVertices);
      padfY = g_new (double, nVertices);

      /* Copy the vertices into the separate x and y arrays. */
      for (j = 0, vert_index = 0; j < poly->num_contours; j++)
        {
          contour = &(poly->contour[j]);
          n = contour->num_vertices;
          for (k = 0; k < n; k++)
            {
              vertex = &(contour->vertex[k]);
              padfX[vert_index] = vertex->x;
              padfY[vert_index] = vertex->y;
              vert_index++;
            }
        }
      
      shape = SHPCreateObject (SHPT_POLYGON, -1, poly->num_contours,
                               panPartStart, NULL, nVertices, padfX, padfY,
                               NULL, NULL);
      /* The -1 is the library's code for creating a new object in the
       * shapefile as opposed to overwriting an existing one. */
      shape_id = SHPWriteObject (shape_file, -1, shape);
      zone_name = ((GString *) g_ptr_array_index (zone_names, i))->str;
      DBFWriteStringAttribute (attribute_file, shape_id, name_field, zone_name);
      #if DEBUG
        g_debug ("wrote shape for \"%s\" zone", zone_name);
      #endif

      g_free (panPartStart);
      g_free (padfX);
      g_free (padfY);
    }

  /* Clean up. */
  SHPClose (shape_file);
  DBFClose (attribute_file);
  g_free (tmp_shp_filename);
  g_free (tmp_dbf_filename);

  return;
}

%}

%union {
  int ival;
  float fval;
  char *sval;
  GString *gsval;
  GArray *aval;
  GPtrArray *lval;
  gpc_polygon *pval;
  gpc_vertex vval;
}

%token NODE RUN DAY POLYGON
%token COMMA COLON EQ LBRACE RBRACE LPAREN RPAREN DQUOTE NEWLINE
%token <ival> INT
%token <fval> FLOAT
%token <sval> VARNAME
%type <gsval> var_name_part
%type <lval> var_name
%type <lval> polygons
%type <pval> polygon
%type <pval> contours
%type <pval> contour
%type <aval> coords
%type <vval> coord
%%
table:
    header_line NEWLINE data_lines NEWLINE
    { }
  ;

header_line:
    RUN COMMA DAY
    {
      /* The header line could look like this if there were no zone-shape
       * columns in the full table file. */
    }
  | RUN COMMA DAY COMMA var_names
    {
      unsigned int i;
      GString *s;
 
      #if DEBUG
        g_debug ("read all zones names");
      #endif
      for (i = 0; i < nzones; i++)
        {
          s = (GString *) g_ptr_array_index (zone_names, i);
          if (s->len > max_zone_name_length)
            max_zone_name_length = s->len;
          #if DEBUG
            g_debug ("zone #%u = \"%s\"", i+1, s->str);
          #endif
        }
      #if DEBUG
        g_debug ("longest zone name = %u chars", max_zone_name_length);            
      #endif
    }
  ;

var_names:
    var_names COMMA var_name
    {
      GString *s;

      /* Make sure the first part of the variable name is "zone-shape" or
       * "zoneShape". */
      s = (GString *) g_ptr_array_index ($3, 0);
      if (g_ascii_strncasecmp (s->str, "zone-shape", 10) != 0
          && g_ascii_strncasecmp (s->str, "zoneShape", 9) != 0)
        {
          g_error ("found a variable \"%s\" that is not a zone-shape", s->str);
        }

      /* Add the name to the list of zone names. */
      g_ptr_array_add (zone_names, s);
      nzones++;

      g_ptr_array_free ($3, TRUE);
    }
  | var_name
    {
      GString *s;

      /* Make sure the first part of the variable name is "zone-shape" or
       * "zoneShape". */
      s = (GString *) g_ptr_array_index ($1, 0);
      if (g_ascii_strncasecmp (s->str, "zone-shape", 10) != 0
          && g_ascii_strncasecmp (s->str, "zoneShape", 9) != 0)
        {
          g_error ("found a variable \"%s\" that is not a zone-shape", s->str);
        }

      /* Add the name to the list of zone names. */
      g_ptr_array_add (zone_names, s);
      nzones++;

      g_ptr_array_free ($1, TRUE);
    }
  ;

var_name:
    /* Each variable name has 1 or more parts, separated by colons.  Each part
     * has 1 or more words, separated by spaces.  We return a var_name as a
     * GPtrArray containing one GString per var_name_part. */
    var_name COLON var_name_part
    {
      #if DEBUG
        GString *s;
        int i;
      #endif

      g_ptr_array_add ($1, $3);
      $$ = $1;
      #if DEBUG
        /* Print all the var_name_parts gathered so far, separated by colons. */
        s = g_string_new (NULL);
        for (i = 0; i < $$->len; i++)
          {
            if (i > 0)
              g_string_append_c (s, ':');
            g_string_append_printf (s, "%s", ((GString *) g_ptr_array_index ($$, i))->str);
          }
        g_debug ("var_name = \"%s\"", s->str);
        g_string_free (s, TRUE);
      #endif
    }
  | var_name_part
    {
      $$ = g_ptr_array_new();
      g_ptr_array_add ($$, $1);
      #if DEBUG
        g_debug ("var_name = \"%s\"", $1->str);
      #endif
    }  
  ;

var_name_part:
    var_name_part VARNAME
    {
      g_string_append_printf ($1, " %s", $2);
      free ($2);
      $$ = $1;
    }
  | VARNAME
    {
      $$ = g_string_new ($1);
      free ($1);
    }
  | var_name_part INT
    {
      g_string_append_printf ($1, " %i", $2);
      $$ = $1;
    }
  | INT
    {
      $$ = g_string_new (NULL);
      g_string_printf ($$, "%i", $1);
    }
  ;

data_lines:
    data_lines NEWLINE data_line
    { }
  | data_line
    { }
  ;

data_line:
    INT COMMA INT
    {
      /* The data lines could look like this if there were no zone-shape
       * columns in the full table file. */
    }
  | INT COMMA INT COMMA polygons
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
      if (day % 7 == 1 && nzones > 0)
        make_arcview ($5, day);

      if (last_day_zones != NULL)
        {
          g_ptr_array_foreach (last_day_zones, gpc_free_polygon_as_GFunc, NULL);
          g_ptr_array_free (last_day_zones, TRUE);
        }

      last_day_zones = $5;
      last_day = day;
    }
  ;

polygons:
    polygons COMMA polygon
    {
      /* Add to the array of zone shapes. */
      $$ = $1;
      g_ptr_array_add ($$, $3);
    }
  | polygon
    {
      /* Initialize an array of zone shapes. */
      $$ = g_ptr_array_sized_new (nzones);
      g_ptr_array_add ($$, $1);
    }
  ;

polygon:
    DQUOTE POLYGON LPAREN contours RPAREN DQUOTE
    {
      $$ = $4;
    }
  | DQUOTE POLYGON LPAREN RPAREN DQUOTE
    {
      $$ = NULL;
    }
  | DQUOTE DQUOTE
    {
      $$ = NULL;
    }
  |
    {
      $$ = NULL;
    }
  ;

contours:
    contours contour
    {
      /* Merge the newest contour ($2, a gpc_polygon object) into the existing
       * polygon ($1, also a gpc_polygon object). */
      gpc_add_contour ($1, $2->contour, 0);

      /* Now that the newest contour has been merged in, delete all parts of
       * that gpc_polygon object except the vertex array. */
      g_free ($2->hole);
      g_free ($2);
      #if DEBUG
        g_debug ("polygon now has %u contours", $$->num_contours);
      #endif
    }
  | contour
    {
      $$ = $1;
      #if DEBUG
        g_debug ("polygon now has %u contours", $$->num_contours);
      #endif
    }
  ;

contour:
    LPAREN coords RPAREN
    {
      gpc_vertex_list *contour;
      gpc_polygon *poly;

      /* An array of gpc_vertex objects has been built at this point; it's
       * contained in a GArray ($2).  Link that array into the gpc_polygon
       * object we're creating, then discard the GArray wrapper struct. */
      contour = g_new (gpc_vertex_list, 1);
      /* In the WKT polygon format, the first and last points are the same
       * (for closed polygons).  The gpc_polygon format doesn't need to look at
       * that repeated point, but the Shapefile format does, so we leave it
       * alone. */
      contour->num_vertices = $2->len;
      contour->vertex = (gpc_vertex *) ($2->data);
      g_array_free ($2, FALSE);

      poly = g_new (gpc_polygon, 1);
      poly->num_contours = 1;
      poly->contour = contour;
      poly->hole = g_new0 (int, 1);

      $$ = poly;
    }
  ;

coords:
    coords COMMA coord
    {
      $$ = $1;
      g_array_append_val ($$, $3);
    }
  | coord
    {
      $$ = g_array_new (FALSE, FALSE, sizeof (gpc_vertex));
      g_array_append_val ($$, $1);
    }
  ;

coord:
    FLOAT FLOAT
    {
      $$.x = $1;
      $$.y = $2;
    }
  | FLOAT INT
    {
      $$.x = $1;
      $$.y = $2;
    }
  | INT FLOAT
    {
      $$.x = $1;
      $$.y = $2;
    }
  | INT INT
    {
      $$.x = $1;
      $$.y = $2;
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
    {
      g_error ("Need the base name of ArcView shape files to write.");
    }

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
  if (g_str_has_suffix (arcview_shp_filename, ".shp"))
    {
      arcview_base_name = g_strndup (arcview_shp_filename,
                                     strlen(arcview_shp_filename) - 4);
    }
  else
    {
      arcview_base_name = g_strdup (arcview_shp_filename);
    }
  g_option_context_free (context);

  #if DEBUG
    g_debug ("base part of ArcView file name = \"%s\"", arcview_base_name);
  #endif  

  nzones = 0;
  zone_names = g_ptr_array_new ();
  max_zone_name_length = 0;
  done = FALSE;
  last_day_zones = NULL;

  /* Call the parser. */
  if (yyin == NULL)
    yyin = stdin;
  while (!feof(yyin) && !done)
    yyparse();

  /* We want ArcView files for the final day.  If the final day was 1 plus a
   * multiple of 7, then the files have already been made.  If not, make
   * them. */
  if (last_day % 7 != 1 && nzones > 0)
    make_arcview (last_day_zones, last_day);

  /* Clean up. */
  g_free (arcview_base_name);
  if (last_day_zones != NULL)
    {
      g_ptr_array_foreach (last_day_zones, gpc_free_polygon_as_GFunc, NULL);
      g_ptr_array_free (last_day_zones, TRUE);
    }
  g_ptr_array_foreach (zone_names, g_string_free_as_GFunc, NULL);
  g_ptr_array_free (zone_names, TRUE);

  return EXIT_SUCCESS;
}

/* end of file weekly_gis_zones.y */
