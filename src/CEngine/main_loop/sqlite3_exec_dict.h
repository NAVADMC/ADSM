/** @file sqlite3_exec_dict.h
 * Interface for sqlite3_exec_dict.c.
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#ifndef SQLITE3_EXEC_DICT_H
#define SQLITE3_EXEC_DICT_H

#include <glib.h>
#include <sqlite3.h>



/**
 * Type of a function used for callbacks.
 */
typedef int (*sqlite3_exec_dict_callback_t) (void *, GHashTable *);



/* Prototypes. */
int sqlite3_exec_dict (sqlite3 *, const char *sql,
                       sqlite3_exec_dict_callback_t callback,
                       void *user_data, char **errmsg);

#endif /* !SQLITE3_EXEC_DICT_H */
