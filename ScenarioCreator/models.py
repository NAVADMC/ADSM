"""This models file specifies all the tables used to create a settings file for
a SpreadModel simulation.
This project uses Django 1.7 migrations for database structure changes.
Use manage.py makemigrations APPNAME whenever the models.py changes.
Then run manage.py migrate to apply the changes.

This file in particular and the project in general
relies heavily on conventions.  Please be careful to follow the existing conventions
whenever you edit this file.
Conventions:
- field names are lower cased and separated by underscores, Django forms relies on this
- hidden fields that will be filled in by exportvalidation.py start with an _
    - forms.py relies on this
- the names of Models are replicated in the hyperlinks
- Model names are used in forms.py by appending <ModelName>Form to the end
- Outdated: Previously scripts/textscrubber.py relies on the only blank lines being between classes
    DO NOT put blank lines in the middle of models or before a class method
- a Model with 'name' as the first field is assumed to be referenced other places
    forms.py will give this special back-track features
- to keep indentation consistent, field attributes (help_text) are double tabbed
    This is one case where normal python convention would look even worse.
    Don't autoformat this page.  You'll regret it
- ForeignKeys that reference singletons (id=1) rely on the views.py redirect if it doesn't exist
    The redirect avoids creating a blank table that you then can't access

Changes made in ScenarioCreator/models.py propagate to the script output

Limit foreignkey choices with a dictionary filter on field values:
                     limit_choices_to={'is_staff': True}
"""

import re
import time
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_extras.db.models import LatitudeField, LongitudeField, MoneyField
from ScenarioCreator.custom_fields import PercentField
from ScenarioCreator.templatetags.db_status_tags import wiki, link
import ScenarioCreator.parser
import Settings.models


def chc(*choice_list):
    return tuple((x, x) for x in choice_list)


def priority_choices():
    return chc('reason, time waiting, production type',
               'reason, production type, time waiting',
               'time waiting, reason, production type',
               'time waiting, production type, reason',
               'production type, reason, time waiting',
               'production type, time waiting, reason')


def squish_name(name):
    return name.lower().strip().replace(' ', '').replace('_', '')


def choice_char_from_value(value, map_tuple):
    value = squish_name(value)
    for key, full_str in map_tuple:
        if value == squish_name(full_str):
            return key
    return None


sqlite_keywords = ['abort', 'action', 'add', 'after', 'all', 'alter', 'analyze', 'and', 'as', 'asc', 'attach', 'autoincrement', 'before', 'begin', 'between', 'by', 'cascade', 'case', 'cast', 'check', 'collate', 'column', 'commit', 'conflict', 'constraint', 'create', 'cross', 'current_date', 'current_time', 'current_timestamp', 'database', 'default', 'deferrable', 'deferred', 'delete', 'desc', 'detach', 'distinct', 'drop', 'each', 'else', 'end', 'escape', 'except', 'exclusive', 'exists', 'explain', 'fail', 'for', 'foreign', 'from', 'full', 'glob', 'group', 'having', 'if', 'ignore', 'immediate', 'in', 'index', 'indexed', 'initially', 'inner', 'insert', 'instead', 'intersect', 'into', 'is', 'isnull', 'join', 'key', 'left', 'like', 'limit', 'match', 'natural', 'no', 'not', 'notnull', 'null', 'of', 'offset', 'on', 'or', 'order', 'outer', 'plan', 'pragma', 'primary', 'query', 'raise', 'recursive', 'references', 'regexp', 'reindex', 'release', 'rename', 'replace', 'restrict', 'right', 'rollback', 'row', 'savepoint', 'select', 'set', 'table', 'temp', 'temporary', 'then', 'to', 'transaction', 'trigger', 'union', 'unique', 'update', 'using', 'vacuum', 'values', 'view', 'virtual', 'when', 'where', 'with', 'without']


from django.db.models.signals import post_delete
from django.dispatch import receiver

@receiver(post_delete)
def delete_repo(sender, instance, **kwargs):
    if sender == Population:
        print("Deleting", sender, instance)
        # at this point the Unit list should be clear as well
        orphans = ProductionType.objects.exclude(unit__isnull=False)
        print("Deleting", orphans)
        orphans.delete()


class BaseModel(models.Model):
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        Settings.models.unsaved_changes(True)  # avoid infinite loop by ensuring unsaved_changes doesn't call BaseModel from SmSession
        from Results.models import delete_all_outputs  # I quickly get circular imports if this is higher up
        delete_all_outputs()
        return super(BaseModel, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None):
        Settings.models.unsaved_changes(True)
        from Results.models import delete_all_outputs  # I quickly get circular imports if this is higher up
        delete_all_outputs()
        return super(BaseModel, self).delete(using)

    class Meta(object):
        abstract = True


