# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations, OperationalError
import json
from collections import OrderedDict
import re



def move_to_new_destruction_global(apps, schema_editor):
    ControlMasterPlan = apps.get_model("ScenarioCreator", "ControlMasterPlan")
    DestructionGlobal = apps.get_model("ScenarioCreator", "DestructionGlobal")

    try:
        control_master_plan = ControlMasterPlan.objects.get()

        try:
            destruction_global = DestructionGlobal.objects.get()
        except DestructionGlobal.DoesNotExist:
            destruction_global = DestructionGlobal()

        destruction_global.destruction_program_delay = control_master_plan.destruction_program_delay
        destruction_global.destruction_capacity = control_master_plan.destruction_capacity
        destruction_global.destruction_priority_order = control_master_plan.destruction_priority_order
        destruction_global.destruction_reason_order = control_master_plan.destruction_reason_order

        destruction_global.save()
    except OperationalError:  #This data migration also gets run on settings.sqlite3 and it should just pass.
        pass


def backwards(apps, schema_editor):
    ControlMasterPlan = apps.get_model("ScenarioCreator", "ControlMasterPlan")
    DestructionGlobal = apps.get_model("ScenarioCreator", "DestructionGlobal")

    try:
        control_master_plan = ControlMasterPlan.objects.get()
        destruction_global = DestructionGlobal.objects.get()

        control_master_plan.destruction_program_delay = destruction_global.destruction_program_delay
        control_master_plan.destruction_capacity = destruction_global.destruction_capacity
        control_master_plan.destruction_priority_order = destruction_global.destruction_priority_order
        control_master_plan.destruction_reason_order = destruction_global.destruction_reason_order

        control_master_plan.save()
        destruction_global.delete()
    except OperationalError:  # This data migration also gets run on settings.sqlite3 and it should just pass.
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0030_destructionglobal'),
    ]

    operations = [
        migrations.RunPython(move_to_new_destruction_global, backwards)
    ]
