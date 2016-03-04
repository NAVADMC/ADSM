# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ScenarioCreator.models


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0013_restart_only_triggers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disease',
            name='use_airborne_exponential_decay',
            field=models.BooleanField(help_text='Indicates if the decrease in probability by <a href="https://github.com/NAVADMC/ADSM/wiki/Model-Specification#airborne-spread" class="wiki">airborne transmission</a> is simulated by the exponential (TRUE) or linear (FALSE) algorithm.', default=False),
        ),
        migrations.AlterField(
            model_name='disease',
            name='use_within_unit_prevalence',
            field=models.BooleanField(help_text='Indicates if <a href="https://github.com/NAVADMC/ADSM/wiki/Model-Specification#prevalence" class="wiki">within unit prevalence</a> should be used in the model.', default=False),
        ),
        migrations.AlterField(
            model_name='diseaseprogression',
            name='disease_clinical_period',
            field=models.ForeignKey(to='ScenarioCreator.ProbabilityFunction', verbose_name='Clinical period', help_text='Defines the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#clinically-infectious" class="wiki">clinical</a> period for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki">production type</a>.', related_name='+'),
        ),
        migrations.AlterField(
            model_name='diseaseprogression',
            name='disease_immune_period',
            field=models.ForeignKey(to='ScenarioCreator.ProbabilityFunction', verbose_name='Immune period', help_text='Defines the natural <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#immune" class="wiki">immune</a> period for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki">production type</a>.', related_name='+'),
        ),
        migrations.AlterField(
            model_name='diseaseprogression',
            name='disease_latent_period',
            field=models.ForeignKey(to='ScenarioCreator.ProbabilityFunction', verbose_name='Latent period', help_text='Defines the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#latent-state" class="wiki">latent period</a> for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki">production type</a>.', related_name='+'),
        ),
        migrations.AlterField(
            model_name='diseaseprogression',
            name='disease_prevalence',
            field=models.ForeignKey(verbose_name='Prevalence', help_text='Defines the prevalance for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki">production type</a>.', to='ScenarioCreator.RelationalFunction', blank=True, related_name='+', null=True),
        ),
        migrations.AlterField(
            model_name='diseaseprogression',
            name='disease_subclinical_period',
            field=models.ForeignKey(to='ScenarioCreator.ProbabilityFunction', verbose_name='Subclinical period', help_text='Defines the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#subclinically-infectious" class="wiki">Subclinical</a> period for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki">production type</a>.', related_name='+'),
        ),
        migrations.AlterField(
            model_name='disseminationrate',
            name='ratio',
            field=ScenarioCreator.models.FloatField(help_text='The threshold is specified by a number of days and a ratio, for example, "initiate a vaccination program if the number of units detected in the last 5 days is 1.5x or more than the number of units detected in the 5 days before that."'),
        ),
    ]
