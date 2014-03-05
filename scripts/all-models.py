
from django.db import models
from django_extras.db.models import PercentField, LatitudeField, LongitudeField, MoneyField


def chc(*choice_list):
    return tuple((x, x) for x in choice_list)


class DbSchemaVersion(models.Model):
    version_number = models.CharField(max_length=255, unique=True)
    version_application = models.CharField(max_length=255, )
    version_date = models.CharField(max_length=255, )
    version_info_url = models.TextField(blank=True)
    version_id = models.IntegerField(blank=True, null=True)


class DynamicBlob(models.Model):
    zone_perimeters = models.CharField(max_length=255, blank=True)  # polygons?


class DynamicUnit(models.Model):
    production_type = models.ForeignKey('InProductionType')
    latitude = LatitudeField()
    longitude = LongitudeField()
    initial_state_code = models.CharField(max_length=255,
                                          choices=(('L', 'Latent'),
                                                   ('S', 'Susceptible'),
                                                   ('B', 'Subclinical'),
                                                   ('C', 'Clinical'),
                                                   ('N', 'Naturally Immune'),
                                                   ('V', 'Vaccine Immune'),
                                                   ('D', 'Destroyed')))
    days_in_initial_state = models.IntegerField(blank=True, null=True)
    days_left_in_initial_state = models.IntegerField(blank=True, null=True)
    initial_size = models.IntegerField()
    _final_state_code = models.CharField(max_length=255, blank=True)
    _final_control_state_code = models.CharField(max_length=255, blank=True)
    _final_detection_state_code = models.CharField(max_length=255, blank=True)
    _cum_infected = models.IntegerField(blank=True, null=True)
    _cum_detected = models.IntegerField(blank=True, null=True)
    _cum_destroyed = models.IntegerField(blank=True, null=True)
    _cum_vaccinated = models.IntegerField(blank=True, null=True)
    user_defined_1 = models.TextField(blank=True)
    user_defined_2 = models.TextField(blank=True)
    user_defined_3 = models.TextField(blank=True)
    user_defined_4 = models.TextField(blank=True)

'''InChart is an equation model that defines either a Probability Distribution Function (pdf) or
 a relational function (relid) depending on which child class is used.  '''
class InChart(models.Model):
    chart_name = models.CharField(max_length=255, )
    # field_name = models.CharField(max_length=255, )  # I don't think this is necessary
    x_axis_units = models.CharField(max_length=255, default="Days")
    y_axis_units = models.CharField(max_length=255, blank=True)
    _notes = models.TextField(blank=True, null=True)  # Why is this hidden?
    class Meta:
        abstract = True


'''There are a large number of fields in this model because different chart_type use different
parameters.  Parameters are all listed as optional because they are frequently unused.  A second
layer of validation will be necessary for required parameters per chart_type.'''
class ProbabilityEquation(InChart):
    chart_type = models.CharField(max_length=255, blank=True,
                                  choices=chc("Point", "Uniform", "Triangular", "Piecewise", "Histogram", "Gaussian",
                                              "Poisson", "Beta", "Gamma", "Weibull", "Exponential", "Pearson5",
                                              "Logistic",
                                              "LogLogistic", "Lognormal", "NegativeBinomial", "Pareto", "Bernoulli",
                                              "Binomial", "Discrete Uniform", "Hypergeometric", "Inverse Gaussian"))
    mean = models.FloatField(blank=True, null=True)
    std_dev = models.FloatField(blank=True, null=True)
    min = models.FloatField(blank=True, null=True)
    mode = models.FloatField(blank=True, null=True)
    max = models.FloatField(blank=True, null=True)
    alpha = models.FloatField(blank=True, null=True)
    alpha2 = models.FloatField(blank=True, null=True)
    beta = models.FloatField(blank=True, null=True)
    location = models.FloatField(blank=True, null=True)
    scale = models.FloatField(blank=True, null=True)
    shape = models.FloatField(blank=True, null=True)  # or should this be the chart_type list of PDF functions?
    n = models.IntegerField(blank=True, null=True)
    p = models.FloatField(blank=True, null=True)
    m = models.IntegerField(blank=True, null=True)
    d = models.IntegerField(blank=True, null=True)
    theta = models.FloatField(blank=True, null=True)
    a = models.FloatField(blank=True, null=True)
    s = models.IntegerField(blank=True, null=True)


