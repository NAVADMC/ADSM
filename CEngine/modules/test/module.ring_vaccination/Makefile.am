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

EXTRA_DIST = radius_0.xml radius_0_w_vars.xml radius_0point5.xml radius_1.xml \
 radius_2point5.xml radius_1_delay_1.xml radius_1_delay_2.xml \
 spread.xml spread_radius_1.xml spread_radius_2point5.xml spread_radius_10.xml \
 2species_same_params.xml 2species_diff_params.xml \
 revaccinate_0.xml revaccinate_1.xml \
 none_trigger_none_vacc.xml cattle_trigger_cattle_vacc.xml \
 cattle_trigger_pigs_vacc.xml cattle_trigger_both_vacc.xml \
 pigs_trigger_cattle_vacc.xml pigs_trigger_pigs_vacc.xml \
 pigs_trigger_both_vacc.xml both_trigger_cattle_vacc.xml \
 both_trigger_pigs_vacc.xml both_trigger_both_vacc.xml \
 trigger_small_ring.xml trigger_large_ring.xml \
 quarantine_waiting_0.xml quarantine_waiting_1.xml quarantine_waiting_2.xml \
 early_exit_1.xml early_exit_1_w_vars.xml \
 early_exit_2.xml early_exit_2_w_vars.xml \
 early_exit_3.xml early_exit_3_w_vars.xml \
 early_exit_4.xml early_exit_4_w_vars.xml early_exit_4_w_vars2.xml \
 early_exit_5.xml early_exit_5_w_vars.xml early_exit_5_w_vars2.xml \
 early_exit_6.xml early_exit_6_w_vars.xml early_exit_6_w_vars2.xml \
 destroyed_while_waiting_1.xml destroyed_while_waiting_1_w_vars.xml \
 destroyed_while_waiting_2.xml destroyed_while_waiting_2_w_vars.xml \
 destroyed_while_waiting_3.xml destroyed_while_waiting_3_w_vars.xml \
 destroyed_while_waiting_4_w_vars.xml \
 destroyed_while_waiting_4_w_vars2.xml \
 destroyed_while_waiting_4_w_vars3.xml \
 lat_and_rtree.xml spread_radius_10_w_vars.xml \
 destroyed_before_ring.xml destroyed_sameday_ring.xml \
 revaccinate_2_prodtypes.xml revaccinate_2_prodtypes_w_vars.xml \
 radius_0_vacc_detected_w_vars.xml \
 detected_before_ring_vacc_detected.xml \
 detected_before_ring_no_vacc_detected.xml \
 detected_sameday_ring_vacc_detected.xml \
 detected_sameday_ring_no_vacc_detected.xml \
 detected_sameday_ring_no_vacc_detected2.xml \
 detected_sameday_rings_no_vacc_detected.xml \
 detected_after_ring_no_vacc_detected.xml \
 detected_after_ring_no_vacc_detected2.xml \
 avg_wait_time.xml \
 initially_vimmune.xml \
 initially_vimmune_avg_wait.xml \
 in_queue_twice.xml in_queue_twice_1_canceled.xml in_queue_twice_both_canceled.xml \
 cancel_max_wait_0.xml cancel_max_wait_1.xml \
 same_unit_detected_twice_check_vacc_threshold.xml \
 trigger_1detect_in_anytype_8units_2rows_4.sqlite3 \
 trigger_3detect_in_anytype_8units_2rows_4.sqlite3 \
 trigger_2detect_in_typeA_8units_2rows_4.sqlite3 \
 trigger_3detect_in_typeA_8units_2rows_4.sqlite3 \
 trigger_1detect_in_typeBorC_8units_2rows_4.sqlite3 \
 trigger_1detect_in_typeC_8units_2rows_4.sqlite3 \
 trigger_3detect_in_typeA_or_2detect_in_typeBorC_8units_2rows_4.sqlite3 \
 trigger_4detect3days_in_anytype_8units_all_infected_diff_types.sqlite3 \
 trigger_6detect4days_in_anytype_8units_all_infected_diff_types.sqlite3 \
 trigger_1point5edr3days_in_anytype_8units_all_infected_diff_types.sqlite3 \
 trigger_1daysincedet_anytype_8units_all_infected_diff_types.sqlite3 \
 trigger_2daysincedet_anytype_8units_all_infected_diff_types.sqlite3 \
 trigger_2daysincedet_typeC_8units_all_infected_diff_types.sqlite3 \
 trigger_5daysincedet_typeA_3daysincedet_typeB_8units_all_infected_diff_types.sqlite3 \
 trigger_1groupAB_8units_all_infected_diff_types.sqlite3 \
 trigger_1groupCD_8units_all_infected_diff_types.sqlite3 \
 trigger_2groupsABC_EF_8units_all_infected_diff_types.sqlite3 \
 trigger_destwait1_cap0_8units_all_infected_diff_types.sqlite3 \
 trigger_destwait3_cap0_8units_all_infected_diff_types.sqlite3 \
 trigger_destwait3_cap3_8units_all_infected_diff_types.sqlite3 \
 stop_vac_3days_nostop_16units_2rings.sqlite3 \
 stop_vac_3days_1_16units_2rings.sqlite3 \
 stop_vac_3days_2_16units_2rings.sqlite3 \
 stop_vac_3days_restart_same_chart_16units_2rings.sqlite3 \
 stop_vac_3days_restart_diff_chart_16units_2rings.sqlite3 \
 vacc_3detect_retro0_8units_2rows.sqlite3 vacc_3detect_retro1_8units_2rows.sqlite3 \
 vacc_4detect_retro3_8units_2rows.sqlite3 \
 retrigger_2detect_16units_2rings.sqlite3 \
 retrigger_2detect6days_16units_2rings.sqlite3 \
 retrigger_7daysincedet_typeB_16units_2rings.sqlite3 \
 retrigger_1.5edr3days_in_typeB_20units_2rings.sqlite3 \
 retrigger_2groupsAC_BD_3daysincedet_16units_2rings.sqlite3 \
 retrigger_destwait2_nonewdetect_16units_2rings.sqlite3 \
 retrigger_destwait2_newdetect1_16units_2rings.sqlite3 \
 retrigger_destwait2_newdetect2_16units_2rings.sqlite3 \
 triggerfirstandrestart_2detect_16units_2rings.sqlite3 \
 triggerfirstonly_2detect_16units_2rings.sqlite3 \
 triggerrestartonly_2detect_16units_2rings.sqlite3 \
 triggerfirst_2detect_triggerrestart_1detect_16units_2rings.sqlite3 \
 vacc_request_from_exam_cancellation_from_test.xml \
 circle3_ring2-4_10units_2cols.sqlite3 \
 ring3-4_ring1-2_10units_2cols.sqlite3 \
 prot_ring_punch_holes_1_14units_2rings_overlap.sqlite3 \
 prot_ring_punch_holes_2_14units_2rings_overlap.sqlite3 \
 prot_ring_punch_holes_3_expiry_21units_3rings_overlap.sqlite3 \
 prot_and_supp_rings_15units_line.sqlite3 \
 prot_ring_not_punch_holes_in_supp_ring_15units_line.sqlite3 \
 vacc_readded_same_day_14units_2rings_overlap.sqlite3
