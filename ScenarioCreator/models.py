# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True

# Changes made in ScenarioCreator/models.py propagate to the script output

# TextField is more costly than CharField.  Only use TextField for descriptions or urls.
# CharFields are max=255 characters and are presented as a single text line in forms.
# TextFields are unlimited and presented as giant text boxes in forms.
# Search:  db_column='[^']*',  to remove column names

from django.db import models
from django_extras.db.models import PercentField, LatitudeField, LongitudeField, MoneyField


def chc(*choice_list):
    return tuple((x, x) for x in choice_list)


class DbSchemaVersion(models.Model):
    version_number = models.CharField(max_length=255, unique=True,
        help_text='', )
    version_application = models.CharField(max_length=255,
        help_text='This gets passed around as an identifier - not sure of definition', )
    version_date = models.CharField(max_length=255,
        help_text='', )
    version_info_url = models.TextField(blank=True,
        help_text='', )
    version_id = models.IntegerField(blank=True, null=True,
        help_text='Number of the NAADSM Version used to run the simulation.', )


class DynamicBlob(models.Model):
    zone_perimeters = models.CharField(max_length=255, blank=True,
        help_text='', )  # polygons?


class DynamicUnit(models.Model):
    production_type = models.ForeignKey('InProductionType',
        help_text='The production type that these outputs apply to.', )
    latitude = LatitudeField(
        help_text='The latitude used to georeference this unit.', )
    longitude = LongitudeField(
        help_text='The longitude used to georeference this unit.', )
    initial_state_code = models.CharField(max_length=255,
        help_text='Code indicating the actual disease state of the unit at the beginning of the simulation.',
                                          choices=(('L', 'Latent'),
                                                   ('S', 'Susceptible'),
                                                   ('B', 'Subclinical'),
                                                   ('C', 'Clinical'),
                                                   ('N', 'Naturally Immune'),
                                                   ('V', 'Vaccine Immune'),
                                                   ('D', 'Destroyed')))
    days_in_initial_state = models.IntegerField(blank=True, null=True,
        help_text='The number of days that the unit will remain in its initial state unless preempted by other events.', )
    days_left_in_initial_state = models.IntegerField(blank=True, null=True,
        help_text='', )
    initial_size = models.IntegerField(
        help_text='The number of animals in the unit.', )
    _final_state_code = models.CharField(max_length=255, blank=True,
        help_text='Code indicating the actual disease state of the unit at the end of the simulation.', )
    _final_control_state_code = models.CharField(max_length=255, blank=True,
        help_text='', )
    _final_detection_state_code = models.CharField(max_length=255, blank=True,
        help_text='', )
    _cum_infected = models.IntegerField(blank=True, null=True,
        help_text='The total number of iterations in which this unit became infected.', )
    _cum_detected = models.IntegerField(blank=True, null=True,
        help_text='The total number of iterations in which this unit was detected.', )
    _cum_destroyed = models.IntegerField(blank=True, null=True,
        help_text='The total number of iterations in which this unit was destroyed.', )
    _cum_vaccinated = models.IntegerField(blank=True, null=True,
        help_text='The total number of iterations in which this unit was vaccinated.', )
    user_defined_1 = models.TextField(blank=True)
    user_defined_2 = models.TextField(blank=True)
    user_defined_3 = models.TextField(blank=True)
    user_defined_4 = models.TextField(blank=True)

'''InChart is an equation model that defines either a Probability Distribution Function (pdf) or
 a relational function (relid) depending on which child class is used.  '''
class InChart(models.Model):
    chart_name = models.CharField(max_length=255,
        help_text='User-assigned name for each function.', )
    # field_name = models.CharField(max_length=255, )  # I don't think this is necessary
    x_axis_units = models.CharField(max_length=255, default="Days",
        help_text='Specifies the descriptive units for the x axis in relational functions.', )
    y_axis_units = models.CharField(max_length=255, blank=True,
        help_text='Specifies the descriptive units for the x axis in probability density and relational functions.', )
    notes = models.TextField(blank=True, null=True,
        help_text='', )  # Why is this hidden?
    class Meta:
        abstract = True


