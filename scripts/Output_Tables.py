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

headers = "Run,Day,outbreakDuration,infnUAll,infnUDir,infnUInd,infnUAir,infnUIni,infnUCattle,infnU_Dogsheep_,infnUSwine,infnU_Bulldog_,infnU_Brownsheep_,infnU_Doe_,infnU_Pig_,infnUDirCattle,infnUDir_Dogsheep_,infnUDirSwine,infnUDir_Bulldog_,infnUDir_Brownsheep_,infnUDir_Doe_,infnUDir_Pig_,infnUIndCattle,infnUInd_Dogsheep_,infnUIndSwine,infnUInd_Bulldog_,infnUInd_Brownsheep_,infnUInd_Doe_,infnUInd_Pig_,infnUAirCattle,infnUAir_Dogsheep_,infnUAirSwine,infnUAir_Bulldog_,infnUAir_Brownsheep_,infnUAir_Doe_,infnUAir_Pig_,infnUIniCattle,infnUIni_Dogsheep_,infnUIniSwine,infnUIni_Bulldog_,infnUIni_Brownsheep_,infnUIni_Doe_,infnUIni_Pig_,infcUAll,infcUDir,infcUInd,infcUAir,infcUIni,infcUCattle,infcU_Dogsheep_,infcUSwine,infcU_Bulldog_,infcU_Brownsheep_,infcU_Doe_,infcU_Pig_,infcUDirCattle,infcUDir_Dogsheep_,infcUDirSwine,infcUDir_Bulldog_,infcUDir_Brownsheep_,infcUDir_Doe_,infcUDir_Pig_,infcUIndCattle,infcUInd_Dogsheep_,infcUIndSwine,infcUInd_Bulldog_,infcUInd_Brownsheep_,infcUInd_Doe_,infcUInd_Pig_,infcUAirCattle,infcUAir_Dogsheep_,infcUAirSwine,infcUAir_Bulldog_,infcUAir_Brownsheep_,infcUAir_Doe_,infcUAir_Pig_,infcUIniCattle,infcUIni_Dogsheep_,infcUIniSwine,infcUIni_Bulldog_,infcUIni_Brownsheep_,infcUIni_Doe_,infcUIni_Pig_,infnAAll,infnADir,infnAInd,infnAAir,infnAIni,infnACattle,infnA_Dogsheep_,infnASwine,infnA_Bulldog_,infnA_Brownsheep_,infnA_Doe_,infnA_Pig_,infnADirCattle,infnADir_Dogsheep_,infnADirSwine,infnADir_Bulldog_,infnADir_Brownsheep_,infnADir_Doe_,infnADir_Pig_,infnAIndCattle,infnAInd_Dogsheep_,infnAIndSwine,infnAInd_Bulldog_,infnAInd_Brownsheep_,infnAInd_Doe_,infnAInd_Pig_,infnAAirCattle,infnAAir_Dogsheep_,infnAAirSwine,infnAAir_Bulldog_,infnAAir_Brownsheep_,infnAAir_Doe_,infnAAir_Pig_,infnAIniCattle,infnAIni_Dogsheep_,infnAIniSwine,infnAIni_Bulldog_,infnAIni_Brownsheep_,infnAIni_Doe_,infnAIni_Pig_,infcAAll,infcADir,infcAInd,infcAAir,infcAIni,infcACattle,infcA_Dogsheep_,infcASwine,infcA_Bulldog_,infcA_Brownsheep_,infcA_Doe_,infcA_Pig_,infcADirCattle,infcADir_Dogsheep_,infcADirSwine,infcADir_Bulldog_,infcADir_Brownsheep_,infcADir_Doe_,infcADir_Pig_,infcAIndCattle,infcAInd_Dogsheep_,infcAIndSwine,infcAInd_Bulldog_,infcAInd_Brownsheep_,infcAInd_Doe_,infcAInd_Pig_,infcAAirCattle,infcAAir_Dogsheep_,infcAAirSwine,infcAAir_Bulldog_,infcAAir_Brownsheep_,infcAAir_Doe_,infcAAir_Pig_,infcAIniCattle,infcAIni_Dogsheep_,infcAIniSwine,infcAIni_Bulldog_,infcAIni_Brownsheep_,infcAIni_Doe_,infcAIni_Pig_,firstDetUInfAll,firstDetAInfAll,ratio,expnUAll,expnUDir,expnUInd,expnUAir,expnUCattle,expnU_Dogsheep_,expnUSwine,expnU_Bulldog_,expnU_Brownsheep_,expnU_Doe_,expnU_Pig_,expnUDirCattle,expnUDir_Dogsheep_,expnUDirSwine,expnUDir_Bulldog_,expnUDir_Brownsheep_,expnUDir_Doe_,expnUDir_Pig_,expnUIndCattle,expnUInd_Dogsheep_,expnUIndSwine,expnUInd_Bulldog_,expnUInd_Brownsheep_,expnUInd_Doe_,expnUInd_Pig_,expnUAirCattle,expnUAir_Dogsheep_,expnUAirSwine,expnUAir_Bulldog_,expnUAir_Brownsheep_,expnUAir_Doe_,expnUAir_Pig_,expcUAll,expcUDir,expcUInd,expcUAir,expcUCattle,expcU_Dogsheep_,expcUSwine,expcU_Bulldog_,expcU_Brownsheep_,expcU_Doe_,expcU_Pig_,expcUDirCattle,expcUDir_Dogsheep_,expcUDirSwine,expcUDir_Bulldog_,expcUDir_Brownsheep_,expcUDir_Doe_,expcUDir_Pig_,expcUIndCattle,expcUInd_Dogsheep_,expcUIndSwine,expcUInd_Bulldog_,expcUInd_Brownsheep_,expcUInd_Doe_,expcUInd_Pig_,expcUAirCattle,expcUAir_Dogsheep_,expcUAirSwine,expcUAir_Bulldog_,expcUAir_Brownsheep_,expcUAir_Doe_,expcUAir_Pig_,expnAAll,expnADir,expnAInd,expnAAir,expnACattle,expnA_Dogsheep_,expnASwine,expnA_Bulldog_,expnA_Brownsheep_,expnA_Doe_,expnA_Pig_,expnADirCattle,expnADir_Dogsheep_,expnADirSwine,expnADir_Bulldog_,expnADir_Brownsheep_,expnADir_Doe_,expnADir_Pig_,expnAIndCattle,expnAInd_Dogsheep_,expnAIndSwine,expnAInd_Bulldog_,expnAInd_Brownsheep_,expnAInd_Doe_,expnAInd_Pig_,expnAAirCattle,expnAAir_Dogsheep_,expnAAirSwine,expnAAir_Bulldog_,expnAAir_Brownsheep_,expnAAir_Doe_,expnAAir_Pig_,expcAAll,expcADir,expcAInd,expcAAir,expcACattle,expcA_Dogsheep_,expcASwine,expcA_Bulldog_,expcA_Brownsheep_,expcA_Doe_,expcA_Pig_,expcADirCattle,expcADir_Dogsheep_,expcADirSwine,expcADir_Bulldog_,expcADir_Brownsheep_,expcADir_Doe_,expcADir_Pig_,expcAIndCattle,expcAInd_Dogsheep_,expcAIndSwine,expcAInd_Bulldog_,expcAInd_Brownsheep_,expcAInd_Doe_,expcAInd_Pig_,expcAAirCattle,expcAAir_Dogsheep_,expcAAirSwine,expcAAir_Bulldog_,expcAAir_Brownsheep_,expcAAir_Doe_,expcAAir_Pig_,adqnUAll,adqcUAll,vacwUAll,vacwUCattle,vacwU_Dogsheep_,vacwUSwine,vacwU_Bulldog_,vacwU_Brownsheep_,vacwU_Doe_,vacwU_Pig_,vacwAAll,vacwACattle,vacwA_Dogsheep_,vacwASwine,vacwA_Bulldog_,vacwA_Brownsheep_,vacwA_Doe_,vacwA_Pig_,vacwUMax,vacwUMaxDay,vacwAMax,vacwAMaxDay,vacwUTimeMax,vacwUTimeAvg,vacwUDaysInQueue,vacwADaysInQueue,zoneAreaHighRisk,zoneAreaMediumRisk,maxZoneAreaHighRisk,maxZoneAreaMediumRisk,maxZoneAreaDayHighRisk,maxZoneAreaDayMediumRisk,finalZoneAreaHighRisk,finalZoneAreaMediumRisk,zonePerimeterHighRisk,zonePerimeterMediumRisk,maxZonePerimeterHighRisk,maxZonePerimeterMediumRisk,maxZonePerimeterDayHighRisk,maxZonePerimeterDayMediumRisk,finalZonePerimeterHighRisk,finalZonePerimeterMediumRisk,num-separate-areasHighRisk,num-separate-areasMediumRisk,unitsInZoneHighRisk,unitsInZoneMediumRisk,unitsInZoneBackground,unitsInZoneHighRiskCattle,unitsInZoneHighRisk_Dogsheep_,unitsInZoneHighRiskSwine,unitsInZoneHighRisk_Bulldog_,unitsInZoneHighRisk_Brownsheep_,unitsInZoneHighRisk_Doe_,unitsInZoneHighRisk_Pig_,unitsInZoneMediumRiskCattle,unitsInZoneMediumRisk_Dogsheep_,unitsInZoneMediumRiskSwine,unitsInZoneMediumRisk_Bulldog_,unitsInZoneMediumRisk_Brownsheep_,unitsInZoneMediumRisk_Doe_,unitsInZoneMediumRisk_Pig_,unitsInZoneBackgroundCattle,unitsInZoneBackground_Dogsheep_,unitsInZoneBackgroundSwine,unitsInZoneBackground_Bulldog_,unitsInZoneBackground_Brownsheep_,unitsInZoneBackground_Doe_,unitsInZoneBackground_Pig_,unitDaysInZoneHighRisk,unitDaysInZoneMediumRisk,unitDaysInZoneBackground,unitDaysInZoneHighRiskCattle,unitDaysInZoneHighRisk_Dogsheep_,unitDaysInZoneHighRiskSwine,unitDaysInZoneHighRisk_Bulldog_,unitDaysInZoneHighRisk_Brownsheep_,unitDaysInZoneHighRisk_Doe_,unitDaysInZoneHighRisk_Pig_,unitDaysInZoneMediumRiskCattle,unitDaysInZoneMediumRisk_Dogsheep_,unitDaysInZoneMediumRiskSwine,unitDaysInZoneMediumRisk_Bulldog_,unitDaysInZoneMediumRisk_Brownsheep_,unitDaysInZoneMediumRisk_Doe_,unitDaysInZoneMediumRisk_Pig_,unitDaysInZoneBackgroundCattle,unitDaysInZoneBackground_Dogsheep_,unitDaysInZoneBackgroundSwine,unitDaysInZoneBackground_Bulldog_,unitDaysInZoneBackground_Brownsheep_,unitDaysInZoneBackground_Doe_,unitDaysInZoneBackground_Pig_,animalDaysInZoneHighRisk,animalDaysInZoneMediumRisk,animalDaysInZoneBackground,animalDaysInZoneHighRiskCattle,animalDaysInZoneHighRisk_Dogsheep_,animalDaysInZoneHighRiskSwine,animalDaysInZoneHighRisk_Bulldog_,animalDaysInZoneHighRisk_Brownsheep_,animalDaysInZoneHighRisk_Doe_,animalDaysInZoneHighRisk_Pig_,animalDaysInZoneMediumRiskCattle,animalDaysInZoneMediumRisk_Dogsheep_,animalDaysInZoneMediumRiskSwine,animalDaysInZoneMediumRisk_Bulldog_,animalDaysInZoneMediumRisk_Brownsheep_,animalDaysInZoneMediumRisk_Doe_,animalDaysInZoneMediumRisk_Pig_,animalDaysInZoneBackgroundCattle,animalDaysInZoneBackground_Dogsheep_,animalDaysInZoneBackgroundSwine,animalDaysInZoneBackground_Bulldog_,animalDaysInZoneBackground_Brownsheep_,animalDaysInZoneBackground_Doe_,animalDaysInZoneBackground_Pig_,deswUAll,deswUCattle,deswU_Dogsheep_,deswUSwine,deswU_Bulldog_,deswU_Brownsheep_,deswU_Doe_,deswU_Pig_,deswAAll,deswACattle,deswA_Dogsheep_,deswASwine,deswA_Bulldog_,deswA_Brownsheep_,deswA_Doe_,deswA_Pig_,deswUMax,deswUMaxDay,deswAMax,deswAMaxDay,deswUTimeMax,deswUTimeAvg,deswUDaysInQueue,deswADaysInQueue,destrOccurred,firstDestruction,firstDestructionUnsp,firstDestructionRing,firstDestructionDirFwd,firstDestructionIndFwd,firstDestructionDirBack,firstDestructionIndBack,firstDestructionDet,firstDestructionIni,firstDestructionCattle,firstDestruction_Dogsheep_,firstDestructionSwine,firstDestruction_Bulldog_,firstDestruction_Brownsheep_,firstDestruction_Doe_,firstDestruction_Pig_,firstDestructionUnspCattle,firstDestructionUnsp_Dogsheep_,firstDestructionUnspSwine,firstDestructionUnsp_Bulldog_,firstDestructionUnsp_Brownsheep_,firstDestructionUnsp_Doe_,firstDestructionUnsp_Pig_,firstDestructionRingCattle,firstDestructionRing_Dogsheep_,firstDestructionRingSwine,firstDestructionRing_Bulldog_,firstDestructionRing_Brownsheep_,firstDestructionRing_Doe_,firstDestructionRing_Pig_,firstDestructionDirFwdCattle,firstDestructionDirFwd_Dogsheep_,firstDestructionDirFwdSwine,firstDestructionDirFwd_Bulldog_,firstDestructionDirFwd_Brownsheep_,firstDestructionDirFwd_Doe_,firstDestructionDirFwd_Pig_,firstDestructionIndFwdCattle,firstDestructionIndFwd_Dogsheep_,firstDestructionIndFwdSwine,firstDestructionIndFwd_Bulldog_,firstDestructionIndFwd_Brownsheep_,firstDestructionIndFwd_Doe_,firstDestructionIndFwd_Pig_,firstDestructionDirBackCattle,firstDestructionDirBack_Dogsheep_,firstDestructionDirBackSwine,firstDestructionDirBack_Bulldog_,firstDestructionDirBack_Brownsheep_,firstDestructionDirBack_Doe_,firstDestructionDirBack_Pig_,firstDestructionIndBackCattle,firstDestructionIndBack_Dogsheep_,firstDestructionIndBackSwine,firstDestructionIndBack_Bulldog_,firstDestructionIndBack_Brownsheep_,firstDestructionIndBack_Doe_,firstDestructionIndBack_Pig_,firstDestructionDetCattle,firstDestructionDet_Dogsheep_,firstDestructionDetSwine,firstDestructionDet_Bulldog_,firstDestructionDet_Brownsheep_,firstDestructionDet_Doe_,firstDestructionDet_Pig_,firstDestructionIniCattle,firstDestructionIni_Dogsheep_,firstDestructionIniSwine,firstDestructionIni_Bulldog_,firstDestructionIni_Brownsheep_,firstDestructionIni_Doe_,firstDestructionIni_Pig_,desnUAll,desnUIni,desnUUnsp,desnURing,desnUDirFwd,desnUIndFwd,desnUDirBack,desnUIndBack,desnUDet,desnUCattle,desnU_Dogsheep_,desnUSwine,desnU_Bulldog_,desnU_Brownsheep_,desnU_Doe_,desnU_Pig_,desnUIniCattle,desnUIni_Dogsheep_,desnUIniSwine,desnUIni_Bulldog_,desnUIni_Brownsheep_,desnUIni_Doe_,desnUIni_Pig_,desnUUnspCattle,desnUUnsp_Dogsheep_,desnUUnspSwine,desnUUnsp_Bulldog_,desnUUnsp_Brownsheep_,desnUUnsp_Doe_,desnUUnsp_Pig_,desnURingCattle,desnURing_Dogsheep_,desnURingSwine,desnURing_Bulldog_,desnURing_Brownsheep_,desnURing_Doe_,desnURing_Pig_,desnUDirFwdCattle,desnUDirFwd_Dogsheep_,desnUDirFwdSwine,desnUDirFwd_Bulldog_,desnUDirFwd_Brownsheep_,desnUDirFwd_Doe_,desnUDirFwd_Pig_,desnUIndFwdCattle,desnUIndFwd_Dogsheep_,desnUIndFwdSwine,desnUIndFwd_Bulldog_,desnUIndFwd_Brownsheep_,desnUIndFwd_Doe_,desnUIndFwd_Pig_,desnUDirBackCattle,desnUDirBack_Dogsheep_,desnUDirBackSwine,desnUDirBack_Bulldog_,desnUDirBack_Brownsheep_,desnUDirBack_Doe_,desnUDirBack_Pig_,desnUIndBackCattle,desnUIndBack_Dogsheep_,desnUIndBackSwine,desnUIndBack_Bulldog_,desnUIndBack_Brownsheep_,desnUIndBack_Doe_,desnUIndBack_Pig_,desnUDetCattle,desnUDet_Dogsheep_,desnUDetSwine,desnUDet_Bulldog_,desnUDet_Brownsheep_,desnUDet_Doe_,desnUDet_Pig_,descUAll,descUIni,descUUnsp,descURing,descUDirFwd,descUIndFwd,descUDirBack,descUIndBack,descUDet,descUCattle,descU_Dogsheep_,descUSwine,descU_Bulldog_,descU_Brownsheep_,descU_Doe_,descU_Pig_,descUIniCattle,descUIni_Dogsheep_,descUIniSwine,descUIni_Bulldog_,descUIni_Brownsheep_,descUIni_Doe_,descUIni_Pig_,descUUnspCattle,descUUnsp_Dogsheep_,descUUnspSwine,descUUnsp_Bulldog_,descUUnsp_Brownsheep_,descUUnsp_Doe_,descUUnsp_Pig_,descURingCattle,descURing_Dogsheep_,descURingSwine,descURing_Bulldog_,descURing_Brownsheep_,descURing_Doe_,descURing_Pig_,descUDirFwdCattle,descUDirFwd_Dogsheep_,descUDirFwdSwine,descUDirFwd_Bulldog_,descUDirFwd_Brownsheep_,descUDirFwd_Doe_,descUDirFwd_Pig_,descUIndFwdCattle,descUIndFwd_Dogsheep_,descUIndFwdSwine,descUIndFwd_Bulldog_,descUIndFwd_Brownsheep_,descUIndFwd_Doe_,descUIndFwd_Pig_,descUDirBackCattle,descUDirBack_Dogsheep_,descUDirBackSwine,descUDirBack_Bulldog_,descUDirBack_Brownsheep_,descUDirBack_Doe_,descUDirBack_Pig_,descUIndBackCattle,descUIndBack_Dogsheep_,descUIndBackSwine,descUIndBack_Bulldog_,descUIndBack_Brownsheep_,descUIndBack_Doe_,descUIndBack_Pig_,descUDetCattle,descUDet_Dogsheep_,descUDetSwine,descUDet_Bulldog_,descUDet_Brownsheep_,descUDet_Doe_,descUDet_Pig_,desnAAll,desnAIni,desnAUnsp,desnARing,desnADirFwd,desnAIndFwd,desnADirBack,desnAIndBack,desnADet,desnACattle,desnA_Dogsheep_,desnASwine,desnA_Bulldog_,desnA_Brownsheep_,desnA_Doe_,desnA_Pig_,desnAIniCattle,desnAIni_Dogsheep_,desnAIniSwine,desnAIni_Bulldog_,desnAIni_Brownsheep_,desnAIni_Doe_,desnAIni_Pig_,desnAUnspCattle,desnAUnsp_Dogsheep_,desnAUnspSwine,desnAUnsp_Bulldog_,desnAUnsp_Brownsheep_,desnAUnsp_Doe_,desnAUnsp_Pig_,desnARingCattle,desnARing_Dogsheep_,desnARingSwine,desnARing_Bulldog_,desnARing_Brownsheep_,desnARing_Doe_,desnARing_Pig_,desnADirFwdCattle,desnADirFwd_Dogsheep_,desnADirFwdSwine,desnADirFwd_Bulldog_,desnADirFwd_Brownsheep_,desnADirFwd_Doe_,desnADirFwd_Pig_,desnAIndFwdCattle,desnAIndFwd_Dogsheep_,desnAIndFwdSwine,desnAIndFwd_Bulldog_,desnAIndFwd_Brownsheep_,desnAIndFwd_Doe_,desnAIndFwd_Pig_,desnADirBackCattle,desnADirBack_Dogsheep_,desnADirBackSwine,desnADirBack_Bulldog_,desnADirBack_Brownsheep_,desnADirBack_Doe_,desnADirBack_Pig_,desnAIndBackCattle,desnAIndBack_Dogsheep_,desnAIndBackSwine,desnAIndBack_Bulldog_,desnAIndBack_Brownsheep_,desnAIndBack_Doe_,desnAIndBack_Pig_,desnADetCattle,desnADet_Dogsheep_,desnADetSwine,desnADet_Bulldog_,desnADet_Brownsheep_,desnADet_Doe_,desnADet_Pig_,descAAll,descAIni,descAUnsp,descARing,descADirFwd,descAIndFwd,descADirBack,descAIndBack,descADet,descACattle,descA_Dogsheep_,descASwine,descA_Bulldog_,descA_Brownsheep_,descA_Doe_,descA_Pig_,descAIniCattle,descAIni_Dogsheep_,descAIniSwine,descAIni_Bulldog_,descAIni_Brownsheep_,descAIni_Doe_,descAIni_Pig_,descAUnspCattle,descAUnsp_Dogsheep_,descAUnspSwine,descAUnsp_Bulldog_,descAUnsp_Brownsheep_,descAUnsp_Doe_,descAUnsp_Pig_,descARingCattle,descARing_Dogsheep_,descARingSwine,descARing_Bulldog_,descARing_Brownsheep_,descARing_Doe_,descARing_Pig_,descADirFwdCattle,descADirFwd_Dogsheep_,descADirFwdSwine,descADirFwd_Bulldog_,descADirFwd_Brownsheep_,descADirFwd_Doe_,descADirFwd_Pig_,descAIndFwdCattle,descAIndFwd_Dogsheep_,descAIndFwdSwine,descAIndFwd_Bulldog_,descAIndFwd_Brownsheep_,descAIndFwd_Doe_,descAIndFwd_Pig_,descADirBackCattle,descADirBack_Dogsheep_,descADirBackSwine,descADirBack_Bulldog_,descADirBack_Brownsheep_,descADirBack_Doe_,descADirBack_Pig_,descAIndBackCattle,descAIndBack_Dogsheep_,descAIndBackSwine,descAIndBack_Bulldog_,descAIndBack_Brownsheep_,descAIndBack_Doe_,descAIndBack_Pig_,descADetCattle,descADet_Dogsheep_,descADetSwine,descADet_Bulldog_,descADet_Brownsheep_,descADet_Doe_,descADet_Pig_,trnUAllp,trnUDirp,trnUIndp,trnUCattlep,trnU_Dogsheep_p,trnUSwinep,trnU_Bulldog_p,trnU_Brownsheep_p,trnU_Doe_p,trnU_Pig_p,trnUDirCattlep,trnUDir_Dogsheep_p,trnUDirSwinep,trnUDir_Bulldog_p,trnUDir_Brownsheep_p,trnUDir_Doe_p,trnUDir_Pig_p,trnUIndCattlep,trnUInd_Dogsheep_p,trnUIndSwinep,trnUInd_Bulldog_p,trnUInd_Brownsheep_p,trnUInd_Doe_p,trnUInd_Pig_p,trcUAllp,trcUDirp,trcUIndp,trcUCattlep,trcU_Dogsheep_p,trcUSwinep,trcU_Bulldog_p,trcU_Brownsheep_p,trcU_Doe_p,trcU_Pig_p,trcUDirCattlep,trcUDir_Dogsheep_p,trcUDirSwinep,trcUDir_Bulldog_p,trcUDir_Brownsheep_p,trcUDir_Doe_p,trcUDir_Pig_p,trcUIndCattlep,trcUInd_Dogsheep_p,trcUIndSwinep,trcUInd_Bulldog_p,trcUInd_Brownsheep_p,trcUInd_Doe_p,trcUInd_Pig_p,trnUAll,trnUDir,trnUInd,trnUCattle,trnU_Dogsheep_,trnUSwine,trnU_Bulldog_,trnU_Brownsheep_,trnU_Doe_,trnU_Pig_,trnUDirCattle,trnUDir_Dogsheep_,trnUDirSwine,trnUDir_Bulldog_,trnUDir_Brownsheep_,trnUDir_Doe_,trnUDir_Pig_,trnUIndCattle,trnUInd_Dogsheep_,trnUIndSwine,trnUInd_Bulldog_,trnUInd_Brownsheep_,trnUInd_Doe_,trnUInd_Pig_,trcUAll,trcUDir,trcUInd,trcUCattle,trcU_Dogsheep_,trcUSwine,trcU_Bulldog_,trcU_Brownsheep_,trcU_Doe_,trcU_Pig_,trcUDirCattle,trcUDir_Dogsheep_,trcUDirSwine,trcUDir_Bulldog_,trcUDir_Brownsheep_,trcUDir_Doe_,trcUDir_Pig_,trcUIndCattle,trcUInd_Dogsheep_,trcUIndSwine,trcUInd_Bulldog_,trcUInd_Brownsheep_,trcUInd_Doe_,trcUInd_Pig_,trnAAllp,trnADirp,trnAIndp,trnACattlep,trnA_Dogsheep_p,trnASwinep,trnA_Bulldog_p,trnA_Brownsheep_p,trnA_Doe_p,trnA_Pig_p,trnADirCattlep,trnADir_Dogsheep_p,trnADirSwinep,trnADir_Bulldog_p,trnADir_Brownsheep_p,trnADir_Doe_p,trnADir_Pig_p,trnAIndCattlep,trnAInd_Dogsheep_p,trnAIndSwinep,trnAInd_Bulldog_p,trnAInd_Brownsheep_p,trnAInd_Doe_p,trnAInd_Pig_p,trcAAllp,trcADirp,trcAIndp,trcACattlep,trcA_Dogsheep_p,trcASwinep,trcA_Bulldog_p,trcA_Brownsheep_p,trcA_Doe_p,trcA_Pig_p,trcADirCattlep,trcADir_Dogsheep_p,trcADirSwinep,trcADir_Bulldog_p,trcADir_Brownsheep_p,trcADir_Doe_p,trcADir_Pig_p,trcAIndCattlep,trcAInd_Dogsheep_p,trcAIndSwinep,trcAInd_Bulldog_p,trcAInd_Brownsheep_p,trcAInd_Doe_p,trcAInd_Pig_p,trnAAll,trnADir,trnAInd,trnACattle,trnA_Dogsheep_,trnASwine,trnA_Bulldog_,trnA_Brownsheep_,trnA_Doe_,trnA_Pig_,trnADirCattle,trnADir_Dogsheep_,trnADirSwine,trnADir_Bulldog_,trnADir_Brownsheep_,trnADir_Doe_,trnADir_Pig_,trnAIndCattle,trnAInd_Dogsheep_,trnAIndSwine,trnAInd_Bulldog_,trnAInd_Brownsheep_,trnAInd_Doe_,trnAInd_Pig_,trcAAll,trcADir,trcAInd,trcACattle,trcA_Dogsheep_,trcASwine,trcA_Bulldog_,trcA_Brownsheep_,trcA_Doe_,trcA_Pig_,trcADirCattle,trcADir_Dogsheep_,trcADirSwine,trcADir_Bulldog_,trcADir_Brownsheep_,trcADir_Doe_,trcADir_Pig_,trcAIndCattle,trcAInd_Dogsheep_,trcAIndSwine,trcAInd_Bulldog_,trcAInd_Brownsheep_,trcAInd_Doe_,trcAInd_Pig_,detOccurred,firstDetection,firstDetectionClin,firstDetectionTest,firstDetectionCattle,firstDetection_Dogsheep_,firstDetectionSwine,firstDetection_Bulldog_,firstDetection_Brownsheep_,firstDetection_Doe_,firstDetection_Pig_,firstDetectionClinCattle,firstDetectionClin_Dogsheep_,firstDetectionClinSwine,firstDetectionClin_Bulldog_,firstDetectionClin_Brownsheep_,firstDetectionClin_Doe_,firstDetectionClin_Pig_,firstDetectionTestCattle,firstDetectionTest_Dogsheep_,firstDetectionTestSwine,firstDetectionTest_Bulldog_,firstDetectionTest_Brownsheep_,firstDetectionTest_Doe_,firstDetectionTest_Pig_,lastDetection,lastDetectionClin,lastDetectionTest,lastDetectionCattle,lastDetection_Dogsheep_,lastDetectionSwine,lastDetection_Bulldog_,lastDetection_Brownsheep_,lastDetection_Doe_,lastDetection_Pig_,lastDetectionClinCattle,lastDetectionClin_Dogsheep_,lastDetectionClinSwine,lastDetectionClin_Bulldog_,lastDetectionClin_Brownsheep_,lastDetectionClin_Doe_,lastDetectionClin_Pig_,lastDetectionTestCattle,lastDetectionTest_Dogsheep_,lastDetectionTestSwine,lastDetectionTest_Bulldog_,lastDetectionTest_Brownsheep_,lastDetectionTest_Doe_,lastDetectionTest_Pig_,detnUAll,detnUClin,detnUTest,detnUCattle,detnU_Dogsheep_,detnUSwine,detnU_Bulldog_,detnU_Brownsheep_,detnU_Doe_,detnU_Pig_,detnUClinCattle,detnUClin_Dogsheep_,detnUClinSwine,detnUClin_Bulldog_,detnUClin_Brownsheep_,detnUClin_Doe_,detnUClin_Pig_,detnUTestCattle,detnUTest_Dogsheep_,detnUTestSwine,detnUTest_Bulldog_,detnUTest_Brownsheep_,detnUTest_Doe_,detnUTest_Pig_,detnAAll,detnAClin,detnATest,detnACattle,detnA_Dogsheep_,detnASwine,detnA_Bulldog_,detnA_Brownsheep_,detnA_Doe_,detnA_Pig_,detnAClinCattle,detnAClin_Dogsheep_,detnAClinSwine,detnAClin_Bulldog_,detnAClin_Brownsheep_,detnAClin_Doe_,detnAClin_Pig_,detnATestCattle,detnATest_Dogsheep_,detnATestSwine,detnATest_Bulldog_,detnATest_Brownsheep_,detnATest_Doe_,detnATest_Pig_,detcUAll,detcUClin,detcUTest,detcUCattle,detcU_Dogsheep_,detcUSwine,detcU_Bulldog_,detcU_Brownsheep_,detcU_Doe_,detcU_Pig_,detcUClinCattle,detcUClin_Dogsheep_,detcUClinSwine,detcUClin_Bulldog_,detcUClin_Brownsheep_,detcUClin_Doe_,detcUClin_Pig_,detcUTestCattle,detcUTest_Dogsheep_,detcUTestSwine,detcUTest_Bulldog_,detcUTest_Brownsheep_,detcUTest_Doe_,detcUTest_Pig_,detcUqAll,detcAAll,detcAClin,detcATest,detcACattle,detcA_Dogsheep_,detcASwine,detcA_Bulldog_,detcA_Brownsheep_,detcA_Doe_,detcA_Pig_,detcAClinCattle,detcAClin_Dogsheep_,detcAClinSwine,detcAClin_Bulldog_,detcAClin_Brownsheep_,detcAClin_Doe_,detcAClin_Pig_,detcATestCattle,detcATest_Dogsheep_,detcATestSwine,detcATest_Bulldog_,detcATest_Brownsheep_,detcATest_Doe_,detcATest_Pig_,tsdUSusc,tsdULat,tsdUSubc,tsdUClin,tsdUNImm,tsdUVImm,tsdUDest,tsdUCattleSusc,tsdUCattleLat,tsdUCattleSubc,tsdUCattleClin,tsdUCattleNImm,tsdUCattleVImm,tsdUCattleDest,tsdU_Dogsheep_Susc,tsdU_Dogsheep_Lat,tsdU_Dogsheep_Subc,tsdU_Dogsheep_Clin,tsdU_Dogsheep_NImm,tsdU_Dogsheep_VImm,tsdU_Dogsheep_Dest,tsdUSwineSusc,tsdUSwineLat,tsdUSwineSubc,tsdUSwineClin,tsdUSwineNImm,tsdUSwineVImm,tsdUSwineDest,tsdU_Bulldog_Susc,tsdU_Bulldog_Lat,tsdU_Bulldog_Subc,tsdU_Bulldog_Clin,tsdU_Bulldog_NImm,tsdU_Bulldog_VImm,tsdU_Bulldog_Dest,tsdU_Brownsheep_Susc,tsdU_Brownsheep_Lat,tsdU_Brownsheep_Subc,tsdU_Brownsheep_Clin,tsdU_Brownsheep_NImm,tsdU_Brownsheep_VImm,tsdU_Brownsheep_Dest,tsdU_Doe_Susc,tsdU_Doe_Lat,tsdU_Doe_Subc,tsdU_Doe_Clin,tsdU_Doe_NImm,tsdU_Doe_VImm,tsdU_Doe_Dest,tsdU_Pig_Susc,tsdU_Pig_Lat,tsdU_Pig_Subc,tsdU_Pig_Clin,tsdU_Pig_NImm,tsdU_Pig_VImm,tsdU_Pig_Dest,tsdASusc,tsdALat,tsdASubc,tsdAClin,tsdANImm,tsdAVImm,tsdADest,tsdACattleSusc,tsdACattleLat,tsdACattleSubc,tsdACattleClin,tsdACattleNImm,tsdACattleVImm,tsdACattleDest,tsdA_Dogsheep_Susc,tsdA_Dogsheep_Lat,tsdA_Dogsheep_Subc,tsdA_Dogsheep_Clin,tsdA_Dogsheep_NImm,tsdA_Dogsheep_VImm,tsdA_Dogsheep_Dest,tsdASwineSusc,tsdASwineLat,tsdASwineSubc,tsdASwineClin,tsdASwineNImm,tsdASwineVImm,tsdASwineDest,tsdA_Bulldog_Susc,tsdA_Bulldog_Lat,tsdA_Bulldog_Subc,tsdA_Bulldog_Clin,tsdA_Bulldog_NImm,tsdA_Bulldog_VImm,tsdA_Bulldog_Dest,tsdA_Brownsheep_Susc,tsdA_Brownsheep_Lat,tsdA_Brownsheep_Subc,tsdA_Brownsheep_Clin,tsdA_Brownsheep_NImm,tsdA_Brownsheep_VImm,tsdA_Brownsheep_Dest,tsdA_Doe_Susc,tsdA_Doe_Lat,tsdA_Doe_Subc,tsdA_Doe_Clin,tsdA_Doe_NImm,tsdA_Doe_VImm,tsdA_Doe_Dest,tsdA_Pig_Susc,tsdA_Pig_Lat,tsdA_Pig_Subc,tsdA_Pig_Clin,tsdA_Pig_NImm,tsdA_Pig_VImm,tsdA_Pig_Dest,average-prevalence,diseaseDuration,tstnUTruePos,tstnUTruePosCattle,tstnUTruePos_Dogsheep_,tstnUTruePosSwine,tstnUTruePos_Bulldog_,tstnUTruePos_Brownsheep_,tstnUTruePos_Doe_,tstnUTruePos_Pig_,tstnUTrueNeg,tstnUTrueNegCattle,tstnUTrueNeg_Dogsheep_,tstnUTrueNegSwine,tstnUTrueNeg_Bulldog_,tstnUTrueNeg_Brownsheep_,tstnUTrueNeg_Doe_,tstnUTrueNeg_Pig_,tstnUFalsePos,tstnUFalsePosCattle,tstnUFalsePos_Dogsheep_,tstnUFalsePosSwine,tstnUFalsePos_Bulldog_,tstnUFalsePos_Brownsheep_,tstnUFalsePos_Doe_,tstnUFalsePos_Pig_,tstnUFalseNeg,tstnUFalseNegCattle,tstnUFalseNeg_Dogsheep_,tstnUFalseNegSwine,tstnUFalseNeg_Bulldog_,tstnUFalseNeg_Brownsheep_,tstnUFalseNeg_Doe_,tstnUFalseNeg_Pig_,tstcUAll,tstcUDirFwd,tstcUIndFwd,tstcUDirBack,tstcUIndBack,tstcUCattle,tstcU_Dogsheep_,tstcUSwine,tstcU_Bulldog_,tstcU_Brownsheep_,tstcU_Doe_,tstcU_Pig_,tstcUDirFwdCattle,tstcUDirFwd_Dogsheep_,tstcUDirFwdSwine,tstcUDirFwd_Bulldog_,tstcUDirFwd_Brownsheep_,tstcUDirFwd_Doe_,tstcUDirFwd_Pig_,tstcUIndFwdCattle,tstcUIndFwd_Dogsheep_,tstcUIndFwdSwine,tstcUIndFwd_Bulldog_,tstcUIndFwd_Brownsheep_,tstcUIndFwd_Doe_,tstcUIndFwd_Pig_,tstcUDirBackCattle,tstcUDirBack_Dogsheep_,tstcUDirBackSwine,tstcUDirBack_Bulldog_,tstcUDirBack_Brownsheep_,tstcUDirBack_Doe_,tstcUDirBack_Pig_,tstcUIndBackCattle,tstcUIndBack_Dogsheep_,tstcUIndBackSwine,tstcUIndBack_Bulldog_,tstcUIndBack_Brownsheep_,tstcUIndBack_Doe_,tstcUIndBack_Pig_,tstcUTruePos,tstcUTruePosCattle,tstcUTruePos_Dogsheep_,tstcUTruePosSwine,tstcUTruePos_Bulldog_,tstcUTruePos_Brownsheep_,tstcUTruePos_Doe_,tstcUTruePos_Pig_,tstcUTrueNeg,tstcUTrueNegCattle,tstcUTrueNeg_Dogsheep_,tstcUTrueNegSwine,tstcUTrueNeg_Bulldog_,tstcUTrueNeg_Brownsheep_,tstcUTrueNeg_Doe_,tstcUTrueNeg_Pig_,tstcUFalsePos,tstcUFalsePosCattle,tstcUFalsePos_Dogsheep_,tstcUFalsePosSwine,tstcUFalsePos_Bulldog_,tstcUFalsePos_Brownsheep_,tstcUFalsePos_Doe_,tstcUFalsePos_Pig_,tstcUFalseNeg,tstcUFalseNegCattle,tstcUFalseNeg_Dogsheep_,tstcUFalseNegSwine,tstcUFalseNeg_Bulldog_,tstcUFalseNeg_Brownsheep_,tstcUFalseNeg_Doe_,tstcUFalseNeg_Pig_,tstcAAll,tstcADirFwd,tstcAIndFwd,tstcADirBack,tstcAIndBack,tstcACattle,tstcA_Dogsheep_,tstcASwine,tstcA_Bulldog_,tstcA_Brownsheep_,tstcA_Doe_,tstcA_Pig_,tstcADirFwdCattle,tstcADirFwd_Dogsheep_,tstcADirFwdSwine,tstcADirFwd_Bulldog_,tstcADirFwd_Brownsheep_,tstcADirFwd_Doe_,tstcADirFwd_Pig_,tstcAIndFwdCattle,tstcAIndFwd_Dogsheep_,tstcAIndFwdSwine,tstcAIndFwd_Bulldog_,tstcAIndFwd_Brownsheep_,tstcAIndFwd_Doe_,tstcAIndFwd_Pig_,tstcADirBackCattle,tstcADirBack_Dogsheep_,tstcADirBackSwine,tstcADirBack_Bulldog_,tstcADirBack_Brownsheep_,tstcADirBack_Doe_,tstcADirBack_Pig_,tstcAIndBackCattle,tstcAIndBack_Dogsheep_,tstcAIndBackSwine,tstcAIndBack_Bulldog_,tstcAIndBack_Brownsheep_,tstcAIndBack_Doe_,tstcAIndBack_Pig_,vaccOccurred,firstVaccination,firstVaccinationRing,firstVaccinationCattle,firstVaccination_Dogsheep_,firstVaccinationSwine,firstVaccination_Bulldog_,firstVaccination_Brownsheep_,firstVaccination_Doe_,firstVaccination_Pig_,firstVaccinationRingCattle,firstVaccinationRing_Dogsheep_,firstVaccinationRingSwine,firstVaccinationRing_Bulldog_,firstVaccinationRing_Brownsheep_,firstVaccinationRing_Doe_,firstVaccinationRing_Pig_,vacnUAll,vacnUIni,vacnURing,vacnUCattle,vacnU_Dogsheep_,vacnUSwine,vacnU_Bulldog_,vacnU_Brownsheep_,vacnU_Doe_,vacnU_Pig_,vacnUIniCattle,vacnUIni_Dogsheep_,vacnUIniSwine,vacnUIni_Bulldog_,vacnUIni_Brownsheep_,vacnUIni_Doe_,vacnUIni_Pig_,vacnURingCattle,vacnURing_Dogsheep_,vacnURingSwine,vacnURing_Bulldog_,vacnURing_Brownsheep_,vacnURing_Doe_,vacnURing_Pig_,vaccUAll,vaccUIni,vaccURing,vaccUCattle,vaccU_Dogsheep_,vaccUSwine,vaccU_Bulldog_,vaccU_Brownsheep_,vaccU_Doe_,vaccU_Pig_,vaccUIniCattle,vaccUIni_Dogsheep_,vaccUIniSwine,vaccUIni_Bulldog_,vaccUIni_Brownsheep_,vaccUIni_Doe_,vaccUIni_Pig_,vaccURingCattle,vaccURing_Dogsheep_,vaccURingSwine,vaccURing_Bulldog_,vaccURing_Brownsheep_,vaccURing_Doe_,vaccURing_Pig_,vacnAAll,vacnAIni,vacnARing,vacnACattle,vacnA_Dogsheep_,vacnASwine,vacnA_Bulldog_,vacnA_Brownsheep_,vacnA_Doe_,vacnA_Pig_,vacnAIniCattle,vacnAIni_Dogsheep_,vacnAIniSwine,vacnAIni_Bulldog_,vacnAIni_Brownsheep_,vacnAIni_Doe_,vacnAIni_Pig_,vacnARingCattle,vacnARing_Dogsheep_,vacnARingSwine,vacnARing_Bulldog_,vacnARing_Brownsheep_,vacnARing_Doe_,vacnARing_Pig_,vaccAAll,vaccAIni,vaccARing,vaccACattle,vaccA_Dogsheep_,vaccASwine,vaccA_Bulldog_,vaccA_Brownsheep_,vaccA_Doe_,vaccA_Pig_,vaccAIniCattle,vaccAIni_Dogsheep_,vaccAIniSwine,vaccAIni_Bulldog_,vaccAIni_Brownsheep_,vaccAIni_Doe_,vaccAIni_Pig_,vaccARingCattle,vaccARing_Dogsheep_,vaccARingSwine,vaccARing_Bulldog_,vaccARing_Brownsheep_,vaccARing_Doe_,vaccARing_Pig_,exmnUAll,exmnURing,exmnUDirFwd,exmnUIndFwd,exmnUDirBack,exmnUIndBack,exmnUDet,exmnUCattle,exmnU_Dogsheep_,exmnUSwine,exmnU_Bulldog_,exmnU_Brownsheep_,exmnU_Doe_,exmnU_Pig_,exmnURingCattle,exmnURing_Dogsheep_,exmnURingSwine,exmnURing_Bulldog_,exmnURing_Brownsheep_,exmnURing_Doe_,exmnURing_Pig_,exmnUDirFwdCattle,exmnUDirFwd_Dogsheep_,exmnUDirFwdSwine,exmnUDirFwd_Bulldog_,exmnUDirFwd_Brownsheep_,exmnUDirFwd_Doe_,exmnUDirFwd_Pig_,exmnUIndFwdCattle,exmnUIndFwd_Dogsheep_,exmnUIndFwdSwine,exmnUIndFwd_Bulldog_,exmnUIndFwd_Brownsheep_,exmnUIndFwd_Doe_,exmnUIndFwd_Pig_,exmnUDirBackCattle,exmnUDirBack_Dogsheep_,exmnUDirBackSwine,exmnUDirBack_Bulldog_,exmnUDirBack_Brownsheep_,exmnUDirBack_Doe_,exmnUDirBack_Pig_,exmnUIndBackCattle,exmnUIndBack_Dogsheep_,exmnUIndBackSwine,exmnUIndBack_Bulldog_,exmnUIndBack_Brownsheep_,exmnUIndBack_Doe_,exmnUIndBack_Pig_,exmnUDetCattle,exmnUDet_Dogsheep_,exmnUDetSwine,exmnUDet_Bulldog_,exmnUDet_Brownsheep_,exmnUDet_Doe_,exmnUDet_Pig_,exmnAAll,exmnARing,exmnADirFwd,exmnAIndFwd,exmnADirBack,exmnAIndBack,exmnADet,exmnACattle,exmnA_Dogsheep_,exmnASwine,exmnA_Bulldog_,exmnA_Brownsheep_,exmnA_Doe_,exmnA_Pig_,exmnARingCattle,exmnARing_Dogsheep_,exmnARingSwine,exmnARing_Bulldog_,exmnARing_Brownsheep_,exmnARing_Doe_,exmnARing_Pig_,exmnADirFwdCattle,exmnADirFwd_Dogsheep_,exmnADirFwdSwine,exmnADirFwd_Bulldog_,exmnADirFwd_Brownsheep_,exmnADirFwd_Doe_,exmnADirFwd_Pig_,exmnAIndFwdCattle,exmnAIndFwd_Dogsheep_,exmnAIndFwdSwine,exmnAIndFwd_Bulldog_,exmnAIndFwd_Brownsheep_,exmnAIndFwd_Doe_,exmnAIndFwd_Pig_,exmnADirBackCattle,exmnADirBack_Dogsheep_,exmnADirBackSwine,exmnADirBack_Bulldog_,exmnADirBack_Brownsheep_,exmnADirBack_Doe_,exmnADirBack_Pig_,exmnAIndBackCattle,exmnAIndBack_Dogsheep_,exmnAIndBackSwine,exmnAIndBack_Bulldog_,exmnAIndBack_Brownsheep_,exmnAIndBack_Doe_,exmnAIndBack_Pig_,exmnADetCattle,exmnADet_Dogsheep_,exmnADetSwine,exmnADet_Bulldog_,exmnADet_Brownsheep_,exmnADet_Doe_,exmnADet_Pig_,exmcUAll,exmcURing,exmcUDirFwd,exmcUIndFwd,exmcUDirBack,exmcUIndBack,exmcUDet,exmcUCattle,exmcU_Dogsheep_,exmcUSwine,exmcU_Bulldog_,exmcU_Brownsheep_,exmcU_Doe_,exmcU_Pig_,exmcURingCattle,exmcURing_Dogsheep_,exmcURingSwine,exmcURing_Bulldog_,exmcURing_Brownsheep_,exmcURing_Doe_,exmcURing_Pig_,exmcUDirFwdCattle,exmcUDirFwd_Dogsheep_,exmcUDirFwdSwine,exmcUDirFwd_Bulldog_,exmcUDirFwd_Brownsheep_,exmcUDirFwd_Doe_,exmcUDirFwd_Pig_,exmcUIndFwdCattle,exmcUIndFwd_Dogsheep_,exmcUIndFwdSwine,exmcUIndFwd_Bulldog_,exmcUIndFwd_Brownsheep_,exmcUIndFwd_Doe_,exmcUIndFwd_Pig_,exmcUDirBackCattle,exmcUDirBack_Dogsheep_,exmcUDirBackSwine,exmcUDirBack_Bulldog_,exmcUDirBack_Brownsheep_,exmcUDirBack_Doe_,exmcUDirBack_Pig_,exmcUIndBackCattle,exmcUIndBack_Dogsheep_,exmcUIndBackSwine,exmcUIndBack_Bulldog_,exmcUIndBack_Brownsheep_,exmcUIndBack_Doe_,exmcUIndBack_Pig_,exmcUDetCattle,exmcUDet_Dogsheep_,exmcUDetSwine,exmcUDet_Bulldog_,exmcUDet_Brownsheep_,exmcUDet_Doe_,exmcUDet_Pig_,exmcAAll,exmcARing,exmcADirFwd,exmcAIndFwd,exmcADirBack,exmcAIndBack,exmcADet,exmcACattle,exmcA_Dogsheep_,exmcASwine,exmcA_Bulldog_,exmcA_Brownsheep_,exmcA_Doe_,exmcA_Pig_,exmcARingCattle,exmcARing_Dogsheep_,exmcARingSwine,exmcARing_Bulldog_,exmcARing_Brownsheep_,exmcARing_Doe_,exmcARing_Pig_,exmcADirFwdCattle,exmcADirFwd_Dogsheep_,exmcADirFwdSwine,exmcADirFwd_Bulldog_,exmcADirFwd_Brownsheep_,exmcADirFwd_Doe_,exmcADirFwd_Pig_,exmcAIndFwdCattle,exmcAIndFwd_Dogsheep_,exmcAIndFwdSwine,exmcAIndFwd_Bulldog_,exmcAIndFwd_Brownsheep_,exmcAIndFwd_Doe_,exmcAIndFwd_Pig_,exmcADirBackCattle,exmcADirBack_Dogsheep_,exmcADirBackSwine,exmcADirBack_Bulldog_,exmcADirBack_Brownsheep_,exmcADirBack_Doe_,exmcADirBack_Pig_,exmcAIndBackCattle,exmcAIndBack_Dogsheep_,exmcAIndBackSwine,exmcAIndBack_Bulldog_,exmcAIndBack_Brownsheep_,exmcAIndBack_Doe_,exmcAIndBack_Pig_,exmcADetCattle,exmcADet_Dogsheep_,exmcADetSwine,exmcADet_Bulldog_,exmcADet_Brownsheep_,exmcADet_Doe_,exmcADet_Pig_"
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

