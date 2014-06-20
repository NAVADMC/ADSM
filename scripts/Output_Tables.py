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
                line += " db_column='" + django_name + "', "
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

'zonc' in "Run,Day,outbreakDuration,infnUAll,infnUDir,infnUInd,infnUAir,infnUIni,infnUB,infnUBDS,infnUS,infnUBD,infnUBS,infnUD,infnUDS,infnUP,infnUDirB,infnUDirBDS,infnUDirS,infnUDirBD,infnUDirBS,infnUDirD,infnUDirDS,infnUDirP,infnUIndB,infnUIndBDS,infnUIndS,infnUIndBD,infnUIndBS,infnUIndD,infnUIndDS,infnUIndP,infnUAirB,infnUAirBDS,infnUAirS,infnUAirBD,infnUAirBS,infnUAirD,infnUAirDS,infnUAirP,infnUIniB,infnUIniBDS,infnUIniS,infnUIniBD,infnUIniBS,infnUIniD,infnUIniDS,infnUIniP,infcUAll,infcUDir,infcUInd,infcUAir,infcUIni,infcUB,infcUBDS,infcUS,infcUBD,infcUBS,infcUD,infcUDS,infcUP,infcUDirB,infcUDirBDS,infcUDirS,infcUDirBD,infcUDirBS,infcUDirD,infcUDirDS,infcUDirP,infcUIndB,infcUIndBDS,infcUIndS,infcUIndBD,infcUIndBS,infcUIndD,infcUIndDS,infcUIndP,infcUAirB,infcUAirBDS,infcUAirS,infcUAirBD,infcUAirBS,infcUAirD,infcUAirDS,infcUAirP,infcUIniB,infcUIniBDS,infcUIniS,infcUIniBD,infcUIniBS,infcUIniD,infcUIniDS,infcUIniP,infnAAll,infnADir,infnAInd,infnAAir,infnAIni,infnAB,infnABDS,infnAS,infnABD,infnABS,infnAD,infnADS,infnAP,infnADirB,infnADirBDS,infnADirS,infnADirBD,infnADirBS,infnADirD,infnADirDS,infnADirP,infnAIndB,infnAIndBDS,infnAIndS,infnAIndBD,infnAIndBS,infnAIndD,infnAIndDS,infnAIndP,infnAAirB,infnAAirBDS,infnAAirS,infnAAirBD,infnAAirBS,infnAAirD,infnAAirDS,infnAAirP,infnAIniB,infnAIniBDS,infnAIniS,infnAIniBD,infnAIniBS,infnAIniD,infnAIniDS,infnAIniP,infcAAll,infcADir,infcAInd,infcAAir,infcAIni,infcAB,infcABDS,infcAS,infcABD,infcABS,infcAD,infcADS,infcAP,infcADirB,infcADirBDS,infcADirS,infcADirBD,infcADirBS,infcADirD,infcADirDS,infcADirP,infcAIndB,infcAIndBDS,infcAIndS,infcAIndBD,infcAIndBS,infcAIndD,infcAIndDS,infcAIndP,infcAAirB,infcAAirBDS,infcAAirS,infcAAirBD,infcAAirBS,infcAAirD,infcAAirDS,infcAAirP,infcAIniB,infcAIniBDS,infcAIniS,infcAIniBD,infcAIniBS,infcAIniD,infcAIniDS,infcAIniP,firstDetUInfAll,firstDetAInfAll,ratio,tsdUSusc,tsdULat,tsdUSubc,tsdUClin,tsdUNImm,tsdUVImm,tsdUDest,tsdUBSusc,tsdUBLat,tsdUBSubc,tsdUBClin,tsdUBNImm,tsdUBVImm,tsdUBDest,tsdUBDSSusc,tsdUBDSLat,tsdUBDSSubc,tsdUBDSClin,tsdUBDSNImm,tsdUBDSVImm,tsdUBDSDest,tsdUSSusc,tsdUSLat,tsdUSSubc,tsdUSClin,tsdUSNImm,tsdUSVImm,tsdUSDest,tsdUBDSusc,tsdUBDLat,tsdUBDSubc,tsdUBDClin,tsdUBDNImm,tsdUBDVImm,tsdUBDDest,tsdUBSSusc,tsdUBSLat,tsdUBSSubc,tsdUBSClin,tsdUBSNImm,tsdUBSVImm,tsdUBSDest,tsdUDSusc,tsdUDLat,tsdUDSubc,tsdUDClin,tsdUDNImm,tsdUDVImm,tsdUDDest,tsdUDSSusc,tsdUDSLat,tsdUDSSubc,tsdUDSClin,tsdUDSNImm,tsdUDSVImm,tsdUDSDest,tsdUPSusc,tsdUPLat,tsdUPSubc,tsdUPClin,tsdUPNImm,tsdUPVImm,tsdUPDest,tsdASusc,tsdALat,tsdASubc,tsdAClin,tsdANImm,tsdAVImm,tsdADest,tsdABSusc,tsdABLat,tsdABSubc,tsdABClin,tsdABNImm,tsdABVImm,tsdABDest,tsdABDSSusc,tsdABDSLat,tsdABDSSubc,tsdABDSClin,tsdABDSNImm,tsdABDSVImm,tsdABDSDest,tsdASSusc,tsdASLat,tsdASSubc,tsdASClin,tsdASNImm,tsdASVImm,tsdASDest,tsdABDSusc,tsdABDLat,tsdABDSubc,tsdABDClin,tsdABDNImm,tsdABDVImm,tsdABDDest,tsdABSSusc,tsdABSLat,tsdABSSubc,tsdABSClin,tsdABSNImm,tsdABSVImm,tsdABSDest,tsdADSusc,tsdADLat,tsdADSubc,tsdADClin,tsdADNImm,tsdADVImm,tsdADDest,tsdADSSusc,tsdADSLat,tsdADSSubc,tsdADSClin,tsdADSNImm,tsdADSVImm,tsdADSDest,tsdAPSusc,tsdAPLat,tsdAPSubc,tsdAPClin,tsdAPNImm,tsdAPVImm,tsdAPDest,average-prevalence,diseaseDuration,vacwUAll,vacwUB,vacwUBDS,vacwUS,vacwUBD,vacwUBS,vacwUD,vacwUDS,vacwUP,vacwAAll,vacwAB,vacwABDS,vacwAS,vacwABD,vacwABS,vacwAD,vacwADS,vacwAP,vacwUMax,vacwUMaxDay,vacwAMax,vacwAMaxDay,vacwUTimeMax,vacwUTimeAvg,vacwUDaysInQueue,vacwADaysInQueue,zoneAreaHighRisk,zoneAreaMediumRisk,maxZoneAreaHighRisk,maxZoneAreaMediumRisk,maxZoneAreaDayHighRisk,maxZoneAreaDayMediumRisk,finalZoneAreaHighRisk,finalZoneAreaMediumRisk,zonePerimeterHighRisk,zonePerimeterMediumRisk,maxZonePerimeterHighRisk,maxZonePerimeterMediumRisk,maxZonePerimeterDayHighRisk,maxZonePerimeterDayMediumRisk,finalZonePerimeterHighRisk,finalZonePerimeterMediumRisk,num-separate-areasHighRisk,num-separate-areasMediumRisk,unitsInZoneHighRisk,unitsInZoneMediumRisk,unitsInZoneBackground,unitsInZoneHighRiskB,unitsInZoneHighRiskBDS,unitsInZoneHighRiskS,unitsInZoneHighRiskBD,unitsInZoneHighRiskBS,unitsInZoneHighRiskD,unitsInZoneHighRiskDS,unitsInZoneHighRiskP,unitsInZoneMediumRiskB,unitsInZoneMediumRiskBDS,unitsInZoneMediumRiskS,unitsInZoneMediumRiskBD,unitsInZoneMediumRiskBS,unitsInZoneMediumRiskD,unitsInZoneMediumRiskDS,unitsInZoneMediumRiskP,unitsInZoneBackgroundB,unitsInZoneBackgroundBDS,unitsInZoneBackgroundS,unitsInZoneBackgroundBD,unitsInZoneBackgroundBS,unitsInZoneBackgroundD,unitsInZoneBackgroundDS,unitsInZoneBackgroundP,unitDaysInZoneHighRisk,unitDaysInZoneMediumRisk,unitDaysInZoneBackground,unitDaysInZoneHighRiskB,unitDaysInZoneHighRiskBDS,unitDaysInZoneHighRiskS,unitDaysInZoneHighRiskBD,unitDaysInZoneHighRiskBS,unitDaysInZoneHighRiskD,unitDaysInZoneHighRiskDS,unitDaysInZoneHighRiskP,unitDaysInZoneMediumRiskB,unitDaysInZoneMediumRiskBDS,unitDaysInZoneMediumRiskS,unitDaysInZoneMediumRiskBD,unitDaysInZoneMediumRiskBS,unitDaysInZoneMediumRiskD,unitDaysInZoneMediumRiskDS,unitDaysInZoneMediumRiskP,unitDaysInZoneBackgroundB,unitDaysInZoneBackgroundBDS,unitDaysInZoneBackgroundS,unitDaysInZoneBackgroundBD,unitDaysInZoneBackgroundBS,unitDaysInZoneBackgroundD,unitDaysInZoneBackgroundDS,unitDaysInZoneBackgroundP,animalDaysInZoneHighRisk,animalDaysInZoneMediumRisk,animalDaysInZoneBackground,animalDaysInZoneHighRiskB,animalDaysInZoneHighRiskBDS,animalDaysInZoneHighRiskS,animalDaysInZoneHighRiskBD,animalDaysInZoneHighRiskBS,animalDaysInZoneHighRiskD,animalDaysInZoneHighRiskDS,animalDaysInZoneHighRiskP,animalDaysInZoneMediumRiskB,animalDaysInZoneMediumRiskBDS,animalDaysInZoneMediumRiskS,animalDaysInZoneMediumRiskBD,animalDaysInZoneMediumRiskBS,animalDaysInZoneMediumRiskD,animalDaysInZoneMediumRiskDS,animalDaysInZoneMediumRiskP,animalDaysInZoneBackgroundB,animalDaysInZoneBackgroundBDS,animalDaysInZoneBackgroundS,animalDaysInZoneBackgroundBD,animalDaysInZoneBackgroundBS,animalDaysInZoneBackgroundD,animalDaysInZoneBackgroundDS,animalDaysInZoneBackgroundP,trnUAllp,trnUDirp,trnUIndp,trnUBp,trnUBDSp,trnUSp,trnUBDp,trnUBSp,trnUDp,trnUDSp,trnUPp,trnUDirBp,trnUDirBDSp,trnUDirSp,trnUDirBDp,trnUDirBSp,trnUDirDp,trnUDirDSp,trnUDirPp,trnUIndBp,trnUIndBDSp,trnUIndSp,trnUIndBDp,trnUIndBSp,trnUIndDp,trnUIndDSp,trnUIndPp,trcUAllp,trcUDirp,trcUIndp,trcUBp,trcUBDSp,trcUSp,trcUBDp,trcUBSp,trcUDp,trcUDSp,trcUPp,trcUDirBp,trcUDirBDSp,trcUDirSp,trcUDirBDp,trcUDirBSp,trcUDirDp,trcUDirDSp,trcUDirPp,trcUIndBp,trcUIndBDSp,trcUIndSp,trcUIndBDp,trcUIndBSp,trcUIndDp,trcUIndDSp,trcUIndPp,trnUAll,trnUDir,trnUInd,trnUB,trnUBDS,trnUS,trnUBD,trnUBS,trnUD,trnUDS,trnUP,trnUDirB,trnUDirBDS,trnUDirS,trnUDirBD,trnUDirBS,trnUDirD,trnUDirDS,trnUDirP,trnUIndB,trnUIndBDS,trnUIndS,trnUIndBD,trnUIndBS,trnUIndD,trnUIndDS,trnUIndP,trcUAll,trcUDir,trcUInd,trcUB,trcUBDS,trcUS,trcUBD,trcUBS,trcUD,trcUDS,trcUP,trcUDirB,trcUDirBDS,trcUDirS,trcUDirBD,trcUDirBS,trcUDirD,trcUDirDS,trcUDirP,trcUIndB,trcUIndBDS,trcUIndS,trcUIndBD,trcUIndBS,trcUIndD,trcUIndDS,trcUIndP,trnAAllp,trnADirp,trnAIndp,trnABp,trnABDSp,trnASp,trnABDp,trnABSp,trnADp,trnADSp,trnAPp,trnADirBp,trnADirBDSp,trnADirSp,trnADirBDp,trnADirBSp,trnADirDp,trnADirDSp,trnADirPp,trnAIndBp,trnAIndBDSp,trnAIndSp,trnAIndBDp,trnAIndBSp,trnAIndDp,trnAIndDSp,trnAIndPp,trcAAllp,trcADirp,trcAIndp,trcABp,trcABDSp,trcASp,trcABDp,trcABSp,trcADp,trcADSp,trcAPp,trcADirBp,trcADirBDSp,trcADirSp,trcADirBDp,trcADirBSp,trcADirDp,trcADirDSp,trcADirPp,trcAIndBp,trcAIndBDSp,trcAIndSp,trcAIndBDp,trcAIndBSp,trcAIndDp,trcAIndDSp,trcAIndPp,trnAAll,trnADir,trnAInd,trnAB,trnABDS,trnAS,trnABD,trnABS,trnAD,trnADS,trnAP,trnADirB,trnADirBDS,trnADirS,trnADirBD,trnADirBS,trnADirD,trnADirDS,trnADirP,trnAIndB,trnAIndBDS,trnAIndS,trnAIndBD,trnAIndBS,trnAIndD,trnAIndDS,trnAIndP,trcAAll,trcADir,trcAInd,trcAB,trcABDS,trcAS,trcABD,trcABS,trcAD,trcADS,trcAP,trcADirB,trcADirBDS,trcADirS,trcADirBD,trcADirBS,trcADirD,trcADirDS,trcADirP,trcAIndB,trcAIndBDS,trcAIndS,trcAIndBD,trcAIndBS,trcAIndD,trcAIndDS,trcAIndP,destrOccurred,firstDestruction,firstDestructionUnsp,firstDestructionRing,firstDestructionDirFwd,firstDestructionIndFwd,firstDestructionDirBack,firstDestructionIndBack,firstDestructionDet,firstDestructionIni,firstDestructionB,firstDestructionBDS,firstDestructionS,firstDestructionBD,firstDestructionBS,firstDestructionD,firstDestructionDS,firstDestructionP,firstDestructionUnspB,firstDestructionUnspBDS,firstDestructionUnspS,firstDestructionUnspBD,firstDestructionUnspBS,firstDestructionUnspD,firstDestructionUnspDS,firstDestructionUnspP,firstDestructionRingB,firstDestructionRingBDS,firstDestructionRingS,firstDestructionRingBD,firstDestructionRingBS,firstDestructionRingD,firstDestructionRingDS,firstDestructionRingP,firstDestructionDirFwdB,firstDestructionDirFwdBDS,firstDestructionDirFwdS,firstDestructionDirFwdBD,firstDestructionDirFwdBS,firstDestructionDirFwdD,firstDestructionDirFwdDS,firstDestructionDirFwdP,firstDestructionIndFwdB,firstDestructionIndFwdBDS,firstDestructionIndFwdS,firstDestructionIndFwdBD,firstDestructionIndFwdBS,firstDestructionIndFwdD,firstDestructionIndFwdDS,firstDestructionIndFwdP,firstDestructionDirBackB,firstDestructionDirBackBDS,firstDestructionDirBackS,firstDestructionDirBackBD,firstDestructionDirBackBS,firstDestructionDirBackD,firstDestructionDirBackDS,firstDestructionDirBackP,firstDestructionIndBackB,firstDestructionIndBackBDS,firstDestructionIndBackS,firstDestructionIndBackBD,firstDestructionIndBackBS,firstDestructionIndBackD,firstDestructionIndBackDS,firstDestructionIndBackP,firstDestructionDetB,firstDestructionDetBDS,firstDestructionDetS,firstDestructionDetBD,firstDestructionDetBS,firstDestructionDetD,firstDestructionDetDS,firstDestructionDetP,firstDestructionIniB,firstDestructionIniBDS,firstDestructionIniS,firstDestructionIniBD,firstDestructionIniBS,firstDestructionIniD,firstDestructionIniDS,firstDestructionIniP,desnUAll,desnUIni,desnUUnsp,desnURing,desnUDirFwd,desnUIndFwd,desnUDirBack,desnUIndBack,desnUDet,desnUB,desnUBDS,desnUS,desnUBD,desnUBS,desnUD,desnUDS,desnUP,desnUIniB,desnUIniBDS,desnUIniS,desnUIniBD,desnUIniBS,desnUIniD,desnUIniDS,desnUIniP,desnUUnspB,desnUUnspBDS,desnUUnspS,desnUUnspBD,desnUUnspBS,desnUUnspD,desnUUnspDS,desnUUnspP,desnURingB,desnURingBDS,desnURingS,desnURingBD,desnURingBS,desnURingD,desnURingDS,desnURingP,desnUDirFwdB,desnUDirFwdBDS,desnUDirFwdS,desnUDirFwdBD,desnUDirFwdBS,desnUDirFwdD,desnUDirFwdDS,desnUDirFwdP,desnUIndFwdB,desnUIndFwdBDS,desnUIndFwdS,desnUIndFwdBD,desnUIndFwdBS,desnUIndFwdD,desnUIndFwdDS,desnUIndFwdP,desnUDirBackB,desnUDirBackBDS,desnUDirBackS,desnUDirBackBD,desnUDirBackBS,desnUDirBackD,desnUDirBackDS,desnUDirBackP,desnUIndBackB,desnUIndBackBDS,desnUIndBackS,desnUIndBackBD,desnUIndBackBS,desnUIndBackD,desnUIndBackDS,desnUIndBackP,desnUDetB,desnUDetBDS,desnUDetS,desnUDetBD,desnUDetBS,desnUDetD,desnUDetDS,desnUDetP,descUAll,descUIni,descUUnsp,descURing,descUDirFwd,descUIndFwd,descUDirBack,descUIndBack,descUDet,descUB,descUBDS,descUS,descUBD,descUBS,descUD,descUDS,descUP,descUIniB,descUIniBDS,descUIniS,descUIniBD,descUIniBS,descUIniD,descUIniDS,descUIniP,descUUnspB,descUUnspBDS,descUUnspS,descUUnspBD,descUUnspBS,descUUnspD,descUUnspDS,descUUnspP,descURingB,descURingBDS,descURingS,descURingBD,descURingBS,descURingD,descURingDS,descURingP,descUDirFwdB,descUDirFwdBDS,descUDirFwdS,descUDirFwdBD,descUDirFwdBS,descUDirFwdD,descUDirFwdDS,descUDirFwdP,descUIndFwdB,descUIndFwdBDS,descUIndFwdS,descUIndFwdBD,descUIndFwdBS,descUIndFwdD,descUIndFwdDS,descUIndFwdP,descUDirBackB,descUDirBackBDS,descUDirBackS,descUDirBackBD,descUDirBackBS,descUDirBackD,descUDirBackDS,descUDirBackP,descUIndBackB,descUIndBackBDS,descUIndBackS,descUIndBackBD,descUIndBackBS,descUIndBackD,descUIndBackDS,descUIndBackP,descUDetB,descUDetBDS,descUDetS,descUDetBD,descUDetBS,descUDetD,descUDetDS,descUDetP,desnAAll,desnAIni,desnAUnsp,desnARing,desnADirFwd,desnAIndFwd,desnADirBack,desnAIndBack,desnADet,desnAB,desnABDS,desnAS,desnABD,desnABS,desnAD,desnADS,desnAP,desnAIniB,desnAIniBDS,desnAIniS,desnAIniBD,desnAIniBS,desnAIniD,desnAIniDS,desnAIniP,desnAUnspB,desnAUnspBDS,desnAUnspS,desnAUnspBD,desnAUnspBS,desnAUnspD,desnAUnspDS,desnAUnspP,desnARingB,desnARingBDS,desnARingS,desnARingBD,desnARingBS,desnARingD,desnARingDS,desnARingP,desnADirFwdB,desnADirFwdBDS,desnADirFwdS,desnADirFwdBD,desnADirFwdBS,desnADirFwdD,desnADirFwdDS,desnADirFwdP,desnAIndFwdB,desnAIndFwdBDS,desnAIndFwdS,desnAIndFwdBD,desnAIndFwdBS,desnAIndFwdD,desnAIndFwdDS,desnAIndFwdP,desnADirBackB,desnADirBackBDS,desnADirBackS,desnADirBackBD,desnADirBackBS,desnADirBackD,desnADirBackDS,desnADirBackP,desnAIndBackB,desnAIndBackBDS,desnAIndBackS,desnAIndBackBD,desnAIndBackBS,desnAIndBackD,desnAIndBackDS,desnAIndBackP,desnADetB,desnADetBDS,desnADetS,desnADetBD,desnADetBS,desnADetD,desnADetDS,desnADetP,descAAll,descAIni,descAUnsp,descARing,descADirFwd,descAIndFwd,descADirBack,descAIndBack,descADet,descAB,descABDS,descAS,descABD,descABS,descAD,descADS,descAP,descAIniB,descAIniBDS,descAIniS,descAIniBD,descAIniBS,descAIniD,descAIniDS,descAIniP,descAUnspB,descAUnspBDS,descAUnspS,descAUnspBD,descAUnspBS,descAUnspD,descAUnspDS,descAUnspP,descARingB,descARingBDS,descARingS,descARingBD,descARingBS,descARingD,descARingDS,descARingP,descADirFwdB,descADirFwdBDS,descADirFwdS,descADirFwdBD,descADirFwdBS,descADirFwdD,descADirFwdDS,descADirFwdP,descAIndFwdB,descAIndFwdBDS,descAIndFwdS,descAIndFwdBD,descAIndFwdBS,descAIndFwdD,descAIndFwdDS,descAIndFwdP,descADirBackB,descADirBackBDS,descADirBackS,descADirBackBD,descADirBackBS,descADirBackD,descADirBackDS,descADirBackP,descAIndBackB,descAIndBackBDS,descAIndBackS,descAIndBackBD,descAIndBackBS,descAIndBackD,descAIndBackDS,descAIndBackP,descADetB,descADetBDS,descADetS,descADetBD,descADetBS,descADetD,descADetDS,descADetP,vaccOccurred,firstVaccination,firstVaccinationRing,firstVaccinationB,firstVaccinationBDS,firstVaccinationS,firstVaccinationBD,firstVaccinationBS,firstVaccinationD,firstVaccinationDS,firstVaccinationP,firstVaccinationRingB,firstVaccinationRingBDS,firstVaccinationRingS,firstVaccinationRingBD,firstVaccinationRingBS,firstVaccinationRingD,firstVaccinationRingDS,firstVaccinationRingP,vacnUAll,vacnUIni,vacnURing,vacnUB,vacnUBDS,vacnUS,vacnUBD,vacnUBS,vacnUD,vacnUDS,vacnUP,vacnUIniB,vacnUIniBDS,vacnUIniS,vacnUIniBD,vacnUIniBS,vacnUIniD,vacnUIniDS,vacnUIniP,vacnURingB,vacnURingBDS,vacnURingS,vacnURingBD,vacnURingBS,vacnURingD,vacnURingDS,vacnURingP,vaccUAll,vaccUIni,vaccURing,vaccUB,vaccUBDS,vaccUS,vaccUBD,vaccUBS,vaccUD,vaccUDS,vaccUP,vaccUIniB,vaccUIniBDS,vaccUIniS,vaccUIniBD,vaccUIniBS,vaccUIniD,vaccUIniDS,vaccUIniP,vaccURingB,vaccURingBDS,vaccURingS,vaccURingBD,vaccURingBS,vaccURingD,vaccURingDS,vaccURingP,vacnAAll,vacnAIni,vacnARing,vacnAB,vacnABDS,vacnAS,vacnABD,vacnABS,vacnAD,vacnADS,vacnAP,vacnAIniB,vacnAIniBDS,vacnAIniS,vacnAIniBD,vacnAIniBS,vacnAIniD,vacnAIniDS,vacnAIniP,vacnARingB,vacnARingBDS,vacnARingS,vacnARingBD,vacnARingBS,vacnARingD,vacnARingDS,vacnARingP,vaccAAll,vaccAIni,vaccARing,vaccAB,vaccABDS,vaccAS,vaccABD,vaccABS,vaccAD,vaccADS,vaccAP,vaccAIniB,vaccAIniBDS,vaccAIniS,vaccAIniBD,vaccAIniBS,vaccAIniD,vaccAIniDS,vaccAIniP,vaccARingB,vaccARingBDS,vaccARingS,vaccARingBD,vaccARingBS,vaccARingD,vaccARingDS,vaccARingP,deswUAll,deswUB,deswUBDS,deswUS,deswUBD,deswUBS,deswUD,deswUDS,deswUP,deswAAll,deswAB,deswABDS,deswAS,deswABD,deswABS,deswAD,deswADS,deswAP,deswUMax,deswUMaxDay,deswAMax,deswAMaxDay,deswUTimeMax,deswUTimeAvg,deswUDaysInQueue,deswADaysInQueue,tstnUTruePos,tstnUTruePosB,tstnUTruePosBDS,tstnUTruePosS,tstnUTruePosBD,tstnUTruePosBS,tstnUTruePosD,tstnUTruePosDS,tstnUTruePosP,tstnUTrueNeg,tstnUTrueNegB,tstnUTrueNegBDS,tstnUTrueNegS,tstnUTrueNegBD,tstnUTrueNegBS,tstnUTrueNegD,tstnUTrueNegDS,tstnUTrueNegP,tstnUFalsePos,tstnUFalsePosB,tstnUFalsePosBDS,tstnUFalsePosS,tstnUFalsePosBD,tstnUFalsePosBS,tstnUFalsePosD,tstnUFalsePosDS,tstnUFalsePosP,tstnUFalseNeg,tstnUFalseNegB,tstnUFalseNegBDS,tstnUFalseNegS,tstnUFalseNegBD,tstnUFalseNegBS,tstnUFalseNegD,tstnUFalseNegDS,tstnUFalseNegP,tstcUAll,tstcUDirFwd,tstcUIndFwd,tstcUDirBack,tstcUIndBack,tstcUB,tstcUBDS,tstcUS,tstcUBD,tstcUBS,tstcUD,tstcUDS,tstcUP,tstcUDirFwdB,tstcUDirFwdBDS,tstcUDirFwdS,tstcUDirFwdBD,tstcUDirFwdBS,tstcUDirFwdD,tstcUDirFwdDS,tstcUDirFwdP,tstcUIndFwdB,tstcUIndFwdBDS,tstcUIndFwdS,tstcUIndFwdBD,tstcUIndFwdBS,tstcUIndFwdD,tstcUIndFwdDS,tstcUIndFwdP,tstcUDirBackB,tstcUDirBackBDS,tstcUDirBackS,tstcUDirBackBD,tstcUDirBackBS,tstcUDirBackD,tstcUDirBackDS,tstcUDirBackP,tstcUIndBackB,tstcUIndBackBDS,tstcUIndBackS,tstcUIndBackBD,tstcUIndBackBS,tstcUIndBackD,tstcUIndBackDS,tstcUIndBackP,tstcUTruePos,tstcUTruePosB,tstcUTruePosBDS,tstcUTruePosS,tstcUTruePosBD,tstcUTruePosBS,tstcUTruePosD,tstcUTruePosDS,tstcUTruePosP,tstcUTrueNeg,tstcUTrueNegB,tstcUTrueNegBDS,tstcUTrueNegS,tstcUTrueNegBD,tstcUTrueNegBS,tstcUTrueNegD,tstcUTrueNegDS,tstcUTrueNegP,tstcUFalsePos,tstcUFalsePosB,tstcUFalsePosBDS,tstcUFalsePosS,tstcUFalsePosBD,tstcUFalsePosBS,tstcUFalsePosD,tstcUFalsePosDS,tstcUFalsePosP,tstcUFalseNeg,tstcUFalseNegB,tstcUFalseNegBDS,tstcUFalseNegS,tstcUFalseNegBD,tstcUFalseNegBS,tstcUFalseNegD,tstcUFalseNegDS,tstcUFalseNegP,tstcAAll,tstcADirFwd,tstcAIndFwd,tstcADirBack,tstcAIndBack,tstcAB,tstcABDS,tstcAS,tstcABD,tstcABS,tstcAD,tstcADS,tstcAP,tstcADirFwdB,tstcADirFwdBDS,tstcADirFwdS,tstcADirFwdBD,tstcADirFwdBS,tstcADirFwdD,tstcADirFwdDS,tstcADirFwdP,tstcAIndFwdB,tstcAIndFwdBDS,tstcAIndFwdS,tstcAIndFwdBD,tstcAIndFwdBS,tstcAIndFwdD,tstcAIndFwdDS,tstcAIndFwdP,tstcADirBackB,tstcADirBackBDS,tstcADirBackS,tstcADirBackBD,tstcADirBackBS,tstcADirBackD,tstcADirBackDS,tstcADirBackP,tstcAIndBackB,tstcAIndBackBDS,tstcAIndBackS,tstcAIndBackBD,tstcAIndBackBS,tstcAIndBackD,tstcAIndBackDS,tstcAIndBackP,detOccurred,firstDetection,firstDetectionClin,firstDetectionTest,firstDetectionB,firstDetectionBDS,firstDetectionS,firstDetectionBD,firstDetectionBS,firstDetectionD,firstDetectionDS,firstDetectionP,firstDetectionClinB,firstDetectionClinBDS,firstDetectionClinS,firstDetectionClinBD,firstDetectionClinBS,firstDetectionClinD,firstDetectionClinDS,firstDetectionClinP,firstDetectionTestB,firstDetectionTestBDS,firstDetectionTestS,firstDetectionTestBD,firstDetectionTestBS,firstDetectionTestD,firstDetectionTestDS,firstDetectionTestP,lastDetection,lastDetectionClin,lastDetectionTest,lastDetectionB,lastDetectionBDS,lastDetectionS,lastDetectionBD,lastDetectionBS,lastDetectionD,lastDetectionDS,lastDetectionP,lastDetectionClinB,lastDetectionClinBDS,lastDetectionClinS,lastDetectionClinBD,lastDetectionClinBS,lastDetectionClinD,lastDetectionClinDS,lastDetectionClinP,lastDetectionTestB,lastDetectionTestBDS,lastDetectionTestS,lastDetectionTestBD,lastDetectionTestBS,lastDetectionTestD,lastDetectionTestDS,lastDetectionTestP,detnUAll,detnUClin,detnUTest,detnUB,detnUBDS,detnUS,detnUBD,detnUBS,detnUD,detnUDS,detnUP,detnUClinB,detnUClinBDS,detnUClinS,detnUClinBD,detnUClinBS,detnUClinD,detnUClinDS,detnUClinP,detnUTestB,detnUTestBDS,detnUTestS,detnUTestBD,detnUTestBS,detnUTestD,detnUTestDS,detnUTestP,detnAAll,detnAClin,detnATest,detnAB,detnABDS,detnAS,detnABD,detnABS,detnAD,detnADS,detnAP,detnAClinB,detnAClinBDS,detnAClinS,detnAClinBD,detnAClinBS,detnAClinD,detnAClinDS,detnAClinP,detnATestB,detnATestBDS,detnATestS,detnATestBD,detnATestBS,detnATestD,detnATestDS,detnATestP,detcUAll,detcUClin,detcUTest,detcUB,detcUBDS,detcUS,detcUBD,detcUBS,detcUD,detcUDS,detcUP,detcUClinB,detcUClinBDS,detcUClinS,detcUClinBD,detcUClinBS,detcUClinD,detcUClinDS,detcUClinP,detcUTestB,detcUTestBDS,detcUTestS,detcUTestBD,detcUTestBS,detcUTestD,detcUTestDS,detcUTestP,detcUqAll,detcAAll,detcAClin,detcATest,detcAB,detcABDS,detcAS,detcABD,detcABS,detcAD,detcADS,detcAP,detcAClinB,detcAClinBDS,detcAClinS,detcAClinBD,detcAClinBS,detcAClinD,detcAClinDS,detcAClinP,detcATestB,detcATestBDS,detcATestS,detcATestBD,detcATestBS,detcATestD,detcATestDS,detcATestP,expnUAll,expnUDir,expnUInd,expnUAir,expnUB,expnUBDS,expnUS,expnUBD,expnUBS,expnUD,expnUDS,expnUP,expnUDirB,expnUDirBDS,expnUDirS,expnUDirBD,expnUDirBS,expnUDirD,expnUDirDS,expnUDirP,expnUIndB,expnUIndBDS,expnUIndS,expnUIndBD,expnUIndBS,expnUIndD,expnUIndDS,expnUIndP,expnUAirB,expnUAirBDS,expnUAirS,expnUAirBD,expnUAirBS,expnUAirD,expnUAirDS,expnUAirP,expcUAll,expcUDir,expcUInd,expcUAir,expcUB,expcUBDS,expcUS,expcUBD,expcUBS,expcUD,expcUDS,expcUP,expcUDirB,expcUDirBDS,expcUDirS,expcUDirBD,expcUDirBS,expcUDirD,expcUDirDS,expcUDirP,expcUIndB,expcUIndBDS,expcUIndS,expcUIndBD,expcUIndBS,expcUIndD,expcUIndDS,expcUIndP,expcUAirB,expcUAirBDS,expcUAirS,expcUAirBD,expcUAirBS,expcUAirD,expcUAirDS,expcUAirP,expnAAll,expnADir,expnAInd,expnAAir,expnAB,expnABDS,expnAS,expnABD,expnABS,expnAD,expnADS,expnAP,expnADirB,expnADirBDS,expnADirS,expnADirBD,expnADirBS,expnADirD,expnADirDS,expnADirP,expnAIndB,expnAIndBDS,expnAIndS,expnAIndBD,expnAIndBS,expnAIndD,expnAIndDS,expnAIndP,expnAAirB,expnAAirBDS,expnAAirS,expnAAirBD,expnAAirBS,expnAAirD,expnAAirDS,expnAAirP,expcAAll,expcADir,expcAInd,expcAAir,expcAB,expcABDS,expcAS,expcABD,expcABS,expcAD,expcADS,expcAP,expcADirB,expcADirBDS,expcADirS,expcADirBD,expcADirBS,expcADirD,expcADirDS,expcADirP,expcAIndB,expcAIndBDS,expcAIndS,expcAIndBD,expcAIndBS,expcAIndD,expcAIndDS,expcAIndP,expcAAirB,expcAAirBDS,expcAAirS,expcAAirBD,expcAAirBS,expcAAirD,expcAAirDS,expcAAirP,adqnUAll,adqcUAll,exmnUAll,exmnURing,exmnUDirFwd,exmnUIndFwd,exmnUDirBack,exmnUIndBack,exmnUDet,exmnUB,exmnUBDS,exmnUS,exmnUBD,exmnUBS,exmnUD,exmnUDS,exmnUP,exmnURingB,exmnURingBDS,exmnURingS,exmnURingBD,exmnURingBS,exmnURingD,exmnURingDS,exmnURingP,exmnUDirFwdB,exmnUDirFwdBDS,exmnUDirFwdS,exmnUDirFwdBD,exmnUDirFwdBS,exmnUDirFwdD,exmnUDirFwdDS,exmnUDirFwdP,exmnUIndFwdB,exmnUIndFwdBDS,exmnUIndFwdS,exmnUIndFwdBD,exmnUIndFwdBS,exmnUIndFwdD,exmnUIndFwdDS,exmnUIndFwdP,exmnUDirBackB,exmnUDirBackBDS,exmnUDirBackS,exmnUDirBackBD,exmnUDirBackBS,exmnUDirBackD,exmnUDirBackDS,exmnUDirBackP,exmnUIndBackB,exmnUIndBackBDS,exmnUIndBackS,exmnUIndBackBD,exmnUIndBackBS,exmnUIndBackD,exmnUIndBackDS,exmnUIndBackP,exmnUDetB,exmnUDetBDS,exmnUDetS,exmnUDetBD,exmnUDetBS,exmnUDetD,exmnUDetDS,exmnUDetP,exmnAAll,exmnARing,exmnADirFwd,exmnAIndFwd,exmnADirBack,exmnAIndBack,exmnADet,exmnAB,exmnABDS,exmnAS,exmnABD,exmnABS,exmnAD,exmnADS,exmnAP,exmnARingB,exmnARingBDS,exmnARingS,exmnARingBD,exmnARingBS,exmnARingD,exmnARingDS,exmnARingP,exmnADirFwdB,exmnADirFwdBDS,exmnADirFwdS,exmnADirFwdBD,exmnADirFwdBS,exmnADirFwdD,exmnADirFwdDS,exmnADirFwdP,exmnAIndFwdB,exmnAIndFwdBDS,exmnAIndFwdS,exmnAIndFwdBD,exmnAIndFwdBS,exmnAIndFwdD,exmnAIndFwdDS,exmnAIndFwdP,exmnADirBackB,exmnADirBackBDS,exmnADirBackS,exmnADirBackBD,exmnADirBackBS,exmnADirBackD,exmnADirBackDS,exmnADirBackP,exmnAIndBackB,exmnAIndBackBDS,exmnAIndBackS,exmnAIndBackBD,exmnAIndBackBS,exmnAIndBackD,exmnAIndBackDS,exmnAIndBackP,exmnADetB,exmnADetBDS,exmnADetS,exmnADetBD,exmnADetBS,exmnADetD,exmnADetDS,exmnADetP,exmcUAll,exmcURing,exmcUDirFwd,exmcUIndFwd,exmcUDirBack,exmcUIndBack,exmcUDet,exmcUB,exmcUBDS,exmcUS,exmcUBD,exmcUBS,exmcUD,exmcUDS,exmcUP,exmcURingB,exmcURingBDS,exmcURingS,exmcURingBD,exmcURingBS,exmcURingD,exmcURingDS,exmcURingP,exmcUDirFwdB,exmcUDirFwdBDS,exmcUDirFwdS,exmcUDirFwdBD,exmcUDirFwdBS,exmcUDirFwdD,exmcUDirFwdDS,exmcUDirFwdP,exmcUIndFwdB,exmcUIndFwdBDS,exmcUIndFwdS,exmcUIndFwdBD,exmcUIndFwdBS,exmcUIndFwdD,exmcUIndFwdDS,exmcUIndFwdP,exmcUDirBackB,exmcUDirBackBDS,exmcUDirBackS,exmcUDirBackBD,exmcUDirBackBS,exmcUDirBackD,exmcUDirBackDS,exmcUDirBackP,exmcUIndBackB,exmcUIndBackBDS,exmcUIndBackS,exmcUIndBackBD,exmcUIndBackBS,exmcUIndBackD,exmcUIndBackDS,exmcUIndBackP,exmcUDetB,exmcUDetBDS,exmcUDetS,exmcUDetBD,exmcUDetBS,exmcUDetD,exmcUDetDS,exmcUDetP,exmcAAll,exmcARing,exmcADirFwd,exmcAIndFwd,exmcADirBack,exmcAIndBack,exmcADet,exmcAB,exmcABDS,exmcAS,exmcABD,exmcABS,exmcAD,exmcADS,exmcAP,exmcARingB,exmcARingBDS,exmcARingS,exmcARingBD,exmcARingBS,exmcARingD,exmcARingDS,exmcARingP,exmcADirFwdB,exmcADirFwdBDS,exmcADirFwdS,exmcADirFwdBD,exmcADirFwdBS,exmcADirFwdD,exmcADirFwdDS,exmcADirFwdP,exmcAIndFwdB,exmcAIndFwdBDS,exmcAIndFwdS,exmcAIndFwdBD,exmcAIndFwdBS,exmcAIndFwdD,exmcAIndFwdDS,exmcAIndFwdP,exmcADirBackB,exmcADirBackBDS,exmcADirBackS,exmcADirBackBD,exmcADirBackBS,exmcADirBackD,exmcADirBackDS,exmcADirBackP,exmcAIndBackB,exmcAIndBackBDS,exmcAIndBackS,exmcAIndBackBD,exmcAIndBackBS,exmcAIndBackD,exmcAIndBackDS,exmcAIndBackP,exmcADetB,exmcADetBDS,exmcADetS,exmcADetBD,exmcADetBS,exmcADetD,exmcADetDS,exmcADetP".lower()

# <codecell>


