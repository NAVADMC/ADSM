# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0014_VaccinationRingRule_and_OneToOneFields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controlmasterplan',
            name='vaccination_priority_order',
            field=models.TextField(help_text='The priority criteria for order of vaccinations.', default='{"Days Holding":["Oldest", "Newest"], "Production Type":["A", "C", "B"], "Reason":["Basic", "Trace fwd direct", "Trace fwd indirect", "Trace back direct", "Trace back indirect", "Ring"], "Direction":["Outside-in", "Inside-out"], "Size":["Largest", "Smallest"]}'),
        ),
    ]
