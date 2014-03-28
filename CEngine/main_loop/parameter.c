/** @file parameter.c
 * Functions for retrieving simulation control parameters.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date March 2003
 *
 * Copyright &copy; University of Guelph, 2003-2009
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#ifdef HAVE_CONFIG_H
#  include <config.h>
#endif

#include "parameter.h"
#include <glib.h>

#if STDC_HEADERS
#  include <stdlib.h>
#endif

#if HAVE_STRING_H
#  include <string.h>
#endif

#if HAVE_ERRNO_H
#  include <errno.h>
#endif



/**
 * Retrieves a value for a real-valued parameter.
 *
 * Side effect: upon return, the location indicated by <i>success</i> contains
 * FALSE if the parameter was missing, out of range, or otherwise invalid, and
 * TRUE otherwise.
 *
 * @param param a real-valued parameter.
 * @param success a location in which to store a success or failure flag.
 * @return the parameter value.  If the conversion did not succeed, this value
 *   is undefined.
 */
double
PAR_get_real (PAR_parameter_t * param, gboolean * success)
{
  scew_element *e;
  double x = 0;
  const char *text;
  char *endptr;

  e = scew_element_by_name (param, "value");
  if (e)
    {
      text = scew_element_contents (e);
      x = strtod (text, &endptr);
      *success = !(text[0] == '\0' || errno == ERANGE || endptr == text);
    }
  else
    {
      g_warning ("parameter %s is missing a \"value\" element", scew_element_name (param));
      *success = FALSE;
    }
  return x;
}



/**
 * Retrieves a length value.
 *
 * Side effect: upon return, the location indicated by <i>success</i> contains
 * FALSE if the parameter was missing, out of range, or otherwise invalid, and
 * TRUE otherwise.
 *
 * @param param a length parameter.
 * @param success a location in which to store a success or failure flag.
 * @return the length.  If the conversion did not succeed, this value is
 *   undefined.
 */
double
PAR_get_length (PAR_parameter_t * param, gboolean * success)
{
  double x;

#if DEBUG
  g_debug ("----- ENTER PAR_get_length");
#endif

  x = PAR_get_real (param, success);
  if (*success == FALSE)
    g_warning ("missing or invalid length parameter");

#if DEBUG
  g_debug ("----- EXIT PAR_get_length");
#endif

  return x;
}



/**
 * Retrieves a time value.
 *
 * Side effect: upon return, the location indicated by <i>success</i> contains
 * FALSE if the parameter was missing, out of range, or otherwise invalid, and
 * TRUE otherwise.
 *
 * @param param a time parameter.
 * @param success a location in which to store a success or failure flag.
 * @return the time.  If the conversion did not succeed, this value is
 *   undefined.
 */
double
PAR_get_time (PAR_parameter_t * param, gboolean * success)
{
  double x;

#if DEBUG
  g_debug ("----- ENTER PAR_get_time");
#endif

  x = PAR_get_real (param, success);
  if (*success == FALSE)
    g_warning ("missing or invalid time parameter");

#if DEBUG
  g_debug ("----- EXIT PAR_get_time");
#endif

  return x;
}



/**
 * Retrieves an angle value.
 *
 * Side effect: upon return, the location indicated by <i>success</i> contains
 * FALSE if the parameter was missing, out of range, or otherwise invalid, and
 * TRUE otherwise.
 *
 * @param param an angle parameter.
 * @param success a location in which to store a success or failure flag.
 * @return the angle, in radians.  If the conversion did not succeed, this
 *   value is undefined.
 */
double
PAR_get_angle (PAR_parameter_t * param, gboolean * success)
{
  double x;

#if DEBUG
  g_debug ("----- ENTER PAR_get_angle");
#endif

  x = PAR_get_real (param, success);
  if (*success == FALSE)
    g_warning ("missing or invalid angle parameter");

#if DEBUG
  g_debug ("----- EXIT PAR_get_angle");
#endif

  return x;
}



/**
 * Retrieves a frequency value.
 *
 * Side effect: upon return, the location indicated by <i>success</i> contains
 * FALSE if the parameter was missing, out of range, or otherwise invalid, and
 * TRUE otherwise.
 *
 * @param param a frequency parameter.
 * @param success a location in which to store a success or failure flag.
 * @return the frequency.  If the conversion did not succeed, this value is
 *   undefined.
 */
double
PAR_get_frequency (PAR_parameter_t * param, gboolean * success)
{
  double x;

#if DEBUG
  g_debug ("----- ENTER PAR_get_frequency");
#endif

  x = PAR_get_real (param, success);
  if (*success == FALSE)
    g_warning ("missing or invalid frequency parameter");

#if DEBUG
  g_debug ("----- EXIT PAR_get_frequency");
#endif

  return x;
}



