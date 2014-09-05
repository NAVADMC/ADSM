from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_hooks()
import re
from ScenarioCreator.models import ProductionType, Scenario, OutputSettings, Population, Unit, Disease, DiseaseProgression, \
    DiseaseProgressionAssignment, DirectSpread, ProductionTypePairTransmission, ControlMasterPlan, ControlProtocol, \
    ProtocolAssignment, Zone, ZoneEffect, ProbabilityFunction, RelationalFunction, ZoneEffectAssignment
from Results.models import DailyControls
from ScenarioCreator.views import unsaved_changes
from Settings.models import scenario_filename
from django.db.models import F


def simulation_ready_to_run(context):
    status_lights = [ready for name, ready in context['relevant_keys'].items()]  # The value here is a tuple which includes the name see basic_context()
    return all(status_lights)  # All green status_lights  (It's a metaphor)


def js(var):
    if var:
        return 'true'
    else:
        return 'false'

def basic_context(request):
    pt_count = ProductionType.objects.count()
    context = {'filename': scenario_filename(),
               'unsaved_changes': unsaved_changes(),
               'Scenario': Scenario.objects.count(),
               'OutputSetting': OutputSettings.objects.count(),
               'Population': Population.objects.count(),
               'ProductionTypes': pt_count,
               'Farms': Unit.objects.count(),
               'Disease': Disease.objects.count(),
               'Progressions': DiseaseProgression.objects.count(),
               'ProgressionAssignment': DiseaseProgressionAssignment.objects.count() == pt_count and pt_count,
               'DirectSpreads': DirectSpread.objects.count(),
               'AssignSpreads': pt_count and
                                ProductionTypePairTransmission.objects.filter(
                                    source_production_type=F('destination_production_type'),
                                    direct_contact_spread__isnull=False)
                                    .count() >= pt_count,
               'ControlMasterPlan': ControlMasterPlan.objects.count(),
               'Protocols': ControlProtocol.objects.count(),
               'ProtocolAssignments': ProtocolAssignment.objects.count(),
               'Zones': Zone.objects.count(),
               'ZoneEffects': ZoneEffect.objects.count(),
               'ZoneEffectAssignments': ZoneEffectAssignment.objects.count() >= Zone.objects.count() and Zone.objects.count(),
               'ProbabilityFunctions': ProbabilityFunction.objects.count(),
               'RelationalFunctions': RelationalFunction.objects.count(),
               'url': request.path,
               'active_link': '/'.join(re.split('\W+', request.path)[2:]),
               'controls_enabled': ControlMasterPlan.objects.filter(disable_all_controls=True).count() == 0,
               'outputs_computed': DailyControls.objects.all().count() > 0,
               }

    validation_models = ['Scenario', 'OutputSetting', 'Population', 'ProductionTypes', 'Farms', 'Disease', 'Progressions', 'ProgressionAssignment',
                         'DirectSpreads', 'AssignSpreads', 'ControlMasterPlan', 'Protocols', 'ProtocolAssignments', 'Zones', 'ZoneEffects',
                         'ZoneEffectAssignments']
    context['relevant_keys'] = {name: context[name] for name in validation_models}
    context['Simulation_ready'] = simulation_ready_to_run(context)
    disease = Disease.objects.get_or_create(pk=1)[0]
    context['javascript_variables'] = {'use_within_unit_prevalence':      js(disease.use_within_unit_prevalence),
                                       'use_airborne_exponential_decay':  js(disease.use_airborne_exponential_decay),
                                       'include_direct_contact_spread':   js(disease.include_direct_contact_spread),
                                       'include_indirect_contact_spread': js(disease.include_indirect_contact_spread),
                                       'include_airborne_spread':         js(disease.include_airborne_spread),
                                       }
    return context