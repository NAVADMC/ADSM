# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0040_unit_unit_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controlmasterplan',
            name='vaccinate_retrospective_days',
            field=models.PositiveIntegerField(help_text='Once a trigger has been activated, detected units prior to the trigger day can be retrospectively included in the vaccination strategy. This number defines how many days before the trigger to step back, and incorporate detected units.', blank=True, null=True, default=0),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='minimum_time_between_vaccinations',
            field=models.PositiveIntegerField(help_text='The minimum time in days between vaccination for units of this <a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#production-type" class="wiki" target="_blank">production type</a>. Default value set to 99999 to stop duplicate vaccinations.', default=99999),
        ),
    ]