/**
 * Retrieves a probability value.
 *
 * Side effect: upon return, the location indicated by <i>success</i> contains
 * FALSE if the parameter was missing, out of range, or otherwise invalid, and
 * TRUE otherwise.
 *
 * @param param a probability parameter.
 * @param success a location in which to store a success or failure flag.
 * @return the probability in [0,1].  If the conversion did not succeed, this
 *   value is undefined.
 */
double
PAR_get_probability (PAR_parameter_t * param, gboolean * success)
{
  double x;
  const char *text;
  char *endptr;

#if DEBUG
  g_debug ("----- ENTER PAR_get_probability");
#endif

  text = scew_element_contents (param);
  x = strtod (text, &endptr);
  *success = !(text[0] == '\0' || errno == ERANGE || endptr == text || x < 0 || x > 1);
  if (*success == FALSE)
    g_warning ("missing or invalid probability parameter");

#if DEBUG
  g_debug ("----- EXIT PAR_get_probability");
#endif

  return x;
}



/**
 * Retrieves a money or cost value.
 *
 * Side effect: upon return, the location indicated by <i>success</i> contains
 * FALSE if the parameter was missing, out of range, or otherwise invalid, and
 * TRUE otherwise.
 *
 * @param param a money parameter.
 * @param success a location in which to store a success or failure flag.
 * @return the amount.  If the conversion did not succeed, this value is
 *   undefined.
 */
double
PAR_get_money (PAR_parameter_t * param, gboolean * success)
{
  double x;

#if DEBUG
  g_debug ("----- ENTER PAR_get_money");
#endif

  x = PAR_get_real (param, success);
  if (*success == FALSE)
    g_warning ("missing or invalid money parameter");

#if DEBUG
  g_debug ("----- EXIT PAR_get_money");
#endif

  return x;
}



/**
 * Retrieves a piecewise probability density function.
 *
 * @param fn_element a piecewise probability distribution function parameter.
 * @return a probability distribution function object.
 */
PDF_dist_t *
PAR_get_piecewise_PDF( scew_element* const fn_element ) 
{
  PDF_dist_t *dist;
  gboolean old_style_xml, new_style_xml;
  unsigned int i, j;
  unsigned int element_count;
  scew_element* e;
  double x, y, *xy;
  unsigned int npoints;
  scew_list *ee;
  scew_list *iter;
  scew_element *ve, *xe, *ye;
  gboolean had_error;
                      
  dist = NULL;
  
  /* Determine whether we're dealing with new- or old-style XML. 
     Depending on what we find, one of two possible parsing approaches will
     be used below.
  */
  old_style_xml = FALSE;
  new_style_xml = FALSE;
  npoints = 0;

  element_count = scew_element_count( fn_element ); 
  for( i = 0; i < element_count; ++i )
    {
      e = scew_element_by_index( fn_element, i );
      
      if( 0 == g_ascii_strcasecmp( "value", scew_element_name( e ) ) )
        {
          if( scew_element_by_name( e, "x" ) )
            {
              /* npoints will be used below by the new-style parsing function.  
                 It will be reset if necessary by the old-style parsing function.
              */
              ++npoints; 
              new_style_xml = TRUE;
            }
          else
            old_style_xml = TRUE;      
        }    
    } 

  if( new_style_xml && old_style_xml )
    {
      g_error( "Multiple XML schema versions seem to be mixed in PAR_get_piecewise_PDF()" );
      goto end;
    }
  else if( (!new_style_xml) && (!old_style_xml) )
    {   
      g_error( "XML schema version cannot be determined in PAR_get_piecewise_PDF()" );
      goto end;  
    }
  
  
  /* If we can tell which style we're parsing, then do it. */
  if( old_style_xml )
    {
      /* This is Neil's original piecewise parsing function. */    
      ee = scew_element_list_by_name (fn_element, "value");
      npoints = scew_list_size (ee);
      #if DEBUG
        g_debug ("%u points", npoints);
      #endif
      
      /* Copy the x,y values from the DOM tree into an array. */
      xy = g_new (double, 2 * npoints);
      
      errno = 0;
      for (i = 0, iter = ee; iter != NULL; i++, iter = scew_list_next(iter))
        {
          xe = (scew_element *) scew_list_data (iter);
          x = strtod (scew_element_contents (xe), NULL);
          g_assert (errno != ERANGE);
          xy[2 * i] = x;
        }
      scew_list_free (ee);
      ee = scew_element_list_by_name (fn_element, "p");
      npoints = scew_list_size (ee);
      for (i = 0, iter = ee; iter != NULL; i++, iter = scew_list_next(iter))
        {
          ye = (scew_element *) scew_list_data (iter);
          y = strtod (scew_element_contents (ye), NULL);
          g_assert (errno != ERANGE);
          xy[2 * i + 1] = y;
        }
      dist = PDF_new_piecewise_dist (npoints, xy);
      g_free (xy);
      scew_list_free (ee);
    }
  else /* if new-style xml */
    {
      /* This function is mostly translated from the Delphi code for parsing new-style piecewise PDFs. */      
      had_error = FALSE;
      xy = g_new (double, 2 * npoints);
      
      j = 0;
      errno = 0;
      for( i = 0; i < element_count; ++i )
        {
          ve = scew_element_by_index( fn_element, i );
          if( 0 == g_ascii_strcasecmp( "value", scew_element_name( ve ) ) )
            {
              xe = scew_element_by_name( ve, "x" );
              ye = scew_element_by_name( ve, "p" );
              
              if( xe )
                {
                  x = strtod( scew_element_contents( xe ), NULL ); 
                  g_assert (errno != ERANGE);
                  xy[2 * j] = x;
                }
              else
                {
                  had_error = TRUE;
                  break;
                }
                
              if( ye )
                {
                  y = strtod( scew_element_contents( ye ), NULL ); 
                  g_assert (errno != ERANGE);
                  xy[2 * j + 1] = y;
                }
              else
                {
                  had_error = TRUE;
                  break;
                } 
                                    
              ++j;
            }  
        }
 
      if( had_error )
        dist = NULL;
      else
        dist = PDF_new_piecewise_dist (npoints, xy);
        
      g_free (xy);    
    }
       
end:
    
  return dist; 
}


