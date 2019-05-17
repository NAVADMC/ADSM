# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ADSMSettings', '0008_smsession_show_help_overlay'),
    ]

    operations = [
        migrations.AddField(
            model_name='smsession',
            name='combining_outputs',
            field=models.BooleanField(default=False),
        ),
    ]
