## Makefile.am -- Process this file with automake to produce Makefile.in

AM_CPPFLAGS = -I.. \
 -I$(top_srcdir)/main_loop \
 -I$(top_srcdir)/unit \
 -I$(top_srcdir)/zone \
 -I$(top_srcdir)/rel_chart \
 -I$(top_srcdir)/gis \
 -I$(top_srcdir)/spatial_search \
 -I$(top_srcdir)/rng @GLIB_CFLAGS@ @GSL_CFLAGS@

AM_YFLAGS = -d -v

noinst_PROGRAMS = shell fcmp
shell_SOURCES = shell.y scanner.l ../prob_dist.c ../prob_dist.h \
  $(top_srcdir)/rng/rng.c $(top_srcdir)/rng/rng.h
shell_LDADD = @GLIB_LIBS@ @GSL_LIBS@
if HAVE_MPI
shell_LDADD += @MPI_LIBS@
endif

fcmp_SOURCES = fcmp.c
fcmp_LDADD = @GLIB_LIBS@ @GSL_LIBS@

# Include the DejaGnu test files in the distribution file.

EXTRA_DIST = config/unix.exp libprob_dist.all/*.exp
