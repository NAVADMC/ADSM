# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0037_auto_20180719_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controlprotocol',
            name='minimum_time_between_vaccinations',
            field=models.PositiveIntegerField(null=True, default=99999, help_text='The minimum time in days between vaccination for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a>. Default value set to 99999 to stop duplicate vaccinations.', blank=True),
        ),
    ]
