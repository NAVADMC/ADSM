/** @file module_loader.h
 * Interface for module_loader.c.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date March 2003
 *
 * Copyright &copy; University of Guelph, 2003-2006
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#ifndef MODULE_LOADER_H
#define MODULE_LOADER_H

#include "module.h"



/* Prototypes. */
int adsm_load_modules (sqlite3 *parameter_db,
                       UNT_unit_list_t *, projPJ, ZON_zone_list_t *,
                       unsigned int *ndays, unsigned int *nruns,
                       adsm_module_t *** models, GPtrArray * outputs, guint *_exit_conditions);
void adsm_unload_modules (int nmodels, adsm_module_t ** models);

#endif /* !MODULE_LOADER_H */
