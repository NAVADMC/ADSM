/** @file trace_exam_model.h
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @version 0.1
 * @date March 2008
 *
 * Copyright &copy; University of Guelph, 2008
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */



#ifndef TRACE_EXAM_MODEL_H
#define TRACE_EXAM_MODEL_H

spreadmodel_model_t *trace_exam_model_new (sqlite3 *, UNT_unit_list_t *,
                                           projPJ, ZON_zone_list_t *);

#endif
