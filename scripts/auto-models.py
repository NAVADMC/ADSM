
from django.db import models
from django_extras.db.models import PercentField, LatitudeField, LongitudeField, MoneyField


def chc(*choice_list):
    return tuple((x, x) for x in choice_list)


class DbSchemaVersion(models.Model):
    version_number = models.CharField(max_length=255, unique=True)
    version_application = models.CharField(max_length=255,  
        help_text='This gets passed around as an identifier - not sure of definition')
    version_date = models.CharField(max_length=255, )
    version_info_url = models.TextField(blank=True)
    version_id = models.IntegerField(blank=True, null=True, 
        help_text='Number of the NAADSM Version used to run the simulation.')


class DynamicBlob(models.Model):
    zone_perimeters = models.CharField(max_length=255, blank=True)  # polygons?


class DynamicUnit(models.Model):
    production_type = models.ForeignKey('InProductionType', 
        help_text='The identifier of the production type that these outputs apply to.')
    latitude = LatitudeField( 
        help_text='The latitude used to georeference this herd.')
    longitude = LongitudeField( 
        help_text='The longitude used to georeference this herd.')
    initial_state_code = models.CharField(max_length=255, 
        help_text='Code indicating the actual disease state of the herd at the beginning of the simulation.',
                                          choices=(('L', 'Latent'),
                                                   ('S', 'Susceptible'),
                                                   ('B', 'Subclinical'),
                                                   ('C', 'Clinical'),
                                                   ('N', 'Naturally Immune'),
                                                   ('V', 'Vaccine Immune'),
                                                   ('D', 'Destroyed')))
    days_in_initial_state = models.IntegerField(blank=True, null=True, 
        help_text='The number of days that the herd will remain in its initial state unless preempted by other events.')
    days_left_in_initial_state = models.IntegerField(blank=True, null=True)
    initial_size = models.IntegerField( 
        help_text='The number of animals in the herd.')
    _final_state_code = models.CharField(max_length=255, blank=True, 
        help_text='Code indicating the actual disease state of the herd at the end of the simulation.')
    _final_control_state_code = models.CharField(max_length=255, blank=True)
    _final_detection_state_code = models.CharField(max_length=255, blank=True)
    _cum_infected = models.IntegerField(blank=True, null=True, 
        help_text='The total number of iterations in which this herd became infected.')
    _cum_detected = models.IntegerField(blank=True, null=True, 
        help_text='The total number of iterations in which this herd was detected.')
    _cum_destroyed = models.IntegerField(blank=True, null=True, 
        help_text='The total number of iterations in which this herd was destroyed.')
    _cum_vaccinated = models.IntegerField(blank=True, null=True, 
        help_text='The total number of iterations in which this herd was vaccinated.')
    user_defined_1 = models.TextField(blank=True)
    user_defined_2 = models.TextField(blank=True)
    user_defined_3 = models.TextField(blank=True)
    user_defined_4 = models.TextField(blank=True)

'''InChart is an equation model that defines either a Probability Distribution Function (pdf) or
 a relational function (relid) depending on which child class is used.  '''
class InChart(models.Model):
    chart_name = models.CharField(max_length=255,  
        help_text='User-assigned name for each function.')
    # field_name = models.CharField(max_length=255, )  # I don't think this is necessary
    x_axis_units = models.CharField(max_length=255, default="Days", 
        help_text='Specifies the descriptive units for the x axis in relational functions.')
    y_axis_units = models.CharField(max_length=255, blank=True, 
        help_text='Specifies the descriptive units for the x axis in probability density  and relational functions.')
    _notes = models.TextField(blank=True, null=True)  # Why is this hidden?
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
        help_text='The mean for probability density function types Gaussian Lognormal Possoin and Exponential.')
    std_dev = models.FloatField(blank=True, null=True, 
        help_text='The mean for probability density function types Gaussian and Lognormal.')
    min = models.FloatField(blank=True, null=True, 
        help_text='The minimumfor probability density function types Uniform Triangular Beta and betaPERT.')
    mode = models.FloatField(blank=True, null=True, 
        help_text='The Mode for probability density function types Point Triangular and BetaPERT.')
    max = models.FloatField(blank=True, null=True, 
        help_text='The maximum value for probability density function types Uniform Triangular Beta and BetaPERT.')
    alpha = models.FloatField(blank=True, null=True, 
        help_text='The alpha parameter for probability density function types Gamma Weibull and Pearson 5 or the alpha1 parameter for Beta probability density functions.')
    alpha2 = models.FloatField(blank=True, null=True, 
        help_text='The alpha2 parameter for Beta probability density function types.')
    beta = models.FloatField(blank=True, null=True, 
        help_text='The beta parameter for probability density function types Gamma Weibull and Pearson 5.')
    location = models.FloatField(blank=True, null=True, 
        help_text='The location parameter for probability density function types Logistic and Loglogistic.')
    scale = models.FloatField(blank=True, null=True, 
        help_text='The scale parameter for probability density function types Logistic and Loglogistic.')
    shape = models.FloatField(blank=True, null=True, 
        help_text='The shape parameter for probability density function types Loglogistic Inverse Gaussian.')  # or should this be the chart_type list of PDF functions?
    n = models.IntegerField(blank=True, null=True, 
        help_text='The n parameter for probability density function types  Binomial Hypergeometric.')
    p = models.FloatField(blank=True, null=True, 
        help_text='The p parameter for probability density function types Negative Binomial Bernoulli.')
    m = models.IntegerField(blank=True, null=True, 
        help_text='The m parameter for probability density function types Hypergeometric.')
    d = models.IntegerField(blank=True, null=True, 
        help_text='The d parameter for probability density function types Hypergeometric.')
    theta = models.FloatField(blank=True, null=True, 
        help_text='The Theta parameter for probability density function types Pareto.')
    a = models.FloatField(blank=True, null=True, 
        help_text='The a parameter for probability density function types Pareto.')
    s = models.IntegerField(blank=True, null=True, 
        help_text='The s parameter for probability density function types Negative Binomial.')


class RelationalEquation(InChart):
    pass  # Inherited fields


class EquationPoint(models.Model):
    chart = models.ForeignKey(RelationalEquation)
    _point_order = models.IntegerField()
    _x = models.FloatField( 
        help_text='The x value of the point.')
    _y = models.FloatField( 
        help_text='The y value of the point.')


class InControlGlobal(models.Model):
    _include_detection = models.BooleanField(default=False,  
        help_text='Indicates if detection of disease in any production type will be modeled.')
    _include_tracing = models.BooleanField(default=False,  
        help_text='Indicates if tracing of units in any production type will be modeled.')
    _include_tracing_unit_exam = models.BooleanField(default=False, )
    _include_tracing_testing = models.BooleanField(default=False,  
        help_text='Indicates if tracing  using herd examination  in any production type will be modeled.')
    _include_destruction = models.BooleanField(default=False,  
        help_text='Indicates if destruction of units in any production type will be modeled.')  # TODO: restrict ForeignKey presence based on boolean include
    _include_vaccination = models.BooleanField(default=False,  
        help_text='A string that identifies the secondary priority order for destruction.')
    _include_zones = models.BooleanField(default=False,  
        help_text='Indicates if zones will be modeled.')
    destruction_delay = models.IntegerField(blank=True, null=True, 
        help_text='The number of days that must pass after the first detection before a destruction program can begin.')
    destruction_capacity_relid = models.ForeignKey(RelationalEquation, related_name='+', blank=True, null=True)
    destruction_priority_order = models.CharField(max_length=255, blank=True, 
        help_text='A string that identifies the primary priority order for destruction.')  # These are an odd legacy.  Leave it for now
    destrucion_reason_order = models.CharField(max_length=255, blank=True, 
        help_text='A string that identifies the primary priority order for destruction.')
    trigger_vaccincation_after_detected_units_count = models.IntegerField(blank=True, null=True)
    vaccination_capacity_relid = models.ForeignKey(RelationalEquation, related_name='+', blank=True, null=True)
    vaccination_priority_order = models.CharField(max_length=255, blank=True, 
        help_text='A string that identifies the primary priority order for vaccination.')


class InControlPlan(models.Model):
    control_plan_name = models.CharField(max_length=255, )
    control_plan_description = models.TextField(blank=True)
    control_plan_group = models.CharField(max_length=255, blank=True)


