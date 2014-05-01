/** @file unit_state_monitor.h
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#ifndef UNIT_STATE_MONITOR_H
#define UNIT_STATE_MONITOR_H

adsm_module_t *unit_state_monitor_new (sqlite3 *, UNT_unit_list_t *,
                                       projPJ, ZON_zone_list_t *);

#endif