/**
 * Retrieves a histogram probability density function.
 *
 * @param fn_element a histogram probability distribution function parameter.
 * @return a probability distribution function object.
 */
PDF_dist_t *
PAR_get_histogram_PDF( scew_element* const fn_element )
{
  PDF_dist_t *dist;
  gboolean old_style_xml;
  unsigned int i, j;
  unsigned int nbins, nbins2;
  gsl_histogram *h;
  double *range; 

  /* Determine whether we're dealing with new- or old-style XML. 
     Depending on what we find, one of two possible parsing approaches will
     be used below.
     
     Only new-style XML has the tag <value> for histogram PDFs.
  */
  if( scew_element_by_name( fn_element, "value" ) )
    old_style_xml = FALSE;
  else
    old_style_xml = TRUE;


  if( old_style_xml ) 
    {
      scew_list *ee, *iter;
      scew_element *xe;
      double x;

      ee = scew_element_list_by_name (fn_element, "x0");
      nbins = scew_list_size (ee);
      #if DEBUG
        g_debug ("%u bins", nbins);
      #endif

      h = gsl_histogram_alloc (nbins);

      /* Copy the range values from the DOM tree into an array. */
      range = g_new (double, nbins + 1);
      errno = 0;
      for (i = 0, iter = ee; iter != NULL; i++, iter = scew_list_next(iter))
        {
          xe = (scew_element *) scew_list_data (iter);
          x = strtod (scew_element_contents (xe), NULL);
          g_assert (errno != ERANGE);
          range[i] = x;
        }
      scew_list_free (ee);
      /* Get the final upper bound of the histogram. */
      ee = scew_element_list_by_name (fn_element, "x1");
      nbins2 = scew_list_size (ee);
      g_assert (nbins2 == nbins);
      xe = (scew_element *) scew_list_data (scew_list_last (ee));
      x = strtod (scew_element_contents (xe), NULL);
      g_assert (errno != ERANGE);
      range[nbins] = x;
      /* FIXME: should we check that the upper limit of one bin really is the
       * lower limit of the next one up? */
      scew_list_free (ee);
      gsl_histogram_set_ranges (h, range, nbins+1);

      /* The upper and lower limits of each bin have been established.  Now
       * fill in the counts in the bins. */
      ee = scew_element_list_by_name (fn_element, "p");
      nbins2 = scew_list_size (ee);
      g_assert (nbins2 == nbins);
      for (i = 0, iter = ee; iter != NULL; i++, iter = scew_list_next(iter))
        {
          xe = (scew_element *) scew_list_data (iter);
          x = strtod (scew_element_contents (xe), NULL);
          g_assert (errno != ERANGE);
          gsl_histogram_accumulate (h, (range[i]+range[i+1])/2.0, x);
        }
      scew_list_free (ee);
      g_free(range);

      /* Last step, take the histogram given by the user, which may contain
       * either counts or probability values in the bins, and turn it into a
       * probability distribution function (where the values of all bins must
       * sum to 1). */
      dist = PDF_new_histogram_dist (h);
      gsl_histogram_free (h); 
    }
  else /* parse new-style XML */
    {
      double x0, x1, p;
      scew_element *ev, *ex0, *ex1, *ep;
      unsigned int element_count;
      gboolean success;
      double* counts;
      
      /* Determine how many histogram bins there are. */
      /*----------------------------------------------*/
      nbins = 0;
      element_count = scew_element_count( fn_element ); 
      for( i = 0; i < element_count; ++i )
        {
          ev = scew_element_by_index( fn_element, i );
          
          if( 0 == g_ascii_strcasecmp( "value", scew_element_name( ev ) ) )
            ++nbins;   
        } 
    
      /* Set up the data structures. */
      /*-----------------------------*/
      range = g_new (double, nbins + 1);
      counts = g_new( double, nbins );           
      
      /* Parse the XML and fill the data structures. */
      /*---------------------------------------------*/
      success = TRUE; /* Until shown otherwise. */
      errno = 0;
      j = 0;
      for( i = 0; i < element_count; ++i )
        {
          ev = scew_element_by_index( fn_element, i );
        
          if( 0 != g_ascii_strcasecmp( "value", scew_element_name( ev ) ) )
            {
              success = FALSE;
              break; 
            }
          else
            {
              ex0 = scew_element_by_name( ev, "x0" );
              ex1 = scew_element_by_name( ev, "x1" );
              ep = scew_element_by_name( ev, "p" );
              
              if( ex0 )
                {
                  x0 = strtod( scew_element_contents( ex0 ), NULL ); 
                  g_assert (errno != ERANGE);
                }
              else
                success = FALSE;
                
              if( ex1 )
                {
                  x1 = strtod( scew_element_contents( ex1 ), NULL ); 
                  g_assert (errno != ERANGE);
                }
              else
                success = FALSE;
                
              if( ep )
                {
                  p = strtod( scew_element_contents( ep ), NULL ); 
                  g_assert (errno != ERANGE);
                }
              else
                success = FALSE;
                
              if( !success )
                break;
              else
                {
                  range[j] = x0;               
                  /* FIXME: should we check that the upper limit of one bin really is the
                   * lower limit of the next one up? */
                  range[j+1] = x1;
                  
                  counts[j] = p;
                  ++j;                
                }               
            }
        }
        
      if( success )
        {
          h = gsl_histogram_alloc (nbins);
          gsl_histogram_set_ranges (h, range, nbins+1);
          
          for( i = 0; i < nbins; ++i )
            gsl_histogram_accumulate (h, (range[i]+range[i+1])/2.0, counts[i]);  
                     
          /* Last step, take the histogram given by the user, which may contain
           * either counts or probability values in the bins, and turn it into a
           * probability distribution function (where the values of all bins must
           * sum to 1). */
          dist = PDF_new_histogram_dist (h);
          gsl_histogram_free (h);   
        }
      else
        dist = NULL;

      g_free(range);
      g_free( counts );

    } 
    
  return dist; 
}



