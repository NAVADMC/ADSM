/** @file trace_zone_focus_model.h
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @version 0.1
 * @date June 2006
 *
 * Copyright &copy; University of Guelph, 2006
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#ifndef TRACE_ZONE_FOCUS_MODEL_H
#define TRACE_ZONE_FOCUS_MODEL_H

adsm_module_t *trace_zone_focus_model_new (sqlite3 *, UNT_unit_list_t *,
                                           projPJ, ZON_zone_list_t *);

#endif
