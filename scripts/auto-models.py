
from django.db import models
from django_extras.db.models import PercentField, LatitudeField, LongitudeField, MoneyField


def chc(*choice_list):
    return tuple((x, x) for x in choice_list)


class DbSchemaVersion(models.Model):
    _version_number = models.CharField(max_length=255, unique=True)
    _version_application = models.CharField(max_length=255, )
    _version_date = models.CharField(max_length=255, )
    _version_info_url = models.TextField(blank=True)
    _version_id = models.IntegerField(blank=True, null=True)


class DynamicBlob(models.Model):
    _zone_perimeters = models.CharField(max_length=255, blank=True)  # polygons?


class DynamicUnit(models.Model):
    _production_type = models.ForeignKey('InProductionType')
    _latitude = LatitudeField()
    _longitude = LongitudeField()
    _initial_state_code = models.CharField(max_length=255,
                                          choices=(('L', 'Latent'),
                                                   ('S', 'Susceptible'),
                                                   ('B', 'Subclinical'),
                                                   ('C', 'Clinical'),
                                                   ('N', 'Naturally Immune'),
                                                   ('V', 'Vaccine Immune'),
                                                   ('D', 'Destroyed')))
    _days_in_initial_state = models.IntegerField(blank=True, null=True)
    _days_left_in_initial_state = models.IntegerField(blank=True, null=True)
    _initial_size = models.IntegerField()
    __final_state_code = models.CharField(max_length=255, blank=True)
    __final_control_state_code = models.CharField(max_length=255, blank=True)
    __final_detection_state_code = models.CharField(max_length=255, blank=True)
    __cum_infected = models.IntegerField(blank=True, null=True)
    __cum_detected = models.IntegerField(blank=True, null=True)
    __cum_destroyed = models.IntegerField(blank=True, null=True)
    __cum_vaccinated = models.IntegerField(blank=True, null=True)
    _user_defined_1 = models.TextField(blank=True)
    _user_defined_2 = models.TextField(blank=True)
    _user_defined_3 = models.TextField(blank=True)
    _user_defined_4 = models.TextField(blank=True)

'''InChart is an equation model that defines either a Probability Distribution Function (pdf) or
 a relational function (relid) depending on which child class is used.  '''
class InChart(models.Model):
    _chart_name = models.CharField(max_length=255, )
    _# field_name = models.CharField(max_length=255, )  # I don't think this is necessary
    _x_axis_units = models.CharField(max_length=255, default="Days")
    _y_axis_units = models.CharField(max_length=255, blank=True)
    __notes = models.TextField(blank=True, null=True)  # Why is this hidden?
    class Meta:
        abstract = True


'''There are a large number of fields in this model because different chart_type use different
parameters.  Parameters are all listed as optional because they are frequently unused.  A second
layer of validation will be necessary for required parameters per chart_type.'''
class ProbabilityEquation(InChart):
    _chart_type = models.CharField(max_length=255, blank=True,
                                  choices=chc("Point", "Uniform", "Triangular", "Piecewise", "Histogram", "Gaussian",
                                              "Poisson", "Beta", "Gamma", "Weibull", "Exponential", "Pearson5",
                                              "Logistic",
                                              "LogLogistic", "Lognormal", "NegativeBinomial", "Pareto", "Bernoulli",
                                              "Binomial", "Discrete Uniform", "Hypergeometric", "Inverse Gaussian"))
    _mean = models.FloatField(blank=True, null=True)
    _std_dev = models.FloatField(blank=True, null=True)
    _min = models.FloatField(blank=True, null=True)
    _mode = models.FloatField(blank=True, null=True)
    _max = models.FloatField(blank=True, null=True)
    _alpha = models.FloatField(blank=True, null=True)
    _alpha2 = models.FloatField(blank=True, null=True)
    _beta = models.FloatField(blank=True, null=True)
    _location = models.FloatField(blank=True, null=True)
    _scale = models.FloatField(blank=True, null=True)
    _shape = models.FloatField(blank=True, null=True)  # or should this be the chart_type list of PDF functions?
    _n = models.IntegerField(blank=True, null=True)
    _p = models.FloatField(blank=True, null=True)
    _m = models.IntegerField(blank=True, null=True)
    _d = models.IntegerField(blank=True, null=True)
    _theta = models.FloatField(blank=True, null=True)
    _a = models.FloatField(blank=True, null=True)
    _s = models.IntegerField(blank=True, null=True)


class RelationalEquation(InChart):
    pass  # Inherited fields


class EquationPoint(models.Model):
    _chart = models.ForeignKey(RelationalEquation)
    __point_order = models.IntegerField()
    __x = models.FloatField()
    __y = models.FloatField()


class InControlGlobal(models.Model):
    __include_detection = models.BooleanField(default=False, )
    __include_tracing = models.BooleanField(default=False, )
    __include_tracing_unit_exam = models.BooleanField(default=False, )
    __include_tracing_testing = models.BooleanField(default=False, )
    __include_destruction = models.BooleanField(default=False, )  # TODO: restrict ForeignKey presence based on boolean include
    __include_vaccination = models.BooleanField(default=False, )
    __include_zones = models.BooleanField(default=False, )
    _destruction_delay = models.IntegerField(blank=True, null=True)
    _destruction_capacity_relid = models.ForeignKey(RelationalEquation, related_name='+', blank=True, null=True)
    _destruction_priority_order = models.CharField(max_length=255, blank=True)  # These are an odd legacy.  Leave it for now
    _destrucion_reason_order = models.CharField(max_length=255, blank=True)
    _trigger_vaccincation_after_detected_units_count = models.IntegerField(blank=True, null=True)
    _vaccination_capacity_relid = models.ForeignKey(RelationalEquation, related_name='+', blank=True, null=True)
    _vaccination_priority_order = models.CharField(max_length=255, blank=True)