/**
 * Retrieves a probability distribution function.
 *
 * @param param a probability distribution function parameter.
 * @return a probability distribution function object.
 */
PDF_dist_t *
PAR_get_PDF (PAR_parameter_t * param)
{
  PDF_dist_t *dist;
  scew_element *e, *tmp, *fn_param;
#if DEBUG
  g_debug ("----- ENTER PAR_get_PDF");
#endif

  /* For old-style XML (used through NAADSM 3.1.23), a block of XML that
     represents a PDF has no <probability-density-function> tag: we can jump 
     right into the individual function types.
     New-style XML (supported in NAADSM 3.1.24 and later) introduces the
     <probability-density-function> tag.  We need to determine which style
     that we're dealing with here.
  */
  tmp = scew_element_by_name (param, "probability-density-function");
  if( tmp )
    fn_param = tmp;  
  else
    fn_param = (scew_element*)param; 


  /* Find out what kind of distribution it is. */
  e = scew_element_by_name (fn_param, "point");
  if (e)
    {
      double value;

      errno = 0;
      value = strtod (scew_element_contents (e), NULL);
      if (errno == ERANGE)
        {
          g_error ("point distribution parameter \"%s\" is not a number", scew_element_contents (e));
        }
      dist = PDF_new_point_dist (value);
      goto end;
    }
  e = scew_element_by_name (fn_param, "uniform");
  if (e)
    {
      double a, b;

      errno = 0;
      a = strtod (scew_element_contents (scew_element_by_name (e, "a")), NULL);
      g_assert (errno != ERANGE);
      b = strtod (scew_element_contents (scew_element_by_name (e, "b")), NULL);
      g_assert (errno != ERANGE);
      dist = PDF_new_uniform_dist (a, b);
      goto end;
    }
  e = scew_element_by_name (fn_param, "triangular");
  if (e)
    {
      double a, c, b;

      errno = 0;
      a = strtod (scew_element_contents (scew_element_by_name (e, "a")), NULL);
      g_assert (errno != ERANGE);
      c = strtod (scew_element_contents (scew_element_by_name (e, "c")), NULL);
      g_assert (errno != ERANGE);
      b = strtod (scew_element_contents (scew_element_by_name (e, "b")), NULL);
      g_assert (errno != ERANGE);
      dist = PDF_new_triangular_dist (a, c, b);
      goto end;
    }
  e = scew_element_by_name (fn_param, "gaussian");
  if (e)
    {
      double mean, stddev;

      errno = 0;
      mean = strtod (scew_element_contents (scew_element_by_name (e, "mean")), NULL);
      g_assert (errno != ERANGE);
      stddev = strtod (scew_element_contents (scew_element_by_name (e, "stddev")), NULL);
      g_assert (errno != ERANGE);
      dist = PDF_new_gaussian_dist (mean, stddev);
      goto end;
    }
  e = scew_element_by_name (fn_param, "inverse-gaussian");
  if (e)
    {
      double mu, lambda;

      errno = 0;
      mu = strtod (scew_element_contents (scew_element_by_name (e, "mu")), NULL);
      g_assert (errno != ERANGE);
      lambda = strtod (scew_element_contents (scew_element_by_name (e, "lambda")), NULL);
      g_assert (errno != ERANGE);
      dist = PDF_new_inverse_gaussian_dist (mu, lambda);
      goto end;
    }
  e = scew_element_by_name (fn_param, "poisson");
  if (e)
    {
      double mean;

      errno = 0;
      mean = strtod (scew_element_contents (scew_element_by_name (e, "mean")), NULL);
      g_assert (errno != ERANGE);
      dist = PDF_new_poisson_dist (mean);
      goto end;
    }
  e = scew_element_by_name (fn_param, "beta");
  if (e)
    {
      double alpha, beta, location, scale;

      errno = 0;
      alpha = strtod (scew_element_contents (scew_element_by_name (e, "alpha")), NULL);
      g_assert (errno != ERANGE);
      beta = strtod (scew_element_contents (scew_element_by_name (e, "beta")), NULL);
      g_assert (errno != ERANGE);
      location = strtod (scew_element_contents (scew_element_by_name (e, "location")), NULL);
      g_assert (errno != ERANGE);
      scale = strtod (scew_element_contents (scew_element_by_name (e, "scale")), NULL);
      g_assert (errno != ERANGE);
      dist = PDF_new_beta_dist (alpha, beta, location, scale);
      goto end;
    }
  e = scew_element_by_name (fn_param, "beta-pert");
  if (e)
    {
      double min, mode, max;

      errno = 0;
      min = strtod (scew_element_contents (scew_element_by_name (e, "min")), NULL);
      g_assert (errno != ERANGE);
      mode = strtod (scew_element_contents (scew_element_by_name (e, "mode")), NULL);
      g_assert (errno != ERANGE);
      max = strtod (scew_element_contents (scew_element_by_name (e, "max")), NULL);
      g_assert (errno != ERANGE);
      dist = PDF_new_beta_pert_dist (min, mode, max);
      goto end;
    }
  e = scew_element_by_name (fn_param, "gamma");
  if (e)
    {
      double alpha, beta;

      errno = 0;
      alpha = strtod (scew_element_contents (scew_element_by_name (e, "alpha")), NULL);
      g_assert (errno != ERANGE);
      beta = strtod (scew_element_contents (scew_element_by_name (e, "beta")), NULL);
      g_assert (errno != ERANGE);
      dist = PDF_new_gamma_dist (alpha, beta);
      goto end;
    }
  e = scew_element_by_name (fn_param, "weibull");
  if (e)
    {
      double alpha, beta;

      errno = 0;
      alpha = strtod (scew_element_contents (scew_element_by_name (e, "alpha")), NULL);
      g_assert (errno != ERANGE);
      beta = strtod (scew_element_contents (scew_element_by_name (e, "beta")), NULL);
      g_assert (errno != ERANGE);
      dist = PDF_new_weibull_dist (alpha, beta);
      goto end;
    }
  e = scew_element_by_name (fn_param, "exponential");
  if (e)
    {
      double mean;

      errno = 0;
      mean = strtod (scew_element_contents (scew_element_by_name (e, "mean")), NULL);
      g_assert (errno != ERANGE);
      dist = PDF_new_exponential_dist (mean);
      goto end;
    }
  e = scew_element_by_name (fn_param, "pearson5");
  if (e)
    {
      double alpha, beta;

      errno = 0;
      alpha = strtod (scew_element_contents (scew_element_by_name (e, "alpha")), NULL);
      g_assert (errno != ERANGE);
      beta = strtod (scew_element_contents (scew_element_by_name (e, "beta")), NULL);
      g_assert (errno != ERANGE);
      dist = PDF_new_pearson5_dist (alpha, beta);
      goto end;
    }
  e = scew_element_by_name (fn_param, "logistic");
  if (e)
    {
      double location, scale;

      errno = 0;
      location = strtod (scew_element_contents (scew_element_by_name (e, "location")), NULL);
      g_assert (errno != ERANGE);
      scale = strtod (scew_element_contents (scew_element_by_name (e, "scale")), NULL);
      g_assert (errno != ERANGE);
      dist = PDF_new_logistic_dist (location, scale);
      goto end;
    }
  e = scew_element_by_name (fn_param, "loglogistic");
  if (e)
    {
      double location, scale, shape;

      errno = 0;
      location = strtod (scew_element_contents (scew_element_by_name (e, "location")), NULL);
      g_assert (errno != ERANGE);
      scale = strtod (scew_element_contents (scew_element_by_name (e, "scale")), NULL);
      g_assert (errno != ERANGE);
      shape = strtod (scew_element_contents (scew_element_by_name (e, "shape")), NULL);
      g_assert (errno != ERANGE);
      dist = PDF_new_loglogistic_dist (location, scale, shape);
      goto end;
    }
  e = scew_element_by_name (fn_param, "lognormal");
  if (e)
    {
      double zeta, sigma;

      errno = 0;
      zeta = strtod (scew_element_contents (scew_element_by_name (e, "zeta")), NULL);
      g_assert (errno != ERANGE);
      sigma = strtod (scew_element_contents (scew_element_by_name (e, "sigma")), NULL);
      g_assert (errno != ERANGE);
      dist = PDF_new_lognormal_dist (zeta, sigma);
      goto end;
    }
  e = scew_element_by_name (fn_param, "piecewise");
  if (e)
    {
      dist = PAR_get_piecewise_PDF( e );
      goto end;
    }
  e = scew_element_by_name (fn_param, "histogram");
  if (e)
    {
      dist = PAR_get_histogram_PDF( e );
      goto end;
    }
  e = scew_element_by_name (fn_param, "negative-binomial");
  if (e)
    {
      double s, p;

      errno = 0;
      s = strtol (scew_element_contents (scew_element_by_name (e, "s")), NULL, 10);
      g_assert (errno != ERANGE);
      g_assert (s > 0);
      p = strtod (scew_element_contents (scew_element_by_name (e, "p")), NULL);
      g_assert (errno != ERANGE);
      g_assert ((0.0 < p) && (p < 1.0));
      dist = PDF_new_negative_binomial_dist (s, p);
      goto end;
    }
  e = scew_element_by_name (fn_param, "pareto");
  if (e)
    {
      double theta, a;

      errno = 0;
      theta = strtod (scew_element_contents (scew_element_by_name (e, "theta")), NULL);
      g_assert (errno != ERANGE);
      a = strtol (scew_element_contents (scew_element_by_name (e, "a")), NULL, 10);
      g_assert (errno != ERANGE);
      dist = PDF_new_pareto_dist (theta, a);
      goto end;
    }
  e = scew_element_by_name (fn_param, "bernoulli");
  if (e)
    {
      double p;

      errno = 0;
      p = strtod (scew_element_contents (scew_element_by_name (e, "p")), NULL);
      g_assert (errno != ERANGE);
      g_assert ((0.0 < p) && (p < 1.0));
      dist = PDF_new_bernoulli_dist (p);
      goto end;
    } 
  e = scew_element_by_name (fn_param, "binomial");
  if (e)
    {
      double n, p;

      errno = 0;
      n = strtol (scew_element_contents (scew_element_by_name (e, "n")), NULL, 10);
      g_assert (errno != ERANGE);
      g_assert (n > 0);
      p = strtod (scew_element_contents (scew_element_by_name (e, "p")), NULL);
      g_assert (errno != ERANGE);
      g_assert ((0.0 < p) && (p < 1.0));
      dist = PDF_new_binomial_dist (n, p);
      goto end;
    }
  e = scew_element_by_name (fn_param, "discrete-uniform");
  if (e)
    {
      double min, max;

      errno = 0;
      min = strtol (scew_element_contents (scew_element_by_name (e, "min")), NULL, 10);
      g_assert (errno != ERANGE);
      max = strtol (scew_element_contents (scew_element_by_name (e, "max")), NULL, 10);
      g_assert (errno != ERANGE);
      dist = PDF_new_discrete_uniform_dist (min, max);
      goto end;
    }
  e = scew_element_by_name (fn_param, "hypergeometric");
  if (e)
    {
      /* n1 = d
       * n2 = m - d
       * t = n
       */
      int n1, n2, t, m;

      errno = 0;
      n1 = strtol (scew_element_contents (scew_element_by_name (e, "d")), NULL, 10);
      g_assert (errno != ERANGE);
      g_assert (0 < n1);
      m = strtol (scew_element_contents (scew_element_by_name (e, "m")), NULL, 10);
      g_assert (errno != ERANGE);
      g_assert (0 < m);
      n2 = m - n1;
      t = strtol (scew_element_contents (scew_element_by_name (e, "n")), NULL, 10);
      g_assert (errno != ERANGE);
      g_assert ((0 < t) && (t < (n1 + n2)));
      dist = PDF_new_hypergeometric_dist (n1, n2, t);
      goto end;
    }

  g_assert_not_reached ();

end:
#if DEBUG
  g_debug ("----- EXIT PAR_get_PDF");
#endif

  return dist;
}



