import subprocess

from django.db.models import F, Count

from ScenarioCreator.models import ProductionType, Scenario, OutputSettings, Population, Unit, Disease, DiseaseProgression, \
    DiseaseProgressionAssignment, DirectSpread, DiseaseSpreadAssignment, ControlMasterPlan, ControlProtocol, \
    ProtocolAssignment, Zone, ZoneEffect, ProbabilityFunction, RelationalFunction, ZoneEffectAssignment, VaccinationTrigger, SpreadBetweenGroups, \
    DestructionWaitTime, TimeFromFirstDetection, DisseminationRate, RateOfNewDetections, DiseaseDetection, ProductionGroup, VaccinationRingRule

from ScenarioCreator.utils import whole_scenario_validation
from Results.models import outputs_exist
from git.git import git


def simulation_ready_to_run(context):
    status_lights = [ready for name, ready in context['missing_values'].items()]  # The value here is a tuple which includes the name see basic_context()
    return all(status_lights) and len(context['whole_scenario_warnings']) == 0  # All green status_lights  (It's a metaphor)


def js(var):
    if var:
        return 'true'
    else:
        return 'false'


def git_adsm_sha():
    try:
        version = subprocess.check_output(git + 'rev-parse HEAD', shell=True, stderr=subprocess.STDOUT).strip()[:7]
    except:
        version = 'no git'
    return version


def singular(name):
    if name[-1] == 's':
        return name[:-1]
    return name


def basic_context(request):
    context = {}
    
    if 'setup/' in request.path:  # inputs specific context
        pt_count = ProductionType.objects.count()

        context.update({
               'Scenario': Scenario.objects.count(),
               'OutputSetting': OutputSettings.objects.count(),
               'Population': Unit.objects.count(),
               'ProductionTypes': ProductionType.objects.all().annotate(unit_count=Count('unit')).values('name', 'unit_count', 'description'),
               'ProductionGroups': ProductionGroup.objects.all(),
               'Farms': Unit.objects.count(),
               'Disease': Disease.objects.all().exclude(name='').count(),
               'Progressions': DiseaseProgression.objects.count() 
                               and pt_count 
                               and DiseaseProgressionAssignment.objects.filter(progression__isnull=False).count() == pt_count,
               'DirectSpreads': DirectSpread.objects.count(),
               'AssignSpreads': pt_count and
                                DiseaseSpreadAssignment.objects.filter(
                                    source_production_type=F('destination_production_type'),
                                    direct_contact_spread__isnull=False
                                ).count() >= pt_count,
               'ControlMasterPlan': ControlMasterPlan.objects.count(),
               'VaccinationTrigger': any([m.objects.count() for m in 
                                          [DiseaseDetection,RateOfNewDetections,DisseminationRate,TimeFromFirstDetection,DestructionWaitTime,SpreadBetweenGroups]]),
               'VaccinationRingRule': VaccinationRingRule.objects.count(),
               'Protocols': ControlProtocol.objects.count(),
               'ProtocolAssignments': ProtocolAssignment.objects.count(),
               'Zones': Zone.objects.count(),
               'ZoneEffects': ZoneEffect.objects.count() 
                              and ZoneEffectAssignment.objects.filter(effect__isnull=False).count() >= Zone.objects.count() 
                              and Zone.objects.count(),
               'ProbabilityFunctions': ProbabilityFunction.objects.count(),
               'RelationalFunctions': RelationalFunction.objects.count(),
               'controls_enabled': ControlMasterPlan.objects.filter(disable_all_controls=True).count() == 0,
               'outputs_exist': outputs_exist(),
               'whole_scenario_warnings': whole_scenario_validation(),
               'dev_version': git_adsm_sha(),
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
                             'ControlMasterPlan': 'ControlMasterPlan/1/', 
                             'Protocols': 'ControlProtocol/', 
                             'ProtocolAssignments': 'AssignProtocols/', 
                             'Zones': 'Zone/', 
                             'ZoneEffects': 'AssignZoneEffects/'}
        context['missing_values'] = {singular(name): validation_models[name] for name in validation_models if not context[name]}
        context['Simulation_ready'] = simulation_ready_to_run(context)
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