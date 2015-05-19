# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations, OperationalError


def move_to_new_vaccination_triggers(apps, schema_editor):
    ControlMasterPlan = apps.get_model("ScenarioCreator", "ControlMasterPlan")
    DiseaseDetection = apps.get_model("ScenarioCreator", "DiseaseDetection")
    ProductionType = apps.get_model("ScenarioCreator", "ProductionType")

    try:
        if ControlMasterPlan.objects.count():
            cm = ControlMasterPlan.objects.get_or_create(id=1)[0]
            number_of_units = cm.units_detected_before_triggering_vaccination
            if number_of_units and number_of_units != 'units_detected_before_triggering_vaccination':  # somehow, the value of this gets set to the field name in tests...
                n = DiseaseDetection.objects.create(number_of_units=int(number_of_units),)
                n.trigger_group.add(*ProductionType.objects.all())  # triggered on all production types 
                n.save()
    except OperationalError:  #This data migration also gets run on settings.sqlite3 and it should just pass.
        pass
        
def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0007_productiongroup_name'),
    ]

    operations = [
        migrations.RunPython(move_to_new_vaccination_triggers, backwards)
    ]