class InControlsProductionType(models.Model):
    production_type = models.ForeignKey('InProductionType', 
        help_text='The identifier of the production type that these outputs apply to.')
    use_detection = models.BooleanField(default=False,  
        help_text='Indicates if disease detection will be modeled for units of this production type.')
    detection_probability_for_observed_time_in_clinical_relid = models.ForeignKey(RelationalEquation, related_name='+', blank=True, null=True)
    detection_probability_report_vs_first_detection_relid = models.ForeignKey(RelationalEquation, related_name='+', blank=True, null=True)
    trace_direct_forward = models.BooleanField(default=False,  
        help_text='Indicator that trace forward will be conducted for direct contacts where the reported unit was the source of contact and was of this production type.')
    trace_direct_back = models.BooleanField(default=False,  
        help_text='Indicator that trace back will be conducted for direct contacts where the reported unit was the source of contact and was of this production type.')
    trace_direct_success = PercentField(blank=True, null=True, 
        help_text='Probability of success of trace for direct contact.')
    trace_direct_trace_period = models.BooleanField(default=False,  
        help_text='Days before detection  (critical period) for tracing of direct contacts.')
    trace_indirect_forward = models.BooleanField(default=False,  
        help_text='Indicator that trace forward will be conducted for indirect contacts where the reported unit was the source of contact and was of this production type.')
    trace_indirect_back = models.BooleanField(default=False,  
        help_text='Indicator that trace back will be conducted for indirect contacts where the reported unit was the source of contact and was of this production type.')
    trace_indirect_success = PercentField(blank=True, null=True, 
        help_text='Probability of success of trace for indirect contact.')
    trace_indirect_trace_period = models.BooleanField(default=False,  
        help_text='Days before detection  (critical period) for tracing of indirect contacts.')
    trace_delay_pdf = models.ForeignKey(ProbabilityEquation, related_name='+', 
        help_text='Identifier of the shipping delay function.')
    use_destruction = models.BooleanField(default=False,  
        help_text='Indicates  if detected clinical units of this production type will be destroyed.')
    destruction_is_ring_trigger = models.BooleanField(default=False,  
        help_text='Indicates if detection of a unit of this production type will trigger the formation of a destruction ring.')
    destruction_ring_radius = models.FloatField(blank=True, null=True, 
        help_text='Radius in kilometers of the destruction ring.')
    destruction_is_ring_target = models.BooleanField(default=False,  
        help_text='Indicates if unit of this production type will be subject to preemptive ring destruction.')
    destroy_direct_forward_traces = models.BooleanField(default=False,  
        help_text='Indicates is units of this type identified by trace forward of indirect contacts will be subject to preemptive desctruction.')
    destroy_indirect_forward_traces = models.BooleanField(default=False,  
        help_text='Indicates is units of this type identified by trace forward of direct contacts will be subject to preemptive desctruction.')
    destroy_direct_back_traces = models.BooleanField(default=False,  
        help_text='Indicates is units of this type identified by tracebackof direct contacts will be subject to preemptive desctruction.')
    destroy_indirect_back_traces = models.BooleanField(default=False,  
        help_text='Indicates is units of this type identified by traceback of indirect contacts will be subject to preemptive desctruction.')
    destruction_priority = models.IntegerField(blank=True, null=True, 
        help_text='The desctruction prioroty of this production type relative to other production types.  A  lower number indicates a higher priority.')
    use_vaccination = models.BooleanField(default=False,  
        help_text='Indicates if units of this production type will be subject to vaccination.')
    vaccination_min_time_between = models.IntegerField(blank=True, null=True, 
        help_text='The minimum time in days between vaccination for units of this production type.')
    vaccinate_detected = models.BooleanField(default=False,  
        help_text='Indicates if units of this production type will be subject to vaccination if infected and detected.')
    days_to_immunity = models.IntegerField(blank=True, null=True, 
        help_text='The number of days required for the onset of vaccine immunity in a newly vaccinated unit of this type.')
    vaccine_immune_period_pdf = models.ForeignKey(ProbabilityEquation, related_name='+')
    vaccinate_ring = models.BooleanField(default=False,  
        help_text='Indicates if detection of a clinical unit of this type will trigger a vaccination ring.')
    vaccination_ring_radius = models.FloatField(blank=True, null=True)
    vaccination_priority = models.IntegerField(blank=True, null=True, 
        help_text='The vacination priority of this production type relative to other production types.  A  lower number indicates a higher priority.')
    cost_destroy_appraisal_per_unit = MoneyField(default=0.0, 
        help_text='The cost associated with appraisal for each destroyed unit of this type.')
    cost_destroy_cleaning_per_unit = MoneyField(default=0.0, 
        help_text='The cost associated with cleaning and disinfection for each destroyed unit of this type.')
    cost_destroy_euthanasia_per_animal = MoneyField(default=0.0, 
        help_text='The cost associated with euthanizing each destroyed animal of this type.')
    cost_destroy_indemnification_per_animal = MoneyField(default=0.0, 
        help_text='The cost of indemnification for each destroyed animal of this type.')
    cost_destroy_disposal_per_animal = MoneyField(default=0.0, 
        help_text='The cost of carcass disposal for each destroyed animal of this type.')
    cost_vaccinate_setup_per_unit = MoneyField(default=0.0, 
        help_text='The cost of site setup for each vaccinated unit of this type.')
    cost_vaccinate_threshold = models.IntegerField(blank=True, null=True, 
        help_text='The number of animals of this type that can be vaccinated before the cost of vaccination increases.')
    cost_vaccinate_baseline_per_animal = MoneyField(default=0.0, 
        help_text='The baseline cost of vaccination for each vaccinated animal of this type. This cost applies to all vaccinations before the threshold is set in costVaccThershold is met. ')
    cost_vaccinate_additional_per_animal = MoneyField(default=0.0)
    zone_detection_is_trigger = models.BooleanField(default=False,  
        help_text='Indicator if detection of infected units of this production type will trigger a zone focus.')
    zone_direct_trace_is_trigger = models.BooleanField(default=False,  
        help_text='Indicator if direct tracing of infected units of this production type will trigger a zone focus.')
    zone_indirect_trace_is_trigger = models.BooleanField(default=False,  
        help_text='Indicator if indirect tracing of infected units of this production type will trigger a zone focus.')
    exam_direct_forward = models.BooleanField(default=False,  
        help_text='Indicator if units identified by the trace-forward of direct contact will be examined for clinical signs of disease.')
    exam_direct_forward_multiplier = models.FloatField(blank=True, null=True, 
        help_text='Multiplier for the probability of observice clinical signs in  units identified by the trace-forward of direct contact.')
    exam_indirect_forward = models.BooleanField(default=False,  
        help_text='Indicator if units identified by the trace-forward of indirect contact will be examined for clinical signs of disease.')
    exam_indirect_forward_multiplier = models.FloatField(blank=True, null=True, 
        help_text='Multiplier for the probability of observice clinical signs in  units identified by the trace-forward of indirect contact .')
    exam_direct_back = models.BooleanField(default=False,  
        help_text='Indicator if units identified by the trace-back of direct contact will be examined for clinical signs of disease.')
    exam_direct_back_multiplier = models.FloatField(blank=True, null=True, 
        help_text='Multiplier for the probability of observice clinical signs in  units identified by the trace-back of direct contact.')
    exam_indirect_back = models.BooleanField(default=False,  
        help_text='Indicator if units identified by the trace-back of indirect contact will be examined for clinical signs of disease.')
    exam_indirect_back_multiplier = models.FloatField(blank=True, null=True, 
        help_text='Multiplier for the probability of observice clinical signs in  units identified by the trace-back of indirect contact.')
    test_direct_forward = models.BooleanField(default=False,  
        help_text='Indicator that diagnostic testing shuold be performed on units identified by trace-forward of direct contacts.')
    test_indirect_forward = models.BooleanField(default=False,  
        help_text='Indicator that diagnostic testing shuold be performed on units identified by trace-forward of indirect contacts.')
    test_direct_back = models.BooleanField(default=False,  
        help_text='Indicator that diagnostic testing should be performed on units identified by trace-back of direct contacts.')
    test_indirect_back = models.BooleanField(default=False,  
        help_text='Indicator that diagnostic testing should be performed on units identified by trace-back of indirect contacts.')
    test_specificity = models.FloatField(blank=True, null=True, 
        help_text='Test Specificity for units of this production type')
    test_sensitivity = models.FloatField(blank=True, null=True, 
        help_text='Test Sensitivity for units of this production type')
    test_delay_pdf = models.ForeignKey(ProbabilityEquation, related_name='+', 
        help_text='Identifier of the function that describes the delay in obtaining test results.')
    vaccinate_restrospective_days = models.BooleanField(default=False, )


class InDiseaseGlobal(models.Model):
    disease_name = models.TextField(blank=True)
    disease_description = models.TextField(blank=True)


class InDiseaseProductionType(models.Model):
    production_type = models.ForeignKey('InProductionType', 
        help_text='The identifier of the production type that these outputs apply to.')
    use_disease_transition = models.BooleanField(default=False,  
        help_text='Indicates if units of this production type will undergo disease transition.')
    disease_latent_period_pdf = models.ForeignKey(ProbabilityEquation, related_name='+')
    disease_subclinical_period_pdf = models.ForeignKey(ProbabilityEquation, related_name='+')
    disease_clinical_period_pdf = models.ForeignKey(ProbabilityEquation, related_name='+')
    disease_immune_period_pdf = models.ForeignKey(ProbabilityEquation, related_name='+')
    disease_prevalence_relid = models.ForeignKey(RelationalEquation, related_name='+')