/**
 * Retrieves a relationship chart.
 *
 * @param param a relationship chart parameter.
 * @return a relationship chart object.
 */
REL_chart_t *
PAR_get_relationship_chart (PAR_parameter_t * param)
{
  REL_chart_t *chart;
  scew_list *ee, *iter;
  unsigned int npoints;
  double *x, *y;
  unsigned int i, j;
  double value;
  scew_element *fn_element;
  gboolean old_style_xml;
  
  #if DEBUG
    g_debug ("----- ENTER PAR_get_relationship_chart");
  #endif
  
  /* Determine whether we're dealing with new- or old-style XML. */
  /*-------------------------------------------------------------*/
  /* New-style XML has the tag <relational-function>. */
  fn_element = scew_element_by_name( param, "relational-function" );
  if( fn_element )
    old_style_xml = FALSE; 
  else
    old_style_xml = TRUE;
  
  /* Parse XML, once we know what style it is. */
  /*-------------------------------------------*/
  if( old_style_xml )
    {
      gboolean xvalue;
      scew_element *e;

      ee = scew_element_list_by_name (param, "value");
      npoints = scew_list_size (ee);
      npoints /= 2;
      #if DEBUG
        g_debug ("%u points", npoints);
      #endif
    
      /* Copy the x,y values from the DOM tree into arrays. */
      x = g_new (double, npoints);
      y = g_new (double, npoints);
    
      i = 0;
      xvalue = TRUE;
      for (iter = ee; iter != NULL; iter = scew_list_next(iter))
        {
          errno = 0;
          e = (scew_element *) scew_list_data (iter);
          value = strtod (scew_element_contents (e), NULL);
          g_assert (errno != ERANGE);
          /* The list of elements alternates x,y,x,y... */
          if (xvalue)
            x[i] = value;
          else
            y[i++] = value;
          xvalue = !xvalue;
        }
      chart = REL_new_chart (x, y, npoints);
      g_free (y);
      g_free (x);
      scew_list_free (ee);
    }
  else /* Parse new-style XML */
    {
      scew_element *ve, *xe, *ye;
      gboolean success;  
      
      success = TRUE; /* Until shown otherwise. */
      
      /* Loop over all elements once to determine the number of points. */
      /*----------------------------------------------------------------*/
      npoints = 0;
      for( i = 0; i < scew_element_count( fn_element ); ++i ) 
        {
          ve = scew_element_by_index( fn_element, i );
          if( 0 == g_ascii_strcasecmp( "value", scew_element_name( ve ) ) )
            ++npoints;    
        }
      
      /* Set up data structures. */
      /*-------------------------*/
      x = g_new (double, npoints);
      y = g_new (double, npoints);
              
      /* Loop over all elements again a second time to fill the array of points. */
      /*-------------------------------------------------------------------------*/ 
      j = 0;
      for( i = 0; i < scew_element_count( fn_element ); ++i ) 
        {
          ve = scew_element_by_index( fn_element, i );
          if( 0 == g_ascii_strcasecmp( "value", scew_element_name( ve ) ) )
            {         
              errno = 0;
              xe = scew_element_by_name( ve, "x" );
              ye = scew_element_by_name( ve, "y" );
              
              if( xe )
                {
                  value = strtod( scew_element_contents( xe ), NULL );
                  g_assert (errno != ERANGE);
                  x[j] = value;  
                }
              else
                success = FALSE;
                
              if( ye )
                {
                  value = strtod( scew_element_contents( ye ), NULL );
                  g_assert (errno != ERANGE);
                  y[j] = value;
                }
              else
                success = FALSE;                        
             
              ++j;
              
              if( !success )
                break; 
            }
        }      
      
      if( !success )
        chart = NULL;
      else
        chart = REL_new_chart (x, y, npoints);
        
      g_free (y);
      g_free (x); 
    }

  #if DEBUG
    g_debug ("----- EXIT PAR_get_relationship_chart");
  #endif

  return chart;
}