class Population(BaseModel):
    source_file = models.CharField(max_length=255, blank=True)  # source_file made generic CharField so Django doesn't try to copy and save the raw file

    def save(self, *args, **kwargs):
        self.id = 1
        super(Population, self).save(*args, **kwargs)
        if self.source_file:
            self.import_population()  # Population must be saved to db so that it can be foreignkeyed

    def delete(self, using=None):
        for id_start in range(0, Unit.objects.count()+900, 900):  # step size 900
            Unit.objects.filter(_population=self, id__gte=id_start, id__lt=id_start + 900).delete()  # bulk delete 900 or less at a time
        super(Population, self).delete(using)

    def import_population(self):
        from Settings.models import SmSession
        session = SmSession.objects.get_or_create(id=1)[0]

        start_time = time.clock()  # perf_counter() would also work
        session.set_population_upload_status("Parsing")
        try:
            p = ScenarioCreator.parser.PopulationParser(self.source_file)
        except BaseException as error:
            self.delete()
            raise error
        data = p.parse_to_dictionary()
        session.set_population_upload_status("Creating objects")
        total = len(data)

        unit_objects = []
        for index, entry_dict in enumerate(data):
            entry_dict['_population'] = self
            unit_objects.append(Unit.create(**entry_dict))
            if index % 2000 == 0:
                progress = index
                session.set_population_upload_status("Creating %s objects:" % total, (float(progress) / total))
        session.set_population_upload_status("Preparing data", 100)
        Unit.objects.bulk_create(unit_objects)
        execution_time = (time.clock() - start_time)
        print("Done creating", '{:,}'.format(len(data)), "Units took %i seconds" % execution_time)


class Unit(BaseModel):
    def population_default():
        return Population.objects.get_or_create(id=1[0])

    _population = models.ForeignKey(Population, default=population_default, )  # If you're having an OperationalError creating a migration, remove the default on ForeignKeys duration south --auto process.
    production_type = models.ForeignKey('ProductionType',
        help_text='The production type that these outputs apply to.', )
    latitude = LatitudeField(
        help_text='The latitude used to georeference this ' + wiki("Unit") + '.', )
    longitude = LongitudeField(
        help_text='The longitude used to georeference this ' + wiki("Unit") + '.', )
    initial_state_choices = (('S', 'Susceptible'),
               ('L', 'Latent'),
               ('B', 'Infectious Subclinical'),
               ('C', 'Infectious Clinical'),
               ('N', 'Naturally Immune'),
               ('V', 'Vaccine Immune'),
               ('D', 'Destroyed'))
    initial_state = models.CharField(max_length=255, default='S',
                                     help_text='Code indicating the actual disease state of the ' + wiki("Unit") + ' at the beginning of the simulation.',
                                     choices=initial_state_choices)
    days_in_initial_state = models.IntegerField(blank=True, null=True,
        help_text='The number of days that the ' + wiki("Unit") + ' will remain in its initial state unless preempted by other events.', )
    days_left_in_initial_state = models.IntegerField(blank=True, null=True,
        help_text='Used for setting up scripted scenarios.', )
    initial_size = models.PositiveIntegerField(validators=[MinValueValidator(1)],
        help_text='The number of animals in the ' + wiki("Unit") + '.', )
    user_notes = models.TextField(blank=True)

    @classmethod
    def create(cls, **kwargs):
        for key in kwargs:  # Convert values into their proper type
            if key == 'production_type':
                kwargs[key] = ProductionType.objects.get_or_create(name=kwargs[key])[0]
            elif key in ('latitude', 'longitude'):
                kwargs[key] = float(kwargs[key])
            elif key == 'initial_size':
                kwargs[key] = int(kwargs[key])
            elif key == 'initial_state':
                kwargs[key] = choice_char_from_value(kwargs[key], Unit._meta.get_field_by_name('initial_state')[0]._choices) or 'S'
        unit = cls(**kwargs)
        return unit

    def __str__(self):
        return "Unit(%s: (%s, %s)" % (self.production_type, self.latitude, self.longitude)


class Function(BaseModel):
    """Function is a model that defines either a Probability Distribution Function (pdf) or
 a relational function (relid) depending on which child class is used.  """
    name = models.CharField(max_length=255,
        help_text='User-assigned name for each function.', )
    x_axis_units = models.CharField(max_length=255, default="Days",
        help_text='Specifies the descriptive units for the x axis in relational functions.', )
    notes = models.TextField(blank=True, null=True, help_text='', )
    class Meta(object):
        abstract = True
    def __str__(self):
        return self.name


