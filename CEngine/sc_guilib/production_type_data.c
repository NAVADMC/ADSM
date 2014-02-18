/** @file production_type_data.c
 * Functions for creating, destroying, printing, and manipulating production types.
 *
 * @author Shaun Case <shaun.case@colostate.edu><br>
 *   Animal Population Health Institute<br>
 *   Department of Clinical Sciences, Colorado State University.<br>
 *   Fort Collins, Colorado  80524<br>
 *   USA
 * @version 0.1
 * @date February 2009
 *
 * Copyright &copy; Colorado State University and University of Guelph, Canada, 2003-2009
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 *
 */
#if HAVE_CONFIG_H
#  include <config.h>
#endif

#ifdef USE_SC_GUILIB
#include <unistd.h>
#include <stdio.h>
#include <expat.h>
/* Expat 1.95 has this constant on my Debian system, but not on Hammerhead's
 * Red Hat system.  ?? */
#ifndef XML_STATUS_ERROR
#  define XML_STATUS_ERROR 0
#endif
#include <time.h>

#if STDC_HEADERS
#  include <stdlib.h>
#  include <string.h>
#endif

#if HAVE_STRINGS_H
#  include <strings.h>
#endif

#if HAVE_CTYPE_H
#  include <ctype.h>
#endif

#if HAVE_MATH_H
#  include <math.h>
#endif

#if HAVE_ERRNO_H
#  include <errno.h>
#endif

#include <general.h>
#include <production_type_data.h>

/**
 * Character data handler for an Expat herd file parser.  Accumulates the
 * complete text for an XML element (which may come in pieces).
 *
 * @param userData a pointer to a PRT_partial_production_type_list_t structure, cast to a
 *   void pointer.
 * @param s complete or partial character data from an XML element.
 * @param len the length of the character data.
 */
static void
charDataPRT (void *userData, const XML_Char * s, int len)
{
  PRT_partial_production_type_list_t *partial;

  partial = (PRT_partial_production_type_list_t *) userData;
  g_string_append_len (partial->s, s, len);
}

/**
 * Start element handler for an Expat herd file parser.  Creates a new production_type
 * when it encounters a \<production-type\> tag.
 *
 * @param userData a pointer to a PRT_partial_production_type_list_t structure, cast to a
 *   void pointer.
 * @param name the tag's name.
 * @param atts the tag's attributes.
 */
static void
startPRTElement (void *userData, const char *name, const char **atts)
{
  PRT_partial_production_type_list_t *partial;

#if DEBUG
  g_debug ("encountered start tag for \"%s\"", name);
#endif

  partial = (PRT_partial_production_type_list_t *) userData;
  if (strcmp (name, "production-type") == 0)
    partial->production_type = PRT_new_production_type_t (NULL, 0);
}

/**
 * End element handler for an Expat production_type file parser.
 *
 * When it encounters an \</id\>, or \</name\> tag, it fills in the
 * corresponding field in the herd most recently created by startPRTElement and
 * clears the character data buffer.  This function issues a warning and fills
 * in a reasonable default value when fields are missing or invalid.
 *
 * When it encounters a \</production-type\> tag, it adds the just-completed production_type to the
 * production_type list.
 *
 * @param userData a pointer to a PRT_partial_production_type_list_t structure, cast to a
 *   void pointer.
 * @param name the tag's name.
 */
