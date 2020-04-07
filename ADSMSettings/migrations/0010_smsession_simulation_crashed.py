# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ADSMSettings', '0009_smsession_combining_outputs'),
    ]

    operations = [
        migrations.AddField(
            model_name='smsession',
            name='simulation_crashed',
            field=models.BooleanField(default=False),
        ),
    ]
