# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0010_auto_20150216_1610'),
    ]

    operations = [
        migrations.CreateModel(
            name='StopVaccination',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('number_of_units', models.PositiveIntegerField(help_text='The threshold is specified by a number of units and a number of days. For example, "no more than 3 units detected within 5 days."')),
                ('days', models.PositiveIntegerField()),
                ('trigger_group', models.ManyToManyField(to='ScenarioCreator.ProductionType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
