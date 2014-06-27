# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import re

# <codecell>

tables_code = """class DailyByProductionType(models.Model):
    iteration = models.IntegerField(blank=True, null=True,
        help_text='The iteration during which the outputs in this records where generated.', )
    production_type = models.ForeignKey(ProductionType,
        help_text='The identifier of the production type that these outputs apply to.', )
    day = models.IntegerField(blank=True, null=True,
        help_text='The day within the iteration on which these outputs were generated.', )
    transition_state_daily_unit_susceptible = models.IntegerField(blank=True, null=True,
        help_text='Number of units that are or become susceptible on the given day', )
    transition_state_daily_animal_susceptible = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units that are or become susceptible on the given day', )
    transition_state_daily_unit_latent = models.IntegerField(blank=True, null=True,
        help_text='Number of units that are or become latent on the given day', )
    transition_state_daily_animal_latent = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units that are or become latent on the given day', )
    transition_state_daily_unit_subclinical = models.IntegerField(blank=True, null=True,
        help_text='Number of units that are or become subclinically infectious on the given day', )
    transition_state_daily_animal_subclinical = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units that are or become infectious on the given day', )
    transition_state_daily_unit_clinical = models.IntegerField(blank=True, null=True,
        help_text='Number of units that are or become clinical on the given day', )
    transition_state_daily_animal_clinical = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units that are or become clinical on the given day', )
    transition_state_daily_unit_nat_immune = models.IntegerField(blank=True, null=True,
        help_text='Number of units that are or become naturally immune on the given day', )
    transition_state_daily_animal_nat_immune = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units that are or become naturally immune on the given day', )
    transition_state_daily_unit_vac_immune = models.IntegerField(blank=True, null=True,
        help_text='Number of units that are or become vaccine immuneon the given day', )
    transition_state_daily_animal_vac_immune = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units that are or become vaccine immune on the given day', )
    transition_state_daily_unit_destroyed = models.IntegerField(blank=True, null=True,
        help_text='Number of units that are destroyed on the given day', )
    transition_state_daily_animal_destroyed = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units that are destroyed on the given day', )
    transition_state_cum_unit_susceptible = models.IntegerField(blank=True, null=True,
        help_text='Number of units that are or become susceptible over the course of an iteration', )
    transition_state_cum_animal_susceptible = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units that are or become susceptible over the course of an iteration', )
    transition_state_cum_unit_latent = models.IntegerField(blank=True, null=True,
        help_text='Number of units that are or become latent over the course of an iteration', )
    transition_state_cum_animal_latent = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units that are or become latent over the course of an iteration', )
    transition_state_cum_unit_subclinical = models.IntegerField(blank=True, null=True,
        help_text='Number of units that are or become subclinically infectious over the course of an iteration', )
    transition_state_cum_animal_subclinical = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units that are or become infectious over the course of an iteration', )
    transition_state_cum_unit_clinical = models.IntegerField(blank=True, null=True,
        help_text='Number of units that are or become clinical over the course of an iteration', )
    transition_state_cum_animal_clinical = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units that are or become clinical over the course of an iteration', )
    transition_state_cum_unit_nat_immune = models.IntegerField(blank=True, null=True,
        help_text='Number of units that are or become naturally immune over the course of an iteration', )
    transition_state_cum_animal_nat_immune = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units that are or become naturally immune over the course of an iteration', )
    transition_state_cum_unit_vac_immune = models.IntegerField(blank=True, null=True,
        help_text='Number of units that are or become vaccine immune over the course of an iteration', )
    transition_state_cum_animal_vac_immune = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units that are or become vaccine immune over the course of an iteration', )
    transition_state_cum_unit_destroyed = models.IntegerField(blank=True, null=True,
        help_text='Number of units that are destroyed over the course of an iteration', )
    transition_state_cum_animal_destroyed = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units that are destroyed over the course of an iteration', )
    infection_new_unit_air = models.IntegerField(blank=True, null=True,
        help_text='(infections new units airborne) Number of units that become infected by airborne spread on a given day', )
    infection_new_animal_air = models.IntegerField(blank=True, null=True,
        help_text='(infections new animals airborne) Number of animals in units that become infected by airborne spread on a given day', )
    infection_new_unit_dir = models.IntegerField(blank=True, null=True,
        help_text='(infections new units direct)Number of units that become infected by direct contact on a given day', )
    infection_new_animal_dir = models.IntegerField(blank=True, null=True,
        help_text='(infections new animals direct)  Number of animals in units that become infected by direct contact on a given day', )
    infection_new_unit_ind = models.IntegerField(blank=True, null=True,
        help_text='(infections new animals indirect) Number of units that become infected by indirect contact on a given day', )
    infection_new_animal_ind = models.IntegerField(blank=True, null=True,
        help_text='(infections new animals indirect) Number of animals in units that become infected by indirect contact on a given day', )
    infection_cum_unit_initial = models.IntegerField(blank=True, null=True,
        help_text='Number of units that are initially infected at the beginning of an iteration', )
    infection_cum_animal_initial = models.IntegerField(blank=True, null=True,
        help_text='Number of animals in units that are initially infected at the beginning of an iteration', )
    infection_cum_unit_air = models.IntegerField(blank=True, null=True,
        help_text='Number of units that become infected by airborne spread over the course of an iteration', )
    infection_cum_animal_air = models.IntegerField(blank=True, null=True,
        help_text='Number of animals in units that become infected by airborne spread over the course of an iteration', )
    infection_cum_unit_dir = models.IntegerField(blank=True, null=True,
        help_text='Number of units that become infected by direct contact over the course of an iteration', )
    infection_cum_animal_dir = models.IntegerField(blank=True, null=True,
        help_text='Number of animals that become infected by direct contact over the course of an iteration', )
    infection_cum_unit_ind = models.IntegerField(blank=True, null=True,
        help_text='Number of units that become infected by indirect contact over the course of an iteration', )
    infection_cum_animal_ind = models.IntegerField(blank=True, null=True,
        help_text='Number of animals in units that become infected by indirect contact over the course of an iteration', )
    exposed_cum_unit_dir = models.IntegerField(blank=True, null=True,
        help_text='Total number of units directly exposed to any infected unit over the course of an iteration', )
    exposed_cum_animal_dir = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units directly exposed to any infected unit over the course of an iteration', )
    exposed_cum_unit_ind = models.IntegerField(blank=True, null=True,
        help_text='Total number of units indirectly exposed to any infected unit over the course of an iteration', )
    exposed_cum_animal_ind = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units indirectly exposed to any infected unit over the course of an iteration', )
    trace_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units directly exposed and successfully traced forward over the course of an iteration', )
    trace_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units directly exposed and successfully traced forward over the course of an iteration', )
    trace_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True,
        help_text='Number of units indirectly exposed and successfully traced forward over the course of an iteration', )
    trace_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units indirectly exposed and successfully traced forward over the course of an iteration', )
    trace_cum_unit_dir_p_fwd = models.IntegerField(blank=True, null=True,
        help_text='Number of units directly exposed that could possibly have been traced forward over the course of an iteration', )
    trace_cum_animal_dir_p_fwd = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units directly exposed that could possibly have been traced forward over the course of an iteration', )
    trace_cum_unit_ind_p_fwd = models.IntegerField(blank=True, null=True,
        help_text='Number of units indirectly exposed that could possibly have been traced forward over the course of an iteration', )
    trace_cum_animal_ind_p_fwd = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units indirectly exposed that could possibly have been traced forward over the course of an iteration', )
    trace_origin_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True,
        help_text='Number of trace-forwards of direct contact that originate at units of the designated type over the course of an iteration', )
    trace_origin_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True,
        help_text='Number of trace-forwards of indirect contact that originate at units of the designated type over the course of an iteration', )
    trace_origin_cum_unit_dir_back = models.IntegerField(blank=True, null=True,
        help_text='Number of trace-backs of direct contact that originate at units of the designated type over the course of an iteration', )
    trace_origin_cum_unit_ind_back = models.IntegerField(blank=True, null=True,
        help_text='Number of trace-backs of indirect contact that originate at units of the designated type over the course of an iteration', )
    trace_new_unit_dir_fwd = models.IntegerField(blank=True, null=True,
        help_text='(trace new Units Direct contact Forward trace) Total number of units directly exposed and successfully traced forward on the given day', )
    trace_new_animal_dir_fwd = models.IntegerField(blank=True, null=True,
        help_text='(trace new Animals Direct contact Forward trace) Total number of animals in all units directly exposed and successfully traced forward on the given day', )
    trace_new_unit_ind_fwd = models.IntegerField(blank=True, null=True,
        help_text='(trace new Units Indirect contact forward trace) Number of units indirectly exposed and successfully traced forward on the given day', )
    trace_new_animal_ind_fwd = models.IntegerField(blank=True, null=True,
        help_text='(trace new Animals Indirect contact forward trace) Total number of animals in all units indirectly exposed and successfully traced forward on the given day', )
    trace_cum_unit_dir_back = models.IntegerField(blank=True, null=True,
        help_text='Number of units successfully traced back from a detected unit after direct contact over the course of the iteration', )
    trace_cum_animal_dir_back = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units successfully traced back from a detected unit over the course of the iteration', )
    trace_cum_unit_ind_back = models.IntegerField(blank=True, null=True,
        help_text='Number of units successfully traced back from a detected unit after indirect contact over the course of the iteration', )
    trace_cum_animal_ind_back = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units successfully traced back from a detected unit after indirect contact over the course of the iteration', )
    trace_cum_unit_dir_p_back = models.IntegerField(blank=True, null=True,
        help_text='Number of units that could possibly have been traced back from a detected unit after direct contact over the course of the iteration', )
    trace_cum_animal_dir_p_back = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units that could possibly have been traced back from a detected unit after direct contact over the course of the iteration', )
    trace_cum_unit_ind_p_back = models.IntegerField(blank=True, null=True,
        help_text='Number of units that could possibly have been traced back from a detected unit after indirect contact over the course of the iteration', )
    trace_cum_animal_ind_p_back = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units that could possibly have been traced back from a detected unit after indirect contact over the course of the iteration', )
    trace_new_unit_dir_back = models.IntegerField(blank=True, null=True,
        help_text='(trace new Units direct contact backwards trace) Number of units successfully traced back from a detected unit after direct contact on the given day', )
    trace_new_animal_dir_back = models.IntegerField(blank=True, null=True,
        help_text='(trace new Units direct contact backwards trace) Total number of animals in units successfully traced back from a detected unit on the given day', )
    trace_new_u_ind_back = models.IntegerField(blank=True, null=True,
        help_text='(trace new Units Indirect contact backwards trace)  Number of units successfully traced back from a detected unit after indirect contact on the given day', )
    trace_new_animal_ind_back = models.IntegerField(blank=True, null=True,
        help_text='(trace new Units Indirect contact Backwards trace) Total number of animals in units successfully traced back from a detected unit after indirect contact on the given day', )
    trace_origin_new_unit_dir_fwd = models.IntegerField(blank=True, null=True,
        help_text='(Trace origin new units direct contact forward)  Number of trace-forwards of direct contact that originate at units of the designated type on the given day', )
    trace_origin_new_unit_ind_fwd = models.IntegerField(blank=True, null=True,
        help_text='Number of trace-backs of direct contact that originate at units of the designated type on the given day', )
    trace_origin_new_unit_dir_back = models.IntegerField(blank=True, null=True,
        help_text='Number of trace-forwards of indirect contact that originate at units of the designated type on the given day', )
    trace_origin_new_unit_ind_back = models.IntegerField(blank=True, null=True,
        help_text='Number of trace-backs of indirect contact that originate at units of the designated type on the given day', )
    exam_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True,
        help_text='Number of units subjected to a unit exam after a trace-forward of direct contact over the course of the iteration', )
    exam_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units subjected to a unit exam after a trace-forward of direct contact over the course of the iteration', )
    exam_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True,
        help_text='Number of units subjected to a unit exam after a trace-forward of indirect contact over the course of the iteration', )
    exam_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units subjected to a unit exam after a trace-forward of indirect contact over the course of the iteration', )
    exam_cum_unit_dir_back = models.IntegerField(blank=True, null=True,
        help_text='Number of units subjected to a unit exam after a trace-back of direct contact over the course of the iteration', )
    exam_cum_animal_dir_back = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units subjected to a unit exam after a trace-back of direct contact over the course of the iteration', )
    exam_cum_unit_ind_back = models.IntegerField(blank=True, null=True,
        help_text='Number of units subjected to a unit exam after a trace-back of indirect contact over the course of the iteration', )
    exam_cum_animal_ind_back = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units subjected to a unit exam after a trace-back of indirect contact over the course of the iteration', )
    exam_new_unit_all = models.IntegerField(blank=True, null=True,
        help_text='(exam new Units All)  Number of units examined for any reason on the given day.', )
    exam_new_animal_all = models.IntegerField(blank=True, null=True,
        help_text='(exam new Animals All)  Number of animals in units examined for any reason on the given day', )
    test_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True,
        help_text='Number of units subjected to diagnostic testing after a trace-forward of direct contact over the course of the iteration', )
    test_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units subjected to diagnostic testing after a trace-forward of direct contact over the course of the iteration', )
    test_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True,
        help_text='Number of units subjected to diagnostic testing after a trace-forward of indirect contact over the course of the iteration', )
    test_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units subjected to diagnostic testing after a trace-forward of indirect contact over the course of the iteration', )
    test_cum_unit_dir_back = models.IntegerField(blank=True, null=True,
        help_text='Number of units subjected to diagnostic testing after a trace-back of direct contact over the course of the iteration', )
    test_cum_animal_dir_back = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units subjected to diagnostic testing after a trace-back of direct contact over the course of the iteration', )
    test_cum_unit_ind_back = models.IntegerField(blank=True, null=True,
        help_text='Number of units subjected to diagnostic testing after a trace-back of indirect contact over the course of the iteration', )
    test_cum_animal_ind_back = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units subjected to diagnostic testing after a trace-back of indirect contact over the course of the iteration', )
    test_cum_unit_true_pos = models.IntegerField(blank=True, null=True,
        help_text='Number of tested units with a true positive diagnostic test result over the course of the iteration', )
    test_cum_animal_true_pos = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in tested units with a true positive diagnostic test result over the course of the iteration', )
    test_new_unit_true_pos = models.IntegerField(blank=True, null=True,
        help_text='(test new Units True Positive)  Number of tested units with a true positive diagnostic test on the given day.', )
    test_new_animal_true_pos = models.IntegerField(blank=True, null=True,
        help_text='(test new Animals True Positive)  Number of animals in tested units with a true positive diagnostic test on the given day.', )
    test_cum_unit_true_neg = models.IntegerField(blank=True, null=True,
        help_text='Number of tested units with a true negative diagnostic test result over the course of the iteration', )
    test_cum_animal_true_neg = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in tested units with a true negative diagnostic test result over the course of the iteration', )
    test_new_unit_true_neg = models.IntegerField(blank=True, null=True,
        help_text='(test cumulative Units True Negative) Number of tested units with a true negative diagnostic test result over the course of the iteration.', )
    test_new_animal_true_neg = models.IntegerField(blank=True, null=True,
        help_text='(test cumulative Animals True Negative) Total number of animals in tested units with a true negative diagnostic test result over the course of the iteration.', )
    test_cum_unit_false_pos = models.IntegerField(blank=True, null=True,
        help_text='Number of tested units with a false positive diagnostic test result over the course of the iteration', )
    test_cum_animal_false_pos = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in tested units with a false positive diagnostic test result over the course of the iteration', )
    test_new_unit_false_pos = models.IntegerField(blank=True, null=True,
        help_text='(test new Units False Positive) Number of tested units with a false positive diagnostic test on the given day.', )
    test_new_animal_false_pos = models.IntegerField(blank=True, null=True,
        help_text='(test new Animals False Positive) Number of animals in tested units with a false positive diagnostic test on the given day.', )
    test_cum_unit_false_neg = models.IntegerField(blank=True, null=True,
        help_text='Number of tested units with a false negative diagnostic test result over the course of the iteration', )
    test_cum_animal_false_neg = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in tested units with a false negative diagnostic test result over the course of the iteration', )
    test_new_unit_false_neg = models.IntegerField(blank=True, null=True,
        help_text='(test new Units False Negative) Number of tested units with a false negative diagnostic test on the given day.', )
    test_new_animal_false_neg = models.IntegerField(blank=True, null=True,
        help_text='(test new Animals False Negative) Number of animals in tested units with a false negative diagnostic test on the given day.', )
    detect_new_unit_clin = models.IntegerField(blank=True, null=True,
        help_text='Number of units detected by clinical signs on the given day', )
    detect_new_animal_clin = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units detected by clinical signs on the given day', )
    detect_cum_unit_clin = models.IntegerField(blank=True, null=True,
        help_text='Number of units detected by clinical signs over the course of an iteration', )
    detect_cum_animal_clin = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units detected by clinical signs over the course of an iteration', )
    detect_new_unit_test = models.IntegerField(blank=True, null=True,
        help_text='(detection new Units Tested)  Number of units detected by diagnostic testing on the given day.  This value includes true- as well as false-positive units.', )
    detect_new_animal_test = models.IntegerField(blank=True, null=True,
        help_text='(detection new Animals Tested)  Total number of animals in units detected by diagnostic testing on the given day.', )
    detect_cum_unit_test = models.IntegerField(blank=True, null=True,
        help_text='Number of units detected by diagnostic testing over the course of the iteration. This value includes true- as well as false-positive units', )
    detect_cum_animal_test = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units detected by diagnostic testing over the course of the iteration', )
    destroy_cum_unit_initial = models.IntegerField(blank=True, null=True,
        help_text='Number of units destroyed prior to the start of the simulation', )
    destroy_cum_animal_initial = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units destroyed prior to the start of the simulation', )
    destroy_cum_unit_detect = models.IntegerField(blank=True, null=True,
        help_text='Number of units destroyed because disease was detected over the course of an iteration', )
    destroy_cum_animal_detect = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units destroyed because disease was detected over the course of an iteration', )
    destroy_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True,
        help_text='Number of units destroyed due to a successful trace forward of direct contact with an infected unit over the course of the iteration', )
    destroy_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units destroyed due to a successful trace forward of direct contact with an infected unit over the course of the iteration', )
    destroy_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True,
        help_text='Number of units destroyed due to a successful trace forward of indirect contact with an infected unit over the course of the iteration', )
    destroy_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units destroyed due to a successful trace forward of indirect contact with an infected unit over the course of the iteration', )
    destroy_cum_unit_dir_back = models.IntegerField(blank=True, null=True,
        help_text='Number of units destroyed due to a successful trace back of direct contact with an infected unit over the course of the iteration', )
    destroy_cum_animal_dir_back = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units destroyed due to a successful trace back of direct contact with an infected unit over the course of the iteration', )
    destroy_cum_unit_ind_back = models.IntegerField(blank=True, null=True,
        help_text='Number of units destroyed due to a successful trace back of indirect contact with an infected unit over the course of the iteration', )
    destroy_cum_animal_ind_back = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units destroyed due to a successful trace back of indirect contact with an infected unit over the course of the iteration', )
    destroy_cum_unit_ring = models.IntegerField(blank=True, null=True,
        help_text='Number of units destroyed because they were in a destruction ring over the course of an iteration', )
    destroy_cum_animal_ring = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units destroyed because they were in a destruction ring over the course of an iteration', )
    destroy_new_unit_all = models.IntegerField(blank=True, null=True,
        help_text='Number of units that are new for a given day of all production types that have moved into tjhe destruction que.', )
    destroy_new_animal_all = models.IntegerField(blank=True, null=True,
        help_text='Number of animals that are new for a given day of all production types that have moved into tjhe destruction que.', )
    destroy_wait_unit_all = models.IntegerField(blank=True, null=True,
        help_text='(destruction waiting Units All)  Total number of units awaiting destruction on the indicated day.', )
    destroy_wait_animal_all = models.IntegerField(blank=True, null=True,
        help_text='(destruction waiting Animals All)  Total number of animals awaiting destruction on the indicated day.', )
    vac_cum_unit_initial = models.IntegerField(blank=True, null=True,
        help_text='Number of units that were vaccine immune prior to the start of the simulation', )
    vac_cum_animal_initial = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units that were vaccine immune prior to the start of the simulation', )
    vac_cum_unit_ring = models.IntegerField(blank=True, null=True,
        help_text='Number of units vaccinated in rings around detected-infected units over the course of an iteration', )
    vac_cum_animal_ring = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units vaccinated in rings around detected-infected units over the course of an iteration', )
    vac_new_unit_all = models.IntegerField(blank=True, null=True,
        help_text='Number of units vaccinated for any reason over the course of an iteration (not including initially infected units)', )
    vac_new_animal_all = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units vaccinated for any reason over the course of an iteration (not including initially infected units)', )
    vac_wait_unit_all = models.IntegerField(blank=True, null=True,
        help_text='(vaccination waiting Units All)  Total number of units awaiting vaccination on the indicated day.  Units that are present in the vaccination queue multiple times will count multiple times toward this total.', )
    vac_wait_animal_all = models.IntegerField(blank=True, null=True,
        help_text='(vaccination waiting Animals All)  Total number of animals awaiting vaccination on the indicated day.  Units that are present in the vaccination queue multiple times will count multiple times toward this total.', )
    zone_new_foci = models.IntegerField(blank=True, null=True,
        help_text='Total number of new zone foci created around units of the indicated type on the given day ', )
    zone_cum_foci = models.IntegerField(blank=True, null=True,
        help_text='Total number of new zone foci created around units of the indicated type over the course of an iteration', )


class DailyByZone(models.Model):
    iteration = models.IntegerField(blank=True, null=True,
        help_text='The iteration during which the outputs in this records where generated.', )
    day = models.IntegerField(blank=True, null=True,
        help_text='The day within the iteration on which these outputs were generated.', )
    zone = models.ForeignKey(Zone,
        help_text='Identifier of the zone for which this event occurred.', )
    zone_area = models.FloatField(blank=True, null=True,
        help_text='In square Kilometers', )
    zone_perimeter = models.FloatField(blank=True, null=True,
        help_text='In Kilometers', )


class DailyByZoneAndProductionType(models.Model):
    iteration = models.IntegerField(blank=True, null=True,
        help_text='The iteration during which the outputs in this records where generated.', )
    day = models.IntegerField(blank=True, null=True,
        help_text='The day within the iteration on which these outputs were generated.', )
    zone = models.ForeignKey(Zone,
        help_text='Identifier of the zone for which this event occurred.', )
    production_type = models.ForeignKey(ProductionType,
        help_text='The identifier of the production type that these outputs apply to.', )
    unit_days_in_zone = models.IntegerField(blank=True, null=True,
        help_text='Total number of unit days spent in a zone (1 unit for 1 day = 1 unit day 1 unit for 2 days = 2 unit days etc.)', )
    animal_days_in_zone = models.IntegerField(blank=True, null=True,
        help_text='Total number of animal days spent in a zone (1 animal for 1 day = 1 animal day 1 animal for 2 days = 2 animal days etc.)', )
    units_in_zone = models.IntegerField(blank=True, null=True,
        help_text='Number of units of the given production type in the zone', )
    animals_in_zone = models.IntegerField(blank=True, null=True,
        help_text='Count of animals of the given production type in the zone', )


class DailyEvents(models.Model):
    iteration = models.IntegerField(blank=True, null=True,
        help_text='The iteration during which the outputs in this records where generated.', )
    day = models.IntegerField(blank=True, null=True,
        help_text='The day within the iteration on which these outputs were generated.', )
    event = models.IntegerField(blank=True, null=True,
        help_text='A number used to identify each event.', )
    unit = models.ForeignKey(Unit,
        help_text='Identifier of the unit for which this event occurred.', )
    zone = models.ForeignKey(Zone,
        help_text='Identifier of the zone for which this event occurred.', )
    event_code = models.CharField(max_length=255, blank=True,
        help_text='Code to indicate the type of event.', )
    new_state_code = models.CharField(max_length=255, blank=True,
        help_text='For transition state changesthis field indicates the state that results from the event.', )
    test_result_code = models.CharField(max_length=255, blank=True,
        help_text='For trace events this field indicates if the attempted trace succeeded.', )


class DailyExposures(models.Model):
    iteration = models.IntegerField(blank=True, null=True,
        help_text='The iteration during which the outputs in this records where generated.', )
    day = models.IntegerField(blank=True, null=True,
        help_text='The day within the iteration on which these outputs were generated.', )
    exposure = models.IntegerField(blank=True, null=True,
        help_text='An identifier of each exposure.', )
    initiated_day = models.IntegerField(blank=True, null=True,
        help_text='', )
    exposed_unit = models.ForeignKey(Unit, related_name='events_where_unit_was_exposed',
        help_text='The identifier of the source unit for the exposure.', )
    exposed_zone = models.ForeignKey(Zone, related_name='events_that_exposed_this_zone',
        help_text='The identifier of the zone of the source unit for the exposure.', )
    exposing_unit = models.ForeignKey(Unit, related_name='events_where_unit_exposed_others',
        help_text='The identifier of the recipient unit for the exposure.', )
    exposing_zone = models.ForeignKey(Zone, related_name='events_that_exposed_others',
        help_text='The identifier of the zone of the recipient unit for the exposure.', )
    spread_method_code = models.CharField(max_length=255, blank=True,
        help_text='Code indicating the mechanism of the disease spread.', )
    is_adequate = models.NullBooleanField(blank=True, null=True,
        help_text='Indicator if the exposure was adequate to transmit dieases.', )  # Changed Booleans to NullBooleans so as not to restrict output
    exposing_unit_status_code = models.CharField(max_length=255, blank=True,
        help_text='Disease state of the exposing unit when the exposure occurred.', )
    exposed_unit_status_code = models.CharField(max_length=255, blank=True,
        help_text='Disease state of the exposed unit when the exposure occurred.', )


class EpidemicCurves(models.Model):
    iteration = models.IntegerField(blank=True, null=True,
        help_text='The iteration during which the outputs in this records where generated.', )
    day = models.IntegerField(blank=True, null=True,
        help_text='The day within the iteration on which these outputs were generated.', )
    production_type = models.ForeignKey(ProductionType,
        help_text='The identifier of the production type that these outputs apply to.', )
    infected_units = models.IntegerField(blank=True, null=True,
        help_text='The number of units of the specified production type infected by any mechanism on the specific day in a spcified iteration.', )
    infected_animals = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in an infected unit.', )
    detected_units = models.IntegerField(blank=True, null=True,
        help_text='The number of clinically ill units of the specified production type detected by any mechanism on the specified day in the specified iteration.', )
    detected_animals = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in the detected unit.', )
    infectious_units = models.IntegerField(blank=True, null=True,
        help_text='Number of infectious units both apparent and not apparent', )
    apparent_infectious_units = models.IntegerField(blank=True, null=True,
        help_text='APPARENT INFECTIOUS UNITS', )


class General(models.Model):
    simulation_start_time = models.DateTimeField(max_length=255, blank=True,
        help_text='The actual clock time according to the system clock of when the simulation started.', )
    simulation_end_time = models.DateTimeField(max_length=255, blank=True,
        help_text='The actual clock time according to the system clock of when the simulation ended.', )
    completed_iterations = models.IntegerField(blank=True, null=True,
        help_text='Number of iterations completed during the simulation run.', )
    version = models.CharField(max_length=255, blank=True,
        help_text='Number of the NAADSM Version used to run the simulation.', )


class Iteration(models.Model):
    iteration = models.IntegerField(blank=True, null=True,
        help_text='The iteration during which the outputs in this records where generated.', )
    disease_ended = models.NullBooleanField(blank=True, null=True,
        help_text='Indicator that disease spread has ended.', )  # Changed Booleans to NullBooleans so as not to restrict output
    disease_end_day = models.IntegerField(blank=True, null=True,
        help_text='Day of the end of disease spread.', )
    outbreak_ended = models.NullBooleanField(blank=True, null=True,
        help_text='Indicator that outbreak  has ended including all control measures supporting the scenario.', )  # Changed Booleans to NullBooleans so as not to restrict output
    outbreak_end_day = models.IntegerField(blank=True, null=True,
        help_text='Day of the end of the outbreak including all control measures supporting the scenario.', )
    zone_foci_created = models.NullBooleanField(blank=True, null=True,
        help_text='Indicator is a Zone focus was created', )  # Changed Booleans to NullBooleans so as not to restrict output
    destroy_wait_unit_max = models.IntegerField(blank=True, null=True,
        help_text='Maximum number of units in queue for destruction on any given day over the course of the iteration', )
    destroy_wait_unit_max_day = models.IntegerField(blank=True, null=True,
        help_text='The first simulation day on which the maximum number of units in queue for destruction was reached', )
    destroy_wait_animal_max = models.FloatField(blank=True, null=True,
        help_text='Maximum number of animals in queue for destruction on any given day over the course of the iteration', )
    destroy_wait_animal_max_day = models.IntegerField(blank=True, null=True,
        help_text='The first simulation day on which the maximum number of animals in queue for destruction was reached', )
    destroy_wait_unit_time_max = models.IntegerField(blank=True, null=True,
        help_text='Maximum number of days spent in queue for destruction by any single unit over the course of the iteration', )
    destroy_wait_unit_time_avg = models.FloatField(blank=True, null=True,
        help_text='Average number of days spent by each unit in queue for destruction over the course of the iteration', )
    vac_wait_unit_max = models.IntegerField(blank=True, null=True,
        help_text='Maximum number of units in queue for vaccination on any given day over the course of the iteration', )
    vac_wait_unit_max_day = models.IntegerField(blank=True, null=True,
        help_text='The first simulation day on which the maximum number of units in queue for vaccination was reached', )
    vac_wait_animal_max = models.FloatField(blank=True, null=True,
        help_text='Maximum number of animals in queue for vaccination on any given day over the course of the iteration', )
    vac_wait_animal_max_day = models.IntegerField(blank=True, null=True,
        help_text='The first simulation day on which the maximum number of animals in queue for vaccination was reached', )
    vac_wait_unit_time_max = models.IntegerField(blank=True, null=True,
        help_text='Maximum number of days spent in queue for vaccination by any single unit over the course of the iteration', )
    vac_wait_unit_time_avg = models.FloatField(blank=True, null=True,
        help_text='Average number of days spent in queue for vaccination by each unit that was vaccinated over the course of the iteration', )


class IterationByUnit(models.Model):
    iteration = models.IntegerField(blank=True, null=True,
        help_text='The iteration during which the outputs in this records where generated.', )
    unit = models.ForeignKey(Unit,
        help_text='Identifier of the unit for which this event occurred.', )
    last_status_code = models.CharField(max_length=255, blank=True,
        help_text='Final status that a unit was in for an iteration', )
    last_status_day = models.IntegerField(blank=True, null=True,
        help_text='Day that a unit was in the final status for an iteration', )
    last_control_state_code = models.CharField(max_length=255, blank=True,
        help_text='Final Control State that a unit was in for an iteration', )
    last_control_state_day = models.IntegerField(blank=True, null=True,
        help_text='Day that a unit went in to the final status for an iteration', )


class IterationByProductionType(models.Model):
    iteration = models.IntegerField(blank=True, null=True,
        help_text='The iteration during which the outputs in this records where generated.', )
    production_type = models.ForeignKey(ProductionType,
        help_text='The identifier of the production type that these outputs apply to.', )
    transition_state_cum_unit_susceptible = models.IntegerField(blank=True, null=True,
        help_text='Number of units that are or become susceptible over the course of an iteration', )
    transition_state_cum_animal_susceptible = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units that are or become susceptible over the course of an iteration', )
    transition_state_cum_unit_latent = models.IntegerField(blank=True, null=True,
        help_text='Number of units that are or become latent over the course of an iteration', )
    transition_state_cum_animal_latent = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units that are or become latent over the course of an iteration', )
    transition_state_cum_unit_subclinical = models.IntegerField(blank=True, null=True,
        help_text='Number of units that are or become subclinically infectious over the course of an iteration', )
    transition_state_cum_animal_subclinical = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units that are or become infectious over the course of an iteration', )
    transition_state_cum_unit_clinical = models.IntegerField(blank=True, null=True,
        help_text='Number of units that are or become clinical over the course of an iteration', )
    transition_state_cum_animal_clinical = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units that are or become clinical over the course of an iteration', )
    transition_state_cum_unit_nat_immune = models.IntegerField(blank=True, null=True,
        help_text='Number of units that are or become naturally immune over the course of an iteration', )
    transition_state_cum_animal_nat_immune = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units that are or become naturally immune over the course of an iteration', )
    transition_state_cum_unit_vac_immune = models.IntegerField(blank=True, null=True,
        help_text='Number of units that are or become vaccine immune over the course of an iteration', )
    transition_state_cum_animal_vac_immune = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units that are or become vaccine immune over the course of an iteration', )
    transition_state_cum_unit_destroyed = models.IntegerField(blank=True, null=True,
        help_text='Number of units that are destroyed over the course of an iteration', )
    transition_state_cum_animal_destroyed = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units that are destroyed over the course of an iteration', )
    infection_cum_unit_initial = models.IntegerField(blank=True, null=True,
        help_text='Number of units that are initially infected at the beginning of an iteration', )
    infection_cum_animal_initial = models.IntegerField(blank=True, null=True,
        help_text='Number of animals in units that are initially infected at the beginning of an iteration', )
    infection_cum_unit_air = models.IntegerField(blank=True, null=True,
        help_text='Number of units that become infected by airborne spread over the course of an iteration', )
    infection_cum_animal_air = models.IntegerField(blank=True, null=True,
        help_text='Number of animals in units that become infected by airborne spread over the course of an iteration', )
    infection_cum_unit_dir = models.IntegerField(blank=True, null=True,
        help_text='Number of units that become infected by direct contact over the course of an iteration', )
    infection_cum_animal_dir = models.IntegerField(blank=True, null=True,
        help_text='Number of animals that become infected by direct contact over the course of an iteration', )
    infection_cum_unit_ind = models.IntegerField(blank=True, null=True,
        help_text='Number of units that become infected by indirect contact over the course of an iteration', )
    infection_cum_animal_ind = models.IntegerField(blank=True, null=True,
        help_text='Number of animals in units that become infected by indirect contact over the course of an iteration', )
    exposed_cum_unit_dir = models.IntegerField(blank=True, null=True,
        help_text='Total number of units directly exposed to any infected unit over the course of an iteration', )
    exposed_cum_animal_dir = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units directly exposed to any infected unit over the course of an iteration', )
    exposed_cum_unit_ind = models.IntegerField(blank=True, null=True,
        help_text='Total number of units indirectly exposed to any infected unit over the course of an iteration', )
    exposed_cum_animal_ind = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units indirectly exposed to any infected unit over the course of an iteration', )
    trace_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units directly exposed and successfully traced forward over the course of an iteration', )
    trace_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units directly exposed and successfully traced forward over the course of an iteration', )
    trace_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True,
        help_text='Number of units indirectly exposed and successfully traced forward over the course of an iteration', )
    trace_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units indirectly exposed and successfully traced forward over the course of an iteration', )
    trace_cum_unit_dir_p_fwd = models.IntegerField(blank=True, null=True,
        help_text='Number of units directly exposed that could possibly have been traced forward over the course of an iteration', )
    trace_cum_animal_dir_pfwd = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units directly exposed that could possibly have been traced forward over the course of an iteration', )
    trace_cum_unit_ind_p_fwd = models.IntegerField(blank=True, null=True,
        help_text='Number of units indirectly exposed that could possibly have been traced forward over the course of an iteration', )
    trace_cum_animal_ind_p_fwd = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units indirectly exposed that could possibly have been traced forward over the course of an iteration', )
    trace_cum_unit_dir_back = models.IntegerField(blank=True, null=True,
        help_text='Number of units successfully traced back from a detected unit after direct contact over the course of the iteration', )
    trace_cum_animal_dir_back = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units successfully traced back from a detected unit over the course of the iteration', )
    trace_cum_unit_ind_back = models.IntegerField(blank=True, null=True,
        help_text='Number of units successfully traced back from a detected unit after indirect contact over the course of the iteration', )
    trace_cum_animal_ind_back = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units successfully traced back from a detected unit after indirect contact over the course of the iteration', )
    trace_cum_unit_dir_p_back = models.IntegerField(blank=True, null=True,
        help_text='Number of units that could possibly have been traced back from a detected unit after direct contact over the course of the iteration', )
    trace_cum_animal_dir_pback = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units that could possibly have been traced back from a detected unit after direct contact over the course of the iteration', )
    trace_cum_unit_ind_p_back = models.IntegerField(blank=True, null=True,
        help_text='Number of units that could possibly have been traced back from a detected unit after indirect contact over the course of the iteration', )
    trace_cum_animal_ind_p_back = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units that could possibly have been traced back from a detected unit after indirect contact over the course of the iteration', )
    trace_origin_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True,
        help_text='Number of trace-forwards of direct contact that originate at units of the designated type over the course of an iteration', )
    trace_origin_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True,
        help_text='Number of trace-forwards of indirect contact that originate at units of the designated type over the course of an iteration', )
    trace_origin_cum_unit_dir_back = models.IntegerField(blank=True, null=True,
        help_text='Number of trace-backs of direct contact that originate at units of the designated type over the course of an iteration', )
    trace_origin_cum_unit_ind_back = models.IntegerField(blank=True, null=True,
        help_text='Number of trace-backs of indirect contact that originate at units of the designated type over the course of an iteration', )
    exam_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True,
        help_text='Number of units subjected to a unit exam after a trace-forward of direct contact over the course of the iteration', )
    exam_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units subjected to a unit exam after a trace-forward of direct contact over the course of the iteration', )
    exam_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True,
        help_text='Number of units subjected to a unit exam after a trace-forward of indirect contact over the course of the iteration', )
    exam_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units subjected to a unit exam after a trace-forward of indirect contact over the course of the iteration', )
    exam_cum_unit_dir_back = models.IntegerField(blank=True, null=True,
        help_text='Number of units subjected to a unit exam after a trace-back of direct contact over the course of the iteration', )
    exam_cum_animal_dir_back = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units subjected to a unit exam after a trace-back of direct contact over the course of the iteration', )
    exam_cum_unit_ind_back = models.IntegerField(blank=True, null=True,
        help_text='Number of units subjected to a unit exam after a trace-back of indirect contact over the course of the iteration', )
    exam_cum_animal_ind_back = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units subjected to a unit exam after a trace-back of indirect contact over the course of the iteration', )
    test_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True,
        help_text='Number of units subjected to diagnostic testing after a trace-forward of direct contact over the course of the iteration', )
    test_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units subjected to diagnostic testing after a trace-forward of direct contact over the course of the iteration', )
    test_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True,
        help_text='Number of units subjected to diagnostic testing after a trace-forward of indirect contact over the course of the iteration', )
    test_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units subjected to diagnostic testing after a trace-forward of indirect contact over the course of the iteration', )
    test_cum_unit_dir_back = models.IntegerField(blank=True, null=True,
        help_text='Number of units subjected to diagnostic testing after a trace-back of direct contact over the course of the iteration', )
    test_cum_animal_dir_back = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units subjected to diagnostic testing after a trace-back of direct contact over the course of the iteration', )
    test_cum_unit_ind_back = models.IntegerField(blank=True, null=True,
        help_text='Number of units subjected to diagnostic testing after a trace-back of indirect contact over the course of the iteration', )
    test_cum_animal_ind_back = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units subjected to diagnostic testing after a trace-back of indirect contact over the course of the iteration', )
    test_cum_unit_true_pos = models.IntegerField(blank=True, null=True,
        help_text='Number of tested units with a true positive diagnostic test result over the course of the iteration', )
    test_cum_animal_true_pos = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in tested units with a true positive diagnostic test result over the course of the iteration', )
    test_cum_unit_true_neg = models.IntegerField(blank=True, null=True,
        help_text='Number of tested units with a true negative diagnostic test result over the course of the iteration', )
    test_cum_animal_true_neg = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in tested units with a true negative diagnostic test result over the course of the iteration', )
    test_cum_unit_false_pos = models.IntegerField(blank=True, null=True,
        help_text='Number of tested units with a false positive diagnostic test result over the course of the iteration', )
    test_cum_animal_false_pos = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in tested units with a false positive diagnostic test result over the course of the iteration', )
    test_cum_unit_false_neg = models.IntegerField(blank=True, null=True,
        help_text='Number of tested units with a false negative diagnostic test result over the course of the iteration', )
    test_cum_animal_false_neg = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in tested units with a false negative diagnostic test result over the course of the iteration', )
    detect_cum_unit_clin = models.IntegerField(blank=True, null=True,
        help_text='Number of units detected by clinical signs over the course of an iteration', )
    detect_cum_animal_clin = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units detected by clinical signs over the course of an iteration', )
    detect_cum_unit_test = models.IntegerField(blank=True, null=True,
        help_text='Number of units detected by diagnostic testing over the course of the iteration. This value includes true- as well as false-positive units', )
    detect_cum_animal_test = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units detected by diagnostic testing over the course of the iteration', )
    destroy_cum_unit_initial = models.IntegerField(blank=True, null=True,
        help_text='Number of units destroyed prior to the start of the simulation', )
    destroy_cum_animal_initial = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units destroyed prior to the start of the simulation', )
    destroy_cum_unit_detect = models.IntegerField(blank=True, null=True,
        help_text='Number of units destroyed because disease was detected over the course of an iteration', )
    destroy_cum_animal_detect = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units destroyed because disease was detected over the course of an iteration', )
    destroy_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True,
        help_text='Number of units destroyed due to a successful trace forward of direct contact with an infected unit over the course of the iteration', )
    destroy_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units destroyed due to a successful trace forward of direct contact with an infected unit over the course of the iteration', )
    destroy_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True,
        help_text='Number of units destroyed due to a successful trace forward of indirect contact with an infected unit over the course of the iteration', )
    destroy_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units destroyed due to a successful trace forward of indirect contact with an infected unit over the course of the iteration', )
    destroy_cum_unit_dir_back = models.IntegerField(blank=True, null=True,
        help_text='Number of units destroyed due to a successful trace back of direct contact with an infected unit over the course of the iteration', )
    destroy_cum_animal_dir_back = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units destroyed due to a successful trace back of direct contact with an infected unit over the course of the iteration', )
    destroy_cum_unit_ind_back = models.IntegerField(blank=True, null=True,
        help_text='Number of units destroyed due to a successful trace back of indirect contact with an infected unit over the course of the iteration', )
    destroy_cum_animal_ind_back = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units destroyed due to a successful trace back of indirect contact with an infected unit over the course of the iteration', )
    destroy_cum_unit_ring = models.IntegerField(blank=True, null=True,
        help_text='Number of units destroyed because they were in a destruction ring over the course of an iteration', )
    destroy_cum_animal_ring = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units destroyed because they were in a destruction ring over the course of an iteration', )
    destroy_wait_unit_max = models.IntegerField(blank=True, null=True,
        help_text='Maximum number of units in queue for destruction on any given day over the course of the iteration', )
    destroy_wait_animal_max = models.IntegerField(blank=True, null=True,
        help_text='Maximum number of animals in queue for destruction on any given day over the course of the iteration', )
    destroy_wait_unit_max_day = models.IntegerField(blank=True, null=True,
        help_text='The first simulation day on which the maximum number of units in queue for destruction was reached', )
    destroy_wait_animal_max_day = models.IntegerField(blank=True, null=True,
        help_text='The first simulation day on which the maximum number of animals in queue for destruction was reached', )
    destroy_wait_unit_time_max = models.IntegerField(blank=True, null=True,
        help_text='Maximum number of days spent in queue for destruction by any single unit over the course of the iteration', )
    destroy_wait_unit_time_avg = models.FloatField(blank=True, null=True,
        help_text='Average number of days spent by each unit in queue for destruction over the course of the iteration', )
    destroy_wait_unit_days_in_queue = models.FloatField(blank=True, null=True,
        help_text='Total number of unit-days spent in queue for destruction', )
    destroy_wait_animal_days_in_queue = models.FloatField(blank=True, null=True,
        help_text='Total number of animal-days spent in queue for destruction', )
    vac_cum_unit_initial = models.IntegerField(blank=True, null=True,
        help_text='Number of units that were vaccine immune prior to the start of the simulation', )
    vac_cum_animal_initial = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in units that were vaccine immune prior to the start of the simulation', )
    vac_cum_unit_ring = models.IntegerField(blank=True, null=True,
        help_text='Number of units vaccinated in rings around detected-infected units over the course of an iteration', )
    vac_cum_animal_ring = models.IntegerField(blank=True, null=True,
        help_text='Total number of animals in all units vaccinated in rings around detected-infected units over the course of an iteration', )
    vac_wait_unit_max = models.IntegerField(blank=True, null=True,
        help_text='Maximum number of units in queue for vaccination on any given day over the course of the iteration', )
    vac_wait_animal_max = models.FloatField(null=True, blank=True,
        help_text='Maximum number of animals in queue for vaccination on any given day over the course of the iteration', )
    vac_wait_unit_max_day = models.IntegerField(blank=True, null=True,
        help_text='The first simulation day on which the maximum number of units in queue for vaccination was reached', )
    vac_wait_animal_max_day = models.IntegerField(blank=True, null=True,
        help_text='The first simulation day on which the maximum number of animals in queue for vaccination was reached', )
    vac_wait_unit_time_max = models.FloatField(null=True, blank=True,
        help_text='Maximum number of days spent in queue for vaccination by any single unit over the course of the iteration', )
    vac_wait_unit_time_avg = models.IntegerField(blank=True, null=True,
        help_text='Average number of days spent in queue for vaccination by each unit that was vaccinated over the course of the iteration', )
    zone_cum_foci = models.IntegerField(blank=True, null=True,
        help_text='Total number of new zone foci created around units of the indicated type over the course of an iteration',)
    first_detection = models.IntegerField(blank=True, null=True,
        help_text='Day of first detection of an infected unit in the specified iteration', )
    first_det_unit_inf = models.IntegerField(blank=True, null=True,
        help_text='Number of units already infected at the time of first detection of an infected unit of any production type in the specified iteration', )
    first_detect_animal_inf = models.IntegerField(blank=True, null=True,
        help_text='Number of animals in units already infected at the time of first detection of an infected unit of any production type in the specified iteration', )
    first_destruction = models.IntegerField(blank=True, null=True,
        help_text='Day of first destruction of a unit in the specified iteration', )
    first_vaccination = models.IntegerField(blank=True, null=True,
        help_text='Day of first vaccination of a unit in the specified iteration', )
    last_detection = models.IntegerField(blank=True, null=True,
        help_text='Day of last detection of an infected unit in the specified iteration', )


class IterationByZone(models.Model):
    iteration = models.IntegerField(blank=True, null=True,
        help_text='The iteration during which the outputs in this records where generated.', )
    zone = models.ForeignKey(Zone,
        help_text='Identifier of the zone for which this event occurred.', )
    max_zone_area = models.FloatField(blank=True, null=True,
        help_text='Maximum area (in square kilometers) reached for the indicated zone over the course of an iteration', )
    max_zone_area_day = models.IntegerField(blank=True, null=True,
        help_text='Day on which maximum area for the indicated zone is reached', )
    final_zone_area = models.FloatField(blank=True, null=True,
        help_text='Area (in square kilometers) of the indicated zone at the end of an iteration', )
    max_zone_perimeter = models.FloatField(blank=True, null=True,
        help_text='Maximum perimeter (in kilometers) reached for the indicated zone over the course of an iteration', )
    max_zone_perimeter_day = models.IntegerField(blank=True, null=True,
        help_text='Day on which maximum perimeter for the indicated zone is reached', )
    final_zone_perimeter = models.FloatField(blank=True, null=True,
        help_text='Perimeter (in kilometers) of the indicated zone at the end of an iteration', )


class IterationByZoneAndProductionType(models.Model):
    iteration = models.IntegerField(blank=True, null=True,
        help_text='The iteration during which the outputs in this records where generated.', )
    zone = models.ForeignKey(Zone,
        help_text='Identifier of the zone for which this event occurred.', )
    production_type = models.ForeignKey(ProductionType,
        help_text='The identifier of the production type that these outputs apply to.', )
    unit_days_in_zone = models.IntegerField(blank=True, null=True,
        help_text='Total number of unit days spent in a zone (1 unit for 1 day = 1 unit day 1 unit for 2 days = 2 unit days etc.)', )
    animal_days_in_zone = models.IntegerField(blank=True, null=True,
        help_text='Total number of animal days spent in a zone (1 animal for 1 day = 1 animal day 1 animal for 2 days = 2 animal days etc.)', )
    cost_surveillance = models.FloatField(blank=True, null=True,
        help_text='Total cost associated with surveillance in a zone over the course of an iteration.', )


class IterationCosts(models.Model):
    iteration = models.IntegerField(blank=True, null=True,
        help_text='The iteration during which the outputs in this records where generated.', )
    production_type = models.ForeignKey(ProductionType,
        help_text='The identifier of the production type that these outputs apply to.', )
    destroy_appraisal = models.FloatField(blank=True, null=True,
        help_text='Total cost of appraisal for all units destroyed over the course of an iteration.', )
    destroy_cleaning = models.FloatField(blank=True, null=True,
        help_text='Total cost of cleaning and disinfection for all units destroyed over the course of an iteration.', )
    destroy_euthanasia = models.FloatField(blank=True, null=True,
        help_text='Total cost of euthanasia for all animals in units destroyed over the course of an iteration.', )
    destroy_indemnification = models.FloatField(blank=True, null=True,
        help_text='Total cost of indemnification for all animals in units destroyed over the course of an iteration.', )
    destroy_disposal = models.FloatField(blank=True, null=True,
        help_text='Total cost of carcass disposal for all animals in units destroyed over the course of an iteration.', )
    vac_cum_setup = models.FloatField(blank=True, null=True,
        help_text='Total cost of vaccination setup for all units vaccinated over the course of an iteration.', )
    vac_cum_vaccination = models.FloatField(blank=True, null=True,
        help_text='Total cost of vaccination for all animals in units vaccinated over the course of an iteration.', )
"""



