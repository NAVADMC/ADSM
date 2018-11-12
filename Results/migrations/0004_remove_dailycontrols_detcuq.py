# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Results', '0003_remove_ratio_averagePrevalence'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailycontrols',
            name='detcUq',
        ),
    ]
