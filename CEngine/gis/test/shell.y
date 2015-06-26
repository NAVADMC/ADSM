%{
#if HAVE_CONFIG_H
#  include <config.h>
#endif

#if HAVE_STDLIB_H
#  include <stdlib.h>
#endif

#include <gis.h>
#include <glib.h>
#include <stdio.h>

#define PROMPT "> "

/** @file gis/test/shell.c
 * A simple shell to exercise libgis.  It provides a way to call the functions
 * offered by the <a href="gis_8h.html">GIS library</a>, so that a suite of
 * tests can be scripted.
 *
 * The commands are:
 * <ul>
 *   <li>
 *     <code>great circle distance (lat1, lon1, lat2, lon2)</code>
 *
 *     Returns the great-circle distance in km between two points.  The
 *     arguments are given in degrees.
 *   <li>
 *     <code>distance (x1, y1, x2, y2)</code>
 *
 *     Returns the distance in km between two points.  The arguments are given
 *     on a km grid.
 *   <li>
 *     <code>great circle heading (lat1, lon1, lat2, lon2)</code>
 *
 *     Returns the initial heading in degrees from point 1 to point 2.  The
 *     arguments are given in degrees.
 *   <li>
 *     <code>heading (x1, y1, x2, y2)</code>
 *
 *     Returns the heading in degrees from point 1 to point 2.  The arguments
 *     are given on a km grid.
 *   <li>
 *     <code>area (x1,y1,x2,y2,...)</code>
 *
 *     Returns the area of a polygon.  The initial point does not have to be
 *     repeated as the final point.  Inputs with zero, one, or two points are
 *     allowed, in which case the area should be 0.
 *   <li>
 *     <code>perimeter (x1,y1,x2,y2,...)</code>
 *
 *     Returns the perimeter of a polygon.  The initial point does not have to
 *     be repeated as the final point.  Inputs with zero, one, or two points
 *     are allowed, in which case the perimeter should be 0.
 *   <li>
 *     <code>point in polygon (x,y,x1,y1,x2,y2,...)</code>
 *
 *     Finds whether the point x,y is inside the polygon whose vertices are
 *     defined by x1,y2,...,xn,yn.  For the polygon, the initial point does not
 *     have to be repeated as the final point.  The output is 't' or 'f'.
 * </ul>
 *
 * The shell exits on EOF (Ctrl+D if you're typing commands into it
 * interactively in Unix).
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @version 0.1
 * @date January 2004
 *
 * Copyright &copy; University of Guelph, 2004-2009
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

void g_free_as_GFunc (gpointer data, gpointer user_data);
%}

%union {
  double fval;
  GSList *lval;
}

%token DISTANCE HEADING AREA PERIMETER GREATCIRCLE POINTINPOLYGON
%token LPAREN RPAREN COMMA
%token <fval> NUM
%type <lval> num_list

%%

commands :
    command commands
  | command
  ;

command :
    function_call
  ;

function_call :
    GREATCIRCLE DISTANCE LPAREN NUM COMMA NUM COMMA NUM COMMA NUM RPAREN
    {
      printf ("%g\n%s", GIS_great_circle_distance ($4, $6, $8, $10), PROMPT);
      fflush (stdout);
    }
  | DISTANCE LPAREN NUM COMMA NUM COMMA NUM COMMA NUM RPAREN
    {
      printf ("%g\n%s", GIS_distance ($3, $5, $7, $9), PROMPT);
      fflush (stdout);
    }
  | GREATCIRCLE HEADING LPAREN NUM COMMA NUM COMMA NUM COMMA NUM RPAREN
    {
      printf ("%g\n%s", GIS_great_circle_heading ($4, $6, $8, $10), PROMPT);
      fflush (stdout);
    }
  | HEADING LPAREN NUM COMMA NUM COMMA NUM COMMA NUM RPAREN
    {
      printf ("%g\n%s", GIS_heading ($3, $5, $7, $9), PROMPT);
      fflush (stdout);
    }
  | AREA LPAREN RPAREN
    {
      gpc_polygon * poly;
      double area;

      poly = gpc_new_polygon (); /* starts with no contours */
      area = GIS_polygon_area (poly);
      gpc_free_polygon (poly);
      printf ("%g\n%s", area, PROMPT);
      fflush (stdout);
    }
  | AREA LPAREN num_list RPAREN
    {
      gpc_polygon * poly;
      double area;
      int len;
      int n;
      gpc_vertex_list *contour;
      gpc_vertex *v;
      GSList *iter;

      /* Initialize a polygon. */
      poly = gpc_new_polygon ();

      len = g_slist_length ($3);
      if (len % 2 != 0)
        {
          g_warning ("number of arguments must be even");
        }
      else
        {
          /* Copy the points into a gpc_contour structure. */
          n = len / 2;
          contour = g_new (gpc_vertex_list, 1);
          contour->num_vertices = n;
          contour->vertex = g_new (gpc_vertex, n);
          /* iter will point to the current node in the GSList of doubles; v
           * will point to the current vertex. */
          v = contour->vertex;
          for (iter = $3; iter != NULL; )
            {
              v->x = *((double *)(iter->data));
              iter = g_slist_next (iter);
              v->y = *((double *)(iter->data));
              iter = g_slist_next (iter);
              v++;
            }
          /* Now merge the (single) contour into a polygon object. */
          gpc_add_contour (poly, contour, 0);
        }
      g_slist_foreach ($3, g_free_as_GFunc, NULL);
      g_slist_free ($3);

      area = GIS_polygon_area (poly);
      gpc_free_polygon (poly);
      printf ("%g\n%s", area, PROMPT);
      fflush (stdout);
    }
  | PERIMETER LPAREN RPAREN
    {
      gpc_polygon * poly;
      double perimeter;

      poly = gpc_new_polygon (); /* starts with no contours */
      perimeter = GIS_polygon_perimeter (poly);
      gpc_free_polygon (poly);
      printf ("%g\n%s", perimeter, PROMPT);
      fflush (stdout);
    }
  | PERIMETER LPAREN num_list RPAREN
    {
      gpc_polygon * poly;
      double perimeter;
      int len;
      int n;
      gpc_vertex_list *contour;
      gpc_vertex *v;
      GSList *iter;

      /* Initialize a polygon. */
      poly = gpc_new_polygon ();

      len = g_slist_length ($3);
      if (len % 2 != 0)
        {
          g_warning ("number of arguments must be even");
        }
      else
        {
          /* Copy the points into a gpc_contour structure. */
          n = len / 2;
          contour = g_new (gpc_vertex_list, 1);
          contour->num_vertices = n;
          contour->vertex = g_new (gpc_vertex, n);
          /* iter will point to the current node in the GSList of doubles; v
           * will point to the current vertex. */
          v = contour->vertex;
          for (iter = $3; iter != NULL; )
            {
              v->x = *((double *)(iter->data));
              iter = g_slist_next (iter);
              v->y = *((double *)(iter->data));
              iter = g_slist_next (iter);
              v++;
            }
          /* Now merge the (single) contour into a polygon object. */
          gpc_add_contour (poly, contour, 0);
        }
      g_slist_foreach ($3, g_free_as_GFunc, NULL);
      g_slist_free ($3);

      perimeter = GIS_polygon_perimeter (poly);
      gpc_free_polygon (poly);
      printf ("%g\n%s", perimeter, PROMPT);
      fflush (stdout);
    }
  | POINTINPOLYGON LPAREN num_list RPAREN
    {
      gpc_polygon * poly;
      double x = 0,y = 0;
      gboolean inside;
      int len;
      int n;
      gpc_vertex_list *contour;
      gpc_vertex *v;
      GSList *iter;

      /* Initialize a polygon. */
      poly = gpc_new_polygon ();

      len = g_slist_length ($3);
      if (len < 2 || len % 2 != 0)
        {
          g_warning ("must have at least 2 arguments, and number of arguments must be even");
        }
      else
        {
          /* Copy the first point as the point to test. */
          iter = $3;
          x = *((double *)(iter->data));
          iter = g_slist_next (iter);
          y = *((double *)(iter->data));
          iter = g_slist_next (iter);
          /* Copy the remaining points into a gpc_contour structure. */
          n = (len - 2) / 2;
          contour = g_new (gpc_vertex_list, 1);
          contour->num_vertices = n;
          contour->vertex = g_new (gpc_vertex, n);
          /* iter will point to the current node in the GSList of doubles; v
           * will point to the current vertex. */
          v = contour->vertex;
          for (; iter != NULL; )
            {
              v->x = *((double *)(iter->data));
              iter = g_slist_next (iter);
              v->y = *((double *)(iter->data));
              iter = g_slist_next (iter);
              v++;
            }
          /* Now merge the (single) contour into a polygon object. */
          gpc_add_contour (poly, contour, 0);
        }
      g_slist_foreach ($3, g_free_as_GFunc, NULL);
      g_slist_free ($3);

      inside = GIS_point_in_polygon (poly, x, y);
      gpc_free_polygon (poly);
      printf (inside ? "t" : "f");
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
 * A log handler that simply discards messages.
 */
void
silent_log_handler (const gchar * log_domain, GLogLevelFlags log_level,
                    const gchar * message, gpointer user_data)
{
  ;
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



int
main (int argc, char *argv[])
{
  g_log_set_handler ("gis", G_LOG_LEVEL_MESSAGE | G_LOG_LEVEL_INFO | G_LOG_LEVEL_DEBUG, silent_log_handler, NULL);

  printf (PROMPT);
  if (yyin == NULL)
    yyin = stdin;
  while (!feof(yyin))
    yyparse();

  return EXIT_SUCCESS;
}

/* end of file shell.y */
