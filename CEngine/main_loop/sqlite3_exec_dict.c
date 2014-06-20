/** @file sqlite3_exec_dict.c
 * A wrapper around sqlite3_exec that returns the retrieved rows in hash table
 * format so that lookups by column name are easy.
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#include "sqlite3_exec_dict.h"



typedef struct
{
  void *user_data;
  GHashTable *dict;
  sqlite3_exec_dict_callback_t callback;
}
intermediate_callback_args_t;



static
int intermediate_callback (void *loc, int ncols,
                           char **value, char **colname)
{
  intermediate_callback_args_t *args;
  void *user_data;
  GHashTable *dict;
  int i;

  args = (intermediate_callback_args_t *) loc;
  user_data = args->user_data;
  dict = args->dict;

  for (i = 0; i < ncols; i++)
    {
      g_hash_table_replace (dict, colname[i], value[i]);
    }

  args->callback (user_data, dict);
}



/**
 * Like sqlite3_exec, but returns the retrieved rows in hash table format
 * instead of a number of columns, array of column names, and array of values.
 *
 * @param db an open database
 * @param sql SQL to be evaluated
 * @param callback Callback function
 * @param user_data 1st argument to callback
 * @param errmsg Error msg written here
 * @return whatever sqlite3_exec returns
 */
int sqlite3_exec_dict (sqlite3* db, const char *sql,
                       int (*callback)(void*,GHashTable*),
                       void *user_data,
                       char **errmsg)
{
  int return_code;
  intermediate_callback_args_t args;

  args.user_data = user_data;
  /* The hash table does not need key or value destroy funcs because the keys
   * and values (both char * types) are owned by sqlite3. */
  args.dict = g_hash_table_new (g_str_hash, g_str_equal);
  args.callback = callback;

  return_code = sqlite3_exec (db, sql, intermediate_callback, &args, errmsg);

  g_hash_table_destroy (args.dict);

  return return_code;
}

/* end of file sqlite3_exec_dict.c */