raw_headers = "Run,Day,outbreakDuration,infnUAll,infnUDir,infnUInd,infnUAir,infnUIni,infnUCattle,infnU_Dogsheep_,infnUSwine,infnU_Bulldog_,infnU_Brownsheep_,infnU_Doe_,infnU_Pig_,infnUDirCattle,infnUDir_Dogsheep_,infnUDirSwine,infnUDir_Bulldog_,infnUDir_Brownsheep_,infnUDir_Doe_,infnUDir_Pig_,infnUIndCattle,infnUInd_Dogsheep_,infnUIndSwine,infnUInd_Bulldog_,infnUInd_Brownsheep_,infnUInd_Doe_,infnUInd_Pig_,infnUAirCattle,infnUAir_Dogsheep_,infnUAirSwine,infnUAir_Bulldog_,infnUAir_Brownsheep_,infnUAir_Doe_,infnUAir_Pig_,infnUIniCattle,infnUIni_Dogsheep_,infnUIniSwine,infnUIni_Bulldog_,infnUIni_Brownsheep_,infnUIni_Doe_,infnUIni_Pig_,infcUAll,infcUDir,infcUInd,infcUAir,infcUIni,infcUCattle,infcU_Dogsheep_,infcUSwine,infcU_Bulldog_,infcU_Brownsheep_,infcU_Doe_,infcU_Pig_,infcUDirCattle,infcUDir_Dogsheep_,infcUDirSwine,infcUDir_Bulldog_,infcUDir_Brownsheep_,infcUDir_Doe_,infcUDir_Pig_,infcUIndCattle,infcUInd_Dogsheep_,infcUIndSwine,infcUInd_Bulldog_,infcUInd_Brownsheep_,infcUInd_Doe_,infcUInd_Pig_,infcUAirCattle,infcUAir_Dogsheep_,infcUAirSwine,infcUAir_Bulldog_,infcUAir_Brownsheep_,infcUAir_Doe_,infcUAir_Pig_,infcUIniCattle,infcUIni_Dogsheep_,infcUIniSwine,infcUIni_Bulldog_,infcUIni_Brownsheep_,infcUIni_Doe_,infcUIni_Pig_,infnAAll,infnADir,infnAInd,infnAAir,infnAIni,infnACattle,infnA_Dogsheep_,infnASwine,infnA_Bulldog_,infnA_Brownsheep_,infnA_Doe_,infnA_Pig_,infnADirCattle,infnADir_Dogsheep_,infnADirSwine,infnADir_Bulldog_,infnADir_Brownsheep_,infnADir_Doe_,infnADir_Pig_,infnAIndCattle,infnAInd_Dogsheep_,infnAIndSwine,infnAInd_Bulldog_,infnAInd_Brownsheep_,infnAInd_Doe_,infnAInd_Pig_,infnAAirCattle,infnAAir_Dogsheep_,infnAAirSwine,infnAAir_Bulldog_,infnAAir_Brownsheep_,infnAAir_Doe_,infnAAir_Pig_,infnAIniCattle,infnAIni_Dogsheep_,infnAIniSwine,infnAIni_Bulldog_,infnAIni_Brownsheep_,infnAIni_Doe_,infnAIni_Pig_,infcAAll,infcADir,infcAInd,infcAAir,infcAIni,infcACattle,infcA_Dogsheep_,infcASwine,infcA_Bulldog_,infcA_Brownsheep_,infcA_Doe_,infcA_Pig_,infcADirCattle,infcADir_Dogsheep_,infcADirSwine,infcADir_Bulldog_,infcADir_Brownsheep_,infcADir_Doe_,infcADir_Pig_,infcAIndCattle,infcAInd_Dogsheep_,infcAIndSwine,infcAInd_Bulldog_,infcAInd_Brownsheep_,infcAInd_Doe_,infcAInd_Pig_,infcAAirCattle,infcAAir_Dogsheep_,infcAAirSwine,infcAAir_Bulldog_,infcAAir_Brownsheep_,infcAAir_Doe_,infcAAir_Pig_,infcAIniCattle,infcAIni_Dogsheep_,infcAIniSwine,infcAIni_Bulldog_,infcAIni_Brownsheep_,infcAIni_Doe_,infcAIni_Pig_,firstDetUInfAll,firstDetAInfAll,ratio,expnUAll,expnUDir,expnUInd,expnUAir,expnUCattle,expnU_Dogsheep_,expnUSwine,expnU_Bulldog_,expnU_Brownsheep_,expnU_Doe_,expnU_Pig_,expnUDirCattle,expnUDir_Dogsheep_,expnUDirSwine,expnUDir_Bulldog_,expnUDir_Brownsheep_,expnUDir_Doe_,expnUDir_Pig_,expnUIndCattle,expnUInd_Dogsheep_,expnUIndSwine,expnUInd_Bulldog_,expnUInd_Brownsheep_,expnUInd_Doe_,expnUInd_Pig_,expnUAirCattle,expnUAir_Dogsheep_,expnUAirSwine,expnUAir_Bulldog_,expnUAir_Brownsheep_,expnUAir_Doe_,expnUAir_Pig_,expcUAll,expcUDir,expcUInd,expcUAir,expcUCattle,expcU_Dogsheep_,expcUSwine,expcU_Bulldog_,expcU_Brownsheep_,expcU_Doe_,expcU_Pig_,expcUDirCattle,expcUDir_Dogsheep_,expcUDirSwine,expcUDir_Bulldog_,expcUDir_Brownsheep_,expcUDir_Doe_,expcUDir_Pig_,expcUIndCattle,expcUInd_Dogsheep_,expcUIndSwine,expcUInd_Bulldog_,expcUInd_Brownsheep_,expcUInd_Doe_,expcUInd_Pig_,expcUAirCattle,expcUAir_Dogsheep_,expcUAirSwine,expcUAir_Bulldog_,expcUAir_Brownsheep_,expcUAir_Doe_,expcUAir_Pig_,expnAAll,expnADir,expnAInd,expnAAir,expnACattle,expnA_Dogsheep_,expnASwine,expnA_Bulldog_,expnA_Brownsheep_,expnA_Doe_,expnA_Pig_,expnADirCattle,expnADir_Dogsheep_,expnADirSwine,expnADir_Bulldog_,expnADir_Brownsheep_,expnADir_Doe_,expnADir_Pig_,expnAIndCattle,expnAInd_Dogsheep_,expnAIndSwine,expnAInd_Bulldog_,expnAInd_Brownsheep_,expnAInd_Doe_,expnAInd_Pig_,expnAAirCattle,expnAAir_Dogsheep_,expnAAirSwine,expnAAir_Bulldog_,expnAAir_Brownsheep_,expnAAir_Doe_,expnAAir_Pig_,expcAAll,expcADir,expcAInd,expcAAir,expcACattle,expcA_Dogsheep_,expcASwine,expcA_Bulldog_,expcA_Brownsheep_,expcA_Doe_,expcA_Pig_,expcADirCattle,expcADir_Dogsheep_,expcADirSwine,expcADir_Bulldog_,expcADir_Brownsheep_,expcADir_Doe_,expcADir_Pig_,expcAIndCattle,expcAInd_Dogsheep_,expcAIndSwine,expcAInd_Bulldog_,expcAInd_Brownsheep_,expcAInd_Doe_,expcAInd_Pig_,expcAAirCattle,expcAAir_Dogsheep_,expcAAirSwine,expcAAir_Bulldog_,expcAAir_Brownsheep_,expcAAir_Doe_,expcAAir_Pig_,adqnUAll,adqcUAll,vacwUAll,vacwUCattle,vacwU_Dogsheep_,vacwUSwine,vacwU_Bulldog_,vacwU_Brownsheep_,vacwU_Doe_,vacwU_Pig_,vacwAAll,vacwACattle,vacwA_Dogsheep_,vacwASwine,vacwA_Bulldog_,vacwA_Brownsheep_,vacwA_Doe_,vacwA_Pig_,vacwUMax,vacwUMaxDay,vacwAMax,vacwAMaxDay,vacwUTimeMax,vacwUTimeAvg,vacwUDaysInQueue,vacwADaysInQueue,zoneAreaHighRisk,zoneAreaMediumRisk,maxZoneAreaHighRisk,maxZoneAreaMediumRisk,maxZoneAreaDayHighRisk,maxZoneAreaDayMediumRisk,finalZoneAreaHighRisk,finalZoneAreaMediumRisk,zonePerimeterHighRisk,zonePerimeterMediumRisk,maxZonePerimeterHighRisk,maxZonePerimeterMediumRisk,maxZonePerimeterDayHighRisk,maxZonePerimeterDayMediumRisk,finalZonePerimeterHighRisk,finalZonePerimeterMediumRisk,num-separate-areasHighRisk,num-separate-areasMediumRisk,unitsInZoneHighRisk,unitsInZoneMediumRisk,unitsInZoneBackground,unitsInZoneHighRiskCattle,unitsInZoneHighRisk_Dogsheep_,unitsInZoneHighRiskSwine,unitsInZoneHighRisk_Bulldog_,unitsInZoneHighRisk_Brownsheep_,unitsInZoneHighRisk_Doe_,unitsInZoneHighRisk_Pig_,unitsInZoneMediumRiskCattle,unitsInZoneMediumRisk_Dogsheep_,unitsInZoneMediumRiskSwine,unitsInZoneMediumRisk_Bulldog_,unitsInZoneMediumRisk_Brownsheep_,unitsInZoneMediumRisk_Doe_,unitsInZoneMediumRisk_Pig_,unitsInZoneBackgroundCattle,unitsInZoneBackground_Dogsheep_,unitsInZoneBackgroundSwine,unitsInZoneBackground_Bulldog_,unitsInZoneBackground_Brownsheep_,unitsInZoneBackground_Doe_,unitsInZoneBackground_Pig_,unitDaysInZoneHighRisk,unitDaysInZoneMediumRisk,unitDaysInZoneBackground,unitDaysInZoneHighRiskCattle,unitDaysInZoneHighRisk_Dogsheep_,unitDaysInZoneHighRiskSwine,unitDaysInZoneHighRisk_Bulldog_,unitDaysInZoneHighRisk_Brownsheep_,unitDaysInZoneHighRisk_Doe_,unitDaysInZoneHighRisk_Pig_,unitDaysInZoneMediumRiskCattle,unitDaysInZoneMediumRisk_Dogsheep_,unitDaysInZoneMediumRiskSwine,unitDaysInZoneMediumRisk_Bulldog_,unitDaysInZoneMediumRisk_Brownsheep_,unitDaysInZoneMediumRisk_Doe_,unitDaysInZoneMediumRisk_Pig_,unitDaysInZoneBackgroundCattle,unitDaysInZoneBackground_Dogsheep_,unitDaysInZoneBackgroundSwine,unitDaysInZoneBackground_Bulldog_,unitDaysInZoneBackground_Brownsheep_,unitDaysInZoneBackground_Doe_,unitDaysInZoneBackground_Pig_,animalDaysInZoneHighRisk,animalDaysInZoneMediumRisk,animalDaysInZoneBackground,animalDaysInZoneHighRiskCattle,animalDaysInZoneHighRisk_Dogsheep_,animalDaysInZoneHighRiskSwine,animalDaysInZoneHighRisk_Bulldog_,animalDaysInZoneHighRisk_Brownsheep_,animalDaysInZoneHighRisk_Doe_,animalDaysInZoneHighRisk_Pig_,animalDaysInZoneMediumRiskCattle,animalDaysInZoneMediumRisk_Dogsheep_,animalDaysInZoneMediumRiskSwine,animalDaysInZoneMediumRisk_Bulldog_,animalDaysInZoneMediumRisk_Brownsheep_,animalDaysInZoneMediumRisk_Doe_,animalDaysInZoneMediumRisk_Pig_,animalDaysInZoneBackgroundCattle,animalDaysInZoneBackground_Dogsheep_,animalDaysInZoneBackgroundSwine,animalDaysInZoneBackground_Bulldog_,animalDaysInZoneBackground_Brownsheep_,animalDaysInZoneBackground_Doe_,animalDaysInZoneBackground_Pig_,deswUAll,deswUCattle,deswU_Dogsheep_,deswUSwine,deswU_Bulldog_,deswU_Brownsheep_,deswU_Doe_,deswU_Pig_,deswAAll,deswACattle,deswA_Dogsheep_,deswASwine,deswA_Bulldog_,deswA_Brownsheep_,deswA_Doe_,deswA_Pig_,deswUMax,deswUMaxDay,deswAMax,deswAMaxDay,deswUTimeMax,deswUTimeAvg,deswUDaysInQueue,deswADaysInQueue,destrOccurred,firstDestruction,firstDestructionUnsp,firstDestructionRing,firstDestructionDirFwd,firstDestructionIndFwd,firstDestructionDirBack,firstDestructionIndBack,firstDestructionDet,firstDestructionIni,firstDestructionCattle,firstDestruction_Dogsheep_,firstDestructionSwine,firstDestruction_Bulldog_,firstDestruction_Brownsheep_,firstDestruction_Doe_,firstDestruction_Pig_,firstDestructionUnspCattle,firstDestructionUnsp_Dogsheep_,firstDestructionUnspSwine,firstDestructionUnsp_Bulldog_,firstDestructionUnsp_Brownsheep_,firstDestructionUnsp_Doe_,firstDestructionUnsp_Pig_,firstDestructionRingCattle,firstDestructionRing_Dogsheep_,firstDestructionRingSwine,firstDestructionRing_Bulldog_,firstDestructionRing_Brownsheep_,firstDestructionRing_Doe_,firstDestructionRing_Pig_,firstDestructionDirFwdCattle,firstDestructionDirFwd_Dogsheep_,firstDestructionDirFwdSwine,firstDestructionDirFwd_Bulldog_,firstDestructionDirFwd_Brownsheep_,firstDestructionDirFwd_Doe_,firstDestructionDirFwd_Pig_,firstDestructionIndFwdCattle,firstDestructionIndFwd_Dogsheep_,firstDestructionIndFwdSwine,firstDestructionIndFwd_Bulldog_,firstDestructionIndFwd_Brownsheep_,firstDestructionIndFwd_Doe_,firstDestructionIndFwd_Pig_,firstDestructionDirBackCattle,firstDestructionDirBack_Dogsheep_,firstDestructionDirBackSwine,firstDestructionDirBack_Bulldog_,firstDestructionDirBack_Brownsheep_,firstDestructionDirBack_Doe_,firstDestructionDirBack_Pig_,firstDestructionIndBackCattle,firstDestructionIndBack_Dogsheep_,firstDestructionIndBackSwine,firstDestructionIndBack_Bulldog_,firstDestructionIndBack_Brownsheep_,firstDestructionIndBack_Doe_,firstDestructionIndBack_Pig_,firstDestructionDetCattle,firstDestructionDet_Dogsheep_,firstDestructionDetSwine,firstDestructionDet_Bulldog_,firstDestructionDet_Brownsheep_,firstDestructionDet_Doe_,firstDestructionDet_Pig_,firstDestructionIniCattle,firstDestructionIni_Dogsheep_,firstDestructionIniSwine,firstDestructionIni_Bulldog_,firstDestructionIni_Brownsheep_,firstDestructionIni_Doe_,firstDestructionIni_Pig_,desnUAll,desnUIni,desnUUnsp,desnURing,desnUDirFwd,desnUIndFwd,desnUDirBack,desnUIndBack,desnUDet,desnUCattle,desnU_Dogsheep_,desnUSwine,desnU_Bulldog_,desnU_Brownsheep_,desnU_Doe_,desnU_Pig_,desnUIniCattle,desnUIni_Dogsheep_,desnUIniSwine,desnUIni_Bulldog_,desnUIni_Brownsheep_,desnUIni_Doe_,desnUIni_Pig_,desnUUnspCattle,desnUUnsp_Dogsheep_,desnUUnspSwine,desnUUnsp_Bulldog_,desnUUnsp_Brownsheep_,desnUUnsp_Doe_,desnUUnsp_Pig_,desnURingCattle,desnURing_Dogsheep_,desnURingSwine,desnURing_Bulldog_,desnURing_Brownsheep_,desnURing_Doe_,desnURing_Pig_,desnUDirFwdCattle,desnUDirFwd_Dogsheep_,desnUDirFwdSwine,desnUDirFwd_Bulldog_,desnUDirFwd_Brownsheep_,desnUDirFwd_Doe_,desnUDirFwd_Pig_,desnUIndFwdCattle,desnUIndFwd_Dogsheep_,desnUIndFwdSwine,desnUIndFwd_Bulldog_,desnUIndFwd_Brownsheep_,desnUIndFwd_Doe_,desnUIndFwd_Pig_,desnUDirBackCattle,desnUDirBack_Dogsheep_,desnUDirBackSwine,desnUDirBack_Bulldog_,desnUDirBack_Brownsheep_,desnUDirBack_Doe_,desnUDirBack_Pig_,desnUIndBackCattle,desnUIndBack_Dogsheep_,desnUIndBackSwine,desnUIndBack_Bulldog_,desnUIndBack_Brownsheep_,desnUIndBack_Doe_,desnUIndBack_Pig_,desnUDetCattle,desnUDet_Dogsheep_,desnUDetSwine,desnUDet_Bulldog_,desnUDet_Brownsheep_,desnUDet_Doe_,desnUDet_Pig_,descUAll,descUIni,descUUnsp,descURing,descUDirFwd,descUIndFwd,descUDirBack,descUIndBack,descUDet,descUCattle,descU_Dogsheep_,descUSwine,descU_Bulldog_,descU_Brownsheep_,descU_Doe_,descU_Pig_,descUIniCattle,descUIni_Dogsheep_,descUIniSwine,descUIni_Bulldog_,descUIni_Brownsheep_,descUIni_Doe_,descUIni_Pig_,descUUnspCattle,descUUnsp_Dogsheep_,descUUnspSwine,descUUnsp_Bulldog_,descUUnsp_Brownsheep_,descUUnsp_Doe_,descUUnsp_Pig_,descURingCattle,descURing_Dogsheep_,descURingSwine,descURing_Bulldog_,descURing_Brownsheep_,descURing_Doe_,descURing_Pig_,descUDirFwdCattle,descUDirFwd_Dogsheep_,descUDirFwdSwine,descUDirFwd_Bulldog_,descUDirFwd_Brownsheep_,descUDirFwd_Doe_,descUDirFwd_Pig_,descUIndFwdCattle,descUIndFwd_Dogsheep_,descUIndFwdSwine,descUIndFwd_Bulldog_,descUIndFwd_Brownsheep_,descUIndFwd_Doe_,descUIndFwd_Pig_,descUDirBackCattle,descUDirBack_Dogsheep_,descUDirBackSwine,descUDirBack_Bulldog_,descUDirBack_Brownsheep_,descUDirBack_Doe_,descUDirBack_Pig_,descUIndBackCattle,descUIndBack_Dogsheep_,descUIndBackSwine,descUIndBack_Bulldog_,descUIndBack_Brownsheep_,descUIndBack_Doe_,descUIndBack_Pig_,descUDetCattle,descUDet_Dogsheep_,descUDetSwine,descUDet_Bulldog_,descUDet_Brownsheep_,descUDet_Doe_,descUDet_Pig_,desnAAll,desnAIni,desnAUnsp,desnARing,desnADirFwd,desnAIndFwd,desnADirBack,desnAIndBack,desnADet,desnACattle,desnA_Dogsheep_,desnASwine,desnA_Bulldog_,desnA_Brownsheep_,desnA_Doe_,desnA_Pig_,desnAIniCattle,desnAIni_Dogsheep_,desnAIniSwine,desnAIni_Bulldog_,desnAIni_Brownsheep_,desnAIni_Doe_,desnAIni_Pig_,desnAUnspCattle,desnAUnsp_Dogsheep_,desnAUnspSwine,desnAUnsp_Bulldog_,desnAUnsp_Brownsheep_,desnAUnsp_Doe_,desnAUnsp_Pig_,desnARingCattle,desnARing_Dogsheep_,desnARingSwine,desnARing_Bulldog_,desnARing_Brownsheep_,desnARing_Doe_,desnARing_Pig_,desnADirFwdCattle,desnADirFwd_Dogsheep_,desnADirFwdSwine,desnADirFwd_Bulldog_,desnADirFwd_Brownsheep_,desnADirFwd_Doe_,desnADirFwd_Pig_,desnAIndFwdCattle,desnAIndFwd_Dogsheep_,desnAIndFwdSwine,desnAIndFwd_Bulldog_,desnAIndFwd_Brownsheep_,desnAIndFwd_Doe_,desnAIndFwd_Pig_,desnADirBackCattle,desnADirBack_Dogsheep_,desnADirBackSwine,desnADirBack_Bulldog_,desnADirBack_Brownsheep_,desnADirBack_Doe_,desnADirBack_Pig_,desnAIndBackCattle,desnAIndBack_Dogsheep_,desnAIndBackSwine,desnAIndBack_Bulldog_,desnAIndBack_Brownsheep_,desnAIndBack_Doe_,desnAIndBack_Pig_,desnADetCattle,desnADet_Dogsheep_,desnADetSwine,desnADet_Bulldog_,desnADet_Brownsheep_,desnADet_Doe_,desnADet_Pig_,descAAll,descAIni,descAUnsp,descARing,descADirFwd,descAIndFwd,descADirBack,descAIndBack,descADet,descACattle,descA_Dogsheep_,descASwine,descA_Bulldog_,descA_Brownsheep_,descA_Doe_,descA_Pig_,descAIniCattle,descAIni_Dogsheep_,descAIniSwine,descAIni_Bulldog_,descAIni_Brownsheep_,descAIni_Doe_,descAIni_Pig_,descAUnspCattle,descAUnsp_Dogsheep_,descAUnspSwine,descAUnsp_Bulldog_,descAUnsp_Brownsheep_,descAUnsp_Doe_,descAUnsp_Pig_,descARingCattle,descARing_Dogsheep_,descARingSwine,descARing_Bulldog_,descARing_Brownsheep_,descARing_Doe_,descARing_Pig_,descADirFwdCattle,descADirFwd_Dogsheep_,descADirFwdSwine,descADirFwd_Bulldog_,descADirFwd_Brownsheep_,descADirFwd_Doe_,descADirFwd_Pig_,descAIndFwdCattle,descAIndFwd_Dogsheep_,descAIndFwdSwine,descAIndFwd_Bulldog_,descAIndFwd_Brownsheep_,descAIndFwd_Doe_,descAIndFwd_Pig_,descADirBackCattle,descADirBack_Dogsheep_,descADirBackSwine,descADirBack_Bulldog_,descADirBack_Brownsheep_,descADirBack_Doe_,descADirBack_Pig_,descAIndBackCattle,descAIndBack_Dogsheep_,descAIndBackSwine,descAIndBack_Bulldog_,descAIndBack_Brownsheep_,descAIndBack_Doe_,descAIndBack_Pig_,descADetCattle,descADet_Dogsheep_,descADetSwine,descADet_Bulldog_,descADet_Brownsheep_,descADet_Doe_,descADet_Pig_,trnUAllp,trnUDirp,trnUIndp,trnUCattlep,trnU_Dogsheep_p,trnUSwinep,trnU_Bulldog_p,trnU_Brownsheep_p,trnU_Doe_p,trnU_Pig_p,trnUDirCattlep,trnUDir_Dogsheep_p,trnUDirSwinep,trnUDir_Bulldog_p,trnUDir_Brownsheep_p,trnUDir_Doe_p,trnUDir_Pig_p,trnUIndCattlep,trnUInd_Dogsheep_p,trnUIndSwinep,trnUInd_Bulldog_p,trnUInd_Brownsheep_p,trnUInd_Doe_p,trnUInd_Pig_p,trcUAllp,trcUDirp,trcUIndp,trcUCattlep,trcU_Dogsheep_p,trcUSwinep,trcU_Bulldog_p,trcU_Brownsheep_p,trcU_Doe_p,trcU_Pig_p,trcUDirCattlep,trcUDir_Dogsheep_p,trcUDirSwinep,trcUDir_Bulldog_p,trcUDir_Brownsheep_p,trcUDir_Doe_p,trcUDir_Pig_p,trcUIndCattlep,trcUInd_Dogsheep_p,trcUIndSwinep,trcUInd_Bulldog_p,trcUInd_Brownsheep_p,trcUInd_Doe_p,trcUInd_Pig_p,trnUAll,trnUDir,trnUInd,trnUCattle,trnU_Dogsheep_,trnUSwine,trnU_Bulldog_,trnU_Brownsheep_,trnU_Doe_,trnU_Pig_,trnUDirCattle,trnUDir_Dogsheep_,trnUDirSwine,trnUDir_Bulldog_,trnUDir_Brownsheep_,trnUDir_Doe_,trnUDir_Pig_,trnUIndCattle,trnUInd_Dogsheep_,trnUIndSwine,trnUInd_Bulldog_,trnUInd_Brownsheep_,trnUInd_Doe_,trnUInd_Pig_,trcUAll,trcUDir,trcUInd,trcUCattle,trcU_Dogsheep_,trcUSwine,trcU_Bulldog_,trcU_Brownsheep_,trcU_Doe_,trcU_Pig_,trcUDirCattle,trcUDir_Dogsheep_,trcUDirSwine,trcUDir_Bulldog_,trcUDir_Brownsheep_,trcUDir_Doe_,trcUDir_Pig_,trcUIndCattle,trcUInd_Dogsheep_,trcUIndSwine,trcUInd_Bulldog_,trcUInd_Brownsheep_,trcUInd_Doe_,trcUInd_Pig_,trnAAllp,trnADirp,trnAIndp,trnACattlep,trnA_Dogsheep_p,trnASwinep,trnA_Bulldog_p,trnA_Brownsheep_p,trnA_Doe_p,trnA_Pig_p,trnADirCattlep,trnADir_Dogsheep_p,trnADirSwinep,trnADir_Bulldog_p,trnADir_Brownsheep_p,trnADir_Doe_p,trnADir_Pig_p,trnAIndCattlep,trnAInd_Dogsheep_p,trnAIndSwinep,trnAInd_Bulldog_p,trnAInd_Brownsheep_p,trnAInd_Doe_p,trnAInd_Pig_p,trcAAllp,trcADirp,trcAIndp,trcACattlep,trcA_Dogsheep_p,trcASwinep,trcA_Bulldog_p,trcA_Brownsheep_p,trcA_Doe_p,trcA_Pig_p,trcADirCattlep,trcADir_Dogsheep_p,trcADirSwinep,trcADir_Bulldog_p,trcADir_Brownsheep_p,trcADir_Doe_p,trcADir_Pig_p,trcAIndCattlep,trcAInd_Dogsheep_p,trcAIndSwinep,trcAInd_Bulldog_p,trcAInd_Brownsheep_p,trcAInd_Doe_p,trcAInd_Pig_p,trnAAll,trnADir,trnAInd,trnACattle,trnA_Dogsheep_,trnASwine,trnA_Bulldog_,trnA_Brownsheep_,trnA_Doe_,trnA_Pig_,trnADirCattle,trnADir_Dogsheep_,trnADirSwine,trnADir_Bulldog_,trnADir_Brownsheep_,trnADir_Doe_,trnADir_Pig_,trnAIndCattle,trnAInd_Dogsheep_,trnAIndSwine,trnAInd_Bulldog_,trnAInd_Brownsheep_,trnAInd_Doe_,trnAInd_Pig_,trcAAll,trcADir,trcAInd,trcACattle,trcA_Dogsheep_,trcASwine,trcA_Bulldog_,trcA_Brownsheep_,trcA_Doe_,trcA_Pig_,trcADirCattle,trcADir_Dogsheep_,trcADirSwine,trcADir_Bulldog_,trcADir_Brownsheep_,trcADir_Doe_,trcADir_Pig_,trcAIndCattle,trcAInd_Dogsheep_,trcAIndSwine,trcAInd_Bulldog_,trcAInd_Brownsheep_,trcAInd_Doe_,trcAInd_Pig_,detOccurred,firstDetection,firstDetectionClin,firstDetectionTest,firstDetectionCattle,firstDetection_Dogsheep_,firstDetectionSwine,firstDetection_Bulldog_,firstDetection_Brownsheep_,firstDetection_Doe_,firstDetection_Pig_,firstDetectionClinCattle,firstDetectionClin_Dogsheep_,firstDetectionClinSwine,firstDetectionClin_Bulldog_,firstDetectionClin_Brownsheep_,firstDetectionClin_Doe_,firstDetectionClin_Pig_,firstDetectionTestCattle,firstDetectionTest_Dogsheep_,firstDetectionTestSwine,firstDetectionTest_Bulldog_,firstDetectionTest_Brownsheep_,firstDetectionTest_Doe_,firstDetectionTest_Pig_,lastDetection,lastDetectionClin,lastDetectionTest,lastDetectionCattle,lastDetection_Dogsheep_,lastDetectionSwine,lastDetection_Bulldog_,lastDetection_Brownsheep_,lastDetection_Doe_,lastDetection_Pig_,lastDetectionClinCattle,lastDetectionClin_Dogsheep_,lastDetectionClinSwine,lastDetectionClin_Bulldog_,lastDetectionClin_Brownsheep_,lastDetectionClin_Doe_,lastDetectionClin_Pig_,lastDetectionTestCattle,lastDetectionTest_Dogsheep_,lastDetectionTestSwine,lastDetectionTest_Bulldog_,lastDetectionTest_Brownsheep_,lastDetectionTest_Doe_,lastDetectionTest_Pig_,detnUAll,detnUClin,detnUTest,detnUCattle,detnU_Dogsheep_,detnUSwine,detnU_Bulldog_,detnU_Brownsheep_,detnU_Doe_,detnU_Pig_,detnUClinCattle,detnUClin_Dogsheep_,detnUClinSwine,detnUClin_Bulldog_,detnUClin_Brownsheep_,detnUClin_Doe_,detnUClin_Pig_,detnUTestCattle,detnUTest_Dogsheep_,detnUTestSwine,detnUTest_Bulldog_,detnUTest_Brownsheep_,detnUTest_Doe_,detnUTest_Pig_,detnAAll,detnAClin,detnATest,detnACattle,detnA_Dogsheep_,detnASwine,detnA_Bulldog_,detnA_Brownsheep_,detnA_Doe_,detnA_Pig_,detnAClinCattle,detnAClin_Dogsheep_,detnAClinSwine,detnAClin_Bulldog_,detnAClin_Brownsheep_,detnAClin_Doe_,detnAClin_Pig_,detnATestCattle,detnATest_Dogsheep_,detnATestSwine,detnATest_Bulldog_,detnATest_Brownsheep_,detnATest_Doe_,detnATest_Pig_,detcUAll,detcUClin,detcUTest,detcUCattle,detcU_Dogsheep_,detcUSwine,detcU_Bulldog_,detcU_Brownsheep_,detcU_Doe_,detcU_Pig_,detcUClinCattle,detcUClin_Dogsheep_,detcUClinSwine,detcUClin_Bulldog_,detcUClin_Brownsheep_,detcUClin_Doe_,detcUClin_Pig_,detcUTestCattle,detcUTest_Dogsheep_,detcUTestSwine,detcUTest_Bulldog_,detcUTest_Brownsheep_,detcUTest_Doe_,detcUTest_Pig_,detcUqAll,detcAAll,detcAClin,detcATest,detcACattle,detcA_Dogsheep_,detcASwine,detcA_Bulldog_,detcA_Brownsheep_,detcA_Doe_,detcA_Pig_,detcAClinCattle,detcAClin_Dogsheep_,detcAClinSwine,detcAClin_Bulldog_,detcAClin_Brownsheep_,detcAClin_Doe_,detcAClin_Pig_,detcATestCattle,detcATest_Dogsheep_,detcATestSwine,detcATest_Bulldog_,detcATest_Brownsheep_,detcATest_Doe_,detcATest_Pig_,tsdUSusc,tsdULat,tsdUSubc,tsdUClin,tsdUNImm,tsdUVImm,tsdUDest,tsdUCattleSusc,tsdUCattleLat,tsdUCattleSubc,tsdUCattleClin,tsdUCattleNImm,tsdUCattleVImm,tsdUCattleDest,tsdU_Dogsheep_Susc,tsdU_Dogsheep_Lat,tsdU_Dogsheep_Subc,tsdU_Dogsheep_Clin,tsdU_Dogsheep_NImm,tsdU_Dogsheep_VImm,tsdU_Dogsheep_Dest,tsdUSwineSusc,tsdUSwineLat,tsdUSwineSubc,tsdUSwineClin,tsdUSwineNImm,tsdUSwineVImm,tsdUSwineDest,tsdU_Bulldog_Susc,tsdU_Bulldog_Lat,tsdU_Bulldog_Subc,tsdU_Bulldog_Clin,tsdU_Bulldog_NImm,tsdU_Bulldog_VImm,tsdU_Bulldog_Dest,tsdU_Brownsheep_Susc,tsdU_Brownsheep_Lat,tsdU_Brownsheep_Subc,tsdU_Brownsheep_Clin,tsdU_Brownsheep_NImm,tsdU_Brownsheep_VImm,tsdU_Brownsheep_Dest,tsdU_Doe_Susc,tsdU_Doe_Lat,tsdU_Doe_Subc,tsdU_Doe_Clin,tsdU_Doe_NImm,tsdU_Doe_VImm,tsdU_Doe_Dest,tsdU_Pig_Susc,tsdU_Pig_Lat,tsdU_Pig_Subc,tsdU_Pig_Clin,tsdU_Pig_NImm,tsdU_Pig_VImm,tsdU_Pig_Dest,tsdASusc,tsdALat,tsdASubc,tsdAClin,tsdANImm,tsdAVImm,tsdADest,tsdACattleSusc,tsdACattleLat,tsdACattleSubc,tsdACattleClin,tsdACattleNImm,tsdACattleVImm,tsdACattleDest,tsdA_Dogsheep_Susc,tsdA_Dogsheep_Lat,tsdA_Dogsheep_Subc,tsdA_Dogsheep_Clin,tsdA_Dogsheep_NImm,tsdA_Dogsheep_VImm,tsdA_Dogsheep_Dest,tsdASwineSusc,tsdASwineLat,tsdASwineSubc,tsdASwineClin,tsdASwineNImm,tsdASwineVImm,tsdASwineDest,tsdA_Bulldog_Susc,tsdA_Bulldog_Lat,tsdA_Bulldog_Subc,tsdA_Bulldog_Clin,tsdA_Bulldog_NImm,tsdA_Bulldog_VImm,tsdA_Bulldog_Dest,tsdA_Brownsheep_Susc,tsdA_Brownsheep_Lat,tsdA_Brownsheep_Subc,tsdA_Brownsheep_Clin,tsdA_Brownsheep_NImm,tsdA_Brownsheep_VImm,tsdA_Brownsheep_Dest,tsdA_Doe_Susc,tsdA_Doe_Lat,tsdA_Doe_Subc,tsdA_Doe_Clin,tsdA_Doe_NImm,tsdA_Doe_VImm,tsdA_Doe_Dest,tsdA_Pig_Susc,tsdA_Pig_Lat,tsdA_Pig_Subc,tsdA_Pig_Clin,tsdA_Pig_NImm,tsdA_Pig_VImm,tsdA_Pig_Dest,average-prevalence,diseaseDuration,tstnUTruePos,tstnUTruePosCattle,tstnUTruePos_Dogsheep_,tstnUTruePosSwine,tstnUTruePos_Bulldog_,tstnUTruePos_Brownsheep_,tstnUTruePos_Doe_,tstnUTruePos_Pig_,tstnUTrueNeg,tstnUTrueNegCattle,tstnUTrueNeg_Dogsheep_,tstnUTrueNegSwine,tstnUTrueNeg_Bulldog_,tstnUTrueNeg_Brownsheep_,tstnUTrueNeg_Doe_,tstnUTrueNeg_Pig_,tstnUFalsePos,tstnUFalsePosCattle,tstnUFalsePos_Dogsheep_,tstnUFalsePosSwine,tstnUFalsePos_Bulldog_,tstnUFalsePos_Brownsheep_,tstnUFalsePos_Doe_,tstnUFalsePos_Pig_,tstnUFalseNeg,tstnUFalseNegCattle,tstnUFalseNeg_Dogsheep_,tstnUFalseNegSwine,tstnUFalseNeg_Bulldog_,tstnUFalseNeg_Brownsheep_,tstnUFalseNeg_Doe_,tstnUFalseNeg_Pig_,tstcUAll,tstcUDirFwd,tstcUIndFwd,tstcUDirBack,tstcUIndBack,tstcUCattle,tstcU_Dogsheep_,tstcUSwine,tstcU_Bulldog_,tstcU_Brownsheep_,tstcU_Doe_,tstcU_Pig_,tstcUDirFwdCattle,tstcUDirFwd_Dogsheep_,tstcUDirFwdSwine,tstcUDirFwd_Bulldog_,tstcUDirFwd_Brownsheep_,tstcUDirFwd_Doe_,tstcUDirFwd_Pig_,tstcUIndFwdCattle,tstcUIndFwd_Dogsheep_,tstcUIndFwdSwine,tstcUIndFwd_Bulldog_,tstcUIndFwd_Brownsheep_,tstcUIndFwd_Doe_,tstcUIndFwd_Pig_,tstcUDirBackCattle,tstcUDirBack_Dogsheep_,tstcUDirBackSwine,tstcUDirBack_Bulldog_,tstcUDirBack_Brownsheep_,tstcUDirBack_Doe_,tstcUDirBack_Pig_,tstcUIndBackCattle,tstcUIndBack_Dogsheep_,tstcUIndBackSwine,tstcUIndBack_Bulldog_,tstcUIndBack_Brownsheep_,tstcUIndBack_Doe_,tstcUIndBack_Pig_,tstcUTruePos,tstcUTruePosCattle,tstcUTruePos_Dogsheep_,tstcUTruePosSwine,tstcUTruePos_Bulldog_,tstcUTruePos_Brownsheep_,tstcUTruePos_Doe_,tstcUTruePos_Pig_,tstcUTrueNeg,tstcUTrueNegCattle,tstcUTrueNeg_Dogsheep_,tstcUTrueNegSwine,tstcUTrueNeg_Bulldog_,tstcUTrueNeg_Brownsheep_,tstcUTrueNeg_Doe_,tstcUTrueNeg_Pig_,tstcUFalsePos,tstcUFalsePosCattle,tstcUFalsePos_Dogsheep_,tstcUFalsePosSwine,tstcUFalsePos_Bulldog_,tstcUFalsePos_Brownsheep_,tstcUFalsePos_Doe_,tstcUFalsePos_Pig_,tstcUFalseNeg,tstcUFalseNegCattle,tstcUFalseNeg_Dogsheep_,tstcUFalseNegSwine,tstcUFalseNeg_Bulldog_,tstcUFalseNeg_Brownsheep_,tstcUFalseNeg_Doe_,tstcUFalseNeg_Pig_,tstcAAll,tstcADirFwd,tstcAIndFwd,tstcADirBack,tstcAIndBack,tstcACattle,tstcA_Dogsheep_,tstcASwine,tstcA_Bulldog_,tstcA_Brownsheep_,tstcA_Doe_,tstcA_Pig_,tstcADirFwdCattle,tstcADirFwd_Dogsheep_,tstcADirFwdSwine,tstcADirFwd_Bulldog_,tstcADirFwd_Brownsheep_,tstcADirFwd_Doe_,tstcADirFwd_Pig_,tstcAIndFwdCattle,tstcAIndFwd_Dogsheep_,tstcAIndFwdSwine,tstcAIndFwd_Bulldog_,tstcAIndFwd_Brownsheep_,tstcAIndFwd_Doe_,tstcAIndFwd_Pig_,tstcADirBackCattle,tstcADirBack_Dogsheep_,tstcADirBackSwine,tstcADirBack_Bulldog_,tstcADirBack_Brownsheep_,tstcADirBack_Doe_,tstcADirBack_Pig_,tstcAIndBackCattle,tstcAIndBack_Dogsheep_,tstcAIndBackSwine,tstcAIndBack_Bulldog_,tstcAIndBack_Brownsheep_,tstcAIndBack_Doe_,tstcAIndBack_Pig_,vaccOccurred,firstVaccination,firstVaccinationRing,firstVaccinationCattle,firstVaccination_Dogsheep_,firstVaccinationSwine,firstVaccination_Bulldog_,firstVaccination_Brownsheep_,firstVaccination_Doe_,firstVaccination_Pig_,firstVaccinationRingCattle,firstVaccinationRing_Dogsheep_,firstVaccinationRingSwine,firstVaccinationRing_Bulldog_,firstVaccinationRing_Brownsheep_,firstVaccinationRing_Doe_,firstVaccinationRing_Pig_,vacnUAll,vacnUIni,vacnURing,vacnUCattle,vacnU_Dogsheep_,vacnUSwine,vacnU_Bulldog_,vacnU_Brownsheep_,vacnU_Doe_,vacnU_Pig_,vacnUIniCattle,vacnUIni_Dogsheep_,vacnUIniSwine,vacnUIni_Bulldog_,vacnUIni_Brownsheep_,vacnUIni_Doe_,vacnUIni_Pig_,vacnURingCattle,vacnURing_Dogsheep_,vacnURingSwine,vacnURing_Bulldog_,vacnURing_Brownsheep_,vacnURing_Doe_,vacnURing_Pig_,vaccUAll,vaccUIni,vaccURing,vaccUCattle,vaccU_Dogsheep_,vaccUSwine,vaccU_Bulldog_,vaccU_Brownsheep_,vaccU_Doe_,vaccU_Pig_,vaccUIniCattle,vaccUIni_Dogsheep_,vaccUIniSwine,vaccUIni_Bulldog_,vaccUIni_Brownsheep_,vaccUIni_Doe_,vaccUIni_Pig_,vaccURingCattle,vaccURing_Dogsheep_,vaccURingSwine,vaccURing_Bulldog_,vaccURing_Brownsheep_,vaccURing_Doe_,vaccURing_Pig_,vacnAAll,vacnAIni,vacnARing,vacnACattle,vacnA_Dogsheep_,vacnASwine,vacnA_Bulldog_,vacnA_Brownsheep_,vacnA_Doe_,vacnA_Pig_,vacnAIniCattle,vacnAIni_Dogsheep_,vacnAIniSwine,vacnAIni_Bulldog_,vacnAIni_Brownsheep_,vacnAIni_Doe_,vacnAIni_Pig_,vacnARingCattle,vacnARing_Dogsheep_,vacnARingSwine,vacnARing_Bulldog_,vacnARing_Brownsheep_,vacnARing_Doe_,vacnARing_Pig_,vaccAAll,vaccAIni,vaccARing,vaccACattle,vaccA_Dogsheep_,vaccASwine,vaccA_Bulldog_,vaccA_Brownsheep_,vaccA_Doe_,vaccA_Pig_,vaccAIniCattle,vaccAIni_Dogsheep_,vaccAIniSwine,vaccAIni_Bulldog_,vaccAIni_Brownsheep_,vaccAIni_Doe_,vaccAIni_Pig_,vaccARingCattle,vaccARing_Dogsheep_,vaccARingSwine,vaccARing_Bulldog_,vaccARing_Brownsheep_,vaccARing_Doe_,vaccARing_Pig_,exmnUAll,exmnURing,exmnUDirFwd,exmnUIndFwd,exmnUDirBack,exmnUIndBack,exmnUDet,exmnUCattle,exmnU_Dogsheep_,exmnUSwine,exmnU_Bulldog_,exmnU_Brownsheep_,exmnU_Doe_,exmnU_Pig_,exmnURingCattle,exmnURing_Dogsheep_,exmnURingSwine,exmnURing_Bulldog_,exmnURing_Brownsheep_,exmnURing_Doe_,exmnURing_Pig_,exmnUDirFwdCattle,exmnUDirFwd_Dogsheep_,exmnUDirFwdSwine,exmnUDirFwd_Bulldog_,exmnUDirFwd_Brownsheep_,exmnUDirFwd_Doe_,exmnUDirFwd_Pig_,exmnUIndFwdCattle,exmnUIndFwd_Dogsheep_,exmnUIndFwdSwine,exmnUIndFwd_Bulldog_,exmnUIndFwd_Brownsheep_,exmnUIndFwd_Doe_,exmnUIndFwd_Pig_,exmnUDirBackCattle,exmnUDirBack_Dogsheep_,exmnUDirBackSwine,exmnUDirBack_Bulldog_,exmnUDirBack_Brownsheep_,exmnUDirBack_Doe_,exmnUDirBack_Pig_,exmnUIndBackCattle,exmnUIndBack_Dogsheep_,exmnUIndBackSwine,exmnUIndBack_Bulldog_,exmnUIndBack_Brownsheep_,exmnUIndBack_Doe_,exmnUIndBack_Pig_,exmnUDetCattle,exmnUDet_Dogsheep_,exmnUDetSwine,exmnUDet_Bulldog_,exmnUDet_Brownsheep_,exmnUDet_Doe_,exmnUDet_Pig_,exmnAAll,exmnARing,exmnADirFwd,exmnAIndFwd,exmnADirBack,exmnAIndBack,exmnADet,exmnACattle,exmnA_Dogsheep_,exmnASwine,exmnA_Bulldog_,exmnA_Brownsheep_,exmnA_Doe_,exmnA_Pig_,exmnARingCattle,exmnARing_Dogsheep_,exmnARingSwine,exmnARing_Bulldog_,exmnARing_Brownsheep_,exmnARing_Doe_,exmnARing_Pig_,exmnADirFwdCattle,exmnADirFwd_Dogsheep_,exmnADirFwdSwine,exmnADirFwd_Bulldog_,exmnADirFwd_Brownsheep_,exmnADirFwd_Doe_,exmnADirFwd_Pig_,exmnAIndFwdCattle,exmnAIndFwd_Dogsheep_,exmnAIndFwdSwine,exmnAIndFwd_Bulldog_,exmnAIndFwd_Brownsheep_,exmnAIndFwd_Doe_,exmnAIndFwd_Pig_,exmnADirBackCattle,exmnADirBack_Dogsheep_,exmnADirBackSwine,exmnADirBack_Bulldog_,exmnADirBack_Brownsheep_,exmnADirBack_Doe_,exmnADirBack_Pig_,exmnAIndBackCattle,exmnAIndBack_Dogsheep_,exmnAIndBackSwine,exmnAIndBack_Bulldog_,exmnAIndBack_Brownsheep_,exmnAIndBack_Doe_,exmnAIndBack_Pig_,exmnADetCattle,exmnADet_Dogsheep_,exmnADetSwine,exmnADet_Bulldog_,exmnADet_Brownsheep_,exmnADet_Doe_,exmnADet_Pig_,exmcUAll,exmcURing,exmcUDirFwd,exmcUIndFwd,exmcUDirBack,exmcUIndBack,exmcUDet,exmcUCattle,exmcU_Dogsheep_,exmcUSwine,exmcU_Bulldog_,exmcU_Brownsheep_,exmcU_Doe_,exmcU_Pig_,exmcURingCattle,exmcURing_Dogsheep_,exmcURingSwine,exmcURing_Bulldog_,exmcURing_Brownsheep_,exmcURing_Doe_,exmcURing_Pig_,exmcUDirFwdCattle,exmcUDirFwd_Dogsheep_,exmcUDirFwdSwine,exmcUDirFwd_Bulldog_,exmcUDirFwd_Brownsheep_,exmcUDirFwd_Doe_,exmcUDirFwd_Pig_,exmcUIndFwdCattle,exmcUIndFwd_Dogsheep_,exmcUIndFwdSwine,exmcUIndFwd_Bulldog_,exmcUIndFwd_Brownsheep_,exmcUIndFwd_Doe_,exmcUIndFwd_Pig_,exmcUDirBackCattle,exmcUDirBack_Dogsheep_,exmcUDirBackSwine,exmcUDirBack_Bulldog_,exmcUDirBack_Brownsheep_,exmcUDirBack_Doe_,exmcUDirBack_Pig_,exmcUIndBackCattle,exmcUIndBack_Dogsheep_,exmcUIndBackSwine,exmcUIndBack_Bulldog_,exmcUIndBack_Brownsheep_,exmcUIndBack_Doe_,exmcUIndBack_Pig_,exmcUDetCattle,exmcUDet_Dogsheep_,exmcUDetSwine,exmcUDet_Bulldog_,exmcUDet_Brownsheep_,exmcUDet_Doe_,exmcUDet_Pig_,exmcAAll,exmcARing,exmcADirFwd,exmcAIndFwd,exmcADirBack,exmcAIndBack,exmcADet,exmcACattle,exmcA_Dogsheep_,exmcASwine,exmcA_Bulldog_,exmcA_Brownsheep_,exmcA_Doe_,exmcA_Pig_,exmcARingCattle,exmcARing_Dogsheep_,exmcARingSwine,exmcARing_Bulldog_,exmcARing_Brownsheep_,exmcARing_Doe_,exmcARing_Pig_,exmcADirFwdCattle,exmcADirFwd_Dogsheep_,exmcADirFwdSwine,exmcADirFwd_Bulldog_,exmcADirFwd_Brownsheep_,exmcADirFwd_Doe_,exmcADirFwd_Pig_,exmcAIndFwdCattle,exmcAIndFwd_Dogsheep_,exmcAIndFwdSwine,exmcAIndFwd_Bulldog_,exmcAIndFwd_Brownsheep_,exmcAIndFwd_Doe_,exmcAIndFwd_Pig_,exmcADirBackCattle,exmcADirBack_Dogsheep_,exmcADirBackSwine,exmcADirBack_Bulldog_,exmcADirBack_Brownsheep_,exmcADirBack_Doe_,exmcADirBack_Pig_,exmcAIndBackCattle,exmcAIndBack_Dogsheep_,exmcAIndBackSwine,exmcAIndBack_Bulldog_,exmcAIndBack_Brownsheep_,exmcAIndBack_Doe_,exmcAIndBack_Pig_,exmcADetCattle,exmcADet_Dogsheep_,exmcADetSwine,exmcADet_Bulldog_,exmcADet_Brownsheep_,exmcADet_Doe_,exmcADet_Pig_"
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