/**
 * Retrieves a boolean parameter from the database.
 *
 * @param loc location of a gboolean into which to write the boolean.
 * @param ncols number of columns in the SQL query result.
 * @param values values returned by the SQL query, all in text form.
 * @param colname names of columns in the SQL query result.
 * @return 0
 */
static int
PAR_get_boolean_callback (void *loc, int ncols, char **value, char **colname)
{
  gboolean *result;
  long int tmp;
  
  g_assert (ncols == 1);
  errno = 0;
  tmp = strtol (value[0], NULL, 10);   /* base 10 */
  g_assert (errno != ERANGE && errno != EINVAL);
  g_assert (tmp == 0 || tmp == 1);
  result = (gboolean *)loc;
  *result = (tmp == 1);
  return 0;
}



/**
 * Retrieves a boolean.
 *
 * @param db a parameter database.
 * @param query the query to retrieve the parameter.
 * @return the boolean.
 */
gboolean
PAR_get_boolean (sqlite3 *db, char *query)
{
  gboolean result;
  char *sqlerr;

#if DEBUG
  g_debug ("----- ENTER PAR_get_boolean");
#endif

  sqlite3_exec (db, query, PAR_get_boolean_callback, &result, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }

#if DEBUG
  g_debug ("----- EXIT PAR_get_boolean");
#endif

  return result;
}