'''There are a large number of fields in this model because different chart_type use different
parameters.  Parameters are all listed as optional because they are frequently unused.  A second
layer of validation will be necessary for required parameters per chart_type.'''
class ProbabilityEquation(InChart):
    chart_type = models.CharField(max_length=255, blank=True,
        help_text='For probability density functions identifies the type of function.',
                                  choices=chc("Point", "Uniform", "Triangular", "Piecewise", "Histogram", "Gaussian",
                                              "Poisson", "Beta", "Gamma", "Weibull", "Exponential", "Pearson5",
                                              "Logistic",
                                              "LogLogistic", "Lognormal", "NegativeBinomial", "Pareto", "Bernoulli",
                                              "Binomial", "Discrete Uniform", "Hypergeometric", "Inverse Gaussian"))
    mean = models.FloatField(blank=True, null=True,
        help_text='The mean for probability density function types Gaussian Lognormal Possoin and Exponential.', )
    std_dev = models.FloatField(blank=True, null=True,
        help_text='The mean for probability density function types Gaussian and Lognormal.', )
    min = models.FloatField(blank=True, null=True,
        help_text='The minimumfor probability density function types Uniform Triangular Beta and betaPERT.', )
    mode = models.FloatField(blank=True, null=True,
        help_text='The Mode for probability density function types Point Triangular and BetaPERT.', )
    max = models.FloatField(blank=True, null=True,
        help_text='The maximum value for probability density function types Uniform Triangular Beta and BetaPERT.', )
    alpha = models.FloatField(blank=True, null=True,
        help_text='The alpha parameter for probability density function types Gamma Weibull and Pearson 5 or the alpha1 parameter for Beta probability density functions.', )
    alpha2 = models.FloatField(blank=True, null=True,
        help_text='The alpha2 parameter for Beta probability density function types.', )
    beta = models.FloatField(blank=True, null=True,
        help_text='The beta parameter for probability density function types Gamma Weibull and Pearson 5.', )
    location = models.FloatField(blank=True, null=True,
        help_text='The location parameter for probability density function types Logistic and Loglogistic.', )
    scale = models.FloatField(blank=True, null=True,
        help_text='The scale parameter for probability density function types Logistic and Loglogistic.', )
    shape = models.FloatField(blank=True, null=True,
        help_text='The shape parameter for probability density function types Loglogistic Inverse Gaussian.', )  # or should this be the chart_type list of PDF functions?
    n = models.IntegerField(blank=True, null=True,
        help_text='The n parameter for probability density function types Binomial Hypergeometric.', )
    p = models.FloatField(blank=True, null=True,
        help_text='The p parameter for probability density function types Negative Binomial Bernoulli.', )
    m = models.IntegerField(blank=True, null=True,
        help_text='The m parameter for probability density function types Hypergeometric.', )
    d = models.IntegerField(blank=True, null=True,
        help_text='The d parameter for probability density function types Hypergeometric.', )
    theta = models.FloatField(blank=True, null=True,
        help_text='The Theta parameter for probability density function types Pareto.', )
    a = models.FloatField(blank=True, null=True,
        help_text='The a parameter for probability density function types Pareto.', )
    s = models.IntegerField(blank=True, null=True,
        help_text='The s parameter for probability density function types Negative Binomial.', )


class RelationalEquation(InChart):
    pass  # Inherited fields


class EquationPoint(models.Model):
    chart = models.ForeignKey(RelationalEquation)
    _point_order = models.IntegerField()
    _x = models.FloatField(
        help_text='The x value of the point.', )
    _y = models.FloatField(
        help_text='The y value of the point.', )


