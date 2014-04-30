/** @file rng.c
 * Functions for getting random numbers.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date October 2005
 *
 * Copyright &copy; University of Guelph, 2005-2008
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#if HAVE_CONFIG_H
#  include <config.h>
#endif

#include "rng.h"

#include "adsm.h"



/**
 * Creates a new random number generator object.
 *
 * @param rng a GSL random number generator.
 * @return a random number generator.
 */
RAN_gen_t *
RAN_new_generator (gsl_rng *rng)
{
  RAN_gen_t *self;

  self = g_new (RAN_gen_t, 1);
  self->fixed = FALSE;
  self->rng = rng;

  return self;
}



/**
 * Returns a random number in [0,1).
 *
 * @param gen a random number generator.
 * @return a random number in [0,1).
 */
double
RAN_num (RAN_gen_t * gen)
{
  if (gen->fixed)
    return gen->fixed_value;
  else
    return gsl_rng_uniform (gen->rng);
}



/**
 * Returns a pointer that allows the generator to be used as a GNU Scientific
 * Library generator.
 *
 * @param gen a random number generator.
 * @return a GSL random number generator.
 */
gsl_rng *
RAN_generator_as_gsl (RAN_gen_t * gen)
{
  return gen->rng;
}



/**
 * Causes a random number generator to always return a particular value.
 *
 * @param gen a random number generator.
 * @param value the value to fix.
 */
void
RAN_fix (RAN_gen_t * gen, double value)
{
  gen->fixed = TRUE;
  gen->fixed_value = value;
}



/**
 * Causes a random number generator to return random values, reversing the
 * effect of RAN_fix().
 *
 * @param gen a random number generator.
 */
void
RAN_unfix (RAN_gen_t * gen)
{
  gen->fixed = FALSE;
}



/**
 * Deletes a random number generator from memory.
 *
 * @param gen a random number generator.
 */
void
RAN_free_generator (RAN_gen_t * gen)
{
  if (gen != NULL)
    {
      gsl_rng_free (gen->rng);
      g_free (gen);
    }
}


DLL_API void
set_rng_read_seed (TRngVoid_1_Int fn)
{
  rng_read_seed = fn;
}


void
clear_rng_fns (void)
{
  set_rng_read_seed (NULL);
}


/* end of file rng.c */
