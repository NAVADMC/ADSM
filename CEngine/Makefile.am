## Makefile.am -- Process this file with automake to produce Makefile.in

AUTOMAKE_OPTIONS = dejagnu

RUNTESTDEFAULTFLAGS = --srcdir $$srcdir/test

SUBDIRS = wml \
  rel_chart \
  gis \
  unit \
  prob_dist \
  reporting \
  modules \
  main_loop \
  dll \
  doc
mandir= $(exec_prefix)/man
man1_MANS=adsm.1
EXTRA_DIST = Doxyfile doxygen.css adsm.1 INSTALL.html
