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

EXTRA_DIST = spread_1.xml spread_2.xml spread_dist_1.xml spread_dist_2.xml \
  spread_dist_3.xml spread_dist_4.xml spread_dist_5.xml spread_dist_6.xml \
  spread_same_loc_1.xml spread_same_loc_2.xml spread_same_loc_3.xml \
  no_quarantine.xml quarantine_fast.xml quarantine_slow.xml \
  fixed_rate_1.xml fixed_rate_2.xml fixed_rate_0.xml \
  fixed_rate_0.5.xml fixed_rate_0.33.xml
