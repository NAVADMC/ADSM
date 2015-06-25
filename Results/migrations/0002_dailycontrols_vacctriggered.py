# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Results', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailycontrols',
            name='vaccTriggered',
            field=models.IntegerField(null=True, blank=True, verbose_name='First Vaccination Trigger Activated'),
            preserve_default=True,
        ),
    ]
