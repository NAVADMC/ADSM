%{
#if HAVE_CONFIG_H
#  include <config.h>
#endif

#include "reporting.h"
#include "table.h"

#if STDC_HEADERS
#  include <string.h>
#elif HAVE_STRINGS_H
#  include <strings.h>
#endif

/** @file filters/scanner.c
 * A scanner for SHARCSpread output.
 *
 * @author Neil Harvey <neilharvey@gmail.com><br>
 *   Grid Computing Research Group<br>
 *   Department of Computing & Information Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @version 0.1
 * @date May 2004
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
#define BUFFERSIZE 1048576
#define ADJUST (tokenpos = charpos, charpos += yyleng)

int yyerror (char *s, int fatal);

char linebuf[BUFFERSIZE];
int charpos = 0, tokenpos = 0;
%}
%option yylineno
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
    return NEWLINE;
  }
  \t {
    tokenpos = charpos;
    charpos += TABWIDTH;
  }
  ,                         { ADJUST; return COMMA; }
  :                         { ADJUST; return COLON; }
  =                         { ADJUST; return EQ; }
  "{"                       { ADJUST; return LBRACE; }
  "}"                       { ADJUST; return RBRACE; }
  "("                       { ADJUST; return LPAREN; }
  ")"                       { ADJUST; return RPAREN; }
  "\""                      { ADJUST; return DQUOTE; }
  "node"                    { ADJUST; return NODE; }
  "run"                     { ADJUST; return RUN; }
  "day"                     { ADJUST; return DAY; }
  "polygon"                 { ADJUST; return POLYGON; }
  [A-Za-z][A-Za-z0-9_-]* {
    ADJUST;
    yylval.sval = g_strdup (yytext);
    return VARNAME;
  }
  [+-]?[[:digit:]]+((\.[[:digit:]]+)|([eE][+-][[:digit:]]+)|(\.[[:digit:]]+[eE][+-][[:digit:]]+)) {
    ADJUST;
    yylval.fval = (double)atof(yytext);
    return FLOAT;
  }
  [+-]?[[:digit:]]+ {
    ADJUST;
    yylval.ival = (int)atoi(yytext);
    return INT;
  }
  ('[^']*')+ {
    ADJUST;
    yylval.sval = g_strndup (yytext+1, yyleng-2);
    return STRING;  
  }
  \n {
    charpos = 0;
    tokenpos = 0;
    return NEWLINE;
  }
  [[:space:]] { /* Ignore whitespace */ }
  . {
    /* Report an unrecognized token. */
    yyerror ("Unrecognized token", 1);
  }
  <<EOF>> {
    BEGIN(INITIAL);
    charpos = 0, tokenpos = 0;
    yyterminate();
  }
}
%%
