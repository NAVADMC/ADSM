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

EXTRA_DIST = delay_0.xml delay_1.xml delay_3.xml \
 delay_0_w_vars.xml delay_1_w_vars.xml delay_3_w_vars.xml \
 delay_0_limit_1.xml delay_0_limit_2.xml \
 delay_0_limit_1-4.xml delay_0_limit_1-4_w_vars.xml \
 delay_3_limit_1-4.xml delay_3_limit_1-4_w_vars.xml \
 delay_0_limit_0.xml trace_out_0.xml trace_out_1.xml \
 trace_out_success.xml trace_out_success_w_vars.xml \
 trace_out_failure.xml trace_out_failure_w_vars.xml \
 trace_out_failure_w_vars2.xml trace_out_failure_w_vars3.xml \
 trace_in_1.xml trace_out_2.xml \
 trace_out_delay_2_window_3.xml trace_out_delay_3_window_3.xml \
 trace_out_delay_4_window_3.xml priority_detect_nearby_trace.xml \
 trace_no_destroy_1.xml trace_no_destroy_2.xml trace_no_destroy_3.xml \
 trace_no_destroy_4.xml trace_no_destroy_5.xml \
 priority_nearby_detect_trace.xml priority_trace_detect_nearby.xml \
 destruction_list_3_units_3_reasons.xml \
 priority_prodtype_time_1.xml priority_prodtype_time_2.xml \
 priority_time_prodtype.xml \
 priority_prodtype_time_reason.xml priority_prodtype_reason_time.xml \
 priority_prodtype-1_time_reason.xml priority_reason_time_prodtype-1.xml \
 vacc_priority_prodtype_time_1.xml vacc_priority_prodtype_time_2.xml \
 vacc_priority_time_prodtype.xml vacc_dest_same_day.xml \
 vacc_dest_same_day_2.xml vacc_dest_same_day_3.xml vacc_dest_same_day_4.xml \
 vacc_threshold_0.xml vacc_threshold_1.xml vacc_threshold_2.xml \
 vacc_threshold_3.xml vacc_threshold_3_backtrack.xml \
 vacc_threshold_4_backtrack.xml \
 vacc_threshold_4_backtrack_4th_detection_by_test.xml \
 trace_out_1_nm.xml \
 trace_out_success_nm.xml trace_out_success_nm_w_vars.xml \
 trace_out_failure_nm.xml trace_out_failure_nm_w_vars.xml \
 trace_in_1_nm.xml trace_out_2_nm.xml \
 trace_out_delay_2_window_3_nm.xml trace_out_delay_3_window_3_nm.xml \
 trace_out_delay_4_window_3_nm.xml \
 trace_no_destroy_1_nm.xml trace_no_destroy_2_nm.xml trace_no_destroy_3_nm.xml \
 trace_no_destroy_4_nm.xml trace_no_destroy_5_nm.xml \
 priority_detect_nearby_trace_nm.xml priority_nearby_detect_trace_nm.xml \
 priority_trace_detect_nearby_nm.xml destruction_list_3_units_3_reasons_nm.xml \
 priority_prodtype_reason_time_nm.xml priority_prodtype_time_reason_nm.xml \
 priority_prodtype-1_time_reason_nm.xml priority_reason_time_prodtype-1_nm.xml \
 trace_in_success.xml trace_line_no_trace.xml trace_line_no_trace_w_vars.xml \
 trace_line_in_out_fail.xml trace_line_in_out_fail_w_vars.xml \
 trace_line_in_out_succeed.xml trace_line_in_out_succeed_w_vars.xml \
 trace_line_in_chain_reaction.xml trace_line_in_chain_reaction2.xml \
 trace_depends_on_source_1.xml trace_depends_on_source_2.xml \
 trace_depends_on_source_3.xml trace_depends_on_source_4.xml \
 trace_in_loop.xml \
 trace_out_results_delayed_0.xml trace_out_results_delayed_1.xml \
 trace_out_results_delayed_2.xml \
 trace_rfc_example_1a.xml trace_rfc_example_1b.xml trace_rfc_example_2.xml \
 trace_rfc_example_3.xml trace_rfc_example_4.xml trace_rfc_example_5.xml \
 trace_rfc_example_6.xml trace_rfc_example_6_w_vars.xml \
 trace_rfc_example_7.xml trace_rfc_example_7_w_vars.xml \
 trace_detect_only_direct_in.xml trace_detect_only_direct_out.xml \
 trace_detect_only_indirect_in.xml trace_detect_only_indirect_out.xml \
 trace_detect_only_direct.xml trace_detect_only_indirect.xml \
 trace_detect_only_in.xml trace_detect_only_out.xml \
 priority_prodtype_reason_time_firstdestr.xml \
 vacc_priority_time_prodtype_firstvacc.xml \
 trace_enable_only_direct_in.xml trace_enable_only_indirect_in.xml \
 trace_in_out_which_first.xml
