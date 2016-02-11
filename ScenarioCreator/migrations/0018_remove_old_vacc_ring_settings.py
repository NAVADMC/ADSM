# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0017_move_vacc_ring_settings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='controlprotocol',
            name='trigger_vaccination_ring',
        ),
        migrations.RemoveField(
            model_name='controlprotocol',
            name='vaccination_ring_radius',
        ),
        migrations.RemoveField(
            model_name='controlprotocol',
            name='use_vaccination',
        ),
    ]