class InControlGlobal(models.Model):
    _include_detection = models.BooleanField(default=False,
        help_text='Indicates if detection of disease in any production type will be modeled.', )
    _include_tracing = models.BooleanField(default=False,
        help_text='Indicates if tracing of units in any production type will be modeled.', )
    _include_tracing_unit_exam = models.BooleanField(default=False,
        help_text='Indicates if tracing using diagnostic testing in any production type will be modeled.', )
    _include_tracing_testing = models.BooleanField(default=False,
        help_text='Indicates if tracing using unit examination in any production type will be modeled.', )
    _include_destruction = models.BooleanField(default=False,
        help_text='Indicates if destruction of units in any production type will be modeled.', )
    _include_vaccination = models.BooleanField(default=False,
        help_text='A string that identifies the secondary priority order for destruction.', )
    _include_zones = models.BooleanField(default=False,
        help_text='Indicates if zones will be modeled.', )
    destruction_delay = models.IntegerField(blank=True, null=True,
        help_text='The number of days that must pass after the first detection before a destruction program can begin.', )
    destruction_capacity_relid = models.ForeignKey(RelationalEquation, related_name='+', blank=True, null=True,
        help_text="The relational function used to define the daily destruction capacity.", )
    destruction_priority_order = models.CharField(max_length=255, blank=True,
        help_text='A string that identifies the primary priority order for destruction.', )  # These are an odd legacy.  Leave it for now
    destrucion_reason_order = models.CharField(max_length=255, blank=True,
        help_text='A string that identifies the primary priority order for destruction.', )
    trigger_vaccincation_after_detected_units_count = models.IntegerField(blank=True, null=True,
        help_text='The number of clinical units which must be detected before the initiation of a vaccination program.', )
    vaccination_capacity_relid = models.ForeignKey(RelationalEquation, related_name='+', blank=True, null=True,
        help_text='Relational fucntion used to define the daily vaccination capacity.', )
    vaccination_priority_order = models.CharField(max_length=255, blank=True,
        help_text='A string that identifies the primary priority order for vaccination.', )


class InControlPlan(models.Model):
    control_plan_name = models.CharField(max_length=255,
                                         help_text='Name your Protocol so you can recognize it later.', )
    notes = models.TextField(blank=True, )
    control_plan_group = models.CharField(max_length=255, blank=True)


