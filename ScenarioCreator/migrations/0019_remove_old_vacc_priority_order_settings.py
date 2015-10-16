# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0018_move_vacc_priority_order_settings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='controlprotocol',
            name='vaccination_priority',
        ),
    ]
