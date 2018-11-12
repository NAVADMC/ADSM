# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0025_auto_20180226_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airbornespread',
            name='transport_delay',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='test_delay',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='trace_result_delay',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='controlprotocol',
            name='vaccine_immune_period',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='directspread',
            name='distance_distribution',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='directspread',
            name='transport_delay',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='diseaseprogression',
            name='disease_clinical_period',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='diseaseprogression',
            name='disease_immune_period',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='diseaseprogression',
            name='disease_latent_period',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='diseaseprogression',
            name='disease_subclinical_period',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='indirectspread',
            name='distance_distribution',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='indirectspread',
            name='transport_delay',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