class InControlsProductionType(models.Model):
    production_type = models.ForeignKey('InProductionType',
        help_text='The production type that these outputs apply to.', )
    use_detection = models.BooleanField(default=False,
        help_text='Indicates if disease detection will be modeled for units of this production type.', )
    detection_probability_for_observed_time_in_clinical_relid = models.ForeignKey(RelationalEquation, related_name='+', blank=True, null=True,
        help_text='Relational function used to define the probability of observing clinical signs in units of this production type.', )
    detection_probability_report_vs_first_detection_relid = models.ForeignKey(RelationalEquation, related_name='+', blank=True, null=True,
        help_text='Relational function used to define the probability of reportin clinical signs in units of this production type.')
    trace_direct_forward = models.BooleanField(default=False,
        help_text='Indicator that trace forward will be conducted for direct contacts where the reported unit was the source of contact and was of this production type.', )
    trace_direct_back = models.BooleanField(default=False,
        help_text='Indicator that trace back will be conducted for direct contacts where the reported unit was the source of contact and was of this production type.', )
    trace_direct_success = PercentField(blank=True, null=True,
        help_text='Probability of success of trace for direct contact.', )
    trace_direct_trace_period = models.BooleanField(default=False,
        help_text='Days before detection  (critical period) for tracing of direct contacts.', )
    trace_indirect_forward = models.BooleanField(default=False,
        help_text='Indicator that trace forward will be conducted for indirect contacts where the reported unit was the source of contact and was of this production type.', )
    trace_indirect_back = models.BooleanField(default=False,
        help_text='Indicator that trace back will be conducted for indirect contacts where the reported unit was the source of contact and was of this production type.', )
    trace_indirect_success = PercentField(blank=True, null=True,
        help_text='Probability of success of trace for indirect contact.', )
    trace_indirect_trace_period = models.BooleanField(default=False,
        help_text='Days before detection  (critical period) for tracing of indirect contacts.', )
    trace_delay_pdf = models.ForeignKey(ProbabilityEquation, related_name='+',
        help_text='Shipping delay function.', )
    use_destruction = models.BooleanField(default=False,
        help_text='Indicates if detected clinical units of this production type will be destroyed.', )
    destruction_is_ring_trigger = models.BooleanField(default=False,
        help_text='Indicates if detection of a unit of this production type will trigger the formation of a destruction ring.', )
    destruction_ring_radius = models.FloatField(blank=True, null=True,
        help_text='Radius in kilometers of the destruction ring.', )
    destruction_is_ring_target = models.BooleanField(default=False,
        help_text='Indicates if unit of this production type will be subject to preemptive ring destruction.', )
    destroy_direct_forward_traces = models.BooleanField(default=False,
        help_text='Indicates is units of this type identified by trace forward of indirect contacts will be subject to preemptive desctruction.', )
    destroy_indirect_forward_traces = models.BooleanField(default=False,
        help_text='Indicates is units of this type identified by trace forward of direct contacts will be subject to preemptive desctruction.', )
    destroy_direct_back_traces = models.BooleanField(default=False,
        help_text='Indicates is units of this type identified by tracebackof direct contacts will be subject to preemptive desctruction.', )
    destroy_indirect_back_traces = models.BooleanField(default=False,
        help_text='Indicates is units of this type identified by traceback of indirect contacts will be subject to preemptive desctruction.', )
    destruction_priority = models.IntegerField(blank=True, null=True,
        help_text='The desctruction prioroty of this production type relative to other production types.  A lower number indicates a higher priority.', )
    use_vaccination = models.BooleanField(default=False,
        help_text='Indicates if units of this production type will be subject to vaccination.', )
    vaccination_min_time_between = models.IntegerField(blank=True, null=True,
        help_text='The minimum time in days between vaccination for units of this production type.', )
    vaccinate_detected = models.BooleanField(default=False,
        help_text='Indicates if units of this production type will be subject to vaccination if infected and detected.', )
    days_to_immunity = models.IntegerField(blank=True, null=True,
        help_text='The number of days required for the onset of vaccine immunity in a newly vaccinated unit of this type.', )
    vaccine_immune_period_pdf = models.ForeignKey(ProbabilityEquation, related_name='+',
        help_text='Defines the vaccine immune period for units of this production type.', )
    vaccinate_ring = models.BooleanField(default=False,
        help_text='Indicates if detection of a clinical unit of this type will trigger a vaccination ring.', )
    vaccination_ring_radius = models.FloatField(blank=True, null=True,
        help_text='Radius in kilometers of the vaccination ring.', )
    vaccination_priority = models.IntegerField(blank=True, null=True,
        help_text='The vacination priority of this production type relative to other production types.  A lower number indicates a higher priority.', )
    cost_destroy_appraisal_per_unit = MoneyField(default=0.0,
        help_text='The cost associated with appraisal for each destroyed unit of this type.', )
    cost_destroy_cleaning_per_unit = MoneyField(default=0.0,
        help_text='The cost associated with cleaning and disinfection for each destroyed unit of this type.', )
    cost_destroy_euthanasia_per_animal = MoneyField(default=0.0,
        help_text='The cost associated with euthanizing each destroyed animal of this type.', )
    cost_destroy_indemnification_per_animal = MoneyField(default=0.0,
        help_text='The cost of indemnification for each destroyed animal of this type.', )
    cost_destroy_disposal_per_animal = MoneyField(default=0.0,
        help_text='The cost of carcass disposal for each destroyed animal of this type.', )
    cost_vaccinate_setup_per_unit = MoneyField(default=0.0,
        help_text='The cost of site setup for each vaccinated unit of this type.', )
    cost_vaccinate_threshold = models.IntegerField(blank=True, null=True,
        help_text='The number of animals of this type that can be vaccinated before the cost of vaccination increases.', )
    cost_vaccinate_baseline_per_animal = MoneyField(default=0.0,
        help_text='The baseline cost of vaccination for each vaccinated animal of this type. This cost applies to all vaccinations before the threshold is set in costVaccThershold is met. ', )
    cost_vaccinate_additional_per_animal = MoneyField(default=0.0,
        help_text='The additional cost of vaccination for each vaccinated animal of this type after the threshold is exceeded.', )
    zone_detection_is_trigger = models.BooleanField(default=False,
        help_text='Indicator if detection of infected units of this production type will trigger a zone focus.', )
    zone_direct_trace_is_trigger = models.BooleanField(default=False,
        help_text='Indicator if direct tracing of infected units of this production type will trigger a zone focus.', )
    zone_indirect_trace_is_trigger = models.BooleanField(default=False,
        help_text='Indicator if indirect tracing of infected units of this production type will trigger a zone focus.', )
    exam_direct_forward = models.BooleanField(default=False,
        help_text='Indicator if units identified by the trace-forward of direct contact will be examined for clinical signs of disease.', )
    exam_direct_forward_multiplier = models.FloatField(blank=True, null=True,
        help_text='Multiplier for the probability of observice clinical signs in units identified by the trace-forward of direct contact.', )
    exam_indirect_forward = models.BooleanField(default=False,
        help_text='Indicator if units identified by the trace-forward of indirect contact will be examined for clinical signs of disease.', )
    exam_indirect_forward_multiplier = models.FloatField(blank=True, null=True,
        help_text='Multiplier for the probability of observice clinical signs in units identified by the trace-forward of indirect contact .', )
    exam_direct_back = models.BooleanField(default=False,
        help_text='Indicator if units identified by the trace-back of direct contact will be examined for clinical signs of disease.', )
    exam_direct_back_multiplier = models.FloatField(blank=True, null=True,
        help_text='Multiplier for the probability of observice clinical signs in units identified by the trace-back of direct contact.', )
    exam_indirect_back = models.BooleanField(default=False,
        help_text='Indicator if units identified by the trace-back of indirect contact will be examined for clinical signs of disease.', )
    exam_indirect_back_multiplier = models.FloatField(blank=True, null=True,
        help_text='Multiplier for the probability of observice clinical signs in units identified by the trace-back of indirect contact.', )
    test_direct_forward = models.BooleanField(default=False,
        help_text='Indicator that diagnostic testing shuold be performed on units identified by trace-forward of direct contacts.', )
    test_indirect_forward = models.BooleanField(default=False,
        help_text='Indicator that diagnostic testing shuold be performed on units identified by trace-forward of indirect contacts.', )
    test_direct_back = models.BooleanField(default=False,
        help_text='Indicator that diagnostic testing should be performed on units identified by trace-back of direct contacts.', )
    test_indirect_back = models.BooleanField(default=False,
        help_text='Indicator that diagnostic testing should be performed on units identified by trace-back of indirect contacts.', )
    test_specificity = models.FloatField(blank=True, null=True,
        help_text='Test Specificity for units of this production type', )
    test_sensitivity = models.FloatField(blank=True, null=True,
        help_text='Test Sensitivity for units of this production type', )
    test_delay_pdf = models.ForeignKey(ProbabilityEquation, related_name='+',
        help_text='Function that describes the delay in obtaining test results.', )
    vaccinate_retrospective_days = models.BooleanField(default=False,
        help_text='Number of days in retrospect that should be used to determine which herds to vaccinate.', )