grammars = {'exp': [('c', 'n'), ('U', 'A'), ('', 'Dir', 'Ind', 'Air'), ('All', 'Cattle', 'Swine')]}

# <codecell>

matching_headers('etection')

# <codecell>

grammars['firstDetection'] = [('', 'Clin', 'Test'), ('', 'Cattle', 'Swine')]# 18 = 2*3*3

# <codecell>

matching_headers('det')

# <codecell>

print(2*2*3*3)  # There are two unnaccounted for in this set

# <codecell>

grammars['det'] = [('c', 'n'), ('U', 'A'), ('All', 'Clin', 'Test'), ('', 'Cattle', 'Swine')]

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

grammars['tr'] = [('n','c'), ('U', 'A'), ('All', 'Dir', 'Ind'), ('', 'Cattle', 'Swine'), ('', 'p')]  # 2*3*3*2
print(2*2*3*3*2)

# <codecell>

from itertools import product, combinations, permutations
list(product(('U', 'A'), ('All', 'Dir', 'Ind'), ('', 'Cattle', 'Swine')))

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

grammars['exm'] = [('n','c'), ('U','A'), ('All','Ring','DirFwd','IndFwd','DirBack','IndBack','Det'), ('','Cattle','Swine')]
print(2*2*7*3)

# <codecell>

