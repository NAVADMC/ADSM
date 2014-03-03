from django.db import models
from ScenarioCreator.models import InProductionType, InZone, DynamicUnit


class Outdailybyproductiontype(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    production_type = models.ForeignKey(InProductionType)
    day = models.IntegerField(blank=True, null=True)
    transition_state_daily_unit_susceptible = models.IntegerField(blank=True, null=True)
    transition_state_daily_animal_susceptible = models.IntegerField(blank=True, null=True)
    transition_state_daily_unit_latent = models.IntegerField(blank=True, null=True)
    transition_state_daily_animal_latent = models.IntegerField(blank=True, null=True)
    transition_state_daily_unit_subclinical = models.IntegerField(blank=True, null=True)
    transition_state_daily_animal_subclinical = models.IntegerField(blank=True, null=True)
    transition_state_daily_unit_clinical = models.IntegerField(blank=True, null=True)
    transition_state_daily_animal_clinical = models.IntegerField(blank=True, null=True)
    transition_state_daily_unit_nat_immune = models.IntegerField(blank=True, null=True)
    transition_state_daily_animal_nat_immune = models.IntegerField(blank=True, null=True)
    transition_state_daily_unit_vac_immune = models.IntegerField(blank=True, null=True)
    transition_state_daily_animal_vac_immune = models.IntegerField(blank=True, null=True)
    transition_state_daily_unit_destroyed = models.IntegerField(blank=True, null=True)
    transition_state_daily_animal_destroyed = models.IntegerField(blank=True, null=True)
    transition_state_cum_unit_susceptible = models.IntegerField(blank=True, null=True)
    transition_state_cum_animal_susceptible = models.IntegerField(blank=True, null=True)
    transition_state_cum_unit_latent = models.IntegerField(blank=True, null=True)
    transition_state_cum_animal_latent = models.IntegerField(blank=True, null=True)
    transition_state_cum_unit_subclinical = models.IntegerField(blank=True, null=True)
    transition_state_cum_animal_subclinical = models.IntegerField(blank=True, null=True)
    transition_state_cum_unit_clinical = models.IntegerField(blank=True, null=True)
    transition_state_cum_animal_clinical = models.IntegerField(blank=True, null=True)
    transition_state_cum_unit_nat_immune = models.IntegerField(blank=True, null=True)
    transition_state_cum_animal_nat_immune = models.IntegerField(blank=True, null=True)
    transition_state_cum_unit_vac_immune = models.IntegerField(blank=True, null=True)
    transition_state_cum_animal_vac_immune = models.IntegerField(blank=True, null=True)
    transition_state_cum_unit_destroyed = models.IntegerField(blank=True, null=True)
    transition_state_cum_animal_destroyed = models.IntegerField(blank=True, null=True)
    infection_new_unit_air = models.IntegerField(blank=True, null=True)
    infection_new_animal_air = models.IntegerField(blank=True, null=True)
    infection_new_unit_dir = models.IntegerField(blank=True, null=True)
    infection_new_animal_dir = models.IntegerField(blank=True, null=True)
    infection_new_unit_ind = models.IntegerField(blank=True, null=True)
    infection_new_animal_ind = models.IntegerField(blank=True, null=True)
    infection_cum_unit_initial = models.IntegerField(blank=True, null=True)
    infection_cum_animal_initial = models.IntegerField(blank=True, null=True)
    infection_cum_unit_air = models.IntegerField(blank=True, null=True)
    infection_cum_animal_air = models.IntegerField(blank=True, null=True)
    infection_cum_unit_dir = models.IntegerField(blank=True, null=True)
    infection_cum_animal_dir = models.IntegerField(blank=True, null=True)
    infection_cum_unit_ind = models.IntegerField(blank=True, null=True)
    infection_cum_animal_ind = models.IntegerField(blank=True, null=True)
    exposed_cum_unit_dir = models.IntegerField(blank=True, null=True)
    exposed_cum_animal_dir = models.IntegerField(blank=True, null=True)
    exposed_cum_unit_ind = models.IntegerField(blank=True, null=True)
    exposed_cum_animal_ind = models.IntegerField(blank=True, null=True)
    trace_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True)
    trace_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True)
    trace_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True)
    trace_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True)
    trace_cum_unit_dir_p_fwd = models.IntegerField(blank=True, null=True)
    trace_cum_animal_dir_p_fwd = models.IntegerField(blank=True, null=True)
    trace_cum_unit_ind_p_fwd = models.IntegerField(blank=True, null=True)
    trace_cum_animal_ind_p_fwd = models.IntegerField(blank=True, null=True)
    trace_origin_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True)
    trace_origin_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True)
    trace_origin_cum_unit_dir_back = models.IntegerField(blank=True, null=True)
    trace_origin_cum_unit_ind_back = models.IntegerField(blank=True, null=True)
    trace_new_unit_dir_fwd = models.IntegerField(blank=True, null=True)
    trace_new_animal_dir_fwd = models.IntegerField(blank=True, null=True)
    trace_new_unit_ind_fwd = models.IntegerField(blank=True, null=True)
    trace_new_animal_ind_fwd = models.IntegerField(blank=True, null=True)
    trace_cum_unit_dir_back = models.IntegerField(blank=True, null=True)
    trace_cum_animal_dir_back = models.IntegerField(blank=True, null=True)
    trace_cum_unit_ind_back = models.IntegerField(blank=True, null=True)
    trace_cum_animal_ind_back = models.IntegerField(blank=True, null=True)
    trace_cum_unit_dir_p_back = models.IntegerField(blank=True, null=True)
    trace_cum_animal_dir_p_back = models.IntegerField(blank=True, null=True)
    trace_cum_unit_ind_p_back = models.IntegerField(blank=True, null=True)
    trace_cum_animal_ind_p_back = models.IntegerField(blank=True, null=True)
    trace_new_unit_dir_back = models.IntegerField(blank=True, null=True)
    trace_new_animal_dir_back = models.IntegerField(blank=True, null=True)
    trace_new_u_ind_back = models.IntegerField(blank=True, null=True)
    trace_new_animal_ind_back = models.IntegerField(blank=True, null=True)
    trace_origin_new_unit_dir_fwd = models.IntegerField(blank=True, null=True)
    trace_origin_new_unit_ind_fwd = models.IntegerField(blank=True, null=True)
    trace_origin_new_unit_dir_back = models.IntegerField(blank=True, null=True)
    trace_origin_new_unit_ind_back = models.IntegerField(blank=True, null=True)
    exam_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True)
    exam_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True)
    exam_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True)
    exam_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True)
    exam_cum_unit_dir_back = models.IntegerField(blank=True, null=True)
    exam_cum_animal_dir_back = models.IntegerField(blank=True, null=True)
    exam_cum_unit_ind_back = models.IntegerField(blank=True, null=True)
    exam_cum_animal_ind_back = models.IntegerField(blank=True, null=True)
    exam_new_unit_all = models.IntegerField(blank=True, null=True)
    exam_new_animal_all = models.IntegerField(blank=True, null=True)
    test_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True)
    test_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True)
    test_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True)
    test_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True)
    test_cum_unit_dir_back = models.IntegerField(blank=True, null=True)
    test_cum_animal_dir_back = models.IntegerField(blank=True, null=True)
    test_cum_unit_ind_back = models.IntegerField(blank=True, null=True)
    test_cum_animal_ind_back = models.IntegerField(blank=True, null=True)
    test_cum_unit_true_pos = models.IntegerField(blank=True, null=True)
    test_cum_animal_true_pos = models.IntegerField(blank=True, null=True)
    test_new_unit_true_pos = models.IntegerField(blank=True, null=True)
    test_new_animal_true_pos = models.IntegerField(blank=True, null=True)
    test_cum_unit_true_neg = models.IntegerField(blank=True, null=True)
    test_cum_animal_true_neg = models.IntegerField(blank=True, null=True)
    test_new_unit_true_neg = models.IntegerField(blank=True, null=True)
    test_new_animal_true_neg = models.IntegerField(blank=True, null=True)
    test_cum_unit_false_pos = models.IntegerField(blank=True, null=True)
    test_cum_animal_false_pos = models.IntegerField(blank=True, null=True)
    test_new_unit_false_pos = models.IntegerField(blank=True, null=True)
    test_new_animal_false_pos = models.IntegerField(blank=True, null=True)
    test_cum_unit_false_neg = models.IntegerField(blank=True, null=True)
    test_cum_animal_false_neg = models.IntegerField(blank=True, null=True)
    test_new_unit_false_neg = models.IntegerField(blank=True, null=True)
    test_new_animal_false_neg = models.IntegerField(blank=True, null=True)
    detect_new_unit_clin = models.IntegerField(blank=True, null=True)
    detect_new_animal_clin = models.IntegerField(blank=True, null=True)
    detect_cum_unit_clin = models.IntegerField(blank=True, null=True)
    detect_cum_animal_clin = models.IntegerField(blank=True, null=True)
    detect_new_unit_test = models.IntegerField(blank=True, null=True)
    detect_new_animal_test = models.IntegerField(blank=True, null=True)
    detect_cum_unit_test = models.IntegerField(blank=True, null=True)
    detect_cum_animal_test = models.IntegerField(blank=True, null=True)
    destroy_cum_unit_initial = models.IntegerField(blank=True, null=True)
    destroy_cum_animal_initial = models.IntegerField(blank=True, null=True)
    destroy_cum_unit_detect = models.IntegerField(blank=True, null=True)
    destroy_cum_animal_detect = models.IntegerField(blank=True, null=True)
    destroy_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True)
    destroy_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True)
    destroy_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True)
    destroy_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True)
    destroy_cum_unit_dir_back = models.IntegerField(blank=True, null=True)
    destroy_cum_animal_dir_back = models.IntegerField(blank=True, null=True)
    destroy_cum_unit_ind_back = models.IntegerField(blank=True, null=True)
    destroy_cum_animal_ind_back = models.IntegerField(blank=True, null=True)
    destroy_cum_unit_ring = models.IntegerField(blank=True, null=True)
    destroy_cum_animal_ring = models.IntegerField(blank=True, null=True)
    destroy_new_unit_all = models.IntegerField(blank=True, null=True)
    destroy_new_animal_all = models.IntegerField(blank=True, null=True)
    destroy_wait_unit_all = models.IntegerField(blank=True, null=True)
    destroy_wait_animal_all = models.IntegerField(blank=True, null=True)
    vac_cum_unit_initial = models.IntegerField(blank=True, null=True)
    vac_cum_animal_initial = models.IntegerField(blank=True, null=True)
    vac_cum_unit_ring = models.IntegerField(blank=True, null=True)
    vac_cum_animal_ring = models.IntegerField(blank=True, null=True)
    vac_new_unit_all = models.IntegerField(blank=True, null=True)
    vac_new_animal_all = models.IntegerField(blank=True, null=True)
    vac_wait_unit_all = models.IntegerField(blank=True, null=True)
    vac_wait_animal_all = models.IntegerField(blank=True, null=True)
    zone_new_foci = models.IntegerField(blank=True, null=True)
    zone_cum_foci = models.IntegerField(blank=True, null=True)


