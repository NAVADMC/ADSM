# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0024_remove_controlprotocol_vaccination_priority'),
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
    ]
