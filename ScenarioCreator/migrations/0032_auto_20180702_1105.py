# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0031_move_destruction_global_settings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='controlmasterplan',
            name='destruction_capacity',
        ),
        migrations.RemoveField(
            model_name='controlmasterplan',
            name='destruction_priority_order',
        ),
        migrations.RemoveField(
            model_name='controlmasterplan',
            name='destruction_program_delay',
        ),
        migrations.RemoveField(
            model_name='controlmasterplan',
            name='destruction_reason_order',
        ),
        migrations.AlterField(
            model_name='destructionglobal',
            name='destruction_priority_order',
            field=models.CharField(choices=[('reason, time waiting, production type', 'reason, time waiting, production type'), ('reason, production type, time waiting', 'reason, production type, time waiting'), ('time waiting, reason, production type', 'time waiting, reason, production type'), ('time waiting, production type, reason', 'time waiting, production type, reason'), ('production type, reason, time waiting', 'production type, reason, time waiting'), ('production type, time waiting, reason', 'production type, time waiting, reason')], default='reason, time waiting, production type', help_text='The primary priority order for destruction.', max_length=255),
        ),
        migrations.AlterField(
            model_name='destructionglobal',
            name='destruction_reason_order',
            field=models.CharField(default='Basic, Trace fwd direct, Trace fwd indirect, Trace back direct, Trace back indirect, Ring', help_text='The secondary priority level for destruction. All options shown, but only enabled options are used.', max_length=255),
        ),
    ]