class InControlPlan(models.Model):
    _control_plan_name = models.CharField(max_length=255, )
    _control_plan_description = models.TextField(blank=True)
    _control_plan_group = models.CharField(max_length=255, blank=True)


class InControlsProductionType(models.Model):
    _production_type = models.ForeignKey('InProductionType')
    _use_detection = models.BooleanField(default=False, )
    _detection_probability_for_observed_time_in_clinical_relid = models.ForeignKey(RelationalEquation, related_name='+', blank=True, null=True)
    _detection_probability_report_vs_first_detection_relid = models.ForeignKey(RelationalEquation, related_name='+', blank=True, null=True)
    _trace_direct_forward = models.BooleanField(default=False, )
    _trace_direct_back = models.BooleanField(default=False, )
    _trace_direct_success = PercentField(blank=True, null=True)
    _trace_direct_trace_period = models.BooleanField(default=False, )
    _trace_indirect_forward = models.BooleanField(default=False, )
    _trace_indirect_back = models.BooleanField(default=False, )
    _trace_indirect_success = PercentField(blank=True, null=True)
    _trace_indirect_trace_period = models.BooleanField(default=False, )
    _trace_delay_pdf = models.ForeignKey(ProbabilityEquation, related_name='+')
    _use_destruction = models.BooleanField(default=False, )
    _destruction_is_ring_trigger = models.BooleanField(default=False, )
    _destruction_ring_radius = models.FloatField(blank=True, null=True)
    _destruction_is_ring_target = models.BooleanField(default=False, )
    _destroy_direct_forward_traces = models.BooleanField(default=False, )
    _destroy_indirect_forward_traces = models.BooleanField(default=False, )
    _destroy_direct_back_traces = models.BooleanField(default=False, )
    _destroy_indirect_back_traces = models.BooleanField(default=False, )
    _destruction_priority = models.IntegerField(blank=True, null=True)
    _use_vaccination = models.BooleanField(default=False, )
    _vaccination_min_time_between = models.IntegerField(blank=True, null=True)
    _vaccinate_detected = models.BooleanField(default=False, )
    _days_to_immunity = models.IntegerField(blank=True, null=True)
    _vaccine_immune_period_pdf = models.ForeignKey(ProbabilityEquation, related_name='+')
    _vaccinate_ring = models.BooleanField(default=False, )
    _vaccination_ring_radius = models.FloatField(blank=True, null=True)
    _vaccination_priority = models.IntegerField(blank=True, null=True)
    _cost_destroy_appraisal_per_unit = MoneyField(default=0.0)
    _cost_destroy_cleaning_per_unit = MoneyField(default=0.0)
    _cost_destroy_euthanasia_per_animal = MoneyField(default=0.0)
    _cost_destroy_indemnification_per_animal = MoneyField(default=0.0)
    _cost_destroy_disposal_per_animal = MoneyField(default=0.0)
    _cost_vaccinate_setup_per_unit = MoneyField(default=0.0)
    _cost_vaccinate_threshold = models.IntegerField(blank=True, null=True)
    _cost_vaccinate_baseline_per_animal = MoneyField(default=0.0)
    _cost_vaccinate_additional_per_animal = MoneyField(default=0.0)
    _zone_detection_is_trigger = models.BooleanField(default=False, )
    _zone_direct_trace_is_trigger = models.BooleanField(default=False, )
    _zone_indirect_trace_is_trigger = models.BooleanField(default=False, )
    _exam_direct_forward = models.BooleanField(default=False, )
    _exam_direct_forward_multiplier = models.FloatField(blank=True, null=True)
    _exam_indirect_forward = models.BooleanField(default=False, )
    _exam_indirect_forward_multiplier = models.FloatField(blank=True, null=True)
    _exam_direct_back = models.BooleanField(default=False, )
    _exam_direct_back_multiplier = models.FloatField(blank=True, null=True)
    _exam_indirect_back = models.BooleanField(default=False, )
    _exam_indirect_back_multiplier = models.FloatField(blank=True, null=True)
    _test_direct_forward = models.BooleanField(default=False, )
    _test_indirect_forward = models.BooleanField(default=False, )
    _test_direct_back = models.BooleanField(default=False, )
    _test_indirect_back = models.BooleanField(default=False, )
    _test_specificity = models.FloatField(blank=True, null=True)
    _test_sensitivity = models.FloatField(blank=True, null=True)
    _test_delay_pdf = models.ForeignKey(ProbabilityEquation, related_name='+')
    _vaccinate_restrospective_days = models.BooleanField(default=False, )


class InDiseaseGlobal(models.Model):
    _disease_name = models.TextField(blank=True)
    _disease_description = models.TextField(blank=True)


class InDiseaseProductionType(models.Model):
    _production_type = models.ForeignKey('InProductionType')
    _use_disease_transition = models.BooleanField(default=False, )
    _disease_latent_period_pdf = models.ForeignKey(ProbabilityEquation, related_name='+')
    _disease_subclinical_period_pdf = models.ForeignKey(ProbabilityEquation, related_name='+')
    _disease_clinical_period_pdf = models.ForeignKey(ProbabilityEquation, related_name='+')
    _disease_immune_period_pdf = models.ForeignKey(ProbabilityEquation, related_name='+')
    _disease_prevalence_relid = models.ForeignKey(RelationalEquation, related_name='+')