class ProbabilityFunction(Function):
    """ There are a large number of fields in this model because different equation_type use different
        parameters.  Parameters are all listed as optional because they are frequently unused.  A second
        layer of validation will be necessary for required parameters per equation_type."""
    equation_type = models.CharField(max_length=255,
        help_text='For probability density functions identifies the type of function.',
        default="Triangular",
        choices=chc("Beta", "BetaPERT", "Bernoulli", "Binomial", "Discrete Uniform",
                    "Exponential", "Fixed Value", "Gamma", "Gaussian", "Histogram", "Hypergeometric",
                    "Inverse Gaussian", "Logistic", "LogLogistic", "Lognormal",
                    "Negative Binomial", "Pareto", "Pearson 5", "Piecewise", "Poisson",
                    "Triangular", "Uniform", "Weibull"))
    mean = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
        help_text='Functions: Inverse Gaussian, Gaussian, Lognormal, Poisson, Exponential.', )
    std_dev = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
        help_text='Functions: Gaussian, Lognormal.', )
    min = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
        help_text='Functions: Discrete Uniform, Uniform, Triangular, Beta, BetaPERT.', )
    mode = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
        help_text='Functions: Fixed Value, Triangular, BetaPERT.', )
    max = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
        help_text='Functions: Discrete Uniform, Uniform, Triangular, Beta, BetaPERT.', )
    alpha = models.FloatField(blank=True, null=True,
        help_text='Functions: Gamma, Weibull, Pearson 5, Beta.', )
    alpha2 = models.FloatField(blank=True, null=True,
        help_text='Functions: Beta.', )
    beta = models.FloatField(blank=True, null=True,
        help_text='Functions: Gamma, Weibull, Pearson 5.', )
    location = models.FloatField(blank=True, null=True,
        help_text='Functions: Logistic, LogLogistic.', )
    scale = models.FloatField(blank=True, null=True,
        help_text='Functions: Logistic, LogLogistic.', )
    shape = models.FloatField(blank=True, null=True,
        help_text='Functions: LogLogistic, Inverse Gaussian.', )
    n = models.PositiveIntegerField(validators=[MinValueValidator(0)], blank=True, null=True,
        help_text='Functions: Hypergeometric.', )
    p = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], blank=True, null=True,
        help_text='Functions: Binomial, Negative Binomial, Bernoulli.', )
    m = models.PositiveIntegerField(validators=[MinValueValidator(0)], blank=True, null=True,
        help_text='Functions: Hypergeometric.', )
    d = models.PositiveIntegerField(validators=[MinValueValidator(0)], blank=True, null=True,
        help_text='Functions: Hypergeometric.', )
    theta = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
        help_text='Functions: Pareto.', )
    a = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
        help_text='Functions:Pareto.', )
    s = models.PositiveIntegerField(validators=[MinValueValidator(0)], blank=True, null=True,
        help_text='Functions: Binomial, Negative Binomial.', )
    graph = models.ForeignKey('RelationalFunction', blank=True, null=True,
        help_text='A series of points used in: Histogram, Piecewise.')


class RelationalFunction(Function):
    y_axis_units = models.CharField(max_length=255, blank=True,
        help_text='Specifies the descriptive units for the x axis in relational functions.', )


class RelationalPoint(BaseModel):
    relational_function = models.ForeignKey(RelationalFunction)
    x = models.FloatField(validators=[MinValueValidator(0.0)], )
    y = models.FloatField(validators=[MinValueValidator(0.0)], )
    def __str__(self):
        return '%i Point(%s, %s)' % (self.relational_function.id, self.x, self.y)


class ControlMasterPlan(BaseModel):
    name = models.CharField(default="Control Master Plan", max_length=255)
    disable_all_controls = models.BooleanField(default=False,
        help_text='Disable all ' + wiki("Control activities", "control-measures") + 
                  ' for this simulation run.  Normally used temporarily to test uncontrolled disease spread.')
    destruction_program_delay = models.PositiveIntegerField(blank=True, null=True,
        help_text='The number of days that must pass after the first detection before a destruction program can begin.', )
    destruction_capacity = models.ForeignKey(RelationalFunction, related_name='+', blank=True, null=True,
        help_text="The relational function used to define the daily destruction capacity.", )
    destruction_priority_order = models.CharField(default='reason, time waiting, production type', max_length=255,
        help_text='The primary priority order for destruction.',
        choices=priority_choices(), )
    destruction_reason_order = models.CharField(max_length=255,
        default='Basic, Trace fwd direct, Trace fwd indirect, Trace back direct, Trace back indirect, Ring',
        # old DB: 'basic,direct-forward,ring,indirect-forward,direct-back,indirect-back'
        # old UI: Detected, Trace forward of direct contact, Ring, Trace forward of indirect contact, Trace back of direct contact, Trace back of indirect contact
        help_text='The secondary priority order for destruction.', )
    units_detected_before_triggering_vaccination = models.PositiveIntegerField(blank=True, null=True,
        help_text='The number of ' + wiki("Units", "unit") + ' which must be detected before the initiation of a vaccination program.', )
    vaccination_capacity = models.ForeignKey(RelationalFunction, related_name='+', blank=True, null=True,
        help_text='Relational function used to define the daily vaccination capacity.', )
    vaccination_priority_order = models.CharField(default='reason, time waiting, production type', max_length=255,
        help_text='The primary priority criteria for order of vaccinations.',
        choices=priority_choices(), )
    # vaccinate_retrospective_days = models.PositiveIntegerField(blank=True, null=True,
    #     help_text='Number of days in retrospect that should be used to determine which herds to vaccinate.', )
    def __str__(self):
        return str(self.name)