# <codecell>

from io import StringIO
StringIO("""hi there
how are you?""").readlines()

# <codecell>

name_conversion_table = StringIO("""General	GeneralID	GENERAL_ID
General	simulationStartTime	SIMULATION_START_TIME
General	simulationEndTime	SIMULATION_END_TIME
General	completedIterations	COMPLETED_ITERATIONS
General	version	VERSION
		
DailyByProductionType	iteration	ITERATION
DailyByProductionType	productionTypeID	_PRODUCTIONTYPEID
DailyByProductionType	day	DAY
DailyByProductionType	tsdUSusc	TRANSITION_STATE_DAILY_UNIT_SUSCEPTIBLE
DailyByProductionType	tsdASusc	TRANSITION_STATE_DAILY_ANIMAL_SUSCEPTIBLE
DailyByProductionType	tsdULat	TRANSITION_STATE_DAILY_UNIT_LATENT
DailyByProductionType	tsdALat	TRANSITION_STATE_DAILY_ANIMAL_LATENT
DailyByProductionType	tsdUSubc	TRANSITION_STATE_DAILY_UNIT_SUBCLINICAL
DailyByProductionType	tsdASubc	TRANSITION_STATE_DAILY_ANIMAL_SUBCLINICAL
DailyByProductionType	tsdUClin	TRANSITION_STATE_DAILY_UNIT_CLINICAL
DailyByProductionType	tsdAClin	TRANSITION_STATE_DAILY_ANIMAL_CLINICAL
DailyByProductionType	tsdUNImm	TRANSITION_STATE_DAILY_UNIT_NAT_IMMUNE
DailyByProductionType	tsdANImm	TRANSITION_STATE_DAILY_ANIMAL_NAT_IMMUNE
DailyByProductionType	tsdUVImm	TRANSITION_STATE_DAILY_UNIT_VAC_IMMUNE
DailyByProductionType	tsdAVImm	TRANSITION_STATE_DAILY_ANIMAL_VAC_IMMUNE
DailyByProductionType	tsdUDest	TRANSITION_STATE_DAILY_UNIT_DESTROYED
DailyByProductionType	tsdADest	TRANSITION_STATE_DAILY_ANIMAL_DESTROYED
DailyByProductionType	tscUSusc	TRANSITION_STATE_CUM_UNIT_SUSCEPTIBLE
DailyByProductionType	tscASusc	TRANSITION_STATE_CUM_ANIMAL_SUSCEPTIBLE
DailyByProductionType	tscULat	TRANSITION_STATE_CUM_UNIT_LATENT
DailyByProductionType	tscALat	TRANSITION_STATE_CUM_ANIMAL_LATENT
DailyByProductionType	tscUSubc	TRANSITION_STATE_CUM_UNIT_SUBCLINICAL
DailyByProductionType	tscASubc	TRANSITION_STATE_CUM_ANIMAL_SUBCLINICAL
DailyByProductionType	tscUClin	TRANSITION_STATE_CUM_UNIT_CLINICAL
DailyByProductionType	tscAClin	TRANSITION_STATE_CUM_ANIMAL_CLINICAL
DailyByProductionType	tscUNImm	TRANSITION_STATE_CUM_UNIT_NAT_IMMUNE
DailyByProductionType	tscANImm	TRANSITION_STATE_CUM_ANIMAL_NAT_IMMUNE
DailyByProductionType	tscUVImm	TRANSITION_STATE_CUM_UNIT_VAC_IMMUNE
DailyByProductionType	tscAVImm	TRANSITION_STATE_CUM_ANIMAL_VAC_IMMUNE
DailyByProductionType	tscUDest	TRANSITION_STATE_CUM_UNIT_DESTROYED
DailyByProductionType	tscADest	TRANSITION_STATE_CUM_ANIMAL_DESTROYED
DailyByProductionType	infnUAir	INFECTION_NEW_UNIT_AIR
DailyByProductionType	infnAAir	INFECTION_NEW_ANIMAL_AIR
DailyByProductionType	infnUDir	INFECTION_NEW_UNIT_DIR
DailyByProductionType	infnADir	INFECTION_NEW_ANIMAL_DIR
DailyByProductionType	infnUInd	INFECTION_NEW_UNIT_IND
DailyByProductionType	infnAInd	INFECTION_NEW_ANIMAL_IND
DailyByProductionType	infcUIni	INFECTION_CUM_UNIT_INITIAL
DailyByProductionType	infcAIni	INFECTION_CUM_ANIMAL_INITIAL
DailyByProductionType	infcUAir	INFECTION_CUM_UNIT_AIR
DailyByProductionType	infcAAir	INFECTION_CUM_ANIMAL_AIR
DailyByProductionType	infcUDir	INFECTION_CUM_UNIT_DIR
DailyByProductionType	infcADir	INFECTION_CUM_ANIMAL_DIR
DailyByProductionType	infcUInd	INFECTION_CUM_UNIT_IND
DailyByProductionType	infcAInd	INFECTION_CUM_ANIMAL_IND
DailyByProductionType	expcUDir	EXPOSED_CUM_UNIT_DIR
DailyByProductionType	expcADir	EXPOSED_CUM_ANIMAL_DIR
DailyByProductionType	expcUInd	EXPOSED_CUM_UNIT_IND
DailyByProductionType	expcAInd	EXPOSED_CUM_ANIMAL_IND
DailyByProductionType	trcUDirFwd	TRACE_CUM_UNIT_DIR_FWD
DailyByProductionType	trcADirFwd	TRACE_CUM_ANIMAL_DIR_FWD
DailyByProductionType	trcUIndFwd	TRACE_CUM_UNIT_IND_FWD
DailyByProductionType	trcAIndFwd	TRACE_CUM_ANIMAL_IND_FWD
DailyByProductionType	trcUDirpFwd	TRACE_CUM_UNIT_DIR_P_FWD
DailyByProductionType	trcADirpFwd	TRACE_CUM_ANIMAL_DIR_P_FWD
DailyByProductionType	trcUIndpFwd	TRACE_CUM_UNIT_IND_P_FWD
DailyByProductionType	trcAIndpFwd	TRACE_CUM_ANIMAL_IND_P_FWD
DailyByProductionType	tocUDirFwd	TRACE_ORIGIN_CUM_UNIT_DIR_FWD
DailyByProductionType	tocUIndFwd	TRACE_ORIGIN_CUM_UNIT_IND_FWD
DailyByProductionType	tocUDirBack	TRACE_ORIGIN_CUM_UNIT_DIR_BACK
DailyByProductionType	tocUIndBack	TRACE_ORIGIN_CUM_UNIT_IND_BACK
DailyByProductionType	trnUDirFwd	TRACE_NEW_UNIT_DIR_FWD
DailyByProductionType	trnADirFwd	TRACE_NEW_ANIMAL_DIR_FWD
DailyByProductionType	trnUIndFwd	TRACE_NEW_UNIT_IND_FWD
DailyByProductionType	trnAIndFwd	TRACE_NEW_ANIMAL_IND_FWD
DailyByProductionType	trcUDirBack	TRACE_CUM_UNIT_DIR_BACK
DailyByProductionType	trcADirBack	TRACE_CUM_ANIMAL_DIR_BACK
DailyByProductionType	trcUIndBack	TRACE_CUM_UNIT_IND_BACK
DailyByProductionType	trcAIndBack	TRACE_CUM_ANIMAL_IND_BACK
DailyByProductionType	trcUDirpBack	TRACE_CUM_UNIT_DIR_P_BACK
DailyByProductionType	trcADirpBack	TRACE_CUM_ANIMAL_DIR_P_BACK
DailyByProductionType	trcUIndpBack	TRACE_CUM_UNIT_IND_P_BACK
DailyByProductionType	trcAIndpBack	TRACE_CUM_ANIMAL_IND_P_BACK
DailyByProductionType	trnUDirBack	TRACE_NEW_UNIT_DIR_BACK
DailyByProductionType	trnADirBack	TRACE_NEW_ANIMAL_DIR_BACK
DailyByProductionType	trnUIndBack	TRACE_NEW_U_IND_BACK
DailyByProductionType	trnAIndBack	TRACE_NEW_ANIMAL_IND_BACK
DailyByProductionType	tonUDirFwd	TRACE_ORIGIN_NEW_UNIT_DIR_FWD
DailyByProductionType	tonUIndFwd	TRACE_ORIGIN_NEW_UNIT_IND_FWD
DailyByProductionType	tonUDirBack	TRACE_ORIGIN_NEW_UNIT_DIR_BACK
DailyByProductionType	tonUIndBack	TRACE_ORIGIN_NEW_UNIT_IND_BACK
DailyByProductionType	exmcUDirFwd	EXAM_CUM_UNIT_DIR_FWD
DailyByProductionType	exmcADirFwd	EXAM_CUM_ANIMAL_DIR_FWD
DailyByProductionType	exmcUIndFwd	EXAM_CUM_UNIT_IND_FWD
DailyByProductionType	exmcAIndFwd	EXAM_CUM_ANIMAL_IND_FWD
DailyByProductionType	exmcUDirBack	EXAM_CUM_UNIT_DIR_BACK
DailyByProductionType	exmcADirBack	EXAM_CUM_ANIMAL_DIR_BACK
DailyByProductionType	exmcUIndBack	EXAM_CUM_UNIT_IND_BACK
DailyByProductionType	exmcAIndBack	EXAM_CUM_ANIMAL_IND_BACK
DailyByProductionType	exmnUAll	EXAM_NEW_UNIT_ALL
DailyByProductionType	exmnAAll	EXAM_NEW_ANIMAL_ALL
DailyByProductionType	tstcUDirFwd	TEST_CUM_UNIT_DIR_FWD
DailyByProductionType	tstcADirFwd	TEST_CUM_ANIMAL_DIR_FWD
DailyByProductionType	tstcUIndFwd	TEST_CUM_UNIT_IND_FWD
DailyByProductionType	tstcAIndFwd	TEST_CUM_ANIMAL_IND_FWD
DailyByProductionType	tstcUDirBack	TEST_CUM_UNIT_DIR_BACK
DailyByProductionType	tstcADirBack	TEST_CUM_ANIMAL_DIR_BACK
DailyByProductionType	tstcUIndBack	TEST_CUM_UNIT_IND_BACK
DailyByProductionType	tstcAIndBack	TEST_CUM_ANIMAL_IND_BACK
DailyByProductionType	tstcUTruePos	TEST_CUM_UNIT_TRUE_POS
DailyByProductionType	tstcATruePos	TEST_CUM_ANIMAL_TRUE_POS
DailyByProductionType	tstnUTruePos	TEST_NEW_UNIT_TRUE_POS
DailyByProductionType	tstnATruePos	TEST_NEW_ANIMAL_TRUE_POS
DailyByProductionType	tstcUTrueNeg	TEST_CUM_UNIT_TRUE_NEG
DailyByProductionType	tstcATrueNeg	TEST_CUM_ANIMAL_TRUE_NEG
DailyByProductionType	tstnUTrueNeg	TEST_NEW_UNIT_TRUE_NEG
DailyByProductionType	tstnATrueNeg	TEST_NEW_ANIMAL_TRUE_NEG
DailyByProductionType	tstcUFalsePos	TEST_CUM_UNIT_FALSE_POS
DailyByProductionType	tstcAFalsePos	TEST_CUM_ANIMAL_FALSE_POS
DailyByProductionType	tstnUFalsePos	TEST_NEW_UNIT_FALSE_POS
DailyByProductionType	tstnAFalsePos	TEST_NEW_ANIMAL_FALSE_POS
DailyByProductionType	tstcUFalseNeg	TEST_CUM_UNIT_FALSE_NEG
DailyByProductionType	tstcAFalseNeg	TEST_CUM_ANIMAL_FALSE_NEG
DailyByProductionType	tstnUFalseNeg	TEST_NEW_UNIT_FALSE_NEG
DailyByProductionType	tstnAFalseNeg	TEST_NEW_ANIMAL_FALSE_NEG
DailyByProductionType	detnUClin	DETECT_NEW_UNIT_CLIN
DailyByProductionType	detnAClin	DETECT_NEW_ANIMAL_CLIN
DailyByProductionType	detcUClin	DETECT_CUM_UNIT_CLIN
DailyByProductionType	detcAClin	DETECT_CUM_ANIMAL_CLIN
DailyByProductionType	detnUTest	DETECT_NEW_UNIT_TEST
DailyByProductionType	detnATest	DETECT_NEW_ANIMAL_TEST
DailyByProductionType	detcUTest	DETECT_CUM_UNIT_TEST
DailyByProductionType	detcATest	DETECT_CUM_ANIMAL_TEST
DailyByProductionType	descUIni	DESTROY_CUM_UNIT_INITIAL
DailyByProductionType	descAIni	DESTROY_CUM_ANIMAL_INITIAL
DailyByProductionType	descUDet	DESTROY_CUM_UNIT_DETECT
DailyByProductionType	descADet	DESTROY_CUM_ANIMAL_DETECT
DailyByProductionType	descUDirFwd	DESTROY_CUM_UNIT_DIR_FWD
DailyByProductionType	descADirFwd	DESTROY_CUM_ANIMAL_DIR_FWD
DailyByProductionType	descUIndFwd	DESTROY_CUM_UNIT_IND_FWD
DailyByProductionType	descAIndFwd	DESTROY_CUM_ANIMAL_IND_FWD
DailyByProductionType	descUDirBack	DESTROY_CUM_UNIT_DIR_BACK
DailyByProductionType	descADirBack	DESTROY_CUM_ANIMAL_DIR_BACK
DailyByProductionType	descUIndBack	DESTROY_CUM_UNIT_IND_BACK
DailyByProductionType	descAIndBack	DESTROY_CUM_ANIMAL_IND_BACK
DailyByProductionType	descURing	DESTROY_CUM_UNIT_RING
DailyByProductionType	descARing	DESTROY_CUM_ANIMAL_RING
DailyByProductionType	desnUAll	DESTROY_NEW_UNIT_ALL
DailyByProductionType	desnAAll	DESTROY_NEW_ANIMAL_ALL
DailyByProductionType	deswUAll	DESTROY_WAIT_UNIT_ALL
DailyByProductionType	deswAAll	DESTROY_WAIT_ANIMAL_ALL
DailyByProductionType	vaccUIni	VAC_CUM_UNIT_INITIAL
DailyByProductionType	vaccAIni	VAC_CUM_ANIMAL_INITIAL
DailyByProductionType	vaccURing	VAC_CUM_UNIT_RING
DailyByProductionType	vaccARing	VAC_CUM_ANIMAL_RING
DailyByProductionType	vacnUAll	VAC_NEW_UNIT_ALL
DailyByProductionType	vacnAAll	VAC_NEW_ANIMAL_ALL
DailyByProductionType	vacwUAll	VAC_WAIT_UNIT_ALL
DailyByProductionType	vacwAAll	VAC_WAIT_ANIMAL_ALL
DailyByProductionType	zonnFoci	ZONE_NEW_FOCI
DailyByProductionType	zoncFoci	ZONE_CUM_FOCI
		
DailyByZone	iteration	ITERATION
DailyByZone	day	DAY
DailyByZone	zoneID	ZONE_ID
DailyByZone	zoneArea	ZONE_AREA
DailyByZone	zonePerimeter	ZONE_PERIMETER
		
DailyByZoneAndProductionType	iteration	ITERATION
DailyByZoneAndProductionType	day	DAY
DailyByZoneAndProductionType	zoneID	ZONE_ID
DailyByZoneAndProductionType	productionTypeID	PRODUCTION_TYPE_ID
DailyByZoneAndProductionType	unitDaysInZone	UNIT_DAYS_IN_ZONE
DailyByZoneAndProductionType	animalDaysInZone	ANIMAL_DAYS_IN_ZONE
DailyByZoneAndProductionType	unitsInZone	UNITS_IN_ZONE
DailyByZoneAndProductionType	animalsInZone	ANIMALS_IN_ZONE
		
DailyEvents	iteration	ITERATION
DailyEvents	day	DAY
DailyEvents	event	EVENT
DailyEvents	unitID	UNIT_ID
DailyEvents	zoneID	ZONE_ID
DailyEvents	eventCode	EVENT_CODE
DailyEvents	newStateCode	NEW_STATE_CODE
DailyEvents	testResultCode	TEST_RESULT_CODE
		
DailyExposures	iteration	ITERATION
DailyExposures	day	DAY
DailyExposures	exposure	EXPOSURE
DailyExposures	initiatedDay	INITIATED_DAY
DailyExposures	exposedUnitID	EXPOSED_UNIT_ID
DailyExposures	exposedZoneID	EXPOSED_ZONE_ID
DailyExposures	exposingUnitID	EXPOSING_UNIT_ID
DailyExposures	exposingZoneID	EXPOSING_ZONE_ID
DailyExposures	spreadMethodCode	SPREAD_METHOD_CODE
DailyExposures	isAdequate	IS_ADEQUATE
DailyExposures	exposingUnitStatusCode	EXPOSING_UNIT_STATUS_CODE
DailyExposures	exposedUnitStatusCode	EXPOSED_UNIT_STATUS_CODE
		
EpidemicCurves	iteration	ITERATION
EpidemicCurves	day	DAY
EpidemicCurves	productionTypeID	PRODUCTION_TYPE_ID
EpidemicCurves	infectedUnits	INFECTED_UNITS
EpidemicCurves	infectedAnimals	INFECTED_ANIMALS
EpidemicCurves	detectedUnits	DETECTED_UNITS
EpidemicCurves	detectedAnimals	DETECTED_ANIMALS
EpidemicCurves	infectiousUnits	INFECTIOUS_UNITS
EpidemicCurves	apparentInfectiousUnits	APPARENT_INFECTIOUS_UNITS
		
Iteration	iteration	ITERATION
Iteration	diseaseEnded	DISEASE_ENDED
Iteration	diseaseEndDay	DISEASE_END_DAY
Iteration	breakEnded	OUTBREAK_ENDED
Iteration	breakEndDay	OUTBREAK_END_DAY
Iteration	zoneFociCreated	ZONE_FOCI_CREATED
Iteration	deswUMax	DESTROY_WAIT_UNIT_MAX
Iteration	deswUMaxDay	DESTROY_WAIT_UNIT_MAX_DAY
Iteration	deswAMax	DESTROY_WAIT_ANIMAL_MAX
Iteration	deswAMaxDay	DESTROY_WAIT_ANIMAL_MAX_DAY
Iteration	deswUTimeMax	DESTROY_WAIT_UNIT_TIME_MAX
Iteration	deswUTimeAvg	DESTROY_WAIT_UNIT_TIME_AVG
Iteration	vacwUMax	VAC_WAIT_UNIT_MAX
Iteration	vacwUMaxDay	VAC_WAIT_UNIT_MAX_DAY
Iteration	vacwAMax	VAC_WAIT_ANIMAL_MAX
Iteration	vacwAMaxDay	VAC_WAIT_ANIMAL_MAX_DAY
Iteration	vacwUTimeMax	VAC_WAIT_UNIT_TIME_MAX
Iteration	vacwUTimeAvg	VAC_WAIT_UNIT_TIME_AVG
		
IterationByUnit	iteration	ITERATION
IterationByUnit	unitID	UNIT_ID
IterationByUnit	lastStatusCode	LAST_STATUS_CODE
IterationByUnit	lastStatusDay	LAST_STATUS_DAY
IterationByUnit	lastControlStateCode	LAST_CONTROL_STATE_CODE
IterationByUnit	lastControlStateDay	LAST_CONTROL_STATE_DAY
		
IterationByProductionType	iteration	ITERATION
IterationByProductionType	productionTypeID	PRODUCTION_TYPE_ID
IterationByProductionType	tscUSusc	TRANSITION_STATE_CUM_UNIT_SUSCEPTIBLE
IterationByProductionType	tscASusc	TRANSITION_STATE_CUM_ANIMAL_SUSCEPTIBLE
IterationByProductionType	tscULat	TRANSITION_STATE_CUM_UNIT_LATENT
IterationByProductionType	tscALat	TRANSITION_STATE_CUM_ANIMAL_LATENT
IterationByProductionType	tscUSubc	TRANSITION_STATE_CUM_UNIT_SUBCLINICAL
IterationByProductionType	tscASubc	TRANSITION_STATE_CUM_ANIMAL_SUBCLINICAL
IterationByProductionType	tscUClin	TRANSITION_STATE_CUM_UNIT_CLINICAL
IterationByProductionType	tscAClin	TRANSITION_STATE_CUM_ANIMAL_CLINICAL
IterationByProductionType	tscUNImm	TRANSITION_STATE_CUM_UNIT_NAT_IMMUNE
IterationByProductionType	tscANImm	TRANSITION_STATE_CUM_ANIMAL_NAT_IMMUNE
IterationByProductionType	tscUVImm	TRANSITION_STATE_CUM_UNIT_VAC_IMMUNE
IterationByProductionType	tscAVImm	TRANSITION_STATE_CUM_ANIMAL_VAC_IMMUNE
IterationByProductionType	tscUDest	TRANSITION_STATE_CUM_UNIT_DESTROYED
IterationByProductionType	tscADest	TRANSITION_STATE_CUM_ANIMAL_DESTROYED
IterationByProductionType	infcUIni	INFECTION_CUM_UNIT_INITIAL
IterationByProductionType	infcAIni	INFECTION_CUM_ANIMAL_INITIAL
IterationByProductionType	infcUAir	INFECTION_CUM_UNIT_AIR
IterationByProductionType	infcAAir	INFECTION_CUM_ANIMAL_AIR
IterationByProductionType	infcUDir	INFECTION_CUM_UNIT_DIR
IterationByProductionType	infcADir	INFECTION_CUM_ANIMAL_DIR
IterationByProductionType	infcUInd	INFECTION_CUM_UNIT_IND
IterationByProductionType	infcAInd	INFECTION_CUM_ANIMAL_IND
IterationByProductionType	expcUDir	EXPOSED_CUM_UNIT_DIR
IterationByProductionType	expcADir	EXPOSED_CUM_ANIMAL_DIR
IterationByProductionType	expcUInd	EXPOSED_CUM_UNIT_IND
IterationByProductionType	expcAInd	EXPOSED_CUM_ANIMAL_IND
IterationByProductionType	trcUDirFwd	TRACE_CUM_UNIT_DIR_FWD
IterationByProductionType	trcADirFwd	TRACE_CUM_ANIMAL_DIR_FWD
IterationByProductionType	trcUIndFwd	TRACE_CUM_UNIT_IND_FWD
IterationByProductionType	trcAIndFwd	TRACE_CUM_ANIMAL_IND_FWD
IterationByProductionType	trcUDirpFwd	TRACE_CUM_UNIT_DIR_P_FWD
IterationByProductionType	trcADirpFwd	TRACE_CUM_ANIMAL_DIR_PFWD
IterationByProductionType	trcUIndpFwd	TRACE_CUM_UNIT_IND_P_FWD
IterationByProductionType	trcAIndpFwd	TRACE_CUM_ANIMAL_IND_P_FWD
IterationByProductionType	trcUDirBack	TRACE_CUM_UNIT_DIR_BACK
IterationByProductionType	trcADirBack	TRACE_CUM_ANIMAL_DIR_BACK
IterationByProductionType	trcUIndBack	TRACE_CUM_UNIT_IND_BACK
IterationByProductionType	trcAIndBack	TRACE_CUM_ANIMAL_IND_BACK
IterationByProductionType	trcUDirpBack	TRACE_CUM_UNIT_DIR_P_BACK
IterationByProductionType	trcADirpBack	TRACE_CUM_ANIMAL_DIR_PBACK
IterationByProductionType	trcUIndpBack	TRACE_CUM_UNIT_IND_P_BACK
IterationByProductionType	trcAIndpBack	TRACE_CUM_ANIMAL_IND_P_BACK
IterationByProductionType	tocUDirFwd	TRACE_ORIGIN_CUM_UNIT_DIR_FWD
IterationByProductionType	tocUIndFwd	TRACE_ORIGIN_CUM_UNIT_IND_FWD
IterationByProductionType	tocUDirBack	TRACE_ORIGIN_CUM_UNIT_DIR_BACK
IterationByProductionType	tocUIndBack	TRACE_ORIGIN_CUM_UNIT_IND_BACK
IterationByProductionType	exmcUDirFwd	EXAM_CUM_UNIT_DIR_FWD
IterationByProductionType	exmcADirFwd	EXAM_CUM_ANIMAL_DIR_FWD
IterationByProductionType	exmcUIndFwd	EXAM_CUM_UNIT_IND_FWD
IterationByProductionType	exmcAIndFwd	EXAM_CUM_ANIMAL_IND_FWD
IterationByProductionType	exmcUDirBack	EXAM_CUM_UNIT_DIR_BACK
IterationByProductionType	exmcADirBack	EXAM_CUM_ANIMAL_DIR_BACK
IterationByProductionType	exmcUIndBack	EXAM_CUM_UNIT_IND_BACK
IterationByProductionType	exmcAIndBack	EXAM_CUM_ANIMAL_IND_BACK
IterationByProductionType	tstcUDirFwd	TEST_CUM_UNIT_DIR_FWD
IterationByProductionType	tstcADirFwd	TEST_CUM_ANIMAL_DIR_FWD
IterationByProductionType	tstcUIndFwd	TEST_CUM_UNIT_IND_FWD
IterationByProductionType	tstcAIndFwd	TEST_CUM_ANIMAL_IND_FWD
IterationByProductionType	tstcUDirBack	TEST_CUM_UNIT_DIR_BACK
IterationByProductionType	tstcADirBack	TEST_CUM_ANIMAL_DIR_BACK
IterationByProductionType	tstcUIndBack	TEST_CUM_UNIT_IND_BACK
IterationByProductionType	tstcAIndBack	TEST_CUM_ANIMAL_IND_BACK
IterationByProductionType	tstcUTruePos	TEST_CUM_UNIT_TRUE_POS
IterationByProductionType	tstcATruePos	TEST_CUM_ANIMAL_TRUE_POS
IterationByProductionType	tstcUTrueNeg	TEST_CUM_UNIT_TRUE_NEG
IterationByProductionType	tstcATrueNeg	TEST_CUM_ANIMAL_TRUE_NEG
IterationByProductionType	tstcUFalsePos	TEST_CUM_UNIT_FALSE_POS
IterationByProductionType	tstcAFalsePos	TEST_CUM_ANIMAL_FALSE_POS
IterationByProductionType	tstcUFalseNeg	TEST_CUM_UNIT_FALSE_NEG
IterationByProductionType	tstcAFalseNeg	TEST_CUM_ANIMAL_FALSE_NEG
IterationByProductionType	detcUClin	DETECT_CUM_UNIT_CLIN
IterationByProductionType	detcAClin	DETECT_CUM_ANIMAL_CLIN
IterationByProductionType	detcUTest	DETECT_CUM_UNIT_TEST
IterationByProductionType	detcATest	DETECT_CUM_ANIMAL_TEST
IterationByProductionType	descUIni	DESTROY_CUM_UNIT_INITIAL
IterationByProductionType	descAIni	DESTROY_CUM_ANIMAL_INITIAL
IterationByProductionType	descUDet	DESTROY_CUM_UNIT_DETECT
IterationByProductionType	descADet	DESTROY_CUM_ANIMAL_DETECT
IterationByProductionType	descUDirFwd	DESTROY_CUM_UNIT_DIR_FWD
IterationByProductionType	descADirFwd	DESTROY_CUM_ANIMAL_DIR_FWD
IterationByProductionType	descUIndFwd	DESTROY_CUM_UNIT_IND_FWD
IterationByProductionType	descAIndFwd	DESTROY_CUM_ANIMAL_IND_FWD
IterationByProductionType	descUDirBack	DESTROY_CUM_UNIT_DIR_BACK
IterationByProductionType	descADirBack	DESTROY_CUM_ANIMAL_DIR_BACK
IterationByProductionType	descUIndBack	DESTROY_CUM_UNIT_IND_BACK
IterationByProductionType	descAIndBack	DESTROY_CUM_ANIMAL_IND_BACK
IterationByProductionType	descURing	DESTROY_CUM_UNIT_RING
IterationByProductionType	descARing	DESTROY_CUM_ANIMAL_RING
IterationByProductionType	deswUMax	DESTROY_WAIT_UNIT_MAX
IterationByProductionType	deswAMax	DESTROY_WAIT_ANIMAL_MAX
IterationByProductionType	deswUMaxDay	DESTROY_WAIT_UNIT_MAX_DAY
IterationByProductionType	deswAMaxDay	DESTROY_WAIT_ANIMAL_MAX_DAY
IterationByProductionType	deswUTimeMax	DESTROY_WAIT_UNIT_TIME_MAX
IterationByProductionType	deswUTimeAvg	DESTROY_WAIT_UNIT_TIME_AVG
IterationByProductionType	deswUDaysInQueue	DESTROY_WAIT_UNIT_DAYS_IN_QUEUE
IterationByProductionType	deswADaysInQueue	DESTROY_WAIT_ANIMAL_DAYS_IN_QUEUE
IterationByProductionType	vaccUIni	VAC_CUM_UNIT_INITIAL
IterationByProductionType	vaccAIni	VAC_CUM_ANIMAL_INITIAL
IterationByProductionType	vaccURing	VAC_CUM_UNIT_RING
IterationByProductionType	vaccARing	VAC_CUM_ANIMAL_RING
IterationByProductionType	vacwUMax	VAC_WAIT_UNIT_MAX
IterationByProductionType	vacwAMax	VAC_WAIT_ANIMAL_MAX
IterationByProductionType	vacwUMaxDay	VAC_WAIT_UNIT_MAX_DAY
IterationByProductionType	vacwAMaxDay	VAC_WAIT_ANIMAL_MAX_DAY
IterationByProductionType	vacwUTimeMax	VAC_WAIT_UNIT_TIME_MAX
IterationByProductionType	vacwUTimeAvg	VAC_WAIT_UNIT_TIME_AVG
IterationByProductionType	zoncFoci	ZONE_CUM_FOCI
IterationByProductionType	firstDetection	FIRST_DETECTION
IterationByProductionType	firstDetUInf	FIRST_DET_UNIT_INF
IterationByProductionType	firstDetAInf	FIRST_DETECT_ANIMAL_INF
IterationByProductionType	firstDestruction	FIRST_DESTRUCTION
IterationByProductionType	firstVaccination	FIRST_VACCINATION
IterationByProductionType	lastDetection	LAST_DETECTION
		
IterationByZone	iteration	ITERATION
IterationByZone	zoneID	ZONE_ID
IterationByZone	maxZoneArea	MAX_ZONE_AREA
IterationByZone	maxZoneAreaDay	MAX_ZONE_AREA_DAY
IterationByZone	finalZoneArea	FINAL_ZONE_AREA
IterationByZone	maxZonePerimeter	MAX_ZONE_PERIMETER
IterationByZone	maxZonePerimeterDay	MAX_ZONE_PERIMETER_DAY
IterationByZone	finalZonePerimeter	FINAL_ZONE_PERIMETER
		
IterationByZoneAndProductionType	iteration	ITERATION
IterationByZoneAndProductionType	zoneID	ZONE_ID
IterationByZoneAndProductionType	productionTypeID	PRODUCTION_TYPE_ID
IterationByZoneAndProductionType	unitDaysInZone	UNIT_DAYS_IN_ZONE
IterationByZoneAndProductionType	animalDaysInZone	ANIMAL_DAYS_IN_ZONE
IterationByZoneAndProductionType	costSurveillance	COST_SURVEILLANCE
		
IterationCosts	iteration	ITERATION
IterationCosts	productionTypeID	PRODUCTION_TYPE_ID
IterationCosts	destrAppraisal	DESTROY_APPRAISAL
IterationCosts	destrCleaning	DESTROY_CLEANING
IterationCosts	destrEuthanasia	DESTROY_EUTHANASIA
IterationCosts	destrIndemnification	DESTROY_INDEMNIFICATION
IterationCosts	destrDisposal	DESTROY_DISPOSAL
IterationCosts	vaccSetup	VAC_CUM_SETUP
IterationCosts	vaccVaccination	VAC_CUM_VACCINATION""").readlines()