/**
 * Retrieves a generic unitless value.
 *
 * Side effect: upon return, the location indicated by <i>success</i> contains
 * FALSE if the parameter was missing, out of range, or otherwise invalid, and
 * TRUE otherwise.
 *
 * @param param a numeric parameter.
 * @param success a location in which to store a success or failure flag.
 * @return the value.  If the conversion did not succeed, this value is
 *   undefined.
 */
double
PAR_get_unitless (PAR_parameter_t * param, gboolean * success)
{
  double x;
  const char *text;
  char *endptr;

#if DEBUG
  g_debug ("----- ENTER PAR_get_unitless");
#endif

  text = scew_element_contents (param);
  x = strtod (text, &endptr);
  *success = !(text[0] == '\0' || errno == ERANGE || endptr == text);
  if (*success == FALSE)
    g_warning ("missing or invalid unitless parameter");

#if DEBUG
  g_debug ("----- EXIT PAR_get_unitless");
#endif

  return x;
}



/**
 * Retrieves a generic unitless integer value.
 *
 * Side effect: upon return, the location indicated by <i>success</i> contains
 * FALSE if the parameter was missing, out of range, or otherwise invalid, and
 * TRUE otherwise.
 *
 * @param param a numeric parameter.
 * @param success a location in which to store a success or failure flag.
 * @return the value.  If the conversion did not succeed, this value is
 *   undefined.
 */
