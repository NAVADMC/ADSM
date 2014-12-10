# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SmSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scenario_filename', models.CharField(blank=True, default='Untitled Scenario', max_length=255)),
                ('unsaved_changes', models.BooleanField(default=False)),
                ('update_available', models.BooleanField(help_text='Is there are new version of ADSM available?', default=False)),
                ('update_on_startup', models.BooleanField(help_text='The user has requested to install the update.', default=False)),
                ('population_upload_status', models.CharField(blank=True, null=True, default='', max_length=255)),
                ('population_upload_percent', models.FloatField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
