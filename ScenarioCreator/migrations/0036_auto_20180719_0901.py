# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0035_auto_20180719_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destructionglobal',
            name='destruction_reason_order',
            field=models.CharField(help_text='The secondary priority level for destruction. All options shown, but only enabled options are used.', default='Basic, Trace fwd direct, Trace fwd indirect, Trace back direct, Trace ack indirect, Ring', max_length=255),
        ),
    ]
