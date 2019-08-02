# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0048_auto_20190603_0251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controlprotocol',
            name='vaccinate_detected_units',
            field=models.BooleanField(help_text='Indicates if detection in units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a> will be included in vaccination.', default=False),
        ),
    ]
