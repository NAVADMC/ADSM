# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True

# Changes made in ScenarioCreator/models.py propagate to the script output

# TextField is more costly than CharField.  Only use TextField for descriptions or urls.
# CharFields are max=255 characters and are presented as a single text line in forms.
# TextFields are unlimited and presented as giant text boxes in forms.
# Search:  db_column='[^']*',  to remove column names
from __future__ import unicode_literals

from django.db import models


def chc(choice_list):
    return tuple((x, x) for x in choice_list)


class DbSchemaVersion(models.Model):
    version_number = models.CharField(max_length=255, unique=True)
    version_application = models.CharField(max_length=255, )
    version_date = models.CharField(max_length=255, )
    version_info_url = models.TextField(blank=True)
    version_id = models.IntegerField(blank=True, null=True)


class DynamicBlob(models.Model):
    zone_perimeters = models.CharField(max_length=255, blank=True)


class DynamicHerd(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    initial_state_code = models.CharField(max_length=255, )
    days_in_initial_state = models.IntegerField()
    days_left_in_initial_state = models.IntegerField()
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


class InChart(models.Model):
    field_name = models.CharField(max_length=255, blank=True)
    chart_name = models.CharField(max_length=255, )
    _ispdf = models.BooleanField()
    chart_type = models.CharField(max_length=255, blank=True)
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
    shape = models.FloatField(blank=True, null=True)
    n = models.IntegerField(blank=True, null=True)
    p = models.FloatField(blank=True, null=True)
    m = models.IntegerField(blank=True, null=True)
    d = models.IntegerField(blank=True, null=True)
    dmin = models.IntegerField(blank=True, null=True)
    dmax = models.IntegerField(blank=True, null=True)
    theta = models.FloatField(blank=True, null=True)
    a = models.FloatField(blank=True, null=True)
    s = models.IntegerField(blank=True, null=True)
    x_axis_units = models.CharField(max_length=255, blank=True)
    y_axis_units = models.CharField(max_length=255, blank=True)
    _notes = models.TextField(blank=True)


class InChartDetail(models.Model):
    _chartid = models.IntegerField()
    _pointorder = models.IntegerField()
    _x = models.FloatField()
    _y = models.FloatField()


class InControlGlobal(models.Model):
    include_detection = models.BooleanField(default=False, )
    include_tracing = models.BooleanField(default=False, )
    include_tracing_herd_exam = models.BooleanField(default=False, )
    include_tracing_testing = models.BooleanField(default=False, )
    include_destruction = models.BooleanField(default=False, )
    destruction_delay = models.IntegerField(blank=True, null=True)
    _destrcapacityrelid = models.IntegerField(blank=True, null=True)
    destruction_priority_order = models.CharField(max_length=255, blank=True)
    destrucion_reason_order = models.CharField(max_length=255, blank=True)
    include_vaccination = models.BooleanField(default=False, )
    vaccincation_detected_units_before_start = models.IntegerField(blank=True, null=True)
    _vacccapacityrelid = models.IntegerField(blank=True, null=True)
    vaccination_priority_order = models.CharField(max_length=255, blank=True)
    include_zones = models.BooleanField(default=False, )
    vaccination_retrospective_days = models.IntegerField(blank=True, null=True)
    _vacccapacitystartrelid = models.IntegerField(blank=True, null=True)
    _vacccapacityrestartrelid = models.IntegerField(blank=True, null=True)


class InControlPlan(models.Model):
    control_plan_name = models.CharField(max_length=255, )
    control_plan_description = models.TextField(blank=True)
    control_plan_group = models.CharField(max_length=255, blank=True)


class InControlsProductionType(models.Model):
    production_type_id = models.IntegerField(unique=True)
    use_detection = models.BooleanField(default=False, )
    _detprobobsvstimeclinicalrelid = models.IntegerField(blank=True, null=True)
    _detprobreportvsfirstdetectionrelid = models.IntegerField(blank=True, null=True)
    trace_direct_forward = models.BooleanField(default=False, )
    trace_direct_back = models.BooleanField(default=False, )
    trace_direct_success = models.FloatField(blank=True, null=True)
    trace_direct_trace_period = models.BooleanField(default=False, )
    trace_indirect_forward = models.BooleanField(default=False, )
    trace_indirect_back = models.BooleanField(default=False, )
    trace_indirect_success = models.FloatField(blank=True, null=True)
    trace_indirect_trace_period = models.BooleanField(default=False, )
    _tracedelaypdfid = models.IntegerField(blank=True, null=True)
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
    _vaccimmuneperiodpdfid = models.IntegerField(blank=True, null=True)
    vaccinate_ring = models.BooleanField(default=False, )
    vaccination_ring_radius = models.FloatField(blank=True, null=True)
    vaccination_priority = models.IntegerField(blank=True, null=True)
    cost_destroy_appraisal_per_unit = models.FloatField(blank=True, null=True)
    cost_destroy_cleaning_per_unit = models.FloatField(blank=True, null=True)
    cost_destroy_euthanasia_per_animal = models.FloatField(blank=True, null=True)
    cost_destroy_indemnification_per_animal = models.FloatField(blank=True, null=True)
    cost_destroy_disposal_per_animal = models.FloatField(blank=True, null=True)
    cost_vaccinate_setup_per_unit = models.FloatField(blank=True, null=True)
    cost_vaccinate_threshold = models.IntegerField(blank=True, null=True)
    cost_vaccinate_baseline_per_animal = models.FloatField(blank=True, null=True)
    cost_vaccinate_additional_per_animal = models.FloatField(blank=True, null=True)
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
    _testdelaypdfid = models.IntegerField(blank=True, null=True)
    vaccinate_restrospective_days = models.BooleanField(default=False, )


class InDiseaseGlobal(models.Model):
    disease_name = models.TextField(blank=True)
    disease_description = models.TextField(blank=True)


class InDiseaseProductionType(models.Model):
    _production_type_id = models.IntegerField(blank=True, null=True)
    use_disease_transition = models.BooleanField(default=False, )
    _dislatentperiodpdfid = models.IntegerField(blank=True, null=True)
    _dissubclinicalperiodpdfid = models.IntegerField(blank=True, null=True)
    _disclinicalperiodpdfid = models.IntegerField(blank=True, null=True)
    _disimmuneperiodpdfid = models.IntegerField(blank=True, null=True)
    _disprevalencerelid = models.IntegerField(blank=True, null=True)


class InDiseaseSpread(models.Model):
    _productiontypepairid = models.IntegerField(unique=True)
    spread_method_code = models.CharField(max_length=255, blank=True)
    latent_can_infect = models.BooleanField(default=False, )
    subclinical_can_infect = models.BooleanField(default=False, )
    mean_contact_rate = models.FloatField(blank=True, null=True)
    use_fixed_contact_rate = models.BooleanField(default=False, )
    fixed_contact_rate = models.FloatField(blank=True, null=True)
    infection_probability = models.FloatField(blank=True, null=True)
    _distancepdfid = models.IntegerField(blank=True, null=True)
    _movementcontrolrelid = models.IntegerField(blank=True, null=True)
    _transportdelaypdfid = models.IntegerField(blank=True, null=True)
    probability_airborne_spread_1km = models.FloatField(blank=True, null=True)
    max_distance_airborne_spread = models.FloatField(blank=True, null=True)
    wind_direction_start = models.IntegerField(blank=True, null=True)
    wind_direction_end = models.IntegerField(blank=True, null=True)


class InGeneral(models.Model):
    language = models.CharField(choices=(('en',"English"), ('es',"Spanish")), max_length=255, blank=True)
    scenario_description = models.TextField(blank=True,
                                            help_text='A short description of the scenario being simulated.')
    iterations = models.IntegerField(blank=True, null=True,
                                     help_text='The number of simulations to run.')
    days = models.IntegerField(blank=True, null=True,
                               help_text='The maximum number of days in a simulation run. A simulation run may end earlier, if there are no latent or infectious animals and no module has pending actions to complete.')
    sim_stop_reason = models.CharField(max_length=255, blank=True,
        choices=(('disease-end','Simulation will stop when there are no more latent or infectious units.'),
                 ('first-detection','Simulation will stop when the first detection occurs.')))
    include_contact_spread = models.BooleanField(default=False, )
    include_airborne_spread = models.BooleanField(default=False, )
    use_airborne_exponential_decay = models.BooleanField(default=False, )
    use_within_herd_prevalence = models.BooleanField(default=False, )
    cost_track_destruction = models.BooleanField(default=False, )
    cost_track_vaccination = models.BooleanField(default=False, )
    cost_track_zone_surveillance = models.BooleanField(default=False, )
    use_fixed_random_seed = models.BooleanField(default=False, )
    random_seed = models.IntegerField(blank=True, null=True)
    ## Outputs requested:
    save_all_daily_outputs = models.BooleanField(default=False, )
    save_daily_outputs_for_iterations = models.BooleanField(default=False, )
    write_daily_states_file = models.BooleanField(default=False, 
      help_text='The number of units in each state.  This variable always reports the counts on the day of reporting, regardless of whether it is reported daily, weekly, or at some other interval.  This variable is needed to create a plot of the states over time.')
    daily_states_filename = models.CharField(max_length=255, blank=True)
    save_daily_events = models.BooleanField(default=False, )
    save_daily_exposures = models.BooleanField(default=False, )
    save_iteration_outputs_for_herds = models.BooleanField(default=False, )
    write_map_output = models.BooleanField(default=False, )
    map_directory = models.CharField(max_length=255, blank=True)


class InProductionType(models.Model):
    production_type_name = models.CharField(max_length=255, )
    production_type_description = models.TextField(blank=True) # This field type is a guess.


class InProductionTypePair(models.Model):
    _sourceproductiontypeid = models.IntegerField()
    _destproductiontypeid = models.IntegerField()
    use_direct_contact = models.BooleanField(default=False, )
    _directcontactspreadid = models.IntegerField(blank=True, null=True)
    use_indirect_contact = models.BooleanField(default=False, )
    _indirectcontactspreadid = models.IntegerField(blank=True, null=True)
    use_airborne_spread = models.BooleanField(default=False, )
    _airbornecontactspreadid = models.IntegerField(blank=True, null=True)


class InZone(models.Model):
    zone_description = models.TextField()
    zone_radius = models.FloatField()


class InZoneProductionTypePair(models.Model):
    _zoneid = models.IntegerField()
    _production_type_id = models.IntegerField()
    use_directmovement_control = models.BooleanField(default=False, )
    _zonedirectmovementrelid = models.IntegerField(blank=True, null=True)
    use_indirect_movement_control = models.BooleanField(default=False, )
    _zoneindirectmovementrelid = models.IntegerField(blank=True, null=True)
    use_detection_multiplier = models.BooleanField(default=False, )
    zone_detection_multiplier = models.FloatField(blank=True, null=True)
    cost_surv_per_animal_day = models.FloatField(blank=True, null=True)


class ReadAllCodes(models.Model):
    _code = models.CharField(max_length=255, )
    _code_type = models.CharField(max_length=255, )
    _code_description = models.TextField()


class ReadAllCodeTypes(models.Model):
    _code_type = models.CharField(max_length=255, )
    _code_type_description = models.TextField()