class InDiseaseSpread(models.Model):
    production_type_pair = models.ForeignKey('InProductionTypePair', 
        help_text='Identifier of the pair of production types that the spread record is representing.')
    spread_method_code = models.CharField(max_length=255, blank=True, 
        help_text='Code indicating the mechanism of the disease spread.')
    latent_can_infect = models.BooleanField(default=False,  
        help_text='Indicates if latent units of the source type can spread disease by direct contact. Not applicable to airborne spread or indirect spread.')
    subclinical_can_infect = models.BooleanField(default=False,  
        help_text='Indicates if subclinical units of the source type can spread disease by direct or indirect contact. ')
    mean_contact_rate = models.FloatField(blank=True, null=True, 
        help_text='The mean contact rate (in recipient herds per source herd per day) for direct or indirect contact models.')
    use_fixed_contact_rate = models.BooleanField(default=False,  
        help_text='Indicates if a fixed contact rate will be used instead of the mean contact rate.')
    fixed_contact_rate = models.FloatField(blank=True, null=True, 
        help_text='The fixed contact rate (in recipient herds per source herd per day) for direct or indirect contact models.')
    infection_probability = models.FloatField(blank=True, null=True, 
        help_text='The probability that a contact will result in disease transmission. Specified for direct and indirect contact models.')
    distance_pdf = models.ForeignKey(ProbabilityEquation, related_name='+', 
        help_text='Identifier of the probability density function used to define the sipment distances for direct and indirect contact models.')
        # This is in Disease because of simulation restrictions
    movement_control_relid = models.ForeignKey(RelationalEquation, related_name='+', 
        help_text='Identifier of the relational function used to define movement control effects for the indicated production types combinations.')
    transport_delay_pdf = models.ForeignKey(ProbabilityEquation, related_name='+', 
        help_text='Identifier of the relational function used to define the shipment delays for the indicated production types combinations.')
    probability_airborne_spread_1km = models.FloatField(blank=True, null=True, 
        help_text='For airborne spread the probability that disease will be spread to unit 1 kn away from the source unit.')
    max_distance_airborne_spread = models.FloatField(blank=True, null=True, 
        help_text='The maximum distance in KM of airborne spread.')
    wind_direction_start = models.IntegerField(blank=True, null=True, 
        help_text='The start angle in degrees of the predominate wind direction for airborne spread.')
    wind_direction_end = models.IntegerField(blank=True, null=True, 
        help_text='The end angle in degrees of the predominate wind direction for airborne spread.')


class InGeneral(models.Model):
    language = models.CharField(choices=(('en',"English"), ('es',"Spanish")), max_length=255, blank=True, 
        help_text='Language that the model is in - English is default.')
    scenario_description = models.TextField(blank=True,
                                            help_text='A short description of the scenario being simulated.')
    iterations = models.IntegerField(blank=True, null=True, 
        help_text='The number of iterations of this scenario that should be run')
    days = models.IntegerField(blank=True, null=True,
                               help_text='The maximum number of days in a simulation run. A simulation run may end earlier, if there are no latent or infectious animals and no module has pending actions to complete.')
    sim_stop_reason = models.CharField(max_length=255, blank=True, 
        help_text='The citerion used to end each iteration. This may be that the specified number of days has passed the first detectino has occurred or the outbreak has ended.',
        choices=(('disease-end','Simulation will stop when there are no more latent or infectious units.'),
                 ('first-detection','Simulation will stop when the first detection occurs.')))
    include_contact_spread = models.BooleanField(default=False,  
        help_text='Indicates if disease spread by direct ot indirect contact is used in the scenario.')
    include_airborne_spread = models.BooleanField(default=False,  
        help_text='Indicates ifairborne spread is used in the model')
    use_airborne_exponential_decay = models.BooleanField(default=False,  
        help_text='Indicates if the decrease in probability by aireborne transmission is simulated by the exponential (TRUE) or linear (FALSE) algorithm.')
    use_within_unit_prevalence = models.BooleanField(default=False, )
    cost_track_destruction = models.BooleanField(default=False,  
        help_text='Indicates if desctruction costs should be tracked in the model.')
    cost_track_vaccination = models.BooleanField(default=False,  
        help_text='Indicates if vaccination costs should be tracked in the model.')
    cost_track_zone_surveillance = models.BooleanField(default=False,  
        help_text='Indicates if zone surveillance costs should be tracked in the model.')
    use_fixed_random_seed = models.BooleanField(default=False,  
        help_text='Indicates if a specific seed value for the random number generator should be used.')
    random_seed = models.IntegerField(blank=True, null=True, 
        help_text='The specified seed value for the random number generator.')
    ## Outputs requested:
    save_all_daily_outputs = models.BooleanField(default=False,  
        help_text='Indicates if daily outputs should be stored for every iteration.')
    maximum_iterations_for_daily_output = models.IntegerField(default=3, )
    write_daily_states_file = models.BooleanField(default=False, 
        help_text='Indicates if a plain text file with the state of each unit on each day of each iteration should be written.')
    daily_states_filename = models.CharField(max_length=255, blank=True, 
        help_text='The file name of the plain text file described above.')
    save_daily_events = models.BooleanField(default=False,  
        help_text='Indicates if all events should be recorded in the scenario database.')
    save_daily_exposures = models.BooleanField(default=False,  
        help_text='Indicates if all exposures should be recorded in the scenario database.')
    save_iteration_outputs_for_units = models.BooleanField(default=False, )
    write_map_output = models.BooleanField(default=False,  
        help_text='Indicates if map outputs for herds should be recorded in the scenario database.')
    map_directory = models.CharField(max_length=255, blank=True, 
        help_text='File path of the desired location for the output file.')


class InProductionType(models.Model):
    production_type_name = models.CharField(max_length=255, )
    production_type_description = models.TextField(blank=True) # This field type is a guess.


class InProductionTypePair(models.Model):
    source_production_type = models.ForeignKey(InProductionType, related_name='used_as_sources', 
        help_text='The identifier of the production type that will be the recipient type for this production type combination.')
    destination_production_type = models.ForeignKey(InProductionType, related_name='used_as_destinations')
    direct_contact_spread_model = models.ForeignKey(InDiseaseSpread,   related_name='direct_spread_pair', blank=True, null=True)  # These can be blank, so no check box necessary
    indirect_contact_spread_model = models.ForeignKey(InDiseaseSpread, related_name='indirect_spread_pair', blank=True, null=True)  # These can be blank, so no check box necessary
    airborne_contact_spread_model = models.ForeignKey(InDiseaseSpread, related_name='airborne_spread_pair', blank=True, null=True)  # These can be blank, so no check box necessary


class InZone(models.Model):
    zone_description = models.TextField( 
        help_text='Description of the zone')
    zone_radius = models.FloatField( 
        help_text='Radius in kilometers of the zone')


class InZoneProductionType(models.Model):
    zone = models.ForeignKey(InZone, 
        help_text='Identifier of the zone for which this event occurred.')
    production_type = models.ForeignKey('InProductionType', 
        help_text='The identifier of the production type that these outputs apply to.')
    zone_indirect_movement_relid = models.ForeignKey(RelationalEquation, related_name='+', blank=True, null=True, 
        help_text='Identifier of the function the describes indirect movement rate.')
    zone_direct_movement_relid = models.ForeignKey(RelationalEquation, related_name='+', blank=True, null=True, 
        help_text='Identifier of the function the describes direct movement rate.')
    zone_detection_multiplier = models.FloatField(default=1.0, 
        help_text='Multiplier for the probability of observice clinical signs in  units of this production type in this zone.')
    cost_surv_per_animal_day = MoneyField(default=0.0, 
        help_text='Cost of surveillance per animal per day in this zone.')


class ReadAllCodes(models.Model):
    _code = models.CharField(max_length=255,  
        help_text='Actual  code used in the simulation')
    _code_type = models.CharField(max_length=255,  
        help_text='Type of code')
    _code_description = models.TextField( 
        help_text='Description of the code type.')


class ReadAllCodeTypes(models.Model):
    _code_type = models.CharField(max_length=255,  
        help_text='Type of code')
    _code_type_description = models.TextField()