combos = product(('n','c'), ('U','A'), ('All','Ring','DirFwd','IndFwd','DirBack','IndBack','Det'), ('','Cattle','Swine'))
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
grammars['tstnU'] = [('TruePos', 'FalsePos', 'TrueNeg','FalseNeg'), ('','Cattle','Swine')]  # first part only
grammars['tstcU'] = [('All', 'DirFwd','IndFwd','DirBack','IndBack', 'TruePos','FalsePos','TrueNeg','FalseNeg'), ('','Cattle','Swine')]  # direction and pos/neg are exclusive
grammars['tstcA'] = [('All','DirFwd','IndFwd','DirBack','IndBack'), ('','Cattle','Swine')]  # direction and pos/neg are exclusive

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

grammars['firstVaccination'] = [('','Ring'), ('','Cattle','Swine')]

# <headingcell level=2>

# vac Headers

# <codecell>

matching_headers('vacw')

# <markdowncell>

# This one defies grammar.  I'm just going to stick it in the model WaitGroup as is.

# <codecell>

grammars['vac'] = ['vacw', 'vacn', 'vacc']
grammars['vacw'] = [('U','A'), ('All','Max','MaxDay','TimeMax','TimeAvg','DaysInQueue'), ('','Cattle','Swine')]
grammars['vacn'] = [('U','A'), ('All','Ini','Ring'), ('','Cattle','Swine')]
grammars['vacc'] = [('U','A'), ('All','Ini','Ring'), ('','Cattle','Swine')]

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

