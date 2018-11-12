# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0029_auto_20180702_1054'),
    ]

    operations = [
        migrations.CreateModel(
            name='DestructionGlobal',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('destruction_program_delay', models.PositiveIntegerField(help_text='The number of days that must pass after the first detection before a destruction program can begin.', null=True, blank=True)),
                ('destruction_priority_order', models.CharField(null=True, choices=[('reason, time waiting, production type', 'reason, time waiting, production type'), ('reason, production type, time waiting', 'reason, production type, time waiting'), ('time waiting, reason, production type', 'time waiting, reason, production type'), ('time waiting, production type, reason', 'time waiting, production type, reason'), ('production type, reason, time waiting', 'production type, reason, time waiting'), ('production type, time waiting, reason', 'production type, time waiting, reason')], max_length=255, help_text='The primary priority order for destruction.', default='reason, time waiting, production type', blank=True)),
                ('destruction_reason_order', models.CharField(help_text='The secondary priority level for destruction. All options shown, but only enabled options are used.', max_length=255, null=True, default='Basic, Trace fwd direct, Trace fwd indirect, Trace back direct, Trace back indirect, Ring', blank=True)),
                ('destruction_capacity', models.ForeignKey(null=True, help_text='The relational function used to define the daily destruction capacity.', to='ScenarioCreator.RelationalFunction', related_name='+', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