class InDiseaseSpread(models.Model):
    _production_type_pair = models.ForeignKey('InProductionTypePair')
    _spread_method_code = models.CharField(max_length=255, blank=True)
    _latent_can_infect = models.BooleanField(default=False, )
    _subclinical_can_infect = models.BooleanField(default=False, )
    _mean_contact_rate = models.FloatField(blank=True, null=True)
    _use_fixed_contact_rate = models.BooleanField(default=False, )
    _fixed_contact_rate = models.FloatField(blank=True, null=True)
    _infection_probability = models.FloatField(blank=True, null=True)
    _distance_pdf = models.ForeignKey(ProbabilityEquation, related_name='+')
        # This is in Disease because of simulation restrictions
    _movement_control_relid = models.ForeignKey(RelationalEquation, related_name='+')
    _transport_delay_pdf = models.ForeignKey(ProbabilityEquation, related_name='+')
    _probability_airborne_spread_1km = models.FloatField(blank=True, null=True)
    _max_distance_airborne_spread = models.FloatField(blank=True, null=True)
    _wind_direction_start = models.IntegerField(blank=True, null=True)
    _wind_direction_end = models.IntegerField(blank=True, null=True)


class InGeneral(models.Model):
    _language = models.CharField(choices=(('en',"English"), ('es',"Spanish")), max_length=255, blank=True)
    _scenario_description = models.TextField(blank=True,
                                            help_text='A short description of the scenario being simulated.')
    _iterations = models.IntegerField(blank=True, null=True,
                                     help_text='The number of simulations to run.')
    _days = models.IntegerField(blank=True, null=True,
                               help_text='The maximum number of days in a simulation run. A simulation run may end earlier, if there are no latent or infectious animals and no module has pending actions to complete.')
    _sim_stop_reason = models.CharField(max_length=255, blank=True,
        choices=(('disease-end','Simulation will stop when there are no more latent or infectious units.'),
                 ('first-detection','Simulation will stop when the first detection occurs.')))
    _include_contact_spread = models.BooleanField(default=False, )
    _include_airborne_spread = models.BooleanField(default=False, )
    _use_airborne_exponential_decay = models.BooleanField(default=False, )
    _use_within_unit_prevalence = models.BooleanField(default=False, )
    _cost_track_destruction = models.BooleanField(default=False, )
    _cost_track_vaccination = models.BooleanField(default=False, )
    _cost_track_zone_surveillance = models.BooleanField(default=False, )
    _use_fixed_random_seed = models.BooleanField(default=False, )
    _random_seed = models.IntegerField(blank=True, null=True)
    ## Outputs requested:
    _save_all_daily_outputs = models.BooleanField(default=False, )
    _maximum_iterations_for_daily_output = models.IntegerField(default=3, )
    _write_daily_states_file = models.BooleanField(default=False,
      help_text='The number of units in each state.  This always reports the counts on the day of reporting, regardless of whether it is reported daily, weekly, or at some other interval.  This variable is needed to create a plot of the states over time.')
    _daily_states_filename = models.CharField(max_length=255, blank=True)
    _save_daily_events = models.BooleanField(default=False, )
    _save_daily_exposures = models.BooleanField(default=False, )
    _save_iteration_outputs_for_units = models.BooleanField(default=False, )
    _write_map_output = models.BooleanField(default=False, )
    _map_directory = models.CharField(max_length=255, blank=True)


class InProductionType(models.Model):
    _production_type_name = models.CharField(max_length=255, )
    _production_type_description = models.TextField(blank=True) # This field type is a guess.


class InProductionTypePair(models.Model):
    _source_production_type = models.ForeignKey(InProductionType, related_name='used_as_sources')
    _destination_production_type = models.ForeignKey(InProductionType, related_name='used_as_destinations')
    _direct_contact_spread_model = models.ForeignKey(InDiseaseSpread,   related_name='direct_spread_pair', blank=True, null=True)  # These can be blank, so no check box necessary
    _indirect_contact_spread_model = models.ForeignKey(InDiseaseSpread, related_name='indirect_spread_pair', blank=True, null=True)  # These can be blank, so no check box necessary
    _airborne_contact_spread_model = models.ForeignKey(InDiseaseSpread, related_name='airborne_spread_pair', blank=True, null=True)  # These can be blank, so no check box necessary


class InZone(models.Model):
    _zone_description = models.TextField()
    _zone_radius = models.FloatField()


class InZoneProductionType(models.Model):
    _zone = models.ForeignKey(InZone)
    _production_type = models.ForeignKey('InProductionType')
    _zone_indirect_movement_relid = models.ForeignKey(RelationalEquation, related_name='+', blank=True, null=True)
    _zone_direct_movement_relid = models.ForeignKey(RelationalEquation, related_name='+', blank=True, null=True)
    _zone_detection_multiplier = models.FloatField(default=1.0)
    _cost_surv_per_animal_day = MoneyField(default=0.0)


class ReadAllCodes(models.Model):
    __code = models.CharField(max_length=255, )
    __code_type = models.CharField(max_length=255, )
    __code_description = models.TextField()


class ReadAllCodeTypes(models.Model):
    __code_type = models.CharField(max_length=255, )
    __code_type_description = models.TextField()









