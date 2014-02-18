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

EXTRA_DIST = spread_1.xml no_spread_1.xml spread_2.xml \
 spread_delay_1.xml spread_delay_2.xml spread_delay_3.xml \
 spread_delay_1_then_2.xml \
 distance_0.xml distance_1.xml distance_2.xml \
 distance_3.xml distance_4.xml distance_5.xml direction_0.xml \
 direction_all.xml direction_n.xml direction_n_w_vars.xml direction_s.xml \
 direction_e.xml direction_w.xml div_zero.xml \
 spread_same_loc_1.xml spread_same_loc_2.xml spread_same_loc_3.xml \
 no_quarantine.xml no_quarantine_w_vars.xml quarantine_fast.xml \
 quarantine_slow.xml 2sources_1target_1.xml 2sources_1target_1_w_vars.xml \
 2sources_1target_2.xml 2sources_1target_2_w_vars.xml \
 2sources_1target_3.xml 2sources_1target_3_w_vars.xml \
 spread_1_exp.xml no_spread_1_exp.xml \
 2prod_types_to_neither.xml 2prod_types_to_cattle.xml \
 2prod_types_to_pigs.xml 2prod_types_to_both.xml \
 prev_default.xml prev_incr.xml
