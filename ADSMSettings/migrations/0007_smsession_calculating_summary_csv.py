# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ADSMSettings', '0006_smsession_show_help_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='smsession',
            name='calculating_summary_csv',
            field=models.BooleanField(default=False),
        ),
    ]