class InDiseaseGlobal(models.Model):
    disease_name = models.TextField(blank=True)
    disease_description = models.TextField(blank=True)


class InDiseaseProductionType(models.Model):
    production_type = models.ForeignKey('InProductionType',
        help_text='The production type that these outputs apply to.', )
    use_disease_transition = models.BooleanField(default=False,
        help_text='Indicates if units of this production type will undergo disease transition.', )
    disease_latent_period_pdf = models.ForeignKey(ProbabilityEquation, related_name='+',
        help_text='Defines the latent period for units of this production type.', )
    disease_subclinical_period_pdf = models.ForeignKey(ProbabilityEquation, related_name='+',
        help_text='Defines the subclinical period for units of this production type.', )
    disease_clinical_period_pdf = models.ForeignKey(ProbabilityEquation, related_name='+',
        help_text='Defines the clinical period for units of this production type.', )
    disease_immune_period_pdf = models.ForeignKey(ProbabilityEquation, related_name='+',
        help_text='Defines the natural immune period for units of this production type.', )
    disease_prevalence_relid = models.ForeignKey(RelationalEquation, related_name='+',
        help_text='Defines the prevelance for units of this production type.', )


class InDiseaseSpread(models.Model):
    production_type_pair = models.ForeignKey('InProductionTypePair',
        help_text='Pair of production types that the spread record is representing.', )
    spread_method_code = models.CharField(max_length=255, blank=True,
        help_text='Code indicating the mechanism of the disease spread.', )
    latent_can_infect = models.BooleanField(default=False,
        help_text='Indicates if latent units of the source type can spread disease by direct contact. Not applicable to airborne spread or indirect spread.', )
    subclinical_can_infect = models.BooleanField(default=False,
        help_text='Indicates if subclinical units of the source type can spread disease by direct or indirect contact. ', )
    mean_contact_rate = models.FloatField(blank=True, null=True,
        help_text='The mean contact rate (in recipient units per source unit per day) for direct or indirect contact models.', )
    use_fixed_contact_rate = models.BooleanField(default=False,
        help_text='Indicates if a fixed contact rate will be used instead of the mean contact rate.', )
    fixed_contact_rate = models.FloatField(blank=True, null=True,
        help_text='The fixed contact rate (in recipient units per source unit per day) for direct or indirect contact models.', )
    infection_probability = models.FloatField(blank=True, null=True,
        help_text='The probability that a contact will result in disease transmission. Specified for direct and indirect contact models.', )
    distance_pdf = models.ForeignKey(ProbabilityEquation, related_name='+',
        help_text='Defines the sipment distances for direct and indirect contact models.', )
        # This is in Disease because of simulation restrictions
    movement_control_relid = models.ForeignKey(RelationalEquation, related_name='+',
        help_text='Relational function used to define movement control effects for the indicated production types combinations.', )
    transport_delay_pdf = models.ForeignKey(ProbabilityEquation, related_name='+',
        help_text='Relational function used to define the shipment delays for the indicated production types combinations.', )
    probability_airborne_spread_1km = models.FloatField(blank=True, null=True,
        help_text='For airborne spread the probability that disease will be spread to unit 1 kn away from the source unit.', )
    max_distance_airborne_spread = models.FloatField(blank=True, null=True,
        help_text='The maximum distance in KM of airborne spread.', )
    wind_direction_start = models.IntegerField(blank=True, null=True,
        help_text='The start angle in degrees of the predominate wind direction for airborne spread.', )
    wind_direction_end = models.IntegerField(blank=True, null=True,
        help_text='The end angle in degrees of the predominate wind direction for airborne spread.', )