class ControlProtocol(BaseModel):
    name = models.CharField(max_length=255,
        help_text='Name your Protocol so you can recognize it later. Ex:"Quarantine"',)
    use_detection = models.BooleanField(default=True,
        help_text='Indicates if disease detection will be modeled for units of this ' + wiki("production type") + '.', )
    detection_probability_for_observed_time_in_clinical = models.ForeignKey(RelationalFunction, related_name='+', blank=True, null=True,
        help_text='Relational function used to define the probability of observing '+wiki("clinical signs", "clinically-infectious")+
                  ' in units of this ' + wiki("production type") + '.', )
    detection_probability_report_vs_first_detection = models.ForeignKey(RelationalFunction, related_name='+', blank=True, null=True,
        help_text='Relational function used to define the probability of reporting '+wiki("clinical signs", "clinically-infectious")+
                  ' in units of this ' + wiki("production type") + '.')
    detection_is_a_zone_trigger = models.BooleanField(default=False,
        help_text='Indicator if detection of infected units of this ' + wiki("production type") + ' will trigger a '+wiki("Zone")+' focus.', )
    use_tracing = models.BooleanField(default=False, )
    trace_direct_forward = models.BooleanField(default=False,
        help_text='Indicator that '+wiki("trace forward")+
                  ' will be conducted for '+wiki("direct contact")+'s where the reported unit was the source of contact and was of this ' + wiki("production type") + '.', )
    trace_direct_back = models.BooleanField(default=False,
        help_text='Indicator that '+wiki("trace back")+' will be conducted for '+wiki("direct contact")+'s where the reported unit was the source of contact and was of this ' + wiki("production type") + '.', )
    direct_trace_success_rate = PercentField(blank=True, null=True,
        help_text='Probability of success of trace for '+wiki("direct contact")+'.', )
    direct_trace_period = models.PositiveIntegerField(blank=True, null=True,
        help_text='Days before detection (critical period) for tracing of '+wiki("direct contact")+'s.', )
    trace_indirect_forward = models.BooleanField(default=False,
        help_text='Indicator that '+wiki("trace forward")+' will be conducted for '+wiki("indirect contact")+'s where the reported unit was the source of contact and was of this ' + wiki("production type") + '.', )
    trace_indirect_back = models.BooleanField(default=False,
        help_text='Indicator that '+wiki("trace back")+' will be conducted for '+wiki("indirect contact")+'s where the reported unit was the source of contact and was of this ' + wiki("production type") + '.', )
    indirect_trace_success = PercentField(blank=True, null=True,
        help_text='Probability of success of trace for '+wiki("indirect contact")+'.', )
    indirect_trace_period = models.PositiveIntegerField(blank=True, null=True,
        help_text='Days before detection  (critical period) for tracing of '+wiki("indirect contact")+'s.', )
    trace_result_delay = models.ForeignKey(ProbabilityFunction, related_name='+', blank=True, null=True,
        help_text='Delay for carrying out trace investigation result (days).', )
    direct_trace_is_a_zone_trigger = models.BooleanField(default=False,
        help_text='Indicator if direct tracing of infected units of this ' + wiki("production type") + ' will trigger a '+wiki("Zone")+' focus.', )
    indirect_trace_is_a_zone_trigger = models.BooleanField(default=False,
        help_text='Indicator if indirect tracing of infected units of this ' + wiki("production type") + ' will trigger a '+wiki("Zone")+' focus.', )
    use_destruction = models.BooleanField(default=False,
        help_text='Indicates if detected units of this ' + wiki("production type") + ' will be destroyed.', )
    destruction_is_a_ring_trigger = models.BooleanField(default=False,
        help_text='Indicates if detection of a unit of this ' + wiki("production type") + ' will trigger the formation of a destruction ring.', )
    destruction_ring_radius = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
        help_text='Radius in kilometers of the destruction ring.', )
    destruction_is_a_ring_target = models.BooleanField(default=False,
        help_text='Indicates if unit of this ' + wiki("production type") + ' will be subject to preemptive ring destruction.', )
    destroy_direct_forward_traces = models.BooleanField(default=False,
        help_text='Indicates if units of this type identified by '+wiki("trace forward")+' of '+wiki("direct contact")+'s will be subject to preemptive destruction.', )
    destroy_indirect_forward_traces = models.BooleanField(default=False,
        help_text='Indicates if units of this type identified by '+wiki("trace forward")+' of '+wiki("indirect contact")+'s will be subject to preemptive destruction.', )
    destroy_direct_back_traces = models.BooleanField(default=False,
        help_text='Indicates if units of this type identified by '+wiki("trace back")+' of '+wiki("direct contact")+'s will be subject to preemptive destruction.', )
    destroy_indirect_back_traces = models.BooleanField(default=False,
        help_text='Indicates if units of this type identified by '+wiki("trace back")+' of '+wiki("indirect contact")+'s will be subject to preemptive destruction.', )
    destruction_priority = models.PositiveIntegerField(default=5, blank=True, null=True,
        help_text='The destruction priority of this ' + wiki("production type") + ' relative to other production types.  A lower number indicates a higher priority.', )
    use_vaccination = models.BooleanField(default=False,
        help_text='Indicates if units of this ' + wiki("production type") + ' will be subject to vaccination.', )
    vaccinate_detected_units = models.BooleanField(default=False,
        help_text='Indicates if detection in units of this ' + wiki("production type") + ' will trigger vaccination.', )
    days_to_immunity = models.PositiveIntegerField(blank=True, null=True,
        help_text='The number of days required for the onset of ' + wiki("vaccine immunity", "vaccine-immune") + ' in a newly vaccinated unit of this type.', )
    minimum_time_between_vaccinations = models.PositiveIntegerField(blank=True, null=True,
        help_text='The minimum time in days between vaccination for units of this ' + wiki("production type") + '.', )
    vaccine_immune_period = models.ForeignKey(ProbabilityFunction, related_name='+', blank=True, null=True,
        help_text='Defines the '+ wiki("vaccine immune") + ' period for units of this ' + wiki("production type") + '.', )
    trigger_vaccination_ring = models.BooleanField(default=False,
        help_text='Indicates if detection of a unit of this type will trigger a vaccination ring.', )
    vaccination_ring_radius = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
        help_text='Radius in kilometers of the vaccination ring.', )
    vaccination_priority = models.PositiveIntegerField(default=5, blank=True, null=True,
        help_text='The vaccination priority of this production type relative to other production types.  A lower number indicates a higher priority.', )
    vaccination_demand_threshold = models.PositiveIntegerField(blank=True, null=True,
        help_text='The number of animals of this type that can be vaccinated before the cost of vaccination increases.', )
    cost_of_vaccination_additional_per_animal = MoneyField(default=0.0,
        help_text='The additional cost of vaccination for each vaccinated animal of this type after the threshold is exceeded.', )
    use_exams = models.BooleanField(default=False, )
    examine_direct_forward_traces = models.BooleanField(default=False,
        help_text='Indicator if units identified by the '+wiki("trace forward")+' of '+wiki("direct contact")+' will be examined for '+
                  wiki("clinical signs", "clinically-infectious")+' of disease.', )
    exam_direct_forward_success_multiplier = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
        help_text='Multiplier for the probability of observing '+wiki("clinical signs", "clinically-infectious")+' in units identified by the '+
                  wiki("trace forward")+' of '+wiki("direct contact")+'.', )
    examine_indirect_forward_traces = models.BooleanField(default=False,
        help_text='Indicator if units identified by the '+wiki("trace forward")+' of '+wiki("indirect contact")+' will be examined for '+
                  wiki("clinical signs", "clinically-infectious")+ ' of disease.', )
    exam_indirect_forward_success_multiplier = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
        help_text='Multiplier for the probability of observing '+wiki("clinical signs", "clinically-infectious")+
            ' in units identified by the '+wiki("trace forward")+' of '+wiki("indirect contact")+' .', )
    examine_direct_back_traces = models.BooleanField(default=False,
        help_text='Indicator if units identified by the '+wiki("trace back")+' of '+wiki("direct contact")+' will be examined for '+
                  wiki("clinical signs", "clinically-infectious")+ ' of disease.', )
    exam_direct_back_success_multiplier = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
        help_text='Multiplier for the probability of observing '+wiki("clinical signs", "clinically-infectious")+
            ' in units identified by the '+wiki("trace back")+' of '+wiki("direct contact")+'.', )
    examine_indirect_back_traces = models.BooleanField(default=False,
        help_text='Indicator if units identified by the '+wiki("trace back")+' of '+wiki("indirect contact")+' will be examined for '+
                  wiki("clinical signs", "clinically-infectious")+ ' of disease.', )
    examine_indirect_back_success_multiplier = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
        help_text='Multiplier for the probability of observing '+wiki("clinical signs", "clinically-infectious")+
                  ' in units identified by the '+wiki("trace back")+' of '+wiki("indirect contact")+'.', )
    use_testing = models.BooleanField(default=False, )
    test_direct_forward_traces = models.BooleanField(default=False,
        help_text='Indicator that diagnostic testing should be performed on units identified by '+wiki("trace forward")+' of '+wiki("direct contact")+'s.', )
    test_indirect_forward_traces = models.BooleanField(default=False,
        help_text='Indicator that diagnostic testing should be performed on units identified by '+wiki("trace forward")+' of '+wiki("indirect contact")+'s.', )
    test_direct_back_traces = models.BooleanField(default=False,
        help_text='Indicator that diagnostic testing should be performed on units identified by '+wiki("trace back")+' of '+wiki("direct contact")+'s.', )
    test_indirect_back_traces = models.BooleanField(default=False,
        help_text='Indicator that diagnostic testing should be performed on units identified by '+wiki("trace back")+' of '+wiki("indirect contact")+'s.', )
    test_specificity = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
        help_text=link("Test Specificity", "http://en.wikipedia.org/wiki/Sensitivity_and_specificity") + ' for units of this production type', )
    test_sensitivity = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
        help_text=link("Test Sensitivity", "http://en.wikipedia.org/wiki/Sensitivity_and_specificity") + ' for units of this production type', )
    test_delay = models.ForeignKey(ProbabilityFunction, related_name='+', blank=True, null=True,
        help_text='Function that describes the delay in obtaining test results.', )
    use_cost_accounting = models.BooleanField(default=False, )
    cost_of_destruction_appraisal_per_unit = MoneyField(default=0.0,
        help_text='The cost associated with appraisal for each destroyed unit of this type.', )
    cost_of_destruction_cleaning_per_unit = MoneyField(default=0.0,
        help_text='The cost associated with cleaning and disinfection for each destroyed unit of this type.', )
    cost_of_euthanasia_per_animal = MoneyField(default=0.0,
        help_text='The cost associated with euthanizing each destroyed animal of this type.', )
    cost_of_indemnification_per_animal = MoneyField(default=0.0,
        help_text='The cost of indemnification for each destroyed animal of this type.', )
    cost_of_carcass_disposal_per_animal = MoneyField(default=0.0,
        help_text='The cost of carcass disposal for each destroyed animal of this type.', )
    cost_of_vaccination_setup_per_unit = MoneyField(default=0.0,
        help_text='The cost of site setup for each vaccinated unit of this type.', )
    cost_of_vaccination_baseline_per_animal = MoneyField(default=0.0,
        help_text='The baseline cost of vaccination for each vaccinated animal of this type. This cost applies to all vaccinations before the threshold is met. ', )
    def __str__(self):
        return "Protocol: %s" % (self.name, )


