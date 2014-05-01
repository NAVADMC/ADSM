/** @file weekly_gis_writer.h
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date Mar 2014
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#ifndef WEEKLY_GIS_WRITER_H
#define WEEKLY_GIS_WRITER_H

adsm_module_t *weekly_gis_writer_new (sqlite3 *, UNT_unit_list_t *,
                                      projPJ, ZON_zone_list_t *);

#endif
