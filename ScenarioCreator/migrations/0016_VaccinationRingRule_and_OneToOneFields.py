# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ScenarioCreator.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0015_auto_20151204_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='VaccinationRingRule',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('outer_radius', ScenarioCreator.models.FloatField(validators=[django.core.validators.MinValueValidator(0.001)])),
                ('inner_radius', ScenarioCreator.models.FloatField(blank=True, validators=[django.core.validators.MinValueValidator(0.001)], null=True)),
                ('target_group', models.ManyToManyField(to='ScenarioCreator.ProductionType', related_name='targeted_by_vaccination_ring')),
                ('trigger_group', models.ManyToManyField(to='ScenarioCreator.ProductionType', related_name='triggers_vaccination_ring')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='disease',
            name='use_airborne_exponential_decay',
            field=models.BooleanField(default=False, help_text='Indicates if the decrease in probability by <a href="https://github.com/NAVADMC/ADSM/wiki/Model-Specification#airborne-spread" class="wiki">airborne transmission</a> is simulated by the exponential (TRUE) or linear (FALSE) algorithm.'),
        ),
        migrations.AlterField(
            model_name='disease',
            name='use_within_unit_prevalence',
            field=models.BooleanField(default=False, help_text='Indicates if <a href="https://github.com/NAVADMC/ADSM/wiki/Model-Specification#prevalence" class="wiki">within unit prevalence</a> should be used in the model.'),
        ),
        migrations.AlterField(
            model_name='diseaseprogression',
            name='disease_clinical_period',
            field=models.ForeignKey(help_text='Defines the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#clinically-infectious" class="wiki">clinical</a> period for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki">production type</a>.', related_name='+', to='ScenarioCreator.ProbabilityFunction', verbose_name='Clinical period'),
        ),
        migrations.AlterField(
            model_name='diseaseprogression',
            name='disease_immune_period',
            field=models.ForeignKey(help_text='Defines the natural <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#immune" class="wiki">immune</a> period for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki">production type</a>.', related_name='+', to='ScenarioCreator.ProbabilityFunction', verbose_name='Immune period'),
        ),
        migrations.AlterField(
            model_name='diseaseprogression',
            name='disease_latent_period',
            field=models.ForeignKey(help_text='Defines the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#latent-state" class="wiki">latent period</a> for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki">production type</a>.', related_name='+', to='ScenarioCreator.ProbabilityFunction', verbose_name='Latent period'),
        ),
        migrations.AlterField(
            model_name='diseaseprogression',
            name='disease_prevalence',
            field=models.ForeignKey(blank=True, help_text='Defines the prevalance for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki">production type</a>.', related_name='+', null=True, to='ScenarioCreator.RelationalFunction', verbose_name='Prevalence'),
        ),
        migrations.AlterField(
            model_name='diseaseprogression',
            name='disease_subclinical_period',
            field=models.ForeignKey(help_text='Defines the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#subclinically-infectious" class="wiki">Subclinical</a> period for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki">production type</a>.', related_name='+', to='ScenarioCreator.ProbabilityFunction', verbose_name='Subclinical period'),
        ),
        migrations.AlterField(
            model_name='diseaseprogressionassignment',
            name='production_type',
            field=models.OneToOneField(help_text='The <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki">production type</a> that these outputs apply to.', to='ScenarioCreator.ProductionType'),
        ),
        migrations.AlterField(
            model_name='disseminationrate',
            name='ratio',
            field=ScenarioCreator.models.FloatField(help_text='The threshold is specified by a number of days and a ratio, for example, "initiate a vaccination program if the number of units detected in the last 5 days is 1.5x or more than the number of units detected in the 5 days before that."'),
        ),
        migrations.AlterField(
            model_name='protocolassignment',
            name='production_type',
            field=models.OneToOneField(help_text='The production type that these outputs apply to.', to='ScenarioCreator.ProductionType'),
        ),
    ]
