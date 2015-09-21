# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ADSMSettings', '0005_auto_20150730_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='smsession',
            name='show_help_text',
            field=models.BooleanField(default=True),
        ),
    ]
