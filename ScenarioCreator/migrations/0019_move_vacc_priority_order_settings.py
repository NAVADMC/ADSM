# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations, OperationalError
import json
from collections import OrderedDict
import re



def move_to_new_vaccination_priority_order(apps, schema_editor):
    ControlMasterPlan = apps.get_model("ScenarioCreator", "ControlMasterPlan")
    ControlProtocol = apps.get_model("ScenarioCreator", "ControlProtocol")
    ProductionType = apps.get_model("ScenarioCreator", "ProductionType")

    try:
        # Get a list of production type names, in priority order.
        production_type_names = []
        for protocol in ControlProtocol.objects.order_by('vaccination_priority'):
            # A ControlProtocol can be linked to multiple ProductionTypes
            production_type_names += [assignment.production_type.name for assignment in protocol.protocolassignment_set.all()]
        # Any production types that were not linked to any ControlProtocol
        # object, add them to the end of the list, in alphabetical order.
        for production_type in ProductionType.objects.order_by('name'):
            if production_type.name not in production_type_names:
            	production_type_names.append(production_type.name)

        plan = ControlMasterPlan.objects.get()
        if (plan.vaccination_priority_order is None
            or plan.vaccination_priority_order == ''):
            # If vaccination_priority_order is null or blank, set it to the
            # default, but with the production type order found above.
            tmp = json.loads(ControlMasterPlan._meta.get_field('vaccination_priority_order').default, object_pairs_hook=OrderedDict)
            tmp['Production Type'] = production_type_names
            plan.vaccination_priority_order = json.dumps(tmp)
            plan.save()
        elif plan.vaccination_priority_order.startswith('{'):
            # If it's already in the new JSON format, leave it alone
            pass
        else:
            # Change from the old format.
            old_order = re.split(r'\s*,\s*', plan.vaccination_priority_order.strip().lower())
            tmp = OrderedDict()
            for criterion in old_order:
                if criterion == 'production type':
                    tmp['Production Type'] = production_type_names
                elif criterion == 'reason':
                    tmp['Reason'] = ['Ring']
                elif criterion == 'time waiting':
                    tmp['Days Holding'] = ['Oldest', 'Newest']
            tmp['Size'] = ['Largest', 'Smallest']
            tmp['Direction'] = ['Outside-in', 'Inside-out']
            plan.vaccination_priority_order = json.dumps(tmp)
            plan.save()
    except OperationalError:  #This data migration also gets run on settings.sqlite3 and it should just pass.
        pass
        
def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0018_remove_old_vacc_ring_settings'),
    ]

    operations = [
        migrations.RunPython(move_to_new_vaccination_priority_order, backwards)
    ]
