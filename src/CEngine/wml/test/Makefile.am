## Makefile.am -- Process this file with automake to produce Makefile.in

AM_CPPFLAGS = -I.. @GLIB_CFLAGS@

AM_YFLAGS = -d -v

noinst_PROGRAMS = shell
shell_SOURCES = shell.y scanner.l ../wml.c
shell_LDADD = @GLIB_LIBS@

# Include the DejaGnu test files in the distribution file.

EXTRA_DIST = config/unix.exp libwml.convexhull/*.exp
