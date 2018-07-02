# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0028_auto_20180627_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='probabilitydensityfunction',
            name='x_axis_units',
            field=models.CharField(default='Time Step Unit', max_length=255, help_text='The x-axis is the time step unit that corresponds to the time unit used for parameterizing the model.  For example, infectious diseases are commonly parameterized in a daily time step, so the x-axis would be “Days”.'),
        ),
        migrations.AlterField(
            model_name='relationalfunction',
            name='x_axis_units',
            field=models.CharField(default='Time Step Unit', max_length=255, help_text='The x-axis is the time step unit that corresponds to the time unit used for parameterizing the model.  For example, infectious diseases are commonly parameterized in a daily time step, so the x-axis would be “Days”.'),
        ),
    ]
