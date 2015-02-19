import subprocess
import re

from django.db.models import F

from ScenarioCreator.models import ProductionType, Scenario, OutputSettings, Population, Unit, Disease, DiseaseProgression, \
    DiseaseProgressionAssignment, DirectSpread, DiseaseSpreadAssignment, ControlMasterPlan, ControlProtocol, \
    ProtocolAssignment, Zone, ZoneEffect, ProbabilityFunction, RelationalFunction, ZoneEffectAssignment, VaccinationTrigger, SpreadBetweenGroups, \
    DestructionWaitTime, TimeFromFirstDetection, DisseminationRate, RateOfNewDetections, DiseaseDetection, ProductionGroup
from Results.models import DailyControls
from ADSMSettings.models import scenario_filename, SmSession
from ADSMSettings.views import unsaved_changes
from ADSMSettings.utils import graceful_startup, supplemental_folder_has_contents
from git.git import git


def simulation_ready_to_run(context):
    status_lights = [ready for name, ready in context['relevant_keys'].items()]  # The value here is a tuple which includes the name see basic_context()
    return all(status_lights)  # All green status_lights  (It's a metaphor)


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


def basic_context(request):
    context = {}
    
    if 'setup/' in request.path:  # inputs specific context
        pt_count = ProductionType.objects.count()

        context.update({
               'Scenario': Scenario.objects.count(),
               'OutputSetting': OutputSettings.objects.count(),
               'Population': Unit.objects.count(),
               'ProductionTypes': list(ProductionType.objects.all().values('name')),
               'ProductionGroups': list(ProductionGroup.objects.all().values('name')),
               'Farms': Unit.objects.count(),
               'Disease': Disease.objects.all().exclude(name='').count(),
               'Progressions': DiseaseProgression.objects.count(),
               'ProgressionAssignment': pt_count and DiseaseProgressionAssignment.objects.filter(progression__isnull=False).count() == pt_count,
               'DirectSpreads': DirectSpread.objects.count(),
               'AssignSpreads': pt_count and
                                DiseaseSpreadAssignment.objects.filter(
                                    source_production_type=F('destination_production_type'),
                                    direct_contact_spread__isnull=False
                                ).count() >= pt_count,
               'ControlMasterPlan': ControlMasterPlan.objects.count(),
               'VaccinationTrigger': any([m.objects.count() for m in 
                                          [DiseaseDetection,RateOfNewDetections,DisseminationRate,TimeFromFirstDetection,DestructionWaitTime,SpreadBetweenGroups]]),
               'Protocols': ControlProtocol.objects.count(),
               'ProtocolAssignments': ProtocolAssignment.objects.count(),
               'Zones': Zone.objects.count(),
               'ZoneEffects': ZoneEffect.objects.count(),
               'ZoneEffectAssignments': ZoneEffectAssignment.objects.count() >= Zone.objects.count() and Zone.objects.count(),
               'ProbabilityFunctions': ProbabilityFunction.objects.count(),
               'RelationalFunctions': RelationalFunction.objects.count(),
               'controls_enabled': ControlMasterPlan.objects.filter(disable_all_controls=True).count() == 0,
               'outputs_computed': DailyControls.objects.count() > 0,
               'supplemental_folder_has_contents': supplemental_folder_has_contents()
               })

        validation_models = ['Scenario', 'OutputSetting', 'Population', 'ProductionTypes', 'Farms', 'Disease', 'Progressions', 'ProgressionAssignment',
                             'DirectSpreads', 'AssignSpreads', 'ControlMasterPlan', 'Protocols', 'ProtocolAssignments', 'Zones', 'ZoneEffects',
                             'ZoneEffectAssignments']
        context['relevant_keys'] = {name: context[name] for name in validation_models}
        context['Simulation_ready'] = simulation_ready_to_run(context)
        disease = Disease.objects.get()
        context['javascript_variables'] = {'use_within_unit_prevalence':      js(disease.use_within_unit_prevalence),
                                           'use_airborne_exponential_decay':  js(disease.use_airborne_exponential_decay),
                                           'include_direct_contact_spread':   js(disease.include_direct_contact_spread),
                                           'include_indirect_contact_spread': js(disease.include_indirect_contact_spread),
                                           'include_airborne_spread':         js(disease.include_airborne_spread),
                                           'outputs_computed':                js(DailyControls.objects.count() > 0),
        }
        
        
    return context