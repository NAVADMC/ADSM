## Makefile.am -- Process this file with automake to produce Makefile.in

SUBDIRS = . \
  module.disease \
  module.direct_contact_spread \
  module.indirect_contact_spread \
  module.airborne_spread \
  module.detection \
  module.control_measures \
  module.ring_destruction \
  module.ring_vaccination \
  module.zones \
  module.economic

AM_CPPFLAGS = -I$(top_srcdir) \
  -I$(top_srcdir)/main_loop \
  -I$(top_srcdir)/replace \
  -I$(top_srcdir)/unit \
  -I$(top_srcdir)/event \
  -I$(top_srcdir)/prob_dist \
  -I$(top_srcdir)/rel_chart \
  -I$(top_srcdir)/gis \
  -I$(top_srcdir)/reporting \
  -I$(top_srcdir)/spatial_search \
  -I$(top_srcdir)/zone \
  -I$(top_srcdir)/rng \
  -I$(top_srcdir)/wml \
  -I$(top_srcdir)/general \
  -I$(top_srcdir)/modules
if USE_SC_GUILIB
  AM_CPPFLAGS +=  -I$(top_srcdir)/sc_guilib
endif
AM_CPPFLAGS += @GLIB_CFLAGS@ @GSL_CFLAGS@ @JSON_GLIB_CFLAGS@

# Create a program just like the real simulator for running small tests.

noinst_PROGRAMS = miniadsm shell shell2 fcmp

