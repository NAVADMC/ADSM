# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def move_to_new_vaccination_triggers(apps, schema_editor):
    ControlMasterPlan = apps.get_model("ScenarioCreator", "ControlMasterPlan")
    DiseaseDetection = apps.get_model("ScenarioCreator", "DiseaseDetection")
    ProductionType = apps.get_model("ScenarioCreator", "ProductionType")

    if ControlMasterPlan.objects.count():
        number_of_units = ControlMasterPlan.objects.first().units_detected_before_triggering_vaccination
        if number_of_units is not None:
            n = DiseaseDetection.objects.create(number_of_units=number_of_units,)
            n.trigger_group.add(*ProductionType.objects.all())  # triggered on all production types 
            n.save()
        
def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0006_productiongroup_name'),
    ]

    operations = [
        migrations.RunPython(move_to_new_vaccination_triggers, backwards)
    ]
