# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import ScenarioCreator.models


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0032_auto_20180702_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controlprotocol',
            name='destruction_ring_radius',
            field=ScenarioCreator.models.FloatField(default=0, null=True, blank=True, validators=[django.core.validators.MinValueValidator(0.0)], help_text='Radius in kilometers of the destruction ring.'),
        ),
    ]
