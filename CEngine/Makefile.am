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
  filters \
  dll \
  doc
mandir= $(exec_prefix)/man
man1_MANS=spreadmodel.1
EXTRA_DIST = Doxyfile doxygen.css spreadmodel.1 INSTALL.html