class RelationalEquation(InChart):
    pass  # Inherited fields


class EquationPoint(models.Model):
    chart = models.ForeignKey(RelationalEquation)
    _point_order = models.IntegerField()
    _x = models.FloatField()
    _y = models.FloatField()


class InControlGlobal(models.Model):
    _include_detection = models.BooleanField(default=False, )
    _include_tracing = models.BooleanField(default=False, )
    _include_tracing_unit_exam = models.BooleanField(default=False, )
    _include_tracing_testing = models.BooleanField(default=False, )
    _include_destruction = models.BooleanField(default=False, )  # TODO: restrict ForeignKey presence based on boolean include
    _include_vaccination = models.BooleanField(default=False, )
    _include_zones = models.BooleanField(default=False, )
    destruction_delay = models.IntegerField(blank=True, null=True)
    destruction_capacity_relid = models.ForeignKey(RelationalEquation, related_name='+', blank=True, null=True)
    destruction_priority_order = models.CharField(max_length=255, blank=True)  # These are an odd legacy.  Leave it for now
    destrucion_reason_order = models.CharField(max_length=255, blank=True)
    trigger_vaccincation_after_detected_units_count = models.IntegerField(blank=True, null=True)
    vaccination_capacity_relid = models.ForeignKey(RelationalEquation, related_name='+', blank=True, null=True)
    vaccination_priority_order = models.CharField(max_length=255, blank=True)


class InControlPlan(models.Model):
    control_plan_name = models.CharField(max_length=255, )
    control_plan_description = models.TextField(blank=True)
    control_plan_group = models.CharField(max_length=255, blank=True)


class InControlsProductionType(models.Model):
    production_type = models.ForeignKey('InProductionType')
    use_detection = models.BooleanField(default=False, )
    detection_probability_for_observed_time_in_clinical_relid = models.ForeignKey(RelationalEquation, related_name='+', blank=True, null=True)
    detection_probability_report_vs_first_detection_relid = models.ForeignKey(RelationalEquation, related_name='+', blank=True, null=True)
    trace_direct_forward = models.BooleanField(default=False, )
    trace_direct_back = models.BooleanField(default=False, )
    trace_direct_success = PercentField(blank=True, null=True)
    trace_direct_trace_period = models.BooleanField(default=False, )
    trace_indirect_forward = models.BooleanField(default=False, )
    trace_indirect_back = models.BooleanField(default=False, )
    trace_indirect_success = PercentField(blank=True, null=True)
    trace_indirect_trace_period = models.BooleanField(default=False, )
    trace_delay_pdf = models.ForeignKey(ProbabilityEquation, related_name='+')
    use_destruction = models.BooleanField(default=False, )
    destruction_is_ring_trigger = models.BooleanField(default=False, )
    destruction_ring_radius = models.FloatField(blank=True, null=True)
    destruction_is_ring_target = models.BooleanField(default=False, )
    destroy_direct_forward_traces = models.BooleanField(default=False, )
    destroy_indirect_forward_traces = models.BooleanField(default=False, )
    destroy_direct_back_traces = models.BooleanField(default=False, )
    destroy_indirect_back_traces = models.BooleanField(default=False, )
    destruction_priority = models.IntegerField(blank=True, null=True)
    use_vaccination = models.BooleanField(default=False, )
    vaccination_min_time_between = models.IntegerField(blank=True, null=True)
    vaccinate_detected = models.BooleanField(default=False, )
    days_to_immunity = models.IntegerField(blank=True, null=True)
    vaccine_immune_period_pdf = models.ForeignKey(ProbabilityEquation, related_name='+')
    vaccinate_ring = models.BooleanField(default=False, )
    vaccination_ring_radius = models.FloatField(blank=True, null=True)
    vaccination_priority = models.IntegerField(blank=True, null=True)
    cost_destroy_appraisal_per_unit = MoneyField(default=0.0)
    cost_destroy_cleaning_per_unit = MoneyField(default=0.0)
    cost_destroy_euthanasia_per_animal = MoneyField(default=0.0)
    cost_destroy_indemnification_per_animal = MoneyField(default=0.0)
    cost_destroy_disposal_per_animal = MoneyField(default=0.0)
    cost_vaccinate_setup_per_unit = MoneyField(default=0.0)
    cost_vaccinate_threshold = models.IntegerField(blank=True, null=True)
    cost_vaccinate_baseline_per_animal = MoneyField(default=0.0)
    cost_vaccinate_additional_per_animal = MoneyField(default=0.0)
    zone_detection_is_trigger = models.BooleanField(default=False, )
    zone_direct_trace_is_trigger = models.BooleanField(default=False, )
    zone_indirect_trace_is_trigger = models.BooleanField(default=False, )
    exam_direct_forward = models.BooleanField(default=False, )
    exam_direct_forward_multiplier = models.FloatField(blank=True, null=True)
    exam_indirect_forward = models.BooleanField(default=False, )
    exam_indirect_forward_multiplier = models.FloatField(blank=True, null=True)
    exam_direct_back = models.BooleanField(default=False, )
    exam_direct_back_multiplier = models.FloatField(blank=True, null=True)
    exam_indirect_back = models.BooleanField(default=False, )
    exam_indirect_back_multiplier = models.FloatField(blank=True, null=True)
    test_direct_forward = models.BooleanField(default=False, )
    test_indirect_forward = models.BooleanField(default=False, )
    test_direct_back = models.BooleanField(default=False, )
    test_indirect_back = models.BooleanField(default=False, )
    test_specificity = models.FloatField(blank=True, null=True)
    test_sensitivity = models.FloatField(blank=True, null=True)
    test_delay_pdf = models.ForeignKey(ProbabilityEquation, related_name='+')
    vaccinate_restrospective_days = models.BooleanField(default=False, )


