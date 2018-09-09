# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ADSMSettings', '0007_smsession_calculating_summary_csv'),
    ]

    operations = [
        migrations.AddField(
            model_name='smsession',
            name='show_help_overlay',
            field=models.BooleanField(default=True),
        ),
    ]
