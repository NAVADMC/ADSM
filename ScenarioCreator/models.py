from django.db import models

from django.db.models.fields.related import ForeignKey


class Scenario(models.Model):
    scenario_name = models.CharField(max_length=255, default='sample')
    description = models.CharField(max_length=255, default='Scenario Description', null=True, blank=True)
    naadsm_version = models.CharField(max_length=255, default='3.2.19')
    language = models.CharField(max_length=255, default='en', choices=(('en', "English"),('es', "Espanol")))
    num_runs = models.IntegerField(default=10)
    num_days = models.IntegerField(default=40)
    # output = ForeignKey(Output, null=True, blank=True) ForeignKey points back here


class Output(models.Model):
    #<element name="variable-name">
    variable_name = models.CharField(max_length=255,
         choices=[(x,x) for x in ("all_units_states","num_units_in_each_state","num_units_in_each_state_by_production_type",
                                  "num_animals_in_each_state","num_animals_in_each_state_by_production_type","diseaseDuration",
                                  "outbreakDuration","clock_time","tsdU","tsdA")])
    #<element name="frequency" type="naadsm:output-variable-frequency" />
    frequency = models.IntegerField(default=1)
    scenario = ForeignKey('Scenario', related_name='output')


class OutputSpecification(models.Model):
    #TODO not sure where this is used
    #TODO double check types on these fields
    #<element name="variable-name">
    # = models.CharField(max_length=255, null=True, blank=True)
    all_units_states = models.CharField(max_length=255, null=True, blank=True)
    num_units_in_each_state = models.IntegerField(default=0)
    num_units_in_each_state_by_production_type = models.IntegerField(default=0)
    num_animals_in_each_state = models.IntegerField(default=0)
    num_animals_in_each_state_by_production_type = models.IntegerField(default=0)
    diseaseDuration = models.IntegerField(default=0)
    outbreakDuration = models.IntegerField(default=0)
    clock_time = models.TimeField(null=True, blank=True)
    tsdU = models.IntegerField(default=0)
    tsdA = models.IntegerField(default=0)
    #<element name="frequency" type="naadsm:output-variable-frequency" />


class airborne_spread_model_type(models.Model):

    pass


class airborne_spread_exponential_model_type(airborne_spread_model_type):
    pass