static void
endPRTElement (void *userData, const char *name)
{
  PRT_partial_production_type_list_t *partial;
  char *filename;
  XML_Parser parser;

#if DEBUG
  g_debug ("encountered end tag for \"%s\"", name);
#endif

  partial = (PRT_partial_production_type_list_t *) userData;
  filename = partial->filename;
  parser = partial->parser;

  /* id tag */

  if (strcmp (name, "id") == 0)
    {
      char *tmp;
      char *tId;
      tmp = g_strdup (partial->s->str);
      g_strstrip (tmp);
#if DEBUG
      g_debug ("  accumulated string (Expat encoding) = \"%s\"", tmp);
#endif
      /* Expat stores the text as UTF-8.  Convert to ISO-8859-1. */
      tId = g_convert_with_fallback (tmp, -1, "ISO-8859-1", "UTF-8", "?", NULL, NULL, NULL);
      g_assert ( tId != NULL );

      partial->production_type->id = atoi( tId );
      g_free ( tId );
      g_free (tmp);
      g_string_truncate (partial->s, 0);
    }

  /* name tag */
  else if (strcmp (name, "name") == 0)
    {
      char *tmp;
      tmp = g_strdup (partial->s->str);
      g_strstrip (tmp);
#if DEBUG
      g_debug ("  accumulated string (Expat encoding) = \"%s\"", tmp);
#endif
      /* Expat stores the text as UTF-8.  Convert to ISO-8859-1. */
      partial->production_type->name = g_convert_with_fallback (tmp, -1, "ISO-8859-1", "UTF-8", "?", NULL, NULL, NULL);
      g_assert ( partial->production_type->name  != NULL);
      g_free (tmp);
      g_string_truncate (partial->s, 0);
    }

  /* production-type tag :  We're done with this production type */

  else if (strcmp (name, "production-type") == 0)
    {
      g_ptr_array_add( partial->production_types, partial->production_type );
    }
  else if ( strcmp( name, "scenario-id" ) == 0 )
    {
      char *tmp;
      tmp = g_strdup (partial->s->str);
      g_strstrip (tmp);
#if DEBUG
      g_debug ("  accumulated string (Expat encoding) = \"%s\"", tmp);
#endif

      _scenario.scenarioId = g_convert_with_fallback (tmp, -1, "ISO-8859-1", "UTF-8", "?", NULL, NULL, NULL);
      g_assert ( _scenario.scenarioId  != NULL);
      g_free (tmp);
      g_string_truncate (partial->s, 0);
    }
  else if (strcmp (name, "random-seed") == 0)
    {
      char *tmp;
      char *tId;
      tmp = g_strdup (partial->s->str);
      g_strstrip (tmp);
#if DEBUG
      g_debug ("  accumulated string (Expat encoding) = \"%s\"", tmp);
#endif
      /* Expat stores the text as UTF-8.  Convert to ISO-8859-1. */
      tId = g_convert_with_fallback (tmp, -1, "ISO-8859-1", "UTF-8", "?", NULL, NULL, NULL);
      g_assert ( tId != NULL );

      _scenario.random_seed = atol( tId );
      g_free ( tId );
      g_free (tmp);
      g_string_truncate (partial->s, 0);
    }
}

GPtrArray *PRT_load_production_type_list ( char *production_type_file )
{
  FILE *fp;
  GPtrArray *ret_val;
  ret_val = NULL;

#if DEBUG
  g_debug ("----- ENTER PRT_load_production_type_list");
#endif

  fp = fopen (production_type_file, "r");
  if (fp == NULL)
  {
      g_error ("could not open file \"%s\": %s", production_type_file, strerror (errno));
  }
  else
  {
    ret_val = PRT_load_production_type_list_from_stream (fp, production_type_file);
    fclose (fp);
  };
#if DEBUG
  g_debug ("----- EXIT PRT_load_production_type_list");
#endif
  return ret_val;
}

