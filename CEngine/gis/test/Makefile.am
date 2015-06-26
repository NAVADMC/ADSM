## Makefile.am -- Process this file with automake to produce Makefile.in

AM_CPPFLAGS = -I.. @GLIB_CFLAGS@ @GSL_CFLAGS@

AM_YFLAGS = -d -v

noinst_PROGRAMS = shell fcmp
shell_SOURCES = shell.y scanner.l ../gis.c ../gis.h
shell_LDADD = @GLIB_LIBS@

fcmp_SOURCES = fcmp.c
fcmp_LDADD = @GLIB_LIBS@ @GSL_LIBS@

# Include the DejaGnu test files in the distribution file.

EXTRA_DIST = config/unix.exp libgis.all/*.exp
