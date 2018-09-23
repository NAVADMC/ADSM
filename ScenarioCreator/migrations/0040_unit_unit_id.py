# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0039_auto_20180723_0856'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='unit_id',
            field=models.CharField(max_length=50, blank=True, null=True),
        ),
    ]
