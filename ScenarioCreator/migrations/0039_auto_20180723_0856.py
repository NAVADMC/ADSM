# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0038_auto_20180720_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destructionglobal',
            name='destruction_priority_order',
            field=models.CharField(default='reason, time waiting, production type', choices=[('reason, time waiting, production type', 'reason, time waiting, production type'), ('reason, production type, time waiting', 'reason, production type, time waiting'), ('time waiting, reason, production type', 'time waiting, reason, production type'), ('time waiting, production type, reason', 'time waiting, production type, reason'), ('production type, reason, time waiting', 'production type, reason, time waiting'), ('production type, time waiting, reason', 'production type, time waiting, reason')], max_length=255, help_text='The primary priority order for destruction.'),
        ),
        migrations.AlterField(
            model_name='destructionglobal',
            name='destruction_reason_order',
            field=models.CharField(default='Basic, Trace fwd direct, Trace fwd indirect, Trace back direct, Trace back indirect, Ring', max_length=255, help_text='The secondary priority level for destruction. All options shown, but only enabled options are used.'),
        ),
    ]