class InGeneral(models.Model):
    language = models.CharField(choices=(('en',"English"), ('es',"Spanish")), max_length=255, blank=True,
        help_text='Language that the model is in - English is default.', )
    scenario_description = models.TextField(blank=True,
        help_text='The description of the scenario.', )
    iterations = models.IntegerField(blank=True, null=True,
        help_text='The number of iterations of this scenario that should be run', )
    days = models.IntegerField(blank=True, null=True,
        help_text='The number of day that iterations of this scenario should run if the command Run> State and run until specified day… is used', )
    sim_stop_reason = models.CharField(max_length=255, blank=True,
        help_text='The citerion used to end each iteration. This may be that the specified number of days has passed the first detectino has occurred or the outbreak has ended.',
        choices=(('disease-end','Simulation will stop when there are no more latent or infectious units.'),
                 ('first-detection','Simulation will stop when the first detection occurs.')))
    include_contact_spread = models.BooleanField(default=False,
        help_text='Indicates if disease spread by direct ot indirect contact is used in the scenario.', )
    include_airborne_spread = models.BooleanField(default=False,
        help_text='Indicates ifairborne spread is used in the model', )
    use_airborne_exponential_decay = models.BooleanField(default=False,
        help_text='Indicates if the decrease in probability by airborne transmission is simulated by the exponential (TRUE) or linear (FALSE) algorithm.', )
    use_within_unit_prevalence = models.BooleanField(default=False,
        help_text='Indicates if within unit prevelance should be used in the model.', )
    cost_track_destruction = models.BooleanField(default=False,
        help_text='Indicates if desctruction costs should be tracked in the model.', )
    cost_track_vaccination = models.BooleanField(default=False,
        help_text='Indicates if vaccination costs should be tracked in the model.', )
    cost_track_zone_surveillance = models.BooleanField(default=False,
        help_text='Indicates if zone surveillance costs should be tracked in the model.', )
    use_fixed_random_seed = models.BooleanField(default=False,
        help_text='Indicates if a specific seed value for the random number generator should be used.', )
    random_seed = models.IntegerField(blank=True, null=True,
        help_text='The specified seed value for the random number generator.', )
    ## Outputs requested:
    save_all_daily_outputs = models.BooleanField(default=False,
        help_text='Indicates if daily outputs should be stored for every iteration.', )
    maximum_iterations_for_daily_output = models.IntegerField(default=3,
        help_text='The number of iterations for which daily outputs should be stored The minimum value is 3.', )
    write_daily_states_file = models.BooleanField(default=False,
        help_text='Indicates if a plain text file with the state of each unit on each day of each iteration should be written.', )
    daily_states_filename = models.CharField(max_length=255, blank=True,
        help_text='The file name of the plain text file described above.', )
    save_daily_events = models.BooleanField(default=False,
        help_text='Indicates if all events should be recorded in the scenario database.', )
    save_daily_exposures = models.BooleanField(default=False,
        help_text='Indicates if all exposures should be recorded in the scenario database.', )
    save_iteration_outputs_for_units = models.BooleanField(default=False,
        help_text='Indicates if iteration outputs for units should be recorded in the scenario database.', )
    write_map_output = models.BooleanField(default=False,
        help_text='Indicates if map outputs for units should be recorded in the scenario database.', )
    map_directory = models.CharField(max_length=255, blank=True,
        help_text='File path of the desired location for the output file.', )