class OutDailyByProductionType(models.Model):
    iteration = models.IntegerField(blank=True, null=True, 
        help_text='The iteration during which the outputs in this records where generated.')
    production_type = models.ForeignKey(InProductionType, 
        help_text='The identifier of the production type that these outputs apply to.')
    day = models.IntegerField(blank=True, null=True, 
        help_text='The day within the iteration on which these outputs were generated.')
    transition_state_daily_unit_susceptible = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that are or become susceptible on the given day')
    transition_state_daily_animal_susceptible = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units that are or become susceptible on the given day')
    transition_state_daily_unit_latent = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that are or become latent on the given day')
    transition_state_daily_animal_latent = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units that are or become latent on the given day')
    transition_state_daily_unit_subclinical = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that are or become subclinically infectious on the given day')
    transition_state_daily_animal_subclinical = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units that are or become infectious on the given day')
    transition_state_daily_unit_clinical = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that are or become clinical on the given day')
    transition_state_daily_animal_clinical = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units that are or become clinical on the given day')
    transition_state_daily_unit_nat_immune = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that are or become naturally immune on the given day')
    transition_state_daily_animal_nat_immune = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units that are or become naturally immune on the given day')
    transition_state_daily_unit_vac_immune = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that are or become vaccine immuneon the given day')
    transition_state_daily_animal_vac_immune = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units that are or become vaccine immune on the given day')
    transition_state_daily_unit_destroyed = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that are destroyed on the given day')
    transition_state_daily_animal_destroyed = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units that are destroyed on the given day')
    transition_state_cum_unit_susceptible = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that are or become susceptible over the course of an iteration')
    transition_state_cum_animal_susceptible = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units that are or become susceptible over the course of an iteration')
    transition_state_cum_unit_latent = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that are or become latent over the course of an iteration')
    transition_state_cum_animal_latent = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units that are or become latent over the course of an iteration')
    transition_state_cum_unit_subclinical = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that are or become subclinically infectious over the course of an iteration')
    transition_state_cum_animal_subclinical = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units that are or become infectious over the course of an iteration')
    transition_state_cum_unit_clinical = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that are or become clinical over the course of an iteration')
    transition_state_cum_animal_clinical = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units that are or become clinical over the course of an iteration')
    transition_state_cum_unit_nat_immune = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that are or become naturally immune over the course of an iteration')
    transition_state_cum_animal_nat_immune = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units that are or become naturally immune over the course of an iteration')
    transition_state_cum_unit_vac_immune = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that are or become vaccine immune over the course of an iteration')
    transition_state_cum_animal_vac_immune = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units that are or become vaccine immune over the course of an iteration')
    transition_state_cum_unit_destroyed = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that are destroyed over the course of an iteration')
    transition_state_cum_animal_destroyed = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units that are destroyed over the course of an iteration')
    infection_new_unit_air = models.IntegerField(blank=True, null=True, 
        help_text='(infections new units airborne) Number of units that become infected by airborne spread on a given day')
    infection_new_animal_air = models.IntegerField(blank=True, null=True, 
        help_text='(infections new animals airborne) Number of animals in units that become infected by airborne spread on a given day')
    infection_new_unit_dir = models.IntegerField(blank=True, null=True, 
        help_text='(infections new units direct)Number of units that become infected by direct contact on a given day')
    infection_new_animal_dir = models.IntegerField(blank=True, null=True, 
        help_text='(infections new animals direct)  Number of animals in units that become infected by direct contact on a given day')
    infection_new_unit_ind = models.IntegerField(blank=True, null=True, 
        help_text='(infections new animals indirect) Number of units that become infected by indirect contact on a given day')
    infection_new_animal_ind = models.IntegerField(blank=True, null=True, 
        help_text='(infections new animals indirect) Number of animals in units that become infected by indirect contact on a given day')
    infection_cum_unit_initial = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that are initially infected at the beginning of an iteration')
    infection_cum_animal_initial = models.IntegerField(blank=True, null=True, 
        help_text='Number of animals in units that are initially infected at the beginning of an iteration')
    infection_cum_unit_air = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that become infected by airborne spread over the course of an iteration')
    infection_cum_animal_air = models.IntegerField(blank=True, null=True, 
        help_text='Number of animals in units that become infected by airborne spread over the course of an iteration')
    infection_cum_unit_dir = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that become infected by direct contact over the course of an iteration')
    infection_cum_animal_dir = models.IntegerField(blank=True, null=True, 
        help_text='Number of animals that become infected by direct contact over the course of an iteration')
    infection_cum_unit_ind = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that become infected by indirect contact over the course of an iteration')
    infection_cum_animal_ind = models.IntegerField(blank=True, null=True, 
        help_text='Number of animals in units that become infected by indirect contact over the course of an iteration')
    exposed_cum_unit_dir = models.IntegerField(blank=True, null=True, 
        help_text='Total number of units directly exposed to any infected unit over the course of an iteration')
    exposed_cum_animal_dir = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units directly exposed to any infected unit over the course of an iteration')
    exposed_cum_unit_ind = models.IntegerField(blank=True, null=True, 
        help_text='Total number of units indirectly exposed to any infected unit over the course of an iteration')
    exposed_cum_animal_ind = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units indirectly exposed to any infected unit over the course of an iteration')
    trace_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units directly exposed and successfully traced forward over the course of an iteration')
    trace_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units directly exposed and successfully traced forward over the course of an iteration')
    trace_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Number of units indirectly exposed and successfully traced forward over the course of an iteration')
    trace_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units indirectly exposed and successfully traced forward over the course of an iteration')
    trace_cum_unit_dir_p_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Number of units directly exposed that could possibly have been traced forward over the course of an iteration')
    trace_cum_animal_dir_p_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units directly exposed that could possibly have been traced forward over the course of an iteration')
    trace_cum_unit_ind_p_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Number of units indirectly exposed that could possibly have been traced forward over the course of an iteration')
    trace_cum_animal_ind_p_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units indirectly exposed that could possibly have been traced forward over the course of an iteration')
    trace_origin_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Number of trace-forwards of direct contact that originate at units of the designated type over the course of an iteration')
    trace_origin_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Number of trace-forwards of indirect contact that originate at units of the designated type over the course of an iteration')
    trace_origin_cum_unit_dir_back = models.IntegerField(blank=True, null=True, 
        help_text='Number of trace-backs of direct contact that originate at units of the designated type over the course of an iteration')
    trace_origin_cum_unit_ind_back = models.IntegerField(blank=True, null=True, 
        help_text='Number of trace-backs of indirect contact that originate at units of the designated type over the course of an iteration')
    trace_new_unit_dir_fwd = models.IntegerField(blank=True, null=True, 
        help_text='(trace new Units Direct contact Forward trace) Total number of units directly exposed and successfully traced forward on the given day')
    trace_new_animal_dir_fwd = models.IntegerField(blank=True, null=True, 
        help_text='(trace new Animals Direct contact Forward trace) Total number of animals in all units directly exposed and successfully traced forward on the given day')
    trace_new_unit_ind_fwd = models.IntegerField(blank=True, null=True, 
        help_text='(trace new Units Indirect contact forward trace) Number of units indirectly exposed and successfully traced forward on the given day')
    trace_new_animal_ind_fwd = models.IntegerField(blank=True, null=True, 
        help_text='(trace new Animals Indirect contact forward trace) Total number of animals in all units indirectly exposed and successfully traced forward on the given day')
    trace_cum_unit_dir_back = models.IntegerField(blank=True, null=True, 
        help_text='Number of units successfully traced back from a detected unit after direct contact over the course of the iteration')
    trace_cum_animal_dir_back = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units successfully traced back from a detected unit over the course of the iteration')
    trace_cum_unit_ind_back = models.IntegerField(blank=True, null=True, 
        help_text='Number of units successfully traced back from a detected unit after indirect contact over the course of the iteration')
    trace_cum_animal_ind_back = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units successfully traced back from a detected unit after indirect contact over the course of the iteration')
    trace_cum_unit_dir_p_back = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that could possibly have been traced back from a detected unit after direct contact over the course of the iteration')
    trace_cum_animal_dir_p_back = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units that could possibly have been traced back from a detected unit after direct contact over the course of the iteration')
    trace_cum_unit_ind_p_back = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that could possibly have been traced back from a detected unit after indirect contact over the course of the iteration')
    trace_cum_animal_ind_p_back = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units that could possibly have been traced back from a detected unit after indirect contact over the course of the iteration')
    trace_new_unit_dir_back = models.IntegerField(blank=True, null=True, 
        help_text='(trace new Units direct contact backwards trace) Number of units successfully traced back from a detected unit after direct contact on the given day')
    trace_new_animal_dir_back = models.IntegerField(blank=True, null=True, 
        help_text='(trace new Units direct contact backwards trace) Total number of animals in units successfully traced back from a detected unit on the given day')
    trace_new_u_ind_back = models.IntegerField(blank=True, null=True, 
        help_text='(trace new Units Indirect contact backwards trace)  Number of units successfully traced back from a detected unit after indirect contact on the given day')
    trace_new_animal_ind_back = models.IntegerField(blank=True, null=True, 
        help_text='(trace new Units Indirect contact Backwards trace) Total number of animals in units successfully traced back from a detected unit after indirect contact on the given day')
    trace_origin_new_unit_dir_fwd = models.IntegerField(blank=True, null=True, 
        help_text='(Trace origin new units direct contact forward)  Number of trace-forwards of direct contact that originate at units of the designated type on the given day')
    trace_origin_new_unit_ind_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Number of trace-backs of direct contact that originate at units of the designated type on the given day')
    trace_origin_new_unit_dir_back = models.IntegerField(blank=True, null=True, 
        help_text='Number of trace-forwards of indirect contact that originate at units of the designated type on the given day')
    trace_origin_new_unit_ind_back = models.IntegerField(blank=True, null=True, 
        help_text='Number of trace-backs of indirect contact that originate at units of the designated type on the given day')
    exam_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Number of units subjected to a herd exam after a trace-forward of direct contact over the course of the iteration')
    exam_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units subjected to a herd exam after a trace-forward of direct contact over the course of the iteration')
    exam_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Number of units subjected to a herd exam after a trace-forward of indirect contact over the course of the iteration')
    exam_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units subjected to a herd exam after a trace-forward of indirect contact over the course of the iteration')
    exam_cum_unit_dir_back = models.IntegerField(blank=True, null=True, 
        help_text='Number of units subjected to a herd exam after a trace-back of direct contact over the course of the iteration')
    exam_cum_animal_dir_back = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units subjected to a herd exam after a trace-back of direct contact over the course of the iteration')
    exam_cum_unit_ind_back = models.IntegerField(blank=True, null=True, 
        help_text='Number of units subjected to a herd exam after a trace-back of indirect contact over the course of the iteration')
    exam_cum_animal_ind_back = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units subjected to a herd exam after a trace-back of indirect contact over the course of the iteration')
    exam_new_unit_all = models.IntegerField(blank=True, null=True, 
        help_text='(exam new Units All)  Number of units examined for any reason on the given day.')
    exam_new_animal_all = models.IntegerField(blank=True, null=True, 
        help_text='(exam new Animals All)  Number of animals in units examined for any reason on the given day')
    test_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Number of units subjected to diagnostic testing after a trace-forward of direct contact over the course of the iteration')
    test_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units subjected to diagnostic testing after a trace-forward of direct contact over the course of the iteration')
    test_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Number of units subjected to diagnostic testing after a trace-forward of indirect contact over the course of the iteration')
    test_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units subjected to diagnostic testing after a trace-forward of indirect contact over the course of the iteration')
    test_cum_unit_dir_back = models.IntegerField(blank=True, null=True, 
        help_text='Number of units subjected to diagnostic testing after a trace-back of direct contact over the course of the iteration')
    test_cum_animal_dir_back = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units subjected to diagnostic testing after a trace-back of direct contact over the course of the iteration')
    test_cum_unit_ind_back = models.IntegerField(blank=True, null=True, 
        help_text='Number of units subjected to diagnostic testing after a trace-back of indirect contact over the course of the iteration')
    test_cum_animal_ind_back = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units subjected to diagnostic testing after a trace-back of indirect contact over the course of the iteration')
    test_cum_unit_true_pos = models.IntegerField(blank=True, null=True, 
        help_text='Number of tested units with a true positive diagnostic test result over the course of the iteration')
    test_cum_animal_true_pos = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in tested units with a true positive diagnostic test result over the course of the iteration')
    test_new_unit_true_pos = models.IntegerField(blank=True, null=True, 
        help_text='(test new Units True Positive)  Number of tested units with a true positive diagnostic test on the given day.')
    test_new_animal_true_pos = models.IntegerField(blank=True, null=True, 
        help_text='(test new Animals True Positive)  Number of animals in tested units with a true positive diagnostic test on the given day.')
    test_cum_unit_true_neg = models.IntegerField(blank=True, null=True, 
        help_text='Number of tested units with a true negative diagnostic test result over the course of the iteration')
    test_cum_animal_true_neg = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in tested units with a true negative diagnostic test result over the course of the iteration')
    test_new_unit_true_neg = models.IntegerField(blank=True, null=True, 
        help_text='(test cumulative Units True Negative) Number of tested units with a true negative diagnostic test result over the course of the iteration.')
    test_new_animal_true_neg = models.IntegerField(blank=True, null=True, 
        help_text='(test cumulative Animals True Negative) Total number of animals in tested units with a true negative diagnostic test result over the course of the iteration.')
    test_cum_unit_false_pos = models.IntegerField(blank=True, null=True, 
        help_text='Number of tested units with a false positive diagnostic test result over the course of the iteration')
    test_cum_animal_false_pos = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in tested units with a false positive diagnostic test result over the course of the iteration')
    test_new_unit_false_pos = models.IntegerField(blank=True, null=True, 
        help_text='(test new Units False Positive) Number of tested units with a false positive diagnostic test on the given day.')
    test_new_animal_false_pos = models.IntegerField(blank=True, null=True, 
        help_text='(test new Animals False Positive) Number of animals in tested units with a false positive diagnostic test on the given day.')
    test_cum_unit_false_neg = models.IntegerField(blank=True, null=True, 
        help_text='Number of tested units with a false negative diagnostic test result over the course of the iteration')
    test_cum_animal_false_neg = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in tested units with a false negative diagnostic test result over the course of the iteration')
    test_new_unit_false_neg = models.IntegerField(blank=True, null=True, 
        help_text='(test new Units False Negative) Number of tested units with a false negative diagnostic test on the given day.')
    test_new_animal_false_neg = models.IntegerField(blank=True, null=True, 
        help_text='(test new Animals False Negative) Number of animals in tested units with a false negative diagnostic test on the given day.')
    detect_new_unit_clin = models.IntegerField(blank=True, null=True, 
        help_text='Number of units detected by clinical signs on the given day')
    detect_new_animal_clin = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units detected by clinical signs on the given day')
    detect_cum_unit_clin = models.IntegerField(blank=True, null=True, 
        help_text='Number of units detected by clinical signs over the course of an iteration')
    detect_cum_animal_clin = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units detected by clinical signs over the course of an iteration')
    detect_new_unit_test = models.IntegerField(blank=True, null=True, 
        help_text='(detection new Units Tested)  Number of units detected by diagnostic testing on the given day.  This value includes true- as well as false-positive units.')
    detect_new_animal_test = models.IntegerField(blank=True, null=True, 
        help_text='(detection new Animals Tested)  Total number of animals in units detected by diagnostic testing on the given day.')
    detect_cum_unit_test = models.IntegerField(blank=True, null=True, 
        help_text='Number of units detected by diagnostic testing over the course of the iteration. This value includes true- as well as false-positive units')
    detect_cum_animal_test = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units detected by diagnostic testing over the course of the iteration')
    destroy_cum_unit_initial = models.IntegerField(blank=True, null=True, 
        help_text='Number of units destroyed prior to the start of the simulation')
    destroy_cum_animal_initial = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units destroyed prior to the start of the simulation')
    destroy_cum_unit_detect = models.IntegerField(blank=True, null=True, 
        help_text='Number of units destroyed because disease was detected over the course of an iteration')
    destroy_cum_animal_detect = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units destroyed because disease was detected over the course of an iteration')
    destroy_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Number of units destroyed due to a successful trace forward of direct contact with an infected unit over the course of the iteration')
    destroy_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units destroyed due to a successful trace forward of direct contact with an infected unit over the course of the iteration')
    destroy_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Number of units destroyed due to a successful trace forward of indirect contact with an infected unit over the course of the iteration')
    destroy_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units destroyed due to a successful trace forward of indirect contact with an infected unit over the course of the iteration')
    destroy_cum_unit_dir_back = models.IntegerField(blank=True, null=True, 
        help_text='Number of units destroyed due to a successful trace back of direct contact with an infected unit over the course of the iteration')
    destroy_cum_animal_dir_back = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units destroyed due to a successful trace back of direct contact with an infected unit over the course of the iteration')
    destroy_cum_unit_ind_back = models.IntegerField(blank=True, null=True, 
        help_text='Number of units destroyed due to a successful trace back of indirect contact with an infected unit over the course of the iteration')
    destroy_cum_animal_ind_back = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units destroyed due to a successful trace back of indirect contact with an infected unit over the course of the iteration')
    destroy_cum_unit_ring = models.IntegerField(blank=True, null=True, 
        help_text='Number of units destroyed because they were in a destruction ring over the course of an iteration')
    destroy_cum_animal_ring = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units destroyed because they were in a destruction ring over the course of an iteration')
    destroy_new_unit_all = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that are new for a given day of all production types that have moved into tjhe destruction que.')
    destroy_new_animal_all = models.IntegerField(blank=True, null=True, 
        help_text='Number of animals that are new for a given day of all production types that have moved into tjhe destruction que.')
    destroy_wait_unit_all = models.IntegerField(blank=True, null=True, 
        help_text='(destruction waiting Units All)  Total number of units awaiting destruction on the indicated day.')
    destroy_wait_animal_all = models.IntegerField(blank=True, null=True, 
        help_text='(destruction waiting Animals All)  Total number of animals awaiting destruction on the indicated day.')
    vac_cum_unit_initial = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that were vaccine immune prior to the start of the simulation')
    vac_cum_animal_initial = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units that were vaccine immune prior to the start of the simulation')
    vac_cum_unit_ring = models.IntegerField(blank=True, null=True, 
        help_text='Number of units vaccinated in rings around detected-infected units over the course of an iteration')
    vac_cum_animal_ring = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units vaccinated in rings around detected-infected units over the course of an iteration')
    vac_new_unit_all = models.IntegerField(blank=True, null=True, 
        help_text='Number of units vaccinated for any reason over the course of an iteration (not including initially infected units)')
    vac_new_animal_all = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units vaccinated for any reason over the course of an iteration (not including initially infected units)')
    vac_wait_unit_all = models.IntegerField(blank=True, null=True, 
        help_text='(vaccination waiting Units All)  Total number of units awaiting vaccination on the indicated day.  Units that are present in the vaccination queue multiple times will count multiple times toward this total.')
    vac_wait_animal_all = models.IntegerField(blank=True, null=True, 
        help_text='(vaccination waiting Animals All)  Total number of animals awaiting vaccination on the indicated day.  Units that are present in the vaccination queue multiple times will count multiple times toward this total.')
    zone_new_foci = models.IntegerField(blank=True, null=True, 
        help_text='Total number of new zone foci created around units of the indicated type on the given day ')
    zone_cum_foci = models.IntegerField(blank=True, null=True, 
        help_text='Total number of new zone foci created around units of the indicated type over the course of an iteration')