# <codecell>

print(name_conversion_table[:10])
name_conversion_array = [line.strip().split('\t') for line in name_conversion_table]
name_conversion_array[:10]

# <codecell>

for index, row in enumerate(name_conversion_array):
    if len(row) == 3:
        name_conversion_array[index] = [row[0], row[1], row[2].lower()]
name_conversion_array[:10]

# <codecell>


# <codecell>

code_chunks = [block.split('\n') for block in tables_code.split('\n\n\n')]
print(code_chunks[-1])
print(len(code_chunks))

# <codecell>

# dictionary-ify code_blocks
code_blocks = {re.sub('class |\(models.Model\):', '', block[0]) : block for block in code_chunks}
code_blocks['Iteration']  

# <codecell>

indentation = '    '

# <codecell>

def substr_indices(array, substr):
    matches = []
    for index, line in enumerate(array):
        if substr in line:
            matches.append(index)
    return matches

# <codecell>

some_list = ['abc-123', 'def-456', 'ghi-789', 'abc-456']
substr_indices(some_list, 'abc')

# <codecell>

line = '    iteration = models.IntegerField(blank=True, null=True,'
line.replace('iteration', 'itr')
print(line)
line += " db_column='iteration', "
line

# <codecell>

def printable_name(underscores_name):
    spaced = re.sub(r'_', r' ', underscores_name)
    return spaced.title()  # capitalize
printable_name('ugly_underscores_of_oblivion')

# <codecell>


# <codecell>

import copy
def reorganize_names(old_blocks):
    code_blocks = copy.deepcopy(old_blocks)
    trouble_makers = {}
    for row in name_conversion_array:
        if len(row) == 3:
            class_name, db_name, django_name = row[:]
            block = code_blocks[class_name]
            matching_lines = substr_indices(block, ' ' + django_name + ' = ')
            if len(matching_lines) != 1:  #couldn't find or found too many
                if '_id' not in django_name:
                    trouble_makers[django_name] = (class_name, django_name, matching_lines)
            else:
#                 print(class_name, db_name, django_name, block[matching_lines[0]], end='\n\n')
                line = block[matching_lines[0]].replace(django_name, db_name) # does not side effect the original
                line += " db_column='" + django_name + "', verbose_name=printable_name('"+django_name+"'), "
                block[matching_lines[0]] = line
    print("Trouble:", trouble_makers)
    return code_blocks

# <codecell>

# print(reorganize_names(code_blocks))
new_code = reorganize_names(code_blocks)

# <codecell>

# order = 'DailyByProductionType DailyByZone DailyByZoneAndProductionType DailyEvents DailyExposures EpidemicCurves General Iteration IterationByUnit IterationByProductionType IterationByZone IterationByZoneAndProductionType IterationCosts'.split()
order = sorted(new_code.keys())
code_string = str('\n\n\n'.join( ['\n'.join(new_code[key]) for key in order ]  ))
print(code_string)

# <codecell>

#find lines that didn't get modified but should have
code_lines = code_string.split('\n')
for index, line in enumerate(code_lines):
    if 'ForeignKey' not in line and 'class' not in line and 'db_column' not in line and 'help_text' not in line and line.strip():
        print('\n'.join(code_lines[index-2 : index+2]))
        print()

# <codecell>

new_code['EpidemicCurves']

# <headingcell level=1>

# 

# <headingcell level=1>

# Parsing

# <codecell>

headers = "Run,Day,outbreakDuration,infnUAll,infnUDir,infnUInd,infnUAir,infnUIni,infnUB,infnUBDS,infnUS,infnUBD,infnUBS,infnUD,infnUDS,infnUP,infnUDirB,infnUDirBDS,infnUDirS,infnUDirBD,infnUDirBS,infnUDirD,infnUDirDS,infnUDirP,infnUIndB,infnUIndBDS,infnUIndS,infnUIndBD,infnUIndBS,infnUIndD,infnUIndDS,infnUIndP,infnUAirB,infnUAirBDS,infnUAirS,infnUAirBD,infnUAirBS,infnUAirD,infnUAirDS,infnUAirP,infnUIniB,infnUIniBDS,infnUIniS,infnUIniBD,infnUIniBS,infnUIniD,infnUIniDS,infnUIniP,infcUAll,infcUDir,infcUInd,infcUAir,infcUIni,infcUB,infcUBDS,infcUS,infcUBD,infcUBS,infcUD,infcUDS,infcUP,infcUDirB,infcUDirBDS,infcUDirS,infcUDirBD,infcUDirBS,infcUDirD,infcUDirDS,infcUDirP,infcUIndB,infcUIndBDS,infcUIndS,infcUIndBD,infcUIndBS,infcUIndD,infcUIndDS,infcUIndP,infcUAirB,infcUAirBDS,infcUAirS,infcUAirBD,infcUAirBS,infcUAirD,infcUAirDS,infcUAirP,infcUIniB,infcUIniBDS,infcUIniS,infcUIniBD,infcUIniBS,infcUIniD,infcUIniDS,infcUIniP,infnAAll,infnADir,infnAInd,infnAAir,infnAIni,infnAB,infnABDS,infnAS,infnABD,infnABS,infnAD,infnADS,infnAP,infnADirB,infnADirBDS,infnADirS,infnADirBD,infnADirBS,infnADirD,infnADirDS,infnADirP,infnAIndB,infnAIndBDS,infnAIndS,infnAIndBD,infnAIndBS,infnAIndD,infnAIndDS,infnAIndP,infnAAirB,infnAAirBDS,infnAAirS,infnAAirBD,infnAAirBS,infnAAirD,infnAAirDS,infnAAirP,infnAIniB,infnAIniBDS,infnAIniS,infnAIniBD,infnAIniBS,infnAIniD,infnAIniDS,infnAIniP,infcAAll,infcADir,infcAInd,infcAAir,infcAIni,infcAB,infcABDS,infcAS,infcABD,infcABS,infcAD,infcADS,infcAP,infcADirB,infcADirBDS,infcADirS,infcADirBD,infcADirBS,infcADirD,infcADirDS,infcADirP,infcAIndB,infcAIndBDS,infcAIndS,infcAIndBD,infcAIndBS,infcAIndD,infcAIndDS,infcAIndP,infcAAirB,infcAAirBDS,infcAAirS,infcAAirBD,infcAAirBS,infcAAirD,infcAAirDS,infcAAirP,infcAIniB,infcAIniBDS,infcAIniS,infcAIniBD,infcAIniBS,infcAIniD,infcAIniDS,infcAIniP,firstDetUInfAll,firstDetAInfAll,ratio,tsdUSusc,tsdULat,tsdUSubc,tsdUClin,tsdUNImm,tsdUVImm,tsdUDest,tsdUBSusc,tsdUBLat,tsdUBSubc,tsdUBClin,tsdUBNImm,tsdUBVImm,tsdUBDest,tsdUBDSSusc,tsdUBDSLat,tsdUBDSSubc,tsdUBDSClin,tsdUBDSNImm,tsdUBDSVImm,tsdUBDSDest,tsdUSSusc,tsdUSLat,tsdUSSubc,tsdUSClin,tsdUSNImm,tsdUSVImm,tsdUSDest,tsdUBDSusc,tsdUBDLat,tsdUBDSubc,tsdUBDClin,tsdUBDNImm,tsdUBDVImm,tsdUBDDest,tsdUBSSusc,tsdUBSLat,tsdUBSSubc,tsdUBSClin,tsdUBSNImm,tsdUBSVImm,tsdUBSDest,tsdUDSusc,tsdUDLat,tsdUDSubc,tsdUDClin,tsdUDNImm,tsdUDVImm,tsdUDDest,tsdUDSSusc,tsdUDSLat,tsdUDSSubc,tsdUDSClin,tsdUDSNImm,tsdUDSVImm,tsdUDSDest,tsdUPSusc,tsdUPLat,tsdUPSubc,tsdUPClin,tsdUPNImm,tsdUPVImm,tsdUPDest,tsdASusc,tsdALat,tsdASubc,tsdAClin,tsdANImm,tsdAVImm,tsdADest,tsdABSusc,tsdABLat,tsdABSubc,tsdABClin,tsdABNImm,tsdABVImm,tsdABDest,tsdABDSSusc,tsdABDSLat,tsdABDSSubc,tsdABDSClin,tsdABDSNImm,tsdABDSVImm,tsdABDSDest,tsdASSusc,tsdASLat,tsdASSubc,tsdASClin,tsdASNImm,tsdASVImm,tsdASDest,tsdABDSusc,tsdABDLat,tsdABDSubc,tsdABDClin,tsdABDNImm,tsdABDVImm,tsdABDDest,tsdABSSusc,tsdABSLat,tsdABSSubc,tsdABSClin,tsdABSNImm,tsdABSVImm,tsdABSDest,tsdADSusc,tsdADLat,tsdADSubc,tsdADClin,tsdADNImm,tsdADVImm,tsdADDest,tsdADSSusc,tsdADSLat,tsdADSSubc,tsdADSClin,tsdADSNImm,tsdADSVImm,tsdADSDest,tsdAPSusc,tsdAPLat,tsdAPSubc,tsdAPClin,tsdAPNImm,tsdAPVImm,tsdAPDest,average-prevalence,diseaseDuration,vacwUAll,vacwUB,vacwUBDS,vacwUS,vacwUBD,vacwUBS,vacwUD,vacwUDS,vacwUP,vacwAAll,vacwAB,vacwABDS,vacwAS,vacwABD,vacwABS,vacwAD,vacwADS,vacwAP,vacwUMax,vacwUMaxDay,vacwAMax,vacwAMaxDay,vacwUTimeMax,vacwUTimeAvg,vacwUDaysInQueue,vacwADaysInQueue,zoneAreaHighRisk,zoneAreaMediumRisk,maxZoneAreaHighRisk,maxZoneAreaMediumRisk,maxZoneAreaDayHighRisk,maxZoneAreaDayMediumRisk,finalZoneAreaHighRisk,finalZoneAreaMediumRisk,zonePerimeterHighRisk,zonePerimeterMediumRisk,maxZonePerimeterHighRisk,maxZonePerimeterMediumRisk,maxZonePerimeterDayHighRisk,maxZonePerimeterDayMediumRisk,finalZonePerimeterHighRisk,finalZonePerimeterMediumRisk,num-separate-areasHighRisk,num-separate-areasMediumRisk,unitsInZoneHighRisk,unitsInZoneMediumRisk,unitsInZoneBackground,unitsInZoneHighRiskB,unitsInZoneHighRiskBDS,unitsInZoneHighRiskS,unitsInZoneHighRiskBD,unitsInZoneHighRiskBS,unitsInZoneHighRiskD,unitsInZoneHighRiskDS,unitsInZoneHighRiskP,unitsInZoneMediumRiskB,unitsInZoneMediumRiskBDS,unitsInZoneMediumRiskS,unitsInZoneMediumRiskBD,unitsInZoneMediumRiskBS,unitsInZoneMediumRiskD,unitsInZoneMediumRiskDS,unitsInZoneMediumRiskP,unitsInZoneBackgroundB,unitsInZoneBackgroundBDS,unitsInZoneBackgroundS,unitsInZoneBackgroundBD,unitsInZoneBackgroundBS,unitsInZoneBackgroundD,unitsInZoneBackgroundDS,unitsInZoneBackgroundP,unitDaysInZoneHighRisk,unitDaysInZoneMediumRisk,unitDaysInZoneBackground,unitDaysInZoneHighRiskB,unitDaysInZoneHighRiskBDS,unitDaysInZoneHighRiskS,unitDaysInZoneHighRiskBD,unitDaysInZoneHighRiskBS,unitDaysInZoneHighRiskD,unitDaysInZoneHighRiskDS,unitDaysInZoneHighRiskP,unitDaysInZoneMediumRiskB,unitDaysInZoneMediumRiskBDS,unitDaysInZoneMediumRiskS,unitDaysInZoneMediumRiskBD,unitDaysInZoneMediumRiskBS,unitDaysInZoneMediumRiskD,unitDaysInZoneMediumRiskDS,unitDaysInZoneMediumRiskP,unitDaysInZoneBackgroundB,unitDaysInZoneBackgroundBDS,unitDaysInZoneBackgroundS,unitDaysInZoneBackgroundBD,unitDaysInZoneBackgroundBS,unitDaysInZoneBackgroundD,unitDaysInZoneBackgroundDS,unitDaysInZoneBackgroundP,animalDaysInZoneHighRisk,animalDaysInZoneMediumRisk,animalDaysInZoneBackground,animalDaysInZoneHighRiskB,animalDaysInZoneHighRiskBDS,animalDaysInZoneHighRiskS,animalDaysInZoneHighRiskBD,animalDaysInZoneHighRiskBS,animalDaysInZoneHighRiskD,animalDaysInZoneHighRiskDS,animalDaysInZoneHighRiskP,animalDaysInZoneMediumRiskB,animalDaysInZoneMediumRiskBDS,animalDaysInZoneMediumRiskS,animalDaysInZoneMediumRiskBD,animalDaysInZoneMediumRiskBS,animalDaysInZoneMediumRiskD,animalDaysInZoneMediumRiskDS,animalDaysInZoneMediumRiskP,animalDaysInZoneBackgroundB,animalDaysInZoneBackgroundBDS,animalDaysInZoneBackgroundS,animalDaysInZoneBackgroundBD,animalDaysInZoneBackgroundBS,animalDaysInZoneBackgroundD,animalDaysInZoneBackgroundDS,animalDaysInZoneBackgroundP,trnUAllp,trnUDirp,trnUIndp,trnUBp,trnUBDSp,trnUSp,trnUBDp,trnUBSp,trnUDp,trnUDSp,trnUPp,trnUDirBp,trnUDirBDSp,trnUDirSp,trnUDirBDp,trnUDirBSp,trnUDirDp,trnUDirDSp,trnUDirPp,trnUIndBp,trnUIndBDSp,trnUIndSp,trnUIndBDp,trnUIndBSp,trnUIndDp,trnUIndDSp,trnUIndPp,trcUAllp,trcUDirp,trcUIndp,trcUBp,trcUBDSp,trcUSp,trcUBDp,trcUBSp,trcUDp,trcUDSp,trcUPp,trcUDirBp,trcUDirBDSp,trcUDirSp,trcUDirBDp,trcUDirBSp,trcUDirDp,trcUDirDSp,trcUDirPp,trcUIndBp,trcUIndBDSp,trcUIndSp,trcUIndBDp,trcUIndBSp,trcUIndDp,trcUIndDSp,trcUIndPp,trnUAll,trnUDir,trnUInd,trnUB,trnUBDS,trnUS,trnUBD,trnUBS,trnUD,trnUDS,trnUP,trnUDirB,trnUDirBDS,trnUDirS,trnUDirBD,trnUDirBS,trnUDirD,trnUDirDS,trnUDirP,trnUIndB,trnUIndBDS,trnUIndS,trnUIndBD,trnUIndBS,trnUIndD,trnUIndDS,trnUIndP,trcUAll,trcUDir,trcUInd,trcUB,trcUBDS,trcUS,trcUBD,trcUBS,trcUD,trcUDS,trcUP,trcUDirB,trcUDirBDS,trcUDirS,trcUDirBD,trcUDirBS,trcUDirD,trcUDirDS,trcUDirP,trcUIndB,trcUIndBDS,trcUIndS,trcUIndBD,trcUIndBS,trcUIndD,trcUIndDS,trcUIndP,trnAAllp,trnADirp,trnAIndp,trnABp,trnABDSp,trnASp,trnABDp,trnABSp,trnADp,trnADSp,trnAPp,trnADirBp,trnADirBDSp,trnADirSp,trnADirBDp,trnADirBSp,trnADirDp,trnADirDSp,trnADirPp,trnAIndBp,trnAIndBDSp,trnAIndSp,trnAIndBDp,trnAIndBSp,trnAIndDp,trnAIndDSp,trnAIndPp,trcAAllp,trcADirp,trcAIndp,trcABp,trcABDSp,trcASp,trcABDp,trcABSp,trcADp,trcADSp,trcAPp,trcADirBp,trcADirBDSp,trcADirSp,trcADirBDp,trcADirBSp,trcADirDp,trcADirDSp,trcADirPp,trcAIndBp,trcAIndBDSp,trcAIndSp,trcAIndBDp,trcAIndBSp,trcAIndDp,trcAIndDSp,trcAIndPp,trnAAll,trnADir,trnAInd,trnAB,trnABDS,trnAS,trnABD,trnABS,trnAD,trnADS,trnAP,trnADirB,trnADirBDS,trnADirS,trnADirBD,trnADirBS,trnADirD,trnADirDS,trnADirP,trnAIndB,trnAIndBDS,trnAIndS,trnAIndBD,trnAIndBS,trnAIndD,trnAIndDS,trnAIndP,trcAAll,trcADir,trcAInd,trcAB,trcABDS,trcAS,trcABD,trcABS,trcAD,trcADS,trcAP,trcADirB,trcADirBDS,trcADirS,trcADirBD,trcADirBS,trcADirD,trcADirDS,trcADirP,trcAIndB,trcAIndBDS,trcAIndS,trcAIndBD,trcAIndBS,trcAIndD,trcAIndDS,trcAIndP,destrOccurred,firstDestruction,firstDestructionUnsp,firstDestructionRing,firstDestructionDirFwd,firstDestructionIndFwd,firstDestructionDirBack,firstDestructionIndBack,firstDestructionDet,firstDestructionIni,firstDestructionB,firstDestructionBDS,firstDestructionS,firstDestructionBD,firstDestructionBS,firstDestructionD,firstDestructionDS,firstDestructionP,firstDestructionUnspB,firstDestructionUnspBDS,firstDestructionUnspS,firstDestructionUnspBD,firstDestructionUnspBS,firstDestructionUnspD,firstDestructionUnspDS,firstDestructionUnspP,firstDestructionRingB,firstDestructionRingBDS,firstDestructionRingS,firstDestructionRingBD,firstDestructionRingBS,firstDestructionRingD,firstDestructionRingDS,firstDestructionRingP,firstDestructionDirFwdB,firstDestructionDirFwdBDS,firstDestructionDirFwdS,firstDestructionDirFwdBD,firstDestructionDirFwdBS,firstDestructionDirFwdD,firstDestructionDirFwdDS,firstDestructionDirFwdP,firstDestructionIndFwdB,firstDestructionIndFwdBDS,firstDestructionIndFwdS,firstDestructionIndFwdBD,firstDestructionIndFwdBS,firstDestructionIndFwdD,firstDestructionIndFwdDS,firstDestructionIndFwdP,firstDestructionDirBackB,firstDestructionDirBackBDS,firstDestructionDirBackS,firstDestructionDirBackBD,firstDestructionDirBackBS,firstDestructionDirBackD,firstDestructionDirBackDS,firstDestructionDirBackP,firstDestructionIndBackB,firstDestructionIndBackBDS,firstDestructionIndBackS,firstDestructionIndBackBD,firstDestructionIndBackBS,firstDestructionIndBackD,firstDestructionIndBackDS,firstDestructionIndBackP,firstDestructionDetB,firstDestructionDetBDS,firstDestructionDetS,firstDestructionDetBD,firstDestructionDetBS,firstDestructionDetD,firstDestructionDetDS,firstDestructionDetP,firstDestructionIniB,firstDestructionIniBDS,firstDestructionIniS,firstDestructionIniBD,firstDestructionIniBS,firstDestructionIniD,firstDestructionIniDS,firstDestructionIniP,desnUAll,desnUIni,desnUUnsp,desnURing,desnUDirFwd,desnUIndFwd,desnUDirBack,desnUIndBack,desnUDet,desnUB,desnUBDS,desnUS,desnUBD,desnUBS,desnUD,desnUDS,desnUP,desnUIniB,desnUIniBDS,desnUIniS,desnUIniBD,desnUIniBS,desnUIniD,desnUIniDS,desnUIniP,desnUUnspB,desnUUnspBDS,desnUUnspS,desnUUnspBD,desnUUnspBS,desnUUnspD,desnUUnspDS,desnUUnspP,desnURingB,desnURingBDS,desnURingS,desnURingBD,desnURingBS,desnURingD,desnURingDS,desnURingP,desnUDirFwdB,desnUDirFwdBDS,desnUDirFwdS,desnUDirFwdBD,desnUDirFwdBS,desnUDirFwdD,desnUDirFwdDS,desnUDirFwdP,desnUIndFwdB,desnUIndFwdBDS,desnUIndFwdS,desnUIndFwdBD,desnUIndFwdBS,desnUIndFwdD,desnUIndFwdDS,desnUIndFwdP,desnUDirBackB,desnUDirBackBDS,desnUDirBackS,desnUDirBackBD,desnUDirBackBS,desnUDirBackD,desnUDirBackDS,desnUDirBackP,desnUIndBackB,desnUIndBackBDS,desnUIndBackS,desnUIndBackBD,desnUIndBackBS,desnUIndBackD,desnUIndBackDS,desnUIndBackP,desnUDetB,desnUDetBDS,desnUDetS,desnUDetBD,desnUDetBS,desnUDetD,desnUDetDS,desnUDetP,descUAll,descUIni,descUUnsp,descURing,descUDirFwd,descUIndFwd,descUDirBack,descUIndBack,descUDet,descUB,descUBDS,descUS,descUBD,descUBS,descUD,descUDS,descUP,descUIniB,descUIniBDS,descUIniS,descUIniBD,descUIniBS,descUIniD,descUIniDS,descUIniP,descUUnspB,descUUnspBDS,descUUnspS,descUUnspBD,descUUnspBS,descUUnspD,descUUnspDS,descUUnspP,descURingB,descURingBDS,descURingS,descURingBD,descURingBS,descURingD,descURingDS,descURingP,descUDirFwdB,descUDirFwdBDS,descUDirFwdS,descUDirFwdBD,descUDirFwdBS,descUDirFwdD,descUDirFwdDS,descUDirFwdP,descUIndFwdB,descUIndFwdBDS,descUIndFwdS,descUIndFwdBD,descUIndFwdBS,descUIndFwdD,descUIndFwdDS,descUIndFwdP,descUDirBackB,descUDirBackBDS,descUDirBackS,descUDirBackBD,descUDirBackBS,descUDirBackD,descUDirBackDS,descUDirBackP,descUIndBackB,descUIndBackBDS,descUIndBackS,descUIndBackBD,descUIndBackBS,descUIndBackD,descUIndBackDS,descUIndBackP,descUDetB,descUDetBDS,descUDetS,descUDetBD,descUDetBS,descUDetD,descUDetDS,descUDetP,desnAAll,desnAIni,desnAUnsp,desnARing,desnADirFwd,desnAIndFwd,desnADirBack,desnAIndBack,desnADet,desnAB,desnABDS,desnAS,desnABD,desnABS,desnAD,desnADS,desnAP,desnAIniB,desnAIniBDS,desnAIniS,desnAIniBD,desnAIniBS,desnAIniD,desnAIniDS,desnAIniP,desnAUnspB,desnAUnspBDS,desnAUnspS,desnAUnspBD,desnAUnspBS,desnAUnspD,desnAUnspDS,desnAUnspP,desnARingB,desnARingBDS,desnARingS,desnARingBD,desnARingBS,desnARingD,desnARingDS,desnARingP,desnADirFwdB,desnADirFwdBDS,desnADirFwdS,desnADirFwdBD,desnADirFwdBS,desnADirFwdD,desnADirFwdDS,desnADirFwdP,desnAIndFwdB,desnAIndFwdBDS,desnAIndFwdS,desnAIndFwdBD,desnAIndFwdBS,desnAIndFwdD,desnAIndFwdDS,desnAIndFwdP,desnADirBackB,desnADirBackBDS,desnADirBackS,desnADirBackBD,desnADirBackBS,desnADirBackD,desnADirBackDS,desnADirBackP,desnAIndBackB,desnAIndBackBDS,desnAIndBackS,desnAIndBackBD,desnAIndBackBS,desnAIndBackD,desnAIndBackDS,desnAIndBackP,desnADetB,desnADetBDS,desnADetS,desnADetBD,desnADetBS,desnADetD,desnADetDS,desnADetP,descAAll,descAIni,descAUnsp,descARing,descADirFwd,descAIndFwd,descADirBack,descAIndBack,descADet,descAB,descABDS,descAS,descABD,descABS,descAD,descADS,descAP,descAIniB,descAIniBDS,descAIniS,descAIniBD,descAIniBS,descAIniD,descAIniDS,descAIniP,descAUnspB,descAUnspBDS,descAUnspS,descAUnspBD,descAUnspBS,descAUnspD,descAUnspDS,descAUnspP,descARingB,descARingBDS,descARingS,descARingBD,descARingBS,descARingD,descARingDS,descARingP,descADirFwdB,descADirFwdBDS,descADirFwdS,descADirFwdBD,descADirFwdBS,descADirFwdD,descADirFwdDS,descADirFwdP,descAIndFwdB,descAIndFwdBDS,descAIndFwdS,descAIndFwdBD,descAIndFwdBS,descAIndFwdD,descAIndFwdDS,descAIndFwdP,descADirBackB,descADirBackBDS,descADirBackS,descADirBackBD,descADirBackBS,descADirBackD,descADirBackDS,descADirBackP,descAIndBackB,descAIndBackBDS,descAIndBackS,descAIndBackBD,descAIndBackBS,descAIndBackD,descAIndBackDS,descAIndBackP,descADetB,descADetBDS,descADetS,descADetBD,descADetBS,descADetD,descADetDS,descADetP,vaccOccurred,firstVaccination,firstVaccinationRing,firstVaccinationB,firstVaccinationBDS,firstVaccinationS,firstVaccinationBD,firstVaccinationBS,firstVaccinationD,firstVaccinationDS,firstVaccinationP,firstVaccinationRingB,firstVaccinationRingBDS,firstVaccinationRingS,firstVaccinationRingBD,firstVaccinationRingBS,firstVaccinationRingD,firstVaccinationRingDS,firstVaccinationRingP,vacnUAll,vacnUIni,vacnURing,vacnUB,vacnUBDS,vacnUS,vacnUBD,vacnUBS,vacnUD,vacnUDS,vacnUP,vacnUIniB,vacnUIniBDS,vacnUIniS,vacnUIniBD,vacnUIniBS,vacnUIniD,vacnUIniDS,vacnUIniP,vacnURingB,vacnURingBDS,vacnURingS,vacnURingBD,vacnURingBS,vacnURingD,vacnURingDS,vacnURingP,vaccUAll,vaccUIni,vaccURing,vaccUB,vaccUBDS,vaccUS,vaccUBD,vaccUBS,vaccUD,vaccUDS,vaccUP,vaccUIniB,vaccUIniBDS,vaccUIniS,vaccUIniBD,vaccUIniBS,vaccUIniD,vaccUIniDS,vaccUIniP,vaccURingB,vaccURingBDS,vaccURingS,vaccURingBD,vaccURingBS,vaccURingD,vaccURingDS,vaccURingP,vacnAAll,vacnAIni,vacnARing,vacnAB,vacnABDS,vacnAS,vacnABD,vacnABS,vacnAD,vacnADS,vacnAP,vacnAIniB,vacnAIniBDS,vacnAIniS,vacnAIniBD,vacnAIniBS,vacnAIniD,vacnAIniDS,vacnAIniP,vacnARingB,vacnARingBDS,vacnARingS,vacnARingBD,vacnARingBS,vacnARingD,vacnARingDS,vacnARingP,vaccAAll,vaccAIni,vaccARing,vaccAB,vaccABDS,vaccAS,vaccABD,vaccABS,vaccAD,vaccADS,vaccAP,vaccAIniB,vaccAIniBDS,vaccAIniS,vaccAIniBD,vaccAIniBS,vaccAIniD,vaccAIniDS,vaccAIniP,vaccARingB,vaccARingBDS,vaccARingS,vaccARingBD,vaccARingBS,vaccARingD,vaccARingDS,vaccARingP,deswUAll,deswUB,deswUBDS,deswUS,deswUBD,deswUBS,deswUD,deswUDS,deswUP,deswAAll,deswAB,deswABDS,deswAS,deswABD,deswABS,deswAD,deswADS,deswAP,deswUMax,deswUMaxDay,deswAMax,deswAMaxDay,deswUTimeMax,deswUTimeAvg,deswUDaysInQueue,deswADaysInQueue,tstnUTruePos,tstnUTruePosB,tstnUTruePosBDS,tstnUTruePosS,tstnUTruePosBD,tstnUTruePosBS,tstnUTruePosD,tstnUTruePosDS,tstnUTruePosP,tstnUTrueNeg,tstnUTrueNegB,tstnUTrueNegBDS,tstnUTrueNegS,tstnUTrueNegBD,tstnUTrueNegBS,tstnUTrueNegD,tstnUTrueNegDS,tstnUTrueNegP,tstnUFalsePos,tstnUFalsePosB,tstnUFalsePosBDS,tstnUFalsePosS,tstnUFalsePosBD,tstnUFalsePosBS,tstnUFalsePosD,tstnUFalsePosDS,tstnUFalsePosP,tstnUFalseNeg,tstnUFalseNegB,tstnUFalseNegBDS,tstnUFalseNegS,tstnUFalseNegBD,tstnUFalseNegBS,tstnUFalseNegD,tstnUFalseNegDS,tstnUFalseNegP,tstcUAll,tstcUDirFwd,tstcUIndFwd,tstcUDirBack,tstcUIndBack,tstcUB,tstcUBDS,tstcUS,tstcUBD,tstcUBS,tstcUD,tstcUDS,tstcUP,tstcUDirFwdB,tstcUDirFwdBDS,tstcUDirFwdS,tstcUDirFwdBD,tstcUDirFwdBS,tstcUDirFwdD,tstcUDirFwdDS,tstcUDirFwdP,tstcUIndFwdB,tstcUIndFwdBDS,tstcUIndFwdS,tstcUIndFwdBD,tstcUIndFwdBS,tstcUIndFwdD,tstcUIndFwdDS,tstcUIndFwdP,tstcUDirBackB,tstcUDirBackBDS,tstcUDirBackS,tstcUDirBackBD,tstcUDirBackBS,tstcUDirBackD,tstcUDirBackDS,tstcUDirBackP,tstcUIndBackB,tstcUIndBackBDS,tstcUIndBackS,tstcUIndBackBD,tstcUIndBackBS,tstcUIndBackD,tstcUIndBackDS,tstcUIndBackP,tstcUTruePos,tstcUTruePosB,tstcUTruePosBDS,tstcUTruePosS,tstcUTruePosBD,tstcUTruePosBS,tstcUTruePosD,tstcUTruePosDS,tstcUTruePosP,tstcUTrueNeg,tstcUTrueNegB,tstcUTrueNegBDS,tstcUTrueNegS,tstcUTrueNegBD,tstcUTrueNegBS,tstcUTrueNegD,tstcUTrueNegDS,tstcUTrueNegP,tstcUFalsePos,tstcUFalsePosB,tstcUFalsePosBDS,tstcUFalsePosS,tstcUFalsePosBD,tstcUFalsePosBS,tstcUFalsePosD,tstcUFalsePosDS,tstcUFalsePosP,tstcUFalseNeg,tstcUFalseNegB,tstcUFalseNegBDS,tstcUFalseNegS,tstcUFalseNegBD,tstcUFalseNegBS,tstcUFalseNegD,tstcUFalseNegDS,tstcUFalseNegP,tstcAAll,tstcADirFwd,tstcAIndFwd,tstcADirBack,tstcAIndBack,tstcAB,tstcABDS,tstcAS,tstcABD,tstcABS,tstcAD,tstcADS,tstcAP,tstcADirFwdB,tstcADirFwdBDS,tstcADirFwdS,tstcADirFwdBD,tstcADirFwdBS,tstcADirFwdD,tstcADirFwdDS,tstcADirFwdP,tstcAIndFwdB,tstcAIndFwdBDS,tstcAIndFwdS,tstcAIndFwdBD,tstcAIndFwdBS,tstcAIndFwdD,tstcAIndFwdDS,tstcAIndFwdP,tstcADirBackB,tstcADirBackBDS,tstcADirBackS,tstcADirBackBD,tstcADirBackBS,tstcADirBackD,tstcADirBackDS,tstcADirBackP,tstcAIndBackB,tstcAIndBackBDS,tstcAIndBackS,tstcAIndBackBD,tstcAIndBackBS,tstcAIndBackD,tstcAIndBackDS,tstcAIndBackP,detOccurred,firstDetection,firstDetectionClin,firstDetectionTest,firstDetectionB,firstDetectionBDS,firstDetectionS,firstDetectionBD,firstDetectionBS,firstDetectionD,firstDetectionDS,firstDetectionP,firstDetectionClinB,firstDetectionClinBDS,firstDetectionClinS,firstDetectionClinBD,firstDetectionClinBS,firstDetectionClinD,firstDetectionClinDS,firstDetectionClinP,firstDetectionTestB,firstDetectionTestBDS,firstDetectionTestS,firstDetectionTestBD,firstDetectionTestBS,firstDetectionTestD,firstDetectionTestDS,firstDetectionTestP,lastDetection,lastDetectionClin,lastDetectionTest,lastDetectionB,lastDetectionBDS,lastDetectionS,lastDetectionBD,lastDetectionBS,lastDetectionD,lastDetectionDS,lastDetectionP,lastDetectionClinB,lastDetectionClinBDS,lastDetectionClinS,lastDetectionClinBD,lastDetectionClinBS,lastDetectionClinD,lastDetectionClinDS,lastDetectionClinP,lastDetectionTestB,lastDetectionTestBDS,lastDetectionTestS,lastDetectionTestBD,lastDetectionTestBS,lastDetectionTestD,lastDetectionTestDS,lastDetectionTestP,detnUAll,detnUClin,detnUTest,detnUB,detnUBDS,detnUS,detnUBD,detnUBS,detnUD,detnUDS,detnUP,detnUClinB,detnUClinBDS,detnUClinS,detnUClinBD,detnUClinBS,detnUClinD,detnUClinDS,detnUClinP,detnUTestB,detnUTestBDS,detnUTestS,detnUTestBD,detnUTestBS,detnUTestD,detnUTestDS,detnUTestP,detnAAll,detnAClin,detnATest,detnAB,detnABDS,detnAS,detnABD,detnABS,detnAD,detnADS,detnAP,detnAClinB,detnAClinBDS,detnAClinS,detnAClinBD,detnAClinBS,detnAClinD,detnAClinDS,detnAClinP,detnATestB,detnATestBDS,detnATestS,detnATestBD,detnATestBS,detnATestD,detnATestDS,detnATestP,detcUAll,detcUClin,detcUTest,detcUB,detcUBDS,detcUS,detcUBD,detcUBS,detcUD,detcUDS,detcUP,detcUClinB,detcUClinBDS,detcUClinS,detcUClinBD,detcUClinBS,detcUClinD,detcUClinDS,detcUClinP,detcUTestB,detcUTestBDS,detcUTestS,detcUTestBD,detcUTestBS,detcUTestD,detcUTestDS,detcUTestP,detcUqAll,detcAAll,detcAClin,detcATest,detcAB,detcABDS,detcAS,detcABD,detcABS,detcAD,detcADS,detcAP,detcAClinB,detcAClinBDS,detcAClinS,detcAClinBD,detcAClinBS,detcAClinD,detcAClinDS,detcAClinP,detcATestB,detcATestBDS,detcATestS,detcATestBD,detcATestBS,detcATestD,detcATestDS,detcATestP,expnUAll,expnUDir,expnUInd,expnUAir,expnUB,expnUBDS,expnUS,expnUBD,expnUBS,expnUD,expnUDS,expnUP,expnUDirB,expnUDirBDS,expnUDirS,expnUDirBD,expnUDirBS,expnUDirD,expnUDirDS,expnUDirP,expnUIndB,expnUIndBDS,expnUIndS,expnUIndBD,expnUIndBS,expnUIndD,expnUIndDS,expnUIndP,expnUAirB,expnUAirBDS,expnUAirS,expnUAirBD,expnUAirBS,expnUAirD,expnUAirDS,expnUAirP,expcUAll,expcUDir,expcUInd,expcUAir,expcUB,expcUBDS,expcUS,expcUBD,expcUBS,expcUD,expcUDS,expcUP,expcUDirB,expcUDirBDS,expcUDirS,expcUDirBD,expcUDirBS,expcUDirD,expcUDirDS,expcUDirP,expcUIndB,expcUIndBDS,expcUIndS,expcUIndBD,expcUIndBS,expcUIndD,expcUIndDS,expcUIndP,expcUAirB,expcUAirBDS,expcUAirS,expcUAirBD,expcUAirBS,expcUAirD,expcUAirDS,expcUAirP,expnAAll,expnADir,expnAInd,expnAAir,expnAB,expnABDS,expnAS,expnABD,expnABS,expnAD,expnADS,expnAP,expnADirB,expnADirBDS,expnADirS,expnADirBD,expnADirBS,expnADirD,expnADirDS,expnADirP,expnAIndB,expnAIndBDS,expnAIndS,expnAIndBD,expnAIndBS,expnAIndD,expnAIndDS,expnAIndP,expnAAirB,expnAAirBDS,expnAAirS,expnAAirBD,expnAAirBS,expnAAirD,expnAAirDS,expnAAirP,expcAAll,expcADir,expcAInd,expcAAir,expcAB,expcABDS,expcAS,expcABD,expcABS,expcAD,expcADS,expcAP,expcADirB,expcADirBDS,expcADirS,expcADirBD,expcADirBS,expcADirD,expcADirDS,expcADirP,expcAIndB,expcAIndBDS,expcAIndS,expcAIndBD,expcAIndBS,expcAIndD,expcAIndDS,expcAIndP,expcAAirB,expcAAirBDS,expcAAirS,expcAAirBD,expcAAirBS,expcAAirD,expcAAirDS,expcAAirP,adqnUAll,adqcUAll,exmnUAll,exmnURing,exmnUDirFwd,exmnUIndFwd,exmnUDirBack,exmnUIndBack,exmnUDet,exmnUB,exmnUBDS,exmnUS,exmnUBD,exmnUBS,exmnUD,exmnUDS,exmnUP,exmnURingB,exmnURingBDS,exmnURingS,exmnURingBD,exmnURingBS,exmnURingD,exmnURingDS,exmnURingP,exmnUDirFwdB,exmnUDirFwdBDS,exmnUDirFwdS,exmnUDirFwdBD,exmnUDirFwdBS,exmnUDirFwdD,exmnUDirFwdDS,exmnUDirFwdP,exmnUIndFwdB,exmnUIndFwdBDS,exmnUIndFwdS,exmnUIndFwdBD,exmnUIndFwdBS,exmnUIndFwdD,exmnUIndFwdDS,exmnUIndFwdP,exmnUDirBackB,exmnUDirBackBDS,exmnUDirBackS,exmnUDirBackBD,exmnUDirBackBS,exmnUDirBackD,exmnUDirBackDS,exmnUDirBackP,exmnUIndBackB,exmnUIndBackBDS,exmnUIndBackS,exmnUIndBackBD,exmnUIndBackBS,exmnUIndBackD,exmnUIndBackDS,exmnUIndBackP,exmnUDetB,exmnUDetBDS,exmnUDetS,exmnUDetBD,exmnUDetBS,exmnUDetD,exmnUDetDS,exmnUDetP,exmnAAll,exmnARing,exmnADirFwd,exmnAIndFwd,exmnADirBack,exmnAIndBack,exmnADet,exmnAB,exmnABDS,exmnAS,exmnABD,exmnABS,exmnAD,exmnADS,exmnAP,exmnARingB,exmnARingBDS,exmnARingS,exmnARingBD,exmnARingBS,exmnARingD,exmnARingDS,exmnARingP,exmnADirFwdB,exmnADirFwdBDS,exmnADirFwdS,exmnADirFwdBD,exmnADirFwdBS,exmnADirFwdD,exmnADirFwdDS,exmnADirFwdP,exmnAIndFwdB,exmnAIndFwdBDS,exmnAIndFwdS,exmnAIndFwdBD,exmnAIndFwdBS,exmnAIndFwdD,exmnAIndFwdDS,exmnAIndFwdP,exmnADirBackB,exmnADirBackBDS,exmnADirBackS,exmnADirBackBD,exmnADirBackBS,exmnADirBackD,exmnADirBackDS,exmnADirBackP,exmnAIndBackB,exmnAIndBackBDS,exmnAIndBackS,exmnAIndBackBD,exmnAIndBackBS,exmnAIndBackD,exmnAIndBackDS,exmnAIndBackP,exmnADetB,exmnADetBDS,exmnADetS,exmnADetBD,exmnADetBS,exmnADetD,exmnADetDS,exmnADetP,exmcUAll,exmcURing,exmcUDirFwd,exmcUIndFwd,exmcUDirBack,exmcUIndBack,exmcUDet,exmcUB,exmcUBDS,exmcUS,exmcUBD,exmcUBS,exmcUD,exmcUDS,exmcUP,exmcURingB,exmcURingBDS,exmcURingS,exmcURingBD,exmcURingBS,exmcURingD,exmcURingDS,exmcURingP,exmcUDirFwdB,exmcUDirFwdBDS,exmcUDirFwdS,exmcUDirFwdBD,exmcUDirFwdBS,exmcUDirFwdD,exmcUDirFwdDS,exmcUDirFwdP,exmcUIndFwdB,exmcUIndFwdBDS,exmcUIndFwdS,exmcUIndFwdBD,exmcUIndFwdBS,exmcUIndFwdD,exmcUIndFwdDS,exmcUIndFwdP,exmcUDirBackB,exmcUDirBackBDS,exmcUDirBackS,exmcUDirBackBD,exmcUDirBackBS,exmcUDirBackD,exmcUDirBackDS,exmcUDirBackP,exmcUIndBackB,exmcUIndBackBDS,exmcUIndBackS,exmcUIndBackBD,exmcUIndBackBS,exmcUIndBackD,exmcUIndBackDS,exmcUIndBackP,exmcUDetB,exmcUDetBDS,exmcUDetS,exmcUDetBD,exmcUDetBS,exmcUDetD,exmcUDetDS,exmcUDetP,exmcAAll,exmcARing,exmcADirFwd,exmcAIndFwd,exmcADirBack,exmcAIndBack,exmcADet,exmcAB,exmcABDS,exmcAS,exmcABD,exmcABS,exmcAD,exmcADS,exmcAP,exmcARingB,exmcARingBDS,exmcARingS,exmcARingBD,exmcARingBS,exmcARingD,exmcARingDS,exmcARingP,exmcADirFwdB,exmcADirFwdBDS,exmcADirFwdS,exmcADirFwdBD,exmcADirFwdBS,exmcADirFwdD,exmcADirFwdDS,exmcADirFwdP,exmcAIndFwdB,exmcAIndFwdBDS,exmcAIndFwdS,exmcAIndFwdBD,exmcAIndFwdBS,exmcAIndFwdD,exmcAIndFwdDS,exmcAIndFwdP,exmcADirBackB,exmcADirBackBDS,exmcADirBackS,exmcADirBackBD,exmcADirBackBS,exmcADirBackD,exmcADirBackDS,exmcADirBackP,exmcAIndBackB,exmcAIndBackBDS,exmcAIndBackS,exmcAIndBackBD,exmcAIndBackBS,exmcAIndBackD,exmcAIndBackDS,exmcAIndBackP,exmcADetB,exmcADetBDS,exmcADetS,exmcADetBD,exmcADetBS,exmcADetD,exmcADetDS,exmcADetP".split(',')
output_line = '5,9,,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,226,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,226,0,0,0,,,,20,0,1,0,0,0,0,10,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,3,0,0,0,0,0,0,2,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,2026,0,226,0,0,0,0,1082,0,0,0,0,0,0,109,0,0,0,0,0,0,84,0,0,0,0,0,0,114,0,0,0,0,0,0,214,0,226,0,0,0,0,92,0,0,0,0,0,0,192,0,0,0,0,0,0,139,0,0,0,0,0,0,1,,0,0,0,0,0,0,0,0,0,0,4328,436,336,456,856,368,768,556,0,,0,,,,0,0,0,0,0,0,,,,,0,0,0,0,,,,,0,0,0,0,21,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,1,1,3,3,1,1,1,0,0,189,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,90,9,9,27,27,9,9,9,0,0,20268,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9738,981,756,1026,3960,828,1728,1251,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,,,,,,,,,,,,,,,,,,,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,,0,,,,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0'.split(',')