grammars['firstDestruction'] = [('','Unsp','Ring','Det','Ini','DirFwd','IndFwd','DirBack','IndBack'), ('','Cattle','Swine')]
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

grammars['des'] = [('n','c'), ('U','A'), ('All','Unsp','Ring','Det','Ini','DirFwd','IndFwd','DirBack','IndBack'), ('','Cattle','Swine')]
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

grammars['tsd'] = [('U','A'), ('','Cattle','Swine'), ('Susc','Lat','Subc','Clin','NImm','VImm','Dest')]

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
PT = ('', 'Cattle', 'Swine')
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

matching_headers('inf')

# <codecell>

grammars['inf'] = [('c', 'n'),
 ('U', 'A'),
 ('', 'Ini', 'Dir', 'Ind', 'Air'),
 ('All', 'Cattle', 'Swine')]

# <codecell>


# <headingcell level=2>

# Column stability between Scenarios

# <codecell>

recent_headers = "Run,Day,outbreakDuration,zoneAreaHighRisk,zoneAreaMediumRisk,maxZoneAreaHighRisk,maxZoneAreaMediumRisk,maxZoneAreaDayHighRisk,maxZoneAreaDayMediumRisk,finalZoneAreaHighRisk,finalZoneAreaMediumRisk,zonePerimeterHighRisk,zonePerimeterMediumRisk,maxZonePerimeterHighRisk,maxZonePerimeterMediumRisk,maxZonePerimeterDayHighRisk,maxZonePerimeterDayMediumRisk,finalZonePerimeterHighRisk,finalZonePerimeterMediumRisk,num-separate-areasHighRisk,num-separate-areasMediumRisk,unitsInZoneHighRisk,unitsInZoneMediumRisk,unitsInZoneBackground,unitsInZoneHighRiskCattle,unitsInZoneHighRiskSwine,unitsInZoneMediumRiskCattle,unitsInZoneMediumRiskSwine,unitsInZoneBackgroundCattle,unitsInZoneBackgroundSwine,unitDaysInZoneHighRisk,unitDaysInZoneMediumRisk,unitDaysInZoneBackground,unitDaysInZoneHighRiskCattle,unitDaysInZoneHighRiskSwine,unitDaysInZoneMediumRiskCattle,unitDaysInZoneMediumRiskSwine,unitDaysInZoneBackgroundCattle,unitDaysInZoneBackgroundSwine,animalDaysInZoneHighRisk,animalDaysInZoneMediumRisk,animalDaysInZoneBackground,animalDaysInZoneHighRiskCattle,animalDaysInZoneHighRiskSwine,animalDaysInZoneMediumRiskCattle,animalDaysInZoneMediumRiskSwine,animalDaysInZoneBackgroundCattle,animalDaysInZoneBackgroundSwine,destrOccurred,firstDestruction,firstDestructionUnsp,firstDestructionRing,firstDestructionDirFwd,firstDestructionIndFwd,firstDestructionDirBack,firstDestructionIndBack,firstDestructionDet,firstDestructionIni,firstDestructionCattle,firstDestructionSwine,firstDestructionUnspCattle,firstDestructionUnspSwine,firstDestructionRingCattle,firstDestructionRingSwine,firstDestructionDirFwdCattle,firstDestructionDirFwdSwine,firstDestructionIndFwdCattle,firstDestructionIndFwdSwine,firstDestructionDirBackCattle,firstDestructionDirBackSwine,firstDestructionIndBackCattle,firstDestructionIndBackSwine,firstDestructionDetCattle,firstDestructionDetSwine,firstDestructionIniCattle,firstDestructionIniSwine,desnUAll,desnUIni,desnUUnsp,desnURing,desnUDirFwd,desnUIndFwd,desnUDirBack,desnUIndBack,desnUDet,desnUCattle,desnUSwine,desnUIniCattle,desnUIniSwine,desnUUnspCattle,desnUUnspSwine,desnURingCattle,desnURingSwine,desnUDirFwdCattle,desnUDirFwdSwine,desnUIndFwdCattle,desnUIndFwdSwine,desnUDirBackCattle,desnUDirBackSwine,desnUIndBackCattle,desnUIndBackSwine,desnUDetCattle,desnUDetSwine,descUAll,descUIni,descUUnsp,descURing,descUDirFwd,descUIndFwd,descUDirBack,descUIndBack,descUDet,descUCattle,descUSwine,descUIniCattle,descUIniSwine,descUUnspCattle,descUUnspSwine,descURingCattle,descURingSwine,descUDirFwdCattle,descUDirFwdSwine,descUIndFwdCattle,descUIndFwdSwine,descUDirBackCattle,descUDirBackSwine,descUIndBackCattle,descUIndBackSwine,descUDetCattle,descUDetSwine,desnAAll,desnAIni,desnAUnsp,desnARing,desnADirFwd,desnAIndFwd,desnADirBack,desnAIndBack,desnADet,desnACattle,desnASwine,desnAIniCattle,desnAIniSwine,desnAUnspCattle,desnAUnspSwine,desnARingCattle,desnARingSwine,desnADirFwdCattle,desnADirFwdSwine,desnAIndFwdCattle,desnAIndFwdSwine,desnADirBackCattle,desnADirBackSwine,desnAIndBackCattle,desnAIndBackSwine,desnADetCattle,desnADetSwine,descAAll,descAIni,descAUnsp,descARing,descADirFwd,descAIndFwd,descADirBack,descAIndBack,descADet,descACattle,descASwine,descAIniCattle,descAIniSwine,descAUnspCattle,descAUnspSwine,descARingCattle,descARingSwine,descADirFwdCattle,descADirFwdSwine,descAIndFwdCattle,descAIndFwdSwine,descADirBackCattle,descADirBackSwine,descAIndBackCattle,descAIndBackSwine,descADetCattle,descADetSwine,expnUAll,expnUDir,expnUInd,expnUAir,expnUCattle,expnUSwine,expnUDirCattle,expnUDirSwine,expnUIndCattle,expnUIndSwine,expnUAirCattle,expnUAirSwine,expcUAll,expcUDir,expcUInd,expcUAir,expcUCattle,expcUSwine,expcUDirCattle,expcUDirSwine,expcUIndCattle,expcUIndSwine,expcUAirCattle,expcUAirSwine,expnAAll,expnADir,expnAInd,expnAAir,expnACattle,expnASwine,expnADirCattle,expnADirSwine,expnAIndCattle,expnAIndSwine,expnAAirCattle,expnAAirSwine,expcAAll,expcADir,expcAInd,expcAAir,expcACattle,expcASwine,expcADirCattle,expcADirSwine,expcAIndCattle,expcAIndSwine,expcAAirCattle,expcAAirSwine,adqnUAll,adqcUAll,deswUAll,deswUCattle,deswUSwine,deswAAll,deswACattle,deswASwine,deswUMax,deswUMaxDay,deswAMax,deswAMaxDay,deswUTimeMax,deswUTimeAvg,deswUDaysInQueue,deswADaysInQueue,detOccurred,firstDetection,firstDetectionClin,firstDetectionTest,firstDetectionCattle,firstDetectionSwine,firstDetectionClinCattle,firstDetectionClinSwine,firstDetectionTestCattle,firstDetectionTestSwine,lastDetection,lastDetectionClin,lastDetectionTest,lastDetectionCattle,lastDetectionSwine,lastDetectionClinCattle,lastDetectionClinSwine,lastDetectionTestCattle,lastDetectionTestSwine,detnUAll,detnUClin,detnUTest,detnUCattle,detnUSwine,detnUClinCattle,detnUClinSwine,detnUTestCattle,detnUTestSwine,detnAAll,detnAClin,detnATest,detnACattle,detnASwine,detnAClinCattle,detnAClinSwine,detnATestCattle,detnATestSwine,detcUAll,detcUClin,detcUTest,detcUCattle,detcUSwine,detcUClinCattle,detcUClinSwine,detcUTestCattle,detcUTestSwine,detcUqAll,detcAAll,detcAClin,detcATest,detcACattle,detcASwine,detcAClinCattle,detcAClinSwine,detcATestCattle,detcATestSwine,trnUAllp,trnUDirp,trnUIndp,trnUCattlep,trnUSwinep,trnUDirCattlep,trnUDirSwinep,trnUIndCattlep,trnUIndSwinep,trcUAllp,trcUDirp,trcUIndp,trcUCattlep,trcUSwinep,trcUDirCattlep,trcUDirSwinep,trcUIndCattlep,trcUIndSwinep,trnUAll,trnUDir,trnUInd,trnUCattle,trnUSwine,trnUDirCattle,trnUDirSwine,trnUIndCattle,trnUIndSwine,trcUAll,trcUDir,trcUInd,trcUCattle,trcUSwine,trcUDirCattle,trcUDirSwine,trcUIndCattle,trcUIndSwine,trnAAllp,trnADirp,trnAIndp,trnACattlep,trnASwinep,trnADirCattlep,trnADirSwinep,trnAIndCattlep,trnAIndSwinep,trcAAllp,trcADirp,trcAIndp,trcACattlep,trcASwinep,trcADirCattlep,trcADirSwinep,trcAIndCattlep,trcAIndSwinep,trnAAll,trnADir,trnAInd,trnACattle,trnASwine,trnADirCattle,trnADirSwine,trnAIndCattle,trnAIndSwine,trcAAll,trcADir,trcAInd,trcACattle,trcASwine,trcADirCattle,trcADirSwine,trcAIndCattle,trcAIndSwine,tstnUTruePos,tstnUTruePosCattle,tstnUTruePosSwine,tstnUTrueNeg,tstnUTrueNegCattle,tstnUTrueNegSwine,tstnUFalsePos,tstnUFalsePosCattle,tstnUFalsePosSwine,tstnUFalseNeg,tstnUFalseNegCattle,tstnUFalseNegSwine,tstcUAll,tstcUDirFwd,tstcUIndFwd,tstcUDirBack,tstcUIndBack,tstcUCattle,tstcUSwine,tstcUDirFwdCattle,tstcUDirFwdSwine,tstcUIndFwdCattle,tstcUIndFwdSwine,tstcUDirBackCattle,tstcUDirBackSwine,tstcUIndBackCattle,tstcUIndBackSwine,tstcUTruePos,tstcUTruePosCattle,tstcUTruePosSwine,tstcUTrueNeg,tstcUTrueNegCattle,tstcUTrueNegSwine,tstcUFalsePos,tstcUFalsePosCattle,tstcUFalsePosSwine,tstcUFalseNeg,tstcUFalseNegCattle,tstcUFalseNegSwine,tstcAAll,tstcADirFwd,tstcAIndFwd,tstcADirBack,tstcAIndBack,tstcACattle,tstcASwine,tstcADirFwdCattle,tstcADirFwdSwine,tstcAIndFwdCattle,tstcAIndFwdSwine,tstcADirBackCattle,tstcADirBackSwine,tstcAIndBackCattle,tstcAIndBackSwine,vacwUAll,vacwUCattle,vacwUSwine,vacwAAll,vacwACattle,vacwASwine,vacwUMax,vacwUMaxDay,vacwAMax,vacwAMaxDay,vacwUTimeMax,vacwUTimeAvg,vacwUDaysInQueue,vacwADaysInQueue,infnUAll,infnUDir,infnUInd,infnUAir,infnUIni,infnUCattle,infnUSwine,infnUDirCattle,infnUDirSwine,infnUIndCattle,infnUIndSwine,infnUAirCattle,infnUAirSwine,infnUIniCattle,infnUIniSwine,infcUAll,infcUDir,infcUInd,infcUAir,infcUIni,infcUCattle,infcUSwine,infcUDirCattle,infcUDirSwine,infcUIndCattle,infcUIndSwine,infcUAirCattle,infcUAirSwine,infcUIniCattle,infcUIniSwine,infnAAll,infnADir,infnAInd,infnAAir,infnAIni,infnACattle,infnASwine,infnADirCattle,infnADirSwine,infnAIndCattle,infnAIndSwine,infnAAirCattle,infnAAirSwine,infnAIniCattle,infnAIniSwine,infcAAll,infcADir,infcAInd,infcAAir,infcAIni,infcACattle,infcASwine,infcADirCattle,infcADirSwine,infcAIndCattle,infcAIndSwine,infcAAirCattle,infcAAirSwine,infcAIniCattle,infcAIniSwine,firstDetUInfAll,firstDetAInfAll,ratio,vaccOccurred,firstVaccination,firstVaccinationRing,firstVaccinationCattle,firstVaccinationSwine,firstVaccinationRingCattle,firstVaccinationRingSwine,vacnUAll,vacnUIni,vacnURing,vacnUCattle,vacnUSwine,vacnUIniCattle,vacnUIniSwine,vacnURingCattle,vacnURingSwine,vaccUAll,vaccUIni,vaccURing,vaccUCattle,vaccUSwine,vaccUIniCattle,vaccUIniSwine,vaccURingCattle,vaccURingSwine,vacnAAll,vacnAIni,vacnARing,vacnACattle,vacnASwine,vacnAIniCattle,vacnAIniSwine,vacnARingCattle,vacnARingSwine,vaccAAll,vaccAIni,vaccARing,vaccACattle,vaccASwine,vaccAIniCattle,vaccAIniSwine,vaccARingCattle,vaccARingSwine,tsdUSusc,tsdULat,tsdUSubc,tsdUClin,tsdUNImm,tsdUVImm,tsdUDest,tsdUCattleSusc,tsdUCattleLat,tsdUCattleSubc,tsdUCattleClin,tsdUCattleNImm,tsdUCattleVImm,tsdUCattleDest,tsdUSwineSusc,tsdUSwineLat,tsdUSwineSubc,tsdUSwineClin,tsdUSwineNImm,tsdUSwineVImm,tsdUSwineDest,tsdASusc,tsdALat,tsdASubc,tsdAClin,tsdANImm,tsdAVImm,tsdADest,tsdACattleSusc,tsdACattleLat,tsdACattleSubc,tsdACattleClin,tsdACattleNImm,tsdACattleVImm,tsdACattleDest,tsdASwineSusc,tsdASwineLat,tsdASwineSubc,tsdASwineClin,tsdASwineNImm,tsdASwineVImm,tsdASwineDest,average-prevalence,diseaseDuration,exmnUAll,exmnURing,exmnUDirFwd,exmnUIndFwd,exmnUDirBack,exmnUIndBack,exmnUDet,exmnUCattle,exmnUSwine,exmnURingCattle,exmnURingSwine,exmnUDirFwdCattle,exmnUDirFwdSwine,exmnUIndFwdCattle,exmnUIndFwdSwine,exmnUDirBackCattle,exmnUDirBackSwine,exmnUIndBackCattle,exmnUIndBackSwine,exmnUDetCattle,exmnUDetSwine,exmnAAll,exmnARing,exmnADirFwd,exmnAIndFwd,exmnADirBack,exmnAIndBack,exmnADet,exmnACattle,exmnASwine,exmnARingCattle,exmnARingSwine,exmnADirFwdCattle,exmnADirFwdSwine,exmnAIndFwdCattle,exmnAIndFwdSwine,exmnADirBackCattle,exmnADirBackSwine,exmnAIndBackCattle,exmnAIndBackSwine,exmnADetCattle,exmnADetSwine,exmcUAll,exmcURing,exmcUDirFwd,exmcUIndFwd,exmcUDirBack,exmcUIndBack,exmcUDet,exmcUCattle,exmcUSwine,exmcURingCattle,exmcURingSwine,exmcUDirFwdCattle,exmcUDirFwdSwine,exmcUIndFwdCattle,exmcUIndFwdSwine,exmcUDirBackCattle,exmcUDirBackSwine,exmcUIndBackCattle,exmcUIndBackSwine,exmcUDetCattle,exmcUDetSwine,exmcAAll,exmcARing,exmcADirFwd,exmcAIndFwd,exmcADirBack,exmcAIndBack,exmcADet,exmcACattle,exmcASwine,exmcARingCattle,exmcARingSwine,exmcADirFwdCattle,exmcADirFwdSwine,exmcAIndFwdCattle,exmcAIndFwdSwine,exmcADirBackCattle,exmcADirBackSwine,exmcAIndBackCattle,exmcAIndBackSwine,exmcADetCattle,exmcADetSwine".split(',')
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

