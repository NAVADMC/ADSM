# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0021_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='controlprotocol',
            name='use_vaccination',
            field=models.BooleanField(default=False, help_text='Indicates if units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a> will be subject to vaccination.'),
        ),
        migrations.AlterField(
            model_name='disease',
            name='use_airborne_exponential_decay',
            field=models.BooleanField(default=False, help_text='Indicates if the decrease in probability by <a href="https://github.com/NAVADMC/ADSM/wiki/Model-Specification#airborne-spread" class="wiki" target="_blank">airborne transmission</a> is simulated by the exponential or linear algorithm.'),
        ),
        migrations.AlterField(
            model_name='disease',
            name='use_within_unit_prevalence',
            field=models.BooleanField(default=False, help_text='Indicates if <a href="https://github.com/NAVADMC/ADSM/wiki/Model-Specification#prevalence" class="wiki" target="_blank">within unit prevalence</a> should be used in the model.'),
        ),
        migrations.AlterField(
            model_name='diseaseprogression',
            name='disease_clinical_period',
            field=models.ForeignKey(help_text='Defines the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#clinically-infectious" class="wiki" target="_blank">clinical</a> period for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a>.', verbose_name='Clinical period', to='ScenarioCreator.ProbabilityFunction', related_name='+'),
        ),
        migrations.AlterField(
            model_name='diseaseprogression',
            name='disease_immune_period',
            field=models.ForeignKey(help_text='Defines the natural <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#immune" class="wiki" target="_blank">immune</a> period for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a>.', verbose_name='Immune period', to='ScenarioCreator.ProbabilityFunction', related_name='+'),
        ),
        migrations.AlterField(
            model_name='diseaseprogression',
            name='disease_latent_period',
            field=models.ForeignKey(help_text='Defines the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#latent-state" class="wiki" target="_blank">latent period</a> for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a>.', verbose_name='Latent period', to='ScenarioCreator.ProbabilityFunction', related_name='+'),
        ),
        migrations.AlterField(
            model_name='diseaseprogression',
            name='disease_prevalence',
            field=models.ForeignKey(blank=True, help_text='Defines the prevalance for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a>.', verbose_name='Prevalence', to='ScenarioCreator.RelationalFunction', related_name='+', null=True),
        ),
        migrations.AlterField(
            model_name='diseaseprogression',
            name='disease_subclinical_period',
            field=models.ForeignKey(help_text='Defines the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#subclinically-infectious" class="wiki" target="_blank">Subclinical</a> period for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a>.', verbose_name='Subclinical period', to='ScenarioCreator.ProbabilityFunction', related_name='+'),
        ),
        migrations.AlterField(
            model_name='diseaseprogressionassignment',
            name='production_type',
            field=models.OneToOneField(help_text='The <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a> that these outputs apply to.', to='ScenarioCreator.ProductionType'),
        ),
    ]
