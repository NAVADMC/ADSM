## Makefile.am -- Process this file with automake to produce Makefile.in

# Create an Expect script from the XML description of tests.

# The Expect script for DejaGnu goes into the distribution file, so that a make
# check can be run after installation.  But the XML file from which the Expect
# script was generated is not needed in the distribution.

dist_noinst_DATA = all.exp

nodist_all_exp_SOURCES = ../tests_start_tag.xml all.xml ../tests_end_tag.xml

all.exp: $(nodist_all_exp_SOURCES)
	cat $^ | python ../xml2expect.py > $@

# Do include the test scenario parameter files in the distribution file.

EXTRA_DIST = no_zones.xml no_zones_w_vars.xml 1_zone_1_focus_w_vars.xml \
  2_zones_1_focus_w_vars.xml 1_zone_2_foci.xml 1_zone_2_foci_w_vars.xml \
  1_zone_2_foci_merge_w_vars.xml 2_zones_2_foci_w_vars.xml \
  2_zones_2_foci_merge1_w_vars.xml 2_zones_2_foci_merge2_w_vars.xml \
  3_foci_merge.xml 3_foci_merge_w_vars.xml 1_zone_13_foci.xml \
  1_zone_13_foci_w_vars.xml 1_zone_13_foci_merge_w_vars.xml \
  trace_0.xml trace_1.xml trace_1_w_vars.xml trace_1_merge_w_vars.xml \
  trace_cattle_w_vars.xml trace_pigs_w_vars.xml \
  detect_1_no_zones.xml detect_1_zones.xml no_zones_2.xml \
  shipping_separated_areas.xml shipping_joined_areas.xml \
  shipping_joined_areas_2.xml donut_0.xml donut_1.xml \
  higher_to_lower_0.xml higher_to_lower_1.xml \
  gingerbread_man_0.xml gingerbread_man_1.xml \
  2targets_same_dist_0.xml 2targets_same_dist_1.xml \
  movement_control_0.xml movement_control_1.xml \
  animal_days_in_zone_1.xml animal_days_in_zone_1_w_destr.xml \
  animal_days_in_zone_1_w_destr_limit.xml \
  animal_days_in_zone_2.xml animal_days_in_zone_2_w_destr.xml \
  rtree_test_1.xml zone_area_1.xml zone_area_2.xml zone_area_3.xml \
  zone_names_utf.xml \
  trace_0_nm.xml trace_1_nm.xml trace_1_nm_w_vars.xml trace_1_merge_nm_w_vars.xml \
  trace_cattle_nm_w_vars.xml trace_pigs_nm_w_vars.xml \
  zone_perimeter_1.xml zone_perimeter_2.xml zone_perimeter_3.xml \
  shipping_joined_areas_2_w_vars.xml \
  donut_holes_removed_2.xml \
  zone_nesting_1.xml zone_nesting_2.xml zone_nesting_3.xml zone_nesting_4.xml \
  zone_nesting_5.xml