successes= ['expnUDirCattle', 'detnUAll', 'trnUDirSwinep', 'tstnUTruePosSwine', 'exmnADirBack', 'trnADir', 'expnAIndSwine', 'exmnUDirBackCattle', 'trnAIndSwine', 'expnUInd', 'exmnURingCattle', 'vacnAIni', 'animalDaysInZoneMediumRiskCattle', 'exmnUDetCattle', 'trnUIndCattle', 'unitsInZoneMediumRiskSwine', 'detnUClin', 'deswADaysInQueue', 'exmnUIndFwd', 'animalDaysInZoneMediumRiskSwine', 'trnUDirCattlep', 'detnATestCattle', 'tstnUFalseNeg', 'tstnUTruePos', 'trnAAllp', 'vaccOccurred', 'expnUDirSwine', 'exmnAIndFwd', 'infnADir', 'detnUClinCattle', 'infnAAir', 'infnAIndSwine', 'exmnADetCattle', 'exmnUDirBackSwine', 'destrOccurred', 'trnAInd', 'exmnADirFwdCattle', 'infnUInd', 'expnAInd', 'trnUIndp', 'exmnADirFwdSwine', 'num-separate-areasHighRisk', 'infnADirSwine', 'detnUClinSwine', 'average-prevalence', 'exmnUIndBack', 'infnUDirSwine', 'trnUInd', 'infnAInd', 'infnUIndSwine', 'infnUAir', 'zonePerimeterHighRisk', 'expnUAir', 'exmnUIndFwdCattle', 'trnUDirp', 'adqcUAll', 'exmnUDetSwine', 'vacwUMax', 'unitDaysInZoneMediumRiskSwine', 'trnUIndCattlep', 'expnUIndCattle', 'vacnUIniSwine', 'exmnAAll', 'vacnAAll', 'unitsInZoneHighRiskSwine', 'vacwADaysInQueue', 'tstnUFalsePosSwine', 'exmnADirBackCattle', 'trnUIndSwinep', 'trnADirCattlep', 'maxZonePerimeterMediumRisk', 'vacnARingCattle', 'detnUTestSwine', 'animalDaysInZoneHighRiskSwine', 'trnUAll', 'exmnADet', 'infnUAirCattle', 'trnAIndSwinep', 'unitDaysInZoneHighRiskSwine', 'trnUDir', 'trnAIndCattlep', 'detnATestSwine', 'detOccurred', 'vacnURing', 'exmnUIndBackSwine', 'animalDaysInZoneMediumRisk', 'num-separate-areasMediumRisk', 'trnADirSwine', 'animalDaysInZoneHighRisk', 'detcUqAll', 'unitsInZoneBackgroundSwine', 'infnUAll', 'detnAClinCattle', 'expnAAll', 'expnUIndSwine', 'animalDaysInZoneHighRiskCattle', 'vacnUIniCattle', 'zonePerimeterMediumRisk', 'trnAIndp', 'tstnUTruePosCattle', 'exmnUAll', 'infnAAirCattle', 'vacnUAll', 'exmnUDet', 'exmnADirBackSwine', 'vacnUIni', 'exmnUIndFwdSwine', 'trnUDirCattle', 'unitsInZoneBackground', 'expnUAirCattle', 'detnUTest', 'vacnAIniCattle', 'trnUAllp', 'infnUDir', 'unitDaysInZoneBackground', 'vacnARingSwine', 'exmnARingCattle', 'zoneAreaHighRisk', 'exmnADirFwd', 'unitDaysInZoneMediumRiskCattle', 'exmnAIndBack', 'expnUAirSwine', 'maxZonePerimeterHighRisk', 'infnAIndCattle', 'exmnARingSwine', 'vacwUDaysInQueue', 'unitDaysInZoneBackgroundCattle', 'vacnARing', 'unitDaysInZoneHighRisk', 'expnAAir', 'expnUAll', 'infnUIndCattle', 'deswAMax', 'expnUDir', 'exmnAIndBackSwine', 'exmnURing', 'unitDaysInZoneBackgroundSwine', 'infnADirCattle', 'animalDaysInZoneBackground', 'unitDaysInZoneHighRiskCattle', 'trnADirCattle', 'unitsInZoneMediumRisk', 'exmnUDirBack', 'expnAAirCattle', 'trnADirSwinep', 'unitsInZoneBackgroundCattle', 'exmnAIndFwdCattle', 'trnUDirSwine', 'tstnUFalseNegCattle', 'unitsInZoneHighRisk', 'exmnUDirFwd', 'infnAAll', 'expnAAirSwine', 'adqnUAll', 'animalDaysInZoneBackgroundCattle', 'animalDaysInZoneBackgroundSwine', 'detnAAll', 'tstnUTrueNegCattle', 'detnATest', 'tstnUFalseNegSwine', 'trnAIndCattle', 'exmnUIndBackCattle', 'vacnURingSwine', 'exmnUDirFwdSwine', 'expnADirSwine', 'exmnADetSwine', 'vacwAMax', 'trnUIndSwine', 'infnUDirCattle', 'expnAIndCattle', 'exmnARing', 'maxZoneAreaMediumRisk', 'tstnUFalsePos', 'maxZoneAreaHighRisk', 'trnAAll', 'deswUDaysInQueue', 'unitsInZoneHighRiskCattle', 'detnAClinSwine', 'trnADirp', 'deswUMax', 'exmnAIndFwdSwine', 'exmnUDirFwdCattle', 'zoneAreaMediumRisk', 'infnAAirSwine', 'unitDaysInZoneMediumRisk', 'expnADirCattle', 'expnADir', 'detnAClin', 'exmnAIndBackCattle', 'vacnURingCattle', 'tstnUTrueNeg', 'tstnUFalsePosCattle', 'tstnUTrueNegSwine', 'infnUAirSwine', 'vacnAIniSwine', 'exmnURingSwine', 'detnUTestCattle', 'unitsInZoneMediumRiskCattle']
failures= ['infnUIniCattle', 'infnAIniSwine', 'infnAIni', 'infnUIni', 'infnAIniCattle', 'infnUIniSwine']