class InDiseaseGlobal(models.Model):
    disease_name = models.TextField(blank=True)
    disease_description = models.TextField(blank=True)


class InDiseaseProductionType(models.Model):
    production_type = models.ForeignKey('InProductionType')
    use_disease_transition = models.BooleanField(default=False, )
    disease_latent_period_pdf = models.ForeignKey(ProbabilityEquation, related_name='+')
    disease_subclinical_period_pdf = models.ForeignKey(ProbabilityEquation, related_name='+')
    disease_clinical_period_pdf = models.ForeignKey(ProbabilityEquation, related_name='+')
    disease_immune_period_pdf = models.ForeignKey(ProbabilityEquation, related_name='+')
    disease_prevalence_relid = models.ForeignKey(RelationalEquation, related_name='+')


class InDiseaseSpread(models.Model):
    production_type_pair = models.ForeignKey('InProductionTypePair')
    spread_method_code = models.CharField(max_length=255, blank=True)
    latent_can_infect = models.BooleanField(default=False, )
    subclinical_can_infect = models.BooleanField(default=False, )
    mean_contact_rate = models.FloatField(blank=True, null=True)
    use_fixed_contact_rate = models.BooleanField(default=False, )
    fixed_contact_rate = models.FloatField(blank=True, null=True)
    infection_probability = models.FloatField(blank=True, null=True)
    distance_pdf = models.ForeignKey(ProbabilityEquation, related_name='+')
        # This is in Disease because of simulation restrictions
    movement_control_relid = models.ForeignKey(RelationalEquation, related_name='+')
    transport_delay_pdf = models.ForeignKey(ProbabilityEquation, related_name='+')
    probability_airborne_spread_1km = models.FloatField(blank=True, null=True)
    max_distance_airborne_spread = models.FloatField(blank=True, null=True)
    wind_direction_start = models.IntegerField(blank=True, null=True)
    wind_direction_end = models.IntegerField(blank=True, null=True)


