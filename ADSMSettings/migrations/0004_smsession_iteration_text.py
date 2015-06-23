# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ADSMSettings', '0003_smsession_simulation_has_started'),
    ]

    operations = [
        migrations.AddField(
            model_name='smsession',
            name='iteration_text',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
    ]