# <codecell>

print(len(headers), len(output_line))

# <codecell>

str(', '.join(assignments for assignments in [x[0]+ '='+ (x[1] if x[1] != '' else '0') for x in zip(headers, output_line)]))[:1000]

# <codecell>

if '0': print('yes')

# <codecell>

import ast
ast.literal_eval(str({1:'a', 2:'b'}))

# <codecell>


# <codecell>


# <codecell>


# <codecell>

lx = substr_indices(headers, 'zon') + substr_indices(headers, 'Zon')
print('\n'.join([headers[x] for x in lx]))

# <codecell>

print(len(headers))
# for h in headers:
#     print(h)

# <codecell>

new_code['EpidemicCurves'][3]

# <codecell>

import re
s = 'a number of things said'
m = bool(re.match(r'aasdasd (\w+) of', s))
m

# <codecell>

headers = "Run,Day,outbreakDuration,infnUAll,infnUDir,infnUInd,infnUAir,infnUIni,infnU_Bull_,infnU_Dogsheep_,infnU_Swine_,infnU_Bulldog_,infnU_Brownsheep_,infnU_Doe_,infnU_Pig_,infnUDir_Bull_,infnUDir_Dogsheep_,infnUDir_Swine_,infnUDir_Bulldog_,infnUDir_Brownsheep_,infnUDir_Doe_,infnUDir_Pig_,infnUInd_Bull_,infnUInd_Dogsheep_,infnUInd_Swine_,infnUInd_Bulldog_,infnUInd_Brownsheep_,infnUInd_Doe_,infnUInd_Pig_,infnUAir_Bull_,infnUAir_Dogsheep_,infnUAir_Swine_,infnUAir_Bulldog_,infnUAir_Brownsheep_,infnUAir_Doe_,infnUAir_Pig_,infnUIni_Bull_,infnUIni_Dogsheep_,infnUIni_Swine_,infnUIni_Bulldog_,infnUIni_Brownsheep_,infnUIni_Doe_,infnUIni_Pig_,infcUAll,infcUDir,infcUInd,infcUAir,infcUIni,infcU_Bull_,infcU_Dogsheep_,infcU_Swine_,infcU_Bulldog_,infcU_Brownsheep_,infcU_Doe_,infcU_Pig_,infcUDir_Bull_,infcUDir_Dogsheep_,infcUDir_Swine_,infcUDir_Bulldog_,infcUDir_Brownsheep_,infcUDir_Doe_,infcUDir_Pig_,infcUInd_Bull_,infcUInd_Dogsheep_,infcUInd_Swine_,infcUInd_Bulldog_,infcUInd_Brownsheep_,infcUInd_Doe_,infcUInd_Pig_,infcUAir_Bull_,infcUAir_Dogsheep_,infcUAir_Swine_,infcUAir_Bulldog_,infcUAir_Brownsheep_,infcUAir_Doe_,infcUAir_Pig_,infcUIni_Bull_,infcUIni_Dogsheep_,infcUIni_Swine_,infcUIni_Bulldog_,infcUIni_Brownsheep_,infcUIni_Doe_,infcUIni_Pig_,infnAAll,infnADir,infnAInd,infnAAir,infnAIni,infnA_Bull_,infnA_Dogsheep_,infnA_Swine_,infnA_Bulldog_,infnA_Brownsheep_,infnA_Doe_,infnA_Pig_,infnADir_Bull_,infnADir_Dogsheep_,infnADir_Swine_,infnADir_Bulldog_,infnADir_Brownsheep_,infnADir_Doe_,infnADir_Pig_,infnAInd_Bull_,infnAInd_Dogsheep_,infnAInd_Swine_,infnAInd_Bulldog_,infnAInd_Brownsheep_,infnAInd_Doe_,infnAInd_Pig_,infnAAir_Bull_,infnAAir_Dogsheep_,infnAAir_Swine_,infnAAir_Bulldog_,infnAAir_Brownsheep_,infnAAir_Doe_,infnAAir_Pig_,infnAIni_Bull_,infnAIni_Dogsheep_,infnAIni_Swine_,infnAIni_Bulldog_,infnAIni_Brownsheep_,infnAIni_Doe_,infnAIni_Pig_,infcAAll,infcADir,infcAInd,infcAAir,infcAIni,infcA_Bull_,infcA_Dogsheep_,infcA_Swine_,infcA_Bulldog_,infcA_Brownsheep_,infcA_Doe_,infcA_Pig_,infcADir_Bull_,infcADir_Dogsheep_,infcADir_Swine_,infcADir_Bulldog_,infcADir_Brownsheep_,infcADir_Doe_,infcADir_Pig_,infcAInd_Bull_,infcAInd_Dogsheep_,infcAInd_Swine_,infcAInd_Bulldog_,infcAInd_Brownsheep_,infcAInd_Doe_,infcAInd_Pig_,infcAAir_Bull_,infcAAir_Dogsheep_,infcAAir_Swine_,infcAAir_Bulldog_,infcAAir_Brownsheep_,infcAAir_Doe_,infcAAir_Pig_,infcAIni_Bull_,infcAIni_Dogsheep_,infcAIni_Swine_,infcAIni_Bulldog_,infcAIni_Brownsheep_,infcAIni_Doe_,infcAIni_Pig_,firstDetUInfAll,firstDetAInfAll,ratio,expnUAll,expnUDir,expnUInd,expnUAir,expnU_Bull_,expnU_Dogsheep_,expnU_Swine_,expnU_Bulldog_,expnU_Brownsheep_,expnU_Doe_,expnU_Pig_,expnUDir_Bull_,expnUDir_Dogsheep_,expnUDir_Swine_,expnUDir_Bulldog_,expnUDir_Brownsheep_,expnUDir_Doe_,expnUDir_Pig_,expnUInd_Bull_,expnUInd_Dogsheep_,expnUInd_Swine_,expnUInd_Bulldog_,expnUInd_Brownsheep_,expnUInd_Doe_,expnUInd_Pig_,expnUAir_Bull_,expnUAir_Dogsheep_,expnUAir_Swine_,expnUAir_Bulldog_,expnUAir_Brownsheep_,expnUAir_Doe_,expnUAir_Pig_,expcUAll,expcUDir,expcUInd,expcUAir,expcU_Bull_,expcU_Dogsheep_,expcU_Swine_,expcU_Bulldog_,expcU_Brownsheep_,expcU_Doe_,expcU_Pig_,expcUDir_Bull_,expcUDir_Dogsheep_,expcUDir_Swine_,expcUDir_Bulldog_,expcUDir_Brownsheep_,expcUDir_Doe_,expcUDir_Pig_,expcUInd_Bull_,expcUInd_Dogsheep_,expcUInd_Swine_,expcUInd_Bulldog_,expcUInd_Brownsheep_,expcUInd_Doe_,expcUInd_Pig_,expcUAir_Bull_,expcUAir_Dogsheep_,expcUAir_Swine_,expcUAir_Bulldog_,expcUAir_Brownsheep_,expcUAir_Doe_,expcUAir_Pig_,expnAAll,expnADir,expnAInd,expnAAir,expnA_Bull_,expnA_Dogsheep_,expnA_Swine_,expnA_Bulldog_,expnA_Brownsheep_,expnA_Doe_,expnA_Pig_,expnADir_Bull_,expnADir_Dogsheep_,expnADir_Swine_,expnADir_Bulldog_,expnADir_Brownsheep_,expnADir_Doe_,expnADir_Pig_,expnAInd_Bull_,expnAInd_Dogsheep_,expnAInd_Swine_,expnAInd_Bulldog_,expnAInd_Brownsheep_,expnAInd_Doe_,expnAInd_Pig_,expnAAir_Bull_,expnAAir_Dogsheep_,expnAAir_Swine_,expnAAir_Bulldog_,expnAAir_Brownsheep_,expnAAir_Doe_,expnAAir_Pig_,expcAAll,expcADir,expcAInd,expcAAir,expcA_Bull_,expcA_Dogsheep_,expcA_Swine_,expcA_Bulldog_,expcA_Brownsheep_,expcA_Doe_,expcA_Pig_,expcADir_Bull_,expcADir_Dogsheep_,expcADir_Swine_,expcADir_Bulldog_,expcADir_Brownsheep_,expcADir_Doe_,expcADir_Pig_,expcAInd_Bull_,expcAInd_Dogsheep_,expcAInd_Swine_,expcAInd_Bulldog_,expcAInd_Brownsheep_,expcAInd_Doe_,expcAInd_Pig_,expcAAir_Bull_,expcAAir_Dogsheep_,expcAAir_Swine_,expcAAir_Bulldog_,expcAAir_Brownsheep_,expcAAir_Doe_,expcAAir_Pig_,adqnUAll,adqcUAll,vacwUAll,vacwU_Bull_,vacwU_Dogsheep_,vacwU_Swine_,vacwU_Bulldog_,vacwU_Brownsheep_,vacwU_Doe_,vacwU_Pig_,vacwAAll,vacwA_Bull_,vacwA_Dogsheep_,vacwA_Swine_,vacwA_Bulldog_,vacwA_Brownsheep_,vacwA_Doe_,vacwA_Pig_,vacwUMax,vacwUMaxDay,vacwAMax,vacwAMaxDay,vacwUTimeMax,vacwUTimeAvg,vacwUDaysInQueue,vacwADaysInQueue,zoneAreaHighRisk,zoneAreaMediumRisk,maxZoneAreaHighRisk,maxZoneAreaMediumRisk,maxZoneAreaDayHighRisk,maxZoneAreaDayMediumRisk,finalZoneAreaHighRisk,finalZoneAreaMediumRisk,zonePerimeterHighRisk,zonePerimeterMediumRisk,maxZonePerimeterHighRisk,maxZonePerimeterMediumRisk,maxZonePerimeterDayHighRisk,maxZonePerimeterDayMediumRisk,finalZonePerimeterHighRisk,finalZonePerimeterMediumRisk,num-separate-areasHighRisk,num-separate-areasMediumRisk,unitsInZoneHighRisk,unitsInZoneMediumRisk,unitsInZoneBackground,unitsInZoneHighRisk_Bull_,unitsInZoneHighRisk_Dogsheep_,unitsInZoneHighRisk_Swine_,unitsInZoneHighRisk_Bulldog_,unitsInZoneHighRisk_Brownsheep_,unitsInZoneHighRisk_Doe_,unitsInZoneHighRisk_Pig_,unitsInZoneMediumRisk_Bull_,unitsInZoneMediumRisk_Dogsheep_,unitsInZoneMediumRisk_Swine_,unitsInZoneMediumRisk_Bulldog_,unitsInZoneMediumRisk_Brownsheep_,unitsInZoneMediumRisk_Doe_,unitsInZoneMediumRisk_Pig_,unitsInZoneBackground_Bull_,unitsInZoneBackground_Dogsheep_,unitsInZoneBackground_Swine_,unitsInZoneBackground_Bulldog_,unitsInZoneBackground_Brownsheep_,unitsInZoneBackground_Doe_,unitsInZoneBackground_Pig_,unitDaysInZoneHighRisk,unitDaysInZoneMediumRisk,unitDaysInZoneBackground,unitDaysInZoneHighRisk_Bull_,unitDaysInZoneHighRisk_Dogsheep_,unitDaysInZoneHighRisk_Swine_,unitDaysInZoneHighRisk_Bulldog_,unitDaysInZoneHighRisk_Brownsheep_,unitDaysInZoneHighRisk_Doe_,unitDaysInZoneHighRisk_Pig_,unitDaysInZoneMediumRisk_Bull_,unitDaysInZoneMediumRisk_Dogsheep_,unitDaysInZoneMediumRisk_Swine_,unitDaysInZoneMediumRisk_Bulldog_,unitDaysInZoneMediumRisk_Brownsheep_,unitDaysInZoneMediumRisk_Doe_,unitDaysInZoneMediumRisk_Pig_,unitDaysInZoneBackground_Bull_,unitDaysInZoneBackground_Dogsheep_,unitDaysInZoneBackground_Swine_,unitDaysInZoneBackground_Bulldog_,unitDaysInZoneBackground_Brownsheep_,unitDaysInZoneBackground_Doe_,unitDaysInZoneBackground_Pig_,animalDaysInZoneHighRisk,animalDaysInZoneMediumRisk,animalDaysInZoneBackground,animalDaysInZoneHighRisk_Bull_,animalDaysInZoneHighRisk_Dogsheep_,animalDaysInZoneHighRisk_Swine_,animalDaysInZoneHighRisk_Bulldog_,animalDaysInZoneHighRisk_Brownsheep_,animalDaysInZoneHighRisk_Doe_,animalDaysInZoneHighRisk_Pig_,animalDaysInZoneMediumRisk_Bull_,animalDaysInZoneMediumRisk_Dogsheep_,animalDaysInZoneMediumRisk_Swine_,animalDaysInZoneMediumRisk_Bulldog_,animalDaysInZoneMediumRisk_Brownsheep_,animalDaysInZoneMediumRisk_Doe_,animalDaysInZoneMediumRisk_Pig_,animalDaysInZoneBackground_Bull_,animalDaysInZoneBackground_Dogsheep_,animalDaysInZoneBackground_Swine_,animalDaysInZoneBackground_Bulldog_,animalDaysInZoneBackground_Brownsheep_,animalDaysInZoneBackground_Doe_,animalDaysInZoneBackground_Pig_,deswUAll,deswU_Bull_,deswU_Dogsheep_,deswU_Swine_,deswU_Bulldog_,deswU_Brownsheep_,deswU_Doe_,deswU_Pig_,deswAAll,deswA_Bull_,deswA_Dogsheep_,deswA_Swine_,deswA_Bulldog_,deswA_Brownsheep_,deswA_Doe_,deswA_Pig_,deswUMax,deswUMaxDay,deswAMax,deswAMaxDay,deswUTimeMax,deswUTimeAvg,deswUDaysInQueue,deswADaysInQueue,destrOccurred,firstDestruction,firstDestructionUnsp,firstDestructionRing,firstDestructionDirFwd,firstDestructionIndFwd,firstDestructionDirBack,firstDestructionIndBack,firstDestructionDet,firstDestructionIni,firstDestruction_Bull_,firstDestruction_Dogsheep_,firstDestruction_Swine_,firstDestruction_Bulldog_,firstDestruction_Brownsheep_,firstDestruction_Doe_,firstDestruction_Pig_,firstDestructionUnsp_Bull_,firstDestructionUnsp_Dogsheep_,firstDestructionUnsp_Swine_,firstDestructionUnsp_Bulldog_,firstDestructionUnsp_Brownsheep_,firstDestructionUnsp_Doe_,firstDestructionUnsp_Pig_,firstDestructionRing_Bull_,firstDestructionRing_Dogsheep_,firstDestructionRing_Swine_,firstDestructionRing_Bulldog_,firstDestructionRing_Brownsheep_,firstDestructionRing_Doe_,firstDestructionRing_Pig_,firstDestructionDirFwd_Bull_,firstDestructionDirFwd_Dogsheep_,firstDestructionDirFwd_Swine_,firstDestructionDirFwd_Bulldog_,firstDestructionDirFwd_Brownsheep_,firstDestructionDirFwd_Doe_,firstDestructionDirFwd_Pig_,firstDestructionIndFwd_Bull_,firstDestructionIndFwd_Dogsheep_,firstDestructionIndFwd_Swine_,firstDestructionIndFwd_Bulldog_,firstDestructionIndFwd_Brownsheep_,firstDestructionIndFwd_Doe_,firstDestructionIndFwd_Pig_,firstDestructionDirBack_Bull_,firstDestructionDirBack_Dogsheep_,firstDestructionDirBack_Swine_,firstDestructionDirBack_Bulldog_,firstDestructionDirBack_Brownsheep_,firstDestructionDirBack_Doe_,firstDestructionDirBack_Pig_,firstDestructionIndBack_Bull_,firstDestructionIndBack_Dogsheep_,firstDestructionIndBack_Swine_,firstDestructionIndBack_Bulldog_,firstDestructionIndBack_Brownsheep_,firstDestructionIndBack_Doe_,firstDestructionIndBack_Pig_,firstDestructionDet_Bull_,firstDestructionDet_Dogsheep_,firstDestructionDet_Swine_,firstDestructionDet_Bulldog_,firstDestructionDet_Brownsheep_,firstDestructionDet_Doe_,firstDestructionDet_Pig_,firstDestructionIni_Bull_,firstDestructionIni_Dogsheep_,firstDestructionIni_Swine_,firstDestructionIni_Bulldog_,firstDestructionIni_Brownsheep_,firstDestructionIni_Doe_,firstDestructionIni_Pig_,desnUAll,desnUIni,desnUUnsp,desnURing,desnUDirFwd,desnUIndFwd,desnUDirBack,desnUIndBack,desnUDet,desnU_Bull_,desnU_Dogsheep_,desnU_Swine_,desnU_Bulldog_,desnU_Brownsheep_,desnU_Doe_,desnU_Pig_,desnUIni_Bull_,desnUIni_Dogsheep_,desnUIni_Swine_,desnUIni_Bulldog_,desnUIni_Brownsheep_,desnUIni_Doe_,desnUIni_Pig_,desnUUnsp_Bull_,desnUUnsp_Dogsheep_,desnUUnsp_Swine_,desnUUnsp_Bulldog_,desnUUnsp_Brownsheep_,desnUUnsp_Doe_,desnUUnsp_Pig_,desnURing_Bull_,desnURing_Dogsheep_,desnURing_Swine_,desnURing_Bulldog_,desnURing_Brownsheep_,desnURing_Doe_,desnURing_Pig_,desnUDirFwd_Bull_,desnUDirFwd_Dogsheep_,desnUDirFwd_Swine_,desnUDirFwd_Bulldog_,desnUDirFwd_Brownsheep_,desnUDirFwd_Doe_,desnUDirFwd_Pig_,desnUIndFwd_Bull_,desnUIndFwd_Dogsheep_,desnUIndFwd_Swine_,desnUIndFwd_Bulldog_,desnUIndFwd_Brownsheep_,desnUIndFwd_Doe_,desnUIndFwd_Pig_,desnUDirBack_Bull_,desnUDirBack_Dogsheep_,desnUDirBack_Swine_,desnUDirBack_Bulldog_,desnUDirBack_Brownsheep_,desnUDirBack_Doe_,desnUDirBack_Pig_,desnUIndBack_Bull_,desnUIndBack_Dogsheep_,desnUIndBack_Swine_,desnUIndBack_Bulldog_,desnUIndBack_Brownsheep_,desnUIndBack_Doe_,desnUIndBack_Pig_,desnUDet_Bull_,desnUDet_Dogsheep_,desnUDet_Swine_,desnUDet_Bulldog_,desnUDet_Brownsheep_,desnUDet_Doe_,desnUDet_Pig_,descUAll,descUIni,descUUnsp,descURing,descUDirFwd,descUIndFwd,descUDirBack,descUIndBack,descUDet,descU_Bull_,descU_Dogsheep_,descU_Swine_,descU_Bulldog_,descU_Brownsheep_,descU_Doe_,descU_Pig_,descUIni_Bull_,descUIni_Dogsheep_,descUIni_Swine_,descUIni_Bulldog_,descUIni_Brownsheep_,descUIni_Doe_,descUIni_Pig_,descUUnsp_Bull_,descUUnsp_Dogsheep_,descUUnsp_Swine_,descUUnsp_Bulldog_,descUUnsp_Brownsheep_,descUUnsp_Doe_,descUUnsp_Pig_,descURing_Bull_,descURing_Dogsheep_,descURing_Swine_,descURing_Bulldog_,descURing_Brownsheep_,descURing_Doe_,descURing_Pig_,descUDirFwd_Bull_,descUDirFwd_Dogsheep_,descUDirFwd_Swine_,descUDirFwd_Bulldog_,descUDirFwd_Brownsheep_,descUDirFwd_Doe_,descUDirFwd_Pig_,descUIndFwd_Bull_,descUIndFwd_Dogsheep_,descUIndFwd_Swine_,descUIndFwd_Bulldog_,descUIndFwd_Brownsheep_,descUIndFwd_Doe_,descUIndFwd_Pig_,descUDirBack_Bull_,descUDirBack_Dogsheep_,descUDirBack_Swine_,descUDirBack_Bulldog_,descUDirBack_Brownsheep_,descUDirBack_Doe_,descUDirBack_Pig_,descUIndBack_Bull_,descUIndBack_Dogsheep_,descUIndBack_Swine_,descUIndBack_Bulldog_,descUIndBack_Brownsheep_,descUIndBack_Doe_,descUIndBack_Pig_,descUDet_Bull_,descUDet_Dogsheep_,descUDet_Swine_,descUDet_Bulldog_,descUDet_Brownsheep_,descUDet_Doe_,descUDet_Pig_,desnAAll,desnAIni,desnAUnsp,desnARing,desnADirFwd,desnAIndFwd,desnADirBack,desnAIndBack,desnADet,desnA_Bull_,desnA_Dogsheep_,desnA_Swine_,desnA_Bulldog_,desnA_Brownsheep_,desnA_Doe_,desnA_Pig_,desnAIni_Bull_,desnAIni_Dogsheep_,desnAIni_Swine_,desnAIni_Bulldog_,desnAIni_Brownsheep_,desnAIni_Doe_,desnAIni_Pig_,desnAUnsp_Bull_,desnAUnsp_Dogsheep_,desnAUnsp_Swine_,desnAUnsp_Bulldog_,desnAUnsp_Brownsheep_,desnAUnsp_Doe_,desnAUnsp_Pig_,desnARing_Bull_,desnARing_Dogsheep_,desnARing_Swine_,desnARing_Bulldog_,desnARing_Brownsheep_,desnARing_Doe_,desnARing_Pig_,desnADirFwd_Bull_,desnADirFwd_Dogsheep_,desnADirFwd_Swine_,desnADirFwd_Bulldog_,desnADirFwd_Brownsheep_,desnADirFwd_Doe_,desnADirFwd_Pig_,desnAIndFwd_Bull_,desnAIndFwd_Dogsheep_,desnAIndFwd_Swine_,desnAIndFwd_Bulldog_,desnAIndFwd_Brownsheep_,desnAIndFwd_Doe_,desnAIndFwd_Pig_,desnADirBack_Bull_,desnADirBack_Dogsheep_,desnADirBack_Swine_,desnADirBack_Bulldog_,desnADirBack_Brownsheep_,desnADirBack_Doe_,desnADirBack_Pig_,desnAIndBack_Bull_,desnAIndBack_Dogsheep_,desnAIndBack_Swine_,desnAIndBack_Bulldog_,desnAIndBack_Brownsheep_,desnAIndBack_Doe_,desnAIndBack_Pig_,desnADet_Bull_,desnADet_Dogsheep_,desnADet_Swine_,desnADet_Bulldog_,desnADet_Brownsheep_,desnADet_Doe_,desnADet_Pig_,descAAll,descAIni,descAUnsp,descARing,descADirFwd,descAIndFwd,descADirBack,descAIndBack,descADet,descA_Bull_,descA_Dogsheep_,descA_Swine_,descA_Bulldog_,descA_Brownsheep_,descA_Doe_,descA_Pig_,descAIni_Bull_,descAIni_Dogsheep_,descAIni_Swine_,descAIni_Bulldog_,descAIni_Brownsheep_,descAIni_Doe_,descAIni_Pig_,descAUnsp_Bull_,descAUnsp_Dogsheep_,descAUnsp_Swine_,descAUnsp_Bulldog_,descAUnsp_Brownsheep_,descAUnsp_Doe_,descAUnsp_Pig_,descARing_Bull_,descARing_Dogsheep_,descARing_Swine_,descARing_Bulldog_,descARing_Brownsheep_,descARing_Doe_,descARing_Pig_,descADirFwd_Bull_,descADirFwd_Dogsheep_,descADirFwd_Swine_,descADirFwd_Bulldog_,descADirFwd_Brownsheep_,descADirFwd_Doe_,descADirFwd_Pig_,descAIndFwd_Bull_,descAIndFwd_Dogsheep_,descAIndFwd_Swine_,descAIndFwd_Bulldog_,descAIndFwd_Brownsheep_,descAIndFwd_Doe_,descAIndFwd_Pig_,descADirBack_Bull_,descADirBack_Dogsheep_,descADirBack_Swine_,descADirBack_Bulldog_,descADirBack_Brownsheep_,descADirBack_Doe_,descADirBack_Pig_,descAIndBack_Bull_,descAIndBack_Dogsheep_,descAIndBack_Swine_,descAIndBack_Bulldog_,descAIndBack_Brownsheep_,descAIndBack_Doe_,descAIndBack_Pig_,descADet_Bull_,descADet_Dogsheep_,descADet_Swine_,descADet_Bulldog_,descADet_Brownsheep_,descADet_Doe_,descADet_Pig_,trnUAllp,trnUDirp,trnUIndp,trnU_Bull_p,trnU_Dogsheep_p,trnU_Swine_p,trnU_Bulldog_p,trnU_Brownsheep_p,trnU_Doe_p,trnU_Pig_p,trnUDir_Bull_p,trnUDir_Dogsheep_p,trnUDir_Swine_p,trnUDir_Bulldog_p,trnUDir_Brownsheep_p,trnUDir_Doe_p,trnUDir_Pig_p,trnUInd_Bull_p,trnUInd_Dogsheep_p,trnUInd_Swine_p,trnUInd_Bulldog_p,trnUInd_Brownsheep_p,trnUInd_Doe_p,trnUInd_Pig_p,trcUAllp,trcUDirp,trcUIndp,trcU_Bull_p,trcU_Dogsheep_p,trcU_Swine_p,trcU_Bulldog_p,trcU_Brownsheep_p,trcU_Doe_p,trcU_Pig_p,trcUDir_Bull_p,trcUDir_Dogsheep_p,trcUDir_Swine_p,trcUDir_Bulldog_p,trcUDir_Brownsheep_p,trcUDir_Doe_p,trcUDir_Pig_p,trcUInd_Bull_p,trcUInd_Dogsheep_p,trcUInd_Swine_p,trcUInd_Bulldog_p,trcUInd_Brownsheep_p,trcUInd_Doe_p,trcUInd_Pig_p,trnUAll,trnUDir,trnUInd,trnU_Bull_,trnU_Dogsheep_,trnU_Swine_,trnU_Bulldog_,trnU_Brownsheep_,trnU_Doe_,trnU_Pig_,trnUDir_Bull_,trnUDir_Dogsheep_,trnUDir_Swine_,trnUDir_Bulldog_,trnUDir_Brownsheep_,trnUDir_Doe_,trnUDir_Pig_,trnUInd_Bull_,trnUInd_Dogsheep_,trnUInd_Swine_,trnUInd_Bulldog_,trnUInd_Brownsheep_,trnUInd_Doe_,trnUInd_Pig_,trcUAll,trcUDir,trcUInd,trcU_Bull_,trcU_Dogsheep_,trcU_Swine_,trcU_Bulldog_,trcU_Brownsheep_,trcU_Doe_,trcU_Pig_,trcUDir_Bull_,trcUDir_Dogsheep_,trcUDir_Swine_,trcUDir_Bulldog_,trcUDir_Brownsheep_,trcUDir_Doe_,trcUDir_Pig_,trcUInd_Bull_,trcUInd_Dogsheep_,trcUInd_Swine_,trcUInd_Bulldog_,trcUInd_Brownsheep_,trcUInd_Doe_,trcUInd_Pig_,trnAAllp,trnADirp,trnAIndp,trnA_Bull_p,trnA_Dogsheep_p,trnA_Swine_p,trnA_Bulldog_p,trnA_Brownsheep_p,trnA_Doe_p,trnA_Pig_p,trnADir_Bull_p,trnADir_Dogsheep_p,trnADir_Swine_p,trnADir_Bulldog_p,trnADir_Brownsheep_p,trnADir_Doe_p,trnADir_Pig_p,trnAInd_Bull_p,trnAInd_Dogsheep_p,trnAInd_Swine_p,trnAInd_Bulldog_p,trnAInd_Brownsheep_p,trnAInd_Doe_p,trnAInd_Pig_p,trcAAllp,trcADirp,trcAIndp,trcA_Bull_p,trcA_Dogsheep_p,trcA_Swine_p,trcA_Bulldog_p,trcA_Brownsheep_p,trcA_Doe_p,trcA_Pig_p,trcADir_Bull_p,trcADir_Dogsheep_p,trcADir_Swine_p,trcADir_Bulldog_p,trcADir_Brownsheep_p,trcADir_Doe_p,trcADir_Pig_p,trcAInd_Bull_p,trcAInd_Dogsheep_p,trcAInd_Swine_p,trcAInd_Bulldog_p,trcAInd_Brownsheep_p,trcAInd_Doe_p,trcAInd_Pig_p,trnAAll,trnADir,trnAInd,trnA_Bull_,trnA_Dogsheep_,trnA_Swine_,trnA_Bulldog_,trnA_Brownsheep_,trnA_Doe_,trnA_Pig_,trnADir_Bull_,trnADir_Dogsheep_,trnADir_Swine_,trnADir_Bulldog_,trnADir_Brownsheep_,trnADir_Doe_,trnADir_Pig_,trnAInd_Bull_,trnAInd_Dogsheep_,trnAInd_Swine_,trnAInd_Bulldog_,trnAInd_Brownsheep_,trnAInd_Doe_,trnAInd_Pig_,trcAAll,trcADir,trcAInd,trcA_Bull_,trcA_Dogsheep_,trcA_Swine_,trcA_Bulldog_,trcA_Brownsheep_,trcA_Doe_,trcA_Pig_,trcADir_Bull_,trcADir_Dogsheep_,trcADir_Swine_,trcADir_Bulldog_,trcADir_Brownsheep_,trcADir_Doe_,trcADir_Pig_,trcAInd_Bull_,trcAInd_Dogsheep_,trcAInd_Swine_,trcAInd_Bulldog_,trcAInd_Brownsheep_,trcAInd_Doe_,trcAInd_Pig_,detOccurred,firstDetection,firstDetectionClin,firstDetectionTest,firstDetection_Bull_,firstDetection_Dogsheep_,firstDetection_Swine_,firstDetection_Bulldog_,firstDetection_Brownsheep_,firstDetection_Doe_,firstDetection_Pig_,firstDetectionClin_Bull_,firstDetectionClin_Dogsheep_,firstDetectionClin_Swine_,firstDetectionClin_Bulldog_,firstDetectionClin_Brownsheep_,firstDetectionClin_Doe_,firstDetectionClin_Pig_,firstDetectionTest_Bull_,firstDetectionTest_Dogsheep_,firstDetectionTest_Swine_,firstDetectionTest_Bulldog_,firstDetectionTest_Brownsheep_,firstDetectionTest_Doe_,firstDetectionTest_Pig_,lastDetection,lastDetectionClin,lastDetectionTest,lastDetection_Bull_,lastDetection_Dogsheep_,lastDetection_Swine_,lastDetection_Bulldog_,lastDetection_Brownsheep_,lastDetection_Doe_,lastDetection_Pig_,lastDetectionClin_Bull_,lastDetectionClin_Dogsheep_,lastDetectionClin_Swine_,lastDetectionClin_Bulldog_,lastDetectionClin_Brownsheep_,lastDetectionClin_Doe_,lastDetectionClin_Pig_,lastDetectionTest_Bull_,lastDetectionTest_Dogsheep_,lastDetectionTest_Swine_,lastDetectionTest_Bulldog_,lastDetectionTest_Brownsheep_,lastDetectionTest_Doe_,lastDetectionTest_Pig_,detnUAll,detnUClin,detnUTest,detnU_Bull_,detnU_Dogsheep_,detnU_Swine_,detnU_Bulldog_,detnU_Brownsheep_,detnU_Doe_,detnU_Pig_,detnUClin_Bull_,detnUClin_Dogsheep_,detnUClin_Swine_,detnUClin_Bulldog_,detnUClin_Brownsheep_,detnUClin_Doe_,detnUClin_Pig_,detnUTest_Bull_,detnUTest_Dogsheep_,detnUTest_Swine_,detnUTest_Bulldog_,detnUTest_Brownsheep_,detnUTest_Doe_,detnUTest_Pig_,detnAAll,detnAClin,detnATest,detnA_Bull_,detnA_Dogsheep_,detnA_Swine_,detnA_Bulldog_,detnA_Brownsheep_,detnA_Doe_,detnA_Pig_,detnAClin_Bull_,detnAClin_Dogsheep_,detnAClin_Swine_,detnAClin_Bulldog_,detnAClin_Brownsheep_,detnAClin_Doe_,detnAClin_Pig_,detnATest_Bull_,detnATest_Dogsheep_,detnATest_Swine_,detnATest_Bulldog_,detnATest_Brownsheep_,detnATest_Doe_,detnATest_Pig_,detcUAll,detcUClin,detcUTest,detcU_Bull_,detcU_Dogsheep_,detcU_Swine_,detcU_Bulldog_,detcU_Brownsheep_,detcU_Doe_,detcU_Pig_,detcUClin_Bull_,detcUClin_Dogsheep_,detcUClin_Swine_,detcUClin_Bulldog_,detcUClin_Brownsheep_,detcUClin_Doe_,detcUClin_Pig_,detcUTest_Bull_,detcUTest_Dogsheep_,detcUTest_Swine_,detcUTest_Bulldog_,detcUTest_Brownsheep_,detcUTest_Doe_,detcUTest_Pig_,detcUqAll,detcAAll,detcAClin,detcATest,detcA_Bull_,detcA_Dogsheep_,detcA_Swine_,detcA_Bulldog_,detcA_Brownsheep_,detcA_Doe_,detcA_Pig_,detcAClin_Bull_,detcAClin_Dogsheep_,detcAClin_Swine_,detcAClin_Bulldog_,detcAClin_Brownsheep_,detcAClin_Doe_,detcAClin_Pig_,detcATest_Bull_,detcATest_Dogsheep_,detcATest_Swine_,detcATest_Bulldog_,detcATest_Brownsheep_,detcATest_Doe_,detcATest_Pig_,tsdUSusc,tsdULat,tsdUSubc,tsdUClin,tsdUNImm,tsdUVImm,tsdUDest,tsdU_Bull_Susc,tsdU_Bull_Lat,tsdU_Bull_Subc,tsdU_Bull_Clin,tsdU_Bull_NImm,tsdU_Bull_VImm,tsdU_Bull_Dest,tsdU_Dogsheep_Susc,tsdU_Dogsheep_Lat,tsdU_Dogsheep_Subc,tsdU_Dogsheep_Clin,tsdU_Dogsheep_NImm,tsdU_Dogsheep_VImm,tsdU_Dogsheep_Dest,tsdU_Swine_Susc,tsdU_Swine_Lat,tsdU_Swine_Subc,tsdU_Swine_Clin,tsdU_Swine_NImm,tsdU_Swine_VImm,tsdU_Swine_Dest,tsdU_Bulldog_Susc,tsdU_Bulldog_Lat,tsdU_Bulldog_Subc,tsdU_Bulldog_Clin,tsdU_Bulldog_NImm,tsdU_Bulldog_VImm,tsdU_Bulldog_Dest,tsdU_Brownsheep_Susc,tsdU_Brownsheep_Lat,tsdU_Brownsheep_Subc,tsdU_Brownsheep_Clin,tsdU_Brownsheep_NImm,tsdU_Brownsheep_VImm,tsdU_Brownsheep_Dest,tsdU_Doe_Susc,tsdU_Doe_Lat,tsdU_Doe_Subc,tsdU_Doe_Clin,tsdU_Doe_NImm,tsdU_Doe_VImm,tsdU_Doe_Dest,tsdU_Pig_Susc,tsdU_Pig_Lat,tsdU_Pig_Subc,tsdU_Pig_Clin,tsdU_Pig_NImm,tsdU_Pig_VImm,tsdU_Pig_Dest,tsdASusc,tsdALat,tsdASubc,tsdAClin,tsdANImm,tsdAVImm,tsdADest,tsdA_Bull_Susc,tsdA_Bull_Lat,tsdA_Bull_Subc,tsdA_Bull_Clin,tsdA_Bull_NImm,tsdA_Bull_VImm,tsdA_Bull_Dest,tsdA_Dogsheep_Susc,tsdA_Dogsheep_Lat,tsdA_Dogsheep_Subc,tsdA_Dogsheep_Clin,tsdA_Dogsheep_NImm,tsdA_Dogsheep_VImm,tsdA_Dogsheep_Dest,tsdA_Swine_Susc,tsdA_Swine_Lat,tsdA_Swine_Subc,tsdA_Swine_Clin,tsdA_Swine_NImm,tsdA_Swine_VImm,tsdA_Swine_Dest,tsdA_Bulldog_Susc,tsdA_Bulldog_Lat,tsdA_Bulldog_Subc,tsdA_Bulldog_Clin,tsdA_Bulldog_NImm,tsdA_Bulldog_VImm,tsdA_Bulldog_Dest,tsdA_Brownsheep_Susc,tsdA_Brownsheep_Lat,tsdA_Brownsheep_Subc,tsdA_Brownsheep_Clin,tsdA_Brownsheep_NImm,tsdA_Brownsheep_VImm,tsdA_Brownsheep_Dest,tsdA_Doe_Susc,tsdA_Doe_Lat,tsdA_Doe_Subc,tsdA_Doe_Clin,tsdA_Doe_NImm,tsdA_Doe_VImm,tsdA_Doe_Dest,tsdA_Pig_Susc,tsdA_Pig_Lat,tsdA_Pig_Subc,tsdA_Pig_Clin,tsdA_Pig_NImm,tsdA_Pig_VImm,tsdA_Pig_Dest,average-prevalence,diseaseDuration,tstnUTruePos,tstnUTruePos_Bull_,tstnUTruePos_Dogsheep_,tstnUTruePos_Swine_,tstnUTruePos_Bulldog_,tstnUTruePos_Brownsheep_,tstnUTruePos_Doe_,tstnUTruePos_Pig_,tstnUTrueNeg,tstnUTrueNeg_Bull_,tstnUTrueNeg_Dogsheep_,tstnUTrueNeg_Swine_,tstnUTrueNeg_Bulldog_,tstnUTrueNeg_Brownsheep_,tstnUTrueNeg_Doe_,tstnUTrueNeg_Pig_,tstnUFalsePos,tstnUFalsePos_Bull_,tstnUFalsePos_Dogsheep_,tstnUFalsePos_Swine_,tstnUFalsePos_Bulldog_,tstnUFalsePos_Brownsheep_,tstnUFalsePos_Doe_,tstnUFalsePos_Pig_,tstnUFalseNeg,tstnUFalseNeg_Bull_,tstnUFalseNeg_Dogsheep_,tstnUFalseNeg_Swine_,tstnUFalseNeg_Bulldog_,tstnUFalseNeg_Brownsheep_,tstnUFalseNeg_Doe_,tstnUFalseNeg_Pig_,tstcUAll,tstcUDirFwd,tstcUIndFwd,tstcUDirBack,tstcUIndBack,tstcU_Bull_,tstcU_Dogsheep_,tstcU_Swine_,tstcU_Bulldog_,tstcU_Brownsheep_,tstcU_Doe_,tstcU_Pig_,tstcUDirFwd_Bull_,tstcUDirFwd_Dogsheep_,tstcUDirFwd_Swine_,tstcUDirFwd_Bulldog_,tstcUDirFwd_Brownsheep_,tstcUDirFwd_Doe_,tstcUDirFwd_Pig_,tstcUIndFwd_Bull_,tstcUIndFwd_Dogsheep_,tstcUIndFwd_Swine_,tstcUIndFwd_Bulldog_,tstcUIndFwd_Brownsheep_,tstcUIndFwd_Doe_,tstcUIndFwd_Pig_,tstcUDirBack_Bull_,tstcUDirBack_Dogsheep_,tstcUDirBack_Swine_,tstcUDirBack_Bulldog_,tstcUDirBack_Brownsheep_,tstcUDirBack_Doe_,tstcUDirBack_Pig_,tstcUIndBack_Bull_,tstcUIndBack_Dogsheep_,tstcUIndBack_Swine_,tstcUIndBack_Bulldog_,tstcUIndBack_Brownsheep_,tstcUIndBack_Doe_,tstcUIndBack_Pig_,tstcUTruePos,tstcUTruePos_Bull_,tstcUTruePos_Dogsheep_,tstcUTruePos_Swine_,tstcUTruePos_Bulldog_,tstcUTruePos_Brownsheep_,tstcUTruePos_Doe_,tstcUTruePos_Pig_,tstcUTrueNeg,tstcUTrueNeg_Bull_,tstcUTrueNeg_Dogsheep_,tstcUTrueNeg_Swine_,tstcUTrueNeg_Bulldog_,tstcUTrueNeg_Brownsheep_,tstcUTrueNeg_Doe_,tstcUTrueNeg_Pig_,tstcUFalsePos,tstcUFalsePos_Bull_,tstcUFalsePos_Dogsheep_,tstcUFalsePos_Swine_,tstcUFalsePos_Bulldog_,tstcUFalsePos_Brownsheep_,tstcUFalsePos_Doe_,tstcUFalsePos_Pig_,tstcUFalseNeg,tstcUFalseNeg_Bull_,tstcUFalseNeg_Dogsheep_,tstcUFalseNeg_Swine_,tstcUFalseNeg_Bulldog_,tstcUFalseNeg_Brownsheep_,tstcUFalseNeg_Doe_,tstcUFalseNeg_Pig_,tstcAAll,tstcADirFwd,tstcAIndFwd,tstcADirBack,tstcAIndBack,tstcA_Bull_,tstcA_Dogsheep_,tstcA_Swine_,tstcA_Bulldog_,tstcA_Brownsheep_,tstcA_Doe_,tstcA_Pig_,tstcADirFwd_Bull_,tstcADirFwd_Dogsheep_,tstcADirFwd_Swine_,tstcADirFwd_Bulldog_,tstcADirFwd_Brownsheep_,tstcADirFwd_Doe_,tstcADirFwd_Pig_,tstcAIndFwd_Bull_,tstcAIndFwd_Dogsheep_,tstcAIndFwd_Swine_,tstcAIndFwd_Bulldog_,tstcAIndFwd_Brownsheep_,tstcAIndFwd_Doe_,tstcAIndFwd_Pig_,tstcADirBack_Bull_,tstcADirBack_Dogsheep_,tstcADirBack_Swine_,tstcADirBack_Bulldog_,tstcADirBack_Brownsheep_,tstcADirBack_Doe_,tstcADirBack_Pig_,tstcAIndBack_Bull_,tstcAIndBack_Dogsheep_,tstcAIndBack_Swine_,tstcAIndBack_Bulldog_,tstcAIndBack_Brownsheep_,tstcAIndBack_Doe_,tstcAIndBack_Pig_,vaccOccurred,firstVaccination,firstVaccinationRing,firstVaccination_Bull_,firstVaccination_Dogsheep_,firstVaccination_Swine_,firstVaccination_Bulldog_,firstVaccination_Brownsheep_,firstVaccination_Doe_,firstVaccination_Pig_,firstVaccinationRing_Bull_,firstVaccinationRing_Dogsheep_,firstVaccinationRing_Swine_,firstVaccinationRing_Bulldog_,firstVaccinationRing_Brownsheep_,firstVaccinationRing_Doe_,firstVaccinationRing_Pig_,vacnUAll,vacnUIni,vacnURing,vacnU_Bull_,vacnU_Dogsheep_,vacnU_Swine_,vacnU_Bulldog_,vacnU_Brownsheep_,vacnU_Doe_,vacnU_Pig_,vacnUIni_Bull_,vacnUIni_Dogsheep_,vacnUIni_Swine_,vacnUIni_Bulldog_,vacnUIni_Brownsheep_,vacnUIni_Doe_,vacnUIni_Pig_,vacnURing_Bull_,vacnURing_Dogsheep_,vacnURing_Swine_,vacnURing_Bulldog_,vacnURing_Brownsheep_,vacnURing_Doe_,vacnURing_Pig_,vaccUAll,vaccUIni,vaccURing,vaccU_Bull_,vaccU_Dogsheep_,vaccU_Swine_,vaccU_Bulldog_,vaccU_Brownsheep_,vaccU_Doe_,vaccU_Pig_,vaccUIni_Bull_,vaccUIni_Dogsheep_,vaccUIni_Swine_,vaccUIni_Bulldog_,vaccUIni_Brownsheep_,vaccUIni_Doe_,vaccUIni_Pig_,vaccURing_Bull_,vaccURing_Dogsheep_,vaccURing_Swine_,vaccURing_Bulldog_,vaccURing_Brownsheep_,vaccURing_Doe_,vaccURing_Pig_,vacnAAll,vacnAIni,vacnARing,vacnA_Bull_,vacnA_Dogsheep_,vacnA_Swine_,vacnA_Bulldog_,vacnA_Brownsheep_,vacnA_Doe_,vacnA_Pig_,vacnAIni_Bull_,vacnAIni_Dogsheep_,vacnAIni_Swine_,vacnAIni_Bulldog_,vacnAIni_Brownsheep_,vacnAIni_Doe_,vacnAIni_Pig_,vacnARing_Bull_,vacnARing_Dogsheep_,vacnARing_Swine_,vacnARing_Bulldog_,vacnARing_Brownsheep_,vacnARing_Doe_,vacnARing_Pig_,vaccAAll,vaccAIni,vaccARing,vaccA_Bull_,vaccA_Dogsheep_,vaccA_Swine_,vaccA_Bulldog_,vaccA_Brownsheep_,vaccA_Doe_,vaccA_Pig_,vaccAIni_Bull_,vaccAIni_Dogsheep_,vaccAIni_Swine_,vaccAIni_Bulldog_,vaccAIni_Brownsheep_,vaccAIni_Doe_,vaccAIni_Pig_,vaccARing_Bull_,vaccARing_Dogsheep_,vaccARing_Swine_,vaccARing_Bulldog_,vaccARing_Brownsheep_,vaccARing_Doe_,vaccARing_Pig_,exmnUAll,exmnURing,exmnUDirFwd,exmnUIndFwd,exmnUDirBack,exmnUIndBack,exmnUDet,exmnU_Bull_,exmnU_Dogsheep_,exmnU_Swine_,exmnU_Bulldog_,exmnU_Brownsheep_,exmnU_Doe_,exmnU_Pig_,exmnURing_Bull_,exmnURing_Dogsheep_,exmnURing_Swine_,exmnURing_Bulldog_,exmnURing_Brownsheep_,exmnURing_Doe_,exmnURing_Pig_,exmnUDirFwd_Bull_,exmnUDirFwd_Dogsheep_,exmnUDirFwd_Swine_,exmnUDirFwd_Bulldog_,exmnUDirFwd_Brownsheep_,exmnUDirFwd_Doe_,exmnUDirFwd_Pig_,exmnUIndFwd_Bull_,exmnUIndFwd_Dogsheep_,exmnUIndFwd_Swine_,exmnUIndFwd_Bulldog_,exmnUIndFwd_Brownsheep_,exmnUIndFwd_Doe_,exmnUIndFwd_Pig_,exmnUDirBack_Bull_,exmnUDirBack_Dogsheep_,exmnUDirBack_Swine_,exmnUDirBack_Bulldog_,exmnUDirBack_Brownsheep_,exmnUDirBack_Doe_,exmnUDirBack_Pig_,exmnUIndBack_Bull_,exmnUIndBack_Dogsheep_,exmnUIndBack_Swine_,exmnUIndBack_Bulldog_,exmnUIndBack_Brownsheep_,exmnUIndBack_Doe_,exmnUIndBack_Pig_,exmnUDet_Bull_,exmnUDet_Dogsheep_,exmnUDet_Swine_,exmnUDet_Bulldog_,exmnUDet_Brownsheep_,exmnUDet_Doe_,exmnUDet_Pig_,exmnAAll,exmnARing,exmnADirFwd,exmnAIndFwd,exmnADirBack,exmnAIndBack,exmnADet,exmnA_Bull_,exmnA_Dogsheep_,exmnA_Swine_,exmnA_Bulldog_,exmnA_Brownsheep_,exmnA_Doe_,exmnA_Pig_,exmnARing_Bull_,exmnARing_Dogsheep_,exmnARing_Swine_,exmnARing_Bulldog_,exmnARing_Brownsheep_,exmnARing_Doe_,exmnARing_Pig_,exmnADirFwd_Bull_,exmnADirFwd_Dogsheep_,exmnADirFwd_Swine_,exmnADirFwd_Bulldog_,exmnADirFwd_Brownsheep_,exmnADirFwd_Doe_,exmnADirFwd_Pig_,exmnAIndFwd_Bull_,exmnAIndFwd_Dogsheep_,exmnAIndFwd_Swine_,exmnAIndFwd_Bulldog_,exmnAIndFwd_Brownsheep_,exmnAIndFwd_Doe_,exmnAIndFwd_Pig_,exmnADirBack_Bull_,exmnADirBack_Dogsheep_,exmnADirBack_Swine_,exmnADirBack_Bulldog_,exmnADirBack_Brownsheep_,exmnADirBack_Doe_,exmnADirBack_Pig_,exmnAIndBack_Bull_,exmnAIndBack_Dogsheep_,exmnAIndBack_Swine_,exmnAIndBack_Bulldog_,exmnAIndBack_Brownsheep_,exmnAIndBack_Doe_,exmnAIndBack_Pig_,exmnADet_Bull_,exmnADet_Dogsheep_,exmnADet_Swine_,exmnADet_Bulldog_,exmnADet_Brownsheep_,exmnADet_Doe_,exmnADet_Pig_,exmcUAll,exmcURing,exmcUDirFwd,exmcUIndFwd,exmcUDirBack,exmcUIndBack,exmcUDet,exmcU_Bull_,exmcU_Dogsheep_,exmcU_Swine_,exmcU_Bulldog_,exmcU_Brownsheep_,exmcU_Doe_,exmcU_Pig_,exmcURing_Bull_,exmcURing_Dogsheep_,exmcURing_Swine_,exmcURing_Bulldog_,exmcURing_Brownsheep_,exmcURing_Doe_,exmcURing_Pig_,exmcUDirFwd_Bull_,exmcUDirFwd_Dogsheep_,exmcUDirFwd_Swine_,exmcUDirFwd_Bulldog_,exmcUDirFwd_Brownsheep_,exmcUDirFwd_Doe_,exmcUDirFwd_Pig_,exmcUIndFwd_Bull_,exmcUIndFwd_Dogsheep_,exmcUIndFwd_Swine_,exmcUIndFwd_Bulldog_,exmcUIndFwd_Brownsheep_,exmcUIndFwd_Doe_,exmcUIndFwd_Pig_,exmcUDirBack_Bull_,exmcUDirBack_Dogsheep_,exmcUDirBack_Swine_,exmcUDirBack_Bulldog_,exmcUDirBack_Brownsheep_,exmcUDirBack_Doe_,exmcUDirBack_Pig_,exmcUIndBack_Bull_,exmcUIndBack_Dogsheep_,exmcUIndBack_Swine_,exmcUIndBack_Bulldog_,exmcUIndBack_Brownsheep_,exmcUIndBack_Doe_,exmcUIndBack_Pig_,exmcUDet_Bull_,exmcUDet_Dogsheep_,exmcUDet_Swine_,exmcUDet_Bulldog_,exmcUDet_Brownsheep_,exmcUDet_Doe_,exmcUDet_Pig_,exmcAAll,exmcARing,exmcADirFwd,exmcAIndFwd,exmcADirBack,exmcAIndBack,exmcADet,exmcA_Bull_,exmcA_Dogsheep_,exmcA_Swine_,exmcA_Bulldog_,exmcA_Brownsheep_,exmcA_Doe_,exmcA_Pig_,exmcARing_Bull_,exmcARing_Dogsheep_,exmcARing_Swine_,exmcARing_Bulldog_,exmcARing_Brownsheep_,exmcARing_Doe_,exmcARing_Pig_,exmcADirFwd_Bull_,exmcADirFwd_Dogsheep_,exmcADirFwd_Swine_,exmcADirFwd_Bulldog_,exmcADirFwd_Brownsheep_,exmcADirFwd_Doe_,exmcADirFwd_Pig_,exmcAIndFwd_Bull_,exmcAIndFwd_Dogsheep_,exmcAIndFwd_Swine_,exmcAIndFwd_Bulldog_,exmcAIndFwd_Brownsheep_,exmcAIndFwd_Doe_,exmcAIndFwd_Pig_,exmcADirBack_Bull_,exmcADirBack_Dogsheep_,exmcADirBack_Swine_,exmcADirBack_Bulldog_,exmcADirBack_Brownsheep_,exmcADirBack_Doe_,exmcADirBack_Pig_,exmcAIndBack_Bull_,exmcAIndBack_Dogsheep_,exmcAIndBack_Swine_,exmcAIndBack_Bulldog_,exmcAIndBack_Brownsheep_,exmcAIndBack_Doe_,exmcAIndBack_Pig_,exmcADet_Bull_,exmcADet_Dogsheep_,exmcADet_Swine_,exmcADet_Bulldog_,exmcADet_Brownsheep_,exmcADet_Doe_,exmcADet_Pig_"
headers = re.sub('_\w+_|All', '', headers) #removes production types
headers = re.sub('HighRisk|MediumRisk', '', headers) #removes zone names
# headers = re.sub('-', '_', headers) #there are 2 hyphenated fields:  average-prevalence num-separate-areasMediumRisk 
headers = headers.split(',')

