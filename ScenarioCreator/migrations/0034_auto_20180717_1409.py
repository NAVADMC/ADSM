# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0033_auto_20180706_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destructionglobal',
            name='destruction_priority_order',
            field=models.CharField(help_text='The primary priority order for destruction.', max_length=255, default='{"Reason": ["Basic", "Trace fwd direct", "Trace fwd indirect", "Trace back direct", "Trace back indirect", "Ring"], "Days Holding": ["Oldest","Newest"], "Production Type": []}', choices=[('reason, time waiting, production type', 'reason, time waiting, production type'), ('reason, production type, time waiting', 'reason, production type, time waiting'), ('time waiting, reason, production type', 'time waiting, reason, production type'), ('time waiting, production type, reason', 'time waiting, production type, reason'), ('production type, reason, time waiting', 'production type, reason, time waiting'), ('production type, time waiting, reason', 'production type, time waiting, reason')]),
        ),
    ]