class OutDailyByProductionType(models.Model):
    _iteration = models.IntegerField(blank=True, null=True)
    _production_type = models.ForeignKey(InProductionType)
    _day = models.IntegerField(blank=True, null=True)
    _transition_state_daily_unit_susceptible = models.IntegerField(blank=True, null=True)
    _transition_state_daily_animal_susceptible = models.IntegerField(blank=True, null=True)
    _transition_state_daily_unit_latent = models.IntegerField(blank=True, null=True)
    _transition_state_daily_animal_latent = models.IntegerField(blank=True, null=True)
    _transition_state_daily_unit_subclinical = models.IntegerField(blank=True, null=True)
    _transition_state_daily_animal_subclinical = models.IntegerField(blank=True, null=True)
    _transition_state_daily_unit_clinical = models.IntegerField(blank=True, null=True)
    _transition_state_daily_animal_clinical = models.IntegerField(blank=True, null=True)
    _transition_state_daily_unit_nat_immune = models.IntegerField(blank=True, null=True)
    _transition_state_daily_animal_nat_immune = models.IntegerField(blank=True, null=True)
    _transition_state_daily_unit_vac_immune = models.IntegerField(blank=True, null=True)
    _transition_state_daily_animal_vac_immune = models.IntegerField(blank=True, null=True)
    _transition_state_daily_unit_destroyed = models.IntegerField(blank=True, null=True)
    _transition_state_daily_animal_destroyed = models.IntegerField(blank=True, null=True)
    _transition_state_cum_unit_susceptible = models.IntegerField(blank=True, null=True)
    _transition_state_cum_animal_susceptible = models.IntegerField(blank=True, null=True)
    _transition_state_cum_unit_latent = models.IntegerField(blank=True, null=True)
    _transition_state_cum_animal_latent = models.IntegerField(blank=True, null=True)
    _transition_state_cum_unit_subclinical = models.IntegerField(blank=True, null=True)
    _transition_state_cum_animal_subclinical = models.IntegerField(blank=True, null=True)
    _transition_state_cum_unit_clinical = models.IntegerField(blank=True, null=True)
    _transition_state_cum_animal_clinical = models.IntegerField(blank=True, null=True)
    _transition_state_cum_unit_nat_immune = models.IntegerField(blank=True, null=True)
    _transition_state_cum_animal_nat_immune = models.IntegerField(blank=True, null=True)
    _transition_state_cum_unit_vac_immune = models.IntegerField(blank=True, null=True)
    _transition_state_cum_animal_vac_immune = models.IntegerField(blank=True, null=True)
    _transition_state_cum_unit_destroyed = models.IntegerField(blank=True, null=True)
    _transition_state_cum_animal_destroyed = models.IntegerField(blank=True, null=True)
    _infection_new_unit_air = models.IntegerField(blank=True, null=True)
    _infection_new_animal_air = models.IntegerField(blank=True, null=True)
    _infection_new_unit_dir = models.IntegerField(blank=True, null=True)
    _infection_new_animal_dir = models.IntegerField(blank=True, null=True)
    _infection_new_unit_ind = models.IntegerField(blank=True, null=True)
    _infection_new_animal_ind = models.IntegerField(blank=True, null=True)
    _infection_cum_unit_initial = models.IntegerField(blank=True, null=True)
    _infection_cum_animal_initial = models.IntegerField(blank=True, null=True)
    _infection_cum_unit_air = models.IntegerField(blank=True, null=True)
    _infection_cum_animal_air = models.IntegerField(blank=True, null=True)
    _infection_cum_unit_dir = models.IntegerField(blank=True, null=True)
    _infection_cum_animal_dir = models.IntegerField(blank=True, null=True)
    _infection_cum_unit_ind = models.IntegerField(blank=True, null=True)
    _infection_cum_animal_ind = models.IntegerField(blank=True, null=True)
    _exposed_cum_unit_dir = models.IntegerField(blank=True, null=True)
    _exposed_cum_animal_dir = models.IntegerField(blank=True, null=True)
    _exposed_cum_unit_ind = models.IntegerField(blank=True, null=True)
    _exposed_cum_animal_ind = models.IntegerField(blank=True, null=True)
    _trace_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True)
    _trace_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True)
    _trace_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True)
    _trace_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True)
    _trace_cum_unit_dir_p_fwd = models.IntegerField(blank=True, null=True)
    _trace_cum_animal_dir_p_fwd = models.IntegerField(blank=True, null=True)
    _trace_cum_unit_ind_p_fwd = models.IntegerField(blank=True, null=True)
    _trace_cum_animal_ind_p_fwd = models.IntegerField(blank=True, null=True)
    _trace_origin_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True)
    _trace_origin_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True)
    _trace_origin_cum_unit_dir_back = models.IntegerField(blank=True, null=True)
    _trace_origin_cum_unit_ind_back = models.IntegerField(blank=True, null=True)
    _trace_new_unit_dir_fwd = models.IntegerField(blank=True, null=True)
    _trace_new_animal_dir_fwd = models.IntegerField(blank=True, null=True)
    _trace_new_unit_ind_fwd = models.IntegerField(blank=True, null=True)
    _trace_new_animal_ind_fwd = models.IntegerField(blank=True, null=True)
    _trace_cum_unit_dir_back = models.IntegerField(blank=True, null=True)
    _trace_cum_animal_dir_back = models.IntegerField(blank=True, null=True)
    _trace_cum_unit_ind_back = models.IntegerField(blank=True, null=True)
    _trace_cum_animal_ind_back = models.IntegerField(blank=True, null=True)
    _trace_cum_unit_dir_p_back = models.IntegerField(blank=True, null=True)
    _trace_cum_animal_dir_p_back = models.IntegerField(blank=True, null=True)
    _trace_cum_unit_ind_p_back = models.IntegerField(blank=True, null=True)
    _trace_cum_animal_ind_p_back = models.IntegerField(blank=True, null=True)
    _trace_new_unit_dir_back = models.IntegerField(blank=True, null=True)
    _trace_new_animal_dir_back = models.IntegerField(blank=True, null=True)
    _trace_new_u_ind_back = models.IntegerField(blank=True, null=True)
    _trace_new_animal_ind_back = models.IntegerField(blank=True, null=True)
    _trace_origin_new_unit_dir_fwd = models.IntegerField(blank=True, null=True)
    _trace_origin_new_unit_ind_fwd = models.IntegerField(blank=True, null=True)
    _trace_origin_new_unit_dir_back = models.IntegerField(blank=True, null=True)
    _trace_origin_new_unit_ind_back = models.IntegerField(blank=True, null=True)
    _exam_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True)
    _exam_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True)
    _exam_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True)
    _exam_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True)
    _exam_cum_unit_dir_back = models.IntegerField(blank=True, null=True)
    _exam_cum_animal_dir_back = models.IntegerField(blank=True, null=True)
    _exam_cum_unit_ind_back = models.IntegerField(blank=True, null=True)
    _exam_cum_animal_ind_back = models.IntegerField(blank=True, null=True)
    _exam_new_unit_all = models.IntegerField(blank=True, null=True)
    _exam_new_animal_all = models.IntegerField(blank=True, null=True)
    _test_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True)
    _test_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True)
    _test_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True)
    _test_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True)
    _test_cum_unit_dir_back = models.IntegerField(blank=True, null=True)
    _test_cum_animal_dir_back = models.IntegerField(blank=True, null=True)
    _test_cum_unit_ind_back = models.IntegerField(blank=True, null=True)
    _test_cum_animal_ind_back = models.IntegerField(blank=True, null=True)
    _test_cum_unit_true_pos = models.IntegerField(blank=True, null=True)
    _test_cum_animal_true_pos = models.IntegerField(blank=True, null=True)
    _test_new_unit_true_pos = models.IntegerField(blank=True, null=True)
    _test_new_animal_true_pos = models.IntegerField(blank=True, null=True)
    _test_cum_unit_true_neg = models.IntegerField(blank=True, null=True)
    _test_cum_animal_true_neg = models.IntegerField(blank=True, null=True)
    _test_new_unit_true_neg = models.IntegerField(blank=True, null=True)
    _test_new_animal_true_neg = models.IntegerField(blank=True, null=True)
    _test_cum_unit_false_pos = models.IntegerField(blank=True, null=True)
    _test_cum_animal_false_pos = models.IntegerField(blank=True, null=True)
    _test_new_unit_false_pos = models.IntegerField(blank=True, null=True)
    _test_new_animal_false_pos = models.IntegerField(blank=True, null=True)
    _test_cum_unit_false_neg = models.IntegerField(blank=True, null=True)
    _test_cum_animal_false_neg = models.IntegerField(blank=True, null=True)
    _test_new_unit_false_neg = models.IntegerField(blank=True, null=True)
    _test_new_animal_false_neg = models.IntegerField(blank=True, null=True)
    _detect_new_unit_clin = models.IntegerField(blank=True, null=True)
    _detect_new_animal_clin = models.IntegerField(blank=True, null=True)
    _detect_cum_unit_clin = models.IntegerField(blank=True, null=True)
    _detect_cum_animal_clin = models.IntegerField(blank=True, null=True)
    _detect_new_unit_test = models.IntegerField(blank=True, null=True)
    _detect_new_animal_test = models.IntegerField(blank=True, null=True)
    _detect_cum_unit_test = models.IntegerField(blank=True, null=True)
    _detect_cum_animal_test = models.IntegerField(blank=True, null=True)
    _destroy_cum_unit_initial = models.IntegerField(blank=True, null=True)
    _destroy_cum_animal_initial = models.IntegerField(blank=True, null=True)
    _destroy_cum_unit_detect = models.IntegerField(blank=True, null=True)
    _destroy_cum_animal_detect = models.IntegerField(blank=True, null=True)
    _destroy_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True)
    _destroy_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True)
    _destroy_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True)
    _destroy_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True)
    _destroy_cum_unit_dir_back = models.IntegerField(blank=True, null=True)
    _destroy_cum_animal_dir_back = models.IntegerField(blank=True, null=True)
    _destroy_cum_unit_ind_back = models.IntegerField(blank=True, null=True)
    _destroy_cum_animal_ind_back = models.IntegerField(blank=True, null=True)
    _destroy_cum_unit_ring = models.IntegerField(blank=True, null=True)
    _destroy_cum_animal_ring = models.IntegerField(blank=True, null=True)
    _destroy_new_unit_all = models.IntegerField(blank=True, null=True)
    _destroy_new_animal_all = models.IntegerField(blank=True, null=True)
    _destroy_wait_unit_all = models.IntegerField(blank=True, null=True)
    _destroy_wait_animal_all = models.IntegerField(blank=True, null=True)
    _vac_cum_unit_initial = models.IntegerField(blank=True, null=True)
    _vac_cum_animal_initial = models.IntegerField(blank=True, null=True)
    _vac_cum_unit_ring = models.IntegerField(blank=True, null=True)
    _vac_cum_animal_ring = models.IntegerField(blank=True, null=True)
    _vac_new_unit_all = models.IntegerField(blank=True, null=True)
    _vac_new_animal_all = models.IntegerField(blank=True, null=True)
    _vac_wait_unit_all = models.IntegerField(blank=True, null=True)
    _vac_wait_animal_all = models.IntegerField(blank=True, null=True)
    _zone_new_foci = models.IntegerField(blank=True, null=True)
    _zone_cum_foci = models.IntegerField(blank=True, null=True)