int
PAR_get_unitless_int (PAR_parameter_t * param, gboolean * success)
{
  long int x;
  const char *text;
  char *endptr;

  #if DEBUG
    g_debug ("----- ENTER PAR_get_unitless_int");
  #endif

  text = scew_element_contents (param);
  x = strtol (text, &endptr, 10);
  *success = !(text[0] == '\0' || errno == ERANGE || endptr == text);
  if (*success == FALSE)
    g_warning ("missing or invalid unitless parameter");

  #if DEBUG
    g_debug ("----- EXIT PAR_get_unitless_int");
  #endif

  return (int) x;
}



/**
 * Retrieves a text parameter from the database.
 *
 * @param loc location of a char * into which to write the starting location of
 *   the text.
 * @param ncols number of columns in the SQL query result.
 * @param values values returned by the SQL query, all in text form.
 * @param colname names of columns in the SQL query result.
 * @return 0
 */
static int
PAR_get_text_callback (void *loc, int ncols, char **value, char **colname)
{
  char **result;
  
  g_assert (ncols == 1);
  result = (char **)loc;
  *result = value[0];
  return 0;
}



/**
 * Retrieves a text value.  The text is copied and must be freed with g_free.
 *
 * @param db a parameter database.
 * @param query the query to retrieve the parameter.
 * @return the text.
 */
char *
PAR_get_text (sqlite3 *db, char *query)
{
  char *text = NULL;
  char *sqlerr;

#if DEBUG
  g_debug ("----- ENTER PAR_get_text");
#endif

  sqlite3_exec (db, query, PAR_get_text_callback, &text, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }
  text = g_strdup (text);

#if DEBUG
  g_debug ("----- EXIT PAR_get_text");
#endif

  return text;
}



/**
 * Retrieves an integer parameter from the database.
 *
 * @param loc location of a gint into which to write the integer.
 * @param ncols number of columns in the SQL query result.
 * @param values values returned by the SQL query, all in text form.
 * @param colname names of columns in the SQL query result.
 * @return 0
 */
static int
PAR_get_int_callback (void *loc, int ncols, char **value, char **colname)
{
  gint *result;
  long int tmp;
  
  g_assert (ncols == 1);
  errno = 0;
  tmp = strtol (value[0], NULL, 10);   /* base 10 */
  g_assert (errno != ERANGE && errno != EINVAL);
  result = (gint *)loc;
  *result = (gint)tmp;
  return 0;
}



/**
 * Retrieves an integer parameter.
 *
 * @param db a parameter database.
 * @param query the query to retrieve the parameter.
 * @return the integer.
 */
gint
PAR_get_int (sqlite3 *db, char *query)
{
  gint result;
  char *sqlerr;

  #if DEBUG
    g_debug ("----- ENTER PAR_get_int");
  #endif

  sqlite3_exec (db, query, PAR_get_int_callback, &result, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }

  #if DEBUG
    g_debug ("----- EXIT PAR_get_int");
  #endif

  return result;
}
/* end of file parameter.c */
