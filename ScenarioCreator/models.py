"""This models file specifies all the tables used to create a settings file for
a ADSM simulation.
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
import os

import re
import time

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django_extras.db.models import LatitudeField, LongitudeField, MoneyField

from ADSMSettings.models import SingletonManager
from ScenarioCreator.custom_fields import PercentField
from ScenarioCreator.templatetags.db_status_tags import wiki, link, bold
import ScenarioCreator.population_parser
import ADSMSettings.models
from Results.utils import delete_all_outputs


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
        ADSMSettings.models.unsaved_changes(True)
        delete_all_outputs()
        return super(BaseModel, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None):
        ADSMSettings.models.unsaved_changes(True)
        delete_all_outputs()
        return super(BaseModel, self).delete(using)

    class Meta(object):
        abstract = True


class InputSingleton(BaseModel):
    objects = SingletonManager()
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.id=1
        return super(InputSingleton, self).save(force_insert, force_update, using, update_fields)
    
    
    class Meta(object):
        abstract = True


class FloatField(models.FloatField):
    pass
    # template_name = 'floppyforms/number.html'  # critically important that floating point values have step="any" on the input


class Population(InputSingleton):
    source_file = models.CharField(max_length=255, blank=True)  # source_file made generic CharField so Django doesn't try to copy and save the raw file

    def save(self, *args, **kwargs):
        super(Population, self).save(*args, **kwargs)
        if self.source_file:
            if self.source_file.endswith('.sqlite3'):
                self.import_population_from_sqlite()
            else:
                self.import_population()  # Population must be saved to db so that it can be foreignkeyed

    def delete(self, using=None):
        if Unit.objects.count():
            for id_start in range(0, Unit.objects.last().id, 900):  # step size 900
                Unit.objects.filter(_population=self, id__lt=id_start + 900).delete()  # bulk delete 900 or less at a time
        super(Population, self).delete(using)

    def import_population(self):
        from ADSMSettings.models import SmSession
        session = SmSession.objects.get()

        start_time = time.clock()  # perf_counter() would also work
        session.set_population_upload_status("Parsing")
        try:
            p = ScenarioCreator.population_parser.PopulationParser(self.source_file)
            data = p.parse_to_dictionary()
        except BaseException as error:
            self.delete()
            raise error
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

    def import_population_from_sqlite(self):
        from django.db import connections, close_old_connections
        try:
            if not os.path.exists(self.source_file):
                raise EOFError("File does not exist in the Workspace folder")

            # connect file_path
            import_db = 'import_db'
            connections.databases[import_db] = {
                'NAME': self.source_file,
                'TEST':{'NAME': self.source_file},
                'ENGINE': 'django.db.backends.sqlite3',
                'OPTIONS': {
                    'timeout': 300,
                }
            }
            # clear any old objects
            # Population.objects.all().delete()
            ProductionType.objects.all().delete()

            # copy all population objects into memory
            if not ProductionType.objects.using(import_db).count():
                raise EOFError('No Production Types found in the target scenario.')
            ProductionType.objects.bulk_create(ProductionType.objects.using(import_db).all())
            Unit.objects.bulk_create(Unit.objects.using(import_db).all())

            # close extra database
            close_old_connections()
            connections[import_db].close()
            connections.databases.pop(import_db)
        except BaseException as error:  # ensure that Population is never left in a bad state
            self.delete()
            raise error


class Unit(BaseModel):
    def save(self, *args, **kwargs):
        self._population = Population.objects.get()
        super(Unit, self).save(*args, **kwargs)

    _population = models.ForeignKey(Population)
    production_type = models.ForeignKey('ProductionType',
        help_text='The production type that these outputs apply to.', )
    latitude = LatitudeField(
        help_text='The latitude used to georeference this ' + wiki("Unit") + '.', )
    longitude = LongitudeField(
        help_text='The longitude used to georeference this ' + wiki("Unit") + '.', )
    initial_state_choices = (('S', 'Susceptible'),  # order matters because this is read by population_parser.convert_numeric_status_codes
               ('L', 'Latent'),
               ('B', 'Infectious Subclinical'),
               ('C', 'Infectious Clinical'),
               ('N', 'Naturally Immune'),
               ('V', 'Vaccine Immune'),
               ('D', 'Destroyed'))
    initial_state = models.CharField(max_length=1, default='S',
                                     help_text='Code indicating the actual disease state of the ' + wiki("Unit") + ' at the beginning of the simulation.',
                                     choices=initial_state_choices)
    days_in_initial_state = models.IntegerField(blank=True, null=True,
        help_text='The number of days that the ' + wiki("Unit") + ' will remain in its initial state unless preempted by other events.', )
    days_left_in_initial_state = models.IntegerField(blank=True, null=True,
        help_text='Used for setting up scripted scenarios.', )
    initial_size = models.PositiveIntegerField(validators=[MinValueValidator(1)],
        help_text='The number of animals in the ' + wiki("Unit") + '.', )
    user_notes = models.CharField(max_length=255, blank=True, null=True)  # as long as possible

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
                if len(kwargs[key]) > 1:
                    new_val = choice_char_from_value(kwargs[key], Unit._meta.get_field_by_name('initial_state')[0]._choices)
                    if new_val is None:
                        raise ValidationError(kwargs[key] + " is not a valid state")
                    kwargs[key] = new_val
        unit = cls(**kwargs)
        unit.full_clean()
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
    mean = FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
        help_text='Functions: Inverse Gaussian, Gaussian, Lognormal, Poisson, Exponential.', )
    std_dev = FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
        help_text='Functions: Gaussian, Lognormal.', )
    min = FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
        help_text='Functions: Discrete Uniform, Uniform, Triangular, Beta, BetaPERT.', )
    mode = FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
        help_text='Functions: Fixed Value, Triangular, BetaPERT.', )
    max = FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
        help_text='Functions: Discrete Uniform, Uniform, Triangular, Beta, BetaPERT.', )
    alpha = FloatField(blank=True, null=True,
        help_text='Functions: Gamma, Weibull, Pearson 5, Beta.', )
    alpha2 = FloatField(blank=True, null=True,
        help_text='Functions: Beta.', )
    beta = FloatField(blank=True, null=True,
        help_text='Functions: Gamma, Weibull, Pearson 5.', )
    location = FloatField(blank=True, null=True,
        help_text='Functions: Logistic, LogLogistic.', )
    scale = FloatField(blank=True, null=True,
        help_text='Functions: Logistic, LogLogistic.', )
    shape = FloatField(blank=True, null=True,
        help_text='Functions: LogLogistic, Inverse Gaussian.', )
    n = models.PositiveIntegerField(validators=[MinValueValidator(0)], blank=True, null=True,
        help_text='Functions: Hypergeometric.', )
    p = FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], blank=True, null=True,
        help_text='Functions: Binomial, Negative Binomial, Bernoulli.', )
    m = models.PositiveIntegerField(validators=[MinValueValidator(0)], blank=True, null=True,
        help_text='Functions: Hypergeometric.', )
    d = models.PositiveIntegerField(validators=[MinValueValidator(0)], blank=True, null=True,
        help_text='Functions: Hypergeometric.', )
    theta = FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
        help_text='Functions: Pareto.', )
    a = FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
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
    x = FloatField(validators=[MinValueValidator(0.0)], )
    y = FloatField(validators=[MinValueValidator(0.0)], )
    def __str__(self):
        return '%i Point(%s, %s)' % (self.relational_function.id, self.x, self.y)


class ControlMasterPlan(InputSingleton):
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
    vaccination_capacity = models.ForeignKey(RelationalFunction, related_name='+', blank=True, null=True,
        help_text='Relational function used to define the daily vaccination capacity.', )
    restart_vaccination_capacity = models.ForeignKey(RelationalFunction, related_name='+', blank=True, null=True,
        help_text='Define if the daily vaccination capacity will be different if started a second time.', )
    vaccination_priority_order = models.CharField(default='reason, time waiting, production type', max_length=255,
        help_text='The primary priority criteria for order of vaccinations.',
        choices=priority_choices(), )
    vaccinate_retrospective_days = models.PositiveIntegerField(blank=True, null=True, default=0,
        help_text='Once a vaccination program starts, this number determines how many days previous to the start of the vaccination program a detection will trigger vaccination.', )
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
    destruction_ring_radius = FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
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
    vaccination_ring_radius = FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
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
    exam_direct_forward_success_multiplier = FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
        help_text='Multiplier for the probability of observing '+wiki("clinical signs", "clinically-infectious")+' in units identified by the '+
                  wiki("trace forward")+' of '+wiki("direct contact")+'.', )
    examine_indirect_forward_traces = models.BooleanField(default=False,
        help_text='Indicator if units identified by the '+wiki("trace forward")+' of '+wiki("indirect contact")+' will be examined for '+
                  wiki("clinical signs", "clinically-infectious")+ ' of disease.', )
    exam_indirect_forward_success_multiplier = FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
        help_text='Multiplier for the probability of observing '+wiki("clinical signs", "clinically-infectious")+
            ' in units identified by the '+wiki("trace forward")+' of '+wiki("indirect contact")+' .', )
    examine_direct_back_traces = models.BooleanField(default=False,
        help_text='Indicator if units identified by the '+wiki("trace back")+' of '+wiki("direct contact")+' will be examined for '+
                  wiki("clinical signs", "clinically-infectious")+ ' of disease.', )
    exam_direct_back_success_multiplier = FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
        help_text='Multiplier for the probability of observing '+wiki("clinical signs", "clinically-infectious")+
            ' in units identified by the '+wiki("trace back")+' of '+wiki("direct contact")+'.', )
    examine_indirect_back_traces = models.BooleanField(default=False,
        help_text='Indicator if units identified by the '+wiki("trace back")+' of '+wiki("indirect contact")+' will be examined for '+
                  wiki("clinical signs", "clinically-infectious")+ ' of disease.', )
    examine_indirect_back_success_multiplier = FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
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
    test_specificity = FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
        help_text=link("Test Specificity", "http://en.wikipedia.org/wiki/Sensitivity_and_specificity") + ' for units of this production type', )
    test_sensitivity = FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True,
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
    def save(self, *args, **kwargs):
        self._master_plan = ControlMasterPlan.objects.get()
        super(ProtocolAssignment, self).save(*args, **kwargs)

    _master_plan = models.ForeignKey('ControlMasterPlan',
                                     help_text='Points back to a master plan for grouping purposes.')
    production_type = models.OneToOneField('ProductionType',
        help_text='The production type that these outputs apply to.', )
    control_protocol = models.ForeignKey('ControlProtocol', blank=True, null=True,  # Just to note you're excluding it
        help_text='The control protocol to apply to this production type.')
    notes = models.CharField(max_length=255, blank=True, null=True,
        help_text='Why should this protocol be assigned to this production type?')
    def __str__(self):
        return "%s applied to %s" % (self.control_protocol, self.production_type)


class Disease(InputSingleton):
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
        help_text = "Indicates if the decrease in probability by "
                    + wiki("airborne transmission", "/Model-Specification#airborne-spread")
                    + " is simulated by the exponential (TRUE) or linear (FALSE) algorithm.",)
    use_within_unit_prevalence = models.BooleanField(default=False,
        help_text='Indicates if ' + wiki("within unit prevalence", "/Model-Specification#prevalence") + ' should be used in the model.', )
    def __str__(self):
        return self.name


class DiseaseProgression(BaseModel):
    def save(self, *args, **kwargs):
        self._disease = Disease.objects.get()
        super(DiseaseProgression, self).save(*args, **kwargs)

    name = models.CharField(max_length=255,
        help_text="Examples: Severe Progression, FMD Long Incubation")
    _disease = models.ForeignKey('Disease')
    disease_latent_period = models.ForeignKey(ProbabilityFunction, related_name='+',
        verbose_name='Latent period',
        help_text='Defines the ' + wiki('latent period',"latent-state") + ' for units of this ' + wiki("production type") + '.', )
    disease_subclinical_period = models.ForeignKey(ProbabilityFunction, related_name='+',
        verbose_name='Subclinical period',
        help_text='Defines the ' + wiki("Subclinical", "subclinically-infectious") + ' period for units of this ' + wiki("production type") + '.', )
    disease_clinical_period = models.ForeignKey(ProbabilityFunction, related_name='+',
        verbose_name='Clinical period',
        help_text='Defines the ' + wiki("clinical", "clinically-infectious") + ' period for units of this ' + wiki("production type") + '.', )
    disease_immune_period = models.ForeignKey(ProbabilityFunction, related_name='+',
        verbose_name='Immune period',
        help_text='Defines the natural ' + wiki('immune') + ' period for units of this ' + wiki("production type") + '.', )
    disease_prevalence = models.ForeignKey(RelationalFunction, related_name='+',
        verbose_name='Prevalence',
        blank=True, null=True,
        help_text='Defines the prevalance for units of this ' + wiki("production type") + '.', )
    def __str__(self):
        return self.name


class DiseaseProgressionAssignment(BaseModel):
    production_type = models.OneToOneField('ProductionType',
        help_text='The ' + wiki("production type") + ' that these outputs apply to.', )
    progression = models.ForeignKey('DiseaseProgression', blank=True, null=True) # can be excluded from disease progression
    # Since there are ProductionTypes that can be listed without having a DiseaseProgressionAssignment,
    # this addresses boolean setting _use_disease_transition in DiseaseProgression
    def __str__(self):
        return "%s have %s progression characteristics" % (self.production_type, self.progression) if self.progression else "No Progression"


class DiseaseSpread(BaseModel):
    def save(self, *args, **kwargs):
        self._disease = Disease.objects.get()
        super(DiseaseSpread, self).save(*args, **kwargs)

    name = models.CharField(max_length=255,)
    _disease = models.ForeignKey('Disease', help_text='Parent disease whose spreading characteristics this describes.')
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
    contact_rate = FloatField(validators=[MinValueValidator(0.0)],
         # Important: Contact_rate help_text has been given special behavior vial two data-visibility-controller 's.
        help_text=mark_safe("""<div class="help-block" data-visibility-controller="use_fixed_contact_rate" data-disabled-value="true">
                                    Fixed baseline contact rate (in outgoing contacts/unit/day) for <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki">direct</a> or <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki">indirect contact</a> models.</div>
                                <div class="help-block" data-visibility-controller="use_fixed_contact_rate" data-disabled-value="false">
                                    Mean baseline contact rate (in outgoing contacts/unit/day) for <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki">direct</a> or <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki">indirect contact</a> models.</div>"""))
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
        return "%s" % (self.name, )


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
        return "%s" % (self.name, )


class AirborneSpread(DiseaseSpread):
    spread_1km_probability = PercentField(validators=[MinValueValidator(0.0), MaxValueValidator(.999)],
        help_text='The probability that disease will be spread to unit 1 km away from the source unit.', )
    max_distance = FloatField(validators=[MinValueValidator(1.1)], blank=True, null=True,
        help_text='The maximum distance in KM of ' + wiki("airborne spread", "airborne-transmission") + '.  Only used in Linear Airborne Decay.', )
    exposure_direction_start = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(360)], default=0,
        help_text='The start angle in degrees of the area at risk of ' + wiki("airborne spread", "airborne-transmission") + '.  0 is North.', )
    exposure_direction_end = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(360)], default=360,
        help_text='The end angle in degrees of the area at risk of ' + wiki("airborne spread", "airborne-transmission") + '.  0 is North.', )
    def __str__(self):
        return "%s " % (self.name, )


class Scenario(InputSingleton):
    description = models.TextField(blank=True,
        help_text='The description of the %s.' % wiki('scenario'), )
    language = models.CharField(default='en', choices=(('en', "English"), ('es', "Spanish")), max_length=255, blank=True,
        help_text='Language that the model is in - English is default.', )
    random_seed = models.IntegerField(blank=True, null=True,
        help_text='The specified seed value for the random number generator.', )
    def __str__(self):
        return "Scenario: %s" % (self.description, )


class OutputSettings(InputSingleton):
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
        footer = "  Please rename the Production Type before proceeding."
        if re.search(r'[,\'"\\]', self.name):
            raise ValidationError(self.name + " CSV special characters not allowed." + footer)
        if self.name.lower() in sqlite_keywords + 'All Ind Dir Air'.lower().split():
            print("Conflicts:", [w for w in sqlite_keywords if w in self.name])
            raise ValidationError(self.name + " Sqlite keywords not allowed." + footer)
        if re.search(r'[^\w\d\- \\/_\(\)]', self.name):  # negative set, list of allowed characters should exclude unicode characters
            raise ValidationError("Special characters are not allowed: " + self.name)
        # if re.match(r'[0-9]', self.name[0]):
        #     raise ValidationError(self.name + " cannot start with a number.")
        if self.name in [z for z in Zone.objects.all().values_list('name', flat=True)]:  # forbid zone names
            raise ValidationError("You really shouldn't have matching Zone and Production Type names.  It makes the output confusing." + footer)

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
    radius = FloatField(validators=[MinValueValidator(0.0)],
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
    zone_detection_multiplier = FloatField(validators=[MinValueValidator(0.0)], default=1.0,
        help_text='Multiplier for the probability of observing '+wiki("clinical signs", "clinically-infectious")+' in units of this ' +
                  wiki("production type") + ' in this '+wiki("Zone")+'.', )
    cost_of_surveillance_per_animal_day = MoneyField(default=0.0,
        help_text='Cost of surveillance per animal per day in this '+wiki("Zone")+'.', )

    def __str__(self):
        return self.name


class ZoneEffectAssignmentManager(models.Manager):
    def ensure_all_zones_and_production_types(self):
        zones = Zone.objects.all()
        production_types = ProductionType.objects.all()
        zone_effect_assignments = [(z.zone, z.production_type) for z in self.all()]

        for zone in zones:
            for production_type in production_types:
                if not (zone, production_type) in zone_effect_assignments:
                    self.create(zone=zone, production_type=production_type)

        return self.get_queryset()


class ZoneEffectAssignment(BaseModel):
    zone = models.ForeignKey(Zone,
        help_text=''+wiki("Zone")+' for which this event occurred.', )
    production_type = models.ForeignKey('ProductionType',
        help_text='The ' + wiki("production type") + ' that these outputs apply to.', )
    effect = models.ForeignKey(ZoneEffect, blank=True, null=True,
        help_text='Describes what effect this '+wiki("Zone")+' has on this ' + wiki("production type") + '.')

    objects = ZoneEffectAssignmentManager()

    def __str__(self):
        return "%s Zone -> %s = %s" % (self.zone.name, self.production_type, self.effect.name if self.effect else "None")


class ProductionGroup(BaseModel):
    name = models.CharField(max_length=255, )
    group = models.ManyToManyField(ProductionType, )
    def __str__(self):
        return self.name


class VaccinationTrigger(BaseModel):
    restart_only = models.BooleanField(default=False, help_text="Allows you to setup less strict criteria for restarting a vaccination program after an outbreak.")
    class Meta(object):
        abstract = True


class FilteredVaccinationTrigger(VaccinationTrigger):
    trigger_group = models.ManyToManyField(ProductionType, )
    class Meta(object):
        abstract = True


class DiseaseDetection(FilteredVaccinationTrigger):
    number_of_units = models.PositiveIntegerField()
    def __str__(self):
        bold_values = tuple(bold(str(x)) for x in [self.number_of_units, ', '.join(pt.name for pt in self.trigger_group.all())])
        s = format_html("{0} infected units detected in {1}", *bold_values)
        return s


class RateOfNewDetections(FilteredVaccinationTrigger):
    number_of_units = models.PositiveIntegerField(help_text='The threshold is specified by a number of units and a number of days, for example, "3 or more units detected within 5 days."')
    days = models.PositiveIntegerField()
    def __str__(self):
        bold_values = tuple(bold(str(x)) for x in [self.number_of_units, self.days, ', '.join(pt.name for pt in self.trigger_group.all())])
        return format_html('{0} infected units within {1} days, detected in {2}', *bold_values)


class DisseminationRate(FilteredVaccinationTrigger):
    ratio = FloatField(help_text='The threshold is specified by a number of days and a ratio, for example, "initiate a vaccination program if the number of units detected in the last 5 days is 1.5x or more than the number of units detected in the 5 days before that."')
    days = models.PositiveIntegerField(help_text='Moving window size for calculating growth ratio.')
    def __str__(self):
        bold_values = tuple(bold(str(x)) for x in [self.ratio, self.days, ', '.join(pt.name for pt in self.trigger_group.all())])
        return format_html("Rate of spread has grown by more than {0}x in the past {1} day period for units in {2}", *bold_values)


class TimeFromFirstDetection(FilteredVaccinationTrigger):
    days = models.PositiveIntegerField(help_text='The number of days to elapsed since the first detection')
    def __str__(self):
        bold_values = tuple(bold(str(x)) for x in [self.days, ', '.join(pt.name for pt in self.trigger_group.all())])
        return format_html("{0} days elapsed since First Detection in {1}", *bold_values)
    
    
class DestructionWaitTime(FilteredVaccinationTrigger):
    days = models.PositiveIntegerField(help_text='Maximum number of days an infected premise should have to wait until destroyed.  The intention of this trigger is to initiate a vaccination program when destruction resources appear to be overwhelmed.')
    def __str__(self):
        bold_values = tuple(bold(str(x)) for x in [self.days, ', '.join(pt.name for pt in self.trigger_group.all())])
        return format_html("{0} days spent waiting in the Destruction Queue for units in {1}", *bold_values)


class SpreadBetweenGroups(VaccinationTrigger):  # doesn't need trigger_group so it doesn't inherit FilteredVaccinationTrigger
    number_of_groups = models.PositiveIntegerField(help_text="Specify in how many groups disease must be detected to trigger a vaccination program")
    relevant_groups = models.ManyToManyField(ProductionGroup, )
    def __str__(self):
        bold_values = tuple(bold(str(x)) for x in [self.number_of_groups, ', '.join(group.name for group in self.relevant_groups.all())])
        return format_html("{0} groups infected between {1}", *bold_values)


class StopVaccination(FilteredVaccinationTrigger, InputSingleton):
    number_of_units = models.PositiveIntegerField(
        help_text='The threshold is specified by a number of units and a number of days. For example, "no more than 3 units detected within 5 days."')
    days = models.PositiveIntegerField()
    def __str__(self):
        bold_values = tuple(bold(str(x)) for x in [self.number_of_units, self.days, ', '.join(pt.name for pt in self.trigger_group.all())])
        return format_html('{1} days with no more than {0} detections, in {2}', *bold_values)

    
class VaccinationRingRule(BaseModel):
    trigger_group = models.ManyToManyField(ProductionType, related_name="triggers_vaccination_ring")
    outer_radius = FloatField(validators=[MinValueValidator(0.001), ], )
    inner_radius = FloatField(blank=True, null=True, validators=[MinValueValidator(0.001), ],)  # optional, can be null
    target_group = models.ManyToManyField(ProductionType, related_name="targeted_by_vaccination_ring")

    def clean_fields(self, exclude=None):
        """Swap fields if their values are backwards"""
        if self.inner_radius is not None and self.inner_radius > self.outer_radius:
            temp = self.outer_radius
            self.outer_radius = self.inner_radius
            self.inner_radius = temp

    def __str__(self):
        bold_values = tuple(bold(str(x)) for x in [', '.join(pt.name for pt in self.trigger_group.all()),
                                                   ', '.join(pt.name for pt in self.target_group.all()),
                                                    self.outer_radius,])
        if self.inner_radius:
            inner = bold(str(self.inner_radius))
            return format_html('When a Unit of {1} is detected vaccinate {2} Units between {0} km to {3} km', inner, *bold_values)
        else:
            return format_html('When a Unit of {0} is detected vaccinate {1} Units within {2} km', *bold_values)



