# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ADSMSettings', '0002_simulationprocessrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='smsession',
            name='simulation_has_started',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