# <codecell>

def count_empty_matches(field_matches):
    count = 0
    for field, matches in field_matches.items():
        if len(matches) == 0:
            count += 1
            print(field)
    print("Total:", count)

# <codecell>


def list_fields_from_code(new_code):
    class_and_field = {}
    for cls, code in new_code.items():
        class_and_field[cls] = {}
        for line in code:
            test = r'    (\w+) = '
            field = re.match(test, line).group(1) if re.match(test, line) else None
            if field:
                class_and_field[cls][field] = line
    return class_and_field

class_and_field = list_fields_from_code(new_code)

# <codecell>

def match_c_headers_to_model(class_and_field, headers):
    matches = {}
    for query_h in headers:
#         print('.', end='')
        matches[query_h] = []
        for cls, fields in class_and_field.items():
            for field in fields:
                if field in query_h or query_h in field:
                    matches[query_h].append( (field, cls) )
    return matches

matches = match_c_headers_to_model(class_and_field, headers)
count_empty_matches(matches)

# <codecell>


# <codecell>

def match_model_to_c_headers(class_and_field, headers):
    matches = {}
    for cls, fields in class_and_field.items():
        for field in fields:
#             print('.', end='')
            matches[field] = []
            for query_h in headers:
                if field in query_h or query_h in field:
                    matches[field].append( query_h )
    return matches

field_matches = match_model_to_c_headers(class_and_field, headers)
count_empty_matches(field_matches)

# <codecell>

[h for h in headers if 'trc' in h]

# <codecell>


# <headingcell level=2>

# Fields that don't match up:

# <markdowncell>

# Separate Fwd and Back:  
# trcUDirp  
#     	 [('trcUDirpBack', 'DailyByProductionType'), ('trcUDirpFwd', 'DailyByProductionType'), ('trcUDirpBack', 'IterationByProductionType'), ('trcUDirpFwd', 'IterationByProductionType')]

# <markdowncell>

# desnUIndBack_Brownsheep_  
#         desnUAll
#         desnAAll

# <markdowncell>

# average-prevalence
#     nothing even close

# <markdowncell>

# infnAIni
#     infnAInd is there.  Ini suffix is never seen

# <codecell>


# <codecell>


# <markdowncell>