miniadsm_SOURCES = $(top_srcdir)/main_loop/cli.c $(top_srcdir)/main_loop/main_loop.c \
  $(top_srcdir)/main_loop/module_loader.c $(top_srcdir)/main_loop/module_loader.h \
  $(top_srcdir)/main_loop/event_manager.c $(top_srcdir)/main_loop/event_manager.h \
  $(top_srcdir)/main_loop/sqlite3_exec_dict.c $(top_srcdir)/main_loop/sqlite3_exec_dict.h \
  $(top_srcdir)/main_loop/parameter.c $(top_srcdir)/main_loop/parameter.h \
  $(top_srcdir)/main_loop/adsm.c $(top_srcdir)/main_loop/adsm.h \
  $(top_srcdir)/replace/replace.c $(top_srcdir)/replace/replace.h \
  $(top_srcdir)/general/general.c $(top_srcdir)/general/general.h \
  $(top_srcdir)/unit/unit.c $(top_srcdir)/unit/unit.h \
  $(top_srcdir)/event/event.c $(top_srcdir)/event/event.h \
  $(top_srcdir)/prob_dist/prob_dist.c $(top_srcdir)/prob_dist/prob_dist.h \
  $(top_srcdir)/rel_chart/rel_chart.c $(top_srcdir)/rel_chart/rel_chart.h \
  $(top_srcdir)/gis/gis.c $(top_srcdir)/gis/gis.h \
  $(top_srcdir)/reporting/reporting.c $(top_srcdir)/reporting/reporting.h \
  $(top_srcdir)/rng/rng.c $(top_srcdir)/rng/rng.h \
  $(top_srcdir)/spatial_search/spatial_search_rtree.c $(top_srcdir)/spatial_search/spatial_search_rtree.h \
  $(top_srcdir)/spatial_search/spatial_search.h \
  $(top_srcdir)/spatial_search/rTreeIndex.c $(top_srcdir)/spatial_search/rTreeIndex.h \
  $(top_srcdir)/spatial_search/ch2d.c $(top_srcdir)/spatial_search/ch2d.h \
  $(top_srcdir)/zone/zone.c $(top_srcdir)/zone/zone.h \
  $(top_srcdir)/wml/wml.c $(top_srcdir)/wml/wml.h \
  $(top_srcdir)/modules/module.h $(top_srcdir)/modules/module.c \
  $(top_srcdir)/modules/module_util.c $(top_srcdir)/modules/module_util.h \
  $(top_srcdir)/modules/population_model.c $(top_srcdir)/modules/population_model.h \
  $(top_srcdir)/modules/disease_model.c $(top_srcdir)/modules/disease_model.h \
  $(top_srcdir)/modules/contact_spread_model.c $(top_srcdir)/modules/contact_spread_model.h \
  $(top_srcdir)/modules/contact_recorder_model.c $(top_srcdir)/modules/contact_recorder_model.h \
  $(top_srcdir)/modules/airborne_spread_model.c $(top_srcdir)/modules/airborne_spread_model.h \
  $(top_srcdir)/modules/detection_model.c $(top_srcdir)/modules/detection_model.h \
  $(top_srcdir)/modules/vaccine_model.c $(top_srcdir)/modules/vaccine_model.h \
  $(top_srcdir)/modules/resources_and_implementation_of_controls_model.c $(top_srcdir)/modules/resources_and_implementation_of_controls_model.h \
  $(top_srcdir)/modules/quarantine_model.c $(top_srcdir)/modules/quarantine_model.h \
  $(top_srcdir)/modules/basic_destruction_model.c $(top_srcdir)/modules/basic_destruction_model.h \
  $(top_srcdir)/modules/ring_destruction_model.c $(top_srcdir)/modules/ring_destruction_model.h \
  $(top_srcdir)/modules/number_of_detections_vaccination_trigger.c $(top_srcdir)/modules/number_of_detections_vaccination_trigger.h \
  $(top_srcdir)/modules/detection_rate_vaccination_trigger.c $(top_srcdir)/modules/detection_rate_vaccination_trigger.h \
  $(top_srcdir)/modules/estimated_dissemination_rate_vaccination_trigger.c $(top_srcdir)/modules/estimated_dissemination_rate_vaccination_trigger.h \
  $(top_srcdir)/modules/days_since_first_detection_vaccination_trigger.c $(top_srcdir)/modules/days_since_first_detection_vaccination_trigger.h \
  $(top_srcdir)/modules/number_of_groups_vaccination_trigger.c $(top_srcdir)/modules/number_of_groups_vaccination_trigger.h \
  $(top_srcdir)/modules/destruction_wait_time_vaccination_trigger.c $(top_srcdir)/modules/destruction_wait_time_vaccination_trigger.h \
  $(top_srcdir)/modules/number_of_detections_vaccination_stop_trigger.c $(top_srcdir)/modules/number_of_detections_vaccination_stop_trigger.h \
  $(top_srcdir)/modules/ring_vaccination_model.c $(top_srcdir)/modules/ring_vaccination_model.h \
  $(top_srcdir)/modules/trace_model.c $(top_srcdir)/modules/trace_model.h \
  $(top_srcdir)/modules/trace_destruction_model.c $(top_srcdir)/modules/trace_destruction_model.h \
  $(top_srcdir)/modules/trace_quarantine_model.c $(top_srcdir)/modules/trace_quarantine_model.h \
  $(top_srcdir)/modules/trace_exam_model.c $(top_srcdir)/modules/trace_exam_model.h \
  $(top_srcdir)/modules/test_model.c $(top_srcdir)/modules/test_model.h \
  $(top_srcdir)/modules/zone_model.c $(top_srcdir)/modules/zone_model.h \
  $(top_srcdir)/modules/basic_zone_focus_model.c $(top_srcdir)/modules/basic_zone_focus_model.h \
  $(top_srcdir)/modules/trace_zone_focus_model.c $(top_srcdir)/modules/trace_zone_focus_model.h \
  $(top_srcdir)/modules/economic_model.c $(top_srcdir)/modules/economic_model.h \
  $(top_srcdir)/modules/unit_state_monitor.c $(top_srcdir)/modules/unit_state_monitor.h \
  $(top_srcdir)/modules/destruction_monitor.c $(top_srcdir)/modules/destruction_monitor.h \
  $(top_srcdir)/modules/destruction_list_monitor.c $(top_srcdir)/modules/destruction_list_monitor.h \
  $(top_srcdir)/modules/trace_monitor.c $(top_srcdir)/modules/trace_monitor.h \
  $(top_srcdir)/modules/vaccination_monitor.c $(top_srcdir)/modules/vaccination_monitor.h \
  $(top_srcdir)/modules/vaccination_list_monitor.c $(top_srcdir)/modules/vaccination_list_monitor.h \
  $(top_srcdir)/modules/detection_monitor.c $(top_srcdir)/modules/detection_monitor.h \
  $(top_srcdir)/modules/exposure_monitor.c $(top_srcdir)/modules/exposure_monitor.h \
  $(top_srcdir)/modules/infection_monitor.c $(top_srcdir)/modules/infection_monitor.h \
  $(top_srcdir)/modules/zone_monitor.c $(top_srcdir)/modules/zone_monitor.h \
  $(top_srcdir)/modules/exam_monitor.c $(top_srcdir)/modules/exam_monitor.h \
  $(top_srcdir)/modules/test_monitor.c $(top_srcdir)/modules/test_monitor.h \
  $(top_srcdir)/modules/table_writer.c $(top_srcdir)/modules/table_writer.h \
  $(top_srcdir)/modules/full_table_writer.c $(top_srcdir)/modules/full_table_writer.h \
  $(top_srcdir)/modules/state_table_writer.c $(top_srcdir)/modules/state_table_writer.h \
  $(top_srcdir)/modules/exposures_table_writer.c $(top_srcdir)/modules/exposures_table_writer.h \
  $(top_srcdir)/modules/apparent_events_table_writer.c $(top_srcdir)/modules/apparent_events_table_writer.h \
  $(top_srcdir)/modules/weekly_gis_writer.c $(top_srcdir)/modules/weekly_gis_writer.h \
  $(top_srcdir)/modules/summary_gis_writer.c $(top_srcdir)/modules/summary_gis_writer.h
