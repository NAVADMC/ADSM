/** @file spatial_search_rtree.h
 * An object to encapsulate a spatial search algorithm.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */
#ifndef SPATIAL_SEARCH_RTREE_H
#define SPATIAL_SEARCH_RTREE_H

#include "spatial_search.h"

spatial_search_t *new_rtree_spatial_search (void);

#endif /* !SPATIAL_SEARCH_RTREE_H */