print(len(successes), len(failures))

# <codecell>

import copy
grammar_backup = copy.deepcopy(grammars)

# <codecell>

sorted(grammars.keys())

# <codecell>

DailyByZoneAndProductionType = {'animalDaysInZone':grammars['animalDaysInZone'], 'unitDaysInZone': grammars['unitDaysInZone'], 'unitsInZone':grammars['unitsInZone']}

# <codecell>

del grammars['animalDaysInZone']
del grammars['unitDaysInZone']
del grammars['unitsInZone']
grammars

# <codecell>

sorted(grammars.keys())

# <codecell>

grammars['lastDetection'] = grammars['firstDetection']

# <codecell>

grammars['tst']

# <markdowncell>

# We'll want to delete the Production Type tuple from the grammar for generation.  We already know everything inside grammars pertains solely to DailyByProductionType.

# <codecell>

[(key, grammars[key]) for key in ['tstnU', 'tstcU', 'tstcA']]

# <codecell>

del grammars['tst']

# <codecell>

grammars['vac']

# <codecell>

[(key, grammars[key]) for key in ['vacw', 'vacn', 'vacc']]

# <codecell>

del grammars['vac']

# <codecell>

grammars['inf'] = grammars['exp']

# <codecell>

sorted(grammars.keys())

# <headingcell level=1>

