# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0003_auto_20150126_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='controlmasterplan',
            name='vaccinate_retrospective_days',
            field=models.PositiveIntegerField(null=True, help_text='Once a vaccination program starts, this number determines how many days previous to the start of the vaccination program a detection will trigger vaccination.', default=0, blank=True),
            preserve_default=True,
        ),
    ]