class OutDailyByZone(models.Model):
    iteration = models.IntegerField(blank=True, null=True, 
        help_text='The iteration during which the outputs in this records where generated.')
    day = models.IntegerField(blank=True, null=True, 
        help_text='The day within the iteration on which these outputs were generated.')
    zone = models.ForeignKey(InZone, 
        help_text='Identifier of the zone for which this event occurred.')
    zone_area = models.FloatField(blank=True, null=True, 
        help_text='In square Kilometers')
    zone_perimeter = models.FloatField(blank=True, null=True, 
        help_text='In Kilometers')


class OutDailyByZoneAndProductionType(models.Model):
    iteration = models.IntegerField(blank=True, null=True, 
        help_text='The iteration during which the outputs in this records where generated.')
    day = models.IntegerField(blank=True, null=True, 
        help_text='The day within the iteration on which these outputs were generated.')
    zone = models.ForeignKey(InZone, 
        help_text='Identifier of the zone for which this event occurred.')
    production_type = models.ForeignKey(InProductionType, 
        help_text='The identifier of the production type that these outputs apply to.')
    unit_days_in_zone = models.IntegerField(blank=True, null=True, 
        help_text='Total number of unit days spent in a zone (1 unit for 1 day = 1 unit day 1 unit for 2 days = 2 unit days etc.)')
    animal_days_in_zone = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animal days spent in a zone (1 animal for 1 day = 1 animal day 1 animal for 2 days = 2 animal days etc.)')
    units_in_zone = models.IntegerField(blank=True, null=True, 
        help_text='Number of units of the given production type in the zone')
    animals_in_zone = models.IntegerField(blank=True, null=True, 
        help_text='Count of animals of the given production type in the zone')