class OutDailyByZone(models.Model):
    _iteration = models.IntegerField(blank=True, null=True)
    _day = models.IntegerField(blank=True, null=True)
    _zone = models.ForeignKey(InZone)
    _zone_area = models.FloatField(blank=True, null=True)
    _zone_perimeter = models.FloatField(blank=True, null=True)


class OutDailyByZoneAndProductionType(models.Model):
    _iteration = models.IntegerField(blank=True, null=True)
    _day = models.IntegerField(blank=True, null=True)
    _zone = models.ForeignKey(InZone)
    _production_type = models.ForeignKey(InProductionType)
    _unit_days_in_zone = models.IntegerField(blank=True, null=True)
    _animal_days_in_zone = models.IntegerField(blank=True, null=True)
    _units_in_zone = models.IntegerField(blank=True, null=True)
    _animals_in_zone = models.IntegerField(blank=True, null=True)


class OutDailyEvents(models.Model):
    _iteration = models.IntegerField(blank=True, null=True)
    _day = models.IntegerField(blank=True, null=True)
    _event = models.IntegerField(blank=True, null=True)
    _unit = models.ForeignKey(DynamicUnit)
    _zone = models.ForeignKey(InZone)
    _event_code = models.CharField(max_length=255, blank=True)
    _new_state_code = models.CharField(max_length=255, blank=True)
    _test_result_code = models.CharField(max_length=255, blank=True)