class Outdailybyzone(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    zone = models.ForeignKey(InZone)
    zone_area = models.FloatField(blank=True, null=True)
    zone_perimeter = models.FloatField(blank=True, null=True)


class Outdailybyzoneandproductiontype(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    zone = models.ForeignKey(InZone)
    production_type = models.ForeignKey(InProductionType)
    unit_days_in_zone = models.IntegerField(blank=True, null=True)
    animal_days_in_zone = models.IntegerField(blank=True, null=True)
    units_in_zone = models.IntegerField(blank=True, null=True)
    animals_in_zone = models.IntegerField(blank=True, null=True)


class Outdailyevents(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    event = models.IntegerField(blank=True, null=True)
    unit = models.ForeignKey(DynamicUnit)
    zone = models.ForeignKey(InZone)
    event_code = models.CharField(max_length=255, blank=True)
    new_state_code = models.CharField(max_length=255, blank=True)
    test_result_code = models.CharField(max_length=255, blank=True)


class Outdailyexposures(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    exposure = models.IntegerField(blank=True, null=True)
    initiated_day = models.IntegerField(blank=True, null=True)
    exposed_unit = models.ForeignKey(DynamicUnit)
    exposed_zone = models.ForeignKey(InZone)
    exposing_unit = models.ForeignKey(DynamicUnit)
    exposing_zone = models.ForeignKey(InZone)
    spread_method_code = models.CharField(max_length=255, blank=True)
    is_adequate = models.IntegerField(blank=True, null=True)
    exposing_unit_status_code = models.CharField(max_length=255, blank=True)
    exposed_unit_status_code = models.CharField(max_length=255, blank=True)


class Outepidemiccurves(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    production_type = models.ForeignKey(InProductionType)
    infected_units = models.IntegerField(blank=True, null=True)
    infected_animals = models.IntegerField(blank=True, null=True)
    detected_units = models.IntegerField(blank=True, null=True)
    detected_animals = models.IntegerField(blank=True, null=True)
    infectious_units = models.IntegerField(blank=True, null=True)
    apparent_infectious_units = models.IntegerField(blank=True, null=True)


class Outgeneral(models.Model):
    simulation_start_time = models.CharField(max_length=255, blank=True)
    simulation_end_time = models.CharField(max_length=255, blank=True)
    completed_iterations = models.IntegerField(blank=True, null=True)
    version = models.CharField(max_length=255, blank=True)


class Outiteration(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    disease_ended = models.IntegerField(blank=True, null=True)
    disease_end_day = models.IntegerField(blank=True, null=True)
    outbreak_ended = models.IntegerField(blank=True, null=True)
    outbreak_end_day = models.IntegerField(blank=True, null=True)
    zone_foci_created = models.IntegerField(blank=True, null=True)
    destroy_wait_unit_max = models.IntegerField(blank=True, null=True)
    destroy_wait_unit_max_day = models.IntegerField(blank=True, null=True)
    destroy_wait_animal_max = models.FloatField(blank=True, null=True)
    destroy_wait_animal_max_day = models.IntegerField(blank=True, null=True)
    destroy_wait_unit_time_max = models.IntegerField(blank=True, null=True)
    destroy_wait_unit_time_avg = models.FloatField(blank=True, null=True)
    vac_wait_unit_max = models.IntegerField(blank=True, null=True)
    vac_wait_unit_max_day = models.IntegerField(blank=True, null=True)
    vac_wait_animal_max = models.FloatField(blank=True, null=True)
    vac_wait_animal_max_day = models.IntegerField(blank=True, null=True)
    vac_wait_unit_time_max = models.IntegerField(blank=True, null=True)
    vac_wait_unit_time_avg = models.FloatField(blank=True, null=True)


class Outiterationbyunit(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    unit = models.ForeignKey(DynamicUnit)
    last_status_code = models.CharField(max_length=255, blank=True)
    last_status_day = models.IntegerField(blank=True, null=True)
    last_control_state_code = models.CharField(max_length=255, blank=True)
    last_control_state_day = models.IntegerField(blank=True, null=True)


class Outiterationbyproductiontype(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    production_type = models.ForeignKey(InProductionType)
    transition_state_cum_unit_susceptible = models.IntegerField(blank=True, null=True)
    transition_state_cum_animal_susceptible = models.IntegerField(blank=True, null=True)
    transition_state_cum_unit_latent = models.IntegerField(blank=True, null=True)
    transition_state_cum_animal_latent = models.IntegerField(blank=True, null=True)
    transition_state_cum_unit_subclinical = models.IntegerField(blank=True, null=True)
    transition_state_cum_animal_subclinical = models.IntegerField(blank=True, null=True)
    transition_state_cum_unit_clinical = models.IntegerField(blank=True, null=True)
    transition_state_cum_animal_clinical = models.IntegerField(blank=True, null=True)
    transition_state_cum_unit_nat_immune = models.IntegerField(blank=True, null=True)
    transition_state_cum_animal_nat_immune = models.IntegerField(blank=True, null=True)
    transition_state_cum_unit_vac_immune = models.IntegerField(blank=True, null=True)
    transition_state_cum_animal_vac_immune = models.IntegerField(blank=True, null=True)
    transition_state_cum_unit_destroyed = models.IntegerField(blank=True, null=True)
    transition_state_cum_animal_destroyed = models.IntegerField(blank=True, null=True)
    infection_cum_unit_initial = models.IntegerField(blank=True, null=True)
    infection_cum_animal_initial = models.IntegerField(blank=True, null=True)
    infection_cum_unit_air = models.IntegerField(blank=True, null=True)
    infection_cum_animal_air = models.IntegerField(blank=True, null=True)
    infection_cum_unit_dir = models.IntegerField(blank=True, null=True)
    infection_cum_animal_dir = models.IntegerField(blank=True, null=True)
    infection_cum_unit_ind = models.IntegerField(blank=True, null=True)
    infection_cum_animal_ind = models.IntegerField(blank=True, null=True)
    exposed_cum_unit_dir = models.IntegerField(blank=True, null=True)
    exposed_cum_animal_dir = models.IntegerField(blank=True, null=True)
    exposed_cum_unit_ind = models.IntegerField(blank=True, null=True)
    exposed_cum_animal_ind = models.IntegerField(blank=True, null=True)
    trace_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True)
    trace_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True)
    trace_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True)
    trace_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True)
    trace_cum_unit_dir_p_fwd = models.IntegerField(blank=True, null=True)
    trace_cum_animal_dir_pfwd = models.IntegerField(blank=True, null=True)
    trace_cum_unit_ind_p_fwd = models.IntegerField(blank=True, null=True)
    trace_cum_animal_ind_p_fwd = models.IntegerField(blank=True, null=True)
    trace_cum_unit_dir_back = models.IntegerField(blank=True, null=True)
    trace_cum_animal_dir_back = models.IntegerField(blank=True, null=True)
    trace_cum_unit_ind_back = models.IntegerField(blank=True, null=True)
    trace_cum_animal_ind_back = models.IntegerField(blank=True, null=True)
    trace_cum_unit_dir_p_back = models.IntegerField(blank=True, null=True)
    trace_cum_animal_dir_pback = models.IntegerField(blank=True, null=True)
    trace_cum_unit_ind_p_back = models.IntegerField(blank=True, null=True)
    trace_cum_animal_ind_p_back = models.IntegerField(blank=True, null=True)
    trace_origin_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True)
    trace_origin_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True)
    trace_origin_cum_unit_dir_back = models.IntegerField(blank=True, null=True)
    trace_origin_cum_unit_ind_back = models.IntegerField(blank=True, null=True)
    exam_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True)
    exam_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True)
    exam_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True)
    exam_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True)
    exam_cum_unit_dir_back = models.IntegerField(blank=True, null=True)
    exam_cum_animal_dir_back = models.IntegerField(blank=True, null=True)
    exam_cum_unit_ind_back = models.IntegerField(blank=True, null=True)
    exam_cum_animal_ind_back = models.IntegerField(blank=True, null=True)
    test_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True)
    test_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True)
    test_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True)
    test_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True)
    test_cum_unit_dir_back = models.IntegerField(blank=True, null=True)
    test_cum_animal_dir_back = models.IntegerField(blank=True, null=True)
    test_cum_unit_ind_back = models.IntegerField(blank=True, null=True)
    test_cum_animal_ind_back = models.IntegerField(blank=True, null=True)
    test_cum_unit_true_pos = models.IntegerField(blank=True, null=True)
    test_cum_animal_true_pos = models.IntegerField(blank=True, null=True)
    test_cum_unit_true_neg = models.IntegerField(blank=True, null=True)
    test_cum_animal_true_neg = models.IntegerField(blank=True, null=True)
    test_cum_unit_false_pos = models.IntegerField(blank=True, null=True)
    test_cum_animal_false_pos = models.IntegerField(blank=True, null=True)
    test_cum_unit_false_neg = models.IntegerField(blank=True, null=True)
    test_cum_animal_false_neg = models.IntegerField(blank=True, null=True)
    detect_cum_unit_clin = models.IntegerField(blank=True, null=True)
    detect_cum_animal_clin = models.IntegerField(blank=True, null=True)
    detect_cum_unit_test = models.IntegerField(blank=True, null=True)
    detect_cum_animal_test = models.IntegerField(blank=True, null=True)
    destroy_cum_unit_initial = models.IntegerField(blank=True, null=True)
    destroy_cum_animal_initial = models.IntegerField(blank=True, null=True)
    destroy_cum_unit_detect = models.IntegerField(blank=True, null=True)
    destroy_cum_animal_detect = models.IntegerField(blank=True, null=True)
    destroy_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True)
    destroy_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True)
    destroy_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True)
    destroy_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True)
    destroy_cum_unit_dir_back = models.IntegerField(blank=True, null=True)
    destroy_cum_animal_dir_back = models.IntegerField(blank=True, null=True)
    destroy_cum_unit_ind_back = models.IntegerField(blank=True, null=True)
    destroy_cum_animal_ind_back = models.IntegerField(blank=True, null=True)
    destroy_cum_unit_ring = models.IntegerField(blank=True, null=True)
    destroy_cum_animal_ring = models.IntegerField(blank=True, null=True)
    destroy_wait_unit_max = models.IntegerField(blank=True, null=True)
    destroy_wait_animal_max = models.IntegerField(blank=True, null=True)
    destroy_wait_unit_max_day = models.IntegerField(blank=True, null=True)
    destroy_wait_animal_max_day = models.IntegerField(blank=True, null=True)
    destroy_wait_unit_time_max = models.IntegerField(blank=True, null=True)
    destroy_wait_unit_time_avg = models.FloatField(blank=True, null=True)
    destroy_wait_unit_days_in_queue = models.FloatField(blank=True, null=True)
    destroy_wait_animal_days_in_queue = models.FloatField(blank=True, null=True)
    vac_cum_unit_initial = models.IntegerField(blank=True, null=True)
    vac_cum_animal_initial = models.IntegerField(blank=True, null=True)
    vac_cum_unit_ring = models.IntegerField(blank=True, null=True)
    vac_cum_animal_ring = models.IntegerField(blank=True, null=True)
    vac_wait_unit_max = models.IntegerField(blank=True, null=True)
    vac_wait_animal_max = models.FloatField(null=True, blank=True)
    vac_wait_unit_max_day = models.IntegerField(blank=True, null=True)
    vac_wait_animal_max_day = models.IntegerField(blank=True, null=True)
    vac_wait_unit_time_max = models.FloatField(null=True, blank=True)
    vac_wait_unit_time_avg = models.IntegerField(blank=True, null=True)
    zone_foci = models.IntegerField(blank=True, null=True)
    first_detection = models.IntegerField(blank=True, null=True)
    first_det_unit_inf = models.IntegerField(blank=True, null=True)
    first_detect_animal_inf = models.IntegerField(blank=True, null=True)
    first_destruction = models.IntegerField(blank=True, null=True)
    first_vaccination = models.IntegerField(blank=True, null=True)
    last_detection = models.IntegerField(blank=True, null=True)


