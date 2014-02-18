## Makefile.am -- Process this file with automake to produce Makefile.in

AM_CPPFLAGS = -I.. -I$(top_srcdir)/main_loop -I$(top_srcdir)/unit -I$(top_srcdir)/rel_chart -I$(top_srcdir)/gis \
  -I$(top_srcdir)/rng \
  -I$(top_srcdir)/spatial_search \
  -I$(top_srcdir)/event -I$(top_srcdir)/reporting -I$(top_srcdir)/general -I$(top_srcdir)/sc_guilib -I$(top_srcdir)/zone  @GLIB_CFLAGS@ @GSL_CFLAGS@ @SCEW_CFLAGS@

AM_YFLAGS = -d -v

bin_PROGRAMS = \
  table_filter \
  full_table_filter \
  exposures_table_filter \
  state_table_filter \
  xml2shp \
  weekly_gis_filter \
  summary_gis_filter \
  shp2png \
  shp2png2 \
  weekly_gis_zones_filter
table_filter_SOURCES = table.y scanner.l $(top_srcdir)/reporting/reporting.c
table_filter_LDADD = @GLIB_LIBS@ @GSL_LIBS@
full_table_filter_SOURCES = full_table.y scanner.l $(top_srcdir)/reporting/reporting.c
full_table_filter_LDADD = @GLIB_LIBS@ @GSL_LIBS@
exposures_table_filter_SOURCES = exposures_table.y scanner.l \
  $(top_srcdir)/unit/unit.c \
  $(top_srcdir)/rel_chart/rel_chart.c \
  $(top_srcdir)/reporting/reporting.c \
  $(top_srcdir)/replace/replace.c
if USE_SC_GUILIB
  exposures_table_filter_SOURCES += $(top_srcdir)/general/general.c \
    $(top_srcdir)/zone/zone.c \
    $(top_srcdir)/sc_guilib/production_type_data.c \
    $(top_srcdir)/sc_guilib/sc_guilib_outputs.c \
    $(top_srcdir)/sc_guilib/sc_database.c
endif
exposures_table_filter_LDADD = @GLIB_LIBS@ @GSL_LIBS@
if HAVE_MPI
exposures_table_filter_LDADD += @MPI_LIBS@
endif
state_table_filter_SOURCES = state_table.y scanner.l
state_table_filter_LDADD = @GLIB_LIBS@
xml2shp_SOURCES = xml2shp.c \
  $(top_srcdir)/unit/unit.c \
  $(top_srcdir)/rel_chart/rel_chart.c \
  $(top_srcdir)/replace/replace.c
if USE_SC_GUILIB
  xml2shp_SOURCES += $(top_srcdir)/general/general.c \
    $(top_srcdir)/zone/zone.c \
    $(top_srcdir)/sc_guilib/production_type_data.c \
    $(top_srcdir)/sc_guilib/sc_guilib_outputs.c \
    $(top_srcdir)/sc_guilib/sc_database.c
endif
xml2shp_LDADD = -lshp @GLIB_LIBS@ @GSL_LIBS@
if HAVE_MPI
xml2shp_LDADD += @MPI_LIBS@
endif
weekly_gis_filter_SOURCES = weekly_gis.y scanner.l \
  $(top_srcdir)/unit/unit.c \
  $(top_srcdir)/rel_chart/rel_chart.c \
  $(top_srcdir)/replace/replace.c
if USE_SC_GUILIB
  weekly_gis_filter_SOURCES += $(top_srcdir)/general/general.c \
    $(top_srcdir)/zone/zone.c \
    $(top_srcdir)/sc_guilib/production_type_data.c \
    $(top_srcdir)/sc_guilib/sc_guilib_outputs.c \
    $(top_srcdir)/sc_guilib/sc_database.c
endif
weekly_gis_filter_LDADD = -lshp @GLIB_LIBS@ @GSL_LIBS@
if HAVE_MPI
weekly_gis_filter_LDADD  += @MPI_LIBS@
endif
summary_gis_filter_SOURCES = summary_gis.y scanner.l \
  $(top_srcdir)/unit/unit.c \
  $(top_srcdir)/rel_chart/rel_chart.c \
  $(top_srcdir)/gis/gis.c \
  $(top_srcdir)/replace/replace.c
if USE_SC_GUILIB
  summary_gis_filter_SOURCES += $(top_srcdir)/general/general.c \
    $(top_srcdir)/zone/zone.c \
    $(top_srcdir)/sc_guilib/production_type_data.c \
    $(top_srcdir)/sc_guilib/sc_guilib_outputs.c \
    $(top_srcdir)/sc_guilib/sc_database.c
endif
summary_gis_filter_LDADD = -lshp @GLIB_LIBS@ @GSL_LIBS@
if HAVE_MPI
summary_gis_filter_LDADD  += @MPI_LIBS@
endif
shp2png_SOURCES = shp2png.c
shp2png_LDADD = -lshp -lgd @GLIB_LIBS@
shp2png2_SOURCES = shp2png2.c
shp2png2_LDADD = -lshp -lgd @GLIB_LIBS@
weekly_gis_zones_filter_SOURCES = weekly_gis_zones.y scanner.l
weekly_gis_zones_filter_LDADD = -lshp @GLIB_LIBS@

CLEANFILES = exposures_table.c exposures_table.h \
  exposures_table.output
