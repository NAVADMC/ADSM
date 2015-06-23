/** @file replace.h
 * Interface for replace.c.
 */

#ifndef REPLACE_H
#define REPLACE_H

#include <config.h>
#include <stdio.h>

#ifndef HAVE_GETSTR
int getstr (char **lineptr, size_t * n, FILE * stream, int delim1, int delim2, size_t offset);
#endif

#ifndef HAVE_GETDELIM
int getdelim (char **lineptr, size_t * n, int delimiter, FILE * stream);
#endif

#ifndef HAVE_GETLINE
int getline (char **lineptr, size_t * n, FILE * stream);
#endif

#ifndef HAVE_STRTOI
int strtoi (const char *nptr, char **endptr);
#endif

#endif /* !REPLACE_H */
