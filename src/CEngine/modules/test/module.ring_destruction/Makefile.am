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

EXTRA_DIST = radius_0.xml radius_0.5.xml radius_1.xml radius_2.5.xml \
 spread.xml spread_radius_1.xml spread_delay_1_radius_1.xml \
 spread_delay_2_radius_1.xml none_trigger_none_dest.xml \
 cattle_trigger_cattle_dest.xml cattle_trigger_pigs_dest.xml \
 cattle_trigger_both_dest.xml pigs_trigger_cattle_dest.xml \
 pigs_trigger_pigs_dest.xml pigs_trigger_both_dest.xml \
 both_trigger_cattle_dest.xml both_trigger_pigs_dest.xml \
 both_trigger_both_dest.xml trigger_small_ring.xml trigger_large_ring.xml \
 quarantine_waiting_0.xml quarantine_waiting_1.xml \
 early_exit_1.xml early_exit_2.xml early_exit_3.xml \
 early_exit_4.xml early_exit_5.xml early_exit_6.xml \
 lat_and_rtree.xml early_exit_2_disease_outbreak_end.xml \
 early_exit_3_disease_outbreak_end.xml \
 initially_destroyed.xml \
 initially_destroyed_avg_wait.xml
