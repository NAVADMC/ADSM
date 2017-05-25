# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0015_auto_20151204_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='initial_state',
            field=models.CharField(default='S', max_length=1, choices=[('S', 'Susceptible'), ('L', 'Latent'), ('B', 'Subclinical'), ('C', 'Clinical'), ('N', 'Naturally Immune'), ('V', 'Vaccine Immune'), ('D', 'Destroyed')], help_text='Code indicating the actual disease state of the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#unit" class="wiki" target="_blank">Unit</a> at the beginning of the simulation.'),
        ),
    ]
