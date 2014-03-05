## Makefile.am -- Process this file with automake to produce Makefile.in

AM_CPPFLAGS = -I.. -I$(top_srcdir)/main_loop -I$(top_srcdir)/unit -I$(top_srcdir)/rel_chart -I$(top_srcdir)/gis \
  -I$(top_srcdir)/rng \
  -I$(top_srcdir)/spatial_search \
  -I$(top_srcdir)/event -I$(top_srcdir)/reporting -I$(top_srcdir)/general -I$(top_srcdir)/sc_guilib -I$(top_srcdir)/zone  @GLIB_CFLAGS@ @GSL_CFLAGS@ @SCEW_CFLAGS@

AM_YFLAGS = -d -v

bin_PROGRAMS = \
  shp2png \
  shp2png2
shp2png_SOURCES = shp2png.c
shp2png_LDADD = -lshp -lgd @GLIB_LIBS@
shp2png2_SOURCES = shp2png2.c
shp2png2_LDADD = -lshp -lgd @GLIB_LIBS@