class ProtocolAssignment(BaseModel):
    def control_master_plan_default():
        return ControlMasterPlan.objects.get_or_create(id=1)[0]

    _master_plan = models.ForeignKey('ControlMasterPlan',
                                     default=control_master_plan_default,
                                     # If you're having an OperationalError creating a migration, remove the default on ForeignKeys duration south --auto process.
                                     help_text='Points back to a master plan for grouping purposes.')
    production_type = models.ForeignKey('ProductionType', unique=True,
        help_text='The production type that these outputs apply to.', )
    control_protocol = models.ForeignKey('ControlProtocol', blank=True, null=True,  # Just to note you're excluding it
        help_text='The control protocol to apply to this production type.')
    notes = models.CharField(max_length=255, blank=True, null=True,
        help_text='Why should this protocol be assigned to this production type?')
    def __str__(self):
        return "%s applied to %s" % (self.control_protocol, self.production_type)


class Disease(BaseModel):
    name = models.CharField(max_length=255,
        help_text='Name of the Disease')
    disease_description = models.TextField(blank=True)
    include_direct_contact_spread = models.BooleanField(default=True,
        help_text='Indicates if disease spread by '+wiki("direct contact")+' is used in the scenario.', )
    include_indirect_contact_spread = models.BooleanField(default=True,
        help_text='Indicates if disease spread by '+wiki("indirect contact")+' is used in the scenario.', )
    include_airborne_spread = models.BooleanField(default=True,
        help_text='Indicates if airborne spread is used in the model', )
    use_airborne_exponential_decay = models.BooleanField(default=False,
        help_text='Indicates if the decrease in probability by ' + wiki('airborne transmission') + ' is simulated by the exponential (TRUE) or linear (FALSE) algorithm.', )
    use_within_unit_prevalence = models.BooleanField(default=False,
        help_text='Indicates if ' + wiki("within unit prevalence") + ' should be used in the model.', )
    def __str__(self):
        return self.name


