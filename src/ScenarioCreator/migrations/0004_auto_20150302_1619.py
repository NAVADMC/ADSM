# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0003_auto_20150126_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='initial_state',
            field=models.CharField(default='S', help_text='Code indicating the actual disease state of the <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#unit" class="wiki">Unit</a> at the beginning of the simulation.', choices=[('S', 'Susceptible'), ('L', 'Latent'), ('B', 'Infectious Subclinical'), ('C', 'Infectious Clinical'), ('N', 'Naturally Immune'), ('V', 'Vaccine Immune'), ('D', 'Destroyed')], max_length=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='unit',
            name='user_notes',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