class Outiterationbyzone(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    zone = models.ForeignKey(InZone)
    max_zone_area = models.FloatField(blank=True, null=True)
    max_zone_area_day = models.IntegerField(blank=True, null=True)
    final_zone_area = models.FloatField(blank=True, null=True)
    max_zone_perimeter = models.FloatField(blank=True, null=True)
    max_zone_perimeter_day = models.IntegerField(blank=True, null=True)
    final_zone_perimeter = models.FloatField(blank=True, null=True)


class Outiterationbyzoneandproductiontype(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    zone = models.ForeignKey(InZone)
    production_type = models.ForeignKey(InProductionType)
    unit_days_in_zone = models.IntegerField(blank=True, null=True)
    animal_days_in_zone = models.IntegerField(blank=True, null=True)
    cost_surveillance = models.FloatField(blank=True, null=True)


class Outiterationcosts(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    production_type = models.ForeignKey(InProductionType)
    destroy_appraisal = models.FloatField(blank=True, null=True)
    destroy_cleaning = models.FloatField(blank=True, null=True)
    destroy_euthanasia = models.FloatField(blank=True, null=True)
    destroy_indemnification = models.FloatField(blank=True, null=True)
    destroy_disposal = models.FloatField(blank=True, null=True)
    vac_cum_setup = models.FloatField(blank=True, null=True)
    vac_cum_vaccination = models.FloatField(blank=True, null=True)