class DiseaseProgression(BaseModel):
    def disease_default():
        return Disease.objects.get_or_create(id=1)[0]

    name = models.CharField(max_length=255,
        help_text="Examples: Severe Progression, FMD Long Incubation")
    _disease = models.ForeignKey('Disease', default=disease_default, )  # If you're having an OperationalError creating a migration, remove the default on ForeignKeys duration south --auto process.
    disease_latent_period = models.ForeignKey(ProbabilityFunction, related_name='+',
        help_text='Defines the ' + wiki('latent period',"latent-state") + ' for units of this ' + wiki("production type") + '.', )
    disease_subclinical_period = models.ForeignKey(ProbabilityFunction, related_name='+',
        help_text='Defines the ' + wiki("Subclinical", "subclinically-infectious") + ' period for units of this ' + wiki("production type") + '.', )
    disease_clinical_period = models.ForeignKey(ProbabilityFunction, related_name='+',
        help_text='Defines the ' + wiki("clinical", "clinically-infectious") + ' period for units of this ' + wiki("production type") + '.', )
    disease_immune_period = models.ForeignKey(ProbabilityFunction, related_name='+',
        help_text='Defines the natural ' + wiki('immune') + ' period for units of this ' + wiki("production type") + '.', )
    disease_prevalence = models.ForeignKey(RelationalFunction, related_name='+',
        blank=True, null=True,
        help_text='Defines the prevalance for units of this ' + wiki("production type") + '.', )
    def __str__(self):
        return self.name


class DiseaseProgressionAssignment(BaseModel):
    production_type = models.ForeignKey('ProductionType', unique=True,
        help_text='The ' + wiki("production type") + ' that these outputs apply to.', )
    progression = models.ForeignKey('DiseaseProgression', blank=True, null=True) # can be excluded from disease progression
    # Since there are ProductionTypes that can be listed without having a DiseaseProgressionAssignment,
    # this addresses boolean setting _use_disease_transition in DiseaseProgression
    def __str__(self):
        return "%s have %s progression characteristics" % (self.production_type, self.progression) if self.progression else "No Progression"


class DiseaseSpread(BaseModel):
    def disease_default():
        return Disease.objects.get_or_create(id=1)[0]

    name = models.CharField(max_length=255,)
    _disease = models.ForeignKey('Disease', default=disease_default,
                                 # If you're having an OperationalError creating a migration, remove the default on ForeignKeys duration south --auto process.
                                 help_text='Parent disease whose spreading characteristics this describes.')
        # This is in Disease because of simulation restrictions
    transport_delay = models.ForeignKey(ProbabilityFunction, related_name='+', blank=True, null=True,  # This will be hidden if it's defaulted
        help_text='WARNING: THIS FIELD IS NOT RECOMMENDED BY ADSM and will be removed in later versions. Consider setting this to "-----".', )
    class Meta(object):
        abstract = True


