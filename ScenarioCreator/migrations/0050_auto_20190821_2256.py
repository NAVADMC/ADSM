# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0049_auto_20190802_0233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disease',
            name='use_airborne_exponential_decay',
            field=models.BooleanField(help_text='Indicates if the decrease in probability of disease spread by <a href="https://github.com/NAVADMC/ADSM/wiki/Model-Specification#airborne-spread" class="wiki" target="_blank">airborne transmission</a> is simulated by the exponential decay algorithm. Linear decay is the default setting algorithm for disease spread.', default=False),
        ),
    ]
