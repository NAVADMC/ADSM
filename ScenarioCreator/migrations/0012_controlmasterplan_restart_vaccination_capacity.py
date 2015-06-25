# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0011_stopvaccination'),
    ]

    operations = [
        migrations.AddField(
            model_name='controlmasterplan',
            name='restart_vaccination_capacity',
            field=models.ForeignKey(to='ScenarioCreator.RelationalFunction', null=True, blank=True, help_text='Define if the daily vaccination capacity will be different if started a second time.', related_name='+'),
            preserve_default=True,
        ),
    ]
