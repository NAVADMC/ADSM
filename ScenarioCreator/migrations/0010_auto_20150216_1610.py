# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ScenarioCreator.models


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0009_remove_controlmasterplan_units_detected_before_triggering_vaccination'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disseminationrate',
            name='ratio',
            field=ScenarioCreator.models.FloatField(help_text='The threshold is specified by a number of days and a ratio, for example, "initiate a vaccination program if the number of units detected in the last 5 days is 1.5× or more than the number of units detected in the 5 days before that."'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timefromfirstdetection',
            name='days',
            field=models.PositiveIntegerField(help_text='The number of days to elapsed since the first detection'),
            preserve_default=True,
        ),
    ]
