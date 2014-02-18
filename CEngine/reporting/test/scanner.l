%{
#if HAVE_CONFIG_H
#  include <config.h>
#endif

#include <reporting.h>
#include <glib.h>
#include "shell.h"

#if STDC_HEADERS
#  include <string.h>
#elif HAVE_STRINGS_H
#  include <strings.h>
#endif

/** @file reporting/test/scanner.c
 * A scanner for a simple shell to exercise libreporting.
 *
 * @author Neil Harvey <neilharvey@gmail.com><br>
 *   Grid Computing Research Group<br>
 *   Department of Computing & Information Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @version 0.1
 * @date August 2004
 *
 * Copyright &copy; University of Guelph, 2004-2007
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
#define BUFFERSIZE 32768
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
  "variable"                { ADJUST; return VARIABLE; }
  "set"                     { ADJUST; return SET; }
  "add"                     { ADJUST; return ADD; }
  "subtract"                { ADJUST; return SUBTRACT; }
  "get"                     { ADJUST; return GET; }
  "daily"                   { ADJUST; return DAILY; }
  "t" {
    ADJUST;
    yylval.bval = TRUE;
    return BOOL;
  }
  "f" {
    ADJUST;
    yylval.bval = FALSE;
    return BOOL;
  }
  [+-]?[[:digit:]]+(\.[[:digit:]]+)([eE][+-][[:digit:]]+)? {
    ADJUST;
    yylval.fval = (double)atof(yytext);
    return REAL;
  }
  [+-]?[[:digit:]]+ {
    ADJUST;
    yylval.ival = (int)atoi(yytext);
    return INT;
  }
  \"[a-zA-Z_][a-zA-Z0-9_. ]*\" {
    ADJUST;
    yylval.sval = g_strndup (yytext+1, yyleng-2);
    return STRING;
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
