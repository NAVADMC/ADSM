from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_hooks()
import re
from ScenarioCreator.models import ProductionType, Scenario, OutputSettings, Population, Unit, Disease, DiseaseProgression, \
    DiseaseProgressionAssignment, DirectSpread, ProductionTypePairTransmission, ControlMasterPlan, ControlProtocol, \
    ProtocolAssignment, Zone, ZoneEffectOnProductionType, ProbabilityFunction, RelationalFunction
from Results.models import DailyControls
from ScenarioCreator.views import unsaved_changes
from Settings.models import scenario_filename


def simulation_ready_to_run(context):
    relevant_keys = ['Scenario', 'OutputSetting', 'Population', 'ProductionTypes', 'Farms', 'Disease', 'Progressions', 'ProgressionAssignment','DirectSpreads',
                     'AssignSpreads',  'ControlMasterPlan', 'Protocols', 'ProtocolAssignments', 'Zones', 'ZoneEffects']
    status_lights = [value for key, value in context.items() if key in relevant_keys]
    return all(status_lights)  # All green status_lights  (It's a metaphor)


def basic_context(request):
    PT_count = ProductionType.objects.count()
    context = {'filename': scenario_filename(),
               'unsaved_changes': unsaved_changes(),
               'Scenario': Scenario.objects.count(),
               'OutputSetting': OutputSettings.objects.count(),
               'Population': Population.objects.count(),
               'ProductionTypes': PT_count,
               'Farms': Unit.objects.count(),
               'Disease': Disease.objects.count(),
               'Progressions': DiseaseProgression.objects.count(),
               'ProgressionAssignment': DiseaseProgressionAssignment.objects.count() == PT_count and PT_count, #Fixed false complete status when there are no Production Types
               'DirectSpreads': DirectSpread.objects.count(),
               'AssignSpreads': ProductionTypePairTransmission.objects.count() >= PT_count and PT_count, #Fixed false complete status when there are no Production Types
               'ControlMasterPlan': ControlMasterPlan.objects.count(),
               'Protocols': ControlProtocol.objects.count(),
               'ProtocolAssignments': ProtocolAssignment.objects.count(),
               'Zones': Zone.objects.count(),
               'ZoneEffects': ZoneEffectOnProductionType.objects.count(),
               'ProbabilityFunctions': ProbabilityFunction.objects.count(),
               'RelationalFunctions': RelationalFunction.objects.count(),
               'url': request.path,
               'active_link': re.split('\W+', request.path)[2],
               'controls_enabled': ControlMasterPlan.objects.filter(disable_all_controls=True).count() == 0,
               'outputs_computed': DailyControls.objects.all().count() > 0
               }

    context['Simulation_ready'] = simulation_ready_to_run(context)
    return context