# #New Output Spec
# 
# * Start with All columns generated by C Sim - listed in [Output Docs](https://github.com/NAVADMC/SpreadModel/wiki/Outputs)
# * Break down redundant information into tables based on Breakdown columns
# * One Table for each Breakdown Permutation (possibly not "Cause / Reason")
#  * Fields broken down by Cause/Reason will ForeignKey to a complex type with BackDirect,ForwardDirect,BackIndirect,ForwardDirect
# * Use Strippable column substrings to determine destination table
# * Calculate "Iteration" level statistics only after gathering "Daily Statistics"

# <codecell>

spec_headers = "expnU,expcU,expnA,expcA,infnU,infcU,infnA,infcA,firstDetection,lastDetection,detnU,detcU,detnA,detcA,trnUp,trnU,trcUp,trcU,trnAp,trnA,trcAp,trcA,exmnU,exmcU,exmnA,exmcA,tstcU,tstcA,firstVaccination,vacnU,vaccU,vacnA,vaccA,firstDestruction,desnU,descU,desnA,descA,tsdUSusc,tsdULat,tsdUSubc,tsdUClin,tsdUNImm,tsdUVImm,tsdUDest,tsdASusc,tsdALat,tsdASubc,tsdAClin,tsdANImm,tsdAVImm,tsdADest,tstcUTruePos,tstcUTrueNeg,tstcUFalsePos,tstcUFalseNeg,vacwU,vacwA,deswU,deswA,unitsInZone,unitDaysInZone,animalDaysInZone,zoneArea,maxZoneArea,maxZoneAreaDay,zonePerimeter,maxZonePerimeter,maxZonePerimeterDay,diseaseDuration,adqnU,adqcU,detOccurred,costSurveillance,vaccOccurred,vacwUMax,vacwUMaxDay,vacwUDaysInQueue,vacwUTimeAvg,vacwUTimeMax,vacwAMax,vacwAMaxDay,vacwADaysInQueue,vaccSetup,vaccVaccination,vaccSubtotal,destrOccurred,deswUMax,deswUMaxDay,deswUDaysInQueue,deswUTimeAvg,deswUTimeMax,deswAMax,deswAMaxDay,deswADaysInQueue,destrAppraisal,destrEuthanasia,destrIndemnification,destrDisposal,destrCleaning,destrSubtotal,outbreakDuration,costsTotal".split(',')

# <codecell>

print('\n'.join([column for column in spec_headers if not len(substr_indices(headers, column))]))

# <codecell>

print([h for h in spec_headers if 'ex' in h])

# <headingcell level=3>

# New Spec Declaration

# <codecell>

new_spec = {}
new_spec['DailyByProductionType'] = "expnU,expcU,expnA,expcA,infnU,infcU,infnA,infcA,firstDetection,lastDetection,detnU,detcU,detnA,detcA,trnUp,trnU,trcUp,trcU,trnAp,trnA,trcAp,trcA,exmnU,exmcU,exmnA,exmcA,tstcU,tstcA,firstVaccination,vacnU,vaccU,vacnA,vaccA,firstDestruction,desnU,descU,desnA,descA,tsdUSusc,tsdULat,tsdUSubc,tsdUClin,tsdUNImm,tsdUVImm,tsdUDest,tsdASusc,tsdALat,tsdASubc,tsdAClin,tsdANImm,tsdAVImm,tsdADest,tstcUTruePos,tstcUTrueNeg,tstcUFalsePos,tstcUFalseNeg,vacwU,vacwA,deswU,deswA".split(',')
new_spec['DailyByZoneAndProductionType'] = "unitsInZone,unitDaysInZone,animalDaysInZone".split(',')
new_spec['DailyByZone'] = "zoneArea,maxZoneArea,maxZoneAreaDay,zonePerimeter,maxZonePerimeter,maxZonePerimeterDay".split(',')
new_spec['DailyControls'] = "diseaseDuration,adqnU,adqcU,detOccurred,costSurveillance,vaccOccurred,vacwUMax,vacwUMaxDay,vacwUDaysInQueue,vacwUTimeAvg,vacwUTimeMax,vacwAMax,vacwAMaxDay,vacwADaysInQueue,vaccSetup,vaccVaccination,vaccSubtotal,destrOccurred,deswUMax,deswUMaxDay,deswUDaysInQueue,deswUTimeAvg,deswUTimeMax,deswAMax,deswAMaxDay,deswADaysInQueue,destrAppraisal,destrEuthanasia,destrIndemnification,destrDisposal,destrCleaning,destrSubtotal,outbreakDuration,costsTotal".split(',')

# <codecell>

raw_headers = "Run,Day,outbreakDuration,infnUAll,infnUDir,infnUInd,infnUAir,infnUIni,infnU_Bull_,infnU_Dogsheep_,infnU_Swine_,infnU_Bulldog_,infnU_Brownsheep_,infnU_Doe_,infnU_Pig_,infnUDir_Bull_,infnUDir_Dogsheep_,infnUDir_Swine_,infnUDir_Bulldog_,infnUDir_Brownsheep_,infnUDir_Doe_,infnUDir_Pig_,infnUInd_Bull_,infnUInd_Dogsheep_,infnUInd_Swine_,infnUInd_Bulldog_,infnUInd_Brownsheep_,infnUInd_Doe_,infnUInd_Pig_,infnUAir_Bull_,infnUAir_Dogsheep_,infnUAir_Swine_,infnUAir_Bulldog_,infnUAir_Brownsheep_,infnUAir_Doe_,infnUAir_Pig_,infnUIni_Bull_,infnUIni_Dogsheep_,infnUIni_Swine_,infnUIni_Bulldog_,infnUIni_Brownsheep_,infnUIni_Doe_,infnUIni_Pig_,infcUAll,infcUDir,infcUInd,infcUAir,infcUIni,infcU_Bull_,infcU_Dogsheep_,infcU_Swine_,infcU_Bulldog_,infcU_Brownsheep_,infcU_Doe_,infcU_Pig_,infcUDir_Bull_,infcUDir_Dogsheep_,infcUDir_Swine_,infcUDir_Bulldog_,infcUDir_Brownsheep_,infcUDir_Doe_,infcUDir_Pig_,infcUInd_Bull_,infcUInd_Dogsheep_,infcUInd_Swine_,infcUInd_Bulldog_,infcUInd_Brownsheep_,infcUInd_Doe_,infcUInd_Pig_,infcUAir_Bull_,infcUAir_Dogsheep_,infcUAir_Swine_,infcUAir_Bulldog_,infcUAir_Brownsheep_,infcUAir_Doe_,infcUAir_Pig_,infcUIni_Bull_,infcUIni_Dogsheep_,infcUIni_Swine_,infcUIni_Bulldog_,infcUIni_Brownsheep_,infcUIni_Doe_,infcUIni_Pig_,infnAAll,infnADir,infnAInd,infnAAir,infnAIni,infnA_Bull_,infnA_Dogsheep_,infnA_Swine_,infnA_Bulldog_,infnA_Brownsheep_,infnA_Doe_,infnA_Pig_,infnADir_Bull_,infnADir_Dogsheep_,infnADir_Swine_,infnADir_Bulldog_,infnADir_Brownsheep_,infnADir_Doe_,infnADir_Pig_,infnAInd_Bull_,infnAInd_Dogsheep_,infnAInd_Swine_,infnAInd_Bulldog_,infnAInd_Brownsheep_,infnAInd_Doe_,infnAInd_Pig_,infnAAir_Bull_,infnAAir_Dogsheep_,infnAAir_Swine_,infnAAir_Bulldog_,infnAAir_Brownsheep_,infnAAir_Doe_,infnAAir_Pig_,infnAIni_Bull_,infnAIni_Dogsheep_,infnAIni_Swine_,infnAIni_Bulldog_,infnAIni_Brownsheep_,infnAIni_Doe_,infnAIni_Pig_,infcAAll,infcADir,infcAInd,infcAAir,infcAIni,infcA_Bull_,infcA_Dogsheep_,infcA_Swine_,infcA_Bulldog_,infcA_Brownsheep_,infcA_Doe_,infcA_Pig_,infcADir_Bull_,infcADir_Dogsheep_,infcADir_Swine_,infcADir_Bulldog_,infcADir_Brownsheep_,infcADir_Doe_,infcADir_Pig_,infcAInd_Bull_,infcAInd_Dogsheep_,infcAInd_Swine_,infcAInd_Bulldog_,infcAInd_Brownsheep_,infcAInd_Doe_,infcAInd_Pig_,infcAAir_Bull_,infcAAir_Dogsheep_,infcAAir_Swine_,infcAAir_Bulldog_,infcAAir_Brownsheep_,infcAAir_Doe_,infcAAir_Pig_,infcAIni_Bull_,infcAIni_Dogsheep_,infcAIni_Swine_,infcAIni_Bulldog_,infcAIni_Brownsheep_,infcAIni_Doe_,infcAIni_Pig_,firstDetUInfAll,firstDetAInfAll,ratio,expnUAll,expnUDir,expnUInd,expnUAir,expnU_Bull_,expnU_Dogsheep_,expnU_Swine_,expnU_Bulldog_,expnU_Brownsheep_,expnU_Doe_,expnU_Pig_,expnUDir_Bull_,expnUDir_Dogsheep_,expnUDir_Swine_,expnUDir_Bulldog_,expnUDir_Brownsheep_,expnUDir_Doe_,expnUDir_Pig_,expnUInd_Bull_,expnUInd_Dogsheep_,expnUInd_Swine_,expnUInd_Bulldog_,expnUInd_Brownsheep_,expnUInd_Doe_,expnUInd_Pig_,expnUAir_Bull_,expnUAir_Dogsheep_,expnUAir_Swine_,expnUAir_Bulldog_,expnUAir_Brownsheep_,expnUAir_Doe_,expnUAir_Pig_,expcUAll,expcUDir,expcUInd,expcUAir,expcU_Bull_,expcU_Dogsheep_,expcU_Swine_,expcU_Bulldog_,expcU_Brownsheep_,expcU_Doe_,expcU_Pig_,expcUDir_Bull_,expcUDir_Dogsheep_,expcUDir_Swine_,expcUDir_Bulldog_,expcUDir_Brownsheep_,expcUDir_Doe_,expcUDir_Pig_,expcUInd_Bull_,expcUInd_Dogsheep_,expcUInd_Swine_,expcUInd_Bulldog_,expcUInd_Brownsheep_,expcUInd_Doe_,expcUInd_Pig_,expcUAir_Bull_,expcUAir_Dogsheep_,expcUAir_Swine_,expcUAir_Bulldog_,expcUAir_Brownsheep_,expcUAir_Doe_,expcUAir_Pig_,expnAAll,expnADir,expnAInd,expnAAir,expnA_Bull_,expnA_Dogsheep_,expnA_Swine_,expnA_Bulldog_,expnA_Brownsheep_,expnA_Doe_,expnA_Pig_,expnADir_Bull_,expnADir_Dogsheep_,expnADir_Swine_,expnADir_Bulldog_,expnADir_Brownsheep_,expnADir_Doe_,expnADir_Pig_,expnAInd_Bull_,expnAInd_Dogsheep_,expnAInd_Swine_,expnAInd_Bulldog_,expnAInd_Brownsheep_,expnAInd_Doe_,expnAInd_Pig_,expnAAir_Bull_,expnAAir_Dogsheep_,expnAAir_Swine_,expnAAir_Bulldog_,expnAAir_Brownsheep_,expnAAir_Doe_,expnAAir_Pig_,expcAAll,expcADir,expcAInd,expcAAir,expcA_Bull_,expcA_Dogsheep_,expcA_Swine_,expcA_Bulldog_,expcA_Brownsheep_,expcA_Doe_,expcA_Pig_,expcADir_Bull_,expcADir_Dogsheep_,expcADir_Swine_,expcADir_Bulldog_,expcADir_Brownsheep_,expcADir_Doe_,expcADir_Pig_,expcAInd_Bull_,expcAInd_Dogsheep_,expcAInd_Swine_,expcAInd_Bulldog_,expcAInd_Brownsheep_,expcAInd_Doe_,expcAInd_Pig_,expcAAir_Bull_,expcAAir_Dogsheep_,expcAAir_Swine_,expcAAir_Bulldog_,expcAAir_Brownsheep_,expcAAir_Doe_,expcAAir_Pig_,adqnUAll,adqcUAll,vacwUAll,vacwU_Bull_,vacwU_Dogsheep_,vacwU_Swine_,vacwU_Bulldog_,vacwU_Brownsheep_,vacwU_Doe_,vacwU_Pig_,vacwAAll,vacwA_Bull_,vacwA_Dogsheep_,vacwA_Swine_,vacwA_Bulldog_,vacwA_Brownsheep_,vacwA_Doe_,vacwA_Pig_,vacwUMax,vacwUMaxDay,vacwAMax,vacwAMaxDay,vacwUTimeMax,vacwUTimeAvg,vacwUDaysInQueue,vacwADaysInQueue,zoneAreaHighRisk,zoneAreaMediumRisk,maxZoneAreaHighRisk,maxZoneAreaMediumRisk,maxZoneAreaDayHighRisk,maxZoneAreaDayMediumRisk,finalZoneAreaHighRisk,finalZoneAreaMediumRisk,zonePerimeterHighRisk,zonePerimeterMediumRisk,maxZonePerimeterHighRisk,maxZonePerimeterMediumRisk,maxZonePerimeterDayHighRisk,maxZonePerimeterDayMediumRisk,finalZonePerimeterHighRisk,finalZonePerimeterMediumRisk,num-separate-areasHighRisk,num-separate-areasMediumRisk,unitsInZoneHighRisk,unitsInZoneMediumRisk,unitsInZoneBackground,unitsInZoneHighRisk_Bull_,unitsInZoneHighRisk_Dogsheep_,unitsInZoneHighRisk_Swine_,unitsInZoneHighRisk_Bulldog_,unitsInZoneHighRisk_Brownsheep_,unitsInZoneHighRisk_Doe_,unitsInZoneHighRisk_Pig_,unitsInZoneMediumRisk_Bull_,unitsInZoneMediumRisk_Dogsheep_,unitsInZoneMediumRisk_Swine_,unitsInZoneMediumRisk_Bulldog_,unitsInZoneMediumRisk_Brownsheep_,unitsInZoneMediumRisk_Doe_,unitsInZoneMediumRisk_Pig_,unitsInZoneBackground_Bull_,unitsInZoneBackground_Dogsheep_,unitsInZoneBackground_Swine_,unitsInZoneBackground_Bulldog_,unitsInZoneBackground_Brownsheep_,unitsInZoneBackground_Doe_,unitsInZoneBackground_Pig_,unitDaysInZoneHighRisk,unitDaysInZoneMediumRisk,unitDaysInZoneBackground,unitDaysInZoneHighRisk_Bull_,unitDaysInZoneHighRisk_Dogsheep_,unitDaysInZoneHighRisk_Swine_,unitDaysInZoneHighRisk_Bulldog_,unitDaysInZoneHighRisk_Brownsheep_,unitDaysInZoneHighRisk_Doe_,unitDaysInZoneHighRisk_Pig_,unitDaysInZoneMediumRisk_Bull_,unitDaysInZoneMediumRisk_Dogsheep_,unitDaysInZoneMediumRisk_Swine_,unitDaysInZoneMediumRisk_Bulldog_,unitDaysInZoneMediumRisk_Brownsheep_,unitDaysInZoneMediumRisk_Doe_,unitDaysInZoneMediumRisk_Pig_,unitDaysInZoneBackground_Bull_,unitDaysInZoneBackground_Dogsheep_,unitDaysInZoneBackground_Swine_,unitDaysInZoneBackground_Bulldog_,unitDaysInZoneBackground_Brownsheep_,unitDaysInZoneBackground_Doe_,unitDaysInZoneBackground_Pig_,animalDaysInZoneHighRisk,animalDaysInZoneMediumRisk,animalDaysInZoneBackground,animalDaysInZoneHighRisk_Bull_,animalDaysInZoneHighRisk_Dogsheep_,animalDaysInZoneHighRisk_Swine_,animalDaysInZoneHighRisk_Bulldog_,animalDaysInZoneHighRisk_Brownsheep_,animalDaysInZoneHighRisk_Doe_,animalDaysInZoneHighRisk_Pig_,animalDaysInZoneMediumRisk_Bull_,animalDaysInZoneMediumRisk_Dogsheep_,animalDaysInZoneMediumRisk_Swine_,animalDaysInZoneMediumRisk_Bulldog_,animalDaysInZoneMediumRisk_Brownsheep_,animalDaysInZoneMediumRisk_Doe_,animalDaysInZoneMediumRisk_Pig_,animalDaysInZoneBackground_Bull_,animalDaysInZoneBackground_Dogsheep_,animalDaysInZoneBackground_Swine_,animalDaysInZoneBackground_Bulldog_,animalDaysInZoneBackground_Brownsheep_,animalDaysInZoneBackground_Doe_,animalDaysInZoneBackground_Pig_,deswUAll,deswU_Bull_,deswU_Dogsheep_,deswU_Swine_,deswU_Bulldog_,deswU_Brownsheep_,deswU_Doe_,deswU_Pig_,deswAAll,deswA_Bull_,deswA_Dogsheep_,deswA_Swine_,deswA_Bulldog_,deswA_Brownsheep_,deswA_Doe_,deswA_Pig_,deswUMax,deswUMaxDay,deswAMax,deswAMaxDay,deswUTimeMax,deswUTimeAvg,deswUDaysInQueue,deswADaysInQueue,destrOccurred,firstDestruction,firstDestructionUnsp,firstDestructionRing,firstDestructionDirFwd,firstDestructionIndFwd,firstDestructionDirBack,firstDestructionIndBack,firstDestructionDet,firstDestructionIni,firstDestruction_Bull_,firstDestruction_Dogsheep_,firstDestruction_Swine_,firstDestruction_Bulldog_,firstDestruction_Brownsheep_,firstDestruction_Doe_,firstDestruction_Pig_,firstDestructionUnsp_Bull_,firstDestructionUnsp_Dogsheep_,firstDestructionUnsp_Swine_,firstDestructionUnsp_Bulldog_,firstDestructionUnsp_Brownsheep_,firstDestructionUnsp_Doe_,firstDestructionUnsp_Pig_,firstDestructionRing_Bull_,firstDestructionRing_Dogsheep_,firstDestructionRing_Swine_,firstDestructionRing_Bulldog_,firstDestructionRing_Brownsheep_,firstDestructionRing_Doe_,firstDestructionRing_Pig_,firstDestructionDirFwd_Bull_,firstDestructionDirFwd_Dogsheep_,firstDestructionDirFwd_Swine_,firstDestructionDirFwd_Bulldog_,firstDestructionDirFwd_Brownsheep_,firstDestructionDirFwd_Doe_,firstDestructionDirFwd_Pig_,firstDestructionIndFwd_Bull_,firstDestructionIndFwd_Dogsheep_,firstDestructionIndFwd_Swine_,firstDestructionIndFwd_Bulldog_,firstDestructionIndFwd_Brownsheep_,firstDestructionIndFwd_Doe_,firstDestructionIndFwd_Pig_,firstDestructionDirBack_Bull_,firstDestructionDirBack_Dogsheep_,firstDestructionDirBack_Swine_,firstDestructionDirBack_Bulldog_,firstDestructionDirBack_Brownsheep_,firstDestructionDirBack_Doe_,firstDestructionDirBack_Pig_,firstDestructionIndBack_Bull_,firstDestructionIndBack_Dogsheep_,firstDestructionIndBack_Swine_,firstDestructionIndBack_Bulldog_,firstDestructionIndBack_Brownsheep_,firstDestructionIndBack_Doe_,firstDestructionIndBack_Pig_,firstDestructionDet_Bull_,firstDestructionDet_Dogsheep_,firstDestructionDet_Swine_,firstDestructionDet_Bulldog_,firstDestructionDet_Brownsheep_,firstDestructionDet_Doe_,firstDestructionDet_Pig_,firstDestructionIni_Bull_,firstDestructionIni_Dogsheep_,firstDestructionIni_Swine_,firstDestructionIni_Bulldog_,firstDestructionIni_Brownsheep_,firstDestructionIni_Doe_,firstDestructionIni_Pig_,desnUAll,desnUIni,desnUUnsp,desnURing,desnUDirFwd,desnUIndFwd,desnUDirBack,desnUIndBack,desnUDet,desnU_Bull_,desnU_Dogsheep_,desnU_Swine_,desnU_Bulldog_,desnU_Brownsheep_,desnU_Doe_,desnU_Pig_,desnUIni_Bull_,desnUIni_Dogsheep_,desnUIni_Swine_,desnUIni_Bulldog_,desnUIni_Brownsheep_,desnUIni_Doe_,desnUIni_Pig_,desnUUnsp_Bull_,desnUUnsp_Dogsheep_,desnUUnsp_Swine_,desnUUnsp_Bulldog_,desnUUnsp_Brownsheep_,desnUUnsp_Doe_,desnUUnsp_Pig_,desnURing_Bull_,desnURing_Dogsheep_,desnURing_Swine_,desnURing_Bulldog_,desnURing_Brownsheep_,desnURing_Doe_,desnURing_Pig_,desnUDirFwd_Bull_,desnUDirFwd_Dogsheep_,desnUDirFwd_Swine_,desnUDirFwd_Bulldog_,desnUDirFwd_Brownsheep_,desnUDirFwd_Doe_,desnUDirFwd_Pig_,desnUIndFwd_Bull_,desnUIndFwd_Dogsheep_,desnUIndFwd_Swine_,desnUIndFwd_Bulldog_,desnUIndFwd_Brownsheep_,desnUIndFwd_Doe_,desnUIndFwd_Pig_,desnUDirBack_Bull_,desnUDirBack_Dogsheep_,desnUDirBack_Swine_,desnUDirBack_Bulldog_,desnUDirBack_Brownsheep_,desnUDirBack_Doe_,desnUDirBack_Pig_,desnUIndBack_Bull_,desnUIndBack_Dogsheep_,desnUIndBack_Swine_,desnUIndBack_Bulldog_,desnUIndBack_Brownsheep_,desnUIndBack_Doe_,desnUIndBack_Pig_,desnUDet_Bull_,desnUDet_Dogsheep_,desnUDet_Swine_,desnUDet_Bulldog_,desnUDet_Brownsheep_,desnUDet_Doe_,desnUDet_Pig_,descUAll,descUIni,descUUnsp,descURing,descUDirFwd,descUIndFwd,descUDirBack,descUIndBack,descUDet,descU_Bull_,descU_Dogsheep_,descU_Swine_,descU_Bulldog_,descU_Brownsheep_,descU_Doe_,descU_Pig_,descUIni_Bull_,descUIni_Dogsheep_,descUIni_Swine_,descUIni_Bulldog_,descUIni_Brownsheep_,descUIni_Doe_,descUIni_Pig_,descUUnsp_Bull_,descUUnsp_Dogsheep_,descUUnsp_Swine_,descUUnsp_Bulldog_,descUUnsp_Brownsheep_,descUUnsp_Doe_,descUUnsp_Pig_,descURing_Bull_,descURing_Dogsheep_,descURing_Swine_,descURing_Bulldog_,descURing_Brownsheep_,descURing_Doe_,descURing_Pig_,descUDirFwd_Bull_,descUDirFwd_Dogsheep_,descUDirFwd_Swine_,descUDirFwd_Bulldog_,descUDirFwd_Brownsheep_,descUDirFwd_Doe_,descUDirFwd_Pig_,descUIndFwd_Bull_,descUIndFwd_Dogsheep_,descUIndFwd_Swine_,descUIndFwd_Bulldog_,descUIndFwd_Brownsheep_,descUIndFwd_Doe_,descUIndFwd_Pig_,descUDirBack_Bull_,descUDirBack_Dogsheep_,descUDirBack_Swine_,descUDirBack_Bulldog_,descUDirBack_Brownsheep_,descUDirBack_Doe_,descUDirBack_Pig_,descUIndBack_Bull_,descUIndBack_Dogsheep_,descUIndBack_Swine_,descUIndBack_Bulldog_,descUIndBack_Brownsheep_,descUIndBack_Doe_,descUIndBack_Pig_,descUDet_Bull_,descUDet_Dogsheep_,descUDet_Swine_,descUDet_Bulldog_,descUDet_Brownsheep_,descUDet_Doe_,descUDet_Pig_,desnAAll,desnAIni,desnAUnsp,desnARing,desnADirFwd,desnAIndFwd,desnADirBack,desnAIndBack,desnADet,desnA_Bull_,desnA_Dogsheep_,desnA_Swine_,desnA_Bulldog_,desnA_Brownsheep_,desnA_Doe_,desnA_Pig_,desnAIni_Bull_,desnAIni_Dogsheep_,desnAIni_Swine_,desnAIni_Bulldog_,desnAIni_Brownsheep_,desnAIni_Doe_,desnAIni_Pig_,desnAUnsp_Bull_,desnAUnsp_Dogsheep_,desnAUnsp_Swine_,desnAUnsp_Bulldog_,desnAUnsp_Brownsheep_,desnAUnsp_Doe_,desnAUnsp_Pig_,desnARing_Bull_,desnARing_Dogsheep_,desnARing_Swine_,desnARing_Bulldog_,desnARing_Brownsheep_,desnARing_Doe_,desnARing_Pig_,desnADirFwd_Bull_,desnADirFwd_Dogsheep_,desnADirFwd_Swine_,desnADirFwd_Bulldog_,desnADirFwd_Brownsheep_,desnADirFwd_Doe_,desnADirFwd_Pig_,desnAIndFwd_Bull_,desnAIndFwd_Dogsheep_,desnAIndFwd_Swine_,desnAIndFwd_Bulldog_,desnAIndFwd_Brownsheep_,desnAIndFwd_Doe_,desnAIndFwd_Pig_,desnADirBack_Bull_,desnADirBack_Dogsheep_,desnADirBack_Swine_,desnADirBack_Bulldog_,desnADirBack_Brownsheep_,desnADirBack_Doe_,desnADirBack_Pig_,desnAIndBack_Bull_,desnAIndBack_Dogsheep_,desnAIndBack_Swine_,desnAIndBack_Bulldog_,desnAIndBack_Brownsheep_,desnAIndBack_Doe_,desnAIndBack_Pig_,desnADet_Bull_,desnADet_Dogsheep_,desnADet_Swine_,desnADet_Bulldog_,desnADet_Brownsheep_,desnADet_Doe_,desnADet_Pig_,descAAll,descAIni,descAUnsp,descARing,descADirFwd,descAIndFwd,descADirBack,descAIndBack,descADet,descA_Bull_,descA_Dogsheep_,descA_Swine_,descA_Bulldog_,descA_Brownsheep_,descA_Doe_,descA_Pig_,descAIni_Bull_,descAIni_Dogsheep_,descAIni_Swine_,descAIni_Bulldog_,descAIni_Brownsheep_,descAIni_Doe_,descAIni_Pig_,descAUnsp_Bull_,descAUnsp_Dogsheep_,descAUnsp_Swine_,descAUnsp_Bulldog_,descAUnsp_Brownsheep_,descAUnsp_Doe_,descAUnsp_Pig_,descARing_Bull_,descARing_Dogsheep_,descARing_Swine_,descARing_Bulldog_,descARing_Brownsheep_,descARing_Doe_,descARing_Pig_,descADirFwd_Bull_,descADirFwd_Dogsheep_,descADirFwd_Swine_,descADirFwd_Bulldog_,descADirFwd_Brownsheep_,descADirFwd_Doe_,descADirFwd_Pig_,descAIndFwd_Bull_,descAIndFwd_Dogsheep_,descAIndFwd_Swine_,descAIndFwd_Bulldog_,descAIndFwd_Brownsheep_,descAIndFwd_Doe_,descAIndFwd_Pig_,descADirBack_Bull_,descADirBack_Dogsheep_,descADirBack_Swine_,descADirBack_Bulldog_,descADirBack_Brownsheep_,descADirBack_Doe_,descADirBack_Pig_,descAIndBack_Bull_,descAIndBack_Dogsheep_,descAIndBack_Swine_,descAIndBack_Bulldog_,descAIndBack_Brownsheep_,descAIndBack_Doe_,descAIndBack_Pig_,descADet_Bull_,descADet_Dogsheep_,descADet_Swine_,descADet_Bulldog_,descADet_Brownsheep_,descADet_Doe_,descADet_Pig_,trnUAllp,trnUDirp,trnUIndp,trnU_Bull_p,trnU_Dogsheep_p,trnU_Swine_p,trnU_Bulldog_p,trnU_Brownsheep_p,trnU_Doe_p,trnU_Pig_p,trnUDir_Bull_p,trnUDir_Dogsheep_p,trnUDir_Swine_p,trnUDir_Bulldog_p,trnUDir_Brownsheep_p,trnUDir_Doe_p,trnUDir_Pig_p,trnUInd_Bull_p,trnUInd_Dogsheep_p,trnUInd_Swine_p,trnUInd_Bulldog_p,trnUInd_Brownsheep_p,trnUInd_Doe_p,trnUInd_Pig_p,trcUAllp,trcUDirp,trcUIndp,trcU_Bull_p,trcU_Dogsheep_p,trcU_Swine_p,trcU_Bulldog_p,trcU_Brownsheep_p,trcU_Doe_p,trcU_Pig_p,trcUDir_Bull_p,trcUDir_Dogsheep_p,trcUDir_Swine_p,trcUDir_Bulldog_p,trcUDir_Brownsheep_p,trcUDir_Doe_p,trcUDir_Pig_p,trcUInd_Bull_p,trcUInd_Dogsheep_p,trcUInd_Swine_p,trcUInd_Bulldog_p,trcUInd_Brownsheep_p,trcUInd_Doe_p,trcUInd_Pig_p,trnUAll,trnUDir,trnUInd,trnU_Bull_,trnU_Dogsheep_,trnU_Swine_,trnU_Bulldog_,trnU_Brownsheep_,trnU_Doe_,trnU_Pig_,trnUDir_Bull_,trnUDir_Dogsheep_,trnUDir_Swine_,trnUDir_Bulldog_,trnUDir_Brownsheep_,trnUDir_Doe_,trnUDir_Pig_,trnUInd_Bull_,trnUInd_Dogsheep_,trnUInd_Swine_,trnUInd_Bulldog_,trnUInd_Brownsheep_,trnUInd_Doe_,trnUInd_Pig_,trcUAll,trcUDir,trcUInd,trcU_Bull_,trcU_Dogsheep_,trcU_Swine_,trcU_Bulldog_,trcU_Brownsheep_,trcU_Doe_,trcU_Pig_,trcUDir_Bull_,trcUDir_Dogsheep_,trcUDir_Swine_,trcUDir_Bulldog_,trcUDir_Brownsheep_,trcUDir_Doe_,trcUDir_Pig_,trcUInd_Bull_,trcUInd_Dogsheep_,trcUInd_Swine_,trcUInd_Bulldog_,trcUInd_Brownsheep_,trcUInd_Doe_,trcUInd_Pig_,trnAAllp,trnADirp,trnAIndp,trnA_Bull_p,trnA_Dogsheep_p,trnA_Swine_p,trnA_Bulldog_p,trnA_Brownsheep_p,trnA_Doe_p,trnA_Pig_p,trnADir_Bull_p,trnADir_Dogsheep_p,trnADir_Swine_p,trnADir_Bulldog_p,trnADir_Brownsheep_p,trnADir_Doe_p,trnADir_Pig_p,trnAInd_Bull_p,trnAInd_Dogsheep_p,trnAInd_Swine_p,trnAInd_Bulldog_p,trnAInd_Brownsheep_p,trnAInd_Doe_p,trnAInd_Pig_p,trcAAllp,trcADirp,trcAIndp,trcA_Bull_p,trcA_Dogsheep_p,trcA_Swine_p,trcA_Bulldog_p,trcA_Brownsheep_p,trcA_Doe_p,trcA_Pig_p,trcADir_Bull_p,trcADir_Dogsheep_p,trcADir_Swine_p,trcADir_Bulldog_p,trcADir_Brownsheep_p,trcADir_Doe_p,trcADir_Pig_p,trcAInd_Bull_p,trcAInd_Dogsheep_p,trcAInd_Swine_p,trcAInd_Bulldog_p,trcAInd_Brownsheep_p,trcAInd_Doe_p,trcAInd_Pig_p,trnAAll,trnADir,trnAInd,trnA_Bull_,trnA_Dogsheep_,trnA_Swine_,trnA_Bulldog_,trnA_Brownsheep_,trnA_Doe_,trnA_Pig_,trnADir_Bull_,trnADir_Dogsheep_,trnADir_Swine_,trnADir_Bulldog_,trnADir_Brownsheep_,trnADir_Doe_,trnADir_Pig_,trnAInd_Bull_,trnAInd_Dogsheep_,trnAInd_Swine_,trnAInd_Bulldog_,trnAInd_Brownsheep_,trnAInd_Doe_,trnAInd_Pig_,trcAAll,trcADir,trcAInd,trcA_Bull_,trcA_Dogsheep_,trcA_Swine_,trcA_Bulldog_,trcA_Brownsheep_,trcA_Doe_,trcA_Pig_,trcADir_Bull_,trcADir_Dogsheep_,trcADir_Swine_,trcADir_Bulldog_,trcADir_Brownsheep_,trcADir_Doe_,trcADir_Pig_,trcAInd_Bull_,trcAInd_Dogsheep_,trcAInd_Swine_,trcAInd_Bulldog_,trcAInd_Brownsheep_,trcAInd_Doe_,trcAInd_Pig_,detOccurred,firstDetection,firstDetectionClin,firstDetectionTest,firstDetection_Bull_,firstDetection_Dogsheep_,firstDetection_Swine_,firstDetection_Bulldog_,firstDetection_Brownsheep_,firstDetection_Doe_,firstDetection_Pig_,firstDetectionClin_Bull_,firstDetectionClin_Dogsheep_,firstDetectionClin_Swine_,firstDetectionClin_Bulldog_,firstDetectionClin_Brownsheep_,firstDetectionClin_Doe_,firstDetectionClin_Pig_,firstDetectionTest_Bull_,firstDetectionTest_Dogsheep_,firstDetectionTest_Swine_,firstDetectionTest_Bulldog_,firstDetectionTest_Brownsheep_,firstDetectionTest_Doe_,firstDetectionTest_Pig_,lastDetection,lastDetectionClin,lastDetectionTest,lastDetection_Bull_,lastDetection_Dogsheep_,lastDetection_Swine_,lastDetection_Bulldog_,lastDetection_Brownsheep_,lastDetection_Doe_,lastDetection_Pig_,lastDetectionClin_Bull_,lastDetectionClin_Dogsheep_,lastDetectionClin_Swine_,lastDetectionClin_Bulldog_,lastDetectionClin_Brownsheep_,lastDetectionClin_Doe_,lastDetectionClin_Pig_,lastDetectionTest_Bull_,lastDetectionTest_Dogsheep_,lastDetectionTest_Swine_,lastDetectionTest_Bulldog_,lastDetectionTest_Brownsheep_,lastDetectionTest_Doe_,lastDetectionTest_Pig_,detnUAll,detnUClin,detnUTest,detnU_Bull_,detnU_Dogsheep_,detnU_Swine_,detnU_Bulldog_,detnU_Brownsheep_,detnU_Doe_,detnU_Pig_,detnUClin_Bull_,detnUClin_Dogsheep_,detnUClin_Swine_,detnUClin_Bulldog_,detnUClin_Brownsheep_,detnUClin_Doe_,detnUClin_Pig_,detnUTest_Bull_,detnUTest_Dogsheep_,detnUTest_Swine_,detnUTest_Bulldog_,detnUTest_Brownsheep_,detnUTest_Doe_,detnUTest_Pig_,detnAAll,detnAClin,detnATest,detnA_Bull_,detnA_Dogsheep_,detnA_Swine_,detnA_Bulldog_,detnA_Brownsheep_,detnA_Doe_,detnA_Pig_,detnAClin_Bull_,detnAClin_Dogsheep_,detnAClin_Swine_,detnAClin_Bulldog_,detnAClin_Brownsheep_,detnAClin_Doe_,detnAClin_Pig_,detnATest_Bull_,detnATest_Dogsheep_,detnATest_Swine_,detnATest_Bulldog_,detnATest_Brownsheep_,detnATest_Doe_,detnATest_Pig_,detcUAll,detcUClin,detcUTest,detcU_Bull_,detcU_Dogsheep_,detcU_Swine_,detcU_Bulldog_,detcU_Brownsheep_,detcU_Doe_,detcU_Pig_,detcUClin_Bull_,detcUClin_Dogsheep_,detcUClin_Swine_,detcUClin_Bulldog_,detcUClin_Brownsheep_,detcUClin_Doe_,detcUClin_Pig_,detcUTest_Bull_,detcUTest_Dogsheep_,detcUTest_Swine_,detcUTest_Bulldog_,detcUTest_Brownsheep_,detcUTest_Doe_,detcUTest_Pig_,detcUqAll,detcAAll,detcAClin,detcATest,detcA_Bull_,detcA_Dogsheep_,detcA_Swine_,detcA_Bulldog_,detcA_Brownsheep_,detcA_Doe_,detcA_Pig_,detcAClin_Bull_,detcAClin_Dogsheep_,detcAClin_Swine_,detcAClin_Bulldog_,detcAClin_Brownsheep_,detcAClin_Doe_,detcAClin_Pig_,detcATest_Bull_,detcATest_Dogsheep_,detcATest_Swine_,detcATest_Bulldog_,detcATest_Brownsheep_,detcATest_Doe_,detcATest_Pig_,tsdUSusc,tsdULat,tsdUSubc,tsdUClin,tsdUNImm,tsdUVImm,tsdUDest,tsdU_Bull_Susc,tsdU_Bull_Lat,tsdU_Bull_Subc,tsdU_Bull_Clin,tsdU_Bull_NImm,tsdU_Bull_VImm,tsdU_Bull_Dest,tsdU_Dogsheep_Susc,tsdU_Dogsheep_Lat,tsdU_Dogsheep_Subc,tsdU_Dogsheep_Clin,tsdU_Dogsheep_NImm,tsdU_Dogsheep_VImm,tsdU_Dogsheep_Dest,tsdU_Swine_Susc,tsdU_Swine_Lat,tsdU_Swine_Subc,tsdU_Swine_Clin,tsdU_Swine_NImm,tsdU_Swine_VImm,tsdU_Swine_Dest,tsdU_Bulldog_Susc,tsdU_Bulldog_Lat,tsdU_Bulldog_Subc,tsdU_Bulldog_Clin,tsdU_Bulldog_NImm,tsdU_Bulldog_VImm,tsdU_Bulldog_Dest,tsdU_Brownsheep_Susc,tsdU_Brownsheep_Lat,tsdU_Brownsheep_Subc,tsdU_Brownsheep_Clin,tsdU_Brownsheep_NImm,tsdU_Brownsheep_VImm,tsdU_Brownsheep_Dest,tsdU_Doe_Susc,tsdU_Doe_Lat,tsdU_Doe_Subc,tsdU_Doe_Clin,tsdU_Doe_NImm,tsdU_Doe_VImm,tsdU_Doe_Dest,tsdU_Pig_Susc,tsdU_Pig_Lat,tsdU_Pig_Subc,tsdU_Pig_Clin,tsdU_Pig_NImm,tsdU_Pig_VImm,tsdU_Pig_Dest,tsdASusc,tsdALat,tsdASubc,tsdAClin,tsdANImm,tsdAVImm,tsdADest,tsdA_Bull_Susc,tsdA_Bull_Lat,tsdA_Bull_Subc,tsdA_Bull_Clin,tsdA_Bull_NImm,tsdA_Bull_VImm,tsdA_Bull_Dest,tsdA_Dogsheep_Susc,tsdA_Dogsheep_Lat,tsdA_Dogsheep_Subc,tsdA_Dogsheep_Clin,tsdA_Dogsheep_NImm,tsdA_Dogsheep_VImm,tsdA_Dogsheep_Dest,tsdA_Swine_Susc,tsdA_Swine_Lat,tsdA_Swine_Subc,tsdA_Swine_Clin,tsdA_Swine_NImm,tsdA_Swine_VImm,tsdA_Swine_Dest,tsdA_Bulldog_Susc,tsdA_Bulldog_Lat,tsdA_Bulldog_Subc,tsdA_Bulldog_Clin,tsdA_Bulldog_NImm,tsdA_Bulldog_VImm,tsdA_Bulldog_Dest,tsdA_Brownsheep_Susc,tsdA_Brownsheep_Lat,tsdA_Brownsheep_Subc,tsdA_Brownsheep_Clin,tsdA_Brownsheep_NImm,tsdA_Brownsheep_VImm,tsdA_Brownsheep_Dest,tsdA_Doe_Susc,tsdA_Doe_Lat,tsdA_Doe_Subc,tsdA_Doe_Clin,tsdA_Doe_NImm,tsdA_Doe_VImm,tsdA_Doe_Dest,tsdA_Pig_Susc,tsdA_Pig_Lat,tsdA_Pig_Subc,tsdA_Pig_Clin,tsdA_Pig_NImm,tsdA_Pig_VImm,tsdA_Pig_Dest,average-prevalence,diseaseDuration,tstnUTruePos,tstnUTruePos_Bull_,tstnUTruePos_Dogsheep_,tstnUTruePos_Swine_,tstnUTruePos_Bulldog_,tstnUTruePos_Brownsheep_,tstnUTruePos_Doe_,tstnUTruePos_Pig_,tstnUTrueNeg,tstnUTrueNeg_Bull_,tstnUTrueNeg_Dogsheep_,tstnUTrueNeg_Swine_,tstnUTrueNeg_Bulldog_,tstnUTrueNeg_Brownsheep_,tstnUTrueNeg_Doe_,tstnUTrueNeg_Pig_,tstnUFalsePos,tstnUFalsePos_Bull_,tstnUFalsePos_Dogsheep_,tstnUFalsePos_Swine_,tstnUFalsePos_Bulldog_,tstnUFalsePos_Brownsheep_,tstnUFalsePos_Doe_,tstnUFalsePos_Pig_,tstnUFalseNeg,tstnUFalseNeg_Bull_,tstnUFalseNeg_Dogsheep_,tstnUFalseNeg_Swine_,tstnUFalseNeg_Bulldog_,tstnUFalseNeg_Brownsheep_,tstnUFalseNeg_Doe_,tstnUFalseNeg_Pig_,tstcUAll,tstcUDirFwd,tstcUIndFwd,tstcUDirBack,tstcUIndBack,tstcU_Bull_,tstcU_Dogsheep_,tstcU_Swine_,tstcU_Bulldog_,tstcU_Brownsheep_,tstcU_Doe_,tstcU_Pig_,tstcUDirFwd_Bull_,tstcUDirFwd_Dogsheep_,tstcUDirFwd_Swine_,tstcUDirFwd_Bulldog_,tstcUDirFwd_Brownsheep_,tstcUDirFwd_Doe_,tstcUDirFwd_Pig_,tstcUIndFwd_Bull_,tstcUIndFwd_Dogsheep_,tstcUIndFwd_Swine_,tstcUIndFwd_Bulldog_,tstcUIndFwd_Brownsheep_,tstcUIndFwd_Doe_,tstcUIndFwd_Pig_,tstcUDirBack_Bull_,tstcUDirBack_Dogsheep_,tstcUDirBack_Swine_,tstcUDirBack_Bulldog_,tstcUDirBack_Brownsheep_,tstcUDirBack_Doe_,tstcUDirBack_Pig_,tstcUIndBack_Bull_,tstcUIndBack_Dogsheep_,tstcUIndBack_Swine_,tstcUIndBack_Bulldog_,tstcUIndBack_Brownsheep_,tstcUIndBack_Doe_,tstcUIndBack_Pig_,tstcUTruePos,tstcUTruePos_Bull_,tstcUTruePos_Dogsheep_,tstcUTruePos_Swine_,tstcUTruePos_Bulldog_,tstcUTruePos_Brownsheep_,tstcUTruePos_Doe_,tstcUTruePos_Pig_,tstcUTrueNeg,tstcUTrueNeg_Bull_,tstcUTrueNeg_Dogsheep_,tstcUTrueNeg_Swine_,tstcUTrueNeg_Bulldog_,tstcUTrueNeg_Brownsheep_,tstcUTrueNeg_Doe_,tstcUTrueNeg_Pig_,tstcUFalsePos,tstcUFalsePos_Bull_,tstcUFalsePos_Dogsheep_,tstcUFalsePos_Swine_,tstcUFalsePos_Bulldog_,tstcUFalsePos_Brownsheep_,tstcUFalsePos_Doe_,tstcUFalsePos_Pig_,tstcUFalseNeg,tstcUFalseNeg_Bull_,tstcUFalseNeg_Dogsheep_,tstcUFalseNeg_Swine_,tstcUFalseNeg_Bulldog_,tstcUFalseNeg_Brownsheep_,tstcUFalseNeg_Doe_,tstcUFalseNeg_Pig_,tstcAAll,tstcADirFwd,tstcAIndFwd,tstcADirBack,tstcAIndBack,tstcA_Bull_,tstcA_Dogsheep_,tstcA_Swine_,tstcA_Bulldog_,tstcA_Brownsheep_,tstcA_Doe_,tstcA_Pig_,tstcADirFwd_Bull_,tstcADirFwd_Dogsheep_,tstcADirFwd_Swine_,tstcADirFwd_Bulldog_,tstcADirFwd_Brownsheep_,tstcADirFwd_Doe_,tstcADirFwd_Pig_,tstcAIndFwd_Bull_,tstcAIndFwd_Dogsheep_,tstcAIndFwd_Swine_,tstcAIndFwd_Bulldog_,tstcAIndFwd_Brownsheep_,tstcAIndFwd_Doe_,tstcAIndFwd_Pig_,tstcADirBack_Bull_,tstcADirBack_Dogsheep_,tstcADirBack_Swine_,tstcADirBack_Bulldog_,tstcADirBack_Brownsheep_,tstcADirBack_Doe_,tstcADirBack_Pig_,tstcAIndBack_Bull_,tstcAIndBack_Dogsheep_,tstcAIndBack_Swine_,tstcAIndBack_Bulldog_,tstcAIndBack_Brownsheep_,tstcAIndBack_Doe_,tstcAIndBack_Pig_,vaccOccurred,firstVaccination,firstVaccinationRing,firstVaccination_Bull_,firstVaccination_Dogsheep_,firstVaccination_Swine_,firstVaccination_Bulldog_,firstVaccination_Brownsheep_,firstVaccination_Doe_,firstVaccination_Pig_,firstVaccinationRing_Bull_,firstVaccinationRing_Dogsheep_,firstVaccinationRing_Swine_,firstVaccinationRing_Bulldog_,firstVaccinationRing_Brownsheep_,firstVaccinationRing_Doe_,firstVaccinationRing_Pig_,vacnUAll,vacnUIni,vacnURing,vacnU_Bull_,vacnU_Dogsheep_,vacnU_Swine_,vacnU_Bulldog_,vacnU_Brownsheep_,vacnU_Doe_,vacnU_Pig_,vacnUIni_Bull_,vacnUIni_Dogsheep_,vacnUIni_Swine_,vacnUIni_Bulldog_,vacnUIni_Brownsheep_,vacnUIni_Doe_,vacnUIni_Pig_,vacnURing_Bull_,vacnURing_Dogsheep_,vacnURing_Swine_,vacnURing_Bulldog_,vacnURing_Brownsheep_,vacnURing_Doe_,vacnURing_Pig_,vaccUAll,vaccUIni,vaccURing,vaccU_Bull_,vaccU_Dogsheep_,vaccU_Swine_,vaccU_Bulldog_,vaccU_Brownsheep_,vaccU_Doe_,vaccU_Pig_,vaccUIni_Bull_,vaccUIni_Dogsheep_,vaccUIni_Swine_,vaccUIni_Bulldog_,vaccUIni_Brownsheep_,vaccUIni_Doe_,vaccUIni_Pig_,vaccURing_Bull_,vaccURing_Dogsheep_,vaccURing_Swine_,vaccURing_Bulldog_,vaccURing_Brownsheep_,vaccURing_Doe_,vaccURing_Pig_,vacnAAll,vacnAIni,vacnARing,vacnA_Bull_,vacnA_Dogsheep_,vacnA_Swine_,vacnA_Bulldog_,vacnA_Brownsheep_,vacnA_Doe_,vacnA_Pig_,vacnAIni_Bull_,vacnAIni_Dogsheep_,vacnAIni_Swine_,vacnAIni_Bulldog_,vacnAIni_Brownsheep_,vacnAIni_Doe_,vacnAIni_Pig_,vacnARing_Bull_,vacnARing_Dogsheep_,vacnARing_Swine_,vacnARing_Bulldog_,vacnARing_Brownsheep_,vacnARing_Doe_,vacnARing_Pig_,vaccAAll,vaccAIni,vaccARing,vaccA_Bull_,vaccA_Dogsheep_,vaccA_Swine_,vaccA_Bulldog_,vaccA_Brownsheep_,vaccA_Doe_,vaccA_Pig_,vaccAIni_Bull_,vaccAIni_Dogsheep_,vaccAIni_Swine_,vaccAIni_Bulldog_,vaccAIni_Brownsheep_,vaccAIni_Doe_,vaccAIni_Pig_,vaccARing_Bull_,vaccARing_Dogsheep_,vaccARing_Swine_,vaccARing_Bulldog_,vaccARing_Brownsheep_,vaccARing_Doe_,vaccARing_Pig_,exmnUAll,exmnURing,exmnUDirFwd,exmnUIndFwd,exmnUDirBack,exmnUIndBack,exmnUDet,exmnU_Bull_,exmnU_Dogsheep_,exmnU_Swine_,exmnU_Bulldog_,exmnU_Brownsheep_,exmnU_Doe_,exmnU_Pig_,exmnURing_Bull_,exmnURing_Dogsheep_,exmnURing_Swine_,exmnURing_Bulldog_,exmnURing_Brownsheep_,exmnURing_Doe_,exmnURing_Pig_,exmnUDirFwd_Bull_,exmnUDirFwd_Dogsheep_,exmnUDirFwd_Swine_,exmnUDirFwd_Bulldog_,exmnUDirFwd_Brownsheep_,exmnUDirFwd_Doe_,exmnUDirFwd_Pig_,exmnUIndFwd_Bull_,exmnUIndFwd_Dogsheep_,exmnUIndFwd_Swine_,exmnUIndFwd_Bulldog_,exmnUIndFwd_Brownsheep_,exmnUIndFwd_Doe_,exmnUIndFwd_Pig_,exmnUDirBack_Bull_,exmnUDirBack_Dogsheep_,exmnUDirBack_Swine_,exmnUDirBack_Bulldog_,exmnUDirBack_Brownsheep_,exmnUDirBack_Doe_,exmnUDirBack_Pig_,exmnUIndBack_Bull_,exmnUIndBack_Dogsheep_,exmnUIndBack_Swine_,exmnUIndBack_Bulldog_,exmnUIndBack_Brownsheep_,exmnUIndBack_Doe_,exmnUIndBack_Pig_,exmnUDet_Bull_,exmnUDet_Dogsheep_,exmnUDet_Swine_,exmnUDet_Bulldog_,exmnUDet_Brownsheep_,exmnUDet_Doe_,exmnUDet_Pig_,exmnAAll,exmnARing,exmnADirFwd,exmnAIndFwd,exmnADirBack,exmnAIndBack,exmnADet,exmnA_Bull_,exmnA_Dogsheep_,exmnA_Swine_,exmnA_Bulldog_,exmnA_Brownsheep_,exmnA_Doe_,exmnA_Pig_,exmnARing_Bull_,exmnARing_Dogsheep_,exmnARing_Swine_,exmnARing_Bulldog_,exmnARing_Brownsheep_,exmnARing_Doe_,exmnARing_Pig_,exmnADirFwd_Bull_,exmnADirFwd_Dogsheep_,exmnADirFwd_Swine_,exmnADirFwd_Bulldog_,exmnADirFwd_Brownsheep_,exmnADirFwd_Doe_,exmnADirFwd_Pig_,exmnAIndFwd_Bull_,exmnAIndFwd_Dogsheep_,exmnAIndFwd_Swine_,exmnAIndFwd_Bulldog_,exmnAIndFwd_Brownsheep_,exmnAIndFwd_Doe_,exmnAIndFwd_Pig_,exmnADirBack_Bull_,exmnADirBack_Dogsheep_,exmnADirBack_Swine_,exmnADirBack_Bulldog_,exmnADirBack_Brownsheep_,exmnADirBack_Doe_,exmnADirBack_Pig_,exmnAIndBack_Bull_,exmnAIndBack_Dogsheep_,exmnAIndBack_Swine_,exmnAIndBack_Bulldog_,exmnAIndBack_Brownsheep_,exmnAIndBack_Doe_,exmnAIndBack_Pig_,exmnADet_Bull_,exmnADet_Dogsheep_,exmnADet_Swine_,exmnADet_Bulldog_,exmnADet_Brownsheep_,exmnADet_Doe_,exmnADet_Pig_,exmcUAll,exmcURing,exmcUDirFwd,exmcUIndFwd,exmcUDirBack,exmcUIndBack,exmcUDet,exmcU_Bull_,exmcU_Dogsheep_,exmcU_Swine_,exmcU_Bulldog_,exmcU_Brownsheep_,exmcU_Doe_,exmcU_Pig_,exmcURing_Bull_,exmcURing_Dogsheep_,exmcURing_Swine_,exmcURing_Bulldog_,exmcURing_Brownsheep_,exmcURing_Doe_,exmcURing_Pig_,exmcUDirFwd_Bull_,exmcUDirFwd_Dogsheep_,exmcUDirFwd_Swine_,exmcUDirFwd_Bulldog_,exmcUDirFwd_Brownsheep_,exmcUDirFwd_Doe_,exmcUDirFwd_Pig_,exmcUIndFwd_Bull_,exmcUIndFwd_Dogsheep_,exmcUIndFwd_Swine_,exmcUIndFwd_Bulldog_,exmcUIndFwd_Brownsheep_,exmcUIndFwd_Doe_,exmcUIndFwd_Pig_,exmcUDirBack_Bull_,exmcUDirBack_Dogsheep_,exmcUDirBack_Swine_,exmcUDirBack_Bulldog_,exmcUDirBack_Brownsheep_,exmcUDirBack_Doe_,exmcUDirBack_Pig_,exmcUIndBack_Bull_,exmcUIndBack_Dogsheep_,exmcUIndBack_Swine_,exmcUIndBack_Bulldog_,exmcUIndBack_Brownsheep_,exmcUIndBack_Doe_,exmcUIndBack_Pig_,exmcUDet_Bull_,exmcUDet_Dogsheep_,exmcUDet_Swine_,exmcUDet_Bulldog_,exmcUDet_Brownsheep_,exmcUDet_Doe_,exmcUDet_Pig_,exmcAAll,exmcARing,exmcADirFwd,exmcAIndFwd,exmcADirBack,exmcAIndBack,exmcADet,exmcA_Bull_,exmcA_Dogsheep_,exmcA_Swine_,exmcA_Bulldog_,exmcA_Brownsheep_,exmcA_Doe_,exmcA_Pig_,exmcARing_Bull_,exmcARing_Dogsheep_,exmcARing_Swine_,exmcARing_Bulldog_,exmcARing_Brownsheep_,exmcARing_Doe_,exmcARing_Pig_,exmcADirFwd_Bull_,exmcADirFwd_Dogsheep_,exmcADirFwd_Swine_,exmcADirFwd_Bulldog_,exmcADirFwd_Brownsheep_,exmcADirFwd_Doe_,exmcADirFwd_Pig_,exmcAIndFwd_Bull_,exmcAIndFwd_Dogsheep_,exmcAIndFwd_Swine_,exmcAIndFwd_Bulldog_,exmcAIndFwd_Brownsheep_,exmcAIndFwd_Doe_,exmcAIndFwd_Pig_,exmcADirBack_Bull_,exmcADirBack_Dogsheep_,exmcADirBack_Swine_,exmcADirBack_Bulldog_,exmcADirBack_Brownsheep_,exmcADirBack_Doe_,exmcADirBack_Pig_,exmcAIndBack_Bull_,exmcAIndBack_Dogsheep_,exmcAIndBack_Swine_,exmcAIndBack_Bulldog_,exmcAIndBack_Brownsheep_,exmcAIndBack_Doe_,exmcAIndBack_Pig_,exmcADet_Bull_,exmcADet_Dogsheep_,exmcADet_Swine_,exmcADet_Bulldog_,exmcADet_Brownsheep_,exmcADet_Doe_,exmcADet_Pig_"
actual_headers = re.sub('_\w+_|All', '', raw_headers) #removes production types
actual_headers = re.sub('HighRisk|MediumRisk', '', actual_headers) #removes zone names
headers = re.sub('-', '_', actual_headers) #there are 2 hyphenated fields:  average-prevalence num-separate-areasMediumRisk 
actual_headers = actual_headers.split(',')