class OutDailyEvents(models.Model):
    iteration = models.IntegerField(blank=True, null=True, 
        help_text='The iteration during which the outputs in this records where generated.')
    day = models.IntegerField(blank=True, null=True, 
        help_text='The day within the iteration on which these outputs were generated.')
    event = models.IntegerField(blank=True, null=True, 
        help_text='A number used to identify each event.')
    unit = models.ForeignKey(DynamicUnit)
    zone = models.ForeignKey(InZone, 
        help_text='Identifier of the zone for which this event occurred.')
    event_code = models.CharField(max_length=255, blank=True, 
        help_text='Code to indicate the type of event.')
    new_state_code = models.CharField(max_length=255, blank=True, 
        help_text='For transition state changesthis field indicates the state that results from the event.')
    test_result_code = models.CharField(max_length=255, blank=True, 
        help_text='For trace events this field indicates if the attempted trace succeeded.')


class OutDailyExposures(models.Model):
    iteration = models.IntegerField(blank=True, null=True, 
        help_text='The iteration during which the outputs in this records where generated.')
    day = models.IntegerField(blank=True, null=True, 
        help_text='The day within the iteration on which these outputs were generated.')
    exposure = models.IntegerField(blank=True, null=True, 
        help_text='An identifier of each exposure.')
    initiated_day = models.IntegerField(blank=True, null=True)
    exposed_unit = models.ForeignKey(DynamicUnit, related_name='events_where_unit_was_exposed')
    exposed_zone = models.ForeignKey(InZone, related_name='events_that_exposed_this_zone', 
        help_text='The identifier of the zone of the source herd for the exposure.')
    exposing_unit = models.ForeignKey(DynamicUnit, related_name='events_where_unit_exposed_others')
    exposing_zone = models.ForeignKey(InZone, related_name='events_that_exposed_others', 
        help_text='The identifier of the zone of the recipient herd for the exposure.')
    spread_method_code = models.CharField(max_length=255, blank=True, 
        help_text='Code indicating the mechanism of the disease spread.')
    is_adequate = models.NullBooleanField(blank=True, null=True, 
        help_text='Indicator if the exposure was adequate to transmit dieases.')  # Changed Booleans to NullBooleans so as not to restrict output
    exposing_unit_status_code = models.CharField(max_length=255, blank=True)
    exposed_unit_status_code = models.CharField(max_length=255, blank=True)


class OutEpidemicCurves(models.Model):
    iteration = models.IntegerField(blank=True, null=True, 
        help_text='The iteration during which the outputs in this records where generated.')
    day = models.IntegerField(blank=True, null=True, 
        help_text='The day within the iteration on which these outputs were generated.')
    production_type = models.ForeignKey(InProductionType, 
        help_text='The identifier of the production type that these outputs apply to.')
    infected_units = models.IntegerField(blank=True, null=True, 
        help_text='The number of units of the specified production type infected by any mechanism on the specific day in a spcified iteration.')
    infected_animals = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in an infected unit.')
    detected_units = models.IntegerField(blank=True, null=True, 
        help_text='The number of clinically ill units of the specified production type detected by any mechanism on the specified day in the specified iteration.')
    detected_animals = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in the detected unit.')
    infectious_units = models.IntegerField(blank=True, null=True, 
        help_text='Number of infectious units both apparent and not apparent')
    apparent_infectious_units = models.IntegerField(blank=True, null=True, 
        help_text='APPARENT INFECTIOUS UNITS')


class OutGeneral(models.Model):
    simulation_start_time = models.DateTimeField(max_length=255, blank=True, 
        help_text='The actual clock time according to the system clock of when the simulation started.')
    simulation_end_time = models.DateTimeField(max_length=255, blank=True, 
        help_text='The actual clock time according to the system clock of when the simulation ended.')
    completed_iterations = models.IntegerField(blank=True, null=True, 
        help_text='Number of iterations completed during the simulation run.')
    version = models.CharField(max_length=255, blank=True, 
        help_text='Number of the NAADSM Version used to run the simulation.')


class OutIteration(models.Model):
    iteration = models.IntegerField(blank=True, null=True, 
        help_text='The iteration during which the outputs in this records where generated.')
    disease_ended = models.NullBooleanField(blank=True, null=True, 
        help_text='Indicator that disease spread has ended.')  # Changed Booleans to NullBooleans so as not to restrict output
    disease_end_day = models.IntegerField(blank=True, null=True, 
        help_text='Day of the end of disease spread.')
    outbreak_ended = models.NullBooleanField(blank=True, null=True, 
        help_text='Indicator that outbreak  has ended including all control measures supporting the scenario.')  # Changed Booleans to NullBooleans so as not to restrict output
    outbreak_end_day = models.IntegerField(blank=True, null=True, 
        help_text='Day of the end of the outbreak including all control measures supporting the scenario.')
    zone_foci_created = models.NullBooleanField(blank=True, null=True, 
        help_text='Indicator is a Zone focus was created')  # Changed Booleans to NullBooleans so as not to restrict output
    destroy_wait_unit_max = models.IntegerField(blank=True, null=True, 
        help_text='Maximum number of units in queue for destruction on any given day over the course of the iteration')
    destroy_wait_unit_max_day = models.IntegerField(blank=True, null=True, 
        help_text='The first simulation day on which the maximum number of units in queue for destruction was reached')
    destroy_wait_animal_max = models.FloatField(blank=True, null=True, 
        help_text='Maximum number of animals in queue for destruction on any given day over the course of the iteration')
    destroy_wait_animal_max_day = models.IntegerField(blank=True, null=True, 
        help_text='The first simulation day on which the maximum number of animals in queue for destruction was reached')
    destroy_wait_unit_time_max = models.IntegerField(blank=True, null=True, 
        help_text='Maximum number of days spent in queue for destruction by any single unit over the course of the iteration')
    destroy_wait_unit_time_avg = models.FloatField(blank=True, null=True, 
        help_text='Average number of days spent by each unit in queue for destruction over the course of the iteration')
    vac_wait_unit_max = models.IntegerField(blank=True, null=True, 
        help_text='Maximum number of units in queue for vaccination on any given day over the course of the iteration')
    vac_wait_unit_max_day = models.IntegerField(blank=True, null=True, 
        help_text='The first simulation day on which the maximum number of units in queue for vaccination was reached')
    vac_wait_animal_max = models.FloatField(blank=True, null=True, 
        help_text='Maximum number of animals in queue for vaccination on any given day over the course of the iteration')
    vac_wait_animal_max_day = models.IntegerField(blank=True, null=True, 
        help_text='The first simulation day on which the maximum number of animals in queue for vaccination was reached')
    vac_wait_unit_time_max = models.IntegerField(blank=True, null=True, 
        help_text='Maximum number of days spent in queue for vaccination by any single unit over the course of the iteration')
    vac_wait_unit_time_avg = models.FloatField(blank=True, null=True, 
        help_text='Average number of days spent in queue for vaccination by each unit that was vaccinated over the course of the iteration')


class OutIterationByUnit(models.Model):
    iteration = models.IntegerField(blank=True, null=True, 
        help_text='The iteration during which the outputs in this records where generated.')
    unit = models.ForeignKey(DynamicUnit)
    last_status_code = models.CharField(max_length=255, blank=True, 
        help_text='Final status that a unit was in for an iteration')
    last_status_day = models.IntegerField(blank=True, null=True, 
        help_text='Day that a unit was in the final status for an iteration')
    last_control_state_code = models.CharField(max_length=255, blank=True, 
        help_text='Final Control State that a unit was in for an iteration')
    last_control_state_day = models.IntegerField(blank=True, null=True, 
        help_text='Day that a unit went in to the final status for an iteration')


