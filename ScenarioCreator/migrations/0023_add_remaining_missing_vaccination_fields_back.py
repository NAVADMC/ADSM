# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ScenarioCreator.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0022_add_use_vaccination_back'),
    ]

    operations = [
        migrations.AddField(
            model_name='controlprotocol',
            name='trigger_vaccination_ring',
            field=models.BooleanField(default=False, help_text='Indicates if detection of a unit of this type will trigger a vaccination ring.'),
        ),
        migrations.AddField(
            model_name='controlprotocol',
            name='vaccination_priority',
            field=models.PositiveIntegerField(default=5, blank=True, help_text='The vaccination priority of this production type relative to other production types.  A lower number indicates a higher priority.', null=True),
        ),
        migrations.AddField(
            model_name='controlprotocol',
            name='vaccination_ring_radius',
            field=ScenarioCreator.models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0.0)], blank=True, help_text='Radius in kilometers of the vaccination ring.'),
        ),
    ]
