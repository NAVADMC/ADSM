# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations, OperationalError


def move_to_new_vaccination_ring_rules(apps, schema_editor):
    ControlProtocol = apps.get_model("ScenarioCreator", "ControlProtocol")
    ProductionType = apps.get_model("ScenarioCreator", "ProductionType")
    VaccinationRingRule = apps.get_model("ScenarioCreator", "VaccinationRingRule")

    try:
        # Create a dictionary where key=radius and value=set of
        # ProductionTypes that trigger a ring with that radius. This will tell
        # us how many VaccinationRingRule objects are needed.
        rings_needed = {}
        for protocol in ControlProtocol.objects.filter(trigger_vaccination_ring=True):
            radius = protocol.vaccination_ring_radius
            # A ControlProtocol can be linked to multiple ProductionTypes
            production_types = [assignment.production_type for assignment in protocol.protocolassignment_set.all()]
            try:
                rings_needed[radius].update(production_types)
            except KeyError:
                rings_needed[radius] = set(production_types)
        # end of loop over ControlProtocols that include triggering
        # vaccination.

        # Now get the set of ProductionTypes that get vaccinated.
        target_production_types = set()
        for protocol in ControlProtocol.objects.filter(use_vaccination=True):
            # A ControlProtocol can be linked to multiple ProductionTypes
            production_types = [assignment.production_type for assignment in protocol.protocolassignment_set.all()]
            target_production_types.update(production_types)
        # end of loop over ControlProtocols that include getting vaccinated.
        
        # Create the VaccinationRingRules
        for radius, trigger_production_types in rings_needed.items():
            rule = VaccinationRingRule(outer_radius=radius)
            rule.save()
            rule.trigger_group.add(*trigger_production_types)
            rule.target_group.add(*target_production_types)
        # end of loop to create rules
    except OperationalError:  #This data migration also gets run on settings.sqlite3 and it should just pass.
        pass
        
def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0015_VaccinationRingRule_and_OneToOneFields'),
    ]

    operations = [
        migrations.RunPython(move_to_new_vaccination_ring_rules, backwards)
    ]
