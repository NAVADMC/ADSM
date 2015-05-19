# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0005_controlmasterplan_vaccinate_retrospective_days'),
    ]

    operations = [
        migrations.CreateModel(
            name='DestructionWaitTime',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('days', models.PositiveIntegerField(help_text='Maximum number of days an infected premise should have to wait until destroyed.  The intention of this trigger is to initiate a vaccination program when destruction resources appear to be overwhelmed.')),
                ('trigger_group', models.ManyToManyField(to='ScenarioCreator.ProductionType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DiseaseDetection',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('number_of_units', models.PositiveIntegerField()),
                ('trigger_group', models.ManyToManyField(to='ScenarioCreator.ProductionType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DisseminationRate',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('ratio', models.FloatField(help_text='The threshold is specified by a number of days and a ratio, for example, "initiate a vaccination program if the number of units detected in the last 5 days is 1.5× or more than the number of units detected in the 5 days before that."')),
                ('days', models.PositiveIntegerField(help_text='Moving window size for calculating growth ratio.')),
                ('trigger_group', models.ManyToManyField(to='ScenarioCreator.ProductionType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductionGroup',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('group', models.ManyToManyField(to='ScenarioCreator.ProductionType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RateOfNewDetections',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('number_of_units', models.PositiveIntegerField(help_text='The threshold is specified by a number of units and a number of days, for example, "3 or more units detected within 5 days."')),
                ('days', models.PositiveIntegerField()),
                ('trigger_group', models.ManyToManyField(to='ScenarioCreator.ProductionType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SpreadBetweenGroups',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('number_of_groups', models.PositiveIntegerField(help_text='Specify in how many groups disease must be detected to trigger a vaccination program')),
                ('relevant_groups', models.ManyToManyField(to='ScenarioCreator.ProductionGroup')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TimeFromFirstDetection',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('days', models.PositiveIntegerField(help_text='The number of days to elapse since the first detection')),
                ('trigger_group', models.ManyToManyField(to='ScenarioCreator.ProductionType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
