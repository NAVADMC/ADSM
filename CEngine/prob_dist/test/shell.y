%{
#if HAVE_CONFIG_H
#  include <config.h>
#endif

#include <prob_dist.h>
#include <glib.h>
#include <math.h>
#include <gsl/gsl_statistics.h>

#define PROMPT "> "

/** @file prob_dist/test/shell.c
 * A simple shell to exercise libprob_dist.  It provides a way to create the
 * probability distributions and call the functions offered by the
 * <a href="prob__dist_8h.html">probability distribution library</a>, so that
 * a suite of tests can be scripted.
 *
 * The commands are:
 * <ul>
 *   <li>
 *     <code>point (x)</code>
 *
 *     Creates a <a href="structPDF__point__dist__t.html">"point"
 *     distribution</a> that only ever returns the value \a x.
 *   <li>
 *     <code>uniform (a,b)</code>
 *
 *     Creates a <a href="structPDF__uniform__dist__t.html">uniform (flat)
 *     distribution</a>.
 *   <li>
 *     <code>triangular (a,c,b)</code>
 *
 *     Creates a <a href="structPDF__triangular__dist__t.html">triangular
 *     distribution</a>.
 *   <li>
 *     <code>piecewise (x1,y1,x2,y2,...)</code>
 *
 *     Creates a <a href="structPDF__piecewise__dist__t.html">piecewise
 *     distribution</a>.
 *   <li>
 *     <code>histogram (low,high,bin1,bin2,...)</code>
 *
 *     Creates a <a href="structPDF__histogram__dist__t.html">histogram
 *     distribution</a>.
 *   <li>
 *     <code>gaussian (mu,sigma)</code>
 *
 *     Creates a <a href="structPDF__gaussian__dist__t.html">Gaussian (normal)
 *     distribution</a>.
 *   <li>
 *     <code>inverse-gaussian (mu,lambda)</code>
 *
 *     Creates a <a href="structPDF__inverse__gaussian__dist__t.html">inverse
 *     Gaussian distribution</a>.
 *   <li>
 *     <code>poisson (mu)</code>
 *
 *     Creates a <a href="structPDF__poisson__dist__t.html">Poisson
 *     distribution</a>.
 *   <li>
 *     <code>beta (alpha, beta, location, scale)</code>
 *
 *     Creates a <a href="structPDF__beta__dist__t.html">beta distribution</a>.
 *   <li>
 *     <code>betapert (min, mode, max)</code>
 *
 *     Creates a <a href="structPDF__beta__dist__t.html">beta distribution</a>.
 *   <li>
 *     <code>gamma (alpha, beta)</code>
 *
 *     Creates a <a href="structPDF__gamma__dist__t.html">gamma distribution</a>.
 *   <li>
 *     <code>weibull (alpha, beta)</code>
 *
 *     Creates a <a href="structPDF__weibull__dist__t.html">Weibull
 *     distribution</a>.
 *   <li>
 *     <code>exponential (mean)</code>
 *
 *     Creates an <a href="structPDF__exponential__dist__t.html">exponential
 *     distribution</a>.
 *   <li>
 *     <code>logistic (location, scale)</code>
 *
 *     Creates an <a href="structPDF__logistic__dist__t.html">logistic
 *     distribution</a>.
 *   <li>
 *     <code>loglogistic (location, scale, shape)</code>
 *
 *     Creates an <a href="structPDF__logistic__dist__t.html">loglogistic
 *     distribution</a>.
 *   <li>
 *     <code>lognormal (zeta, sigma)</code>
 *
 *     Creates an <a href="structPDF__lognormal__dist__t.html">lognormal
 *     distribution</a>.
 *   <li>
 *     <code>negbinomial (s, p)</code>
 *
 *     Creates an <a href="structPDF__negbinomial__dist__t.html">negative
 *     binomial distribution</a>.
 *   <li>
 *     <code>pareto (theta, a)</code>
 *
 *     Creates an <a href="structPDF__pareto__dist__t.html">Pareto
 *     distribution</a>.
 *   <li>
 *     <code>binomial (n, p)</code>
 *
 *     Creates an <a href="structPDF__binomial__dist__t.html">binomial
 *     distribution</a>.
 *   <li>
 *     <code>discrete-uniform (min, max)</code>
 *
 *     Creates an <a href="structPDF__discrete__uniform__dist__t.html">discrete
 *     uniform distribution</a>.
 *   <li>
 *     <code>hypergeometric (n1, n2, t)</code>
 *
 *     Creates an <a href="structPDF__hypergeometric__dist__t.html">hypergeometric
 *     distribution</a>.
 *   <li>
 *     <code>pdf (x)</code>
 *
 *     Returns the value of the probability distribution function at \a x for
 *     the most recently created distribution.
 *   <li>
 *     <code>cdf (x)</code>
 *
 *     Returns the value of the cumulative distribution function at \a x (the
 *     area under the probability distribution curve to the left of <i>x</i>)
 *     for the most recently created distribution.
 *   <li>
 *     <code>invcdf (area)</code>
 *
 *     Returns the value of the inverse cumulative distribution function at
 *     \a area (<i>x</i> such that the area under the probability distribution
 *     curve to the left of <i>x</i> = <i>area</i>) for the most recently
 *     created distribution.
 *   <li>
 *     <code>min ()</code>
 *
 *     Returns the minimum of the range for the most recently created
 *     distribution.
 *   <li>
 *     <code>max ()</code>
 *
 *     Returns the maximum of the range for the most recently created
 *     distribution.
 *   <li>
 *     <code>mean ()</code>
 *
 *     Returns the mean for the most recently created distribution.
 *   <li>
 *     <code>variance ()</code>
 *
 *     Returns the variance for the most recently created
 *     distribution.
 *   <li>
 *     <code>sample_min (iter)</code>
 *
 *     Returns the minimum of the range for the most recently created
 *     distribution based on \a iter samples.
 *   <li>
 *     <code>sample_max (iter)</code>
 *
 *     Returns the maximum of the range for the most recently created
 *     distribution based on \a iter samples.
 *   <li>
 *     <code>sample_mean (iter)</code>
 *
 *     Returns the mean for the most recently created distribution
 *     based on \a iter samples.
 *   <li>
 *     <code>sample_variance (iter)</code>
 *
 *     Returns the variance for the most recently created
 *     distribution based on \a iter samples.
 *   <li>
 *     <code>sample (iter,low,high)</code>
 *
 *     Samples \a iter numbers from the most recently created distribution and
 *     builds a histogram.  The histogram's first bin counts results in
 *     [<i>low</i>,<i>low</i>+1), the second counts results in
 *     [<i>low</i>+1, <i>low</i>+2), etc., and the last bin counts results in
 *     [<i>high</i>-1, <i>high</i>).  Results below <i>low</i> or at or above
 *     <i>high</i> are not counted.  The output from this command is the
 *     fraction of results that fell in each bin, separated by spaces.
 * </ul>
 *
 * The shell exits on EOF (Ctrl+D if you're typing commands into it
 * interactively in Unix).
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date July 2003
 *
 * Copyright &copy; University of Guelph, 2003-2008
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

RAN_gen_t *rng;
PDF_dist_t *current_dist = NULL;
double * current_sample = NULL;
int ncurrent_samples = -1;

void g_free_as_GFunc (gpointer data, gpointer user_data);

static void current_sample_free(void)
{
  ncurrent_samples = -1;
  g_free (current_sample);
  current_sample = NULL;
}

static gboolean current_sample_create(int nsamples)
{
  int i;

  if (1 > nsamples)
    return FALSE;
  if (ncurrent_samples == nsamples)
    return TRUE;
  current_sample_free ();
  current_sample = g_new0(double, nsamples);
  if (NULL == current_sample)
    return FALSE;
  for (i = 0; i < nsamples; i++)
    current_sample[i] = PDF_random (current_dist, rng);
  ncurrent_samples = nsamples;
  return TRUE;
}
%}

%union {
  double fval;
  GSList *lval;
}

%token POINT UNIFORM TRIANGULAR PIECEWISE HISTOGRAM GAUSSIAN INVGAUSSIAN
%token POISSON BETA
%token BETAPERT GAMMA WEIBULL EXPONENTIAL LOGISTIC LOGLOGISTIC LOGNORMAL
%token NEGBINOMIAL PARETO
%token BINOMIAL DISCRETEUNIFORM HYPERGEOMETRIC
%token PDF CDF INVCDF SAMPLE
%token HAS_MIN HAS_MAX HAS_MEAN HAS_VARIANCE
%token REAL_MIN REAL_MAX REAL_MEAN REAL_VARIANCE
%token SAMPLE_MIN SAMPLE_MAX SAMPLE_MEAN SAMPLE_VARIANCE
%token NUM
%token LPAREN RPAREN COMMA
%type <fval> NUM
%type <lval> num_list

%%

commands :
    command commands
  | command
  ;

command :
    new_command
  | function_call
  | sample_command
  ;

new_command :
    POINT LPAREN NUM RPAREN
    {
      current_sample_free ();
      PDF_free_dist (current_dist);
      current_dist = PDF_new_point_dist ($3);
      PDF_printf_dist (current_dist);
      printf ("\n%s", PROMPT);
      fflush (stdout);
    }
  | UNIFORM LPAREN NUM COMMA NUM RPAREN
    { 
      current_sample_free ();
      PDF_free_dist (current_dist);
      current_dist = PDF_new_uniform_dist ($3, $5);
      PDF_printf_dist (current_dist);
      printf ("\n%s", PROMPT);
      fflush (stdout);
    }
  | TRIANGULAR LPAREN NUM COMMA NUM COMMA NUM RPAREN
    { 
      current_sample_free ();
      PDF_free_dist (current_dist);
      current_dist = PDF_new_triangular_dist ($3, $5, $7);
      PDF_printf_dist (current_dist);
      printf ("\n%s", PROMPT);
      fflush (stdout);
    }
  | PIECEWISE LPAREN num_list RPAREN
    {
      int npoints;
      double *x, *y, *px, *py;
      GSList *iter;

      current_sample_free ();
      PDF_free_dist (current_dist);

      npoints = g_slist_length ($3);
      if (npoints % 2 != 0)
	{
	  g_warning ("number of arguments must be even");
	  current_dist = NULL;
	}
      else
	{
	  /* Copy the arguments into x and y arrays, then free the argument list
	   * structure. */
      npoints /= 2;
      x = g_new (double, npoints);
      y = g_new (double, npoints);
	  
	  for (iter = $3, px = x, py = y; iter != NULL; )
	    {
	      *px++ = *((double *)(iter->data));
	      iter = g_slist_next (iter);
	      *py++ = *((double *)(iter->data));
	      iter = g_slist_next (iter);
	    }
	  g_slist_foreach ($3, g_free_as_GFunc, NULL);
	  g_slist_free ($3);

	  current_dist = PDF_new_piecewise_dist (npoints, x, y);
	  g_free (x);
	  g_free (y);
	}
      PDF_printf_dist (current_dist);
      printf ("\n%s", PROMPT);
      fflush (stdout);
    }
  | GAUSSIAN LPAREN NUM COMMA NUM RPAREN
    {
      current_sample_free ();
      PDF_free_dist (current_dist);
      current_dist = PDF_new_gaussian_dist ($3, $5);
      PDF_printf_dist (current_dist);
      printf ("\n%s", PROMPT);
      fflush (stdout);
    }
  | INVGAUSSIAN LPAREN NUM COMMA NUM RPAREN
    {
      current_sample_free ();
      PDF_free_dist (current_dist);
      current_dist = PDF_new_inverse_gaussian_dist ($3, $5);
      PDF_printf_dist (current_dist);
      printf ("\n%s", PROMPT);
      fflush (stdout);
    }
  | POISSON LPAREN NUM RPAREN
    {
      current_sample_free ();
      PDF_free_dist (current_dist);
      current_dist = PDF_new_poisson_dist ($3);
      PDF_printf_dist (current_dist);
      printf ("\n%s", PROMPT);
      fflush (stdout);
    }
  | BETA LPAREN NUM COMMA NUM COMMA NUM COMMA NUM RPAREN
    {
      current_sample_free ();
      PDF_free_dist (current_dist);
      current_dist = PDF_new_beta_dist ($3, $5, $7, $9);
      PDF_printf_dist (current_dist);
      printf ("\n%s", PROMPT);
      fflush (stdout);
    }
  | BETAPERT LPAREN NUM COMMA NUM COMMA NUM RPAREN
    {
      current_sample_free ();
      PDF_free_dist (current_dist);
      current_dist = PDF_new_beta_pert_dist ($3, $5, $7);
      PDF_printf_dist (current_dist);
      printf ("\n%s", PROMPT);
      fflush (stdout);
    }
  | GAMMA LPAREN NUM COMMA NUM RPAREN
    {
      current_sample_free ();
      PDF_free_dist (current_dist);
      current_dist = PDF_new_gamma_dist ($3, $5);
      PDF_printf_dist (current_dist);
      printf ("\n%s", PROMPT);
      fflush (stdout);
    }
  | WEIBULL LPAREN NUM COMMA NUM RPAREN
    {
      current_sample_free ();
      PDF_free_dist (current_dist);
      current_dist = PDF_new_weibull_dist ($3, $5);
      PDF_printf_dist (current_dist);
      printf ("\n%s", PROMPT);
      fflush (stdout);
    }
  | EXPONENTIAL LPAREN NUM RPAREN
    {
      current_sample_free ();
      PDF_free_dist (current_dist);
      current_dist = PDF_new_exponential_dist ($3);
      PDF_printf_dist (current_dist);
      printf ("\n%s", PROMPT);
      fflush (stdout);
    }
  | LOGISTIC LPAREN NUM COMMA NUM RPAREN
    {
      current_sample_free ();
      PDF_free_dist (current_dist);
      current_dist = PDF_new_logistic_dist ($3, $5);
      PDF_printf_dist (current_dist);
      printf ("\n%s", PROMPT);
      fflush (stdout);
    }
  | LOGLOGISTIC LPAREN NUM COMMA NUM COMMA NUM RPAREN
    {
      current_sample_free ();
      PDF_free_dist (current_dist);
      current_dist = PDF_new_loglogistic_dist ($3, $5, $7);
      PDF_printf_dist (current_dist);
      printf ("\n%s", PROMPT);
      fflush (stdout);
    }
  | LOGNORMAL LPAREN NUM COMMA NUM RPAREN
    {
      current_sample_free ();
      PDF_free_dist (current_dist);
      current_dist = PDF_new_lognormal_dist ($3, $5);
      PDF_printf_dist (current_dist);
      printf ("\n%s", PROMPT);
      fflush (stdout);
    }
  | NEGBINOMIAL LPAREN NUM COMMA NUM RPAREN
    {
      current_sample_free ();
      PDF_free_dist (current_dist);
      current_dist = PDF_new_negative_binomial_dist ($3, $5);
      PDF_printf_dist (current_dist);
      printf ("\n%s", PROMPT);
      fflush (stdout);
    }
  | PARETO LPAREN NUM COMMA NUM RPAREN
    {
      current_sample_free ();
      PDF_free_dist (current_dist);
      current_dist = PDF_new_pareto_dist ($3, $5);
      PDF_printf_dist (current_dist);
      printf ("\n%s", PROMPT);
      fflush (stdout);
    }
  | BINOMIAL LPAREN NUM COMMA NUM RPAREN
    {
      current_sample_free ();
      PDF_free_dist (current_dist);
      current_dist = PDF_new_binomial_dist ($3, $5);
      PDF_printf_dist (current_dist);
      printf ("\n%s", PROMPT);
      fflush (stdout);
    }
  | DISCRETEUNIFORM LPAREN NUM COMMA NUM RPAREN
    {
      current_sample_free ();
      PDF_free_dist (current_dist);
      current_dist = PDF_new_discrete_uniform_dist ($3, $5);
      PDF_printf_dist (current_dist);
      printf ("\n%s", PROMPT);
      fflush (stdout);
    }
  | HYPERGEOMETRIC LPAREN NUM COMMA NUM COMMA NUM RPAREN
    {
      current_sample_free ();
      PDF_free_dist (current_dist);
      current_dist = PDF_new_hypergeometric_dist ($3, $5, $7);
      PDF_printf_dist (current_dist);
      printf ("\n%s", PROMPT);
      fflush (stdout);
    }
  | HISTOGRAM LPAREN NUM COMMA NUM COMMA num_list RPAREN
    {
      int nbins; /* number of bins in the histogram */
      double width; /* width of each bin */
      gsl_histogram *histogram;
      double x;
      GSList *iter;

      current_sample_free ();
      PDF_free_dist (current_dist);

      /* Allocate a histogram data structure. */
      nbins = g_slist_length ($7);
      histogram = gsl_histogram_alloc (nbins);
      gsl_histogram_set_ranges_uniform (histogram, $3, $5);

      /* Copy the arguments into the histogram, then free the argument list
       * structure. */
      width = ($5 - $3) / nbins;
      for (iter = $7, x = $3 + width/2; iter != NULL; iter = g_slist_next (iter))
	{
	  gsl_histogram_accumulate (histogram, x, *((double *)(iter->data)));
	  x += width;
	}
      g_slist_foreach ($7, g_free_as_GFunc, NULL);
      g_slist_free ($7);

      current_dist = PDF_new_histogram_dist (histogram);
      gsl_histogram_free (histogram);
      PDF_printf_dist (current_dist);
      printf ("\n%s", PROMPT);
      fflush (stdout);
    }
  ;

