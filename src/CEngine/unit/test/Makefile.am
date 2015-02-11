## Makefile.am -- Process this file with automake to produce Makefile.in

AM_CPPFLAGS = -I.. -I$(top_srcdir)/main_loop -I$(top_srcdir)/rel_chart -I$(top_srcdir)/general -I$(top_srcdir)/zone \
  -I$(top_srcdir)/spatial_search \
  @GLIB_CFLAGS@ @GSL_CFLAGS@
if USE_SC_GUILIB
  AM_CPPFLAGS += -I$(top_srcdir)/sc_guilib -I$(top_srcdir)/gis
endif


AM_YFLAGS = -d -v

noinst_PROGRAMS = shell
shell_SOURCES = shell.y scanner.l ../unit.c \
  $(top_srcdir)/rel_chart/rel_chart.c \
  $(top_srcdir)/main_loop/sqlite3_exec_dict.c \
  $(top_srcdir)/replace/replace.c
if USE_SC_GUILIB
  shell_SOURCES += $(top_srcdir)/general/general.c \
    $(top_srcdir)/zone/zone.c \
    $(top_srcdir)/gis/gis.c \
    $(top_srcdir)/sc_guilib/production_type_data.c \
    $(top_srcdir)/sc_guilib/sc_guilib_outputs.c \
    $(top_srcdir)/sc_guilib/sc_database.c
endif
shell_LDADD = @GLIB_LIBS@ @GSL_LIBS@ @SQLITE_LIBS@

# Include the DejaGnu test files in the distribution file.

EXTRA_DIST = config/unix.exp libunit.all/*.exp
