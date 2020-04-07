# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0046_auto_20190516_1018'),
    ]

    operations = [
        migrations.RenameModel("ControlMasterPlan", "VaccinationGlobal"),
        migrations.AddField(
            model_name='VaccinationGlobal',
            name='control_plan',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
