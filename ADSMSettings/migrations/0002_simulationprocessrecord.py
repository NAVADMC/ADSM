# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ADSMSettings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimulationProcessRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('is_parser', models.BooleanField(default=True)),
                ('pid', models.IntegerField(default=0)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