class InGeneral(models.Model):
    language = models.CharField(choices=(('en',"English"), ('es',"Spanish")), max_length=255, blank=True)
    scenario_description = models.TextField(blank=True,)
    iterations = models.IntegerField(blank=True, null=True,)
    days = models.IntegerField(blank=True, null=True, )
    sim_stop_reason = models.CharField(max_length=255, blank=True,
        choices=(('disease-end','Simulation will stop when there are no more latent or infectious units.'),
                 ('first-detection','Simulation will stop when the first detection occurs.')))
    include_contact_spread = models.BooleanField(default=False, )
    include_airborne_spread = models.BooleanField(default=False, )
    use_airborne_exponential_decay = models.BooleanField(default=False, )
    use_within_unit_prevalence = models.BooleanField(default=False, )
    cost_track_destruction = models.BooleanField(default=False, )
    cost_track_vaccination = models.BooleanField(default=False, )
    cost_track_zone_surveillance = models.BooleanField(default=False, )
    use_fixed_random_seed = models.BooleanField(default=False, )
    random_seed = models.IntegerField(blank=True, null=True)
    ## Outputs requested:
    save_all_daily_outputs = models.BooleanField(default=False, )
    maximum_iterations_for_daily_output = models.IntegerField(default=3, )
    write_daily_states_file = models.BooleanField(default=False,)
    daily_states_filename = models.CharField(max_length=255, blank=True)
    save_daily_events = models.BooleanField(default=False, )
    save_daily_exposures = models.BooleanField(default=False, )
    save_iteration_outputs_for_units = models.BooleanField(default=False, )
    write_map_output = models.BooleanField(default=False, )
    map_directory = models.CharField(max_length=255, blank=True)


class InProductionType(models.Model):
    production_type_name = models.CharField(max_length=255, )
    production_type_description = models.TextField(blank=True) # This field type is a guess.


class InProductionTypePair(models.Model):
    source_production_type = models.ForeignKey(InProductionType, related_name='used_as_sources')
    destination_production_type = models.ForeignKey(InProductionType, related_name='used_as_destinations')
    direct_contact_spread_model = models.ForeignKey(InDiseaseSpread,   related_name='direct_spread_pair', blank=True, null=True)  # These can be blank, so no check box necessary
    indirect_contact_spread_model = models.ForeignKey(InDiseaseSpread, related_name='indirect_spread_pair', blank=True, null=True)  # These can be blank, so no check box necessary
    airborne_contact_spread_model = models.ForeignKey(InDiseaseSpread, related_name='airborne_spread_pair', blank=True, null=True)  # These can be blank, so no check box necessary


class InZone(models.Model):
    zone_description = models.TextField()
    zone_radius = models.FloatField()


class InZoneProductionType(models.Model):
    zone = models.ForeignKey(InZone)
    production_type = models.ForeignKey('InProductionType')
    zone_indirect_movement_relid = models.ForeignKey(RelationalEquation, related_name='+', blank=True, null=True)
    zone_direct_movement_relid = models.ForeignKey(RelationalEquation, related_name='+', blank=True, null=True)
    zone_detection_multiplier = models.FloatField(default=1.0)
    cost_surv_per_animal_day = MoneyField(default=0.0)


class ReadAllCodes(models.Model):
    _code = models.CharField(max_length=255, )
    _code_type = models.CharField(max_length=255, )
    _code_description = models.TextField()


class ReadAllCodeTypes(models.Model):
    _code_type = models.CharField(max_length=255, )
    _code_type_description = models.TextField()









class OutDailyByProductionType(models.Model):
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