function_call :
    PDF LPAREN NUM RPAREN
    {
      printf ("%g\n%s", PDF_pdf ($3, current_dist), PROMPT);
      fflush (stdout);
    }
  | CDF LPAREN NUM RPAREN
    {
      printf ("%g\n%s", PDF_cdf ($3, current_dist), PROMPT);
      fflush (stdout);
    }
  | INVCDF LPAREN NUM RPAREN
    {
      printf ("%g\n%s", PDF_inverse_cdf ($3, current_dist), PROMPT);
      fflush (stdout);
    }
  | HAS_MIN LPAREN RPAREN
    {
      printf ("%d\n%s", PDF_has_min (current_dist), PROMPT);
      fflush (stdout);
    }
  | HAS_MAX LPAREN RPAREN
    {
      printf ("%d\n%s", PDF_has_max (current_dist), PROMPT);
      fflush (stdout);
    }
  | HAS_MEAN LPAREN RPAREN
    {
      printf ("%d\n%s", PDF_has_mean (current_dist), PROMPT);
      fflush (stdout);
    }
  | HAS_VARIANCE LPAREN RPAREN
    {
      printf ("%d\n%s", PDF_has_variance (current_dist), PROMPT);
      fflush (stdout);
    }
  | REAL_MIN LPAREN RPAREN
    {
      printf ("%g\n%s", PDF_min (current_dist), PROMPT);
      fflush (stdout);
    }
  | REAL_MAX LPAREN RPAREN
    {
      printf ("%g\n%s", PDF_max (current_dist), PROMPT);
      fflush (stdout);
    }
  | REAL_MEAN LPAREN RPAREN
    {
      printf ("%g\n%s", PDF_mean (current_dist), PROMPT);
      fflush (stdout);
    }
  | REAL_VARIANCE LPAREN RPAREN
    {
      printf ("%g\n%s", PDF_variance (current_dist), PROMPT);
      fflush (stdout);
    }
  | SAMPLE_MIN LPAREN NUM RPAREN
    {
      current_sample_create($3);
      printf ("%g\n%s", gsl_stats_min(current_sample, 1, ncurrent_samples), PROMPT);
      fflush (stdout);
    }
  | SAMPLE_MAX LPAREN NUM RPAREN
    {
      current_sample_create($3);
      printf ("%g\n%s", gsl_stats_max(current_sample, 1, ncurrent_samples), PROMPT);
      fflush (stdout);
    }
  | SAMPLE_MEAN LPAREN NUM RPAREN
    {
      current_sample_create($3);
      printf ("%g\n%s", gsl_stats_mean(current_sample, 1, ncurrent_samples), PROMPT);
      fflush (stdout);
    }
  | SAMPLE_VARIANCE LPAREN NUM RPAREN
    {
      current_sample_create($3);
      printf ("%g\n%s", gsl_stats_variance(current_sample, 1, ncurrent_samples), PROMPT);
      fflush (stdout);
    }
  ;