class OutDailyExposures(models.Model):
    _iteration = models.IntegerField(blank=True, null=True)
    _day = models.IntegerField(blank=True, null=True)
    _exposure = models.IntegerField(blank=True, null=True)
    _initiated_day = models.IntegerField(blank=True, null=True)
    _exposed_unit = models.ForeignKey(DynamicUnit, related_name='events_where_unit_was_exposed')
    _exposed_zone = models.ForeignKey(InZone, related_name='events_that_exposed_this_zone')
    _exposing_unit = models.ForeignKey(DynamicUnit, related_name='events_where_unit_exposed_others')
    _exposing_zone = models.ForeignKey(InZone, related_name='events_that_exposed_others')
    _spread_method_code = models.CharField(max_length=255, blank=True)
    _is_adequate = models.NullBooleanField(blank=True, null=True)  # Changed Booleans to NullBooleans so as not to restrict output
    _exposing_unit_status_code = models.CharField(max_length=255, blank=True)
    _exposed_unit_status_code = models.CharField(max_length=255, blank=True)


class OutEpidemicCurves(models.Model):
    _iteration = models.IntegerField(blank=True, null=True)
    _day = models.IntegerField(blank=True, null=True)
    _production_type = models.ForeignKey(InProductionType)
    _infected_units = models.IntegerField(blank=True, null=True)
    _infected_animals = models.IntegerField(blank=True, null=True)
    _detected_units = models.IntegerField(blank=True, null=True)
    _detected_animals = models.IntegerField(blank=True, null=True)
    _infectious_units = models.IntegerField(blank=True, null=True)
    _apparent_infectious_units = models.IntegerField(blank=True, null=True)


class OutGeneral(models.Model):
    _simulation_start_time = models.DateTimeField(max_length=255, blank=True)
    _simulation_end_time = models.DateTimeField(max_length=255, blank=True)
    _completed_iterations = models.IntegerField(blank=True, null=True)
    _version = models.CharField(max_length=255, blank=True)


class OutIteration(models.Model):
    _iteration = models.IntegerField(blank=True, null=True)
    _disease_ended = models.NullBooleanField(blank=True, null=True)  # Changed Booleans to NullBooleans so as not to restrict output
    _disease_end_day = models.IntegerField(blank=True, null=True)
    _outbreak_ended = models.NullBooleanField(blank=True, null=True)  # Changed Booleans to NullBooleans so as not to restrict output
    _outbreak_end_day = models.IntegerField(blank=True, null=True)
    _zone_foci_created = models.NullBooleanField(blank=True, null=True)  # Changed Booleans to NullBooleans so as not to restrict output
    _destroy_wait_unit_max = models.IntegerField(blank=True, null=True)
    _destroy_wait_unit_max_day = models.IntegerField(blank=True, null=True)
    _destroy_wait_animal_max = models.FloatField(blank=True, null=True)
    _destroy_wait_animal_max_day = models.IntegerField(blank=True, null=True)
    _destroy_wait_unit_time_max = models.IntegerField(blank=True, null=True)
    _destroy_wait_unit_time_avg = models.FloatField(blank=True, null=True)
    _vac_wait_unit_max = models.IntegerField(blank=True, null=True)
    _vac_wait_unit_max_day = models.IntegerField(blank=True, null=True)
    _vac_wait_animal_max = models.FloatField(blank=True, null=True)
    _vac_wait_animal_max_day = models.IntegerField(blank=True, null=True)
    _vac_wait_unit_time_max = models.IntegerField(blank=True, null=True)
    _vac_wait_unit_time_avg = models.FloatField(blank=True, null=True)