class OutDailyByZone(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    zone = models.ForeignKey(InZone)
    zone_area = models.FloatField(blank=True, null=True)
    zone_perimeter = models.FloatField(blank=True, null=True)


class OutDailyByZoneAndProductionType(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    zone = models.ForeignKey(InZone)
    production_type = models.ForeignKey(InProductionType)
    unit_days_in_zone = models.IntegerField(blank=True, null=True)
    animal_days_in_zone = models.IntegerField(blank=True, null=True)
    units_in_zone = models.IntegerField(blank=True, null=True)
    animals_in_zone = models.IntegerField(blank=True, null=True)


class OutDailyEvents(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    event = models.IntegerField(blank=True, null=True)
    unit = models.ForeignKey(DynamicUnit)
    zone = models.ForeignKey(InZone)
    event_code = models.CharField(max_length=255, blank=True)
    new_state_code = models.CharField(max_length=255, blank=True)
    test_result_code = models.CharField(max_length=255, blank=True)


class OutDailyExposures(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    exposure = models.IntegerField(blank=True, null=True)
    initiated_day = models.IntegerField(blank=True, null=True)
    exposed_unit = models.ForeignKey(DynamicUnit, related_name='events_where_unit_was_exposed')
    exposed_zone = models.ForeignKey(InZone, related_name='events_that_exposed_this_zone')
    exposing_unit = models.ForeignKey(DynamicUnit, related_name='events_where_unit_exposed_others')
    exposing_zone = models.ForeignKey(InZone, related_name='events_that_exposed_others')
    spread_method_code = models.CharField(max_length=255, blank=True)
    is_adequate = models.NullBooleanField(blank=True, null=True)  # Changed Booleans to NullBooleans so as not to restrict output
    exposing_unit_status_code = models.CharField(max_length=255, blank=True)
    exposed_unit_status_code = models.CharField(max_length=255, blank=True)


class OutEpidemicCurves(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    production_type = models.ForeignKey(InProductionType)
    infected_units = models.IntegerField(blank=True, null=True)
    infected_animals = models.IntegerField(blank=True, null=True)
    detected_units = models.IntegerField(blank=True, null=True)
    detected_animals = models.IntegerField(blank=True, null=True)
    infectious_units = models.IntegerField(blank=True, null=True)
    apparent_infectious_units = models.IntegerField(blank=True, null=True)


class OutGeneral(models.Model):
    simulation_start_time = models.DateTimeField(max_length=255, blank=True)
    simulation_end_time = models.DateTimeField(max_length=255, blank=True)
    completed_iterations = models.IntegerField(blank=True, null=True)
    version = models.CharField(max_length=255, blank=True)


class OutIteration(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    disease_ended = models.NullBooleanField(blank=True, null=True)  # Changed Booleans to NullBooleans so as not to restrict output
    disease_end_day = models.IntegerField(blank=True, null=True)
    outbreak_ended = models.NullBooleanField(blank=True, null=True)  # Changed Booleans to NullBooleans so as not to restrict output
    outbreak_end_day = models.IntegerField(blank=True, null=True)
    zone_foci_created = models.NullBooleanField(blank=True, null=True)  # Changed Booleans to NullBooleans so as not to restrict output
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


class OutIterationByUnit(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    unit = models.ForeignKey(DynamicUnit)
    last_status_code = models.CharField(max_length=255, blank=True)
    last_status_day = models.IntegerField(blank=True, null=True)
    last_control_state_code = models.CharField(max_length=255, blank=True)
    last_control_state_day = models.IntegerField(blank=True, null=True)


class OutIterationByProductionType(models.Model):
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


class OutIterationByZone(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    zone = models.ForeignKey(InZone)
    max_zone_area = models.FloatField(blank=True, null=True)
    max_zone_area_day = models.IntegerField(blank=True, null=True)
    final_zone_area = models.FloatField(blank=True, null=True)
    max_zone_perimeter = models.FloatField(blank=True, null=True)
    max_zone_perimeter_day = models.IntegerField(blank=True, null=True)
    final_zone_perimeter = models.FloatField(blank=True, null=True)


class OutIterationByZoneAndProductionType(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    zone = models.ForeignKey(InZone)
    production_type = models.ForeignKey(InProductionType)
    unit_days_in_zone = models.IntegerField(blank=True, null=True)
    animal_days_in_zone = models.IntegerField(blank=True, null=True)
    cost_surveillance = models.FloatField(blank=True, null=True)


class OutIterationCosts(models.Model):
    iteration = models.IntegerField(blank=True, null=True)
    production_type = models.ForeignKey(InProductionType)
    destroy_appraisal = models.FloatField(blank=True, null=True)
    destroy_cleaning = models.FloatField(blank=True, null=True)
    destroy_euthanasia = models.FloatField(blank=True, null=True)
    destroy_indemnification = models.FloatField(blank=True, null=True)
    destroy_disposal = models.FloatField(blank=True, null=True)
    vac_cum_setup = models.FloatField(blank=True, null=True)
    vac_cum_vaccination = models.FloatField(blank=True, null=True)