sample_command :
    SAMPLE LPAREN NUM COMMA NUM COMMA NUM RPAREN
    {
      unsigned int iterations, i;
      int low, high;
      unsigned int *count;
      int nbins, bin;
      double r;
      
      iterations = (unsigned int)$3;
      low = (int)$5;
      high = (int)$7;

      /* Build a histogram by drawing random numbers. */
      nbins = high - low;
      count = g_new0 (unsigned int, nbins);
      for (i = 0; i < iterations; i++)
	{
	  r = PDF_random (current_dist, rng);
	  bin = (int) (floor (r - low));
	  if (bin >= 0 && bin < nbins)
	    count[bin]++;
	}

      printf ("%g", (double) count[0] / iterations);
      for (i = 1; i < nbins; i++)
        printf (" %g", (double) count[i] / iterations);
      printf ("\n%s", PROMPT);
      fflush (stdout);

      g_free (count);
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
  gsl_rng *gsl_format_rng;

  g_log_set_handler ("prob_dist", G_LOG_LEVEL_MESSAGE | G_LOG_LEVEL_INFO | G_LOG_LEVEL_DEBUG, silent_log_handler, NULL);

  /* Initialize the pseudo-random number generator. */
  gsl_rng_env_setup();
  gsl_format_rng = gsl_rng_alloc (gsl_rng_taus2);
  gsl_rng_set (gsl_format_rng, time(NULL));
  rng = RAN_new_generator (gsl_format_rng);

  printf (PROMPT);
  if (yyin == NULL)
    yyin = stdin;
  while (!feof(yyin))
    yyparse();

  RAN_free_generator (rng);
  return EXIT_SUCCESS;
}

/* end of file shell.y */
