# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import ScenarioCreator.models


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0044_auto_20190317_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airbornespread',
            name='max_distance',
            field=ScenarioCreator.models.FloatField(default=1.1, help_text='The maximum distance in KM of <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#airborne-transmission" class="wiki" target="_blank">airborne spread</a>.', validators=[django.core.validators.MinValueValidator(1.1)]),
        ),
    ]
