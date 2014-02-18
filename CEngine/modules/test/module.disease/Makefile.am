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

EXTRA_DIST = disease_1.xml disease_2.xml disease_3.xml disease_2species.xml \
  disease_2species_same_params.xml disease_neg_days.xml override_days_left.xml \
  prevalence_default.xml prevalence_1.xml prevalence_2.xml \
  vaccine_prevents_infection_0.xml vaccine_prevents_infection_1.xml \
  no_early_exit_1.xml \
  early_exit_1.xml early_exit_2.xml early_exit_3.xml early_exit_4.xml \
  natural_immunity_prevents_infection_0.xml \
  natural_immunity_prevents_infection_1.xml \
  disease_0days.xml disease_2species_same_params_w_vars.xml \
  disease_2species_same_params_w_vars2.xml
