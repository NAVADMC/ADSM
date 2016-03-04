# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django_extras.db.models.fields
import ScenarioCreator.models
import ScenarioCreator.custom_fields


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0014_auto_20150918_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airbornespread',
            name='exposure_direction_end',
            field=models.PositiveIntegerField(help_text='The end angle in degrees of the area at risk of <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#airborne-transmission" class="wiki" target="_blank">airborne spread</a>.  0 is North.', default=360, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(360)]),
        ),
        migrations.AlterField(
            model_name='airbornespread',
            name='exposure_direction_start',
            field=models.PositiveIntegerField(help_text='The start angle in degrees of the area at risk of <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#airborne-transmission" class="wiki" target="_blank">airborne spread</a>.  0 is North.', default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(360)]),
        ),
        migrations.AlterField(
            model_name='airbornespread',
            name='max_distance',
            field=ScenarioCreator.models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1.1)], help_text='The maximum distance in KM of <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#airborne-transmission" class="wiki" target="_blank">airborne spread</a>.  Only used in Linear Airborne Decay.'),
        ),
        migrations.AlterField(
            model_name='controlmasterplan',
            name='disable_all_controls',
            field=models.BooleanField(help_text='Disable all <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#control-measures" class="wiki" target="_blank">Control activities</a> for this simulation run.  Normally used temporarily to test uncontrolled disease spread.', default=False),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='days_to_immunity',
            field=models.PositiveIntegerField(blank=True, null=True, help_text='The number of days required for the onset of <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#vaccine-immune" class="wiki" target="_blank">vaccine immunity</a> in a newly vaccinated unit of this type.'),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='destroy_direct_back_traces',
            field=models.BooleanField(help_text='Indicates if units of this type identified by <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#trace-back" class="wiki" target="_blank">trace back</a> of <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki" target="_blank">direct contact</a>s will be subject to preemptive destruction.', default=False),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='destroy_direct_forward_traces',
            field=models.BooleanField(help_text='Indicates if units of this type identified by <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#trace-forward" class="wiki" target="_blank">trace forward</a> of <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki" target="_blank">direct contact</a>s will be subject to preemptive destruction.', default=False),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='destroy_indirect_back_traces',
            field=models.BooleanField(help_text='Indicates if units of this type identified by <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#trace-back" class="wiki" target="_blank">trace back</a> of <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki" target="_blank">indirect contact</a>s will be subject to preemptive destruction.', default=False),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='destroy_indirect_forward_traces',
            field=models.BooleanField(help_text='Indicates if units of this type identified by <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#trace-forward" class="wiki" target="_blank">trace forward</a> of <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki" target="_blank">indirect contact</a>s will be subject to preemptive destruction.', default=False),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='destruction_is_a_ring_target',
            field=models.BooleanField(help_text='Indicates if unit of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a> will be subject to preemptive ring destruction.', default=False),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='destruction_is_a_ring_trigger',
            field=models.BooleanField(help_text='Indicates if detection of a unit of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a> will trigger the formation of a destruction ring.', default=False),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='destruction_priority',
            field=models.PositiveIntegerField(blank=True, null=True, help_text='The destruction priority of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a> relative to other production types.  A lower number indicates a higher priority.', default=5),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='detection_is_a_zone_trigger',
            field=models.BooleanField(help_text='Indicator if detection of infected units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a> will trigger a <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#zone" class="wiki" target="_blank">Zone</a> focus.', default=False),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='detection_probability_for_observed_time_in_clinical',
            field=models.ForeignKey(to='ScenarioCreator.RelationalFunction', related_name='+', blank=True, null=True, help_text='Relational function used to define the probability of observing <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#clinically-infectious" class="wiki" target="_blank">clinical signs</a> in units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a>.'),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='detection_probability_report_vs_first_detection',
            field=models.ForeignKey(to='ScenarioCreator.RelationalFunction', related_name='+', blank=True, null=True, help_text='Relational function used to define the probability of reporting <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#clinically-infectious" class="wiki" target="_blank">clinical signs</a> in units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a>.'),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='direct_trace_is_a_zone_trigger',
            field=models.BooleanField(help_text='Indicator if direct tracing of infected units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a> will trigger a <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#zone" class="wiki" target="_blank">Zone</a> focus.', default=False),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='direct_trace_period',
            field=models.PositiveIntegerField(blank=True, null=True, help_text='Days before detection (critical period) for tracing of <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki" target="_blank">direct contact</a>s.'),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='direct_trace_success_rate',
            field=ScenarioCreator.custom_fields.PercentField(blank=True, null=True, help_text='Probability of success of trace for <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki" target="_blank">direct contact</a>.'),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='exam_direct_back_success_multiplier',
            field=ScenarioCreator.models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0)], help_text='Multiplier for the probability of observing <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#clinically-infectious" class="wiki" target="_blank">clinical signs</a> in units identified by the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#trace-back" class="wiki" target="_blank">trace back</a> of <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki" target="_blank">direct contact</a>.'),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='exam_direct_forward_success_multiplier',
            field=ScenarioCreator.models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0)], help_text='Multiplier for the probability of observing <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#clinically-infectious" class="wiki" target="_blank">clinical signs</a> in units identified by the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#trace-forward" class="wiki" target="_blank">trace forward</a> of <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki" target="_blank">direct contact</a>.'),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='exam_indirect_forward_success_multiplier',
            field=ScenarioCreator.models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0)], help_text='Multiplier for the probability of observing <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#clinically-infectious" class="wiki" target="_blank">clinical signs</a> in units identified by the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#trace-forward" class="wiki" target="_blank">trace forward</a> of <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki" target="_blank">indirect contact</a> .'),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='examine_direct_back_traces',
            field=models.BooleanField(help_text='Indicator if units identified by the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#trace-back" class="wiki" target="_blank">trace back</a> of <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki" target="_blank">direct contact</a> will be examined for <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#clinically-infectious" class="wiki" target="_blank">clinical signs</a> of disease.', default=False),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='examine_direct_forward_traces',
            field=models.BooleanField(help_text='Indicator if units identified by the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#trace-forward" class="wiki" target="_blank">trace forward</a> of <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki" target="_blank">direct contact</a> will be examined for <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#clinically-infectious" class="wiki" target="_blank">clinical signs</a> of disease.', default=False),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='examine_indirect_back_success_multiplier',
            field=ScenarioCreator.models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0)], help_text='Multiplier for the probability of observing <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#clinically-infectious" class="wiki" target="_blank">clinical signs</a> in units identified by the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#trace-back" class="wiki" target="_blank">trace back</a> of <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki" target="_blank">indirect contact</a>.'),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='examine_indirect_back_traces',
            field=models.BooleanField(help_text='Indicator if units identified by the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#trace-back" class="wiki" target="_blank">trace back</a> of <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki" target="_blank">indirect contact</a> will be examined for <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#clinically-infectious" class="wiki" target="_blank">clinical signs</a> of disease.', default=False),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='examine_indirect_forward_traces',
            field=models.BooleanField(help_text='Indicator if units identified by the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#trace-forward" class="wiki" target="_blank">trace forward</a> of <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki" target="_blank">indirect contact</a> will be examined for <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#clinically-infectious" class="wiki" target="_blank">clinical signs</a> of disease.', default=False),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='indirect_trace_is_a_zone_trigger',
            field=models.BooleanField(help_text='Indicator if indirect tracing of infected units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a> will trigger a <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#zone" class="wiki" target="_blank">Zone</a> focus.', default=False),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='indirect_trace_period',
            field=models.PositiveIntegerField(blank=True, null=True, help_text='Days before detection  (critical period) for tracing of <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki" target="_blank">indirect contact</a>s.'),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='indirect_trace_success',
            field=ScenarioCreator.custom_fields.PercentField(blank=True, null=True, help_text='Probability of success of trace for <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki" target="_blank">indirect contact</a>.'),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='minimum_time_between_vaccinations',
            field=models.PositiveIntegerField(blank=True, null=True, help_text='The minimum time in days between vaccination for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a>.'),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='test_direct_back_traces',
            field=models.BooleanField(help_text='Indicator that diagnostic testing should be performed on units identified by <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#trace-back" class="wiki" target="_blank">trace back</a> of <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki" target="_blank">direct contact</a>s.', default=False),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='test_direct_forward_traces',
            field=models.BooleanField(help_text='Indicator that diagnostic testing should be performed on units identified by <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#trace-forward" class="wiki" target="_blank">trace forward</a> of <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki" target="_blank">direct contact</a>s.', default=False),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='test_indirect_back_traces',
            field=models.BooleanField(help_text='Indicator that diagnostic testing should be performed on units identified by <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#trace-back" class="wiki" target="_blank">trace back</a> of <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki" target="_blank">indirect contact</a>s.', default=False),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='test_indirect_forward_traces',
            field=models.BooleanField(help_text='Indicator that diagnostic testing should be performed on units identified by <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#trace-forward" class="wiki" target="_blank">trace forward</a> of <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki" target="_blank">indirect contact</a>s.', default=False),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='test_sensitivity',
            field=ScenarioCreator.models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0)], help_text='<a href="http://en.wikipedia.org/wiki/Sensitivity_and_specificity" class="wiki" target="_blank">Test Sensitivity</a> for units of this production type'),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='test_specificity',
            field=ScenarioCreator.models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0)], help_text='<a href="http://en.wikipedia.org/wiki/Sensitivity_and_specificity" class="wiki" target="_blank">Test Specificity</a> for units of this production type'),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='trace_direct_back',
            field=models.BooleanField(help_text='Indicator that <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#trace-back" class="wiki" target="_blank">trace back</a> will be conducted for <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki" target="_blank">direct contact</a>s where the reported unit was the source of contact and was of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a>.', default=False),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='trace_direct_forward',
            field=models.BooleanField(help_text='Indicator that <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#trace-forward" class="wiki" target="_blank">trace forward</a> will be conducted for <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki" target="_blank">direct contact</a>s where the reported unit was the source of contact and was of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a>.', default=False),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='trace_indirect_back',
            field=models.BooleanField(help_text='Indicator that <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#trace-back" class="wiki" target="_blank">trace back</a> will be conducted for <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki" target="_blank">indirect contact</a>s where the reported unit was the source of contact and was of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a>.', default=False),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='trace_indirect_forward',
            field=models.BooleanField(help_text='Indicator that <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#trace-forward" class="wiki" target="_blank">trace forward</a> will be conducted for <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki" target="_blank">indirect contact</a>s where the reported unit was the source of contact and was of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a>.', default=False),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='use_destruction',
            field=models.BooleanField(help_text='Indicates if detected units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a> will be destroyed.', default=False),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='use_detection',
            field=models.BooleanField(help_text='Indicates if disease detection will be modeled for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a>.', default=True),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='use_vaccination',
            field=models.BooleanField(help_text='Indicates if units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a> will be subject to vaccination.', default=False),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='vaccinate_detected_units',
            field=models.BooleanField(help_text='Indicates if detection in units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a> will trigger vaccination.', default=False),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='vaccine_immune_period',
            field=models.ForeignKey(to='ScenarioCreator.ProbabilityFunction', related_name='+', blank=True, null=True, help_text='Defines the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#vaccine-immune" class="wiki" target="_blank">vaccine immune</a> period for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a>.'),
        ),
        migrations.AlterField(
            model_name='directspread',
            name='contact_rate',
            field=ScenarioCreator.models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)], help_text='<div class="help-block" data-visibility-controller="use_fixed_contact_rate" data-disabled-value="false">\n                                    Fixed baseline contact rate (in outgoing contacts/unit/day).</div>\n                                <div class="help-block" data-visibility-controller="use_fixed_contact_rate" data-disabled-value="true">\n                                    Mean baseline contact rate (in outgoing contacts/unit/day).</div>'),
        ),
        migrations.AlterField(
            model_name='directspread',
            name='distance_distribution',
            field=models.ForeignKey(to='ScenarioCreator.ProbabilityFunction', related_name='+', help_text='Defines the shipment distances for <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki" target="_blank">direct</a> or <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki" target="_blank">indirect contact</a> models.'),
        ),
        migrations.AlterField(
            model_name='directspread',
            name='infection_probability',
            field=ScenarioCreator.custom_fields.PercentField(blank=True, null=True, help_text='The probability that a <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#effective-contact" class="wiki" target="_blank">contact will result in disease transmission</a>. Specified for <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki" target="_blank">direct</a> or <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki" target="_blank">indirect contact</a> models.'),
        ),
        migrations.AlterField(
            model_name='directspread',
            name='latent_animals_can_infect_others',
            field=models.BooleanField(help_text='Indicates if <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#latent-state" class="wiki" target="_blank">latent</a> units of the source type can spread disease.', default=False),
        ),
        migrations.AlterField(
            model_name='directspread',
            name='movement_control',
            field=models.ForeignKey(to='ScenarioCreator.RelationalFunction', related_name='+', help_text='<a href="https://github.com/NAVADMC/ADSM/wiki/Relational-functions" class="wiki" target="_blank">Relational function</a> used to define movement control effects for the indicated <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production types</a> combinations.'),
        ),
        migrations.AlterField(
            model_name='directspread',
            name='subclinical_animals_can_infect_others',
            field=models.BooleanField(help_text='Indicates if <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#subclinically-infectious" class="wiki" target="_blank">Subclinical</a> units of the source type can spread disease. ', default=False),
        ),
        migrations.AlterField(
            model_name='disease',
            name='include_direct_contact_spread',
            field=models.BooleanField(help_text='Indicates if disease spread by <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki" target="_blank">direct contact</a> is used in the scenario.', default=True),
        ),
        migrations.AlterField(
            model_name='disease',
            name='include_indirect_contact_spread',
            field=models.BooleanField(help_text='Indicates if disease spread by <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki" target="_blank">indirect contact</a> is used in the scenario.', default=True),
        ),
        migrations.AlterField(
            model_name='disease',
            name='use_airborne_exponential_decay',
            field=models.BooleanField(help_text='Indicates if the decrease in probability by <a href="https://github.com/NAVADMC/ADSM/wiki/Model-Specification#airborne-spread" class="wiki" target="_blank">airborne transmission</a> is simulated by the exponential or linear algorithm.', default=False),
        ),
        migrations.AlterField(
            model_name='disease',
            name='use_within_unit_prevalence',
            field=models.BooleanField(help_text='Indicates if <a href="https://github.com/NAVADMC/ADSM/wiki/Model-Specification#prevalence" class="wiki" target="_blank">within unit prevalence</a> should be used in the model.', default=False),
        ),
        migrations.AlterField(
            model_name='diseaseprogression',
            name='disease_clinical_period',
            field=models.ForeignKey(help_text='Defines the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#clinically-infectious" class="wiki" target="_blank">clinical</a> period for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a>.', related_name='+', verbose_name='Clinical period', to='ScenarioCreator.ProbabilityFunction'),
        ),
        migrations.AlterField(
            model_name='diseaseprogression',
            name='disease_immune_period',
            field=models.ForeignKey(help_text='Defines the natural <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#immune" class="wiki" target="_blank">immune</a> period for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a>.', related_name='+', verbose_name='Immune period', to='ScenarioCreator.ProbabilityFunction'),
        ),
        migrations.AlterField(
            model_name='diseaseprogression',
            name='disease_latent_period',
            field=models.ForeignKey(help_text='Defines the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#latent-state" class="wiki" target="_blank">latent period</a> for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a>.', related_name='+', verbose_name='Latent period', to='ScenarioCreator.ProbabilityFunction'),
        ),
        migrations.AlterField(
            model_name='diseaseprogression',
            name='disease_prevalence',
            field=models.ForeignKey(help_text='Defines the prevalance for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a>.', related_name='+', blank=True, null=True, verbose_name='Prevalence', to='ScenarioCreator.RelationalFunction'),
        ),
        migrations.AlterField(
            model_name='diseaseprogression',
            name='disease_subclinical_period',
            field=models.ForeignKey(help_text='Defines the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#subclinically-infectious" class="wiki" target="_blank">Subclinical</a> period for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a>.', related_name='+', verbose_name='Subclinical period', to='ScenarioCreator.ProbabilityFunction'),
        ),
        migrations.AlterField(
            model_name='diseaseprogressionassignment',
            name='production_type',
            field=models.ForeignKey(to='ScenarioCreator.ProductionType', help_text='The <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a> that these outputs apply to.', unique=True),
        ),
        migrations.AlterField(
            model_name='diseasespreadassignment',
            name='airborne_spread',
            field=models.ForeignKey(to='ScenarioCreator.AirborneSpread', related_name='airborne_spread_pair', blank=True, null=True, help_text='Disease spread mechanism used to model spread by <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#airborne-transmission" class="wiki" target="_blank">airborne spread</a> between these types.'),
        ),
        migrations.AlterField(
            model_name='diseasespreadassignment',
            name='destination_production_type',
            field=models.ForeignKey(to='ScenarioCreator.ProductionType', related_name='used_as_destinations', help_text='The <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a> that will be the recipient type for this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a> combination.'),
        ),
        migrations.AlterField(
            model_name='diseasespreadassignment',
            name='direct_contact_spread',
            field=models.ForeignKey(to='ScenarioCreator.DirectSpread', related_name='direct_spread_pair', blank=True, null=True, help_text='Disease spread mechanism used to model spread by <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki" target="_blank">direct contact</a> between these types.'),
        ),
        migrations.AlterField(
            model_name='diseasespreadassignment',
            name='indirect_contact_spread',
            field=models.ForeignKey(to='ScenarioCreator.IndirectSpread', related_name='indirect_spread_pair', blank=True, null=True, help_text='Disease spread mechanism used to model spread by <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki" target="_blank">indirect contact</a> between these types.'),
        ),
        migrations.AlterField(
            model_name='diseasespreadassignment',
            name='source_production_type',
            field=models.ForeignKey(to='ScenarioCreator.ProductionType', related_name='used_as_sources', help_text='The <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a> that will be the source type for this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a> combination.'),
        ),
        migrations.AlterField(
            model_name='indirectspread',
            name='contact_rate',
            field=ScenarioCreator.models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)], help_text='<div class="help-block" data-visibility-controller="use_fixed_contact_rate" data-disabled-value="false">\n                                    Fixed baseline contact rate (in outgoing contacts/unit/day).</div>\n                                <div class="help-block" data-visibility-controller="use_fixed_contact_rate" data-disabled-value="true">\n                                    Mean baseline contact rate (in outgoing contacts/unit/day).</div>'),
        ),
        migrations.AlterField(
            model_name='indirectspread',
            name='distance_distribution',
            field=models.ForeignKey(to='ScenarioCreator.ProbabilityFunction', related_name='+', help_text='Defines the shipment distances for <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki" target="_blank">direct</a> or <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki" target="_blank">indirect contact</a> models.'),
        ),
        migrations.AlterField(
            model_name='indirectspread',
            name='infection_probability',
            field=ScenarioCreator.custom_fields.PercentField(help_text='The probability that a contact will result in disease transmission.'),
        ),
        migrations.AlterField(
            model_name='indirectspread',
            name='movement_control',
            field=models.ForeignKey(to='ScenarioCreator.RelationalFunction', related_name='+', help_text='<a href="https://github.com/NAVADMC/ADSM/wiki/Relational-functions" class="wiki" target="_blank">Relational function</a> used to define movement control effects for the indicated <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production types</a> combinations.'),
        ),
        migrations.AlterField(
            model_name='indirectspread',
            name='subclinical_animals_can_infect_others',
            field=models.BooleanField(help_text='Indicates if <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#subclinically-infectious" class="wiki" target="_blank">Subclinical</a> units of the source type can spread disease. ', default=False),
        ),
        migrations.AlterField(
            model_name='outputsettings',
            name='cost_track_zone_surveillance',
            field=models.BooleanField(help_text='Disable this to ignore entered <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#zone" class="wiki" target="_blank">Zone</a> surveillance costs.', default=True),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='description',
            field=models.TextField(blank=True, help_text='The description of the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#scenario" class="wiki" target="_blank">scenario</a>.'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='days_in_initial_state',
            field=models.IntegerField(blank=True, null=True, help_text='The number of days that the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#unit" class="wiki" target="_blank">Unit</a> will remain in its initial state unless preempted by other events.'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='initial_size',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], help_text='The number of animals in the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#unit" class="wiki" target="_blank">Unit</a>.'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='initial_state',
            field=models.CharField(max_length=1, choices=[('S', 'Susceptible'), ('L', 'Latent'), ('B', 'Infectious Subclinical'), ('C', 'Infectious Clinical'), ('N', 'Naturally Immune'), ('V', 'Vaccine Immune'), ('D', 'Destroyed')], help_text='Code indicating the actual disease state of the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#unit" class="wiki" target="_blank">Unit</a> at the beginning of the simulation.', default='S'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='latitude',
            field=django_extras.db.models.fields.LatitudeField(validators=[django.core.validators.MinValueValidator(-90.0), django.core.validators.MaxValueValidator(90.0)], help_text='The latitude used to georeference this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#unit" class="wiki" target="_blank">Unit</a>.'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='longitude',
            field=django_extras.db.models.fields.LongitudeField(validators=[django.core.validators.MinValueValidator(-180.0), django.core.validators.MaxValueValidator(180.0)], help_text='The longitude used to georeference this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#unit" class="wiki" target="_blank">Unit</a>.'),
        ),
        migrations.AlterField(
            model_name='zone',
            name='name',
            field=models.TextField(help_text='Description of the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#zone" class="wiki" target="_blank">Zone</a>'),
        ),
        migrations.AlterField(
            model_name='zone',
            name='radius',
            field=ScenarioCreator.models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)], help_text='Radius in kilometers of the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#zone" class="wiki" target="_blank">Zone</a>'),
        ),
        migrations.AlterField(
            model_name='zoneeffect',
            name='cost_of_surveillance_per_animal_day',
            field=django_extras.db.models.fields.MoneyField(decimal_places=4, max_digits=20, help_text='Cost of surveillance per animal per day in this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#zone" class="wiki" target="_blank">Zone</a>.', default=0.0),
        ),
        migrations.AlterField(
            model_name='zoneeffect',
            name='zone_detection_multiplier',
            field=ScenarioCreator.models.FloatField(help_text='Multiplier for the probability of observing <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#clinically-infectious" class="wiki" target="_blank">clinical signs</a> in units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a> in this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#zone" class="wiki" target="_blank">Zone</a>.', default=1.0, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='zoneeffectassignment',
            name='effect',
            field=models.ForeignKey(to='ScenarioCreator.ZoneEffect', blank=True, null=True, help_text='Describes what effect this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#zone" class="wiki" target="_blank">Zone</a> has on this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a>.'),
        ),
        migrations.AlterField(
            model_name='zoneeffectassignment',
            name='production_type',
            field=models.ForeignKey(help_text='The <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a> that these outputs apply to.', to='ScenarioCreator.ProductionType'),
        ),
        migrations.AlterField(
            model_name='zoneeffectassignment',
            name='zone',
            field=models.ForeignKey(help_text='<a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#zone" class="wiki" target="_blank">Zone</a> for which this event occurred.', to='ScenarioCreator.Zone'),
        ),
    ]
