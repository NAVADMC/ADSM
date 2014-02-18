/** @file mpix.c
 * Terry Moreland-like extensions for MPI.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date March 2002
 *
 * Copyright &copy; University of Guelph, 2002-2006
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#if HAVE_CONFIG_H
#  include <config.h>
#endif

#include "mpix.h"

#if STDC_HEADERS
#  include <stdlib.h>
#endif

#include <string.h>



/**
 * Initializes the MPI libraries, and additionally stores the rank & number of
 * processors in an easy-to-access struct.
 *
 * @param argc pointer to main's argc.
 * @param argv pointer to main's argv.
 * @return an MPI status code.
 */
int
MPIx_Init (int *argc, char ***argv)
{
  int err;

  if ((err = MPI_Init (argc, argv)) == MPI_SUCCESS)
    {
      MPI_Comm_rank (MPI_COMM_WORLD, &me.rank);
      MPI_Comm_size (MPI_COMM_WORLD, &me.np);
    }
  return err;
}



/**
 * Broadcasts a dynamically-allocated string.  This is a bit of a pain because
 * we must broadcast its length first so that destination nodes can create a
 * place to put it.
 *
 * @param s a location in which to store the start of the string.
 * @param rank the sending processor.
 * @param comm the group of receiving processors.
 * @return an MPI status code.
 */
int
MPI_Bcaststr (char **s, int rank, MPI_Comm comm)
{
  int len, err;

  if (me.rank == rank)
    len = strlen (*s) + 1;

  if ((err = MPI_Bcast (&len, 1, MPI_INT, rank, comm)) == MPI_SUCCESS)
    {
      if (me.rank != rank)
        *s = (char *) malloc (len * sizeof (char));
      err = MPI_Bcast (*s, len, MPI_CHAR, rank, comm);
    }
  return err;
}



/**
 * Broadcasts dynamically-allocated data.  The destination nodes must allocate
 * space to store it.
 *
 * @param buffer a location in which to store the start of the data.
 * @param count count of the data being sent.
 * @param datatype type of the data being sent.
 * @param rank the sending processor.
 * @param comm the group of receiving processors.
 * @return an MPI status code.
 */
int
MPI_Bcastd (void **buffer, int count, MPI_Datatype datatype, int rank, MPI_Comm comm)
{
  int size;

  /* Broadcast the amount of space needed (only the sending node is likely to
   * have the correct value) */
  MPI_Bcast (&count, 1, MPI_INT, rank, comm);
  /* Allocate space on receiving nodes */
  if (me.rank != rank)
    {
      MPI_Type_size (datatype, &size);
      *buffer = malloc (count * size);
    }
  return MPI_Bcast (*buffer, count, datatype, rank, comm);
}

/* end of file mpix.c */
