from django.db import models
from ScenarioCreator.models import InProductionType, InZone, DynamicUnit


class OutDailyByProductionType(models.Model):
    iteration = models.IntegerField(blank=True, null=True,
        help_text='The iteration during which the outputs in this records where generated.', )
    production_type = models.ForeignKey(InProductionType,
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


class OutDailyByZone(models.Model):
    iteration = models.IntegerField(blank=True, null=True,
        help_text='The iteration during which the outputs in this records where generated.', )
    day = models.IntegerField(blank=True, null=True,
        help_text='The day within the iteration on which these outputs were generated.', )
    zone = models.ForeignKey(InZone,
        help_text='Identifier of the zone for which this event occurred.', )
    zone_area = models.FloatField(blank=True, null=True,
        help_text='In square Kilometers', )
    zone_perimeter = models.FloatField(blank=True, null=True,
        help_text='In Kilometers', )


class OutDailyByZoneAndProductionType(models.Model):
    iteration = models.IntegerField(blank=True, null=True,
        help_text='The iteration during which the outputs in this records where generated.', )
    day = models.IntegerField(blank=True, null=True,
        help_text='The day within the iteration on which these outputs were generated.', )
    zone = models.ForeignKey(InZone,
        help_text='Identifier of the zone for which this event occurred.', )
    production_type = models.ForeignKey(InProductionType,
        help_text='The identifier of the production type that these outputs apply to.', )
    unit_days_in_zone = models.IntegerField(blank=True, null=True,
        help_text='Total number of unit days spent in a zone (1 unit for 1 day = 1 unit day 1 unit for 2 days = 2 unit days etc.)', )
    animal_days_in_zone = models.IntegerField(blank=True, null=True,
        help_text='Total number of animal days spent in a zone (1 animal for 1 day = 1 animal day 1 animal for 2 days = 2 animal days etc.)', )
    units_in_zone = models.IntegerField(blank=True, null=True,
        help_text='Number of units of the given production type in the zone', )
    animals_in_zone = models.IntegerField(blank=True, null=True,
        help_text='Count of animals of the given production type in the zone', )


class OutDailyEvents(models.Model):
    iteration = models.IntegerField(blank=True, null=True,
        help_text='The iteration during which the outputs in this records where generated.', )
    day = models.IntegerField(blank=True, null=True,
        help_text='The day within the iteration on which these outputs were generated.', )
    event = models.IntegerField(blank=True, null=True,
        help_text='A number used to identify each event.', )
    unit = models.ForeignKey(DynamicUnit,
        help_text='Identifier of the unit for which this event occurred.', )
    zone = models.ForeignKey(InZone,
        help_text='Identifier of the zone for which this event occurred.', )
    event_code = models.CharField(max_length=255, blank=True,
        help_text='Code to indicate the type of event.', )
    new_state_code = models.CharField(max_length=255, blank=True,
        help_text='For transition state changesthis field indicates the state that results from the event.', )
    test_result_code = models.CharField(max_length=255, blank=True,
        help_text='For trace events this field indicates if the attempted trace succeeded.', )


class OutDailyExposures(models.Model):
    iteration = models.IntegerField(blank=True, null=True,
        help_text='The iteration during which the outputs in this records where generated.', )
    day = models.IntegerField(blank=True, null=True,
        help_text='The day within the iteration on which these outputs were generated.', )
    exposure = models.IntegerField(blank=True, null=True,
        help_text='An identifier of each exposure.', )
    initiated_day = models.IntegerField(blank=True, null=True,
        help_text='', )
    exposed_unit = models.ForeignKey(DynamicUnit, related_name='events_where_unit_was_exposed',
        help_text='The identifier of the source unit for the exposure.', )
    exposed_zone = models.ForeignKey(InZone, related_name='events_that_exposed_this_zone',
        help_text='The identifier of the zone of the source unit for the exposure.', )
    exposing_unit = models.ForeignKey(DynamicUnit, related_name='events_where_unit_exposed_others',
        help_text='The identifier of the recipient unit for the exposure.', )
    exposing_zone = models.ForeignKey(InZone, related_name='events_that_exposed_others',
        help_text='The identifier of the zone of the recipient unit for the exposure.', )
    spread_method_code = models.CharField(max_length=255, blank=True,
        help_text='Code indicating the mechanism of the disease spread.', )
    is_adequate = models.NullBooleanField(blank=True, null=True,
        help_text='Indicator if the exposure was adequate to transmit dieases.', )  # Changed Booleans to NullBooleans so as not to restrict output
    exposing_unit_status_code = models.CharField(max_length=255, blank=True,
        help_text='Disease state of the exposing unit when the exposure occurred.', )
    exposed_unit_status_code = models.CharField(max_length=255, blank=True,
        help_text='Disease state of the exposed unit when the exposure occurred.', )


class OutEpidemicCurves(models.Model):
    iteration = models.IntegerField(blank=True, null=True,
        help_text='The iteration during which the outputs in this records where generated.', )
    day = models.IntegerField(blank=True, null=True,
        help_text='The day within the iteration on which these outputs were generated.', )
    production_type = models.ForeignKey(InProductionType,
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


class OutGeneral(models.Model):
    simulation_start_time = models.DateTimeField(max_length=255, blank=True,
        help_text='The actual clock time according to the system clock of when the simulation started.', )
    simulation_end_time = models.DateTimeField(max_length=255, blank=True,
        help_text='The actual clock time according to the system clock of when the simulation ended.', )
    completed_iterations = models.IntegerField(blank=True, null=True,
        help_text='Number of iterations completed during the simulation run.', )
    version = models.CharField(max_length=255, blank=True,
        help_text='Number of the NAADSM Version used to run the simulation.', )


class OutIteration(models.Model):
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


class OutIterationByUnit(models.Model):
    iteration = models.IntegerField(blank=True, null=True,
        help_text='The iteration during which the outputs in this records where generated.', )
    unit = models.ForeignKey(DynamicUnit,
        help_text='Identifier of the unit for which this event occurred.', )
    last_status_code = models.CharField(max_length=255, blank=True,
        help_text='Final status that a unit was in for an iteration', )
    last_status_day = models.IntegerField(blank=True, null=True,
        help_text='Day that a unit was in the final status for an iteration', )
    last_control_state_code = models.CharField(max_length=255, blank=True,
        help_text='Final Control State that a unit was in for an iteration', )
    last_control_state_day = models.IntegerField(blank=True, null=True,
        help_text='Day that a unit went in to the final status for an iteration', )


class OutIterationByProductionType(models.Model):
    iteration = models.IntegerField(blank=True, null=True,
        help_text='The iteration during which the outputs in this records where generated.', )
    production_type = models.ForeignKey(InProductionType,
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
    zone_foci = models.IntegerField(blank=True, null=True)
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


class OutIterationByZone(models.Model):
    iteration = models.IntegerField(blank=True, null=True,
        help_text='The iteration during which the outputs in this records where generated.', )
    zone = models.ForeignKey(InZone,
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


class OutIterationByZoneAndProductionType(models.Model):
    iteration = models.IntegerField(blank=True, null=True,
        help_text='The iteration during which the outputs in this records where generated.', )
    zone = models.ForeignKey(InZone,
        help_text='Identifier of the zone for which this event occurred.', )
    production_type = models.ForeignKey(InProductionType,
        help_text='The identifier of the production type that these outputs apply to.', )
    unit_days_in_zone = models.IntegerField(blank=True, null=True,
        help_text='Total number of unit days spent in a zone (1 unit for 1 day = 1 unit day 1 unit for 2 days = 2 unit days etc.)', )
    animal_days_in_zone = models.IntegerField(blank=True, null=True,
        help_text='Total number of animal days spent in a zone (1 animal for 1 day = 1 animal day 1 animal for 2 days = 2 animal days etc.)', )
    cost_surveillance = models.FloatField(blank=True, null=True,
        help_text='Total cost associated with surveillance in a zone over the course of an iteration.', )


class OutIterationCosts(models.Model):
    iteration = models.IntegerField(blank=True, null=True,
        help_text='The iteration during which the outputs in this records where generated.', )
    production_type = models.ForeignKey(InProductionType,
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