# Generating a new Flat DailyByProductionType

# <codecell>

sorted(explain.keys())

# <codecell>

explain.update({
 'des':'Destruction',
 'desw': 'Destruction Wait Time',
 'det': 'Detection',
 'exm': 'Examination',
 'exp': 'Exposure',
 'firstDestruction': "First Destruction",
 'firstDetection': "First Detection",
 'firstVaccination': 'First Vaccination',
 'lastDetection': "Last Detection",
 'tr': 'Trace',
 'tsd': 'Transition State Daily',
 'tstcA': 'Lab Test Cumulative Animals',
 'tstcU': 'Lab Test Cumulative Units',
 'tstnU': 'Lab Test New Units',
 'vacc': 'Vaccination Cumulative',
 'vacn': 'Vaccination New',
 'vacw': 'Vaccination Wait Time'
})

# <codecell>

explain['inf'] = 'Infection'

# <codecell>

grammars['vacw']

# <codecell>

explain.update({
'All': 'For Any Reason', 
'Max': 'Max', 
'MaxDay': 'Day with Max', 
'TimeMax': 'Max Time', 
'TimeAvg': 'Average Time', 
'DaysInQueue': 'Days in Queue'
})

# <codecell>

PT_All = ('All', 'Cattle', 'Swine')

# <codecell>

def flat_stat_code(prefix, grammar):
    combos = product([prefix], *grammar)
    for line in combos:
        explanation = ' '.join([explain[part] for part in line])
        print_line = '    '+''.join(line)+ ' = models.IntegerField(blank=True, null=True, verbose_name="'+explanation+'")'
        print(re.sub(r'(\w)  (\w)', r'\1 \2', print_line))

# <codecell>

def generate_grammar_code(grammars=grammars):
    for key in sorted(grammars.keys()): # Alphabetical order keeps it nicely sorted except firstDetection and lastDetection
        field_grammar = copy.deepcopy(grammars[key]) # we don't want to side effect this
        try: field_grammar.remove(PT_All)
        except: pass
        try: field_grammar.remove(PT)
        except: pass
        flat_stat_code(key, field_grammar)

# <codecell>

DailyByZoneAndProductionType

# <codecell>


# <codecell>

#failures 4
#['expnAAll', 'expnUAll', 'infnAAll', 'infnUAll']
[x for x in combo_set('exp') if 'expnUAll' in x]

# <codecell>

matching_headers('desw')

# <markdowncell>

# Looks like there's a minor problem with desw expecting production type breakdown

# <codecell>

grammars['desw'] = [('U', 'A'),
 ('All', 'Cattle', 'Swine')]

# <codecell>

DailyControls = {'desw': [('U', 'A'),
 ('Max', 'MaxDay', 'TimeMax', 'TimeAvg', 'DaysInQueue'),]}

# <codecell>

generate_grammar_code()

# <codecell>

generate_grammar_code(DailyControls)

# <codecell>

matching_headers('tsdU')

# <markdowncell>

# This is a problem because the prodution type is inserted in the middle.  Solution: replace PT and PT_all with an underscores, then instead of appending the production type, replace('_', pt)

# <markdowncell>

# Wait, that won't work because Django forbids trailing underscores in field names.

# <codecell>

matching_headers('-')

# <codecell>

[x for x in cause_sweep if '-' in x]

# <codecell>

matching_headers('vacwADaysInQueue')

# <codecell>

dailyControls = '''diseaseDuration
adqnUAll
adqcUAll
detOccurred
costSurveillance
vaccOccurred
vacwUDaysInQueue
vacwUTimeAvg
vacwUTimeMax
vacwADaysInQueue
vaccSetup
vaccVaccination
vaccSubtotal
destrOccurred
deswUMax
deswUMaxDay
deswUTimeMax
deswUTimeAvg
deswUDaysInQueue
deswAMax
deswAMaxDay
deswATimeMax
deswATimeAvg
deswADaysInQueue
destrAppraisal
destrEuthanasia
destrIndemnification
destrDisposal
destrCleaning
destrSubtotal
outbreakDuration
costsTotal
firstDetUInfAll
firstDetAInfAll
ratio
average_prevalence
detcUqAll'''.split()
dailyPT = '''desnUAll
desnUUnsp
desnURing
desnUDet
desnUIni
desnUDirFwd
desnUIndFwd
desnUDirBack
desnUIndBack
desnAAll
desnAUnsp
desnARing
desnADet
desnAIni
desnADirFwd
desnAIndFwd
desnADirBack
desnAIndBack
descUAll
descUUnsp
descURing
descUDet
descUIni
descUDirFwd
descUIndFwd
descUDirBack
descUIndBack
descAAll
descAUnsp
descARing
descADet
descAIni
descADirFwd
descAIndFwd
descADirBack
descAIndBack
deswU
deswA
detcUAll
detcUClin
detcUTest
detcAAll
detcAClin
detcATest
detnUAll
detnUClin
detnUTest
detnAAll
detnAClin
detnATest
exmnUAll
exmnURing
exmnUDirFwd
exmnUIndFwd
exmnUDirBack
exmnUIndBack
exmnUDet
exmnAAll
exmnARing
exmnADirFwd
exmnAIndFwd
exmnADirBack
exmnAIndBack
exmnADet
exmcUAll
exmcURing
exmcUDirFwd
exmcUIndFwd
exmcUDirBack
exmcUIndBack
exmcUDet
exmcAAll
exmcARing
exmcADirFwd
exmcAIndFwd
exmcADirBack
exmcAIndBack
exmcADet
expcU
expcUDir
expcUInd
expcUAir
expcA
expcADir
expcAInd
expcAAir
expnU
expnUDir
expnUInd
expnUAir
expnA
expnADir
expnAInd
expnAAir
firstDestruction
firstDestructionUnsp
firstDestructionRing
firstDestructionDet
firstDestructionIni
firstDestructionDirFwd
firstDestructionIndFwd
firstDestructionDirBack
firstDestructionIndBack
firstDetection
firstDetectionClin
firstDetectionTest
firstVaccination
firstVaccinationRing
infcU
infcUIni
infcUDir
infcUInd
infcUAir
infcA
infcAIni
infcADir
infcAInd
infcAAir
infnU
infnUIni
infnUDir
infnUInd
infnUAir
infnA
infnAIni
infnADir
infnAInd
infnAAir
lastDetection
lastDetectionClin
lastDetectionTest
trnUAll
trnUAllp
trnUDir
trnUDirp
trnUInd
trnUIndp
trnAAll
trnAAllp
trnADir
trnADirp
trnAInd
trnAIndp
trcUAll
trcUAllp
trcUDir
trcUDirp
trcUInd
trcUIndp
trcAAll
trcAAllp
trcADir
trcADirp
trcAInd
trcAIndp
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
tstcAAll
tstcADirFwd
tstcAIndFwd
tstcADirBack
tstcAIndBack
tstcUAll
tstcUDirFwd
tstcUIndFwd
tstcUDirBack
tstcUIndBack
tstcUTruePos
tstcUFalsePos
tstcUTrueNeg
tstcUFalseNeg
tstnUTruePos
tstnUFalsePos
tstnUTrueNeg
tstnUFalseNeg
vaccUAll
vaccUIni
vaccURing
vaccAAll
vaccAIni
vaccARing
vacnUAll
vacnUIni
vacnURing
vacnAAll
vacnAIni
vacnARing
vacwUAll
vacwUMax
vacwUMaxDay
vacwUTimeMax
vacwUTimeAvg
vacwUDaysInQueue
vacwAAll
vacwAMax
vacwAMaxDay
vacwATimeMax
vacwATimeAvg
vacwADaysInQueue'''.split()
len(dailyPT)

# <codecell>

[c for c in dailyControls if c in dailyPT]

# <codecell>

[(key, value) for key, value in grammars.items() if PT_All in value]

# <codecell>

grammars['exp'] = [('c', 'n'),
 ('U', 'A'),
 ('', 'Dir', 'Ind', 'Air'),
 ('', 'Cattle', 'Swine')]

# <codecell>

[x for x in '''expnUAll
expnUDir
expnUInd
expnUAir
expnUCattle
expnUSwine
expnUDirCattle
expnUDirSwine
expnUIndCattle
expnUIndSwine
expnUAirCattle
expnUAirSwine
expcUAll
expcUDir
expcUInd
expcUAir
expcUCattle
expcUSwine
expcUDirCattle
expcUDirSwine
expcUIndCattle
expcUIndSwine
expcUAirCattle
expcUAirSwine
expnAAll
expnADir
expnAInd
expnAAir
expnACattle
expnASwine
expnADirCattle
expnADirSwine
expnAIndCattle
expnAIndSwine
expnAAirCattle
expnAAirSwine
expcAAll
expcADir
expcAInd
expcAAir
expcACattle
expcASwine
expcADirCattle
expcADirSwine
expcAIndCattle
expcAIndSwine
expcAAirCattle
expcAAirSwine'''.split() if 'All' in x]

# <codecell>

[x for x in cause_sweep if 'Unit' in x ]

# <codecell>

'asdhjk, asdajk, asda\r\n'.strip()
