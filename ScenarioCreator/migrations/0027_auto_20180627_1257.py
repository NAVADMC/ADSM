# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0026_auto_20180627_1252'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProbabilityFunction',
            new_name='ProbabilityDensityFunction',
        ),
    ]