if USE_SC_GUILIB
  miniadsm_SOURCES += $(top_srcdir)/sc_guilib/production_type_data.c \
    $(top_srcdir)/sc_guilib/sc_guilib_outputs.c \
    $(top_srcdir)/sc_guilib/sc_database.c
endif
miniadsm_CPPFLAGS = $(AM_CPPFLAGS)
miniadsm_LDADD = @GLIB_LIBS@ @GSL_LIBS@ @SQLITE_LIBS@ @JSON_GLIB_LIBS@

shell_SOURCES = shell.c $(top_builddir)/replace/replace.c
shell_LDADD = @GLIB_LIBS@

shell2_SOURCES = shell2.c $(top_builddir)/replace/replace.c
shell2_LDADD = @GLIB_LIBS@

fcmp_SOURCES = fcmp.c
fcmp_LDADD = @GLIB_LIBS@ @GSL_LIBS@

# Create a C file for Doxygen that contains documentation for the test cases.
# Include that in the distribution file, but not the files that generated it.

dist_noinst_DATA = testsuite.c
testsuite_c_SOURCES = tests_start_tag.xml \
  module.disease/all.xml \
  module.direct_contact_spread/all.xml \
  module.indirect_contact_spread/all.xml \
  module.airborne_spread/all.xml \
  module.detection/all.xml \
  module.control_measures/all.xml \
  module.ring_destruction/all.xml \
  module.ring_vaccination/all.xml \
  module.zones/all.xml \
  module.economic/all.xml \
  tests_end_tag.xml

testsuite.c: $(testsuite_c_SOURCES)
	cat $^ | python xml2dox.py > $@

dist_noinst_SCRIPTS = xml2dox.py xml2expect.py

# Include the DejaGnu test files in the distribution file.

EXTRA_DIST = config/unix.exp 1unit.xml 2units.xml \
  2units_pigs_cattle_pigs_infected.xml 2units_pigs_cattle_all_infected.xml \
  2targets_same_dist_same_size.xml 2targets_same_dist_diff_size.xml \
  3units.xml 3units_2_at_same_loc.xml 3targets_same_dist_same_size.xml \
  3units_pigs_2cattle_pigs_infected.xml \
  3units_pigs_cattle_sheep_sheep_infected.xml \
  3units_pigs_cattle_sheep_pigs_sheep_infected.xml \
  3units_pigs_cattle_sheep_all_infected.xml \
  4units_line.xml 4units_all_infected.xml 4units_line_2.xml 4units_line_3.xml \
  4units_line_4.xml 4units_line_5_xy.xml 4units_2.xml 4units_2_reversed.xml \
  5units.xml 5units_2.xml 5units_very_close.xml 6units.xml 6units_2.xml 7units.xml \
  8units_all_infected.xml 8units_all_infected_diff_types.xml \
  8units_2rows.xml 8units_2rows_2.xml 8units_2rows_3.xml 8units_2rows_4.xml \
  9units.xml \
  9units_hexagon.xml \
  units_circle.xml units_circle2.xml 16units_square.xml 16units_2rings.xml \
  1unit_1dayleft.xml 1unit_3daysleft.xml \
  1unit_start_infectious.xml 1unit_start_infectious_1dayleft.xml \
  1unit_start_infectious_2daysleft.xml 1unit_start_subclinical.xml \
  1unit_start_infectious_1dayin.xml \
  1unit_start_infectious_1dayin_4daysleft.xml \
  2units_1_start_nimmune.xml 2units_1_start_nimmune_2daysleft.xml \
  2units_1_start_nimmune_3daysleft.xml 2units_1_start_vimmune.xml \
  2units_1_start_vimmune_1dayleft.xml 2units_1_start_vimmune_2daysleft.xml \
  2units_1_start_destroyed.xml \
  no_rtree_lat0.xml rtree_lat0.xml no_rtree_lat45.xml rtree_lat45.xml \
  no_rtree_lat_minus45.xml rtree_lat_minus45.xml \
  no_rtree_contact_spread.xml rtree_contact_spread.xml \
  2units_ascii.xml 2units_iso88591.xml 2units_utf8.xml 2units_utf8_no_bom.xml \
  2units_utf16_big_endian.xml 2units_utf16_big_endian_no_bom.xml \
  2units_utf16_little_endian.xml 2units_utf16_little_endian_no_bom.xml \
  2units_xy.xml 4units_line_xy.xml no_rtree_lat45_xy.xml rtree_lat45_xy.xml \
  3units_1_start_vimmune.xml \
  3units_1_start_destroyed.xml \
  $(testsuite_c_SOURCES)