class OutIterationByProductionType(models.Model):
    iteration = models.IntegerField(blank=True, null=True, 
        help_text='The iteration during which the outputs in this records where generated.')
    production_type = models.ForeignKey(InProductionType, 
        help_text='The identifier of the production type that these outputs apply to.')
    transition_state_cum_unit_susceptible = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that are or become susceptible over the course of an iteration')
    transition_state_cum_animal_susceptible = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units that are or become susceptible over the course of an iteration')
    transition_state_cum_unit_latent = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that are or become latent over the course of an iteration')
    transition_state_cum_animal_latent = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units that are or become latent over the course of an iteration')
    transition_state_cum_unit_subclinical = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that are or become subclinically infectious over the course of an iteration')
    transition_state_cum_animal_subclinical = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units that are or become infectious over the course of an iteration')
    transition_state_cum_unit_clinical = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that are or become clinical over the course of an iteration')
    transition_state_cum_animal_clinical = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units that are or become clinical over the course of an iteration')
    transition_state_cum_unit_nat_immune = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that are or become naturally immune over the course of an iteration')
    transition_state_cum_animal_nat_immune = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units that are or become naturally immune over the course of an iteration')
    transition_state_cum_unit_vac_immune = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that are or become vaccine immune over the course of an iteration')
    transition_state_cum_animal_vac_immune = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units that are or become vaccine immune over the course of an iteration')
    transition_state_cum_unit_destroyed = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that are destroyed over the course of an iteration')
    transition_state_cum_animal_destroyed = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units that are destroyed over the course of an iteration')
    infection_cum_unit_initial = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that are initially infected at the beginning of an iteration')
    infection_cum_animal_initial = models.IntegerField(blank=True, null=True, 
        help_text='Number of animals in units that are initially infected at the beginning of an iteration')
    infection_cum_unit_air = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that become infected by airborne spread over the course of an iteration')
    infection_cum_animal_air = models.IntegerField(blank=True, null=True, 
        help_text='Number of animals in units that become infected by airborne spread over the course of an iteration')
    infection_cum_unit_dir = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that become infected by direct contact over the course of an iteration')
    infection_cum_animal_dir = models.IntegerField(blank=True, null=True, 
        help_text='Number of animals that become infected by direct contact over the course of an iteration')
    infection_cum_unit_ind = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that become infected by indirect contact over the course of an iteration')
    infection_cum_animal_ind = models.IntegerField(blank=True, null=True, 
        help_text='Number of animals in units that become infected by indirect contact over the course of an iteration')
    exposed_cum_unit_dir = models.IntegerField(blank=True, null=True, 
        help_text='Total number of units directly exposed to any infected unit over the course of an iteration')
    exposed_cum_animal_dir = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units directly exposed to any infected unit over the course of an iteration')
    exposed_cum_unit_ind = models.IntegerField(blank=True, null=True, 
        help_text='Total number of units indirectly exposed to any infected unit over the course of an iteration')
    exposed_cum_animal_ind = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units indirectly exposed to any infected unit over the course of an iteration')
    trace_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units directly exposed and successfully traced forward over the course of an iteration')
    trace_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units directly exposed and successfully traced forward over the course of an iteration')
    trace_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Number of units indirectly exposed and successfully traced forward over the course of an iteration')
    trace_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units indirectly exposed and successfully traced forward over the course of an iteration')
    trace_cum_unit_dir_p_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Number of units directly exposed that could possibly have been traced forward over the course of an iteration')
    trace_cum_animal_dir_pfwd = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units directly exposed that could possibly have been traced forward over the course of an iteration')
    trace_cum_unit_ind_p_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Number of units indirectly exposed that could possibly have been traced forward over the course of an iteration')
    trace_cum_animal_ind_p_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units indirectly exposed that could possibly have been traced forward over the course of an iteration')
    trace_cum_unit_dir_back = models.IntegerField(blank=True, null=True, 
        help_text='Number of units successfully traced back from a detected unit after direct contact over the course of the iteration')
    trace_cum_animal_dir_back = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units successfully traced back from a detected unit over the course of the iteration')
    trace_cum_unit_ind_back = models.IntegerField(blank=True, null=True, 
        help_text='Number of units successfully traced back from a detected unit after indirect contact over the course of the iteration')
    trace_cum_animal_ind_back = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units successfully traced back from a detected unit after indirect contact over the course of the iteration')
    trace_cum_unit_dir_p_back = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that could possibly have been traced back from a detected unit after direct contact over the course of the iteration')
    trace_cum_animal_dir_pback = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units that could possibly have been traced back from a detected unit after direct contact over the course of the iteration')
    trace_cum_unit_ind_p_back = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that could possibly have been traced back from a detected unit after indirect contact over the course of the iteration')
    trace_cum_animal_ind_p_back = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units that could possibly have been traced back from a detected unit after indirect contact over the course of the iteration')
    trace_origin_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Number of trace-forwards of direct contact that originate at units of the designated type over the course of an iteration')
    trace_origin_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Number of trace-forwards of indirect contact that originate at units of the designated type over the course of an iteration')
    trace_origin_cum_unit_dir_back = models.IntegerField(blank=True, null=True, 
        help_text='Number of trace-backs of direct contact that originate at units of the designated type over the course of an iteration')
    trace_origin_cum_unit_ind_back = models.IntegerField(blank=True, null=True, 
        help_text='Number of trace-backs of indirect contact that originate at units of the designated type over the course of an iteration')
    exam_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Number of units subjected to a herd exam after a trace-forward of direct contact over the course of the iteration')
    exam_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units subjected to a herd exam after a trace-forward of direct contact over the course of the iteration')
    exam_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Number of units subjected to a herd exam after a trace-forward of indirect contact over the course of the iteration')
    exam_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units subjected to a herd exam after a trace-forward of indirect contact over the course of the iteration')
    exam_cum_unit_dir_back = models.IntegerField(blank=True, null=True, 
        help_text='Number of units subjected to a herd exam after a trace-back of direct contact over the course of the iteration')
    exam_cum_animal_dir_back = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units subjected to a herd exam after a trace-back of direct contact over the course of the iteration')
    exam_cum_unit_ind_back = models.IntegerField(blank=True, null=True, 
        help_text='Number of units subjected to a herd exam after a trace-back of indirect contact over the course of the iteration')
    exam_cum_animal_ind_back = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units subjected to a herd exam after a trace-back of indirect contact over the course of the iteration')
    test_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Number of units subjected to diagnostic testing after a trace-forward of direct contact over the course of the iteration')
    test_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units subjected to diagnostic testing after a trace-forward of direct contact over the course of the iteration')
    test_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Number of units subjected to diagnostic testing after a trace-forward of indirect contact over the course of the iteration')
    test_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units subjected to diagnostic testing after a trace-forward of indirect contact over the course of the iteration')
    test_cum_unit_dir_back = models.IntegerField(blank=True, null=True, 
        help_text='Number of units subjected to diagnostic testing after a trace-back of direct contact over the course of the iteration')
    test_cum_animal_dir_back = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units subjected to diagnostic testing after a trace-back of direct contact over the course of the iteration')
    test_cum_unit_ind_back = models.IntegerField(blank=True, null=True, 
        help_text='Number of units subjected to diagnostic testing after a trace-back of indirect contact over the course of the iteration')
    test_cum_animal_ind_back = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units subjected to diagnostic testing after a trace-back of indirect contact over the course of the iteration')
    test_cum_unit_true_pos = models.IntegerField(blank=True, null=True, 
        help_text='Number of tested units with a true positive diagnostic test result over the course of the iteration')
    test_cum_animal_true_pos = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in tested units with a true positive diagnostic test result over the course of the iteration')
    test_cum_unit_true_neg = models.IntegerField(blank=True, null=True, 
        help_text='Number of tested units with a true negative diagnostic test result over the course of the iteration')
    test_cum_animal_true_neg = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in tested units with a true negative diagnostic test result over the course of the iteration')
    test_cum_unit_false_pos = models.IntegerField(blank=True, null=True, 
        help_text='Number of tested units with a false positive diagnostic test result over the course of the iteration')
    test_cum_animal_false_pos = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in tested units with a false positive diagnostic test result over the course of the iteration')
    test_cum_unit_false_neg = models.IntegerField(blank=True, null=True, 
        help_text='Number of tested units with a false negative diagnostic test result over the course of the iteration')
    test_cum_animal_false_neg = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in tested units with a false negative diagnostic test result over the course of the iteration')
    detect_cum_unit_clin = models.IntegerField(blank=True, null=True, 
        help_text='Number of units detected by clinical signs over the course of an iteration')
    detect_cum_animal_clin = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units detected by clinical signs over the course of an iteration')
    detect_cum_unit_test = models.IntegerField(blank=True, null=True, 
        help_text='Number of units detected by diagnostic testing over the course of the iteration. This value includes true- as well as false-positive units')
    detect_cum_animal_test = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units detected by diagnostic testing over the course of the iteration')
    destroy_cum_unit_initial = models.IntegerField(blank=True, null=True, 
        help_text='Number of units destroyed prior to the start of the simulation')
    destroy_cum_animal_initial = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units destroyed prior to the start of the simulation')
    destroy_cum_unit_detect = models.IntegerField(blank=True, null=True, 
        help_text='Number of units destroyed because disease was detected over the course of an iteration')
    destroy_cum_animal_detect = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units destroyed because disease was detected over the course of an iteration')
    destroy_cum_unit_dir_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Number of units destroyed due to a successful trace forward of direct contact with an infected unit over the course of the iteration')
    destroy_cum_animal_dir_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units destroyed due to a successful trace forward of direct contact with an infected unit over the course of the iteration')
    destroy_cum_unit_ind_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Number of units destroyed due to a successful trace forward of indirect contact with an infected unit over the course of the iteration')
    destroy_cum_animal_ind_fwd = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units destroyed due to a successful trace forward of indirect contact with an infected unit over the course of the iteration')
    destroy_cum_unit_dir_back = models.IntegerField(blank=True, null=True, 
        help_text='Number of units destroyed due to a successful trace back of direct contact with an infected unit over the course of the iteration')
    destroy_cum_animal_dir_back = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units destroyed due to a successful trace back of direct contact with an infected unit over the course of the iteration')
    destroy_cum_unit_ind_back = models.IntegerField(blank=True, null=True, 
        help_text='Number of units destroyed due to a successful trace back of indirect contact with an infected unit over the course of the iteration')
    destroy_cum_animal_ind_back = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units destroyed due to a successful trace back of indirect contact with an infected unit over the course of the iteration')
    destroy_cum_unit_ring = models.IntegerField(blank=True, null=True, 
        help_text='Number of units destroyed because they were in a destruction ring over the course of an iteration')
    destroy_cum_animal_ring = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units destroyed because they were in a destruction ring over the course of an iteration')
    destroy_wait_unit_max = models.IntegerField(blank=True, null=True, 
        help_text='Maximum number of units in queue for destruction on any given day over the course of the iteration')
    destroy_wait_animal_max = models.IntegerField(blank=True, null=True, 
        help_text='Maximum number of animals in queue for destruction on any given day over the course of the iteration')
    destroy_wait_unit_max_day = models.IntegerField(blank=True, null=True, 
        help_text='The first simulation day on which the maximum number of units in queue for destruction was reached')
    destroy_wait_animal_max_day = models.IntegerField(blank=True, null=True, 
        help_text='The first simulation day on which the maximum number of animals in queue for destruction was reached')
    destroy_wait_unit_time_max = models.IntegerField(blank=True, null=True, 
        help_text='Maximum number of days spent in queue for destruction by any single unit over the course of the iteration')
    destroy_wait_unit_time_avg = models.FloatField(blank=True, null=True, 
        help_text='Average number of days spent by each unit in queue for destruction over the course of the iteration')
    destroy_wait_unit_days_in_queue = models.FloatField(blank=True, null=True, 
        help_text='Total number of unit-days spent in queue for destruction')
    destroy_wait_animal_days_in_queue = models.FloatField(blank=True, null=True, 
        help_text='Total number of animal-days spent in queue for destruction')
    vac_cum_unit_initial = models.IntegerField(blank=True, null=True, 
        help_text='Number of units that were vaccine immune prior to the start of the simulation')
    vac_cum_animal_initial = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in units that were vaccine immune prior to the start of the simulation')
    vac_cum_unit_ring = models.IntegerField(blank=True, null=True, 
        help_text='Number of units vaccinated in rings around detected-infected units over the course of an iteration')
    vac_cum_animal_ring = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animals in all units vaccinated in rings around detected-infected units over the course of an iteration')
    vac_wait_unit_max = models.IntegerField(blank=True, null=True, 
        help_text='Maximum number of units in queue for vaccination on any given day over the course of the iteration')
    vac_wait_animal_max = models.FloatField(null=True, blank=True, 
        help_text='Maximum number of animals in queue for vaccination on any given day over the course of the iteration')
    vac_wait_unit_max_day = models.IntegerField(blank=True, null=True, 
        help_text='The first simulation day on which the maximum number of units in queue for vaccination was reached')
    vac_wait_animal_max_day = models.IntegerField(blank=True, null=True, 
        help_text='The first simulation day on which the maximum number of animals in queue for vaccination was reached')
    vac_wait_unit_time_max = models.FloatField(null=True, blank=True, 
        help_text='Maximum number of days spent in queue for vaccination by any single unit over the course of the iteration')
    vac_wait_unit_time_avg = models.IntegerField(blank=True, null=True, 
        help_text='Average number of days spent in queue for vaccination by each unit that was vaccinated over the course of the iteration')
    zone_foci = models.IntegerField(blank=True, null=True)
    first_detection = models.IntegerField(blank=True, null=True, 
        help_text='Day of first detection of an infected unit in the specified iteration')
    first_det_unit_inf = models.IntegerField(blank=True, null=True, 
        help_text='Number of units already infected at the time of first detection of an infected unit of any production type in the specified iteration')
    first_detect_animal_inf = models.IntegerField(blank=True, null=True, 
        help_text='Number of animals in units already infected at the time of first detection of an infected unit of any production type in the specified iteration')
    first_destruction = models.IntegerField(blank=True, null=True, 
        help_text='Day of first destruction of a unit in the specified iteration')
    first_vaccination = models.IntegerField(blank=True, null=True, 
        help_text='Day of first vaccination of a unit in the specified iteration')
    last_detection = models.IntegerField(blank=True, null=True, 
        help_text='Day of last detection of an infected unit in the specified iteration')


