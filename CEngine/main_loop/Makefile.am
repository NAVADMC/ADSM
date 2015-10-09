## Makefile.am -- Process this file with automake to produce Makefile.in

AM_CPPFLAGS = -I$(top_srcdir) \
  -I$(top_srcdir)/replace \
  -I$(top_srcdir)/unit \
  -I$(top_srcdir)/event \
  -I$(top_srcdir)/prob_dist \
  -I$(top_srcdir)/rel_chart \
  -I$(top_srcdir)/gis \
  -I$(top_srcdir)/reporting \
  -I$(top_srcdir)/rng \
  -I$(top_srcdir)/spatial_search \
  -I$(top_srcdir)/zone \
  -I$(top_srcdir)/wml \
  -I$(top_srcdir)/general \
  -I$(top_srcdir)/modules
if USE_SC_GUILIB
  AM_CPPFLAGS +=  -I$(top_srcdir)/sc_guilib 
endif
AM_CPPFLAGS += @GLIB_CFLAGS@ @GSL_CFLAGS@ @JSON_GLIB_CFLAGS@

include_HEADERS = adsm.h
lib_LIBRARIES = libadsm.a
libadsm_a_SOURCES = main_loop.c module_loader.c module_loader.h \
  event_manager.c event_manager.h \
  sqlite3_exec_dict.c sqlite3_exec_dict.h \
  parameter.c parameter.h \
  adsm.c adsm.h \
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
  libadsm_a_SOURCES += $(top_srcdir)/sc_guilib/production_type_data.c \
    $(top_srcdir)/sc_guilib/production_type_data.h \
    $(top_srcdir)/sc_guilib/sc_guilib_outputs.c \
    $(top_srcdir)/sc_guilib/sc_guilib_outputs.h \
    $(top_srcdir)/sc_guilib/sc_database.c \
    $(top_srcdir)/sc_guilib/sc_database.h
endif

bin_PROGRAMS = adsm
adsm_SOURCES = cli.c
adsm_LDADD = libadsm.a @GLIB_LIBS@ @GSL_LIBS@ @SQLITE_LIBS@ @JSON_GLIB_LIBS@
