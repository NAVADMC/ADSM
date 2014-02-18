/** @file exam_monitor.h
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date July 2009
 *
 * Copyright &copy; University of Guelph, 2009
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#ifndef EXAM_MONITOR_H
#define EXAM_MONITOR_H

spreadmodel_model_t *exam_monitor_new (scew_element * params, UNT_unit_list_t *,
                                       projPJ, ZON_zone_list_t *);

#endif
