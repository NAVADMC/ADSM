# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Results', '0002_dailycontrols_vacctriggered'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailycontrols',
            name='averagePrevalence',
        ),
        migrations.RemoveField(
            model_name='dailycontrols',
            name='ratio',
        ),
    ]
