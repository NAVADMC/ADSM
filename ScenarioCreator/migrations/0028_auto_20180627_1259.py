# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0027_auto_20180627_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airbornespread',
            name='transport_delay',
            field=models.ForeignKey(to='ScenarioCreator.ProbabilityDensityFunction', related_name='+', help_text='WARNING: THIS FIELD IS NOT RECOMMENDED BY ADSM and will be removed in later versions. Consider setting this to "-----".', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='test_delay',
            field=models.ForeignKey(to='ScenarioCreator.ProbabilityDensityFunction', related_name='+', help_text='Function that describes the delay in obtaining test results.', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='trace_result_delay',
            field=models.ForeignKey(to='ScenarioCreator.ProbabilityDensityFunction', related_name='+', help_text='Delay for carrying out trace investigation result (days).', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='vaccine_immune_period',
            field=models.ForeignKey(to='ScenarioCreator.ProbabilityDensityFunction', related_name='+', help_text='Defines the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#vaccine-immune" class="wiki" target="_blank">vaccine immune</a> period for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a>.', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='directspread',
            name='distance_distribution',
            field=models.ForeignKey(to='ScenarioCreator.ProbabilityDensityFunction', help_text='Defines the shipment distances for <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki" target="_blank">direct</a> or <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki" target="_blank">indirect contact</a> models.', related_name='+'),
        ),
        migrations.AlterField(
            model_name='directspread',
            name='transport_delay',
            field=models.ForeignKey(to='ScenarioCreator.ProbabilityDensityFunction', related_name='+', help_text='WARNING: THIS FIELD IS NOT RECOMMENDED BY ADSM and will be removed in later versions. Consider setting this to "-----".', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='diseaseprogression',
            name='disease_clinical_period',
            field=models.ForeignKey(to='ScenarioCreator.ProbabilityDensityFunction', help_text='Defines the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#clinically-infectious" class="wiki" target="_blank">clinical</a> period for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a>.', related_name='+', verbose_name='Clinical period'),
        ),
        migrations.AlterField(
            model_name='diseaseprogression',
            name='disease_immune_period',
            field=models.ForeignKey(to='ScenarioCreator.ProbabilityDensityFunction', help_text='Defines the natural <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#immune" class="wiki" target="_blank">immune</a> period for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a>.', related_name='+', verbose_name='Immune period'),
        ),
        migrations.AlterField(
            model_name='diseaseprogression',
            name='disease_latent_period',
            field=models.ForeignKey(to='ScenarioCreator.ProbabilityDensityFunction', help_text='Defines the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#latent-state" class="wiki" target="_blank">latent period</a> for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a>.', related_name='+', verbose_name='Latent period'),
        ),
        migrations.AlterField(
            model_name='diseaseprogression',
            name='disease_subclinical_period',
            field=models.ForeignKey(to='ScenarioCreator.ProbabilityDensityFunction', help_text='Defines the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#subclinically-infectious" class="wiki" target="_blank">Subclinical</a> period for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a>.', related_name='+', verbose_name='Subclinical period'),
        ),
        migrations.AlterField(
            model_name='indirectspread',
            name='distance_distribution',
            field=models.ForeignKey(to='ScenarioCreator.ProbabilityDensityFunction', help_text='Defines the shipment distances for <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#direct-contact" class="wiki" target="_blank">direct</a> or <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#indirect-contact" class="wiki" target="_blank">indirect contact</a> models.', related_name='+'),
        ),
        migrations.AlterField(
            model_name='indirectspread',
            name='transport_delay',
            field=models.ForeignKey(to='ScenarioCreator.ProbabilityDensityFunction', related_name='+', help_text='WARNING: THIS FIELD IS NOT RECOMMENDED BY ADSM and will be removed in later versions. Consider setting this to "-----".', blank=True, null=True),
        ),
    ]
