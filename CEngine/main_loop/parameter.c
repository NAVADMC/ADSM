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



typedef struct
{
  GArray *x; /* growable array of doubles */
  GArray *y; /* growable array of doubles */
}
PAR_get_relchart_callback_args_t;


  
/**
 * Retrieves a relationship chart parameter from the database. This callback
 * function is called once for each x-y pair (database row) in the chart.
 *
 * @param loc location of a PAR_get_relchart_callback_args_t object into which
 *  to accumulate the x-y pairs.
 * @param ncols number of columns in the SQL query result.
 * @param values values returned by the SQL query, all in text form.
 * @param colname names of columns in the SQL query result.
 * @return 0
 */
static int
PAR_get_relchart_callback (void *loc, int ncols, char **value, char **colname)
{
  PAR_get_relchart_callback_args_t *build;
  double x, y;
  
  g_assert (ncols == 2);
  build = (PAR_get_relchart_callback_args_t *) loc;
  errno = 0;
  x = strtod (value[0], NULL);
  if (errno == ERANGE)
    {
      g_error ("relationship chart point \"%s\" is not a number", value[0]);
    }
  errno = 0;
  y = strtod (value[1], NULL);
  if (errno == ERANGE)
    {
      g_error ("relationship chart point \"%s\" is not a number", value[1]);
    }
  g_array_append_val (build->x, x);
  g_array_append_val (build->y, y);
  return 0;
}




/**
 * Retrieves a relationship chart.
 *
 * @param db a parameter database.
 * @param id the database ID of the relationship chart.
 * @return a relationship chart object.
 */
REL_chart_t *
PAR_get_relchart (sqlite3 *db, guint id)
{
  REL_chart_t *chart;
  PAR_get_relchart_callback_args_t build;
  char *query;
  char *sqlerr;
  
  #if DEBUG
    g_debug ("----- ENTER PAR_get_relationship_chart");
  #endif

  build.x = g_array_new (/* zero_terminated = */ FALSE, /* clear = */ FALSE, sizeof (double));
  build.y = g_array_new (/* zero_terminated = */ FALSE, /* clear = */ FALSE, sizeof (double));
  query = g_strdup_printf ("SELECT x,y FROM ScenarioCreator_relationalfunction fn,ScenarioCreator_relationalpoint pt WHERE fn.id=%u AND pt.relational_function_id=fn.id ORDER BY x ASC", id);
  sqlite3_exec (db, query, PAR_get_relchart_callback, &build, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }
  g_free (query);

  chart = REL_new_chart ((double *)(build.x->data), (double *)(build.y->data), build.x->len);
  g_array_free (build.x, /* free_segment = */ TRUE);
  g_array_free (build.y, /* free_segment = */ TRUE);

  #if DEBUG
    g_debug ("----- EXIT PAR_get_relationship_chart");
  #endif

  return chart;
}



typedef struct
{
  sqlite3 *db; /**< A parameter database. */
  PDF_dist_t *dist; /**< A location into which to write the pointer to the
    created object. */
}
PAR_get_PDF_callback_args_t;


  
/**
 * Retrieves a probability distribution function parameter from the database.
 *
 * @param data pointer to a PAR_get_PDF_callback_args_t structure.
 * @param ncols number of columns in the SQL query result.
 * @param values values returned by the SQL query, all in text form.
 * @param colname names of columns in the SQL query result.
 * @return 0
 */