GPtrArray *PRT_load_production_type_list_from_stream (FILE *stream, const char *filename)
{
  GPtrArray *production_types;
  PRT_partial_production_type_list_t to_pass;
  XML_Parser parser;            /* to read the file */
  int xmlerr;
  char *linebuf = NULL;
  size_t bufsize = 0;
  ssize_t linelen;

#if DEBUG
  g_debug ("----- ENTER PRT_load_production_type_list_from_stream");
#endif

  if (stream == NULL)
    stream = stdin;
  if (filename == NULL)
    filename = "input";

  production_types = g_ptr_array_new();

  parser = XML_ParserCreate (NULL);
  if (parser == NULL)
    {
      g_warning ("failed to create parser for reading file of units");
      goto end;
    }

  to_pass.production_types = production_types;
  to_pass.production_type = NULL;
  to_pass.s = g_string_new (NULL);
  to_pass.filename = g_strdup( filename );
  to_pass.parser = parser;

  XML_SetUserData (parser, &to_pass);
  XML_SetElementHandler (parser, startPRTElement, endPRTElement);
  XML_SetCharacterDataHandler (parser, charDataPRT);

  while (1)
    {
      linelen = getline (&linebuf, &bufsize, stream);
      if (linelen == -1)
        {
          xmlerr = XML_Parse (parser, NULL, 0, 1);
          if (xmlerr == XML_STATUS_ERROR)
            {
              g_error ("%s at line %d in %s",
                       XML_ErrorString (XML_GetErrorCode (parser)),
                       XML_GetCurrentLineNumber (parser), filename);
            }
          break;
        }
      xmlerr = XML_Parse (parser, linebuf, linelen, 0);
      if (xmlerr == XML_STATUS_ERROR)
        {
          g_error ("%s at line %d in %s",
                   XML_ErrorString (XML_GetErrorCode (parser)),
                   XML_GetCurrentLineNumber (parser), filename);
        }
    }

  /* Clean up. */
  XML_ParserFree (parser);
  g_string_free (to_pass.s, TRUE);
  free (linebuf);

end:
#if DEBUG
  g_debug ("----- EXIT PRT_load_production_type_list_from_stream");
#endif
  return production_types;
}

void PRT_free_production_type_list ( GPtrArray *production_type_list )
{
  int i;
  PRT_production_type_data_t *p_data;

  if ( production_type_list != NULL )
  {
    for( i = 0; i < production_type_list->len; i++ )
    {
      p_data = (PRT_production_type_data_t*)(g_ptr_array_index (production_type_list, i ));
      if ( p_data != NULL )
      {
        g_free( p_data->name );
        g_free( p_data );
      };
    };
    g_ptr_array_free( production_type_list, TRUE );
  };
}

PRT_production_type_data_t *PRT_new_production_type_t( char *_name, int _id )
{
  PRT_production_type_data_t *ret_val = NULL;

  /*if ( ( _name != NULL ) && ( _id > 0 ) )*/
  {
/*    if ( strlen( _name ) > 0 )*/
    {
      if ( (ret_val = g_new (PRT_production_type_data_t, 1)) != NULL )
      {
        CLEAR_PRT_SUMMARY_DATA( &(ret_val->data) );
        CLEAR_PRT_DAILY_DATA( &(ret_val->d_data) );
        ret_val->data.firstDetection = -1;
        ret_val->data.firstDestruction = -1;
        ret_val->data.firstVaccination = -1;
        ret_val->name = _name;
        ret_val->id = _id;
      };
    };
  };

  return ret_val;
}

void clear_production_type_list_data( GPtrArray *_production_type_list )
{
  int i;
  PRT_production_type_data_t *p_data;
#if DEBUG
  g_debug ("----- ENTER clear_production_type_list_data");
#endif
  if ( _production_type_list != NULL )
  {
    for( i = 0; i < _production_type_list->len; i++ )
    {
      p_data = (PRT_production_type_data_t*)(g_ptr_array_index (_production_type_list, i ));
      if ( p_data != NULL )
      {
        CLEAR_PRT_SUMMARY_DATA( &(p_data->data) );
        CLEAR_PRT_DAILY_DATA( &(p_data->d_data) );
        p_data->data.firstDetection = -1;
        p_data->data.firstDestruction = -1;
        p_data->data.firstVaccination = -1;
      };
    };
  };
#if DEBUG
  g_debug ("----- EXIT clear_production_type_list_data");
#endif
}
#endif
/*  End of File: production_type_data.c */
