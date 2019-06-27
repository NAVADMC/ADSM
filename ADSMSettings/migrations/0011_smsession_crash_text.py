# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ADSMSettings', '0010_smsession_simulation_crashed'),
    ]

    operations = [
        migrations.AddField(
            model_name='smsession',
            name='crash_text',
            field=models.TextField(blank=True, null=True, default=None),
        ),
    ]
