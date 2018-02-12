# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0023_add_remaining_missing_vaccination_fields_back'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='controlprotocol',
            name='vaccination_priority',
        ),
    ]