class OutIterationByZone(models.Model):
    iteration = models.IntegerField(blank=True, null=True, 
        help_text='The iteration during which the outputs in this records where generated.')
    zone = models.ForeignKey(InZone, 
        help_text='Identifier of the zone for which this event occurred.')
    max_zone_area = models.FloatField(blank=True, null=True, 
        help_text='Maximum area (in square kilometers) reached for the indicated zone over the course of an iteration')
    max_zone_area_day = models.IntegerField(blank=True, null=True, 
        help_text='Day on which maximum area for the indicated zone is reached')
    final_zone_area = models.FloatField(blank=True, null=True, 
        help_text='Area (in square kilometers) of the indicated zone at the end of an iteration')
    max_zone_perimeter = models.FloatField(blank=True, null=True, 
        help_text='Maximum perimeter (in kilometers) reached for the indicated zone over the course of an iteration')
    max_zone_perimeter_day = models.IntegerField(blank=True, null=True, 
        help_text='Day on which maximum perimeter for the indicated zone is reached')
    final_zone_perimeter = models.FloatField(blank=True, null=True, 
        help_text='Perimeter (in kilometers) of the indicated zone at the end of an iteration')


class OutIterationByZoneAndProductionType(models.Model):
    iteration = models.IntegerField(blank=True, null=True, 
        help_text='The iteration during which the outputs in this records where generated.')
    zone = models.ForeignKey(InZone, 
        help_text='Identifier of the zone for which this event occurred.')
    production_type = models.ForeignKey(InProductionType, 
        help_text='The identifier of the production type that these outputs apply to.')
    unit_days_in_zone = models.IntegerField(blank=True, null=True, 
        help_text='Total number of unit days spent in a zone (1 unit for 1 day = 1 unit day 1 unit for 2 days = 2 unit days etc.)')
    animal_days_in_zone = models.IntegerField(blank=True, null=True, 
        help_text='Total number of animal days spent in a zone (1 animal for 1 day = 1 animal day 1 animal for 2 days = 2 animal days etc.)')
    cost_surveillance = models.FloatField(blank=True, null=True, 
        help_text='Total cost associated with surveillance in a zone over the course of an iteration.')


class OutIterationCosts(models.Model):
    iteration = models.IntegerField(blank=True, null=True, 
        help_text='The iteration during which the outputs in this records where generated.')
    production_type = models.ForeignKey(InProductionType, 
        help_text='The identifier of the production type that these outputs apply to.')
    destroy_appraisal = models.FloatField(blank=True, null=True, 
        help_text='Total cost of appraisal for all units destroyed over the course of an iteration.')
    destroy_cleaning = models.FloatField(blank=True, null=True, 
        help_text='Total cost of cleaning and disinfection for all units destroyed over the course of an iteration.')
    destroy_euthanasia = models.FloatField(blank=True, null=True, 
        help_text='Total cost of euthanasia for all animals in units destroyed over the course of an iteration.')
    destroy_indemnification = models.FloatField(blank=True, null=True, 
        help_text='Total cost of indemnification for all animals in units destroyed over the course of an iteration.')
    destroy_disposal = models.FloatField(blank=True, null=True, 
        help_text='Total cost of carcass disposal for all animals in units destroyed over the course of an iteration.')
    vac_cum_setup = models.FloatField(blank=True, null=True, 
        help_text='Total cost of vaccination setup for all units vaccinated over the course of an iteration.')
    vac_cum_vaccination = models.FloatField(blank=True, null=True, 
        help_text='Total cost of vaccination for all animals in units vaccinated over the course of an iteration.')