# <codecell>


# <codecell>

field_matches = match_model_to_c_headers(new_spec, spec_headers)
count_empty_matches(field_matches)

# <codecell>

field_matches = match_c_headers_to_model(new_spec, spec_headers)
count_empty_matches(field_matches)

# <codecell>

field_matches = match_model_to_c_headers(new_spec, actual_headers)
count_empty_matches(field_matches)

# <codecell>

field_matches = match_c_headers_to_model(new_spec, actual_headers)
count_empty_matches(field_matches)

# <headingcell level=2>

# Header Grammars

# <codecell>

cause_sweep = raw_headers.split(',')
removed_pts = '_Bulldog_ _Brownsheep_ _Doe_ _Pig_ _Dogsheep_'.split()
cause_sweep = [h for h in cause_sweep if not any([pt in h for pt in removed_pts])]
print(len(cause_sweep))

# <codecell>

def matching_headers(prefix, exclude=None):
    matches = [h for h in cause_sweep if h.startswith(prefix)]
    if exclude is not None:
        matches = [m for m in matches if exclude not in m]
    print('\n'.join(matches))
    print('Total:', len(matches))

# <codecell>

matching_headers('exp')

# <codecell>

grammars = {'exp': [('c', 'n'), ('U', 'A'), ('', 'Dir', 'Ind', 'Air'), ('All', '_Bull_', '_Swine_')]}

# <codecell>

matching_headers('etection')

# <codecell>

grammars['firstDetection'] = [('', 'Clin', 'Test'), ('', '_Bull_', '_Swine_')]# 18 = 2*3*3

# <codecell>

matching_headers('det')

# <codecell>

print(2*2*3*3)  # There are two unnaccounted for in this set

# <codecell>

grammars['det'] = [('c', 'n'), ('U', 'A'), ('All', 'Clin', 'Test'), ('', '_Bull_', '_Swine_')]

# <codecell>

from collections import defaultdict
a = {'All':'from Either method', 'Clin':'from Clinical signs', 'Test': 'from Lab Tests', 'U':'Units', 'A':'Animals', 'p':'Possible',
     'Dir': 'Direct Spread', 'Ind':'Indirect Spread', 'Air':'Airborne Spread'}
explain = defaultdict(lambda: '', a)

# <codecell>

for a in ('U', 'A'):
    for b in ('All', 'Clin', 'Test'):
        print('    '+a+b+ ' = models.IntegerField(blank=True, null=True, verbose_name="'+explain[b]+'")')

# <codecell>

for a in ('U', 'A'):
    for b, verbose in (('All','from Either method'), ('Clin','from Clinical signs'), ('Test', 'from Lab Tests')):
        print('    '+a+b+ ' = models.IntegerField(blank=True, null=True, verbose_name="'+verbose+'")')

# <codecell>

matching_headers('tr')

# <codecell>

grammars['tr'] = [('n','c'), ('U', 'A'), ('All', 'Dir', 'Ind'), ('', '_Bull_', '_Swine_'), ('', 'p')]  # 2*3*3*2
print(2*2*3*3*2)

# <codecell>

grammar =  [('U', 'A'), ('All', 'Dir', 'Ind'), ('', 'p')]
def not_as_cool_as_product(grammar):
    result = []
    for possibilities in grammar:
        if len(result) == 0:
            result = list(possibilities)
        else:
            temp = list(result)
            result = []
            for suffix in possibilities:
                result += [a+suffix for a in temp]
    return result
not_as_cool_as_product(grammar)

# <codecell>

from itertools import product, combinations, permutations
list(product(('U', 'A'), ('All', 'Dir', 'Ind'), ('', '_Bull_', '_Swine_')))

# <codecell>

def stat_group_code(grammar):
    combos = product(*grammar)
    for line in combos:
        explanation = ' '.join([explain[part] for part in line])
        print('    '+''.join(line)+ ' = models.IntegerField(blank=True, null=True, verbose_name="'+explanation+'")')

# <codecell>

stat_group_code( [('U', 'A'), ('All', 'Dir', 'Ind'), ('', 'p')] )

# <codecell>

matching_headers('exm')

# <codecell>

grammars['exm'] = [('n','c'), ('U','A'), ('All','Ring','DirFwd','IndFwd','DirBack','IndBack','Det'), ('','_Bull_','_Swine_')]
print(2*2*7*3)

# <codecell>

combos = product(('n','c'), ('U','A'), ('All','Ring','DirFwd','IndFwd','DirBack','IndBack','Det'), ('','_Bull_','_Swine_'))
close = '\nexm'.join([''.join(line) for line in combos])
print(re.sub(r'All_', '_', close))  # special rule implemented

# <markdowncell>

# <u>exm Grammar exception</u>
# =====================
# When 'All' is followed by a Production Type, remove the word 'All'.
# `re.sub(r'All_', '_', close)`  The database will follow the expected format that includes "All" in these cases, but the exception will need to be added to the switcher that take CEngine output and finds the DB match.
# * Same rule applies to `tstcA`

# <codecell>

grammar = [('U','A'), ('All','Ring','DirFwd','IndFwd','DirBack','IndBack','Det')]
explain.update({'DirFwd':'because of Direct Forward trace', 
                'IndFwd':'because of Indirect Forward trace', 
                'DirBack':'because of Direct Back trace', 
                'IndBack':'because of Indirect Back trace', 
                'Ring':'because of Ring'})
stat_group_code(grammar)

# <headingcell level=3>

# tst Header

# <codecell>

matching_headers('tst')

# <codecell>

grammars['tst'] = ['tstnU', 'tstcU', 'tstcA']  # references the three exclusive branches
grammars['tstnU'] = [('TruePos', 'FalsePos', 'TrueNeg','FalseNeg'), ('','_Bull_','_Swine_')]  # first part only
grammars['tstcU'] = [('All', 'DirFwd','IndFwd','DirBack','IndBack', 'TruePos','FalsePos','TrueNeg','FalseNeg'), ('','_Bull_','_Swine_')]  # direction and pos/neg are exclusive
grammars['tstcA'] = [('All','DirFwd','IndFwd','DirBack','IndBack'), ('','_Bull_','_Swine_')]  # direction and pos/neg are exclusive

4*3 + 8*3 + 5*3

# <codecell>

def combo_set(*prefixes):
    combos = set()
    for prefix in prefixes:
        tree = grammars[prefix]
        parts = product(*tree)
        combos = combos.union({prefix + ''.join(line) for line in parts})
    return combos

# <codecell>

the54 = combo_set(*grammars['tst'])
len(combo_set(*grammars['tst']))

# <codecell>

def subset_check(full_list, sub_list):
    print("Subset Check:", set(sub_list).issubset(set(full_list)))
    stragglers = set(sub_list) - set(full_list).intersection(set(sub_list))
    return stragglers

# <codecell>

x = [h for h in cause_sweep if 'tst' in h]
subset_check(x, the54)
# x

# <markdowncell>

# The four that don't match here are from the exm grammar exception about 'All' already noted above.  
# So what are we still missing?

# <codecell>

subset_check(x, the54)

# <markdowncell>

# That's the same exception as before.  We're done.

# <codecell>

explain.update({'TruePos':'True Positives', 'FalsePos':'False Positives', 'TrueNeg':'True Negatives','FalseNeg':'False Negatives'})

# <codecell>

stat_group_code([('U',), ('TruePos', 'FalsePos', 'TrueNeg','FalseNeg')])

# <markdowncell>

#    
# ##firstVaccination

# <codecell>

matching_headers('firstVaccination')

# <codecell>

grammars['firstVaccination'] = [('','Ring'), ('','_Bull_','_Swine_')]

# <headingcell level=2>

# vac Headers

# <codecell>

matching_headers('vacw')

# <markdowncell>

# This one defies grammar.  I'm just going to stick it in the model WaitGroup as is.

# <codecell>

grammars['vac'] = ['vacw', 'vacn', 'vacc']
grammars['vacw'] = [('U','A'), ('All','Max','MaxDay','TimeMax','TimeAvg','DaysInQueue'), ('','_Bull_','_Swine_')]
grammars['vacn'] = [('U','A'), ('All','Ini','Ring'), ('','_Bull_','_Swine_')]
grammars['vacc'] = [('U','A'), ('All','Ini','Ring'), ('','_Bull_','_Swine_')]

# <codecell>

from io import StringIO
import sys

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout

# <codecell>

with Capturing() as print_out:
    matching_headers('vac')
x = [x for x in print_out[:-1] if 'vacw' not in x]
print(len(x))
x

# <codecell>

explain['Ini'] = 'Initially'

# <codecell>

stat_group_code([('U','A'), ('All','Ini','Ring')])

# <codecell>


# <headingcell level=2>

# firstDestruction

# <codecell>

matching_headers('firstDestruction')

# <codecell>

grammars['firstDestruction'] = [('','Unsp','Ring','Det','Ini','DirFwd','IndFwd','DirBack','IndBack'), ('','_Bull_','_Swine_')]
9*3

# <codecell>

x = [h for h in cause_sweep if 'firstDestruction' in h]
subset_check(x, combo_set('firstDestruction'))
subset_check(combo_set('firstDestruction'), x)

# <markdowncell>

# **Perfect Match**

# <codecell>

explain.update({'Unsp':'Unspecified', 'Det':'because of Detection'})

# <codecell>

stat_group_code([('','Unsp','Ring','Det','Ini','DirFwd','IndFwd','DirBack','IndBack')])

# <markdowncell>

#   
# ##des Headers

# <codecell>

matching_headers('des', 'desw')

# <codecell>

grammars['des'] = [('n','c'), ('U','A'), ('All','Unsp','Ring','Det','Ini','DirFwd','IndFwd','DirBack','IndBack'), ('','_Bull_','_Swine_')]
len(combo_set('des'))

# <codecell>

x = [h for h in cause_sweep if 'des' in h and 'desw' not in h]
subset_check(x, combo_set('des'))

# <codecell>

subset_check(combo_set('des'), x)

# <markdowncell>

# This is a correct match.  Same exception as before, plus the `destrOccurred` which has been added to the unaccounted list

# <headingcell level=3>

# desw Headers

# <codecell>

matching_headers('desw')

# <codecell>

grammars['desw'] = grammars['vacw']  #same structure, same python Group model used

# <headingcell level=1>

# ByProductionType Header Grammars

# <headingcell level=2>

# tsd Headers

# <codecell>

matching_headers('tsd')

# <codecell>

grammars['tsd'] = [('U','A'), ('','_Bull_','_Swine_'), ('Susc','Lat','Subc','Clin','NImm','VImm','Dest')]

# <codecell>

def set_equality_check(prefix):
    x = [h for h in cause_sweep if prefix in h ]
    a = subset_check(x, combo_set(prefix))
    b = subset_check(combo_set(prefix), x)
    return (a, b)

set_equality_check('tsd')

# <codecell>

explain.update({'Susc':'Susceptible', 'Lat':'Latent', 'Subc':'Subclinical', 'Clin':'Clinical', 'NImm':'Natural Immune', 'VImm':'Vaccine Immune', 'Dest':'Destroyed'})

# <codecell>

stat_group_code([('U','A'), ('Susc','Lat','Subc','Clin','NImm','VImm','Dest')])

# <markdowncell>

#   

# <markdowncell>

# Just making sure I got everything

# <codecell>

matching_headers('vacw')

# <codecell>

grammars['desw']

# <headingcell level=1>

# DailyByZoneAndProductionType

# <codecell>

matching_headers('unitsInZone')

# <codecell>

ZONES = ('Background', 'HighRisk', 'MediumRisk')
PT = ('', '_Bull_', '_Swine_')
grammars['unitsInZone'] = [ZONES, PT]
combo_set('unitsInZone')

# <codecell>

set_equality_check('unitsInZone')

# <headingcell level=3>

# unitDaysInZone Headers

# <codecell>

matching_headers('unitDaysInZone')

# <markdowncell>

# Same as before.

# <codecell>

grammars['unitDaysInZone'] = grammars['unitsInZone']

# <codecell>

re.sub(r'([a-z])([A-Z])', r'\1_\2', 'unitDaysInZone').lower()

# <codecell>

matching_headers('animalDaysInZone')

# <codecell>

grammars['animalDaysInZone'] = grammars['unitsInZone']

# <markdowncell>

# Same as before

# <headingcell level=1>

# DailyByZone Headers

# <codecell>

for field in ['zoneArea','maxZoneArea','maxZoneAreaDay','zonePerimeter','maxZonePerimeter','maxZonePerimeterDay']:
    matching_headers(field)

# <markdowncell>

# Nothing intersting going on here.

# <headingcell level=2>

# DailyControls Headers

# <codecell>

matching_headers('adq')

# <codecell>

for field in ['diseaseDuration','adqnU','adqcU','detOccurred','costSurveillance','vaccOccurred','vacwUMax','vacwUMaxDay','vacwUDaysInQueue']:
    matching_headers(field)

# <codecell>

matching_headers('costSurveillance')

# <markdowncell>

# Probably missing because I didn't specify costs

# <codecell>

fields = '''vacwUTimeAvg
vacwUTimeMax
vacwAMax
vacwAMaxDay
vacwADaysInQueue
vaccSetup
vaccVaccination
vaccSubtotal
destrOccurred
deswUMax
deswUMaxDay
deswUDaysInQueue
deswUTimeAvg
deswUTimeMax
deswAMax
deswAMaxDay
deswADaysInQueue
destrAppraisal
destrEuthanasia
destrIndemnification'''.split()

# <codecell>

for field in fields:
    matching_headers(field)

# <markdowncell>

# A couple missing fields.  I'll stick to Neil's notes and assume that they are missing because of settings.

# <codecell>

fields = '''destrDisposal
destrCleaning
destrSubtotal
outbreakDuration
costsTotal'''.split()
for field in fields:
    matching_headers(field)

# <codecell>


# <headingcell level=2>

# Fields I couln't grammarify

# <markdowncell>

# detcUqAll

# <codecell>


# <headingcell level=1>

# Outputs that don't match any prefix so far

# <codecell>

prefixes = '''expnU
expcU
expnA
expcA
infnU
infcU
infnA
infcA
firstDetection
lastDetection
detnU
detcU
detnA
detcA
trnUp
trnU
trcUp
trcU
trnAp
trnA
trcAp
trcA
exmnU
exmcU
exmnA
exmcA
tstcU
tstcA
firstVaccination
vacnU
vaccU
vacnA
vaccA
firstDestruction
desnU
descU
desnA
descA
tsdUSusc
tsdULat
tsdUSubc
tsdUClin
tsdUNImm
tsdUVImm
tsdUDest
tsdASusc
tsdALat
tsdASubc
tsdAClin
tsdANImm
tsdAVImm
tsdADest
tstcUTruePos
tstcUTrueNeg
tstcUFalsePos
tstcUFalseNeg
vacwU
vacwA
deswU
deswA
unitsInZone
unitDaysInZone
animalDaysInZone
zoneArea
maxZoneArea
maxZoneAreaDay
zonePerimeter
maxZonePerimeter
maxZonePerimeterDay
diseaseDuration
adqnU
adqcU
detOccurred
costSurveillance
vaccOccurred
vacwUMax
vacwUMaxDay
vacwUDaysInQueue
vacwUTimeAvg
vacwUTimeMax
vacwAMax
vacwAMaxDay
vacwADaysInQueue
vaccSetup
vaccVaccination
vaccSubtotal
destrOccurred
deswUMax
deswUMaxDay
deswUDaysInQueue
deswUTimeAvg
deswUTimeMax
deswAMax
deswAMaxDay
deswADaysInQueue
destrAppraisal
destrEuthanasia
destrIndemnification
destrDisposal
destrCleaning
destrSubtotal
outbreakDuration
costsTotal
tsd
tst'''.split()

# <codecell>

print('\n'.join([h for h in cause_sweep if not any([covered in h for covered in prefixes])]))

# <codecell>

grammars['tsd']

# <codecell>

grammars['tst']

# <codecell>

[x for x in cause_sweep if 'trnUDir' in x]

