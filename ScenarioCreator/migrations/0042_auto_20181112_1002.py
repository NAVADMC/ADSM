# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0041_auto_20181105_1819'),
    ]

    operations = [
        migrations.RenameField(
            model_name='directspread',
            old_name='latent_animals_can_infect_others',
            new_name='latent_units_can_infect_others',
        ),
        migrations.RenameField(
            model_name='directspread',
            old_name='subclinical_animals_can_infect_others',
            new_name='subclinical_units_can_infect_others',
        ),
        migrations.RenameField(
            model_name='indirectspread',
            old_name='subclinical_animals_can_infect_others',
            new_name='subclinical_units_can_infect_others',
        ),
    ]
