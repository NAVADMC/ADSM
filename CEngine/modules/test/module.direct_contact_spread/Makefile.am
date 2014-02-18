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

EXTRA_DIST = spread_1.xml spread_2.xml spread_2_poisson.xml spread_3.xml \
  spread_4.xml spread_5.xml spread_1_w_vars.xml spread_5_w_vars.xml \
  no_spread_1.xml no_spread_2.xml no_spread_1_w_vars.xml no_spread_2_w_vars.xml \
  spread_dist_1.xml spread_dist_2.xml spread_dist_3.xml spread_dist_4.xml \
  spread_dist_5.xml spread_dist_6.xml spread_same_loc_1.xml \
  spread_same_loc_2.xml spread_same_loc_3.xml no_quarantine.xml \
  quarantine_fast.xml quarantine_slow.xml \
  spread_delay_1.xml  spread_delay_2.xml spread_delay_3.xml \
  spread_delay_1_then_2.xml \
  mult_exposure_1.xml mult_exposure_2.xml mult_exposure_2b.xml \
  fixed_rate_1.xml fixed_rate_2.xml fixed_rate_0.xml \
  fixed_rate_0.5.xml fixed_rate_0.33.xml \
  prevalence_1.xml prevalence_0.xml prevalence_day2.xml prevalence_day4.xml \
  advance_along_line_0.8.xml advance_along_line_0.9.xml \
  advance_along_line_0.95.xml drift.xml rtree_fallback.xml \
  spread_ascii.xml spread_ascii_w_vars.xml spread_iso88591_w_vars.xml \
  spread_utf8_w_vars.xml spread_utf8_no_bom_w_vars.xml \
  spread_utf16_big_endian_w_vars.xml spread_utf16_big_endian_no_bom_w_vars.xml \
  spread_utf16_little_endian_w_vars.xml spread_utf16_little_endian_no_bom_w_vars.xml
