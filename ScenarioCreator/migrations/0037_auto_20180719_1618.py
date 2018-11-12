# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0036_auto_20180719_0901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controlprotocol',
            name='destruction_is_a_ring_target',
            field=models.BooleanField(default=False, help_text='Indicates if unit of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a> will be subject to preemptive ring destruction.', verbose_name='In the event of a trace, Destruction is a ring target'),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='destruction_is_a_ring_trigger',
            field=models.BooleanField(default=False, help_text='Indicates if detection of a unit of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a> will trigger the formation of a destruction ring.', verbose_name='Detection is a ring trigger'),
        ),
    ]
