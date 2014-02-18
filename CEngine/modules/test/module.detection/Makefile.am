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

EXTRA_DIST = detected_1.xml detected_1_w_vars.xml \
  undetected_1.xml undetected_1_w_vars.xml \
  detected_2.xml detected_3.xml days_awareness_0.xml days_awareness_low1.xml \
  days_awareness_1daypast.xml days_awareness_2dayspast.xml \
  days_awareness_3dayspast.xml days_awareness_2dayspast_2.xml \
  days_awareness_2dayspast_3.xml \
  detected_half_the_time.xml \
  trace_rfc_example_1a.xml trace_rfc_example_2.xml \
  trace_rfc_example_1a_firstdet.xml trace_rfc_example_2_firstdet.xml \
  trace_rfc_example_1a_exams.xml trace_rfc_example_2_exams.xml \
  trace_rfc_example_7_exams.xml \
  trace_rfc_example_1a_tests.xml trace_rfc_example_2_tests.xml \
  test_sensitivity_fail_latent.xml \
  test_sensitivity_fail_latent_w_vars.xml \
  test_sensitivity_succeed_latent.xml \
  test_sensitivity_succeed_latent_w_vars.xml \
  test_sensitivity_fail_subclinical.xml \
  test_sensitivity_fail_subclinical_w_vars.xml \
  test_sensitivity_succeed_subclinical.xml \
  test_sensitivity_succeed_subclinical_w_vars.xml \
  test_sensitivity_fail_clinical.xml \
  test_sensitivity_fail_clinical_w_vars.xml \
  test_sensitivity_succeed_clinical.xml \
  test_sensitivity_succeed_clinical_w_vars.xml \
  test_sensitivity_fail_nimmune.xml \
  test_sensitivity_fail_nimmune_w_vars.xml \
  test_sensitivity_succeed_nimmune.xml \
  test_sensitivity_succeed_nimmune_w_vars.xml \
  test_specificity_fail_susceptible.xml \
  test_specificity_fail_susceptible_w_vars.xml \
  test_specificity_succeed_susceptible.xml \
  test_specificity_succeed_susceptible_w_vars.xml \
  test_specificity_fail_vimmune.xml \
  test_specificity_fail_vimmune_w_vars.xml \
  test_specificity_succeed_vimmune.xml \
  test_specificity_succeed_vimmune_w_vars.xml \
  test_destroyed_baseline.xml \
  test_destroyed_baseline_w_vars.xml \
  test_destroyed.xml \
  test_destroyed_w_vars.xml \
  trace_to_prev_detected_unit_0.xml trace_to_prev_detected_unit.xml \
  exam_and_self_reporting_same_day.xml \
  test_result_and_self_reporting_same_day.xml \
  test_result_and_self_reporting_same_day2.xml \
  test_result_after_self_reporting.xml \
  trace_back_count_exams.xml \
  inf_at_first_det_1.xml inf_at_first_det_2.xml inf_at_first_det_no_det.xml