class OutIterationByUnit(models.Model):
    _iteration = models.IntegerField(blank=True, null=True)
    _unit = models.ForeignKey(DynamicUnit)
    _last_status_code = models.CharField(max_length=255, blank=True)
    _last_status_day = models.IntegerField(blank=True, null=True)
    _last_control_state_code = models.CharField(max_length=255, blank=True)
    _last_control_state_day = models.IntegerField(blank=True, null=True)


class OutIterationByProductionType(models.Model):
    _iteration = models.IntegerField(blank=True, null=True)
    _production_type = models.ForeignKey(InProductionType)
    _transition_state_cum_unit_susceptible = models.IntegerField(blank=True, null=True)
    _transition_state_cum_animal_susceptible = models.IntegerField(blank=True, null=True)
    _transition_state_cum_unit_latent = models.IntegerField(blank=True, null=True)
    _transition_state_cum_animal_latent = models.IntegerField(blank=True, null=True)
    _transition_state_cum_unit_subclinical = models.IntegerField(blank=True, null=True)
    _transition_state_cum_animal_subclinical = models.IntegerField(blank=True, null=True)
    _transition_state_cum_unit_clinical = models.IntegerField(blank=True, null=True)
    _transition_state_cum_animal_clinical = models.IntegerField(blank=True, null=True)
    _transition_state_cum_unit_nat_immune = models.IntegerField(blank=True, null=True)
    _transition_state_cum_animal_nat_immune = models.IntegerField(blank=True, null=True)
    _transition_state_cum_unit_vac_immune = models.IntegerField(blank=True, null=True)
    _transition_state_cum_animal_vac_immune = models.IntegerField(blank=True, null=True)
    _transition_state_cum_unit_destroyed = models.IntegerField(blank=True, null=True)
    _transition_state_cum_animal_destroyed = models.IntegerField(blank=True, null=True)
    _infection_cum_unit_initial = models.IntegerField(blank=True, null=True)
    _infection_cum_animal_initial = models.IntegerField(blank=True, null=True)
    _infection_cum_unit_air = models.IntegerField(blank=True, null=True)
    _infection_cum_animal_air = models.IntegerField(blank=True, null=True)
    _infection_cum_unit_dir = models.IntegerField(blank=True, null=True)
    _infection_cum_animal_dir = models.IntegerField(blank=True, null=True)
    _infection_cum_unit_ind = models.IntegerField(blank=True, null=True)
    _infection_cum_animal_ind = models.IntegerField(blank=True, null=True)
    _exposed_cum_unit_dir = models.IntegerField(blank=True, null=True)
    _exposed_cum_animal_dir = models.IntegerField(blank=True, null=True)
    _exposed_cum_unit_ind = models.IntegerField(blank=True, null=True)
    _exposed_cum_animal_ind = models.IntegerField(blank=True, null=True)
    _trace_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True)
    _trace_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True)
    _trace_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True)
    _trace_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True)
    _trace_cum_unit_dir_p_fwd = models.IntegerField(blank=True, null=True)
    _trace_cum_animal_dir_pfwd = models.IntegerField(blank=True, null=True)
    _trace_cum_unit_ind_p_fwd = models.IntegerField(blank=True, null=True)
    _trace_cum_animal_ind_p_fwd = models.IntegerField(blank=True, null=True)
    _trace_cum_unit_dir_back = models.IntegerField(blank=True, null=True)
    _trace_cum_animal_dir_back = models.IntegerField(blank=True, null=True)
    _trace_cum_unit_ind_back = models.IntegerField(blank=True, null=True)
    _trace_cum_animal_ind_back = models.IntegerField(blank=True, null=True)
    _trace_cum_unit_dir_p_back = models.IntegerField(blank=True, null=True)
    _trace_cum_animal_dir_pback = models.IntegerField(blank=True, null=True)
    _trace_cum_unit_ind_p_back = models.IntegerField(blank=True, null=True)
    _trace_cum_animal_ind_p_back = models.IntegerField(blank=True, null=True)
    _trace_origin_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True)
    _trace_origin_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True)
    _trace_origin_cum_unit_dir_back = models.IntegerField(blank=True, null=True)
    _trace_origin_cum_unit_ind_back = models.IntegerField(blank=True, null=True)
    _exam_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True)
    _exam_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True)
    _exam_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True)
    _exam_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True)
    _exam_cum_unit_dir_back = models.IntegerField(blank=True, null=True)
    _exam_cum_animal_dir_back = models.IntegerField(blank=True, null=True)
    _exam_cum_unit_ind_back = models.IntegerField(blank=True, null=True)
    _exam_cum_animal_ind_back = models.IntegerField(blank=True, null=True)
    _test_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True)
    _test_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True)
    _test_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True)
    _test_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True)
    _test_cum_unit_dir_back = models.IntegerField(blank=True, null=True)
    _test_cum_animal_dir_back = models.IntegerField(blank=True, null=True)
    _test_cum_unit_ind_back = models.IntegerField(blank=True, null=True)
    _test_cum_animal_ind_back = models.IntegerField(blank=True, null=True)
    _test_cum_unit_true_pos = models.IntegerField(blank=True, null=True)
    _test_cum_animal_true_pos = models.IntegerField(blank=True, null=True)
    _test_cum_unit_true_neg = models.IntegerField(blank=True, null=True)
    _test_cum_animal_true_neg = models.IntegerField(blank=True, null=True)
    _test_cum_unit_false_pos = models.IntegerField(blank=True, null=True)
    _test_cum_animal_false_pos = models.IntegerField(blank=True, null=True)
    _test_cum_unit_false_neg = models.IntegerField(blank=True, null=True)
    _test_cum_animal_false_neg = models.IntegerField(blank=True, null=True)
    _detect_cum_unit_clin = models.IntegerField(blank=True, null=True)
    _detect_cum_animal_clin = models.IntegerField(blank=True, null=True)
    _detect_cum_unit_test = models.IntegerField(blank=True, null=True)
    _detect_cum_animal_test = models.IntegerField(blank=True, null=True)
    _destroy_cum_unit_initial = models.IntegerField(blank=True, null=True)
    _destroy_cum_animal_initial = models.IntegerField(blank=True, null=True)
    _destroy_cum_unit_detect = models.IntegerField(blank=True, null=True)
    _destroy_cum_animal_detect = models.IntegerField(blank=True, null=True)
    _destroy_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True)
    _destroy_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True)
    _destroy_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True)
    _destroy_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True)
    _destroy_cum_unit_dir_back = models.IntegerField(blank=True, null=True)
    _destroy_cum_animal_dir_back = models.IntegerField(blank=True, null=True)
    _destroy_cum_unit_ind_back = models.IntegerField(blank=True, null=True)
    _destroy_cum_animal_ind_back = models.IntegerField(blank=True, null=True)
    _destroy_cum_unit_ring = models.IntegerField(blank=True, null=True)
    _destroy_cum_animal_ring = models.IntegerField(blank=True, null=True)
    _destroy_wait_unit_max = models.IntegerField(blank=True, null=True)
    _destroy_wait_animal_max = models.IntegerField(blank=True, null=True)
    _destroy_wait_unit_max_day = models.IntegerField(blank=True, null=True)
    _destroy_wait_animal_max_day = models.IntegerField(blank=True, null=True)
    _destroy_wait_unit_time_max = models.IntegerField(blank=True, null=True)
    _destroy_wait_unit_time_avg = models.FloatField(blank=True, null=True)
    _destroy_wait_unit_days_in_queue = models.FloatField(blank=True, null=True)
    _destroy_wait_animal_days_in_queue = models.FloatField(blank=True, null=True)
    _vac_cum_unit_initial = models.IntegerField(blank=True, null=True)
    _vac_cum_animal_initial = models.IntegerField(blank=True, null=True)
    _vac_cum_unit_ring = models.IntegerField(blank=True, null=True)
    _vac_cum_animal_ring = models.IntegerField(blank=True, null=True)
    _vac_wait_unit_max = models.IntegerField(blank=True, null=True)
    _vac_wait_animal_max = models.FloatField(null=True, blank=True)
    _vac_wait_unit_max_day = models.IntegerField(blank=True, null=True)
    _vac_wait_animal_max_day = models.IntegerField(blank=True, null=True)
    _vac_wait_unit_time_max = models.FloatField(null=True, blank=True)
    _vac_wait_unit_time_avg = models.IntegerField(blank=True, null=True)
    _zone_foci = models.IntegerField(blank=True, null=True)
    _first_detection = models.IntegerField(blank=True, null=True)
    _first_det_unit_inf = models.IntegerField(blank=True, null=True)
    _first_detect_animal_inf = models.IntegerField(blank=True, null=True)
    _first_destruction = models.IntegerField(blank=True, null=True)
    _first_vaccination = models.IntegerField(blank=True, null=True)
    _last_detection = models.IntegerField(blank=True, null=True)


