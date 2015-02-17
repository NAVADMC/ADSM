# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0007_move_vacc_units_detected'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='controlmasterplan',
            name='units_detected_before_triggering_vaccination',
        ),
    ]