static int
PAR_get_PDF_callback (void *data, int ncols, char **value, char **colname)
{
  PAR_get_PDF_callback_args_t *args;
  PDF_dist_t *dist = NULL;
  char *equation_type;
  #if DEBUG
    GString *s;
    int i;
  #endif
  
  g_assert (ncols == 19);

  args = (PAR_get_PDF_callback_args_t *)data;

  #if DEBUG
    s = g_string_new ("[");
    for (i = 0; i < ncols; i++)
      {
        if (i > 0)
          g_string_append_c (s, ',');
        g_string_append_printf (s, "%s=%s", colname[i], value[i]);
      }
    g_string_append_c (s, ']');    
    g_debug ("query returned %s", s->str);
    g_string_free (s, TRUE);    
  #endif
  equation_type = value[0];
  if (strcmp (equation_type, "Point") == 0)
    {
      double mode;
      errno = 0;
      mode = strtod (value[4], NULL);
      if (errno == ERANGE)
        {
          g_error ("point distribution parameter \"%s\" is not a number", value[4]);
        }
      dist = PDF_new_point_dist (mode);
    }
  else if (strcmp (equation_type, "Triangular") == 0)
    {
      double a,c,b;

      errno = 0;
      a = strtod (value[3], NULL);
      g_assert (errno != ERANGE);

      errno = 0;
      c = strtod (value[4], NULL);
      g_assert (errno != ERANGE);

      errno = 0;
      b = strtod (value[5], NULL);
      g_assert (errno != ERANGE);

      dist = PDF_new_triangular_dist (a, c, b);
    }
  else if (strcmp (equation_type, "Piecewise") == 0)
    {
      guint rel_id;
      PAR_get_relchart_callback_args_t build;
      char *query;
      char *sqlerr;

      rel_id = 0; /* Filling this in for now just to prevent an uninitialized
        variable warning */
      build.x = g_array_new (/* zero_terminated = */ FALSE, /* clear = */ FALSE, sizeof (double));
      build.y = g_array_new (/* zero_terminated = */ FALSE, /* clear = */ FALSE, sizeof (double));
      query = g_strdup_printf ("SELECT x,y FROM ScenarioCreator_relationalfunction fn,ScenarioCreator_relationalpoint pt WHERE fn.id=%u AND pt.relational_function_id=fn.id ORDER BY _point_order", rel_id);
      sqlite3_exec (args->db, query, PAR_get_relchart_callback, &build, &sqlerr);
      if (sqlerr)
        {
          g_error ("%s", sqlerr);
        }
      g_free (query);

      dist = PDF_new_piecewise_dist (build.x->len, (double *)(build.x->data), (double *)(build.y->data));
      g_array_free (build.x, /* free_segment = */ TRUE);
      g_array_free (build.y, /* free_segment = */ TRUE);
    }
  else if (strcmp (equation_type, "Histogram") == 0)
    {
      guint rel_id;
      PAR_get_relchart_callback_args_t build;
      char *query;
      char *sqlerr;
      guint nbins, i;
      gsl_histogram *h;
      double *range;

      rel_id = 0; /* Filling this in for now just to prevent an uninitialized
        variable warning */
      build.x = g_array_new (/* zero_terminated = */ FALSE, /* clear = */ FALSE, sizeof (double));
      build.y = g_array_new (/* zero_terminated = */ FALSE, /* clear = */ FALSE, sizeof (double));
      query = g_strdup_printf ("SELECT x,y FROM ScenarioCreator_relationalfunction fn,ScenarioCreator_relationalpoint pt WHERE fn.id=%u AND pt.relational_function_id=fn.id ORDER BY _point_order", rel_id);
      sqlite3_exec (args->db, query, PAR_get_relchart_callback, &build, &sqlerr);
      if (sqlerr)
        {
          g_error ("%s", sqlerr);
        }
      g_free (query);

      nbins = build.x->len - 1;
      h = gsl_histogram_alloc (nbins);
      /* The x-values read from the database define the range (upper and lower
       * limit) of each bin. */
      range = (double *)(build.x->data);
      gsl_histogram_set_ranges (h, range, nbins + 1);
      /* The y-values read from the database give the amount to add to each bin
       * (the final y-value is ignored). */
      for (i = 0; i < nbins; i++)
        gsl_histogram_accumulate (h, (range[i]+range[i+1])/2.0, g_array_index(build.y, double, i));

      dist = PDF_new_histogram_dist (h);
      gsl_histogram_free (h);   
    }
  else
    {
      g_warning ("%s distribution not supported", equation_type);
      g_assert_not_reached();
    }
  args->dist = dist;
  return 0;
}



/**
 * Retrieves a probability distribution function.
 *
 * @param db a parameter database.
 * @param id the database ID of the probability distribution function.
 * @return a probability distribution function object.
 */
PDF_dist_t *
PAR_get_PDF (sqlite3 *db, guint id)
{
  PAR_get_PDF_callback_args_t args;
  char *query;
  char *sqlerr;
#if DEBUG
  g_debug ("----- ENTER PAR_get_PDF");
#endif

  args.db = db;
  args.dist = NULL;
  query = g_strdup_printf ("SELECT equation_type,mean,std_dev,min,mode,max,alpha,alpha2,beta,location,scale,shape,n,p,m,d,theta,a,s FROM ScenarioCreator_probabilityfunction WHERE id=%u", id);
  sqlite3_exec (db, query, PAR_get_PDF_callback, &args, &sqlerr);
  if (sqlerr)
    {
      g_error ("%s", sqlerr);
    }
  g_free (query);

  /* Find out what kind of distribution it is. */
/*
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
       n1 = d
       n2 = m - d
       t = n
      
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
*/

#if DEBUG
  g_debug ("----- EXIT PAR_get_PDF");
#endif

  return args.dist;
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
  gboolean result = FALSE;
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
  gchar *normalized;
  
  g_assert (ncols == 1);
  normalized = g_utf8_normalize (value[0], -1, G_NORMALIZE_DEFAULT);
  
  result = (char **)loc;
  *result = normalized;
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
  gint result = 0;
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