class OutIterationByZone(models.Model):
    _iteration = models.IntegerField(blank=True, null=True)
    _zone = models.ForeignKey(InZone)
    _max_zone_area = models.FloatField(blank=True, null=True)
    _max_zone_area_day = models.IntegerField(blank=True, null=True)
    _final_zone_area = models.FloatField(blank=True, null=True)
    _max_zone_perimeter = models.FloatField(blank=True, null=True)
    _max_zone_perimeter_day = models.IntegerField(blank=True, null=True)
    _final_zone_perimeter = models.FloatField(blank=True, null=True)


class OutIterationByZoneAndProductionType(models.Model):
    _iteration = models.IntegerField(blank=True, null=True)
    _zone = models.ForeignKey(InZone)
    _production_type = models.ForeignKey(InProductionType)
    _unit_days_in_zone = models.IntegerField(blank=True, null=True)
    _animal_days_in_zone = models.IntegerField(blank=True, null=True)
    _cost_surveillance = models.FloatField(blank=True, null=True)


class OutIterationCosts(models.Model):
    _iteration = models.IntegerField(blank=True, null=True)
    _production_type = models.ForeignKey(InProductionType)
    _destroy_appraisal = models.FloatField(blank=True, null=True)
    _destroy_cleaning = models.FloatField(blank=True, null=True)
    _destroy_euthanasia = models.FloatField(blank=True, null=True)
    _destroy_indemnification = models.FloatField(blank=True, null=True)
    _destroy_disposal = models.FloatField(blank=True, null=True)
    _vac_cum_setup = models.FloatField(blank=True, null=True)
    _vac_cum_vaccination = models.FloatField(blank=True, null=True)