class InProductionType(models.Model):
    production_type_name = models.CharField(max_length=255, )
    production_type_description = models.TextField(blank=True)


class InProductionTypePair(models.Model):
    source_production_type = models.ForeignKey(InProductionType, related_name='used_as_sources',
        help_text='The Production type that will be the source type for this production type combination.', )
    destination_production_type = models.ForeignKey(InProductionType, related_name='used_as_destinations',
        help_text='The Production type that will be the recipient type for this production type combination.', )
    direct_contact_spread_model = models.ForeignKey(InDiseaseSpread,   related_name='direct_spread_pair', blank=True, null=True,  # These can be blank, so no check box necessary
        help_text='Disease spread mechanism used to model spread by direct contact between these types.', )
    indirect_contact_spread_model = models.ForeignKey(InDiseaseSpread, related_name='indirect_spread_pair', blank=True, null=True,  # These can be blank, so no check box necessary
        help_text='Disease spread mechanism used to model spread by indirect contact between these types.', )
    airborne_contact_spread_model = models.ForeignKey(InDiseaseSpread, related_name='airborne_spread_pair', blank=True, null=True,  # These can be blank, so no check box necessary
        help_text='Disease spread mechanism used to model spread by airbornespread between these types.', )


class InZone(models.Model):
    zone_description = models.TextField(
        help_text='Description of the zone', )
    zone_radius = models.FloatField(
        help_text='Radius in kilometers of the zone', )


class InZoneProductionType(models.Model):
    zone = models.ForeignKey(InZone,
        help_text='Zone for which this event occurred.', )
    production_type = models.ForeignKey('InProductionType',
        help_text='The production type that these outputs apply to.', )
    zone_indirect_movement_relid = models.ForeignKey(RelationalEquation, related_name='+', blank=True, null=True,
        help_text='Function the describes indirect movement rate.', )
    zone_direct_movement_relid = models.ForeignKey(RelationalEquation, related_name='+', blank=True, null=True,
        help_text='Function the describes direct movement rate.', )
    zone_detection_multiplier = models.FloatField(default=1.0,
        help_text='Multiplier for the probability of observice clinical signs in units of this production type in this zone.', )
    cost_surv_per_animal_day = MoneyField(default=0.0,
        help_text='Cost of surveillance per animal per day in this zone.', )


class ReadAllCodes(models.Model):
    _code = models.CharField(max_length=255,
        help_text='Actual code used in the simulation', )
    _code_type = models.CharField(max_length=255,
        help_text='Type of code', )
    _code_description = models.TextField(
        help_text='Description of the code type.', )


class ReadAllCodeTypes(models.Model):
    _code_type = models.CharField(max_length=255,
        help_text='Type of code', )
    _code_type_description = models.TextField()

