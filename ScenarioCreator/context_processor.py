import re
from ScenarioCreator.models import ProductionType, Scenario, OutputSettings, Population, Unit, Disease, DiseaseProgression, \
    DiseaseProgressionAssignment, DirectSpread, ProductionTypePairTransmission, ControlMasterPlan, ControlProtocol, \
    ProtocolAssignment, Zone, ZoneEffectOnProductionType, ProbabilityFunction, RelationalFunction
from ScenarioCreator.views import scenario_filename, unsaved_changes


def simulation_ready_to_run(context):
    context = dict(context)
    # excluded statuses that shouldn't be blocking a simulation run
    for key in ['filename', 'unsaved_changes', 'IndirectSpreads', 'AirborneSpreads', 'ProbabilityFunctions', 'RelationalFunctions']:
        context.pop(key, None)
    return all(context.values())


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
               }
    context['Simulation'] = simulation_ready_to_run(context)
    return context