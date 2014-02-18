/** @file mpix.h
 * Interface for mpix.c.
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
#ifndef MPIX_H
#define MPIX_H

#include <mpi.h>

#define ROOT 0



/** Simple global access to rank & number of processors. */
struct
{
  int rank;
  int np;
}
me;



/* Prototypes. */
int MPIx_Init (int *argc, char ***argv);
int MPI_Bcaststr (char **s, int rank, MPI_Comm comm);
int MPI_Bcastd (void **buffer, int count, MPI_Datatype datatype, int rank, MPI_Comm comm);

#endif /* !MPIX_H */
