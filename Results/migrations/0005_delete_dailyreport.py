# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Results', '0004_remove_dailycontrols_detcuq'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DailyReport',
        ),
    ]