class AbstractSpread(DiseaseSpread):  # lots of fields between Direct and Indirect that were not in Airborne
    subclinical_animals_can_infect_others = models.BooleanField(default=False,
        help_text='Indicates if ' + wiki("Subclinical", "subclinically-infectious") + 
                  ' units of the source type can spread disease by ' + wiki("direct", "direct-contact") + ' or '+ 
                  wiki("indirect contact") + '. ', )
    contact_rate = models.FloatField(validators=[MinValueValidator(0.0)],
        help_text='The average contact rate (in recipient units per source unit per day) for ' + 
                  wiki("direct", "direct-contact") + ' or '+ 
                  wiki("indirect contact") + ' models.', )
    use_fixed_contact_rate = models.BooleanField(default=False,
        help_text='Use a fixed contact rate or model contact rate as a mean distribution.', )
    distance_distribution = models.ForeignKey(ProbabilityFunction, related_name='+',
        help_text='Defines the shipment distances for ' + wiki("direct", "direct-contact") + ' or '+ 
                  wiki("indirect contact") + ' models.', )
    movement_control = models.ForeignKey(RelationalFunction, related_name='+',
        help_text=wiki("Relational function","/Relational-functions") + ' used to define movement control effects for the indicated ' + 
                  wiki("production types","production-type") + ' combinations.', )
    class Meta(object):
        abstract = True


class IndirectSpread(AbstractSpread):
    """This has to inherit from AbstractSpread or else Django treats DirectSpread and IndirectSpread as
    interchangable, which they are not."""
    infection_probability = PercentField(
        help_text='The probability that a contact will result in disease transmission. Specified for ' + 
                  wiki("direct", "direct-contact") + ' or '+ 
                  wiki("indirect contact") + ' models.', )

    def __str__(self):
        return "%s %i" % (self.name, self.id)


class DirectSpread(AbstractSpread):
    """This has to inherit from AbstractSpread or else Django treats DirectSpread and IndirectSpread as
    interchangable, which they are not."""
    infection_probability = PercentField(blank=True, null=True,
        help_text='The probability that a '+ wiki("contact will result in disease transmission", "effective-contact") + 
                  '. Specified for ' + 
                  wiki("direct", "direct-contact") + ' or '+ 
                  wiki("indirect contact") + ' models.', )
    latent_animals_can_infect_others = models.BooleanField(default=False,
        help_text='Indicates if '+wiki("latent", "latent-state")+' units of the source type can spread disease by ' + 
                  wiki("direct contact") + '.', )
    def __str__(self):
        return "%s %i" % (self.name, self.id)


class AirborneSpread(DiseaseSpread):
    spread_1km_probability = PercentField(validators=[MinValueValidator(0.0), MaxValueValidator(.999)],
        help_text='The probability that disease will be spread to unit 1 km away from the source unit.', )
    max_distance = models.FloatField(validators=[MinValueValidator(1.1)], blank=True, null=True,
        help_text='The maximum distance in KM of ' + wiki("airborne spread", "airborne-transmission") + '.  Only used in Linear Airborne Decay.', )
    exposure_direction_start = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(360)], default=0,
        help_text='The start angle in degrees of the area at risk of ' + wiki("airborne spread", "airborne-transmission") + '.  0 is North.', )
    exposure_direction_end = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(360)], default=360,
        help_text='The end angle in degrees of the area at risk of ' + wiki("airborne spread", "airborne-transmission") + '.  0 is North.', )
    def __str__(self):
        return "%s %i" % (self.name, self.id)


class Scenario(BaseModel):
    description = models.TextField(blank=True,
        help_text='The description of the %s.' % wiki('scenario'), )
    language = models.CharField(default='en', choices=(('en', "English"), ('es', "Spanish")), max_length=255, blank=True,
        help_text='Language that the model is in - English is default.', )
    random_seed = models.IntegerField(blank=True, null=True,
        help_text='The specified seed value for the random number generator.', )
    def __str__(self):
        return "Scenario: %s" % (self.description, )


