# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0034_auto_20180717_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destructionglobal',
            name='destruction_priority_order',
            field=models.CharField(max_length=255, default='{"Days Holding":["Oldest", "Newest"], "Production Type":[], "Size":["Largest", "Smallest"]}', help_text='The primary priority order for destruction.'),
        ),
        migrations.AlterField(
            model_name='destructionglobal',
            name='destruction_reason_order',
            field=models.CharField(max_length=255, default='Basic, Trace fwd direct, Trace fwd indirect, Trace back direct, Trace back indirect, Ring', help_text='The secondary priority level for destruction. All options shown, but grayed elements are not used.'),
        ),
    ]
