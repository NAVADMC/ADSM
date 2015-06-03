# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0012_controlmasterplan_restart_vaccination_capacity'),
    ]

    operations = [
        migrations.AddField(
            model_name='destructionwaittime',
            name='restart_only',
            field=models.BooleanField(default=False, help_text='Allows you to setup less strict criteria for restarting a vaccination program after an outbreak.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='diseasedetection',
            name='restart_only',
            field=models.BooleanField(default=False, help_text='Allows you to setup less strict criteria for restarting a vaccination program after an outbreak.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='disseminationrate',
            name='restart_only',
            field=models.BooleanField(default=False, help_text='Allows you to setup less strict criteria for restarting a vaccination program after an outbreak.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rateofnewdetections',
            name='restart_only',
            field=models.BooleanField(default=False, help_text='Allows you to setup less strict criteria for restarting a vaccination program after an outbreak.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='spreadbetweengroups',
            name='restart_only',
            field=models.BooleanField(default=False, help_text='Allows you to setup less strict criteria for restarting a vaccination program after an outbreak.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stopvaccination',
            name='restart_only',
            field=models.BooleanField(default=False, help_text='Allows you to setup less strict criteria for restarting a vaccination program after an outbreak.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='timefromfirstdetection',
            name='restart_only',
            field=models.BooleanField(default=False, help_text='Allows you to setup less strict criteria for restarting a vaccination program after an outbreak.'),
            preserve_default=True,
        ),
    ]