class OutputSettings(BaseModel):
    iterations = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)],
        help_text='The number of iterations of this scenario that should be run', )
    stop_criteria = models.CharField(max_length=255, default='disease-end',
        help_text='The criterion used to end each iteration.',
        choices=(('disease-end', 'Stop when there are no more latent or infectious units.'),
                 ('first-detection', 'Stop when the first detection occurs.'),
                 ('outbreak-end', 'Stop when there are no more latent or infectious units and all control activities are finished'),
                 ('stop-days', 'Stop after a specified number of days')))
    days = models.PositiveIntegerField(default=1825, validators=[MinValueValidator(1)],
        help_text='The maximum number of days that iterations of this scenario should run.', )
    ## Cost Tracking
    cost_track_destruction = models.BooleanField(default=True,
        help_text='Disable this to ignore entered destruction costs.', )
    cost_track_vaccination = models.BooleanField(default=True,
        help_text='Disable this to ignore entered vaccination costs.', )
    cost_track_zone_surveillance = models.BooleanField(default=True,
        help_text='Disable this to ignore entered '+wiki("Zone")+' surveillance costs.', )

    ## Outputs requested:
    save_daily_unit_states = models.BooleanField(default=False,
        help_text='Create a plain text file with the state of each unit on each day of each iteration.', )
    save_daily_events = models.BooleanField(default=False,
        help_text='Save all daily events in a supplemental file.', )
    save_daily_exposures = models.BooleanField(default=False,
        help_text='Save all exposures in a supplemental file.', )
    save_iteration_outputs_for_units = models.BooleanField(default=True,
        help_text='Required for the Population Map. Save all iteration outputs for units in a supplemental file.', )
    save_map_output = models.BooleanField(default=False,
        help_text='Create map outputs for units in supplemental directory.', )

    def clean_fields(self, exclude=None):
        if self.stop_criteria != 'stop-days':
            self.days = 1825  # 5 year maximum simulation time

    def __str__(self):
        return "Output Settings"


class ProductionType(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def clean_fields(self, exclude=None):
        if re.findall(r'\W', self.name) or self.name.lower() in sqlite_keywords + 'All Ind Dir Air'.split():
            print("Conflicts:", re.findall(r'\W', self.name))
            raise ValidationError(self.name + " must only have alpha-numeric characters.  Keywords not allowed.")
        if re.match(r'[0-9]', self.name[0]):
            raise ValidationError(self.name + " cannot start with a number.")
        if self.name in [z.name for z in Zone.objects.all()]:  # forbid zone names
            raise ValidationError("You really shouldn't have matching Zone and Production Type names.  It makes the output confusing.")

    def __str__(self):
        return self.name


class DiseaseSpreadAssignment(BaseModel):
    source_production_type = models.ForeignKey(ProductionType, related_name='used_as_sources',
        help_text='The ' + wiki("production type") + ' that will be the source type for this ' + wiki("production type") + ' combination.', )
    destination_production_type = models.ForeignKey(ProductionType, related_name='used_as_destinations',
        help_text='The ' + wiki("production type") + ' that will be the recipient type for this ' + wiki("production type") + ' combination.', )
    direct_contact_spread = models.ForeignKey(DirectSpread, related_name='direct_spread_pair', blank=True, null=True,  # These can be blank, so no check box necessary
        help_text='Disease spread mechanism used to model spread by '+wiki("direct contact")+' between these types.', )
    indirect_contact_spread = models.ForeignKey(IndirectSpread, related_name='indirect_spread_pair', blank=True, null=True,  # These can be blank, so no check box necessary
        help_text='Disease spread mechanism used to model spread by '+wiki("indirect contact")+' between these types.', )
    airborne_spread = models.ForeignKey(AirborneSpread, related_name='airborne_spread_pair', blank=True, null=True,  # These can be blank, so no check box necessary
        help_text='Disease spread mechanism used to model spread by ' + wiki("airborne spread", "airborne-transmission") + ' between these types.', )
    class Meta(object):
        unique_together = ('source_production_type', 'destination_production_type',)
    def __str__(self):
        return "%s -> %s" % (self.source_production_type, self.destination_production_type)


class Zone(BaseModel):
    name = models.TextField(
        help_text='Description of the ' + wiki("Zone"), )
    radius = models.FloatField(validators=[MinValueValidator(0.0)],
        help_text='Radius in kilometers of the '+wiki("Zone")+'', )

    def clean_fields(self, exclude=None):
        if self.name in [pt.name for pt in ProductionType.objects.all()]:
            raise ValidationError("Don't use matching Production Type and "+wiki("Zone")+" names.  It makes the output confusing.")

    def __str__(self):
        return "%s: %skm" % (self.name, self.radius)


class ZoneEffect(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    zone_direct_movement = models.ForeignKey(RelationalFunction, related_name='+', blank=True, null=True,
        help_text='Function the describes direct movement rate.', )
    zone_indirect_movement = models.ForeignKey(RelationalFunction, related_name='+', blank=True, null=True,
        help_text='Function the describes indirect movement rate.', )
    zone_detection_multiplier = models.FloatField(validators=[MinValueValidator(0.0)], default=1.0,
        help_text='Multiplier for the probability of observing '+wiki("clinical signs", "clinically-infectious")+' in units of this ' + 
                  wiki("production type") + ' in this '+wiki("Zone")+'.', )
    cost_of_surveillance_per_animal_day = MoneyField(default=0.0,
        help_text='Cost of surveillance per animal per day in this '+wiki("Zone")+'.', )

    def __str__(self):
        return self.name


class ZoneEffectAssignment(BaseModel):
    zone = models.ForeignKey(Zone,
        help_text=''+wiki("Zone")+' for which this event occurred.', )
    production_type = models.ForeignKey('ProductionType',
        help_text='The ' + wiki("production type") + ' that these outputs apply to.', )
    effect = models.ForeignKey(ZoneEffect, blank=True, null=True,
        help_text='Describes what effect this '+wiki("Zone")+' has on this ' + wiki("production type") + '.')

    def __str__(self):
        return "%s Zone -> %s = %s" % (self.zone.name, self.production_type, self.effect.name if self.effect else "None")
