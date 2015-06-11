# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import ScenarioCreator.models


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0013_restart_only_triggers'),
    ]

    operations = [
        migrations.CreateModel(
            name='VaccinationRingRule',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('outer_radius', ScenarioCreator.models.FloatField(help_text='Outer edge of Vaccination Ring in Kilometers', validators=[django.core.validators.MinValueValidator(0.001)])),
                ('inner_radius', ScenarioCreator.models.FloatField(blank=True, help_text='Inner edge of Vaccination Ring in Kilometers, used to make a doughnut shape (optional)', null=True, validators=[django.core.validators.MinValueValidator(0.001)])),
                ('target_group', models.ManyToManyField(to='ScenarioCreator.ProductionType', related_name='targeted_by_vaccination_ring')),
                ('trigger_group', models.ManyToManyField(to='ScenarioCreator.ProductionType', related_name='triggers_vaccination_ring')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='disease',
            name='use_airborne_exponential_decay',
            field=models.BooleanField(help_text='Indicates if the decrease in probability by <a href="https://github.com/NAVADMC/ADSM/wiki/Model-Specification#airborne-spread" class="wiki">airborne transmission</a> is simulated by the exponential (TRUE) or linear (FALSE) algorithm.', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='disease',
            name='use_within_unit_prevalence',
            field=models.BooleanField(help_text='Indicates if <a href="https://github.com/NAVADMC/ADSM/wiki/Model-Specification#prevalence" class="wiki">within unit prevalence</a> should be used in the model.', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='diseaseprogressionassignment',
            name='production_type',
            field=models.OneToOneField(help_text='The <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki">production type</a> that these outputs apply to.', to='ScenarioCreator.ProductionType'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='disseminationrate',
            name='ratio',
            field=ScenarioCreator.models.FloatField(help_text='The threshold is specified by a number of days and a ratio, for example, "initiate a vaccination program if the number of units detected in the last 5 days is 1.5x or more than the number of units detected in the 5 days before that."'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='protocolassignment',
            name='production_type',
            field=models.OneToOneField(help_text='The production type that these outputs apply to.', to='ScenarioCreator.ProductionType'),
            preserve_default=True,
        ),
    ]
