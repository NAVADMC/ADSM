/** @file replace.c
 * This file provides copies of functions that may not be available on specific
 * systems.
 */

#include "replace.h"

#if HAVE_ERRNO_H
# include <errno.h>
#endif

#if HAVE_LIMITS_H
# include <limits.h>
#endif

#if HAVE_STDLIB_H
# include <stdlib.h>
#endif



#ifndef HAVE_GETSTR
/* Always add at least this many bytes when extending the buffer.  */
#define MIN_CHUNK 64

/* Read up to (and including) a delimiter DELIM1 from STREAM into *LINEPTR
   + OFFSET (and NUL-terminate it).  If DELIM2 is non-zero, then read up
   and including the first occurrence of DELIM1 or DELIM2.  *LINEPTR is
   a pointer returned from malloc (or NULL), pointing to *N characters of
   space.  It is realloc'd as necessary.  Return the number of characters
   read (not including the NUL terminator), or -1 on error or EOF.  */

int
getstr (char **lineptr, size_t * n, FILE * stream, int delim1, int delim2, size_t offset)
{
  size_t nchars_avail;          /* Allocated but unused chars in *LINEPTR.  */
  char *read_pos;               /* Where we're reading into *LINEPTR. */
  int ret;

  if (!lineptr || !n || !stream)
    return -1;

  if (!*lineptr)
    {
      *n = MIN_CHUNK;
      *lineptr = malloc (*n);
      if (!*lineptr)
        return -1;
    }

  if (*n < offset)
    return -1;

  nchars_avail = *n - offset;
  read_pos = *lineptr + offset;

  for (;;)
    {
      register int c = getc (stream);

      /* We always want at least one char left in the buffer, since we
         always (unless we get an error while reading the first char)
         NUL-terminate the line buffer.  */

      if (nchars_avail < 2)
        {
          if (*n > MIN_CHUNK)
            *n *= 2;
          else
            *n += MIN_CHUNK;

          nchars_avail = *n + *lineptr - read_pos;
          *lineptr = realloc (*lineptr, *n);
          if (!*lineptr)
            return -1;
          read_pos = *n - nchars_avail + *lineptr;
        }

      if (c == EOF || ferror (stream))
        {
          /* Return partial line, if any.  */
          if (read_pos == *lineptr)
            return -1;
          else
            break;
        }

      *read_pos++ = c;
      nchars_avail--;

      if (c == delim1 || (delim2 && c == delim2))
        /* Return the line.  */
        break;
    }

  /* Done - NUL terminate and return the number of chars read.  */
  *read_pos = '\0';

  ret = read_pos - (*lineptr + offset);
  return ret;
}
#endif



#ifndef HAVE_GETDELIM
int
getdelim (char **lineptr, size_t * n, int delimiter, FILE * stream)
{
  return getstr (lineptr, n, stream, delimiter, 0, 0);
}
#endif



#ifndef HAVE_GETLINE
int
getline (char **lineptr, size_t * n, FILE * stream)
{
  return getdelim (lineptr, n, '\n', stream);
}
#endif



#ifndef HAVE_STRTOI
/**
 * Converts a string to an integer.  Relies on the presence of strtol.
 *
 * @param nptr a string.
 * @param endptr if this is not NULL, some error-handling information will be
 *   stored in this address.  See below.
 * @return an integer corresponding to the string.  If there are no digits in
 *  the string, we return 0, set errno=EINVAL, and set *endptr=nptr (if endptr
 *  is not null).  If there are invalid digits in the string, we return the
 *  value computed up to the first invalid digit and set *endptr to point to
 *  the first invalid character (if endptr is not NULL).  If underflow occurs,
 *  we return INT_MIN and set errno to ERANGE.  If overflow occurs, we return
 *  INT_MAX and set errno to ERANGE.  This mimics the behavior of strtol.
 */
int
strtoi (const char *nptr, char **endptr)
{
  long int n;
  int i = 0;

  /* If nptr is null, follow the behavior for no digits seen. */
  if (nptr == NULL)
    {
      errno = EINVAL;
      if (endptr != NULL)
        *endptr = (char *) nptr;
    }
  else
    {
      n = strtol (nptr, endptr, 10);
      if (errno == ERANGE)
        {
          /* The string was outside the range that a long int can represent. */
          if (n == LONG_MIN)
            i = INT_MIN;
          else if (n == LONG_MAX)
            i = INT_MAX;
        }
      else if ((endptr != NULL && *endptr == nptr) || errno == EINVAL)
        {
          /* No digits seen, therefore no conversion was performed. */
          ;
        }
      else if (n < INT_MIN)
        {
          /* The string was smaller than the smallest value that an int can
           * represent. */
          errno = ERANGE;
          i = INT_MIN;
        }
      else if (n > INT_MAX)
        {
          /* The string was larger than the largest value that an int can
           * represent. */
          errno = ERANGE;
          i = INT_MAX;
        }
      else
        i = (int) n;
    }
  return i;
}
#endif

/* end of file replace.c */
