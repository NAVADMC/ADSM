# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ADSMSettings', '0004_smsession_iteration_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='smsession',
            name='update_on_startup',
        ),
        migrations.AddField(
            model_name='smsession',
            name='simulation_version',
            field=models.CharField(default=None, null=True, blank=True, max_length=25, help_text='ADSM Simulation version.'),
        ),
        migrations.AlterField(
            model_name='smsession',
            name='update_available',
            field=models.CharField(default=None, null=True, blank=True, max_length=25, help_text='Is there are new version of ADSM available?'),
        ),
    ]