# <codecell>

grammars['firstVaccination']

# <codecell>


# <headingcell level=2>

# Column stability between Scenarios

# <codecell>

recent_headers = "Run,Day,outbreakDuration,zoneAreaHighRisk,zoneAreaMediumRisk,maxZoneAreaHighRisk,maxZoneAreaMediumRisk,maxZoneAreaDayHighRisk,maxZoneAreaDayMediumRisk,finalZoneAreaHighRisk,finalZoneAreaMediumRisk,zonePerimeterHighRisk,zonePerimeterMediumRisk,maxZonePerimeterHighRisk,maxZonePerimeterMediumRisk,maxZonePerimeterDayHighRisk,maxZonePerimeterDayMediumRisk,finalZonePerimeterHighRisk,finalZonePerimeterMediumRisk,num-separate-areasHighRisk,num-separate-areasMediumRisk,unitsInZoneHighRisk,unitsInZoneMediumRisk,unitsInZoneBackground,unitsInZoneHighRisk_Bull_,unitsInZoneHighRisk_Swine_,unitsInZoneMediumRisk_Bull_,unitsInZoneMediumRisk_Swine_,unitsInZoneBackground_Bull_,unitsInZoneBackground_Swine_,unitDaysInZoneHighRisk,unitDaysInZoneMediumRisk,unitDaysInZoneBackground,unitDaysInZoneHighRisk_Bull_,unitDaysInZoneHighRisk_Swine_,unitDaysInZoneMediumRisk_Bull_,unitDaysInZoneMediumRisk_Swine_,unitDaysInZoneBackground_Bull_,unitDaysInZoneBackground_Swine_,animalDaysInZoneHighRisk,animalDaysInZoneMediumRisk,animalDaysInZoneBackground,animalDaysInZoneHighRisk_Bull_,animalDaysInZoneHighRisk_Swine_,animalDaysInZoneMediumRisk_Bull_,animalDaysInZoneMediumRisk_Swine_,animalDaysInZoneBackground_Bull_,animalDaysInZoneBackground_Swine_,destrOccurred,firstDestruction,firstDestructionUnsp,firstDestructionRing,firstDestructionDirFwd,firstDestructionIndFwd,firstDestructionDirBack,firstDestructionIndBack,firstDestructionDet,firstDestructionIni,firstDestruction_Bull_,firstDestruction_Swine_,firstDestructionUnsp_Bull_,firstDestructionUnsp_Swine_,firstDestructionRing_Bull_,firstDestructionRing_Swine_,firstDestructionDirFwd_Bull_,firstDestructionDirFwd_Swine_,firstDestructionIndFwd_Bull_,firstDestructionIndFwd_Swine_,firstDestructionDirBack_Bull_,firstDestructionDirBack_Swine_,firstDestructionIndBack_Bull_,firstDestructionIndBack_Swine_,firstDestructionDet_Bull_,firstDestructionDet_Swine_,firstDestructionIni_Bull_,firstDestructionIni_Swine_,desnUAll,desnUIni,desnUUnsp,desnURing,desnUDirFwd,desnUIndFwd,desnUDirBack,desnUIndBack,desnUDet,desnU_Bull_,desnU_Swine_,desnUIni_Bull_,desnUIni_Swine_,desnUUnsp_Bull_,desnUUnsp_Swine_,desnURing_Bull_,desnURing_Swine_,desnUDirFwd_Bull_,desnUDirFwd_Swine_,desnUIndFwd_Bull_,desnUIndFwd_Swine_,desnUDirBack_Bull_,desnUDirBack_Swine_,desnUIndBack_Bull_,desnUIndBack_Swine_,desnUDet_Bull_,desnUDet_Swine_,descUAll,descUIni,descUUnsp,descURing,descUDirFwd,descUIndFwd,descUDirBack,descUIndBack,descUDet,descU_Bull_,descU_Swine_,descUIni_Bull_,descUIni_Swine_,descUUnsp_Bull_,descUUnsp_Swine_,descURing_Bull_,descURing_Swine_,descUDirFwd_Bull_,descUDirFwd_Swine_,descUIndFwd_Bull_,descUIndFwd_Swine_,descUDirBack_Bull_,descUDirBack_Swine_,descUIndBack_Bull_,descUIndBack_Swine_,descUDet_Bull_,descUDet_Swine_,desnAAll,desnAIni,desnAUnsp,desnARing,desnADirFwd,desnAIndFwd,desnADirBack,desnAIndBack,desnADet,desnA_Bull_,desnA_Swine_,desnAIni_Bull_,desnAIni_Swine_,desnAUnsp_Bull_,desnAUnsp_Swine_,desnARing_Bull_,desnARing_Swine_,desnADirFwd_Bull_,desnADirFwd_Swine_,desnAIndFwd_Bull_,desnAIndFwd_Swine_,desnADirBack_Bull_,desnADirBack_Swine_,desnAIndBack_Bull_,desnAIndBack_Swine_,desnADet_Bull_,desnADet_Swine_,descAAll,descAIni,descAUnsp,descARing,descADirFwd,descAIndFwd,descADirBack,descAIndBack,descADet,descA_Bull_,descA_Swine_,descAIni_Bull_,descAIni_Swine_,descAUnsp_Bull_,descAUnsp_Swine_,descARing_Bull_,descARing_Swine_,descADirFwd_Bull_,descADirFwd_Swine_,descAIndFwd_Bull_,descAIndFwd_Swine_,descADirBack_Bull_,descADirBack_Swine_,descAIndBack_Bull_,descAIndBack_Swine_,descADet_Bull_,descADet_Swine_,expnUAll,expnUDir,expnUInd,expnUAir,expnU_Bull_,expnU_Swine_,expnUDir_Bull_,expnUDir_Swine_,expnUInd_Bull_,expnUInd_Swine_,expnUAir_Bull_,expnUAir_Swine_,expcUAll,expcUDir,expcUInd,expcUAir,expcU_Bull_,expcU_Swine_,expcUDir_Bull_,expcUDir_Swine_,expcUInd_Bull_,expcUInd_Swine_,expcUAir_Bull_,expcUAir_Swine_,expnAAll,expnADir,expnAInd,expnAAir,expnA_Bull_,expnA_Swine_,expnADir_Bull_,expnADir_Swine_,expnAInd_Bull_,expnAInd_Swine_,expnAAir_Bull_,expnAAir_Swine_,expcAAll,expcADir,expcAInd,expcAAir,expcA_Bull_,expcA_Swine_,expcADir_Bull_,expcADir_Swine_,expcAInd_Bull_,expcAInd_Swine_,expcAAir_Bull_,expcAAir_Swine_,adqnUAll,adqcUAll,deswUAll,deswU_Bull_,deswU_Swine_,deswAAll,deswA_Bull_,deswA_Swine_,deswUMax,deswUMaxDay,deswAMax,deswAMaxDay,deswUTimeMax,deswUTimeAvg,deswUDaysInQueue,deswADaysInQueue,detOccurred,firstDetection,firstDetectionClin,firstDetectionTest,firstDetection_Bull_,firstDetection_Swine_,firstDetectionClin_Bull_,firstDetectionClin_Swine_,firstDetectionTest_Bull_,firstDetectionTest_Swine_,lastDetection,lastDetectionClin,lastDetectionTest,lastDetection_Bull_,lastDetection_Swine_,lastDetectionClin_Bull_,lastDetectionClin_Swine_,lastDetectionTest_Bull_,lastDetectionTest_Swine_,detnUAll,detnUClin,detnUTest,detnU_Bull_,detnU_Swine_,detnUClin_Bull_,detnUClin_Swine_,detnUTest_Bull_,detnUTest_Swine_,detnAAll,detnAClin,detnATest,detnA_Bull_,detnA_Swine_,detnAClin_Bull_,detnAClin_Swine_,detnATest_Bull_,detnATest_Swine_,detcUAll,detcUClin,detcUTest,detcU_Bull_,detcU_Swine_,detcUClin_Bull_,detcUClin_Swine_,detcUTest_Bull_,detcUTest_Swine_,detcUqAll,detcAAll,detcAClin,detcATest,detcA_Bull_,detcA_Swine_,detcAClin_Bull_,detcAClin_Swine_,detcATest_Bull_,detcATest_Swine_,trnUAllp,trnUDirp,trnUIndp,trnU_Bull_p,trnU_Swine_p,trnUDir_Bull_p,trnUDir_Swine_p,trnUInd_Bull_p,trnUInd_Swine_p,trcUAllp,trcUDirp,trcUIndp,trcU_Bull_p,trcU_Swine_p,trcUDir_Bull_p,trcUDir_Swine_p,trcUInd_Bull_p,trcUInd_Swine_p,trnUAll,trnUDir,trnUInd,trnU_Bull_,trnU_Swine_,trnUDir_Bull_,trnUDir_Swine_,trnUInd_Bull_,trnUInd_Swine_,trcUAll,trcUDir,trcUInd,trcU_Bull_,trcU_Swine_,trcUDir_Bull_,trcUDir_Swine_,trcUInd_Bull_,trcUInd_Swine_,trnAAllp,trnADirp,trnAIndp,trnA_Bull_p,trnA_Swine_p,trnADir_Bull_p,trnADir_Swine_p,trnAInd_Bull_p,trnAInd_Swine_p,trcAAllp,trcADirp,trcAIndp,trcA_Bull_p,trcA_Swine_p,trcADir_Bull_p,trcADir_Swine_p,trcAInd_Bull_p,trcAInd_Swine_p,trnAAll,trnADir,trnAInd,trnA_Bull_,trnA_Swine_,trnADir_Bull_,trnADir_Swine_,trnAInd_Bull_,trnAInd_Swine_,trcAAll,trcADir,trcAInd,trcA_Bull_,trcA_Swine_,trcADir_Bull_,trcADir_Swine_,trcAInd_Bull_,trcAInd_Swine_,tstnUTruePos,tstnUTruePos_Bull_,tstnUTruePos_Swine_,tstnUTrueNeg,tstnUTrueNeg_Bull_,tstnUTrueNeg_Swine_,tstnUFalsePos,tstnUFalsePos_Bull_,tstnUFalsePos_Swine_,tstnUFalseNeg,tstnUFalseNeg_Bull_,tstnUFalseNeg_Swine_,tstcUAll,tstcUDirFwd,tstcUIndFwd,tstcUDirBack,tstcUIndBack,tstcU_Bull_,tstcU_Swine_,tstcUDirFwd_Bull_,tstcUDirFwd_Swine_,tstcUIndFwd_Bull_,tstcUIndFwd_Swine_,tstcUDirBack_Bull_,tstcUDirBack_Swine_,tstcUIndBack_Bull_,tstcUIndBack_Swine_,tstcUTruePos,tstcUTruePos_Bull_,tstcUTruePos_Swine_,tstcUTrueNeg,tstcUTrueNeg_Bull_,tstcUTrueNeg_Swine_,tstcUFalsePos,tstcUFalsePos_Bull_,tstcUFalsePos_Swine_,tstcUFalseNeg,tstcUFalseNeg_Bull_,tstcUFalseNeg_Swine_,tstcAAll,tstcADirFwd,tstcAIndFwd,tstcADirBack,tstcAIndBack,tstcA_Bull_,tstcA_Swine_,tstcADirFwd_Bull_,tstcADirFwd_Swine_,tstcAIndFwd_Bull_,tstcAIndFwd_Swine_,tstcADirBack_Bull_,tstcADirBack_Swine_,tstcAIndBack_Bull_,tstcAIndBack_Swine_,vacwUAll,vacwU_Bull_,vacwU_Swine_,vacwAAll,vacwA_Bull_,vacwA_Swine_,vacwUMax,vacwUMaxDay,vacwAMax,vacwAMaxDay,vacwUTimeMax,vacwUTimeAvg,vacwUDaysInQueue,vacwADaysInQueue,infnUAll,infnUDir,infnUInd,infnUAir,infnUIni,infnU_Bull_,infnU_Swine_,infnUDir_Bull_,infnUDir_Swine_,infnUInd_Bull_,infnUInd_Swine_,infnUAir_Bull_,infnUAir_Swine_,infnUIni_Bull_,infnUIni_Swine_,infcUAll,infcUDir,infcUInd,infcUAir,infcUIni,infcU_Bull_,infcU_Swine_,infcUDir_Bull_,infcUDir_Swine_,infcUInd_Bull_,infcUInd_Swine_,infcUAir_Bull_,infcUAir_Swine_,infcUIni_Bull_,infcUIni_Swine_,infnAAll,infnADir,infnAInd,infnAAir,infnAIni,infnA_Bull_,infnA_Swine_,infnADir_Bull_,infnADir_Swine_,infnAInd_Bull_,infnAInd_Swine_,infnAAir_Bull_,infnAAir_Swine_,infnAIni_Bull_,infnAIni_Swine_,infcAAll,infcADir,infcAInd,infcAAir,infcAIni,infcA_Bull_,infcA_Swine_,infcADir_Bull_,infcADir_Swine_,infcAInd_Bull_,infcAInd_Swine_,infcAAir_Bull_,infcAAir_Swine_,infcAIni_Bull_,infcAIni_Swine_,firstDetUInfAll,firstDetAInfAll,ratio,vaccOccurred,firstVaccination,firstVaccinationRing,firstVaccination_Bull_,firstVaccination_Swine_,firstVaccinationRing_Bull_,firstVaccinationRing_Swine_,vacnUAll,vacnUIni,vacnURing,vacnU_Bull_,vacnU_Swine_,vacnUIni_Bull_,vacnUIni_Swine_,vacnURing_Bull_,vacnURing_Swine_,vaccUAll,vaccUIni,vaccURing,vaccU_Bull_,vaccU_Swine_,vaccUIni_Bull_,vaccUIni_Swine_,vaccURing_Bull_,vaccURing_Swine_,vacnAAll,vacnAIni,vacnARing,vacnA_Bull_,vacnA_Swine_,vacnAIni_Bull_,vacnAIni_Swine_,vacnARing_Bull_,vacnARing_Swine_,vaccAAll,vaccAIni,vaccARing,vaccA_Bull_,vaccA_Swine_,vaccAIni_Bull_,vaccAIni_Swine_,vaccARing_Bull_,vaccARing_Swine_,tsdUSusc,tsdULat,tsdUSubc,tsdUClin,tsdUNImm,tsdUVImm,tsdUDest,tsdU_Bull_Susc,tsdU_Bull_Lat,tsdU_Bull_Subc,tsdU_Bull_Clin,tsdU_Bull_NImm,tsdU_Bull_VImm,tsdU_Bull_Dest,tsdU_Swine_Susc,tsdU_Swine_Lat,tsdU_Swine_Subc,tsdU_Swine_Clin,tsdU_Swine_NImm,tsdU_Swine_VImm,tsdU_Swine_Dest,tsdASusc,tsdALat,tsdASubc,tsdAClin,tsdANImm,tsdAVImm,tsdADest,tsdA_Bull_Susc,tsdA_Bull_Lat,tsdA_Bull_Subc,tsdA_Bull_Clin,tsdA_Bull_NImm,tsdA_Bull_VImm,tsdA_Bull_Dest,tsdA_Swine_Susc,tsdA_Swine_Lat,tsdA_Swine_Subc,tsdA_Swine_Clin,tsdA_Swine_NImm,tsdA_Swine_VImm,tsdA_Swine_Dest,average-prevalence,diseaseDuration,exmnUAll,exmnURing,exmnUDirFwd,exmnUIndFwd,exmnUDirBack,exmnUIndBack,exmnUDet,exmnU_Bull_,exmnU_Swine_,exmnURing_Bull_,exmnURing_Swine_,exmnUDirFwd_Bull_,exmnUDirFwd_Swine_,exmnUIndFwd_Bull_,exmnUIndFwd_Swine_,exmnUDirBack_Bull_,exmnUDirBack_Swine_,exmnUIndBack_Bull_,exmnUIndBack_Swine_,exmnUDet_Bull_,exmnUDet_Swine_,exmnAAll,exmnARing,exmnADirFwd,exmnAIndFwd,exmnADirBack,exmnAIndBack,exmnADet,exmnA_Bull_,exmnA_Swine_,exmnARing_Bull_,exmnARing_Swine_,exmnADirFwd_Bull_,exmnADirFwd_Swine_,exmnAIndFwd_Bull_,exmnAIndFwd_Swine_,exmnADirBack_Bull_,exmnADirBack_Swine_,exmnAIndBack_Bull_,exmnAIndBack_Swine_,exmnADet_Bull_,exmnADet_Swine_,exmcUAll,exmcURing,exmcUDirFwd,exmcUIndFwd,exmcUDirBack,exmcUIndBack,exmcUDet,exmcU_Bull_,exmcU_Swine_,exmcURing_Bull_,exmcURing_Swine_,exmcUDirFwd_Bull_,exmcUDirFwd_Swine_,exmcUIndFwd_Bull_,exmcUIndFwd_Swine_,exmcUDirBack_Bull_,exmcUDirBack_Swine_,exmcUIndBack_Bull_,exmcUIndBack_Swine_,exmcUDet_Bull_,exmcUDet_Swine_,exmcAAll,exmcARing,exmcADirFwd,exmcAIndFwd,exmcADirBack,exmcAIndBack,exmcADet,exmcA_Bull_,exmcA_Swine_,exmcARing_Bull_,exmcARing_Swine_,exmcADirFwd_Bull_,exmcADirFwd_Swine_,exmcAIndFwd_Bull_,exmcAIndFwd_Swine_,exmcADirBack_Bull_,exmcADirBack_Swine_,exmcAIndBack_Bull_,exmcAIndBack_Swine_,exmcADet_Bull_,exmcADet_Swine_".split(',')
[r for r in recent_headers if len(substr_indices(cause_sweep, r)) == 0]  # if you can't find a match in previous headers

# <markdowncell>

# The above `recent_headers` was created after modifying the scenario, adding cost accounting and zone effects.  The empty set indicates the column names haven't changed any.  This means we have been working with a stable set.

# <codecell>

[h for h in cause_sweep if len(substr_indices(recent_headers, h)) == 0]  # if you can't find a match in previous headers

# <codecell>

set(recent_headers) == set(cause_sweep)

# <headingcell level=4>

# Migrations for other database will need to be handled manually, or a more programmatic "reset" needs to be created for Results.

# <codecell>


# <headingcell level=1>

# Parsing Test Notes

# <codecell>

successes= ['expnUDir_Bull_', 'detnUAll', 'trnUDir_Swine_p', 'tstnUTruePos_Swine_', 'exmnADirBack', 'trnADir', 'expnAInd_Swine_', 'exmnUDirBack_Bull_', 'trnAInd_Swine_', 'expnUInd', 'exmnURing_Bull_', 'vacnAIni', 'animalDaysInZoneMediumRisk_Bull_', 'exmnUDet_Bull_', 'trnUInd_Bull_', 'unitsInZoneMediumRisk_Swine_', 'detnUClin', 'deswADaysInQueue', 'exmnUIndFwd', 'animalDaysInZoneMediumRisk_Swine_', 'trnUDir_Bull_p', 'detnATest_Bull_', 'tstnUFalseNeg', 'tstnUTruePos', 'trnAAllp', 'vaccOccurred', 'expnUDir_Swine_', 'exmnAIndFwd', 'infnADir', 'detnUClin_Bull_', 'infnAAir', 'infnAInd_Swine_', 'exmnADet_Bull_', 'exmnUDirBack_Swine_', 'destrOccurred', 'trnAInd', 'exmnADirFwd_Bull_', 'infnUInd', 'expnAInd', 'trnUIndp', 'exmnADirFwd_Swine_', 'num-separate-areasHighRisk', 'infnADir_Swine_', 'detnUClin_Swine_', 'average-prevalence', 'exmnUIndBack', 'infnUDir_Swine_', 'trnUInd', 'infnAInd', 'infnUInd_Swine_', 'infnUAir', 'zonePerimeterHighRisk', 'expnUAir', 'exmnUIndFwd_Bull_', 'trnUDirp', 'adqcUAll', 'exmnUDet_Swine_', 'vacwUMax', 'unitDaysInZoneMediumRisk_Swine_', 'trnUInd_Bull_p', 'expnUInd_Bull_', 'vacnUIni_Swine_', 'exmnAAll', 'vacnAAll', 'unitsInZoneHighRisk_Swine_', 'vacwADaysInQueue', 'tstnUFalsePos_Swine_', 'exmnADirBack_Bull_', 'trnUInd_Swine_p', 'trnADir_Bull_p', 'maxZonePerimeterMediumRisk', 'vacnARing_Bull_', 'detnUTest_Swine_', 'animalDaysInZoneHighRisk_Swine_', 'trnUAll', 'exmnADet', 'infnUAir_Bull_', 'trnAInd_Swine_p', 'unitDaysInZoneHighRisk_Swine_', 'trnUDir', 'trnAInd_Bull_p', 'detnATest_Swine_', 'detOccurred', 'vacnURing', 'exmnUIndBack_Swine_', 'animalDaysInZoneMediumRisk', 'num-separate-areasMediumRisk', 'trnADir_Swine_', 'animalDaysInZoneHighRisk', 'detcUqAll', 'unitsInZoneBackground_Swine_', 'infnUAll', 'detnAClin_Bull_', 'expnAAll', 'expnUInd_Swine_', 'animalDaysInZoneHighRisk_Bull_', 'vacnUIni_Bull_', 'zonePerimeterMediumRisk', 'trnAIndp', 'tstnUTruePos_Bull_', 'exmnUAll', 'infnAAir_Bull_', 'vacnUAll', 'exmnUDet', 'exmnADirBack_Swine_', 'vacnUIni', 'exmnUIndFwd_Swine_', 'trnUDir_Bull_', 'unitsInZoneBackground', 'expnUAir_Bull_', 'detnUTest', 'vacnAIni_Bull_', 'trnUAllp', 'infnUDir', 'unitDaysInZoneBackground', 'vacnARing_Swine_', 'exmnARing_Bull_', 'zoneAreaHighRisk', 'exmnADirFwd', 'unitDaysInZoneMediumRisk_Bull_', 'exmnAIndBack', 'expnUAir_Swine_', 'maxZonePerimeterHighRisk', 'infnAInd_Bull_', 'exmnARing_Swine_', 'vacwUDaysInQueue', 'unitDaysInZoneBackground_Bull_', 'vacnARing', 'unitDaysInZoneHighRisk', 'expnAAir', 'expnUAll', 'infnUInd_Bull_', 'deswAMax', 'expnUDir', 'exmnAIndBack_Swine_', 'exmnURing', 'unitDaysInZoneBackground_Swine_', 'infnADir_Bull_', 'animalDaysInZoneBackground', 'unitDaysInZoneHighRisk_Bull_', 'trnADir_Bull_', 'unitsInZoneMediumRisk', 'exmnUDirBack', 'expnAAir_Bull_', 'trnADir_Swine_p', 'unitsInZoneBackground_Bull_', 'exmnAIndFwd_Bull_', 'trnUDir_Swine_', 'tstnUFalseNeg_Bull_', 'unitsInZoneHighRisk', 'exmnUDirFwd', 'infnAAll', 'expnAAir_Swine_', 'adqnUAll', 'animalDaysInZoneBackground_Bull_', 'animalDaysInZoneBackground_Swine_', 'detnAAll', 'tstnUTrueNeg_Bull_', 'detnATest', 'tstnUFalseNeg_Swine_', 'trnAInd_Bull_', 'exmnUIndBack_Bull_', 'vacnURing_Swine_', 'exmnUDirFwd_Swine_', 'expnADir_Swine_', 'exmnADet_Swine_', 'vacwAMax', 'trnUInd_Swine_', 'infnUDir_Bull_', 'expnAInd_Bull_', 'exmnARing', 'maxZoneAreaMediumRisk', 'tstnUFalsePos', 'maxZoneAreaHighRisk', 'trnAAll', 'deswUDaysInQueue', 'unitsInZoneHighRisk_Bull_', 'detnAClin_Swine_', 'trnADirp', 'deswUMax', 'exmnAIndFwd_Swine_', 'exmnUDirFwd_Bull_', 'zoneAreaMediumRisk', 'infnAAir_Swine_', 'unitDaysInZoneMediumRisk', 'expnADir_Bull_', 'expnADir', 'detnAClin', 'exmnAIndBack_Bull_', 'vacnURing_Bull_', 'tstnUTrueNeg', 'tstnUFalsePos_Bull_', 'tstnUTrueNeg_Swine_', 'infnUAir_Swine_', 'vacnAIni_Swine_', 'exmnURing_Swine_', 'detnUTest_Bull_', 'unitsInZoneMediumRisk_Bull_']
failures= ['tstcUDirFwd_Bull_', 'desnADirFwd', 'exmcUIndFwd_Bull_', 'trcAInd_Bull_p', 'tstcUTruePos_Bull_', 'descURing_Bull_', 'trcAAll', 'tsdU_Bull_Subc', 'desnAUnsp_Swine_', 'infcADir_Bull_', 'expcUDir', 'tstcAIndBack', 'infcUIni_Bull_', 'descADirFwd_Swine_', 'tsdA_Swine_Lat', 'tstcUTruePos_Swine_', 'tsdU_Swine_Lat', 'tsdA_Swine_NImm', 'exmcA_Swine_', 'infcADir', 'vaccU_Bull_', 'detcAClin', 'exmnU_Bull_', 'tstcUTrueNeg', 'vaccA_Bull_', 'trcADir_Swine_', 'exmcURing_Bull_', 'trcA_Bull_', 'trcA_Swine_p', 'desnADirFwd_Swine_', 'infnAIni_Bull_', 'deswU_Bull_', 'tsdASubc', 'tsdU_Bull_NImm', 'exmcUDet', 'tstcUFalseNeg_Swine_', 'expcUDir_Bull_', 'tstcAIndFwd_Bull_', 'tstcUFalseNeg', 'vaccARing_Swine_', 'descUIndBack_Bull_', 'exmcUDet_Swine_', 'deswU_Swine_', 'descADirBack_Swine_', 'trcUDir_Bull_', 'descADirFwd_Bull_', 'detcUTest_Bull_', 'expnU_Bull_', 'infcU_Bull_', 'trcAInd_Swine_p', 'trcUDir_Swine_p', 'exmnA_Bull_', 'trnU_Swine_', 'exmcUDirFwd_Swine_', 'expnA_Bull_', 'exmnU_Swine_', 'trcUDir', 'expcADir_Swine_', 'detcUClin_Swine_', 'vaccA_Swine_', 'infcUAir', 'trcU_Swine_', 'desnARing_Swine_', 'tsdA_Bull_NImm', 'trnA_Swine_', 'desnUIndBack', 'desnUIndFwd', 'trcAInd_Swine_', 'infcA_Bull_', 'trcUInd_Swine_p', 'tstcA_Bull_', 'trcA_Swine_', 'tstcUDirBack', 'vacnU_Bull_', 'desnU_Bull_', 'trnA_Bull_', 'infcUDir_Bull_', 'detcA_Swine_', 'tsdU_Swine_Subc', 'vacwU_Swine_', 'detcUAll', 'descUIni', 'exmcURing_Swine_', 'vaccAIni_Swine_', 'exmcAIndFwd_Bull_', 'exmcURing', 'deswA_Bull_', 'infcUAir_Bull_', 'exmcARing_Swine_', 'expcAAir', 'descUDirFwd_Bull_', 'exmcU_Bull_', 'tsdUDest', 'infnU_Bull_', 'infnUIni_Bull_', 'vaccARing_Bull_', 'infcAAir', 'desnAIni_Swine_', 'expcAInd_Bull_', 'detnA_Swine_', 'exmcADet', 'detcUTest_Swine_', 'tstcU_Swine_', 'tsdULat', 'desnADirBack_Bull_', 'tsdA_Swine_Clin', 'infcUDir', 'trcADir', 'exmcAAll', 'trcUIndp', 'descUIndBack_Swine_', 'desnUIndFwd_Bull_', 'infcUIni', 'deswAAll', 'exmcUIndBack', 'infcAAir_Bull_', 'desnUUnsp_Bull_', 'descA_Swine_', 'desnAIndBack', 'infnUIni', 'expnU_Swine_', 'desnAIndBack_Swine_', 'descUUnsp', 'expcUInd', 'desnURing', 'trcUInd_Bull_', 'infnAIni', 'infcUInd_Bull_', 'tstcADirBack_Swine_', 'descUDirFwd', 'descAUnsp_Swine_', 'detcU_Bull_', 'expcA_Bull_', 'desnAIndBack_Bull_', 'desnARing', 'tsdA_Bull_Clin', 'tsdUVImm', 'infcAInd_Swine_', 'exmcUIndFwd', 'desnURing_Bull_', 'detnU_Swine_', 'descURing_Swine_', 'vaccAAll', 'expcAInd_Swine_', 'tsdU_Swine_NImm', 'desnUIni_Swine_', 'detcATest_Swine_', 'desnURing_Swine_', 'tstcAAll', 'infcUIni_Swine_', 'trcUDirp', 'expcUInd_Bull_', 'descUUnsp_Bull_', 'exmcAIndBack_Swine_', 'infcUAll', 'descUDet_Swine_', 'tstcUIndBack_Swine_', 'tstcUTrueNeg_Swine_', 'desnUUnsp_Swine_', 'descUDirBack_Swine_', 'desnUIndBack_Swine_', 'tsdA_Bull_Lat', 'desnADirBack_Swine_', 'trcU_Bull_p', 'expcAAll', 'detcAClin_Swine_', 'exmcU_Swine_', 'exmcUDirBack', 'tstcADirBack_Bull_', 'tstcUIndFwd_Swine_', 'desnUIndFwd_Swine_', 'descUIndFwd_Swine_', 'desnAIni_Bull_', 'tsdU_Swine_Susc', 'exmcAIndBack', 'desnA_Swine_', 'tsdU_Swine_VImm', 'tsdALat', 'expnA_Swine_', 'exmcADet_Swine_\r\n', 'trcU_Bull_', 'infcUAir_Swine_', 'desnADirFwd_Bull_', 'descA_Bull_', 'vaccUIni_Bull_', 'desnUDet_Swine_', 'desnADet_Bull_', 'descUDirBack', 'tstcUFalsePos_Bull_', 'exmcARing', 'exmcUDet_Bull_', 'descUUnsp_Swine_', 'trcUAll', 'vacwUAll', 'trcAIndp', 'detcUClin', 'vaccU_Swine_', 'tstcA_Swine_', 'exmcADirFwd_Bull_', 'desnUDirFwd', 'descUIni_Bull_', 'exmcADirBack_Swine_', 'desnUDirBack', 'tstcUDirFwd', 'descADet_Bull_', 'desnUDirBack_Swine_', 'infnA_Bull_', 'tsdA_Swine_Susc', 'exmcUDirBack_Swine_', 'desnAAll', 'infcAInd_Bull_', 'desnU_Swine_', 'tsdA_Bull_VImm', 'expcA_Swine_', 'expcADir', 'vaccAIni', 'descADet_Swine_', 'descUIndFwd', 'tsdUSusc', 'exmcAIndFwd', 'desnUDet_Bull_', 'desnUDirFwd_Bull_', 'descADirBack', 'infcAIni_Swine_', 'tsdA_Bull_Dest', 'exmcUIndFwd_Swine_', 'tstcU_Bull_', 'tstcADirBack', 'expcAInd', 'exmnA_Swine_', 'descARing', 'detcUTest', 'tsdU_Bull_Lat', 'exmcADet_Bull_', 'trcUAllp', 'infnU_Swine_', 'descAIni', 'trcUDir_Bull_p', 'vaccURing_Swine_', 'descUDet_Bull_', 'tsdA_Swine_VImm', 'infcUInd_Swine_', 'descUIni_Swine_', 'trcAInd_Bull_', 'detcATest', 'detnU_Bull_', 'desnUIni', 'tstcUIndBack', 'exmcAIndBack_Bull_', 'vaccAIni_Bull_', 'desnUIndBack_Bull_', 'tsdU_Bull_Dest', 'exmcAIndFwd_Swine_', 'tstcUIndFwd_Bull_', 'descADet', 'tstcUIndFwd', 'descUAll', 'vacnU_Swine_', 'infcUInd', 'tsdAVImm', 'trcADir_Bull_p', 'trnA_Swine_p', 'infcA_Swine_', 'expcUAll', 'descARing_Bull_', 'descAIndFwd', 'tstcUDirBack_Swine_', 'infcAIni_Bull_', 'expcU_Swine_', 'detcU_Swine_', 'trnU_Bull_', 'exmcARing_Bull_', 'expcAAir_Swine_', 'trcAInd', 'tsdASusc', 'tsdADest', 'desnAUnsp_Bull_', 'descAUnsp_Bull_', 'exmcUDirFwd', 'descAIndBack', 'tstcADirFwd_Swine_', 'desnARing_Bull_', 'tsdAClin', 'desnUDirFwd_Swine_', 'infcAIni', 'infnUIni_Swine_', 'descAAll', 'infnA_Swine_', 'descADirBack_Bull_', 'deswA_Swine_', 'tstcAIndBack_Bull_', 'vacwA_Bull_', 'trcUInd_Swine_', 'trcUInd_Bull_p', 'trcADir_Swine_p', 'exmcUIndBack_Bull_', 'vaccURing', 'tstcUFalseNeg_Bull_', 'desnADet_Swine_', 'tstcUFalsePos', 'vaccUIni_Swine_', 'exmcADirFwd', 'infcUDir_Swine_', 'exmcUDirFwd_Bull_', 'descARing_Swine_', 'trcADir_Bull_', 'detcAClin_Bull_', 'tsdU_Swine_Dest', 'desnUDet', 'desnA_Bull_', 'vaccUAll', 'trnU_Bull_p', 'tstcAIndBack_Swine_', 'expcUAir', 'tsdA_Swine_Dest', 'trcA_Bull_p', 'exmcUIndBack_Swine_', 'descU_Swine_', 'tstcAIndFwd_Swine_', 'desnUIni_Bull_', 'tsdUSubc', 'exmcA_Bull_', 'tstcUIndBack_Bull_', 'descAIndBack_Swine_', 'trcU_Swine_p', 'expcADir_Bull_', 'tstcUFalsePos_Swine_', 'vacnA_Swine_', 'desnAIndFwd', 'trcAAllp', 'infcAInd', 'descUIndFwd_Bull_', 'vacnA_Bull_', 'tsdANImm', 'tsdU_Bull_VImm', 'desnAIni', 'desnUAll', 'vaccARing', 'descAIndFwd_Bull_', 'descURing', 'infnAIni_Swine_', 'exmcADirBack_Bull_', 'deswUAll', 'descAIni_Swine_', 'infcU_Swine_', 'trcADirp', 'detcA_Bull_', 'vacwU_Bull_', 'tsdUNImm', 'expcUAir_Bull_', 'desnAIndFwd_Swine_', 'tstcAIndFwd', 'vacwA_Swine_', 'tsdA_Bull_Subc', 'tsdU_Bull_Susc', 'detcUClin_Bull_', 'desnAIndFwd_Bull_', 'infcAAll', 'exmcADirBack', 'expcUDir_Swine_', 'vaccURing_Bull_', 'tstcUDirFwd_Swine_', 'vaccUIni', 'detcATest_Bull_', 'tstcUTrueNeg_Bull_', 'tsdA_Bull_Susc', 'descAIndFwd_Swine_', 'exmcUDirBack_Bull_', 'tstcUDirBack_Bull_', 'desnADirBack', 'descADirFwd', 'infcADir_Swine_', 'descAIni_Bull_', 'desnAUnsp', 'tsdUClin', 'infcAAir_Swine_', 'detcAAll', 'expcUInd_Swine_', 'trnU_Swine_p', 'desnUDirBack_Bull_', 'trcUDir_Swine_', 'desnADet', 'expcUAir_Swine_', 'tsdA_Swine_Subc', 'descUDirBack_Bull_', 'tstcADirFwd_Bull_', 'tstcUAll', 'detnA_Bull_', 'descUDirFwd_Swine_', 'trnA_Bull_p', 'vacwAAll', 'expcAAir_Bull_', 'exmcADirFwd_Swine_', 'descUDet', 'descAUnsp', 'descU_Bull_', 'descAIndBack_Bull_', 'desnUUnsp', 'expcU_Bull_', 'exmcUAll', 'trcUInd', 'tstcUTruePos', 'tstcADirFwd', 'descUIndBack', 'tsdU_Bull_Clin', 'tsdU_Swine_Clin']
print(len(successes), len(failures))

# <codecell>


