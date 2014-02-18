%{
#if HAVE_CONFIG_H
#  include <config.h>
#endif

#include <glib.h>
#include "shell.h"

#if STDC_HEADERS
#  include <string.h>
#elif HAVE_STRINGS_H
#  include <strings.h>
#endif

/** @file gis/test/scanner.c
 * A scanner for a simple shell to exercise libgis.
 *
 * @author Neil Harvey <neilharvey@gmail.com><br>
 *   Grid Computing Research Group<br>
 *   Department of Computing & Information Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @version 0.1
 * @date January 2004
 *
 * Copyright &copy; University of Guelph, 2004-2008
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 *
 * @todo Check for overflow in string-to-int and string-to-float conversions.
 *
 */
#define TABWIDTH 8
#define BUFFERSIZE 2048
#define ADJUST (tokenpos = charpos, charpos += yyleng)

#ifdef USE_PLAIN_YACC
int yyerror (char *s);
#else
int yyerror (char *s, int fatal);
#endif

char linebuf[BUFFERSIZE];
int charpos = 0, tokenpos = 0;
%}
%option case-insensitive
%option noyywrap
%x PASTFIRSTLINE
%%
.*	{
  /* Copy a line of input to a buffer, then "put it back" for processing by
   * lex.  This allows us to print pretty error messages showing the entire
   * current line of input. */
  strncpy (linebuf, yytext, BUFFERSIZE);
  /* If the input line didn't fit in the buffer, null-terminate it. */
  linebuf[BUFFERSIZE-1] = '\0';
  yyless(0);
  BEGIN(PASTFIRSTLINE);
}
<PASTFIRSTLINE>{
  \n.* {
    /* Copy a line of input to a buffer (see comment above). */
    strncpy (linebuf, yytext+1, BUFFERSIZE);
    /* If the input line didn't fit in the buffer, null-terminate it. */
    linebuf[BUFFERSIZE-1] = '\0';
    yyless(1);
    charpos = 0;
    tokenpos = 0;
  }
  \t {
    tokenpos = charpos;
    charpos += TABWIDTH;
  }
  ","                       { ADJUST; return COMMA; }
  "("                       { ADJUST; return LPAREN; }
  ")"                       { ADJUST; return RPAREN; }
  dist(ance?)               { ADJUST; return DISTANCE; }
  "heading"                 { ADJUST; return HEADING; }
  "area"                    { ADJUST; return AREA; }
  "perimeter"               { ADJUST; return PERIMETER; }
  "great circle"            { ADJUST; return GREATCIRCLE; }
  "point in polygon"        { ADJUST; return POINTINPOLYGON; }
  [+-]?[[:digit:]]+(\.[[:digit:]]+)?([eE][+-][[:digit:]]+)? {
    ADJUST;
    yylval.fval = (double)atof(yytext);
    return NUM;
  }
  \n {
    charpos = 0;
    tokenpos = 0;
  }
  [[:space:]] { /* Ignore whitespace */ }
  . {
    /* Report an unrecognized token. */
#ifdef USE_PLAIN_YACC 
    yyerror ("Unrecognized token");
#else
    yyerror ("Unrecognized token", 1);
#endif
  }
}
%%
