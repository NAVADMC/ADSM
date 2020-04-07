from django.db.models import F, Count

from ScenarioCreator.models import ProductionType, Scenario, OutputSettings, Unit, Disease, DiseaseProgression, \
    DiseaseProgressionAssignment, DirectSpread, DiseaseSpreadAssignment, VaccinationGlobal, ControlProtocol, \
    ProtocolAssignment, Zone, ZoneEffect, ProbabilityDensityFunction, RelationalFunction, ZoneEffectAssignment, SpreadBetweenGroups, \
    DestructionWaitTime, TimeFromFirstDetection, DisseminationRate, RateOfNewDetections, DiseaseDetection, ProductionGroup, VaccinationRingRule, \
    DestructionGlobal
from Results.models import outputs_exist


def js(var):
    if var:
        return 'true'
    else:
        return 'false'


def singular(name):
    if name[-1] == 's':
        return name[:-1]
    return name


def basic_context(request):
    context = {'request': request}
    if request.path and request.path != '/' and '/LoadingScreen/' not in request.path:  # #635 this needs to run even in AJAX
        context['outputs_exist'] = outputs_exist()  # I don't want this triggering on LoadingScreen

    if not request.is_ajax() and 'setup/' in request.path:  # inputs specific context not filled from ajax requests
        pt_count = ProductionType.objects.count()

        context.update({
               'Scenario': Scenario.objects.count(),
               'OutputSetting': OutputSettings.objects.count(),
               'Population': Unit.objects.count(),
               'ProductionTypes': ProductionType.objects.all().annotate(unit_count=Count('unit')).values('name', 'unit_count', 'description'),
               'ProductionGroups': ProductionGroup.objects.all(),
               'Farms': Unit.objects.count(),
               'Disease': Disease.objects.all().exclude(name='').count(),
               'Progressions': DiseaseProgression.objects.count() and pt_count,
               'ProgressionAssignment': pt_count and DiseaseProgressionAssignment.objects.filter(progression__isnull=False).count() == pt_count,
               'DirectSpreads': DirectSpread.objects.count(),
               'AssignSpreads': pt_count and
                                DiseaseSpreadAssignment.objects.filter(  #completely empty assignments
                                    direct_contact_spread__isnull=True,
                                    indirect_contact_spread__isnull=True,
                                    airborne_spread__isnull=True
                                ).count() < pt_count ** 2,  # all possible assignments == pt_count^2
               'VaccinationGlobal': VaccinationGlobal.objects.count(),
               'VaccinationTrigger': any([m.objects.count() for m in 
                                          [DiseaseDetection,RateOfNewDetections,DisseminationRate,TimeFromFirstDetection,DestructionWaitTime,SpreadBetweenGroups]]),
               'VaccinationRingRule': VaccinationRingRule.objects.count(),
               'DestructionGlobal': DestructionGlobal.objects.get(id=0).validate(),
               'Protocols': ControlProtocol.objects.count(),
               'ProtocolAssignments': ProtocolAssignment.objects.count(),
               'Zones': Zone.objects.count(),
               'ZoneEffects': ZoneEffect.objects.count(),
               'ZoneEffectAssignments': ZoneEffectAssignment.objects.filter(effect__isnull=False).count() >= Zone.objects.count() and Zone.objects.count(),
               'ProbabilityDensityFunctions': ProbabilityDensityFunction.objects.count(),
               'RelationalFunctions': RelationalFunction.objects.count(),
               'controls_enabled': VaccinationGlobal.objects.filter(disable_all_controls=True).count() == 0,
               })

        validation_models = {'Scenario': 'Scenario/1/', 
                             'OutputSetting': 'OutputSetting/1/', 
                             'Population': 'Populations/', 
                             'ProductionTypes': 'ProductionType/', 
                             'Farms': 'Populations/', 
                             'Disease': 'Disease/1/', 
                             'Progressions': 'AssignProgressions/',
                             'DirectSpreads': 'DirectSpreads/', 
                             'AssignSpreads': 'AssignSpreads/', 
                             'VaccinationGlobal': 'VaccinationGlobal/1/',
                             'Protocols': 'ControlProtocol/', 
                             'ProtocolAssignments': 'AssignProtocols/', 
                             'Zones': 'Zone/', 
                             'ZoneEffects': 'ZoneEffect/',
                             'ZoneEffectAssignments': 'AssignZoneEffects/'}
        context['missing_values'] = {singular(name): validation_models[name] for name in validation_models if not context[name]}
        context['Simulation_ready'] = not len(context['missing_values'])
        disease = Disease.objects.get()
        context['javascript_variables'] = {'use_within_unit_prevalence':      js(disease.use_within_unit_prevalence),
                                           'use_airborne_exponential_decay':  js(disease.use_airborne_exponential_decay),
                                           'include_direct_contact_spread':   js(disease.include_direct_contact_spread),
                                           'include_indirect_contact_spread': js(disease.include_indirect_contact_spread),
                                           'include_airborne_spread':         js(disease.include_airborne_spread),
                                           'outputs_exist':                   js(outputs_exist()),
                                           'controls_enabled':                js(context['controls_enabled']),
                                           }
        
    return context
